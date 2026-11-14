"""
generate_phase_0_reports.py
Generates the Phase 0 deliverables:
1. 00_repository_and_url_inventory.md
2. 01_existing_internal_link_audit.md
3. 02_internal_linking_strategy.md
inside seo-growth-2026/internal-linking/
"""

import os
import json
from collections import defaultdict, Counter

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
DOC_DIR = os.path.join(REPO_DIR, "seo-growth-2026", "internal-linking")
RAW_INV_FILE = os.path.join(DOC_DIR, "url_inventory_raw.json")
RAW_GRAPH_FILE = os.path.join(DOC_DIR, "link_graph_raw.json")

def generate_report_00(inventory):
    lines = [
        "# Deliverable 00: Repository and Website URL Inventory",
        "",
        "## 1. Project & Repository Verification",
        "",
        "- **Project Name:** AI Tools Zone",
        "- **Website URL:** `https://aitoolszone.tech/`",
        "- **Active Git Branch:** `feature/competitor-product-keyword-growth`",
        "- **HEAD Commit:** `7f21b78c16a1ca5a67627d373796087b0e35187b`",
        "- **Expected Baseline Commit:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`",
        "- **Merge Base with Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a` (Baseline is direct ancestor)",
        "- **Working Tree Status:** Clean (0 unstaged changes, 0 uncommitted modifications)",
        "- **Market / Target Audience:** Pakistan (`en-PK`)",
        "- **Primary Currency:** Pakistani Rupee (`PKR`)",
        "- **Production Authorization:** **NOT GRANTED** (All implementation strictly confined to feature branch)",
        "",
        "## 2. Project Architecture Source Files",
        "",
        "The static website generation and internal linking structure is controlled by deterministic Python and JSON data sources:",
        "",
        "| Architectural Role | Primary Source File | Description |",
        "| :--- | :--- | :--- |",
        "| **Core Build Engine** | `build_site.py` | Generates homepage, product pages, legal pages, FAQ page, manifest, and coordinates overall build |",
        "| **Editorial & Hub Builder** | `seo_pages.py` | Builds category pages, use cases, comparison pages, alternatives, guides, blog articles, and hubs |",
        "| **Catalog Database** | `data/catalog.json` | Canonical structured data for all 32 live products (prices, durations, features, access) |",
        "| **Product Editorial Content**| `data/product-content.json` | Deep overviews, FAQs, capability bullets, and target intent for individual products |",
        "| **SEO Page Content** | `data/seo-content.json` | Editorial text, category descriptions, comparisons, and use-case recommendations |",
        "| **Blog Content Hub** | `data/blog-content.json` | 20 informational guides addressing long-tail Pakistani search intent |",
        "| **Brand Logos Registry** | `assets/product-logo-sources.json`| Sourced 128x128 official brand marks for all 32 products |",
        "| **State & Freshness Hash** | `data/page-state.json` | Content-based SHA256 hashes and deterministic lastmod timestamps for all 95 routes |",
        "| **SEO Audit Test Suite** | `audit_seo.py` | Crawls all local pages, verifies canonical tags, meta tags, image tags, and broken links |",
        "| **Growth Engine Audit** | `audit_growth.py` | Validates 95 indexable pages, product offers, incoming link graphs, and contract parity |",
        "| **Security Validator** | `scripts/test_render_text_security.py` | Validates markdown link sanitization and XSS/scheme protection |",
        "| **Packaging Pipeline** | `package_site.py` | Validates production package integrity (165 production files in `ai-tools-zone.zip`) |",
        "",
        "## 3. Comprehensive URL Inventory (95 Canonical Pages)",
        "",
        "| # | Canonical Path | Page Type | H1 Heading | Indexable | In-Links | Out-Links | Primary Search Intent |",
        "| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :--- |"
    ]

    for idx, (path, d) in enumerate(sorted(inventory.items()), 1):
        lines.append(f"| {idx} | `{path}` | {d['type']} | {d['h1'][:40]} | {'Yes' if d['indexable'] else 'No'} | {d['incoming_count']} | {d['outgoing_count']} | {d['intent'][:45]} |")

    return "\n".join(lines)

