import urllib.request
import ssl
from bs4 import BeautifulSoup
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='ignore')

# 1. Inspect aitoolgems.tech
html_gems = fetch_html('https://aitoolgems.tech/')
soup_gems = BeautifulSoup(html_gems, 'html.parser')
cards_gems = soup_gems.find_all(class_=re.compile(r'product|card|item', re.I))
print(f"aitoolgems: found {len(cards_gems)} card-like elements")

# Look for titles and prices in aitoolgems
gems_products = []
for el in soup_gems.find_all(['div', 'article', 'section'], class_=re.compile(r'product|card', re.I)):
    text = el.get_text(separator=' ', strip=True)
    if 'PKR' in text or 'Rs' in text or '/-' in text:
        # extract name and price
        lines = [line.strip() for line in el.stripped_strings if line.strip()]
        if len(lines) >= 2:
            gems_products.append(lines[:5])

print(f"aitoolgems extracted candidate blocks: {len(gems_products)}")
if gems_products:
    print("Sample aitoolgems block:", gems_products[0])
