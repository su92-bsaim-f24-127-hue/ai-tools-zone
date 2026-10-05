"""Meaningful mutation tests: route contracts, credential guard and IndexNow deltas."""
import json
from audit_growth import ROOT,contract_errors,secret_findings
from scripts.indexnow import changed
state=json.loads((ROOT/'data/page-state.json').read_text());catalog=json.loads((ROOT/'data/catalog.json').read_text());contract=json.loads((ROOT/'data/seo-contract.json').read_text())
assert not contract_errors(contract,state,catalog)
assert contract_errors(contract,{**state,'/accidental/':{}},catalog)
mutated=[dict(p) for p in catalog];mutated[0]['slug']='accidental-new-url'
assert contract_errors(contract,state,mutated)
assert secret_findings('gh'+'p_'+'a'*36)
assert not secret_findings('d2b7303797fa48c694dde2b0ff780947')
assert changed({'/same/':{'sha256':'1'},'/gone/':{'sha256':'2'},'/edit/':{'sha256':'a'}},{'/same/':{'sha256':'1'},'/new/':{'sha256':'3'},'/edit/':{'sha256':'b'}})==['/edit/','/gone/','/new/']
assert changed(state,state)==[]
print('PASS: 7 growth regression assertions (unexpected routes/slugs, credential guard, changed/deleted/added/no-change notifications).')
