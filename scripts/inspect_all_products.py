import json

with open(r'C:\Users\ELITEBOOK\projects\ai-tools-zone\data\catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

print(f"=== PRODUCTION CATALOG ({len(cat)} Products) ===")
for i, p in enumerate(cat, 1):
    print(f"{i}. {p.get('name')} ({p.get('id')}) | PKR {p.get('price')} | {p.get('duration')} | {p.get('category')} | {p.get('access_type')}")

with open(r'C:\Users\ELITEBOOK\projects\ai-tools-zone\data\product-content.json', 'r', encoding='utf-8') as f:
    pc = json.load(f)

print(f"\n=== PRODUCT CONTENT JSON ({len(pc)} Items) ===")
for slug, data in pc.items():
    print(f"- {slug} | Status: {data.get('status', 'active')} | Indexable: {data.get('is_indexable', True)}")
