"""Static editorial pages and freshness records; no browser or third-party build dependency."""
from urllib.parse import quote
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from datetime import datetime, timezone, timedelta
import hashlib
import json
import re

ROOT = Path(__file__).parent
# Pakistan has a fixed UTC+05:00 offset. Keep local Windows and UTC CI dates aligned
# without requiring an OS timezone database on Windows.
SITE_TIMEZONE = timezone(timedelta(hours=5))

def content_date(now=None):
    return (now or datetime.now(timezone.utc)).astimezone(SITE_TIMEZONE).date()

CONTENT = json.loads((ROOT / 'data/seo-content.json').read_text(encoding='utf-8'))
BLOG = json.loads((ROOT / 'data/blog-content.json').read_text(encoding='utf-8'))
CATEGORIES = {c['name']: c for c in CONTENT['categories']}
HUBS = {
    'products': ('All AI Tools & Digital Subscriptions in Pakistan', 'Compare the complete catalog by total PKR price, duration and access. AI and non-AI subscriptions are labeled by category so you can find the right kind of offer.'),
    'categories': ('Browse AI Tools & Subscription Categories', 'Start with the work you need to do. Explore assistants, video, design, voice, development and productivity, or browse the separate digital subscription categories.'),
    'use-cases': ('Choose AI Tools by Your Workflow', 'Find a practical starting point for study, creative projects, development or business work. Each guide connects tasks with catalog offers and the questions to ask before buying.'),
    'compare': ('Compare AI Tools in Pakistan', 'Compare selected tools and seller-listed offers side by side. Our pages explain use cases, price, duration and access differences; they are not lab benchmarks or claims of equivalent vendor entitlements.'),
    'alternatives': ('AI Tool Alternatives for Specific Tasks', 'Explore another way to complete your task. These shortlists distinguish general assistants from specialized tools and explain where an alternative will not replace your whole workflow.'),
    'guides': ('AI Subscription Buying Guides for Pakistan', 'Understand the offer before paying. Use these guides to check access, total cost, delivery and support, then confirm the actual plan with AI Tools Zone on WhatsApp.'),
    'pricing': ('AI Tools Pricing in Pakistan: Compare PKR Plans', 'Compare total seller-listed prices in PKR, including options under PKR 1,000 and PKR 2,000. These are different offers with different durations and allowances, not equivalent monthly subscriptions.'),
    'blog': ('AI Tools Zone Blog', 'Practical, source-linked guides for comparing AI subscriptions and planning AI workflows for people and businesses in Pakistan.')
}
e = lambda value: escape(str(value), quote=True)

def category_path(name):
    return '/categories/' + CATEGORIES[name]['slug'] + '/'

def product_path(product):
    return '/products/' + product['slug'] + '/'

def label_for(path):
    if path.strip('/') in HUBS:
        return HUBS[path.strip('/')][0]
    for category in CONTENT['categories']:
        if category_path(category['name']) == path:
            return category['heading']
    for page in CONTENT['pages']:
        if page['path'] == path:
            return page['title']
    for article in BLOG['articles']:
        if article['path'] == path:
            return article['title']
    return {'/terms/':'Ordering, refunds and warranty', '/about/':'About AI Tools Zone and contact'}.get(path, path)

def links(paths):
    return '<ul class="reading-links">' + ''.join(f'<li><a href="{p}">{e(label_for(p))}</a></li>' for p in paths) + '</ul>'

def breadcrumbs(items):
    return '<nav aria-label="Breadcrumb"><ol class="breadcrumb">' + ''.join(
        f'<li><a href="{e(url)}">{e(label)}</a></li><li aria-hidden="true">/</li>' if i < len(items)-1 else f'<li aria-current="page">{e(label)}</li>'
        for i, (label,url) in enumerate(items)) + '</ol></nav>'

def breadcrumb_schema(origin, items):
    return {'@type':'BreadcrumbList','@id':origin+items[-1][1]+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':label,'item':origin+url} for i,(label,url) in enumerate(items)]}

def faq_html(items):
    # Visible answers are useful even without a search-engine FAQ enhancement.
    return '<section class="content-block"><h2>Questions before you choose</h2>' + ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q,a in items) + '</section>'

def plan_table(products, caption='Compare seller-listed plans'):
    if not products:
        return '<p>No offers currently match this budget. <a href="/products/">Explore all listed plans</a>.</p>'
    rows=''.join(f'<tr><th scope="row"><a href="{product_path(p)}">{e(p["name"])}</a><span class="table-category">{e(p["category"])}</span></th><td>PKR {p["price"]:,}</td><td>{e(p["duration"])}</td><td>{e(p["access"])}</td><td><a class="inline-link" data-product-id="{p['id']}" href="https://wa.me/923430173923?text={quote(p['orderMessage'])}" target="_blank" rel="noopener noreferrer">Order on WhatsApp</a></td></tr>' for p in products)
    return f'<div class="table-scroll" tabindex="0" role="region" aria-label="{e(caption)}"><table class="plan-table"><caption>{e(caption)}</caption><thead><tr><th scope="col">Tool</th><th scope="col">Listed price</th><th scope="col">Duration / allowance</th><th scope="col">Access</th><th scope="col">Next step</th></tr></thead><tbody>{rows}</tbody></table></div>'

