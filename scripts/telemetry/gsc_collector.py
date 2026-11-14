"""AI Tools Zone — Google Search Console Data Collector & 97-Route Inspection Sweep.

Executes:
1. Complete URL Inspection sweep across all 97 canonical public routes (concurrent pool with 5 workers).
2. Pakistan-filtered Search Analytics queries (site-wide, page-level, query-level, device).
3. Commercial pages and educational guides performance categorization.
"""

import sys
import os
import json
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from .config import (
        WEBSITE_ORIGIN,
        GSC_PROPERTY_ID,
        GSC_READONLY_SCOPE,
        get_canonical_routes,
        get_expected_page_count,
    )
    from .auth import get_adc_credentials, get_gsc_service
except ImportError:
    from config import (
        WEBSITE_ORIGIN,
        GSC_PROPERTY_ID,
        GSC_READONLY_SCOPE,
        get_canonical_routes,
        get_expected_page_count,
    )
    from auth import get_adc_credentials, get_gsc_service

from google.auth.transport.requests import AuthorizedSession

logger = logging.getLogger("telemetry.gsc_collector")


def inspect_single_route(session: AuthorizedSession, route: str, idx: int, total: int) -> Dict[str, Any]:
    """Inspect a single route via URL Inspection API with robust retry logic."""
    full_url = f"{WEBSITE_ORIGIN}{route}"
    req_body = {
        "inspectionUrl": full_url,
        "siteUrl": GSC_PROPERTY_ID,
        "languageCode": "en-PK"
    }

    entry: Dict[str, Any] = {
        "index": idx,
        "route": route,
        "full_url": full_url,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    inspect_endpoint = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

    for attempt in range(2):
        t0 = time.time()
        try:
            resp = session.post(inspect_endpoint, json=req_body, timeout=30)
            elapsed = time.time() - t0

            if resp.status_code == 200:
                res = resp.json()
                inspection = res.get("inspectionResult", {})
                index_status = inspection.get("indexStatusResult", {})
                rich_results = inspection.get("richResultsResult", {})

                entry["success"] = True
                entry["verdict"] = index_status.get("verdict", "UNKNOWN")
                entry["coverage_state"] = index_status.get("coverageState", "UNKNOWN")
                entry["robots_txt_state"] = index_status.get("robotsTxtState", "UNKNOWN")
                entry["indexing_state"] = index_status.get("indexingState", "UNKNOWN")
                entry["page_fetch_state"] = index_status.get("pageFetchState", "UNKNOWN")
                entry["user_canonical"] = index_status.get("userCanonical", "")
                entry["google_canonical"] = index_status.get("googleCanonical", "")
                entry["last_crawl_time"] = index_status.get("lastCrawlTime", "")
                entry["crawled_as"] = index_status.get("crawledAs", "")

                detected_rich = rich_results.get("detectedItems", [])
                entry["rich_result_types"] = [
                    item.get("richResultType") for item in detected_rich if item.get("richResultType")
                ]
                entry["rich_verdict"] = rich_results.get("verdict", "UNKNOWN")
                entry["latency_sec"] = round(elapsed, 2)
                return entry
            else:
                if attempt == 0:
                    time.sleep(2.0)
                else:
                    entry["success"] = False
                    entry["http_status"] = resp.status_code
                    entry["verdict"] = "FAIL"
                    entry["coverage_state"] = f"HTTP_{resp.status_code}: {resp.text[:100]}"
                    entry["latency_sec"] = round(elapsed, 2)
                    return entry
        except Exception as exc:
            if attempt == 0:
                time.sleep(2.0)
            else:
                entry["success"] = False
                entry["verdict"] = "ERROR"
                entry["coverage_state"] = f"EXCEPTION: {type(exc).__name__}"
                entry["latency_sec"] = round(time.time() - t0, 2)
                return entry

    return entry


def run_url_inspection_sweep(max_workers: int = 5) -> List[Dict[str, Any]]:
    """Inspect all 97 canonical public routes concurrently via URL Inspection API."""
    routes = get_canonical_routes()
    expected_count = get_expected_page_count()
    if len(routes) != expected_count:
        raise ValueError(f"Route count mismatch: expected {expected_count}, got {len(routes)}")

    creds = get_adc_credentials(scopes=[GSC_READONLY_SCOPE])
    session = AuthorizedSession(creds)

    print(f"Starting URL Inspection sweep for all {len(routes)} canonical routes (workers={max_workers})...", flush=True)
    sweep_start = time.time()

    results_dict: Dict[int, Dict[str, Any]] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_route = {
            pool.submit(inspect_single_route, session, route, idx, len(routes)): (idx, route)
            for idx, route in enumerate(routes, start=1)
        }

        completed_count = 0
        for future in as_completed(future_to_route):
            idx, route = future_to_route[future]
            completed_count += 1
            try:
                entry = future.result()
            except Exception as exc:
                entry = {
                    "index": idx,
                    "route": route,
                    "full_url": f"{WEBSITE_ORIGIN}{route}",
                    "success": False,
                    "verdict": "ERROR",
                    "coverage_state": str(exc),
                }

            results_dict[idx] = entry
            verdict = entry.get("verdict", "N/A")
            cov = entry.get("coverage_state", "N/A")
            lat = entry.get("latency_sec", 0)
            print(f"[{completed_count:02d}/{len(routes)}] ({idx:02d}) {route} -> {verdict} ({cov}) [{lat}s]", flush=True)

    # Sort results in canonical index order
    ordered_results = [results_dict[i] for i in sorted(results_dict.keys())]

    sweep_duration = time.time() - sweep_start
    print(f"\nCompleted URL Inspection sweep of {len(routes)} routes in {sweep_duration:.2f}s ({sweep_duration/len(routes):.2f}s/route average)\n", flush=True)
    return ordered_results


def collect_search_analytics(
    start_date: str = "2026-10-15",
    end_date: str = "2026-11-11"
) -> Dict[str, Any]:
    """Query Search Analytics API with Pakistan geographic isolation."""
    gsc = get_gsc_service()
    analytics_data: Dict[str, Any] = {
        "date_range": {"start_date": start_date, "end_date": end_date},
        "query_timestamp": datetime.now(timezone.utc).isoformat(),
    }

    print(f"Collecting Search Analytics for {start_date} to {end_date}...", flush=True)

    # 1. Global Site-wide Totals (Dimensionless)
    try:
        global_totals_req = {
            "startDate": start_date,
            "endDate": end_date,
            "dataState": "final",
            "type": "web"
        }
        res_global = gsc.searchanalytics().query(siteUrl=GSC_PROPERTY_ID, body=global_totals_req).execute()
        rows_global = res_global.get("rows", [])
        if rows_global:
            r = rows_global[0]
            analytics_data["global_totals"] = {
                "clicks": r.get("clicks", 0),
                "impressions": r.get("impressions", 0),
                "ctr": round(r.get("ctr", 0.0), 4),
                "position": round(r.get("position", 0.0), 2),
                "totals_complete": True
            }
        else:
            analytics_data["global_totals"] = {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0, "totals_complete": True}
        print(f"Global Totals: Clicks={analytics_data['global_totals']['clicks']}, Impressions={analytics_data['global_totals']['impressions']}", flush=True)
    except Exception as exc:
        analytics_data["global_totals"] = {"error": str(exc), "totals_complete": False}

    # 2. Pakistan Site-wide Totals
    try:
        pak_totals_req = {
            "startDate": start_date,
            "endDate": end_date,
            "dataState": "final",
            "type": "web",
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "country",
                    "operator": "equals",
                    "expression": "pak"
                }]
            }]
        }
        res_pak = gsc.searchanalytics().query(siteUrl=GSC_PROPERTY_ID, body=pak_totals_req).execute()
        rows_pak = res_pak.get("rows", [])
        if rows_pak:
            r = rows_pak[0]
            analytics_data["pakistan_totals"] = {
                "clicks": r.get("clicks", 0),
                "impressions": r.get("impressions", 0),
                "ctr": round(r.get("ctr", 0.0), 4),
                "position": round(r.get("position", 0.0), 2),
                "totals_complete": True
            }
        else:
            analytics_data["pakistan_totals"] = {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0, "totals_complete": True}
        print(f"Pakistan Totals: Clicks={analytics_data['pakistan_totals']['clicks']}, Impressions={analytics_data['pakistan_totals']['impressions']}, CTR={analytics_data['pakistan_totals']['ctr']:.4f}, Pos={analytics_data['pakistan_totals']['position']:.1f}", flush=True)
    except Exception as exc:
        analytics_data["pakistan_totals"] = {"error": str(exc), "totals_complete": False}

    # 3. Pakistan Page-level Performance
    try:
        pak_pages_req = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["page"],
            "dataState": "final",
            "type": "web",
            "rowLimit": 1000,
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "country",
                    "operator": "equals",
                    "expression": "pak"
                }]
            }]
        }
        res_pages = gsc.searchanalytics().query(siteUrl=GSC_PROPERTY_ID, body=pak_pages_req).execute()
        analytics_data["pakistan_pages"] = res_pages.get("rows", [])
        print(f"Pakistan Page Rows: {len(analytics_data['pakistan_pages'])} pages with impressions", flush=True)
    except Exception as exc:
        analytics_data["pakistan_pages"] = []
        analytics_data["pakistan_pages_error"] = str(exc)

    # 4. Pakistan Query-level Performance
    try:
        pak_queries_req = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["query"],
            "dataState": "final",
            "type": "web",
            "rowLimit": 1000,
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "country",
                    "operator": "equals",
                    "expression": "pak"
                }]
            }]
        }
        res_queries = gsc.searchanalytics().query(siteUrl=GSC_PROPERTY_ID, body=pak_queries_req).execute()
        analytics_data["pakistan_queries"] = res_queries.get("rows", [])
        print(f"Pakistan Query Rows: {len(analytics_data['pakistan_queries'])} unique queries", flush=True)
    except Exception as exc:
        analytics_data["pakistan_queries"] = []
        analytics_data["pakistan_queries_error"] = str(exc)

    # 5. Pakistan Page + Query
    try:
        pak_page_query_req = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["page", "query"],
            "dataState": "final",
            "type": "web",
            "rowLimit": 1000,
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "country",
                    "operator": "equals",
                    "expression": "pak"
                }]
            }]
        }
        res_pq = gsc.searchanalytics().query(siteUrl=GSC_PROPERTY_ID, body=pak_page_query_req).execute()
        analytics_data["pakistan_page_queries"] = res_pq.get("rows", [])
        print(f"Pakistan Page+Query Combinations: {len(analytics_data['pakistan_page_queries'])} rows", flush=True)
    except Exception as exc:
        analytics_data["pakistan_page_queries"] = []
        analytics_data["pakistan_page_queries_error"] = str(exc)

    # 6. Pakistan Device Breakdown
    try:
        pak_devices_req = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["device"],
            "dataState": "final",
            "type": "web",
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "country",
                    "operator": "equals",
                    "expression": "pak"
                }]
            }]
        }
        res_devices = gsc.searchanalytics().query(siteUrl=GSC_PROPERTY_ID, body=pak_devices_req).execute()
        analytics_data["pakistan_devices"] = res_devices.get("rows", [])
    except Exception as exc:
        analytics_data["pakistan_devices"] = []
        analytics_data["pakistan_devices_error"] = str(exc)

    # 7. Pakistan Date Breakdown
    try:
        pak_dates_req = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["date"],
            "dataState": "final",
            "type": "web",
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "country",
                    "operator": "equals",
                    "expression": "pak"
                }]
            }]
        }
        res_dates = gsc.searchanalytics().query(siteUrl=GSC_PROPERTY_ID, body=pak_dates_req).execute()
        analytics_data["pakistan_dates"] = res_dates.get("rows", [])
    except Exception as exc:
        analytics_data["pakistan_dates"] = []
        analytics_data["pakistan_dates_error"] = str(exc)

    return analytics_data


