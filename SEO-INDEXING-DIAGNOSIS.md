# Canonical and duplicate URL diagnosis

**Checked:** 29 October 2026 (Asia/Karachi)
**Site:** <https://aitoolszone.tech/>
**Method:** public HTTP requests with a desktop-browser user agent, DNS lookup, and a local comparison of generated indexable pages. These checks do not reveal Google's private index or its selected canonical decisions.

## Findings

| Severity | URL or scope | Observed result | Meaning and action |
|---|---|---|---|
| Medium | `https://aitoolszone.tech/sitemap.xml` | HTTP 200; 67 URLs, all unique. The URL set matches the local 67-route page state. | No duplicate sitemap entries were found. Keep submitting only these canonical HTTPS URLs. |
| Medium | All 67 sitemap URLs | Each returned HTTP 200; each tested page declared the matching HTTPS self-canonical. | No page-level canonical mismatch was reproduced. A declared canonical is a hint; only Search Console can show Google's selected canonical for a URL. |
| Medium | `https://aitoolszone.tech/robots.txt` | HTTP 200; public paths are allowed and the file names the HTTPS sitemap. | No search-crawler block was found in this file. `GPTBot` is separately disallowed by the site's stated training policy. |
| Medium | `http://aitoolszone.tech/` | HTTP 200, no `Location` redirect, and the response body is byte-identical to HTTPS (61,348 bytes; SHA-256 `200306a2cc4f56a5b8d9da624375123e9593ec3949496dd11e0794f4c811ab88`). The page's HTML canonical points to HTTPS. | This is the confirmed duplicate protocol variant. Configure an HTTP-to-HTTPS redirect at the serving edge or GitHub Pages settings, then retest. The static site generator cannot control that response. |
| Low | `https://aitoolszone.tech/index.html` and `/products/chatgpt-plus` | They return a 307 redirect to `/` and `/products/chatgpt-plus/`, respectively. | These variants already consolidate to the preferred trailing-slash URLs. Internal links and the sitemap use the preferred form. |
| Medium | `www.aitoolszone.tech` | DNS lookup returned `NXDOMAIN`; no HTTP response is available. | `www` is currently unavailable rather than a served duplicate. If you want it as an alias, configure its DNS record with the active DNS provider and let GitHub Pages redirect it to the apex domain. |
| Low | 67 local indexable pages | 67 unique titles, 67 unique visible main-content fingerprints, and no duplicate sitemap URLs. | No exact duplicate page was found. Repeated seller terms and safety disclosures on product pages are intentional and should remain visible; they do not create a duplicate URL by themselves. |

The live audit checked 73 requests: 67 sitemap pages plus six URL controls. All 67 sitemap pages returned 200 and the one deliberately unknown route returned the expected 404. The HTTP homepage control failed the expected redirect check. The two `www` controls were unverified because DNS does not resolve. This is not evidence that Googlebot is blocked.

## Recommended owner actions

1. In the Cloudflare zone, enable **Always Use HTTPS** (or confirm GitHub Pages **Enforce HTTPS** is correctly enabled). Use one effective redirect path and retest that `http://aitoolszone.tech/` returns a permanent redirect to `https://aitoolszone.tech/` with the path and query preserved. Cloudflare warns to check existing redirects to avoid loops. Do not change nameservers for this.
2. If you want `www.aitoolszone.tech` to work, add a `www` CNAME in the active Cloudflare DNS zone pointing to `su92-bsaim-f24-127-hue.github.io` and confirm the GitHub Pages custom-domain configuration. GitHub Pages documents automatic apex/`www` redirection when both hostnames have correct DNS records. Do not replace existing records.
3. In Search Console, inspect the exact URLs reported under **Page indexing**. “Alternate page with proper canonical tag” can be an expected duplicate consolidation; for “Duplicate, Google chose different canonical,” compare Google's selected canonical with the URL Inspection live test before changing a page.
4. After any host change, re-run `python audit_seo_live.py`. It now uses a browser-like user agent because the public edge returned 403 to the default Python client. That request does not impersonate or verify Googlebot.

Google recommends consistent canonical signals and generally prefers HTTPS. The project already publishes self-canonicals and an HTTPS-only sitemap; the remaining confirmed protocol duplication is a host configuration issue, not a missing canonical tag. See [Google's canonicalization guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [GitHub Pages HTTPS guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https), and [GitHub Pages custom-domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

## Validation status

- Local build: 67 canonical routes.
- Local SEO audit: 6,118 checks, zero errors or warnings; 67 unique main-content fingerprints.
- Local growth audit: 2,836 checks, zero errors; 67 indexable routes.
- Freshness, deterministic-build and package regression: passed.
- Growth regression: 7 assertions passed.
- Live sitemap pages: 67/67 HTTP 200 and self-canonical.
- Live canonical-host issue: HTTP homepage still returns 200 without redirect; `www` remains DNS NXDOMAIN. These require owner-controlled hosting/DNS settings.

Search Console URL Inspection, current indexed-page totals, and Google's selected canonicals were not inspected in this review.
