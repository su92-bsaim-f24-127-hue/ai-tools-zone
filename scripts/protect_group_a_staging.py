#!/usr/bin/env python3
"""
Protect Group A Staged Product Pages from Search Engine Indexing
AI Tools Zone - Phase 4.1.2 Staging Index Protection
"""

import re
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

def main():
    repo_root = Path(__file__).resolve().parent.parent
    staging_dir = repo_root / "staging" / "catalog-expansion" / "products"
    
    print(f"Applying <meta name=\"robots\" content=\"noindex, nofollow\"/> to {len(GROUP_A_SLUGS)} Group A staged pages...")
    
    verified_count = 0
    for slug in GROUP_A_SLUGS:
        html_file = staging_dir / slug / "index.html"
        if not html_file.exists():
            print(f"ERROR: Missing staged HTML file: {html_file}")
            continue
            
        raw_html = html_file.read_text(encoding="utf-8")
        
        # Replace existing robots tag if present, or insert before </head>
        if re.search(r'<meta\s+[^>]*name=["\']robots["\'][^>]*>', raw_html, re.I):
            new_html = re.sub(
                r'<meta\s+[^>]*name=["\']robots["\'][^>]*>',
                '<meta name="robots" content="noindex, nofollow"/>',
                raw_html,
                flags=re.I
            )
        elif re.search(r'<meta\s+[^>]*content=["\'][^"\']*["\']\s+name=["\']robots["\'][^>]*>', raw_html, re.I):
            new_html = re.sub(
                r'<meta\s+[^>]*content=["\'][^"\']*["\']\s+name=["\']robots["\'][^>]*>',
                '<meta name="robots" content="noindex, nofollow"/>',
                raw_html,
                flags=re.I
            )
        else:
            new_html = raw_html.replace('</head>', '<meta name="robots" content="noindex, nofollow"/>\n</head>')
            
        html_file.write_text(new_html, encoding="utf-8")
        
        # Verify using BeautifulSoup
        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
        head = soup.find("head")
        robots_tag = head.find("meta", attrs={"name": "robots"}) if head else None
        
        if robots_tag and "noindex" in robots_tag.get("content", "").lower():
            verified_count += 1
            print(f"[VERIFIED] {slug}: {robots_tag}")
        else:
            print(f"[FAILED] {slug}: robots tag not verified!")
            
    print("-" * 50)
    print(f"Total Group A pages protected: {verified_count} / {len(GROUP_A_SLUGS)}")
    
    # Also verify all 52 staged products now have noindex
    all_staged = list(staging_dir.glob("*/index.html"))
    total_noindex = 0
    for f in all_staged:
        s = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
        r = s.find("meta", attrs={"name": "robots"})
        if r and "noindex" in r.get("content", "").lower():
            total_noindex += 1
            
    print(f"Total staged products carrying noindex: {total_noindex} / {len(all_staged)}")

if __name__ == "__main__":
    main()
