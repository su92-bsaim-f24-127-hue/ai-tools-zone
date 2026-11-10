import json
from pathlib import Path

path = Path('data/seo-contract.json')
contract = json.loads(path.read_text(encoding='utf-8'))

new_route = "/compare/leonardo-vs-midjourney/"
if new_route not in contract['routes']:
    contract['routes'].append(new_route)

contract['routes'].sort()
contract['expected_pages'] = len(contract['routes'])
contract['reason'] = "Add Leonardo AI vs Midjourney comparison page for commercial AI image generator search queries in Pakistan; preserve all existing routes and product slugs."

path.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('Updated data/seo-contract.json. Expected pages:', contract['expected_pages'])
