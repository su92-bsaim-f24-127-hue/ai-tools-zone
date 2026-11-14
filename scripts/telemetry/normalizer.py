"""AI Tools Zone — Telemetry Normalization & Local Storage Engine (Stage 4).

Normalizes Google Search Console and Google Analytics 4 telemetry outputs into a
consistent, validated, schema-compliant, immutable JSON archive.

Key Guarantees:
1. Strict Date Normalization (ISO 8601 YYYY-MM-DD and UTC timestamps).
2. Canonical URL Normalization (correlated against the 97 routes in data/seo-contract.json).
3. Metric Non-Conflation (GSC clicks and GA4 sessions are strictly separate; WhatsApp leads are never called sales).
4. Atomic, Immutable Archival under scratch/telemetry_archive/ with validation.
5. Complete Secret Redaction.
"""

import os
import re
import json
import uuid
import tempfile
import logging
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, List, Any, Optional, Tuple, Set

from .config import (
    ROOT_DIR,
    GSC_PROPERTY_ID,
    GA4_PROPERTY_RESOURCE,
    WEBSITE_ORIGIN,
    get_canonical_routes,
    get_expected_page_count,
)

logger = logging.getLogger("telemetry.normalizer")

# Schema & Storage Constants
SCHEMA_VERSION: str = "1.0.0"
DEFAULT_ARCHIVE_DIR: Path = ROOT_DIR / "scratch" / "telemetry_archive"

# Secret detection patterns for safety validation
SENSITIVE_PATTERNS = [
    re.compile(r"ya29\.[a-zA-Z0-9_\-]+"),
    re.compile(r"AIzaSy[a-zA-Z0-9_\-]+"),
    re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----"),
    re.compile(r"Bearer\s+[a-zA-Z0-9_\.\-]+"),
]


class NormalizationError(ValueError):
    """Raised when telemetry normalization or validation fails."""
    pass


class ImmutableArchiveError(FileExistsError):
    """Raised when an attempt is made to overwrite an immutable telemetry archive file."""
    pass


def get_git_commit_sha() -> Optional[str]:
    """Retrieve the current Git commit SHA safely if repository is accessible."""
    try:
        import subprocess
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(ROOT_DIR),
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8").strip()
    except Exception:
        return None


