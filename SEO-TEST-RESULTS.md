# SEO, website and conversion test results

**Run:** 29 October 2026 (Asia/Karachi)<br>
**Target:** local rebuilt static site in the existing repository.<br>
**Live comparison:** public production site before the pending source edits are deployed.

## Local build and code checks

| Command | Result | Evidence |
|---|---|---|
| `python build_site.py` | PASS | Built 20 product pages, 3 information pages, 404, sitemap and manifest; 67 canonical pages. |
| `python build_keyword_map.py` | PASS | Wrote 270 unique intent mappings; search demand, competition and Google indexing remain unverified. |
| `python test_seo_build.py` | PASS | Freshness, unchanged-date preservation, deterministic build and safe production-package checks passed. |
| `python audit_seo.py` | PASS | 6,118 checks; 67 unique main-content pages; zero errors/warnings; max crawl depth 2; 105 local resources checked. |
| `python audit_growth.py` | PASS | 2,841 checks; zero errors; 67 indexable pages; 68 pages inventoried including the 404; 20 product offers; 1,752 incoming internal links. |
| `python test_growth.py` | PASS | Seven regression assertions passed. |

## Browser, ordering and accessibility checks

| Command | Result | Evidence |
|---|---|---|
| `python audit_seo_browser.py` | PASS | 151 checks; no failures or console errors. Local desktop lab readings: LCP 816 ms, CLS 0.00252, 721 DOM nodes, 25 resources. These are lab results from the local build, not field Core Web Vitals. |
| `python audit_growth_browser.py` | PASS | 36 checks; zero failures across search, filters, finder, mobile widths and measurement hooks. |
| `python audit_whatsapp.py` | PASS | 30 checks; all 20 product WhatsApp Web message parity/destination, copy fallback and 320–1440px layout checks passed. |
| `python audit_accessibility.py` | PASS | Zero axe violations across the tested light/dark, desktop/mobile, product, dialog, finder and comparison states. |
| `python audit_site.py` | PASS | 149 checks; zero failures or JavaScript errors; zero accessibility violations. Verified 20 order controls, filters, comparison/finder/theme, sitemap/robots, 92 local links/resources and no-JavaScript ordering. |

## Live production checks

| Command/scope | Result | Evidence |
|---|---|---|
| `python audit_seo_live.py` | FAIL — owner-controlled redirect | 73 requests: 70 HTTP 200, two unresolved DNS/HTTP results for `www`, and one deliberate missing-route 404. The only failure was `http://aitoolszone.tech/` returning 200 instead of redirecting to HTTPS. The 67 sitemap URLs each passed 200/self-canonical checks. |
| `https://aitoolszone.tech/robots.txt` | PASS | HTTP 200; intended public paths allowed; HTTPS sitemap referenced; Googlebot not blocked. |
| `https://aitoolszone.tech/sitemap.xml` | PASS | HTTP 200; 67 unique canonical HTTPS routes. |
| `www.aitoolszone.tech` | UNVERIFIED | DNS `NXDOMAIN`, so no HTTP response or redirect can be tested. |

The live crawl is a public web request and does not verify how Google's own crawler or index sees a URL. Current Search Console URL Inspection, field Core Web Vitals and PageSpeed Insights results were not available. Search Console owner steps are in [SEARCH-CONSOLE-SETUP.md](SEARCH-CONSOLE-SETUP.md).

## Reproducibility

From the repository root, run the commands in the tables above. `audit_seo_live.py` and `audit_seo_browser.py` require network/browser support. The static build does not change Cloudflare or GitHub Pages settings. After the owner enables an HTTP-to-HTTPS redirect and after deployment, rerun the live audit and inspect representative changed URLs.
