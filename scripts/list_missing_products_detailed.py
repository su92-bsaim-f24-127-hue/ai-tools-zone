import csv
import json
import re

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
COMP_FILE = rf"{REPO_DIR}\competitor-research\tri_competitor_product_and_price_matrix.csv"

missing_products = []

with open(COMP_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        atz_price = r["AI Tools Zone Price (PKR)"].strip()
        name = r["Product Name"].strip()
        if atz_price == "N/A" or not atz_price:
            missing_products.append(r)

print(f"Total missing products from AI Tools Zone: {len(missing_products)}")
for p in missing_products[:25]:
    print(f"- {p['Product Name']} | Cat: {p['Category']} | Gems: {p['AIToolGems Price (PKR)']} | Pak: {p['AIToolsPak Price (PKR)']} | DT: {p['DigitalTools Price (PKR)']}")
