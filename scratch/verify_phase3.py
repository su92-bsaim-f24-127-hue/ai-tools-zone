import json
import re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qs, unquote
import xml.etree.ElementTree as ET

ROOT = Path('.')
ORIGIN = 'https://aitoolszone.tech'

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.schemas = []
        self.titles = []
        self.h1s = []
        self.h2s = []
        self.visible = []
        self.capture = None
        self.buf = []
        self.ignore = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag in ('title', 'h1', 'h2') or (tag == 'script' and attrs.get('type') == 'application/ld+json'):
            self.capture = tag
            self.buf = []
        if tag in ('script', 'style'):
            self.ignore = True

    def handle_endtag(self, tag):
        if self.capture == tag:
            text = ''.join(self.buf).strip()
            if tag == 'title': self.titles.append(text)
            elif tag == 'h1': self.h1s.append(text)
            elif tag == 'h2': self.h2s.append(text)
            elif tag == 'script': self.schemas.append(text)
            self.capture = None
        if tag in ('script', 'style'):
            self.ignore = False

    def handle_data(self, data):
        if self.capture:
            self.buf.append(data)
        if not self.ignore:
            self.visible.append(data)

def run_checks():
    report = {}
    
    # 1. Sitemap verification
    sitemap = ET.parse('sitemap.xml').getroot()
    urls = [node.text for node in sitemap.findall('{*}url/{*}loc')]
    report['sitemap_url_count'] = len(urls)
    report['sitemap_unique'] = len(urls) == len(set(urls))
    
    # 2. Canonical matching
    canonical_mismatches = []
    h1_issues = []
    schemas_verified = []
    meta_descriptions = {}
    whatsapp_links_checked = 0
    whatsapp_errors = []
    sticky_bars_checked = 0
    sticky_bar_errors = []
    
    catalog = json.loads(Path('data/catalog.json').read_text(encoding='utf-8'))
    products = {p['slug']: p for p in catalog}
    
    for u in urls:
        path = urlparse(u).path
        file_path = ROOT / (path.lstrip('/') + 'index.html' if path != '/' else 'index.html')
        if not file_path.exists():
            canonical_mismatches.append(f'File missing for {u}')
            continue
        html = file_path.read_text(encoding='utf-8')
        insp = Inspector()
        insp.feed(html)
        
        # Check canonical tag
        canonical_tag = [a.get('href') for t, a in insp.tags if t == 'link' and a.get('rel') == 'canonical']
        if canonical_tag != [u]:
            canonical_mismatches.append(f'{path}: expected {u}, got {canonical_tag}')
            
        # Check H1 count
        if len(insp.h1s) != 1:
            h1_issues.append(f'{path}: has {len(insp.h1s)} H1s ({insp.h1s})')
            
        # Check description length
        desc = [a.get('content') for t, a in insp.tags if t == 'meta' and a.get('name') == 'description']
        if desc:
            meta_descriptions[path] = desc[0]
            
        # Check Product Page specific requirements
        if path.startswith('/products/'):
            slug = path.split('/')[2]
            p = products.get(slug)
            if p:
                # Check Sticky Bar
                if 'class="mobile-sticky-bar"' in html:
                    sticky_bars_checked += 1
                    # Verify sticky bar price and accessibility
                    if f'PKR {p["price"]:,}' not in html:
                        sticky_bar_errors.append(f'{slug}: price PKR {p["price"]} missing in sticky bar')
                    if 'aria-label="Quick WhatsApp order bar"' not in html:
                        sticky_bar_errors.append(f'{slug}: sticky bar missing aria-label')
                    if 'data-web-enhanced="true"' not in html:
                        sticky_bar_errors.append(f'{slug}: sticky bar missing data-web-enhanced attribute')
                else:
                    sticky_bar_errors.append(f'{slug}: missing .mobile-sticky-bar')
                
                # Check WhatsApp message and URL
                wa_links = [a.get('href') for t, a in insp.tags if t == 'a' and 'wa.me' in a.get('href', '')]
                for wa_href in wa_links:
                    whatsapp_links_checked += 1
                    parsed_wa = urlparse(wa_href)
                    if parsed_wa.path != '/923430173923':
                        whatsapp_errors.append(f'{slug}: incorrect WA number in {wa_href}')
                    query = parse_qs(parsed_wa.query)
                    if 'text' in query:
                        msg = query['text'][0]
                        if p['name'] not in msg or f'PKR {p["price"]:,}' not in msg:
                            whatsapp_errors.append(f'{slug}: message missing name or price')
                
                # Check Structured Data
                product_schema_found = False
                for s_raw in insp.schemas:
                    try:
                        s_obj = json.loads(s_raw)
                        nodes = s_obj.get('@graph', [s_obj])
                        for n in nodes:
                            if n.get('@type') == 'Product':
                                product_schema_found = True
                                offer = n.get('offers', {})
                                if offer.get('validFrom') != '2026-01-01':
                                    whatsapp_errors.append(f'{slug}: Offer missing validFrom: 2026-01-01')
                                if offer.get('priceValidUntil') != '2026-12-31':
                                    whatsapp_errors.append(f'{slug}: Offer missing priceValidUntil: 2026-12-31')
                                if offer.get('availability') != 'https://schema.org/InStock':
                                    whatsapp_errors.append(f'{slug}: Offer missing InStock')
                                if offer.get('price') != p['price']:
                                    whatsapp_errors.append(f'{slug}: Offer price mismatch')
                    except Exception as err:
                        whatsapp_errors.append(f'{slug}: JSON-LD parse error: {err}')
                if not product_schema_found:
                    whatsapp_errors.append(f'{slug}: Product schema not found')

    report['canonical_mismatches'] = canonical_mismatches
    report['h1_issues'] = h1_issues
    report['sticky_bars_checked'] = sticky_bars_checked
    report['sticky_bar_errors'] = sticky_bar_errors
    report['whatsapp_links_checked'] = whatsapp_links_checked
    report['whatsapp_errors'] = whatsapp_errors
    
    # 3. Four comparison pages verification
    comp_pages = [
        '/compare/chatgpt-vs-claude/',
        '/compare/leonardo-vs-midjourney/',
        '/compare/capcut-vs-runway/',
        '/compare/canva-vs-adobe/'
    ]
    comp_results = {}
    for cp in comp_pages:
        html = (ROOT / cp.lstrip('/') / 'index.html').read_text(encoding='utf-8')
        insp = Inspector()
        insp.feed(html)
        has_table = '<table class="plan-table">' in html
        has_faq = 'Questions before you choose' in html or 'faq' in html.lower()
        has_sources = 'Official product references' in html or 'official' in html.lower()
        comp_results[cp] = {
            'title': insp.titles[0] if insp.titles else None,
            'h1': insp.h1s[0] if insp.h1s else None,
            'has_comparison_table': has_table,
            'has_faq': has_faq,
            'has_sources': has_sources,
            'word_count': len(' '.join(insp.visible).split())
        }
    report['comparison_pages'] = comp_results
    
    # 4. Robots.txt verification
    robots_txt = Path('robots.txt').read_text(encoding='utf-8')
    report['robots_has_sitemap'] = 'Sitemap: https://aitoolszone.tech/sitemap.xml' in robots_txt
    report['robots_blocks_gptbot'] = 'User-agent: GPTBot\nDisallow: /' in robots_txt
    report['robots_allows_claude_search'] = 'User-agent: Claude-SearchBot\nAllow: /' in robots_txt
    report['robots_allows_perplexity'] = 'User-agent: PerplexityBot\nAllow: /' in robots_txt
    report['robots_allows_oai'] = 'User-agent: OAI-SearchBot\nAllow: /' in robots_txt
    
    # 5. Top 5 product meta description inspection
    top5_slugs = ['chatgpt-plus', 'capcut-pro', 'canva-pro-edu', 'adobe-creative-cloud', 'youtube-premium']
    top5_desc = {s: meta_descriptions.get(f'/products/{s}/') for s in top5_slugs}
    report['top5_meta_descriptions'] = top5_desc
    
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    run_checks()
