"""Unit tests for AI Tools Zone Telemetry Normalization & Storage Engine (Stage 4).

Covers all 14 required test criteria using mocked datasets and temporary directories:
1. Valid GSC normalization.
2. Valid GA4 normalization.
3. Canonical URL matching.
4. Unmatched URL handling.
5. GSC/GA4 metric separation.
6. Missing source data.
7. Empty datasets.
8. Duplicate records.
9. Invalid dates and URLs.
10. Schema validation.
11. Immutable archive behavior.
12. Atomic write behavior.
13. Partial collection handling.
14. Credential and token redaction.
"""

import os
import json
import tempfile
import unittest
from pathlib import Path

from scripts.telemetry.normalizer import (
    SCHEMA_VERSION,
    normalize_date,
    validate_date_range,
    normalize_url_path,
    match_canonical_route,
    normalize_telemetry,
    validate_normalized_payload,
    save_telemetry_snapshot,
    scan_for_secrets,
    classify_route_indexation,
    NormalizationError,
    ImmutableArchiveError,
)
from scripts.telemetry.config import get_canonical_routes, get_expected_page_count


class TestNormalizer(unittest.TestCase):

    def setUp(self):
        self.canonical_routes = get_canonical_routes()
        self.expected_count = get_expected_page_count()

        # Mock representative GSC collection output
        self.mock_gsc = {
            "site_totals": {
                "clicks": 8,
                "impressions": 179,
                "ctr": 0.0447,
                "position": 19.19,
                "is_empty": False,
                "data_state": "final",
                "date_range": {"start_date": "2026-10-15", "end_date": "2026-11-11"},
            },
            "pakistan_performance": {
                "total_rows": 2,
                "rows": [
                    {
                        "page": "https://aitoolszone.tech/blog/how-to-pay-for-chatgpt-plus-pakistan/",
                        "query": "how to buy chatgpt plus in pakistan",
                        "device": "DESKTOP",
                        "date": "2026-10-28",
                        "clicks": 0,
                        "impressions": 1,
                        "ctr": 0.0,
                        "position": 100.0,
                    },
                    {
                        "page": "https://aitoolszone.tech/pricing/",
                        "query": "ai tools pakistan pricing",
                        "device": "MOBILE",
                        "date": "2026-10-29",
                        "clicks": 2,
                        "impressions": 10,
                        "ctr": 0.2,
                        "position": 4.5,
                    },
                ],
            },
            "url_inspection_sweep": {
                "total_successful": 97,
                "inspected_routes": [
                    {
                        "route": "/pricing/",
                        "verdict": "PASS",
                        "coverage_state": "Submitted and indexed",
                        "robots_txt_state": "ALLOWED",
                        "indexing_state": "INDEXING_ALLOWED",
                        "last_crawl_time": "2026-11-09T19:00:43Z",
                        "google_canonical": "https://aitoolszone.tech/pricing/",
                        "user_canonical": "https://aitoolszone.tech/pricing/",
                        "crawled_as": "MOBILE",
                    }
                ],
            },
        }

        # Mock representative GA4 collection output
        self.mock_ga4 = {
            "organic_landing_performance": {
                "total_rows": 2,
                "total_sessions": 12,
                "total_users": 10,
                "total_engaged_sessions": 8,
                "date_range": {"start_date": "2026-10-15", "end_date": "2026-11-11"},
                "rows": [
                    {
                        "landing_page": "/",
                        "device_category": "desktop",
                        "date": "20261105",
                        "sessions": 8,
                        "total_users": 6,
                        "engaged_sessions": 6,
                        "engagement_rate": 0.75,
                        "average_session_duration": 120.0,
                    },
                    {
                        "landing_page": "/pricing/",
                        "device_category": "mobile",
                        "date": "20261106",
                        "sessions": 4,
                        "total_users": 4,
                        "engaged_sessions": 2,
                        "engagement_rate": 0.50,
                        "average_session_duration": 45.0,
                    },
                ],
            },
            "whatsapp_lead_performance": {
                "total_lead_events": 4,
                "total_lead_users": 4,
                "rows": [
                    {
                        "event_name": "whatsapp_click",
                        "landing_page": "/",
                        "date": "20261107",
                        "event_count": 2,
                        "total_users": 2,
                    },
                    {
                        "event_name": "product_whatsapp_click",
                        "landing_page": "/products/veo-3-ultra/",
                        "date": "20261108",
                        "event_count": 2,
                        "total_users": 2,
                    },
                ],
            },
            "ai_assistant_traffic": {
                "total_ai_sessions": 0,
                "total_ai_users": 0,
                "is_empty": True,
                "rows": [],
            },
        }

    # 1. Valid GSC normalization
    def test_01_valid_gsc_normalization(self):
        payload = normalize_telemetry(gsc_data=self.mock_gsc, ga4_data=None)
        self.assertEqual(payload["schema_version"], SCHEMA_VERSION)
        self.assertEqual(payload["collection_status"], "partial")
        self.assertTrue(payload["data_quality"]["completeness"]["gsc_available"])
        self.assertFalse(payload["data_quality"]["completeness"]["ga4_available"])

        totals = payload["summary"]["gsc_site_totals"]
        self.assertEqual(totals["clicks"], 8)
        self.assertEqual(totals["impressions"], 179)
        self.assertAlmostEqual(totals["ctr"], 0.0447)
        self.assertAlmostEqual(totals["average_position"], 19.19)

        # Verify inspection on /pricing/
        pricing_record = next(r for r in payload["correlated_routes"] if r["canonical_route"] == "/pricing/")
        self.assertIsNotNone(pricing_record["inspection"])
        self.assertEqual(pricing_record["inspection"]["verdict"], "PASS")
        self.assertEqual(pricing_record["inspection"]["coverage_state"], "Submitted and indexed")

    # 2. Valid GA4 normalization
    def test_02_valid_ga4_normalization(self):
        payload = normalize_telemetry(gsc_data=None, ga4_data=self.mock_ga4)
        self.assertEqual(payload["collection_status"], "partial")
        self.assertFalse(payload["data_quality"]["completeness"]["gsc_available"])
        self.assertTrue(payload["data_quality"]["completeness"]["ga4_available"])

        summary = payload["summary"]
        self.assertEqual(summary["ga4_organic_sessions"], 12)
        self.assertEqual(summary["ga4_organic_users"], 10)
        self.assertEqual(summary["whatsapp_interaction_events"], 4)
        self.assertEqual(summary["whatsapp_unique_users"], 4)

        # Verify homepage correlation
        home_record = next(r for r in payload["correlated_routes"] if r["canonical_route"] == "/")
        self.assertEqual(home_record["ga4_performance"]["sessions"], 8)
        self.assertEqual(home_record["whatsapp_leads"]["event_breakdown"]["whatsapp_click"], 2)

    # 3. Canonical URL matching
    def test_03_canonical_url_matching(self):
        routes_set = set(self.canonical_routes)

        test_cases = [
            ("https://aitoolszone.tech/products/chatgpt-plus/", "/products/chatgpt-plus/", True),
            ("/products/chatgpt-plus/", "/products/chatgpt-plus/", True),
            ("/products/chatgpt-plus", "/products/chatgpt-plus/", True),
            ("https://aitoolszone.tech/", "/", True),
            ("/", "/", True),
            ("https://aitoolszone.tech/blog/ai-subscription-prices-pakistan", "/blog/ai-subscription-prices-pakistan/", True),
            ("https://aitoolszone.tech/compare/canva-vs-adobe/", "/compare/canva-vs-adobe/", True),
        ]

        for raw_input, expected_path, expected_match in test_cases:
            path, is_canon = match_canonical_route(raw_input, routes_set)
            self.assertEqual(path, expected_path, f"Failed path normalization for: {raw_input}")
            self.assertEqual(is_canon, expected_match, f"Failed canonical matching for: {raw_input}")

    # 4. Unmatched URL handling
    def test_04_unmatched_url_handling(self):
        gsc_unmatched = {
            "site_totals": {"clicks": 0, "impressions": 1, "ctr": 0.0, "position": 1.0},
            "pakistan_performance": {
                "rows": [
                    {
                        "page": "https://aitoolszone.tech/non-existent-page-123/",
                        "query": "random query",
                        "device": "DESKTOP",
                        "date": "2026-11-01",
                        "clicks": 0,
                        "impressions": 5,
                    }
                ]
            },
        }
        ga4_unmatched = {
            "organic_landing_performance": {
                "rows": [
                    {
                        "landing_page": "(not set)",
                        "device_category": "desktop",
                        "date": "20261101",
                        "sessions": 2,
                        "total_users": 2,
                    },
                    {
                        "landing_page": "/staging-test-route/",
                        "device_category": "mobile",
                        "date": "20261101",
                        "sessions": 1,
                        "total_users": 1,
                    },
                ]
            }
        }

        payload = normalize_telemetry(gsc_data=gsc_unmatched, ga4_data=ga4_unmatched)

        # Canonical count matches expected contract count
        self.assertEqual(len(payload["correlated_routes"]), self.expected_count)

        # Unmatched entries recorded in diagnostics
        unmatched_gsc = payload["unmatched_records"]["gsc_urls"]
        unmatched_ga4 = payload["unmatched_records"]["ga4_landing_pages"]

        self.assertEqual(len(unmatched_gsc), 1)
        self.assertEqual(unmatched_gsc[0]["normalized_path"], "/non-existent-page-123/")

        self.assertEqual(len(unmatched_ga4), 2)
        ga4_paths = [r["normalized_path"] for r in unmatched_ga4]
        self.assertIn("(not set)", ga4_paths)
        self.assertIn("/staging-test-route/", ga4_paths)

    # 5. GSC/GA4 metric separation
    def test_05_gsc_ga4_metric_separation(self):
        payload = normalize_telemetry(gsc_data=self.mock_gsc, ga4_data=self.mock_ga4)

        pricing = next(r for r in payload["correlated_routes"] if r["canonical_route"] == "/pricing/")
        gsc_block = pricing["gsc_performance"]
        ga4_block = pricing["ga4_performance"]

        # GSC contains clicks/impressions; does not contain sessions
        self.assertIn("clicks", gsc_block)
        self.assertIn("impressions", gsc_block)
        self.assertNotIn("sessions", gsc_block)
        self.assertEqual(gsc_block["clicks"], 2)
        self.assertEqual(gsc_block["impressions"], 10)

        # GA4 contains sessions/users; does not contain clicks
        self.assertIn("sessions", ga4_block)
        self.assertIn("total_users", ga4_block)
        self.assertNotIn("clicks", ga4_block)
        self.assertEqual(ga4_block["sessions"], 4)
        self.assertEqual(ga4_block["total_users"], 4)

        # Summary keeps them strictly decoupled
        summary = payload["summary"]
        self.assertEqual(summary["gsc_site_totals"]["clicks"], 8)
        self.assertEqual(summary["ga4_organic_sessions"], 12)
        self.assertNotIn("total_clicks_and_sessions", summary)

    # 6. Missing source data
    def test_06_missing_source_data(self):
        with self.assertRaises(NormalizationError) as ctx:
            normalize_telemetry(gsc_data=None, ga4_data=None)
        self.assertIn("Both GSC and GA4 datasets are missing", str(ctx.exception))

    # 7. Empty datasets
    def test_07_empty_datasets(self):
        empty_gsc = {"site_totals": {"is_empty": True, "clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}}
        empty_ga4 = {
            "organic_landing_performance": {"rows": []},
            "whatsapp_lead_performance": {"rows": []},
            "ai_assistant_traffic": {"rows": []},
        }

        payload = normalize_telemetry(gsc_data=empty_gsc, ga4_data=empty_ga4)
        self.assertEqual(payload["collection_status"], "empty")
        self.assertEqual(payload["summary"]["ga4_organic_sessions"], 0)
        self.assertEqual(payload["summary"]["gsc_site_totals"]["clicks"], 0)

    # 8. Duplicate records handling
    def test_08_duplicate_records_handling(self):
        gsc_with_dupes = {
            "site_totals": {"clicks": 2, "impressions": 20, "ctr": 0.1, "position": 5.0},
            "pakistan_performance": {
                "rows": [
                    {"page": "/pricing/", "query": "pricing query", "device": "DESKTOP", "date": "2026-11-01", "clicks": 1, "impressions": 10},
                    {"page": "/pricing/", "query": "pricing query", "device": "DESKTOP", "date": "2026-11-01", "clicks": 1, "impressions": 10},  # duplicate
                ]
            },
        }
        payload = normalize_telemetry(gsc_data=gsc_with_dupes, ga4_data=None)

        warnings = payload["data_quality"]["validation_warnings"]
        self.assertTrue(any("Duplicate GSC row detected" in w for w in warnings))

        # Check pricing route has only 1 deduplicated row counted
        pricing = next(r for r in payload["correlated_routes"] if r["canonical_route"] == "/pricing/")
        self.assertEqual(pricing["gsc_performance"]["clicks"], 1)
        self.assertEqual(pricing["gsc_performance"]["impressions"], 10)

    # 9. Invalid dates and URLs
    def test_09_invalid_dates_and_urls(self):
        # Invalid date format
        with self.assertRaises(NormalizationError):
            normalize_date("2026/11/01")

        with self.assertRaises(NormalizationError):
            normalize_date("bad-date")

        # Invalid date range (start > end)
        with self.assertRaises(NormalizationError):
            validate_date_range("2026-11-15", "2026-11-01")

        # Valid date formats
        self.assertEqual(normalize_date("20261105"), "2026-11-05")
        self.assertEqual(normalize_date("2026-11-05"), "2026-11-05")
        self.assertEqual(normalize_date("2026-11-05T12:00:00Z"), "2026-11-05")

        # URL normalization
        self.assertEqual(normalize_url_path("(not set)"), "(not set)")
        self.assertEqual(normalize_url_path(""), "(not set)")
        self.assertEqual(normalize_url_path("https://aitoolszone.tech/PRODUCTS/Canva-pro-edu"), "/products/canva-pro-edu/")

    # 10. Schema validation
    def test_10_schema_validation(self):
        payload = normalize_telemetry(gsc_data=self.mock_gsc, ga4_data=self.mock_ga4)
        validate_normalized_payload(payload)

        # Missing required key
        invalid_payload = dict(payload)
        del invalid_payload["summary"]
        with self.assertRaises(NormalizationError):
            validate_normalized_payload(invalid_payload)

        # Invalid schema version
        bad_version = dict(payload)
        bad_version["schema_version"] = "9.9.9"
        with self.assertRaises(NormalizationError):
            validate_normalized_payload(bad_version)

        # Route count violation
        tampered_routes = dict(payload)
        tampered_routes["correlated_routes"] = payload["correlated_routes"][:50]
        with self.assertRaises(NormalizationError):
            validate_normalized_payload(tampered_routes)

    # 11. Immutable archive behavior
    def test_11_immutable_archive_behavior(self):
        payload = normalize_telemetry(gsc_data=self.mock_gsc, ga4_data=self.mock_ga4)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # First write succeeds
            saved_file = save_telemetry_snapshot(payload, archive_dir=tmp_path, filename="test_snap.json")
            self.assertTrue(saved_file.exists())

            # Second write to identical path raises ImmutableArchiveError
            with self.assertRaises(ImmutableArchiveError) as ctx:
                save_telemetry_snapshot(payload, archive_dir=tmp_path, filename="test_snap.json")
            self.assertIn("Immutable archive violation", str(ctx.exception))

    # 12. Atomic write behavior
    def test_12_atomic_write_behavior(self):
        payload = normalize_telemetry(gsc_data=self.mock_gsc, ga4_data=self.mock_ga4)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            saved_path = save_telemetry_snapshot(payload, archive_dir=tmp_path)

            self.assertTrue(saved_path.exists())
            # Ensure no temporary files left behind
            temp_files = list(tmp_path.glob("tmp_telemetry_*"))
            self.assertEqual(len(temp_files), 0)

            # Confirm file contains valid readable JSON
            with open(saved_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            self.assertEqual(loaded["schema_version"], SCHEMA_VERSION)
            self.assertEqual(loaded["summary"]["canonical_route_count"], self.expected_count)

    # 13. Partial collection handling
    def test_13_partial_collection_handling(self):
        # GSC only
        payload_gsc_only = normalize_telemetry(gsc_data=self.mock_gsc, ga4_data=None)
        self.assertEqual(payload_gsc_only["collection_status"], "partial")
        self.assertTrue(payload_gsc_only["data_quality"]["completeness"]["gsc_available"])
        self.assertFalse(payload_gsc_only["data_quality"]["completeness"]["ga4_available"])

        # GA4 only
        payload_ga4_only = normalize_telemetry(gsc_data=None, ga4_data=self.mock_ga4)
        self.assertEqual(payload_ga4_only["collection_status"], "partial")
        self.assertFalse(payload_ga4_only["data_quality"]["completeness"]["gsc_available"])
        self.assertTrue(payload_ga4_only["data_quality"]["completeness"]["ga4_available"])

    # 14. Credential and token redaction
    def test_14_credential_and_token_redaction(self):
        # Test secret scanner detects ya29 tokens
        with self.assertRaises(NormalizationError):
            scan_for_secrets({"token": "Bearer ya29.a0AfH6SMtestFakeToken"})

        # Test secret scanner detects AIza keys
        with self.assertRaises(NormalizationError):
            scan_for_secrets({"api_key": "AIzaSyD_testFakeKey12345"})

        # Test secret scanner detects private key block
        with self.assertRaises(NormalizationError):
            scan_for_secrets(["-----BEGIN RSA PRIVATE KEY-----"])

        # Clean payload passes without error
        clean_payload = normalize_telemetry(gsc_data=self.mock_gsc, ga4_data=self.mock_ga4)
        scan_for_secrets(clean_payload)  # No exception

    # 15. Indexation classification rules (Stage 6R Remediation)
    def test_15_indexation_classification_rules(self):
        # 1. Submitted and indexed -> INDEXED
        self.assertEqual(
            classify_route_indexation({"verdict": "PASS", "coverage_state": "Submitted and indexed"}),
            "INDEXED"
        )
        self.assertEqual(
            classify_route_indexation({"verdict": "PASS", "coverage_state": "Indexed, not submitted in sitemap"}),
            "INDEXED"
        )

        # 2. Discovered — currently not indexed -> PENDING (never INDEXED)
        self.assertEqual(
            classify_route_indexation({"verdict": "NEUTRAL", "coverage_state": "Discovered – currently not indexed"}),
            "PENDING"
        )
        self.assertEqual(
            classify_route_indexation({"verdict": "NEUTRAL", "coverage_state": "Discovered - currently not indexed"}),
            "PENDING"
        )

        # 3. Crawled — currently not indexed -> PENDING (never INDEXED)
        self.assertEqual(
            classify_route_indexation({"verdict": "NEUTRAL", "coverage_state": "Crawled - currently not indexed"}),
            "PENDING"
        )
        self.assertEqual(
            classify_route_indexation({"verdict": "NEUTRAL", "coverage_state": "Crawled – currently not indexed"}),
            "PENDING"
        )

        # 4. URL is unknown to Google -> PENDING
        self.assertEqual(
            classify_route_indexation({"verdict": "NEUTRAL", "coverage_state": "URL is unknown to Google"}),
            "PENDING"
        )

        # 5. NOT_INSPECTED
        self.assertEqual(classify_route_indexation({"verdict": "NOT_INSPECTED"}), "NOT_INSPECTED")
        self.assertEqual(classify_route_indexation({"coverage_state": "Not Inspected"}), "NOT_INSPECTED")
        self.assertEqual(classify_route_indexation(None), "NOT_INSPECTED")
        self.assertEqual(classify_route_indexation({}), "NOT_INSPECTED")

        # 6. Missing coverage state
        self.assertEqual(classify_route_indexation({"verdict": "PASS", "coverage_state": None}), "INDEXED")
        self.assertEqual(classify_route_indexation({"verdict": "NEUTRAL", "coverage_state": None}), "PENDING")

        # 7. Unexpected coverage text
        self.assertEqual(
            classify_route_indexation({"verdict": "NEUTRAL", "coverage_state": "unexpected text from googlebot"}),
            "PENDING"
        )

        # 8. Case and whitespace variations
        self.assertEqual(
            classify_route_indexation({"verdict": "pass", "coverage_state": "  SUBMITTED AND INDEXED  "}),
            "INDEXED"
        )
        self.assertEqual(
            classify_route_indexation({"verdict": "neutral", "coverage_state": "  Discovered – Currently Not Indexed  "}),
            "PENDING"
        )

        # 9. Conflicting verdict and coverage values
        # Verdict FAIL overrides positive coverage -> ERROR (never INDEXED)
        self.assertEqual(
            classify_route_indexation({"verdict": "FAIL", "coverage_state": "Submitted and indexed"}),
            "ERROR"
        )
        # Coverage "not indexed" prevents false indexation claim even if verdict is PASS -> PENDING
        self.assertEqual(
            classify_route_indexation({"verdict": "PASS", "coverage_state": "Crawled - currently not indexed"}),
            "PENDING"
        )
        # Blocked coverage with PASS verdict -> ERROR
        self.assertEqual(
            classify_route_indexation({"verdict": "PASS", "coverage_state": "Blocked by robots.txt"}),
            "ERROR"
        )

        # 10. API errors
        self.assertEqual(
            classify_route_indexation({"verdict": "API_ERROR", "coverage_state": "api_error: HTTP 429"}),
            "API_ERROR"
        )

    # 16. Eight previously misclassified routes corrected (Stage 6R Remediation)
    def test_16_eight_misclassified_routes_corrected(self):
        # The 8 specific routes identified in the Stage 6 audit:
        # 7 with "Discovered – currently not indexed" and 1 with "Crawled - currently not indexed"
        routes_to_test = [
            ("/blog/ai-agency-automation-pakistan-n8n-make/", "NEUTRAL", "Discovered – currently not indexed"),
            ("/blog/best-ai-tools-for-students-pakistan/", "NEUTRAL", "Discovered – currently not indexed"),
            ("/blog/canva-pro-vs-adobe-creative-cloud-pakistan-freelancers/", "NEUTRAL", "Discovered – currently not indexed"),
            ("/products/linkedin-premium/", "NEUTRAL", "Discovered – currently not indexed"),
            ("/products/microsoft-office-365/", "NEUTRAL", "Discovered – currently not indexed"),
            ("/products/perplexity-pro/", "NEUTRAL", "Discovered – currently not indexed"),
            ("/products/replit-core/", "NEUTRAL", "Crawled - currently not indexed"),
            ("/products/youtube-premium/", "NEUTRAL", "Discovered – currently not indexed"),
        ]

        # 1. Direct classification verification: all 8 must evaluate to PENDING, 0 to INDEXED
        for route_path, verdict, coverage in routes_to_test:
            insp = {"verdict": verdict, "coverage_state": coverage}
            self.assertEqual(
                classify_route_indexation(insp),
                "PENDING",
                f"Route {route_path} was misclassified! Expected PENDING, got {classify_route_indexation(insp)}"
            )

        # 2. Integration verification: normalize a dataset containing these routes
        inspections = [
            {
                "route": route_path,
                "inspection_url": f"https://aitoolszone.tech{route_path}",
                "verdict": verdict,
                "coverage_state": coverage,
            }
            for route_path, verdict, coverage in routes_to_test
        ]
        # Add 1 genuinely indexed route
        inspections.append({
            "route": "/",
            "inspection_url": "https://aitoolszone.tech/",
            "verdict": "PASS",
            "coverage_state": "Submitted and indexed",
        })

        gsc_mock = {
            "site_totals": {"clicks": 1, "impressions": 10, "ctr": 0.1, "position": 5.0, "is_empty": False, "data_state": "final"},
            "url_inspection_sweep": {
                "total_expected": len(self.canonical_routes),
                "inspected_routes": inspections,
            }
        }

        payload = normalize_telemetry(gsc_data=gsc_mock, ga4_data=None)

        # Exactly 1 route should be counted in canonical_indexed_count (the '/' route)
        self.assertEqual(payload["summary"]["canonical_indexed_count"], 1)

        # All 8 tested routes should be counted in pending count
        self.assertGreaterEqual(payload["summary"]["canonical_pending_count"], 8)


if __name__ == "__main__":
    unittest.main()
