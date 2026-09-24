"""Pinned fallbacks for vendors whose marketing homepages reject automated requests."""
from pathlib import Path
from io import BytesIO
import json, requests
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
manifest_path=ROOT/'assets/product-logo-sources.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
sources={
 'chatgpt':('https://openai.com/favicon.ico',None),
 'adobe':('https://www.adobe.com/favicon.ico',None),
 'leonardo':('https://files.readme.io/e6fd24fe6d94d90d5c885217bfc7e206f382cccef4e950586465ac1a3750f90d-Leonardo_Icon_ElectricPurple_1.png',None),
 'windows':('https://cdn.jsdelivr.net/npm/simple-icons@11/icons/windows11.svg','#0078D4'),
 'nordvpn':('https://cdn.jsdelivr.net/npm/simple-icons@11/icons/nordvpn.svg','#4687FF')
}
for id,(url,colour) in sources.items():
 r=requests.get(url,timeout=25); r.raise_for_status()
 if colour:
  # Preserve the distributed official glyph with its published brand colour.
  content=r.text.replace('<svg ',f'<svg fill="{colour}" ',1)
  path=ROOT/f'assets/products/{id}.svg'; path.write_text(content,encoding='utf-8')
 else:
  im=Image.open(BytesIO(r.content)).convert('RGBA'); im.thumbnail((128,128),Image.Resampling.LANCZOS)
  path=ROOT/f'assets/products/{id}.webp'; im.save(path,'WEBP',lossless=True)
 manifest[id].pop('error',None)
 manifest[id].update(source=url,path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size)
 if colour: manifest[id].update(colour=colour,attribution='Simple Icons v11, CC0. Brand trademarks remain with their owners.')
 if id=='leonardo': manifest[id]['source_page']='https://docs.leonardo.ai/'
 print(id,path.stat().st_size,flush=True)
manifest_path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
