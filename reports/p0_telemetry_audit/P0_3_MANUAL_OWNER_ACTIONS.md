# P0.3 & P0.2 — Manual Owner Actions & Configuration Guide

**Project:** AI Tools Zone  
**Production Domain:** `https://aitoolszone.tech/`  
**Execution Timestamp:** November 14, 2026  
**Audience:** Site Owner / Google Account Administrator  
**Estimated Time Required:** 10–15 minutes total  

---

## 1. Overview of Required Owner Actions

Because third-party agents and automated CLI tools cannot log into your personal Google account without violating security boundaries, the following **two critical setup tasks** must be performed directly by the site owner:

1. **Google Search Console (P0.2):** Submit priority commercial URLs for immediate crawling and indexing re-evaluation.
2. **Google Analytics 4 (P0.3):** Mark `whatsapp_click` / `product_whatsapp_click` as **Key Events** (Conversions) and register custom dimensions in the GA4 Admin Console.

---

## 2. Google Search Console Actions (P0.2)

### Step 1: Open Google Search Console
1. Navigate to: [https://search.google.com/search-console](https://search.google.com/search-console)
2. In the top-left property dropdown, ensure you are on `https://aitoolszone.tech/` (or the Domain property `aitoolszone.tech`).

### Step 2: Confirm Sitemap Status
1. Click **Sitemaps** in the left sidebar (under *Indexing*).
2. Look at the submitted sitemap: `https://aitoolszone.tech/sitemap.xml`.
3. Verify that the **Status** column displays **"Success"**.
4. Confirm that **Discovered pages** reflects **95** (or is updating toward 95).
   > *Note:* If it is already marked "Success", do NOT resubmit it.

### Step 3: Request Priority URL Indexing (Top 5 Commercial Pages)
For each of the 5 priority URLs below, perform the following in the top Search Console inspection bar:

1. Paste URL #1: `https://aitoolszone.tech/products/chatgpt-plus/` and press `Enter`.
2. Wait for Google to retrieve data from the index.
3. If it says *"URL is not on Google"* or *"Discovered - currently not indexed"*, click the **"TEST LIVE URL"** button in the top right.
4. Once the live test completes with a green checkmark, click **"REQUEST INDEXING"**.
5. Repeat for the remaining 4 URLs:
   - `https://aitoolszone.tech/products/canva-pro-edu/`
   - `https://aitoolszone.tech/products/capcut-pro/`
   - `https://aitoolszone.tech/products/adobe-creative-cloud/`
   - `https://aitoolszone.tech/products/replit-core/`

> [!TIP]
> Google enforces a daily quota on manual indexing requests (typically 10–20 per day). Submitting these top 5 commercial revenue drivers ensures Googlebot re-crawls your highest-value pages first.

---

## 3. Google Analytics 4 (GA4) Configuration (P0.3)

Our automated browser tests confirmed that your website is actively transmitting `whatsapp_click`, `product_whatsapp_click`, and `generate_lead` with PKR price values to Measurement ID `G-TSBF626Q60`. 

To turn these into visible **Key Events** (formerly known as Conversions) and report on them by product name:

### Step 1: Mark Events as Key Events
1. Open Google Analytics: [https://analytics.google.com/](https://analytics.google.com/)
2. Select your AI Tools Zone property (`G-TSBF626Q60`).
3. Click the **Admin** gear icon in the bottom-left corner.
4. Under the **Data display** section, click **Events**.
5. In the existing events table, locate:
   - `whatsapp_click`
   - `product_whatsapp_click`
   - `generate_lead`
6. Toggle the switch in the **Mark as key event** column to **ON (Blue)** for each.
   > *Note:* If `product_whatsapp_click` does not appear in the table yet because it has not received traffic in the last 24 hours, click the blue **"Create event"** or **"New key event"** button at the top right, type `product_whatsapp_click` exactly, and save.

### Step 2: Register Custom Dimensions (Product & Section)
To see which specific AI tool or website section generated the WhatsApp click:
1. In the same **Admin** > **Data display** menu, click **Custom definitions**.
2. Click **Create custom dimension** (blue button).
3. Set up Dimension 1:
   - **Dimension name:** `Product Name`
   - **Scope:** `Event`
   - **Description:** `The AI tool identifier clicked for WhatsApp order`
   - **Event parameter:** `product`
   - Click **Save**.
4. Set up Dimension 2:
   - **Dimension name:** `Page Section`
   - **Scope:** `Event`
   - **Description:** `Website section where interaction occurred`
   - **Event parameter:** `section`
   - Click **Save**.

---

## 4. Business Impact of Completing These Actions

- **Search Console Submission:** Breaks the indexing freeze on your top revenue-generating tools so they appear in Google search results for Pakistani users.
- **GA4 Key Event Tagging:** Allows you to see exactly which Google search keywords and landing pages generate high-intent WhatsApp order conversations.
- **Revenue Clarity:** Accurately separates casual homepage visitors from commercial buyers ordering ChatGPT, Canva, or Adobe subscriptions.
