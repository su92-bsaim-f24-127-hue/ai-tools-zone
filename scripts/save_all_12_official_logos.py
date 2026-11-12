"""
save_all_12_official_logos.py
Downloads and standardizes all 12 official logos into assets/products/ as 64x64 WebP (or SVG),
updates assets/product-logo-sources.json, and re-compiles the site.
"""

import os
import io
import ssl
import urllib.request
import json
from PIL import Image

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
ASSETS_PROD_DIR = os.path.join(REPO_DIR, "assets", "products")
LOGOS_JSON = os.path.join(REPO_DIR, "assets", "product-logo-sources.json")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

LOGO_MAP = {
    "cursor": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://cursor.com&size=128",
        "website": "https://cursor.com/",
        "fmt": "webp"
    },
    "copilot": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://github.com/features/copilot&size=128",
        "website": "https://github.com/features/copilot",
        "fmt": "webp"
    },
    "claude": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://claude.ai&size=128",
        "website": "https://claude.ai/",
        "fmt": "webp"
    },
    "deepseek": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://deepseek.com&size=128",
        "website": "https://deepseek.com/",
        "fmt": "webp"
    },
    "perplexity": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://perplexity.ai&size=128",
        "website": "https://perplexity.ai/",
        "fmt": "webp"
    },
    "bolt-new": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://bolt.new&size=128",
        "website": "https://bolt.new/",
        "fmt": "webp"
    },
    "runway": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://runwayml.com&size=128",
        "website": "https://runwayml.com/",
        "fmt": "webp"
    },
    "descript": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://descript.com&size=128",
        "website": "https://descript.com/",
        "fmt": "webp"
    },
    "grammarly": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://grammarly.com&size=128",
        "website": "https://grammarly.com/",
        "fmt": "webp"
    },
    "quillbot": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://quillbot.com&size=128",
        "website": "https://quillbot.com/",
        "fmt": "webp"
    },
    "office365": {
        "url": "https://res.cdn.office.net/files/fabric-cdn-prod_20221209.001/assets/brand-icons/product/svg/office_48x1.svg",
        "website": "https://microsoft.com/microsoft-365",
        "fmt": "svg"
    },
    "coursera-plus": {
        "url": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://coursera.org&size=128",
        "website": "https://coursera.org/",
        "fmt": "webp"
    }
}

with open(LOGOS_JSON, "r", encoding="utf-8") as f:
    logos_data = json.load(f)

for pid, info in LOGO_MAP.items():
    print(f"Fetching official logo for {pid}...")
    req = urllib.request.Request(info["url"], headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = resp.read()
        
    if info["fmt"] == "svg":
        out_file = os.path.join(ASSETS_PROD_DIR, f"{pid}.svg")
        with open(out_file, "wb") as sf:
            sf.write(data)
        logos_data[pid] = {
            "website": info["website"],
            "source": info["url"],
            "path": f"assets/products/{pid}.svg",
            "bytes": len(data)
        }
        print(f"  [SAVED] {pid}.svg ({len(data)} bytes)")
    else:
        img = Image.open(io.BytesIO(data))
        img = img.convert("RGBA")
        img = img.resize((64, 64), Image.Resampling.LANCZOS)
        out_file = os.path.join(ASSETS_PROD_DIR, f"{pid}.webp")
        img.save(out_file, format="WEBP", quality=95)
        logos_data[pid] = {
            "website": info["website"],
            "source": info["url"],
            "path": f"assets/products/{pid}.webp",
            "bytes": os.path.getsize(out_file)
        }
        print(f"  [SAVED] {pid}.webp ({os.path.getsize(out_file)} bytes)")

with open(LOGOS_JSON, "w", encoding="utf-8") as f:
    json.dump(logos_data, f, indent=2, ensure_ascii=False)

print("All 12 official logos downloaded and assets/product-logo-sources.json updated!")
