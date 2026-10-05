> **6 October 2026 update:** Current strategy: improve qualified discovery and WhatsApp conversion using real offer clarity and buyer questions. Prioritize Search Console evidence over page volume. Cloudflare visitor analytics is connected; custom click events are local hooks only. See [AI-VISIBILITY-MONITORING.md](AI-VISIBILITY-MONITORING.md) for a 30-day operating plan and [SEO-GROWTH-RELEASE.md](SEO-GROWTH-RELEASE.md) for the shipped changes.

# Search, answer and entity strategy

AI Tools Zone is an independent Pakistan-focused marketplace. Its useful search proposition is a readable catalog of seller-listed PKR offers, with explicit duration, access, limitations and WhatsApp confirmation. It is not an official reseller or a benchmark laboratory unless evidence establishes that separately.

## Architecture and intent ownership

Keep `/` for the business and overall discovery. `/products/` lists all offers; existing product URLs own brand + Pakistan + price + buy queries. `/categories/` groups ten actual catalog categories. `/use-cases/` contains four audience workflows. `/compare/` has three selected comparisons. `/alternatives/` has two task-oriented shortlists. `/guides/` explains choosing a subscription and access types. `/pricing/` owns catalog-wide PKR and budget comparisons using section anchors instead of duplicate pages.

The implementation creates 28 pages, taking the canonical sitemap from 24 to 52. This is not a target page count to keep increasing. New pages require a distinct decision, actual supporting catalog data, original useful content, relevant internal links and an owner able to keep them current.

[SEO-KEYWORD-MAP.csv](SEO-KEYWORD-MAP.csv) records intent, competitor evidence, baseline coverage, destination, priority, content type, links, schema, direct-answer opportunity and entity context. Priority reflects purchase relevance, usefulness and maintainability, not invented search volume.

## Linking and entity model

Home links to all hubs, categories and product detail pages in initial HTML. Categories link to their products and selected workflows/comparisons. Products link back to their category and relevant editorial pages. Editorial tables link to products. Breadcrumbs connect every non-home canonical page with a useful parent. The audited maximum link distance from home is two clicks.

One Organization ID and one WebSite ID identify AI Tools Zone consistently. WebPage nodes describe documents; Product/Offer nodes describe the seller offers; ItemList nodes describe collections, not fabricated ratings. BreadcrumbList mirrors visible navigation. Official vendor links identify product references without `sameAs` assertions about marketplace ownership. No invented social profiles, addresses, certifications or affiliation.

SoftwareApplication markup is deliberately omitted: the catalog mixes invitations, shared accounts, licenses, credits and non-software services, and lacks verified application-level operating-system/rating/entitlement data. Product + Offer is the more accurate description of these offers. FAQ answers are visible, accessible content; no FAQ rich-result promise or unsupported review schema is added. Rich-result eligibility and actual presentation must be checked separately.

## Direct answers and editorial rules

Product introductions state the tool, seller, PKR price, duration/allowance, access and confirmation requirement. Categories answer what work the tools address. Comparisons explain the decision before a generated price table. Questions receive short answers followed by supporting details and relevant sources.

Preserve original seller figures without treating them as independently verified vendor prices. Never infer that a lower price buys the same entitlement. Do not invent current model names, quotas, inventory, discount percentages or performance scores. General advice is framed as a selection method, not personal hands-on testing. Product references support vendor context, not authorization of the seller's offer.

For Pakistan intent, use PKR, actual ordering methods and the correct contact number. English content uses `en-PK`. No hreflang is emitted because there are no separately maintained translations. No city doorway pages or unsupported LocalBusiness address is added.

## Crawl policy and hosting

Googlebot and Bingbot inherit public wildcard access. OAI-SearchBot is explicitly allowed for discovery. GPTBot is separately disallowed as a conservative training opt-out; no training permission is granted to achieve search access. ChatGPT-User is not blocked, but user-triggered access has different behavior and is not promised by robots alone. Unknown bot-specific allowances were not added. Actual crawler identities require provider-published verification, not trusting a spoofable user-agent.

