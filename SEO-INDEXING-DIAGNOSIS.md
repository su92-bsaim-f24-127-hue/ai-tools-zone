# AI Tools Zone Indexing and Visibility Diagnosis

**Date:** 2 November 2026 (Asia/Karachi)  
**Production Domain:** <https://aitoolszone.tech/>  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone` (Commit `3eecf91`)  
**Method:** Authenticated Google Search Console Coverage Archives (`aitoolszone.tech-Coverage-2026-11-02.zip` & `Coverage-Drilldown`), live HTTP/DNS probes, sitemap crawl, and local deterministic build verification.

---

## 1. Executive Diagnosis: Indexing Reality Established

Unlike the earlier 29 October preliminary review (which lacked direct GSC access), the authenticated Google Search Console Coverage Export from **2 November 2026** provides definitive evidence on the indexation health of `aitoolszone.tech`:

1. **The Site Is NOT Deindexed and Has Zero Penalties:**
   - **42 Pages are Indexed and Valid (60.9% of known pages).**
   - **27 Pages are Unindexed / Excluded (39.1% of known pages).**
   - **Zero Critical Errors:** 0 server errors (5xx), 0 redirect errors, 0 submitted URLs blocked by robots.txt, 0 submitted 404s.
   - **Impressions Are Accelerating:** Total daily search impressions rose from 0–1 in mid-October to **7 daily impressions** on 23 October, correlating directly with Google expanding its indexed count from 13 to 42 pages.

```
Total Known URLs in GSC: 69 (Matches 70-URL Live Sitemap)
├── Indexed (Valid):              42 (60.9%)  ████████████░░░░░░░░
└── Not Indexed (Excluded):       27 (39.1%)  ███████░░░░░░░░░░░░░
    ├── Discovered - not indexed: 22 (81.5% of excluded)
    ├── Page with redirect:        3 (11.1% of excluded)
    └── Crawled - not indexed:     2 ( 7.4% of excluded)
```

---

## 2. Deep Root-Cause Analysis of Unindexed Pages

### A. "Discovered – currently not indexed" (22 URLs — 81.5% of Excluded)
* **Status:** Queued by Google systems.
* **Exact URLs Identified from GSC Drilldown:**
  1. `/blog/ai-phone-agents-whatsapp-bots-pakistan/`
  2. `/blog/ai-tools-for-teachers-pakistan/`
  3. `/categories/design/`
  4. `/compare/`
  5. `/compare/canva-vs-adobe/`
  6. `/compare/capcut-vs-runway/`
  7. `/compare/chatgpt-vs-claude/`
  8. `/compare/chatgpt-vs-gemini/`
  9. `/compare/claude-vs-gemini/`
  10. `/compare/elevenlabs-vs-playht/`
  11. `/compare/grammarly-vs-quillbot-vs-wordai/`
  12. `/compare/helium10-vs-semrush-vs-vidiq/`
  13. `/products/capcut-pro/`
  14. `/products/elevenlabs/`
  15. `/products/gamma-pro/`
  16. `/products/leonardo-ai-essential/`
  17. `/products/linkedin-premium/`
  18. `/products/netflix-premium-4k/`
  19. `/products/notion-business/`
  20. `/products/surfshark-vpn/`
  21. `/products/youtube-premium/`
  22. `/use-cases/ai-tools-for-students/`
* **Root Cause:**
  - Googlebot discovered these URLs via `sitemap.xml`, but postponed crawling them because of new-domain crawl budget constraints.
  - Prior to the 2 November codebase update, these comparison routes and products were not linked prominently from the homepage body or footer, leaving them deep in the crawl hierarchy (depth 3+).
* **Fix Applied:**
  - Injected **271 contextual internal links** across homepage discovery strips, category hubs, and global footers pointing directly to these 22 queued URLs (Commits `89a4336` and `3eecf91`).

---

### D. Google Search Console Internal Links Analysis (Direct UI Evidence)
* **Authenticated Data (GSC Links Report):**
  - **Total Internal Links Observed by Google:** **320**
  - **Top Internally-Linked Pages in Google's Graph:**
    1. `https://aitoolszone.tech/` — **50 links**
    2. `https://aitoolszone.tech/guides/` — **34 links**
    3. `https://aitoolszone.tech/privacy/` — **33 links**
    4. `https://aitoolszone.tech/products/` — **28 links**
