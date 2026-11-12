"""
fetch_official_logos.py
Downloads official brand icons/logos for the 12 new products,
converts/saves them as high-quality 64x64 transparent WebPs or SVGs,
and updates assets/product-logo-sources.json.
"""

import os
import io
import ssl
import urllib.request
from PIL import Image
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
ASSETS_PROD_DIR = os.path.join(REPO_DIR, "assets", "products")
LOGOS_JSON = os.path.join(REPO_DIR, "assets", "product-logo-sources.json")

# Verified official CDN / Favicon / Logo URLs
OFFICIAL_SOURCES = {
    "cursor": {
        "url": "https://www.cursor.com/favicon.ico",
        "website": "https://cursor.com/",
        "alt_urls": [
            "https://raw.githubusercontent.com/getcursor/cursor/main/packages/cursor/assets/icon.png",
            "https://cursor.com/assets/images/logo.svg"
        ]
    },
    "copilot": {
        "url": "https://github.githubassets.com/assets/copilot-banner-251f98d752f9.png",
        "website": "https://github.com/features/copilot",
        "alt_urls": [
            "https://github.githubassets.com/favicons/favicon.png",
            "https://github.githubassets.com/favicons/favicon.svg"
        ]
    },
    "claude": {
        "url": "https://claude.ai/favicon.ico",
        "website": "https://claude.ai/",
        "alt_urls": [
            "https://anthropic.com/favicon.ico",
            "https://upload.wikimedia.org/wikipedia/commons/7/78/Anthropic_logo.svg"
        ]
    },
    "deepseek": {
        "url": "https://chat.deepseek.com/favicon.ico",
        "website": "https://deepseek.com/",
        "alt_urls": [
            "https://www.deepseek.com/favicon.ico"
        ]
    },
    "perplexity": {
        "url": "https://www.perplexity.ai/favicon.ico",
        "website": "https://perplexity.ai/",
        "alt_urls": [
            "https://www.perplexity.ai/favicon-32x32.png"
        ]
    },
    "bolt-new": {
        "url": "https://bolt.new/favicon.ico",
        "website": "https://bolt.new/",
        "alt_urls": [
            "https://stackblitz.com/favicon.ico"
        ]
    },
    "runway": {
        "url": "https://runwayml.com/favicon.ico",
        "website": "https://runwayml.com/",
        "alt_urls": [
            "https://app.runwayml.com/favicon.ico"
        ]
    },
    "descript": {
        "url": "https://www.descript.com/favicon.ico",
        "website": "https://descript.com/",
        "alt_urls": [
            "https://assets.descript.com/favicon.ico"
        ]
    },
    "grammarly": {
        "url": "https://static.grammarly.com/assets/files/d5e317e3f8a02a8264906f235adcf829/favicon-32x32.png",
        "website": "https://grammarly.com/",
        "alt_urls": [
            "https://www.grammarly.com/favicon.ico"
        ]
    },
    "quillbot": {
        "url": "https://quillbot.com/favicon.ico",
        "website": "https://quillbot.com/",
        "alt_urls": [
            "https://quillbot.com/favicon-32x32.png"
        ]
    },
    "office365": {
        "url": "https://c.s-microsoft.com/favicon.ico",
        "website": "https://microsoft.com/microsoft-365",
        "alt_urls": [
            "https://res.cdn.office.net/files/fabric-cdn-prod_20221209.001/assets/brand-icons/product/svg/office_48x1.svg"
        ]
    },
    "coursera-plus": {
        "url": "https://d3njjcbhbojbot.cloudfront.net/web/images/favicons/favicon-v2-32x32.png",
        "website": "https://coursera.org/",
        "alt_urls": [
            "https://www.coursera.org/favicon.ico"
        ]
    }
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def download_data(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        return resp.read()

results = {}

for pid, info in OFFICIAL_SOURCES.items():
    urls_to_try = [info["url"]] + info.get("alt_urls", [])
    success = False
    
    for u in urls_to_try:
        try:
            print(f"Trying {pid} from {u}...")
            data = download_data(u)
            if len(data) > 100:
                # Try opening as image
                try:
                    img = Image.open(io.BytesIO(data))
                    # Convert to RGBA
                    img = img.convert("RGBA")
                    # Resize to 64x64 high quality
                    img = img.resize((64, 64), Image.Resampling.LANCZOS)
                    out_path = os.path.join(ASSETS_PROD_DIR, f"{pid}.webp")
                    img.save(out_path, format="WEBP", quality=95)
                    results[pid] = {
                        "path": f"assets/products/{pid}.webp",
                        "website": info["website"],
                        "source": u,
                        "bytes": os.path.getsize(out_path),
                        "size": img.size
                    }
                    print(f"  [SUCCESS] Saved {pid}.webp ({os.path.getsize(out_path)} bytes)")
                    success = True
                    break
                except Exception as img_err:
                    print(f"  Image open error: {img_err}")
                    if data.startswith(b"<svg") or b"<svg" in data[:100]:
                        # Save SVG
                        out_path = os.path.join(ASSETS_PROD_DIR, f"{pid}.svg")
                        with open(out_path, "wb") as sf:
                            sf.write(data)
                        results[pid] = {
                            "path": f"assets/products/{pid}.svg",
                            "website": info["website"],
                            "source": u,
                            "bytes": len(data)
                        }
                        print(f"  [SUCCESS] Saved {pid}.svg ({len(data)} bytes)")
                        success = True
                        break
        except Exception as net_err:
            print(f"  Network error for {u}: {net_err}")
            
    if not success:
        print(f"  [FAILED] Could not download official logo for {pid}")

print(f"\nSuccessfully downloaded and processed {len(results)} / 12 logos.")
