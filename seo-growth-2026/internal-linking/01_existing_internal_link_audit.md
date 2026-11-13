# Deliverable 01: Existing Internal Link Audit & Gap Analysis

## 1. Executive Summary & Core Metrics

- **Total Canonical Pages Inspected:** 95
- **Total Internal Link References Extracted:** 3,717
- **Broken Internal Links:** 0 (100% of internal URLs resolve successfully)
- **Redirecting / Non-Canonical Internal Links:** 0
- **Average Incoming Links Per Page:** 39.1
- **Min Incoming Links:** 3 (`/alternatives/`)
- **Max Incoming Links:** 220 (`/pricing/`)

## 2. Link Distribution by Location Context

| Link Location Context | Link Count | Share of Total Links | Description |
| :--- | :---: | :---: | :--- |
| **Body Content (Contextual)** | 1,156 | 31.1% | Links placed inside editorial text, product cards, tables, and recommendation blocks |
| **Header & Primary Navigation** | 854 | 23.0% | Sitewide navigation links in `<header>` and `<nav>` |
| **Footer Navigation** | 1,611 | 43.3% | Sitewide footer links providing baseline crawlability |
| **Other UI / Chrome** | 96 | 2.6% | Sticky order bars, breadcrumb trails, and floating elements |

## 3. Incoming Link Density by Page Category

| Page Category | Page Count | Avg Incoming Links | Min In-Links | Max In-Links | Topical Link Health |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **alternatives** | 2 | 9.0 | 8 | 10 | NEEDS ENHANCEMENT |
| **alternatives_hub** | 1 | 3.0 | 3 | 3 | NEEDS ENHANCEMENT |
| **blog** | 20 | 19.7 | 3 | 194 | MODERATE |
| **blog_hub** | 1 | 211.0 | 211 | 211 | STRONG |
| **categories_hub** | 1 | 201.0 | 201 | 201 | STRONG |
| **category** | 10 | 17.0 | 11 | 24 | MODERATE |
| **compare_hub** | 1 | 207.0 | 207 | 207 | STRONG |
| **comparison** | 11 | 52.9 | 6 | 110 | STRONG |
| **faq** | 1 | 107.0 | 107 | 107 | STRONG |
| **guide** | 3 | 45.3 | 34 | 56 | MODERATE |
| **guides_hub** | 1 | 103.0 | 103 | 103 | STRONG |
| **home** | 1 | 202.0 | 202 | 202 | STRONG |
| **legal_info** | 3 | 116.0 | 98 | 148 | STRONG |
| **pricing** | 1 | 220.0 | 220 | 220 | STRONG |
| **product** | 32 | 15.4 | 6 | 36 | MODERATE |
| **products_hub** | 1 | 139.0 | 139 | 139 | STRONG |
| **use_case** | 4 | 44.2 | 18 | 115 | MODERATE |
| **use_cases_hub** | 1 | 7.0 | 7 | 7 | NEEDS ENHANCEMENT |

## 4. Under-Linked Pages & Topical Authority Gaps

The audit identified that while navigational baseline crawlability is 100%, several key informational and hub pages suffer from low body-content link equity:

1. **Informational Buying Guides in `/blog/` (Only 5–6 Incoming Links Each):**
   - `/blog/where-to-buy-ai-tools-pakistan/` (Only 5 incoming links: 1 footer, 4 contextual)
   - `/blog/how-to-pay-for-chatgpt-plus-pakistan/` (Only 5 incoming links: 1 footer, 4 contextual)
   - `/blog/best-ai-video-generators-pakistan/` (Only 5 incoming links)
   - `/blog/best-ai-image-generators-pakistan/` (Only 6 incoming links)
   - `/blog/ai-tools-for-pakistani-students-research-thesis/` (Only 6 incoming links)

2. **Alternative Evaluation Hub (`/alternatives/`):**
   - Only 3 incoming links sitewide.

3. **Topical Silos Between Commercial & Informational Layers:**
   - Product pages have strong links to parent categories, but rarely link contextually to relevant buying guides or use cases.
   - The student use-case page (`/use-cases/ai-tools-for-students/`) links to older tools, but has not yet linked to newly integrated student tools such as **Coursera Plus**, **Grammarly Premium**, or **QuillBot Premium**.
   - Category pages (`/categories/ai-video/`, `/categories/design/`) do not contextually reference their respective comparison guides or top products inside body paragraphs.

## 5. Top Sitewide Anchor Text Analysis

| Rank | Anchor Text | Occurrences | Context / Role |
| :---: | :--- | :---: | :--- |
| 1 | `Blog` | 210 | Sitewide navigation / discovery |
| 2 | `Categories` | 200 | Sitewide navigation / discovery |
| 3 | `AI for Business` | 190 | Sitewide navigation / discovery |
| 4 | `PKR prices` | 189 | Sitewide navigation / discovery |
| 5 | `AI TOOLS ZONE` | 95 | Sitewide navigation / discovery |
| 6 | `Compare` | 95 | Sitewide navigation / discovery |
| 7 | `Compare AI tools` | 95 | Sitewide navigation / discovery |
| 8 | `About & contact` | 95 | Sitewide navigation / discovery |
| 9 | `FAQs` | 95 | Sitewide navigation / discovery |
| 10 | `Privacy` | 95 | Sitewide navigation / discovery |
| 11 | `Ordering & warranty` | 95 | Sitewide navigation / discovery |
| 12 | `Canva vs Adobe` | 95 | Sitewide navigation / discovery |
| 13 | `CapCut vs Runway` | 95 | Sitewide navigation / discovery |
| 14 | `Leonardo vs Midjourney` | 95 | Sitewide navigation / discovery |
| 15 | `Skip to content` | 94 | Sitewide navigation / discovery |
| 16 | `All tools ↗` | 94 | Sitewide navigation / discovery |
| 17 | `Home` | 94 | Sitewide navigation / discovery |
| 18 | `ChatGPT vs Gemini` | 94 | Sitewide navigation / discovery |
| 19 | `ChatGPT vs Claude` | 94 | Sitewide navigation / discovery |
| 20 | `AI for Students` | 94 | Sitewide navigation / discovery |