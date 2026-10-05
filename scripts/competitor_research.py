"""Research-only, one sample per domain; robots required, no redirects/challenge bypass."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from datetime import datetime, timezone
import json, time

ROOT=Path(__file__).resolve().parents[1]
AGENT='AIToolsZoneResearch/1.0 (+https://aitoolszone.tech/about/)'
SAMPLES=[('TAAFT','https://theresanaiforthat.com/','directory'),('Futurepedia','https://www.futurepedia.io/ai-tools/productivity','category'),('Toolify','https://www.toolify.ai/','directory'),('TopAI','https://topai.tools/','directory'),('FutureTools','https://www.futuretools.io/','directory'),('AIxploria','https://www.aixploria.com/en/categories-ai/','category'),('AI Tools Pak','https://aitoolspak.tech/','marketplace'),('Bunny Tools','https://www.bunnytools.store/','marketplace')]
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
opener=build_opener(NoRedirect())
def fetch(url):
    with opener.open(Request(url,headers={'User-Agent':AGENT}),timeout=20) as r:
        return r.read(1500000).decode('utf-8','replace')
class Sample(HTMLParser):
    def __init__(self):
        super().__init__();self.title=[];self.headings=[];self.paths=set();self.schemas=set();self.capture='';self.buffer=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('title','h1','h2') or tag=='script' and a.get('type')=='application/ld+json': self.capture=tag;self.buffer=[]
        if tag=='a':
            url=urlparse(a.get('href',''))
            if not url.netloc and url.path.startswith('/'):
                part=url.path.strip('/').split('/')[0]
                if part and len(part)<35:self.paths.add('/'+part+'/')
    def handle_data(self,text):
        if self.capture:self.buffer.append(text)
    def handle_endtag(self,tag):
        if tag!=self.capture:return
        text=' '.join(''.join(self.buffer).split())
        if tag=='title':self.title.append(text)
        elif tag in ('h1','h2'):self.headings.append(text)
        else:
            def walk(value):
                if isinstance(value,dict):
                    t=value.get('@type',[]);self.schemas.update([t] if isinstance(t,str) else t)
                    for v in value.values():walk(v)
                elif isinstance(value,list):
                    for v in value:walk(v)
            try:walk(json.loads(text))
            except (ValueError,TypeError):pass
        self.capture=''
def run():
    now=datetime.now(timezone.utc);results=[]
    for name,url,kind in SAMPLES:
        row={'name':name,'url':url,'page_type':kind,'collected_at':now.isoformat(),'research_only':True}
        try:
            parsed=urlparse(url);robots_url=f'{parsed.scheme}://{parsed.netloc}/robots.txt'
            robots=RobotFileParser();robots.parse(fetch(robots_url).splitlines())
            if not robots.can_fetch(AGENT,url):row['status']='skipped: robots disallow'
            else:
                delay=max(2,robots.crawl_delay(AGENT) or 0)
                rate=robots.request_rate(AGENT)
                if rate:delay=max(delay,rate.seconds/rate.requests)
                if delay>30:raise ValueError('crawl delay exceeds bounded session')
                time.sleep(delay);html=fetch(url)
                if any(x in html.lower() for x in ['verify you are human','cf-chl-','captcha','access denied']):row['status']='skipped: access challenge detected'
                else:
                    sample=Sample();sample.feed(html);words=24;snippets=[]
                    for s in sample.title[:1]+sample.headings[:2]:
                        chunk=s.split()[:words];snippets.append(' '.join(chunk));words-=len(chunk)
                    row.update(status='sampled',title=snippets[0] if snippets else '',headings=snippets[1:],schema_types=sorted(sample.schemas),navigation_prefixes=sorted(sample.paths)[:30],content_gap_notes='Human review required; no automatic ranking conclusions.')
        except (HTTPError,OSError,ValueError) as exc:row['status']='skipped: '+str(exc)[:180]
        results.append(row);print(name+': '+row['status'],flush=True)
    out=ROOT/'data/competitor-intelligence';out.mkdir(parents=True,exist_ok=True)
    (out/(now.date().isoformat()+'.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':run()
