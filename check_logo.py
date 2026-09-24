from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'.test-deps'))
from playwright.sync_api import sync_playwright
root=Path(__file__).parent
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.goto('http://127.0.0.1:8080',wait_until='networkidle')
    page.emulate_media(reduced_motion='reduce')
    for width in [1440,390]:
        page.set_viewport_size({'width':width,'height':1000 if width==1440 else 844})
        page.locator('header').screenshot(path=str(root/f'verification/logo-header-{width}.png'))
        page.locator('footer').scroll_into_view_if_needed()
        page.locator('footer').screenshot(path=str(root/f'verification/logo-footer-{width}.png'))
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert page.locator('header .brand img').evaluate('e=>e.complete && e.naturalWidth>0')
        assert page.locator('footer .brand img').evaluate('e=>e.complete && e.naturalWidth>0')
        page.locator('header .brand').click()
        assert page.url.endswith('#')
    assert page.request.get('http://127.0.0.1:8080/assets/icon-48.png').status==200
    assert (root/'assets/icon-48.png').stat().st_size<10000
    assert page.locator('.hero-brand-logo').evaluate('e=>e.complete && e.naturalWidth>0')
    print('PASS: header/footer logos load at desktop and mobile sizes; no overflow; home link and favicon work.')
    browser.close()
