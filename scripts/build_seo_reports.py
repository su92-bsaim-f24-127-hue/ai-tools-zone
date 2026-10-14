"""Generate reviewable page inventory/readiness evidence; never packaged into the site."""
from pathlib import Path
import csv,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from audit_growth import run
assert not run(),'Fix audit findings before preparing reports'
pages=json.loads((ROOT/'verification/page-inventory.json').read_text(encoding='utf-8'))
live_path=ROOT/'verification/seo-live-after.json'
live=json.loads(live_path.read_text(encoding='utf-8')) if live_path.exists() else {}
live_by_url={r.get('url'):r for r in live.get('results',[])}
followup_path=ROOT/'verification/seo-live-followup.json'
followup=json.loads(followup_path.read_text(encoding='utf-8')) if followup_path.exists() else {}
live_by_url.update({r.get('url'):r for r in followup.get('results',[])})
checked_at=live.get('checked_at_utc','')
def live_fields(page):
    result=live_by_url.get(page.get('url'))
    fields={'live_http_status':'not checked','live_final_url':'','live_redirect_count':'','live_checked_at_utc':checked_at,'live_verification':'not checked'}
    if not result:
        if page.get('path')=='/404.html':fields['live_verification']='excluded from sitemap'
        return fields
    status=result.get('status')
    fields.update({'live_http_status':status if status is not None else 'unverified','live_final_url':result.get('final',''),'live_redirect_count':len(result.get('redirects',[])),'live_checked_at_utc':followup.get('checked_at_utc',checked_at) if result in followup.get('results',[]) else checked_at,'live_verification':'unverified' if result.get('classification','').startswith('unverified') or status is None else 'verified'})
    return fields
pages=[{**page,**live_fields(page)} for page in pages]
out=ROOT/'reports';out.mkdir(exist_ok=True)
with (out/'seo-page-inventory.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(pages[0]));writer.writeheader()
    writer.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in p.items()} for p in pages)
rows=[]
for p in pages:
    if not p['indexable']:continue
    product='Product' in p['schema_types'];sourced=any(h not in ('wa.me','fonts.googleapis.com') for h in p['outgoing_hosts'])
    # 1=observable signal present; 0=not observed; U=requires a human/source check.
    # Presence is not proof of factual truth, editorial quality, trust or a citation.
    rows.append({'path':p['path'],'crawlability':1,'indexability':1,'factual_clarity':1 if product or p['path']=='/pricing/' else 'U','entity_clarity':1,'direct_answers':'U','evidence':'U','source_attribution':1 if sourced else 0,'originality':'U','internal_links':1 if p['incoming_links'] and p['internal_links'] else 0,'structured_data':1,'freshness':1 if p['content_lastmod'] else 0,'trust':'U','conversion_clarity':1 if 'wa.me' in p['outgoing_hosts'] else 0,'next_review':'Verify plan entitlements, actual availability and whether the direct answer fully satisfies its intent; no citation prediction.'})
with (out/'citation-readiness.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print(f'Inventory: {len(pages)} pages including 404. Readiness: {len(rows)} canonical pages; unknowns are explicit.')
