# Bounded competitor research

## Public-search matrix update: 14 October 2026

The spreadsheet-compatible [competitor matrix](SEO-COMPETITOR-MATRIX.csv) records 15 competitor samples plus an AI Tools Zone self-benchmark, including structure, content, search-sample visibility, public mention/backlink limits and user-experience observations. It opens in Excel and other spreadsheet apps. Queries covered global AI directories and Pakistan subscription sellers. Search-result observations describe the public search tool's sample only; they are not Google rankings, traffic estimates or proof of indexing. The exact-domain search for `aitoolszone.tech` returned no result in that limited sample, while direct Google Search access returned a restriction page rather than ordinary results. Neither observation establishes that Google has or has not indexed the site.

Backlink notes are deliberately conservative: no backlink index was available. A third-party mention is not a verified link, endorsement, editorially earned link or measure of authority. Competitor prices, inventory, ratings, counts, seller status and service claims were not copied or independently verified. For the latest site-by-site evidence, sample status and opportunities, use the CSV; the machine-readable page sample remains [2026-10-14.json](data/competitor-intelligence/2026-10-14.json).

## Fresh sample: 14 October 2026 (Pakistan time)

Evidence: [machine-readable 12-page sample](data/competitor-intelligence/2026-10-14.json). Eight public pages were sampled; four were skipped (TAAFT and Toolify returned 403, FutureTools redirected with 308, and Pak Tools Store returned 421). The collector checked robots rules, did not follow those redirects or bypass challenges, and sampled no more than one page per host. Global tool directories are discovery competitors; local sellers and marketplaces are the closer commercial comparison set. This is page-level research, not a rank, traffic, conversion, customer-review or whole-site study.

| Public sample | Observable page signal | Practical gap to address | Evidence limit |
|---|---|---|---|
| [AI Tools Pak](https://aitoolspak.tech/ai-subscription-price-index-pakistan/) | A dedicated Pakistan PKR index page describes its own offer count and update date | Keep a dated, reproducible, item-level PKR/access snapshot with visible methodology | Counts, freshness and ?verified? status are the publisher?s claims; not independently audited here |
| [SubBazaar](https://subbazaar.pk/?category=ai-tools) | AI category shows visible products and pricing/terms | Make duration, access, renewal and seller confirmation easy to compare | Page copy and inventory can change; seller claims not independently tested |
| [JKDigital guide](https://www.jkdigital.pk/blog/best-ai-tools-provider-in-pakistan-lowest-prices-2026) | Local buying criteria framed around price, breadth and support | Answer buyer questions with explicit facts and limits on each offer | Provider article is promotional; its claims are self-reported |
| [AI Tool Gems](https://aitoolgems.tech/) | Local PKR offers and WhatsApp-oriented purchase journey | State seller identity, exact product/term and what a buyer must confirm | Public page snapshot only; no independent fulfillment test |
| [PrimePass](https://primepass.app/) | Subscription bundle model and bundle-focused navigation | Explain when an individual offer versus bundle fits the use case | Reviews/user counts and service claims are publisher-provided, not verified |
| [Toolmandi](https://toolmandi.store/about) | Pakistan-focused marketplace positioning and category navigation | Keep local relevance tied to current catalog facts, not broad unsupported superiority | About page is not independent evidence of service performance |
| [Futurepedia](https://www.futurepedia.io/ai-tools/productivity), [TopAI.tools](https://topai.tools/) | Global task/category discovery structures | Bridge genuine tasks to offers available in this seller's catalog | Global directory samples are not local subscription sellers |

No prices, copy, ratings or reviews from competitors were imported. The implementation recommendation is differentiation through dated owner-checked terms, useful buyer explanations and clear independent-seller disclosure. No claim about search position or competitor performance follows from this sample.


Research run: 6 October 2026, Pakistan time (5 October UTC). Evidence: `data/competitor-intelligence/2026-10-05.json`. This is a sample, not a ranking/traffic dataset or endorsement of any seller.

Run `python scripts/competitor_research.py` manually. It requests robots.txt first, obeys the research user agent's allow/disallow rules and crawl delay, and samples at most one configured public page per host. Missing robots, errors, redirects, access challenges and long delays cause a skip. It never follows login links or challenges, never collects customer profiles, and stores at most 24 words of title/heading snippets per domain plus schema types and navigation prefixes. It is separate from both the build and production package. Repeated runs should be deliberate research sessions, not frequent polling.

Five samples succeeded: TAAFT, Futurepedia, Toolify, TopAI and AI Tools Pak. FutureTools returned a redirect, AIxploria had a DNS failure, and Bunny Tools' robots request returned 404. These three were investigated but not re-fetched through an alternate access path. Their previous September observations remain dated historical evidence, not a fresh audit.

| Sample | Observable strength / captured intent | Limitation or unanswered need | Original response in this release |
|---|---|---|---|
| [TAAFT](https://theresanaiforthat.com/) | Search-led broad tool discovery | Sample does not establish Pakistan seller-plan terms or PKR buying support; schema/navigation parser found no usable signal, not proof of absence | Interpret buyer task queries over our own actual offers |
| [Futurepedia](https://www.futurepedia.io/ai-tools/productivity) | Productivity taxonomy, editorial-guideline and tutorial routes; Organization/BreadcrumbList schema | Vendor discovery alone does not resolve our specific access, duration or final seller price | Accessible plan tables and transparent catalog methodology |
| [Toolify](https://www.toolify.ai/) | Category, model, news and discovery taxonomies | Broad lists do not establish comparable offer durations or eligibility in Pakistan | Bounded catalog filters; compare allowance with total price |
| [TopAI](https://topai.tools/) | Use cases, playbooks, guides and AI-assisted discovery routes | No claim that its recommendations answer this store's current offer conditions | Natural-language intent mapping plus visible use-case guides |
| [AI Tools Pak](https://aitoolspak.tech/) | Local buying intent, PKR titles and rich offer/entity markup | Schema presence does not verify stock, entitlements, affiliations or customer satisfaction | Short order path with exact offer URL; clear independent-seller terms and no unsupported schema claims |

“Limitation” here means an unanswered need in this small sample, not a claim that a competitor is globally worse. Competitor claims, counts, discounts and features were not imported into our catalog. Automated metadata cannot assess full content quality or AI citations. No paid placements, backlinks or outreach were purchased or sent.

Next research should be driven by actual Search Console queries and support questions. Inspect a relevant public page only when permitted, record source/date and original observations, then write independent useful content with vendor attribution. Do not expand pages merely to match competitors' volume.
