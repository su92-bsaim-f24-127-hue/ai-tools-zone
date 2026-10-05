"""Discovery/conversion tests; WhatsApp requests are intercepted and never sent."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).parent;sys.path.insert(0,str(ROOT/'.test-deps'))
from playwright.sync_api import sync_playwright
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)});print(('PASS ' if value else 'FAIL ')+name,flush=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    context=browser.new_context(reduced_motion='reduce',viewport={'width':390,'height':844})
    context.route('https://wa.me/**',lambda r:r.fulfill(status=200,body='Intercepted; no message sent'))
    context.add_init_script("window.measured=[];document.addEventListener('aitz:measure',e=>measured.push(e.detail))")
    page=context.new_page();page.goto('http://127.0.0.1:8080/',wait_until='networkidle')
    def ids():return page.locator('.product-card').evaluate_all('els=>els.map(e=>e.dataset.product)')
    cases=[('I need an AI video tool',{'veo','elevenlabs','capcut','adobe'}),('AI tools under PKR 2000',{'gemini','leonardo','canva','capcut','adobe','lovable'}),('AI tools for students',{'chatgpt','gemini','canva','gamma','notion'}),('tools for YouTube',{'veo','elevenlabs','capcut','adobe'}),('private AI subscriptions',{'chatgpt','leonardo','elevenlabs','figma','capcut','adobe','lovable','gamma','replit','n8n'}),('YouTube Premium',{'youtube'}),('nonexistent-unicorn-product',set())]
    for query,expected in cases:
        page.locator('#search').fill(query)
        check(query,set(ids())==expected)
    page.locator('#search').fill('');page.locator('#filter-toggle').click()
    page.locator('#intent-filter').select_option('study');page.locator('#duration-filter').select_option('monthly')
    check('Audience + duration intersect',ids()==['chatgpt'])
    page.locator('#access-filter').select_option('Shared');check('Conflicting filters produce empty state',ids()==[])
    page.locator('#reset-filters').click();check('Reset restores default 8',len(ids())==8)
    for width in (320,390,768,1024,1440):
        page.set_viewport_size({'width':width,'height':1000})
        check(f'Expanded filters no overflow {width}',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    check('Filter/query state leaves canonical and URL unchanged',page.url=='http://127.0.0.1:8080/' and page.locator('link[rel="canonical"]').get_attribute('href')=='https://aitoolszone.tech/')
    page.locator('#search').fill('PRIVATE_QUERY_03330000000');page.wait_for_timeout(650)
    check('Search event contains no query/phone',any(e['name']=='tool_search' for e in page.evaluate('measured')) and '03330000000' not in json.dumps(page.evaluate('measured')))
    page.evaluate("aitzMeasure('not_allowed',{product:'03330000000',message:'secret'})")
    check('Unknown event rejected',not any(e['name']=='not_allowed' for e in page.evaluate('measured')))
    page.locator('#reset-filters').click()
    page.locator('[data-compare="chatgpt"]').check()
    check('Compare add event',any(e['name']=='compare_add' and e.get('product')=='chatgpt' for e in page.evaluate('measured')))
    page.locator('[data-finder]').first.click()
    check('Finder start event',any(e['name']=='tool_finder_start' for e in page.evaluate('measured')))
    page.locator('#finder-form button[type="submit"]').click()
    check('Finder completion event',any(e['name']=='tool_finder_complete' for e in page.evaluate('measured')))
    page.keyboard.press('Escape')
    check('Filter event',any(e['name']=='filter_use' for e in page.evaluate('measured')))
    page.goto('http://127.0.0.1:8080/compare/chatgpt-vs-gemini/',wait_until='networkidle')
    check('Comparison view hook',any(e['name']=='comparison_view' for e in page.evaluate('measured')))
    with page.expect_popup() as popup:page.locator('[data-product-id="chatgpt"]').click()
    popup.value.close()
    check('Product WhatsApp click hook',any(e['name']=='product_whatsapp_click' and e['product']=='chatgpt' for e in page.evaluate('measured')))
    check('Comparison order table before explanation',page.locator('h2').first.inner_text()=='Listed plans at a glance')
    for path,event in [('/products/chatgpt-plus/','product_view'),('/categories/ai-video/','category_view'),('/alternatives/chatgpt/','alternative_view'),('/guides/catalog-methodology/','guide_view'),('/pricing/','pricing_view')]:
        page.goto('http://127.0.0.1:8080'+path,wait_until='domcontentloaded')
        check(event,any(e['name']==event for e in page.evaluate('measured')))
    page.goto('http://127.0.0.1:8080/products/chatgpt-plus/',wait_until='domcontentloaded')
    context.route('https://chatgpt.com/**',lambda r:r.fulfill(status=200,body='Intercepted vendor link'))
    # prevent navigation while preserving the real bubbling click for event verification
    page.locator('main a[target="_blank"]').first.evaluate("el=>el.addEventListener('click',e=>e.preventDefault())")
    page.locator('main a[target="_blank"]').first.click()
    check('Outbound vendor event',any(e['name']=='outbound_vendor_click' for e in page.evaluate('measured')))
    browser.close()
report={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)}
(ROOT/'verification/growth-browser.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'}));raise SystemExit(bool(report['failed']))