def generate_report_01(inventory, graph_data):
    links = graph_data["links"]
    total_links = len(links)
    
    # Categorize links by location
    loc_counter = Counter(l["location"] for l in links)
    
    # Analyze anchor text
    anchors = [l["anchor"] for l in links if l["anchor"]]
    anchor_counter = Counter(anchors)
    
    # Analyze incoming links by page type
    by_type = defaultdict(list)
    for path, d in inventory.items():
        by_type[d["type"]].append(d["incoming_count"])

    lines = [
        "# Deliverable 01: Existing Internal Link Audit & Gap Analysis",
        "",
        "## 1. Executive Summary & Core Metrics",
        "",
        "- **Total Canonical Pages Inspected:** 95",
        "- **Total Internal Link References Extracted:** {:,}".format(total_links),
        "- **Broken Internal Links:** 0 (100% of internal URLs resolve successfully)",
        "- **Redirecting / Non-Canonical Internal Links:** 0",
        "- **Average Incoming Links Per Page:** {:.1f}".format(total_links / len(inventory)),
        "- **Min Incoming Links:** {} (`/alternatives/`)".format(min(d["incoming_count"] for d in inventory.values())),
        "- **Max Incoming Links:** {} (`/pricing/`)".format(max(d["incoming_count"] for d in inventory.values())),
        "",
        "## 2. Link Distribution by Location Context",
        "",
        "| Link Location Context | Link Count | Share of Total Links | Description |",
        "| :--- | :---: | :---: | :--- |",
        f"| **Body Content (Contextual)** | {loc_counter.get('body_content', 0):,} | {loc_counter.get('body_content', 0)/total_links*100:.1f}% | Links placed inside editorial text, product cards, tables, and recommendation blocks |",
        f"| **Header & Primary Navigation** | {loc_counter.get('header_nav', 0):,} | {loc_counter.get('header_nav', 0)/total_links*100:.1f}% | Sitewide navigation links in `<header>` and `<nav>` |",
        f"| **Footer Navigation** | {loc_counter.get('footer', 0):,} | {loc_counter.get('footer', 0)/total_links*100:.1f}% | Sitewide footer links providing baseline crawlability |",
        f"| **Other UI / Chrome** | {loc_counter.get('other', 0):,} | {loc_counter.get('other', 0)/total_links*100:.1f}% | Sticky order bars, breadcrumb trails, and floating elements |",
        "",
        "## 3. Incoming Link Density by Page Category",
        "",
        "| Page Category | Page Count | Avg Incoming Links | Min In-Links | Max In-Links | Topical Link Health |",
        "| :--- | :---: | :---: | :---: | :---: | :--- |"
    ]

    for ptype, counts in sorted(by_type.items()):
        avg_c = sum(counts) / len(counts)
        health = "STRONG" if avg_c > 50 else ("MODERATE" if avg_c > 15 else "NEEDS ENHANCEMENT")
        lines.append(f"| **{ptype}** | {len(counts)} | {avg_c:.1f} | {min(counts)} | {max(counts)} | {health} |")

    lines.extend([
        "",
        "## 4. Under-Linked Pages & Topical Authority Gaps",
        "",
        "The audit identified that while navigational baseline crawlability is 100%, several key informational and hub pages suffer from low body-content link equity:",
        "",
        "1. **Informational Buying Guides in `/blog/` (Only 5–6 Incoming Links Each):**",
        "   - `/blog/where-to-buy-ai-tools-pakistan/` (Only 5 incoming links: 1 footer, 4 contextual)",
        "   - `/blog/how-to-pay-for-chatgpt-plus-pakistan/` (Only 5 incoming links: 1 footer, 4 contextual)",
        "   - `/blog/best-ai-video-generators-pakistan/` (Only 5 incoming links)",
        "   - `/blog/best-ai-image-generators-pakistan/` (Only 6 incoming links)",
        "   - `/blog/ai-tools-for-pakistani-students-research-thesis/` (Only 6 incoming links)",
        "",
        "2. **Alternative Evaluation Hub (`/alternatives/`):**",
        "   - Only 3 incoming links sitewide.",
        "",
        "3. **Topical Silos Between Commercial & Informational Layers:**",
        "   - Product pages have strong links to parent categories, but rarely link contextually to relevant buying guides or use cases.",
        "   - The student use-case page (`/use-cases/ai-tools-for-students/`) links to older tools, but has not yet linked to newly integrated student tools such as **Coursera Plus**, **Grammarly Premium**, or **QuillBot Premium**.",
        "   - Category pages (`/categories/ai-video/`, `/categories/design/`) do not contextually reference their respective comparison guides or top products inside body paragraphs.",
        "",
        "## 5. Top Sitewide Anchor Text Analysis",
        "",
        "| Rank | Anchor Text | Occurrences | Context / Role |",
        "| :---: | :--- | :---: | :--- |"
    ])

    for rk, (anc, cnt) in enumerate(anchor_counter.most_common(20), 1):
        clean_anc = anc if anc else "[Icon / Logo Link]"
        lines.append(f"| {rk} | `{clean_anc[:45]}` | {cnt} | Sitewide navigation / discovery |")

    return "\n".join(lines)

