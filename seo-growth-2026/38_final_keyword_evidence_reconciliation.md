# FINAL KEYWORD EVIDENCE & CLASSIFICATION RECONCILIATION

**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Branch:** `feature/competitor-product-keyword-growth`  
**Audit Stage:** Phase 2.1 — Evidence & Risk Reconciliation  
**Date:** 2026-11-12

## 1. Resolution of Inconsistencies in Previous Keyword Reports

The Phase 2 independent review identified two important classification overstatements in the initial keyword research:

1. **224 Keywords Classified as 'Observed Competitor Ranking Queries':**  
   - *Audit Finding:* These keywords were identified based on their presence in competitor H1 tags, title elements, and URL slugs (`aitoolspak.tech/claude-pro-pakistan/`, `aitoolgems.tech/tools/midjourney/`).  
   - *Correction:* The presence of a keyword in competitor page copy or URL paths proves that the competitor **targets** that keyword; it does NOT prove that the competitor ranks on page 1 of Google Pakistan or captures traffic.  
   - *Reclassification:* Reclassified as **`Competitor-Targeted On-Page Keyword (H1/Title/URL Observation)`**.

2. **98 Keywords Classified as 'Google Keyword Planner Data':**  
   - *Audit Finding:* No raw exported Google Keyword Planner CSV, XLSX, or API token export exists in the repository for these 98 queries.  
   - *Correction:* Adhering to the non-fabrication rule, unverified third-party planner attributions must be downgraded.  
   - *Reclassification:* Downgraded to **`Modeled Commercial Intent Keyword (Downgraded: No Direct GKP CSV Export)`**.

## 2. Reconciled 6-Tier Keyword Evidence Breakdown (847 Keywords)

| Classification Tier | Previous Label | Corrected Empirical Classification | Count | % | Evidence Grounding |
|---|---|---|---|---|---|
| **Tier 1** | GSC Query | **Actual Google Search Console Query (Verified First-Party Data)** | 35 | 4.1% | Verified impressions in `phase-7/phase_7b_gsc_performance_report.md` |
| **Tier 2** | Observed Ranking Query | **Competitor-Targeted On-Page Keyword (H1/Title/URL Observation)** | 224 | 26.4% | Direct match to public H1s/URLs of `aitoolspak.tech` and `aitoolgems.tech` |
| **Tier 3** | SERP Query | **SERP-Observed Query (Google PK Auto-Suggest / PAA Observation)** | 185 | 21.8% | Live Google Pakistan search suggestions and PAA query strings |
| **Tier 4** | GKP Data | **Modeled Commercial Intent Keyword (Downgraded: No Local GKP CSV)**| 98 | 11.6% | Programmatic intent-modeled commercial search patterns |
| **Tier 5** | Tool Estimate | **Third-Party Tool Benchmark (DataForSEO / Semrush Estimate)** | 62 | 7.3% | Phase 5 competitive domain overlap and SERP difficulty data |
| **Tier 6** | Generated Hypothesis | **Generated Buyer-Intent Hypothesis (Programmatic Local Pattern)** | 243 | 28.7% | Synthesized intent modifiers (`[tool] jazzcash`, `order [tool] easypaisa`) |
| **Total** | — | **Full Reconciled Keyword Inventory** | **847** | **100.0%** | [`23_buyer_intent_keyword_map.csv`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/seo-growth-2026/23_buyer_intent_keyword_map.csv) |

## 3. Strict Boundary Rules on Demand, Rankings, Traffic & Conversions

1. **Search Demand $\neq$ Traffic:** Search volume indicates market curiosity; it does not indicate website visitors.
2. **On-Page Targeting $\neq$ Ranking:** A competitor placing `buy claude in pakistan` in an H1 does not prove they hold top ranking.
3. **Ranking $\neq$ Sales:** Even top-ranked pages experience bounce rates; sales conversion depends on local trust, payment ease, and WhatsApp responsiveness.
4. **Zero Competitor Traffic Claims:** AI Tools Zone asserts zero claims regarding competitor monthly visits or revenue.