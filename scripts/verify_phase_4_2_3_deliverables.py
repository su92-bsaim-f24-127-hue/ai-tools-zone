import os
import csv
from pathlib import Path

p = Path("seo-growth-2026/phase-4.2.3")
print(f"Checking deliverables in {p}:")
for f in sorted(p.glob("*")):
    content = f.read_text(encoding="utf-8")
    lines = len(content.splitlines())
    size = f.stat().st_size
    print(f"{f.name:<65} | {lines:>4} lines | {size:>7} bytes")
    if f.suffix == ".csv":
        with open(f, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            print(f"   -> CSV header cols: {len(rows[0])}, data rows: {len(rows)-1}")
