# AI Tools Zone

Independent digital marketplace for AI tools and digital subscriptions in Pakistan. Twenty products, original brand icons, direct WhatsApp ordering, comparison, a tool finder and persistent light/dark themes.

## Run and build

Run `python -m http.server 8080 --bind 127.0.0.1` from this directory, then open http://127.0.0.1:8080/.

The deployed site is static. No runtime framework, API keys, payment SDK or build server is required. Use a local server to preview folder-based product URLs.

Run `python build_site.py` after changing the catalog or homepage template. Then run `python package_site.py` to refresh `ai-tools-zone.zip`.

## Source files

- `data/catalog.json`: editable plan prices, descriptions, duration, access, delivery and replacement coverage.
- `templates/home.html`: homepage layout and copy.
- `build_site.py`: builds index.html, catalog.js, twenty product pages, information pages, sitemap, robots and manifest.
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

All Buy Now links open `https://wa.me/923430173923` with the selected plan details. Customers review and send their message. No message is sent automatically and no payment is collected by this website. The shopping bag and its checkout controls have been removed.

## Catalog accuracy

Listed prices and plan details originate from the user-supplied catalog, initially recorded on September 10, 2026. Vendor entitlements, unlimited allowances, licensing and plan availability have not been independently verified. Confirm these before accepting payment and keep the catalog current. No ratings, fabricated reviews, prior-price discounts or stock guarantees are included in the structured data.

## Verification

With the local server running, use `python audit_site.py` for the full storefront audit and `python audit_accessibility.py` for axe-core checks across page templates, both themes and modal states. The latter expects the pinned axe-core 4.10.3 diagnostic file in `verification/axe.min.js`.

`check_theme.py` and `check_logo.py` provide focused checks. The old `test_site.py` and `review_site.py` commands now forward to the current audit, since bag-based tests no longer match the buying flow.

Tests use the installed Chrome and Playwright in `.test-deps`. Screenshots and machine-readable results are written to `verification/`. Test browser contexts are isolated. WhatsApp navigation is intercepted during automated testing.

## Publish to aitoolszone.tech

1. Upload the contents of ai-tools-zone.zip to the static host's document root.
2. Connect aitoolszone.tech, enable HTTPS, and redirect any alternate www/http hostname to https://aitoolszone.tech.
3. Ensure clean folder URLs serve their index.html files and unknown URLs return a real HTTP 404 with 404.html.
4. If the host supports Netlify/Cloudflare Pages-style `_headers`, the supplied headers add security and cache settings. Otherwise configure equivalents in the host. Python's development server does not apply this file.
5. Verify the live canonical URLs, social card, robots.txt and sitemap.xml. Then verify domain ownership in Search Console and submit https://aitoolszone.tech/sitemap.xml.
6. Measure real production performance and inspect representative URLs after deployment.

Canonical URLs point to the user-confirmed production domain. A local build does not publish the website or guarantee search indexing, rich results or AI citations. SEO-PLAN.md documents the strategy; AUDIT.md records checks and deployment follow-ups.

## Privacy

Only the selected theme is stored by this version. Any old bag value is left untouched in browser storage but is no longer read. Search and comparison run locally. Google Fonts remains the only runtime asset dependency outside this website. Privacy, ordering/warranty and contact information are available as crawlable pages.
