> **6 November 2026 review:** Reviewed the supplied `Desktop/gemini/SEO-STRATEGY.md` against repository `4187477`, local Search Console exports and live HTTP evidence. The supplied file is unchanged. Current inventory: 71 canonical pages and 20 products. See [diagnosis](SEO-INDEXING-DIAGNOSIS.md), [owner actions](SEARCH-CONSOLE-OWNER-ACTIONS.md) and [validation](SEO-TEST-RESULTS.md).

# Search, answer and entity strategy

## Decisions from the supplied strategy

| Recommendation or claim | Evidence and action |
|---|---|
| Cloudflare blocked Googlebot on November 1 | The saved **www** host export reports 100% robots fetch failures that day and 0% November 2-4. It identifies no WAF rule or cause. Current www requests return 522. Investigate hostname routing and Security Events. |
| Bypass a user agent containing Googlebot | A user agent is self-declared. Use verified-bot evidence and narrow exceptions only after identifying the blocking service. WAF custom rules cannot skip Bot Fight Mode; Super Bot Fight Mode differs. [Cloudflare guidance](https://developers.cloudflare.com/bots/troubleshooting/false-positives/). |
| Excellent Core Web Vitals from static hosting | No current LCP, INP or CLS measurements establish this. Measure field data and lab performance separately. |
| 15-25 indexed pages, DA below 5 and precise growth targets | Unverified as current baselines. The coverage export's latest observation is October 23: 42 indexed and 27 excluded. Current rank, backlink, sales and AI-citation metrics need evidence. |
| Minimum 400-800 words per page | Improve missing answers and original usefulness. Google has no preferred word count. [Helpful-content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). |
| Product/return schema means Merchant Center readiness | Unsupported postal returns, refund windows, shipping, manufacturer IDs, stock and offer dates were found in the generator and corrected. Eligibility and actual rich-result display need separate validation. [Structured-data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies). |
| Google Indexing API for products/blogs | This API supports JobPosting or BroadcastEvent inside VideoObject. Use Search Console and the sitemap for this catalog. [API limits](https://developers.google.com/search/apis/indexing-api/v3/using-api). |
| Add IndexNow, sitemap and canonicals | Already implemented. Preserve stable apex HTTPS URLs and semantic-change notifications. Submission does not prove indexing. |
| Add payment/comparison guides | These intent groups already have pages. Improve existing targets before creating overlapping URLs. Raast acceptance, tax rates and bank-decline explanations require verification. |
| Add testimonials, founder details and 24-hour refunds | Publish only real identity, consented customer proof and owner-confirmed policies. Existing conditional refunds and replacement support remain authoritative. |
| Guaranteed citation uplift and traffic forecasts | The supplied percentages lack matching site/engine/locale evidence. Treat research as context; establish a baseline before setting numeric growth goals. |
| Add pricing.md and AI files | Crawlable `/pricing/`, `llms.txt` and `llms-full.txt` already exist. Avoid another manually maintained price copy. Google requires no special AI file or markup. [AI guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide). |
| Enable HTTP/3 and 0-RTT | The apex already advertises HTTP/3. No measured issue justifies a transport-setting change in this review. |

## Priorities for the next 30 days

1. Repair the verified www 522 response and validate redirects, paths and query strings using the owner guide.
2. Inspect the homepage, ChatGPT Plus, Canva Pro, CapCut Pro, design category and ChatGPT/Gemini comparison in Search Console. Record canonical, crawl and indexing evidence before requesting indexing.
3. Review those commercial offers with the owner for actual entitlements, account eligibility, renewal, availability and support. Update catalog facts while preserving slugs.
4. Improve `/blog/how-to-pay-for-chatgpt-plus-pakistan/` and `/blog/jazzcash-easypaisa-ai-tools-pakistan/` using verified payment information. Avoid unsupported bank/tax claims.
5. Improve the existing `/compare/chatgpt-vs-gemini/` with sourced differences and seller-plan limitations. Review overlap with the similarly named blog comparison before adding pages.
6. Export a 28-day Search Console baseline filtered to Pakistan; compare equal periods by query and landing page. Verify GA4 receipt of events and reconcile qualified inquiries with actual orders.

AI Tools Zone is an independent Pakistan-focused marketplace. Its useful search proposition is a readable catalog of seller-listed PKR offers, with explicit duration, access, limitations and WhatsApp confirmation. It is not an official reseller or a benchmark laboratory unless evidence establishes that separately.

## Architecture and intent ownership

Keep `/` for the business and overall discovery. `/products/` lists all offers; existing product URLs own brand + Pakistan + price + buy queries. `/categories/` groups ten actual catalog categories. `/use-cases/` contains four audience workflows. `/compare/` has ten selected comparisons. `/alternatives/` has two task-oriented shortlists. `/guides/` explains choosing a subscription and access types. `/pricing/` owns catalog-wide PKR and budget comparisons using section anchors instead of duplicate pages.

The current sitemap has 71 canonical URLs, including 20 product pages, 10 category pages, 10 comparisons, 10 blog articles, four use cases, two alternatives, three guides, their hubs, pricing and information pages. New pages require a distinct decision, supporting facts, original useful content and relevant internal links.

[SEO-KEYWORD-MAP.csv](SEO-KEYWORD-MAP.csv) records intent, competitor evidence, baseline coverage, destination, priority, content type, links, schema, direct-answer opportunity and entity context. Priority reflects purchase relevance, usefulness and maintainability, not invented search volume.

## Linking and entity model

Home links to all hubs, categories and product detail pages in initial HTML. Categories link to their products and selected workflows/comparisons. Products link back to their category and relevant editorial pages. Editorial tables link to products. Breadcrumbs connect every non-home canonical page with a useful parent. The 6 November local audit found a maximum link distance of three clicks.

One Organization ID and one WebSite ID identify AI Tools Zone consistently. WebPage nodes describe documents; Product/Offer nodes describe the seller offers; ItemList nodes describe collections, not fabricated ratings. BreadcrumbList mirrors visible navigation. Official vendor links identify product references without `sameAs` assertions about marketplace ownership. No invented social profiles, addresses, certifications or affiliation.

SoftwareApplication markup is deliberately omitted: the catalog mixes invitations, shared accounts, licenses, credits and non-software services, and lacks verified application-level operating-system/rating/entitlement data. Product + Offer is the more accurate description of these offers. FAQ answers are visible, accessible content; no FAQ rich-result promise or unsupported review schema is added. Rich-result eligibility and actual presentation must be checked separately.

## Direct answers and editorial rules

Product introductions state the tool, seller, PKR price, duration/allowance, access and confirmation requirement. Categories answer what work the tools address. Comparisons explain the decision before a generated price table. Questions receive short answers followed by supporting details and relevant sources.

Preserve original seller figures without treating them as independently verified vendor prices. Never infer that a lower price buys the same entitlement. Do not invent current model names, quotas, inventory, discount percentages or performance scores. General advice is framed as a selection method, not personal hands-on testing. Product references support vendor context, not authorization of the seller's offer.

For Pakistan intent, use PKR, actual ordering methods and the correct contact number. English content uses `en-PK`. No hreflang is emitted because there are no separately maintained translations. No city doorway pages or unsupported LocalBusiness address is added.

## Crawl policy and hosting

Googlebot and Bingbot inherit wildcard access. OAI-SearchBot, PerplexityBot and Claude-SearchBot are explicitly allowed for discovery. GPTBot remains disallowed. ClaudeBot is a training crawler; its pre-existing allowance is preserved separately. User-triggered retrieval has different behavior and is not guaranteed by robots alone. Verify crawler identities with provider guidance rather than a user-agent string.

Production packaging is an allowlist excluding source catalog, templates, scripts, private files and diagnostics. A public repository still exposes committed source. `_headers` is packaged for the Cloudflare Worker static-assets deployment; the apex currently returns its CSP and HSTS headers. GitHub Pages does not enforce this file. Hostname-level redirects require the appropriate edge configuration.

## Freshness and catalog maintenance

Edit `data/catalog.json`, preserving each `slug` even when a display name changes. Validate availability, entitlement, eligibility, duration, access, vendor link and support terms with the seller before accepting payment. Review active offers weekly and immediately on a supplier change; do not invent a verification timestamp when only the page layout changes.

Edit original guidance in `data/seo-content.json`; update it when vendor policies or buyer needs change. All price tables, structured offers and prepared messages derive from the catalog. There are no independently maintained price copies in the new editorial copy.

`data/page-state.json` persists a semantic content hash and lastmod. The fingerprint includes visible text, metadata, links and schema, while ignoring style/ordinary script bodies and asset cache tokens. Unchanged builds retain dates. Date-only freshness uses the Pakistan business calendar (UTC+05:00) consistently in local builds and UTC-hosted CI. Dates indicate a page-content change, not a price/stock verification. Never reset the state file just to make pages look fresh. Review deleted URLs before removing a page: GitHub Pages has no general per-path 301 configuration. Preserve useful URLs or configure a real host redirect before a migration.

## Measurement without invented results

Cloudflare Web Analytics records aggregate visits. The existing Google tag receives bounded events forwarded by `measurement.js` when available. Custom payloads omit query strings, order-message text, phone/customer details and search terms. Dashboard delivery and key-event configuration still need account verification; source code alone does not establish recorded counts. A WhatsApp click is not a completed sale.

Review GA4 automatic/enhanced measurement and privacy settings separately. Measure organic landing-page activity and lead intent; reconcile actual sales with order records.

| Source | Weekly measurement | Required manual setup |
|---|---|---|
| Google Search Console | Impressions, clicks, CTR, position, queries, landing pages, indexed/excluded pages, CWV reports | Verify DNS domain property, submit sitemap, inspect representative templates |
| Bing Webmaster Tools | Crawl/index status, query/page performance; AI Performance if exposed for the account | Verify/import property, submit sitemap, inspect URLs; do not claim unavailable reports exist |
| Installed analytics | Cloudflare visits/page views and the existing Google tag/event forwarding | Verify GA4 delivery, attribution and key-event configuration in the owner account |
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
