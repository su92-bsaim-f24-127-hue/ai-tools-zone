"""AI Tools Zone — GA4 Telemetry Data Collector & Lead Attribution.

Queries Google Analytics Data API v1beta for:
1. Pakistan-filtered organic landing page performance (2026-10-15 to 2026-11-11 matching GSC, and trailing 28 days).
2. Segmenting 72 currently indexed routes (distinguishing 42 previously indexed vs 30 newly indexed).
3. Discrete analysis of `generate_lead` vs `whatsapp_click` vs other conversion events.
4. Landing page correlation with WhatsApp intent events.
5. AI Assistants channel investigation (`sessionMedium == 'ai-assistant'` and AI referral sources).
6. Comparison with GSC search click totals.
"""

import sys
import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root / "scripts" / "telemetry"))

from config import (
    WEBSITE_ORIGIN,
    GA4_PROPERTY_ID,
    GA4_PROPERTY_RESOURCE,
    GA4_READONLY_SCOPE,
)
from auth import get_adc_credentials
from google.auth.transport.requests import AuthorizedSession


def get_ga4_session():
    creds = get_adc_credentials([GA4_READONLY_SCOPE])
    return AuthorizedSession(creds)


def run_ga4_report(session: AuthorizedSession, body: Dict[str, Any]) -> Dict[str, Any]:
    url = f"https://analyticsdata.googleapis.com/v1beta/{GA4_PROPERTY_RESOURCE}:runReport"
    resp = session.post(url, json=body, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"GA4 runReport failed (HTTP {resp.status_code}): {resp.text}")
    return resp.json()


