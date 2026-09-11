from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent/'.test-deps'))
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},color_scheme='dark',reduced_motion='reduce')
    page.goto('http://127.0.0.1:8080',wait_until='networkidle')
    assert page.locator('html').get_attribute('data-theme')=='dark'
    page.locator('#theme-toggle').click()
    assert page.locator('html').get_attribute('data-theme')=='light'
    assert page.locator('.button-black').evaluate('e=>getComputedStyle(e).color')=='rgb(240, 240, 232)'
    page.reload(wait_until='networkidle')
    assert page.locator('html').get_attribute('data-theme')=='light'
    page.screenshot(path='verification/theme-light-desktop.png')
    page.set_viewport_size({'width':360,'height':800})
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('#theme-toggle').click()
    assert page.locator('html').get_attribute('data-theme')=='dark'
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path='verification/theme-dark-mobile.png')
    print('PASS: theme switching, saved preference, light-theme button contrast and mobile overflow.')
    browser.close()
