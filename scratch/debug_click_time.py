import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

async def main():
    root = Path('.').resolve()
    target_url = (root / 'products/chatgpt-plus/index.html').as_uri()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=EDGE_PATH, headless=True)
        mobile_page = await browser.new_page(viewport={'width': 390, 'height': 844})
        
        mobile_page.on('console', lambda msg: print('PAGE CONSOLE:', msg.text))
        
        await mobile_page.goto(target_url)
        sticky_bar = mobile_page.locator('.mobile-sticky-bar')
        sticky_btn = sticky_bar.locator('.sticky-buy-btn')
        
        t0 = time.time()
        await sticky_btn.click()
        t1 = time.time()
        print(f"Time for click 1: {(t1 - t0)*1000:.1f}ms")
        await sticky_btn.click()
        t2 = time.time()
        print(f"Time for click 2: {(t2 - t1)*1000:.1f}ms")
        print(f"Total time: {(t2 - t0)*1000:.1f}ms")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
