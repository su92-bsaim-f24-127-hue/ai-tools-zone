"""Audit representative page templates and interactive states with axe-core."""
from pathlib import Path
import json, sys
sys.path.insert(0,str(Path(__file__).parent/'.test-deps'))
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
OUT=ROOT/'verification'
reports=[]
def audit(page,name):
 page.add_script_tag(path=str(OUT/'axe.min.js'))
 result=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})")
 violations=[{'id':v['id'],'impact':v['impact'],'nodes':[{'target':n['target'],'summary':n['failureSummary']} for n in v['nodes']]} for v in result['violations']]
 reports.append({'page':name,'violations':violations,'passed_rules':len(result['passes'])})
 print(name,len(violations),'violations',flush=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
 for theme in ['light','dark']:
  context=browser.new_context(color_scheme=theme,reduced_motion='reduce',viewport={'width':1440,'height':1000})
  page=context.new_page()
  for route in ['/','/products/chatgpt-plus/','/about/','/privacy/','/terms/']:
   page.goto('http://127.0.0.1:8080'+route,wait_until='networkidle')
   audit(page,theme+' desktop '+route)
   if route=='/products/chatgpt-plus/':
    page.set_viewport_size({'width':390,'height':844});audit(page,theme+' mobile product');page.set_viewport_size({'width':1440,'height':1000})
  page.goto('http://127.0.0.1:8080/',wait_until='networkidle')
  page.locator('[data-detail]').first.click();audit(page,theme+' product dialog');page.keyboard.press('Escape')
  page.locator('[data-finder]').first.click();audit(page,theme+' finder');page.keyboard.press('Escape')
  page.locator('footer [data-open-compare]').click();audit(page,theme+' compare picker')
  page.locator('#modal [data-compare="chatgpt"]').check();page.locator('#modal [data-compare="gemini"]').check();page.locator('#modal [data-open-compare]').click()
  page.set_viewport_size({'width':390,'height':844});audit(page,theme+' mobile comparison');page.keyboard.press('Escape')
  audit(page,theme+' mobile home')
  context.close()
 browser.close()
(OUT/'accessibility-results.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
print('Total violations:',sum(len(r['violations']) for r in reports))
sys.exit(1 if any(r['violations'] for r in reports) else 0)
