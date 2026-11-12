import json

with open(r'C:\Users\ELITEBOOK\projects\ai-tools-zone\data\expanded-catalog-77.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

group_a_slugs = [
    'cursor-ai-pro', 'github-copilot', 'claude-pro', 'deepseek-unlimited',
    'perplexity-pro', 'bolt-new-pro', 'runway-ml-gen-3', 'descript-creator',
    'grammarly-premium', 'quillbot-premium', 'microsoft-office-365', 'coursera-plus-premium'
]

products = [p for p in d['products'] if p['Unique Slug'] in group_a_slugs]
print(f"Found {len(products)} Group A products:")
for p in products:
    print(f"- ID: {p['Product ID']} | Name: {p['Product Name']} | Slug: {p['Unique Slug']} | Cat: {p['Category']} | Price: {p['Price (PKR)']} | Duration: {p['Billing Duration']}")
