"""AI Tools Zone — Google Analytics 4 Data Collection Engine (Stage 3).

Reliable, read-only GA4 telemetry collector providing:
1. Organic Search landing-page performance (Organic Search + Pakistan isolation).
2. AI assistant referral traffic (ChatGPT, Claude, Gemini, Copilot, Perplexity identification).
3. Commercial WhatsApp lead tracking (generate_lead, whatsapp_click event tracking).
4. Strict GA4 token quota protection (monitors token budget, aborts below 500 hourly remaining).

Adheres strictly to zero-leak credential isolation and read-only least privilege.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from googleapiclient.errors import HttpError

from .auth import get_ga4_service, mask_identifier
from .config import (
    GA4_PROPERTY_ID,
    GA4_PROPERTY_RESOURCE,
    GA4_READONLY_SCOPE,
)

logger = logging.getLogger("telemetry.ga4")

# Quota budget threshold: abort if remaining hourly tokens fall below this limit
MIN_HOURLY_TOKENS_THRESHOLD: int = 500

# Verified target WhatsApp commercial events
TARGET_WHATSAPP_EVENTS: List[str] = [
    "generate_lead",
    "whatsapp_click",
    "product_whatsapp_click",
]

# AI Assistant signature keywords for source/medium classification
AI_PLATFORM_PATTERNS: Dict[str, List[str]] = {
    "ChatGPT": ["chatgpt", "openai", "chat.openai.com"],
    "Claude": ["claude", "anthropic", "claude.ai"],
    "Gemini": ["gemini", "bard", "gemini.google.com"],
    "Copilot": ["copilot", "bing.com/chat"],
    "Perplexity": ["perplexity", "perplexity.ai"],
}


class GA4QuotaExhaustedError(RuntimeError):
    """Raised when GA4 hourly token budget is exhausted or falls below safety threshold."""
    pass


class GA4ClientError(RuntimeError):
    """General exception for GA4 Data API query failures."""
    pass


class QuotaTracker:
    """Monitors GA4 property token consumption across requests and enforces budget gates."""

    def __init__(self, min_hourly_threshold: int = MIN_HOURLY_TOKENS_THRESHOLD):
        self.min_hourly_threshold = min_hourly_threshold
        self.total_daily_consumed: int = 0
        self.total_hourly_consumed: int = 0
        self.last_remaining_daily: Optional[int] = None
        self.last_remaining_hourly: Optional[int] = None
        self.requests_executed: int = 0

    def record(self, property_quota: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Record quota consumption and enforce safety boundaries."""
        self.requests_executed += 1
        if not property_quota:
            return self.to_dict()

        tokens_per_day = property_quota.get("tokensPerDay", {})
        tokens_per_hour = property_quota.get("tokensPerHour", {})

        consumed_day = tokens_per_day.get("consumed", 0)
        remaining_day = tokens_per_day.get("remaining")
        consumed_hour = tokens_per_hour.get("consumed", 0)
        remaining_hour = tokens_per_hour.get("remaining")

        self.total_daily_consumed += consumed_day
        self.total_hourly_consumed += consumed_hour
        if remaining_day is not None:
            self.last_remaining_daily = remaining_day
        if remaining_hour is not None:
            self.last_remaining_hourly = remaining_hour

        # Quota Safety Gate: Abort if remaining hourly tokens fall below safety threshold
        if remaining_hour is not None and remaining_hour < self.min_hourly_threshold:
            raise GA4QuotaExhaustedError(
                f"GA4 hourly token budget critically low: {remaining_hour} remaining "
                f"(safety threshold: {self.min_hourly_threshold}). Aborting further queries."
            )

        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        """Return serialized snapshot of current quota telemetry."""
        return {
            "requests_executed": self.requests_executed,
            "total_daily_consumed": self.total_daily_consumed,
            "total_hourly_consumed": self.total_hourly_consumed,
            "last_remaining_daily": self.last_remaining_daily,
            "last_remaining_hourly": self.last_remaining_hourly,
            "min_hourly_threshold": self.min_hourly_threshold,
        }


def _safe_error_message(exc: Exception) -> str:
    """Redact potentially sensitive details from error messages."""
    msg = str(exc)
    for sensitive_keyword in ["Bearer", "ya29.", "AIza", "key="]:
        if sensitive_keyword in msg:
            return f"{type(exc).__name__}: [REDACTED_CREDENTIAL]"
    return f"{type(exc).__name__}: {msg}"


