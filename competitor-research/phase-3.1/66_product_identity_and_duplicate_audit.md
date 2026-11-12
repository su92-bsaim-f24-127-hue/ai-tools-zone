# Phase 3.1 — Product Identity and Duplicate Overlap Audit

**Project:** AI Tools Zone  
**Website:** https://aitoolszone.tech/  
**Audit Date:** 12 November 2026  
**Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  

---

## 1. Executive Summary

This report investigates reported product overlaps, brand naming ambiguities, and potential keyword cannibalization across the 77-product inventory.
The objective is to determine whether records represent identical products, different editions, distinct access models, or naming artifacts, and to recommend definitive canonical treatments.

---

## 2. Detailed Audit of Reported Overlaps

### A. Existing Grammarly vs New Grammarly Premium
- **Findings:** An audit of `data/catalog.json` reveals that AI Tools Zone **does not** currently sell Grammarly on its active production site. The mention of 'existing Grammarly' arose from earlier roadmap discussions. The candidate `grammarly-premium` (ID: `grammarly`, slug: `grammarly-premium`) in `ENQUIRE` status represents the sole Grammarly record.
- **Search Intent:** Targets high-volume queries like `grammarly in pakistan`, `grammarly premium price pakistan`, and `buy grammarly pakistan`.
- **Canonical Recommendation:** Maintain single canonical page at `/products/grammarly-premium/`. No cannibalization risk exists.

### B. Existing QuillBot vs New QuillBot
- **Findings:** Like Grammarly, QuillBot does not exist in `data/catalog.json`. The only record is `quillbot-premium` (ID: `quillbot`, slug: `quillbot-premium`) in `ENQUIRE`.
- **Search Intent:** Targets `quillbot in pakistan`, `quillbot premium pkr`, and `quillbot paraphraser pakistan`.
- **Canonical Recommendation:** Single canonical destination at `/products/quillbot-premium/`. Zero duplicate conflict.

### C. Perplexity vs Perplexity Pro
- **Findings:** In competitor pricing tables, competitor sites list 'Perplexity' and 'Perplexity Pro' interchangeably. Perplexity AI provides a free tier, while its commercial offering is 'Perplexity Pro' ($20/month).
- **Catalog Status:** AI Tools Zone has cataloged exactly one record: `perplexity-pro` (ID: `perplexity`, slug: `perplexity-pro`).
- **Canonical Recommendation:** Use `/products/perplexity-pro/` as the primary canonical destination. The page title and H1 capture both 'Perplexity AI' and 'Perplexity Pro' search intent, avoiding duplicate pages.

### D. Replit vs Replit Core
- **Findings:** Replit rebranded its individual paid tier from 'Replit Hacker' to 'Replit Core'. AI Tools Zone already has `replit-core` in active production (`data/catalog.json`, PKR 3,200). Competitor research extracted Replit Core, but Phase 3 correctly reconciled it with the active catalog.
- **Canonical Recommendation:** Preserve the existing active production URL `/products/replit-core.html`. Do not publish a separate `/products/replit/` page. Re-confirm that Replit Core satisfies all generic 'Replit in Pakistan' queries.

### E. DeepSeek vs DeepSeek R1
- **Findings:** DeepSeek operates free web chat and API endpoints, while DeepSeek R1 is its open-weights reasoning model. Pakistani users search for 'DeepSeek in Pakistan' seeking web access and local billing support. The catalog contains a single record: `deepseek-unlimited` (ID: `deepseek`, slug: `deepseek-unlimited`).
- **Canonical Recommendation:** Keep single canonical page at `/products/deepseek-unlimited/`. Dedicated articles comparing DeepSeek R1 to ChatGPT Plus can be staged under `/blog/` or `/compare/` without creating duplicate product listings.

### F. GitHub Copilot: ENQUIRE vs COMING_SOON
- **Findings:** In Report 64's textual diagram, `github-copilot` was erroneously listed in both branches. A code-level audit of `data/draft-catalog-recommendations.json` and `expanded_product_inventory_77.csv` confirms GitHub Copilot appears **exactly once**, classified as `ENQUIRE` with slug `github-copilot`.
- **Canonical Recommendation:** Retain `/products/github-copilot/` under `ENQUIRE`. Correct the narrative documentation to remove the duplicate mention.

---

## 3. Brand & Plan Distinction Audit

The table below analyzes similar product lines across the 77 inventory items:

| Brand | Product Line 1 | Product Line 2 | Nature of Distinction | Justification for Separate URLs |
|---|---|---|---|---|
| **Google** | Gemini Pro (Active) | Google AI Ultra (Coming Soon) | Tier / Architecture (Pro vs Ultra 2M token tier) | Distinct official pricing ($20 vs $250+ enterprise) |
| **Google** | Google NotebookLM Pro (Coming Soon) | Google One 2TB (Active) | Function (AI Research Workspace vs Cloud Storage) | Distinct workflows and standalone user bases |
| **TradingView** | TradingView Pro (Coming Soon) | Windows 11 Pro Key (Active) | Different software categories (Finance vs OS) | Unrelated software products |
| **Anthropic** | Claude Pro (Enquire) | None (Single Anthropic offer) | Flagship consumer subscription | N/A |

---

## 4. Slug Uniqueness and Consistency Audit

- **Total Slugs Tested:** 77 across JSON, CSV, staging HTML, and sitemaps.
- **Unique Slugs:** 77 (100%).
- **Collisions:** 0.
- **Character Standard:** Lowercase alphanumeric characters separated by single hyphens (`^[a-z0-9]+(-[a-z0-9]+)*$`). All slugs conform.