def comparison_table(entries, by_id):
    """Show source-backed evaluation routes without inventing equivalent plans."""
    rows=[]
    for item in entries:
        product=by_id.get(item.get('product',''))
        name=e(item['name'])
        source=f'<a href="{e(item["officialUrl"])}" target="_blank" rel="noopener noreferrer">Official product information ↗</a>'
        listing=(f'<a href="{product_path(product)}">Current AI Tools Zone listing</a>' if product
                 else '<span>Not currently listed</span>')
        rows.append(f'<tr><th scope="row">{name}</th><td>{source}</td><td>{listing}</td><td>{e(item["test"])}</td></tr>')
    return '<section class="content-block"><h2>Compare by the work you need done</h2><p>Vendor plan details can change and may vary by country or account. This guide gives you a fair test to run; it does not claim a hands-on benchmark or equal plan entitlements.</p><div class="table-scroll" tabindex="0" role="region" aria-label="Tool comparison and official references"><table class="plan-table"><caption>Original workflow comparison with official vendor references</caption><thead><tr><th scope="col">Tool</th><th scope="col">Source</th><th scope="col">AI Tools Zone catalogue</th><th scope="col">A useful side-by-side test</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div></section>'

def tiles(entries):
    return '<div class="editorial-grid">' + ''.join(f'<article class="editorial-card"><h2><a href="{path}">{e(title)}</a></h2><p>{e(summary)}</p></article>' for path,title,summary in entries) + '</div>'

def product_context(p):
    related = [page['path'] for page in CONTENT['pages'] if p['id'] in page['products']]
    return '<section class="content-block"><h2>Choose this plan with context</h2>' + links([category_path(p['category'])] + related[:3] + ['/guides/private-vs-shared-access/']) + '</section>'

def home_discovery():
    return '<section class="answer-strip wrap" aria-labelledby="buying-guides"><h2 id="buying-guides">Choose with a clearer picture.</h2><p>Compare complete plans, explore tools for your work, and understand access before you buy.</p>' + links(['/products/','/categories/','/use-cases/','/compare/','/alternatives/','/guides/','/pricing/']) + '</section>'

