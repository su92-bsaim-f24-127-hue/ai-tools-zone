#!/usr/bin/env python3
"""
Test Suite: Group A Staged Product Robots Meta Directive Verification
AI Tools Zone - Phase 4.1.2 Regression Test
"""

import sys
from pathlib import Path
from bs4 import BeautifulSoup

GROUP_A_SLUGS = [
    "bolt-new-pro",
    "claude-pro",
    "coursera-plus-premium",
    "cursor-ai-pro",
    "deepseek-unlimited",
    "descript-creator",
    "github-copilot",
    "grammarly-premium",
    "microsoft-office-365",
    "perplexity-pro",
    "quillbot-premium",
    "runway-ml-gen-3"
]

def run_tests():
    repo_root = Path(__file__).resolve().parent.parent
    staging_dir = repo_root / "staging" / "catalog-expansion" / "products"
    sitemap_xml = repo_root / "sitemap.xml"
    
    print("VERIFYING GROUP A STAGED ROBOTS DIRECTIVES:")
    print("=" * 60)
    errors = []
    
    # 1. Verify robots tag on every Group A HTML page
    for slug in GROUP_A_SLUGS:
        f = staging_dir / slug / "index.html"
        if not f.exists():
            errors.append(f"Missing staged file: {f}")
            print(f"[FAIL] Missing {slug}")
            continue
        soup = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
        head = soup.find("head")
        if not head:
            errors.append(f"No <head> tag in {slug}")
            print(f"[FAIL] No head in {slug}")
            continue
        robots = head.find("meta", attrs={"name": "robots"})
        if not robots or "noindex" not in robots.get("content", "").lower():
            errors.append(f"Missing or invalid robots directive in {slug}: {robots}")
            print(f"[FAIL] {slug}: {robots}")
        else:
            print(f"[PASS] {slug}: {robots.get('content')}")
            
    # 2. Verify complete absence from root sitemap.xml
    sitemap_text = sitemap_xml.read_text(encoding="utf-8")
    for slug in GROUP_A_SLUGS:
        if f"/products/{slug}/" in sitemap_text:
            errors.append(f"Group A slug {slug} leaked into root sitemap.xml!")
            print(f"[FAIL] {slug} found in root sitemap.xml")
            
    print("=" * 60)
    if errors:
        print(f"FAILED: {len(errors)} assertions failed.")
        for e in errors:
            print(" -", e)
        return 1
    else:
        print(f"ALL {len(GROUP_A_SLUGS)} GROUP A STAGED PAGES CARRY VERIFIED NOINDEX (0 errors).")
        print("ZERO GROUP A URLS IN ROOT SITEMAP.XML.")
        return 0

if __name__ == "__main__":
    sys.exit(run_tests())
