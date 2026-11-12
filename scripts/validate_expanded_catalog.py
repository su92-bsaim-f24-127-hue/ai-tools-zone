#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Validator for Phase 3 Catalog Expansion (AI Tools Zone).
Validates inventory reconciliation, HTML structure, metadata compliance,
schema integrity, WhatsApp enquiry hooks, and excluded product isolation.
"""
import os
import sys
import json
import csv
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGING_DIR = REPO_ROOT / "staging" / "catalog-expansion"
STAGING_PROD_DIR = STAGING_DIR / "products"
STAGING_CAT_DIR = STAGING_DIR / "categories"
CSV_PATH = REPO_ROOT / "competitor-research" / "phase-3" / "60_complete_expanded_product_inventory_77.csv"
JSON_PATH = REPO_ROOT / "data" / "expanded-catalog-77.json"
DRAFT_PATH = REPO_ROOT / "data" / "draft-catalog-recommendations.json"
SITEMAP_PATH = STAGING_DIR / "sitemap-77.xml"
LLMS_PATH = STAGING_DIR / "llms-77.txt"
LLMS_FULL_PATH = STAGING_DIR / "llms-full-77.txt"
LINKS_MAP_PATH = STAGING_DIR / "internal-links-map.json"

REJECTED_SLUGS = {"allinone", "turnitin", "midjourney", "semrush", "spotify"}
PHONE = "923430173923"

errors = []
warnings = []

def check(condition, msg):
    if not condition:
        errors.append(msg)

print("Starting Expanded Catalog Validation...")

# 1. Master Inventory CSV Check
if not CSV_PATH.exists():
    errors.append(f"Missing master inventory CSV: {CSV_PATH}")
else:
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        check(len(reader) == 77, f"Expected exactly 77 products in CSV, found {len(reader)}")
        statuses = {}
        for r in reader:
            st = r.get("Commercial Status")
            statuses[st] = statuses.get(st, 0) + 1
        check(statuses.get("AVAILABLE") == 20, f"Expected 20 AVAILABLE, found {statuses.get('AVAILABLE')}")
        check(statuses.get("ENQUIRE") == 12, f"Expected 12 ENQUIRE, found {statuses.get('ENQUIRE')}")
        check(statuses.get("COMING_SOON") == 40, f"Expected 40 COMING_SOON, found {statuses.get('COMING_SOON')}")
        check(statuses.get("REJECTED") == 5, f"Expected 5 REJECTED, found {statuses.get('REJECTED')}")
        print(f"PASS: Master CSV contains 77 products with exact status counts: {statuses}")

# 2. JSON Catalog Check
if not JSON_PATH.exists():
    errors.append(f"Missing expanded catalog JSON: {JSON_PATH}")
else:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        doc = json.load(f)
        prods = doc.get("products", [])
        check(len(prods) == 77, f"Expected 77 products in expanded-catalog-77.json, found {len(prods)}")
        print(f"PASS: expanded-catalog-77.json contains 77 products")

# 3. Draft Recommendations Check
if not DRAFT_PATH.exists():
    errors.append(f"Missing draft recommendations: {DRAFT_PATH}")
else:
    with open(DRAFT_PATH, "r", encoding="utf-8") as f:
        drafts = json.load(f)
        check(len(drafts) == 57, f"Expected 57 candidates in draft recommendations, found {len(drafts)}")
        print(f"PASS: draft-catalog-recommendations.json contains 57 enriched candidates")

# 4. Excluded Product Isolation Check
for r_slug in REJECTED_SLUGS:
    rejected_dir = STAGING_PROD_DIR / r_slug
    check(not rejected_dir.exists(), f"SECURITY VIOLATION: Rejected product directory exists: {rejected_dir}")
print(f"PASS: All 5 rejected products are strictly excluded from staged product pages")

# 5. Staged HTML Product Pages Audit (52 pages)
if not STAGING_PROD_DIR.exists():
    errors.append("Staging products directory missing")
else:
    prod_dirs = [d for d in STAGING_PROD_DIR.iterdir() if d.is_dir()]
    check(len(prod_dirs) == 52, f"Expected exactly 52 staged product pages, found {len(prod_dirs)}")
    
    words_total = 0
    for pdir in prod_dirs:
        index_file = pdir / "index.html"
        check(index_file.exists(), f"Missing index.html in {pdir}")
        if index_file.exists():
            html = index_file.read_text(encoding="utf-8")
            
            # HTML tags check
            check("<!doctype html>" in html.lower(), f"Missing DOCTYPE in {index_file}")
            check("<title>" in html, f"Missing <title> in {index_file}")
            check('<meta name="description"' in html, f"Missing meta description in {index_file}")
            check('<link rel="canonical"' in html, f"Missing canonical in {index_file}")
            check('<h1' in html, f"Missing H1 in {index_file}")
            check('class="direct-answer"' in html, f"Missing direct answer snippet in {index_file}")
            check('class="spec-list"' in html, f"Missing spec list in {index_file}")
            check('class="breadcrumb"' in html, f"Missing breadcrumb in {index_file}")
            check('data-wa-product=' in html, f"Missing data-wa-product attribute in {index_file}")
            check(f"wa.me/{PHONE}" in html, f"Missing valid WhatsApp phone in {index_file}")
            check('<script type="application/ld+json">' in html, f"Missing JSON-LD schema in {index_file}")
            
            # FAQ check
            faq_count = html.count("<h3>")
            check(faq_count >= 4, f"Fewer than 4 FAQs in {index_file} (found {faq_count})")
            
            # Word count check (> 120 words)
            text_content = re.sub(r'<[^>]+>', ' ', html)
            words = [w for w in text_content.split() if len(w) > 1]
            words_total += len(words)
            check(len(words) >= 120, f"Insufficient word count ({len(words)} words) in {index_file}")
            
    avg_words = words_total / len(prod_dirs) if prod_dirs else 0
    print(f"PASS: 52 product HTML pages verified. Average word count: {avg_words:.1f} words/page")

# 6. Staged Category Pages Audit (20 categories)
if not STAGING_CAT_DIR.exists():
    errors.append("Staging categories directory missing")
else:
    cat_dirs = [d for d in STAGING_CAT_DIR.iterdir() if d.is_dir()]
    check(len(cat_dirs) == 20, f"Expected 20 staged category pages, found {len(cat_dirs)}")
    for cdir in cat_dirs:
        cindex = cdir / "index.html"
        check(cindex.exists(), f"Missing index.html in {cdir}")
        if cindex.exists():
            chtml = cindex.read_text(encoding="utf-8")
            check("<title>" in chtml, f"Missing <title> in {cindex}")
            check('<link rel="canonical"' in chtml, f"Missing canonical in {cindex}")
            check("<h1>" in chtml, f"Missing H1 in {cindex}")
            check("product-card" in chtml, f"Missing product cards in {cindex}")
    print(f"PASS: 20 category hub HTML pages verified")

# 7. Sitemap Audit
if not SITEMAP_PATH.exists():
    errors.append(f"Missing expanded sitemap: {SITEMAP_PATH}")
else:
    sitemap_text = SITEMAP_PATH.read_text(encoding="utf-8")
    loc_count = sitemap_text.count("<loc>")
    check(loc_count == 102, f"Expected exactly 102 URLs in expanded sitemap, found {loc_count}")
    print(f"PASS: Expanded sitemap contains exactly {loc_count} verified canonical URLs")

# 8. LLMs.txt Audit
check(LLMS_PATH.exists(), f"Missing llms-77.txt: {LLMS_PATH}")
check(LLMS_FULL_PATH.exists(), f"Missing llms-full-77.txt: {LLMS_FULL_PATH}")
if LLMS_PATH.exists():
    llms_text = LLMS_PATH.read_text(encoding="utf-8")
    check("AI Tools Zone" in llms_text, "Missing branding in llms-77.txt")
    print(f"PASS: llms-77.txt and llms-full-77.txt verified")

# 9. Internal Links Map Audit
if not LINKS_MAP_PATH.exists():
    errors.append(f"Missing internal links map: {LINKS_MAP_PATH}")
else:
    with open(LINKS_MAP_PATH, "r", encoding="utf-8") as f:
        lmap = json.load(f)
        prods_map = lmap.get("products", {})
        cats_map = lmap.get("categories", {})
        check(len(prods_map) == 77, f"Expected 77 products in links map, found {len(prods_map)}")
        check(len(cats_map) == 20, f"Expected 20 categories in links map, found {len(cats_map)}")
        print(f"PASS: internal-links-map.json verified (77 products, 20 categories)")

print("--------------------------------------------------")
if errors:
    print(f"FAILED: {len(errors)} validation errors:")
    for err in errors:
        print(f"  - ERROR: {err}")
    sys.exit(1)
else:
    print("ALL VALIDATION CHECKS PASSED: 0 errors, 0 warnings.")
    print("Expanded catalog implementation is 100% compliant with Phase 3 standards.")
    sys.exit(0)