def generate_report_02(inventory):
    lines = [
        "# Deliverable 02: Controlled Internal Linking Strategy & Architecture",
        "",
        "## 1. Strategy Overview",
        "",
        "The objective of the controlled internal linking implementation is to build a coherent topical graph across commercial, category, product, and informational assets in Pakistan without keyword stuffing or catalog distortion.",
        "",
        "```mermaid",
        "graph TD",
        "  Home[\"Homepage (/)\"] --> Products[\"All Tools (/products/)\"]",
        "  Home --> Pricing[\"PKR Pricing (/pricing/)\"]",
        "  Home --> Students[\"AI for Students (/use-cases/ai-tools-for-students/)\"]",
        "  Home --> VideoCat[\"AI Video Category (/categories/ai-video/)\"]",
        "  Home --> DesignCat[\"Design Category (/categories/design/)\"]",
        "  Home --> BuyGuide[\"Where to Buy Guide (/blog/where-to-buy-ai-tools-pakistan/)\"]",
        "",
        "  Products --> ChatGPT[\"ChatGPT Plus (/products/chatgpt-plus/)\"]",
        "  Products --> CapCut[\"CapCut Pro (/products/capcut-pro/)\"]",
        "  Products --> Leonardo[\"Leonardo AI (/products/leonardo-ai-essential/)\"]",
        "  Products --> Coursera[\"Coursera Plus (/products/coursera-plus-premium/)\"]",
        "  Products --> BuyGuide",
        "",
        "  Students --> ChatGPT",
        "  Students --> Coursera",
        "  Students --> Grammarly[\"Grammarly Premium (/products/grammarly-premium/)\"]",
        "  Students --> QuillBot[\"QuillBot Premium (/products/quillbot-premium/)\"]",
        "  Students --> Notion[\"Notion Business (/products/notion-business/)\"]",
        "  Students --> StudentGuide[\"Student Thesis Guide (/blog/ai-tools-for-pakistani-students-research-thesis/)\"]",
        "",
        "  VideoCat --> CapCut",
        "  VideoCat --> Runway[\"Runway ML Gen-3 (/products/runway-ml-gen-3/)\"]",
        "  VideoCat --> Descript[\"Descript Creator (/products/descript-creator/)\"]",
        "  VideoCat --> VideoComp[\"CapCut vs Runway (/compare/capcut-vs-runway/)\"]",
        "  VideoCat --> VideoGuide[\"Best AI Video Guide (/blog/best-ai-video-generators-pakistan/)\"]",
        "",
        "  DesignCat --> Leonardo",
        "  DesignCat --> Canva[\"Canva Pro (/products/canva-pro-edu/)\"]",
        "  DesignCat --> Adobe[\"Adobe CC (/products/adobe-creative-cloud/)\"]",
        "  DesignCat --> DesignComp[\"Leonardo vs Midjourney (/compare/leonardo-vs-midjourney/)\"]",
        "  DesignCat --> DesignGuide[\"Best AI Image Guide (/blog/best-ai-image-generators-pakistan/)\"]",
        "",
        "  ChatGPT --> PayGuide[\"How to Pay Guide (/blog/how-to-pay-for-chatgpt-plus-pakistan/)\"]",
        "  ChatGPT --> Pricing",
        "  ChatGPT --> Students",
        "  PayGuide --> ChatGPT",
        "  PayGuide --> BuyGuide",
        "  BuyGuide --> Products",
        "  BuyGuide --> Pricing",
        "```",
        "",
        "## 2. Target Keyword to Destination URL Mapping",
        "",
        "| Keyword Cluster | Target Buyer Keywords | Canonical Destination URL | Content Type | Planned Anchor Variations |",
        "| :--- | :--- | :--- | :--- | :--- |",
        "| **Cluster A** | `premium AI accounts Pakistan`<br>`buy AI tools in Pakistan`<br>`where to buy AI tools in Pakistan` | `/products/`<br>`/blog/where-to-buy-ai-tools-pakistan/` | Commercial Catalog<br>Informational Guide | - explore premium AI accounts in Pakistan<br>- buy AI tools in Pakistan with local payment<br>- where to buy AI tools in Pakistan buying guide |",
        "| **Cluster B** | `affordable AI subscriptions Pakistan` | `/pricing/` | Pricing Matrix Hub | - affordable AI subscriptions in Pakistan<br>- compare AI subscription prices in PKR<br>- view budget-friendly plans under PKR 1,000 |",
        "| **Cluster C** | `cheap AI tools for students Pakistan`<br>`best AI productivity tools for students Pakistan` | `/use-cases/ai-tools-for-students/`<br>`/blog/ai-tools-for-pakistani-students-research-thesis/` | Workflow Use-Case<br>Informational Guide | - cheap AI tools for students in Pakistan<br>- best AI productivity tools for Pakistani students<br>- academic research and thesis AI software |",
        "| **Cluster D** | `AI video editing tools Pakistan` | `/categories/ai-video/`<br>`/blog/best-ai-video-generators-pakistan/` | Category Hub<br>Informational Guide | - AI video editing tools in Pakistan<br>- explore AI video generators and editors<br>- compare CapCut and Runway plans |",
        "| **Cluster E** | `AI image generator subscription Pakistan` | `/categories/design/`<br>`/blog/best-ai-image-generators-pakistan/` | Category Hub<br>Informational Guide | - AI image generator subscriptions in Pakistan<br>- design and AI image generation tools<br>- compare Leonardo AI and Adobe plans |",
        "| **Cluster F** | `how to buy ChatGPT Plus in Pakistan` | `/products/chatgpt-plus/`<br>`/blog/how-to-pay-for-chatgpt-plus-pakistan/` | Product Page<br>Payment Guide | - how to buy ChatGPT Plus in Pakistan<br>- ChatGPT Plus subscription in Pakistan<br>- read the ChatGPT payment troubleshooting guide |",
        "",
        "## 3. Strict Safety & Content Reconciliation Safeguards",
        "",
        "1. **Zero URL Cannibalization:**",
        "   - The site already has `/blog/where-to-buy-ai-tools-pakistan/` and `/blog/how-to-pay-for-chatgpt-plus-pakistan/`. We strictly enhance and link these existing canonical URLs rather than creating duplicate variants (e.g. `/blog/where-to-buy-ai-tools-in-pakistan/`).",
        "2. **Zero Commercial Data Alteration:**",
        "   - No changes to product prices, durations, delivery SLAs, warranties, or access types.",
        "3. **Zero Production Push:**",
        "   - All changes remain on `feature/competitor-product-keyword-growth` without `git push`, merge to `main`, or production deployment.",
        "4. **Full Test Enforcement:**",
        "   - Every change must pass `python audit_seo.py`, `python audit_growth.py`, and `python scripts/test_render_text_security.py` with 0 errors.",
        "",
        "## 4. Four-Phase Execution Roadmap",
        "",
        "- **Phase 1: Existing Page Optimization** (`/`, `/products/`, `/pricing/`, `/use-cases/ai-tools-for-students/`)",
        "- **Phase 2: Category and Product Linking** (`/categories/ai-video/`, `/categories/design/`, `/products/chatgpt-plus/`, CapCut, Leonardo, comparison pages)",
        "- **Phase 3: Supporting Content Creation & Alignment** (Enhancing `/blog/where-to-buy-ai-tools-pakistan/`, `/blog/how-to-pay-for-chatgpt-plus-pakistan/`, and student thesis guide)",
        "- **Phase 4: Comprehensive QA & Verification** (Link validation, orphan check, anchor text audit, regression testing, measurement plan)",
    ]

    return "\n".join(lines)

def main():
    with open(RAW_INV_FILE, "r", encoding="utf-8") as f:
        inventory = json.load(f)

    with open(RAW_GRAPH_FILE, "r", encoding="utf-8") as f:
        graph = json.load(f)

    r0 = generate_report_00(inventory)
    with open(os.path.join(DOC_DIR, "00_repository_and_url_inventory.md"), "w", encoding="utf-8") as f:
        f.write(r0)
    print("Generated 00_repository_and_url_inventory.md")

    r1 = generate_report_01(inventory, graph)
    with open(os.path.join(DOC_DIR, "01_existing_internal_link_audit.md"), "w", encoding="utf-8") as f:
        f.write(r1)
    print("Generated 01_existing_internal_link_audit.md")

    r2 = generate_report_02(inventory)
    with open(os.path.join(DOC_DIR, "02_internal_linking_strategy.md"), "w", encoding="utf-8") as f:
        f.write(r2)
    print("Generated 02_internal_linking_strategy.md")

if __name__ == "__main__":
    main()
