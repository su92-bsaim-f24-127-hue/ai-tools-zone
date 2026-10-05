"""Submit meaningful public URL changes after successful deployment. Default: dry run.
IndexNow keys prove host control; they are intentionally public, not API secrets.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import argparse,json,subprocess,time

ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://aitoolszone.tech'
def changed(before,after):
    return sorted(p for p in set(before)|set(after) if before.get(p,{}).get('sha256')!=after.get(p,{}).get('sha256'))
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--submit',action='store_true');parser.add_argument('--base-ref',default='HEAD^');args=parser.parse_args()
    before=json.loads(subprocess.check_output(['git','show',args.base_ref+':data/page-state.json'],cwd=ROOT))
    after=json.loads((ROOT/'data/page-state.json').read_text());paths=changed(before,after)
    assert all(p.startswith('/') and p.endswith('/') and '?' not in p and '#' not in p and '..' not in p and not p.startswith('//') for p in paths)
    config=json.loads((ROOT/'data/indexnow.json').read_text());key=config['key']
    payload={'host':'aitoolszone.tech','key':key,'keyLocation':ORIGIN+'/'+key+'.txt','urlList':[ORIGIN+p for p in paths]}
    report={'mode':'submit' if args.submit else 'dry-run','urls':payload['urlList'],'status':'no changes' if not paths else 'prepared'}
    if args.submit and paths:
        assert len(paths)<=10000,'Split batches explicitly before submitting more than 10,000 URLs'
        # Pages may take a short time to reach the edge after deploy-pages succeeds.
        for attempt in range(3):
            try:
                with urlopen(payload['keyLocation'],timeout=20) as r:assert r.read().decode().strip()==key,'Live proof mismatch'
                break
            except (OSError,AssertionError):
                if attempt==2:raise
                time.sleep(5)
        request=Request('https://api.indexnow.org/indexnow',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json; charset=utf-8','User-Agent':'AIToolsZoneIndexNow/1.0'},method='POST')
        try:
            with urlopen(request,timeout=30) as response:
                report.update(http_status=response.status,status='received; indexing not guaranteed')
        except HTTPError as error:
            report.update(http_status=error.code,status='not accepted; review response',response=error.read(1000).decode('utf-8','replace'))
    out=ROOT/'verification';out.mkdir(exist_ok=True)
    (out/'indexnow.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    if report.get('http_status',200) not in (200,202):raise SystemExit(1)
if __name__=='__main__':main()
