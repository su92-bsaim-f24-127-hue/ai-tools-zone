# Phase 12 Search Console & Analytics Measurement Plan

**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Evaluation Period:** November 15, 2026 – December 15, 2026 (30-Day Growth Monitoring)  
**Author:** Senior SEO Strategist & Technical Analyst  

---

## 1. Verified Telemetry Baseline (Empirical Ground Truth)

In strict accordance with the non-destructive rule (*"Do not fabricate analytics values"*), the baseline below uses verified empirical records from Google Search Console (GSC) and Google Analytics 4 (GA4) established during Phase 10:

| Metric Dimension | Current Baseline Value (Trailing 7-Day Window) | Target 30-Day Milestone (Post-Phase 12) | Measurement Source |
|---|---|---|---|
| **Canonical Public Routes** | 99 routes | 104 routes (+5 growth guides) | `sitemap.xml` / `seo-contract.json` |
| **Indexed Routes (Google)** | 74 / 99 routes (74.7%) | 95+ / 104 routes (>91%) | GSC URL Inspection API |
| **GSC Organic Clicks (7d)** | 4 clicks | 25–40 clicks / 7d | Google Search Console API |
| **GSC Total Impressions (7d)** | 53 impressions | 350–500 impressions / 7d | Google Search Console API |
| **GSC Average CTR** | 7.55% | 7.0% – 8.5% | Google Search Console API |
| **GSC Average Position** | 17.96 | < 12.0 (Page 1 visibility) | Google Search Console API |
| **GA4 Organic Pakistani Users**| 8 users (100% Pakistan) | 50+ users / 7d | Google Analytics 4 (`G-TSBF626Q60`) |
| **GA4 Organic Sessions** | 9 sessions | 65+ sessions / 7d | Google Analytics 4 (`G-TSBF626Q60`) |
| **Average Engagement Time** | 97.8s (Home) / 946s (Blog) | > 120s across all landing pages | GA4 User Engagement Duration |
| **WhatsApp Order Clicks** | Baseline monitored via `whatsapp.js` | 15–25 qualified lead clicks / week | GA4 Custom Event `whatsapp_order_click` |

---

## 2. Target Keyword & Query Tracking Matrix

The following query clusters will be monitored weekly through Google Search Console performance extracts:

```
+-------------------------------------------------------+-----------------------------+-------------------------------+
| Target Query Cluster                                  | Target Landing Page         | Baseline Rank / Impression St |
+-------------------------------------------------------+-----------------------------+-------------------------------+
| "buy AI tools in Pakistan"                            | / & /buy-ai-tools-in-pakistan| Position 18–25 (New Guide)    |
| "premium AI accounts Pakistan"                        | /buy-ai-tools-in-pakistan/  | New Target (0 baseline impr)  |
| "affordable AI subscriptions Pakistan"                | /buy-ai-tools-in-pakistan/  | Position 16–22 (Pricing hub)  |
| "where to buy AI tools in Pakistan"                   | /buy-ai-tools-in-pakistan/  | Position 14–19 (Blog guide)   |
| "how to buy ChatGPT Plus in Pakistan"                 | /how-to-buy-chatgpt-plus... | Position 15–20 (Blog payment) |
| "ChatGPT Plus price in Pakistan"                      | /how-to-buy-chatgpt-plus... | Position 12–18 (Product page) |
| "best AI productivity tools for students Pakistan"   | /best-ai-tools-for-students | Position 22–30 (Thesis blog)  |
| "cheap AI tools for students Pakistan"                | /best-ai-tools-for-students | Position 19–25 (Cheap tools)  |
| "AI video editing tools Pakistan"                     | /ai-video-editing-tools...  | Position 25–35 (Video cat)    |
| "AI image generator subscription Pakistan"            | /ai-image-generator-sub...  | Position 28–40 (Design cat)   |
+-------------------------------------------------------+-----------------------------+-------------------------------+
```

---

## 3. Four-Week Milestone Reporting Schedule

Googlebot indexation and ranking re-scoring follow multi-week cycles. Telemetry will be collected and reported on the following weekly cadence:

### Week 1 (Days 1–7): Indexation & Crawler Discovery
- **Action:** Dispatch automated IndexNow pings and monitor Googlebot crawler hits in server access logs.
- **KPI:** Verify all 5 new URLs are crawled by Googlebot and AI search crawlers (`OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`).
- **Target:** 5 / 5 new routes recognized in GSC Coverage report ("Discovered" or "Crawled").

### Week 2 (Days 8–14): Initial SERP Impressions
- **Action:** Extract GSC query reports to identify the first recorded impressions for long-tail variations of target queries.
- **KPI:** Total 7-day impressions cross 100+ across all catalog and guide pages.
- **Verification:** Inspect CTR and bounce rate on `/buy-ai-tools-in-pakistan/` and `/how-to-buy-chatgpt-plus-in-pakistan/`.

### Week 3 (Days 15–21): Keyword Ranking Trajectory & Internal Link Flow
- **Action:** Measure average position shifts for primary commercial queries (`buy AI tools in Pakistan`, `how to buy ChatGPT Plus in Pakistan`).
- **KPI:** Primary queries break into top 15 results in Pakistani search results.
- **Verification:** Track organic inbound referral paths to product catalog pages via internal breadcrumbs.

### Week 4 (Days 22–30): Commercial Lead Generation & Revenue Audit
- **Action:** Measure full 30-day organic growth and WhatsApp conversion rate.
- **KPI:** Achieve 50+ monthly organic visitors, 15+ WhatsApp qualified purchase conversations, and zero indexation regressions across all 104 routes.
- **Deliverable:** Generate Phase 12 30-Day Performance Audit Report.

---

## 4. Conversion & Event Telemetry Schema

All user conversion interactions continue to be tracked cleanly via `measurement.js` and `whatsapp.js` without third-party cookie creep:

```javascript
// GA4 Event: Purchase Intent Trigger
gtag('event', 'whatsapp_order_click', {
  'event_category': 'ecommerce',
  'event_label': product_name,
  'product_id': product_id,
  'price_pkr': price_pkr,
  'page_location': window.location.pathname
});

// GA4 Event: Guide Reading Engagement
gtag('event', 'guide_scroll_depth', {
  'event_category': 'engagement',
  'event_label': '50_percent_read',
  'page_path': window.location.pathname
});
```
