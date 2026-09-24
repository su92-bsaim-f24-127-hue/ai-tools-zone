"""Regression checks for the 3D-rendered homepage emblem and its motion."""
from pathlib import Path
import json
import sys
from PIL import Image

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / '.test-deps'))
from playwright.sync_api import sync_playwright

OUT = ROOT / 'verification'
OUT.mkdir(exist_ok=True)
checks = []
errors = []

def check(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)

for filename in ['hero-logo-3d.webp', 'hero-logo-3d-mobile.webp']:
    with Image.open(ROOT / 'assets' / filename) as asset:
        check(filename + ' has real alpha transparency', asset.mode == 'RGBA' and asset.getchannel('A').getextrema() == (0, 255))
        check(filename + ' fits web asset budget', (ROOT / 'assets' / filename).stat().st_size < 250000)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1, reduced_motion='no-preference')
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('http://127.0.0.1:8080/', wait_until='networkidle')
    art = page.locator('#hero-art')
    logo = page.locator('.hero-brand-logo')
    floating = page.locator('.logo-float')
    check('New sculpted logo is loaded', logo.evaluate("el=>el.complete && el.naturalWidth>0 && el.currentSrc.includes('hero-logo-3d')"))
    check('Old backing plate is removed', page.locator('.logo-depth').count() == 0)
    check('Original favicon is retained', page.locator('link[rel=icon]').first.get_attribute('href') == 'assets/icon-48.png')
    check('No silhouette-clipping frame', logo.evaluate("el=>getComputedStyle(el).clipPath === 'none'"))
    first = floating.evaluate('el=>getComputedStyle(el).transform')
    page.wait_for_timeout(600)
    check('Sculpted emblem floats and rotates', first != floating.evaluate('el=>getComputedStyle(el).transform'))
    box = art.bounding_box()
    page.mouse.move(box['x'] + box['width'] * .8, box['y'] + box['height'] * .3)
    check('Pointer tilt responds', art.evaluate("el=>parseFloat(el.style.getPropertyValue('--ry')) > 0"))
    page.mouse.move(0, 0)
    check('Pointer tilt resets', art.evaluate("el=>el.style.getPropertyValue('--ry') === '0deg'"))
    page.locator('#motion-toggle').click()
    check('Pause stops emblem and shadow', all(page.locator(selector).evaluate("el=>getComputedStyle(el).animationPlayState === 'paused'") for selector in ['.logo-float', '.logo-shadow']))
    page.locator('#motion-toggle').click()
    check('Play resumes motion', floating.evaluate("el=>getComputedStyle(el).animationPlayState === 'running'"))
    page.emulate_media(reduced_motion='reduce')
    check('Reduced motion disables emblem and shadow animations', all(page.locator(selector).evaluate("el=>getComputedStyle(el).animationName === 'none'") for selector in ['.logo-float', '.logo-shadow']))
    for theme in ['light', 'dark']:
        if page.locator('html').get_attribute('data-theme') != theme:
            page.locator('#theme-toggle').click()
        for width, height in [(1440, 1000), (1024, 900), (768, 1024), (390, 844), (360, 800)]:
            page.set_viewport_size({'width': width, 'height': height})
            art.scroll_into_view_if_needed()
            page.wait_for_timeout(150)
            check(f'{theme} {width}px has no horizontal overflow', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
            bounds = logo.bounding_box()
            check(f'{theme} {width}px emblem stays inside viewport', bounds['x'] >= 0 and bounds['x'] + bounds['width'] <= width)
            if width in [1440, 390]:
                art.screenshot(path=str(OUT / f'hero-3d-{theme}-{width}.png'))
                page.evaluate("scrollTo({top:0,behavior:'instant'})")
                page.screenshot(path=str(OUT / f'home-3d-{theme}-{width}.png'))
    check('No JavaScript errors', not errors)
    browser.close()

result = {'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks), 'checks': checks, 'js_errors': errors}
(OUT / 'hero-logo-results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({k: result[k] for k in ['passed', 'failed', 'js_errors']}))
sys.exit(1 if result['failed'] else 0)
