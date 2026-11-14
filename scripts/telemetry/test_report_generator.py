"""Unit tests for AI Tools Zone SEO Reporting Engine (Stage 5).

Covers:
1. Correct weekly report generation.
2. Correct week-over-week calculations.
3. GSC and GA4 metric separation.
4. All 97 canonical routes represented in indexation matrix.
5. Indexation transitions.
6. Historical report preservation (ReportPreservationError).
7. Malformed archive handling (MalformedArchiveError).
8. Secret and token redaction.
"""

import os
import json
import tempfile
import unittest
from pathlib import Path

from scripts.telemetry.config import get_canonical_routes, get_expected_page_count, WEBSITE_ORIGIN
from scripts.telemetry.report_generator import (
    load_snapshot,
    calculate_wow_comparison,
    generate_indexation_matrix_rows,
    generate_weekly_seo_performance_markdown,
    save_weekly_report,
    save_indexation_matrix_csv,
    generate_reports,
    ReportGenerationError,
    MalformedArchiveError,
    ReportPreservationError,
)
from scripts.telemetry.normalizer import scan_for_secrets


def create_mock_snapshot(
    run_id: str = "mock_test_run",
    start_date: str = "2026-10-15",
    end_date: str = "2026-11-11",
    clicks: int = 20,
    impressions: int = 500,
    ctr: float = 0.04,
    position: float = 18.5,
    sessions: int = 35,
    users: int = 25,
    whatsapp_events: int = 12,
    ai_sessions: int = 0,
    indexed_routes_count: int = 80,
    collection_status: str = "success",
) -> dict:
    """Helper to generate a schema-valid mock snapshot for tests."""
    routes = get_canonical_routes()
    correlated = []

    for idx, r in enumerate(routes):
        is_indexed = idx < indexed_routes_count
        correlated.append({
            "canonical_route": r,
            "is_canonical": True,
            "inspection": {
                "verdict": "PASS" if is_indexed else "NEUTRAL",
                "coverage_state": "Submitted and indexed" if is_indexed else "Discovered – currently not indexed",
                "indexing_state": "INDEXING_ALLOWED",
                "robots_txt_state": "ALLOWED",
                "page_fetch_state": "SUCCESSFUL",
                "last_crawl_time": "2026-11-09T19:00:43Z" if is_indexed else None,
                "google_canonical": f"{WEBSITE_ORIGIN}{r}",
                "user_canonical": f"{WEBSITE_ORIGIN}{r}",
            },
            "gsc_performance": {
                "has_data": idx == 0,
                "clicks": clicks if idx == 0 else 0,
                "impressions": impressions if idx == 0 else 0,
                "ctr": ctr if idx == 0 else 0.0,
                "average_position": position if idx == 0 else 0.0,
                "distinct_queries": 1 if idx == 0 else 0,
                "top_queries": [{"query": "test tool pakistan", "clicks": clicks, "impressions": impressions, "position": position}] if idx == 0 else [],
            },
            "ga4_performance": {
                "has_data": idx == 0,
                "sessions": sessions if idx == 0 else 0,
                "total_users": users if idx == 0 else 0,
                "engaged_sessions": int(sessions * 0.7) if idx == 0 else 0,
                "engagement_rate": 0.7 if idx == 0 else 0.0,
                "average_session_duration": 45.0 if idx == 0 else 0.0,
            },
            "whatsapp_leads": {
                "has_events": idx == 0,
                "total_lead_interactions": whatsapp_events if idx == 0 else 0,
                "unique_prospective_users": 8 if idx == 0 else 0,
                "event_breakdown": {
                    "whatsapp_click": int(whatsapp_events / 2) if idx == 0 else 0,
                    "product_whatsapp_click": int(whatsapp_events / 2) if idx == 0 else 0,
                    "generate_lead": 0,
                },
            },
            "ai_referrals": {
                "has_referrals": idx == 0 and ai_sessions > 0,
                "sessions": ai_sessions if idx == 0 else 0,
                "users": ai_sessions if idx == 0 else 0,
                "platforms": ["ChatGPT"] if (idx == 0 and ai_sessions > 0) else [],
            },
        })

    return {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "created_at_utc": "2026-11-14T20:00:00Z",
        "collection_status": collection_status,
        "reporting_date_range": {
            "start_date": start_date,
            "end_date": end_date,
        },
        "source_metadata": {
            "gsc_property": "sc-domain:aitoolszone.tech",
            "ga4_property": "properties/562093633",
            "origin": WEBSITE_ORIGIN,
            "commit_sha": "abcd1234abcd1234abcd1234abcd1234abcd1234",
        },
        "summary": {
            "canonical_route_count": len(routes),
            "canonical_indexed_count": indexed_routes_count,
            "canonical_pending_count": len(routes) - indexed_routes_count,
            "gsc_site_totals": {
                "clicks": clicks,
                "impressions": impressions,
                "ctr": ctr,
                "average_position": position,
                "is_empty": False,
                "data_state": "final",
            },
            "gsc_pakistan_queries_count": 1,
            "ga4_organic_sessions": sessions,
            "ga4_organic_users": users,
            "whatsapp_interaction_events": whatsapp_events,
            "whatsapp_unique_users": 8,
            "ai_assistant_sessions": ai_sessions,
        },
        "correlated_routes": correlated,
        "unmatched_records": {
            "gsc_urls": [],
            "ga4_landing_pages": [],
        },
        "data_quality": {
            "completeness": {
                "gsc_available": True,
                "ga4_available": True,
                "url_inspections_available": True,
            },
            "validation_warnings": [],
        },
        "attribution_notes": {
            "non_conflation_rule": "GSC clicks represent SERP departures; GA4 sessions represent executed browser page loads.",
            "whatsapp_conversions": "WhatsApp events reflect click triggers.",
            "ai_referrals": "AI referrals without standard HTTP Referer headers fall into Direct.",
        },
    }


