# Bounded competitor research

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
