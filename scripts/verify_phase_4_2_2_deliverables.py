import os
from pathlib import Path

p = Path("seo-growth-2026/phase-4.2.2")
print(f"Checking deliverables in {p}:")
for f in sorted(p.glob("*")):
    content = f.read_text(encoding="utf-8")
    lines = len(content.splitlines())
    size = f.stat().st_size
    print(f"{f.name:<60} | {lines:>4} lines | {size:>7} bytes")
