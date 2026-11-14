"""Unit tests for AI Tools Zone Telemetry Alert Engine (Stage 5).

Covers:
1. P0 unexpected de-indexation detection.
2. Temporary API errors NOT classified as de-indexation.
3. Systemic URL inspection failure (P0).
4. Major telemetry collection failure (P0).
5. P1 traffic decline detection (>20% WoW drop).
6. Low-volume safeguards (prevent false positive P1 warnings on low baselines).
7. Incomplete reporting period safeguards.
8. P2 newly indexed notifications.
9. Healthy status conditions ("System Healthy & Stable").
10. Missing source data / incomplete collection suppresses healthy status.
11. Secret and token redaction on alert report.
12. Historical alert report preservation (ReportPreservationError).
"""

import os
import json
import tempfile
import unittest
from pathlib import Path

from scripts.telemetry.config import get_canonical_routes, get_expected_page_count, WEBSITE_ORIGIN
from scripts.telemetry.evaluate_alerts import (
    evaluate_alerts,
    generate_alerts_markdown,
    save_alerts_report,
    run_alert_evaluation,
    Alert,
    MIN_CLICKS_BASELINE,
    MIN_IMPRESSIONS_BASELINE,
    MIN_SESSIONS_BASELINE,
)
from scripts.telemetry.report_generator import ReportPreservationError
from scripts.telemetry.test_report_generator import create_mock_snapshot


