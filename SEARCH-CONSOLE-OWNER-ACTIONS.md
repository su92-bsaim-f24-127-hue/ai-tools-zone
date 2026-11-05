# Search Console and hostname owner actions

**Updated:** 6 November 2026, Asia/Karachi. The custom domain uses the Cloudflare Worker `ai-tools-zone` with static assets; GitHub Pages deploys separately. No DNS/account settings changed in this review.

## 1. Resolve the confirmed www failure

Public checks returned HTTP 522 for the www homepage. The canonical host is `aitoolszone.tech`.

1. In the Cloudflare account managing this domain, inspect the existing www DNS record, proxy state, Worker domains/routes and redirect rules. Record their current values before editing.
2. Configure a **Single Redirect** for the exact hostname:
   - Match: `(http.host eq "www.aitoolszone.tech")`.
   - Dynamic target: `concat("https://aitoolszone.tech", http.request.uri.path)`.
   - Status: **301**. Enable **Preserve query string**.
3. The redirect needs proxied DNS for www and an active edge certificate. If either is missing, correct that specific configuration using Cloudflare's domain-redirect guidance. Preserve unrelated DNS, TXT verification records, email records and nameservers. Do not point this Worker at an assumed Pages hostname.
4. Check HTTPS and HTTP www for `/`, `/robots.txt`, and `/products/chatgpt-plus/?source=check`. Expect an apex redirect preserving path/query, then the appropriate response. Rerun `python audit_seo_live.py`.

Worker `_redirects` supports path rules and cannot repair requests that fail before reaching the assets. References: [Cloudflare custom domains and www redirects](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/#redirect-between-www-and-root-domain), [Worker redirects](https://developers.cloudflare.com/workers/static-assets/redirects/).

If a crawler is challenged, find its request in Security Events and record timestamp, hostname, action and service. Verify the bot before creating a narrow exception. A user-agent substring is insufficient. WAF skip rules cannot bypass Bot Fight Mode; scoped Super Bot Fight Mode exceptions are different. [Cloudflare guidance](https://developers.cloudflare.com/bots/troubleshooting/false-positives/).

## 2. Check the right Search Console property

1. Open [Search Console](https://search.google.com/search-console/). Use the existing verified property when available.
2. If verification is needed, add a **Domain** property for `aitoolszone.tech` and copy Google's exact unique DNS TXT value.
3. Add it at the actual authoritative DNS provider. Confirm the provider/nameservers before editing; preserve existing records.
4. Return and click Verify. Domain verification uses DNS. HTML tags/files are a separate URL-prefix method; existing site verification tokens remain intact.
5. Submit `https://aitoolszone.tech/sitemap.xml` under Sitemaps. It is a URL-set sitemap with 71 entries, not a sitemap index. Record status and last-read date.

## 3. Inspect important URLs

Start with the homepage, `/products/chatgpt-plus/`, `/products/canva-pro-edu/`, `/products/capcut-pro/`, `/categories/design/` and `/compare/chatgpt-vs-gemini/` on the HTTPS apex hostname.

For each, record indexed status, exclusion reason, crawling/indexing permission, last crawl, user canonical and Google-selected canonical. Use Test Live URL to investigate current fetch/render problems. Fix genuine errors before requesting indexing for eligible important pages. Requests have quotas; no fixed daily allowance or indexing deadline is promised. [Google recrawl guide](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).

A successful live test does not prove inclusion in the index. Normal product/blog pages are not eligible for the Google Indexing API.

## 4. Measure outcomes

- Check Page Indexing, Crawl Stats, Sitemaps, Manual Actions and Security Issues separately. Coverage exports alone cannot prove no manual action exists.
- Export a 28-day Performance baseline filtered to Pakistan: query, page, clicks, impressions, CTR and average position. Compare equal windows; average position is not a fixed live SERP rank.
- Use Core Web Vitals for field data; keep Lighthouse lab results separate.
- Verify the existing GA4 tag receives `page_view`, `product_view` and `product_whatsapp_click`; configure meaningful key events. Reconcile actual orders separately.
- Retain dated exports. Set traffic/customer targets only after a measured baseline is available.