class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.routes = get_canonical_routes()
        self.expected_count = get_expected_page_count()
        self.current_snapshot = create_mock_snapshot(
            run_id="run_current",
            clicks=20,
            impressions=500,
            sessions=35,
            users=25,
            whatsapp_events=12,
            indexed_routes_count=80,
        )
        self.previous_snapshot = create_mock_snapshot(
            run_id="run_prev",
            start_date="2026-09-15",
            end_date="2026-10-14",
            clicks=15,
            impressions=400,
            sessions=25,
            users=20,
            whatsapp_events=8,
            indexed_routes_count=75,
        )

    def test_01_weekly_report_generation(self):
        """Verify generation of Markdown weekly performance report with required sections."""
        md = generate_weekly_seo_performance_markdown(self.current_snapshot, self.previous_snapshot)
        self.assertIsInstance(md, str)
        self.assertIn("# AI Tools Zone — Weekly SEO Performance Report", md)
        self.assertIn("Reporting Period", md)
        self.assertIn("2026-10-15 to 2026-11-11", md)
        self.assertIn("Executive Performance Summary", md)
        self.assertIn("Google Search Console Performance", md)
        self.assertIn("Google Analytics 4 Organic Search Performance", md)
        self.assertIn("Commercial Lead Tracking", md)
        self.assertIn("AI Assistant Referral Traffic Tracking", md)
        self.assertIn("Underperforming Pages & Optimization Queue", md)
        self.assertIn("Telemetry Observations vs Strategic Recommendations", md)

    def test_02_week_over_week_calculations(self):
        """Verify correct Week-over-Week calculations and delta percentages."""
        curr_summary = self.current_snapshot["summary"]
        prev_summary = self.previous_snapshot["summary"]

        wow = calculate_wow_comparison(curr_summary, prev_summary)
        self.assertTrue(wow["has_baseline"])
        metrics = wow["metrics"]

        # Clicks: 20 vs 15 -> +33.3% (+5)
        self.assertEqual(metrics["gsc_clicks"]["current"], 20)
        self.assertEqual(metrics["gsc_clicks"]["previous"], 15)
        self.assertEqual(metrics["gsc_clicks"]["abs_delta"], 5)
        self.assertEqual(metrics["gsc_clicks"]["pct_delta"], 33.33)

        # Impressions: 500 vs 400 -> +25.0% (+100)
        self.assertEqual(metrics["gsc_impressions"]["abs_delta"], 100)
        self.assertEqual(metrics["gsc_impressions"]["pct_delta"], 25.0)

        # GA4 sessions: 35 vs 25 -> +40.0% (+10)
        self.assertEqual(metrics["ga4_organic_sessions"]["abs_delta"], 10)
        self.assertEqual(metrics["ga4_organic_sessions"]["pct_delta"], 40.0)

        # WhatsApp interactions: 12 vs 8 -> +50.0% (+4)
        self.assertEqual(metrics["whatsapp_interactions"]["abs_delta"], 4)
        self.assertEqual(metrics["whatsapp_interactions"]["pct_delta"], 50.0)

    def test_03_metric_separation_integrity(self):
        """Verify that GSC clicks and GA4 sessions are strictly separated in reporting."""
        md = generate_weekly_seo_performance_markdown(self.current_snapshot, self.previous_snapshot)

        # Verify explicit Non-Conflation Rule alert callout exists
        self.assertIn("Metric Non-Conflation Rule", md)
        self.assertIn("Google Search Console clicks represent SERP departures", md)
        self.assertIn("Google Analytics 4 sessions represent successfully executed browser page loads", md)
        self.assertIn("never summed or conflated", md)

        # Ensure distinct table rows for GSC clicks and GA4 sessions
        self.assertIn("**GSC Organic Clicks**", md)
        self.assertIn("**GA4 Organic Sessions**", md)

    def test_04_all_routes_represented_in_indexation_matrix(self):
        """Verify that all canonical public routes from contract are represented in indexation matrix."""
        rows = generate_indexation_matrix_rows(self.current_snapshot, self.previous_snapshot)
        self.assertEqual(len(rows), self.expected_count)

        # Verify all routes in seo-contract are accounted for
        matrix_paths = set(r["route_path"] for r in rows)
        for expected_route in self.routes:
            self.assertIn(expected_route, matrix_paths)

    def test_05_indexation_transitions(self):
        """Verify indexation transitions (NEW_INDEXED, DE_INDEXED, UNCHANGED_INDEXED, UNCHANGED_PENDING)."""
        # In setup: previous had 75 indexed, current has 80 indexed -> routes 75..79 transitioned
        rows = generate_indexation_matrix_rows(self.current_snapshot, self.previous_snapshot)

        transitions = [r["indexation_transition"] for r in rows]
        self.assertIn("UNCHANGED_INDEXED", transitions)
        self.assertIn("NEW_INDEXED", transitions)
        self.assertIn("UNCHANGED_PENDING", transitions)

        # Verify new indexed routes are correctly tagged
        new_indexed = [r for r in rows if r["indexation_transition"] == "NEW_INDEXED"]
        self.assertEqual(len(new_indexed), 5)

        # Test FIRST_OBSERVATION when previous is None
        rows_no_prev = generate_indexation_matrix_rows(self.current_snapshot, None)
        transitions_no_prev = set(r["indexation_transition"] for r in rows_no_prev)
        self.assertEqual(transitions_no_prev, {"FIRST_OBSERVATION"})

    def test_06_historical_report_preservation(self):
        """Verify that saving with overwrite=False raises ReportPreservationError if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "weekly_seo_performance.md"
            test_file.write_text("Existing report content", encoding="utf-8")

            # Attempting to save without overwrite must raise ReportPreservationError
            with self.assertRaises(ReportPreservationError):
                save_weekly_report("New report content", test_file, overwrite=False)

            # Content must remain intact
            self.assertEqual(test_file.read_text(encoding="utf-8"), "Existing report content")

            # Saving with overwrite=True succeeds
            save_weekly_report("Updated report content", test_file, overwrite=True)
            self.assertEqual(test_file.read_text(encoding="utf-8"), "Updated report content")

    def test_07_malformed_archive_handling(self):
        """Verify graceful error handling for malformed or missing snapshots."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Case 1: Corrupted JSON
            corrupt_file = Path(tmpdir) / "corrupt.json"
            corrupt_file.write_text("{bad json: true", encoding="utf-8")
            with self.assertRaises(MalformedArchiveError):
                load_snapshot(corrupt_file)

            # Case 2: Missing schema keys
            invalid_file = Path(tmpdir) / "invalid.json"
            invalid_file.write_text(json.dumps({"some_key": 123}), encoding="utf-8")
            with self.assertRaises(MalformedArchiveError):
                load_snapshot(invalid_file)

            # Case 3: Non-existent file
            with self.assertRaises(FileNotFoundError):
                load_snapshot(Path(tmpdir) / "does_not_exist.json")

    def test_08_secret_and_token_redaction(self):
        """Verify that reports are checked for credentials and tokens before saving."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "secret_leak.md"
            leaked_content = "Report data: Authorization: Bearer ya29.a0AfH6SMBxyz_fake_token_value"

            # Pre-save scan should raise ValueError on detected credential pattern
            with self.assertRaises(ValueError):
                save_weekly_report(leaked_content, out_path)

            self.assertFalse(out_path.exists())


if __name__ == "__main__":
    unittest.main()
