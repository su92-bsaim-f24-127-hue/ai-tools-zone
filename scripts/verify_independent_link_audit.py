"""
scripts/verify_independent_link_audit.py
Performs an independent crawl of all generated HTML files on disk,
recalculates link graphs, verifies each added link, and checks canonicality.
"""

import os
import json
import re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

REPO_DIR = Path(r"C:\Users\ELITEBOOK\projects\ai-tools-zone")
STATE_FILE = REPO_DIR / "data" / "page-state.json"

with open(STATE_FILE, "r", encoding="utf-8") as f:
    routes = json.load(f)

class SimpleLinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_a = None
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            self.current_a = attrs_dict
            self.current_text = []

    def handle_data(self, data):
        if self.current_a is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.current_a is not None:
            href = self.current_a.get("href", "")
            text = " ".join("".join(self.current_text).split())
            self.links.append({"href": href, "text": text, "attrs": self.current_a})
            self.current_a = None
            self.current_text = []

def file_for_path(path):
    clean = path.strip("/")
    if not clean:
        return REPO_DIR / "index.html"
    return REPO_DIR / clean / "index.html"

def audit_all():
    print("=== STARTING INDEPENDENT RECALCULATION & AUDIT ===")
    canonical_paths = set(routes)
    
    # Track link graph
    incoming = {p: [] for p in routes}
    outgoing = {p: [] for p in routes}
    all_extracted_links = []
    broken_links = []
    non_canonical_links = []
    
    for path in routes:
        html_file = file_for_path(path)
        if not html_file.exists():
            print(f"ERROR: HTML file missing for route: {path} -> {html_file}")
            continue
        
        content = html_file.read_text(encoding="utf-8")
        parser = SimpleLinkExtractor()
        parser.feed(content)
        
        for item in parser.links:
            href = item["href"]
            text = item["text"]
            
            # Filter internal links
            if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
                continue
            
            # Parse URL
            parsed = urlparse(href)
            if parsed.scheme in ["http", "https"]:
                # External
                continue
            
            # Clean path
            target_path = parsed.path
            if not target_path.startswith("/"):
                # Relative link e.g. from index.html: "products/"
                base = path if path.endswith("/") else path + "/"
                target_path = urljoin(base, target_path)
            
            if not target_path.endswith("/") and not target_path.endswith(".html") and not parsed.fragment:
                # Missing trailing slash
                target_path += "/"
            
            # Verify if target path is in canonical routes
            # (Strip hash or check if base path is in canonical routes)
            base_target = target_path
            if not base_target.endswith("/"):
                base_target = base_target + "/"
                
            is_canonical = base_target in canonical_paths or target_path in canonical_paths
            
            target_file = file_for_path(base_target)
            target_exists = target_file.exists()
            
            link_record = {
                "source": path,
                "target_raw": href,
                "target_resolved": target_path,
                "base_target": base_target,
                "text": text,
                "canonical": is_canonical,
                "exists": target_exists
            }
            
            all_extracted_links.append(link_record)
            outgoing[path].append(link_record)
            
            if base_target in incoming:
                incoming[base_target].append(link_record)
            elif target_path in incoming:
                incoming[target_path].append(link_record)
            else:
                if not target_exists:
                    broken_links.append(link_record)
                if not is_canonical:
                    non_canonical_links.append(link_record)

    total_links = len(all_extracted_links)
    print(f"Total Internal Links Extracted: {total_links}")
    print(f"Broken Links Found: {len(broken_links)}")
    print(f"Non-Canonical Internal Links Found: {len(non_canonical_links)}")
    
    # Specific targeted link verification
    checks = [
        ("/", "/products/", "premium AI accounts in Pakistan"),
        ("/", "/pricing/", "affordable AI subscriptions"),
        ("/", "/use-cases/ai-tools-for-students/", "AI tools for students"),
        ("/", "/categories/ai-video/", "AI video editing tools"),
        ("/", "/categories/design/", "AI image generation tools"),
        ("/", "/blog/where-to-buy-ai-tools-pakistan/", "where to buy AI tools in Pakistan"),
        ("/products/", "/pricing/", "compare AI subscription prices in PKR"),
        ("/products/", "/use-cases/ai-tools-for-students/", "student-friendly AI tools and thesis software"),
        ("/products/", "/categories/ai-video/", "AI video editing tools and generators"),
        ("/products/", "/categories/design/", "AI image generator subscriptions and design tools"),
        ("/products/", "/blog/where-to-buy-ai-tools-pakistan/", "where to buy AI tools in Pakistan"),
        ("/pricing/", "/products/", "all tools directory"),
        ("/pricing/", "/use-cases/ai-tools-for-students/", "budget-friendly AI tools for students"),
        ("/pricing/", "/categories/ai-video/", "AI video editing subscriptions"),
        ("/pricing/", "/categories/design/", "AI image generation software"),
        ("/use-cases/ai-tools-for-students/", "/products/chatgpt-plus/", "ChatGPT Plus"),
        ("/use-cases/ai-tools-for-students/", "/products/gemini-pro/", "Gemini Pro"),
        ("/use-cases/ai-tools-for-students/", "/products/quillbot-premium/", "QuillBot Premium"),
        ("/use-cases/ai-tools-for-students/", "/products/grammarly-premium/", "Grammarly Premium"),
        ("/use-cases/ai-tools-for-students/", "/products/perplexity-pro/", "Perplexity Pro"),
        ("/use-cases/ai-tools-for-students/", "/products/notion-business/", "Notion Business"),
        ("/use-cases/ai-tools-for-students/", "/products/canva-pro-edu/", "Canva Pro Edu"),
        ("/use-cases/ai-tools-for-students/", "/products/coursera-plus-premium/", "Coursera Plus"),
        ("/use-cases/ai-tools-for-students/", "/blog/ai-tools-for-pakistani-students-research-thesis/", "playbook for student research and thesis writing"),
        ("/use-cases/ai-tools-for-students/", "/pricing/", "PKR pricing guide"),
        ("/categories/ai-video/", "/products/capcut-pro/", "CapCut Pro"),
        ("/categories/ai-video/", "/products/runway-ml-gen-3/", "Runway ML Gen-3"),
        ("/categories/ai-video/", "/products/veo-3-ultra/", "Veo 3 Ultra"),
        ("/categories/ai-video/", "/products/descript-creator/", "Descript Creator"),
        ("/categories/ai-video/", "/compare/capcut-vs-runway/", "CapCut vs Runway comparison guide"),
        ("/categories/ai-video/", "/blog/best-ai-video-generators-pakistan/", "best AI video generators guide"),
        ("/categories/design/", "/products/canva-pro-edu/", "Canva Pro Edu"),
        ("/categories/design/", "/products/leonardo-ai-essential/", "Leonardo AI Essential"),
        ("/categories/design/", "/products/figma-pro-private/", "Figma Pro Private"),
        ("/categories/design/", "/products/adobe-creative-cloud/", "Adobe Creative Cloud"),
        ("/categories/design/", "/compare/leonardo-vs-midjourney/", "Leonardo vs Midjourney comparison"),
        ("/categories/design/", "/compare/canva-vs-adobe/", "Canva vs Adobe guide"),
        ("/categories/design/", "/blog/best-ai-image-generators-pakistan/", "best AI image generators guide"),
        ("/products/chatgpt-plus/", "/blog/how-to-pay-for-chatgpt-plus-pakistan/", "how to pay for ChatGPT Plus in Pakistan guide"),
        ("/products/chatgpt-plus/", "/use-cases/ai-tools-for-students/", "AI tools for students playbook"),
        ("/products/chatgpt-plus/", "/pricing/", "PKR pricing catalog"),
        ("/products/capcut-pro/", "/categories/ai-video/", "AI Video editing category"),
        ("/products/capcut-pro/", "/compare/capcut-vs-runway/", "CapCut vs Runway"),
        ("/products/capcut-pro/", "/products/runway-ml-gen-3/", "Runway ML Gen-3"),
        ("/products/capcut-pro/", "/products/veo-3-ultra/", "Veo 3 Ultra"),
        ("/products/leonardo-ai-essential/", "/categories/design/", "Design & AI Image tools category"),
        ("/products/leonardo-ai-essential/", "/compare/leonardo-vs-midjourney/", "Leonardo vs Midjourney guide"),
        ("/compare/capcut-vs-runway/", "/products/capcut-pro/", "CapCut Pro"),
        ("/compare/capcut-vs-runway/", "/products/runway-ml-gen-3/", "Runway ML Gen-3"),
        ("/blog/where-to-buy-ai-tools-pakistan/", "/products/", "complete products catalog"),
        ("/blog/where-to-buy-ai-tools-pakistan/", "/pricing/", "PKR pricing guide"),
        ("/blog/where-to-buy-ai-tools-pakistan/", "/use-cases/ai-tools-for-students/", "AI tools for students"),
        ("/blog/where-to-buy-ai-tools-pakistan/", "/categories/ai-video/", "AI video editing tools"),
        ("/blog/where-to-buy-ai-tools-pakistan/", "/categories/design/", "AI image generator subscriptions"),
        ("/blog/how-to-pay-for-chatgpt-plus-pakistan/", "/products/chatgpt-plus/", "ChatGPT Plus product offer page"),
        ("/blog/how-to-pay-for-chatgpt-plus-pakistan/", "/pricing/", "PKR pricing page"),
        ("/blog/ai-tools-for-pakistani-students-research-thesis/", "/use-cases/ai-tools-for-students/", "AI tools for students hub")
    ]
    
    print("\n=== INDEPENDENT VERIFICATION OF TARGETED CONTEXTUAL LINKS ===")
    pass_count = 0
    fail_count = 0
    for src, dst, txt in checks:
        found = False
        src_outgoing = outgoing.get(src, [])
        for link in src_outgoing:
            # Check target match (either exact or base)
            if link["base_target"] == dst or link["target_resolved"] == dst:
                if txt.lower() in link["text"].lower():
                    found = True
                    break
        if found:
            pass_count += 1
            print(f"[VERIFIED PASS] {src} -> {dst} (Anchor: '{txt}')")
        else:
            fail_count += 1
            print(f"[VERIFIED FAIL] {src} -> {dst} (Anchor: '{txt}' NOT FOUND)")

    print(f"\nVerification Results: {pass_count} passed, {fail_count} failed out of {len(checks)} sampled key links.")
    
    # Key target page incoming links recount
    targets = [
        "/products/", "/pricing/", "/use-cases/ai-tools-for-students/",
        "/categories/ai-video/", "/categories/design/",
        "/products/chatgpt-plus/", "/products/capcut-pro/",
        "/products/leonardo-ai-essential/", "/products/runway-ml-gen-3/",
        "/blog/where-to-buy-ai-tools-pakistan/", "/blog/how-to-pay-for-chatgpt-plus-pakistan/",
        "/blog/ai-tools-for-pakistani-students-research-thesis/",
        "/blog/best-ai-video-generators-pakistan/", "/blog/best-ai-image-generators-pakistan/"
    ]
    print("\n=== RECALCULATED INCOMING LINK COUNTS FOR HIGH-VALUE TARGETS ===")
    results = {}
    for t in targets:
        inc_count = len(incoming.get(t, []))
        out_count = len(outgoing.get(t, []))
        results[t] = {"incoming": inc_count, "outgoing": out_count}
        print(f"{t:55}: {inc_count:3d} in, {out_count:3d} out")
        
    return {
        "total_links": total_links,
        "broken_links": len(broken_links),
        "non_canonical": len(non_canonical_links),
        "checks_passed": pass_count,
        "checks_failed": fail_count,
        "targets": results
    }

if __name__ == "__main__":
    audit_all()
