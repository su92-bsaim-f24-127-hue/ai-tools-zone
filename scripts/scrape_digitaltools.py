import urllib.request
import ssl
from bs4 import BeautifulSoup
import re
import csv
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://digitaltools.com.pk/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

print(f"Title: {soup.title.string if soup.title else 'No Title'}")

# WooCommerce / WordPress standard extraction
# Look for product cards: li.product, div.product, etc.
products = []
product_elements = soup.find_all(['li', 'div'], class_=re.compile(r'product', re.I))
print(f"Found {len(product_elements)} product elements")

for p in product_elements:
    title_el = p.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|name|product', re.I))
    price_el = p.find(class_=re.compile(r'price', re.I))
    
    if title_el and price_el:
        name = title_el.get_text(strip=True)
        price_text = price_el.get_text(strip=True)
        link_el = p.find('a', href=True)
        link = link_el['href'] if link_el else ''
        
        # Clean price
        m = re.search(r'([\d,]+)', price_text.replace('₨', '').replace('Rs', '').replace('PKR', ''))
        cleaned_price = m.group(1).replace(',', '') if m else ''
        
        if name and len(name) > 2 and name not in [x['name'] for x in products]:
            products.append({
                'name': name,
                'price_raw': price_text,
                'price': cleaned_price,
                'link': link
            })

print(f"Extracted {len(products)} unique products from digitaltools.com.pk")
for p in products[:15]:
    print(f"- {p['name']} | Price: {p['price_raw']} -> {p['price']} | Link: {p['link']}")
