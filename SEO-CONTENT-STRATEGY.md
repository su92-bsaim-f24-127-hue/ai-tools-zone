# AI Tools Zone content strategy

Updated 20 October 2026. The site has 53 canonical sitemap URLs, including 20 product pages. The 205-row [keyword map](SEO-KEYWORD-MAP.csv) assigns intent to existing destinations; it contains no measured search volumes or rank estimates. This strategy keeps the current useful page set stable and improves it from real customer and webmaster evidence.

## Page roles and editorial rules

| Page group | Buyer intent | Content to maintain | Evidence required |
|---|---|---|---|
| Homepage and `/pricing/` | Browse Pakistani offers; compare budget and terms | Short direct answer, current catalog, clear seller identity and purchase steps | Catalog values and owner-confirmed current terms |
| 20 `/products/{slug}/` pages | Check a particular product, price or plan | One offer per page; PKR amount, duration/allowance, access, limitations, confirmation step, canonical URL and relevant links | Current supplier terms and owner-checked offer; do not imply vendor authorization |
| Category and use-case pages | Find a tool for a task, audience or workflow | Explain the task and selection criteria, then link only to relevant listed offers | The displayed catalog and a clear distinction between description and hands-on testing |
| Comparison and alternative pages | Evaluate named options | Compare the same dimensions and disclose differences in access, duration and price | Comparable current offers; never imply equivalent plans when terms differ |
| Methodology and access guides | Understand how prices and account access work | Explain what the listing means, what is not verified, and what a buyer should confirm | Current owner process and primary vendor policy pages when making vendor-policy claims |

Each page should answer its intended question early, identify the source and date of change where facts can expire, use one descriptive H1 and meaningful subheadings, and offer a helpful internal next step. Keep visible copy and structured data consistent. Product and seller claims must remain bounded to what the owner can substantiate; customer reviews, official affiliations, inventory certainty, guaranteed outcomes and “lowest price” claims require separate evidence and must not be fabricated.

## Research and prioritization

Start with Google Search Console and Bing Webmaster query/page data once the owner verifies those properties. Review impressions, clicks, country, device, indexed/canonical state and the actual landing page; annotate deployment dates and compare like-for-like date windows. After verification, also inspect Search Console's Generative AI performance report for AI-feature impressions/pages where data is available; keep this separate from conventional clicks and owner-confirmed orders. Google announced worldwide report availability on 31 August 2026 ([official report announcement](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports?facet3=pdf)). Add recurring buyer questions from support only as anonymized themes. Use Cloudflare Web Analytics for aggregate visits/referrers; it does not currently record custom search, product, WhatsApp or purchase conversion events. A WhatsApp click is not a sale.

Competitor work is a bounded hypothesis source, not a proxy for ranking, traffic or quality. The 20 October public sample found global directories emphasizing category/task discovery and local seller pages showing dated PKR comparisons with duration, access and methodology. Improve the existing `/pricing/`, catalog-methodology and product pages only after the owner verifies their own current facts and assigns a maintenance owner. The new sample and earlier skipped-page limits are documented in [COMPETITOR-RESEARCH.md](COMPETITOR-RESEARCH.md); do not infer inaccessible competitors' content.

Do not create pages for every product/query/city permutation. A new URL needs a distinct customer decision, original answer, sufficient current facts, a non-overlapping destination and a maintenance owner. Otherwise update the existing canonical page. Do not copy competitor copy, use generated doorway pages, fabricate reviews or claim first place.

## GEO and answer visibility

Write clear, quotable answers for people, cite the basis of time-sensitive seller facts, and maintain normal crawlability, useful pages and valid visible-page-matched structured data. Google states its AI features use the same foundational SEO requirements and does not require special AI text files or “GEO hacks”; inclusion is not guaranteed ([Google AI features guidance](https://developers.google.com/search/docs/appearance/ai-features), [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)). Structured data can make a page eligible for supported search displays but does not guarantee a rich result; it must reflect visible content ([Product snippets](https://developers.google.com/search/docs/appearance/structured-data/product-snippet)).

## Review cycle

- Monthly: check catalog accuracy, broken internal links, sitemap/canonical changes, Search Console coverage and representative mobile pages.
- Quarterly: review query/page demand and anonymized customer questions; update only the destination that needs a clearer answer.
- After a material offer change: rebuild, run SEO/growth/browser checks, confirm the sitemap reflects actual content changes, then publish through the existing GitHub Pages workflow.

Current implementation state, open measurement limits and the 30/60/90-day owner actions are in [SEO-AUDIT.md](SEO-AUDIT.md), [SEO-IMPLEMENTATION.md](SEO-IMPLEMENTATION.md) and [SEO-PLAN.md](SEO-PLAN.md).
