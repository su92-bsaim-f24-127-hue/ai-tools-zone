# Phase 3.1.2 — Group C Corrections & Group D Exclusions Audit

**Project:** AI Tools Zone  
**Website:** https://aitoolszone.tech/  
**Audit Date:** 12 November 2026  

---

## 1. Group C Audit: Three Pages Requiring Substantive Corrections

The following 3 pages from the candidate pipeline contain material identity, pricing, or categorization problems and are **strictly held from production release**:

### 1. `google-notebooklm-pro` (Google NotebookLM Pro)
- **Material Defect:** Google NotebookLM (`notebooklm.google.com`) is an experimental research tool provided **free of charge** by Google. Google has not launched a standalone consumer 'NotebookLM Pro' paid tier. Commercial features are available only via enterprise Google Workspace Gemini add-ons.
- **Consumer Trust Risk:** Advertising a 'Pro' tier for a free Google product risks misleading Pakistani students and researchers.
- **Correction Plan:** Reframe page title and content to *'Google NotebookLM Guide & Workspace Integration'*. Explicitly inform users that personal NotebookLM is free, while AI Tools Zone provides enterprise Google Workspace domain setup.
- **Status:** `HOLD — CONTENT CORRECTION REQUIRED` (Excluded from release).

### 2. `google-ai-ultra` (Google AI Ultra)
- **Material Defect:** Google's paid consumer tier is officially branded as *'Google One AI Premium'* ($19.99/mo, granting access to Gemini Advanced / 1.5 Pro). 'Ultra' refers to Google's model architecture (Gemini Ultra), not a standalone consumer subscription.
- **Consumer Trust Risk:** Naming ambiguity leads to confusion with Google's active product `gemini-pro` (PKR 2,000).
- **Correction Plan:** Rename product to *'Google One AI Premium (Gemini Advanced)'* and document exact 2TB Google Drive + Gemini Advanced bundle features.
- **Status:** `HOLD — CONTENT CORRECTION REQUIRED` (Excluded from release).

### 3. `enterprise-ai-api-credits` (Enterprise AI API Credits)
- **Material Defect:** This listing represents an aggregate, generic concept rather than an identifiable SaaS subscription.
- **Consumer Trust Risk:** Users cannot evaluate pricing, quotas, or delivery terms without knowing the specific provider (e.g. OpenAI vs Anthropic vs OpenRouter).
- **Correction Plan:** Split into specific developer credit guides or move to an agency B2B consulting section (`/services/developer-api/`).
- **Status:** `HOLD — CONTENT CORRECTION REQUIRED` (Excluded from release).

---

## 2. Group D Audit: Five Permanently Rejected Risk Offerings

The 5 rejected candidate products were audited across all repository assets to ensure zero commercial leakage:

| Rejected Product | Identifier Slug | Core Reason for Permanent Rejection | Production Catalog Check | Staging HTML Check | Sitemap Check | Category Hub Check | Final Safety Verdict |
|---|---|---|:---:|:---:|:---:|:---:|:---:|
| **All-in-One Mega AI Portal** | `all-in-one-mega-ai-portal` | Shared multi-tool cookie portal; guaranteed session death & 90%+ support churn | **0 (Clean)** | **0 (None)** | **0 (None)** | **0 (None)** | `PERMANENTLY EXCLUDED` |
| **Turnitin Student / Instructor** | `turnitin-plagiarism-checker` | Institutional academic licensing; extreme ethical violation; high ban rate | **0 (Clean)** | **0 (None)** | **0 (None)** | **0 (None)** | `PERMANENTLY EXCLUDED` |
| **Midjourney Pro** | `midjourney-pro` | Discord MFA binding; constant IP verification blocks and account lockouts | **0 (Clean)** | **0 (None)** | **0 (None)** | **0 (None)** | `PERMANENTLY EXCLUDED` |
| **SEMrush Pro** | `semrush-pro` | Strict anti-bot browser fingerprinting; immediate cookie invalidation | **0 (Clean)** | **0 (None)** | **0 (None)** | **0 (None)** | `PERMANENTLY EXCLUDED` |
| **Spotify Premium** | `spotify-premium` | Non-AI commodity entertainment; geographic address verification lockouts | **0 (Clean)** | **0 (None)** | **0 (None)** | **0 (None)** | `PERMANENTLY EXCLUDED` |

### Safety Affirmation:
- 0 HTML files exist in `staging/catalog-expansion/products/` for any of the 5 rejected products.
- 0 entries exist in `staging/catalog-expansion/sitemap-77.xml` or production `sitemap.xml`.
- 0 product cards appear in any of the 20 staged category hubs.
- The records are preserved solely in internal CSV archives (`expanded_product_inventory_77.csv`) for risk governance.