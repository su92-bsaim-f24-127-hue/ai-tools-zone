import json
from pathlib import Path

content = json.loads(Path('data/product-content.json').read_text(encoding='utf-8'))

for pid in ['chatgpt', 'canva', 'windows', 'netflix', 'adobe']:
    print(f"=== {pid} ===")
    p = content.get(pid, {})
    print("META:", p.get('meta_description'))
    print("HEADLINE:", p.get('headline'))
    print("OVERVIEW:", p.get('overview_text'))
    print("WHY BUY:", p.get('why_buy_local'))
    faqs = p.get('faqs', [])
    for idx, f in enumerate(faqs):
        print(f"  FAQ {idx+1}: Q: {f.get('q')} | A: {f.get('a')}")
    print()
