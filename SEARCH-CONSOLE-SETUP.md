# Google Search Console setup

This is an owner-run checklist. Current Search Console indexing, impressions, clicks and rankings were not inspected today. A page returning HTTP 200 or appearing in the sitemap does not mean Google has indexed it.

**Current public check — 29 October 2026:** the HTTPS homepage, `robots.txt` and `sitemap.xml` return HTTP 200. The sitemap contains 67 unique canonical HTTPS URLs, and all 67 pages return HTTP 200 with matching self-canonicals. The Google verification meta tag and HTML proof file remain public. These checks do not prove current Search Console ownership or indexing. An earlier authenticated Search Console visit on 22 October showed the URL-prefix property as verified and the submitted sitemap as successful with 66 discovered pages; that account view has not been refreshed today.

**Canonical follow-up:** the HTTP homepage returns the same content as HTTPS without redirecting, and `www.aitoolszone.tech` currently returns DNS `NXDOMAIN`. See [SEO-INDEXING-DIAGNOSIS.md](SEO-INDEXING-DIAGNOSIS.md) for the precise owner-controlled Cloudflare/GitHub Pages steps. Do not add extra canonical tags to compensate for missing host redirects.

## HTML-tag verification option

The exact HTML tag you supplied is published in the homepage head and was confirmed in the live page source on 22 October 2026. In Search Console, select the URL-prefix property https://aitoolszone.tech/, choose the HTML tag method, and verify that the token displayed in the current Google wizard matches the published tag. A Domain property cannot use this method; use the DNS TXT method below. Keep the tag in the homepage template after verification.

## HTML-file verification option

If Google gave you the HTML-file method for the URL-prefix property https://aitoolszone.tech/, the supplied verification file is published at the site root and is included in the production package. A live check on 22 October 2026 returned HTTP 200 and the exact body below. Open https://aitoolszone.tech/googleade07204a5ea7ade.html in a private/incognito browser window to confirm it remains accessible:

```text
google-site-verification: googleade07204a5ea7ade.html
```

Then return to the same URL-prefix property's verification screen and click **Verify**. Google says HTML-file verification is for URL-prefix properties, not Domain properties; a Domain property must be verified with the DNS TXT method in the next section. Keep the verification file on the site after verification so Google can continue confirming ownership. [Google ownership verification methods](https://support.google.com/webmasters/answer/9008080).

## If ownership verification still fails

1. Check the property shown in Search Console. The homepage tag and HTML file verify the URL-prefix property https://aitoolszone.tech/; they do not verify the Domain property aitoolszone.tech. A Domain property requires the exact DNS TXT value Google provides.
2. Check the verification method selected in the Google wizard. Use the meta-tag proof with HTML tag, or the public file URL with HTML file. Confirm the current Google token/file name matches the proof being checked.
3. Confirm you are signed into the Google account that was granted ownership and that the final address is the aitoolszone.tech host after redirects. Do not remove the live tag or file.
4. If Google generated a new token or file name, use that exact new proof and publish it before retrying. Never guess a TXT value or overwrite unrelated DNS records.


## 1. Add the Domain property

1. Open [Google Search Console](https://search.google.com/search-console/) and sign in to your own Google account.
2. In the property selector, choose **Add property**, then choose **Domain**.
3. Enter `aitoolszone.tech` without `https://`, `www`, or a page path.
4. Google will show a unique DNS TXT verification record. Copy the exact TXT value Google gives you. Do not use a value from an example or from someone else's website.

## 2. Publish Google's TXT record in the active DNS zone

The public DNS delegation checked on **29 October 2026** points to these authoritative Cloudflare nameservers:

```text
amanda.ns.cloudflare.com
giancarlo.ns.cloudflare.com
```

The earlier 14 October Orderbox delegation note is outdated. Cloudflare is the publicly delegated DNS provider now. Open the `aitoolszone.tech` zone in the Cloudflare account that manages these nameservers; do not switch nameservers or replace any existing records for Search Console verification.

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

The current public sitemap check on 29 October 2026 returned HTTP 200 and contained 67 unique canonical HTTPS URLs on `aitoolszone.tech`. All 67 listed pages returned HTTP 200 and declared the matching HTTPS self-canonical. The HTTP homepage still does not redirect to HTTPS, and `www.aitoolszone.tech` currently returns DNS `NXDOMAIN`; see [SEO-INDEXING-DIAGNOSIS.md](SEO-INDEXING-DIAGNOSIS.md).

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

Review **Page indexing**, the sitemap report and the standard Search results Performance report. After verification, look for the **Generative AI performance** report under Performance. Google says the Search report rolled out worldwide on 31 August 2026 and includes AI Overviews and AI Mode; Discover has a separate generative-AI report. The report can show impressions by page, country, date and device. Do not interpret a missing report or data as zero, or claim that impressions represent clicks, leads or sales. See [Google's Search report help](https://support.google.com/webmasters/answer/16984139) and [report announcement](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports?facet3=pdf).

### Check the Search generative AI inclusion setting

After you can open the verified property, go to **Settings → Search generative AI**. Confirm that **Include my site's links and content in Search generative AI features** is selected, or that the property inherits an included setting from its parent. Google documents inclusion as the default for properties, but this project cannot inspect your account setting; its current value is **unverified**. Do not change a setting you do not understand. Google says this control affects eligibility for AI Overviews, AI Mode and generative features in Discover, but is not a ranking signal for other Search results. See [Google's Search generative AI control guide](https://support.google.com/webmasters/answer/16908024).

The Search report covers impressions for AI Overviews and AI Mode; Discover has a separate generative-AI report. Google may not show a report when there is not enough reportable activity. A missing report does not prove that the website is excluded. The site source currently allows Googlebot and contains no `nosnippet`, `max-snippet:0` or `data-nosnippet` exclusion, but source inspection cannot reveal the account-level Search Console setting. Google's [AI features guidance](https://developers.google.com/search/docs/appearance/ai-features) says normal Search eligibility and helpful content still apply; no special AI file or schema guarantees inclusion.

## 6. Resolve genuine errors

Check **Page indexing** and the sitemap report for affected URLs and exact reasons. Confirm a reported issue against the specific page before changing code. For a genuine problem, fix the source, rebuild and deploy, then retest the URL and allow Google to recrawl. Treat temporary reports and processing delays carefully; do not remove a valid URL merely because it is not indexed yet. Monitor search queries, pages, impressions, clicks and click-through rate over comparable date ranges.

The local build and public crawl confirm technical response/metadata behavior only. No authenticated Search Console property or Google indexing result was available for this review.
