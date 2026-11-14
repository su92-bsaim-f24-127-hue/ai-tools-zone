"""
audit_internal_links_detailed.py
Crawls and parses all 95 rendered HTML canonical pages of AI Tools Zone.
Builds the complete URL inventory, link graph, anchor text registry, and gap analysis.
Outputs structured JSON and Markdown for Phase 0 and Phase 4.
"""

import os
import json
import re
from urllib.parse import urlparse, urljoin
from collections import defaultdict, Counter
from bs4 import BeautifulSoup

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
ORIGIN = "https://aitoolszone.tech"
STATE_FILE = os.path.join(REPO_DIR, "data", "page-state.json")
CATALOG_FILE = os.path.join(REPO_DIR, "data", "catalog.json")

def file_for_path(path):
    rel = path.strip("/")
    if not rel:
        return os.path.join(REPO_DIR, "index.html")
    candidate_html = os.path.join(REPO_DIR, rel + ".html")
    if os.path.isfile(candidate_html):
        return candidate_html
    candidate_index = os.path.join(REPO_DIR, rel, "index.html")
    if os.path.isfile(candidate_index):
        return candidate_index
    return os.path.join(REPO_DIR, rel)

def get_page_type(path):
    if path == "/": return "home"
    if path == "/products/": return "products_hub"
    if path.startswith("/products/"): return "product"
    if path == "/categories/": return "categories_hub"
    if path.startswith("/categories/"): return "category"
    if path == "/compare/": return "compare_hub"
    if path.startswith("/compare/"): return "comparison"
    if path == "/alternatives/": return "alternatives_hub"
    if path.startswith("/alternatives/"): return "alternatives"
    if path == "/guides/": return "guides_hub"
    if path.startswith("/guides/"): return "guide"
    if path == "/use-cases/": return "use_cases_hub"
    if path.startswith("/use-cases/"): return "use_case"
    if path == "/blog/": return "blog_hub"
    if path.startswith("/blog/"): return "blog"
    if path in ("/pricing/", "/pricing"): return "pricing"
    if path in ("/faq/", "/faq"): return "faq"
    if path in ("/about/", "/privacy/", "/terms/"): return "legal_info"
    return "other"

def infer_intent_and_topic(path, page_type, title, h1):
    if path == "/":
        return "Commercial Discovery & Marketplace Overview", "Overview of AI subscriptions, tools, PKR pricing, and trust signals in Pakistan"
    if page_type == "products_hub":
        return "Commercial Exploration / Tool Catalog", "Full catalog directory of AI tools and software subscriptions available in Pakistan"
    if page_type == "product":
        return "Commercial Purchase / Transactional Intent", f"Specific pricing, subscription terms, and WhatsApp ordering for {h1}"
    if page_type == "pricing":
        return "Commercial Comparison / Price Evaluation", "PKR price breakdown and budget brackets across all AI subscriptions"
    if page_type == "category":
        return "Category-Level Commercial & Informational Evaluation", f"Category curation and plan options for {h1}"
    if page_type == "comparison":
        return "Commercial Investigation & Tool Evaluation", f"Direct feature, price, and workflow comparison for {h1}"
    if page_type == "alternatives":
        return "Commercial Alternative Evaluation", f"Alternative software and AI workflow substitutes for {h1}"
    if page_type == "use_case":
        return "Workflow-Specific Informational & Tool Adoption", f"Workflow guidance and recommended software stacks for {h1}"
    if page_type == "guide":
        return "Informational / Buying Decision Support", f"Methodology and safety guidelines for {h1}"
    if page_type == "blog":
        return "Informational / Long-Tail Organic Query Resolution", f"In-depth guide and actionable workflow advice for {h1}"
    if page_type == "faq":
        return "Transactional Assurance & FAQ Resolution", "Answers to ordering, payment, and account delivery questions"
    return "Trust, Transparency & Compliance", f"Legal and policy terms for {h1}"

