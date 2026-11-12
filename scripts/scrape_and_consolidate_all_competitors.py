"""
scrape_and_consolidate_all_competitors.py
Fetches, cleans, and consolidates live product data and buyer-intent keywords
from aitoolgems.tech, aitoolspak.tech, and digitaltools.com.pk.
"""

import os
import csv
import json
import re
import urllib.request
import ssl
from bs4 import BeautifulSoup

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
COMPETITOR_DIR = os.path.join(REPO_DIR, "competitor-research")
os.makedirs(COMPETITOR_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

print("1. Scraping digitaltools.com.pk live...")
html_dt = fetch_html("https://digitaltools.com.pk/")
soup_dt = BeautifulSoup(html_dt, "html.parser")
dt_products = []

for li in soup_dt.find_all("li", class_=re.compile(r"type-product")):
    title_el = li.find(["h2", "h3", "a", "span"], class_=re.compile(r"woocommerce-loop-product__title|title", re.I))
    price_el = li.find(class_=re.compile(r"price", re.I))
    link_el = li.find("a", href=True)
    
    if title_el and price_el:
        raw_name = title_el.get_text(strip=True)
        raw_price = price_el.get_text(separator=" ", strip=True)
        link = link_el["href"] if link_el else ""
        
        # Clean price (look for Current price is: ₨ X or ₨X)
        current_price_match = re.search(r"Current price is:\s*₨\s*([\d,]+)", raw_price)
        if current_price_match:
            price = current_price_match.group(1).replace(",", "")
        else:
            m = re.findall(r"₨\s*([\d,]+)", raw_price)
            price = m[-1].replace(",", "") if m else ""
            
        # Clean product name
        cleaned_name = re.sub(r"\|.*$", "", raw_name)
        cleaned_name = re.sub(r"–.*$", "", cleaned_name)
        cleaned_name = re.sub(r"Subscription in Pakistan.*$", "", cleaned_name, flags=re.I)
        cleaned_name = re.sub(r"Subscription Price in Pakistan.*$", "", cleaned_name, flags=re.I)
        cleaned_name = cleaned_name.strip()
        
        if cleaned_name and price and cleaned_name not in [x["name"] for x in dt_products]:
            dt_products.append({
                "name": cleaned_name,
                "raw_title": raw_name,
                "price": price,
                "link": link,
                "source": "digitaltools.com.pk"
            })

print(f"Extracted {len(dt_products)} products from digitaltools.com.pk")

# Save digitaltools inventory
dt_csv_path = os.path.join(COMPETITOR_DIR, "digitaltools_complete_inventory.csv")
with open(dt_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Product Name", "Cleaned Title", "Price (PKR)", "Product URL", "Competitor Website"])
    for p in dt_products:
        writer.writerow([p["name"], p["raw_title"], p["price"], p["link"], p["source"]])

print("Saved digitaltools_complete_inventory.csv")

# 2. Read aitoolgems & aitoolspak existing master inventories
gems_csv_path = os.path.join(COMPETITOR_DIR, "aitoolgems_complete_inventory.csv")
pak_csv_path = os.path.join(COMPETITOR_DIR, "aitoolspak_complete_inventory.csv")

gems_items = []
if os.path.exists(gems_csv_path):
    with open(gems_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            gems_items.append(r)

pak_items = []
if os.path.exists(pak_csv_path):
    with open(pak_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            pak_items.append(r)

print(f"Loaded {len(gems_items)} aitoolgems products, {len(pak_items)} aitoolspak products.")

# 3. Create a master 3-way competitor comparison table
master_comparison = {}

for g in gems_items:
    name = g["Product Name"].strip()
    norm = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
    master_comparison[norm] = {
        "canonical_name": name,
        "category": g.get("Category", ""),
        "aitoolgems_price": g.get("Price", ""),
        "aitoolgems_duration": g.get("Duration", ""),
        "aitoolgems_access": g.get("Account Type", ""),
        "aitoolspak_price": "N/A",
        "aitoolspak_duration": "N/A",
        "aitoolspak_access": "N/A",
        "digitaltools_price": "N/A",
        "digitaltools_duration": "N/A",
        "aitoolszone_price": "N/A"
    }

for p in pak_items:
    name = p["Product Name"].strip()
    norm = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
    if norm not in master_comparison:
        master_comparison[norm] = {
            "canonical_name": name,
            "category": p.get("Category", ""),
            "aitoolgems_price": "N/A",
            "aitoolgems_duration": "N/A",
            "aitoolgems_access": "N/A",
            "aitoolspak_price": p.get("Price", ""),
            "aitoolspak_duration": p.get("Duration", ""),
            "aitoolspak_access": p.get("Account Type", ""),
            "digitaltools_price": "N/A",
            "digitaltools_duration": "N/A",
            "aitoolszone_price": "N/A"
        }
    else:
        master_comparison[norm]["aitoolspak_price"] = p.get("Price", "")
        master_comparison[norm]["aitoolspak_duration"] = p.get("Duration", "")
        master_comparison[norm]["aitoolspak_access"] = p.get("Account Type", "")

for d in dt_products:
    name = d["name"].strip()
    norm = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
    matched = False
    for k in master_comparison:
        if k in norm or norm in k:
            master_comparison[k]["digitaltools_price"] = d["price"]
            matched = True
            break
    if not matched:
        master_comparison[norm] = {
            "canonical_name": name,
            "category": "Digital Tools",
            "aitoolgems_price": "N/A",
            "aitoolgems_duration": "N/A",
            "aitoolgems_access": "N/A",
            "aitoolspak_price": "N/A",
            "aitoolspak_duration": "N/A",
            "aitoolspak_access": "N/A",
            "digitaltools_price": d["price"],
            "digitaltools_duration": "Monthly/Yearly",
            "aitoolszone_price": "N/A"
        }

# Match AI Tools Zone prices
with open(os.path.join(REPO_DIR, "data", "catalog.json"), "r", encoding="utf-8") as f:
    atz_cat = json.load(f)

for p in atz_cat:
    name = p["name"].strip()
    norm = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
    for k in master_comparison:
        if k in norm or norm in k:
            master_comparison[k]["aitoolszone_price"] = str(p["price"])
            break

print(f"Consolidated multi-competitor comparison with {len(master_comparison)} unique products.")

# Save master 3-way competitor comparison CSV
comp_csv_path = os.path.join(COMPETITOR_DIR, "tri_competitor_product_and_price_matrix.csv")
with open(comp_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Product Name", "Category", "AI Tools Zone Price (PKR)",
        "AIToolGems Price (PKR)", "AIToolsPak Price (PKR)", "DigitalTools Price (PKR)",
        "AIToolGems Duration", "AIToolGems Access"
    ])
    for item in sorted(master_comparison.values(), key=lambda x: x["canonical_name"]):
        writer.writerow([
            item["canonical_name"],
            item["category"],
            item["aitoolszone_price"],
            item["aitoolgems_price"],
            item["aitoolspak_price"],
            item["digitaltools_price"],
            item["aitoolgems_duration"],
            item["aitoolgems_access"]
        ])

print("Saved tri_competitor_product_and_price_matrix.csv")
