"""AI Tools Zone — Unified SEO Telemetry Pipeline Runner.

Orchestrates the complete SEO telemetry workflow for local scheduled runs and GitHub Actions:
1. Authenticates securely via Application Default Credentials (ADC) or WIF.
2. Collects Google Search Console totals, Pakistan queries, and route inspections.
3. Collects Google Analytics 4 organic traffic, WhatsApp leads, and AI referrals.
4. Normalizes and correlates data against the 98-route canonical contract.
5. Emits an immutable JSON archive snapshot under scratch/telemetry_archive/.
6. Generates the Weekly SEO Performance Report (Markdown) and Route Matrix (CSV).
7. Evaluates multi-tier SEO alerts (P0, P1, P2) and system health.
8. Enforces strict secret scanning and output completeness validation.
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from typing import Dict, Any, Optional, List, Tuple

# Internal telemetry module imports
from .config import (
    ROOT_DIR,
    GSC_PROPERTY_ID,
    GA4_PROPERTY_RESOURCE,
    get_canonical_routes,
    get_expected_page_count,
)
from .auth import verify_connectivity
from .gsc_client import (
    get_site_totals,
    get_pakistan_performance,
    inspect_canonical_routes,
)
from .ga4_client import (
    get_organic_landing_page_performance,
    get_whatsapp_lead_performance,
    get_ai_assistant_traffic,
)
from .normalizer import (
    normalize_telemetry,
    save_telemetry_snapshot,
    scan_for_secrets,
    DEFAULT_ARCHIVE_DIR,
)
from .report_generator import (
    generate_weekly_seo_performance_markdown,
    generate_indexation_matrix_rows,
    save_weekly_report,
    save_indexation_matrix_csv,
    load_snapshot,
    DEFAULT_REPORTS_DIR,
)
from .evaluate_alerts import (
    evaluate_alerts,
    generate_alerts_markdown,
    save_alerts_report,
)

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("telemetry.pipeline")


def calculate_reporting_window(days: int = 7) -> Tuple[str, str]:
    """Calculate the trailing reporting date range.

    Defaults to a 7-day window ending 3 days prior to today,
    guaranteeing finalized (dataState: final) Search Console data.
    """
    today = date.today()
    end_date = today - timedelta(days=3)
    start_date = end_date - timedelta(days=days - 1)
    return start_date.isoformat(), end_date.isoformat()


def find_latest_prior_snapshot(
    archive_dir: Path,
    exclude_path: Optional[Path] = None,
) -> Optional[Path]:
    """Locate the most recent historical snapshot prior to the current run."""
    if not archive_dir.exists():
        return None
    snapshots = sorted(
        [p for p in archive_dir.glob("run_*.json") if p != exclude_path],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return snapshots[0] if snapshots else None


def execute_pipeline(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    days: int = 7,
    skip_inspection: bool = False,
    snapshot_path: Optional[str] = None,
    output_dir: Optional[Path] = None,
    archive_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Execute the end-to-end telemetry pipeline.

    Returns:
        Dict[str, Any]: Execution summary, output file paths, and health status.
    """
    reports_dir = Path(output_dir) if output_dir else DEFAULT_REPORTS_DIR
    archives_dir = Path(archive_dir) if archive_dir else DEFAULT_ARCHIVE_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)
    archives_dir.mkdir(parents=True, exist_ok=True)

    summary: Dict[str, Any] = {
        "status": "pending",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "stages": {},
    }

    # Case A: Execute from pre-existing snapshot (Offline / Testing mode)
    if snapshot_path:
        logger.info("Executing pipeline from pre-existing snapshot: %s", snapshot_path)
        active_snapshot_path = Path(snapshot_path)
        payload = load_snapshot(active_snapshot_path)
        prev_snapshot_path = find_latest_prior_snapshot(archives_dir, exclude_path=active_snapshot_path)
        prev_payload = load_snapshot(prev_snapshot_path) if prev_snapshot_path else None
        summary["stages"]["source"] = {"mode": "snapshot", "path": str(active_snapshot_path)}

    # Case B: Execute live collection via Google APIs
    else:
        # Determine dates
        if not start_date or not end_date:
            start_date, end_date = calculate_reporting_window(days=days)
        logger.info("Reporting period: %s to %s (%d days)", start_date, end_date, days)

        # Stage 1: Auth check
        logger.info("Stage 1: Verifying Google Cloud API connectivity...")
        auth_outcome = verify_connectivity()
        if auth_outcome.get("status") != "success":
            logger.error("Authentication connectivity failed: %s", auth_outcome)
            raise RuntimeError(f"Authentication verification failed: {auth_outcome}")
        summary["stages"]["auth"] = "success"

        # Stage 2: GSC Collection
        logger.info("Stage 2: Collecting Google Search Console telemetry...")
        gsc_totals = get_site_totals(start_date=start_date, end_date=end_date)
        gsc_pk = get_pakistan_performance(start_date=start_date, end_date=end_date)

        if skip_inspection:
            logger.info("Skipping live URL inspection sweep; reusing latest available inspection data.")
            prev_snap = find_latest_prior_snapshot(archives_dir)
            if prev_snap:
                prev_data = load_snapshot(prev_snap)
                gsc_sweep = {"inspected_routes": [
                    {"route": r["canonical_route"], **r.get("inspection", {})}
                    for r in prev_data.get("correlated_routes", [])
                ]}
            else:
                gsc_sweep = {"inspected_routes": []}
        else:
            logger.info("Executing URL inspection sweep across canonical inventory...")
            gsc_sweep = inspect_canonical_routes()

        gsc_data = {
            "site_totals": gsc_totals,
            "pakistan_performance": gsc_pk,
            "url_inspection_sweep": gsc_sweep,
        }
        summary["stages"]["gsc_collection"] = {
            "clicks": gsc_totals.get("clicks", 0),
            "impressions": gsc_totals.get("impressions", 0),
            "inspected_routes": len(gsc_sweep.get("inspected_routes", [])),
        }

        # Stage 3: GA4 Collection
        logger.info("Stage 3: Collecting Google Analytics 4 telemetry...")
        ga4_organic = get_organic_landing_page_performance(start_date=start_date, end_date=end_date)
        ga4_whatsapp = get_whatsapp_lead_performance(start_date=start_date, end_date=end_date)
        ga4_ai = get_ai_assistant_traffic(start_date=start_date, end_date=end_date)

        ga4_data = {
            "organic_landing_performance": ga4_organic,
            "whatsapp_leads": ga4_whatsapp,
            "ai_referral_traffic": ga4_ai,
        }
        summary["stages"]["ga4_collection"] = {
            "organic_rows": len(ga4_organic.get("rows", [])),
            "whatsapp_events": ga4_whatsapp.get("total_events", 0),
            "ai_sessions": ga4_ai.get("total_sessions", 0),
        }

        # Stage 4: Normalization & Archival
        logger.info("Stage 4: Normalizing telemetry datasets...")
        payload = normalize_telemetry(
            gsc_data=gsc_data,
            ga4_data=ga4_data,
            canonical_routes=get_canonical_routes(),
        )
        saved_archive_path = save_telemetry_snapshot(payload, archive_dir=archives_dir)
        logger.info("Saved normalized archive: %s", saved_archive_path)

        prev_snapshot_path = find_latest_prior_snapshot(archives_dir, exclude_path=saved_archive_path)
        prev_payload = load_snapshot(prev_snapshot_path) if prev_snapshot_path else None
        summary["stages"]["normalization"] = {
            "archive_path": str(saved_archive_path),
            "canonical_routes": len(payload.get("correlated_routes", [])),
            "indexed_count": payload.get("summary", {}).get("canonical_indexed_count", 0),
            "pending_count": payload.get("summary", {}).get("canonical_pending_count", 0),
        }

    # Stage 5: Report Generation
    logger.info("Stage 5: Generating weekly SEO performance reports...")
    utc_ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    # Generate Markdown report
    weekly_md = generate_weekly_seo_performance_markdown(payload, prev_payload)
    scan_for_secrets(weekly_md)
    ts_weekly = reports_dir / f"weekly_seo_performance_{utc_ts}.md"
    save_weekly_report(weekly_md, ts_weekly, overwrite=False)

    root_weekly = reports_dir / "weekly_seo_performance.md"
    save_weekly_report(weekly_md, root_weekly, overwrite=True)

    # Generate CSV matrix
    matrix_rows = generate_indexation_matrix_rows(payload, prev_payload)
    scan_for_secrets(matrix_rows)
    ts_matrix = reports_dir / f"route_indexation_matrix_{utc_ts}.csv"
    save_indexation_matrix_csv(matrix_rows, ts_matrix, overwrite=False)

    root_matrix = reports_dir / "route_indexation_matrix.csv"
    save_indexation_matrix_csv(matrix_rows, root_matrix, overwrite=True)

    summary["stages"]["reports"] = {
        "weekly_report": str(root_weekly),
        "indexation_matrix": str(root_matrix),
        "total_routes_in_matrix": len(matrix_rows),
    }

    # Stage 6: Alert Evaluation
    logger.info("Stage 6: Evaluating SEO alerts and health status...")
    evaluation = evaluate_alerts(payload, prev_payload)
    alerts_md = generate_alerts_markdown(evaluation, payload)
    scan_for_secrets(alerts_md)

    ts_alerts = reports_dir / f"seo_alerts_{utc_ts}.md"
    save_alerts_report(alerts_md, ts_alerts, overwrite=False)

    root_alerts = reports_dir / "seo_alerts.md"
    save_alerts_report(alerts_md, root_alerts, overwrite=True)

    summary["stages"]["alerts"] = {
        "report": str(root_alerts),
        "healthy": evaluation.get("healthy", False),
        "status_message": evaluation.get("status_message"),
        "counts": evaluation.get("counts", {}),
    }

    # Summary completion
    summary["completed_at"] = datetime.now(timezone.utc).isoformat()
    summary["healthy"] = evaluation.get("healthy", False)
    summary["status_message"] = evaluation.get("status_message")
    summary["status"] = "success"

    # Optional GitHub Actions step summary
    github_summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_summary_file:
        try:
            with open(github_summary_file, "a", encoding="utf-8") as f:
                f.write(f"## AI Tools Zone — SEO Telemetry Execution\n\n")
                f.write(f"- **System Status:** `{summary['status_message']}`\n")
                f.write(f"- **Healthy Gate:** `{'PASS' if summary['healthy'] else 'ALERT'}`\n")
                f.write(f"- **Active Alerts:** P0={evaluation['counts'].get('p0', 0)}, P1={evaluation['counts'].get('p1', 0)}, P2={evaluation['counts'].get('p2', 0)}\n")
                f.write(f"- **Canonical Inventory:** {len(matrix_rows)} routes evaluated\n")
                f.write(f"- **Generated Reports:** `weekly_seo_performance.md`, `route_indexation_matrix.csv`, `seo_alerts.md`\n")
        except Exception as exc:
            logger.warning("Could not append to GITHUB_STEP_SUMMARY: %s", exc)

    logger.info("Pipeline execution completed successfully. Health: %s", summary["status_message"])
    return summary


