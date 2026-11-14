"""
scripts/diagnose_rendering_issues.py
Diagnoses why markdown links in seo_pages.py categories and pages were not rendered.
"""

import re
from pathlib import Path

REPO_DIR = Path(r"C:\Users\ELITEBOOK\projects\ai-tools-zone")

def inspect_file(rel_path, search_term):
    file_path = REPO_DIR / rel_path
    if not file_path.exists():
        print(f"File not found: {rel_path}")
        return
    text = file_path.read_text(encoding="utf-8")
    matches = [m.start() for m in re.finditer(re.escape(search_term), text, re.IGNORECASE)]
    print(f"\n--- Checking {rel_path} for '{search_term}' ---")
    if matches:
        print(f"Found {len(matches)} occurrences.")
        for idx in matches[:3]:
            start = max(0, idx - 100)
            end = min(len(text), idx + 200)
            snippet = text[start:end].replace("\n", " ")
            print(f"Snippet: ... {snippet} ...")
    else:
        print("Not found.")

def main():
    inspect_file("categories/ai-video/index.html", "capcut-vs-runway")
    inspect_file("categories/ai-video/index.html", "[CapCut Pro]")
    inspect_file("use-cases/ai-tools-for-students/index.html", "[ChatGPT Plus]")
    inspect_file("use-cases/ai-tools-for-students/index.html", "ai-tools-for-pakistani-students-research-thesis")
    inspect_file("categories/design/index.html", "[Leonardo AI Essential]")

if __name__ == "__main__":
    main()
