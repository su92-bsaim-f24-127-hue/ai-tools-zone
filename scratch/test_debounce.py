import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

async def main():
    root = Path('.').resolve()
    target_url = (root / 'products/chatgpt-plus/index.html').as_uri()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=EDGE_PATH, headless=True)
        mobile_page = await browser.new_page(viewport={'width': 390, 'height': 844})
        
        events_emitted = []
        await mobile_page.expose_function('recordEvent', lambda detail: events_emitted.append(detail))
        
        await mobile_page.add_init_script("""
            document.addEventListener('aitz:measure', e => {
                window.recordEvent(e.detail);
            });
        """)
        
        await mobile_page.goto(target_url)
        await mobile_page.wait_for_timeout(500)
        
        # Dispatch two rapid clicks within 50ms via page evaluate
        events_emitted.clear()
        await mobile_page.evaluate("""() => {
            const btn = document.querySelector('.sticky-buy-btn');
            btn.click();
            setTimeout(() => btn.click(), 50);
        }""")
        await mobile_page.wait_for_timeout(300)
        
        lead_events = [e for e in events_emitted if e['name'] == 'generate_lead']
        print(f"Lead events captured on rapid double click: {len(lead_events)}")
        print(f"All captured event names: {[e['name'] for e in events_emitted]}")
        assert len(lead_events) == 1, f"Debounce failed: expected 1 generate_lead, got {len(lead_events)}"
        
        await browser.close()
        print("DEBOUNCE TEST PASSED PERFECTLY!")

if __name__ == '__main__':
    asyncio.run(main())
