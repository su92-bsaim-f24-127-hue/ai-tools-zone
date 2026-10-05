# AI Tools Zone

Independent digital marketplace for AI tools and digital subscriptions in Pakistan. Twenty products, original brand icons, direct WhatsApp ordering, comparison, a tool finder and persistent light/dark themes.

## Run and build

Run `python -m http.server 8080 --bind 127.0.0.1` from this directory, then open http://127.0.0.1:8080/.

The deployed site is static. No runtime framework, API keys, payment SDK or build server is required. Use a local server to preview folder-based product URLs.

Run `python build_site.py` after changing the catalog, homepage template or editorial data, then `python audit_seo.py`. Run `python package_site.py` to refresh `ai-tools-zone.zip`. Run `python build_keyword_map.py` when updating search-intent coverage.

## Source files

- `data/catalog.json`: editable plan prices, descriptions, duration, access, delivery, replacement coverage and stable URL slugs. Preserve slugs when renaming products.
- `data/seo-content.json`: original category, workflow, comparison, alternatives and buying-guide content.
- `seo_pages.py`: renders editorial pages and shared catalog tables; records content-based sitemap freshness.
- `data/page-state.json`: persisted content fingerprints and lastmod dates. Do not reset this file for routine builds.
- `templates/home.html`: homepage layout and copy.
- `build_site.py`: builds the homepage, catalog.js, twenty product pages, information pages, editorial collections, sitemap, robots and manifest (53 canonical pages).
- `app.js`: search, filters, finder, quick views and comparison.
- `theme.js`: early theme selection, persistent preference and system-theme fallback.
- `scene.js`: CSS 3D logo motion, pause, pointer tilt and reduced-motion handling.
- `styles.css` and `enhancements.css`: layout, both themes and accessibility improvements.
- `assets/product-logo-sources.json`: icon provenance and source URLs.

The creator bundle is computed from the four catalog prices at build time. Generated HTML and catalog.js should not be edited directly; changes would be overwritten by the next build.

## Brand assets

The favicon emblem is extracted from the exact viewBox of the previously supplied favicon. Optimized WebP/PNG/ICO files preserve that artwork. The original oversized PNG/SVG files remain in the workspace but are not loaded by the site or included in the deployment ZIP.

The homepage hero uses a separately generated 3D-rendered crystal/metal interpretation of that emblem, with a transparent silhouette, gentle perspective motion and pointer tilt. The actual favicon and small identity marks remain unchanged. `output/imagegen/hero-logo-3d-prompt.md` records the built-in image-generation prompt and preserved source. Run `python scripts/prepare_hero_logo.py` to regenerate the 960 px and 480 px WebP delivery assets from that source, then rebuild the site. `python check_hero_logo.py` checks its responsive layouts, transparency and animation controls.

Product icons are hosted locally. Most are from vendors' own sites or documented asset hosts. Windows and NordVPN use Simple Icons v11's original vector glyphs with the published brand colours (CC0 distribution; trademarks remain with their owners). Veo is represented by its vendor Google DeepMind's official icon. Leonardo uses its official developer documentation icon. Product logo usage does not imply affiliation or endorsement.

## WhatsApp purchases

All Order on WhatsApp links open `https://wa.me/923430173923` with the selected plan details. Customers review and send their message. No message is sent automatically and no payment is collected by this website. The shopping bag and its checkout controls have been removed.

## Catalog accuracy

Listed prices and plan details originate from the user-supplied catalog, initially recorded on September 10, 2026. Vendor entitlements, unlimited allowances, licensing and plan availability have not been independently verified. Confirm these before accepting payment and keep the catalog current. No ratings, fabricated reviews, prior-price discounts or stock guarantees are included in the structured data.

## Verification

Run `python audit_seo.py` for dependency-free checks on all generated metadata, schema, prices, links, crawl depth, robots and sitemap entries. It also runs in GitHub Actions before deployment. `python test_seo_build.py` checks content freshness, build determinism and production package boundaries. `python audit_seo_browser.py` checks all pages in mobile/no-JS and desktop/JS contexts. `python audit_seo_live.py` checks the deployed sitemap, page responses and redirects; add `--external` to report outbound vendor URL accessibility.

With the local server running, use `python audit_site.py` for the full storefront audit and `python audit_accessibility.py` for axe-core checks across page templates, both themes and modal states. The latter expects the pinned axe-core 4.10.3 diagnostic file in `verification/axe.min.js`.

