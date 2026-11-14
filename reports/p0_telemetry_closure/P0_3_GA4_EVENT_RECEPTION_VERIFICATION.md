# P0.3 — GA4 Event Reception & Conversion Strategy Audit Report

**Project:** AI Tools Zone  
**Production Domain:** `https://aitoolszone.tech/`  
**Measurement Stream ID:** `G-TSBF626Q60`  
**Baseline Commit:** `d3e161862e2008745458915c62a2839bff7988e7`  
**Execution Timestamp:** 2026-11-14 17:42:00 UTC+5  
**Audit Scope:** Event Reception Analysis, Telemetry Taxonomy & Recommended Key Event Strategy  
**Audit Status:** **VERIFIED IN BROWSER / PENDING OWNER GA4 CONSOLE VERIFICATION**

---

## 1. Executive Summary

This evaluation analyzed the complete event taxonomy implemented in `measurement.js` and established the optimal conversion event architecture for tracking commercial inquiries on AI Tools Zone.

- **Browser-Side Event Emission:** 100% verified. All 7 core events (`page_view`, `product_view`, `product_page_view`, `whatsapp_click`, `product_whatsapp_click`, `generate_lead`, `cta_click`) fire with exact parameter schemas.
- **Google-Side Reception Boundary:** Direct access to Google Analytics internal property reports requires owner authentication. While browser network dispatches return `HTTP 204`, confirmation of reception inside GA4 reports must be verified by the site owner via **GA4 Realtime** (see Section 3).
- **Conversion Strategy Recommendation:** **`generate_lead` must be designated as the PRIMARY Key Event**. Supporting events (`whatsapp_click`, `product_whatsapp_click`) should remain diagnostic supporting events to prevent triple-counting conversions.

---

## 2. Event Taxonomy & Payload Matrix

The following table documents the exact technical specification of each event fired across the commercial funnel:

| Event Name | Triggering User Action | Transmitted Parameters | Value / Currency | Intended Reporting Purpose |
| :--- | :--- | :--- | :---: | :--- |
| **`page_view`** | Document load on canonical page | `page`, `section` | — | Traffic volume & page engagement |
| **`product_view`** | Product landing page open | `page`, `section`, `product` | — | Product interest & catalog reach |
| **`product_page_view`**| Product landing page open | `page`, `section`, `product` | — | Specialized funnel step analysis |
| **`whatsapp_click`** | Click on ANY WhatsApp link | `page`, `section`, `product` | — | Diagnostic click tracking across all pages |
| **`product_whatsapp_click`** | Click on product `.buy-now` CTA | `page`, `section`, `product` | — | Diagnostic product order initiation |
| **`generate_lead`** | Click on product `.buy-now` CTA | `page`, `section`, `product`, `value`, `currency` | **PKR [Price]** (e.g. 2300) | **PRIMARY COMMERCIAL KEY EVENT** |
| **`cta_click`** | Click on general interactive button | `page`, `section`, `label` | — | UI element engagement |

---

## 3. Realtime vs. DebugView Event Visibility

Because `debug_mode: true` is not configured in the production tag, incoming traffic behaves differently across GA4 report views:

| View in GA4 | Expected Behavior for Current Production Traffic | Reason |
| :--- | :---: | :--- |
| **GA4 Realtime (`Reports > Realtime`)** | **VISIBLE** (Card: *Event count by Event name*) | Standard production events appear in Realtime within 10–30 seconds. |
| **GA4 DebugView (`Admin > DebugView`)** | **NOT VISIBLE** (*"No devices available"*) | Explicitly filters out all hits lacking `ep.debug_mode=true` or `_dbg=1`. |
| **Standard Reports (`Engagement > Events`)** | **VISIBLE** (24-hour processing latency) | Processed into standard aggregate dimension tables overnight. |

> [!TIP]
> The site owner can immediately verify live traffic without code changes by opening **Reports > Realtime** in GA4 and clicking a product button on `aitoolszone.tech`.

---

## 4. Conversion Event Strategy Evaluation

### 4.1 The Multiple-Event Problem
When a user clicks **"Order on WhatsApp ↗"** on `/products/chatgpt-plus/`, the site currently emits three overlapping conversion-related events:
1. `whatsapp_click`
2. `product_whatsapp_click`
3. `generate_lead`

If the owner toggles all three as **Key Events** in GA4:
- GA4 will record **3 conversions for a single user click**.
- Google Ads or conversion analytics will report a 300% inflated conversion rate.
- Cost-per-acquisition (CPA) calculations will be severely distorted.

### 4.2 Recommended Primary Key Event: `generate_lead`
**`generate_lead` should be the SOLE primary Key Event** for commercial tracking because:
1. **Google Standard Schema:** It is an officially recognized standard event in GA4, unlocking automated monetization and ROAS metrics.
2. **Monetary Value:** It carries `value: 2300` and `currency: 'PKR'`, enabling GA4 to track Total Event Value by marketing channel.
3. **Intent Differentiation:** It only fires on commercial product purchase buttons, whereas general footer/contact WhatsApp links fire `whatsapp_click` without monetary value.
4. **Accurate Conversion Accounting:** A WhatsApp click represents a high-intent customer inquiry, matching the definition of a "Lead" rather than a completed purchase ("Purchase").

### 4.3 Role of Supporting Events
- `whatsapp_click` and `product_whatsapp_click` should remain active in the code as **Standard Events** (NOT Key Events). They provide valuable diagnostic telemetry for technical audits without polluting marketing conversion counts.

---

## 5. Verification Checklist for Site Owner

1. Log into [Google Analytics](https://analytics.google.com/) (`G-TSBF626Q60`).
2. Navigate to **Admin > Data display > Events**.
3. Toggle `generate_lead` to **"Mark as key event"** (ON).
4. Leave `whatsapp_click` and `product_whatsapp_click` as standard events (OFF).
5. Open **Reports > Realtime**, perform a test click on the website, and confirm `generate_lead` appears in the Realtime card.
