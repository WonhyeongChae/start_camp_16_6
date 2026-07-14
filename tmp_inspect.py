import json
from pathlib import Path
base = Path('data/raw')
for path in sorted(base.glob('*.json')):
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    items = data.get('items', [])
    print(path.name, 'count=', len(items), 'contentType=', data.get('contentType'), 'region=', data.get('region'))
    if items:
        sample = items[0]
        print(' sample=', sample.get('title'), '|', sample.get('contentid'), '|', sample.get('addr1'))
