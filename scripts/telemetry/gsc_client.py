"""AI Tools Zone — Google Search Console Data Collection Engine (Stage 2).

Reliable, read-only Search Console telemetry collector providing:
1. Authoritative site totals (dimensionless query, final data state).
2. Pakistan search performance (country == 'pak' filter, pagination).
3. 97-route URL inspection sweep with rate-limiting (<= 5 req/sec) and exponential backoff retry.

Adheres strictly to zero-leak credential isolation and read-only least privilege.
"""

import time
import socket
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Callable
from urllib.error import HTTPError

from googleapiclient.errors import HttpError

# Guard against infinite TCP socket hangs on remote Google API endpoints
DEFAULT_SOCKET_TIMEOUT: float = 30.0
socket.setdefaulttimeout(DEFAULT_SOCKET_TIMEOUT)

from .auth import get_gsc_service, mask_identifier
from .config import (
    GSC_PROPERTY_ID,
    WEBSITE_ORIGIN,
    get_canonical_routes,
    get_expected_page_count,
)

logger = logging.getLogger("telemetry.gsc")


class RateLimiter:
    """Enforces a maximum request rate (requests per second) across API calls."""

    def __init__(self, max_rps: float = 5.0):
        if max_rps <= 0:
            raise ValueError("max_rps must be greater than 0")
        self.min_interval: float = 1.0 / max_rps
        self.last_call_time: float = 0.0

    def acquire(self) -> float:
        """Sleep if necessary to respect the maximum rate limit. Returns elapsed sleep time."""
        now = time.time()
        elapsed = now - self.last_call_time
        sleep_time = self.min_interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
            self.last_call_time = time.time()
            return sleep_time
        self.last_call_time = now
        return 0.0


def _safe_error_message(exc: Exception) -> str:
    """Redact potentially sensitive details from error messages."""
    msg = str(exc)
    for sensitive_keyword in ["Bearer", "ya29.", "AIza", "key="]:
        if sensitive_keyword in msg:
            return f"{type(exc).__name__}: [REDACTED_CREDENTIAL]"
    return f"{type(exc).__name__}: {msg}"


def _is_transient_error(exc: Exception) -> bool:
    """Determine whether an exception qualifies for transient retry."""
    if isinstance(exc, HttpError):
        # 429: Too Many Requests; 500, 502, 503, 504: Server-side transient errors
        return exc.resp.status in (429, 500, 502, 503, 504)
    if isinstance(exc, (HTTPError, OSError, TimeoutError, socket.timeout)):
        return True
    return False


def _execute_with_retry(
    operation: Callable[[], Any],
    max_retries: int = 3,
    initial_backoff: float = 1.0,
    backoff_factor: float = 2.0,
) -> Any:
    """Execute a callable with exponential backoff on transient errors."""
    delay = initial_backoff
    last_exc = None

    for attempt in range(1, max_retries + 1):
        try:
            return operation()
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries and _is_transient_error(exc):
                logger.warning(
                    "Transient error on attempt %d/%d: %s. Retrying in %.2fs...",
                    attempt,
                    max_retries,
                    _safe_error_message(exc),
                    delay,
                )
                time.sleep(delay)
                delay *= backoff_factor
            else:
                raise last_exc
    raise last_exc


def get_site_totals(
    start_date: str,
    end_date: str,
    site_url: str = GSC_PROPERTY_ID,
    service: Optional[Any] = None,
    data_state: str = "final",
) -> Dict[str, Any]:
    """Retrieve authoritative dimensionless Google Search Console site totals.

    Rule: Never adds dimensions ('query', 'page', etc.) to this query. Summing
    query-filtered rows causes 15-40% undercounting due to Google's anonymization
    thresholds. A dimensionless query returns true site-wide totals.
    """
    gsc = service or get_gsc_service()

    body: Dict[str, Any] = {
        "startDate": start_date,
        "endDate": end_date,
        "dataState": data_state,
        "type": "web",
    }

    resp = _execute_with_retry(
        lambda: gsc.searchanalytics().query(siteUrl=site_url, body=body).execute()
    )

    collected_at = datetime.now(timezone.utc).isoformat()
    rows = resp.get("rows", [])

    if not rows:
        return {
            "clicks": 0,
            "impressions": 0,
            "ctr": 0.0,
            "position": 0.0,
            "is_empty": True,
            "date_range": {"start_date": start_date, "end_date": end_date},
            "data_state": data_state,
            "response_aggregation_type": resp.get("responseAggregationType", "byProperty"),
            "property": site_url,
            "collected_at": collected_at,
        }

    first_row = rows[0]
    return {
        "clicks": int(first_row.get("clicks", 0)),
        "impressions": int(first_row.get("impressions", 0)),
        "ctr": float(first_row.get("ctr", 0.0)),
        "position": float(first_row.get("position", 0.0)),
        "is_empty": False,
        "date_range": {"start_date": start_date, "end_date": end_date},
        "data_state": data_state,
        "response_aggregation_type": resp.get("responseAggregationType", "byProperty"),
        "property": site_url,
        "collected_at": collected_at,
    }


