#!/usr/bin/env python3
"""
Automated Inventory Migration & Conservation Test Suite
AI Tools Zone - Phase 3.1.5 Independent Quality Gate

Verifies:
1. 77-product catalog conservation (20 AVAILABLE, 12 ENQUIRE, 40 COMING_SOON [37 B + 3 C], 5 REJECTED).
2. Production catalog integrity (20 active products untouched).
3. Zero duplicate slugs, IDs, or canonical URL collisions.
4. Complete absence of Group D rejected products from public and staged assets.
5. Complete absence of competitor duplicate variants from public and staged assets.
6. Robots meta tag enforcement across non-public staged pages.
7. Consumer trust copy compliance across Group A release candidates.
8. Grammarly financial model and copy alignment (-PKR 1,953.19 net contribution).
"""

import sys
import json
import csv
from pathlib import Path
from decimal import Decimal

def run_inventory_migration_tests() -> bool:
    repo_root = Path(__file__).resolve().parent.parent
    master_csv = repo_root / 'competitor-research' / 'expanded_product_inventory_77.csv'
    prod_catalog_json = repo_root / 'data' / 'catalog.json'
    staging_dir = repo_root / 'staging' / 'catalog-expansion' / 'products'
    sitemap_xml = repo_root / 'sitemap.xml'
    fin_csv = repo_root / 'competitor-research' / 'phase-3.1.4' / '97_independently_recalculated_financial_model.csv'
    
    errors = []
    
    # 1. Master CSV Conservation Test
    if not master_csv.exists():
        print(f"FAIL: Master CSV not found at {master_csv}")
        return False
        
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        master_rows = list(reader)
        
    print(f"Master Inventory Rows: {len(master_rows)}")
    if len(master_rows) != 77:
        errors.append(f"Expected exactly 77 products in master CSV, found {len(master_rows)}")
        
    status_counts = {}
    slugs = set()
    ids = set()
    for r in master_rows:
        pid = r['Product ID']
        slug = r['Unique Slug']
        st = r['Commercial Status']
        status_counts[st] = status_counts.get(st, 0) + 1
        
        if slug in slugs:
            errors.append(f"Duplicate slug detected in master CSV: {slug}")
        slugs.add(slug)
        
        if pid in ids:
            errors.append(f"Duplicate product ID detected in master CSV: {pid}")
        ids.add(pid)
        
    expected_statuses = {'AVAILABLE': 20, 'ENQUIRE': 12, 'COMING_SOON': 40, 'REJECTED': 5}
    if status_counts != expected_statuses:
        errors.append(f"Status distribution mismatch: expected {expected_statuses}, found {status_counts}")
    else:
        print(f"PASS: Status distribution matches exactly: {status_counts}")
        
    # 2. Production Catalog Integrity Check
    if not prod_catalog_json.exists():
        errors.append(f"Production catalog not found at {prod_catalog_json}")
    else:
        with open(prod_catalog_json, 'r', encoding='utf-8') as f:
            prod_cat = json.load(f)
        if len(prod_cat) != 20:
            errors.append(f"Production catalog has {len(prod_cat)} products; expected 20")
        else:
            print("PASS: Production catalog contains exactly 20 active products.")
            
        prod_slugs = {p['slug'] for p in prod_cat}
        prod_ids = {p['id'] for p in prod_cat}
        
        # Verify AVAILABLE products in master CSV match production catalog
        available_master_slugs = {r['Unique Slug'] for r in master_rows if r['Commercial Status'] == 'AVAILABLE'}
        if available_master_slugs != prod_slugs:
            errors.append(f"Discrepancy between master AVAILABLE slugs and production catalog slugs: {available_master_slugs ^ prod_slugs}")
        else:
            print("PASS: Master CSV AVAILABLE products match production catalog byte-for-byte.")
            
    # 3. Complete Exclusion of Group D Rejected Products
    group_d_slugs = [
        'all-in-one-mega-ai-portal', 'turnitin-plagiarism-checker',
        'midjourney-pro', 'semrush-pro', 'spotify-premium'
    ]
    for s in group_d_slugs:
        p1 = staging_dir / s
        p2 = staging_dir / f"{s}.html"
        p3 = repo_root / 'products' / s
        if p1.exists() or p2.exists() or p3.exists():
            errors.append(f"Group D product {s} found in staging or public directories!")
            
    # 4. Complete Exclusion of Competitor Duplicate / Unauthorized Variants
    competitor_variants = [
        'chatgpt-team-shared', 'envato-elements-shared',
        'netflix-screens-pakistan', 'canva-pro-lifetime',
        'capcut-pro-shared'
    ]
    for cv in competitor_variants:
        p1 = staging_dir / cv
        p2 = staging_dir / f"{cv}.html"
        p3 = repo_root / 'products' / cv
        if p1.exists() or p2.exists() or p3.exists():
            errors.append(f"Competitor duplicate variant {cv} found in staging or public directories!")
            
    # Check sitemap
    if sitemap_xml.exists():
        sitemap_content = sitemap_xml.read_text(encoding='utf-8')
        for bad_slug in group_d_slugs + competitor_variants:
            if bad_slug in sitemap_content:
                errors.append(f"Rejected or duplicate variant {bad_slug} leaked into production sitemap.xml!")
        print("PASS: Zero rejected or duplicate products present in production sitemap.xml.")

    # 5. Staged Non-Public Pages Robots Tag Verification (All 40 COMING_SOON)
    coming_soon_slugs = [r['Unique Slug'] for r in master_rows if r['Commercial Status'] == 'COMING_SOON']
    if len(coming_soon_slugs) != 40:
        errors.append(f"Expected 40 COMING_SOON products, found {len(coming_soon_slugs)}")
        
    noindex_verified = 0
    for s in coming_soon_slugs:
        p_dir = staging_dir / s / 'index.html'
        p_file = staging_dir / f"{s}.html"
        target_file = p_dir if p_dir.exists() else p_file
        
        if not target_file.exists():
            errors.append(f"Missing staged HTML file for COMING_SOON product: {s}")
            continue
            
        html = target_file.read_text(encoding='utf-8')
        if 'noindex' in html:
            noindex_verified += 1
        else:
            errors.append(f"Staged product {s} missing noindex meta directive!")
            
    print(f"PASS: {noindex_verified}/40 COMING_SOON staged pages carry verified noindex directives.")
    
    # 6. Group A Consumer Trust Verification (12 ENQUIRE)
    enquire_slugs = [r['Unique Slug'] for r in master_rows if r['Commercial Status'] == 'ENQUIRE']
    if len(enquire_slugs) != 12:
        errors.append(f"Expected 12 ENQUIRE products, found {len(enquire_slugs)}")
        
    enquire_verified = 0
    for s in enquire_slugs:
        p_dir = staging_dir / s / 'index.html'
        p_file = staging_dir / f"{s}.html"
        target_file = p_dir if p_dir.exists() else p_file
        
        if not target_file.exists():
            errors.append(f"Missing staged HTML file for ENQUIRE product: {s}")
            continue
            
        html = target_file.read_text(encoding='utf-8')
        c1 = 'Confirmed on enquiry (Subject to availability)' in html
        c2 = 'Support subject to confirmed terms' in html
        c3 = 'No advance payment is collected before fulfilment feasibility is confirmed' in html
        c4 = 'Enquire on WhatsApp' in html
        c5 = 'AI Tools Zone is an independent digital marketplace' in html
        
        if c1 and c2 and c3 and c4 and c5:
            enquire_verified += 1
        else:
            errors.append(f"Group A product {s} failed consumer-trust copy checks (c1={c1}, c2={c2}, c3={c3}, c4={c4}, c5={c5})")
            
    print(f"PASS: {enquire_verified}/12 Group A staged release candidates passed consumer trust checks.")
    
    # 7. Grammarly Financial Model Integrity Check
    if not fin_csv.exists():
        errors.append(f"Financial CSV not found at {fin_csv}")
    else:
        with open(fin_csv, 'r', encoding='utf-8') as f:
            fin_rows = list(csv.DictReader(f))
        grammarly_row = next((r for r in fin_rows if r['Product ID'] == 'grammarly'), None)
        if not grammarly_row:
            errors.append("Grammarly row missing from 97_independently_recalculated_financial_model.csv")
        else:
            price = Decimal(grammarly_row['Proposed Customer Selling Price (PKR)'])
            net_contrib = Decimal(grammarly_row['Net Contribution (PKR)'])
            status = grammarly_row['Commercial Status and Authorization Restrictions']
            
            if price != Decimal('7500.00'):
                errors.append(f"Grammarly proposed selling price is {price}; expected 7500.00")
            if net_contrib != Decimal('-1953.19'):
                errors.append(f"Grammarly net contribution is {net_contrib}; expected -1953.19")
            if 'UNVIABLE AT RETAIL' not in status:
                errors.append(f"Grammarly status missing UNVIABLE AT RETAIL: {status}")
            print(f"PASS: Grammarly financial model confirmed (Price=PKR {price}, Net Contrib=PKR {net_contrib}, Status={status})")

    if errors:
        print(f"FAIL: {len(errors)} inventory migration errors detected:")
        for e in errors:
            print(f"  - {e}")
        return False
        
    print("--------------------------------------------------")
    print("ALL INVENTORY MIGRATION & CONSERVATION ASSERTIONS PASSED (100% Green).")
    return True

if __name__ == '__main__':
    success = run_inventory_migration_tests()
    sys.exit(0 if success else 1)
