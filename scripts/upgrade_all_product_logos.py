"""
upgrade_all_product_logos.py
Upgrades all 20 legacy products in AI Tools Zone to authentic, high-resolution original brand logos
using official CDNs and Google's high-res FaviconV2 service (128x128).
Converts each logo to optimized 64x64 WebP with RGBA transparency and Lanczos antialiasing.
Updates assets/product-logo-sources.json.
"""

import os
import json
import io
import urllib.request
from PIL import Image

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
ASSETS_DIR = os.path.join(REPO_DIR, "assets", "products")
SOURCES_JSON = os.path.join(REPO_DIR, "assets", "product-logo-sources.json")

# Brand logo sources for the original 20 products
ORIGINAL_20_SOURCES = {
    "chatgpt": {
        "website": "https://chatgpt.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://chatgpt.com&size=128",
        "ext": "webp"
    },
    "gemini": {
        "website": "https://gemini.google.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://gemini.google.com&size=128",
        "ext": "webp"
    },
    "veo": {
        "website": "https://deepmind.google/technologies/veo/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://deepmind.google/technologies/veo/&size=128",
        "ext": "webp"
    },
    "leonardo": {
        "website": "https://leonardo.ai/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://leonardo.ai&size=128",
        "ext": "webp"
    },
    "elevenlabs": {
        "website": "https://elevenlabs.io/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://elevenlabs.io&size=128",
        "ext": "webp"
    },
    "canva": {
        "website": "https://www.canva.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.canva.com&size=128",
        "ext": "webp"
    },
    "figma": {
        "website": "https://www.figma.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.figma.com&size=128",
        "ext": "webp"
    },
    "capcut": {
        "website": "https://www.capcut.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.capcut.com&size=128",
        "ext": "webp"
    },
    "adobe": {
        "website": "https://www.adobe.com/creativecloud.html",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.adobe.com&size=128",
        "ext": "webp"
    },
    "lovable": {
        "website": "https://lovable.dev/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://lovable.dev&size=128",
        "ext": "webp"
    },
    "gamma": {
        "website": "https://gamma.app/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://gamma.app&size=128",
        "ext": "webp"
    },
    "replit": {
        "website": "https://replit.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://replit.com&size=128",
        "ext": "webp"
    },
    "n8n": {
        "website": "https://n8n.io/",
        "source": "https://n8n.io/apple-touch-icon.png",
        "ext": "webp"
    },
    "notion": {
        "website": "https://www.notion.so/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.notion.so&size=128",
        "ext": "webp"
    },
    "nordvpn": {
        "website": "https://nordvpn.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://nordvpn.com&size=128",
        "ext": "webp"
    },
    "surfshark": {
        "website": "https://surfshark.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://surfshark.com&size=128",
        "ext": "webp"
    },
    "youtube": {
        "website": "https://www.youtube.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.youtube.com&size=128",
        "ext": "webp"
    },
    "netflix": {
        "website": "https://www.netflix.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.netflix.com&size=128",
        "ext": "webp"
    },
    "linkedin": {
        "website": "https://www.linkedin.com/",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.linkedin.com&size=128",
        "ext": "webp"
    },
    "windows": {
        "website": "https://www.microsoft.com/windows",
        "source": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://www.microsoft.com/windows&size=128",
        "ext": "webp"
    }
}

def main():
    with open(SOURCES_JSON, "r", encoding="utf-8") as f:
        registry = json.load(f)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    upgraded = []
    for pid, meta in ORIGINAL_20_SOURCES.items():
        url = meta["source"]
        ext = meta["ext"]
        dest_filename = f"{pid}.{ext}"
        dest_rel_path = f"assets/products/{dest_filename}"
        dest_abs_path = os.path.join(REPO_DIR, dest_rel_path)

        print(f"Fetching authentic logo for '{pid}' from {url}...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()

            im = Image.open(io.BytesIO(data))
            # Convert to RGBA
            if im.mode != "RGBA":
                im = im.convert("RGBA")

            # Resize with Lanczos to crisp 64x64
            im_resized = im.resize((64, 64), Image.Resampling.LANCZOS)
            im_resized.save(dest_abs_path, format="WEBP", quality=92, method=6)
            
            file_bytes = os.path.getsize(dest_abs_path)
            registry[pid] = {
                "website": meta["website"],
                "source": url,
                "path": dest_rel_path,
                "bytes": file_bytes,
                "original_resolution": f"{im.size[0]}x{im.size[1]}"
            }
            upgraded.append((pid, file_bytes, f"{im.size[0]}x{im.size[1]}"))
            print(f" -> SUCCESS: Saved {dest_filename} ({file_bytes} bytes, original {im.size[0]}x{im.size[1]})")

        except Exception as e:
            print(f" -> FAILED for {pid}: {e}")

    with open(SOURCES_JSON, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    print("\n" + "="*60)
    print(f"UPGRADED {len(upgraded)} / {len(ORIGINAL_20_SOURCES)} PRODUCT LOGOS:")
    for pid, b, orig in upgraded:
        print(f" - {pid:12} : {b:5} bytes | original resolution: {orig}")
    print("="*60)

if __name__ == "__main__":
    main()