def build_pages(products, origin, shell, write):
    paths = []
    by_id = {p['id']:p for p in products}
    disclaimer = '<p class="offer-note">Prices describe AI Tools Zone offers, not official vendor pricing. Availability, included features, eligibility and the final price are confirmed before payment. <a href="/guides/choose-ai-subscription/">See the buying checklist</a> and <a href="/guides/catalog-methodology/">how we compare offers</a>.</p>'

    def publish(path, title, description, content, listed=(), crumbs=None, extra_schema=()):
        items = crumbs or [('Home','/'), (title,path)]
        graph = [breadcrumb_schema(origin,items)]
        if listed:
            graph.append({'@type':'ItemList','@id':origin+path+'#plans','name':title,'itemListElement':[{'@type':'ListItem','position':i+1,'name':p['name'],'url':origin+product_path(p)} for i,p in enumerate(listed)]})
        graph.extend(extra_schema)
        body = '<main id="main" class="wrap editorial-page">' + breadcrumbs(items) + f'<h1>{e(title)}</h1>' + content + '</main>'
        write(path.strip('/')+'/index.html',shell(title+' | AI Tools Zone', description, path, body, {'@context':'https://schema.org','@graph':graph}, '/'))
        paths.append(path)

    for c in CONTENT['categories']:
        selected = [p for p in products if p['category']==c['name']]
        if not selected:
            raise ValueError('Empty category: '+c['name'])
        intro = ''.join('<p>'+e(text)+'</p>' for text in c['intro'])
        content = intro + '<section class="content-block"><h2>Available listings and PKR prices</h2>' + plan_table(selected) + disclaimer + '</section>'
        content += '<section class="content-block"><h2>How to choose for your work</h2><p>'+e(c['choose'])+'</p></section>'
        content += faq_html(c['faq']) + '<section class="content-block"><h2>Related decisions</h2>'+links(c['related'])+'</section>'
        content += '<section class="content-block"><h2>Check the product source</h2><p>For current vendor features and terms, consult the official websites. Marketplace access conditions still need separate confirmation.</p><ul>'+''.join(f'<li><a href="{e(p["vendor"])}" target="_blank" rel="noopener noreferrer">{e(p["name"])} official website</a></li>' for p in selected)+'</ul></section>'
        publish(category_path(c['name']),c['heading'],f'Compare {c["name"].lower()} listings in Pakistan by PKR price, duration and access. Read practical selection advice and confirm the specific offer before ordering.',content,selected,[('Home','/'),('Categories','/categories/'),(c['name'],category_path(c['name']))])

    for page in CONTENT['pages']:
        selected=[by_id[id] for id in page['products']]
        content='<p class="direct-answer">'+e(page['answer'])+'</p>'
        if selected:
            content += '<section class="content-block"><h2>Listed plans at a glance</h2>'+plan_table(selected)+disclaimer+'</section>'
        if page.get('comparison'):
            content += comparison_table(page['comparison'], by_id)
        for heading,body in page['sections']:
            content += f'<section class="content-block"><h2>{e(heading)}</h2><p>{e(body)}</p></section>'
        content += faq_html(page['faq']) + '<section class="content-block"><h2>Continue your comparison</h2>'+links(page['related'])+'</section>'
        if page.get('sources'):
            content += '<section class="content-block"><h2>Official product references</h2><ul>'+''.join(f'<li><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(name)}</a></li>' for name,url in page['sources'])+'</ul><p>These references describe the vendors. They do not establish authorization or the entitlements of an independently supplied offer.</p></section>'
        publish(page['path'],page['title'],page['description'],content,selected,[('Home','/'),(HUBS[page['type']][0],'/'+page['type']+'/'),(page['title'],page['path'])])

    for article in BLOG['articles']:
        path=article['path']
        content='<p class="direct-answer">'+e(article['summary'])+'</p>'
        content += '<p class="article-date">Published <time datetime="'+e(article['datePublished'])+'">'+e(article['dateLabel'])+'</time> · Research and planning guide</p>'
        for section in article['sections']:
            content += '<section class="content-block"><h2>'+e(section['heading'])+'</h2>'
            content += ''.join('<p>'+e(paragraph)+'</p>' for paragraph in section.get('paragraphs',[]))
            if section.get('bullets'):
                content += '<ul>'+''.join('<li>'+e(item)+'</li>' for item in section['bullets'])+'</ul>'
            content += '</section>'
        content += '<section class="content-block"><h2>Official references</h2><ul>'+''.join('<li><a href="'+e(ref['url'])+'" target="_blank" rel="noopener noreferrer">'+e(ref['name'])+'</a></li>' for ref in article['references'])+'</ul><p>Provider documentation describes its own product and policies; verify current availability and requirements before choosing a service.</p></section>'
        content += faq_html(article['faq'])
        content += '<section class="content-block"><h2>Explore related AI Tools Zone pages</h2>'+links(article['related'])+'</section>'
        article_schema={
            '@type':'Article','@id':origin+path+'#article','headline':article['title'],
            'description':article['description'],'datePublished':article['datePublished'],
            'inLanguage':'en-PK','mainEntityOfPage':origin+path,
            'author':{'@id':origin+'/#organization'},'publisher':{'@id':origin+'/#organization'}
        }
        publish(path,article['title'],article['description'],content,(),
                [('Home','/'),('Blog','/blog/'),(article['title'],path)],(article_schema,))

    for hub,(title,intro) in HUBS.items():
        content='<p class="direct-answer">'+e(intro)+'</p>'
        selected=[]
        if hub == 'products':
            selected=products
            content += plan_table(products)+disclaimer+'<h2>Browse by category</h2>'+links([category_path(c['name']) for c in CONTENT['categories']])
            content += '<h2>Find the right starting point</h2>'+links(['/use-cases/','/compare/','/pricing/'])
        elif hub == 'pricing':
            selected=products
            content += '<nav aria-label="Price ranges">'+links(['/pricing/#under-1000','/pricing/#under-2000','/pricing/#all-prices']).replace('/pricing/#under-1000</a>','Under PKR 1,000</a>').replace('/pricing/#under-2000</a>','Under PKR 2,000</a>').replace('/pricing/#all-prices</a>','All listed prices</a>')+'</nav>'
            ai_categories={'AI Assistants','AI Video','Design','AI Voice','Development','Productivity'}
            for budget in (1000,2000):
                content += f'<section class="content-block" id="under-{budget}"><h2>AI and creative tools under PKR {budget:,}</h2>'+plan_table([p for p in products if p['price']<budget and p['category'] in ai_categories], f'Offers below PKR {budget:,}')+'</section>'
            content += '<section class="content-block" id="all-prices"><h2>All digital subscription prices</h2>'+plan_table(sorted(products,key=lambda p:p['price']))+disclaimer+'</section>'
            content += faq_html([('Are these official vendor prices?','No. These are AI Tools Zone seller-listed offers in PKR. Confirm the specific access, eligibility, allowance and final price before payment.'),('Are budget offers automatically equivalent to a full-price subscription?','No. Access type and allowances can differ. Compare the complete offer and check official vendor options before choosing.'),('How are PKR prices kept current?','The marketplace maintains its own catalog. A page update is not a stock check; ask support to reconfirm the offer before paying.')]) + links(['/guides/choose-ai-subscription/','/guides/private-vs-shared-access/'])
        elif hub == 'categories':
            content += tiles([(category_path(c['name']),c['heading'],c['intro'][0]) for c in CONTENT['categories']])
        elif hub == 'blog':
            entries=[(a['path'],a['title'],a['summary']) for a in BLOG['articles']]
            content += tiles(entries)
            content += '<section class="content-block"><h2>More practical guides</h2><p>Use the existing workflow, buying and comparison pages when you are choosing a listed subscription. We keep research linked to the right canonical page instead of cloning the same topic into thin articles or republishing fast-moving news without verification.</p>'+links(['/compare/','/use-cases/ai-tools-for-students/','/use-cases/ai-tools-for-creators/','/use-cases/ai-tools-for-developers/','/use-cases/ai-tools-for-business/','/categories/ai-assistants/','/categories/ai-video/','/categories/design/','/categories/ai-voice/','/categories/development/','/guides/choose-ai-subscription/','/guides/private-vs-shared-access/','/guides/catalog-methodology/','/pricing/'])+'</section>'
            content += '<p class="offer-note">AI Tools Zone currently lists subscriptions and buying information. Custom bot or phone-agent implementation is not listed as an orderable service.</p>'
            extra=[{'@type':'ItemList','@id':origin+'/blog/#articles','name':'AI Tools Zone practical guides','itemListElement':[{'@type':'ListItem','position':i+1,'name':a['title'],'url':origin+a['path']} for i,a in enumerate(BLOG['articles'])]}]
            publish('/blog/',title,intro,content,selected,extra_schema=extra)
            continue
        else:
            content += tiles([(p['path'],p['title'],p['answer']) for p in CONTENT['pages'] if p['type']==hub])
            content += '<section class="content-block"><h2>From a shortlist to a confirmed plan</h2><p>Open the product page for the listed price, duration, access, delivery estimate and replacement coverage. Discuss your requirements on WhatsApp before paying. These guides reflect buying considerations, not hands-on benchmarks or vendor endorsements.</p>'+links(['/products/','/pricing/','/guides/choose-ai-subscription/'])+'</section>'
        publish('/'+hub+'/',title,intro,content,selected)
    return paths

