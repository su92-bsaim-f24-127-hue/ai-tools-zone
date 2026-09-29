"""Regression checks for stable freshness and production packaging."""
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import date
from zipfile import ZipFile
import hashlib,json,subprocess,sys
import seo_pages
ROOT=Path(__file__).parent

with TemporaryDirectory() as directory:
    original_root=seo_pages.ROOT
    seo_pages.ROOT=Path(directory)
    def write(path,text):
        target=seo_pages.ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    def record():return json.loads((seo_pages.ROOT/'data/page-state.json').read_text())['/']
    try:
        html='<title>Test</title><main><h1>A real plan</h1><p>PKR 100</p></main><script src="app.js?v=one"></script><style>p{color:red}</style>'
        write('index.html',html);seo_pages.finalize(['/'],'https://example.test',write)
        state=record();state['lastmod']='2020-01-02';write('data/page-state.json',json.dumps({'/':state}))
        write('index.html',html.replace('v=one','v=two').replace('color:red','color:blue'))
        seo_pages.finalize(['/'],'https://example.test',write)
        assert record()==state,'Asset/cache/style changes must not pretend content is fresh'
        write('index.html',html.replace('PKR 100','PKR 200'));seo_pages.finalize(['/'],'https://example.test',write)
        assert record()['lastmod']==date.today().isoformat() and record()['sha256']!=state['sha256'],'A changed visible price must update freshness'
    finally:seo_pages.ROOT=original_root

subprocess.run([sys.executable,str(ROOT/'build_site.py')],cwd=ROOT,check=True,capture_output=True)
state=json.loads((ROOT/'data/page-state.json').read_text())
files=[ROOT/('index.html' if path=='/' else path.strip('/')+'/index.html') for path in state]
files += [ROOT/'sitemap.xml',ROOT/'data/page-state.json',ROOT/'catalog.js',ROOT/'robots.txt']
snapshot={f:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
subprocess.run([sys.executable,str(ROOT/'build_site.py')],cwd=ROOT,check=True,capture_output=True)
assert snapshot=={f:hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'Build output must be deterministic'
subprocess.run([sys.executable,str(ROOT/'package_site.py')],cwd=ROOT,check=True,capture_output=True)
with ZipFile(ROOT/'ai-tools-zone.zip') as archive:
    names=set(archive.namelist())
    assert all(f.relative_to(ROOT).as_posix() in names for f in files if f.parent!=ROOT/'data'),'Missing generated production file'
    assert not any(n.startswith(('data/','templates/','.git/','.tools/','verification/','tmp/','output/')) or n.endswith(('.py','.md','.env')) for n in names),'Development or private file packaged'
    assert 'CNAME' in names and 'measurement.js' in names and '404.html' in names
print('PASS: meaningful freshness, unchanged-date preservation, deterministic build and safe production package.')
