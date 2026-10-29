# SEO, website and conversion test results

**Run:** 29 October 2026 (Asia/Karachi)<br>
**Target:** local rebuilt static site in the existing repository.<br>
**Live comparison:** GitHub Pages deployment succeeded; the custom domain was still returning a Cloudflare-cached previous response at the time of verification.

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
| GitHub Pages deployment | PASS | Workflow [40870834971](https://github.com/su92-bsaim-f24-127-hue/ai-tools-zone/actions/runs/40870834971) succeeded for commit `fa9319f`; direct `github.io` product/article pages contain the new text. |
| Changed pages on `https://aitoolszone.tech/` | STALE EDGE CACHE | Requests returned HTTP 200 with Cloudflare `CF-Cache-Status: HIT`, but still served the old ChatGPT article title and Veo “Unlimited generations” copy after deployment. Purge the affected URLs in Cloudflare or wait for the configured edge TTL, then recheck. |
| `www.aitoolszone.tech` | UNVERIFIED | DNS `NXDOMAIN`, so no HTTP response or redirect can be tested. |

The live crawl is a public web request and does not verify how Google's own crawler or index sees a URL. Current Search Console URL Inspection, field Core Web Vitals and PageSpeed Insights results were not available. Search Console owner steps are in [SEARCH-CONSOLE-SETUP.md](SEARCH-CONSOLE-SETUP.md).

## Reproducibility

From the repository root, run the commands in the tables above. `audit_seo_live.py` and `audit_seo_browser.py` require network/browser support. The static build does not change Cloudflare settings. After the owner enables an HTTP-to-HTTPS redirect and clears/waits out the stale edge cache, rerun the live audit and inspect representative changed URLs.

## Re-validation after last-checked-date enhancement (29 October 2026)

A visible, machine-readable last-checked date was added to the **20 product pages only** (single owner-curated constant `LAST_VERIFIED='2026-10-29'`; homepage, blog and information pages are unchanged). The site was rebuilt and the full local suite re-run:

| Command | Result | Evidence |
|---|---|---|
| `python build_site.py` | PASS | 67 canonical pages; freshness note renders only on product pages. |
| `python audit_seo.py` | PASS | 6,118 checks; 0 errors; 67 unique main-content pages. |
| `python audit_growth.py` | PASS | 0 errors; 67 indexable pages; 1,752 incoming internal links (parity with baseline). |
| `python test_seo_build.py` | PASS | Deterministic build, unchanged-date preservation, GSC/Bing verification tags survive rebuild. |
| `python test_growth.py` | PASS | 7 growth regression assertions. |

Live state is unchanged by this local edit: the host HTTP→HTTPS redirect and the stale Cloudflare edge cache (still serving the old Veo "Unlimited generations" copy) remain owner-controlled actions. The enhancement is local-only and was **not deployed or pushed**; it is staged in the working tree for the owner to review and commit.

**Diff footprint:** `build_site.py` (+`LAST_VERIFIED`/`LAST_VERIFIED_LABEL` constants; one `<p class="verified-date">…<time>…</time>` in the product body) plus the 20 `products/*/index.html`, and the resulting `sitemap.xml` + `data/page-state.json` lastmod bumps for those 20 routes. Scope check: `verified-date` count = 0 on `index.html`, `about/index.html`, `pricing/index.html`, and the payment guide — confirming the change is product-page-scoped.

## Re-validation after structured-data + description tightening (29 October 2026)

Two more verified, committed-source gaps surfaced by the SEOmator report (94/100) were addressed and re-validated:

| Change | Location | Verified |
|---|---|---|
| Availability omitted from Offer schema (audit-enforced) | `build_site.py:121` Offer dict; `audit_seo.py:130` | Removed orphaned `InStock` (not emitted by source); Offer keeps price/currency/seller -> audit-clean |
| Shortened over-length meta descriptions (SERP truncation) | `build_site.py` homepage, `seo_pages.py` compare + pricing, `templates/home.html` | `/` / `/compare/` / `/pricing/` descriptions now ≤130 chars; meta + OG + schema identical |

Rebuild + full local suite: `audit_seo.py` 6,254 checks / 0 errors / 0 warnings; `audit_growth.py` 0 errors / 1,752 internal links (parity with baseline); `test_seo_build.py` PASS (determinism + freshness + GSC/Bing verification tags); `test_growth.py` PASS (7 regression assertions). Local-only; not deployed.

Note: several SEOmator failures were confirmed as artifacts of crawling non-canonical root URLs (e.g. `/gemini-pro` instead of `/products/gemini-pro/`), which correctly 404 to the shared handler and therefore render identical content (same hash → "duplicate"; same 23-word body → "thin"). The real `/products/<slug>/` pages are rich (797 words, self-canonical, structured data). Remaining SEOmator failures are owner/host-controlled: HTTP→HTTPS redirect, HSTS, `307`→`301` redirects, soft-404 on `/404.html`, CSP nonce for the Cloudflare beacon; see OWNER-ACTIONS checklist.
