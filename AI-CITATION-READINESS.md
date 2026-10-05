# Citation readiness, not citation prediction

The generated [per-page checklist](reports/citation-readiness.csv) covers every canonical page across 13 requested dimensions. `1` means an observable prerequisite exists, `0` means not observed, and `U` means human/source review is necessary. These are checklist scores, not an aggregate SEO score or probability of citation. Rebuild with `python scripts/build_seo_reports.py` after the audits pass.

| Dimension | Required evidence before considering it complete |
|---|---|
| Crawlability | robots allows public search pages; initial links and deployed HTTP checks pass |
| Indexability | self canonical, index directive, sitemap inclusion; actual indexing is separately verified in webmaster tools |
| Factual clarity | exact offer price, currency, duration/access and limitations visible; vendor entitlement needs owner verification |
| Entity clarity | consistent seller/product names and stable linked IDs |
| Direct answers | human reads the opening answer against the page's actual buying question |
| Evidence | factual feature claims checked with vendor/offer documentation, not just a link present |
| Source attribution | appropriate official references; marketplace terms clearly separated |
| Originality | independent useful explanation; no copied descriptions or fabricated testing |
| Internal links | reachable page and contextual next decisions |
| Structured data | valid graph, visible facts agree; no fake reviews/stock |
| Freshness | semantic content date exists; no invented last-verified claim |
| Trust | seller identity/contact/policies accurate; no implied affiliation |
| Conversion clarity | clear WhatsApp next step and review-before-send behavior |

Unknown dimensions stay unknown until reviewed. Pages without vendor links may be appropriate seller policy pages; zero attribution is not automatically a defect. The detailed [page inventory](reports/seo-page-inventory.csv) records titles, descriptions, headings, canonicals, robots, links/incoming links, schema, social tags, images, breadcrumbs and intended buyer questions, including the excluded 404.

Search accessibility helps retrieval; it does not guarantee inclusion or citation. [Google's AI search guidance](https://developers.google.com/search/docs/appearance/ai-features) supports the same fundamentals as regular search. No `llms.txt`, invisible bot instructions or new unsupported schema was added.
