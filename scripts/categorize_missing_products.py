import csv
import json
import re
from collections import defaultdict

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
COMP_FILE = rf"{REPO_DIR}\competitor-research\tri_competitor_product_and_price_matrix.csv"

# Load live catalog products
with open(rf"{REPO_DIR}\data\catalog.json", "r", encoding="utf-8") as f:
    live_cat = json.load(f)

live_names = {p["name"].lower().strip() for p in live_cat}
live_ids = {p["id"].lower().strip() for p in live_cat}

missing_by_cat = defaultdict(list)

# Common name normalization map
def clean_product_name(raw_name):
    name = raw_name.strip()
    name = re.sub(r"^(Buy|Get|Official)\s+", "", name, flags=re.I)
    name = re.sub(r"\s+(in Pakistan|Price in Pakistan|Official Subscription|Subscription).*$", "", name, flags=re.I)
    name = re.sub(r"\s*\(.*?\)", "", name)
    name = re.sub(r"\s*–.*$", "", name)
    name = re.sub(r"\s*\|.*$", "", name)
    return name.strip()

with open(COMP_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        atz = r["AI Tools Zone Price (PKR)"].strip()
        if atz == "N/A" or not atz:
            raw_name = r["Product Name"]
            cleaned = clean_product_name(raw_name)
            
            # Check if it's really missing
            if cleaned.lower() in live_names or cleaned.lower() in live_ids:
                continue
            if any(l in cleaned.lower() for l in ["chatgpt plus", "canva pro edu", "capcut pro", "gemini pro", "leonardo ai", "elevenlabs", "figma pro", "adobe creative", "lovable pro", "gamma pro", "replit core", "n8n starter", "notion business", "nordvpn", "surfshark", "youtube premium", "netflix premium", "linkedin premium", "windows 11 pro", "veo 3"]):
                continue

            # Categorize
            cat = r["Category"]
            price_gems = r["AIToolGems Price (PKR)"]
            price_pak = r["AIToolsPak Price (PKR)"]
            price_dt = r["DigitalTools Price (PKR)"]
            
            # Pick best available price
            prices = [p for p in [price_gems, price_pak, price_dt] if p != "N/A" and p]
            display_price = f"PKR {prices[0]}" if prices else "Contact via WhatsApp"
            
            missing_by_cat[cat].append({
                "name": cleaned,
                "raw_name": raw_name,
                "category": cat,
                "price": display_price,
                "gems_price": price_gems,
                "pak_price": price_pak,
                "dt_price": price_dt
            })

# Deduplicate within category by cleaned name
deduped_missing = {}
for cat, items in missing_by_cat.items():
    seen = {}
    for item in items:
        k = item["name"].lower()
        if k not in seen:
            seen[k] = item
    deduped_missing[cat] = list(seen.values())

total_count = sum(len(v) for v in deduped_missing.values())
print(f"Total Unique Missing Products: {total_count}")
for cat, items in sorted(deduped_missing.items()):
    print(f"\n### {cat} ({len(items)} Products):")
    for it in sorted(items, key=lambda x: x["name"]):
        print(f"  - {it['name']} | Best Competitor Price: {it['price']}")