def main():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        page_state = json.load(f)

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # 1. Parse all pages
    url_inventory = {}
    links_list = []
    incoming_links = defaultdict(list)
    outgoing_links = defaultdict(list)
    broken_links = []
    external_links = defaultdict(set)

    for path in sorted(page_state.keys()):
        filepath = file_for_path(path)
        if not os.path.exists(filepath):
            print(f"File missing for {path}: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        
        # Meta tags
        title_tag = soup.find("title")
        title = title_tag.get_text().strip() if title_tag else ""

        h1_tag = soup.find("h1")
        h1 = h1_tag.get_text().strip() if h1_tag else ""

        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc.get("content", "").strip() if meta_desc else ""

        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        canonical = canonical_tag.get("href", "").strip() if canonical_tag else ""

        robots_tag = soup.find("meta", attrs={"name": "robots"})
        robots = robots_tag.get("content", "").strip() if robots_tag else "index,follow"

        ptype = get_page_type(path)
        intent, topic = infer_intent_and_topic(path, ptype, title, h1)

        # Links extraction
        page_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            anchor_text = a.get_text(separator=" ", strip=True)
            
            # Determine location context
            parent_tag = a.parent.name if a.parent else ""
            in_header = bool(a.find_parent("header") or a.find_parent("nav"))
            in_footer = bool(a.find_parent("footer"))
            in_main = bool(a.find_parent("main"))
            
            location = "body_content"
            if in_header:
                location = "header_nav"
            elif in_footer:
                location = "footer"
            elif not in_main:
                location = "other"

            parsed = urlparse(urljoin(ORIGIN + path, href))
            if parsed.scheme in ("http", "https"):
                if parsed.netloc == "aitoolszone.tech":
                    target_path = parsed.path
                    if not target_path.endswith("/") and not target_path.endswith(".html"):
                        target_path += "/"
                    
                    is_valid = target_path in page_state
                    links_list.append({
                        "source": path,
                        "destination": target_path,
                        "anchor": anchor_text,
                        "location": location,
                        "is_valid": is_valid
                    })
                    outgoing_links[path].append(target_path)
                    incoming_links[target_path].append(path)
                    if not is_valid and not target_path.startswith("/admin"):
                        broken_links.append((path, href, target_path))
                else:
                    external_links[path].add(parsed.geturl())

        url_inventory[path] = {
            "path": path,
            "url": ORIGIN + path,
            "type": ptype,
            "title": title,
            "h1": h1,
            "meta_description": description,
            "canonical": canonical,
            "robots": robots,
            "indexable": "noindex" not in robots.lower(),
            "topic": topic,
            "intent": intent,
            "incoming_count": 0, # Will fill
            "outgoing_count": len(outgoing_links[path])
        }

    for path, data in url_inventory.items():
        data["incoming_count"] = len(incoming_links[path])

    print("\n" + "="*60)
    print("PHASE 0 INVENTORY SUMMARY:")
    print(f"Total Canonical Pages Inventoried: {len(url_inventory)}")
    print(f"Total Internal Link References Extracted: {len(links_list)}")
    print(f"Broken Internal Links Found: {len(broken_links)}")

    # Incoming link distribution
    incoming_counts = [d["incoming_count"] for d in url_inventory.values()]
    print(f"Min Incoming Links: {min(incoming_counts)}")
    print(f"Max Incoming Links: {max(incoming_counts)}")
    print(f"Average Incoming Links: {sum(incoming_counts) / len(incoming_counts):.1f}")
    
    # Bottom 10 incoming links
    lowest = sorted(url_inventory.values(), key=lambda x: x["incoming_count"])[:15]
    print("\nLowest incoming link count pages:")
    for item in lowest:
        print(f" - {item['path']:40} : {item['incoming_count']} incoming (type: {item['type']})")

    # Save detailed data for reports
    out_dir = os.path.join(REPO_DIR, "seo-growth-2026", "internal-linking")
    os.makedirs(out_dir, exist_ok=True)
    
    with open(os.path.join(out_dir, "url_inventory_raw.json"), "w", encoding="utf-8") as f:
        json.dump(url_inventory, f, indent=2)

    with open(os.path.join(out_dir, "link_graph_raw.json"), "w", encoding="utf-8") as f:
        json.dump({
            "total_links": len(links_list),
            "links": links_list,
            "broken": broken_links
        }, f, indent=2)

    print(f"\nRaw inventory and link graph written to {out_dir}")

if __name__ == "__main__":
    main()