class ContentFingerprint(HTMLParser):
    """Hash meaningful text/links/structured data, ignoring asset cache busts and layout."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts=[]
        self.ignore=False
        self.json_script=False
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag in ('style','script'):
            self.json_script=tag=='script' and attrs.get('type')=='application/ld+json'
            self.ignore=not self.json_script
        if tag=='a': self.parts.append(attrs.get('href',''))
        if tag=='meta' and attrs.get('name') in ('description','robots'): self.parts.append(attrs.get('content',''))
        if tag=='link' and attrs.get('rel')=='canonical': self.parts.append(attrs.get('href',''))
        if tag=='img': self.parts.append(attrs.get('alt',''))
    def handle_endtag(self, tag):
        if tag in ('style','script'): self.ignore=False; self.json_script=False
    def handle_data(self, data):
        if not self.ignore:
            text=' '.join(data.split())
            text=re.sub(r'© \d{4}', '© YEAR', text)
            if text: self.parts.append(text)

def finalize(paths, origin, write):
    state_path=ROOT/'data/page-state.json'
    previous=json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    state={}
    for path in paths:
        html=(ROOT/(path.strip('/')+'/index.html' if path!='/' else 'index.html')).read_text(encoding='utf-8')
        parser=ContentFingerprint(); parser.feed(html)
        digest=hashlib.sha256('\n'.join(parser.parts).encode()).hexdigest()
        old=previous.get(path,{})
        state[path]={'sha256':digest,'lastmod':old['lastmod'] if old.get('sha256')==digest else content_date().isoformat()}
    write('data/page-state.json',json.dumps(state,indent=2)+'\n')
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{origin}{path}</loc><lastmod>{state[path]["lastmod"]}</lastmod></url>\n' for path in paths)+'</urlset>\n')
    write('robots.txt',f'# Public search discovery; this file is not access control.\nUser-agent: *\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\n# Model-training policy is independent of search discovery.\nUser-agent: GPTBot\nDisallow: /\n\nSitemap: {origin}/sitemap.xml\n')
