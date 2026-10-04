"""RTT-001 (IQ-13b): download the browser logos listed in kits/rtt-001/logos.json from Wikimedia Commons.

Runs on a GitHub-hosted runner (.github/workflows/rtt001_assets.yml), because upload.wikimedia.org answers
HTTP 429 to the Claude Code cloud container (4 Oct 2026). Standard library only.

    python scripts/rtt001_fetch_logos.py kits/rtt-001/logos.json OUT_DIR

For every entry: ask the file's wiki (Commons, or English Wikipedia for its local non-free files; IQ-13c) for the
file's current URL and SHA-1, download it, and keep it only if its SHA-1 equals BOTH logos.json's sha1 (read at the
file page when the logo was chosen) and the API's. An entry with a direct `url` (a maker's own file, e.g. Apple's
Safari icon) is kept only if its SHA-256 equals logos.json's sha256_local. Entries with `same_as` are skipped.
Writes OUT_DIR/<browser_id>.<ext> and OUT_DIR/manifest.csv (browser, file, Commons page, licence, author,
SHA-1, SHA-256, bytes). Prints only names, sizes and hashes. Exit 1 if anything is missing or differs.
"""
import csv
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = 'RaceThroughTime/1.0 (https://github.com/marketmarathon/race-through-time; one-off download of about 30 browser logos)'
API = 'https://commons.wikimedia.org/w/api.php'


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


def main():
    spec, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    logos = json.load(open(spec, encoding='utf-8'))['logos']
    rows, bad = [], []
    logos = [L for L in logos if not L.get('same_as')]       # IQ-13c: a browser that reuses another's file
    for L in logos:
        if L.get('url'):                                      # IQ-13c: a maker's own file (no wiki): SHA-256 as recorded
            time.sleep(2)
            b = get(L['url'])
            if hashlib.sha256(b).hexdigest() != L['sha256_local']:
                bad.append('%s: downloaded SHA-256 %s, expected %s' % (L['browser_id'], hashlib.sha256(b).hexdigest(), L['sha256_local'])); continue
            s1 = hashlib.sha1(b).hexdigest()
        else:
            api = 'https://%s/w/api.php' % L.get('site', 'commons.wikimedia.org')   # IQ-13c: also Wikipedia-local (non-free) files
            q = urllib.parse.urlencode({'action': 'query', 'titles': L['commons_title'], 'prop': 'imageinfo',
                                        'iiprop': 'url|sha1', 'format': 'json', 'formatversion': '2'})
            page = json.loads(get(api + '?' + q))['query']['pages'][0]
            ii = page.get('imageinfo', [{}])[0]
            if ii.get('sha1') != L['sha1']:
                bad.append('%s: file page SHA-1 %s, logos.json %s' % (L['browser_id'], ii.get('sha1'), L['sha1'])); continue
            time.sleep(4)
            b = get(ii['url'])
            s1 = hashlib.sha1(b).hexdigest()
            if s1 != L['sha1']:
                bad.append('%s: downloaded SHA-1 %s, expected %s' % (L['browser_id'], s1, L['sha1'])); continue
        name = L['browser_id'] + '.' + L['ext']
        with open(os.path.join(out, name), 'wb') as f:
            f.write(b)
        s256 = hashlib.sha256(b).hexdigest()
        rows.append({'browser_id': L['browser_id'], 'file': name, 'page': L['page'], 'status': L.get('status', ''), 'licence': L['licence'],
                     'author': L['author'], 'sha1': s1, 'sha256': s256, 'bytes': len(b)})
        print('%s  %s  %d bytes  sha1 %s' % (s256, name, len(b), s1))
    with open(os.path.join(out, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['browser_id'], lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)
    for m in bad:
        print('::error::' + m)
    sys.exit(1 if bad or len(rows) != len(logos) else 0)


if __name__ == '__main__':
    main()
