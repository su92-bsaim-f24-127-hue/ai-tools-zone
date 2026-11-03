# Google Search Console actions

**Prepared:** 3 November 2026 (Asia/Karachi)
**Access status:** No authenticated Search Console session was available for this audit. Current ownership, indexing reports, selected canonicals, and query metrics are unverified.

## 1. Confirm ownership without replacing existing proof

1. Open [Google Search Console](https://search.google.com/search-console/) using the Google account that owns the site.
2. Check whether the **Domain** property `aitoolszone.tech` and/or the **URL-prefix** property `https://aitoolszone.tech/` appears in the property selector.
3. The repository contains existing Google HTML verification files and the homepage verification tag. Keep those files/tags in the build; do not replace them.
4. A Domain property requires the exact DNS TXT token shown by Google's current wizard. A URL-prefix property can use its matching HTML-tag or HTML-file method. If verification fails, compare the token/file name with the live property wizard; never guess a token or remove other DNS records.
5. Confirm the current verification method reports **Verified** in Search Console. A public tag/file response does not prove account-level acceptance.

## 2. Submit and reconcile the sitemap

Submit `https://aitoolszone.tech/sitemap.xml` under **Indexing → Sitemaps** for the verified property. Record the submission status, last read, discovered URLs, and any exact errors.

As of this audit, the local generated sitemap contains 71 canonical routes while production serves 70. The local-only article `/blog/chatgpt-plus-vs-gemini-pro-pakistan/` currently returns 404. After its normal deployment, confirm that the live sitemap is updated and resubmit/recheck it. Do not request indexing for the 404 production URL before deployment.

## 3. Inspect representative URLs

Use URL Inspection for these routes after confirming the correct property:

- `https://aitoolszone.tech/`
- `https://aitoolszone.tech/products/chatgpt-plus/`
- `https://aitoolszone.tech/products/gemini-pro/`
- `https://aitoolszone.tech/products/canva-pro-edu/`
- `https://aitoolszone.tech/categories/ai-assistants/`
- `https://aitoolszone.tech/categories/design/`
- `https://aitoolszone.tech/guides/choose-ai-subscription/`
- `https://aitoolszone.tech/guides/private-vs-shared-access/`
- `https://aitoolszone.tech/blog/chatgpt-plus-vs-gemini-pro-pakistan/` (after deployment)

For each, record: URL on Google, last crawl, crawl allowed, indexing allowed, user-declared canonical, Google-selected canonical, and the exact exclusion reason if any. A successful HTTP response or sitemap inclusion is not evidence that Google indexed the page. Request indexing only after the deployed page is correct; Google does not guarantee inclusion.

## 4. Review account reports

Check these reports and save the date/property used so later reviews can compare like periods:

- **Page indexing:** indexed and excluded URLs, grouped by Google's exact reason.
- **Manual actions** and **Security issues:** current property status.
- **Performance → Search results:** clicks, impressions, CTR, average position, query/page/country/device.
- **Core Web Vitals:** field LCP, INP and CLS by device, if data is available.
- **Links:** referring domains and pages; review topical relevance and actual source-page context.
- **Sitemaps:** last read and discovered counts.

If a report has no data, record “not available” rather than zero. Do not infer a penalty, deindexing, or ranking cause from the local audit or from one manual search.

## 5. Host and structured-data follow-up

- The apex HTTP URL currently redirects permanently to HTTPS. The `www` HTTPS host returns HTTP 522; if `www` should be supported, have the DNS/origin owner repair it and then verify that both HTTP and HTTPS `www` requests resolve to the apex HTTPS URL.
- Once representative pages are deployed, test a product/Offer, a blog article, and breadcrumbs with [Google's Rich Results Test](https://search.google.com/test/rich-results). Review warnings against visible content and Google's supported features; valid JSON-LD syntax alone does not guarantee a rich result.

Do not share Google passwords, recovery codes, verification tokens, or DNS credentials in this repository or chat.
