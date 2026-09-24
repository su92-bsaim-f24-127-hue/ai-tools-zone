"""Optimize existing brand artwork and collect vendor-hosted product icons."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
from io import BytesIO
import json, requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
OUT = ASSETS / 'products'
OUT.mkdir(exist_ok=True)
SITES = {
 'chatgpt': 'https://chatgpt.com/', 'gemini': 'https://gemini.google.com/',
 'veo': 'https://deepmind.google/models/veo/', 'leonardo': 'https://leonardo.ai/',
 'elevenlabs': 'https://elevenlabs.io/', 'canva': 'https://www.canva.com/',
 'figma': 'https://www.figma.com/', 'capcut': 'https://www.capcut.com/',
 'adobe': 'https://www.adobe.com/creativecloud.html', 'lovable': 'https://lovable.dev/',
 'gamma': 'https://gamma.app/', 'replit': 'https://replit.com/', 'n8n': 'https://n8n.io/',
 'notion': 'https://www.notion.com/', 'nordvpn': 'https://nordvpn.com/',
 'surfshark': 'https://surfshark.com/', 'youtube': 'https://www.youtube.com/',
 'netflix': 'https://www.netflix.com/', 'linkedin': 'https://www.linkedin.com/',
 'windows': 'https://www.microsoft.com/en-us/windows/'
}

class Icons(HTMLParser):
 def __init__(self): super().__init__(); self.urls=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='link' and 'icon' in a.get('rel','').lower() and a.get('href'):
   self.urls.append((2 if 'apple' in a['rel'] else 1, a['href']))

def fetch_icon(item):
 id,site=item
 try:
  response=requests.get(site,timeout=18,headers={'User-Agent':'Mozilla/5.0'})
  parser=Icons(); parser.feed(response.text)
  candidates=[urljoin(response.url,u) for _,u in sorted(parser.urls,reverse=True)]
  candidates += [urljoin(site,'/apple-touch-icon.png'),urljoin(site,'/favicon.ico')]
  for url in dict.fromkeys(candidates):
   try:
    r=requests.get(url,timeout=12,headers={'User-Agent':'Mozilla/5.0'})
    if r.status_code!=200: continue
    if '<svg' in r.text[:500] and 'html' not in r.headers.get('Content-Type',''):
     if '<script' in r.text or '<foreignObject' in r.text: continue
     path=OUT/(id+'.svg'); path.write_bytes(r.content)
    else:
     im=Image.open(BytesIO(r.content)).convert('RGBA')
     if min(im.size)<24: continue
     im.thumbnail((128,128),Image.Resampling.LANCZOS)
     path=OUT/(id+'.webp'); im.save(path,'WEBP',lossless=True)
    return id,{'website':site,'source':url,'path':path.relative_to(ROOT).as_posix(),'bytes':path.stat().st_size}
   except Exception: continue
  return id,{'website':site,'error':'No usable icon found'}
 except Exception as e: return id,{'website':site,'error':str(e)}

if __name__=='__main__':
 original=Image.open(ASSETS/'ai-tools-zone-logo.png').convert('RGB')
 # Match the existing favicon's viewBox exactly; preserve the supplied artwork.
 emblem=original.crop((565,110,1131,676))
 for size,name in [(512,'brand-emblem.webp'),(128,'brand-icon.webp')]:
  emblem.resize((size,size),Image.Resampling.LANCZOS).save(ASSETS/name,'WEBP',quality=88)
 for size in [32,48,180,192,512]:
  emblem.resize((size,size),Image.Resampling.LANCZOS).save(ASSETS/f'icon-{size}.png',optimize=True)
 emblem.resize((64,64),Image.Resampling.LANCZOS).save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
 original.thumbnail((600,600),Image.Resampling.LANCZOS)
 original.save(ASSETS/'brand-wordmark.webp','WEBP',quality=88)
 # Social card uses the unmodified supplied identity on its matching background.
 card=Image.new('RGB',(1200,630),(16,17,15))
 source=Image.open(ASSETS/'ai-tools-zone-logo.png').convert('RGB'); source.thumbnail((1150,630),Image.Resampling.LANCZOS)
 card.paste(source,((1200-source.width)//2,(630-source.height)//2)); card.save(ASSETS/'social-card.jpg',quality=86,optimize=True)
 manifest=dict(ThreadPoolExecutor(max_workers=10).map(fetch_icon,SITES.items()))
 (ASSETS/'product-logo-sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 print(json.dumps(manifest,indent=2))
