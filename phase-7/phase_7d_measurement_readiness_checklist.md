# Phase 7D — Measurement Readiness & Verification Checklist

**Project:** AI Tools Zone  
**Domain:** [https://aitoolszone.tech/](https://aitoolszone.tech/)  
**Measurement ID:** `G-TSBF626Q60`  
**GSC Property:** `sc-domain:aitoolszone.tech`  
**Production Baseline:** [`e5d26f4`](https://github.com/su92-bsaim-f24-127-hue/ai-tools-zone/commit/e5d26f4)  
**Report Date:** November 11, 2026  
**Auditor:** Lead Analytics Implementation & QA Specialist  

---

## 1. Executive Purpose

This checklist provides an actionable, step-by-step verification protocol for the AI Tools Zone site administrator. It ensures that all analytics instruments, Google Search Console indexing workflows, and conversion reporting pipelines are mathematically sound and operational.

---

## 2. Google Analytics 4 (GA4) Readiness Protocol

### Check 2.1: Client-Side Event Dispatching (Pre-Verified in Production)
- [x] **`measurement.js` Active in Head/Body:** Confirmed deferred load across all 83 pages `[Official Exported Actual]`.
- [x] **800ms Debounce Guard:** Prevents duplicate lead firing on double-tap mobile clicks `[Official Exported Actual]`.
- [x] **Dynamic Section Attribution:** Resolves `section` parameter (`home`, `products`, `categories`, `compare`, `faq`) `[Official Exported Actual]`.
- [x] **Integer PKR Price Formatting:** `value: link.dataset.price ? Number(link.dataset.price) : undefined` ensures numeric e-commerce parameters `[Official Exported Actual]`.

---

### Check 2.2: GA4 Realtime Verification Protocol (Admin Action)

Execute this test to confirm that client-side dispatches are received by Google Analytics servers:

1. **Open GA4 Console:** Sign in to [Google Analytics](https://analytics.google.com/) > Select Property **`G-TSBF626Q60`**.
2. **Access Realtime Report:** In the left sidebar, click **Reports > Realtime**.
3. **Trigger Test Interaction:**
   - In a separate, clean browser tab (Chrome/Edge with ad blockers disabled), open:  
     `https://aitoolszone.tech/products/chatgpt-plus/`
   - Click the primary WhatsApp CTA button: **"Order on WhatsApp"**.
4. **Confirm Realtime Ingestion:**
   - In GA4 Realtime, locate the card **Event count by Event name**.
   - Verify that **`generate_lead`**, **`product_whatsapp_click`**, and **`whatsapp_click`** appear within 30–60 seconds.
5. **Inspect Event Parameters:**
   - Click directly on **`generate_lead`** in the table.
   - Verify that the following parameter values appear:
     - `product` = `chatgpt-plus`
     - `value` = `2300`
     - `currency` = `PKR`
     - `section` = `products`

---

### Check 2.3: GA4 DebugView Granular Inspection (Admin Action)

For deep inspection of raw network payloads and parameter data types:

1. **Activate Debug Mode:**
   - Append `?_dbg=1` to any product URL (e.g. `https://aitoolszone.tech/products/canva-pro-edu/?_dbg=1`), or
   - Use Google Tag Assistant at [tagassistant.google.com](https://tagassistant.google.com/).
2. **Open DebugView in GA4:**
   - Go to **Admin (Gear Icon) > Data display > DebugView**.
3. **Verify Incoming Timeline:**
   - Confirm that the `generate_lead` event node appears on the minute timeline.
   - Click the event to verify that `value` is registered as a **numeric type** and `currency` is **`PKR`**.

---

### Check 2.4: GA4 Key Event Configuration (Mandatory Admin Action)

> [!IMPORTANT]
> **Forward-Only Processing Warning:**  
> In Google Analytics 4, events are standard engagement events by default. To populate Conversion Rate, Cost per Acquisition, and Acquisition Channel Conversion tables, `generate_lead` must be marked as a **Key Event**. GA4 does **NOT** retroactively update historical data; Key Event status applies strictly forward from the moment of activation.

**Activation Steps:**
1. In GA4, navigate to **Admin > Data display > Events**.
2. In the **Existing events** table, locate **`generate_lead`**.
3. In the column **Mark as key event** (formerly "Mark as conversion"), toggle the switch to **Active (Blue)**.
4. *Verification:* Go to **Admin > Data display > Key events** and confirm that `generate_lead` is listed.

---

## 3. Google Search Console (GSC) Readiness Protocol

### Check 3.1: Sitemap Processing & Submission
- [x] **Live Sitemap Health:** Verified [`https://aitoolszone.tech/sitemap.xml`](https://aitoolszone.tech/sitemap.xml) contains all 83 canonical URLs with content-based `lastmod` dates `[Official Exported Actual]`.
- [x] **Robots.txt Declaration:** Verified `Sitemap: https://aitoolszone.tech/sitemap.xml` present in [`robots.txt`](https://aitoolszone.tech/robots.txt) `[Official Exported Actual]`.
- [ ] **GSC Console Submission (Admin Action):**
  - Open Google Search Console > Select `sc-domain:aitoolszone.tech`.
  - Go to **Indexing > Sitemaps**.
  - Submit `sitemap.xml` and confirm "Success" status.

---

### Check 3.2: Priority URL Inspection Requests (Admin Action)

Accelerate Googlebot re-crawling of the core pages optimized in Phase 7C:

1. In GSC, use the top search bar to inspect each of the following URLs individually:
   - `https://aitoolszone.tech/products/chatgpt-plus/`
   - `https://aitoolszone.tech/products/canva-pro-edu/`
   - `https://aitoolszone.tech/products/capcut-pro/`
   - `https://aitoolszone.tech/products/gemini-pro/`
   - `https://aitoolszone.tech/products/adobe-creative-cloud/`
   - `https://aitoolszone.tech/blog/how-to-pay-for-chatgpt-plus-pakistan/`
   - `https://aitoolszone.tech/faq/`
2. If the page is indexed, click **Request Indexing** to submit a re-crawl notification to Googlebot's queue.
3. *Note:* Re-crawling is not guaranteed on a fixed schedule (may take days to weeks); manual requests inform Googlebot that fresh content is available.

---

## 4. Post-Deployment Measurement Windows Protocol

To evaluate Phase 7C without confusing correlation with causation:

```text
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│       Pre-Deployment Benchmark       │     │       Post-Crawl Evaluation          │
│   Oct 28, 2026 – Nov 10, 2026        │ vs. │  Equal 14-Day Post-Recrawl Window    │
│            (14 Days)                 │     │ (Begins AFTER re-crawl is confirmed) │
└──────────────────────────────────────┘     └──────────────────────────────────────┘
```

1. **Pre-Deployment Baseline Established:**
   - 14-day pre-deployment baseline recorded for all 8 Phase 7C URLs in `phase_7d_phase7c_impact_analysis.md`.
2. **Crawl Verification Gate:**
   - Monitor GSC URL Inspection weekly.
   - Do **NOT** calculate post-deployment CTR until Googlebot has crawled at least 6 of the 8 updated URLs and refreshed SERP snippets.
3. **Equal-Window Comparative Analysis:**
   - Compare an equal 14-day window post-crawl against the 14-day pre-deployment window.
   - Track: Impressions, Clicks, CTR, Average Position.

---

## 5. Google API Automation Upgrade (Tier 0 to Tier 1 / Tier 2)

To enable automated daily reporting without manual CSV downloads:

- [ ] **Step 1: Create Google Cloud Service Account:**
  - In [Google Cloud Console](https://console.cloud.google.com/), enable `Google Search Console API` and `Google Analytics Data API`.
  - Create a service account (e.g. `seo-agent`) and generate a JSON key file.
  - Save securely to `C:\Users\ELITEBOOK\.config\claude-seo\service_account.json` (never commit this file to Git).
- [ ] **Step 2: Grant GSC Property Access:**
  - In GSC > **Settings > Users and permissions > Add user** > Enter `client_email` with **Full** permission.
- [ ] **Step 3: Grant GA4 Property Access:**
  - In GA4 > **Admin > Property Access Management > Add users** > Enter `client_email` with **Viewer** permission.
- [ ] **Step 4: Update Local Config:**
  - Add `"service_account_path": "C:\\Users\\ELITEBOOK\\.config\\claude-seo\\service_account.json"` to `~/.config/claude-seo/google-api.json`.
