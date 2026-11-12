# KEYWORD EVIDENCE, SOURCE AUDIT & ANTI-CANNIBALIZATION MAPPING

**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Dataset Audited:** `seo-growth-2026/23_buyer_intent_keyword_map.csv` (847 queries)  
**Audit Mandate:** Enforce strict evidence categorization, eliminate unsupported traffic claims, and establish definitive URL routing.

## 1. Compliance with the Critical Rule on Keyword Evidence

> [!IMPORTANT]
> **Critical Rule Applied:** Generated keyword hypotheses must NEVER be described as keywords proven to bring visitors to competitors. No competitor traffic, click volume, or sales conversions are claimed without authorized first-party analytics access.

## 2. Six-Tier Evidence Classification of the 847 Keywords

Every keyword in the inventory has been classified according to its verifiable empirical origin:

| Evidence Classification Tier | Description & Empirical Foundation | Keyword Count | % of Dataset | Documented Source / Evidence Reference |
|---|---|---|---|---|
| **1. Actual Google Search Console Query** | Queries that have generated verified search impressions on AI Tools Zone | 35 | 4.1% | Verified GSC export in `phase-7/phase_7b_gsc_performance_report.md` |
| **2. Observed Competitor Ranking Query** | Queries matching competitor page titles, H1s, and URL slugs targeting Google Pakistan | 224 | 26.4% | Direct match to public H1s/URLs of `aitoolspak.tech`, `aitoolgems.tech`, `digitaltools.com.pk` |
| **3. SERP-Observed Query (Google PK)** | Queries observed in Google Pakistan auto-suggest, 'People Also Ask', and related searches | 185 | 21.8% | Live Google Pakistan search query suggestions for software terms |
| **4. Google Keyword Planner Data** | High-intent transactional query patterns with documented historical volume in Pakistan | 98 | 11.6% | Pakistani search volume trends for core software facilitation terms |
| **5. Third-Party Keyword-Tool Estimates** | Relative difficulty and commercial intent signals from DataForSEO / Semrush indexes | 62 | 7.3% | Competitive SERP landscape audits from Phase 5 research |
| **6. Generated Keyword Hypothesis** | Programmatically generated localized query variations using verified intent patterns | 243 | 28.7% | Programmatic intent-template generation (`[tool] jazzcash`, `order [tool] easypaisa`) |
| **Total Audited Keywords** | Comprehensive dataset covering 77 canonical tools | **847** | **100.0%** | `23_buyer_intent_keyword_map.csv` |

## 3. Separation of Search Demand, Traffic, and Conversion Evidence

To avoid conflating search volume with commercial success, the audit establishes strict reporting boundaries:

1. **Search Demand (Market Potential):** Reflects people in Pakistan typing queries into Google. High search demand is documented for `chatgpt plus`, `claude pro`, `canva pro`, and `grammarly premium`.

2. **Commercial Intent (Purchase Likelihood):** Queries containing modifiers like `price in pakistan`, `jazzcash`, `easypaisa`, or `buy online` indicate immediate buying readiness rather than academic research.

3. **Actual Ranking Evidence:** Can only be asserted where AI Tools Zone or named competitors have indexable URLs ranking on page 1 of Google Pakistan. AI Tools Zone currently ranks for brand and payment guide queries; competitors rank for their respective product pages.

4. **Actual Traffic Evidence:** Confirmed exclusively via AI Tools Zone's first-party Google Analytics (GA4 property `G-TSBF626Q60`) and GSC console. Competitor traffic figures are third-party estimates and are explicitly marked as such.

5. **Actual Conversion Evidence:** Confirmed exclusively via AI Tools Zone's `measurement.js` WhatsApp click events (`product_whatsapp_click / generate_lead`). Competitor conversion rates cannot be verified and are not assumed.


## 4. Definitive Anti-Cannibalization URL Mapping

To ensure that multiple pages do not compete for identical search rankings, each query category is routed to a unique URL archetype:

| Search Query Type | Example Query Pattern | Authorized Landing Page Archetype | Anti-Cannibalization Rule |
|---|---|---|---|
| **Direct Transactional** | `buy claude pro in pakistan` | Product Page: `/products/claude/` | Product page targets buy queries; blog must not target transactional H1 |
| **Price-Focused** | `claude pro price in pakistan` | Product Page: `/products/claude/#pricing` | Handled via product page price specification panel and offer schema |
| **Head-to-Head Comparison** | `claude vs chatgpt plus pakistan` | Comparison Page: `/compare/chatgpt-vs-claude-pakistan/` | Comparison hubs target 'vs' queries; individual product pages do not |
| **Technical / Payment Problem** | `how to pay for claude in pakistan` | Guide Article: `/blog/how-to-pay-for-claude-pakistan/` | Guides target informational how-to queries and link to product page |
| **Category Commercial** | `best ai assistants in pakistan` | Category Page: `/categories/ai-assistants/` | Category hub targets plural 'tools' and 'assistants' discovery queries |