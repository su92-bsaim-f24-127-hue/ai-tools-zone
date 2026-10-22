"""Build a bounded, evidence-labeled keyword-to-page map.

Search demand, difficulty and Google indexing are not inferred from public page
samples. Unlisted products remain explicit gaps instead of getting doorway URLs.
"""
from pathlib import Path
from urllib.parse import urlsplit
import csv
import json
import re
from seo_pages import BLOG, CONTENT, category_path, product_path

ROOT = Path(__file__).parent
ORIGIN = 'https://aitoolszone.tech'
STATE = json.loads((ROOT / 'data/page-state.json').read_text(encoding='utf-8'))
CATALOG = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
rows = []


def search_intent(keyword, kind):
    q = keyword.casefold().strip()
    if 'ai tools zone' in q or 'aitoolszone' in q:
        return 'Navigational'
    if re.search(r'\b(buy|order|purchase|get access)\b', q):
        return 'Transactional'
    if re.search(r'\b(price|pricing|cost|pk(r|rs)|under|vs|versus|alternatives|compare|best)\b', q):
        return 'Commercial investigation'
    if kind in ('guides', 'trust') or re.match(r'^(what is|what are|what payment|what warranty|how do|how does|how long|difference between)\b', q):
        return 'Informational'
    if kind in ('home', 'catalog', 'product', 'pricing', 'category', 'use-case', 'compare', 'alternatives'):
        return 'Commercial investigation'
    return 'Informational'


def live_status(path):
    """Use only a recent, recorded live crawl; otherwise report the limit."""
    route = urlsplit(path).path or '/'
    report_path = ROOT / 'verification/seo-live-after.json'
    if report_path.is_file():
        try:
            report = json.loads(report_path.read_text(encoding='utf-8'))
            checked = report.get('checked_at_utc', '')[:10]
            result = next((r for r in report.get('results', [])
                           if urlsplit(r.get('url', '')).path == route
                           and urlsplit(r.get('url', '')).netloc == 'aitoolszone.tech'), None)
            if result and result.get('status') == 200:
                return f'Live HTTP 200 ({checked}); Google indexing unverified'
        except (OSError, ValueError, TypeError):
            pass
    if route in STATE:
        return 'In generated sitemap; live status and Google indexing unverified'
    return 'No current page for this query; Google status unverified'


def secondary_url(primary, links):
    primary_route = urlsplit(primary).path if primary else ''
    candidates = [part.strip() for part in links.split(';') if part.strip().startswith('/')]
    return next((candidate for candidate in candidates
                 if urlsplit(candidate).path != primary_route), '')


def add(keywords, path, intent_note, kind, coverage, competitors, priority='P2',
        links='', answer='Answer the task before listing options', action=None):
    for keyword in keywords:
        rows.append({
            'Keyword': keyword,
            'Search intent': search_intent(keyword, kind),
            'Primary target URL': path,
            'Secondary supporting URL': secondary_url(path, links),
            'Content type': kind,
            'Priority': priority,
            'Business value': ('High' if kind in ('home', 'product', 'pricing', 'catalog')
                               else 'Medium' if kind in ('category', 'use-case', 'compare', 'alternatives')
                               else 'Supporting'),
            'Competition level': 'Unverified; no localized query-level competition dataset',
            'Current status': live_status(path) if path else 'Not served: no current catalog offer/page',
            'Demand evidence': 'Unverified; no Search Console query data or reliable search-volume dataset',
            'Recommended action': action or answer,
            'Competitor evidence': competitors,
            'Coverage notes': coverage,
            'Internal links': links,
            'Schema': ('Product + Offer + BreadcrumbList + WebPage' if kind == 'product'
                       else 'WebPage + BreadcrumbList; ItemList only on visible collections' if path
                       else 'None; no page recommended yet'),
            'AEO opportunity': answer,
            'GEO/entity opportunity': ('AI Tools Zone; independent marketplace; Pakistan; PKR; '
                                       'seller-listed offer; confirm availability and terms on WhatsApp'),
        })


add(['AI tools', 'best AI tools', 'AI tools directory', 'AI tools Pakistan',
     'AI tools in Pakistan', 'AI software Pakistan', 'AI subscriptions Pakistan',
     'AI tools online Pakistan'], '/', 'Discovery / commercial', 'home',
    'Live homepage and catalog; Google index status remains unverified',
    'Futurepedia, Toolify and TopAI category/task discovery observed; no query ranks measured',
    'P1', '/products/; /categories/; /use-cases/',
    'State marketplace identity and explain how buying works')
