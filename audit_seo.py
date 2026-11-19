"""Dependency-free production SEO regression audit. Run after build_site.py."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote, parse_qs
from urllib.robotparser import RobotFileParser
from collections import Counter, deque
from datetime import date, timedelta
import json
import re
import sys
from hashlib import sha256
import xml.etree.ElementTree as ET
from seo_pages import content_date

ROOT=Path(__file__).parent
ORIGIN='https://aitoolszone.tech'
SETTINGS=json.loads((ROOT/'data/site-settings.json').read_text(encoding='utf-8'))
WHATSAPP_NUMBER=''.join(ch for ch in SETTINGS['whatsappNumber'] if ch.isdigit())
FOLDERS=('products','categories','use-cases','compare','alternatives','guides','pricing','blog','about','privacy','terms','faq','buy-ai-tools-in-pakistan','how-to-buy-chatgpt-plus-in-pakistan','best-ai-tools-for-students-pakistan','ai-video-editing-tools-pakistan','ai-image-generator-subscriptions-pakistan')

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.titles=[]; self.h1=[]; self.schemas=[]; self.visible=[]
        self.capture=None; self.buffer=[]; self.ignore=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if tag in ('title','h1') or (tag=='script' and attrs.get('type')=='application/ld+json'):
            self.capture=tag; self.buffer=[]
        if tag in ('script','style'): self.ignore+=1
    def handle_endtag(self, tag):
        if self.capture==tag:
            text=''.join(self.buffer).strip()
            if tag=='title':self.titles.append(text)
            elif tag=='h1':self.h1.append(text)
            else:self.schemas.append(text)
            self.capture=None
        if tag in ('script','style'): self.ignore=max(0,self.ignore-1)
    def handle_data(self, text):
        if self.capture:self.buffer.append(text)
        if not self.ignore:self.visible.append(text)
    def attrs(self, tag, **match):
        return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in match.items())]

def file_for(path):
    clean=unquote(path).lstrip('/')
    return ROOT/(clean+'index.html' if not clean or clean.endswith('/') else clean)


def evaluate_period(target_text, p):
    target_text = re.sub(r'\b(final|first|gap|second|third|multi)-year\b', r'\1_academic_yr', target_text, flags=re.I)
    dur = p["duration"]
    found_words = re.findall(r'\b(lifetime|one-time|months?|mo|years?|yrs?)\b', target_text, re.I)
    if not found_words:
        return "not applicable"
    has_lifetime = bool(re.search(r'\b(lifetime|one-time)\b', target_text, re.I))
    if has_lifetime:
        return "ok" if dur == "Lifetime" else "mismatch"
    if dur == "Lifetime":
        return "mismatch"
    if dur in ["8,500 Credits", "40 USD Credits", "Confirm before ordering"]:
        return "mismatch"
    if dur == "1 Month":
        if re.search(r'\b(years?|yrs?)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b([2-9]|\d{2,})\s*(months?|mo)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*month|1-month|month|monthly|mo|1\s*mo)\b', target_text, re.I): return "ok"
        return "mismatch"
    if dur == "2 Months":
        if re.search(r'\b(years?|yrs?|lifetime|one-time)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*month|1-month|3\s*months?|18\s*months?)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(2\s*months?|2-month|2\s*mo)\b', target_text, re.I): return "ok"
        return "mismatch"
    if dur == "3 Months":
        if re.search(r'\b(years?|yrs?|lifetime|one-time)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*month|1-month|2\s*months?|18\s*months?)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(3\s*months?|3-month|3\s*mo)\b', target_text, re.I): return "ok"
        return "mismatch"
    if dur == "1 Year":
        if re.search(r'\b(months?|mo|lifetime|one-time)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(2\s*years?|2-year)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*year|1-year|year|annual|annually|1\s*yr|yr)\b', target_text, re.I): return "ok"
        return "mismatch"
    if dur == "2 Years":
        if re.search(r'\b(months?|mo|lifetime|one-time)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(1\s*year|1-year)\b', target_text, re.I): return "mismatch"
        if re.search(r'\b(2\s*years?|2-year|2\s*yrs?)\b', target_text, re.I): return "ok"
        return "mismatch"
    return "not applicable"

def run():
    errors=[]; warnings=[]; checks=0
    def check(value,message):
        nonlocal checks
        checks+=1
        if not value:errors.append(message)
    sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
    urls=[n.text for n in sitemap.findall('{*}url/{*}loc')]
    check(len(urls)==len(set(urls)),'Duplicate sitemap URLs')
    canonical_paths={urlparse(u).path for u in urls}
    files=[ROOT/'index.html']+[p for folder in FOLDERS for p in (ROOT/folder).rglob('*.html')]
    pages={('/' if f==ROOT/'index.html' else '/'+f.relative_to(ROOT).as_posix().removesuffix('index.html')):Page(f.read_text(encoding='utf-8')) for f in files}
    check(set(pages)==canonical_paths,'Generated pages and sitemap differ')
    check(all(u==ORIGIN+urlparse(u).path and u.endswith('/') for u in urls),'Sitemap has noncanonical/query URLs')
    states=json.loads((ROOT/'data/page-state.json').read_text())
    for node in sitemap.findall('{*}url'):
        path=urlparse(node.find('{*}loc').text).path
        lastmod=node.find('{*}lastmod')
        check(lastmod is not None and date.fromisoformat(lastmod.text)<=content_date(),path+' invalid lastmod')
        check(lastmod is not None and lastmod.text==states.get(path,{}).get('lastmod'),path+' lastmod differs from source record')
    catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
    products_checked = 0
    badge_conflicts = 0
    desc_conflicts = 0
    for p in catalog:
        products_checked += 1
        badge = p.get('badge', '')
        dur = p.get('duration', '')
        acc = p.get('access', '')
        
        # Badge checks: "N-Year Plan", "N-Month Plan", "Shared Access", "Private", "Invitation"
        m_year = re.search(r'(\d+)-Year Plan', badge, re.I)
        if m_year:
            n_years = m_year.group(1)
            expected_dur = f"{n_years} Year" if n_years == '1' else f"{n_years} Years"
            if dur != expected_dur:
                badge_conflicts += 1
                check(False, f"Badge duration mismatch for {p['id']}: badge has '{badge}', duration is '{dur}'")
                
        m_month = re.search(r'(\d+)-Month Plan', badge, re.I)
        if m_month:
            n_months = m_month.group(1)
            expected_dur = f"{n_months} Month" if n_months == '1' else f"{n_months} Months"
            if dur != expected_dur:
                badge_conflicts += 1
                check(False, f"Badge duration mismatch for {p['id']}: badge has '{badge}', duration is '{dur}'")
                
        if re.search(r'Shared Access', badge, re.I) and acc != 'Shared':
            badge_conflicts += 1
            check(False, f"Badge access mismatch for {p['id']}: badge has '{badge}', access is '{acc}'")
            
        if re.search(r'\bPrivate\b', badge, re.I) and acc != 'Private':
            badge_conflicts += 1
            check(False, f"Badge access mismatch for {p['id']}: badge has '{badge}', access is '{acc}'")
            
        if re.search(r'\bInvitation\b', badge, re.I) and acc != 'Invitation':
            badge_conflicts += 1
            check(False, f"Badge access mismatch for {p['id']}: badge has '{badge}', access is '{acc}'")

        # Description check on catalog description: check PKR amounts, "for N months", "per month", "per year", "N-year", "N-month", access types, delivery ranges, warranty days
        desc = p.get('description', '')
        dl = desc.lower()
        m_price = re.search(r'PKR\s+([\d,]+)', desc)
        if m_price:
            desc_price = int(m_price.group(1).replace(',', ''))
            if desc_price != p['price']:
                desc_conflicts += 1
                check(False, f"Catalog description price mismatch for {p['id']}: description has PKR {desc_price}, field has PKR {p['price']}")
                
        m_m = re.search(r'(\d+)-month|for (\d+) months?', dl)
        if m_m:
            n = m_m.group(1) or m_m.group(2)
            exp = f"{n} Month" if n == '1' else f"{n} Months"
            if dur != exp:
                desc_conflicts += 1
                check(False, f"Catalog description duration mismatch for {p['id']}: description has '{exp}', field has '{dur}'")
        if 'per month' in dl and dur != '1 Month':
            desc_conflicts += 1
            check(False, f"Catalog description duration mismatch for {p['id']}: description has 'per month', field has '{dur}'")
        if 'per year' in dl and dur != '1 Year':
            desc_conflicts += 1
            check(False, f"Catalog description duration mismatch for {p['id']}: description has 'per year', field has '{dur}'")
        m_y = re.search(r'(\d+)-year|for (\d+) years?', dl)
        if m_y:
            n = m_y.group(1) or m_y.group(2)
            exp = f"{n} Year" if n == '1' else f"{n} Years"
            if dur != exp:
                desc_conflicts += 1
                check(False, f"Catalog description duration mismatch for {p['id']}: description has '{exp}', field has '{dur}'")

        if 'private access' in dl and acc != 'Private':
            desc_conflicts += 1
            check(False, f"Catalog description access mismatch for {p['id']}: description has 'Private', field has '{acc}'")
        if 'shared access' in dl and acc != 'Shared':
            desc_conflicts += 1
            check(False, f"Catalog description access mismatch for {p['id']}: description has 'Shared', field has '{acc}'")
        if 'invitation access' in dl and acc != 'Invitation':
            desc_conflicts += 1
            check(False, f"Catalog description access mismatch for {p['id']}: description has 'Invitation', field has '{acc}'")
        if 'license key' in dl and acc != 'License Key':
            desc_conflicts += 1
            check(False, f"Catalog description access mismatch for {p['id']}: description has 'License Key', field has '{acc}'")

        deliv = p['delivery'].replace('-', '–')
        if '15 to 30 minutes' in dl and deliv != '15–30 min':
            desc_conflicts += 1
            check(False, f"Catalog description delivery mismatch for {p['id']}: description has '15 to 30 minutes', field has '{deliv}'")
        if '30 to 60 minutes' in dl and deliv != '30–60 min':
            desc_conflicts += 1
            check(False, f"Catalog description delivery mismatch for {p['id']}: description has '30 to 60 minutes', field has '{deliv}'")
        if '1 to 2 hours' in dl and deliv != '1–2 hours':
            desc_conflicts += 1
            check(False, f"Catalog description delivery mismatch for {p['id']}: description has '1 to 2 hours', field has '{deliv}'")

        warr = p['warranty']
        if '7 days' in dl and warr != '7 Days':
            desc_conflicts += 1
            check(False, f"Catalog description warranty mismatch for {p['id']}: description has '7 days', field has '{warr}'")
        if '30 days' in dl and warr != '30 Days':
            desc_conflicts += 1
            check(False, f"Catalog description warranty mismatch for {p['id']}: description has '30 days', field has '{warr}'")
        if 'no replacement warranty' in dl and warr != 'No Warranty':
            desc_conflicts += 1
            check(False, f"Catalog description warranty mismatch for {p['id']}: description has 'No Warranty', field has '{warr}'")

    print(f"Description & badge audit: {products_checked} products checked, {desc_conflicts + badge_conflicts} conflicts (must be 0)")

    PLAN_WORDS = ['Pro', 'Plus', 'Premium', 'Essential', 'Edu', 'Starter', 'Business', 'Creator', 'Unlimited', 'Core', 'Private', 'Key', '4K']
    plan_regex = re.compile(rf'\b(?:{"|".join(PLAN_WORDS)})\b', re.I)
    extra_names = {
        "Gamma App": "gamma-pro",
        "Google Gemini Pro": "gemini-pro",
        "Google Veo": "veo-3-ultra",
        "Leonardo AI": "leonardo-ai-essential",
        "Runway": "runway-ml-gen-3",
        "Copilot": "github-copilot",
        "Notion": "notion-business",
        "Figma": "figma-pro-private",
        "Canva Pro": "canva-pro-edu",
    }
    p_by_slug = {p["slug"]: p for p in catalog}
    alias_to_product = {}
    for p in catalog:
        alias_to_product[p["name"]] = p
    for p in catalog:
        stripped = plan_regex.sub('', p["name"])
        stripped = ' '.join(stripped.split()).strip()
        if stripped and stripped != p["name"] and len(stripped) >= 3:
            if stripped not in alias_to_product:
                alias_to_product[stripped] = p
    for alias, slug in extra_names.items():
        if slug in p_by_slug:
            alias_to_product[alias] = p_by_slug[slug]
    sorted_aliases = sorted(alias_to_product.keys(), key=lambda a: len(a), reverse=True)
    catalog_products = sorted(catalog, key=lambda p: len(p['name']), reverse=True)
    products={'/products/'+p['slug']+'/':p for p in catalog}
    graph={path:set() for path in pages}; inbound=Counter(); descriptions=[]; titles=[]; external=set(); assets=set()
    main_content_fingerprints={}
    all_price_mentions=[]
    for path,page in pages.items():
        check(len(page.titles)==1 and bool(page.titles[0]),path+' needs one title')
        check(len(page.h1)==1 and bool(page.h1[0]),path+' needs one H1')
        page_html=file_for(path).read_text(encoding='utf-8')
        main_match=re.search(r'<main\b[^>]*>(.*?)</main>',page_html,re.S|re.I)
        main_text=' '.join(' '.join(Page(main_match.group(1) if main_match else '').visible).split()).casefold()
        check(bool(main_text),path+' missing visible main content')
        clean_html = re.sub(r'no official affiliation[^<.]*', '', page_html, flags=re.I)
        clean_html = re.sub(r'visit the official product website[^<.]*', '', clean_html, flags=re.I)
        clean_html = re.sub(r'official vendor usage limits[^<.]*', '', clean_html, flags=re.I)
        clean_html = re.sub(r'not an authorized distributor or partner', '', clean_html, flags=re.I)
        forbidden_terms = [
            (r'\bauthorized\b', 'authorized'),
            (r'\bgenuine\b', 'genuine'),
            (r'\bauthentic\b', 'authentic'),
            (r'military-grade', 'military-grade'),
            (r'official\s+retail', 'official retail'),
            (r'\bforever\b', 'forever'),
            (r'\btypically\b', 'typically'),
            (r'\baccredited\b', 'accredited'),
            (r'\bseamlessly\b', 'seamlessly'),
            (r'\bindustry-leading\b', 'industry-leading'),
            (r'\bsecurely\b', 'securely'),
            (r'\bpirated\b', 'pirated'),
            (r'\bcracked\b', 'cracked'),
            (r'\bmalware\b', 'malware'),
            (r'high reliability', 'high reliability'),
            (r'\bessential for\b', 'essential for'),
            (r'\beliminating\b', 'eliminating'),
            (r'confirms that all features', 'confirms that all features'),
            (r'\bfully active\b', 'fully active'),
            (r'peace of mind', 'peace of mind'),
            (r'100% safe', '100% safe'),
            (r'\bguaranteed\b', 'guaranteed'),
            (r'tied directly to your registered email', 'tied directly to your registered email'),
            (r'\bretail\s+(?:key|license|activation)\b', 'retail key/license/activation'),
            (r'\b25-digit\b', '25-digit'),
            (r'completely private', 'completely private'),
            (r'100%\s*private', '100% private'),
            (r'zero buffering', 'zero buffering'),
            (r'\bperfect for\b', 'perfect for'),
            (r'\bexceptional\b', 'exceptional'),
            (r'\bmassive\b', 'massive'),
            (r'\bincredible\b', 'incredible'),
            (r'\bpristine\b', 'pristine'),
            (r'\bcomprehensive\b', 'comprehensive'),
            (r'household verification', 'household verification'),
            (r'\bproduction-grade\b', 'production-grade'),
            (r'\bstudio-grade\b', 'studio-grade'),
            (r'\b10Gbps\b', '10Gbps'),
            (r'\bhigh-accuracy\b', 'high-accuracy'),
            (r'with high precision', 'with high precision'),
            (r'zero international card decline', 'zero international card decline'),
            (r'last 90 days', 'last 90 days'),
            (r'completely untouched', 'completely untouched'),
            (r'\bROI\b', 'ROI'),
            (r'return on investment', 'return on investment'),
            (r'bypassing the 10% withholding tax', 'bypassing 10% withholding tax'),
            (r'zero\b[^\.]*\bbank withholding taxes', 'zero bank withholding taxes'),
            (r'without international forex taxes', 'without international forex taxes'),
            (r'without bank forex tax', 'without bank forex tax'),
            (r'bank tax withholding', 'bank tax withholding'),
            (r'advance tax surcharges', 'advance tax surcharges'),
            (r'tax surcharges', 'tax surcharges'),
            (r'~PKR\s*5,800', '~PKR 5,800'),
            (r'PKR\s*6,000\+', 'PKR 6,000+'),
            (r'17,000\+\s*with taxes', '17,000+ with taxes'),
        ]
        for pat, label in forbidden_terms:
            check(not bool(re.search(pat, clean_html, re.I)), path + f' forbidden term found: {label}')
        # Tax percentage audit: allow only 0.5% and 1.0%, and only inside card_tax_note
        tax_pct_matches = list(re.finditer(r'(?:(\d+(?:\.\d+)?%)\s*(?:[^\w\n]+\w+){0,3}\s*tax|tax\s*(?:[^\w\n]+\w+){0,3}\s*(\d+(?:\.\d+)?%))', clean_html, re.I))
        for tpm in tax_pct_matches:
            pct = tpm.group(1) or tpm.group(2)
            if pct not in ('0.5%', '1.0%'):
                check(False, path + f' unauthorized tax percentage found: {tpm.group(0)}')
            else:
                m_start = tpm.start()
                context_snippet = clean_html[max(0, m_start-200):min(len(clean_html), m_start+200)]
                context_snippet_clean = ' '.join(context_snippet.split())
                if "Section 236Y" not in context_snippet_clean or "Active Taxpayers List" not in context_snippet_clean:
                    check(False, path + f' tax percentage {pct} found outside card_tax_note: {tpm.group(0)}')

        # Universal % sign audit: any % sign outside the tax note fails the build
        for v_chunk in page.visible:
            if '%' in v_chunk:
                v_lower = v_chunk.lower()
                is_tax_note = ('0.5%' in v_chunk or '1.0%' in v_chunk) and ('236y' in v_lower or 'active taxpayers list' in v_lower or 'withholding' in v_lower or 'advance tax' in v_lower)
                check(is_tax_note, path + f' unauthorized % sign found: {v_chunk.strip()[:80]}')

        # Leaked internal text audit: fail if visible text contains internal leak words
        vis_text = ' '.join(page.visible)
        leak_words = ['catalog.json', 'site-facts', 'TODO', 'FIXME', 'undefined', 'NaN', '{{', '}}', '[object', 'scratch', 'staging']
        for lw in leak_words:
            if lw in ('scratch', 'staging', 'TODO', 'FIXME', 'undefined', 'NaN'):
                pat = rf'\b{re.escape(lw)}\b'
            else:
                pat = re.escape(lw)
            check(not bool(re.search(pat, vis_text)), path + f' leaked internal text found: {lw}')
        check(not bool(re.search(r'\.json\b', vis_text)), path + ' leaked internal text found: .json')
        check(not bool(re.search(r'\bNone\b', vis_text)), path + ' leaked internal text found: None')

        # External anchor words audit: fail if anchor contains banned words unless in URL path
        banned_anchor_words = ['official', 'technical', 'specifications', 'standards', 'guidelines', 'framework', 'safeguards', 'licensing', 'compliance']
        for a_match in re.finditer(r'<a\b[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>', page_html, re.S|re.I):
            href = a_match.group(1)
            if 'aitoolszone.tech' in href or 'wa.me' in href:
                continue
            anchor_text = re.sub(r'<[^>]+>', ' ', a_match.group(2)).strip()
            u_path = urlparse(href).path.lower()
            for bw in banned_anchor_words:
                if re.search(rf'\b{re.escape(bw)}\b', anchor_text, re.I):
                    check(bw in u_path, path + f' banned word "{bw}" in external anchor "{anchor_text}" for {href}')

        if path.startswith('/products/'):
            check(not bool(re.search(r'\bofficial\b', clean_html, re.I)), path + ' unauthorized official claim on product page')
        # Check Table Rows for product and price
        html_lines = page_html.splitlines()
        rel_file = path.strip('/') + '/index.html' if path != '/' else 'index.html'
        for tr_match in re.finditer(r'<tr\b[^>]*>(.*?)</tr>', page_html, re.S|re.I):
            tr_content = tr_match.group(1)
            line_num = page_html[:tr_match.start()].count('\n') + 1
            cells = re.findall(r'<(?:th|td)\b[^>]*>(.*?)</(?:th|td)>', tr_content, re.S|re.I)
            if not cells: continue
            clean_cells = [__import__('html').unescape(' '.join(re.sub(r'<[^>]+>', ' ', c).split())) for c in cells]
            for alias in sorted_aliases:
                p = alias_to_product[alias]
                prod_cell_idx = next((i for i, c in enumerate(clean_cells) if re.search(rf'\b{re.escape(alias)}\b', c, re.I)), None)
                if prod_cell_idx is not None:
                    price_candidates = []
                    for c in clean_cells:
                        for pm in re.finditer(r'PKR\s*([0-9,]+)', c, re.I):
                            is_official = '$' in c or '~' in c
                            price_candidates.append((int(pm.group(1).replace(',', '')), c, is_official))
                    if not price_candidates: continue
                    exact_cands = [cand for cand in price_candidates if cand[0] == p['price']]
                    best_cand = exact_cands[0] if exact_cands else ([cand for cand in price_candidates if not cand[2]] or price_candidates)[0]
                    found_price = best_cand[0]
                    exp_price = p['price']
                    period_res = evaluate_period(best_cand[1], p)
                    if period_res == "not applicable":
                        period_res = evaluate_period(' '.join(clean_cells), p)
                    status = "ok"
                    if found_price != exp_price or period_res == "mismatch":
                        status = "mismatch"
                    all_price_mentions.append({
                        "file": rel_file, "line": line_num, "product": p['name'],
                        "found_price": found_price, "expected_price": exp_price,
                        "period_check": period_res, "status": status
                    })
                    if status == "mismatch":
                        check(False, f"{path}:{line_num} price/period mismatch in table row for {p['name']}: found PKR {found_price} (expected {exp_price}), period {period_res}")
                    break

        # Check Sentences outside tables
        clean_no_tables = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', page_html, flags=re.S|re.I)
        clean_no_tables = re.sub(r'<tr\b[^>]*>.*?</tr>', ' ', clean_no_tables, flags=re.S|re.I)
        clean_no_tables = re.sub(r'</(p|li|h[1-6]|div|article|section|aside|dd|dt|header|footer|nav)>|<br\s*/?>', '.\n', clean_no_tables, flags=re.I)
        clean_no_tables = re.sub(r'<[^>]+>', ' ', clean_no_tables)
        clean_no_tables = __import__('html').unescape(clean_no_tables)
        for line in [l.strip() for l in clean_no_tables.split('\n') if l.strip()]:
            current_named_product = products.get(path)
            for s in re.split(r'(?<=[.!?])\s+', line):
                s_clean = ' '.join(s.split())
                if not s_clean: continue
                # Update current_named_product if any product is named in this sentence
                for alias in sorted_aliases:
                    if re.search(rf'\b{re.escape(alias)}\b', s_clean, re.I):
                        current_named_product = alias_to_product[alias]
                        break
                alias_matches = []
                for alias in sorted_aliases:
                    p = alias_to_product[alias]
                    for m in re.finditer(rf'\b{re.escape(alias)}\b.{{0,60}}?PKR\s*([0-9,]+)', s_clean, re.I):
                        start_idx = m.start()
                        end_idx = m.end()
                        intervening = s_clean[start_idx + len(alias):end_idx]
                        if any(other_a != alias and re.search(rf'\b{re.escape(other_a)}\b', intervening, re.I) for other_a in sorted_aliases):
                            continue
                        if any(other_a != alias and len(other_a) > len(alias) and s_clean[start_idx:start_idx+len(other_a)].lower() == other_a.lower() for other_a in sorted_aliases):
                            continue
                        alias_matches.append((start_idx, end_idx, alias, p, m.group(1).replace(',', '')))
                # Pronoun resolution: "it", "this plan", "AI Tools Zone lists it"
                if not alias_matches and current_named_product is not None:
                    m_pronoun = re.search(r'\b(?:AI Tools Zone lists it|this plan|it)\b.{0,60}?PKR\s*([0-9,]+)', s_clean, re.I)
                    if m_pronoun:
                        alias_matches.append((m_pronoun.start(), m_pronoun.end(), current_named_product['name'], current_named_product, m_pronoun.group(1).replace(',', '')))
                # Check stated bundle totals
                total_matches = [int(m.group(1).replace(',', '')) for m in re.finditer(r'(?:first-period cost.*?(?:is|of)\s*PKR|combined.*?(?:cost|is)\s*PKR|total.*?PKR|cost.*?PKR)\s*([0-9,]+)', s_clean, re.I)]
                under_matches = [int(m.group(1).replace(',', '')) for m in re.finditer(r'under\s*PKR\s*([0-9,]+)\s*(?:total|combined)', s_clean, re.I)]
                if total_matches or under_matches:
                    found_prods = []
                    for alias in sorted_aliases:
                        if re.search(rf'\b{re.escape(alias)}\b', s_clean, re.I):
                            p = alias_to_product[alias]
                            if p['slug'] not in [x['slug'] for x in found_prods]:
                                if not any(re.search(rf'\b{re.escape(other_a)}\b', s_clean, re.I) and len(other_a) > len(alias) and alias.lower() in other_a.lower() for other_a in sorted_aliases):
                                    found_prods.append(p)
                    if len(found_prods) >= 2:
                        computed_sum = sum(prod['price'] for prod in found_prods)
                        line_num = 1
                        for idx_raw, raw_line in enumerate(html_lines, 1):
                            if s_clean[:30] in raw_line or (len(s_clean) > 15 and s_clean[:15] in raw_line):
                                line_num = idx_raw
                                break
                        if under_matches:
                            for limit in under_matches:
                                check(computed_sum < limit, f"{path}:{line_num} bundle total mismatch: sum {computed_sum} >= limit {limit} in '{s_clean}'")
                        if total_matches:
                            for stated in total_matches:
                                check(computed_sum == stated, f"{path}:{line_num} bundle total mismatch: sum {computed_sum} != stated {stated} in '{s_clean}'")
                if not alias_matches:
                    continue
                alias_matches.sort(key=lambda x: (x[0], -len(x[2])))
                filtered_matches = []
                last_end = -1
                for am in alias_matches:
                    if am[0] >= last_end:
                        filtered_matches.append(am)
                        last_end = am[1]
                for idx_pm, (start_p, end_p, alias, p, price_str) in enumerate(filtered_matches):
                    try: found_price = int(price_str)
                    except ValueError: continue
                    exp_price = p['price']
                    pname = p['name']
                    line_num = 1
                    for idx_raw, raw_line in enumerate(html_lines, 1):
                        if s_clean[:30] in raw_line or (len(s_clean) > 15 and s_clean[:15] in raw_line):
                            line_num = idx_raw
                            break
                    if re.search(r'(range\s+from\b.*?\bto\b|start\s+at\b.*?\bextending\s+to\b)', s_clean, re.I):
                        all_price_mentions.append({
                            "file": rel_file, "line": line_num, "product": pname,
                            "found_price": found_price, "expected_price": exp_price,
                            "period_check": "not applicable", "status": "skipped"
                        })
                        continue
                    next_start = filtered_matches[idx_pm + 1][0] if idx_pm + 1 < len(filtered_matches) else len(s_clean)
                    clause = s_clean[start_p:next_start]
                    period_res = evaluate_period(clause, p)
                    status = "ok"
                    if found_price != exp_price or period_res == "mismatch":
                        status = "mismatch"
                    all_price_mentions.append({
                        "file": rel_file, "line": line_num, "product": pname,
                        "found_price": found_price, "expected_price": exp_price,
                        "period_check": period_res, "status": status
                    })
                    if status == "mismatch":
                        check(False, f"{path}:{line_num} price/period mismatch in sentence for {pname}: found PKR {found_price} (expected {exp_price}), period {period_res} in '{s_clean}'")

        if main_text:
            fingerprint=sha256(main_text.encode('utf-8')).hexdigest()
            previous=main_content_fingerprints.get(fingerprint)
            check(previous is None,path+' duplicates visible main content from '+str(previous))
            if previous is None:main_content_fingerprints[fingerprint]=path
        titles+=page.titles
        description=page.attrs('meta',name='description')
        check(len(description)==1 and bool(description[0].get('content')),path+' missing description')
        descriptions += [x.get('content','') for x in description]
        check(page.attrs('link',rel='canonical')==[{'rel':'canonical','href':ORIGIN+path}],path+' canonical mismatch')
        check(not any('noindex' in a.get('content','') for a in page.attrs('meta',name='robots')),path+' noindex in sitemap')
        for prop in ('title','description','image','url','type','locale'):
            check(bool(page.attrs('meta',property='og:'+prop)),path+' missing OG '+prop)
        check(bool(page.attrs('meta',name='twitter:card')),path+' missing Twitter card')
        for rel in ('icon','manifest'):
            check(bool(page.attrs('link',rel=rel)),path+' missing '+rel)
        check(bool(page.attrs('html',lang='en-PK')),path+' incorrect document language')
        check(bool(page.attrs('main')),path+' missing main landmark')
        ids=[a['id'] for _,a in page.tags if 'id' in a]
        check(len(ids)==len(set(ids)),path+' duplicate HTML IDs')
        if len(' '.join(page.visible).split())<120:warnings.append(path+' short content: review purpose, not an automatic ranking issue')
        schema_nodes=[]
        for schema_raw in page.schemas:
            try:
                obj=json.loads(schema_raw); check(obj.get('@context')=='https://schema.org',path+' incorrect schema context'); schema_nodes.extend(obj.get('@graph',[obj]))
            except ValueError:check(False,path+' invalid JSON-LD')
        types=[n.get('@type') for n in schema_nodes]
        schema_ids=[n['@id'] for n in schema_nodes if '@id' in n]
        check(len(schema_ids)==len(set(schema_ids)),path+' duplicate schema entity definitions')
        for required in ['Organization','WebSite','WebPage']+(['BreadcrumbList'] if path!='/' else []):
            check(types.count(required)==1,path+' missing/duplicate '+required)
        if path!='/':
            nav=re.search(r'<nav aria-label="Breadcrumb">(.*?)</nav>',page_html,re.S)
            check(nav is not None,path+' missing visible breadcrumb')
            if nav:
                crumbs=[]
                for li in re.findall(r'<li\b([^>]*)>(.*?)</li>',nav[1],re.S):
                    if 'aria-hidden' in li[0]:continue
                    part=Page(li[1]);anchors=part.attrs('a')
                    crumbs.append((''.join(part.visible).strip(),urljoin(ORIGIN+path,anchors[0]['href']) if anchors else ORIGIN+path))
                nodes=[n for n in schema_nodes if n.get('@type')=='BreadcrumbList']
                if nodes:check(crumbs==[(n['name'],n['item']) for n in nodes[0]['itemListElement']],path+' visible/schema breadcrumb mismatch')
        reviews_file = ROOT / 'data/reviews.json'
        reviews_data = json.loads(reviews_file.read_text(encoding='utf-8')) if reviews_file.exists() else {}
        for n in schema_nodes:
            if n.get('@type')=='Product':
                if 'aggregateRating' in n:
                    p_slug = path.strip('/').split('/')[-1]
                    p_revs = reviews_data.get(p_slug, []) if isinstance(reviews_data, dict) else [r for r in reviews_data if r.get('product_slug')==p_slug or r.get('product_id')==p_slug]
                    consented = [r for r in p_revs if r.get('consent') is True]
                    stated_count = n['aggregateRating'].get('reviewCount', 0)
                    check(len(consented) >= stated_count and len(consented) > 0, path+' unverified aggregateRating without data/reviews.json source')
            if n.get('@type')=='Organization':
                check('hasMerchantReturnPolicy' not in n,path+' unsupported organization return policy')
        if path in products:
            p=products[path]; nodes=[n for n in schema_nodes if n.get('@type')=='Product']
            check(len(nodes)==1,path+' missing Product schema')
            if nodes:
                check(nodes[0].get('brand',{}).get('@type')=='Brand' and bool(nodes[0].get('brand',{}).get('name')),path+' missing product brand')
                check(nodes[0].get('sku')==p['slug'],path+' missing product sku')
                check('mpn' not in nodes[0],path+' seller slug must not become a manufacturer part number')
                p_slug = p['slug']
                p_revs = reviews_data.get(p_slug, reviews_data.get(p['id'], [])) if isinstance(reviews_data, dict) else [r for r in reviews_data if r.get('product_slug')==p_slug or r.get('product_id')==p['id']]
                consented = [r for r in p_revs if r.get('consent') is True]
                if 'aggregateRating' in nodes[0]:
                    stated_count = nodes[0]['aggregateRating'].get('reviewCount', 0)
                    check(len(consented) >= stated_count and len(consented) > 0, path+' unverified aggregateRating without data/reviews.json source')
                if 'review' in nodes[0]:
                    check(bool(consented), path+' unverified Review without data/reviews.json source')
                offer=nodes[0].get('offers',{})
                check(offer.get('price')==p['price'] and offer.get('priceCurrency')=='PKR',path+' incorrect structured price/currency')
                check(offer.get('url')==ORIGIN+path,path+' incorrect offer URL')
                check('availability' not in offer,path+' availability should not be present on offer')
                check('itemCondition' not in offer,path+' itemCondition should not be present on offer')
                check('validFrom' not in offer,path+' validFrom should not be present on ordinary price offer')
                check('validThrough' not in offer,path+' validThrough should not be present on ordinary price offer')
                expected_pvu = SETTINGS.get('priceValidUntil', '2026-12-31')
                check(offer.get('priceValidUntil')==expected_pvu,path+f' missing or invalid priceValidUntil (expected {expected_pvu}, got {offer.get("priceValidUntil")})')
                check(offer.get('seller',{}).get('@id')==ORIGIN+'/#organization',path+' disconnected seller identity')
                check('hasMerchantReturnPolicy' not in offer,path+' unexpected hasMerchantReturnPolicy on offer')
                check('shippingDetails' not in offer,path+' unexpected shippingDetails on digital product offer')
                check('warranty' not in nodes[0],path+' warranty should not be defined on product root')
                if p.get('warranty', '').strip().lower() in ('no warranty', 'none', 'no replacement warranty'):
                    check('warranty' not in offer,path+' unexpected warranty on offer for '+p['id'])
                else:
                    check(offer.get('warranty',{}).get('@type')=='WarrantyPromise',path+' missing warranty promise on offer')
                    check(offer.get('warranty',{}).get('durationOfWarranty',{}).get('unitCode')=='DAY',path+' missing warranty duration unit')
            visible=' '.join(page.visible)
            check(all(str(value) in visible for value in [p['name'],f'{p["price"]:,}',p['duration'],p['access']]),path+' incomplete initial HTML plan')
            if 'customer review' in visible.lower() or 'customer ratings' in visible.lower() or 'verified buyer' in visible.lower():
                check(bool(consented), path+' customer review/rating text found without data/reviews.json source')
            def _walk_nd(val):
                if isinstance(val, dict):
                    if 'reviewBody' in val: check(False, path+' reviewBody schema found without data/reviews.json source')
                    for v in val.values(): _walk_nd(v)
                elif isinstance(val, list):
                    for v in val: _walk_nd(v)
            _walk_nd(schema_nodes)
            check(any(a.get('href','').startswith('/categories/') for a in page.attrs('a')),path+' missing category link')
        for tag,attrs in page.tags:
            if tag=='img':
                check('alt' in attrs,path+' missing image alt attribute')
                check(attrs.get('width','').isdigit() and attrs.get('height','').isdigit(),path+' missing image dimensions')
            references=[]
            if tag in ('a','link') and attrs.get('href'):references.append(attrs['href'])
            if tag in ('img','script','source') and attrs.get('src'):references.append(attrs['src'])
            if tag in ('img','source') and attrs.get('srcset'):references.extend(x.strip().split()[0] for x in attrs['srcset'].split(','))
            for ref in references:
                target=urlparse(urljoin(ORIGIN+path,ref))
                if target.scheme not in ('http','https'):continue
                if target.netloc!='aitoolszone.tech':
                    if tag=='a':external.add(target.geturl())
                    if target.netloc=='wa.me':
                        check(target.path=='/'+WHATSAPP_NUMBER,path+' incorrect WhatsApp number')
                        if path in products and 'text' in parse_qs(target.query):
                            order=parse_qs(target.query)['text'][0]
                            check(products[path]['name'] in order and f'{products[path]["price"]:,}' in order,path+' stale WhatsApp order')
                    continue
                dest=file_for(target.path)
                check(dest.is_file(),path+' broken local URL '+ref)
                if target.path in pages and tag=='a':
                    graph[path].add(target.path)
                    if target.path!=path:inbound[target.path]+=1
                    if target.fragment:
                        check(any(a.get('id')==unquote(target.fragment) for _,a in pages[target.path].tags),path+' missing anchor '+ref)
                elif dest.is_file() and tag!='a':assets.add(dest)
    for value,count in Counter(titles).items():check(count==1,'Duplicate title: '+value)
    for value,count in Counter(descriptions).items():check(count==1,'Duplicate description: '+value)
    distances={'/':0}; queue=deque(['/'])
    while queue:
        path=queue.popleft()
        for dest in graph[path]:
            if dest not in distances:distances[dest]=distances[path]+1;queue.append(dest)
    for path in pages:
        check(path in distances,path+' unreachable from homepage')
        check(path=='/' or inbound[path]>0,path+' orphan page')
    for asset in assets:
        if asset.suffix in ('.png','.webp','.jpg','.svg') and asset.stat().st_size>300000:warnings.append(str(asset.relative_to(ROOT))+' image exceeds 300 KB')
    robots=RobotFileParser(); robots.parse((ROOT/'robots.txt').read_text().splitlines())
    for bot in ('Googlebot','Bingbot','OAI-SearchBot','ChatGPT-User','PerplexityBot','ClaudeBot'):
        for path in pages:check(robots.can_fetch(bot,ORIGIN+path),bot+' blocked '+path)
    check(not robots.can_fetch('GPTBot',ORIGIN+'/'),'Training policy unintentionally permits GPTBot')
    check(ORIGIN+'/sitemap.xml' in (robots.site_maps() or []),'Robots sitemap missing')
    check((ROOT/'llms.txt').is_file() and (ROOT/'llms.txt').stat().st_size>100,'Missing or empty llms.txt')
    check((ROOT/'llms-full.txt').is_file() and (ROOT/'llms-full.txt').stat().st_size>200,'Missing or empty llms-full.txt')
    notfound=Page((ROOT/'404.html').read_text(encoding='utf-8'))
    check(any('noindex' in a.get('content','') for a in notfound.attrs('meta',name='robots')),'404 missing noindex')
    check('/404.html' not in canonical_paths,'404 included in sitemap')
    vis_404 = ' '.join(notfound.visible)
    for lw in leak_words:
        if lw in ('scratch', 'staging', 'TODO', 'FIXME', 'undefined', 'NaN'):
            pat = rf'\b{re.escape(lw)}\b'
        else:
            pat = re.escape(lw)
        check(not bool(re.search(pat, vis_404)), f'/404.html leaked internal text found: {lw}')
    check(not bool(re.search(r'\.json\b', vis_404)), '/404.html leaked internal text found: .json')
    check(not bool(re.search(r'\bNone\b', vis_404)), '/404.html leaked internal text found: None')
    report={'pages':len(pages),'unique_main_content_pages':len(main_content_fingerprints),'checks':checks,'errors':errors,'warnings':warnings,'max_crawl_depth':max(distances.values()),'external_links':sorted(external),'local_resources_checked':len(assets),'crawl_depth':distances}
    out=ROOT/'verification';out.mkdir(exist_ok=True)
    (out/'seo-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    csv_path = out / 'price-mentions.csv'
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = __import__('csv').writer(f)
        writer.writerow(['file', 'line', 'product', 'found price', 'expected price', 'period check', 'status'])
        for m in all_price_mentions:
            writer.writerow([m['file'], m['line'], m['product'], m['found_price'], m['expected_price'], m['period_check'], m['status']])
    status_counts = Counter(m['status'] for m in all_price_mentions)
    print(f"Total price mentions checked: {len(all_price_mentions)} (ok: {status_counts.get('ok', 0)}, mismatch: {status_counts.get('mismatch', 0)}, skipped: {status_counts.get('skipped', 0)})")
    print(json.dumps({k:v for k,v in report.items() if k not in ('external_links','crawl_depth')},indent=2))
    return bool(errors)

if __name__=='__main__':sys.exit(run())
