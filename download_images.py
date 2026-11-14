"""Cache official public product thumbnails. Never stores cookies or credentials."""
import json
import time
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

root = Path(__file__).resolve().parent
data_path = root / 'catalog.json'
data = json.loads(data_path.read_text())
(root / 'images').mkdir(exist_ok=True)
items = [p for p in data['products'] if p.get('image')]

def download(p):
    path = root / 'images' / (p['article'] + '.webp')
    if path.exists() and path.stat().st_size > 500:
        return p['article'], path.name, None
    for attempt in range(3):
        try:
            req = urllib.request.Request(p['image'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=25) as r:
                content = r.read()
                if not r.headers.get('Content-Type', '').startswith('image/'):
                    raise ValueError('response is not an image')
            if len(content) < 500:
                raise ValueError('empty image')
            path.write_bytes(content)
            return p['article'], path.name, None
        except Exception as e:
            error = str(e)
            time.sleep(attempt + 1)
    return p['article'], None, error

results = {}
with ThreadPoolExecutor(max_workers=5) as pool:
    for n, f in enumerate(as_completed([pool.submit(download,p) for p in items]), 1):
        article, name, error = f.result()
        results[article] = (name,error)
        if n % 50 == 0 or n == len(items):
            print(f'Images {n}/{len(items)}; errors {sum(bool(e) for _,e in results.values())}', flush=True)
for p in data['products']:
    if p['article'] in results:
        name,error = results[p['article']]
        if name:
            p['localImage']='images/'+name
        elif error:
            p['imageError']=error
data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(json.dumps({'images':len(items),'saved':sum(bool(n) for n,e in results.values()),'failed':sum(bool(e) for n,e in results.values())}),flush=True)
