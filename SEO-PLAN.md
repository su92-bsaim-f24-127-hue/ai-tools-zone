# AI Tools Zone: implementation plan

Production origin: https://aitoolszone.tech

## 1. Brand and purchase journey
- Replace the hero rings and placeholder brand decorations with the existing AI Tools Zone favicon artwork; preserve depth, floating motion, pointer tilt, pause, and reduced-motion support.
- Use locally hosted original product logos in their original colours, with an asset source manifest.
- Replace the shopping bag with direct Buy Now links to +92 343 0173923. Include product, PKR price, duration, access and warranty in a message the customer reviews and sends.
- Retain filtering, comparison, tool finder and both colour themes.

## 2. SEO and crawlability
- Render the complete catalog in the initial HTML and link to twenty dedicated product pages.
- Give each page a unique title, description, canonical URL, one clear H1 and meaningful internal links.
- Use the supplied catalog as the price source. Do not invent ratings, reviews, stock status or official affiliations.
- Add Organization/WebSite data, Product/Offer data on individual product pages and BreadcrumbList data matching visible breadcrumbs.

## 3. GEO and AEO
- Provide concise, visible answers about purchase steps, access types, delivery estimates, coverage and payment methods.
- Make product price, duration and seller identity unambiguous in HTML; link relevant tools and official vendor websites for context.
- Describe this business as an independent Pakistan-focused digital marketplace. Product entitlements and availability must be confirmed by the seller.
- Use factual, readable content, not hidden keywords, fabricated reviews or unsupported promises of AI citations.

## 4. Technical SEO and performance
- Build sitemap.xml, robots.txt, social cards, icons and a useful 404 page for the confirmed production domain.
- Optimize existing brand images into appropriately sized WebP/PNG/ICO assets; host product logos locally and give images dimensions.
- Replace heavy WebGL rings with CSS 3D logo motion, paused outside the viewport and with reduced-motion support.
- Keep primary content and WhatsApp links usable without JavaScript. Improve mobile text, contrast, focus and tap targets.
- Add hosting header examples; only deploy-specific settings verified on the final host can be considered live.

## 5. Audit and completion
- Test all twenty product Buy Now links and their encoded messages without sending WhatsApp messages.
- Exercise search, filters, comparison, finder, theme persistence and animation controls.
- Check desktop and mobile screenshots in both themes, links, images, console errors, no-JS catalog, canonicals, metadata and JSON-LD.
- Rebuild the deployable ZIP and record results in AUDIT.md. Publishing, search-engine submission and field Core Web Vitals require a live deployment and are not claimed as complete locally.

## Sources guiding the plan
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/appearance/structured-data/product-snippet
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap

Google's guidance treats established SEO, accessible content and reliable information as the foundation for generative search. Structured data does not guarantee enhanced search results or AI citations. FAQ answers are useful visible content; no FAQ rich-result eligibility is assumed.
