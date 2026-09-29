# AI Tools Zone SEO audit

Audit started 29 September 2026. Scope: source generator, templates, catalog, generated HTML, assets, JavaScript, existing test scripts, packaging, GitHub Pages workflow and the public website.

## Verified baseline

The live crawl returned HTTP 200 for all 24 sitemap URLs. Every one had one H1 and a matching HTTPS, non-www canonical. HTTP and www requests resolved to the canonical host; the product URL without a final slash resolved to its slash version. A fabricated route returned 404. A query-string home URL canonicalized to `/`. Raw responses are saved locally in `verification/seo-live-before.json`.

Products, prices and purchase links already exist in initial HTML. There is no demonstrated critical indexing outage. Search/filter state does not create indexable facet URLs. Existing product URLs must be retained.

## Confirmed improvement opportunities

| Priority | Finding | Action |
|---|---|---|
| P1 | Category cards point to a homepage fragment and JavaScript replaces them with buttons | Generate useful category pages and keep crawlable category anchors |
| P1 | Product breadcrumb schema omits the visible catalog level | Match visible and structured breadcrumbs |
| P1 | Non-home pages omit manifest; information pages omit entity schema | Share metadata and entity graph through generator |
| P1 | Product slugs derive from names and would change after a rename | Store stable explicit slugs in catalog |
| P1 | No automated all-page SEO/link graph validation | Add dependency-free audit to local build and CI |
| P2 | No task, comparison, alternatives or price overview pages | Publish a limited original collection with useful decisions and current catalog data |
| P2 | Sitemap has no lastmod | Add persisted content hashes; do not mark unchanged pages fresh |
| P2 | Crawler policy only has wildcard allow | Separate search discovery from training controls |
| P3 | Google Fonts discovered through CSS @import | Discover stylesheet and font connection in HTML head |

Existing optimized hero WebP sizes are 228,446 bytes (desktop) and 73,008 bytes (mobile). Product logos are small local images. Large original logo files are excluded from the production ZIP. The hero already has responsive sizing and high fetch priority; animations support reduced motion. A small early theme script prevents theme flash; catalog, app and scene scripts are deferred. Preserve these working choices.

`_headers` is a deployment template, not an active GitHub Pages security-header configuration. GitHub Pages cannot apply that file. Do not describe the CSP in it as live protection. Robots rules are not access control; production packaging must exclude repository and diagnostic files.

## Evidence limits

No authenticated Search Console, Bing Webmaster, CrUX or analytics property is connected. Index counts, rankings, traffic, real-user LCP/INP/CLS and conversions are unknown. Direct Google and Bing result-page requests failed in the research tool; they do not establish Pakistan rankings. AI Overview/Copilot/ChatGPT citation presence is not verified. Seller prices and access claims originate in the owner's catalog, not vendor authorization or a new stock check.

Final validation and deployment results will be recorded in SEO-IMPLEMENTATION.md. Competitor observations and uncertainty are documented separately in SEO-COMPETITOR-GAPS.md.

## Post-implementation validation

The generated site now has 52 indexable canonical pages and 135 mapped search intents. All 4,197 static SEO checks passed, with no missing metadata, broken internal references, schema/breadcrumb mismatches, orphan pages or initial-HTML product omissions. Maximum crawl depth is two links from home. Browser coverage includes all 52 pages in mobile/no-JS and desktop/JS modes, with additional 320/768/1024-width checks; 121 checks passed. The original storefront regression suite remains at 149 passing checks and axe reported zero violations across 36 states.

External link sampling found 18 accessible destinations and five blocked/timed-out requests among 23 references, with no observed missing-page response. Those five need manual checking; do not equate a bot access error with a broken public link. No controlled before/after speed test or field INP measurement was available, so performance gains are not quantified. Dead-looking legacy CSS was not aggressively removed without proving it unused across all interactive states.

The first CI attempt correctly stopped publishing when the date audit treated Pakistan midnight as a future UTC date. Build and validation now use the same Pakistan calendar, with explicit midnight-boundary regression checks. See the implementation report for the successful deployment record and live URL verification.
