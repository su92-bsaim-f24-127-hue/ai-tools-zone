import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import json
import time
from urllib.parse import urlparse

ORIGIN = 'https://aitoolszone.tech'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-Tools-Zone-Live-Verifier/1.0'}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.getcode(), resp.read().decode('utf-8', errors='replace')

def main():
    print('=== VERIFYING LIVE PRODUCTION DEPLOYMENT ===')
    
    # 1. Sitemap
    sitemap_url = f'{ORIGIN}/sitemap.xml'
    code, sitemap_xml = fetch(sitemap_url)
    print(f'Sitemap ({sitemap_url}): HTTP {code}')
    assert code == 200, 'Sitemap failed'
    root = ET.fromstring(sitemap_xml)
    urls = [node.text for node in root.findall('{*}url/{*}loc')]
    print(f'Total URLs in live sitemap: {len(urls)}')
    assert len(urls) == 82, f'Expected 82 URLs in sitemap, got {len(urls)}'
    
    # 2. Robots.txt
    robots_url = f'{ORIGIN}/robots.txt'
    code, robots_txt = fetch(robots_url)
    print(f'Robots.txt ({robots_url}): HTTP {code}')
    assert 'Sitemap: https://aitoolszone.tech/sitemap.xml' in robots_txt
    assert 'User-agent: Claude-SearchBot' in robots_txt
    assert 'User-agent: GPTBot\nDisallow: /' in robots_txt
    print('Robots.txt directives verified!')
    
    # 3. Discovery files
    code, llms = fetch(f'{ORIGIN}/llms.txt')
    print(f'llms.txt: HTTP {code}')
    assert code == 200 and 'ChatGPT Plus' in llms
    code, llms_full = fetch(f'{ORIGIN}/llms-full.txt')
    print(f'llms-full.txt: HTTP {code}')
    assert code == 200 and '2,300' in llms_full
    
    # 4. Critical new & modified routes
    check_routes = [
        '/',
        '/products/chatgpt-plus/',
        '/products/capcut-pro/',
        '/products/canva-pro-edu/',
        '/products/adobe-creative-cloud/',
        '/products/youtube-premium/',
        '/compare/leonardo-vs-midjourney/',
        '/compare/canva-vs-adobe/',
        '/compare/capcut-vs-runway/',
        '/compare/chatgpt-vs-claude/',
        '/use-cases/ai-tools-for-students/'
    ]
    
    for r in check_routes:
        url = f'{ORIGIN}{r}'
        code, body = fetch(url)
        print(f'{r}: HTTP {code} ({len(body)} bytes)')
        assert code == 200, f'Route {r} returned {code}'
        if r.startswith('/products/'):
            assert 'mobile-sticky-bar' in body, f'{r} missing mobile-sticky-bar'
            assert 'validFrom":"2026-01-01"' in body or 'validFrom": "2026-01-01"' in body or '"validFrom":"2026-01-01"' in body, f'{r} missing validFrom'
        if r == '/products/chatgpt-plus/':
            assert '2,300' in body, 'ChatGPT missing PKR 2,300'
        if r == '/compare/leonardo-vs-midjourney/':
            assert 'Leonardo AI vs Midjourney' in body
            assert '<table class="plan-table">' in body
    
    # 5. Check all 82 canonical URLs
    print(f'Pinging all {len(urls)} canonical URLs on production...')
    failures = []
    for i, u in enumerate(urls):
        try:
            c, b = fetch(u)
            if c != 200:
                failures.append(f'{u}: HTTP {c}')
        except Exception as err:
            failures.append(f'{u}: {err}')
        if (i + 1) % 20 == 0 or (i + 1) == len(urls):
            print(f'Verified {i+1}/{len(urls)} routes...')
    
    if failures:
        print(f'FAILED ROUTES ({len(failures)}):')
        for f in failures:
            print(f)
        raise RuntimeError('Live verification failed!')
    else:
        print('ALL 82 CANONICAL ROUTES RETURNED HTTP 200 OK ON LIVE WEBSITE!')

if __name__ == '__main__':
    main()