def _classify_ai_source(source: str, medium: str) -> str:
    """Classify traffic source into a canonical AI assistant platform or 'Other AI'."""
    lower_source = (source or "").lower()
    lower_medium = (medium or "").lower()
    combined = f"{lower_source} {lower_medium}"

    for platform, patterns in AI_PLATFORM_PATTERNS.items():
        if any(pat in combined for pat in patterns):
            return platform
    return "Other AI"


def get_organic_landing_page_performance(
    start_date: str,
    end_date: str,
    property_id: str = GA4_PROPERTY_RESOURCE,
    service: Optional[Any] = None,
    row_limit: int = 5000,
    max_rows: Optional[int] = None,
    quota_tracker: Optional[QuotaTracker] = None,
) -> Dict[str, Any]:
    """Collect GA4 organic search landing page performance isolated to Pakistan.

    Dimensions:
    - landingPage
    - deviceCategory
    - date

    Metrics:
    - sessions
    - totalUsers
    - engagedSessions
    - engagementRate
    - averageSessionDuration

    Filters:
    - sessionDefaultChannelGroup == 'Organic Search'
    - country == 'Pakistan'
    """
    ga4 = service or get_ga4_service()
    tracker = quota_tracker or QuotaTracker()

    dimension_filter = {
        "andGroup": {
            "expressions": [
                {
                    "filter": {
                        "fieldName": "sessionDefaultChannelGroup",
                        "stringFilter": {
                            "matchType": "EXACT",
                            "value": "Organic Search",
                        },
                    }
                },
                {
                    "filter": {
                        "fieldName": "country",
                        "stringFilter": {
                            "matchType": "EXACT",
                            "value": "Pakistan",
                        },
                    }
                },
            ]
        }
    }

    all_rows: List[Dict[str, Any]] = []
    offset = 0
    batch_size = min(row_limit, 10000)
    collected_at = datetime.now(timezone.utc).isoformat()

    while True:
        body: Dict[str, Any] = {
            "dateRanges": [{"startDate": start_date, "endDate": end_date}],
            "dimensions": [
                {"name": "landingPage"},
                {"name": "deviceCategory"},
                {"name": "date"},
            ],
            "metrics": [
                {"name": "sessions"},
                {"name": "totalUsers"},
                {"name": "engagedSessions"},
                {"name": "engagementRate"},
                {"name": "averageSessionDuration"},
            ],
            "dimensionFilter": dimension_filter,
            "limit": batch_size,
            "offset": offset,
            "returnPropertyQuota": True,
        }

        try:
            resp = ga4.properties().runReport(property=property_id, body=body).execute()
        except HttpError as exc:
            if exc.resp.status in (429, 403) and "quota" in str(exc).lower():
                raise GA4QuotaExhaustedError(_safe_error_message(exc)) from None
            raise GA4ClientError(_safe_error_message(exc)) from None
        except Exception as exc:
            raise GA4ClientError(_safe_error_message(exc)) from None

        # Track and guard quota
        tracker.record(resp.get("propertyQuota"))

        rows = resp.get("rows", [])
        if not rows:
            break

        for r in rows:
            dim_vals = [v.get("value", "") for v in r.get("dimensionValues", [])]
            met_vals = [v.get("value", "0") for v in r.get("metricValues", [])]

            landing_page = dim_vals[0] if len(dim_vals) > 0 else ""
            device_category = dim_vals[1] if len(dim_vals) > 1 else ""
            row_date = dim_vals[2] if len(dim_vals) > 2 else ""

            sessions = int(met_vals[0]) if len(met_vals) > 0 else 0
            total_users = int(met_vals[1]) if len(met_vals) > 1 else 0
            engaged_sessions = int(met_vals[2]) if len(met_vals) > 2 else 0
            engagement_rate = float(met_vals[3]) if len(met_vals) > 3 else 0.0
            avg_duration = float(met_vals[4]) if len(met_vals) > 4 else 0.0

            all_rows.append({
                "landing_page": landing_page,
                "device_category": device_category,
                "date": row_date,
                "sessions": sessions,
                "total_users": total_users,
                "engaged_sessions": engaged_sessions,
                "engagement_rate": engagement_rate,
                "average_session_duration": avg_duration,
            })

        if len(rows) < batch_size:
            break

        offset += len(rows)
        if max_rows and len(all_rows) >= max_rows:
            all_rows = all_rows[:max_rows]
            break

    total_sessions = sum(r["sessions"] for r in all_rows)
    total_users_sum = sum(r["total_users"] for r in all_rows)
    total_engaged = sum(r["engaged_sessions"] for r in all_rows)

    return {
        "property": property_id,
        "collected_at": collected_at,
        "date_range": {"start_date": start_date, "end_date": end_date},
        "filters": {
            "channel_group": "Organic Search",
            "country": "Pakistan",
        },
        "total_rows": len(all_rows),
        "total_sessions": total_sessions,
        "total_users": total_users_sum,
        "total_engaged_sessions": total_engaged,
        "is_empty": len(all_rows) == 0,
        "rows": all_rows,
        "quota": tracker.to_dict(),
    }