Production packaging is an allowlist. It excludes `.git`, source catalog, templates, scripts, diagnostics, private environment files and reports. A public GitHub repository still exposes committed source: robots is not access control. Never commit secrets. `_headers` remains a portable host configuration example; GitHub Pages does not enforce it. Stronger custom HTTP headers need a compatible host or edge proxy, not fictitious application of this file.

## Freshness and catalog maintenance

Edit `data/catalog.json`, preserving each `slug` even when a display name changes. Validate availability, entitlement, eligibility, duration, access, vendor link and support terms with the seller before accepting payment. Review active offers weekly and immediately on a supplier change; do not invent a verification timestamp when only the page layout changes.

Edit original guidance in `data/seo-content.json`; update it when vendor policies or buyer needs change. All price tables, structured offers and prepared messages derive from the catalog. There are no independently maintained price copies in the new editorial copy.

`data/page-state.json` persists a semantic content hash and lastmod. The fingerprint includes visible text, metadata, links and schema, while ignoring style/ordinary script bodies and asset cache tokens. Unchanged builds retain dates. Date-only freshness uses the Pakistan business calendar (UTC+05:00) consistently in local builds and UTC-hosted CI. Dates indicate a page-content change, not a price/stock verification. Never reset the state file just to make pages look fresh. Review deleted URLs before removing a page: GitHub Pages has no general per-path 301 configuration. Preserve useful URLs or configure a real host redirect before a migration.

## Measurement without invented results

No analytics service was present and none is connected now. `measurement.js` dispatches local `aitz:measure` events for page views, WhatsApp clicks, finder opens and comparison opens. It sends no network data and stores nothing. Payloads omit query strings, order-message text, phone/customer details and search terms. These events are integration hooks, not recorded conversion counts. A WhatsApp click is only a lead-intent event, not a sale.

If the owner later chooses a privacy-appropriate analytics provider, attach a listener before the deferred measurement script, review consent/privacy obligations for the selected setup and update the privacy policy. Measure organic landing-page visits and lead intent; reconcile actual sales separately with order records.

| Source | Weekly measurement | Required manual setup |
|---|---|---|
| Google Search Console | Impressions, clicks, CTR, position, queries, landing pages, indexed/excluded pages, CWV reports | Verify DNS domain property, submit sitemap, inspect representative templates |
| Bing Webmaster Tools | Crawl/index status, query/page performance; AI Performance if exposed for the account | Verify/import property, submit sitemap, inspect URLs; do not claim unavailable reports exist |
| Optional site analytics | Product/category/comparison visits and WhatsApp intent by landing page/referral | Choose provider and implement approved collection; current hooks do not collect |
| Manual AI/search sample | Citation URL, prompt, model/search mode, date, locale and whether site is actually cited | Repeat a small fixed sample without treating one result as rank or market share |
| Actual order records | Confirmed inquiries and completed orders | Owner records outcomes; no message content captured by this website |

Sample monitoring questions: “How much does ChatGPT Plus cost in Pakistan?”, “Which AI tools fit a student budget in Pakistan?”, “What is private versus shared AI access?”, “ChatGPT or Gemini for study?”, and “Which tool should I use for editing existing videos?”. Record absence as absence, not a guaranteed future result. Establish a baseline, review after 28 days and again after 90 days; do not manufacture traffic targets without baseline data.

## Primary technical references

- [Google: AI features and websites](https://developers.google.com/search/docs/appearance/ai-features): normal search eligibility and useful accessible content still matter; no special AI schema or AI text file is required.
- [Google: building sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap): use canonical URLs and accurate meaningful lastmod values.
- [Google: Product snippets](https://developers.google.com/search/docs/appearance/structured-data/product-snippet): structured product data must describe the visible offer; test eligibility rather than assume display.
- [OpenAI crawler documentation](https://developers.openai.com/api/docs/bots): search discovery and training crawler controls are separate.
- [Bing crawler documentation](https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0): use official crawler guidance; the web reader returned a sparse page, so no additional crawler behavior is inferred.

Better crawlability and clearer content can improve eligibility and understanding. Rankings, indexing, rich results and AI citations are not guaranteed.