add(['AI tools price Pakistan', 'AI tools pricing Pakistan', 'AI tools PKR',
     'buy AI subscriptions Pakistan', 'cheap AI tools Pakistan',
     'AI subscription deals Pakistan', 'AI software deals Pakistan'], '/pricing/',
    'Commercial comparison', 'pricing', 'Live pricing page; listed offers have different terms',
    'AI Tools Pak and local price-guide structures observed; no query ranks measured',
    'P1', '/products/; /guides/choose-ai-subscription/',
    'Show seller-listed prices with duration and access; do not imply equivalent plans or discounts')
add(['AI tools under 1000 PKR'], '/pricing/#under-1000', 'Budget comparison', 'pricing',
    'Existing budget section; no duplicate landing page', 'Exact localized query demand not measured',
    'P2', '/products/', 'List only catalog matches below the stated amount')
add(['AI tools under 2000 PKR'], '/pricing/#under-2000', 'Budget comparison', 'pricing',
    'Existing budget section; no duplicate landing page', 'Exact localized query demand not measured',
    'P2', '/products/', 'List only catalog matches below the stated amount')

for product in CATALOG:
    path = product_path(product)
    add([product['name'] + ' Pakistan', product['name'] + ' price Pakistan',
         'buy ' + product['name'] + ' Pakistan', product['name'] + ' subscription Pakistan',
         product['name'] + ' PKR', product['name'] + ' plan Pakistan'], path,
        'Transactional / plan evaluation', 'product',
        'Live product page; seller terms require owner confirmation',
        'Overlapping product-price pages observed on Pakistan seller sites; positions/demand unverified',
        'P1', category_path(product['category']) + '; /guides/private-vs-shared-access/',
        'State current seller-listed PKR price, duration, access and limitations; confirm availability before payment')

aliases = {
    'chatgpt-plus': ['ChatGPT price Pakistan', 'ChatGPT Plus price Pakistan',
                     'How much does ChatGPT Plus cost in Pakistan?', 'Is ChatGPT Plus available in Pakistan?'],
    'gemini-pro': ['Gemini price Pakistan', 'Gemini subscription Pakistan'],
    'canva-pro-edu': ['Canva Pro Pakistan', 'Canva Pro price Pakistan', 'buy Canva Pro Pakistan'],
    'figma-pro-private': ['Figma Pro Pakistan'], 'replit-core': ['Replit Pakistan'],
    'n8n-starter': ['n8n Pakistan'], 'veo-3-ultra': ['Veo 3 Pakistan'],
}
for slug, keywords in aliases.items():
    add(keywords, '/products/' + slug + '/', 'Commercial / direct question', 'product',
        'Live existing page; no alias URL created', 'Product intent in local marketplace samples; exact query position unknown',
        'P1', '/pricing/; /categories/',
        'Answer from the seller catalog without asserting official retail equivalence')

category_keywords = {
    'AI Assistants': ['AI writing tools', 'best AI writing tools', 'AI assistants Pakistan'],
    'AI Video': ['AI video generators', 'best AI video tools', 'AI video editing tools Pakistan'],
    'Design': ['AI image generators', 'AI design tools', 'AI tools for graphic designers'],
    'AI Voice': ['AI voice generators', 'AI voice tools Pakistan'],
    'Development': ['AI coding tools', 'best AI coding tools', 'AI automation tools'],
    'Productivity': ['AI productivity tools', 'AI presentation tools'],
    'VPN & Security': ['VPN plans Pakistan'],
    'Entertainment': ['digital entertainment subscriptions Pakistan'],
    'Business': ['professional subscriptions Pakistan'],
    'Software': ['software licenses Pakistan'],
}
products_by_category = {}
for product in CATALOG:
    products_by_category.setdefault(product['category'], []).append(product)
for category in CONTENT['categories']:
    name = category['name']
    related = '; '.join(product_path(p) for p in products_by_category.get(name, []))
    links = related or '/products/; /categories/'
    add(category_keywords[name], category_path(name), 'Category discovery', 'category',
        'Live category page with linked catalog offers',
        'Category and task organization observed at Futurepedia/TopAI; local query demand unverified',
        'P1', links, 'Explain the category and how to compare seller-listed offers')