def normalize_date(date_val: Any) -> str:
    """Normalize a date string to ISO 8601 (YYYY-MM-DD).

    Supports:
    - YYYY-MM-DD (e.g. GSC '2026-10-28')
    - YYYYMMDD (e.g. GA4 '20261107')
    - ISO 8601 timestamp (e.g. '2026-11-09T19:00:43Z')
    """
    if not date_val:
        raise NormalizationError("Date value cannot be empty or None")

    s = str(date_val).strip()

    # Case 1: 8-digit GA4 format YYYYMMDD
    if len(s) == 8 and s.isdigit():
        try:
            dt = datetime.strptime(s, "%Y%m%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError as exc:
            raise NormalizationError(f"Invalid YYYYMMDD date: {s}") from exc

    # Case 2: Standard YYYY-MM-DD
    if len(s) == 10 and re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        try:
            dt = datetime.strptime(s, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError as exc:
            raise NormalizationError(f"Invalid YYYY-MM-DD date: {s}") from exc

    # Case 3: Full ISO timestamp
    if "T" in s:
        try:
            # Strip trailing Z or offset for date extraction
            clean_date = s.split("T")[0]
            dt = datetime.strptime(clean_date, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except Exception as exc:
            raise NormalizationError(f"Cannot extract valid date from timestamp: {s}") from exc

    raise NormalizationError(f"Unrecognized date format: {date_val}")


def validate_date_range(start_date: str, end_date: str) -> Tuple[str, str]:
    """Validate and normalize a reporting date range."""
    norm_start = normalize_date(start_date)
    norm_end = normalize_date(end_date)
    if norm_start > norm_end:
        raise NormalizationError(
            f"Invalid date range: start_date ({norm_start}) is after end_date ({norm_end})"
        )
    return norm_start, norm_end


def normalize_url_path(url_or_path: Any) -> str:
    """Normalize a full URL or relative route to a canonical path.

    Rules:
    - Drops origin (e.g. 'https://aitoolszone.tech/products/chatgpt-plus/' -> '/products/chatgpt-plus/').
    - Drops query strings and fragments.
    - Preserves '(not set)'.
    - Ensures leading slash.
    - Appends trailing slash to non-file paths.
    - Lowercases path for consistency.
    """
    if not url_or_path:
        return "(not set)"

    raw = str(url_or_path).strip()
    if raw in ("(not set)", "not set", "None", ""):
        return "(not set)"

    parsed = urlparse(raw)
    path = parsed.path if parsed.path else "/"

    # Lowercase path
    path = path.lower()

    if not path.startswith("/"):
        path = "/" + path

    # If it's not root, does not end with '/', and has no file extension (.html, .xml, etc.), append '/'
    if path != "/" and not path.endswith("/"):
        basename = path.rsplit("/", 1)[-1]
        if "." not in basename:
            path += "/"

    return path


def match_canonical_route(
    url_or_path: str, canonical_routes_set: Set[str]
) -> Tuple[str, bool]:
    """Match a URL or path against the authoritative 97 canonical public routes."""
    normalized = normalize_url_path(url_or_path)
    is_canonical = normalized in canonical_routes_set
    return normalized, is_canonical


EXPLICIT_INDEXED_COVERAGE_STATES: Set[str] = {
    "submitted and indexed",
    "indexed, not submitted in sitemap",
}

EXPLICIT_PENDING_COVERAGE_STATES: Set[str] = {
    "discovered – currently not indexed",
    "discovered - currently not indexed",
    "crawled - currently not indexed",
    "crawled – currently not indexed",
    "url is unknown to google",
}

EXPLICIT_ERROR_COVERAGE_STATES: Set[str] = {
    "blocked by robots.txt",
    "page with redirect",
    "not found (404)",
    "soft 404",
    "server error (5xx)",
    "duplicate without user-selected canonical",
    "duplicate, google chose different canonical than user",
}


def classify_route_indexation(inspection: Optional[Dict[str, Any]]) -> str:
    """Classify the Google Search Console indexation state of a route into mutually exclusive categories.

    Returned States:
    - 'INDEXED': Confirmed indexed by Google (PASS verdict with indexed coverage).
    - 'PENDING': Awaiting discovery or crawl evaluation (Discovered, Crawled-not-indexed, URL unknown).
    - 'ERROR': Technical crawl or indexing failure (FAIL verdict or error coverage).
    - 'API_ERROR': Inspection query encountered a transient API failure (429, 5xx, timeout).
    - 'NOT_INSPECTED': Route has not yet undergone URL inspection.

    Mutually Exclusive Guarantees:
    1. 'currently not indexed' is NEVER classified as 'INDEXED'.
    2. Any coverage state containing 'not indexed' immediately disqualifies the 'INDEXED' classification.
    3. Conflicting signals: Verdict 'FAIL' always overrides positive coverage to 'ERROR'.
    4. Handles case insensitivity, leading/trailing whitespace, and unexpected text safely.
    """
    if not inspection or not isinstance(inspection, dict):
        return "NOT_INSPECTED"

    verdict = str(inspection.get("verdict") or "").strip().upper()
    coverage = str(inspection.get("coverage_state") or "").strip().lower()

    if not verdict and not coverage:
        return "NOT_INSPECTED"

    if verdict == "NOT_INSPECTED" or coverage == "not inspected":
        return "NOT_INSPECTED"

    # API errors take precedence to prevent transient network issues from polluting SEO metrics
    if verdict == "API_ERROR" or "api_error" in coverage:
        return "API_ERROR"

    # Strict invariant: Any presence of "not indexed" precludes INDEXED
    has_not_indexed = "not indexed" in coverage

    # 1. Genuine INDEXED
    if verdict == "PASS" and not has_not_indexed:
        if coverage in EXPLICIT_ERROR_COVERAGE_STATES or "blocked" in coverage or "error" in coverage:
            return "ERROR"
        return "INDEXED"

    if coverage in EXPLICIT_INDEXED_COVERAGE_STATES and verdict != "FAIL":
        return "INDEXED"

    # 2. PENDING states (discovered, crawled-not-indexed, unknown to google)
    if has_not_indexed or "unknown to google" in coverage or coverage in EXPLICIT_PENDING_COVERAGE_STATES:
        if verdict == "FAIL":
            return "ERROR"
        return "PENDING"

    # 3. Technical ERROR / FAIL
    if verdict == "FAIL" or coverage in EXPLICIT_ERROR_COVERAGE_STATES or "error" in coverage or "blocked" in coverage:
        return "ERROR"

    # 4. Fallback for NEUTRAL or unmapped text
    if verdict == "NEUTRAL":
        return "PENDING"

    return "PENDING"


def scan_for_secrets(data: Any) -> None:
    """Recursively scan an object to guarantee no secrets exist before saving."""
    if isinstance(data, str):
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(data):
                raise NormalizationError(
                    f"Security violation: Secret or token pattern detected in payload ({pattern.pattern})"
                )
    elif isinstance(data, dict):
        for k, v in data.items():
            scan_for_secrets(k)
            scan_for_secrets(v)
    elif isinstance(data, (list, tuple, set)):
        for item in data:
            scan_for_secrets(item)


def normalize_telemetry(
    gsc_data: Optional[Dict[str, Any]] = None,
    ga4_data: Optional[Dict[str, Any]] = None,
    run_id: Optional[str] = None,
    commit_sha: Optional[str] = None,
    canonical_routes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Normalize, validate, and correlate GSC and GA4 collection datasets.

    Produces a validated, schema-compliant dictionary ready for immutable archival.
    """
    utc_now = datetime.now(timezone.utc)
    created_at_utc = utc_now.strftime("%Y-%m-%dT%H:%M:%SZ")
    active_run_id = run_id or f"tel_{utc_now.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    active_commit = commit_sha or get_git_commit_sha()

    routes = list(canonical_routes) if canonical_routes is not None else get_canonical_routes()
    routes_set = set(routes)
    expected_route_count = len(routes)

    validation_warnings: List[str] = []

    # Assess source availability
    has_gsc = gsc_data is not None and isinstance(gsc_data, dict)
    has_ga4 = ga4_data is not None and isinstance(ga4_data, dict)

    if not has_gsc and not has_ga4:
        raise NormalizationError("Cannot normalize telemetry: Both GSC and GA4 datasets are missing")

    # 1. Determine Reporting Date Range
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    if has_gsc and "site_totals" in gsc_data:
        gsc_dr = gsc_data["site_totals"].get("date_range", {})
        if gsc_dr.get("start_date") and gsc_dr.get("end_date"):
            start_date, end_date = validate_date_range(gsc_dr["start_date"], gsc_dr["end_date"])

    if has_ga4 and "organic_landing_performance" in ga4_data:
        ga4_dr = ga4_data["organic_landing_performance"].get("date_range", {})
        if ga4_dr.get("start_date") and ga4_dr.get("end_date"):
            try:
                ga4_s, ga4_e = validate_date_range(ga4_dr["start_date"], ga4_dr["end_date"])
                if start_date is None:
                    start_date, end_date = ga4_s, ga4_e
            except Exception as exc:
                validation_warnings.append(f"GA4 date range warning: {exc}")

    # Fallback date range if neither gave dates
    if start_date is None or end_date is None:
        start_date = utc_now.strftime("%Y-%m-%d")
        end_date = start_date
        validation_warnings.append("Reporting date range was not explicitly specified; defaulted to run date")

    # 2. Extract & Normalize GSC Data
    normalized_site_totals: Optional[Dict[str, Any]] = None
    gsc_pk_rows: List[Dict[str, Any]] = []
    gsc_inspections_map: Dict[str, Dict[str, Any]] = {}
    unmatched_gsc_urls: List[Dict[str, Any]] = []

    if has_gsc:
        # Site totals
        raw_totals = gsc_data.get("site_totals", {})
        if raw_totals:
            normalized_site_totals = {
                "clicks": int(raw_totals.get("clicks", 0)),
                "impressions": int(raw_totals.get("impressions", 0)),
                "ctr": float(raw_totals.get("ctr", 0.0)),
                "average_position": float(raw_totals.get("position", 0.0)),
                "is_empty": bool(raw_totals.get("is_empty", False)),
                "data_state": str(raw_totals.get("data_state", "final")),
            }
            # Metric sanity check
            if normalized_site_totals["clicks"] > normalized_site_totals["impressions"]:
                validation_warnings.append("GSC site totals anomaly: clicks exceed impressions")
            if not (0.0 <= normalized_site_totals["ctr"] <= 1.0):
                validation_warnings.append(f"GSC site totals anomaly: CTR outside [0, 1]: {normalized_site_totals['ctr']}")

        # URL inspection sweep
        raw_sweep = gsc_data.get("url_inspection_sweep", {})
        raw_inspections = raw_sweep.get("inspected_routes", []) if isinstance(raw_sweep, dict) else []
        for insp in raw_inspections:
            r_path, _ = match_canonical_route(insp.get("route") or insp.get("inspection_url", ""), routes_set)
            gsc_inspections_map[r_path] = {
                "verdict": insp.get("verdict", "VERDICT_UNSPECIFIED"),
                "coverage_state": insp.get("coverage_state"),
                "indexing_state": insp.get("indexing_state"),
                "robots_txt_state": insp.get("robots_txt_state"),
                "page_fetch_state": insp.get("page_fetch_state"),
                "last_crawl_time": insp.get("last_crawl_time"),
                "google_canonical": insp.get("google_canonical"),
                "user_canonical": insp.get("user_canonical"),
                "crawled_as": insp.get("crawled_as"),
                "referring_urls": insp.get("referring_urls", []),
                "rich_results_verdict": insp.get("rich_results_verdict"),
            }

        # Pakistan performance queries
        raw_pk = gsc_data.get("pakistan_performance", {})
        raw_pk_rows = raw_pk.get("rows", []) if isinstance(raw_pk, dict) else raw_pk.get("sample_rows", [])

        seen_gsc_keys: Set[Tuple[str, str, str, str]] = set()

        for r in raw_pk_rows:
            page_val = r.get("page", "")
            norm_path, is_canon = match_canonical_route(page_val, routes_set)
            query_val = str(r.get("query", ""))
            device_val = str(r.get("device", "DESKTOP")).upper()
            date_val = normalize_date(r.get("date", start_date))

            dedup_key = (norm_path, query_val, device_val, date_val)
            if dedup_key in seen_gsc_keys:
                validation_warnings.append(f"Duplicate GSC row detected and ignored for key: {dedup_key}")
                continue
            seen_gsc_keys.add(dedup_key)

            row_data = {
                "path": norm_path,
                "is_canonical": is_canon,
                "query": query_val,
                "device": device_val,
                "date": date_val,
                "clicks": int(r.get("clicks", 0)),
                "impressions": int(r.get("impressions", 0)),
                "ctr": float(r.get("ctr", 0.0)),
                "position": float(r.get("position", 0.0)),
            }

            if is_canon:
                gsc_pk_rows.append(row_data)
            else:
                unmatched_gsc_urls.append({
                    "original_url": page_val,
                    "normalized_path": norm_path,
                    "query": query_val,
                    "clicks": row_data["clicks"],
                    "impressions": row_data["impressions"],
                    "date": date_val,
                })

    # 3. Extract & Normalize GA4 Data
    ga4_organic_rows: List[Dict[str, Any]] = []
    ga4_whatsapp_rows: List[Dict[str, Any]] = []
    ga4_ai_rows: List[Dict[str, Any]] = []
    unmatched_ga4_paths: List[Dict[str, Any]] = []

    if has_ga4:
        # Organic performance
        raw_organic = ga4_data.get("organic_landing_performance", {})
        raw_org_rows = raw_organic.get("rows", []) if isinstance(raw_organic, dict) else []

        seen_ga4_org_keys: Set[Tuple[str, str, str]] = set()

        for r in raw_org_rows:
            lp = r.get("landing_page", "")
            norm_path, is_canon = match_canonical_route(lp, routes_set)
            device = str(r.get("device_category", "desktop")).lower()
            row_date = normalize_date(r.get("date", start_date))

            dedup_key = (norm_path, device, row_date)
            if dedup_key in seen_ga4_org_keys:
                validation_warnings.append(f"Duplicate GA4 organic row detected for key: {dedup_key}")
                continue
            seen_ga4_org_keys.add(dedup_key)

            row_data = {
                "landing_page": norm_path,
                "is_canonical": is_canon,
                "device_category": device,
                "date": row_date,
                "sessions": int(r.get("sessions", 0)),
                "total_users": int(r.get("total_users", 0)),
                "engaged_sessions": int(r.get("engaged_sessions", 0)),
                "engagement_rate": float(r.get("engagement_rate", 0.0)),
                "average_session_duration": float(r.get("average_session_duration", 0.0)),
            }

            if is_canon:
                ga4_organic_rows.append(row_data)
            else:
                unmatched_ga4_paths.append({
                    "original_landing_page": lp,
                    "normalized_path": norm_path,
                    "sessions": row_data["sessions"],
                    "total_users": row_data["total_users"],
                    "date": row_date,
                    "reason": "Not in 97 canonical public routes",
                })

        # WhatsApp commercial leads
        raw_leads = ga4_data.get("whatsapp_lead_performance", {})
        raw_lead_rows = raw_leads.get("rows", []) if isinstance(raw_leads, dict) else []
        for r in raw_lead_rows:
            lp = r.get("landing_page", "")
            norm_path, is_canon = match_canonical_route(lp, routes_set)
            ev_name = str(r.get("event_name", ""))
            row_date = normalize_date(r.get("date", start_date))

            row_data = {
                "event_name": ev_name,
                "landing_page": norm_path,
                "is_canonical": is_canon,
                "date": row_date,
                "event_count": int(r.get("event_count", 0)),
                "total_users": int(r.get("total_users", 0)),
            }
            if is_canon:
                ga4_whatsapp_rows.append(row_data)
            else:
                unmatched_ga4_paths.append({
                    "original_landing_page": lp,
                    "normalized_path": norm_path,
                    "event_name": ev_name,
                    "event_count": row_data["event_count"],
                    "date": row_date,
                    "reason": "WhatsApp event on non-canonical path",
                })

        # AI Assistant traffic
        raw_ai = ga4_data.get("ai_assistant_traffic", {})
        raw_ai_rows = raw_ai.get("rows", []) if isinstance(raw_ai, dict) else []
        for r in raw_ai_rows:
            lp = r.get("landing_page", "")
            norm_path, is_canon = match_canonical_route(lp, routes_set)
            row_date = normalize_date(r.get("date", start_date))

            row_data = {
                "platform": str(r.get("platform", "Other AI")),
                "session_source": str(r.get("session_source", "")),
                "session_medium": str(r.get("session_medium", "")),
                "landing_page": norm_path,
                "is_canonical": is_canon,
                "date": row_date,
                "sessions": int(r.get("sessions", 0)),
                "total_users": int(r.get("total_users", 0)),
                "engaged_sessions": int(r.get("engaged_sessions", 0)),
            }
            if is_canon:
                ga4_ai_rows.append(row_data)
            else:
                unmatched_ga4_paths.append({
                    "original_landing_page": lp,
                    "normalized_path": norm_path,
                    "sessions": row_data["sessions"],
                    "date": row_date,
                    "reason": "AI referral on non-canonical path",
                })

    # 4. Cross-Source Correlation Across 97 Canonical Public Routes
    correlated_routes: List[Dict[str, Any]] = []
    indexed_count = 0
    pending_count = 0
    not_inspected_count = 0
    error_count = 0
    api_error_count = 0

    for route in routes:
        # GSC Inspection state
        inspection_data = gsc_inspections_map.get(route)
        cat = classify_route_indexation(inspection_data)
        if cat == "INDEXED":
            indexed_count += 1
        elif cat == "PENDING":
            pending_count += 1
        elif cat == "NOT_INSPECTED":
            not_inspected_count += 1
        elif cat == "API_ERROR":
            api_error_count += 1
        elif cat == "ERROR":
            error_count += 1

        # GSC Query aggregate for this route
        route_gsc_rows = [r for r in gsc_pk_rows if r["path"] == route]
        route_gsc_clicks = sum(r["clicks"] for r in route_gsc_rows)
        route_gsc_impressions = sum(r["impressions"] for r in route_gsc_rows)
        route_gsc_ctr = (route_gsc_clicks / route_gsc_impressions) if route_gsc_impressions > 0 else 0.0

        if route_gsc_impressions > 0:
            weighted_pos = sum(r["position"] * r["impressions"] for r in route_gsc_rows) / route_gsc_impressions
        else:
            weighted_pos = None

        gsc_summary = {
            "has_data": len(route_gsc_rows) > 0,
            "clicks": route_gsc_clicks if len(route_gsc_rows) > 0 else None,
            "impressions": route_gsc_impressions if len(route_gsc_rows) > 0 else None,
            "ctr": round(route_gsc_ctr, 4) if len(route_gsc_rows) > 0 else None,
            "average_position": round(weighted_pos, 2) if weighted_pos is not None else None,
            "distinct_queries": len(set(r["query"] for r in route_gsc_rows)),
            "top_queries": sorted(
                [{"query": r["query"], "clicks": r["clicks"], "impressions": r["impressions"], "position": r["position"]} for r in route_gsc_rows],
                key=lambda x: (x["clicks"], x["impressions"]),
                reverse=True
            )[:5],
        }

        # GA4 Organic traffic aggregate for this route
        route_ga4_rows = [r for r in ga4_organic_rows if r["landing_page"] == route]
        route_ga4_sessions = sum(r["sessions"] for r in route_ga4_rows)
        route_ga4_users = sum(r["total_users"] for r in route_ga4_rows)
        route_ga4_engaged = sum(r["engaged_sessions"] for r in route_ga4_rows)

        if route_ga4_sessions > 0:
            weighted_eng_rate = sum(r["engagement_rate"] * r["sessions"] for r in route_ga4_rows) / route_ga4_sessions
            weighted_duration = sum(r["average_session_duration"] * r["sessions"] for r in route_ga4_rows) / route_ga4_sessions
        else:
            weighted_eng_rate = None
            weighted_duration = None

        ga4_summary = {
            "has_data": len(route_ga4_rows) > 0,
            "sessions": route_ga4_sessions if len(route_ga4_rows) > 0 else None,
            "total_users": route_ga4_users if len(route_ga4_rows) > 0 else None,
            "engaged_sessions": route_ga4_engaged if len(route_ga4_rows) > 0 else None,
            "engagement_rate": round(weighted_eng_rate, 4) if weighted_eng_rate is not None else None,
            "average_session_duration": round(weighted_duration, 2) if weighted_duration is not None else None,
        }

        # WhatsApp commercial lead events for this route
        route_lead_rows = [r for r in ga4_whatsapp_rows if r["landing_page"] == route]
        wa_clicks = sum(r["event_count"] for r in route_lead_rows if r["event_name"] == "whatsapp_click")
        prod_wa_clicks = sum(r["event_count"] for r in route_lead_rows if r["event_name"] == "product_whatsapp_click")
        gen_leads = sum(r["event_count"] for r in route_lead_rows if r["event_name"] == "generate_lead")
        lead_users = sum(r["total_users"] for r in route_lead_rows)

        whatsapp_summary = {
            "has_events": len(route_lead_rows) > 0,
            "total_lead_interactions": len(route_lead_rows) > 0 and (wa_clicks + prod_wa_clicks + gen_leads) or 0,
            "unique_prospective_users": len(route_lead_rows) > 0 and lead_users or 0,
            "event_breakdown": {
                "whatsapp_click": wa_clicks,
                "product_whatsapp_click": prod_wa_clicks,
                "generate_lead": gen_leads,
            },
        }

        # AI Assistant referral traffic for this route
        route_ai_rows = [r for r in ga4_ai_rows if r["landing_page"] == route]
        ai_sessions = sum(r["sessions"] for r in route_ai_rows)
        ai_users = sum(r["total_users"] for r in route_ai_rows)
        ai_platforms = sorted(list(set(r["platform"] for r in route_ai_rows)))

        ai_summary = {
            "has_referrals": len(route_ai_rows) > 0,
            "sessions": ai_sessions if len(route_ai_rows) > 0 else 0,
            "users": ai_users if len(route_ai_rows) > 0 else 0,
            "platforms": ai_platforms,
        }

        correlated_routes.append({
            "canonical_route": route,
            "is_canonical": True,
            "inspection": inspection_data,
            "gsc_performance": gsc_summary,
            "ga4_performance": ga4_summary,
            "whatsapp_leads": whatsapp_summary,
            "ai_referrals": ai_summary,
        })

    # 5. Determine Overall Collection Status
    if has_gsc and has_ga4:
        # Check if both succeeded with content
        gsc_empty = normalized_site_totals is None or normalized_site_totals.get("is_empty", False)
        ga4_empty = len(ga4_organic_rows) == 0 and len(ga4_whatsapp_rows) == 0 and len(ga4_ai_rows) == 0
        if gsc_empty and ga4_empty:
            collection_status = "empty"
        else:
            collection_status = "success"
    elif has_gsc or has_ga4:
        collection_status = "partial"
    else:
        collection_status = "failure"

    # 6. Global Rollup Summary
    unique_gsc_queries = len(set(r["query"] for r in gsc_pk_rows))
    total_ga4_sessions = sum(r["sessions"] for r in ga4_organic_rows)
    total_ga4_users = sum(r["total_users"] for r in ga4_organic_rows)
    total_whatsapp_events = sum(r["event_count"] for r in ga4_whatsapp_rows)
    total_whatsapp_users = sum(r["total_users"] for r in ga4_whatsapp_rows)
    total_ai_sessions = sum(r["sessions"] for r in ga4_ai_rows)

    summary_block = {
        "canonical_route_count": expected_route_count,
        "canonical_indexed_count": indexed_count,
        "canonical_pending_count": pending_count,
        "canonical_not_inspected_count": not_inspected_count,
        "canonical_error_count": error_count,
        "canonical_api_error_count": api_error_count,
        "gsc_site_totals": normalized_site_totals,
        "gsc_pakistan_queries_count": unique_gsc_queries,
        "ga4_organic_sessions": total_ga4_sessions,
        "ga4_organic_users": total_ga4_users,
        "whatsapp_interaction_events": total_whatsapp_events,
        "whatsapp_unique_users": total_whatsapp_users,
        "ai_assistant_sessions": total_ai_sessions,
    }

    # 7. Assembled Payload
    snapshot_payload: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "run_id": active_run_id,
        "created_at_utc": created_at_utc,
        "collection_status": collection_status,
        "reporting_date_range": {
            "start_date": start_date,
            "end_date": end_date,
        },
        "source_metadata": {
            "gsc_property": GSC_PROPERTY_ID,
            "ga4_property": GA4_PROPERTY_RESOURCE,
            "origin": WEBSITE_ORIGIN,
            "commit_sha": active_commit,
        },
        "summary": summary_block,
        "correlated_routes": correlated_routes,
        "unmatched_records": {
            "gsc_urls": unmatched_gsc_urls,
            "ga4_landing_pages": unmatched_ga4_paths,
        },
        "data_quality": {
            "completeness": {
                "gsc_available": has_gsc,
                "ga4_available": has_ga4,
                "url_inspections_available": len(gsc_inspections_map) > 0,
            },
            "validation_warnings": validation_warnings,
        },
        "attribution_notes": {
            "non_conflation_rule": "GSC clicks represent SERP departures; GA4 sessions represent executed browser page loads. They are never summed.",
            "whatsapp_conversions": "WhatsApp events reflect click-to-chat triggers, not completed sales or guaranteed payments.",
            "ai_referrals": "AI referrals without standard HTTP Referer headers typically fall into Direct / (none).",
        },
    }

    # Verify no credentials or tokens exist
    scan_for_secrets(snapshot_payload)

    return snapshot_payload


def validate_normalized_payload(payload: Dict[str, Any], expected_routes_count: Optional[int] = None) -> None:
    """Validate that a normalized payload adheres strictly to required schema rules."""
    required_keys = [
        "schema_version",
        "run_id",
        "created_at_utc",
        "collection_status",
        "reporting_date_range",
        "source_metadata",
        "summary",
        "correlated_routes",
        "unmatched_records",
        "data_quality",
    ]
    for k in required_keys:
        if k not in payload:
            raise NormalizationError(f"Schema validation failed: Missing required top-level key '{k}'")

    if payload["schema_version"] != SCHEMA_VERSION:
        raise NormalizationError(
            f"Schema version mismatch: expected '{SCHEMA_VERSION}', got '{payload['schema_version']}'"
        )

    if payload["collection_status"] not in ("success", "partial", "empty", "failure"):
        raise NormalizationError(
            f"Invalid collection_status: '{payload['collection_status']}'"
        )

    # Validate route count: use explicitly passed expected count, snapshot recorded count, or live contract
    routes = payload.get("correlated_routes", [])
    expected = expected_routes_count or payload.get("summary", {}).get("canonical_route_count") or get_expected_page_count()
    if len(routes) != expected:
        raise NormalizationError(
            f"Correlated routes count mismatch: found {len(routes)}, expected {expected}"
        )

    # Scan for secret leaks
    scan_for_secrets(payload)


def save_telemetry_snapshot(
    payload: Dict[str, Any],
    archive_dir: Optional[Path] = None,
    filename: Optional[str] = None,
) -> Path:
    """Save a normalized telemetry snapshot atomically and immutably.

    Guarantees:
    - Never overwrites an existing snapshot file (raises ImmutableArchiveError).
    - Writes to temporary file before atomic replace.
    - Validates payload before writing.
    - Directory created safely.
    """
    dest_dir = archive_dir or DEFAULT_ARCHIVE_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)

    validate_normalized_payload(payload)

    run_id = payload.get("run_id", "unknown_run")
    clean_time = payload.get("created_at_utc", "").replace(":", "").replace("-", "")
    target_filename = filename or f"run_{clean_time}_{run_id}.json"
    target_path = dest_dir / target_filename

    # Immutability Check: Refuse overwrite
    if target_path.exists():
        raise ImmutableArchiveError(
            f"Immutable archive violation: Snapshot file already exists at {target_path}"
        )

    # Atomic write pattern: Write to temp file in dest directory, sync, then replace
    temp_fd, temp_path_str = tempfile.mkstemp(
        prefix="tmp_telemetry_",
        suffix=".json",
        dir=str(dest_dir),
    )
    temp_path = Path(temp_path_str)

    try:
        with open(temp_fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())

        # Check immutability once more right before atomic rename
        if target_path.exists():
            raise ImmutableArchiveError(
                f"Immutable archive violation: Target file was created concurrently at {target_path}"
            )

        # Atomic rename
        os.replace(str(temp_path), str(target_path))
        logger.info("Successfully archived immutable telemetry snapshot: %s", target_path)
        return target_path

    except Exception:
        # Clean up temporary file on any error
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
        raise
