import csv

with open('competitor-research/phase-3.1.4/97_independently_recalculated_financial_model.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        print(f"{r['Product ID']:15} | {r['Product Name']:22} | PKR {r['Proposed Customer Selling Price (PKR)']:>8} | Net: PKR {r['Net Contribution (PKR)']:>8} | {r['Commercial Status and Authorization Restrictions']}")