def get_ai_assistant_traffic(
    start_date: str,
    end_date: str,
    property_id: str = GA4_PROPERTY_RESOURCE,
    service: Optional[Any] = None,
    row_limit: int = 5000,
    max_rows: Optional[int] = None,
    quota_tracker: Optional[QuotaTracker] = None,
) -> Dict[str, Any]:
    """Identify and collect referral traffic from AI Assistants (ChatGPT, Claude, Gemini, Copilot, Perplexity).

    Queries available sessionSource and sessionMedium dimensions using partial regex matching.
    Reports actual source/medium values observed and documents classification limitations.
    """
    ga4 = service or get_ga4_service()
    tracker = quota_tracker or QuotaTracker()
    collected_at = datetime.now(timezone.utc).isoformat()

    # Match verified AI assistant domains and platforms
    ai_regex = "(?i)(chatgpt|openai|claude|anthropic|gemini|bard|copilot|perplexity)"

    body: Dict[str, Any] = {
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "dimensions": [
            {"name": "sessionSource"},
            {"name": "sessionMedium"},
            {"name": "landingPage"},
            {"name": "date"},
        ],
        "metrics": [
            {"name": "sessions"},
            {"name": "totalUsers"},
            {"name": "engagedSessions"},
        ],
        "dimensionFilter": {
            "filter": {
                "fieldName": "sessionSource",
                "stringFilter": {
                    "matchType": "PARTIAL_REGEXP",
                    "value": ai_regex,
                },
            }
        },
        "limit": min(row_limit, 10000),
        "returnPropertyQuota": True,
    }

    try:
        resp = ga4.properties().runReport(property=property_id, body=body).execute()
    except HttpError as exc:
        if exc.resp.status in (429, 403) and "quota" in str(exc).lower():
            raise GA4QuotaExhaustedError(_safe_error_message(exc)) from None
        raise GA4ClientError(_safe_error_message(exc)) from None
    except Exception as exc:
        raise GA4ClientError(_safe_error_message(exc)) from None

    tracker.record(resp.get("propertyQuota"))

    raw_rows = resp.get("rows", [])
    classified_rows: List[Dict[str, Any]] = []

    for r in raw_rows:
        dim_vals = [v.get("value", "") for v in r.get("dimensionValues", [])]
        met_vals = [v.get("value", "0") for v in r.get("metricValues", [])]

        source = dim_vals[0] if len(dim_vals) > 0 else ""
        medium = dim_vals[1] if len(dim_vals) > 1 else ""
        landing_page = dim_vals[2] if len(dim_vals) > 2 else ""
        row_date = dim_vals[3] if len(dim_vals) > 3 else ""

        sessions = int(met_vals[0]) if len(met_vals) > 0 else 0
        total_users = int(met_vals[1]) if len(met_vals) > 1 else 0
        engaged_sessions = int(met_vals[2]) if len(met_vals) > 2 else 0

        platform = _classify_ai_source(source, medium)

        classified_rows.append({
            "platform": platform,
            "session_source": source,
            "session_medium": medium,
            "landing_page": landing_page,
            "date": row_date,
            "sessions": sessions,
            "total_users": total_users,
            "engaged_sessions": engaged_sessions,
        })

    # Groupings by platform
    platform_breakdown: Dict[str, Dict[str, int]] = {
        name: {"sessions": 0, "users": 0} for name in AI_PLATFORM_PATTERNS.keys()
    }
    platform_breakdown["Other AI"] = {"sessions": 0, "users": 0}

    for item in classified_rows:
        plat = item["platform"]
        if plat not in platform_breakdown:
            platform_breakdown[plat] = {"sessions": 0, "users": 0}
        platform_breakdown[plat]["sessions"] += item["sessions"]
        platform_breakdown[plat]["users"] += item["total_users"]

    total_ai_sessions = sum(r["sessions"] for r in classified_rows)
    total_ai_users = sum(r["total_users"] for r in classified_rows)

    classification_notes = (
        "AI referral detection searches sessionSource for ChatGPT/OpenAI, Claude/Anthropic, "
        "Gemini/Bard, Copilot, and Perplexity signatures. Note that AI assistant referrals without "
        "HTTP referrers or originating inside mobile webviews often appear as Direct / (none)."
    )

    return {
        "property": property_id,
        "collected_at": collected_at,
        "date_range": {"start_date": start_date, "end_date": end_date},
        "target_platforms": list(AI_PLATFORM_PATTERNS.keys()),
        "total_ai_sessions": total_ai_sessions,
        "total_ai_users": total_ai_users,
        "is_empty": len(classified_rows) == 0,
        "platform_breakdown": platform_breakdown,
        "rows": classified_rows,
        "classification_notes": classification_notes,
        "quota": tracker.to_dict(),
    }