def main():
    session = get_ga4_session()
    print("=" * 70)
    print("AI Tools Zone — Phase 5.5E GA4 Data Collection & Lead Attribution")
    print(f"Property Resource: {GA4_PROPERTY_RESOURCE}")
    print("=" * 70)

    # 1. Total traffic overview: Last 28 days (2026-10-15 to 2026-11-11 matching GSC period)
    gsc_period = {"startDate": "2026-10-15", "endDate": "2026-11-11"}
    extended_period = {"startDate": "2026-10-15", "endDate": "2026-11-13"}

    # Query 1A: Overall Traffic by Default Channel Group (GSC Period)
    q1a = {
        "dateRanges": [gsc_period],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "totalUsers"},
            {"name": "engagedSessions"},
            {"name": "engagementRate"},
            {"name": "averageSessionDuration"},
            {"name": "eventCount"}
        ],
        "returnPropertyQuota": True
    }
    res_1a = run_ga4_report(session, q1a)
    print("\n--- 1A. Channel Group Overview (2026-10-15 to 2026-11-11) ---")
    for row in res_1a.get("rows", []):
        ch = row["dimensionValues"][0]["value"]
        sess = row["metricValues"][0]["value"]
        users = row["metricValues"][1]["value"]
        eng_sess = row["metricValues"][2]["value"]
        eng_rate = float(row["metricValues"][3]["value"]) * 100
        avg_dur = float(row["metricValues"][4]["value"])
        events = row["metricValues"][5]["value"]
        print(f"  Channel: {ch:<20} | Sessions: {sess:<4} | Users: {users:<4} | Engaged: {eng_sess:<3} | EngRate: {eng_rate:.1f}% | AvgDur: {avg_dur:.1f}s | Events: {events}")

    # Query 1B: Country Breakdown of Traffic
    q1b = {
        "dateRanges": [gsc_period],
        "dimensions": [{"name": "country"}],
        "metrics": [{"name": "sessions"}, {"name": "totalUsers"}],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 10
    }
    res_1b = run_ga4_report(session, q1b)
    print("\n--- 1B. Top Countries (2026-10-15 to 2026-11-11) ---")
    for row in res_1b.get("rows", []):
        country = row["dimensionValues"][0]["value"]
        sess = row["metricValues"][0]["value"]
        users = row["metricValues"][1]["value"]
        print(f"  Country: {country:<20} | Sessions: {sess:<4} | Users: {users}")

    # Query 2: Organic Search Landing Pages (Pakistan Only, 2026-10-15 to 2026-11-11)
    q2 = {
        "dateRanges": [gsc_period],
        "dimensions": [{"name": "landingPage"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "totalUsers"},
            {"name": "engagedSessions"},
            {"name": "engagementRate"},
            {"name": "averageSessionDuration"},
            {"name": "eventCount"}
        ],
        "dimensionFilter": {
            "andGroup": {
                "expressions": [
                    {
                        "filter": {
                            "fieldName": "sessionDefaultChannelGroup",
                            "stringFilter": {"matchType": "EXACT", "value": "Organic Search"}
                        }
                    },
                    {
                        "filter": {
                            "fieldName": "country",
                            "stringFilter": {"matchType": "EXACT", "value": "Pakistan"}
                        }
                    }
                ]
            }
        },
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 100
    }
    res_2 = run_ga4_report(session, q2)
    print("\n--- 2. Pakistan Organic Search Landing Pages (2026-10-15 to 2026-11-11) ---")
    if not res_2.get("rows"):
        print("  No Organic Search sessions from Pakistan recorded during Oct 15 - Nov 11 window.")
    for row in res_2.get("rows", []):
        page = row["dimensionValues"][0]["value"]
        sess = row["metricValues"][0]["value"]
        users = row["metricValues"][1]["value"]
        eng_rate = float(row["metricValues"][3]["value"]) * 100
        print(f"  Landing: {page:<40} | Sessions: {sess} | Users: {users} | EngRate: {eng_rate:.1f}%")

    # Query 2B: All-Channel Landing Pages (Pakistan Only, 2026-10-15 to 2026-11-13)
    q2b = {
        "dateRanges": [extended_period],
        "dimensions": [{"name": "landingPage"}, {"name": "sessionDefaultChannelGroup"}],
        "metrics": [{"name": "sessions"}, {"name": "totalUsers"}, {"name": "engagedSessions"}],
        "dimensionFilter": {
            "filter": {
                "fieldName": "country",
                "stringFilter": {"matchType": "EXACT", "value": "Pakistan"}
            }
        },
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 50
    }
    res_2b = run_ga4_report(session, q2b)
    print("\n--- 2B. All Pakistan Landing Pages by Channel (Oct 15 - Nov 13) ---")
    for row in res_2b.get("rows", []):
        page = row["dimensionValues"][0]["value"]
        ch = row["dimensionValues"][1]["value"]
        sess = row["metricValues"][0]["value"]
        users = row["metricValues"][1]["value"]
        print(f"  Page: {page:<40} | Channel: {ch:<16} | Sessions: {sess} | Users: {users}")

    # Query 3: Conversion Events & WhatsApp Clicks (Discrete Breakdown)
    # Check all events in the period
    q3 = {
        "dateRanges": [extended_period],
        "dimensions": [{"name": "eventName"}],
        "metrics": [{"name": "eventCount"}, {"name": "totalUsers"}],
        "orderBys": [{"metric": {"metricName": "eventCount"}, "desc": True}],
        "limit": 50
    }
    res_3 = run_ga4_report(session, q3)
    print("\n--- 3. Event Names & Counts (Oct 15 - Nov 13) ---")
    for row in res_3.get("rows", []):
        ev = row["dimensionValues"][0]["value"]
        cnt = row["metricValues"][0]["value"]
        usr = row["metricValues"][1]["value"]
        print(f"  Event: {ev:<30} | Count: {cnt:<6} | Users: {usr}")

    # Query 4: Landing Pages associated with WhatsApp / Lead Events
    # Filter for generate_lead, whatsapp_click, product_whatsapp_click
    q4 = {
        "dateRanges": [extended_period],
        "dimensions": [{"name": "pagePath"}, {"name": "eventName"}],
        "metrics": [{"name": "eventCount"}, {"name": "totalUsers"}],
        "dimensionFilter": {
            "filter": {
                "fieldName": "eventName",
                "inListFilter": {
                    "values": [
                        "generate_lead",
                        "whatsapp_click",
                        "product_whatsapp_click",
                        "cta_click"
                    ]
                }
            }
        },
        "orderBys": [{"metric": {"metricName": "eventCount"}, "desc": True}],
        "limit": 50
    }
    res_4 = run_ga4_report(session, q4)
    print("\n--- 4. WhatsApp & Lead Intent Events by Page Path (Oct 15 - Nov 13) ---")
    if not res_4.get("rows"):
        print("  Zero generate_lead / whatsapp_click events recorded in this date range.")
    for row in res_4.get("rows", []):
        path = row["dimensionValues"][0]["value"]
        ev = row["dimensionValues"][1]["value"]
        cnt = row["metricValues"][0]["value"]
        usr = row["metricValues"][1]["value"]
        print(f"  Page: {path:<40} | Event: {ev:<24} | Count: {cnt} | Users: {usr}")

    # Query 5: AI Assistants Channel & AI Referrers
    q5 = {
        "dateRanges": [extended_period],
        "dimensions": [
            {"name": "sessionSource"},
            {"name": "sessionMedium"},
            {"name": "sessionDefaultChannelGroup"}
        ],
        "metrics": [{"name": "sessions"}, {"name": "totalUsers"}, {"name": "engagedSessions"}],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 50
    }
    res_5 = run_ga4_report(session, q5)
    print("\n--- 5. Traffic Sources & Mediums (AI Assistants & Referrals) ---")
    ai_sources_found = []
    for row in res_5.get("rows", []):
        src = row["dimensionValues"][0]["value"]
        med = row["dimensionValues"][1]["value"]
        ch = row["dimensionValues"][2]["value"]
        sess = row["metricValues"][0]["value"]
        users = row["metricValues"][1]["value"]
        is_ai = med == "ai-assistant" or any(k in src.lower() for k in ["chatgpt", "claude", "gemini", "copilot", "perplexity", "anthropic", "openai"])
        if is_ai:
            ai_sources_found.append((src, med, ch, sess, users))
        print(f"  Source: {src:<25} | Medium: {med:<15} | Channel: {ch:<16} | Sessions: {sess} | Users: {users} {'[AI REFERRAL]' if is_ai else ''}")

    print(f"\nAI Referral Summary: {len(ai_sources_found)} AI referral source(s) identified.")

    # Save full results payload
    payload = {
        "metadata": {
            "property_id": GA4_PROPERTY_ID,
            "property_resource": GA4_PROPERTY_RESOURCE,
            "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
            "periods": {
                "gsc_aligned": gsc_period,
                "extended": extended_period
            }
        },
        "channel_group_gsc_period": res_1a.get("rows", []),
        "countries_gsc_period": res_1b.get("rows", []),
        "pakistan_organic_landing": res_2.get("rows", []),
        "pakistan_all_channels_landing": res_2b.get("rows", []),
        "all_events": res_3.get("rows", []),
        "lead_and_whatsapp_events_by_page": res_4.get("rows", []),
        "traffic_sources": res_5.get("rows", []),
        "ai_sources_identified": ai_sources_found
    }

    out_file = repo_root / "scratch" / "phase_5_5e_ga4_telemetry_dump.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nPayload saved to: {out_file}")


if __name__ == "__main__":
    main()