`check_theme.py` and `check_logo.py` provide focused checks. The old `test_site.py` and `review_site.py` commands now forward to the current audit, since bag-based tests no longer match the buying flow.

Tests use the installed Chrome and Playwright in `.test-deps`. Screenshots and machine-readable results are written to `verification/`. Test browser contexts are isolated. WhatsApp navigation is intercepted during automated testing.

## Publish to aitoolszone.tech

Push to `main` in `su92-bsaim-f24-127-hue/ai-tools-zone`. `.github/workflows/pages.yml` builds, runs the SEO audit, packages only production files and deploys to GitHub Pages. `CNAME` preserves `aitoolszone.tech`; `.nojekyll` preserves plain static publishing. The ZIP remains suitable for another static host if needed.

After deployment, run `python audit_seo_live.py`. Verify ownership in Google Search Console and Bing Webmaster Tools and submit `https://aitoolszone.tech/sitemap.xml`. Actual indexed pages, search performance and field Core Web Vitals need those external tools; local passing tests do not establish them.

GitHub Pages and the Python development server do not apply `_headers`. It is a portable Netlify/Cloudflare-style configuration example. Stronger custom response headers require a compatible host or proxy.

Canonical URLs point to the user-confirmed production domain. Indexing, rankings, rich results and AI citations are not guaranteed. Current documentation: `SEO-AUDIT.md`, `SEO-STRATEGY.md`, `SEO-COMPETITOR-GAPS.md`, `SEO-KEYWORD-MAP.csv`, and `SEO-IMPLEMENTATION.md`. `SEO-PLAN.md` and `AUDIT.md` are historical records.

## Privacy

Only the selected theme is stored by this version. Any old bag value is left untouched in browser storage but is no longer read. Search and comparison run locally. Google Fonts and Cloudflare Web Analytics are external runtime services. Privacy, ordering/warranty and contact information are available as crawlable pages.

`measurement.js` exposes optional document events named `aitz:measure`; it does not send analytics, use cookies or persist events. See `SEO-STRATEGY.md` before connecting any collection service. GPTBot training access is disallowed separately from OAI-SearchBot search access.

## Private visitor analytics

Cloudflare Web Analytics is installed by the shared HTML writer in `build_site.py`, including every generated page. The public beacon token identifies the collection site; it is not a credential for reading reports. The existing `measurement.js` custom events remain local and are not forwarded to Cloudflare.

To view counts, log into your own Cloudflare account, open **Web Analytics**, choose **aitoolszone.tech**, and select the date range. Keep account access limited to yourself; this website does not provide public reports, a shared dashboard link, or a client-side admin password. Dashboard membership cannot be verified from the public token.

Visits/page views are measured browser activity, not a verified count of distinct people. Ad blockers and disabled JavaScript can reduce collection; verification visits may appear. Historical visits before installation cannot be recovered. Data may take a few minutes to appear.

The privacy page describes the service. `_headers` allows its script/collection endpoint on compatible hosts; GitHub Pages does not apply that configuration file.

Setup reference: https://developers.cloudflare.com/web-analytics/get-started/

## October customer-discovery release

Read [SEO-GROWTH-RELEASE.md](SEO-GROWTH-RELEASE.md) for changes, evidence and remaining owner actions. `search.js` interprets bounded catalog queries; audience/duration filters are client-side. `data/seo-contract.json` protects the route count and stable product slugs. `audit_growth.py` checks order-message parity, entity IDs, placeholder navigation and common credential signatures. Signature scanning cannot prove that all private data has been detected; review the staged diff too.

Run `python audit_growth.py`, `python test_growth.py`, `python audit_growth_browser.py` (local server required), and `python scripts/build_seo_reports.py` for release validation and the per-page reports. `scripts/competitor_research.py` is a manual, robots-respecting research task, excluded from deployment. `scripts/indexnow.py` defaults to a dry run; the Pages workflow submits semantic URL changes only after successful deployment. The public proof key is not a secret.

[Search Console setup](SEARCH-CONSOLE-SETUP.md) ? [Bing and IndexNow](BING-WEBMASTER-SETUP.md) ? [Citation readiness](AI-CITATION-READINESS.md) ? [Customer and AI monitoring](AI-VISIBILITY-MONITORING.md). Cloudflare visit analytics is connected, but the optional conversion events are local hooks and have no configured collector.