def main() -> None:
    """CLI entry point for the pipeline runner."""
    parser = argparse.ArgumentParser(description="AI Tools Zone SEO Telemetry Pipeline Runner")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=7, help="Trailing period duration in days (default: 7)")
    parser.add_argument("--skip-inspection", action="store_true", help="Skip live URL inspection and reuse latest snapshot")
    parser.add_argument("--snapshot", help="Run reporting and alert stages from a pre-existing snapshot JSON")
    parser.add_argument("--output-dir", help="Directory for generated reports (default: reports/seo-telemetry)")
    parser.add_argument("--archive-dir", help="Directory for snapshots (default: scratch/telemetry_archive)")

    args = parser.parse_args()

    try:
        res = execute_pipeline(
            start_date=args.start_date,
            end_date=args.end_date,
            days=args.days,
            skip_inspection=args.skip_inspection,
            snapshot_path=args.snapshot,
            output_dir=Path(args.output_dir) if args.output_dir else None,
            archive_dir=Path(args.archive_dir) if args.archive_dir else None,
        )
        print("\n" + "=" * 60)
        print("PIPELINE EXECUTION SUMMARY")
        print("=" * 60)
        print(f"Status         : {res.get('status').upper()}")
        print(f"Health Message : {res.get('status_message')}")
        print(f"Healthy Gate   : {res.get('healthy')}")
        print("=" * 60)

        # Fail visibly on P0 critical alerts
        p0_count = res.get("stages", {}).get("alerts", {}).get("counts", {}).get("p0", 0)
        if p0_count > 0:
            logger.error("Pipeline finished with %d critical P0 alert(s)!", p0_count)
            sys.exit(2)

        sys.exit(0)
    except Exception as exc:
        logger.exception("Pipeline execution failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
