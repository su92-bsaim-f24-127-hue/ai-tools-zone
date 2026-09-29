"""Dependency-free production SEO regression audit. Run after build_site.py."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote, parse_qs
from urllib.robotparser import RobotFileParser
from collections import Counter, deque
from datetime import date
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).parent
ORIGIN='https://aitoolszone.tech'
FOLDERS=('products','categories','use-cases','compare','alternatives','guides','pricing','about','privacy','terms')

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.titles=[]; self.h1=[]; self.schemas=[]; self.visible=[]
        self.capture=None; self.buffer=[]; self.ignore=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if tag in ('title','h1') or (tag=='script' and attrs.get('type')=='application/ld+json'):
            self.capture=tag; self.buffer=[]
        if tag in ('script','style'): self.ignore+=1
    def handle_endtag(self, tag):
        if self.capture==tag:
            text=''.join(self.buffer).strip()
            if tag=='title':self.titles.append(text)
            elif tag=='h1':self.h1.append(text)
            else:self.schemas.append(text)
            self.capture=None
        if tag in ('script','style'): self.ignore=max(0,self.ignore-1)
    def handle_data(self, text):
        if self.capture:self.buffer.append(text)
        if not self.ignore:self.visible.append(text)
    def attrs(self, tag, **match):
        return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in match.items())]

def file_for(path):
    clean=unquote(path).lstrip('/')
    return ROOT/(clean+'index.html' if not clean or clean.endswith('/') else clean)

def run():
    errors=[]; warnings=[]; checks=0
    def check(value,message):
        nonlocal checks
        checks+=1
        if not value:errors.append(message)
    sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
    urls=[n.text for n in sitemap.findall('{*}url/{*}loc')]
    check(len(urls)==len(set(urls)),'Duplicate sitemap URLs')
    canonical_paths={urlparse(u).path for u in urls}
    files=[ROOT/'index.html']+[p for folder in FOLDERS for p in (ROOT/folder).rglob('*.html')]
    pages={('/' if f==ROOT/'index.html' else '/'+f.relative_to(ROOT).as_posix().removesuffix('index.html')):Page(f.read_text(encoding='utf-8')) for f in files}
    check(set(pages)==canonical_paths,'Generated pages and sitemap differ')
    check(all(u==ORIGIN+urlparse(u).path and u.endswith('/') for u in urls),'Sitemap has noncanonical/query URLs')
    states=json.loads((ROOT/'data/page-state.json').read_text())
    for node in sitemap.findall('{*}url'):
        path=urlparse(node.find('{*}loc').text).path
        lastmod=node.find('{*}lastmod')
        check(lastmod is not None and date.fromisoformat(lastmod.text)<=date.today(),path+' invalid lastmod')
        check(lastmod is not None and lastmod.text==states.get(path,{}).get('lastmod'),path+' lastmod differs from source record')
    catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
    products={'/products/'+p['slug']+'/':p for p in catalog}
    graph={path:set() for path in pages}; inbound=Counter(); descriptions=[]; titles=[]; external=set(); assets=set()
    for path,page in pages.items():
        check(len(page.titles)==1 and bool(page.titles[0]),path+' needs one title')
        check(len(page.h1)==1 and bool(page.h1[0]),path+' needs one H1')
        titles+=page.titles
        description=page.attrs('meta',name='description')
        check(len(description)==1 and bool(description[0].get('content')),path+' missing description')
        descriptions += [x.get('content','') for x in description]
        check(page.attrs('link',rel='canonical')==[{'rel':'canonical','href':ORIGIN+path}],path+' canonical mismatch')
        check(not any('noindex' in a.get('content','') for a in page.attrs('meta',name='robots')),path+' noindex in sitemap')
        for prop in ('title','description','image','url','type','locale'):
            check(bool(page.attrs('meta',property='og:'+prop)),path+' missing OG '+prop)
        check(bool(page.attrs('meta',name='twitter:card')),path+' missing Twitter card')
        for rel in ('icon','manifest'):
            check(bool(page.attrs('link',rel=rel)),path+' missing '+rel)
        check(bool(page.attrs('html',lang='en-PK')),path+' incorrect document language')
        check(bool(page.attrs('main')),path+' missing main landmark')
        ids=[a['id'] for _,a in page.tags if 'id' in a]
        check(len(ids)==len(set(ids)),path+' duplicate HTML IDs')
        if len(' '.join(page.visible).split())<120:warnings.append(path+' short content: review purpose, not an automatic ranking issue')
        schema_nodes=[]
        for raw in page.schemas:
            try:
                obj=json.loads(raw); check(obj.get('@context')=='https://schema.org',path+' incorrect schema context'); schema_nodes.extend(obj.get('@graph',[obj]))
            except ValueError:check(False,path+' invalid JSON-LD')
        types=[n.get('@type') for n in schema_nodes]
        schema_ids=[n['@id'] for n in schema_nodes if '@id' in n]
        check(len(schema_ids)==len(set(schema_ids)),path+' duplicate schema entity definitions')
        for required in ['Organization','WebSite','WebPage']+(['BreadcrumbList'] if path!='/' else []):
            check(types.count(required)==1,path+' missing/duplicate '+required)
        if path!='/':
            raw=file_for(path).read_text(encoding='utf-8')
            nav=re.search(r'<nav aria-label="Breadcrumb">(.*?)</nav>',raw,re.S)
            check(nav is not None,path+' missing visible breadcrumb')
            if nav:
                crumbs=[]
                for li in re.findall(r'<li\b([^>]*)>(.*?)</li>',nav[1],re.S):
                    if 'aria-hidden' in li[0]:continue
                    part=Page(li[1]);anchors=part.attrs('a')
                    crumbs.append((''.join(part.visible).strip(),urljoin(ORIGIN+path,anchors[0]['href']) if anchors else ORIGIN+path))
                nodes=[n for n in schema_nodes if n.get('@type')=='BreadcrumbList']
                if nodes:check(crumbs==[(n['name'],n['item']) for n in nodes[0]['itemListElement']],path+' visible/schema breadcrumb mismatch')
        for n in schema_nodes:
            check('aggregateRating' not in n and 'review' not in n,path+' unverified rating markup')
        if path in products:
            p=products[path]; nodes=[n for n in schema_nodes if n.get('@type')=='Product']
            check(len(nodes)==1,path+' missing Product schema')
            if nodes:
                offer=nodes[0].get('offers',{})
                check(offer.get('price')==p['price'] and offer.get('priceCurrency')=='PKR',path+' incorrect structured price/currency')
                check(offer.get('url')==ORIGIN+path,path+' incorrect offer URL')
                check('availability' not in offer,path+' unverified stock status')
                check(offer.get('seller',{}).get('@id')==ORIGIN+'/#organization',path+' disconnected seller identity')
            visible=' '.join(page.visible)
            check(all(str(value) in visible for value in [p['name'],f'{p["price"]:,}',p['duration'],p['access']]),path+' incomplete initial HTML plan')
            check(any(a.get('href','').startswith('/categories/') for a in page.attrs('a')),path+' missing category link')
        for tag,attrs in page.tags:
            if tag=='img':
                check('alt' in attrs,path+' missing image alt attribute')
                check(attrs.get('width','').isdigit() and attrs.get('height','').isdigit(),path+' missing image dimensions')
            references=[]
            if tag in ('a','link') and attrs.get('href'):references.append(attrs['href'])
            if tag in ('img','script','source') and attrs.get('src'):references.append(attrs['src'])
            if tag in ('img','source') and attrs.get('srcset'):references.extend(x.strip().split()[0] for x in attrs['srcset'].split(','))
            for ref in references:
                target=urlparse(urljoin(ORIGIN+path,ref))
                if target.scheme not in ('http','https'):continue
                if target.netloc!='aitoolszone.tech':
                    if tag=='a':external.add(target.geturl())
                    if target.netloc=='wa.me':
                        check(target.path=='/923430173923',path+' incorrect WhatsApp number')
                        if path in products and 'text' in parse_qs(target.query):
                            order=parse_qs(target.query)['text'][0]
                            check(products[path]['name'] in order and f'{products[path]["price"]:,}' in order,path+' stale WhatsApp order')
                    continue
                dest=file_for(target.path)
                check(dest.is_file(),path+' broken local URL '+ref)
                if target.path in pages and tag=='a':
                    graph[path].add(target.path)
                    if target.path!=path:inbound[target.path]+=1
                    if target.fragment:
                        check(any(a.get('id')==unquote(target.fragment) for _,a in pages[target.path].tags),path+' missing anchor '+ref)
                elif dest.is_file() and tag!='a':assets.add(dest)
    for value,count in Counter(titles).items():check(count==1,'Duplicate title: '+value)
    for value,count in Counter(descriptions).items():check(count==1,'Duplicate description: '+value)
    distances={'/':0}; queue=deque(['/'])
    while queue:
        path=queue.popleft()
        for dest in graph[path]:
            if dest not in distances:distances[dest]=distances[path]+1;queue.append(dest)
    for path in pages:
        check(path in distances,path+' unreachable from homepage')
        check(path=='/' or inbound[path]>0,path+' orphan page')
    for asset in assets:
        if asset.suffix in ('.png','.webp','.jpg','.svg') and asset.stat().st_size>300000:warnings.append(str(asset.relative_to(ROOT))+' image exceeds 300 KB')
    robots=RobotFileParser(); robots.parse((ROOT/'robots.txt').read_text().splitlines())
    for bot in ('Googlebot','Bingbot','OAI-SearchBot','ChatGPT-User'):
        for path in pages:check(robots.can_fetch(bot,ORIGIN+path),bot+' blocked '+path)
    check(not robots.can_fetch('GPTBot',ORIGIN+'/'),'Training policy unintentionally permits GPTBot')
    check(ORIGIN+'/sitemap.xml' in (robots.site_maps() or []),'Robots sitemap missing')
    notfound=Page((ROOT/'404.html').read_text(encoding='utf-8'))
    check(any('noindex' in a.get('content','') for a in notfound.attrs('meta',name='robots')),'404 missing noindex')
    check('/404.html' not in canonical_paths,'404 included in sitemap')
    report={'pages':len(pages),'checks':checks,'errors':errors,'warnings':warnings,'max_crawl_depth':max(distances.values()),'external_links':sorted(external),'local_resources_checked':len(assets),'crawl_depth':distances}
    out=ROOT/'verification';out.mkdir(exist_ok=True)
    (out/'seo-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('external_links','crawl_depth')},indent=2))
    return bool(errors)

if __name__=='__main__':sys.exit(run())
