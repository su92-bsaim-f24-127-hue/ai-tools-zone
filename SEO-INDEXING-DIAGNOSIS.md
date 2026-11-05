# AI Tools Zone indexing diagnosis

**Reviewed:** 6 November 2026, Asia/Karachi. Baseline repository: `4187477`. Requests used a browser-like user agent from this workstation, not a verified Googlebot address.

## Confirmed evidence

| Evidence | Observed result | Interpretation |
|---|---|---|
| `python audit_seo_live.py`, 77 requests | 74 final HTTP 200 responses, two 522 responses, one expected 404 | All 71 sitemap pages passed response, single-H1, canonical and entity checks. Overall live audit **failed** because www variants failed. |
| HTTPS www homepage | HTTP 522, no apex redirect | High-priority hostname availability defect. Exact cause requires Cloudflare routing/DNS/account evidence. |
| HTTPS www robots.txt | HTTP 522 on a separate resource probe | The hostname problem also affects crawler-policy retrieval. Apex robots.txt, sitemap.xml, llms.txt and llms-full.txt all returned HTTP 200. |
| HTTP www homepage | 301 to HTTPS www, then 522 | HTTPS upgrade alone does not repair www. |
| HTTP apex homepage | 301 to HTTPS apex, final 200 | Main hostname HTTPS redirect works. |
| `/products/chatgpt-plus` | 307 to `/products/chatgpt-plus/`, final 200 | Temporary normalization exists; it does not prove indexing failure. Links and sitemap use the trailing-slash canonical. |
| Unknown audit route | HTTP 404 | Expected missing-page behavior. |
| `/?category=design` | 200, canonical apex homepage | Query variant identifies the intended homepage. |
| Apex headers | CSP, HSTS and HTTP/3 advertisement present | Observed hosting behavior; no Core Web Vitals score inferred. |
| Product/organization JSON-LD | Seller slugs treated as MPNs; warranty days converted to refund windows; postal returns, zero-day shipping, fixed stock/expiry, lastmod used as validFrom | Unsupported claims confirmed in source. Generator and accuracy checks corrected in this review. |

Raw local evidence is in `verification/strategy-live-before.json`, `verification/strategy-resources.json` and `verification/seo-audit.json`; diagnostics are excluded from production packaging. See [test results](SEO-TEST-RESULTS.md) for validation and deployment limits.

## What the saved Search Console exports establish

Read directly from the owner's Downloads folder. No authenticated account actions were performed in this review.

- `aitoolszone.tech-Coverage-2026-11-02.zip`: the last Chart.csv observation is **2026-10-23**, with **42 indexed, 27 not indexed and 7 impressions**. This is historical evidence, not a November 6 status.
- Its issue table reports **22 discovered/currently not indexed, 2 crawled/currently not indexed and 3 redirect pages**. The 69 known URLs in that snapshot are not the same population as the current 71-URL sitemap.
- `aitoolszone.tech-Coverage-Drilldown-2026-11-02.zip`: lists 22 discovered URLs. The `1970-01-01` last-crawl entries must not be reported as genuine crawl dates.
- `www.aitoolszone.tech-Crawl-stats-Host-status-2026-11-05.zip`: robots fetch failures are **100% on November 1**, then **0% on November 2-4**. This is the **www** hostname. DNS and connectivity charts show 0% failures on those dates. Request volumes and the responsible service are not established.

These files establish historical indexing and a historical www robots problem. They do not establish a WAF cause, a clean Manual Actions report, current rankings, or automatic indexing after adding links. Earlier promises of indexing within days, fixed future link counts and zero penalties are withdrawn.

## Prioritized actions

1. **High, owner configuration:** resolve www routing and validate its robots URL with an apex redirect. Follow [owner actions](SEARCH-CONSOLE-OWNER-ACTIONS.md). No DNS or account settings changed here.
2. **High, implemented in code:** align structured data with supported facts. Preserve Product/Offer identity, brand, seller SKU, price, currency, plan terms and canonical URLs. Optional fields must not contain invented facts merely to silence warnings.
3. **Medium, owner evidence:** inspect excluded URLs individually. Their statuses do not identify duplication, crawl budget or content quality as the exact cause. Compare the reported canonical, crawl and rendered-page evidence before selecting a fix.
4. **Medium, content maintenance:** improve existing commercial and payment guides using verified terms. Avoid overlapping pages and arbitrary word targets.
5. **Measurement:** current Search Console status, manual actions, performance, Core Web Vitals, backlink metrics and completed orders remain unverified here.

References: [Google structured-data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies), [recrawl requests](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl), [Cloudflare bot false positives](https://developers.cloudflare.com/bots/troubleshooting/false-positives/).
