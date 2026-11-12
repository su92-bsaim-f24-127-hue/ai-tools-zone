import csv

with open('competitor-research/phase-3.1.4/97_independently_recalculated_financial_model.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        print(f"{r['Product ID']:25} | {r['Product Name']:25} | PKR {r['Proposed Retail Price PKR']:>8} | {r['Commercial Approval Status']}")