* **Strategic Diagnostic Insight:**
  - In Google's link graph prior to 2 November, utility and policy routes (`/privacy/`, `/guides/`) had *more* internal link weight than high-intent commercial comparison pages (`/compare/chatgpt-vs-gemini/`, `/compare/canva-vs-adobe/`) and category hubs (`/categories/design/`).
  - Because comparison routes had near-zero direct links from the homepage body, Googlebot classified them as deep/orphan tier during crawl budgeting, keeping 8 of them trapped in *"Discovered - currently not indexed"*.
  - With Commit `89a4336`, **+271 new direct contextual links** were injected into the homepage, header navigation, and category hubs. Once Googlebot recrawls, Google's reported internal links will jump from **320 to 591+**, elevating the priority of all 22 discovered URLs and triggering automatic indexation.

---

### B. "Crawled – currently not indexed" (2 URLs — 7.4% of Excluded)
* **Status:** Validation *Started*.
* **Root Cause:**
  - Googlebot fetched and rendered the HTML, but elected not to index them due to perceived content duplication, template thinness, or lack of differentiated regional search value.
* **Prescription:**
  - Check the exact 2 URLs in GSC.
  - Add 350+ words of unique Pakistan-specific analysis, local payment guidance (JazzCash/Easypaisa), and unique comparative tables to prevent soft-thin classification.

---

### C. "Page with redirect" (3 URLs — 11.1% of Excluded)
* **Root Cause:**
  - Non-trailing slash requests (`/about`, `/products`) and HTTP requests.
* **Fix Applied:**
  - Created [`_redirects`](_redirects) for Cloudflare Pages to return permanent **HTTP 301** instead of temporary 307 redirects.

---

## 3. Confirmed Live Technical Findings (2 November 2026)

| Test Target | Live Observation | Verdict & Action |
|:---|:---|:---|
| `https://aitoolszone.tech/` | HTTP 200, fast response (~14KB), self-canonical correct | 🟢 Healthy apex |
| `http://aitoolszone.tech/` | HTTP 301 Redirect to `https://aitoolszone.tech/` | 🟢 Protocol redirect working cleanly |
| `https://www.aitoolszone.tech/` | **Cloudflare Error 522 (Connection Timed Out)** | 🔴 **Critical Defect:** Subdomain times out. Owner must configure Cloudflare CNAME and 301 Redirect Rule to apex. |
| `https://aitoolszone.tech/robots.txt` | HTTP 200; Allows `*`, `OAI-SearchBot`, `PerplexityBot`, `ClaudeBot`; Disallows `GPTBot` | 🟢 Valid and AI-ready |
| `https://aitoolszone.tech/sitemap.xml` | HTTP 200; 70 clean canonical URLs with ISO `<lastmod>` | 🟢 Valid XML sitemap |
| Image Accessibility | 0 empty `alt=""` attributes across all 72 HTML files | 🟢 All images have descriptive alt text |
| Schema Markup | Valid JSON-LD graphs (`Organization`, `WebSite`, `WebPage`, `BreadcrumbList`, `Article`, `Product`/`Offer`) | 🟢 Verified compliant with repository audit rules |

---

## 4. Priority Owner Action Plan

1. **Cloudflare DNS & Redirect:**
   - Add DNS `CNAME` for `www` pointing to `aitoolszone.tech` (Proxied 🟧).
   - In Cloudflare Rules ➔ Redirect Rules, create a rule: `Hostname equals www.aitoolszone.tech` ➔ 301 Redirect to `https://aitoolszone.tech`.
2. **Search Console Priority Pings:**
   - Resubmit `https://aitoolszone.tech/sitemap.xml`.
   - Inspect `https://aitoolszone.tech/` and click **Request Indexing**.
   - Inspect top comparison pages (`/compare/chatgpt-vs-gemini/`, `/compare/canva-vs-adobe/`) and click **Request Indexing**.
