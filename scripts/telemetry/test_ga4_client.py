"""Unit tests for AI Tools Zone Google Analytics 4 Data Collection Engine (Stage 3).

Covers all 12 required test criteria using mocked API responses:
1. Successful organic traffic retrieval.
2. Empty response.
3. Pakistan country filtering.
4. Organic channel filtering.
5. AI referral classification.
6. Missing AI referral data.
7. WhatsApp event retrieval.
8. Missing conversion events.
9. Pagination.
10. Quota monitoring.
11. Abort below 500 remaining tokens.
12. Credential redaction.
"""

import unittest
from unittest.mock import MagicMock
import httplib2
from googleapiclient.errors import HttpError

from scripts.telemetry.ga4_client import (
    QuotaTracker,
    GA4QuotaExhaustedError,
    GA4ClientError,
    get_organic_landing_page_performance,
    get_ai_assistant_traffic,
    get_whatsapp_lead_performance,
    _safe_error_message,
    _classify_ai_source,
)


def make_http_error(status: int, reason: str = "Error") -> HttpError:
    resp = httplib2.Response({"status": str(status), "reason": reason})
    return HttpError(resp, b"{\"error\": {\"message\": \"test error\"}}")


class TestGA4Client(unittest.TestCase):

    def setUp(self):
        self.mock_service = MagicMock()

    # 1. Successful organic traffic retrieval
    def test_01_successful_organic_traffic_retrieval(self):
        mock_resp = {
            "rows": [
                {
                    "dimensionValues": [{"value": "/blog/how-to-pay-for-chatgpt-plus-pakistan/"}, {"value": "mobile"}, {"value": "20261105"}],
                    "metricValues": [{"value": "12"}, {"value": "10"}, {"value": "8"}, {"value": "0.6667"}, {"value": "45.2"}],
                }
            ],
            "propertyQuota": {
                "tokensPerDay": {"consumed": 2, "remaining": 199998},
                "tokensPerHour": {"consumed": 2, "remaining": 39998},
            },
        }
        self.mock_service.properties().runReport().execute.return_value = mock_resp
        self.mock_service.properties().runReport.reset_mock()

        res = get_organic_landing_page_performance("28daysAgo", "yesterday", service=self.mock_service)

        self.assertFalse(res["is_empty"])
        self.assertEqual(res["total_rows"], 1)
        self.assertEqual(res["total_sessions"], 12)
        self.assertEqual(res["total_users"], 10)
        self.assertEqual(res["total_engaged_sessions"], 8)
        row = res["rows"][0]
        self.assertEqual(row["landing_page"], "/blog/how-to-pay-for-chatgpt-plus-pakistan/")
        self.assertEqual(row["device_category"], "mobile")
        self.assertEqual(row["date"], "20261105")
        self.assertEqual(row["sessions"], 12)
        self.assertAlmostEqual(row["engagement_rate"], 0.6667)
        self.assertAlmostEqual(row["average_session_duration"], 45.2)

    # 2. Empty response
    def test_02_empty_organic_response(self):
        self.mock_service.properties().runReport().execute.return_value = {"rows": []}
        self.mock_service.properties().runReport.reset_mock()

        res = get_organic_landing_page_performance("28daysAgo", "yesterday", service=self.mock_service)

        self.assertTrue(res["is_empty"])
        self.assertEqual(res["total_rows"], 0)
        self.assertEqual(res["total_sessions"], 0)
        self.assertEqual(res["total_users"], 0)
        self.assertEqual(res["rows"], [])

    # 3. Pakistan country filtering
    def test_03_pakistan_country_filtering(self):
        self.mock_service.properties().runReport().execute.return_value = {"rows": []}
        self.mock_service.properties().runReport.reset_mock()

        get_organic_landing_page_performance("28daysAgo", "yesterday", service=self.mock_service)

        call_kwargs = self.mock_service.properties().runReport.call_args[1]
        body = call_kwargs["body"]
        expressions = body["dimensionFilter"]["andGroup"]["expressions"]
        country_filter = next(
            e["filter"] for e in expressions if e["filter"]["fieldName"] == "country"
        )
        self.assertEqual(country_filter["stringFilter"]["matchType"], "EXACT")
        self.assertEqual(country_filter["stringFilter"]["value"], "Pakistan")

    # 4. Organic channel filtering
    def test_04_organic_channel_filtering(self):
        self.mock_service.properties().runReport().execute.return_value = {"rows": []}
        self.mock_service.properties().runReport.reset_mock()

        get_organic_landing_page_performance("28daysAgo", "yesterday", service=self.mock_service)

        call_kwargs = self.mock_service.properties().runReport.call_args[1]
        body = call_kwargs["body"]
        expressions = body["dimensionFilter"]["andGroup"]["expressions"]
        channel_filter = next(
            e["filter"] for e in expressions if e["filter"]["fieldName"] == "sessionDefaultChannelGroup"
        )
        self.assertEqual(channel_filter["stringFilter"]["matchType"], "EXACT")
        self.assertEqual(channel_filter["stringFilter"]["value"], "Organic Search")

    # 5. AI referral classification
    def test_05_ai_referral_classification(self):
        mock_resp = {
            "rows": [
                {
                    "dimensionValues": [{"value": "chat.openai.com"}, {"value": "referral"}, {"value": "/pricing/"}, {"value": "20261101"}],
                    "metricValues": [{"value": "5"}, {"value": "4"}, {"value": "3"}],
                },
                {
                    "dimensionValues": [{"value": "claude.ai"}, {"value": "referral"}, {"value": "/products/claude-pro/"}, {"value": "20261102"}],
                    "metricValues": [{"value": "3"}, {"value": "3"}, {"value": "2"}],
                },
                {
                    "dimensionValues": [{"value": "gemini.google.com"}, {"value": "referral"}, {"value": "/categories/ai-assistants/"}, {"value": "20261103"}],
                    "metricValues": [{"value": "2"}, {"value": "2"}, {"value": "1"}],
                },
                {
                    "dimensionValues": [{"value": "copilot.microsoft.com"}, {"value": "referral"}, {"value": "/"}, {"value": "20261104"}],
                    "metricValues": [{"value": "1"}, {"value": "1"}, {"value": "1"}],
                },
                {
                    "dimensionValues": [{"value": "perplexity.ai"}, {"value": "referral"}, {"value": "/products/perplexity-pro/"}, {"value": "20261105"}],
                    "metricValues": [{"value": "4"}, {"value": "4"}, {"value": "3"}],
                },
            ],
            "propertyQuota": {
                "tokensPerHour": {"consumed": 1, "remaining": 39999},
            },
        }
        self.mock_service.properties().runReport().execute.return_value = mock_resp
        self.mock_service.properties().runReport.reset_mock()

        res = get_ai_assistant_traffic("28daysAgo", "yesterday", service=self.mock_service)

        self.assertFalse(res["is_empty"])
        self.assertEqual(res["total_ai_sessions"], 15)
        self.assertEqual(res["total_ai_users"], 14)
        breakdown = res["platform_breakdown"]
        self.assertEqual(breakdown["ChatGPT"]["sessions"], 5)
        self.assertEqual(breakdown["Claude"]["sessions"], 3)
        self.assertEqual(breakdown["Gemini"]["sessions"], 2)
        self.assertEqual(breakdown["Copilot"]["sessions"], 1)
        self.assertEqual(breakdown["Perplexity"]["sessions"], 4)

    # 6. Missing AI referral data
    def test_06_missing_ai_referral_data(self):
        self.mock_service.properties().runReport().execute.return_value = {"rows": []}
        self.mock_service.properties().runReport.reset_mock()

        res = get_ai_assistant_traffic("28daysAgo", "yesterday", service=self.mock_service)

        self.assertTrue(res["is_empty"])
        self.assertEqual(res["total_ai_sessions"], 0)
        self.assertEqual(res["total_ai_users"], 0)
        self.assertIn("classification_notes", res)

    # 7. WhatsApp event retrieval
    def test_07_whatsapp_event_retrieval(self):
        mock_resp = {
            "rows": [
                {
                    "dimensionValues": [{"value": "whatsapp_click"}, {"value": "/products/chatgpt-plus/"}, {"value": "20261106"}],
                    "metricValues": [{"value": "4"}, {"value": "3"}],
                },
                {
                    "dimensionValues": [{"value": "product_whatsapp_click"}, {"value": "/products/chatgpt-plus/"}, {"value": "20261106"}],
                    "metricValues": [{"value": "4"}, {"value": "3"}],
                },
            ],
            "propertyQuota": {
                "tokensPerHour": {"consumed": 1, "remaining": 39999},
            },
        }
        self.mock_service.properties().runReport().execute.return_value = mock_resp
        self.mock_service.properties().runReport.reset_mock()

        res = get_whatsapp_lead_performance("28daysAgo", "yesterday", service=self.mock_service)

        self.assertFalse(res["is_empty"])
        self.assertEqual(res["total_lead_events"], 8)
        self.assertEqual(res["total_lead_users"], 6)
        self.assertEqual(res["event_summary"]["whatsapp_click"]["event_count"], 4)
        self.assertEqual(res["event_summary"]["whatsapp_click"]["unique_users"], 3)
        self.assertTrue(res["event_summary"]["whatsapp_click"]["detected_in_dataset"])
        self.assertIn("/products/chatgpt-plus/", res["landing_page_summary"])

    # 8. Missing conversion events
    def test_08_missing_conversion_events(self):
        mock_resp = {
            "rows": [
                {
                    "dimensionValues": [{"value": "whatsapp_click"}, {"value": "/"}, {"value": "20261106"}],
                    "metricValues": [{"value": "2"}, {"value": "2"}],
                }
            ]
        }
        self.mock_service.properties().runReport().execute.return_value = mock_resp
        self.mock_service.properties().runReport.reset_mock()

        res = get_whatsapp_lead_performance("28daysAgo", "yesterday", service=self.mock_service)

        summary = res["event_summary"]
        self.assertFalse(summary["generate_lead"]["detected_in_dataset"])
        self.assertEqual(summary["generate_lead"]["event_count"], 0)
        self.assertEqual(summary["generate_lead"]["unique_users"], 0)
        self.assertEqual(summary["generate_lead"]["status"], "0 (no occurrences recorded in date range)")

    # 9. Pagination
    def test_09_pagination(self):
        batch_1 = {
            "rows": [
                {
                    "dimensionValues": [{"value": "/page1/"}, {"value": "desktop"}, {"value": "20261101"}],
                    "metricValues": [{"value": "10"}, {"value": "8"}, {"value": "6"}, {"value": "0.6"}, {"value": "30.0"}],
                },
                {
                    "dimensionValues": [{"value": "/page2/"}, {"value": "mobile"}, {"value": "20261101"}],
                    "metricValues": [{"value": "5"}, {"value": "5"}, {"value": "4"}, {"value": "0.8"}, {"value": "25.0"}],
                },
            ]
        }
        batch_2 = {
            "rows": [
                {
                    "dimensionValues": [{"value": "/page3/"}, {"value": "desktop"}, {"value": "20261102"}],
                    "metricValues": [{"value": "2"}, {"value": "2"}, {"value": "1"}, {"value": "0.5"}, {"value": "15.0"}],
                }
            ]
        }
        self.mock_service.properties().runReport().execute.side_effect = [batch_1, batch_2]
        self.mock_service.properties().runReport.reset_mock()

        res = get_organic_landing_page_performance("28daysAgo", "yesterday", service=self.mock_service, row_limit=2)

        self.assertEqual(self.mock_service.properties().runReport.call_count, 2)
        call1_body = self.mock_service.properties().runReport.call_args_list[0][1]["body"]
        call2_body = self.mock_service.properties().runReport.call_args_list[1][1]["body"]
        self.assertEqual(call1_body["offset"], 0)
        self.assertEqual(call2_body["offset"], 2)
        self.assertEqual(res["total_rows"], 3)
        self.assertEqual(len(res["rows"]), 3)

    # 10. Quota monitoring
    def test_10_quota_monitoring(self):
        tracker = QuotaTracker()
        quota_payload = {
            "tokensPerDay": {"consumed": 5, "remaining": 199995},
            "tokensPerHour": {"consumed": 5, "remaining": 39995},
        }
        tracker.record(quota_payload)
        summary = tracker.to_dict()
        self.assertEqual(summary["requests_executed"], 1)
        self.assertEqual(summary["total_daily_consumed"], 5)
        self.assertEqual(summary["total_hourly_consumed"], 5)
        self.assertEqual(summary["last_remaining_daily"], 199995)
        self.assertEqual(summary["last_remaining_hourly"], 39995)

    # 11. Abort below 500 remaining tokens
    def test_11_abort_below_500_remaining_tokens(self):
        critical_quota = {
            "tokensPerHour": {"consumed": 100, "remaining": 450},
            "tokensPerDay": {"consumed": 100, "remaining": 199900},
        }
        mock_resp = {
            "rows": [],
            "propertyQuota": critical_quota,
        }
        self.mock_service.properties().runReport().execute.return_value = mock_resp
        self.mock_service.properties().runReport.reset_mock()

        with self.assertRaises(GA4QuotaExhaustedError) as ctx:
            get_organic_landing_page_performance("28daysAgo", "yesterday", service=self.mock_service)

        self.assertIn("critically low", str(ctx.exception))
        self.assertIn("450 remaining", str(ctx.exception))

    # 12. Credential redaction
    def test_12_credential_redaction(self):
        exc_with_token = Exception("HTTP 401: Invalid token Bearer ya29.a0AfH6SMfake_ga4_secret_xyz in authorization")
        sanitized = _safe_error_message(exc_with_token)
        self.assertNotIn("ya29.", sanitized)
        self.assertNotIn("fake_ga4_secret", sanitized)
        self.assertIn("[REDACTED_CREDENTIAL]", sanitized)

        exc_with_key = Exception("Request denied for key=AIzaSyD_fake_ga4_key_99999")
        sanitized_key = _safe_error_message(exc_with_key)
        self.assertNotIn("AIzaSyD", sanitized_key)
        self.assertIn("[REDACTED_CREDENTIAL]", sanitized_key)


if __name__ == "__main__":
    unittest.main()
