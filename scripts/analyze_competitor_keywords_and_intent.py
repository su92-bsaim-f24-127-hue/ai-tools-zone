"""
analyze_competitor_keywords_and_intent.py
Analyzes high-converting buyer-intent keywords across competitors,
ranking them by Buyer Intent Score and Pakistani search behavior.
"""

import os
import csv
import json
from collections import defaultdict

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
KEYWORD_MAP_PATH = os.path.join(REPO_DIR, "seo-growth-2026", "23_buyer_intent_keyword_map.csv")
COMPETITOR_CSV = os.path.join(REPO_DIR, "competitor-research", "tri_competitor_product_and_price_matrix.csv")

keywords_by_intent = defaultdict(list)
keywords_by_product = defaultdict(list)

with open(KEYWORD_MAP_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        intent = r["Search Intent Category"]
        score = int(r["Buyer Intent Score (0-100)"])
        prod = r["Product Name"]
        keywords_by_intent[intent].append(r)
        keywords_by_product[prod].append(r)

print(f"Total Keywords Analyzed: {sum(len(v) for v in keywords_by_intent.values())}")
for intent, kw_list in sorted(keywords_by_intent.items(), key=lambda x: len(x[1]), reverse=True):
    top_score = max(int(k["Buyer Intent Score (0-100)"]) for k in kw_list)
    print(f"- {intent}: {len(kw_list)} keywords (Top Score: {top_score})")

# Top 25 Highest Converting Buyer Intent Keywords in Pakistan
all_keywords = []
with open(KEYWORD_MAP_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        all_keywords.append(r)

top_buyer_keywords = sorted(all_keywords, key=lambda x: int(x["Buyer Intent Score (0-100)"]), reverse=True)[:30]

print("\n--- TOP 30 HIGHEST BUYING-INTENT KEYWORDS IN PAKISTAN ---")
for i, kw in enumerate(top_buyer_keywords, 1):
    print(f"{i}. [{kw['Buyer Intent Score (0-100)']}] {kw['Keyword']} | Prod: {kw['Product Name']} | Local Signal: {kw['Local Payment Signal']}")
