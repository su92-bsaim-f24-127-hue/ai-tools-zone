# GitHub Pages publication

Repository: https://github.com/su92-bsaim-f24-127-hue/ai-tools-zone

The GitHub Actions workflow builds the site and deploys the production ZIP contents on every push to main. Development scripts, test dependencies and original image-generation files are not published in the Pages artifact.

Custom domain: `aitoolszone.tech`. The same domain is already used by canonical links and the sitemap. For Actions deployments, the repository Pages setting is authoritative; the CNAME file is also included for branch-based hosting compatibility.

Set the following records at the domain's DNS provider:

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | su92-bsaim-f24-127-hue.github.io |

Replace conflicting records for these same web hosts, keeping unrelated mail and verification records. DNS may take up to 24 hours to propagate. After the domain check and certificate issuance complete, enable Enforce HTTPS in repository Settings → Pages if it is not already enabled.

GitHub Pages does not apply the Netlify/Cloudflare-style `_headers` file. Pages serves the built folder URLs and `404.html`; HTTPS is managed in Pages settings.

Official setup: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
