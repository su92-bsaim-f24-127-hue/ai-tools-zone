import json
from pathlib import Path
from bs4 import BeautifulSoup

def main():
    catalog = json.loads(Path('data/catalog.json').read_text(encoding='utf-8'))
    print(f"Authoritative Catalog Count: {len(catalog)}")
    
    results = []
    for p in catalog:
        slug = p['slug']
        html_file = Path(f'products/{slug}/index.html')
        if not html_file.exists():
            print(f"ERROR: {html_file} missing")
            continue
            
        soup = BeautifulSoup(html_file.read_text(encoding='utf-8'), 'html.parser')
        title = soup.title.string.strip() if soup.title else ''
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_tag.get('content', '').strip() if meta_tag else ''
        h1 = soup.h1.string.strip() if soup.h1 else ''
        
        # Check canonical
        canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
        canonical = canonical_tag.get('href', '').strip() if canonical_tag else ''
        
        # Check headings
        headings = [h.name for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        
        results.append({
            'id': p['id'],
            'name': p['name'],
            'slug': slug,
            'price': p['price'],
            'duration': p['duration'],
            'access': p['access'],
            'canonical': canonical,
            'title': title,
            'title_len': len(title),
            'meta': meta_desc,
            'meta_len': len(meta_desc),
            'h1': h1,
            'headings_count': len(headings),
            'headings_list': headings
        })
        
        print(f"[{p['id']}] {p['name']} ({slug})")
        print(f"  Title ({len(title)} chars): {title}")
        print(f"  Meta ({len(meta_desc)} chars): {meta_desc}")
        print(f"  H1: {h1}")
        print(f"  Canonical: {canonical}")
        print(f"  Price: PKR {p['price']:,} / {p['duration']} ({p['access']})")
        print("-" * 50)

if __name__ == '__main__':
    main()