def get_pakistan_performance(
    start_date: str,
    end_date: str,
    site_url: str = GSC_PROPERTY_ID,
    service: Optional[Any] = None,
    dimensions: Optional[List[str]] = None,
    row_limit: int = 5000,
    max_rows: Optional[int] = None,
    data_state: str = "final",
) -> Dict[str, Any]:
    """Collect Pakistan domestic search performance with query and page breakdown.

    Applies country filter 'pak' (ISO 3166-1 alpha-3 lowercase).
    Handles pagination using startRow and rowLimit to prevent silent truncation.
    """
    gsc = service or get_gsc_service()
    dims = dimensions or ["page", "query", "device", "date"]

    batch_size = min(row_limit, 25000)
    all_rows: List[Dict[str, Any]] = []
    start_row = 0
    collected_at = datetime.now(timezone.utc).isoformat()

    while True:
        body: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
            "dataState": data_state,
            "type": "web",
            "dimensions": dims,
            "dimensionFilterGroups": [
                {
                    "filters": [
                        {
                            "dimension": "country",
                            "operator": "equals",
                            "expression": "pak",
                        }
                    ]
                }
            ],
            "startRow": start_row,
            "rowLimit": batch_size,
        }

        resp = _execute_with_retry(
            lambda: gsc.searchanalytics().query(siteUrl=site_url, body=body).execute()
        )

        rows = resp.get("rows", [])
        if not rows:
            break

        for r in rows:
            keys = r.get("keys", [])
            row_dict: Dict[str, Any] = {
                "clicks": int(r.get("clicks", 0)),
                "impressions": int(r.get("impressions", 0)),
                "ctr": float(r.get("ctr", 0.0)),
                "position": float(r.get("position", 0.0)),
            }
            # Map keys dynamically to requested dimensions
            for i, dim_name in enumerate(dims):
                row_dict[dim_name] = keys[i] if i < len(keys) else None

            all_rows.append(row_dict)

        if len(rows) < batch_size:
            # Reached end of available rows
            break

        start_row += len(rows)
        if max_rows and len(all_rows) >= max_rows:
            all_rows = all_rows[:max_rows]
            break

    return {
        "total_rows": len(all_rows),
        "rows": all_rows,
        "date_range": {"start_date": start_date, "end_date": end_date},
        "country_filter": "pak",
        "dimensions": dims,
        "data_state": data_state,
        "property": site_url,
        "collected_at": collected_at,
    }


def inspect_canonical_routes(
    site_url: str = GSC_PROPERTY_ID,
    service: Optional[Any] = None,
    routes: Optional[List[str]] = None,
    max_rps: float = 5.0,
    max_retries: int = 3,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
) -> Dict[str, Any]:
    """Inspect canonical public routes via Google URL Inspection API.

    Guarantees:
    - Never duplicates routes; loads authoritative list from data/seo-contract.json if routes is None.
    - Paces requests to <= 5 req/sec (via RateLimiter).
    - Retries transient errors (429, 5xx) with exponential backoff.
    - Records failed inspections separately without aborting the sweep.
    - Never claims a route is indexed or de-indexed on API failure.
    """
    gsc = service or get_gsc_service()
    target_routes = list(routes) if routes is not None else get_canonical_routes()
    expected_count = len(target_routes) if routes is not None else get_expected_page_count()

    limiter = RateLimiter(max_rps=max_rps)
    inspected_results: List[Dict[str, Any]] = []
    failed_inspections: List[Dict[str, Any]] = []
    start_time = time.time()
    collected_at = datetime.now(timezone.utc).isoformat()

    for idx, route in enumerate(target_routes, start=1):
        full_url = f"{WEBSITE_ORIGIN}{route}"

        if progress_callback:
            progress_callback(idx, len(routes), full_url)

        # Enforce rate limiting
        limiter.acquire()

        body = {
            "inspectionUrl": full_url,
            "siteUrl": site_url,
            "languageCode": "en-PK",
        }

        try:
            resp = _execute_with_retry(
                lambda: gsc.urlInspection().index().inspect(body=body).execute(),
                max_retries=max_retries,
            )

            inspection_result = resp.get("inspectionResult", {})
            index_status = inspection_result.get("indexStatusResult", {})
            rich_results = inspection_result.get("richResultsResult", {})

            inspected_results.append({
                "route": route,
                "inspection_url": full_url,
                "verdict": index_status.get("verdict", "VERDICT_UNSPECIFIED"),
                "coverage_state": index_status.get("coverageState"),
                "indexing_state": index_status.get("indexingState"),
                "robots_txt_state": index_status.get("robotsTxtState"),
                "page_fetch_state": index_status.get("pageFetchState"),
                "last_crawl_time": index_status.get("lastCrawlTime"),
                "google_canonical": index_status.get("googleCanonical"),
                "user_canonical": index_status.get("userCanonical"),
                "crawled_as": index_status.get("crawledAs"),
                "referring_urls": index_status.get("referringUrls", []),
                "rich_results_verdict": rich_results.get("verdict"),
                "inspection_result_link": inspection_result.get("inspectionResultLink"),
            })

        except Exception as exc:
            logger.error(
                "Permanent inspection failure for %s: %s",
                full_url,
                _safe_error_message(exc),
            )
            failed_inspections.append({
                "route": route,
                "inspection_url": full_url,
                "error_type": type(exc).__name__,
                "error_message": _safe_error_message(exc),
                "retries_attempted": max_retries,
            })

    duration_seconds = time.time() - start_time

    return {
        "property": site_url,
        "collected_at": collected_at,
        "duration_seconds": round(duration_seconds, 2),
        "total_expected": expected_count,
        "total_attempted": len(target_routes),
        "total_successful": len(inspected_results),
        "total_failed": len(failed_inspections),
        "success_rate": round(len(inspected_results) / len(target_routes), 4) if target_routes else 0.0,
        "inspected_routes": inspected_results,
        "failed_inspections": failed_inspections,
    }
