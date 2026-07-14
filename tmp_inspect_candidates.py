import json
from pathlib import Path
base = Path('data/raw')
for path in sorted(base.glob('*.json')):
    with path.open('r', encoding='utf-8') as f:
        payload = json.load(f)
    items = payload.get('items', [])
    print(path.name, 'count', len(items), 'contentType', payload.get('contentType'))
    for item in items[:5]:
        print(' ', item.get('contentid'), item.get('title'), '|', item.get('addr1'), '|', (item.get('firstimage') or '')[:80])
    print()
