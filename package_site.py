from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json, re

root=Path(__file__).parent
production=['index.html','styles.css','catalog.js','app.js','scene.js','assets/favicon-logo.svg','assets/ai-tools-zone-logo.png']
with ZipFile(root/'ai-tools-zone.zip','w',ZIP_DEFLATED) as archive:
    for file in production:
        archive.write(root/file,file)
    archive.write(root/'README.md','README.md')

html=(root/'index.html').read_text(encoding='utf-8')
assert '03136726285' not in html  # International number is used in all links.
assert '923136726285' in html
assert 'PKR 7,400' in html
source=(root/'reference-app.js').read_text(encoding='utf-8')
original=source[source.index('const products = ['):source.index('const categoryData')].replace('const products =','window.PRODUCTS =')
assert (root/'catalog.js').read_text(encoding='utf-8') == original
print(json.dumps({'archive':'ai-tools-zone.zip','size_bytes':(root/'ai-tools-zone.zip').stat().st_size,'production_files':production,'catalog_exactly_matches_demo':True},indent=2))
