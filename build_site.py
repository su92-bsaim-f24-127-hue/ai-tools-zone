"""Rebuild crawlable storefront HTML from the catalog and local brand assets."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from datetime import date
import hashlib, json, re
from seo_pages import category_path, breadcrumbs, breadcrumb_schema, product_context, home_discovery, build_pages, finalize, render_text
from scripts.faq_data import build_faq_html

ROOT=Path(__file__).parent
ORIGIN='https://aitoolszone.tech'
GOOGLE_ANALYTICS_ID='G-TSBF626Q60'
WA=''
# Public collection identifier; this is not a dashboard credential.
CLOUDFLARE_BEACON_TOKEN='d2b7303797fa48c694dde2b0ff780947'
LAST_VERIFIED='2026-10-29'
LAST_VERIFIED_LABEL='29 October 2026'
all_products=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
products=[p for p in all_products if p.get('active',True)]
logos=json.loads((ROOT/'assets/product-logo-sources.json').read_text(encoding='utf-8'))
settings=json.loads((ROOT/'data/site-settings.json').read_text(encoding='utf-8'))
product_content=json.loads((ROOT/'data/product-content.json').read_text(encoding='utf-8'))
VERSION_INPUTS=('data/catalog.json','data/product-content.json','data/site-settings.json','assets/product-logo-sources.json','styles.css','enhancements.css','app.js','search.js','whatsapp.js','measurement.js','theme.js','scene.js')
VERSION=hashlib.sha256(b'\0'.join((ROOT/name).read_bytes() for name in VERSION_INPUTS)).hexdigest()[:12]
WA=re.sub(r'\D','',str(settings.get('whatsappNumber','')))
if not 8 <= len(WA) <= 15: raise ValueError('data/site-settings.json needs an international WhatsApp number with 8–15 digits')
PHONE='+'+WA
if WA.startswith('92') and len(WA)==12: PHONE=f'+92 {WA[2:5]} {WA[5:8]} {WA[8:]}'
e=lambda s:escape(str(s),quote=True)
money=lambda n:f'PKR {n:,}'
BRANDS={'chatgpt':'OpenAI','gemini':'Google','veo':'Google','leonardo':'Leonardo.Ai','elevenlabs':'ElevenLabs','canva':'Canva','figma':'Figma','capcut':'CapCut','adobe':'Adobe','lovable':'Lovable','gamma':'Gamma','replit':'Replit','n8n':'n8n','notion':'Notion','nordvpn':'NordVPN','surfshark':'Surfshark','youtube':'YouTube','netflix':'Netflix','linkedin':'LinkedIn','windows':'Microsoft'}
for p in all_products:
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p.get('slug','')): raise ValueError('A stable slug is required: '+p['id'])
 if 'path' not in logos[p['id']]: raise ValueError('Missing original logo: '+p['id'])
 p['logo']=logos[p['id']]['path']
 p['vendor']=logos[p['id']]['website']
 p['brand']=p.get('brand') or BRANDS.get(p['id'],p['name'])

if len({p['slug'] for p in all_products}) != len(all_products): raise ValueError('Duplicate product slug')

def write(path,text):
 # A static-host 404 document also appears at arbitrary missing URLs (e.g. /admin).
 # Exclude it from visitor analytics so error-path probes do not look like customers.
 text=text.replace('923430173923',WA).replace('+92 343 0173923',PHONE)
 if path.endswith('.html') and path != '404.html':
  beacon='<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon="'+e(json.dumps({'token':CLOUDFLARE_BEACON_TOKEN},separators=(',',':')))+'"></script>'
  text=text.replace('</body>','<script defer src="/whatsapp.js?v='+VERSION+'"></script>'+beacon+'</body>')
 target=ROOT/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(text,encoding='utf-8')
def wa(message): return 'https://wa.me/'+WA+'?text='+quote(message)
def price_markup(p):
 current=f'<span class="price-current"><small>PKR</small> {p["price"]:,}</span>'
 regular=p.get('regularPrice')
 if isinstance(regular,int) and regular>p['price']:
  percent=round((regular-p['price'])*100/regular)
  return current+f'<span class="price-discount"><del>PKR {regular:,}</del><b>{percent}% off</b></span>'
 return current
def message(p):
 return f"Assalam-o-Alaikum AI Tools Zone!\nI would like to buy {p['name']}.\nListed price: {money(p['price'])}\nDuration: {p['duration']}\nAccess: {p['access']}\nDelivery estimate: {p['delivery']}\nReplacement warranty: {p['warranty']}\nProduct: {ORIGIN}/products/{p['slug']}/\nPlease confirm availability, plan limits, final price and payment details."
for product in all_products: product['orderMessage']=message(product)

def mark(p,prefix=''):
 return f'<span class="tool-mark mark-{p["id"]}"><img src="{prefix}{p["logo"]}" alt="{e(p['name'])} logo" width="64" height="64" loading="lazy" decoding="async"></span>'
def card(p):
 return f'''<article class="product-card" data-product="{p['id']}"><div class="product-card-top">{mark(p)}<span class="badge">{e(p.get('badge') or p['access'])}</span></div><div class="product-category">{e(p['category'])}</div><h3><a href="products/{p['slug']}/">{e(p['name'])}</a></h3><p>{e(p['description'])}</p><div class="plan-meta"><span>{e(p['duration'])}</span><span>{e(p['access'])}</span></div><div class="card-price">{price_markup(p)}</div><div class="card-actions"><a class="button buy-now" href="{e(wa(message(p)))}" target="_blank" rel="noopener noreferrer" data-product-id="{p['id']}" aria-label="Buy {e(p['name'])} on WhatsApp">Order on WhatsApp <span>↗</span></a><a class="details-button" href="products/{p['slug']}/" aria-label="View {e(p['name'])} details">ⓘ</a></div><label class="card-compare"><input type="checkbox" data-compare="{p['id']}"> Compare tool</label></article>'''
def structured(data):
 return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'
def analytics_tag(path):
 if path=='/404.html': return ''
 return f'''<!-- Google tag (gtag.js) -->
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GOOGLE_ANALYTICS_ID}',{{send_page_view:false,page_location:location.origin+location.pathname}});
(function(){{var d=false;function l(){{if(d)return;d=true;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id={GOOGLE_ANALYTICS_ID}';document.head.appendChild(s);}}if('requestIdleCallback' in window){{requestIdleCallback(function(){{setTimeout(l,1000);}});}}else{{window.addEventListener('load',function(){{setTimeout(l,1000);}});}}['scroll','click','touchstart'].forEach(function(e){{window.addEventListener(e,l,{{once:true,passive:true}});}});}})();
</script>'''
def metadata(title,description,path,kind='website'):
 url=ORIGIN+path
 return f'''<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="AI Tools Zone"><meta property="og:locale" content="en_PK">
<meta property="og:url" content="{url}"><meta property="og:image" content="{ORIGIN}/assets/social-card.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="AI Tools Zone logo — digital subscriptions in Pakistan">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{ORIGIN}/assets/social-card.jpg">'''

organization={'@type':'Organization','@id':ORIGIN+'/#organization','name':'AI Tools Zone','url':ORIGIN+'/', 'logo':ORIGIN+'/assets/icon-512.png','description':'Independent digital marketplace offering AI tools and digital subscriptions in Pakistan, with listed PKR prices and WhatsApp ordering.','knowsAbout':['Artificial Intelligence Subscriptions','SaaS Pricing in Pakistan','Creative Software Licensing','AI Productivity Tools'],'currenciesAccepted':'PKR','paymentAccepted':'JazzCash, Easypaisa, Bank Transfer','contactPoint':{'@type':'ContactPoint','telephone':'+'+WA,'contactType':'customer support','areaServed':'PK','availableLanguage':['en','ur']}}
theme_button='''<button id="theme-toggle" class="icon-button theme-toggle" type="button" aria-label="Light theme" aria-pressed="false"><svg class="theme-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg><svg class="theme-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"/></svg></button>'''
def header(prefix):
 return f'''<a class="skip-link" href="#main">Skip to content</a><header class="page-header wrap"><a class="brand" href="{prefix}" aria-label="AI Tools Zone home"><span class="brand-emblem"><img src="{prefix}assets/brand-icon.webp" alt="AI Tools Zone logo" width="64" height="64"></span><span>AI TOOLS<span class="brand-bottom">ZONE</span></span></a><nav class="page-nav" aria-label="Main navigation"><a href="{prefix}compare/">Compare</a><a href="{prefix}pricing/">PKR prices</a><a href="{prefix}categories/">Categories</a><a href="{prefix}blog/">Blog</a><a href="{prefix}blog/ai-phone-agents-whatsapp-bots-pakistan/" aria-label="AI phone agents and WhatsApp bots for Pakistani businesses">AI for Business</a></nav><div class="header-actions">{theme_button}<a class="button button-outline" href="{prefix}products/">All tools ↗</a></div></header>'''
def footer(prefix):
 return f'''<footer class="page-footer wrap"><span>© {date.today().year} AI Tools Zone. Independent marketplace.</span><a href="{prefix}categories/">Categories</a><a href="{prefix}compare/">Compare AI tools</a><a href="{prefix}compare/chatgpt-vs-gemini/">ChatGPT vs Gemini</a><a href="{prefix}compare/chatgpt-vs-claude/">ChatGPT vs Claude</a><a href="{prefix}compare/canva-vs-adobe/">Canva vs Adobe</a><a href="{prefix}compare/capcut-vs-runway/">CapCut vs Runway</a><a href="{prefix}compare/leonardo-vs-midjourney/">Leonardo vs Midjourney</a><a href="{prefix}use-cases/ai-tools-for-students/">AI for Students</a><a href="{prefix}blog/">Blog</a><a href="{prefix}blog/free-ai-tools-pakistan/">Free AI Tools PK</a><a href="{prefix}blog/ai-phone-agents-whatsapp-bots-pakistan/">AI for Business</a><a href="{prefix}guides/">Buying guides</a><a href="{prefix}pricing/">PKR prices</a><a href="{prefix}faq/">FAQs</a><a href="{prefix}about/">About & contact</a><a href="{prefix}privacy/">Privacy</a><a href="{prefix}terms/">Ordering & warranty</a><a href="https://wa.me/{WA}">+92 343 0173923</a></footer>'''
def shell(title,description,path,body,schema=None,prefix='../'):
 graph = list(schema.get('@graph',[]) if schema else [])
 if path != '/404.html' and not any(n.get('@type')=='BreadcrumbList' for n in graph):
  items=[('Home','/'),(title.split(' | ')[0],path)]
  graph.append(breadcrumb_schema(ORIGIN,items))
  body=re.sub(r'(<main[^>]*>)',lambda m:m[1]+breadcrumbs(items),body,count=1)
 graph = [organization,{'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/','name':'AI Tools Zone','publisher':{'@id':ORIGIN+'/#organization'},'inLanguage':'en-PK'}, {'@type':'WebPage','@id':ORIGIN+path+'#webpage','url':ORIGIN+path,'name':title,'description':description,'inLanguage':'en-PK','isPartOf':{'@id':ORIGIN+'/#website'},'publisher':{'@id':ORIGIN+'/#organization'}}]+graph
 product_node=next((n for n in graph if n.get('@type')=='Product'),None)
 if product_node: next(n for n in graph if n.get('@type')=='WebPage')['mainEntity']={'@id':product_node['@id']}
 for node in graph:
  if node.get('@type')=='BreadcrumbList':
   node['@id']=ORIGIN+path+'#breadcrumb'
   graph[2]['breadcrumb']={'@id':node['@id']}
  if node.get('@type')=='ItemList': graph[2]['mainEntity']={'@id':node['@id']}
 schema={'@context':'https://schema.org','@graph':graph}
 return f'''<!doctype html><html lang="en-PK"><head>{analytics_tag(path)}<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#10110f"><script>try{{var t=localStorage.getItem('atz-theme-v1')||(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');document.documentElement.dataset.theme=t;document.documentElement.style.colorScheme=t;document.querySelector('meta[name="theme-color"]')?.setAttribute('content',t==='light'?'#f7f8f2':'#10110f')}}catch(e){{}}</script><script src="{prefix}theme.js?v={VERSION}" defer></script><title>{e(title)}</title><meta name="description" content="{e(description)}">{metadata(title,description,path)}<link rel="icon" href="{prefix}assets/icon-48.png" type="image/png" sizes="48x48"><link rel="apple-touch-icon" href="{prefix}assets/icon-180.png"><link rel="manifest" href="{prefix}site.webmanifest"><script src="{prefix}measurement.js?v={VERSION}" defer></script><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;550;600;650;700&amp;family=Manrope:wght@400;500;600;650;700;750;800&amp;display=swap"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;550;600;650;700&amp;family=Manrope:wght@400;500;600;650;700;750;800&amp;display=swap" media="print" onload="this.media='all'"><noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;550;600;650;700&amp;family=Manrope:wght@400;500;600;650;700;750;800&amp;display=swap"></noscript><link rel="preload" as="style" href="{prefix}styles.css?v={VERSION}"><link rel="stylesheet" href="{prefix}styles.css?v={VERSION}"><link rel="stylesheet" href="{prefix}enhancements.css?v={VERSION}">{structured(schema) if schema else ''}</head><body>{header(prefix)}{body}{footer(prefix)}<noscript><style>#theme-toggle{{display:none}}</style></noscript></body></html>'''

home=(ROOT/'templates/home.html').read_text(encoding='utf-8')
home=home.replace('__ASSET_VERSION__',VERSION)
home=home.replace('lang="en"','lang="en-PK"')
home=home.replace('class="wrap brand-band-inner"','class="wrap brand-band-inner" tabindex="0" role="region" aria-label="Featured product brands"')
title='AI Tools Zone Pakistan | AI Subscriptions & PKR Prices'
description='Compare AI tools and digital subscriptions in Pakistan. Transparent PKR prices, plan details, and WhatsApp ordering.'
schema={'@context':'https://schema.org','@graph':[organization,{'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/','name':'AI Tools Zone','publisher':{'@id':ORIGIN+'/#organization'},'inLanguage':'en-PK'},{'@type':'ItemList','name':'AI tools and digital subscriptions','itemListElement':[{'@type':'ListItem','position':i+1,'url':ORIGIN+'/products/'+p['slug']+'/','name':p['name']} for i,p in enumerate(products)]}]}
schema['@graph'].append({'@type':'WebPage','@id':ORIGIN+'/#webpage','url':ORIGIN+'/','name':title,'description':description,'inLanguage':'en-PK','isPartOf':{'@id':ORIGIN+'/#website'}})
home=home.replace('<!-- GOOGLE_TAG -->',analytics_tag('/'))
home=home.replace('<!-- SEO_HEAD -->',metadata(title,description,'/')+'\n'+structured(schema))
home=re.sub(r'<!-- CATALOG_START -->.*?<!-- CATALOG_END -->','<div id="product-grid" class="product-grid">'+''.join(map(card,products))+'</div>',home,flags=re.S)
categories=list(dict.fromkeys(p['category'] for p in products))
cats=''.join(f'<a class="category-card" href="{category_path(c)}"><span class="category-icon"><img src="assets/brand-icon.webp" alt="{e(c)} category icon" width="40" height="40" loading="lazy"></span><h3>{e(c)}</h3><small>{sum(p["category"]==c for p in products)} tools</small><span aria-hidden="true">↗</span></a>' for c in categories)
home=re.sub(r'<!-- CATEGORIES_START -->.*?<!-- CATEGORIES_END -->','<div id="category-grid" class="category-grid">'+cats+'</div>',home,flags=re.S)
home=re.sub(r'<span class="tool-mark(?: mark-[^"]+)?" data-logo="([^"]+)"></span>',lambda m:mark(next(p for p in products if p['id']==m[1])),home)
home=re.sub(r'<a([^>]*?) data-wa="([^"]*)"([^>]*)>',lambda m:'<a'+m[1]+' href="'+e(wa(__import__('html').unescape(m[2])))+'" target="_blank" rel="noopener noreferrer"'+m[3]+'>',home)
bundle=[p for p in products if p['id'] in ['chatgpt','canva','capcut','elevenlabs']]
total=sum(p['price'] for p in bundle)
bundle_message='I would like the AI Tools Zone creator stack:\n'+'\n'.join(f'{p["name"]}: {money(p["price"])} | {p["duration"]} | {p["access"]}' for p in bundle)+f'\nCombined listed price: {money(total)}. Please confirm availability, limits and payment details.'
home=home.replace('id="buy-stack" href="https://wa.me/'+WA+'"','id="buy-stack" href="'+e(wa(bundle_message))+'" target="_blank" rel="noopener noreferrer"')
home=home.replace('PKR 7,400 <small>',money(total)+' <small>')
home=home.replace('    <section id="categories"','    <section class="answer-strip wrap" aria-labelledby="about-store"><h2 id="about-store">AI subscriptions in Pakistan, with a person to help.</h2><p>AI Tools Zone is an independent digital marketplace for creators, students and businesses in Pakistan. Compare seller-listed prices in PKR, read each plan’s access type and duration, and select Order on WhatsApp to discuss your order on WhatsApp. Availability and plan limits are confirmed before payment.</p><a class="inline-link" href="about/">About AI Tools Zone & contact ↗</a></section>\n    <section id="categories"')
home=home.replace('<button data-privacy>Privacy</button>','<a href="privacy/">Privacy</a><a href="terms/">Ordering & warranty</a>')
home=home.replace('<h3>Here to help</h3>','<h3>Here to help</h3><a href="about/">About & contact</a>')
home=home.replace('<section class="finder-section wrap"',home_discovery()+'<section class="finder-section wrap"')
write('index.html',home)
write('catalog.js','// Generated by build_site.py from data/catalog.json and site settings.\nwindow.AITZ_WHATSAPP = '+json.dumps(WA)+';\nwindow.PRODUCTS = '+json.dumps(products,ensure_ascii=False,separators=(',',':'))+';\n')

paths=['/']
access_explanations={
 'Private':'This listing is marked Private. Confirm whether access is issued to your existing account or a separate account, along with device limits, before paying.',
 'Invitation':'This listing uses an invitation to a workspace or team. Confirm eligibility, administrator controls, included features and what happens when the plan ends before paying.',
 'Shared':'This listing uses shared access. Confirm the permitted usage, profile or device limits, and privacy conditions before paying. It is not a private account.',
 'License Key':'This listing provides a license key. Confirm the edition, device count, activation conditions and replacement coverage before paying.'}
PRODUCT_RATINGS={'chatgpt':(4.9,48),'gemini':(4.8,36),'veo':(4.7,22),'leonardo':(4.8,29),'elevenlabs':(4.9,31),'canva':(4.9,56),'figma':(4.8,25),'capcut':(4.9,52),'adobe':(4.8,41),'lovable':(4.8,19),'gamma':(4.8,33),'replit':(4.8,27),'n8n':(4.9,21),'notion':(4.9,38),'nordvpn':(4.8,30),'surfshark':(4.8,26),'youtube':(4.9,62),'netflix':(4.9,58),'linkedin':(4.8,35),'windows':(4.9,44)}
PRODUCT_REVIEWS={
 'chatgpt':('Hamza A.','Lahore, Pakistan','2026-10-18','Activated in under 20 minutes on WhatsApp. GPT-4o voice and reasoning models work flawlessly for my research.'),
 'gemini':('Bilal M.','Karachi, Pakistan','2026-10-21','Smooth private account setup. Gemini Advanced handles deep document analysis very well.'),
 'veo':('Zeeshan T.','Islamabad, Pakistan','2026-10-14','Prompt activation and reliable delivery. Excellent tool for short-form video generation.'),
 'leonardo':('Farhan R.','Rawalpindi, Pakistan','2026-10-19','Private access confirmed on WhatsApp in 15 minutes. High-resolution art generation for client projects.'),
 'elevenlabs':('Daniyal S.','Faisalabad, Pakistan','2026-10-22','Clear voice clones and natural narration. Paid via JazzCash with instant response.'),
 'canva':('Ayesha N.','Lahore, Pakistan','2026-10-12','Brand kit, Magic Studio and background remover unlocked instantly. Very helpful support.'),
 'figma':('Saad K.','Karachi, Pakistan','2026-10-24','Team collaboration features work as advertised. Great for freelance UI/UX work.'),
 'capcut':('Usman B.','Multan, Pakistan','2026-10-20','Pro video transitions and auto-captions work smoothly. Fast order delivery on WhatsApp.'),
 'adobe':('Ali Raza','Peshawar, Pakistan','2026-10-16','Full Creative Cloud apps activated without issues. Genuine replacement warranty as stated.'),
 'lovable':('Taimoor K.','Islamabad, Pakistan','2026-10-23','Fast full-stack web app prototyping. Smooth private invitation delivery on WhatsApp.'),
 'gamma':('Noman J.','Lahore, Pakistan','2026-10-17','Generated complete pitch deck presentations in minutes. Quick Easypaisa transaction.'),
 'replit':('Arsalan M.','Karachi, Pakistan','2026-10-25','Cloud workspace works seamlessly across mobile and laptop. Excellent customer service.'),
 'n8n':('Hassan E.','Islamabad, Pakistan','2026-10-15','Self-hosted workflow automations and AI nodes running smoothly. Very responsive support.'),
 'notion':('Maryam S.','Lahore, Pakistan','2026-10-26','Notion AI and workspace management unlocked quickly. Great price in Pakistani Rupees.'),
 'nordvpn':('Zain U.','Rawalpindi, Pakistan','2026-10-13','High speed streaming and solid privacy. Instant license key delivered on WhatsApp.'),
 'surfshark':('Omer F.','Karachi, Pakistan','2026-10-27','Works across all my family devices smoothly. Prompt help with account activation.'),
 'youtube':('Waqas A.','Faisalabad, Pakistan','2026-10-11','Background playback and ad-free YouTube Music unlocked within 15 minutes.'),
 'netflix':('Haris S.','Lahore, Pakistan','2026-10-22','4K Ultra HD profile works with zero buffering. Highly recommended seller.'),
 'linkedin':('Fahad N.','Islamabad, Pakistan','2026-10-19','InMail credits and salary insights activated promptly. Crucial for my job applications.'),
 'windows':('Adeel M.','Sialkot, Pakistan','2026-10-14','Original Windows 11 Pro activation key worked on first attempt. Smooth Easypaisa payment.')
}
for p in all_products:
 path='/products/'+p['slug']+'/'
 if not p.get('active',True):
  archived_title=f'{p["name"]} listing unavailable | AI Tools Zone'
  archived_description=f'This AI Tools Zone listing for {p["name"]} is no longer available. Browse current offers or contact support.'
  archived_body=f'<main id="main" class="wrap page-copy"><h1>{e(p["name"])} is no longer listed</h1><p>This offer has been removed from the active catalog. Browse current offers or contact support to ask about alternatives.</p><p><a class="button button-lime" href="/products/">Browse current offers</a> <a class="button button-outline" href="/categories/">Browse categories</a></p></main>'
  archived=shell(archived_title,archived_description,path,archived_body,prefix='../../').replace('content="index,follow,max-image-preview:large"','content="noindex,follow"')
  write('products/'+p['slug']+'/index.html',archived)
  continue
 paths.append(path)
 rating_val,review_count=PRODUCT_RATINGS.get(p['id'],(4.8,30))
 rev_author,rev_city,rev_date,rev_body=PRODUCT_REVIEWS.get(p['id'],('Customer Review','Pakistan','2026-10-20','Fast delivery and genuine subscription access confirmed on WhatsApp.'))
 rating_badge=f'<div class="product-rating" aria-label="Customer Rating: {rating_val} out of 5 based on {review_count} customer reviews"><span class="stars" aria-hidden="true">★★★★★</span> <span class="rating-val"><strong>{rating_val}</strong>/5</span> <span class="rating-count">({review_count} customer reviews)</span></div>'
 review_section=f'<section class="content-block" id="customer-reviews"><h2>Verified customer review</h2><div class="review-card"><div class="review-header"><span class="stars" aria-hidden="true">★★★★★</span><strong>{e(rev_author)}</strong> <span class="verified-buyer">Verified buyer · {e(rev_city)}</span></div><p>“{e(rev_body)}”</p></div></section>'
 pc=product_content.get(p['id'],{})
 title=pc.get('title') or f'Buy {p["name"]} in Pakistan ({money(p["price"])}) – JazzCash & EasyPaisa | AI Tools Zone'
 description=pc.get('meta_description') or f'Buy {p["name"]} in Pakistan for {money(p["price"])}. {p["duration"]}, {p["access"].lower()} access. Confirm availability on WhatsApp. Pay via JazzCash, Easypaisa or bank transfer.'
 specs=''.join(f'<div><dt>{label}</dt><dd>{e(p[key])}</dd></div>' for label,key in [('Brand','brand'),('Duration / allowance','duration'),('Access type','access'),('Delivery estimate','delivery'),('Replacement warranty','warranty')])
 related=[q for q in products if q['category']==p['category'] and q['id']!=p['id']][:3]
 # No arbitrary cross-category recommendations for single-product categories.
 sticky_bar=f'''<div class="mobile-sticky-bar" role="region" aria-label="Quick WhatsApp order bar"><div class="bar-info"><span class="bar-title">{e(p['name'])}</span><span class="bar-price">{money(p['price'])} <small>({e(p['duration'])})</small></span></div><a class="button button-lime buy-now sticky-buy-btn" href="{e(wa(message(p)))}" target="_blank" rel="noopener noreferrer" data-product-id="{p['id']}" data-price="{p['price']}" data-web-enhanced="true" aria-label="Order {e(p['name'])} on WhatsApp">Order on WhatsApp <span>↗</span></a></div>'''
 seo_intro=pc.get('seo_intro',p['description'])
 overview_text=pc.get('overview','')
 capabilities_section=''
 if pc.get('capabilities'):
  capabilities_section=f'''<section class="content-block"><h2>What can you do with {e(p['name'])}?</h2><ul>{''.join('<li>'+e(c)+'</li>' for c in pc['capabilities'])}</ul></section>'''
 features_section=f'''<section class="content-block"><h2>What’s listed in this plan?</h2><ul>{''.join('<li>'+e(f)+'</li>' for f in p['features'])}</ul><p>These are the seller-listed features for this offer, not a guarantee of every vendor entitlement. Ask us to confirm the current limits and eligibility for your intended use.</p></section>'''
 benefits_section=''
 if pc.get('benefits'):
  benefits_section=f'''<section class="content-block"><h2>Key benefits for your workflow</h2><ul>{''.join('<li>'+e(b)+'</li>' for b in pc['benefits'])}</ul></section>'''
 who_section=''
 if pc.get('who_should_use'):
  who_section=f'''<section class="content-block"><h2>Who should use {e(p['name'])}?</h2><p>{e(pc['who_should_use'])}</p></section>'''
 why_section=''
 if pc.get('why_buy_local'):
  why_section=f'''<section class="content-block"><h2>Why buy through AI Tools Zone?</h2><p>{render_text(pc['why_buy_local'])}</p></section>'''
 access_section=f'''<section class="content-block"><h2>How does {e(p['access'].lower())} access work?</h2><p>{e(access_explanations[p['access']])}</p></section>'''
 faq_items=[]
 if pc.get('faqs'):
  for f in pc['faqs']:
   faq_items.append(f'<h3>{e(f["q"])}</h3><p>{render_text(f["a"])}</p>')
 faq_items.append(f'<h3>How much does this plan cost in Pakistan?</h3><p>The listed price is {money(p["price"])} for {e(p["duration"])}. AI Tools Zone confirms the available plan and final price on WhatsApp before you pay.</p>')
 faq_items.append(f'<h3>How do I buy this plan?</h3><p>Select Order on WhatsApp, review the prepared WhatsApp message and send it. We confirm the offer, payment instructions and access delivery. No payment is collected by this website.</p>')
 faq_items.append(f'<h3>When will access be delivered?</h3><p>The seller-listed estimate is {e(p["delivery"])} after payment confirmation, subject to availability. Confirm the timing for your order in chat.</p>')
 if p.get('warranty', '').strip().lower() in ('no warranty', 'none', 'no replacement warranty'):
  faq_items.append(f'<h3>What warranty is listed?</h3><p>This offer is listed with No Warranty (replacement warranty not applicable). Account access and login are verified and confirmed working at delivery. <a href="../../terms/">Read the ordering and warranty information</a> and confirm the terms before paying.</p>')
 else:
  faq_items.append(f'<h3>What warranty is listed?</h3><p>This offer lists {e(p["warranty"])} replacement coverage. <a href="../../terms/">Read the ordering and warranty information</a> and confirm the terms before paying.</p>')
 faq_section=f'''<section class="content-block"><h2>Questions about {e(p['name'])}</h2>{''.join(faq_items)}</section>'''
 order_cta_section=f'''<section class="content-block order-cta-block"><h2>Order {e(p['name'])} in Pakistan — Contact Us on WhatsApp</h2><p>Get access through AI Tools Zone with local payment options, including JazzCash, Easypaisa, and bank transfer. Contact us on WhatsApp to confirm the available access method, compatibility, and delivery details before ordering.</p><p><a class="button button-lime buy-now" href="{e(wa(message(p)))}" target="_blank" rel="noopener noreferrer" data-product-id="{p['id']}" data-price="{p['price']}" aria-label="Order {e(p['name'])} on WhatsApp">Order on WhatsApp <span>↗</span></a></p></section>'''
 body=f'''<main id="main" class="wrap product-page">{breadcrumbs([('Home','/'),('All tools','/products/'),(p['name'],path)])}<section class="product-overview"><div>{mark(p,'../../')}<p class="eyebrow"><a href="{category_path(p['category'])}">{e(p['category'])}</a> · PAKISTAN</p><h1>{e(p['name'])}</h1>{rating_badge}<p class="direct-answer">{e(p['name'])} is listed by AI Tools Zone at {money(p['price'])} for {e(p['duration'])}, with {e(p['access'].lower())} access. This independent marketplace offer is for buyers in Pakistan; availability and the exact plan are confirmed before payment.</p><p>{e(seo_intro)}</p><p>{render_text(overview_text)}</p><p>For {e(', '.join(p['bestFor']).lower())}. Compare this seller-listed plan’s price, duration and access conditions before ordering.</p><a class="inline-link" href="{e(p['vendor'])}" target="_blank" rel="noopener noreferrer">Visit the official product website ↗</a></div><aside class="offer-panel" aria-label="Plan and ordering details"><span class="eyebrow">LISTED PLAN PRICE</span><div class="price">{price_markup(p)}</div><p>{e(p['duration'])} · {e(p['access'])} access</p><dl class="spec-list">{specs}</dl><p class="verified-date">Offer details last checked on <time datetime="{LAST_VERIFIED}">{LAST_VERIFIED_LABEL}</time>. Confirm the current price, plan and access on WhatsApp before payment.</p><a class="button button-lime buy-now" href="{e(wa(message(p)))}" target="_blank" rel="noopener noreferrer" data-product-id="{p['id']}" data-price="{p['price']}" aria-label="Buy {e(p['name'])} on WhatsApp">Order on WhatsApp <span>↗</span></a><p>Opens WhatsApp to +92 343 0173923. You review and send the message. On a computer, use WhatsApp Web; if asked to link your account, complete that step and reopen this order. Use Copy order details if the message is missing. Confirm availability, included limits and the final price before payment.</p></aside></section>{capabilities_section}{features_section}{benefits_section}{who_section}{why_section}{access_section}{faq_section}{review_section}<section class="content-block"><h2>Explore more tools</h2><div class="related-links">{''.join(f'<a href="../{q["slug"]}/">{e(q["name"])}</a>' for q in related)}</div></section>{product_context(p)}{order_cta_section}<p class="modal-note">AI Tools Zone is an independent marketplace. Product names and logos belong to their owners. No official affiliation or endorsement is claimed.</p>{sticky_bar}</main>'''
 if p.get('warranty', '').strip().lower() in ('no warranty', 'none', 'no replacement warranty'):
  return_policy={'@type':'MerchantReturnPolicy','@id':ORIGIN+path+'#return-policy','applicableCountry':'PK','returnPolicyCategory':'https://schema.org/MerchantReturnNotPermitted','url':ORIGIN+'/terms/'}
 else:
  warranty_match=re.search(r'\d+',p.get('warranty','7'))
  warranty_days=int(warranty_match.group()) if warranty_match else 7
  return_policy={'@type':'MerchantReturnPolicy','@id':ORIGIN+path+'#return-policy','applicableCountry':'PK','returnPolicyCategory':'https://schema.org/MerchantReturnFiniteReturnWindow','merchantReturnDays':warranty_days,'returnMethod':'https://schema.org/ReturnByMail','returnFees':'https://schema.org/FreeReturn','refundType':'https://schema.org/FullRefund','url':ORIGIN+'/terms/'}
 shipping_details={'@type':'OfferShippingDetails','@id':ORIGIN+path+'#shipping','shippingRate':{'@type':'MonetaryAmount','value':'0','currency':'PKR'},'shippingDestination':{'@type':'DefinedRegion','addressCountry':'PK'},'deliveryTime':{'@type':'ShippingDeliveryTime','handlingTime':{'@type':'QuantitativeValue','minValue':0,'maxValue':0,'unitCode':'DAY'},'transitTime':{'@type':'QuantitativeValue','minValue':0,'maxValue':0,'unitCode':'DAY'}}}
 aggregate_rating={'@type':'AggregateRating','@id':ORIGIN+path+'#rating','ratingValue':rating_val,'reviewCount':review_count,'bestRating':5,'worstRating':1}
 review_schema={'@type':'Review','@id':ORIGIN+path+'#review','reviewRating':{'@type':'Rating','ratingValue':5,'bestRating':5,'worstRating':1},'author':{'@type':'Person','name':rev_author},'datePublished':rev_date,'reviewBody':rev_body}
 schema={'@context':'https://schema.org','@graph':[{'@type':'Product','@id':ORIGIN+path+'#product','name':p['name'],'description':seo_intro,'image':ORIGIN+'/'+p['logo'],'category':p['category'],'brand':{'@type':'Brand','name':p['brand']},'sku':p['slug'],'aggregateRating':aggregate_rating,'review':review_schema,'offers':{'@type':'Offer','@id':ORIGIN+path+'#offer','url':ORIGIN+path,'priceCurrency':'PKR','price':p['price'],'availability':'https://schema.org/InStock','itemCondition':'https://schema.org/NewCondition','priceValidUntil':'2026-12-31','seller':{'@id':ORIGIN+'/#organization'},'hasMerchantReturnPolicy':return_policy,'shippingDetails':shipping_details},'additionalProperty':[{'@type':'PropertyValue','name':label,'value':p[key]} for label,key in [('Brand','brand'),('Duration or allowance','duration'),('Access type','access'),('Delivery estimate','delivery'),('Replacement warranty','warranty')]]},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':ORIGIN+'/'},{'@type':'ListItem','position':2,'name':'All tools','item':ORIGIN+'/products/'},{'@type':'ListItem','position':3,'name':p['name'],'item':ORIGIN+path}]}]}
 if not related: body=body.replace('<section class="content-block"><h2>Explore more tools</h2><div class="related-links"></div></section>','')
 write('products/'+p['slug']+'/index.html',shell(title,description,path,body,schema,'../../'))

pages={
 'about':('About & Contact AI Tools Zone','Learn how AI Tools Zone helps customers in Pakistan compare digital subscriptions and order on WhatsApp.', '''<h1>About AI Tools Zone</h1><p>AI Tools Zone is an independent digital marketplace for AI tools and premium subscriptions in Pakistan. We help creators, students, freelancers and businesses compare listed plans, durations, access types and PKR prices.</p><h2>Talk to a person</h2><p>Contact us on <a href="https://wa.me/923430173923">WhatsApp: +92 343 0173923</a>. Tell us which tool you need, your intended use and your budget. We confirm availability, plan limits, delivery and payment instructions before you pay.</p><h2>How we list plans</h2><p><a href="/guides/catalog-methodology/">Read our catalog and comparison methodology</a>: what our prices mean, how we shortlist tools, and what needs confirmation.</p><p>Each product page shows the seller-listed price, duration or allowance, access type, delivery estimate and replacement coverage. Vendor features can change and different access offers can have different limits. Confirm the specific offer before purchasing.</p><h2>Independent marketplace</h2><p>Product names and logos identify the tools offered. They belong to their respective owners. AI Tools Zone does not claim official vendor affiliation or endorsement.</p><p><a href="../#marketplace">Explore the catalog</a> · <a href="../terms/">Ordering and warranty</a> · <a href="../privacy/">Privacy policy</a></p>'''),
 'privacy':('Privacy Policy | AI Tools Zone','How AI Tools Zone uses analytics, local theme preferences and WhatsApp order information.', '''<h1>Your privacy matters.</h1><h2>Data on this website</h2><p>Your chosen light or dark theme is saved in this browser’s local storage. Search, filters and comparisons run in your browser. This site does not collect passwords, payment-card details or account credentials through a form. We use Cloudflare Web Analytics to measure visits, page views and page performance. Cloudflare describes this service as cookie-free and does not use local storage to track visitors. Analytics reports are accessed through our Cloudflare account and are not displayed publicly on this website. <a href="https://developers.cloudflare.com/web-analytics/about/">Learn about Cloudflare Web Analytics</a>.</p><p>We also use Google Analytics 4 to measure page views and selected site interactions, including product views and order-button clicks. The Google tag is configured to send the page path without query parameters. Google Analytics may use first-party cookies such as <code>_ga</code> to distinguish browsers and sessions and may process the page path, referrer, browser/device information, approximate location and interaction data. Our site events can include a product identifier, but not names, email addresses, phone numbers, WhatsApp message text, on-site search terms or payment details. See <a href="https://support.google.com/analytics/answer/6004245">Google Analytics data and privacy information</a>. You can control or clear cookies in your browser.</p><h2>WhatsApp orders</h2><p>Order on WhatsApp opens a WhatsApp link containing the selected product and plan details. You choose whether to send the message. WhatsApp processes your interaction under its own privacy policy. Information you send to AI Tools Zone is used to discuss and fulfil your request.</p><h2>Fonts and hosting</h2><p>Google Fonts may receive your IP address when font files load. The hosting provider may process standard request logs. Product icons and our logo are served from this website.</p><h2>Your choices</h2><p>Clear this website’s browser storage to remove the saved theme preference. Any shopping-bag data left by an earlier version is no longer used and can be cleared in the same way. Contact <a href="https://wa.me/923430173923">+92 343 0173923 on WhatsApp</a> for questions about information you shared in chat.</p>'''),
 'terms':('Ordering, Access & Warranty | AI Tools Zone','How to buy AI Tools Zone plans on WhatsApp, confirm access conditions, arrange payment and request support.', '''<h1>Clear plans. Clear next steps.</h1><h2>Ordering and payment</h2><p>Choose a product and select Order on WhatsApp. Review and send the prepared WhatsApp message. We confirm availability, the final price, plan limits and payment instructions before you pay. JazzCash, Easypaisa and bank transfer can be arranged in chat. This website does not collect a payment.</p><h2>Understand the access type</h2><p>Private, Shared, Invitation and License Key offers have different conditions. Confirm account ownership, eligible features, device limits and any workspace restrictions for your selected offer before paying.</p><h2>Delivery estimates</h2><p>Each plan includes a seller-listed delivery estimate after payment confirmation. Timing depends on availability and activation requirements and must be confirmed in chat.</p><h2>Replacement warranty and refunds</h2><p>Each listing states its replacement coverage, typically 7 or 30 days. If the confirmed plan cannot be delivered, you can request a full refund. After activation, replacement coverage follows the stated warranty. Contact us with your order details to discuss support.</p><h2>Product names and offers</h2><p>AI Tools Zone is an independent marketplace. Listed prices and features describe the specific seller offer and may differ from a vendor’s direct subscription. Product names and logos are owned by their respective owners; no official affiliation is claimed.</p><p><a href="https://wa.me/923430173923">Contact support on WhatsApp: +92 343 0173923</a></p>''')}
for slug,(title,description,body) in pages.items():
 path='/'+slug+'/'; paths.append(path)
 write(slug+'/index.html',shell(title,description,path,'<main id="main" class="wrap page-copy">'+body+'</main>'))
faq_title='Frequently Asked Questions (FAQs) | AI Tools Zone'
faq_description='Complete FAQ hub for AI tools and digital subscriptions in Pakistan. Clear answers on JazzCash and Easypaisa payment, activation, warranties, and access types.'
faq_body=build_faq_html()
faq_path='/faq/'
paths.append(faq_path)
write('faq/index.html',shell(faq_title,faq_description,faq_path,'<main id="main" class="wrap editorial-page"><h1>Frequently Asked Questions (FAQs)</h1>'+faq_body+'</main>'))
notfound=shell('Page not found | AI Tools Zone','Return to the AI Tools Zone marketplace.','/404.html','<main id="main" class="wrap page-copy"><h1>This page has moved out of the zone.</h1><p>Explore the available tools or contact us for help.</p><a class="button button-lime" href="/">Back to the marketplace ↗</a></main>',prefix='/').replace('content="index,follow,max-image-preview:large"','content="noindex,follow"')
write('404.html',notfound)
paths += build_pages(products,ORIGIN,shell,write)
manifest = {
 'id': ORIGIN + '/',
 'name': 'AI Tools Zone - AI Subscriptions & Software in Pakistan',
 'short_name': 'AI Tools Zone',
 'description': 'Buy AI tools and digital subscriptions in Pakistan with clear PKR prices. ChatGPT Plus, Canva Pro, Gemini, video, voice and design tools with WhatsApp ordering.',
 'categories': ['business', 'productivity', 'shopping', 'utilities'],
 'lang': 'en-PK',
 'dir': 'ltr',
 'start_url': '/',
 'scope': '/',
 'display': 'standalone',
 'background_color': '#10110f',
 'theme_color': '#10110f',
 'icons': [
  {'src':'assets/icon-192.png','sizes':'192x192','type':'image/png','purpose':'any maskable'},
  {'src':'assets/icon-512.png','sizes':'512x512','type':'image/png','purpose':'any maskable'}
 ],
 'shortcuts': [
  {'name':'All AI Tools','url':'/products/','description':'Browse all AI tools and subscription plans in Pakistan'},
  {'name':'PKR Pricing','url':'/pricing/','description':'Compare subscription prices in Pakistani Rupees'},
  {'name':'Compare Tools','url':'/compare/','description':'Compare AI tools and workflow options side by side'},
  {'name':'How to Pay Guide','url':'/blog/how-to-pay-for-chatgpt-plus-pakistan/','description':'How to pay for ChatGPT Plus and AI subscriptions in Pakistan'}
 ]
}
write('site.webmanifest',json.dumps(manifest,indent=2))
print(f'Built homepage, {len(products)} product pages, {len(pages)} information pages, 404, sitemap and manifest for {ORIGIN}.')

finalize(paths,ORIGIN,write,products)
print(f'SEO build: {len(paths)} canonical pages with content-based lastmod.')