use_cases = {
    'students': ['AI tools for students', 'AI education tools', 'AI tools for teachers',
                 'AI tools for researchers', 'What is the best AI tool for students?'],
    'creators': ['AI tools for content creators', 'AI tools for freelancers', 'AI tools for YouTubers',
                 'AI tools for designers', 'AI tools for marketers', 'AI marketing tools'],
    'developers': ['AI tools for developers'],
    'business': ['AI tools for businesses', 'AI business tools'],
}
use_case_links = {
    'students': '/categories/ai-assistants/; /compare/chatgpt-vs-gemini/; /pricing/',
    'creators': '/categories/design/; /categories/ai-video/; /categories/ai-voice/',
    'developers': '/categories/development/; /categories/productivity/; /products/replit-core/',
    'business': '/categories/business/; /categories/productivity/; /products/notion-business/',
}
for slug, keywords in use_cases.items():
    add(keywords, '/use-cases/ai-tools-for-' + slug + '/', 'Workflow selection', 'use-case',
        'Live consolidated audience guide; no one-page-per-keyword expansion',
        'Task/use-case discovery observed at TopAI; exact audience SERPs not verified',
        'P2', use_case_links[slug],
        'Start with the output needed and a practical selection checklist')

for page in CONTENT['pages']:
    if page['type'] == 'compare':
        keywords = [page['path'].strip('/').split('/')[-1].replace('-', ' ')]
    elif page['type'] == 'alternatives':
        keywords = [page['path'].strip('/').split('/')[-1] + ' alternatives']
        if 'chatgpt' in page['path']:
            keywords.append('Gemini alternatives')
    elif page['type'] == 'guides':
        if 'methodology' in page['path']:
            keywords = ['How does AI Tools Zone compare subscriptions?', 'AI Tools Zone price methodology']
        elif 'choose-' in page['path']:
            keywords = ['How do I choose an AI subscription?', 'How do I buy an AI subscription in Pakistan?']
        else:
            keywords = ['What is the difference between private and shared access?',
                        'AI subscription invitation meaning']
    else:
        continue
    add(keywords, page['path'], 'Informational / commercial comparison', page['type'],
        'Live original guide/comparison page; Google index status unverified',
        'Pakistan price-guide and global task/comparison structures observed; no query ranks measured',
        'P2', '; '.join(page['related']),
        'Give a direct answer, state limitations and link comparable catalog offers')

add(['Which AI tool should I use for video editing?'], '/categories/ai-video/',
    'Question', 'category', 'Live category page with video and editing offers',
    'Video taxonomy observed; exact query ranking/demand unknown', 'P1',
    '/products/capcut-pro/; /compare/capcut-vs-canva/',
    'Distinguish editing existing clips from generating video')
add(['Which AI tools are available in Pakistan?', 'What AI tools can I buy in Pakistan?'], '/products/',
    'Discovery / transaction', 'catalog', 'Live catalog hub; availability is confirmed in chat',
    'Local PKR catalogs observed; no market-wide inventory or search demand measured', 'P1',
    '/categories/; /use-cases/', 'List actual offers, then confirm availability and terms in chat')
add(['buy AI tools Pakistan', 'best AI tools Pakistan'], '/', 'Commercial discovery', 'home',
    'Live catalog with task search and internal links', 'Directory discovery observed; localized positions unverified',
    'P1', '/pricing/; /products/', 'Answer the task before listing relevant available offers')
add(['AI subscriptions price Pakistan', 'AI tools monthly price Pakistan',
     'AI tools yearly price Pakistan'], '/pricing/', 'Price comparison', 'pricing',
    'Live pricing page retains actual offer durations', 'Local price-index formats observed; no query data',
    'P1', '/products/; /guides/catalog-methodology/',
    'Explain duration/access differences; do not invent monthly equivalents')
add(['What payment methods are available?', 'How long does delivery take?', 'What warranty is offered?'],
    '/terms/', 'Ordering / support', 'trust', 'Live seller terms; product-specific values remain on product pages',
    'No competitor policy is adopted', 'P1', '/products/; /about/',
    'Answer from the published seller terms and ask customers to confirm order-specific conditions')