def get_whatsapp_lead_performance(
    start_date: str,
    end_date: str,
    property_id: str = GA4_PROPERTY_RESOURCE,
    service: Optional[Any] = None,
    row_limit: int = 5000,
    max_rows: Optional[int] = None,
    quota_tracker: Optional[QuotaTracker] = None,
) -> Dict[str, Any]:
    """Track commercial lead events (generate_lead, whatsapp_click, product_whatsapp_click).

    Correlates lead actions with landing pages.
    Distinguishes total event actions (eventCount) from unique users (totalUsers).
    Safely labels missing events with zero counts.
    """
    ga4 = service or get_ga4_service()
    tracker = quota_tracker or QuotaTracker()
    collected_at = datetime.now(timezone.utc).isoformat()

    body: Dict[str, Any] = {
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "dimensions": [
            {"name": "eventName"},
            {"name": "landingPage"},
            {"name": "date"},
        ],
        "metrics": [
            {"name": "eventCount"},
            {"name": "totalUsers"},
        ],
        "dimensionFilter": {
            "filter": {
                "fieldName": "eventName",
                "inListFilter": {
                    "values": TARGET_WHATSAPP_EVENTS,
                },
            }
        },
        "limit": min(row_limit, 10000),
        "returnPropertyQuota": True,
    }

    try:
        resp = ga4.properties().runReport(property=property_id, body=body).execute()
    except HttpError as exc:
        if exc.resp.status in (429, 403) and "quota" in str(exc).lower():
            raise GA4QuotaExhaustedError(_safe_error_message(exc)) from None
        raise GA4ClientError(_safe_error_message(exc)) from None
    except Exception as exc:
        raise GA4ClientError(_safe_error_message(exc)) from None

    tracker.record(resp.get("propertyQuota"))

    raw_rows = resp.get("rows", [])
    parsed_rows: List[Dict[str, Any]] = []

    # Initialize event-level tally for all target events
    event_summary: Dict[str, Dict[str, Any]] = {}
    for ev in TARGET_WHATSAPP_EVENTS:
        event_summary[ev] = {
            "event_count": 0,
            "unique_users": 0,
            "detected_in_dataset": False,
            "status": "0 (no occurrences recorded in date range)",
        }

    landing_page_summary: Dict[str, Dict[str, int]] = {}

    for r in raw_rows:
        dim_vals = [v.get("value", "") for v in r.get("dimensionValues", [])]
        met_vals = [v.get("value", "0") for v in r.get("metricValues", [])]

        event_name = dim_vals[0] if len(dim_vals) > 0 else ""
        landing_page = dim_vals[1] if len(dim_vals) > 1 else ""
        row_date = dim_vals[2] if len(dim_vals) > 2 else ""

        event_count = int(met_vals[0]) if len(met_vals) > 0 else 0
        total_users = int(met_vals[1]) if len(met_vals) > 1 else 0

        parsed_rows.append({
            "event_name": event_name,
            "landing_page": landing_page,
            "date": row_date,
            "event_count": event_count,
            "total_users": total_users,
        })

        if event_name in event_summary:
            event_summary[event_name]["event_count"] += event_count
            event_summary[event_name]["unique_users"] += total_users
            event_summary[event_name]["detected_in_dataset"] = True
            event_summary[event_name]["status"] = (
                f"{event_summary[event_name]['event_count']} events recorded"
            )

        if landing_page not in landing_page_summary:
            landing_page_summary[landing_page] = {"event_count": 0, "users": 0}
        landing_page_summary[landing_page]["event_count"] += event_count
        landing_page_summary[landing_page]["users"] += total_users

    total_events = sum(r["event_count"] for r in parsed_rows)
    total_unique_users = sum(r["total_users"] for r in parsed_rows)

    return {
        "property": property_id,
        "collected_at": collected_at,
        "date_range": {"start_date": start_date, "end_date": end_date},
        "target_events": TARGET_WHATSAPP_EVENTS,
        "total_lead_events": total_events,
        "total_lead_users": total_unique_users,
        "is_empty": len(parsed_rows) == 0,
        "event_summary": event_summary,
        "landing_page_summary": landing_page_summary,
        "rows": parsed_rows,
        "quota": tracker.to_dict(),
    }
