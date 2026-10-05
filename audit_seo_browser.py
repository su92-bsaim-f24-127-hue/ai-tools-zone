"""Check every canonical page in mobile/no-JS and desktop/JS contexts."""
from pathlib import Path
import json, sys, xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).parent/'.test-deps'))
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
paths=[n.text.replace('https://aitoolszone.tech','') for n in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
checks=[]; errors=[]; metrics={}
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    for js,width in [(False,390),(True,1440)]:
        context=browser.new_context(java_script_enabled=js,viewport={'width':width,'height':900},reduced_motion='reduce')
        page=context.new_page()
        page.on('pageerror',lambda error:errors.append(str(error)))
        for path in paths:
            response=page.goto('http://127.0.0.1:8080'+path,wait_until='load')
            result={'path':path,'js':js,'width':width,'status':response.status,'h1':page.locator('h1').count(),'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth'),'main_text':len(page.locator('main').inner_text())}
            result['passed']=result['status']==200 and result['h1']==1 and not result['overflow'] and result['main_text']>180
            checks.append(result)
        if js:
            for path in ['/','/pricing/','/categories/','/compare/chatgpt-vs-gemini/','/products/chatgpt-plus/']:
                for width in [320,768,1024]:
                    page.set_viewport_size({'width':width,'height':900})
                    page.goto('http://127.0.0.1:8080'+path,wait_until='load')
                    checks.append({'path':path,'width':width,'passed':page.evaluate('document.documentElement.scrollWidth<=innerWidth')})
            page.set_viewport_size({'width':1440,'height':1000})
            page.goto('http://127.0.0.1:8080/pricing/',wait_until='networkidle')
            page.screenshot(path=str(ROOT/'verification/seo-pricing-desktop.png'),full_page=True)
            page.set_viewport_size({'width':390,'height':844});page.goto('http://127.0.0.1:8080/categories/ai-assistants/',wait_until='networkidle')
            page.screenshot(path=str(ROOT/'verification/seo-category-mobile.png'),full_page=True)
            page.goto('http://127.0.0.1:8080/',wait_until='networkidle')
            page.locator('#category-grid a').first.click()
            checks.append({'name':'Category anchors navigate with JS','passed':'/categories/ai-assistants/' in page.url})
            page.goto('http://127.0.0.1:8080/products/chatgpt-plus/',wait_until='networkidle')
            page.evaluate("window.testEvents=[];document.addEventListener('aitz:measure',e=>testEvents.push(e.detail))")
            context.route('https://wa.me/**',lambda route:route.fulfill(status=200,body='Intercepted test only'))
            with page.expect_popup() as popup:page.locator('.buy-now').click()
            popup.value.close()
            events=page.evaluate('testEvents')
            checks.append({'name':'Optional WhatsApp click events have only bounded product context, no personal fields','passed':len(events)==2 and {e['name'] for e in events}=={'whatsapp_click','product_whatsapp_click'} and all(set(e)=={'name','page','section','product'} and e['product']=='chatgpt' for e in events)})
        context.close()
    # A local desktop lab observation, explicitly not field CWV or a ranking score.
    context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
    context.add_init_script("window.lab={lcp:null,cls:0};new PerformanceObserver(l=>{for(const e of l.getEntries())lab.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)lab.cls+=e.value}).observe({type:'layout-shift',buffered:true});")
    page=context.new_page();page.goto('http://127.0.0.1:8080/',wait_until='networkidle');page.wait_for_timeout(1000)
    metrics=page.evaluate('({ ...lab,domNodes:document.querySelectorAll("*").length,resourceCount:performance.getEntriesByType("resource").length,thirdPartyHosts:[...new Set(performance.getEntriesByType("resource").map(e=>new URL(e.name).hostname).filter(h=>h!==location.hostname))]})')
    browser.close()
report={'checks':len(checks),'failed':[c for c in checks if not c['passed']],'console_errors':errors,'local_desktop_lab_not_field_CWV':metrics,'results':checks}
(ROOT/'verification/seo-browser.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
sys.exit(bool(report['failed'] or errors))
