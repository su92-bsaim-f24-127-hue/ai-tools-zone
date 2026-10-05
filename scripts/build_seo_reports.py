"""Generate reviewable page inventory/readiness evidence; never packaged into the site."""
from pathlib import Path
import csv,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from audit_growth import run
assert not run(),'Fix audit findings before preparing reports'
pages=json.loads((ROOT/'verification/page-inventory.json').read_text(encoding='utf-8'))
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
