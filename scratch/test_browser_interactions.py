import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

async def main():
    root = Path('.').resolve()
    target_url = (root / 'products/chatgpt-plus/index.html').as_uri()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=EDGE_PATH, headless=True)
        
        # Test 1: Desktop Viewport (1280x800)
        desktop_page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        await desktop_page.goto(target_url)
        
        desktop_sticky_bar = desktop_page.locator('.mobile-sticky-bar')
        is_desktop_visible = await desktop_sticky_bar.is_visible()
        print(f"Desktop sticky bar visible: {is_desktop_visible} (Expected: False)")
        assert not is_desktop_visible, "Sticky bar should be hidden on desktop viewports!"
        
        # Test 2: Mobile Viewport (iPhone 14 / 390x844)
        mobile_page = await browser.new_page(viewport={'width': 390, 'height': 844})
        
        # Capture CustomEvent and dataLayer
        events_emitted = []
        await mobile_page.expose_function('recordEvent', lambda detail: events_emitted.append(detail))
        
        await mobile_page.add_init_script("""
            window.capturedEvents = [];
            document.addEventListener('aitz:measure', e => {
                window.capturedEvents.push(e.detail);
                window.recordEvent(e.detail);
            });
        """)
        
        await mobile_page.goto(target_url)
        await mobile_page.wait_for_timeout(500)
        
        mobile_sticky_bar = mobile_page.locator('.mobile-sticky-bar')
        is_mobile_visible = await mobile_sticky_bar.is_visible()
        print(f"Mobile sticky bar visible: {is_mobile_visible} (Expected: True)")
        assert is_mobile_visible, "Sticky bar should be visible on mobile viewports!"
        
        # Verify text inside sticky bar
        bar_text = await mobile_sticky_bar.inner_text()
        print(f"Mobile sticky bar text: {bar_text.strip().replace(chr(10), ' ')}")
        assert "PKR 2,300" in bar_text, "Sticky bar must display exact PKR price!"
        assert "ChatGPT Plus" in bar_text, "Sticky bar must display product name!"
        
        # Verify initial pageview and product view events
        initial_event_names = [e['name'] for e in events_emitted]
        print(f"Initial events on product page: {initial_event_names}")
        assert 'page_view' in initial_event_names, "page_view must be emitted"
        assert 'product_view' in initial_event_names, "product_view must be emitted"
        assert 'product_page_view' in initial_event_names, "product_page_view must be emitted"
        
        # Test Click & Debounce
        sticky_btn = mobile_sticky_bar.locator('.sticky-buy-btn')
        events_emitted.clear()
        
        # Rapid double click
        await sticky_btn.click()
        await sticky_btn.click()
        await mobile_page.wait_for_timeout(300)
        
        click_events = [e['name'] for e in events_emitted]
        print(f"Events after rapid double click: {click_events}")
        lead_events = [e for e in events_emitted if e['name'] == 'generate_lead']
        assert len(lead_events) == 1, f"Expected exactly 1 generate_lead event due to debounce, got {len(lead_events)}"
        lead = lead_events[0]
        print(f"generate_lead detail: {lead}")
        assert lead['product'] == 'chatgpt'
        assert lead['value'] == 2300
        assert lead['currency'] == 'PKR'
        
        # Verify padding-bottom on mobile
        padding = await mobile_page.eval_on_selector('.product-page', 'el => window.getComputedStyle(el).paddingBottom')
        print(f"Product page padding-bottom on mobile: {padding}")
        assert padding == '76px', f"Expected padding-bottom 76px, got {padding}"
        
        await browser.close()
        print("ALL BROWSER INTERACTION TESTS PASSED CLEANLY IN REAL CHROMIUM ENGINE!")

if __name__ == '__main__':
    asyncio.run(main())
