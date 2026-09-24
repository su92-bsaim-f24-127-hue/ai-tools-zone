"""Rebuild crawlable storefront HTML from the catalog and local brand assets."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from datetime import date
import json, re

ROOT=Path(__file__).parent
ORIGIN='https://aitoolszone.tech'
WA='923136726285'
VERSION='20260916-hero3d-2'
products=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
logos=json.loads((ROOT/'assets/product-logo-sources.json').read_text(encoding='utf-8'))
e=lambda s:escape(str(s),quote=True)
money=lambda n:f'PKR {n:,}'
for p in products:
 p['slug']=re.sub(r'[^a-z0-9]+','-',p['name'].lower()).strip('-')
 if 'path' not in logos[p['id']]: raise ValueError('Missing original logo: '+p['id'])
 p['logo']=logos[p['id']]['path']
 p['vendor']=logos[p['id']]['website']

def write(path,text):
 target=ROOT/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(text,encoding='utf-8')
def wa(message): return 'https://wa.me/'+WA+'?text='+quote(message)
def message(p):
 return f"Assalam-o-Alaikum AI Tools Zone!\nI would like to buy {p['name']}.\nListed price: {money(p['price'])}\nDuration: {p['duration']}\nAccess: {p['access']}\nDelivery estimate: {p['delivery']}\nReplacement warranty: {p['warranty']}\nPlease confirm availability, plan limits, final price and payment details."
def mark(p,prefix=''):
 return f'<span class="tool-mark mark-{p["id"]}"><img src="{prefix}{p["logo"]}" alt="" width="64" height="64" loading="lazy" decoding="async"></span>'
def card(p):
 return f'''<article class="product-card" data-product="{p['id']}"><div class="product-card-top">{mark(p)}<span class="badge">{e(p['access'])}</span></div><div class="product-category">{e(p['category'])}</div><h3><a href="products/{p['slug']}/">{e(p['name'])}</a></h3><p>{e(p['description'])}</p><div class="plan-meta"><span>{e(p['duration'])}</span><span>{e(p['access'])}</span></div><div class="card-price"><small>PKR</small> {p['price']:,}</div><div class="card-actions"><a class="button buy-now" href="{e(wa(message(p)))}" target="_blank" rel="noopener noreferrer" aria-label="Buy {e(p['name'])} on WhatsApp">Buy Now <span>↗</span></a><a class="details-button" href="products/{p['slug']}/" aria-label="View {e(p['name'])} details">ⓘ</a></div><label class="card-compare"><input type="checkbox" data-compare="{p['id']}"> Compare tool</label></article>'''
def structured(data):
 return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'
def metadata(title,description,path,kind='website'):
 url=ORIGIN+path
 return f'''<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="AI Tools Zone"><meta property="og:locale" content="en_PK">
<meta property="og:url" content="{url}"><meta property="og:image" content="{ORIGIN}/assets/social-card.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="AI Tools Zone logo — digital subscriptions in Pakistan">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{ORIGIN}/assets/social-card.jpg">'''

organization={'@type':'Organization','@id':ORIGIN+'/#organization','name':'AI Tools Zone','url':ORIGIN+'/', 'logo':ORIGIN+'/assets/icon-512.png','description':'Independent digital marketplace offering AI tools and digital subscriptions in Pakistan, with listed PKR prices and WhatsApp ordering.','contactPoint':{'@type':'ContactPoint','telephone':'+92-313-6726285','contactType':'customer support','areaServed':'PK','availableLanguage':['en','ur']}}
theme_button='''<button id="theme-toggle" class="icon-button theme-toggle" type="button" aria-label="Light theme" aria-pressed="false"><svg class="theme-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg><svg class="theme-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"/></svg></button>'''
def header(prefix):
 return f'''<a class="skip-link" href="#main">Skip to content</a><header class="page-header wrap"><a class="brand" href="{prefix}" aria-label="AI Tools Zone home"><span class="brand-emblem"><img src="{prefix}assets/brand-icon.webp" alt="" width="128" height="128"></span><span>AI TOOLS<span class="brand-bottom">ZONE</span></span></a><div class="header-actions">{theme_button}<a class="button button-outline" href="{prefix}#marketplace">All tools ↗</a></div></header>'''
def footer(prefix):
 return f'''<footer class="page-footer wrap"><span>© {date.today().year} AI Tools Zone. Independent marketplace.</span><a href="{prefix}about/">About & contact</a><a href="{prefix}privacy/">Privacy</a><a href="{prefix}terms/">Ordering & warranty</a><a href="https://wa.me/{WA}">+92 313 6726285</a></footer>'''
def shell(title,description,path,body,schema=None,prefix='../'):
 return f'''<!doctype html><html lang="en-PK"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#10110f"><script src="{prefix}theme.js?v={VERSION}"></script><title>{e(title)}</title><meta name="description" content="{e(description)}">{metadata(title,description,path)}<link rel="icon" href="{prefix}assets/icon-48.png" type="image/png" sizes="48x48"><link rel="apple-touch-icon" href="{prefix}assets/icon-180.png"><link rel="stylesheet" href="{prefix}styles.css?v={VERSION}"><link rel="stylesheet" href="{prefix}enhancements.css?v={VERSION}">{structured(schema) if schema else ''}</head><body>{header(prefix)}{body}{footer(prefix)}<noscript><style>#theme-toggle{{display:none}}</style></noscript></body></html>'''

home=(ROOT/'templates/home.html').read_text(encoding='utf-8')
home=home.replace('__ASSET_VERSION__',VERSION)
home=home.replace('lang="en"','lang="en-PK"')
home=home.replace('class="wrap brand-band-inner"','class="wrap brand-band-inner" tabindex="0" role="region" aria-label="Featured product brands"')
title='AI Tools & Digital Subscriptions in Pakistan | AI Tools Zone'
description='Compare AI tools and digital subscriptions in Pakistan. View PKR prices, plan details and access types, then buy through AI Tools Zone on WhatsApp.'
schema={'@context':'https://schema.org','@graph':[organization,{'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/','name':'AI Tools Zone','publisher':{'@id':ORIGIN+'/#organization'},'inLanguage':'en-PK'},{'@type':'ItemList','name':'AI tools and digital subscriptions','itemListElement':[{'@type':'ListItem','position':i+1,'url':ORIGIN+'/products/'+p['slug']+'/','name':p['name']} for i,p in enumerate(products)]}]}
home=home.replace('<!-- SEO_HEAD -->',metadata(title,description,'/')+'\n'+structured(schema))
home=re.sub(r'<!-- CATALOG_START -->.*?<!-- CATALOG_END -->','<div id="product-grid" class="product-grid">'+''.join(map(card,products))+'</div>',home,flags=re.S)
categories=list(dict.fromkeys(p['category'] for p in products))
cats=''.join(f'<a class="category-card" data-browse-category="{e(c)}" href="#marketplace"><span class="category-icon"><img src="assets/brand-icon.webp" alt="" width="40" height="40" loading="lazy"></span><h3>{e(c)}</h3><small>{sum(p["category"]==c for p in products)} tools</small><span aria-hidden="true">↗</span></a>' for c in categories)
home=re.sub(r'<!-- CATEGORIES_START -->.*?<!-- CATEGORIES_END -->','<div id="category-grid" class="category-grid">'+cats+'</div>',home,flags=re.S)
home=re.sub(r'<span class="tool-mark(?: mark-[^"]+)?" data-logo="([^"]+)"></span>',lambda m:mark(next(p for p in products if p['id']==m[1])),home)
home=re.sub(r'<a([^>]*?) data-wa="([^"]*)"([^>]*)>',lambda m:'<a'+m[1]+' href="'+e(wa(__import__('html').unescape(m[2])))+'" target="_blank" rel="noopener noreferrer"'+m[3]+'>',home)
bundle=[p for p in products if p['id'] in ['chatgpt','canva','capcut','elevenlabs']]
total=sum(p['price'] for p in bundle)
bundle_message='I would like the AI Tools Zone creator stack:\n'+'\n'.join(f'{p["name"]}: {money(p["price"])} | {p["duration"]} | {p["access"]}' for p in bundle)+f'\nCombined listed price: {money(total)}. Please confirm availability, limits and payment details.'
home=home.replace('id="buy-stack" href="https://wa.me/'+WA+'"','id="buy-stack" href="'+e(wa(bundle_message))+'" target="_blank" rel="noopener noreferrer"')
home=home.replace('PKR 7,400 <small>',money(total)+' <small>')
home=home.replace('    <section id="categories"','    <section class="answer-strip wrap" aria-labelledby="about-store"><h2 id="about-store">AI subscriptions in Pakistan, with a person to help.</h2><p>AI Tools Zone is an independent digital marketplace for creators, students and businesses in Pakistan. Compare seller-listed prices in PKR, read each plan’s access type and duration, and select Buy Now to discuss your order on WhatsApp. Availability and plan limits are confirmed before payment.</p><a class="inline-link" href="about/">About AI Tools Zone & contact ↗</a></section>\n    <section id="categories"')
home=home.replace('<button data-privacy>Privacy</button>','<a href="privacy/">Privacy</a><a href="terms/">Ordering & warranty</a>')
home=home.replace('<h3>Here to help</h3>','<h3>Here to help</h3><a href="about/">About & contact</a>')
write('index.html',home)
write('catalog.js','// Generated by build_site.py from data/catalog.json.\nwindow.PRODUCTS = '+json.dumps(products,ensure_ascii=False,separators=(',',':'))+';\n')

paths=['/']
access_explanations={
 'Private':'This listing is marked Private. Confirm whether access is issued to your existing account or a separate account, along with device limits, before paying.',
 'Invitation':'This listing uses an invitation to a workspace or team. Confirm eligibility, administrator controls, included features and what happens when the plan ends before paying.',
 'Shared':'This listing uses shared access. Confirm the permitted usage, profile or device limits, and privacy conditions before paying. It is not a private account.',
 'License Key':'This listing provides a license key. Confirm the edition, device count, activation conditions and replacement coverage before paying.'}
for p in products:
 path='/products/'+p['slug']+'/'
 paths.append(path)
 title=f'{p["name"]} Price in Pakistan | AI Tools Zone'
 description=f'{p["name"]}: {money(p["price"])}. {p["duration"]}, {p["access"].lower()} access. View seller-listed features and order on WhatsApp. Availability confirmed before payment.'
 specs=''.join(f'<div><dt>{label}</dt><dd>{e(p[key])}</dd></div>' for label,key in [('Duration / allowance','duration'),('Access type','access'),('Delivery estimate','delivery'),('Replacement warranty','warranty')])
 related=[q for q in products if q['category']==p['category'] and q['id']!=p['id']][:3]
 if not related: related=[q for q in products if q['id']!=p['id']][:3]
 body=f'''<main id="main" class="wrap product-page"><nav aria-label="Breadcrumb"><ol class="breadcrumb"><li><a href="../../">Home</a></li><li aria-hidden="true">/</li><li><a href="../../#marketplace">All tools</a></li><li aria-hidden="true">/</li><li aria-current="page">{e(p['name'])}</li></ol></nav><section class="product-overview"><div>{mark(p,'../../')}<p class="eyebrow">{e(p['category'])} · PAKISTAN</p><h1>{e(p['name'])}</h1><p>{e(p['description'])}</p><p>For {e(', '.join(p['bestFor']).lower())}. Compare this seller-listed plan’s price, duration and access conditions before ordering.</p><a class="inline-link" href="{e(p['vendor'])}" target="_blank" rel="noopener noreferrer">Visit the official product website ↗</a></div><aside class="offer-panel" aria-label="Plan and ordering details"><span class="eyebrow">LISTED PLAN PRICE</span><div class="price"><small>PKR</small> {p['price']:,}</div><p>{e(p['duration'])} · {e(p['access'])} access</p><dl class="spec-list">{specs}</dl><a class="button button-lime buy-now" href="{e(wa(message(p)))}" target="_blank" rel="noopener noreferrer" aria-label="Buy {e(p['name'])} on WhatsApp">Buy Now <span>↗</span></a><p>Opens WhatsApp to +92 313 6726285. You review and send the message. Confirm availability, included limits and the final price before payment.</p></aside></section><section class="content-block"><h2>What’s listed in this plan?</h2><ul>{''.join('<li>'+e(f)+'</li>' for f in p['features'])}</ul><p>These are the seller-listed features for this offer, not a guarantee of every vendor entitlement. Ask us to confirm the current limits and eligibility for your intended use.</p></section><section class="content-block"><h2>How does {e(p['access'].lower())} access work?</h2><p>{e(access_explanations[p['access']])}</p></section><section class="content-block"><h2>Questions about {e(p['name'])}</h2><h3>How much does this plan cost in Pakistan?</h3><p>The listed price is {money(p['price'])} for {e(p['duration'])}. AI Tools Zone confirms the available plan and final price on WhatsApp before you pay.</p><h3>How do I buy this plan?</h3><p>Select Buy Now, review the prepared WhatsApp message and send it. We confirm the offer, payment instructions and access delivery. No payment is collected by this website.</p><h3>When will access be delivered?</h3><p>The seller-listed estimate is {e(p['delivery'])} after payment confirmation, subject to availability. Confirm the timing for your order in chat.</p><h3>What warranty is listed?</h3><p>This offer lists {e(p['warranty'])} replacement coverage. <a href="../../terms/">Read the ordering and warranty information</a> and confirm the terms before paying.</p></section><section class="content-block"><h2>Explore more tools</h2><div class="related-links">{''.join(f'<a href="../{q["slug"]}/">{e(q["name"])}</a>' for q in related)}</div></section><p class="modal-note">AI Tools Zone is an independent marketplace. Product names and logos belong to their owners. No official affiliation or endorsement is claimed.</p></main>'''
 schema={'@context':'https://schema.org','@graph':[{'@type':'Product','@id':ORIGIN+path+'#product','name':p['name'],'description':p['description'],'image':ORIGIN+'/'+p['logo'],'category':p['category'],'offers':{'@type':'Offer','url':ORIGIN+path,'priceCurrency':'PKR','price':p['price'],'seller':{'@type':'Organization','name':'AI Tools Zone','url':ORIGIN+'/'}},'additionalProperty':[{'@type':'PropertyValue','name':label,'value':p[key]} for label,key in [('Duration or allowance','duration'),('Access type','access'),('Delivery estimate','delivery'),('Replacement warranty','warranty')]]},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':ORIGIN+'/'},{'@type':'ListItem','position':2,'name':p['name'],'item':ORIGIN+path}]}]}
 write('products/'+p['slug']+'/index.html',shell(title,description,path,body,schema,'../../'))

pages={
 'about':('About & Contact AI Tools Zone','Learn how AI Tools Zone helps customers in Pakistan compare digital subscriptions and order on WhatsApp.', '''<h1>About AI Tools Zone</h1><p>AI Tools Zone is an independent digital marketplace for AI tools and premium subscriptions in Pakistan. We help creators, students, freelancers and businesses compare listed plans, durations, access types and PKR prices.</p><h2>Talk to a person</h2><p>Contact us on <a href="https://wa.me/923136726285">WhatsApp: +92 313 6726285</a>. Tell us which tool you need, your intended use and your budget. We confirm availability, plan limits, delivery and payment instructions before you pay.</p><h2>How we list plans</h2><p>Each product page shows the seller-listed price, duration or allowance, access type, delivery estimate and replacement coverage. Vendor features can change and different access offers can have different limits. Confirm the specific offer before purchasing.</p><h2>Independent marketplace</h2><p>Product names and logos identify the tools offered. They belong to their respective owners. AI Tools Zone does not claim official vendor affiliation or endorsement.</p><p><a href="../#marketplace">Explore the catalog</a> · <a href="../terms/">Ordering and warranty</a> · <a href="../privacy/">Privacy policy</a></p>'''),
 'privacy':('Privacy Policy | AI Tools Zone','How AI Tools Zone uses local theme preferences and WhatsApp order information.', '''<h1>Your privacy matters.</h1><h2>Data on this website</h2><p>Your chosen light or dark theme is saved in this browser’s local storage. Search, filters and comparisons run in your browser. This site does not collect passwords, payment-card details or account credentials through a form. It has no integrated analytics service.</p><h2>WhatsApp orders</h2><p>Buy Now opens a WhatsApp link containing the selected product and plan details. You choose whether to send the message. WhatsApp processes your interaction under its own privacy policy. Information you send to AI Tools Zone is used to discuss and fulfil your request.</p><h2>Fonts and hosting</h2><p>Google Fonts may receive your IP address when font files load. The hosting provider may process standard request logs. Product icons and our logo are served from this website.</p><h2>Your choices</h2><p>Clear this website’s browser storage to remove the saved theme preference. Any shopping-bag data left by an earlier version is no longer used and can be cleared in the same way. Contact <a href="https://wa.me/923136726285">+92 313 6726285 on WhatsApp</a> for questions about information you shared in chat.</p>'''),
 'terms':('Ordering, Access & Warranty | AI Tools Zone','How to buy AI Tools Zone plans on WhatsApp, confirm access conditions, arrange payment and request support.', '''<h1>Clear plans. Clear next steps.</h1><h2>Ordering and payment</h2><p>Choose a product and select Buy Now. Review and send the prepared WhatsApp message. We confirm availability, the final price, plan limits and payment instructions before you pay. JazzCash, Easypaisa and bank transfer can be arranged in chat. This website does not collect a payment.</p><h2>Understand the access type</h2><p>Private, Shared, Invitation and License Key offers have different conditions. Confirm account ownership, eligible features, device limits and any workspace restrictions for your selected offer before paying.</p><h2>Delivery estimates</h2><p>Each plan includes a seller-listed delivery estimate after payment confirmation. Timing depends on availability and activation requirements and must be confirmed in chat.</p><h2>Replacement warranty and refunds</h2><p>Each listing states its replacement coverage, typically 7 or 30 days. If the confirmed plan cannot be delivered, you can request a full refund. After activation, replacement coverage follows the stated warranty. Contact us with your order details to discuss support.</p><h2>Product names and offers</h2><p>AI Tools Zone is an independent marketplace. Listed prices and features describe the specific seller offer and may differ from a vendor’s direct subscription. Product names and logos are owned by their respective owners; no official affiliation is claimed.</p><p><a href="https://wa.me/923136726285">Contact support on WhatsApp: +92 313 6726285</a></p>''')}
for slug,(title,description,body) in pages.items():
 path='/'+slug+'/'; paths.append(path)
 write(slug+'/index.html',shell(title,description,path,'<main id="main" class="wrap page-copy">'+body+'</main>'))
notfound=shell('Page not found | AI Tools Zone','Return to the AI Tools Zone marketplace.','/404.html','<main id="main" class="wrap page-copy"><h1>This page has moved out of the zone.</h1><p>Explore the available tools or contact us for help.</p><a class="button button-lime" href="/">Back to the marketplace ↗</a></main>',prefix='/').replace('content="index,follow,max-image-preview:large"','content="noindex,follow"')
write('404.html',notfound)
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{ORIGIN}{path}</loc></url>\n' for path in paths)+'</urlset>\n')
write('robots.txt',f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
write('site.webmanifest',json.dumps({'name':'AI Tools Zone','short_name':'AI Tools Zone','start_url':'/','display':'browser','background_color':'#10110f','theme_color':'#10110f','icons':[{'src':'assets/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'assets/icon-512.png','sizes':'512x512','type':'image/png'}]},indent=2))
print(f'Built homepage, {len(products)} product pages, {len(pages)} information pages, 404, sitemap and manifest for {ORIGIN}.')