# Explicitly record high-commercial queries for products the owner does not list.
for brand, keywords in {
    'Claude': ['Claude Pakistan', 'Claude Pro price Pakistan', 'buy Claude Pro Pakistan'],
    'Perplexity': ['Perplexity Pro Pakistan', 'Perplexity Pro price Pakistan'],
    'Runway': ['Runway AI Pakistan', 'Runway AI subscription price Pakistan'],
    'Cursor': ['Cursor Pro Pakistan', 'Cursor AI price Pakistan'],
}.items():
    add(keywords, '', 'Transactional / commercial investigation', 'uncovered offer',
        f'{brand} is not in the current catalog; no target page is recommended',
        'Competitor/public samples are not evidence of an eligible or verified AI Tools Zone offer',
        'P3', '', 'Do not publish a product page until a genuine offer and its terms are owner-confirmed',
        action='Leave uncovered; only reconsider after the owner confirms a current, accurately describable offer.')

add(['AI Tools Zone', 'AIToolsZone website'], '/', 'Navigational', 'home',
    'Live homepage; Google index status unverified', 'Brand query results were not measured in localized Search Console data',
    'P2', '/about/; /products/', 'Keep the business name, homepage title and contact identity consistent')

add(['compare AI tools in Pakistan', 'AI tools comparison Pakistan',
     'AI subscriptions comparison Pakistan'], '/compare/',
    'Compare options by use case and offer terms', 'compare',
    'Existing comparison hub and three focused comparison pages; no performance ranking claimed',
    'AI Tools Pak comparison hub observed; localized query demand and position unverified',
    'P1', '/pricing/; /categories/; /guides/choose-ai-subscription/',
    'Explain what the comparison covers and distinguish workflow fit from seller-offer terms')
add(['AI Tools Zone blog', 'AI tools blog Pakistan'], '/blog/',
    'Find practical AI buying and workflow guides', 'blog',
    'New curated blog hub with a source-linked business automation guide and links to existing guides',
    'AI Tools Pak blog hub observed; no query rank or traffic inferred',
    'P2', '/compare/; /guides/; /use-cases/ai-tools-for-business/',
    'Publish durable, researched guidance; do not copy competitor text or invent tool tests')
for article in BLOG['articles']:
    if article.get('keywords'):
        coverage = ('Original source-linked guide; the page distinguishes current AI Tools Zone listings from other vendors'
                    if article['path'] != '/blog/ai-phone-agents-whatsapp-bots-pakistan/'
                    else 'Original informational guide; custom phone-agent and WhatsApp-bot implementation is not an orderable service')
        action = ('Publish useful, source-linked advice; do not copy competitor text or imply an unlisted offer'
                  if article['path'] != '/blog/ai-phone-agents-whatsapp-bots-pakistan/'
                  else 'Explain use cases, platform requirements, human handoff, policy and cost factors without promising deployment')
        add(article['keywords'], article['path'], 'Pakistan-focused informational / commercial guide', 'blog',
            coverage, 'AI Tools Pak blog topic coverage observed; demand, rankings and traffic remain unverified',
            'P2', '; '.join(article['related']), action)

seen = set()
unique_rows = []
for row in rows:
    normalized = row['Keyword'].casefold()
    if normalized in seen:
        continue
    seen.add(normalized)
    primary = row['Primary target URL']
    secondary = row['Secondary supporting URL']
    for label, value in (('primary', primary), ('secondary', secondary)):
        if not value:
            continue
        route = urlsplit(value).path or '/'
        if route not in STATE:
            raise ValueError(f"{row['Keyword']}: {label} route is not a canonical project page: {value}")
    unique_rows.append(row)

fields = [
    'Keyword', 'Search intent', 'Primary target URL', 'Secondary supporting URL',
    'Content type', 'Priority', 'Business value', 'Competition level', 'Current status',
    'Demand evidence', 'Recommended action', 'Competitor evidence', 'Coverage notes',
    'Internal links', 'Schema', 'AEO opportunity', 'GEO/entity opportunity',
]
with (ROOT / 'SEO-KEYWORD-MAP.csv').open('w', encoding='utf-8', newline='') as output:
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(unique_rows)
print(f'Wrote {len(unique_rows)} unique intent mappings. Search demand, competition and indexing remain unverified unless stated otherwise.')
