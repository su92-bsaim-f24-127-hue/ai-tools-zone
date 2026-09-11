# AI Tools Zone

A complete responsive storefront with original WebGL 3D artwork, 20 products, search, ten categories, price/access filters, comparison, a guided finder, persistent shopping bag and WhatsApp ordering.

## Open the website

Open `index.html` directly in Chrome or Edge. No build process is needed.

For a local server, run `python -m http.server 8080 --bind 127.0.0.1` in this folder, then visit `http://localhost:8080`.

## Edit products and prices

Edit `catalog.js`. Prices, durations, access types, delivery estimates, features and replacement warranties were copied from the supplied demo at https://aitoolgems.tech/ on September 10, 2026. These are the demo's listed offers, not independently verified vendor entitlements. Confirm current availability and limits before accepting payment.

The original creator bundle is ChatGPT Plus, Canva Pro Edu, CapCut Pro and ElevenLabs, totaling PKR 7,400. If these prices change, update the static bundle display in `index.html`; the cart always calculates from the catalog.

## WhatsApp

All contact and order links use `923136726285` (+92 313 6726285). Product and shopping-bag orders generate detailed messages. Customers review and send the message in WhatsApp. No message is automatically sent and no online payment is collected.

## Publish

Upload `index.html`, `styles.css`, `catalog.js`, `app.js`, `scene.js` and the `assets` folder to any static web host. The included `ai-tools-zone.zip` contains only production files. The website has not replaced the existing demo or been connected to a public domain.

## Design and research

- Demo catalog and original functionality: https://aitoolgems.tech/
- Search, compare and WhatsApp purchase patterns: https://aitoolspak.tech/
- Subscription store browsing: https://www.bunnytools.store/
- Catalog organization: https://www.sundayproduct.com/products
- 3D interaction reference collection: https://www.awwwards.com/websites/3d/

The visual design and implementation are original. No competitor reviews, customer counts, or unverified affiliation claims are used. There are no paid runtime dependencies. Google Fonts is optional and falls back to local system fonts; all 3D visuals and brand monogram tiles work without external images.

## Verification

`test_site.py` uses Playwright with installed Chrome to verify ordering, filtering, comparison, finder, persistence and responsive widths. Test artifacts are in `verification/`. Run with `python test_site.py` after installing Playwright into `.test-deps`.

`review_site.py` additionally exercises all 20 product orders, every category/access/sort choice, all finder workflows, comparison selection, nested-dialog back navigation, mobile controls, privacy clearing and keyboard focus. Run with `python review_site.py`.

The September 11 review repaired dialog feedback, direct bag access, quantity-control focus, comparison selection, stale filters on All tools navigation, repeated policy links, modal back navigation and mobile menu state. Finder choices now survive retries, video creation excludes streaming subscriptions, and Continue exploring takes shoppers back to the catalog.

## Privacy and accessibility

Only the bag and the visitor's selected color theme are saved locally in the browser. There is no analytics integration or backend. Native modal dialogs provide keyboard focus containment and Escape dismissal. The layout includes keyboard focus indicators, labeled controls, reduced-motion handling and a 3D fallback for browsers without WebGL.
