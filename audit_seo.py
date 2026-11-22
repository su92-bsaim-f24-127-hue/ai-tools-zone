"""Dependency-free production SEO regression audit. Run after build_site.py."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote, parse_qs
from urllib.robotparser import RobotFileParser
from collections import Counter, deque
from datetime import date, timedelta
import json
import re
import sys
from hashlib import sha256
import xml.etree.ElementTree as ET
from seo_pages import content_date

ROOT=Path(__file__).parent
ORIGIN='https://aitoolszone.tech'
SETTINGS=json.loads((ROOT/'data/site-settings.json').read_text(encoding='utf-8'))
WHATSAPP_NUMBER=''.join(ch for ch in SETTINGS['whatsappNumber'] if ch.isdigit())
FOLDERS=('products','categories','use-cases','compare','alternatives','guides','pricing','blog','about','privacy','terms','faq','buy-ai-tools-in-pakistan','how-to-buy-chatgpt-plus-in-pakistan','best-ai-tools-for-students-pakistan','ai-video-editing-tools-pakistan','ai-image-generator-subscriptions-pakistan')

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


def evaluate_period(target_text, p):
    target_text = re.sub(r'\b(final|first|gap|second|third|multi)-year\b', r'\1_academic_yr', target_text, flags=re.I)
    dur = p["duration"]
    found_words = re.findall(r'\b(lifetime|one-time|months?|mo|years?|yrs?)\b', target_text, re.I)
    if not found_words:
        return "not applicable"
    has_lifetime = bool(re.search(r'\b(lifetime|one-time)\b', target_text, re.I))
    if has_lifetime:
        return "ok" if dur == "Lifetime" else "mismatch"
    if dur == "Lifetime":
        return "mismatch"
    if dur in ["8,500 Credits", "40 USD Credits", "Confirm before ordering"]:
        return "mismatch"
    if dur == "1 Month":
        if re.search(r'\b(years?|yrs?)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b([2-9]|\d{2,})\s*(months?|mo)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*month|1-month|month|monthly|mo|1\s*mo)\b', target_text, re.I): return "ok"
        return "mismatch"
    if dur == "2 Months":
        if re.search(r'\b(years?|yrs?|lifetime|one-time)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*month|1-month|3\s*months?|18\s*months?)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(2\s*months?|2-month|2\s*mo)\b', target_text, re.I): return "ok"
        return "mismatch"
    if dur == "3 Months":
        if re.search(r'\b(years?|yrs?|lifetime|one-time)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*month|1-month|2\s*months?|18\s*months?)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(3\s*months?|3-month|3\s*mo)\b', target_text, re.I): return "ok"
        return "mismatch"
    if dur == "1 Year":
        if re.search(r'\b(months?|mo|lifetime|one-time)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(2\s*years?|2-year)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*year|1-year|year|annual|annually|1\s*yr|yr)\b', target_text, re.I): return "ok"
        return "mismatch"
    if dur == "2 Years":
        if re.search(r'\b(months?|mo|lifetime|one-time)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*year|1-year)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(2\s*years?|2-year|2\s*yrs?)\b', target_text, re.I): return "ok"
        return "mismatch"
    return "not applicable"

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
        check(lastmod is not None and date.fromisoformat(lastmod.text)<=content_date(),path+' invalid lastmod')
        check(lastmod is not None and lastmod.text==states.get(path,{}).get('lastmod'),path+' lastmod differs from source record')
    catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
    products_checked = 0
    badge_conflicts = 0
    desc_conflicts = 0
    for p in catalog:
        products_checked += 1
        badge = p.get('badge', '')
        dur = p.get('duration', '')
        acc = p.get('access', '')
        
        # Badge checks: "N-Year Plan", "N-Month Plan", "Shared Access", "Private", "Invitation"
        m_year = re.search(r'(\d+)-Year Plan', badge, re.I)
        if m_year:
            n_years = m_year.group(1)
            expected_dur = f"{n_years} Year" if n_years == '1' else f"{n_years} Years"
            if dur != expected_dur:
                badge_conflicts += 1
                check(False, f"Badge duration mismatch for {p['id']}: badge has '{badge}', duration is '{dur}'")
                
        m_month = re.search(r'(\d+)-Month Plan', badge, re.I)
        if m_month:
            n_months = m_month.group(1)
            expected_dur = f"{n_months} Month" if n_months == '1' else f"{n_months} Months"
            if dur != expected_dur:
                badge_conflicts += 1
                check(False, f"Badge duration mismatch for {p['id']}: badge has '{badge}', duration is '{dur}'")
                
        if re.search(r'Shared Access', badge, re.I) and acc != 'Shared':
            badge_conflicts += 1
            check(False, f"Badge access mismatch for {p['id']}: badge has '{badge}', access is '{acc}'")
            
        if re.search(r'\bPrivate\b', badge, re.I) and acc != 'Private':
            badge_conflicts += 1
            check(False, f"Badge access mismatch for {p['id']}: badge has '{badge}', access is '{acc}'")
            
        if re.search(r'\bInvitation\b', badge, re.I) and acc != 'Invitation':
            badge_conflicts += 1
            check(False, f"Badge access mismatch for {p['id']}: badge has '{badge}', access is '{acc}'")

        # Description check on catalog description: check PKR amounts, "for N months", "per month", "per year", "N-year", "N-month", access types, delivery ranges, warranty days
        desc = p.get('description', '')
        dl = desc.lower()
        m_price = re.search(r'PKR\s+([\d,]+)', desc)
        if m_price:
            desc_price = int(m_price.group(1).replace(',', ''))
            if desc_price != p['price']:
                desc_conflicts += 1
                check(False, f"Catalog description price mismatch for {p['id']}: description has PKR {desc_price}, field has PKR {p['price']}")
                
        m_m = re.search(r'(\d+)-month|for (\d+) months?', dl)
        if m_m:
            n = m_m.group(1) or m_m.group(2)
            exp = f"{n} Month" if n == '1' else f"{n} Months"
            if dur != exp:
                desc_conflicts += 1
                check(False, f"Catalog description duration mismatch for {p['id']}: description has '{exp}', field has '{dur}'")
        if 'per month' in dl and dur != '1 Month':
            desc_conflicts += 1
            check(False, f"Catalog description duration mismatch for {p['id']}: description has 'per month', field has '{dur}'")
        if 'per year' in dl and dur != '1 Year':
            desc_conflicts += 1
            check(False, f"Catalog description duration mismatch for {p['id']}: description has 'per year', field has '{dur}'")
        m_y = re.search(r'(\d+)-year|for (\d+) years?', dl)
        if m_y:
            n = m_y.group(1) or m_y.group(2)
            exp = f"{n} Year" if n == '1' else f"{n} Years"
            if dur != exp:
                desc_conflicts += 1
                check(False, f"Catalog description duration mismatch for {p['id']}: description has '{exp}', field has '{dur}'")

        if 'private access' in dl and acc != 'Private':
            desc_conflicts += 1
            check(False, f"Catalog description access mismatch for {p['id']}: description has 'Private', field has '{acc}'")
        if 'shared access' in dl and acc != 'Shared':
            desc_conflicts += 1
            check(False, f"Catalog description access mismatch for {p['id']}: description has 'Shared', field has '{acc}'")
        if 'invitation access' in dl and acc != 'Invitation':
            desc_conflicts += 1
            check(False, f"Catalog description access mismatch for {p['id']}: description has 'Invitation', field has '{acc}'")
        if 'license key' in dl and acc != 'License Key':
            desc_conflicts += 1
            check(False, f"Catalog description access mismatch for {p['id']}: description has 'License Key', field has '{acc}'")

        deliv = p['delivery'].replace('-', '–')
        if '15 to 30 minutes' in dl and deliv != '15–30 min':
            desc_conflicts += 1
            check(False, f"Catalog description delivery mismatch for {p['id']}: description has '15 to 30 minutes', field has '{deliv}'")
        if '30 to 60 minutes' in dl and deliv != '30–60 min':
            desc_conflicts += 1
            check(False, f"Catalog description delivery mismatch for {p['id']}: description has '30 to 60 minutes', field has '{deliv}'")
        if '1 to 2 hours' in dl and deliv != '1–2 hours':
            desc_conflicts += 1
            check(False, f"Catalog description delivery mismatch for {p['id']}: description has '1 to 2 hours', field has '{deliv}'")

        warr = p['warranty']
        if '7 days' in dl and warr != '7 Days':
            desc_conflicts += 1
            check(False, f"Catalog description warranty mismatch for {p['id']}: description has '7 days', field has '{warr}'")
        if '30 days' in dl and warr != '30 Days':
            desc_conflicts += 1
            check(False, f"Catalog description warranty mismatch for {p['id']}: description has '30 days', field has '{warr}'")
        if 'no replacement warranty' in dl and warr != 'No Warranty':
            desc_conflicts += 1
            check(False, f"Catalog description warranty mismatch for {p['id']}: description has 'No Warranty', field has '{warr}'")

    print(f"Description & badge audit: {products_checked} products checked, {desc_conflicts + badge_conflicts} conflicts (must be 0)")

    PLAN_WORDS = ['Pro', 'Plus', 'Premium', 'Essential', 'Edu', 'Starter', 'Business', 'Creator', 'Unlimited', 'Core', 'Private', 'Key', '4K']
    plan_regex = re.compile(rf'\b(?:{"|".join(PLAN_WORDS)})\b', re.I)
    extra_names = {
        "Gamma App": "gamma-pro",
        "Google Gemini Pro": "gemini-pro",
        "Google Veo": "veo-3-ultra",
        "Leonardo AI": "leonardo-ai-essential",
        "Runway": "runway-ml-gen-3",
        "Copilot": "github-copilot",
        "Notion": "notion-business",
        "Figma": "figma-pro-private",
        "Canva Pro": "canva-pro-edu",
    }
    p_by_slug = {p["slug"]: p for p in catalog}
    alias_to_product = {}
    for p in catalog:
        alias_to_product[p["name"]] = p
    for p in catalog:
        stripped = plan_regex.sub('', p["name"])
        stripped = ' '.join(stripped.split()).strip()
        if stripped and stripped != p["name"] and len(stripped) >= 3:
            if stripped not in alias_to_product:
                alias_to_product[stripped] = p
    for alias, slug in extra_names.items():
        if slug in p_by_slug:
            alias_to_product[alias] = p_by_slug[slug]
    sorted_aliases = sorted(alias_to_product.keys(), key=lambda a: len(a), reverse=True)
    catalog_products = sorted(catalog, key=lambda p: len(p['name']), reverse=True)
    products={'/products/'+p['slug']+'/':p for p in catalog}
    graph={path:set() for path in pages}; inbound=Counter(); descriptions=[]; titles=[]; external=set(); assets=set()
    main_content_fingerprints={}
    all_price_mentions=[]
    for path,page in pages.items():
        check(len(page.titles)==1 and bool(page.titles[0]),path+' needs one title')
        check(len(page.h1)==1 and bool(page.h1[0]),path+' needs one H1')
        page_html=file_for(path).read_text(encoding='utf-8')
        html_lines = page_html.splitlines()
        main_match=re.search(r'<main\b[^>]*>(.*?)</main>',page_html,re.S|re.I)
        main_text=' '.join(' '.join(Page(main_match.group(1) if main_match else '').visible).split()).casefold()
        check(bool(main_text),path+' missing visible main content')
        if main_text:
            fingerprint=sha256(main_text.encode('utf-8')).hexdigest()
            previous=main_content_fingerprints.get(fingerprint)
            check(previous is None,path+' duplicates visible main content from '+str(previous))
            if previous is None:main_content_fingerprints[fingerprint]=path
        # Guardrail: check for outdated model-name patterns in editorial/product copy (excluding reviews)
        clean_page_html = re.sub(r'<section\b[^>]*\bid=["\']customer-reviews["\'][^>]*>.*?</section>', '', page_html, flags=re.S|re.I)
        clean_page_html = re.sub(r'"reviewBody":\s*"[^"]*"', '', clean_page_html)
        outdated_model_patterns = [
            (r'\bGPT-4o\b', 'GPT-4o'),
            (r'\bGPT-4\b(?!\w)', 'GPT-4'),
            (r'\bo1-(?:preview|mini)\b', 'o1-preview/mini'),
            (r'\bDALL[- ]?E(?: 3)?\b', 'DALL-E 3'),
            (r'\bClaude 3\.[57]\b', 'Claude 3.x'),
            (r'\bGemini 1\.5\b', 'Gemini 1.5'),
            (r'\bLlama [23]\b', 'Llama 2/3'),
            (r'\bSWE-bench\b', 'SWE-bench'),
            (r'\b200k context\b', '200k context'),
        ]
        for pat, pat_name in outdated_model_patterns:
            check(not re.search(pat, clean_page_html, re.I), f"{path} contains outdated model pattern '{pat_name}'")
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
        for schema_raw in page.schemas:
            try:
                obj=json.loads(schema_raw); check(obj.get('@context')=='https://schema.org',path+' incorrect schema context'); schema_nodes.extend(obj.get('@graph',[obj]))
            except ValueError:check(False,path+' invalid JSON-LD')
        types=[n.get('@type') for n in schema_nodes]
        schema_ids=[n['@id'] for n in schema_nodes if '@id' in n]
        check(len(schema_ids)==len(set(schema_ids)),path+' duplicate schema entity definitions')
        for required in ['Organization','WebSite','WebPage']+(['BreadcrumbList'] if path!='/' else []):
            check(types.count(required)==1,path+' missing/duplicate '+required)
        if path!='/':
            nav=re.search(r'<nav aria-label="Breadcrumb">(.*?)</nav>',page_html,re.S)
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
            if n.get('@type')=='Product':
                check(n.get('aggregateRating',{}).get('@type')=='AggregateRating',path+' missing aggregateRating')
            if n.get('@type')=='Organization':
                check('hasMerchantReturnPolicy' not in n,path+' unsupported organization return policy')
        if path in products:
            p=products[path]; nodes=[n for n in schema_nodes if n.get('@type')=='Product']
            check(len(nodes)==1,path+' missing Product schema')
            if nodes:
                check(nodes[0].get('brand',{}).get('@type')=='Brand' and bool(nodes[0].get('brand',{}).get('name')),path+' missing product brand')
                check(nodes[0].get('sku')==p['slug'],path+' missing product sku')
                check('mpn' not in nodes[0],path+' seller slug must not become a manufacturer part number')
                check(nodes[0].get('aggregateRating',{}).get('@type')=='AggregateRating',path+' missing product aggregateRating')
                rev=nodes[0].get('review')
                has_rev=(isinstance(rev,dict) and rev.get('@type')=='Review') or (isinstance(rev,list) and len(rev)>0 and rev[0].get('@type')=='Review')
                check(has_rev,path+' missing product review')
                offer=nodes[0].get('offers',{})
                check(offer.get('price')==p['price'] and offer.get('priceCurrency')=='PKR',path+' incorrect structured price/currency')
                check(offer.get('url')==ORIGIN+path,path+' incorrect offer URL')
                # Product availability is required by Google Search Console for Product snippets
                check(offer.get('availability')=='https://schema.org/InStock',path+' missing or invalid availability')
                check(offer.get('itemCondition')=='https://schema.org/NewCondition',path+' missing or invalid itemCondition')
                check(offer.get('validFrom') in ('2026-10-26', '2026-10-26T00:00:00+05:00', '2026-10-29', '2026-10-29T00:00:00+05:00'),path+' missing or invalid validFrom')
                check('validThrough' not in offer,path+' validThrough should not be present on ordinary price offer')
                expected_pvu = SETTINGS.get('priceValidUntil', '2026-12-31')
                check(offer.get('priceValidUntil')==expected_pvu,path+f' missing or invalid priceValidUntil (expected {expected_pvu}, got {offer.get("priceValidUntil")})')
                check(offer.get('seller',{}).get('@id')==ORIGIN+'/#organization',path+' disconnected seller identity')
                check('warranty' not in nodes[0],path+' warranty should not be defined on product root')
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
                        check(target.path=='/'+WHATSAPP_NUMBER,path+' incorrect WhatsApp number')
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
    for bot in ('Googlebot','Bingbot','OAI-SearchBot','ChatGPT-User','PerplexityBot','ClaudeBot'):
        for path in pages:check(robots.can_fetch(bot,ORIGIN+path),bot+' blocked '+path)
    check(not robots.can_fetch('GPTBot',ORIGIN+'/'),'Training policy unintentionally permits GPTBot')
    check(ORIGIN+'/sitemap.xml' in (robots.site_maps() or []),'Robots sitemap missing')
    check((ROOT/'llms.txt').is_file() and (ROOT/'llms.txt').stat().st_size>100,'Missing or empty llms.txt')
    check((ROOT/'llms-full.txt').is_file() and (ROOT/'llms-full.txt').stat().st_size>200,'Missing or empty llms-full.txt')
    notfound=Page((ROOT/'404.html').read_text(encoding='utf-8'))
    check(any('noindex' in a.get('content','') for a in notfound.attrs('meta',name='robots')),'404 missing noindex')
    check('/404.html' not in canonical_paths,'404 included in sitemap')
    vis_404 = ' '.join(notfound.visible)
    leak_words = ['catalog.json', 'site-facts', 'TODO', 'FIXME', 'undefined', 'NaN', '{{', '}}', '[object', 'scratch', 'staging']
    for lw in leak_words:
        if lw in ('scratch', 'staging', 'TODO', 'FIXME', 'undefined', 'NaN'):
            pat = rf'\b{re.escape(lw)}\b'
        else:
            pat = re.escape(lw)
        check(not bool(re.search(pat, vis_404)), f'/404.html leaked internal text found: {lw}')
    check(not bool(re.search(r'\.json\b', vis_404)), '/404.html leaked internal text found: .json')
    check(not bool(re.search(r'\bNone\b', vis_404)), '/404.html leaked internal text found: None')
    report={'pages':len(pages),'unique_main_content_pages':len(main_content_fingerprints),'checks':checks,'errors':errors,'warnings':warnings,'max_crawl_depth':max(distances.values()),'external_links':sorted(external),'local_resources_checked':len(assets),'crawl_depth':distances}
    out=ROOT/'verification';out.mkdir(exist_ok=True)
    (out/'seo-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    csv_path = out / 'price-mentions.csv'
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = __import__('csv').writer(f)
        writer.writerow(['file', 'line', 'product', 'found price', 'expected price', 'period check', 'status'])
        for m in all_price_mentions:
            writer.writerow([m['file'], m['line'], m['product'], m['found_price'], m['expected_price'], m['period_check'], m['status']])
    status_counts = Counter(m['status'] for m in all_price_mentions)
    print(f"Total price mentions checked: {len(all_price_mentions)} (ok: {status_counts.get('ok', 0)}, mismatch: {status_counts.get('mismatch', 0)}, skipped: {status_counts.get('skipped', 0)})")
    print(json.dumps({k:v for k,v in report.items() if k not in ('external_links','crawl_depth')},indent=2))
    return bool(errors)

if __name__=='__main__':sys.exit(run())
