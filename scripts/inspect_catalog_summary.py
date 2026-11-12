import json
from pathlib import Path

catalog = json.loads(Path('data/catalog.json').read_text(encoding='utf-8'))
for p in catalog:
    print(f"{p['id']:12} | {p['name']:26} | {p['price']:5} PKR | {p['duration']:20} | {p['access']:12}")
