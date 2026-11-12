import json
from pathlib import Path

content = json.loads(Path('data/product-content.json').read_text(encoding='utf-8'))

def inspect_obj(pid, obj, path=""):
    if isinstance(obj, str):
        for w in ['instant', 'guarantee', 'authorized', 'official partner', 'oem', 'genuine']:
            if w in obj.lower():
                print(f"[{pid}] {path}: ({w}) -> {obj}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            inspect_obj(pid, item, f"{path}[{idx}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            inspect_obj(pid, v, f"{path}.{k}" if path else k)

for pid, p in content.items():
    inspect_obj(pid, p)
