# Google Search Console setup

This is an owner-run checklist. Search Console ownership, indexing status, impressions, clicks and rankings have not been verified from this code workspace. A page returning HTTP 200 or appearing in the sitemap does not mean Google has indexed it.

**Live check on 20 October 2026:** the homepage and `robots.txt` returned HTTP 200, and `sitemap.xml` returned HTTP 200 with 53 URLs. The live homepage did not contain the Google verification meta tag, and `https://aitoolszone.tech/googleade07204a5ea7ade.html` returned HTTP 404. Both proof methods are present in this local project but have not reached the live site. This is consistent with an ownership-verification failure; publish the website changes first, then verify using the exact method selected in Search Console.

## HTML-tag verification option

The exact HTML tag you supplied is already in the homepage template and generated homepage in this project. After the change is published, open `https://aitoolszone.tech/` and use **View page source** to confirm the `google-site-verification` meta tag is in the `<head>`. Then choose the HTML-tag method for the `https://aitoolszone.tech/` **URL-prefix** property and click **Verify**. A Domain property cannot use this meta-tag method; use the DNS TXT method below. Keep the tag in the homepage template after verification.

## HTML-file verification option

If Google gave you the HTML file method for the URL-prefix property `https://aitoolszone.tech/`, the supplied verification filename and content have been added to the site root as `googleade07204a5ea7ade.html`, and the GitHub Pages production package is configured to publish it. It currently returns HTTP 404 on the live site. After you publish the change, open `https://aitoolszone.tech/googleade07204a5ea7ade.html` in a private/incognito browser window. Confirm it displays exactly:

```text
google-site-verification: googleade07204a5ea7ade.html
```

Then return to the same URL-prefix property's verification screen and click **Verify**. Google says HTML-file verification is for URL-prefix properties, not Domain properties; a Domain property must be verified with the DNS TXT method in the next section. Keep the verification file on the site after verification so Google can continue confirming ownership. [Google ownership verification methods](https://support.google.com/webmasters/answer/9008080).

## 1. Add the Domain property

1. Open [Google Search Console](https://search.google.com/search-console/) and sign in to your own Google account.
2. In the property selector, choose **Add property**, then choose **Domain**.
3. Enter `aitoolszone.tech` without `https://`, `www`, or a page path.
4. Google will show a unique DNS TXT verification record. Copy the exact TXT value Google gives you. Do not use a value from an example or from someone else's website.

## 2. Publish Google's TXT record in the active DNS zone

The public DNS delegation checked on **14 October 2026** points to these authoritative nameservers:

```text
tech-domains.mercury.orderbox-dns.com
tech-domains.mars.orderbox-dns.com
tech-domains.earth.orderbox-dns.com
tech-domains.venus.orderbox-dns.com
```

These nameservers identify the active DNS service as Orderbox nameservers, but do not identify which registrar/reseller account provides your login. Open the domain/DNS dashboard for the registrar or reseller that manages the zone served by those nameservers. A Cloudflare dashboard or screenshot by itself does not prove Cloudflare is authoritative for this domain; do not switch nameservers just for verification.

1. Open the active DNS zone for `aitoolszone.tech` and choose **Add record**.
2. Select type **TXT**. For the name/host, use `@` or leave it blank if that dashboard instructs you to do so for the root domain.
3. Paste Google's exact TXT value into the content/value field. Keep the existing records and nameservers unchanged. Leave TTL at the provider's default unless Google or the provider instructs otherwise.
4. Save the new TXT record. Do not delete, replace, or edit unrelated records.
5. After DNS has had time to update, return to Search Console and click **Verify**. If Google cannot find the record yet, confirm that it was added to the active zone and retry later; do not create a guessed value.

Never share your Google password, DNS password, recovery codes, or DNS API credentials. The TXT verification value is unique to your property; copy it directly from Google's screen into your DNS provider.

## 3. Submit the sitemap

After Search Console verifies the property:

1. Select the verified property you used: `aitoolszone.tech` (Domain) or `https://aitoolszone.tech/` (URL-prefix).
2. Open **Sitemaps** in the left navigation.
3. Enter `https://aitoolszone.tech/sitemap.xml` and submit it.
4. Revisit the report and record Google's processing status and any reported errors. Submission is a discovery hint, not a promise of indexing.

The public sitemap was checked on 20 October 2026: it returned HTTP 200 and contained 53 unique HTTPS URLs on `aitoolszone.tech`.

## 4. Inspect important URLs

Use **URL inspection** for these existing pages:

- `https://aitoolszone.tech/`
- `https://aitoolszone.tech/products/chatgpt-plus/`
- `https://aitoolszone.tech/products/gemini-pro/`
- `https://aitoolszone.tech/products/canva-pro-edu/`
- `https://aitoolszone.tech/categories/ai-assistants/`
- `https://aitoolszone.tech/categories/design/`
- `https://aitoolszone.tech/guides/choose-ai-subscription/`
- `https://aitoolszone.tech/guides/private-vs-shared-access/`

For each URL, note whether it is on Google, whether crawling and indexing are allowed, the last crawl date, Google's selected canonical, and any indexing/crawl reason. If a page is eligible but not indexed, investigate the reported reason and check the live page before requesting indexing. Use **Request indexing** only for a corrected or important page; Google may take time and does not guarantee inclusion.

## 5. Review indexing, Search and generative-AI reports

Review **Page indexing**, the sitemap report and the standard Search results Performance report. After verification, also look for the **Generative AI performance** report under Performance. Google says the report became available to all websites worldwide on 31 August 2026; it reports impressions and pages across generative Search/Discover features, countries and dates, with device detail for Search. Do not interpret missing report data as a zero or claim that impressions represent clicks, leads or sales. See [Google's report documentation announcement](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports?facet3=pdf).

## 6. Resolve genuine errors

Check **Page indexing** and the sitemap report for affected URLs and exact reasons. Confirm a reported issue against the specific page before changing code. For a genuine problem, fix the source, rebuild and deploy, then retest the URL and allow Google to recrawl. Treat temporary reports and processing delays carefully; do not remove a valid URL merely because it is not indexed yet. Monitor search queries, pages, impressions, clicks and click-through rate over comparable date ranges.

The local build and public crawl confirm technical response/metadata behavior only. No authenticated Search Console property or Google indexing result was available for this review.
