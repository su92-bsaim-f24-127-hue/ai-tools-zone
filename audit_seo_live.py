"""Fetch each sitemap page and outbound destination; no messages or payments sent.

Usage: python audit_seo_live.py [--external]
External anti-bot/access failures are reported as unverified, not declared broken.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from datetime import datetime, timezone
import json, sys, xml.etree.ElementTree as ET
from audit_seo import Page
ROOT=Path(__file__).parent
class RedirectRecorder(__import__('urllib.request',fromlist=['HTTPRedirectHandler']).HTTPRedirectHandler):
    def __init__(self):self.chain=[]
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        self.chain.append({'status':code,'from':req.full_url,'to':newurl})
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def fetch(url):
    from urllib.request import build_opener
    redirect=RedirectRecorder();opener=build_opener(redirect)
    try:
        r=opener.open(Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; AI-Tools-Zone-audit/1.0)'}),timeout=25)
        body=r.read().decode('utf-8','replace');page=Page(body)
        return {'url':url,'status':r.status,'final':r.url,'redirects':redirect.chain,'canonical':page.attrs('link',rel='canonical'),'titles':page.titles,'h1_count':len(page.h1),'schema_types':[n.get('@type') for raw in page.schemas for n in json.loads(raw).get('@graph',[json.loads(raw)])],'robots':page.attrs('meta',name='robots'),'headers':dict(r.headers)}
    except HTTPError as error:
        return {'url':url,'status':error.code,'redirects':redirect.chain,'classification':'missing' if error.code in (404,410) else 'unverified-access-response'}
    except Exception as error:return {'url':url,'error':str(error),'classification':'unverified'}
def main():
    external='--external' in sys.argv
    if external:
        links=json.loads((ROOT/'verification/seo-audit.json').read_text())['external_links']
        urls=sorted(set(u.split('#')[0] for u in links if urlparse(u).hostname!='wa.me'))
    else:
        sitemap=urlopen('https://aitoolszone.tech/sitemap.xml',timeout=20).read()
        urls=[n.text for n in ET.fromstring(sitemap).findall('{*}url/{*}loc')]
        urls+=['http://aitoolszone.tech/','https://www.aitoolszone.tech/','http://www.aitoolszone.tech/','https://aitoolszone.tech/products/chatgpt-plus','https://aitoolszone.tech/no-such-page-seo-audit/','https://aitoolszone.tech/?category=design']
    results=list(ThreadPoolExecutor(max_workers=6).map(fetch,urls))
    failures=[]
    if not external:
        expected=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
        if urls[:-6]!=expected:failures.append('Live sitemap differs from current build')
        for r in results[:-6]:
            if r.get('status')!=200 or r.get('h1_count')!=1 or r.get('canonical')!=[{'rel':'canonical','href':r['url']}]:failures.append(r['url']+' page/canonical mismatch')
            if not {'WebPage','Organization','WebSite'}.issubset(set(r.get('schema_types',[]))):failures.append(r['url']+' missing entity graph')
        for r in results[-6:-2]:
            if r.get('status')!=200 or not r.get('redirects') or not r.get('final','').startswith('https://aitoolszone.tech/'):failures.append(r['url']+' redirect mismatch')
        if results[-2].get('status')!=404:failures.append('Unknown route does not return HTTP 404')
        if results[-1].get('canonical')!=[{'rel':'canonical','href':'https://aitoolszone.tech/'}]:failures.append('Query-string home does not canonicalize cleanly')
    report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'external':external,'failures':failures,'results':results}
    dest=ROOT/'verification'/('seo-external.json' if external else 'seo-live-after.json');dest.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'checked':len(results),'failures':failures,'status_counts':{str(code):sum(r.get('status')==code for r in results) for code in set(r.get('status') for r in results)},'unverified':[r['url'] for r in results if r.get('classification')=='unverified' or r.get('status') in (403,429)],'missing':[r['url'] for r in results if r.get('status') in (404,410)]},indent=2))
    if failures:sys.exit(1)
if __name__=='__main__':main()
