"""Meaningful mutation tests: route contracts, credential guard and IndexNow deltas."""
import json
from audit_growth import ROOT,contract_errors,secret_findings,is_production_asset,audit_asset_secrets
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

# Regression Test 1: Production assets containing a genuine secret are detected
assert is_production_asset('index.html')
assert is_production_asset('build_site.py')
assert is_production_asset('.github/workflows/pages.yml')
assert audit_asset_secrets('index.html', 'gh'+'p_'+'a'*36) == 'index.html potential credential; inspect before publishing'
assert audit_asset_secrets('build_site.py', '-----BEGIN RSA PRIVATE KEY-----') == 'build_site.py potential credential; inspect before publishing'

# Regression Test 2: Test fixtures do not cause production asset false positives
assert not is_production_asset('scripts/telemetry/test_normalizer.py')
assert not is_production_asset('test_growth.py')
assert audit_asset_secrets('scripts/telemetry/test_normalizer.py', '-----BEGIN RSA PRIVATE KEY-----') is None
assert audit_asset_secrets('test_growth.py', 'gh'+'p_'+'a'*36) is None

# Regression Test 3: Historical documentation does not cause production asset false positives
assert not is_production_asset('seo-growth-2026/phase-5/phase_5_5f_h_telemetry_release_readiness_audit.md')
assert not is_production_asset('reports/seo-telemetry/weekly_seo_performance.md')
assert audit_asset_secrets('seo-growth-2026/phase-5/phase_5_5f_h_telemetry_release_readiness_audit.md', '-----BEGIN RSA PRIVATE KEY-----') is None

# Regression Test 4: Existing security checks remain active
assert secret_findings('AKIA1234567890123456')
assert secret_findings('sk-proj-12345678901234567890123456789012345')

print('PASS: 11 growth regression assertions (unexpected routes/slugs, credential guard, changed/deleted/added/no-change notifications, test/doc boundaries).')
