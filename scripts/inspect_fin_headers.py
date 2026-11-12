import csv

with open('competitor-research/phase-3.1.4/97_independently_recalculated_financial_model.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print("HEADERS:")
    for idx, h in enumerate(headers):
        print(f"  {idx}: {h}")
    row1 = next(reader)
    print("\nROW 1:")
    for h, v in zip(headers, row1):
        print(f"  {h}: {v}")