def main():
    print("=" * 70, flush=True)
    print("AI Tools Zone — Phase 5.5D Search Console Data Collection", flush=True)
    print("=" * 70, flush=True)

    sweep_results = run_url_inspection_sweep(max_workers=5)
    analytics_results = collect_search_analytics(start_date="2026-10-15", end_date="2026-11-11")

    # Combine into unified dataset
    combined_payload = {
        "metadata": {
            "collection_timestamp": datetime.now(timezone.utc).isoformat(),
            "target_property": GSC_PROPERTY_ID,
            "target_website": WEBSITE_ORIGIN,
            "total_routes_inspected": len(sweep_results),
            "expected_routes": get_expected_page_count(),
        },
        "url_inspection_sweep": sweep_results,
        "search_analytics": analytics_results,
    }

    # Save to scratch directory
    scratch_dir = Path(__file__).resolve().parent.parent.parent / "scratch"
    scratch_dir.mkdir(exist_ok=True)
    out_file = scratch_dir / "phase_5_5d_gsc_telemetry_dump.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(combined_payload, f, indent=2)

    print("\n" + "=" * 70, flush=True)
    print(f"Data Collection Completed! Payload saved to: {out_file}", flush=True)
    print("=" * 70, flush=True)


if __name__ == "__main__":
    main()
