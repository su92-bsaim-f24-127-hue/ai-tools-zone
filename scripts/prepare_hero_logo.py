"""Create web-sized, alpha-preserving exports of the approved 3D logo render.

This performs delivery-format optimization only, not creative image editing.
The original generated PNG is preserved in output/imagegen/.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'output/imagegen/hero-logo-3d-source.png'
with Image.open(source) as image:
    assert image.mode == 'RGBA', 'The hero needs a genuinely transparent render.'
    assert image.getchannel('A').getextrema() == (0, 255)
    for size, filename in [(960, 'hero-logo-3d.webp'), (480, 'hero-logo-3d-mobile.webp')]:
        exported = image.copy()
        exported.thumbnail((size, size), Image.Resampling.LANCZOS)
        destination = ROOT / 'assets' / filename
        exported.save(destination, 'WEBP', quality=90, method=6, exact=True)
        print(f'{filename}: {exported.size}, {destination.stat().st_size:,} bytes')
