# Measure discovery through to customers

Start with evidence, not forecasts. Current traffic, ranking, citations, WhatsApp inquiries and completed orders are unknown to this agent. Cloudflare's public beacon ID does not grant access to the private dashboard.

## Weekly owner record

Keep a private spreadsheet with week, visits, page views, top landing pages, referrers, Search Console impressions/clicks/CTR, Bing clicks/citations where available, WhatsApp inquiries, qualified inquiries, completed orders and cancellations. Do not commit names, phone numbers, transcripts, payments or this private sheet to GitHub. Ask a customer how they found the store only where useful; do not infer an order from a click.

Funnel: search impression → landing page → relevant plan/comparison → WhatsApp click → conversation → confirmed order. A click is only an intent signal; conversation and purchase happen off-site and need seller records. No custom click collector is currently configured. Therefore a website click-to-order conversion rate is not yet measurable end to end.

Cloudflare Web Analytics already records visits/page views privately to the owner's account. The screenshot supplied on 6 October showed **Last 24 hours** (not 7 days), 9 visits and 9 page views. Its listed `/admin` and `/admin/` URLs return 404, so they are requests for missing pages rather than real storefront sections. The generated 404 previously loaded the beacon; this release removes analytics from 404 responses to keep missing-route probes out of storefront visit totals. Recheck the same date window after deployment; the reported count may fall even though qualified visits are unchanged. Its [FAQ](https://developers.cloudflare.com/web-analytics/faq/) says custom events and UTM reporting are not supported; ad blockers and delivery failures also affect measurement. The `aitz:measure` events are tested local integration hooks only. They are not saved, exported, shown publicly or sent to Cloudflare. To measure clicks centrally, supply a supported analytics property/collector and implement its consent/privacy requirements. Never expose a private dashboard credential in client code.

Available bounded hooks: product_view, category_view, comparison_view, alternative_view, guide_view, pricing_view, tool_search, filter_use, compare_add, tool_finder_start, tool_finder_complete, whatsapp_click, product_whatsapp_click and outbound_vendor_click. Payloads contain only an allowlisted event name, canonical page path, section and optional allowlisted catalog product ID. Search text, query parameters, message bodies, phone numbers and purchase details are excluded.

## AI answer checks

Monthly, use a fixed small set of questions about Pakistan offers, access and comparisons. Record date, engine/interface, locale, exact question, whether a citation actually appeared and its destination. Compare the same questions; a single personalized response is not a rank or market share. Do not automate prompts to manipulate engines or claim an answer was cited without saving evidence privately. GSC does not provide a clean separate AI conversion funnel; Bing reporting covers its stated experiences only.

## Customer acquisition priorities

First week: verify search properties, check actual offer eligibility and availability, reply consistently to inbound inquiries, and record objections. Weeks 2–3: prioritize the three landing pages with real impressions or buyer questions; improve the answer/offer clarity using those observations. Week 4: compare equal windows and investigate drop-offs. If relevant visits occur without conversations, review price/access uncertainty and support response; if conversations occur without orders, investigate offer fit, entitlement and payment confidence. No artificial testimonials, fabricated urgency, bought backlinks or automatic unsolicited outreach.
