"""RTT-001 era photos (DEC-221): find candidate photographs of the devices of each era on Wikimedia Commons.

Runs on a GitHub-hosted runner (.github/workflows/rtt001_photos.yml), because Wikimedia answers HTTP 429 to the Claude
Code cloud container (6 Oct 2026). Standard library only.

    python scripts/rtt001_photo_candidates.py kits/rtt-001/photo_search.json OUT_DIR

For every era in photo_search.json, each query is run as a Commons file search (namespace 6, bitmaps only) and each
listed category is read; every hit's file page metadata is read through the API (extmetadata). A file is kept only if
  - its licence allows commercial use: public domain / PD-*, CC0, CC BY x.y, CC BY-SA x.y (never NC, never ND, never
    GFDL-only, never "fair use" / non-free);
  - it is a JPEG or PNG at least 1000 px wide;
  - it is not a duplicate of a file already kept.
Kept files (at most `per_era` per era, in query order) are downloaded as Commons' own 1600 px wide rendering of the
file (thumburl; the same licensed work, scaled) to OUT_DIR/<era>/<nn>_<safe title>.jpg|png, and OUT_DIR/manifest.json
records for each: era, file title, file page, original size, licence, licence URL, author (artist, HTML stripped),
credit, attribution required, restrictions (personality rights, trademarks), description (first 300 characters),
the downloaded rendering's URL, size and SHA-256, and the original's SHA-1 (from the API). Prints a one-line summary
per kept file and nothing else. The photos are never committed to the public repo (DEC-006, DEC-060).
"""
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = 'RaceThroughTime/1.0 (https://github.com/marketmarathon/race-through-time; one-off search for about 40 device photos)'
API = 'https://commons.wikimedia.org/w/api.php'
OK = re.compile(r'^(public domain|pd\b.*|cc0.*|cc[- ]by(-sa)?[- ][0-9.]+.*|cc[- ]by(-sa)?$)', re.I)
BAD = re.compile(r'\b(nc|nd|non-?commercial|no ?deriv|fair use|non-free)\b', re.I)


def get(url, tries=7):
    wait = 5
    for i in range(tries):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                ra = e.headers.get('Retry-After')
                time.sleep(int(ra) if ra and ra.isdigit() else wait)
                wait *= 2
                continue
            raise


def api(params):
    time.sleep(1.0)
    params = dict(params, format='json', formatversion='2')
    return json.loads(get(API + '?' + urllib.parse.urlencode(params)))


def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()


def info(titles):
    out = {}
    for i in range(0, len(titles), 40):
        r = api({'action': 'query', 'titles': '|'.join(titles[i:i + 40]), 'prop': 'imageinfo',
                 'iiprop': 'url|size|mime|sha1|extmetadata', 'iiurlwidth': '1600'})
        for p in r.get('query', {}).get('pages', []):
            if p.get('imageinfo'):
                out[p['title']] = p['imageinfo'][0]
    return out


def main():
    spec, outdir = sys.argv[1], sys.argv[2]
    S = json.load(open(spec, encoding='utf-8'))
    os.makedirs(outdir, exist_ok=True)
    manifest, seen = [], set()
    for era in S['eras']:
        titles = []
        for q in era.get('queries', []):
            r = api({'action': 'query', 'list': 'search', 'srsearch': q + ' filetype:bitmap', 'srnamespace': '6', 'srlimit': str(S.get('per_query', 10))})
            titles += [h['title'] for h in r.get('query', {}).get('search', [])]
        for c in era.get('categories', []):
            r = api({'action': 'query', 'list': 'categorymembers', 'cmtitle': c, 'cmtype': 'file', 'cmlimit': str(S.get('per_category', 15))})
            titles += [m['title'] for m in r.get('query', {}).get('categorymembers', [])]
        titles = [t for i, t in enumerate(titles) if t not in titles[:i]]
        meta = info(titles)
        kept = 0
        for t in titles:
            ii = meta.get(t)
            if not ii or t in seen or kept >= S.get('per_era', 12):
                continue
            em = ii.get('extmetadata', {})
            lic = strip(em.get('LicenseShortName', {}).get('value', ''))
            if not OK.match(lic) or BAD.search(lic) or ii.get('mime') not in ('image/jpeg', 'image/png') or ii.get('width', 0) < 1000:
                continue
            seen.add(t); kept += 1
            ext = 'png' if ii['mime'] == 'image/png' else 'jpg'
            safe = re.sub(r'[^A-Za-z0-9]+', '_', t[5:].rsplit('.', 1)[0])[:60]
            d = os.path.join(outdir, era['id']); os.makedirs(d, exist_ok=True)
            fn = '%02d_%s.%s' % (kept, safe, ext)
            url = ii.get('thumburl') or ii['url']
            b = get(url); time.sleep(1.0)
            open(os.path.join(d, fn), 'wb').write(b)
            row = {'era': era['id'], 'file': era['id'] + '/' + fn, 'title': t, 'page': ii.get('descriptionurl'),
                   'original_size': [ii.get('width'), ii.get('height')], 'licence': lic,
                   'licence_url': strip(em.get('LicenseUrl', {}).get('value', '')),
                   'author': strip(em.get('Artist', {}).get('value', ''))[:200], 'credit': strip(em.get('Credit', {}).get('value', ''))[:200],
                   'attribution_required': strip(em.get('AttributionRequired', {}).get('value', '')),
                   'restrictions': strip(em.get('Restrictions', {}).get('value', '')),
                   'description': strip(em.get('ImageDescription', {}).get('value', ''))[:300],
                   'date': strip(em.get('DateTimeOriginal', {}).get('value', ''))[:40],
                   'rendering_url': url, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'original_sha1': ii.get('sha1')}
            manifest.append(row)
            print('%-10s %-62s %-16s %s' % (era['id'], fn, lic[:16], row['sha256'][:12]))
    json.dump(manifest, open(os.path.join(outdir, 'manifest.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('%d candidate files kept' % len(manifest))


if __name__ == '__main__':
    main()
