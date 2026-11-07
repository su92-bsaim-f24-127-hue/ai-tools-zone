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
SETTINGS = json.loads((ROOT / 'data/site-settings.json').read_text(encoding='utf-8'))
WHATSAPP_NUMBER = ''.join(ch for ch in str(SETTINGS.get('whatsappNumber','')) if ch.isdigit())
CATEGORIES = {c['name']: c for c in CONTENT['categories']}
HUBS = {
    'products': ('All AI Tools & Digital Subscriptions in Pakistan', 'Compare the complete catalog by total PKR price, duration and access. AI and non-AI subscriptions are labeled by category so you can find the right kind of offer.'),
    'categories': ('Browse AI Tools & Subscription Categories', 'Start with the work you need to do. Explore assistants, video, design, voice, development and productivity, or browse the separate digital subscription categories.'),
    'use-cases': ('Choose AI Tools by Your Workflow', 'Find a practical starting point for study, creative projects, development or business work. Each guide connects tasks with catalog offers and the questions to ask before buying.'),
    'compare': ('Compare AI Tools in Pakistan', 'Compare AI tools side by side. Our pages explain use-case fit, price, duration and access differences for Pakistan buyers.'),
    'alternatives': ('AI Tool Alternatives for Specific Tasks', 'Explore another way to complete your task. These shortlists distinguish general assistants from specialized tools and explain where an alternative will not replace your whole workflow.'),
    'guides': ('AI Subscription Buying Guides for Pakistan', 'Understand the offer before paying. Use these guides to check access, total cost, delivery and support, then confirm the actual plan with AI Tools Zone on WhatsApp.'),
    'pricing': ('AI Tools Pricing in Pakistan: Compare PKR Plans', 'Seller-listed PKR prices, including offers under PKR 1,000 and PKR 2,000. Each offer has its own duration and allowances.'),
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

def price_markup(product):
    current=f'<span class="price-current">PKR {product["price"]:,}</span>'
    regular=product.get('regularPrice')
    if isinstance(regular,int) and regular>product['price']:
        percent=round((regular-product['price'])*100/regular)
        return current+f'<span class="price-discount"><del>PKR {regular:,}</del><b>{percent}% off</b></span>'
    return current

def plan_table(products, caption='Compare seller-listed plans'):
    if not products:
        return '<p>No offers currently match this budget. <a href="/products/">Explore all listed plans</a>.</p>'
    rows=[]
    for p in products:
        order_url=f'https://wa.me/{WHATSAPP_NUMBER}?text={quote(p["orderMessage"])}'
        rows.append(f'<tr><th scope="row"><a href="{product_path(p)}">{e(p["name"])}</a><span class="table-category">{e(p["category"])}</span></th><td>{price_markup(p)}</td><td>{e(p["duration"])}</td><td>{e(p["access"])}</td><td><a class="inline-link" data-product-id="{e(p["id"])}" href="{e(order_url)}" target="_blank" rel="noopener noreferrer">Order on WhatsApp</a></td></tr>')
    return f'<div class="table-scroll" tabindex="0" role="region" aria-label="{e(caption)}"><table class="plan-table"><caption>{e(caption)}</caption><thead><tr><th scope="col">Tool</th><th scope="col">Listed price</th><th scope="col">Duration / allowance</th><th scope="col">Access</th><th scope="col">Next step</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

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
    cards = []
    for item in entries:
        path, title, summary = item[0], item[1], item[2]
        tag = item[3] if len(item) > 3 else ''
        cta = item[4] if len(item) > 4 else 'Read guide →'
        tag_html = f'<p class="eyebrow">{e(tag)}</p>' if tag else ''
        cards.append(f'<article class="editorial-card guide-card">{tag_html}<h2><a href="{path}">{e(title)}</a></h2><p>{e(summary)}</p><a class="guide-cta" href="{path}">{e(cta)}</a></article>')
    return '<div class="editorial-grid guide-grid">' + ''.join(cards) + '</div>'

def product_context(p):
    related = [page['path'] for page in CONTENT['pages'] if p['id'] in page['products']]
    note = ''
    if p['id'] == 'chatgpt':
        note = ('<section class="content-block"><h2>Confirm account ownership before ordering</h2>'
                '<p>OpenAI says an account is meant for the individual who created it. This listing is marked Private by the seller, but that label alone does not verify who created or controls an account. Ask the seller to explain the setup and confirm the current terms before paying; never share your password or one-time codes.</p>'
                '<p><a href="https://help.openai.com/en/articles/10471989-openai-account-sharing-policy" target="_blank" rel="noopener noreferrer">Read OpenAI account-sharing guidance</a>.</p></section>')
    elif p['id'] == 'canva':
        note = ('<section class="content-block"><h2>Check the Canva Education eligibility</h2>'
                '<p>This seller-listed Pro Edu invitation is not proof of an official Canva Education entitlement. Canva Education is free for eligible K–12 teachers and schools; higher-education institutions are not currently eligible for that program. Check the current eligibility rules and ask the seller who controls the workspace and what happens if access is declined.</p>'
                '<p><a href="https://www.canva.com/education/eligibility-guidelines/" target="_blank" rel="noopener noreferrer">Check Canva Education eligibility</a>.</p></section>')
    return note + '<section class="content-block"><h2>Choose this plan with context</h2>' + links([category_path(p['category'])] + related[:3] + ['/guides/private-vs-shared-access/']) + '</section>'

def home_discovery():
    return '<section class="answer-strip wrap" aria-labelledby="buying-guides"><h2 id="buying-guides">Choose with a clearer picture.</h2><p>Compare complete plans, explore tools for your work, and understand access before you buy.</p>' + links(['/products/','/categories/','/use-cases/','/compare/','/compare/chatgpt-vs-gemini/','/compare/chatgpt-vs-claude/','/compare/canva-vs-adobe/','/blog/free-ai-tools-pakistan/','/blog/ai-tools-for-pakistani-freelancers/','/pricing/']) + '</section>'

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
        h1_tag = '' if path == '/guides/' else f'<h1>{e(title)}</h1>'
        body = '<main id="main" class="wrap editorial-page">' + breadcrumbs(items) + h1_tag + content + '</main>'
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
        selected=[by_id[id] for id in page['products'] if id in by_id]
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
        separator = chr(183)
        date_line = 'Published <time datetime="'+e(article['datePublished'])+'">'+e(article['dateLabel'])+'</time>'
        if article.get('dateModified'):
            date_line += ' '+separator+' Updated <time datetime="'+e(article['dateModified'])+'">'+e(article.get('dateModifiedLabel', article['dateModified']))+'</time>'
        content += '<p class="article-date">'+date_line+' '+separator+' Research and planning guide</p>'
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
        if article.get('dateModified'):
            article_schema['dateModified'] = article['dateModified']
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
            blog_meta = {
                '/blog/ai-phone-agents-whatsapp-bots-pakistan/': ('BUSINESS AUTOMATION', 'Read automation guide →'),
                '/blog/free-ai-tools-pakistan/': ('FREE WORKFLOWS', 'Explore free tools →'),
                '/blog/ai-tools-for-pakistani-freelancers/': ('FREELANCE DELIVERABLES', 'Read freelancer guide →'),
                '/blog/ai-tools-for-teachers-pakistan/': ('EDUCATION & CLASSROOM', 'Read teacher guide →'),
                '/blog/ai-tools-for-content-creators-pakistan/': ('CREATOR STRATEGY', 'Read creator guide →'),
                '/blog/ai-subscription-vs-api-credits-pakistan/': ('API VS SUBSCRIPTION', 'Compare costs →'),
                '/blog/how-to-pay-for-chatgpt-plus-pakistan/': ('PAYMENT OPTIONS', 'Read payment guide →'),
                '/blog/jazzcash-easypaisa-ai-tools-pakistan/': ('LOCAL WALLET GUIDE', 'Read wallet guide →'),
                '/blog/avoiding-account-bans-shared-ai-tools-pakistan/': ('ACCOUNT SAFETY', 'Read safety guide →'),
                '/blog/chatgpt-plus-vs-gemini-pro-pakistan/': ('MODEL COMPARISON', 'Read comparison →'),
                '/blog/cheap-ai-subscriptions-pakistan/': ('PRICE GUIDE', 'Read cheap AI guide →'),
                '/blog/how-to-earn-money-with-ai-pakistan/': ('MONETIZATION & INCOME', 'Read earning guide →'),
                '/blog/where-to-buy-ai-tools-pakistan/': ('BUYER PROTECTION', 'Read safe buying guide →'),
                '/blog/best-ai-image-generators-pakistan/': ('IMAGE GENERATION', 'Compare image tools →'),
                '/blog/best-ai-video-generators-pakistan/': ('VIDEO CREATION', 'Compare video tools →'),
                '/blog/cursor-vs-copilot-pakistan/': ('DEVELOPER TOOLS', 'Compare coding tools →'),
            }
            blog_entries = []
            for a in BLOG['articles']:
                tag, cta = blog_meta.get(a['path'], ('EDITORIAL GUIDE', 'Read guide →'))
                blog_entries.append((a['path'], a['title'], a['summary'], tag, cta))

            hero_blog = f'''<div class="guide-hero">
<p class="eyebrow">AI TOOLS ZONE EDITORIAL BLOG</p>
<p class="lead">Practical, source-linked guides on AI subscriptions, local payment methods (JazzCash, Easypaisa), account security, and creator workflows in Pakistan.</p>
<div class="byline"><span>Reviewed by AI Tools Zone Editorial Team</span><span>Updated November 2026</span><a href="/guides/">Browse all 40+ tool guides &amp; comparisons</a></div>
</div>'''
            content = hero_blog + tiles(blog_entries)
            content += '<section class="content-block"><h2>More practical guides &amp; comparisons</h2><p>Use our dedicated workflow, buying, and comparison hubs to evaluate specific plans. We keep research linked to the right canonical pages instead of cloning duplicate articles.</p>' + links(['/guides/','/compare/','/use-cases/ai-tools-for-students/','/use-cases/ai-tools-for-creators/','/use-cases/ai-tools-for-developers/','/use-cases/ai-tools-for-business/','/categories/ai-assistants/','/categories/ai-video/','/categories/design/','/categories/ai-voice/','/categories/development/','/guides/choose-ai-subscription/','/guides/private-vs-shared-access/','/guides/catalog-methodology/','/pricing/']) + '</section>'
            content += '<p class="offer-note">AI Tools Zone currently lists subscriptions and buying information. Custom bot or phone-agent implementation is not listed as an orderable service.</p>'
            extra = [{'@type':'ItemList','@id':origin+'/blog/#articles','name':'AI Tools Zone practical guides','itemListElement':[{'@type':'ListItem','position':i+1,'name':a['title'],'url':origin+a['path']} for i,a in enumerate(BLOG['articles'])]}]
            publish('/blog/', title, intro, content, selected, extra_schema=extra)
            continue
        elif hub == 'guides':
            all_guides = [
                ('EDITORIAL GUIDE', 'Canva Pro Edu in Pakistan: Features, Pricing & Guide (2026)', 'Complete guide to Canva Pro Edu in Pakistan. Review features, access types, and flat PKR pricing via EasyPaisa and JazzCash.', '/products/canva-pro-edu/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'ElevenLabs in Pakistan: Features, Pricing & Guide (2026)', 'Complete guide to ElevenLabs in Pakistan. Review features, access types, and flat PKR pricing via EasyPaisa and JazzCash.', '/products/elevenlabs/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Leonardo AI Essential in Pakistan: Features, Pricing & Guide (2026)', 'Complete guide to Leonardo AI Essential in Pakistan. Review features, access types, and flat PKR pricing via EasyPaisa and JazzCash.', '/products/leonardo-ai-essential/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Veo 3 Ultra in Pakistan: Features, Pricing & Guide (2026)', 'Complete guide to Veo 3 Ultra in Pakistan. Review features, access types, and flat PKR pricing via EasyPaisa and JazzCash.', '/products/veo-3-ultra/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Gemini Pro in Pakistan: Features, Pricing & Guide (2026)', 'Complete guide to Gemini Pro in Pakistan. Review features, access types, and flat PKR pricing via EasyPaisa and JazzCash.', '/products/gemini-pro/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'ChatGPT Plus in Pakistan: Features, Pricing & Guide (2026)', 'Complete guide to ChatGPT Plus in Pakistan. Review features, access types, and flat PKR pricing via EasyPaisa and JazzCash.', '/products/chatgpt-plus/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Canva Pro in Pakistan: Features, Team Invites & Pricing Guide (2026)', 'Complete guide to Canva Pro in Pakistan. Review Brand Kits, Magic Studio AI, Invitation vs Lifetime options in PKR, and local payment verification.', '/products/canva-pro-edu/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'NordVPN vs Surfshark in Pakistan: Best VPN for Freelancers (2026)', 'Compare NordVPN vs Surfshark in Pakistan for remote work security, banking access, and streaming. Review local PKR rates with EasyPaisa and JazzCash.', '/products/nordvpn/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Gamma App in Pakistan: AI Presentations & Pitch Decks Guide (2026)', 'How Pakistani professionals and agencies use Gamma App for AI presentations and pitch decks. Review Plus/Pro credits, exports, and PKR payment methods.', '/products/gamma-pro/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Grok 2 AI in Pakistan: Features, X Premium & Local Access (2026)', 'How to use Grok 2 AI and Aurora image generation in Pakistan. Review real-time search capabilities, access options, and PKR rates via EasyPaisa.', '/blog/chatgpt-plus-vs-gemini-pro-pakistan/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Semrush Pro in Pakistan: SEO Agency Pricing & Local Guide (2026)', 'Complete guide to Semrush Pro in Pakistan for freelance SEOs and agencies. Review keyword research, backlink audits, and PKR pricing without bank forex tax.', '/compare/helium10-vs-semrush-vs-vidiq/', 'Read guide →'),
                ('HEAD-TO-HEAD COMPARISON', 'ChatGPT Plus vs Claude Pro in Pakistan (2026)', 'Compare GPT-4o with Claude 3.5 Sonnet on coding, SWE-bench, context windows, PKR pricing, and EasyPaisa payment.', '/compare/chatgpt-vs-claude/', 'Compare ChatGPT & Claude →'),
                ('CREATOR COMPARISON', 'CapCut Pro vs Runway ML in Pakistan (2026)', 'Timeline editing vs generative text-to-video AI. Compare CapCut Pro VIP (Rs. 950) with Runway Gen-3 in PKR with local payment.', '/compare/capcut-vs-runway/', 'Compare CapCut & Runway →'),
                ('EDITORIAL GUIDE', 'Grammarly vs QuillBot in Pakistan: Best AI Writing Tools (2026)', 'Compare Grammarly Premium vs QuillBot in Pakistan. Review grammar checks, paraphrasing, thesis writing workflows, and PKR pricing via EasyPaisa.', '/compare/grammarly-vs-quillbot-vs-wordai/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Runway Gen-3 Alpha in Pakistan: AI Video Generator Guide (2026)', 'Explore Runway Gen-3 Alpha in Pakistan for high-definition AI cinematography. Compare monthly credits in PKR, camera controls, and local payment methods.', '/compare/capcut-vs-runway/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'HeyGen AI Video in Pakistan: Avatar Creation & Pricing Guide (2026)', 'Complete guide to HeyGen AI video avatars in Pakistan. Review video translation, digital twin generation, and flat PKR pricing via local wallets.', '/categories/ai-video/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'DeepSeek AI in Pakistan: Pricing, Local Access & Guide (2026)', 'How to access DeepSeek V3 and R1 reasoning models in Pakistan. Compare open-weights coding, local PKR pricing, and payment via EasyPaisa and JazzCash.', '/blog/ai-subscription-vs-api-credits-pakistan/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Perplexity AI Pro in Pakistan: Pricing, Search Features & Guide (2026)', 'Complete guide to Perplexity AI Pro in Pakistan. Compare Pro Search, Claude 3.5 & GPT-4o models in PKR with EasyPaisa, JazzCash, and SadaPay payment.', '/categories/ai-assistants/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'n8n Workflow Automation in Pakistan: Small Business Guide (2026)', 'How Pakistani digital agencies and businesses use n8n for workflow automation. Compare cloud pricing in PKR and replace expensive Zapier accounts.', '/products/n8n-starter/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Lovable vs Replit in Pakistan: Best AI App Builder (2026)', 'Compare Lovable Pro vs Replit Core in Pakistan. Review full-stack AI coding workflows, cloud deployment, and PKR pricing with local payment.', '/compare/replit-vs-lovable/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'ElevenLabs Voice AI in Pakistan: Pricing, Urdu Support & Guide', 'Complete guide to ElevenLabs Voice AI in Pakistan. Review character plans in PKR, Urdu voice cloning, and payment via EasyPaisa and JazzCash.', '/products/elevenlabs/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Top AI Video Generators in Pakistan: CapCut, Veo & Runway (2026)', 'Best AI video generators in Pakistan compared for 2026. Explore CapCut Pro VIP, Google Veo 3 Ultra & ElevenLabs with PKR pricing and verified WhatsApp delivery.', '/categories/ai-video/', 'Read guide →'),
                ('EDITORIAL GUIDE', 'Best Midjourney Alternatives in Pakistan: Free & Paid (2026)', 'Compare top Midjourney alternatives in Pakistan with PKR pricing. Review Leonardo AI, Adobe Firefly & DALL-E with EasyPaisa and JazzCash payment.', '/products/leonardo-ai-essential/', 'Read guide →'),
                ('PRICE GUIDE', 'AI Tools Price Guide for Pakistan', 'Compare all 20 current listings in PKR, including duration, access type and the checks to make before payment.', '/pricing/', 'Read the price guide →'),
                ('PRICE GUIDE', 'Cheap AI Subscriptions in Pakistan: PKR Prices & Buying Tips (2026)', 'Find cheap AI subscriptions in Pakistan starting under PKR 1,000. Compare real PKR prices for Gemini Pro, CapCut Pro, Canva, and ChatGPT with safe buying advice.', '/blog/cheap-ai-subscriptions-pakistan/', 'Read cheap AI guide →'),
                ('ASSISTANT COMPARISON', 'ChatGPT Plus vs Gemini Pro', 'Choose between two general-purpose AI assistants using tasks, access terms and current Pakistan marketplace listings.', '/compare/chatgpt-vs-gemini/', 'Compare ChatGPT and Gemini →'),
                ('DESIGN COMPARISON', 'Canva Pro vs Figma Pro', 'Understand which design workflow fits content creators, teams, students and product designers.', '/products/figma-pro-private/', 'Compare Canva and Figma →'),
                ('ALTERNATIVES', 'ChatGPT Alternatives in Pakistan', 'Explore high-performance alternatives including Claude Pro, Google Gemini, and specialized coding models.', '/alternatives/chatgpt/', 'Explore ChatGPT alternatives →'),
                ('AUDIENCE GUIDE', 'AI Tools for Pakistani Students', 'Top budget-friendly tools for research, thesis editing, presentations and study productivity with PKR pricing.', '/use-cases/ai-tools-for-students/', 'View student guide →'),
                ('BUSINESS GUIDE', 'AI Tools for Pakistani Businesses', 'Scale marketing, customer communication, and workflow automation for agencies and local businesses.', '/use-cases/ai-tools-for-business/', 'View business guide →'),
                ('CREATOR GUIDE', 'AI Tools for Pakistani Creators', 'Produce viral YouTube shorts, TikToks, Reels, and high-CTR thumbnails using CapCut, Leonardo and Canva.', '/use-cases/ai-tools-for-creators/', 'View creator guide →'),
                ('DEVELOPER GUIDE', 'AI Tools for Pakistani Developers', 'Accelerate coding, API integrations, and app generation using Replit Core, n8n, and Lovable Pro.', '/use-cases/ai-tools-for-developers/', 'View developer guide →'),
                ('PRODUCTIVITY', 'AI Productivity Tools in Pakistan', 'Organize workspaces, automate repetitive tasks, and streamline documentation with Notion Plus and AI workflows.', '/categories/productivity/', 'View productivity guide →'),
                ('PAKISTAN DIRECTORY', 'AI Tools in Pakistan (2026 Directory)', 'Complete directory of verified tools available with local payment options (EasyPaisa, JazzCash, Bank IBFT).', '/products/', 'Browse directory →'),
                ('SUBSCRIPTION GUIDE', 'AI Subscriptions Pakistan Guide', 'Understand private vs shared workspaces, invitation seats, warranties, and safe subscription activation.', '/guides/private-vs-shared-access/', 'Read subscription guide →'),
                ('PRICING ANALYSIS', 'AI Tools Pricing in PKR', 'Detailed cost breakdown, billing cycles, and value ratings across 20 tools in the Pakistani market.', '/pricing/', 'View pricing breakdown →'),
                ('TOOL SPOTLIGHT', 'Google Gemini Pro Pakistan Guide', '18-month invitation seats, multimodal capabilities, 2M token context, and Google Workspace integration.', '/products/gemini-pro/', 'Read Gemini guide →'),
                ('TOOL SPOTLIGHT', 'Canva Pro Pakistan Guide', 'Everything you need to know about Canva Pro Edu, brand kits, AI magic studio, and invitation access.', '/products/canva-pro-edu/', 'Read Canva guide →'),
                ('TOOL SPOTLIGHT', 'CapCut Pro Pakistan Guide', 'Unlock pro video filters, auto-captions, remove background, and export in 4K 60fps for Pakistani editors.', '/products/capcut-pro/', 'Read CapCut guide →'),
                ('MODEL SPOTLIGHT', 'Claude 3.5 Sonnet Pakistan Guide', 'Complete guide to Claude 3.5 Sonnet & Claude Pro in Pakistan. Pricing in PKR, payment workarounds, and coding benchmarks.', '/compare/chatgpt-vs-claude/', 'Read Claude guide →'),
                ('DEVELOPER SPOTLIGHT', 'Cursor AI Pakistan Guide', 'Complete Cursor AI guide for Pakistani developers. Pro pricing in PKR, EasyPaisa payment, and Replit vs Copilot comparison.', '/use-cases/ai-tools-for-developers/', 'Read Cursor guide →'),
                ('TOOL SPOTLIGHT', 'Adobe Creative Cloud in Pakistan: Apps, Firefly & Pricing (2026)', 'Complete guide to Adobe Creative Cloud in Pakistan. Full desktop apps, Firefly generative credits, and genuine replacement warranty.', '/products/adobe-creative-cloud/', 'Read Adobe guide →'),
                ('TOOL SPOTLIGHT', 'Netflix Premium in Pakistan: 4K Ultra HD Profiles & Pricing (2026)', 'Complete guide to Netflix Premium 4K Ultra HD in Pakistan. Private profiles, zero screen-limit issues, and EasyPaisa renewal.', '/products/netflix-premium-4k/', 'Read Netflix guide →'),
                ('TOOL SPOTLIGHT', 'YouTube Premium in Pakistan: Ad-Free Music & Video Guide (2026)', 'Complete guide to YouTube Premium in Pakistan. Ad-free videos, background audio, YouTube Music, and instant activation.', '/products/youtube-premium/', 'Read YouTube guide →'),
                ('TOOL SPOTLIGHT', 'LinkedIn Premium in Pakistan: InMail Credits & Career Guide (2026)', 'Complete guide to LinkedIn Premium Business in Pakistan. InMail message credits, applicant insights, and competitive salary data.', '/products/linkedin-premium/', 'Read LinkedIn guide →'),
                ('TOOL SPOTLIGHT', 'Windows 11 Pro in Pakistan: Lifetime License Key & Setup Guide (2026)', 'Complete guide to Windows 11 Pro original activation keys in Pakistan. BitLocker encryption, Hyper-V, and instant key delivery.', '/products/windows-11-pro-key/', 'Read Windows guide →'),
                ('TOOL SPOTLIGHT', 'Notion Business in Pakistan: Team Workspace & Notion AI Guide (2026)', 'Complete guide to Notion Business with Notion AI. Team wikis, project boards, unlimited blocks, and PKR subscription plans.', '/products/notion-business/', 'Read Notion guide →'),
                ('MONETIZATION & INCOME', 'How to Earn Money with AI in Pakistan (2026 Guide)', 'Discover 6 proven freelancing and agency business models to earn PKR with AI tools like ChatGPT, Midjourney, and CapCut.', '/blog/how-to-earn-money-with-ai-pakistan/', 'Read earning guide →'),
                ('BUYER PROTECTION', 'Where to Buy AI Tools Safely in Pakistan (2026)', 'Avoid WhatsApp scams and account bans. How to identify trusted AI sellers in Pakistan with JazzCash, EasyPaisa, and warranty protection.', '/blog/where-to-buy-ai-tools-pakistan/', 'Read safe buying guide →'),
                ('IMAGE GENERATION', 'Best AI Image Generators in Pakistan (2026)', 'Compare Leonardo AI, Midjourney, and Adobe Firefly for Pakistani designers, agencies, and e-commerce sellers with PKR pricing.', '/blog/best-ai-image-generators-pakistan/', 'Compare image tools →'),
                ('VIDEO CREATION', 'Best AI Video Generators in Pakistan (2026)', 'Compare CapCut Pro, Runway Gen-3, Google Veo 3, and HeyGen for Pakistani creators, YouTubers, and TikTokers.', '/blog/best-ai-video-generators-pakistan/', 'Compare video tools →'),
                ('DEVELOPER TOOLS', 'Cursor AI vs GitHub Copilot in Pakistan (2026)', 'Compare the top 2 AI code editors for Pakistani software engineers, freelancers, and computer science students.', '/blog/cursor-vs-copilot-pakistan/', 'Compare coding tools →')
            ]

            hero_guides = f'''<section class="hero guide-hero-clean">
<p class="eyebrow">AI TOOLS ZONE EDITORIAL DESK &amp; BLOG</p>
<h1>Practical AI tool guides &amp; blog for Pakistan.</h1>
<p class="lead">Use current marketplace data, direct comparisons and official product sources to choose the right tool before you order. Every guide separates vendor features from AI Tools Zone marketplace terms.</p>
<div class="byline"><span>Reviewed by AI Tools Zone Editorial Team</span><span>Updated November 2026</span><a href="/guides/catalog-methodology/">Our review method</a></div>
</section>'''

            grid_cards = []
            for tag, g_title, g_desc, g_href, g_cta in all_guides:
                grid_cards.append(f'<article class="guide-card"><p class="eyebrow">{e(tag)}</p><h2><a href="{g_href}">{e(g_title)}</a></h2><p>{e(g_desc)}</p><a class="guide-cta" href="{g_href}">{e(g_cta)}</a></article>')
            grid_html = '<section class="guide-grid">' + ''.join(grid_cards) + '</section>'

            layout_html = f'''<section class="layout">
<article class="article">
<h2 id="what-makes-these-guides-useful">What makes these Pakistan AI tool guides useful?</h2>
<div class="answer"><strong>Short answer:</strong> each guide combines the marketplace details a buyer can verify—PKR price, duration, access type, delivery estimate and warranty—with links to the vendor’s official product information. That keeps the decision clear without presenting a marketplace offer as an official vendor plan.</div>
<p>AI subscriptions are difficult to compare when prices, billing periods and access arrangements are mixed together. A low price does not automatically mean better value. A one-month private plan, a shared workspace, an invitation-based seat and a lifetime license key are different products with different risks. Our guides put those facts next to each other and explain what questions to ask before sending payment.</p>
<h2 id="how-we-research-and-update-the-guides">How we research and update the guides</h2>
<p>AI Tools Zone records its own listed marketplace price and fulfillment terms as first-party information. Features are checked against official sources such as OpenAI, Google, Canva and Figma. We show a review date, link to the relevant product pages and avoid inventing customer ratings. If a vendor changes its product, the vendor page is authoritative for features; the WhatsApp team confirms current marketplace availability and exact access conditions before payment.</p>
<p>Comparisons are organized by real tasks: writing, research, coding, image creation, presentations, social content, interface design and team collaboration. This is more useful than declaring one tool universally “best.” A creator preparing daily social posts may need a different workflow from a product designer maintaining a component library.</p>
<h2 id="start-with-the-right-question">Start with the right question</h2>
<ul class="checklist">
<li>What outcome do you need: writing, video, images, voice, coding, design or productivity?</li>
<li>Do you require private access, or are invitation/shared terms acceptable?</li>
<li>How long do you need the plan, and what is the effective monthly cost?</li>
<li>Does the listed warranty cover your intended use?</li>
<li>Have current availability, payment route and delivery time been confirmed before payment?</li>
</ul>
<div class="cta"><a class="button button-lime" href="/products/">Browse all 20 tools</a><a class="button button-outline" href="/guides/private-vs-shared-access/">Understand access types</a></div>
</article>
<aside class="toc">
<strong>ON THIS PAGE</strong>
<a href="#what-makes-these-guides-useful">Why guides are useful</a>
<a href="#how-we-research-and-update-the-guides">How we research</a>
<a href="#start-with-the-right-question">Key questions</a>
<a href="/guides/private-vs-shared-access/">Understand access types</a>
<a href="/pricing/">Compare PKR pricing</a>
</aside>
</section>'''

            content = hero_guides + grid_html + layout_html

            extra = [{
                '@type': 'ItemList',
                '@id': origin + '/guides/#all-guides',
                'name': 'AI Tools Zone Pakistan Guides & Comparisons Directory',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': i + 1, 'name': item[1], 'url': origin + item[3]}
                    for i, item in enumerate(all_guides)
                ]
            }]
            publish('/guides/', title, intro, content, selected, extra_schema=extra)
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

def build_llms_txt(origin, products):
    lines=[
        "# AI Tools Zone\n\n",
        "> Independent digital marketplace for AI tools and digital subscriptions in Pakistan, offering seller-listed PKR prices and WhatsApp ordering.\n\n",
        "Compare current listings by price, duration and access type. Confirm availability, included limits and final price before payment.\n\n",
        "## Key Store Sections\n\n",
        f"- [Current offers]({origin}/products/): {len(products)} currently active catalog listings.\n",
        f"- [PKR pricing]({origin}/pricing/): Compare listed offers and plan terms.\n",
        f"- [Compare tools]({origin}/compare/): Read workflow comparisons and selection notes.\n",
        f"- [Categories]({origin}/categories/): Browse offers by category.\n",
        f"- [Buying guides]({origin}/guides/): Review access and buying questions.\n",
        f"- [About and WhatsApp support]({origin}/about/): Contact and ordering information.\n",
        f"- [Terms and warranty]({origin}/terms/): Read ordering and support terms.\n\n",
        "## Current listings\n\n",
    ]
    for product in products:
        lines.append(f"- [{product['name']}]({origin}/products/{product['slug']}/): {product['category']}; PKR {product['price']:,}; {product['duration']}; {product['access']} access. Confirm current terms before ordering.\n")
    lines.extend(["\n## Full catalog manifest\n\n",f"- [Full catalog and offer specifications]({origin}/llms-full.txt): details for {len(products)} current listings.\n"])
    return ''.join(lines)

def build_llms_full_txt(products, origin):
    lines = [
        "# AI Tools Zone - Full Catalog & Offer Specifications",
        "",
        "> Independent digital marketplace for AI tools and digital subscriptions in Pakistan.",
        f"> Origin: {origin}",
        f"> Customer Support: WhatsApp +{WHATSAPP_NUMBER}",
        "> Accepted Payment Methods: JazzCash, Easypaisa, Bank Transfer (arranged in chat)",
        "",
        f"## Product Catalog ({len(products)} Seller-Listed Offers in PKR)",
        ""
    ]
    for p in products:
        lines.append(f"### {p['name']}")
        lines.append(f"- **URL**: {origin}/products/{p['slug']}/")
        lines.append(f"- **Category**: {p['category']}")
        lines.append(f"- **Current seller-listed price**: PKR {p['price']:,}")
        if p.get('regularPrice'):
            lines.append(f"- **Regular price used for the promotion**: PKR {p['regularPrice']:,}")
        lines.append(f"- **Duration / Allowance**: {p['duration']}")
        lines.append(f"- **Access Type**: {p['access']}")
        lines.append(f"- **Delivery Estimate**: {p['delivery']}")
        lines.append(f"- **Replacement Warranty**: {p['warranty']}")
        if p.get('bestFor'):
            lines.append(f"- **Best For**: {', '.join(p['bestFor'])}")
        lines.append(f"- **Description**: {p['description']}")
        if p.get('features'):
            features = '; '.join(p['features'])
            lines.append(f"- **Included Features**: {features}")
        if p.get('vendor'):
            lines.append(f"- **Official Vendor**: {p['vendor']}")
        lines.append("")
    return "\n".join(lines) + "\n"

def finalize(paths, origin, write, products=None):
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
    robots_txt = (
        "# Public search discovery; this file is not access control.\n"
        "User-agent: *\n"
        "Allow: /\n\n"
        "# Dedicated AI search engines (for live search citations and answers)\n"
        "User-agent: OAI-SearchBot\n"
        "Allow: /\n\n"
        "User-agent: PerplexityBot\n"
        "Allow: /\n\n"
        "User-agent: Claude-SearchBot\n"
        "Allow: /\n\n"
        "# Model-training policy is independent of search discovery.\n"
        "# Preserve the existing ClaudeBot allowance; it is a training crawler.\n"
        "User-agent: ClaudeBot\n"
        "Allow: /\n\n"
        "User-agent: GPTBot\n"
        "Disallow: /\n\n"
        f"Sitemap: {origin}/sitemap.xml\n"
    )
    write('robots.txt', robots_txt)
    write('llms.txt', build_llms_txt(origin, products or []))
    if products is None:
        cat_file = ROOT/'data/catalog.json'
        if cat_file.is_file():
            try:
                products = json.loads(cat_file.read_text(encoding='utf-8'))
            except Exception:
                products = []
    if products:
        write('llms-full.txt', build_llms_full_txt(products, origin))
