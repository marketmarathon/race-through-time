"""RTT-103 (IQ-18): look up and download the company logos listed in kits/rtt-103/logos.json from Wikimedia Commons.

Runs on a GitHub-hosted runner (.github/workflows/rtt103_assets.yml): Wikimedia answers HTTP 429 to the Claude Code
cloud container (8 Oct 2026, as for RTT-001). Standard library only.

    python scripts/rtt103_fetch_logos.py kits/rtt-103/logos.json OUT_DIR

For every entry: the first `candidates` title that exists on Commons, else the first search hit (namespace File)
whose title contains "logo". IQ-18b: an entry may name another wiki (`site`, e.g. en.wikipedia.org for its local
non-free files) and a `page` whose images are searched after the candidates (only titles containing "logo"), skipping titles that contain any of `exclude` (e.g. "Cloud": never the Baidu Cloud product logo). The API gives the file's URL, SHA-1, licence, author and restrictions; the file is kept
only if the downloaded SHA-1 equals the API's. Writes OUT_DIR/<id>.<ext> and OUT_DIR/manifest.csv (id, file, page,
title, licence, author, restrictions, sha1, sha256, bytes, width, height). Prints only titles, names, sizes and
hashes. Exit 1 if a required entry is missing or differs (entries with "optional": true may be missing).
"""
import csv
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

UA = 'RaceThroughTime/1.0 (https://github.com/marketmarathon/race-through-time; one-off download of about 10 company logos)'
API = 'https://commons.wikimedia.org/w/api.php'


def get(url, tries=7):
    wait = 5
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                ra = e.headers.get('Retry-After')
                time.sleep(int(ra) if ra and ra.isdigit() else wait)
                wait *= 2
                continue
            raise


def api(site=None, **p):
    p.update(format='json', formatversion='2')
    time.sleep(2)
    return json.loads(get(('https://%s/w/api.php' % site if site else API) + '?' + urllib.parse.urlencode(p)))


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s or ''))).strip()


def main():
    spec, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rows, bad = [], []
    for L in json.load(open(spec, encoding='utf-8'))['logos']:
        info, site = None, L.get('site')
        bad_t = lambda t: any(x.lower() in t.lower() for x in L.get('exclude', []))
        cands = list(L.get('candidates', []))
        if L.get('page'):                                   # IQ-18b: the images on a wiki page (lead image first)
            pg = api(site, action='query', titles=L['page'], prop='pageimages|images', piprop='name', imlimit=100)['query']['pages'][0]
            imgs = [i['title'] for i in pg.get('images', [])]
            lead = ('File:' + pg['pageimage'].replace('_', ' ')) if pg.get('pageimage') else None
            print('%s: page %s on %s: lead image %s; images %s' % (L['id'], L['page'], site, lead, ' | '.join(imgs)))
            cands += [t for t in [lead] + imgs if t and 'logo' in t.lower()]   # IQ-18b run 3: logo titles only (run 2 took a lead photo)
        cands = [t for t in cands if not bad_t(t)]
        for t in cands:
            pg = api(site, action='query', titles=t, prop='imageinfo', iiprop='url|sha1|size|extmetadata')['query']['pages'][0]
            if pg.get('imageinfo'):
                info = (t, pg['imageinfo'][0]); break
            print('%s: no file %s' % (L['id'], t))
        if not info and L.get('search') and not site:
            hits = [h['title'] for h in api(action='query', list='search', srsearch=L['search'], srnamespace=6, srlimit=10)['query']['search']]
            print('%s: search "%s" -> %s' % (L['id'], L['search'], ' | '.join(hits)))
            for t in hits:
                if 'logo' in t.lower() and t.lower().endswith(('.svg', '.png')) and not bad_t(t):
                    pg = api(action='query', titles=t, prop='imageinfo', iiprop='url|sha1|size|extmetadata')['query']['pages'][0]
                    if pg.get('imageinfo'):
                        info = (t, pg['imageinfo'][0]); break
        if not info:
            (print if L.get('optional') else bad.append)('%s: no file found' % L['id']); continue
        title, ii = info
        time.sleep(4)
        b = get(ii['url'])
        s1 = hashlib.sha1(b).hexdigest()
        if s1 != ii['sha1']:
            bad.append('%s: downloaded SHA-1 %s, API %s' % (L['id'], s1, ii['sha1'])); continue
        ext = title.rsplit('.', 1)[1].lower()
        name = L['id'] + '.' + ext
        with open(os.path.join(out, name), 'wb') as f:
            f.write(b)
        m = ii.get('extmetadata', {})
        rows.append({'id': L['id'], 'file': name, 'title': title,
                     'page': 'https://%s/wiki/' % (site or 'commons.wikimedia.org') + urllib.parse.quote(title.replace(' ', '_')),
                     'licence': plain(m.get('LicenseShortName', {}).get('value')),
                     'author': plain(m.get('Artist', {}).get('value'))[:200],
                     'restrictions': plain(m.get('Restrictions', {}).get('value')), 'site': site or 'commons.wikimedia.org',
                     'nonfree': plain(m.get('NonFree', {}).get('value')),
                     'sha1': s1, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b),
                     'width': ii.get('width'), 'height': ii.get('height')})
        print('%s  %s  %d bytes  %s  licence: %s' % (rows[-1]['sha256'], name, len(b), title, rows[-1]['licence']))
    with open(os.path.join(out, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['id'], lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)
    for m in bad:
        print('::error::' + m)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
