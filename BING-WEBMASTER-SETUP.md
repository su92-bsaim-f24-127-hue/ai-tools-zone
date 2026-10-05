# Bing, IndexNow and AI visibility

Owner action: sign in to [Bing Webmaster Tools](https://www.bing.com/webmasters/), add `https://aitoolszone.tech/`, and verify via an offered ownership method or import a verified Search Console property. Submit `https://aitoolszone.tech/sitemap.xml`. No authenticated property or citation statistics were accessible during this implementation.

The repository now includes an intentionally public IndexNow host-proof key in `data/indexnow.json` and its matching root text file. `package_site.py` includes only that specific proof file. It is not an API password or access to analytics.

After a successful push deployment, `scripts/indexnow.py --submit --base-ref HEAD^` compares persisted semantic content hashes with the previous commit, notifies only changed/added/deleted canonical routes and checks the live proof first. Documentation-only changes produce no submission; manual workflow dispatch skips notification. Default invocation is dry-run. The notification step is nonblocking so an external API outage cannot unpublish a working site; inspect the step log for failures and retry the exact changed set only after fixing the cause.

The current catalog is small enough for one batch. Do not notify unchanged URLs repeatedly. A 200 means received and 202 means verification may still be pending; neither proves indexing, ranking or an AI citation. See the [IndexNow protocol](https://www.indexnow.org/documentation) and [official FAQ](https://www.indexnow.org/faq).

Review Bing Search Performance, URL Inspection, sitemap status and IndexNow diagnostics. Where available, review AI Performance's cited pages and grounding queries, and any account-visible preview metrics. These describe the covered experiences, not every AI assistant on the internet. [Bing's AI Performance help](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c) describes current report availability; actual metrics require your verified account.