class TestAlertEngine(unittest.TestCase):

    def setUp(self):
        self.routes = get_canonical_routes()
        self.expected_count = get_expected_page_count()
        # Clean baseline snapshot with healthy complete data
        self.baseline_snapshot = create_mock_snapshot(
            run_id="run_baseline",
            start_date="2026-10-15",
            end_date="2026-11-11",
            clicks=50,
            impressions=1000,
            sessions=60,
            users=45,
            whatsapp_events=20,
            indexed_routes_count=80,
            collection_status="success",
        )

    def test_01_healthy_status_conditions(self):
        """Verify exact string 'System Healthy & Stable' is returned ONLY when all criteria are met."""
        # Current snapshot identical to baseline (no alerts, complete data, success status)
        current = create_mock_snapshot(
            run_id="run_current_identical",
            start_date="2026-11-12",
            end_date="2026-12-09",
            clicks=50,
            impressions=1000,
            sessions=60,
            users=45,
            whatsapp_events=20,
            indexed_routes_count=80,
            collection_status="success",
        )

        res = evaluate_alerts(current, self.baseline_snapshot)
        self.assertTrue(res["healthy"])
        self.assertEqual(res["status_message"], "System Healthy & Stable")
        self.assertEqual(res["total_alerts"], 0)

        # Markdown report must contain the exact string
        md = generate_alerts_markdown(res, current)
        self.assertIn("System Healthy & Stable", md)

    def test_02_p0_unexpected_deindexation(self):
        """Verify that unexpected de-indexation of previously indexed routes triggers a P0 alert."""
        current = create_mock_snapshot(
            run_id="run_current_deindexed",
            clicks=50,
            impressions=1000,
            sessions=60,
            indexed_routes_count=80,
        )
        # Modify route 0 to be Crawled - currently not indexed (previously was PASS / Submitted and indexed)
        current["correlated_routes"][0]["inspection"] = {
            "verdict": "NEUTRAL",
            "coverage_state": "Crawled - currently not indexed",
            "indexing_state": "INDEXING_ALLOWED",
            "robots_txt_state": "ALLOWED",
            "page_fetch_state": "SUCCESSFUL",
            "last_crawl_time": "2026-11-12T10:00:00Z",
            "google_canonical": f"{WEBSITE_ORIGIN}/",
            "user_canonical": f"{WEBSITE_ORIGIN}/",
        }

        res = evaluate_alerts(current, self.baseline_snapshot)
        self.assertFalse(res["healthy"])
        self.assertNotEqual(res["status_message"], "System Healthy & Stable")
        self.assertEqual(res["counts"]["p0"], 1)

        p0_alert = [a for a in res["alerts"] if a["level"] == "P0"][0]
        self.assertEqual(p0_alert["category"], "DE_INDEXATION")
        self.assertIn(self.routes[0], p0_alert["affected_routes"])

    def test_03_api_error_not_classified_as_deindexation(self):
        """Verify that temporary API inspection errors are NOT classified as de-indexation."""
        current = create_mock_snapshot(
            run_id="run_current_api_error",
            clicks=50,
            impressions=1000,
            sessions=60,
            indexed_routes_count=80,
        )
        # Simulate route 0 encountering an API error (e.g. 429 quota exhaustion or backend timeout)
        current["correlated_routes"][0]["inspection"] = {
            "verdict": "API_ERROR",
            "coverage_state": "api_error: transient HTTP 429",
            "indexing_state": "UNKNOWN",
            "robots_txt_state": "UNKNOWN",
            "page_fetch_state": "UNKNOWN",
            "last_crawl_time": None,
            "google_canonical": None,
            "user_canonical": None,
        }

        res = evaluate_alerts(current, self.baseline_snapshot)

        # Must NOT generate a DE_INDEXATION alert for route 0
        deindex_alerts = [a for a in res["alerts"] if a.get("category") == "DE_INDEXATION"]
        self.assertEqual(len(deindex_alerts), 0)

    def test_04_systemic_inspection_failure_p0(self):
        """Verify that failure of >50% routes in URL inspection triggers a P0 alert."""
        current = create_mock_snapshot(run_id="run_systemic_failure")

        # Mark 60 out of 97 routes as API_ERROR
        for idx in range(60):
            current["correlated_routes"][idx]["inspection"] = {
                "verdict": "API_ERROR",
                "coverage_state": "api_error: quota exceeded",
            }

        res = evaluate_alerts(current, self.baseline_snapshot)
        self.assertFalse(res["healthy"])
        p0_alerts = [a for a in res["alerts"] if a["level"] == "P0"]
        self.assertTrue(any(a["category"] == "INSPECTION_SYSTEM_FAILURE" for a in p0_alerts))

    def test_05_major_collection_failure_p0(self):
        """Verify that collection_status == 'failure' triggers a P0 alert and suppresses healthy status."""
        current = create_mock_snapshot(run_id="run_failed", collection_status="failure")

        res = evaluate_alerts(current, self.baseline_snapshot)
        self.assertFalse(res["healthy"])
        self.assertNotEqual(res["status_message"], "System Healthy & Stable")
        p0_alerts = [a for a in res["alerts"] if a["level"] == "P0"]
        self.assertTrue(any(a["category"] == "SYSTEM_FAILURE" for a in p0_alerts))

    def test_06_p1_traffic_decline_detection(self):
        """Verify that >20% decline in GSC clicks with sufficient baseline triggers a P1 alert."""
        # Baseline: 50 clicks, 1000 impressions, 60 sessions
        # Current: 30 clicks (-40%), 700 impressions (-30%), 40 sessions (-33.3%)
        current = create_mock_snapshot(
            run_id="run_decline",
            start_date="2026-11-12",
            end_date="2026-12-09",
            clicks=30,
            impressions=700,
            sessions=40,
        )

        res = evaluate_alerts(current, self.baseline_snapshot)
        self.assertFalse(res["healthy"])
        self.assertGreaterEqual(res["counts"]["p1"], 1)

        p1_categories = [a["category"] for a in res["alerts"] if a["level"] == "P1"]
        self.assertIn("TRAFFIC_DECLINE", p1_categories)
        self.assertIn("IMPRESSIONS_DECLINE", p1_categories)
        self.assertIn("SESSIONS_DECLINE", p1_categories)

    def test_07_low_volume_safeguard(self):
        """Verify that small volume drops below baseline thresholds DO NOT trigger false positive P1 alerts."""
        # Low volume baseline: 5 clicks (< 10), 30 impressions (< 50), 4 sessions (< 10)
        low_baseline = create_mock_snapshot(
            run_id="run_low_baseline",
            start_date="2026-10-15",
            end_date="2026-11-11",
            clicks=5,
            impressions=30,
            sessions=4,
        )
        # Current drops: 2 clicks (-60%), 15 impressions (-50%), 2 sessions (-50%)
        low_current = create_mock_snapshot(
            run_id="run_low_current",
            start_date="2026-11-12",
            end_date="2026-12-09",
            clicks=2,
            impressions=15,
            sessions=2,
        )

        res = evaluate_alerts(low_current, low_baseline)

        # P1 alerts should be 0 because baselines are below MIN_CLICKS_BASELINE and MIN_IMPRESSIONS_BASELINE
        p1_alerts = [a for a in res["alerts"] if a["level"] == "P1"]
        self.assertEqual(len(p1_alerts), 0)

    def test_08_incomplete_reporting_period_safeguard(self):
        """Verify that truncated date ranges (e.g. 7 days vs 28 days) suppress false positive WoW decline alerts."""
        # Baseline was 28 days (2026-10-15 to 2026-11-11 = 28 days)
        # Current is only 7 days (2026-11-12 to 2026-11-18 = 7 days)
        truncated_current = create_mock_snapshot(
            run_id="run_truncated",
            start_date="2026-11-12",
            end_date="2026-11-18",
            clicks=15,          # Lower absolute numbers due to short period
            impressions=250,
            sessions=15,
        )

        res = evaluate_alerts(truncated_current, self.baseline_snapshot)

        # Due to duration mismatch guard, WoW traffic decline P1 alerts must be suppressed
        traffic_p1 = [a for a in res["alerts"] if a["level"] == "P1" and a["category"] in ("TRAFFIC_DECLINE", "IMPRESSIONS_DECLINE", "SESSIONS_DECLINE")]
        self.assertEqual(len(traffic_p1), 0)

    def test_09_p2_newly_indexed_notifications(self):
        """Verify that routes transitioning from pending to indexed trigger a P2 notification."""
        # Baseline had 75 indexed
        baseline_75 = create_mock_snapshot(run_id="run_75", indexed_routes_count=75)
        # Current has 80 indexed (+5 routes newly indexed)
        current_80 = create_mock_snapshot(run_id="run_80", indexed_routes_count=80)

        res = evaluate_alerts(current_80, baseline_75)
        self.assertEqual(res["counts"]["p2"], 1)
        p2_alert = [a for a in res["alerts"] if a["level"] == "P2"][0]
        self.assertEqual(p2_alert["category"], "NEW_INDEXATION")
        self.assertEqual(len(p2_alert["affected_routes"]), 5)

        # Because a P2 alert exists, healthy flag should be False (Healthy requires 0 alerts)
        self.assertFalse(res["healthy"])

    def test_10_missing_source_data_suppresses_healthy_status(self):
        """Verify that incomplete or missing source data never outputs 'System Healthy & Stable'."""
        current = create_mock_snapshot(run_id="run_missing_ga4")
        # Mark GA4 as unavailable
        current["data_quality"]["completeness"]["ga4_available"] = False
        current["collection_status"] = "partial"

        res = evaluate_alerts(current, None)
        self.assertFalse(res["healthy"])
        self.assertNotEqual(res["status_message"], "System Healthy & Stable")
        self.assertIn("DEGRADED", res["status_message"])

    def test_11_secret_redaction_in_alerts_report(self):
        """Verify that alert reports containing secret patterns are blocked before saving."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "leaked_alert.md"
            leaked_content = "Alert details: bearer_token = ya29.a0AfH6SMB_secret_key_12345"

            with self.assertRaises(ValueError):
                save_alerts_report(leaked_content, out_file)

            self.assertFalse(out_file.exists())

    def test_12_historical_alerts_report_preservation(self):
        """Verify that save_alerts_report with overwrite=False raises ReportPreservationError if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            existing_file = Path(tmpdir) / "seo_alerts.md"
            existing_file.write_text("Existing alert history", encoding="utf-8")

            with self.assertRaises(ReportPreservationError):
                save_alerts_report("New alert content", existing_file, overwrite=False)

            self.assertEqual(existing_file.read_text(encoding="utf-8"), "Existing alert history")


if __name__ == "__main__":
    unittest.main()
