# Google Search Console & Cloudflare Owner Action Guide

**Date:** 2 November 2026 (Asia/Karachi)  
**Target Domain:** <https://aitoolszone.tech/>  
**Property in GSC:** `URL prefix: https://aitoolszone.tech/`  
**Hosting Environment:** Cloudflare Pages (Custom Domain `aitoolszone.tech`)

---

## 1. Urgent Edge Fix: Cloudflare WWW Subdomain (Resolves Error 522)

### The Problem
Currently, navigating to `https://www.aitoolszone.tech/` results in a **Cloudflare Error 522 (Connection Timed Out)**. Search engines and users who type `www.` cannot reach the site, causing dropped crawls and broken link equity.

### The Fix (2-Minute Setup in Cloudflare Dashboard)

#### Step A: Configure the DNS CNAME Record
1. Log in to your [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Select your domain: `aitoolszone.tech`.
3. In the left sidebar, navigate to **DNS** ➔ **Records**.
4. Click **Add record**:
   * **Type:** `CNAME`
   * **Name:** `www`
   * **Target:** `aitoolszone.tech` (or your Cloudflare Pages hostname, e.g., `ai-tools-zone.pages.dev`)
   * **Proxy status:** **Proxied (🟧 Orange Cloud enabled)**
   * **TTL:** `Auto`
5. Click **Save**.

#### Step B: Create the 301 Permanent Redirect Rule
1. In the Cloudflare left sidebar, click **Rules** ➔ **Redirect Rules**.
2. Click **Create rule**.
3. Configure the rule as follows:
   * **Rule name:** `Redirect WWW to Non-WWW Apex`
   * **If incoming requests match:**
     * **Field:** `Hostname`
     * **Operator:** `equals`
     * **Value:** `www.aitoolszone.tech`
   * **Then (URL Redirect):**
     * **Type:** `Dynamic`
     * **Expression:** `concat("https://aitoolszone.tech", http.request.uri.path)`
     * **Status code:** `301` (Permanent Redirect)
     * **Preserve query string:** Checked / Yes
4. Click **Deploy**.

---

## 2. Google Search Console: Sitemap Refresh

1. Open [Google Search Console](https://search.google.com/search-console).
2. Ensure you have selected the property: `https://aitoolszone.tech/`.
3. In the left navigation menu, click **Indexing** ➔ **Sitemaps**.
4. Under **Add a new sitemap**, enter:
   ```text
   sitemap.xml
   ```
5. Click **Submit**.
6. Verify the status changes to **Success** and that **Discovered pages: 70** is displayed.

---

## 3. Fast-Track Indexing: Manual Priority URL Inspection

Because Google queues pages based on crawl budget for new domains, you can request immediate crawl indexing for our highest-priority commercial and comparison pages:

1. At the very top of Google Search Console, find the search bar: **"Inspect any URL in 'aitoolszone.tech'"**.
2. Paste each of the following 5 priority URLs one by one:
   * `https://aitoolszone.tech/` (Apex Homepage)
   * `https://aitoolszone.tech/compare/chatgpt-vs-gemini/` (High-volume comparison)
   * `https://aitoolszone.tech/compare/canva-vs-adobe/` (High-volume creative comparison)
   * `https://aitoolszone.tech/products/chatgpt-plus/` (Commercial flagship product)
   * `https://aitoolszone.tech/products/capcut-pro/` (High-growth video editing tool)
3. For each URL:
   * Press **Enter**.
   * Click the gray button: **Test Live URL** (Wait ~15-30 seconds).
   * Confirm green checkmark: *"URL is available to Google"*.
   * Click **Request Indexing**.
   * Wait for the confirmation dialog: *"Indexing requested"*.

*(Note: Google limits manual requests to roughly 10-15 per day, which is why doing these top 5 yields maximum immediate ROI).*

---

## 4. Understanding the Search Console "Links" Report

### The Screenshot Explained
In Google Search Console under **Links** ➔ **Top internally-linked pages**, Google currently shows:
* **Total internal links:** **320**
* Top pages:
  * `https://aitoolszone.tech/` — **50 links**
  * `https://aitoolszone.tech/guides/` — **34 links**
  * `https://aitoolszone.tech/privacy/` — **33 links**
  * `https://aitoolszone.tech/products/` — **28 links**

### Why this caused the 22 "Discovered - currently not indexed" pages:
* Googlebot discovered pages via `sitemap.xml`, but saw that comparison pages (`/compare/chatgpt-vs-gemini/`) and newly added products had almost 0 direct links from the homepage body.
* In contrast, utility pages like `/privacy/` had 33 links because they were in every footer.
* Googlebot concluded: *"These comparison pages aren't linked prominently by the site owner, so they are low crawl priority."*

### What We Did to Fix This:
* In Commit `89a4336`, we injected **271 new contextual internal links** across the homepage body, header navigation, and category hubs pointing directly to all 8 comparison hubs and all 20 product pages.
* **Expected Result:** Over the next 3 to 7 days, as Googlebot recrawls the homepage and navigation, Google's reported internal link count will jump from **320 to 591+**, automatically promoting the 22 queued pages into active indexing.

---

## 5. How to Monitor Progress Over the Next 14 Days

| Day Range | Search Console Metric to Check | Expected Health Milestone |
|:---|:---|:---|
| **Days 1–3** | Sitemaps ➔ `sitemap.xml` | Status: *Success*, Discovered: 70 URLs. |
| **Days 4–7** | Pages ➔ "Discovered - not indexed" | Count should drop from 22 down to <10 as Google crawls the new internal links. |
| **Days 8–10** | Links ➔ Top internally-linked pages | Total internal links should increase from 320 to 500+. |
| **Days 11–14** | Performance ➔ Search Results | Daily impressions should increase above 15–20/day, with queries like `"ai tools zone pakistan"` maintaining #1 and product queries beginning to surface. |
