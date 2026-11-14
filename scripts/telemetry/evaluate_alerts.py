"""AI Tools Zone — Telemetry Alert Engine (Stage 5).

Evaluates normalized telemetry snapshots against multi-tier SEO alerting thresholds:
- P0 (Critical): Unexpected de-indexation, systemic inspection failure, major collection failure.
- P1 (Warning): >20% WoW decline in clicks, impressions, or sessions (with volume safeguards).
- P2 (Informational): Newly indexed canonical URLs, recovery, positive organic growth.
- Healthy Status: Outputs exact string "System Healthy & Stable" ONLY under verified complete conditions.

Guarantees:
- Temporary API errors or missing data are NEVER classified as de-indexation.
- Low-volume safeguards prevent false positive alerts on statistical noise.
- Incomplete reporting periods and duration mismatches suppress deceptive decline alerts.
- Secret and token redaction before writing alerts report.
- Historical report preservation: existing alerts files are never overwritten when overwrite=False.
"""

import os
import re
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union

from .config import ROOT_DIR, WEBSITE_ORIGIN, get_canonical_routes, get_expected_page_count
from .normalizer import (
    DEFAULT_ARCHIVE_DIR,
    validate_normalized_payload,
    scan_for_secrets,
    classify_route_indexation,
)
from .report_generator import (
    DEFAULT_REPORTS_DIR,
    ReportPreservationError,
    MalformedArchiveError,
    load_snapshot,
)

logger = logging.getLogger("telemetry.evaluate_alerts")

# Alert Thresholds & Safeguards
DECLINE_THRESHOLD_PCT: float = 20.0  # 20% week-over-week drop
GROWTH_THRESHOLD_PCT: float = 20.0   # 20% week-over-week increase

MIN_CLICKS_BASELINE: int = 10        # Minimum baseline clicks required to trigger P1 alert
MIN_IMPRESSIONS_BASELINE: int = 50   # Minimum baseline impressions required to trigger P1 alert
MIN_SESSIONS_BASELINE: int = 10      # Minimum baseline organic sessions required to trigger P1 alert


class Alert:
    """Represents an individual telemetry alert event."""

    def __init__(
        self,
        level: str,
        category: str,
        title: str,
        details: str,
        affected_routes: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
    ):
        if level not in ("P0", "P1", "P2"):
            raise ValueError(f"Invalid alert level: {level}. Must be P0, P1, or P2.")
        self.level = level
        self.category = category
        self.title = title
        self.details = details
        self.affected_routes = affected_routes or []
        self.metrics = metrics or {}
        self.timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "category": self.category,
            "title": self.title,
            "details": self.details,
            "affected_routes": self.affected_routes,
            "metrics": self.metrics,
            "timestamp_utc": self.timestamp_utc,
        }


def _calculate_period_duration_days(start_str: Optional[str], end_str: Optional[str]) -> Optional[int]:
    """Calculate the number of days in a date range string."""
    if not start_str or not end_str:
        return None
    try:
        d1 = datetime.strptime(start_str, "%Y-%m-%d")
        d2 = datetime.strptime(end_str, "%Y-%m-%d")
        return (d2 - d1).days + 1
    except Exception:
        return None


