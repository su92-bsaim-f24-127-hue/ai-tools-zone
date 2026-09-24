"""Full storefront audit. All WhatsApp navigation is intercepted; no messages are sent."""
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urljoin
import json, sys, re, xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).parent/'.test-deps'))
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parent
OUT=ROOT/'verification'; OUT.mkdir(exist_ok=True)
BASE='http://127.0.0.1:8080'
checks=[]; errors=[]; violations=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)})
 print(('PASS ' if value else 'FAIL ')+name,flush=True)
def no_overflow(page): return page.evaluate('document.documentElement.scrollWidth <= innerWidth')

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 context=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='dark',reduced_motion='reduce')
 context.route('https://wa.me/**',lambda route:route.fulfill(status=200,body='WhatsApp destination intercepted by local audit.'))
 page=context.new_page(); page.on('pageerror',lambda error:errors.append(str(error)))
 response=page.goto(BASE,wait_until='networkidle')
 check('Homepage returns HTTP 200',response.status==200)
 check('Brand logo replaces old rings',page.locator('.hero-brand-logo').count()==1 and page.locator('#zone-canvas').count()==0)
 check('Shopping bag controls removed',page.locator('[data-add],[data-cart],#add-stack,.cart-trigger').count()==0)
 check('Reduced motion pauses brand animation',page.locator('body').evaluate("el=>el.classList.contains('paused')"))
 page.emulate_media(reduced_motion='no-preference')
 first=page.locator('.logo-float').evaluate('el=>getComputedStyle(el).transform')
 page.wait_for_timeout(350)
 check('Logo really animates in 3D',first!=page.locator('.logo-float').evaluate('el=>getComputedStyle(el).transform'))
 page.locator('#motion-toggle').click()
 check('Logo animation can be paused',page.locator('.logo-float').evaluate('el=>getComputedStyle(el).animationPlayState')=='paused')
 page.emulate_media(reduced_motion='reduce')
 products=page.evaluate('PRODUCTS')
 page.locator('#show-more').click()
 check('All 20 products expand',page.locator('.product-card').count()==20)
 page.locator('#product-grid').screenshot(path=str(OUT/'updated-all-products.png'))
 for product in products:
  a=page.locator(f'[data-product="{product["id"]}"] .buy-now')
  link=a.get_attribute('href'); order=parse_qs(urlparse(link).query)['text'][0]
  check(product['name']+' direct Buy Now details',urlparse(link).netloc=='wa.me' and urlparse(link).path=='/923136726285' and all(str(v) in order for v in [product['name'],f'{product["price"]:,}',product['duration'],product['access'],product['warranty']]))
  check(product['name']+' original local logo',page.locator(f'[data-product="{product["id"]}"] .tool-mark img').evaluate('el=>el.complete && el.naturalWidth>0') and product['logo'].startswith('assets/products/'))
 with page.expect_popup() as popup_info: page.locator('.buy-now').first.click()
 popup=popup_info.value; popup.wait_for_load_state()
 check('Buy Now opens the correct WhatsApp destination',popup.url.startswith('https://wa.me/923136726285?text='))
 popup.close()
 page.locator('#search').fill('ChatGPT'); check('Search returns matching product',page.locator('.product-card').count()==1)
 page.locator('#search').fill('no-result-123'); check('Empty search offers reset',page.locator('[data-reset]').is_visible())
 page.locator('[data-reset]').click()
 page.locator('#filter-toggle').click(); page.locator('#access-filter').select_option('Private'); page.locator('#budget-filter').fill('1000')
 check('Budget and access filters combine',page.locator('.product-card').count()==1 and 'CapCut' in page.locator('.product-card').inner_text())
 page.locator('#reset-filters').click()
 for category in dict.fromkeys(q['category'] for q in products):
  page.locator('[data-category]').filter(has_text=re.compile('^'+re.escape(category)+'$')).click()
  check('Category '+category,page.locator('.product-card').count()==sum(q['category']==category for q in products))
 page.locator('[data-category="All tools"]').click()
 for sort in ['price-low','price-high','name']:
  page.locator('#sort').select_option(sort)
  ids=page.locator('.product-card').evaluate_all('els=>els.map(el=>el.dataset.product)')
  expected=sorted(products,key=(lambda q:q['name'].lower()) if sort=='name' else (lambda q:q['price']),reverse=sort=='price-high')
  check('Sort '+sort,ids==[q['id'] for q in expected])
 page.locator('#reset-filters').click()
 for id in ['chatgpt','gemini']: page.locator(f'[data-compare="{id}"]').check()
 page.locator('#compare-bar [data-open-compare]').click()
 check('Comparison renders correct plans',page.locator('.compare-table thead th').count()==3)
 page.locator('.compare-table [data-detail]').first.click()
 check('Detail dialog uses Buy Now',page.locator('#modal a').filter(has_text='Buy Now').count()==1)
 page.locator('[data-modal-back]').click(); check('Dialog back restores comparison',page.locator('.compare-table').count()==1)
 page.keyboard.press('Escape'); page.locator('#clear-compare').click()
 for intent in ['writing','video','design','code','study','voice','automation','business','entertainment','vpn']:
  page.locator('[data-finder]').first.click(); page.locator('[name=intent]').select_option(intent); page.locator('[name=budget]').select_option('any'); page.locator('#finder-form button').click()
  check('Finder '+intent,page.locator('.finder-result').count()>0)
  page.keyboard.press('Escape')
 page.locator('#theme-toggle').click(); page.reload(wait_until='networkidle')
 check('Light theme persists after reload',page.locator('html').get_attribute('data-theme')=='light' and page.locator('body').evaluate('el=>getComputedStyle(el).backgroundColor')=='rgb(247, 248, 242)')
 for theme in ['light','dark']:
  if page.locator('html').get_attribute('data-theme')!=theme: page.locator('#theme-toggle').click()
  for width,height in [(1440,1000),(1024,768),(768,1024),(390,844),(360,800)]:
   page.set_viewport_size({'width':width,'height':height}); page.evaluate('scrollTo(0,0)')
   check(f'{theme} layout at {width}px',no_overflow(page))
   if width in [1440,390]:
    page.screenshot(path=str(OUT/f'updated-{theme}-{width}.png'))
    page.locator('#marketplace').evaluate('el=>el.scrollIntoView({block:"start",behavior:"instant"})'); page.screenshot(path=str(OUT/f'updated-catalog-{theme}-{width}.png'))
    page.evaluate('scrollTo(0,0)')
  page.locator('#menu-toggle').click(); check(theme+' mobile menu opens',page.locator('#main-nav').is_visible())
  page.keyboard.press('Escape'); check(theme+' menu Escape',page.locator('#menu-toggle').get_attribute('aria-expanded')=='false')
  if (OUT/'axe.min.js').exists():
   page.add_script_tag(path=str(OUT/'axe.min.js'))
   result=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
   violations.extend({'theme':theme,'id':v['id'],'impact':v['impact'],'nodes':[{'target':n['target'],'summary':n['failureSummary']} for n in v['nodes']]} for v in result['violations'])
 check('Theme and animation buttons at least 40px',page.locator('#theme-toggle').bounding_box()['width']>=40 and page.locator('#motion-toggle').bounding_box()['width']>=40)
 page.set_viewport_size({'width':1440,'height':1000})
 for product in products:
  path='/products/'+product['slug']+'/'
  response=page.goto(BASE+path,wait_until='domcontentloaded')
  schemas=[json.loads(s) for s in page.locator('script[type="application/ld+json"]').all_text_contents()]
  product_schema=schemas[0]['@graph'][0]
  check(product['name']+' crawlable page and schema',response.status==200 and page.locator('h1').inner_text()==product['name'] and page.locator('link[rel=canonical]').get_attribute('href')=='https://aitoolszone.tech'+path and product_schema['offers']['price']==product['price'] and 'aggregateRating' not in product_schema)
  check(product['name']+' page Buy Now',urlparse(page.locator('.buy-now').get_attribute('href')).path=='/923136726285')
  if product['id']=='chatgpt':
   for theme in ['dark','light']:
    if page.locator('html').get_attribute('data-theme')!=theme:page.locator('#theme-toggle').click()
    for width in [1440,390]:
     page.set_viewport_size({'width':width,'height':900}); check(f'{theme} product page {width}px',no_overflow(page)); page.screenshot(path=str(OUT/f'updated-product-{theme}-{width}.png'),full_page=True)
   page.set_viewport_size({'width':1440,'height':1000})
 for slug in ['about','privacy','terms']:
  response=page.goto(BASE+'/'+slug+'/',wait_until='domcontentloaded');check(slug+' information page',response.status==200 and page.locator('h1').count()==1)
 sitemap=ET.fromstring(page.request.get(BASE+'/sitemap.xml').text())
 urls=[n.text for n in sitemap.findall('{*}url/{*}loc')]
 check('Sitemap contains 24 canonical URLs',len(urls)==24 and all(u.startswith('https://aitoolszone.tech/') for u in urls))
 check('Robots lists correct sitemap','Sitemap: https://aitoolszone.tech/sitemap.xml' in page.request.get(BASE+'/robots.txt').text())
 check('Favicon optimized below 10 KB',(ROOT/'assets/icon-48.png').stat().st_size<10000)
 # Check all internally referenced resources and links from generated pages.
 checked=set(); bad=[]
 for file in [ROOT/'index.html',*ROOT.glob('products/*/index.html'),*ROOT.glob('about/index.html'),*ROOT.glob('privacy/index.html'),*ROOT.glob('terms/index.html')]:
  page_url=BASE+'/'+file.relative_to(ROOT).as_posix().replace('index.html','')
  text=file.read_text(encoding='utf-8')
  for ref in re.findall(r'(?:href|src)="([^"]+)"',text):
   url=urljoin(page_url,ref).split('#')[0]
   if not url.startswith(BASE) or url in checked: continue
   checked.add(url); status=page.request.get(url).status
   if status!=200: bad.append((url,status))
 check(f'All {len(checked)} local links and resources resolve',not bad)
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
 plain=nojs.new_page();plain.goto(BASE,wait_until='networkidle')
 check('All 20 plans readable without JavaScript',plain.locator('.product-card').count()==20)
 check('Buy Now works without JavaScript',plain.locator('.product-card .buy-now[href^="https://wa.me/923136726285"]').count()==20)
 check('No-JS mobile layout fits',no_overflow(plain))
 plain.goto(BASE+'/products/chatgpt-plus/',wait_until='domcontentloaded');check('Product details readable without JavaScript',plain.locator('h1').inner_text()=='ChatGPT Plus' and plain.locator('.buy-now').count()==1)
 check('No uncaught JavaScript errors',not errors)
 browser.close()
report={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,'js_errors':errors,'broken_links':bad,'accessibility_violations':violations}
(OUT/'audit-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['passed','failed','js_errors']}));print('Accessibility rule violations:',len(violations))
sys.exit(1 if report['failed'] else 0)
