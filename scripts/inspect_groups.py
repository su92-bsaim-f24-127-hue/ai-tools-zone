from pathlib import Path

staging_dir = Path('staging/catalog-expansion/products')

# Group C slugs
group_c_slugs = ['chatprd-ai', 'enterprise-ai-api-credits', 'windsurf-editor']

# Group D rejected products
group_d_slugs = [
    'chatgpt-team-shared', 'envato-elements-shared',
    'netflix-screens-pakistan', 'canva-pro-lifetime',
    'capcut-pro-shared'
]

# Check Group D: should NOT exist anywhere in staging
for slug in group_d_slugs:
    p1 = staging_dir / slug
    p2 = staging_dir / f'{slug}.html'
    if p1.exists() or p2.exists():
        print(f'CRITICAL ERROR: Group D product {slug} exists in staging!')
    else:
        print(f'PASS: Group D {slug} is strictly absent from staging.')

# Check all staged products
all_staged = [p.name for p in staging_dir.iterdir()]
print(f'Total staged product items: {len(all_staged)}')

group_a_slugs = [
    'claude-pro', 'cursor-ai-pro', 'microsoft-office-365', 'grammarly-premium',
    'perplexity-pro', 'github-copilot', 'quillbot-premium', 'coursera-plus-premium',
    'runway-ml-gen-3', 'deepseek-unlimited', 'bolt-new-pro', 'descript-creator'
]

group_b_and_c = [s for s in all_staged if s not in group_a_slugs]
print(f'Total Group B & C items: {len(group_b_and_c)}')

noindex_count = 0
for item in group_b_and_c:
    p = staging_dir / item
    if p.is_dir():
        html_file = p / 'index.html'
    else:
        html_file = p
    
    html = html_file.read_text(encoding='utf-8')
    if 'noindex' in html:
        noindex_count += 1
    else:
        print(f'WARNING: {item} does not have noindex!')

print(f'noindex verified on {noindex_count} / {len(group_b_and_c)} Group B & C items.')
