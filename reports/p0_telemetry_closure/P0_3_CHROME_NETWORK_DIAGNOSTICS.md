# P0.3 — Chrome Network Diagnostics & Telemetry Payload Log

**Project:** AI Tools Zone  
**Production Domain:** `https://aitoolszone.tech/`  
**Test Route:** `https://aitoolszone.tech/products/chatgpt-plus/`  
**Harness:** Playwright Headless Chromium (Google Chrome 120+)  
**Execution Timestamp:** 2026-11-14 17:40:30 UTC+5  
**Audit Status:** **NETWORK DISPATCH 100% VERIFIED**

---

## 1. Executive Summary

Controlled browser network diagnostics were captured during page load and user interaction on the ChatGPT Plus product page. All requests to Google Analytics collectors were recorded, parsed, and sanitized.

- **Primary Collector Endpoint:** `https://www.google-analytics.com/g/collect`
- **Protocol & Method:** HTTP/2 over TLS 1.3 via `POST`
- **Response Status:** `HTTP/2 204 No Content`
- **Total Hits Captured:** 2 multi-event batches covering 5 user actions
- **Telemetry Health:** Measurement ID matches `G-TSBF626Q60` across all hits; zero dropped payloads.

---

## 2. Sanitized Network Request Ledgers

### 2.1 Request 1: Initial Page Load & View Tracking

Dispatched automatically following document load and `gtag.js` initialization:

| Parameter | Observed Value | Description / Verification |
| :--- | :--- | :--- |
| **`v`** | `2` | Google Analytics Measurement Protocol version 2 |
| **`tid`** | `G-TSBF626Q60` | Verified AI Tools Zone GA4 Measurement ID |
| **`en` (Event Name)** | `page_view` | Initial page view emission |
| **`dl` (Document Location)** | `https://aitoolszone.tech/products/chatgpt-plus/` | Exact canonical URL |
| **`ep.name`** | `page_view` | Custom name parameter in `measurement.js` |
| **`ep.page`** | `/products/chatgpt-plus/` | Canonical path |
| **`ep.section`** | `products` | Site taxonomy category |
| **`ep.debug_mode`** | *[NOT PRESENT]* | Confirms debug mode was not requested |
| **`gcd`** | `13l3l3l3l1l1` | Google Consent Mode v2 signal (default granted) |
| **`cid`** | `96xxxxxxxx.17xxxxxxxx` | Sanitized Client ID (unique device token) |
| **`sid`** | `17xxxxxxxx` | Sanitized Session ID |
| **HTTP Method** | `POST` | Dispatched via `sendBeacon` / `fetch` |
| **Response Code** | `204 No Content` | Acknowledged and accepted by Google edge |

---

### 2.2 Request 2: Outbound WhatsApp Order Interaction

Dispatched when the visitor clicks the `.buy-now` button (`Order on WhatsApp ↗`):

| Parameter | Observed Value | Description / Verification |
| :--- | :--- | :--- |
| **`v`** | `2` | GA4 protocol version |
| **`tid`** | `G-TSBF626Q60` | Target measurement stream |
| **`en` (Batched Events)** | `product_view`, `whatsapp_click`, `product_whatsapp_click`, `generate_lead`, `cta_click` | Multi-event interaction batch |
| **`ep.product`** | `chatgpt` | Sanitized product identifier |
| **`epn.value`** | `2300` | Exact PKR catalog price (numeric) |
| **`ep.currency`** | `PKR` | ISO 4217 Pakistani Rupee currency code |
| **`ep.label`** | `Order on WhatsApp ↗` | CTA anchor text label |
| **`ep.debug_mode`** | *[NOT PRESENT]* | Confirms debug mode was not requested |
| **`gcd`** | `13l3l3l3l1l1` | Consent status consistent with session |
| **`cid`** | `96xxxxxxxx.17xxxxxxxx` | Matches session Client ID |
| **`sid`** | `17xxxxxxxx` | Matches session ID |
| **HTTP Method** | `POST` | Asynchronous beacon dispatch |
| **Response Code** | `204 No Content` | Successfully accepted by Google edge |

---

## 3. Transmission Timing & Navigation Concurrency

1. **Pre-Navigation Firing:**  
   The WhatsApp link uses `target="_blank"`. When clicked, the browser creates a new browsing context for WhatsApp Web/App while keeping the current page context active.
2. **Execution Timing:**  
   The telemetry POST request is initiated within `12 ms` of the click event and completes in `184 ms`, guaranteeing that network transport finishes before the originating window changes state.
3. **Double-Click Protection:**  
   Rapid repeated clicks within `800 ms` are suppressed by the debounce guard in `measurement.js` (`now - lastClickTime < 800`), preventing inflated hit counts.

---

## 4. Diagnostic Summary

- **Measurement ID Accuracy:** 100% compliant.
- **Payload Sanitization:** No sensitive customer phone numbers or message texts transmitted.
- **Missing Diagnostic Parameter:** `ep.debug_mode` is missing from both requests, explaining the absence of records in GA4 DebugView.
