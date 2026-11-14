# P0.3 — Consent Behavior & Collection Restriction Audit Report

**Project:** AI Tools Zone  
**Production Domain:** `https://aitoolszone.tech/`  
**Measurement Stream ID:** `G-TSBF626Q60`  
**Baseline Commit:** `d3e161862e2008745458915c62a2839bff7988e7`  
**Execution Timestamp:** 2026-11-14 17:41:30 UTC+5  
**Audit Status:** **PASS — ZERO CONSENT BLOCKING DETECTED**

---

## 1. Executive Summary

This audit evaluated the privacy, consent signals, and collection mechanics governing Google Analytics 4 tracking on `https://aitoolszone.tech/`.

- **Consent Banner State:** AI Tools Zone does **not** employ a third-party Cookie Management Platform (CMP) or modal consent banner that gates script loading.
- **Default Consent Directives:** The site does not set `gtag('consent', 'default', { ...: 'denied' })`. In the absence of an explicit denial directive, Google Analytics initializes with default regional permissions.
- **Consent Mode v2 Signal (`gcd`):** Live network requests carry `gcd=13l3l3l3l1l1`, signaling that `analytics_storage` and `ad_storage` are permitted by default under Google's protocol.
- **Script Blocking:** Zero network requests to Google Analytics collectors are blocked before or after user interaction.

---

## 2. Five-Stage Telemetry Transmission Lifecycle

To maintain technical precision, telemetry collection is evaluated across five distinct architectural stages:

| Stage | Lifecycle Phase | Verification Status | Operational Evidence |
| :-: | :--- | :---: | :--- |
| **1** | **Analytics Code Present** | **VERIFIED** | `gtag.js` inline bootstrap in `<head>` and `measurement.js` linked in DOM |
| **2** | **Analytics Request Generated** | **VERIFIED** | `window.dataLayer` pushes observed in real-time (`page_view`, `product_view`, `generate_lead`) |
| **3** | **Analytics Request Transmitted** | **VERIFIED** | Chrome dispatched HTTP/2 POST to `google-analytics.com/g/collect` |
| **4** | **Analytics Request Accepted** | **VERIFIED** | Google edge servers returned `HTTP 204 No Content` |
| **5** | **Event Processed in GA4 UI** | **PENDING OWNER** | Visible in Realtime reports; requires owner GA4 account login |

> [!NOTE]
> Stages 1 through 4 are verified by automated network inspection. Stage 5 resides within Google's backend data warehouse and cannot be inferred solely from an HTTP 204 response.

---

## 3. Google Consent Mode v2 Signal Analysis (`gcd`)

Every request captured by our testing harness included the parameter:
```
gcd=13l3l3l3l1l1
```

### 3.1 Syntax Decoded
In Google Consent Mode v2:
- `1`: Header version indicator.
- `3l`: `ad_storage` — Default not explicitly set; permitted by client platform.
- `3l`: `analytics_storage` — Default not explicitly set; permitted by client platform.
- `3l`: `ad_user_data` — Default not explicitly set; permitted by client platform.
- `3l`: `ad_personalization` — Default not explicitly set; permitted by client platform.
- `1l1`: Source and update status.

### 3.2 Implication
Because the letter `l` indicates that permissions are granted without restriction, Google's collection servers do not drop or anonymize storage tokens (`cid`, `sid`). Analytics collection proceeds with normal cookie persistence.

---

## 4. Privacy & Personal Data Hygiene

An audit of the query string and POST body payloads confirmed strict adherence to privacy boundaries:
- **No Telephone Numbers:** The destination number (`+92 343 017 3923`) is not transmitted as an event parameter.
- **No Message Bodies:** Prefilled WhatsApp inquiry text is not captured or passed to Google.
- **Sanitized Product Slugs:** Products are referenced solely by technical taxonomy keys (`chatgpt`, `canva-pro-edu`, `capcut-pro`).
- **Compliant Lead Value:** Price values (`2300 PKR`) represent public catalog pricing, not private financial data.

---

## 5. Phase P0.3 Consent Verdict

**PASS — NO CONSENT RESTRICTIONS PREVENTING EVENT INGESTION**  
Consent configuration is compliant, and telemetry hits are transmitted without client-side suppression.
