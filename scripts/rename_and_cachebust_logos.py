"""
rename_and_cachebust_logos.py
Permanently resolves Cloudflare and client-side browser disk cache sticking issues by:
1. Renaming all 32 product logos to cache-busted unique filenames: assets/products/<id>-brand.<ext>
2. Updating assets/product-logo-sources.json with the new canonical paths and byte sizes.
3. Updating _headers to prevent aggressive 7-day edge caching on product logos.
"""

import os
import json
import shutil

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
SOURCES_JSON = os.path.join(REPO_DIR, "assets", "product-logo-sources.json")
HEADERS_FILE = os.path.join(REPO_DIR, "_headers")

def main():
    with open(SOURCES_JSON, "r", encoding="utf-8") as f:
        registry = json.load(f)

    renamed = []
    for pid, meta in registry.items():
        old_rel_path = meta["path"]
        old_abs_path = os.path.join(REPO_DIR, old_rel_path)
        
        # Determine extension
        ext = old_rel_path.split(".")[-1]
        new_filename = f"{pid}-brand.{ext}"
        new_rel_path = f"assets/products/{new_filename}"
        new_abs_path = os.path.join(REPO_DIR, new_rel_path)

        if not os.path.exists(old_abs_path):
            print(f"ERROR: Old path does not exist: {old_abs_path}")
            continue

        # Copy to new cache-busted path
        shutil.copy2(old_abs_path, new_abs_path)
        new_bytes = os.path.getsize(new_abs_path)

        # Update registry
        meta["path"] = new_rel_path
        meta["bytes"] = new_bytes
        renamed.append((pid, new_rel_path, new_bytes))
        print(f"Renamed logo for '{pid}' -> {new_rel_path} ({new_bytes} B)")

    with open(SOURCES_JSON, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    # Update _headers to control cache for /assets/products/*
    with open(HEADERS_FILE, "r", encoding="utf-8") as f:
        headers_content = f.read()

    products_cache_rule = "\n/assets/products/*\n  Cache-Control: public, max-age=3600, must-revalidate\n"
    if "/assets/products/*" not in headers_content:
        # Insert before /assets/*
        headers_content = headers_content.replace("/assets/*", "/assets/products/*\n  Cache-Control: public, max-age=3600, must-revalidate\n\n/assets/*")
        with open(HEADERS_FILE, "w", encoding="utf-8") as f:
            f.write(headers_content)
        print("Updated _headers with /assets/products/* cache-revalidation rule.")

    print(f"\nSuccessfully migrated and cache-busted {len(renamed)} / {len(registry)} logos.")

if __name__ == "__main__":
    main()
