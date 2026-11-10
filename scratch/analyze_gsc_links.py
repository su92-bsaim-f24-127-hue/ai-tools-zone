from pathlib import Path
import re
from urllib.parse import urlparse, urljoin

gsc_22 = [
    '/categories/design/',
    '/products/youtube-premium/',
    '/products/surfshark-vpn/',
    '/products/notion-business/',
    '/products/netflix-premium-4k/',
    '/products/linkedin-premium/',
    '/products/leonardo-ai-essential/',
    '/products/gamma-pro/',
    '/products/elevenlabs/',
    '/products/capcut-pro/',
    '/compare/helium10-vs-semrush-vs-vidiq/',
    '/compare/grammarly-vs-quillbot-vs-wordai/',
    '/compare/elevenlabs-vs-playht/',
    '/compare/claude-vs-gemini/',
    '/compare/chatgpt-vs-gemini/',
    '/compare/chatgpt-vs-claude/',
    '/compare/capcut-vs-runway/',
    '/compare/canva-vs-adobe/',
    '/compare/',
    '/blog/ai-tools-for-teachers-pakistan/',
    '/blog/ai-phone-agents-whatsapp-bots-pakistan/',
    '/use-cases/ai-tools-for-students/'
]

root = Path('.')
html_files = [f for f in root.glob('**/*.html') if 'verification' not in str(f) and 'node_modules' not in str(f)]
inbound = {u: set() for u in gsc_22}

for f in html_files:
    source = '/' + f.relative_to(root).as_posix().removesuffix('index.html')
    if source == '//': source = '/'
    content = f.read_text(encoding='utf-8')
    for href in re.findall(r'href=["\']([^"\']+)["\']', content):
        target = urlparse(urljoin('https://aitoolszone.tech' + source, href)).path
        if target in inbound and source != target:
            inbound[target].add(source)

print('=== ACCURATE INCOMING LINK COUNTS FOR 22 DISCOVERED URLS ===')
for u in sorted(gsc_22):
    sources = list(inbound[u])
    from_home = '/' in sources
    print(f'{u}: {len(sources)} linking pages | Direct from Home: {from_home}')
