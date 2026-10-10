"""RTT-102 (IQ-19): look up and download the assistant logos listed in kits/rtt-102/logos.json from Wikimedia.

Runs on a GitHub-hosted runner (.github/workflows/rtt102_assets.yml): Wikimedia answers HTTP 429 to the Claude Code
cloud container (as for RTT-001 and RTT-103). Standard library only. Adapted from scripts/rtt103_fetch_logos.py (that
file is RTT-103's and is not changed).

    python3 scripts/rtt102_fetch_logos.py kits/rtt-102/logos.json OUT_DIR

For every entry, candidate files are gathered in this order: each `candidates` title (Commons, or the entry's `site`),
then Commons search hits for `search` (namespace File, titles containing "logo" or "icon", .svg or .png), then the
images on `page` of `page_site` (e.g. the assistant's English Wikipedia article; titles containing "logo" or "icon"),
skipping titles that contain any of `exclude`. The first `keep` (default 3) candidates that exist are downloaded: the
first as OUT_DIR/<id>.<ext> (the one the render uses unless the config names another), the others as
OUT_DIR/alt/<id>__<n>.<ext> so the choice can be checked by eye before the config names a file. The API gives each
file's URL, SHA-1, licence, author and restrictions; a file is kept only if its downloaded SHA-1 equals the API's.
Run 2: an entry with `site` en.wikipedia.org looks its candidates up there first (a local file), then on Commons.
Writes OUT_DIR/manifest.csv (every kept file). Prints only titles, names, sizes, licences and hashes. Exit 1 if a
required entry has no file (entries with "optional": true may have none).
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

UA = 'RaceThroughTime/1.0 (https://github.com/marketmarathon/race-through-time; one-off download of about 30 logo files)'


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


def api(site, **p):
    p.update(format='json', formatversion='2')
    time.sleep(2)
    return json.loads(get('https://%s/w/api.php?%s' % (site, urllib.parse.urlencode(p))))


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s or ''))).strip()


def info(site, title):
    pg = api(site, action='query', titles=title, prop='imageinfo', iiprop='url|sha1|size|extmetadata')['query']['pages'][0]
    return pg['imageinfo'][0] if pg.get('imageinfo') else None


def main():
    spec, out = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(out, 'alt'), exist_ok=True)
    rows, bad = [], []
    for L in json.load(open(spec, encoding='utf-8'))['logos']:
        bad_t = lambda t: any(x.lower() in t.lower() for x in L.get('exclude', []))
        ok_t = lambda t: ('logo' in t.lower() or 'icon' in t.lower()) and t.lower().endswith(('.svg', '.png')) and not bad_t(t)
        cands = [(L.get('site', 'commons.wikimedia.org'), t) for t in L.get('candidates', []) if not bad_t(t)]
        if L.get('search'):
            hits = [h['title'] for h in api('commons.wikimedia.org', action='query', list='search', srsearch=L['search'],
                                            srnamespace=6, srlimit=15)['query']['search']]
            print('%s: search "%s" -> %s' % (L['id'], L['search'], ' | '.join(hits)))
            cands += [('commons.wikimedia.org', t) for t in hits if ok_t(t)]
        if L.get('page'):
            ps = L.get('page_site', 'en.wikipedia.org')
            pg = api(ps, action='query', titles=L['page'], prop='pageimages|images', piprop='name', imlimit=100)['query']['pages'][0]
            imgs = [i['title'] for i in pg.get('images', [])]
            print('%s: page %s on %s: images %s' % (L['id'], L['page'], ps, ' | '.join(imgs)))
            cands += [(ps, t) for t in imgs if ok_t(t)]
        seen, kept = set(), 0
        for site, t in cands:
            if (t in seen) or kept >= L.get('keep', 3):
                continue
            seen.add(t)
            ii = info(site, t)
            if not ii and site != 'commons.wikimedia.org':
                ii, site = info('commons.wikimedia.org', t), 'commons.wikimedia.org'   # a wiki page may show a Commons file
            if not ii:
                print('%s: no file %s on %s' % (L['id'], t, site))
                continue
            time.sleep(4)
            b = get(ii['url'])
            s1 = hashlib.sha1(b).hexdigest()
            if s1 != ii['sha1']:
                print('%s: %s downloaded SHA-1 %s, API %s - not kept' % (L['id'], t, s1, ii['sha1']))
                continue
            ext = t.rsplit('.', 1)[1].lower()
            name = '%s.%s' % (L['id'], ext) if kept == 0 else 'alt/%s__%d.%s' % (L['id'], kept, ext)
            with open(os.path.join(out, name), 'wb') as f:
                f.write(b)
            m = ii.get('extmetadata', {})
            rows.append({'id': L['id'], 'rank': kept, 'file': name, 'title': t, 'site': site,
                         'page': 'https://%s/wiki/%s' % (site, urllib.parse.quote(t.replace(' ', '_'))),
                         'licence': plain(m.get('LicenseShortName', {}).get('value')),
                         'author': plain(m.get('Artist', {}).get('value'))[:200],
                         'restrictions': plain(m.get('Restrictions', {}).get('value')),
                         'nonfree': plain(m.get('NonFree', {}).get('value')),
                         'sha1': s1, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b),
                         'width': ii.get('width'), 'height': ii.get('height')})
            print('%s  %s  %d bytes  %s (%s)  licence: %s' % (rows[-1]['sha256'], name, len(b), t, site, rows[-1]['licence']))
            kept += 1
        if not kept:
            (print if L.get('optional') else bad.append)('%s: no file found' % L['id'])
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
