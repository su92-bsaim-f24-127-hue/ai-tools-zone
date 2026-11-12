import json
import os

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
STATE_PATH = os.path.join(REPO_DIR, "data", "page-state.json")
CATALOG_PATH = os.path.join(REPO_DIR, "data", "catalog.json")
CONTRACT_PATH = os.path.join(REPO_DIR, "data", "seo-contract.json")

with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
    contract = json.load(f)

routes = sorted(list(state.keys()))
product_slugs = {p['id']: p['slug'] for p in catalog}

contract['routes'] = routes
contract['product_slugs'] = product_slugs
contract['reason'] = "Expand production catalog from 20 to 32 products adding Group A high-demand AI developer, video, academic, and productivity tools with full Pakistani buyer-intent optimization."

with open(CONTRACT_PATH, "w", encoding="utf-8") as f:
    json.dump(contract, f, indent=2, ensure_ascii=False)

print(f"Updated seo-contract.json: {len(routes)} routes, {len(product_slugs)} products.")
