"""Package the built static site only, without development files or original oversized assets."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
root=Path(__file__).parent
production=['index.html','404.html','styles.css','enhancements.css','catalog.js','app.js','theme.js','scene.js','favicon.ico','site.webmanifest','robots.txt','sitemap.xml','_headers']
production += ['CNAME', '.nojekyll']
production += [p.relative_to(root).as_posix() for folder in ['products','about','privacy','terms'] for p in (root/folder).rglob('*.html')]
production += ['assets/'+name for name in ['brand-emblem.webp','brand-icon.webp','brand-wordmark.webp','hero-logo-3d.webp','hero-logo-3d-mobile.webp','icon-32.png','icon-48.png','icon-180.png','icon-192.png','icon-512.png','social-card.jpg','product-logo-sources.json']]
logos=json.loads((root/'assets/product-logo-sources.json').read_text(encoding='utf-8'))
production += [item['path'] for item in logos.values()]
with ZipFile(root/'ai-tools-zone.zip','w',ZIP_DEFLATED) as archive:
    for file in dict.fromkeys(production):
        assert (root/file).is_file(), file
        archive.write(root/file,file)
    for doc in ['README.md','SEO-PLAN.md','AUDIT.md']:
        if (root/doc).exists(): archive.write(root/doc,doc)
print(json.dumps({'archive':'ai-tools-zone.zip','size_bytes':(root/'ai-tools-zone.zip').stat().st_size,'production_files':len(set(production)),'domain':'https://aitoolszone.tech'},indent=2))
