"""Check app/Web order parity and copy recovery without sending any messages."""
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import sys,json
ROOT=Path(__file__).parent;sys.path.insert(0,str(ROOT/'.test-deps'))
from playwright.sync_api import sync_playwright
results=[]
def check(name,ok):results.append({'name':name,'passed':bool(ok)});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    context=browser.new_context(reduced_motion='reduce',viewport={'width':1440,'height':1000})
    context.route('https://web.whatsapp.com/**',lambda r:r.fulfill(status=200,body='Web navigation intercepted, no message sent.'))
    page=context.new_page();page.goto('http://127.0.0.1:8080/',wait_until='networkidle');page.locator('#show-more').click()
    page.wait_for_function("document.querySelectorAll('.product-card .whatsapp-web-link').length===20")
    for card in page.locator('.product-card').all():
        app=parse_qs(urlparse(card.locator('.buy-now').get_attribute('href')).query)
        web=urlparse(card.locator('.whatsapp-web-link').get_attribute('href'));params=parse_qs(web.query)
        check(card.get_attribute('data-product')+' Web message parity',web.netloc=='web.whatsapp.com' and params.get('phone')==['923430173923'] and params.get('text')==app.get('text'))
    page.locator('#search').fill('ChatGPT');page.wait_for_function("document.querySelectorAll('.product-card .whatsapp-web-link').length===1")
    check('Search rebuild has exactly one alternate per product',page.locator('.product-card .order-alternatives').count()==1)
    for width in (320,390,768,1440):
        page.set_viewport_size({'width':width,'height':900});check(f'Order controls fit {width}',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.goto('http://127.0.0.1:8080/products/chatgpt-plus/',wait_until='networkidle')
    original=parse_qs(urlparse(page.locator('.buy-now').get_attribute('href')).query)['text'][0]
    page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.copied=text}}})")
    page.locator('.order-alternatives button').click();check('Copy preserves complete order',page.evaluate('copied')==original)
    page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('Permission denied')}}})")
    page.locator('.order-alternatives button').click();check('Denied clipboard gives selectable message',page.locator('.order-alternatives textarea').input_value()==original)
    page.evaluate("window.events=[];document.addEventListener('aitz:measure',e=>events.push(e.detail))")
    with page.expect_popup() as popup:page.locator('.whatsapp-web-link').click()
    check('Direct Web navigation uses correct phone',parse_qs(urlparse(popup.value.url).query).get('phone')==['923430173923']);popup.value.close()
    check('Web click counted locally as order not vendor link',{e['name'] for e in page.evaluate('events')}=={'whatsapp_click','product_whatsapp_click'})
    page.goto('http://127.0.0.1:8080/',wait_until='networkidle');page.locator('[data-detail="chatgpt"]').click()
    check('Quick view Web alternative',page.locator('#modal .whatsapp-web-link').count()==1)
    browser.close()
report={'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'results':results}
(ROOT/'verification/whatsapp-web-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='results'}));raise SystemExit(bool(report['failed']))
