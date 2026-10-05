"""Additional release contracts, offer/CTA parity and a complete public-page inventory."""
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse, urljoin, parse_qs
import csv,json,re,subprocess
from audit_seo import Page, file_for, ORIGIN, ROOT

class InventoryPage(Page):
    def __init__(self,text):
        self.headings=[];self.heading=None;self.heading_text=[]
        super().__init__(text)
    def handle_starttag(self,tag,attrs):
        super().handle_starttag(tag,attrs)
        if re.fullmatch('h[1-6]',tag):self.heading=tag;self.heading_text=[]
    def handle_data(self,text):
        super().handle_data(text)
        if self.heading:self.heading_text.append(text)
    def handle_endtag(self,tag):
        super().handle_endtag(tag)
        if tag==self.heading:
            self.headings.append((tag,' '.join(''.join(self.heading_text).split())));self.heading=None

SECRET_PATTERNS=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'\bgh[pousr]_[A-Za-z0-9]{30,}',r'\bgithub_pat_[A-Za-z0-9_]{40,}',r'\bAKIA[0-9A-Z]{16}\b',r'\bsk-(?:proj-)?[A-Za-z0-9_-]{35,}']
def secret_findings(text):return [pattern for pattern in SECRET_PATTERNS if re.search(pattern,text)]
def contract_errors(contract,state,products):
    errors=[]
    if len(state)!=contract['expected_pages'] or sorted(state)!=contract['routes']:errors.append('Unexpected public routes/page count; document reason and review contract')
    if {p['id']:p['slug'] for p in products}!=contract['product_slugs']:errors.append('Product slug changed: preserve URL or implement and verify redirect before updating contract')
    if not contract.get('reason'):errors.append('Missing page-count change reason')
    return errors
def run():
    state=json.loads((ROOT/'data/page-state.json').read_text());products=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
    contract=json.loads((ROOT/'data/seo-contract.json').read_text());errors=contract_errors(contract,state,products);checks=3
    def check(ok,msg):
        nonlocal checks
        checks+=1
        if not ok:errors.append(msg)
    pages={p:InventoryPage(file_for(p).read_text(encoding='utf-8')) for p in [*state,'/404.html']}
    incoming=Counter();records=[];by_id={p['id']:p for p in products}
    for path,page in pages.items():
        internal=[];outgoing=[]
        for a in page.attrs('a'):
            href=a.get('href','');u=urlparse(urljoin(ORIGIN+path,href))
            check(href!='#',path+' placeholder navigation')
            if u.netloc=='aitoolszone.tech':
                internal.append(u.path)
                if u.path!=path:incoming[u.path]+=1
            else:outgoing.append(u.netloc)
            if a.get('data-product-id'):
                p=by_id.get(a['data-product-id']);message=parse_qs(u.query).get('text',[''])[0]
                check(bool(p) and u.netloc=='wa.me' and u.path=='/923430173923' and all(str(v) in message for v in [p['name'],f"{p['price']:,}",p['duration'],p['access'],ORIGIN+'/products/'+p['slug']+'/']),path+' order message differs from catalog')
        levels=[int(h[0][1]) for h in page.headings]
        check(all(b<=a+1 for a,b in zip(levels,levels[1:])),path+' heading level skipped')
        visible=' '.join(page.visible)
        check(not re.search(r'\blorem ipsum\b|\bTODO\b|\bPLACEHOLDER\b|\bguaranteed (?:ranking|rankings|AI citations)\b',visible,re.I),path+' placeholder/unsupported guarantee')
        schemas=[n for raw in page.schemas for n in json.loads(raw).get('@graph',[])]
        ids=[n['@id'] for n in schemas if '@id' in n]
        check(len(ids)==len(set(ids)),path+' duplicate schema node IDs')
        def nodes(value):
            if isinstance(value,dict):
                yield value
                for v in value.values():yield from nodes(v)
            elif isinstance(value,list):
                for v in value:yield from nodes(v)
        check(not any(n.get('@type') in ('Review','AggregateRating') or 'aggregateRating' in n or 'review' in n for n in nodes(schemas)),path+' unsupported review/rating')
        for node in schemas:
            if node.get('@type')=='BreadcrumbList':check(node.get('@id')==ORIGIN+path+'#breadcrumb',path+' unstable breadcrumb ID')
            if node.get('@type')=='Product':check(node['offers'].get('@id')==ORIGIN+path+'#offer',path+' unstable offer ID')
        meta={a.get('name',a.get('property')):a.get('content') for a in page.attrs('meta')}
        kind=path.strip('/').split('/')[0] or 'home'
        records.append({'path':path,'url':ORIGIN+path,'canonical':[a['href'] for a in page.attrs('link',rel='canonical')],'title':page.titles,'description':meta.get('description'),'h1':page.h1,'headings':page.headings,'robots':meta.get('robots'),'indexable':path in state,'word_count':len(visible.split()),'internal_links':sorted(set(internal)),'outgoing_hosts':sorted(set(outgoing)),'schema_types':[n.get('@type') for n in schemas],'social':{k:v for k,v in meta.items() if k and k.startswith(('og:','twitter:'))},'images':page.attrs('img'),'breadcrumbs':bool(page.attrs('nav',**{'aria-label':'Breadcrumb'})),'intent':'commercial offer evaluation' if kind in ('home','products','categories','pricing','compare','alternatives') else 'buying information / trust','answer_opportunity':'Listed price with duration/access' if kind in ('products','pricing','compare') else 'Task selection, access definitions and next buying step','content_lastmod':state.get(path,{}).get('lastmod'),'structured_parity':'Automated metadata/offer checks; external entitlements need owner verification'})
    for row in records:row['incoming_links']=incoming[row['path']]
    key=json.loads((ROOT/'data/indexnow.json').read_text())['key']
    check(bool(re.fullmatch('[a-f0-9]{32}',key)) and (ROOT/(key+'.txt')).read_text().strip()==key,'IndexNow host proof missing')
    # Scan tracked text plus current source additions. Never scan private/unrelated output directories.
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    tracked+=['search.js','audit_growth.py','test_growth.py']+[p.relative_to(ROOT).as_posix() for p in (ROOT/'scripts').glob('*.py')]
    for name in set(tracked):
        file=ROOT/name
        if file.is_file() and file.suffix in ('.js','.py','.json','.html','.yml','.md','.txt','.csv'):
            check(not secret_findings(file.read_text(encoding='utf-8',errors='replace')),name+' potential credential; inspect before publishing')
    out=ROOT/'verification';out.mkdir(exist_ok=True)
    (out/'page-inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={'checks':checks,'errors':errors,'indexable_pages':len(state),'inventoried_pages':len(records),'product_offers':len(products),'incoming_links':sum(incoming.values())}
    (out/'growth-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return bool(errors)
if __name__=='__main__':raise SystemExit(run())