def evaluate_alerts(
    current_snapshot: Dict[str, Any],
    previous_snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Evaluate telemetry data against P0, P1, and P2 alerting thresholds.

    Args:
        current_snapshot: Current normalized telemetry snapshot payload.
        previous_snapshot: Optional previous snapshot payload for comparative evaluation.

    Returns:
        Dict[str, Any]: Evaluation summary including healthy flag, status message, and alerts grouped by level.
    """
    alerts: List[Alert] = []

    # 1. Inspect System Status & Completeness
    collection_status = current_snapshot.get("collection_status", "unknown")
    data_quality = current_snapshot.get("data_quality", {})
    completeness = data_quality.get("completeness", {})
    curr_summary = current_snapshot.get("summary", {})
    curr_gsc = curr_summary.get("gsc_site_totals") or {}
    validation_warnings = data_quality.get("validation_warnings", [])

    has_gsc = completeness.get("gsc_available", False)
    has_ga4 = completeness.get("ga4_available", False)
    has_inspections = completeness.get("url_inspections_available", False)

    # ----------------------------------------------------
    # P0 Checks: System Failures & Unexpected De-Indexation
    # ----------------------------------------------------
    # Check 1.1: Total Collection Engine Failure
    if collection_status == "failure":
        alerts.append(Alert(
            level="P0",
            category="SYSTEM_FAILURE",
            title="Telemetry Data Collection Total Failure",
            details="The telemetry collection engine reported collection_status == 'failure'. No valid data retrieved.",
        ))

    # Check 1.2: Systemic URL Inspection Subsystem Failure
    curr_routes = current_snapshot.get("correlated_routes", [])
    total_routes_count = len(curr_routes)
    api_error_routes: List[str] = []
    missing_inspection_routes: List[str] = []

    for r in curr_routes:
        insp = r.get("inspection")
        route_path = r.get("canonical_route", "")
        if insp is None:
            missing_inspection_routes.append(route_path)
        elif insp.get("verdict") == "API_ERROR" or "api_error" in (insp.get("coverage_state") or "").lower():
            api_error_routes.append(route_path)

    if total_routes_count > 0:
        error_ratio = (len(api_error_routes) + len(missing_inspection_routes)) / total_routes_count
        if not has_inspections or error_ratio >= 0.50:
            alerts.append(Alert(
                level="P0",
                category="INSPECTION_SYSTEM_FAILURE",
                title="Systemic URL Inspection Failure",
                details=(
                    f"More than 50% of canonical routes failed URL inspection "
                    f"({len(api_error_routes)} API errors, {len(missing_inspection_routes)} missing out of {total_routes_count})."
                ),
                affected_routes=api_error_routes + missing_inspection_routes,
            ))

    # Check 1.3: Unexpected De-Indexation of Previously Indexed Canonical Pages
    if previous_snapshot:
        prev_routes_map = {r["canonical_route"]: r for r in previous_snapshot.get("correlated_routes", [])}
        deindexed_routes: List[str] = []

        for r in curr_routes:
            route_path = r.get("canonical_route", "")
            curr_insp = r.get("inspection")
            prev_route = prev_routes_map.get(route_path)
            prev_insp = prev_route.get("inspection") if prev_route else None

            # Guard: If current inspection failed due to API error or is missing,
            # DO NOT classify it as de-indexation!
            if curr_insp is None:
                continue
            curr_verdict = curr_insp.get("verdict", "")
            curr_coverage = (curr_insp.get("coverage_state") or "").lower()
            if curr_verdict == "API_ERROR" or "api_error" in curr_coverage:
                continue

            # Determine if previously and currently indexed via authoritative classifier
            if prev_insp is not None:
                is_prev_indexed = (classify_route_indexation(prev_insp) == "INDEXED")
                is_curr_indexed = (classify_route_indexation(curr_insp) == "INDEXED")

                # De-indexation occurs only if previously indexed and genuinely NOT indexed now
                if is_prev_indexed and not is_curr_indexed:
                    deindexed_routes.append(route_path)

        if deindexed_routes:
            alerts.append(Alert(
                level="P0",
                category="DE_INDEXATION",
                title="Unexpected De-Indexation of Canonical Routes",
                details=f"{len(deindexed_routes)} canonical route(s) were previously indexed by Google but are no longer indexed.",
                affected_routes=deindexed_routes,
            ))

    # ----------------------------------------------------
    # P1 Checks: Significant Performance Declines (>20% WoW)
    # ----------------------------------------------------
    if previous_snapshot and collection_status != "partial" and collection_status != "failure":
        prev_summary = previous_snapshot.get("summary", {})
        prev_gsc = prev_summary.get("gsc_site_totals") or {}

        # Period duration check to prevent false positives from unequal windows
        curr_dr = current_snapshot.get("reporting_date_range", {})
        prev_dr = previous_snapshot.get("reporting_date_range", {})
        curr_days = _calculate_period_duration_days(curr_dr.get("start_date"), curr_dr.get("end_date"))
        prev_days = _calculate_period_duration_days(prev_dr.get("start_date"), prev_dr.get("end_date"))

        # Only evaluate WoW traffic decline if durations match (or both are None)
        can_evaluate_wow = True
        if curr_days and prev_days and curr_days < (prev_days * 0.75):
            can_evaluate_wow = False
            logger.info("Current period duration (%d days) is significantly shorter than previous (%d days). Suppressing WoW decline alerts.", curr_days, prev_days)

        if can_evaluate_wow:
            # Check 2.1: GSC Organic Clicks Decline > 20%
            curr_clicks = curr_gsc.get("clicks")
            prev_clicks = prev_gsc.get("clicks")
            if curr_clicks is not None and prev_clicks is not None:
                # Safeguard: Apply minimum baseline threshold
                if prev_clicks >= MIN_CLICKS_BASELINE:
                    decline_pct = ((prev_clicks - curr_clicks) / prev_clicks) * 100.0
                    if decline_pct > DECLINE_THRESHOLD_PCT:
                        alerts.append(Alert(
                            level="P1",
                            category="TRAFFIC_DECLINE",
                            title="Significant GSC Organic Clicks Decline",
                            details=f"GSC organic clicks declined by {decline_pct:.1f}% WoW (from {prev_clicks} to {curr_clicks}).",
                            metrics={"previous_clicks": prev_clicks, "current_clicks": curr_clicks, "decline_pct": round(decline_pct, 1)},
                        ))

            # Check 2.2: GSC Impressions Decline > 20%
            curr_imp = curr_gsc.get("impressions")
            prev_imp = prev_gsc.get("impressions")
            if curr_imp is not None and prev_imp is not None:
                # Safeguard: Apply minimum baseline threshold
                if prev_imp >= MIN_IMPRESSIONS_BASELINE:
                    decline_pct = ((prev_imp - curr_imp) / prev_imp) * 100.0
                    if decline_pct > DECLINE_THRESHOLD_PCT:
                        alerts.append(Alert(
                            level="P1",
                            category="IMPRESSIONS_DECLINE",
                            title="Significant GSC Search Impressions Decline",
                            details=f"GSC search impressions declined by {decline_pct:.1f}% WoW (from {prev_imp} to {curr_imp}).",
                            metrics={"previous_impressions": prev_imp, "current_impressions": curr_imp, "decline_pct": round(decline_pct, 1)},
                        ))

            # Check 2.3: GA4 Organic Sessions Decline > 20%
            curr_sessions = curr_summary.get("ga4_organic_sessions")
            prev_sessions = prev_summary.get("ga4_organic_sessions")
            if curr_sessions is not None and prev_sessions is not None:
                # Safeguard: Apply minimum baseline threshold
                if prev_sessions >= MIN_SESSIONS_BASELINE:
                    decline_pct = ((prev_sessions - curr_sessions) / prev_sessions) * 100.0
                    if decline_pct > DECLINE_THRESHOLD_PCT:
                        alerts.append(Alert(
                            level="P1",
                            category="SESSIONS_DECLINE",
                            title="Significant GA4 Organic Search Sessions Decline",
                            details=f"GA4 Pakistan organic sessions declined by {decline_pct:.1f}% WoW (from {prev_sessions} to {curr_sessions}).",
                            metrics={"previous_sessions": prev_sessions, "current_sessions": curr_sessions, "decline_pct": round(decline_pct, 1)},
                        ))

    # ----------------------------------------------------
    # P2 Checks: Informational Notifications
    # ----------------------------------------------------
    if previous_snapshot:
        prev_routes_map = {r["canonical_route"]: r for r in previous_snapshot.get("correlated_routes", [])}
        newly_indexed_routes: List[str] = []
        recovered_routes: List[str] = []

        for r in curr_routes:
            route_path = r.get("canonical_route", "")
            curr_insp = r.get("inspection")
            prev_route = prev_routes_map.get(route_path)
            prev_insp = prev_route.get("inspection") if prev_route else None

            if curr_insp is None:
                continue

            is_curr_indexed = (classify_route_indexation(curr_insp) == "INDEXED")

            if prev_insp is not None:
                prev_verdict = prev_insp.get("verdict", "")
                is_prev_indexed = (classify_route_indexation(prev_insp) == "INDEXED")

                if not is_prev_indexed and is_curr_indexed:
                    if prev_verdict == "FAIL":
                        recovered_routes.append(route_path)
                    else:
                        newly_indexed_routes.append(route_path)

        if newly_indexed_routes:
            alerts.append(Alert(
                level="P2",
                category="NEW_INDEXATION",
                title="Newly Indexed Canonical Routes",
                details=f"{len(newly_indexed_routes)} canonical route(s) transitioned into indexed status in Google Search Console.",
                affected_routes=newly_indexed_routes,
            ))

        if recovered_routes:
            alerts.append(Alert(
                level="P2",
                category="INDEXATION_RECOVERY",
                title="Recovered Canonical Routes",
                details=f"{len(recovered_routes)} canonical route(s) recovered from technical crawl/indexation failure.",
                affected_routes=recovered_routes,
            ))

        # Positive growth notification
        prev_summary = previous_snapshot.get("summary", {})
        prev_gsc = prev_summary.get("gsc_site_totals") or {}
        curr_clicks = curr_gsc.get("clicks", 0)
        prev_clicks = prev_gsc.get("clicks", 0)

        if prev_clicks >= MIN_CLICKS_BASELINE and curr_clicks > prev_clicks:
            growth_pct = ((curr_clicks - prev_clicks) / prev_clicks) * 100.0
            if growth_pct >= GROWTH_THRESHOLD_PCT:
                alerts.append(Alert(
                    level="P2",
                    category="ORGANIC_GROWTH",
                    title="Positive Organic Search Traffic Growth",
                    details=f"GSC organic clicks grew by +{growth_pct:.1f}% WoW ({prev_clicks} -> {curr_clicks}).",
                    metrics={"growth_pct": round(growth_pct, 1), "current_clicks": curr_clicks, "previous_clicks": prev_clicks},
                ))

    # ----------------------------------------------------
    # Healthy Status Verification
    # ----------------------------------------------------
    # Requirements for "System Healthy & Stable":
    # 1. collection_status == "success"
    # 2. No P0, P1, or P2 alerts exist.
    # 3. Data is sufficiently complete (GSC available, GA4 available, inspections available, totals not empty).
    # 4. No critical validation failures.
    p0_alerts = [a for a in alerts if a.level == "P0"]
    p1_alerts = [a for a in alerts if a.level == "P1"]
    p2_alerts = [a for a in alerts if a.level == "P2"]

    has_required_completeness = (
        has_gsc
        and has_ga4
        and has_inspections
        and bool(curr_gsc)
        and not curr_gsc.get("is_empty", False)
    )

    no_alerts = len(alerts) == 0
    is_success = (collection_status == "success")
    no_critical_validation = len([w for w in validation_warnings if "anomaly" in w.lower()]) == 0

    is_healthy = is_success and no_alerts and has_required_completeness and no_critical_validation

    if is_healthy:
        status_message = "System Healthy & Stable"
    elif len(p0_alerts) > 0:
        status_message = f"CRITICAL: {len(p0_alerts)} P0 Alert(s) Active"
    elif len(p1_alerts) > 0:
        status_message = f"WARNING: {len(p1_alerts)} P1 Alert(s) Active"
    elif len(p2_alerts) > 0:
        status_message = f"NOTICE: {len(p2_alerts)} P2 Informational Notice(s) Active"
    elif not has_required_completeness or not is_success:
        status_message = "DEGRADED: Telemetry Dataset Incomplete or Partial"
    else:
        status_message = "ATTENTION: Telemetry Requires Verification"

    return {
        "healthy": is_healthy,
        "status_message": status_message,
        "total_alerts": len(alerts),
        "counts": {
            "p0": len(p0_alerts),
            "p1": len(p1_alerts),
            "p2": len(p2_alerts),
        },
        "alerts": [a.to_dict() for a in alerts],
        "completeness": {
            "collection_status": collection_status,
            "gsc_available": has_gsc,
            "ga4_available": has_ga4,
            "url_inspections_available": has_inspections,
            "gsc_totals_present": bool(curr_gsc),
        },
    }


def generate_alerts_markdown(
    evaluation: Dict[str, Any],
    snapshot: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate Markdown report for telemetry alerts and health status.

    Args:
        evaluation: Evaluation dictionary returned by evaluate_alerts().
        snapshot: Optional snapshot payload for date range / metadata context.

    Returns:
        str: Markdown document content.
    """
    status_msg = evaluation.get("status_message", "Unknown Status")
    is_healthy = evaluation.get("healthy", False)
    counts = evaluation.get("counts", {})
    alerts = evaluation.get("alerts", [])

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    date_range = snapshot.get("reporting_date_range", {}) if snapshot else {}
    start_date = date_range.get("start_date", "N/A")
    end_date = date_range.get("end_date", "N/A")

    lines = [
        f"# AI Tools Zone — SEO Telemetry Alerts & System Health",
        f"",
        f"> **Evaluation UTC:** `{created_at}` | **Reporting Range:** `{start_date}` to `{end_date}`  ",
        f"> **System Status:** **`{status_msg}`**  ",
        f"",
    ]

    if is_healthy:
        lines.extend([
            f"> [!TIP]",
            f"> ### System Status: **System Healthy & Stable**",
            f"> All telemetry pipelines succeeded with full completeness. Zero P0 (Critical), P1 (Warning), or P2 (Notice) alerts detected across the canonical inventory.",
            f"",
        ])
    elif counts.get("p0", 0) > 0:
        lines.extend([
            f"> [!CAUTION]",
            f"> ### Critical Attention Required: {counts['p0']} P0 Alert(s) Active",
            f"> Severe telemetry anomalies or unexpected de-indexation events detected. Review root cause immediately.",
            f"",
        ])
    elif counts.get("p1", 0) > 0:
        lines.extend([
            f"> [!WARNING]",
            f"> ### Warning: {counts['p1']} P1 Performance Decline Alert(s) Active",
            f"> Significant week-over-week performance declines exceeded safety thresholds.",
            f"",
        ])
    else:
        lines.extend([
            f"> [!NOTE]",
            f"> ### Notice: {counts.get('p2', 0)} Informational Update(s)",
            f"> Informational updates or indexation state transitions recorded.",
            f"",
        ])

    lines.extend([
        f"---",
        f"",
        f"## 1. Alert Summary Matrix",
        f"",
        f"| Severity Level | Active Count | Threshold Description | Response SLA |",
        f"| :--- | :--- | :--- | :--- |",
        f"| **P0 — Critical** | **{counts.get('p0', 0)}** | Unexpected de-indexation, systemic inspection failure, total collection error | Immediate (< 4 hours) |",
        f"| **P1 — Warning** | **{counts.get('p1', 0)}** | >20% WoW decline in clicks, impressions, or sessions (volume safeguarded) | Next Sprint Review |",
        f"| **P2 — Informational** | **{counts.get('p2', 0)}** | Newly indexed routes, crawl recovery, positive traffic acceleration | Informational Notice |",
        f"",
        f"---",
        f"",
        f"## 2. Active Alerts Detail",
        f"",
    ])

    if alerts:
        for idx, a in enumerate(alerts, 1):
            lvl = a.get("level")
            title = a.get("title")
            cat = a.get("category")
            details = a.get("details")
            affected = a.get("affected_routes", [])

            lines.append(f"### Alert {idx}: [{lvl}] {title}")
            lines.append(f"- **Category:** `{cat}`")
            lines.append(f"- **Description:** {details}")
            if affected:
                lines.append(f"- **Affected Routes ({len(affected)}):**")
                for r in affected[:10]:
                    lines.append(f"  - `{r}`")
                if len(affected) > 10:
                    lines.append(f"  - *...and {len(affected) - 10} additional routes*")
            lines.append("")
    else:
        lines.extend([
            f"**No active alerts.** All metrics are operating within normal baseline variance.",
            f"",
        ])

    lines.extend([
        f"---",
        f"",
        f"## 3. Thresholds & Safeguards Configuration",
        f"",
        f"- **Decline Alert Threshold:** `> {DECLINE_THRESHOLD_PCT}%` Week-over-Week reduction.",
        f"- **Growth Alert Threshold:** `> {GROWTH_THRESHOLD_PCT}%` Week-over-Week increase.",
        f"- **Minimum Click Baseline:** `{MIN_CLICKS_BASELINE}` clicks (prevents false positive warnings on low-volume noise).",
        f"- **Minimum Impression Baseline:** `{MIN_IMPRESSIONS_BASELINE}` impressions.",
        f"- **Minimum Session Baseline:** `{MIN_SESSIONS_BASELINE}` organic sessions.",
        f"- **Unequal Period Guard:** Active (suppresses WoW alerts if current date span is significantly truncated).",
        f"- **API Error Isolation:** Active (transient HTTP 429/5xx or API errors are never treated as de-indexation).",
        f"",
        f"---",
        f"*Alert report generated by AI Tools Zone SEO Telemetry Alerting Engine Stage 5.*",
    ])

    return "\n".join(lines)


def save_alerts_report(
    content: str,
    output_path: Optional[Path] = None,
    overwrite: bool = False,
) -> Path:
    """Save the SEO Alerts Report safely and immutably.

    Args:
        content: Markdown string.
        output_path: Optional destination Path. If None, generates a timestamped file under DEFAULT_REPORTS_DIR.
        overwrite: If False, raises ReportPreservationError if target file exists.

    Returns:
        Path: Path to the saved report file.

    Raises:
        ReportPreservationError: If target file exists and overwrite is False.
    """
    # Secret scan
    scan_for_secrets(content)

    DEFAULT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if output_path is None:
        utc_ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        target_path = DEFAULT_REPORTS_DIR / f"seo_alerts_{utc_ts}.md"
    else:
        target_path = Path(output_path)

    if target_path.exists() and not overwrite:
        raise ReportPreservationError(
            f"Preservation violation: Historical alert report already exists at {target_path} and overwrite=False."
        )

    # Atomic write
    tmp_path = target_path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content)
        tmp_path.replace(target_path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass

    logger.info("Saved SEO alerts report to %s", target_path)
    return target_path


def run_alert_evaluation(
    snapshot_source: Union[Dict[str, Any], str, Path, None] = None,
    previous_snapshot_source: Union[Dict[str, Any], str, Path, None] = None,
    output_dir: Optional[Path] = None,
    overwrite: bool = False,
) -> Dict[str, Any]:
    """Execute the complete alert evaluation pipeline.

    Args:
        snapshot_source: Current snapshot (dict, path, or None).
        previous_snapshot_source: Previous snapshot (dict, path, or None).
        output_dir: Custom destination directory.
        overwrite: Whether to overwrite existing files.

    Returns:
        Dict[str, Any]: Evaluation results and output report path.
    """
    target_dir = Path(output_dir) if output_dir else DEFAULT_REPORTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    curr_snapshot = load_snapshot(snapshot_source)
    prev_snapshot = None
    if previous_snapshot_source:
        try:
            prev_snapshot = load_snapshot(previous_snapshot_source)
        except Exception as exc:
            logger.warning("Could not load previous snapshot for alert evaluation: %s", exc)

    evaluation = evaluate_alerts(curr_snapshot, prev_snapshot)
    alerts_md = generate_alerts_markdown(evaluation, curr_snapshot)

    utc_ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    target_path = target_dir / f"seo_alerts_{utc_ts}.md"
    saved_path = save_alerts_report(alerts_md, target_path, overwrite=overwrite)

    return {
        "evaluation": evaluation,
        "report_path": saved_path,
        "healthy": evaluation.get("healthy", False),
        "status_message": evaluation.get("status_message"),
    }
