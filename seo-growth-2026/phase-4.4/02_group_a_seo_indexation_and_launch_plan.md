# Phase 4.4 — Group A SEO Indexation & Public Launch Plan
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Scope:** Controlled Activation of Group A Landing Pages from Staging to Production  
**Status:** **SEO ACTIVATION BLUEPRINT**

---

## 1. Background & Rationale

During Phases 4.0 through 4.3, twelve Group A high-opportunity product pages were kept under strict `noindex, nofollow` protection to prevent premature customer acquisition before commercial fulfillment workflows were validated.

With the consulting model fully proven in Phase 4.3, the developer-focused Group A products are now ready for indexation:
1. **`cursor-ai-pro`** (`/products/cursor-ai-pro/`)
2. **`github-copilot`** (`/products/github-copilot/`)
3. **`claude-pro`** (`/products/claude-pro/`)

---

## 2. Step-by-Step Indexation & Release Plan

### Step 1: Pre-Release Verification
- Verify that product pages feature the unbundled consulting model (Model D) with clear domestic PKR pricing (PKR 500 / PKR 1,000) and prominent notices stating that third-party software subscriptions are paid directly by the customer to the vendor.
- Confirm zero claims of unofficial reseller status, shared accounts, or warranty on third-party accounts.

### Step 2: Codebase Modification (`build_site.py` & Metadata)
- Update `data/product-content.json` to switch `is_indexable` to `true` for approved products.
- In `build_site.py`, update the robots meta tag generator to output `<meta name="robots" content="index, follow">` for approved developer products.
- Add approved URLs to `sitemap.xml`.

### Step 3: Google Search Console & IndexNow Ping
- Dispatch IndexNow API notifications for `/products/cursor-ai-pro/`, `/products/github-copilot/`, and `/products/claude-pro/`.
- Request URL Inspection and indexation in Google Search Console.

---

## 3. Ongoing Protection of High-Risk Products

The remaining Group A and off-catalog products remain under strict commercial hold:
- `netflix-premium-4k`: **STRICTLY ON HOLD** (No indexation, no commercial offering).
- `veo-3-ultra` / Google Flow: **STRICTLY ON HOLD** (No indexation, no commercial offering).
- `surfshark-vpn`: **STRICTLY ON HOLD** (No indexation, no commercial offering).
- `n8n-starter`: **STRICTLY ON HOLD** (No indexation, no commercial offering).
