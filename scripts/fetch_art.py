#!/usr/bin/env python3
"""Download the portraits listed in content/art.json from Wikimedia Commons.

Writes  dist/assets/portraits/<id>.jpg        master, at most 600 px wide
        dist/assets/portraits/<id>-192.webp   small copy for the reader
Needs Pillow. Existing files are kept; pass --force to download them again.
Run `python3 scripts/build.py` after this script.
"""
import io, json, os, sys, time, urllib.parse, urllib.request
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'dist', 'assets', 'portraits')
API = 'https://commons.wikimedia.org/w/api.php'
UA = {'User-Agent': 'DCWayfinderArtFetch/0.1 (study reader; build script)'}
WIDTH = 600

def fetch(url):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return r.read()
        except Exception as e:
            error = e
            wait = getattr(e, 'headers', None) and e.headers.get('Retry-After')
            time.sleep(int(wait) if wait and wait.isdigit() else 15 * (attempt + 1))
    raise error

art = json.load(open(os.path.join(ROOT, 'content', 'art.json'), encoding='utf-8'))
os.makedirs(OUT, exist_ok=True)
force = '--force' in sys.argv
todo = {pid: a for pid, a in art.items() if force or not os.path.exists(os.path.join(OUT, a['file']))}
ids = list(todo)
done = 0
for i in range(0, len(ids), 20):
    batch = ids[i:i + 20]
    query = urllib.parse.urlencode({'action': 'query', 'titles': '|'.join('File:' + todo[p]['commonsFile'] for p in batch),
                                    'prop': 'imageinfo', 'iiprop': 'url', 'iiurlwidth': WIDTH, 'format': 'json'})
    result = json.loads(fetch(f'{API}?{query}'))['query']
    renamed = {n['to']: n['from'] for n in result.get('normalized', [])}
    urls = {}
    for page in result['pages'].values():
        info = (page.get('imageinfo') or [None])[0]
        if info: urls[renamed.get(page['title'], page['title'])[5:]] = info.get('thumburl') or info['url']
    for pid in batch:
        url = urls.get(todo[pid]['commonsFile'])
        if not url: print('missing on Commons:', pid); continue
        image = Image.open(io.BytesIO(fetch(url)))
        image.seek(0)
        image = image.convert('RGB')
        # An optional `crop` is [left, top, right, bottom] as fractions of the image.
        if todo[pid].get('crop'):
            l, t, r, b = todo[pid]['crop']
            image = image.crop((round(l * image.width), round(t * image.height), round(r * image.width), round(b * image.height)))
        if image.width > WIDTH: image = image.resize((WIDTH, round(image.height * WIDTH / image.width)), Image.LANCZOS)
        master = os.path.join(OUT, todo[pid]['file'])
        image.save(master, 'JPEG', quality=88, optimize=True)
        # The reader shows a square cut from the top of the image.
        side = min(image.size)
        left = (image.width - side) // 2
        image.crop((left, 0, left + side, side)).resize((192, 192), Image.LANCZOS).save(master[:-4] + '-192.webp', 'WEBP', quality=82)
        done += 1
        print('saved', todo[pid]['file'], f'{image.width}x{image.height}', flush=True)
        time.sleep(1.5)
print(f'{done} downloaded, {len(art) - len(todo)} already present, {len(todo) - done} failed.')
