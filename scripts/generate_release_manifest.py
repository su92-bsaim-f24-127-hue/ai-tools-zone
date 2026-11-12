import csv
from pathlib import Path

master_csv = 'competitor-research/expanded_product_inventory_77.csv'
out_path = 'competitor-research/phase-3.1.4/103_exact_final_release_manifest.csv'

fieldnames = [
    'Product ID',
    'Product Name',
    'Canonical Slug',
    'Release Group',
    'Catalog Action',
    'Staged File Path',
    'Production Canonical URL',
    'Robots Meta Directive',
    'Sitemap Status',
    'Commercial Authorization Status',
    'Owner Review Eligibility',
    'Release Restrictions & Consumer Trust Safeguards'
]

group_a = {
    'claude', 'cursor', 'office365', 'grammarly',
    'perplexity', 'copilot', 'quillbot', 'coursera-plus',
    'runway', 'deepseek', 'bolt-new', 'descript'
}

group_c = {'chatprd', 'enterprise-api', 'windsurf'}

group_d = {
    'chatgpt-team-shared', 'envato-elements', 'netflix-screens',
    'canva-pro-lifetime', 'capcut-pro'
}

rows = []
with open(master_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        pid = r['Product ID']
        name = r['Product Name']
        slug = r['Unique Slug']
        status = r['Commercial Status']
        
        if status == 'AVAILABLE':
            group = 'Active Production Baseline'
            action = 'NONE (Existing Production Baseline)'
            staged_path = f'products/{slug}/index.html'
            canon_url = f'https://aitoolszone.tech/products/{slug}/'
            robots = 'index, follow'
            sitemap = 'Active in Production Sitemap (83 routes)'
            comm_status = 'AUTHORIZED (Production Active)'
            owner_review = 'ALREADY ACTIVE (Baseline a09b8c4)'
            safeguards = 'Production baseline active; Verified WhatsApp fulfilment; Untouched in Phase 3.1.4'
        elif status == 'REJECTED':
            group = 'Group D (Permanently Excluded)'
            action = 'REJECT (Fraudulent / EULA Breach)'
            staged_path = 'N/A (Strictly Zero Staged Files)'
            canon_url = 'N/A (Excluded)'
            robots = 'N/A (Excluded)'
            sitemap = 'Strictly Excluded from Sitemap'
            comm_status = 'PERMANENTLY PROHIBITED'
            owner_review = 'NOT ELIGIBLE (Zero Tolerance Policy)'
            safeguards = 'Violates vendor terms or copyright; Zero files permitted in repository'
        elif pid in group_a:
            group = 'Group A (Public Release & Index Ready)'
            action = 'ADD (Release Candidate for Owner Approval)'
            staged_path = f'staging/catalog-expansion/products/{slug}/index.html'
            canon_url = f'https://aitoolszone.tech/products/{slug}/'
            robots = 'index, follow'
            sitemap = 'Eligible for production sitemap upon owner release authorization'
            
            if pid == 'claude':
                comm_status = 'NOT AUTHORIZED (PENDING LEGAL/TAX REVIEW)'
            elif pid == 'cursor':
                comm_status = 'NOT AUTHORIZED (PENDING SUPPLIER VERIFICATION)'
            elif pid == 'office365':
                comm_status = 'NOT AUTHORIZED (PENDING PROVIDER AUTHORIZATION)'
            elif pid == 'grammarly':
                comm_status = 'NOT AUTHORIZED (UNVIABLE AT RETAIL)'
            else:
                comm_status = 'NOT AUTHORIZED FOR DIRECT SALE (Enquiry Only / Pending Supplier Clearance)'
                
            owner_review = 'ELIGIBLE FOR OWNER REVIEW (Release Candidate)'
            safeguards = 'Consumer trust copy corrected; Delivery SLA softened; Advance payment disclaimer verified'
        elif pid in group_c:
            group = 'Group C (Staged Architecture Review)'
            action = 'HOLD (Architecture Review Required)'
            staged_path = f'staging/catalog-expansion/products/{slug}/index.html'
            canon_url = f'https://aitoolszone.tech/products/{slug}/'
            robots = 'noindex, follow'
            sitemap = 'Strictly Excluded from Sitemap'
            comm_status = 'NOT AUTHORIZED (Hold Status)'
            owner_review = 'HOLD (Technical Feasibility Review Required)'
            safeguards = 'Carries noindex; Excluded from sitemap; No commercial claims permitted'
        else:
            group = 'Group B (Demand Validation / Pre-Launch Testing)'
            action = 'ADD (Demand Validation Staged)'
            staged_path = f'staging/catalog-expansion/products/{slug}/index.html'
            canon_url = f'https://aitoolszone.tech/products/{slug}/'
            robots = 'noindex, follow'
            sitemap = 'Strictly Excluded from Sitemap'
            comm_status = 'NOT AUTHORIZED (Demand Validation Only)'
            owner_review = 'HOLD (Retain as noindex during Phase 3.1.4)'
            safeguards = 'Carries noindex; Excluded from sitemap; Traffic validation without indexation penalty'
            
        rows.append({
            'Product ID': pid,
            'Product Name': name,
            'Canonical Slug': slug,
            'Release Group': group,
            'Catalog Action': action,
            'Staged File Path': staged_path,
            'Production Canonical URL': canon_url,
            'Robots Meta Directive': robots,
            'Sitemap Status': sitemap,
            'Commercial Authorization Status': comm_status,
            'Owner Review Eligibility': owner_review,
            'Release Restrictions & Consumer Trust Safeguards': safeguards
        })

with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Successfully wrote {len(rows)} products to {out_path}')
