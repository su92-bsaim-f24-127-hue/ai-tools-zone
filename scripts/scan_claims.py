import json
from pathlib import Path

content = json.loads(Path('data/product-content.json').read_text(encoding='utf-8'))

for pid, p in content.items():
    text = json.dumps(p)
    matches = []
    for w in ['instant', 'guarantee', 'authorized', 'official partner', 'oem', 'genuine']:
        if w in text.lower():
            matches.append(w)
    if matches:
        print(f"[{pid}] matches: {matches}")
