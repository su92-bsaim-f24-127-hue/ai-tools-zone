"""Unit tests for AI Tools Zone Google Search Console Data Collection Engine (Stage 2).

Covers all 10 required test criteria using mocked API responses:
1. Successful site totals response.
2. Empty Search Analytics response.
3. Pakistan country filter correctness.
4. Pagination behavior.
5. Successful URL inspection parsing.
6. All 97 routes being processed.
7. Rate limiting.
8. Retry behavior for transient failures.
9. Permanent failure recording.
10. Credential redaction in logs.
"""

import time
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
import httplib2
from googleapiclient.errors import HttpError

from scripts.telemetry.gsc_client import (
    RateLimiter,
    get_site_totals,
    get_pakistan_performance,
    inspect_canonical_routes,
    _safe_error_message,
    _is_transient_error,
)
from scripts.telemetry.config import get_canonical_routes, get_expected_page_count


def make_http_error(status: int, reason: str = "Error") -> HttpError:
    resp = httplib2.Response({"status": str(status), "reason": reason})
    return HttpError(resp, b"{\"error\": {\"message\": \"test error\"}}")


class TestGSCClient(unittest.TestCase):

    def setUp(self):
        self.mock_service = MagicMock()

    # 1. Successful site totals response
    def test_01_successful_site_totals(self):
        mock_response = {
            "rows": [
                {
                    "clicks": 1420,
                    "impressions": 48500,
                    "ctr": 0.029278,
                    "position": 14.2,
                }
            ],
            "responseAggregationType": "byProperty",
        }
        self.mock_service.searchanalytics().query().execute.return_value = mock_response

        res = get_site_totals("2026-10-15", "2026-11-11", service=self.mock_service)

        self.assertFalse(res["is_empty"])
        self.assertEqual(res["clicks"], 1420)
        self.assertEqual(res["impressions"], 48500)
        self.assertAlmostEqual(res["ctr"], 0.029278)
        self.assertAlmostEqual(res["position"], 14.2)
        self.assertEqual(res["date_range"], {"start_date": "2026-10-15", "end_date": "2026-11-11"})

        # Verify dimensionless body (no dimensions key)
        call_kwargs = self.mock_service.searchanalytics().query.call_args[1]
        body = call_kwargs["body"]
        self.assertNotIn("dimensions", body)
        self.assertEqual(body["dataState"], "final")

    # 2. Empty Search Analytics response
    def test_02_empty_site_totals(self):
        self.mock_service.searchanalytics().query().execute.return_value = {}

        res = get_site_totals("2026-10-15", "2026-11-11", service=self.mock_service)

        self.assertTrue(res["is_empty"])
        self.assertEqual(res["clicks"], 0)
        self.assertEqual(res["impressions"], 0)
        self.assertEqual(res["ctr"], 0.0)
        self.assertEqual(res["position"], 0.0)

    # 3. Pakistan country filter correctness
    def test_03_pakistan_country_filter(self):
        mock_response = {
            "rows": [
                {
                    "keys": ["https://aitoolszone.tech/products/chatgpt-plus/", "chatgpt pakistan", "DESKTOP", "2026-11-01"],
                    "clicks": 5,
                    "impressions": 100,
                    "ctr": 0.05,
                    "position": 3.0,
                }
            ]
        }
        self.mock_service.searchanalytics().query().execute.return_value = mock_response

        res = get_pakistan_performance("2026-10-15", "2026-11-11", service=self.mock_service)

        call_kwargs = self.mock_service.searchanalytics().query.call_args[1]
        body = call_kwargs["body"]
        self.assertIn("dimensionFilterGroups", body)
        filter_group = body["dimensionFilterGroups"][0]["filters"][0]
        self.assertEqual(filter_group["dimension"], "country")
        self.assertEqual(filter_group["operator"], "equals")
        self.assertEqual(filter_group["expression"], "pak")
        self.assertEqual(body["dataState"], "final")

        self.assertEqual(res["total_rows"], 1)
        self.assertEqual(res["country_filter"], "pak")
        row = res["rows"][0]
        self.assertEqual(row["page"], "https://aitoolszone.tech/products/chatgpt-plus/")
        self.assertEqual(row["query"], "chatgpt pakistan")
        self.assertEqual(row["device"], "DESKTOP")
        self.assertEqual(row["date"], "2026-11-01")
        self.assertEqual(row["clicks"], 5)

    # 4. Pagination behavior
    def test_04_pagination_behavior(self):
        batch_1 = {
            "rows": [
                {"keys": ["https://aitoolszone.tech/page1/", "q1", "DESKTOP", "2026-11-01"], "clicks": 1, "impressions": 10, "ctr": 0.1, "position": 1.0},
                {"keys": ["https://aitoolszone.tech/page2/", "q2", "MOBILE", "2026-11-01"], "clicks": 2, "impressions": 20, "ctr": 0.1, "position": 2.0},
            ]
        }
        batch_2 = {
            "rows": [
                {"keys": ["https://aitoolszone.tech/page3/", "q3", "DESKTOP", "2026-11-02"], "clicks": 3, "impressions": 30, "ctr": 0.1, "position": 3.0},
            ]
        }
        # First call returns 2 rows (full batch of size 2), second call returns 1 row (< batch_size, stopping pagination)
        self.mock_service.searchanalytics().query().execute.side_effect = [batch_1, batch_2]
        self.mock_service.searchanalytics().query.reset_mock()

        res = get_pakistan_performance("2026-10-15", "2026-11-11", service=self.mock_service, row_limit=2)

        self.assertEqual(self.mock_service.searchanalytics().query.call_count, 2)
        # Verify startRow values
        call1_body = self.mock_service.searchanalytics().query.call_args_list[0][1]["body"]
        call2_body = self.mock_service.searchanalytics().query.call_args_list[1][1]["body"]
        self.assertEqual(call1_body["startRow"], 0)
        self.assertEqual(call2_body["startRow"], 2)

        self.assertEqual(res["total_rows"], 3)
        self.assertEqual(len(res["rows"]), 3)

    # 5. Successful URL inspection parsing
    def test_05_successful_url_inspection(self):
        mock_resp = {
            "inspectionResult": {
                "inspectionResultLink": "https://search.google.com/search-console/inspect?id=123",
                "indexStatusResult": {
                    "verdict": "PASS",
                    "coverageState": "Submitted and indexed",
                    "robotsTxtState": "ALLOWED",
                    "indexingState": "INDEXING_ALLOWED",
                    "pageFetchState": "SUCCESSFUL",
                    "lastCrawlTime": "2026-11-10T12:00:00Z",
                    "googleCanonical": "https://aitoolszone.tech/pricing/",
                    "userCanonical": "https://aitoolszone.tech/pricing/",
                    "crawledAs": "MOBILE",
                    "referringUrls": ["https://aitoolszone.tech/"],
                },
                "richResultsResult": {"verdict": "PASS"},
            }
        }
        self.mock_service.urlInspection().index().inspect().execute.return_value = mock_resp

        with patch("scripts.telemetry.gsc_client.get_canonical_routes", return_value=["/pricing/"]):
            res = inspect_canonical_routes(service=self.mock_service, max_rps=100.0)

        self.assertEqual(res["total_attempted"], 1)
        self.assertEqual(res["total_successful"], 1)
        self.assertEqual(res["total_failed"], 0)
        item = res["inspected_routes"][0]
        self.assertEqual(item["route"], "/pricing/")
        self.assertEqual(item["verdict"], "PASS")
        self.assertEqual(item["coverage_state"], "Submitted and indexed")
        self.assertEqual(item["robots_txt_state"], "ALLOWED")
        self.assertEqual(item["indexing_state"], "INDEXING_ALLOWED")
        self.assertEqual(item["google_canonical"], "https://aitoolszone.tech/pricing/")
        self.assertEqual(item["user_canonical"], "https://aitoolszone.tech/pricing/")
        self.assertEqual(item["crawled_as"], "MOBILE")
        self.assertEqual(item["referring_urls"], ["https://aitoolszone.tech/"])

    # 6. All routes being processed
    def test_06_all_routes_processed(self):
        routes = get_canonical_routes()
        expected = get_expected_page_count()
        self.assertEqual(len(routes), expected)

        mock_resp = {
            "inspectionResult": {
                "indexStatusResult": {
                    "verdict": "PASS",
                    "coverageState": "Submitted and indexed",
                }
            }
        }
        self.mock_service.urlInspection().index().inspect().execute.return_value = mock_resp
        self.mock_service.urlInspection().index().inspect.reset_mock()

        # Mock RateLimiter to run instantaneously in tests
        with patch.object(RateLimiter, "acquire", return_value=0.0):
            res = inspect_canonical_routes(service=self.mock_service)

        self.assertEqual(res["total_expected"], expected)
        self.assertEqual(res["total_attempted"], expected)
        self.assertEqual(res["total_successful"], expected)
        self.assertEqual(res["total_failed"], 0)
        self.assertEqual(len(res["inspected_routes"]), expected)
        self.assertEqual(self.mock_service.urlInspection().index().inspect.call_count, expected)

    # 7. Rate limiting behavior
    def test_07_rate_limiter_timing(self):
        limiter = RateLimiter(max_rps=20.0)  # 0.05s min interval
        t0 = time.time()
        for _ in range(3):
            limiter.acquire()
        t1 = time.time()
        # 3 calls at 20 rps require at least 2 interval sleeps (>= 0.09s)
        self.assertGreaterEqual(t1 - t0, 0.08)

    # 8. Retry behavior for transient failures
    def test_08_retry_on_transient_error(self):
        error_429 = make_http_error(429, "Too Many Requests")
        mock_success = {
            "inspectionResult": {
                "indexStatusResult": {
                    "verdict": "PASS",
                    "coverageState": "Submitted and indexed",
                }
            }
        }
        # Fail twice with 429, succeed on third attempt
        self.mock_service.urlInspection().index().inspect().execute.side_effect = [
            error_429,
            error_429,
            mock_success,
        ]
        self.mock_service.urlInspection().index().inspect.reset_mock()

        with patch("scripts.telemetry.gsc_client.get_canonical_routes", return_value=["/about/"]):
            with patch("time.sleep", return_value=None):  # Fast backoff
                res = inspect_canonical_routes(service=self.mock_service, max_retries=3)

        self.assertEqual(res["total_attempted"], 1)
        self.assertEqual(res["total_successful"], 1)
        self.assertEqual(res["total_failed"], 0)
        self.assertEqual(self.mock_service.urlInspection().index().inspect.call_count, 3)

    # 9. Permanent failure recording
    def test_09_permanent_failure_recorded_separately(self):
        error_500 = make_http_error(500, "Internal Server Error")
        self.mock_service.urlInspection().index().inspect().execute.side_effect = error_500

        with patch("scripts.telemetry.gsc_client.get_canonical_routes", return_value=["/faq/"]):
            with patch("time.sleep", return_value=None):
                res = inspect_canonical_routes(service=self.mock_service, max_retries=2)

        self.assertEqual(res["total_attempted"], 1)
        self.assertEqual(res["total_successful"], 0)
        self.assertEqual(res["total_failed"], 1)
        self.assertEqual(len(res["failed_inspections"]), 1)
        failure = res["failed_inspections"][0]
        self.assertEqual(failure["route"], "/faq/")
        self.assertEqual(failure["error_type"], "HttpError")

    # 10. Credential redaction in logs
    def test_10_credential_redaction(self):
        exc_with_token = Exception("Request failed with Bearer ya29.a0AfH6SMtest_fake_token_12345 in header")
        sanitized = _safe_error_message(exc_with_token)
        self.assertNotIn("ya29.", sanitized)
        self.assertNotIn("test_fake_token", sanitized)
        self.assertIn("[REDACTED_CREDENTIAL]", sanitized)

        exc_with_key = Exception("Invalid key=AIzaSyDtestKey98765 parameter")
        sanitized_key = _safe_error_message(exc_with_key)
        self.assertNotIn("AIzaSyD", sanitized_key)
        self.assertIn("[REDACTED_CREDENTIAL]", sanitized_key)

    # 11. Single route targeted inspection (Stage 6R Remediation)
    def test_11_single_route_inspection(self):
        target = "/blog/cheap-ai-tools-for-students-pakistan/"
        mock_resp = {
            "inspectionResult": {
                "indexStatusResult": {
                    "verdict": "NEUTRAL",
                    "coverageState": "URL is unknown to Google",
                }
            }
        }
        self.mock_service.urlInspection().index().inspect().execute.return_value = mock_resp
        self.mock_service.urlInspection().index().inspect.reset_mock()

        with patch.object(RateLimiter, "acquire", return_value=0.0):
            res = inspect_canonical_routes(service=self.mock_service, routes=[target])

        self.assertEqual(res["total_expected"], 1)
        self.assertEqual(res["total_attempted"], 1)
        self.assertEqual(res["total_successful"], 1)
        self.assertEqual(res["total_failed"], 0)
        self.assertEqual(len(res["inspected_routes"]), 1)
        self.assertEqual(res["inspected_routes"][0]["route"], target)
        self.assertEqual(res["inspected_routes"][0]["coverage_state"], "URL is unknown to Google")
        self.assertEqual(self.mock_service.urlInspection().index().inspect.call_count, 1)


if __name__ == "__main__":
    unittest.main()
