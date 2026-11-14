"""Build a portable HTML catalog from the captured public product snapshot."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
catalog = json.loads((root / 'catalog.json').read_text())
assert len(catalog['products']) == catalog['targetCount'], 'incomplete collection'
assert len({p['article'] for p in catalog['products']}) == catalog['targetCount'], 'duplicate articles'
for p in catalog['products']:
    assert p['url'].startswith('https://www.arket.com/ko-kr/about-arket/product.')
    if p['status'] == 'ok':
        assert p['price'] >= 0 and p['originalPrice'] >= p['price']
        assert p['availableSizes'] == [s['name'] for s in p['sizes'] if s['available']]
        assert p['article'] in p['url']
payload = json.dumps(catalog, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
template = (root / 'template.html').read_text()
assert template.count('__CATALOG_DATA__') == 1
(root / 'index.html').write_text(template.replace('__CATALOG_DATA__', payload))
(root / '.nojekyll').touch()
print(json.dumps({'products':len(catalog['products']), 'verified':sum(p['status']=='ok' for p in catalog['products']), 'unavailable':sum(p['status']=='error' for p in catalog['products']), 'htmlBytes':(root/'index.html').stat().st_size}))
