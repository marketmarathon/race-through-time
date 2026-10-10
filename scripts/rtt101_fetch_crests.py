"""RTT-101 (IQ-21, design round 1): look up and download every Premier League club's crest from Wikipedia.

Owner decision DEC-700 (Luke, 10 Oct 2026): each club's crest on a tile beside its bar, purely to identify the club,
as RTT-001's browser logos (house style section 7). Runs on a GitHub-hosted runner
(.github/workflows/rtt101_assets.yml): Wikimedia answers HTTP 429 to the Claude Code cloud container (10 Oct 2026, as
for RTT-001 and RTT-103). Standard library only.

    python scripts/rtt101_fetch_crests.py data/rtt-101/clubs.csv OUT_DIR

For every club in clubs.csv (all 51, by `wikipedia_title`; Wimbledon F.C. is the old club's own article, never AFC
Wimbledon's or MK Dons'):
  - the article's lead image on English Wikipedia (pageimages) is taken as the club's crest today. The API says where
    the file lives: on Wikimedia Commons ("shared": a free licence, Commons first) or on English Wikipedia itself
    ("local": almost always a non-free logo used under the article's fair-use rationale). It is kept only if its title
    looks like a crest (crest, badge, logo, emblem, coat, shield, FC, AFC; never a photograph);
  - every other image on the article and on "History of <club>" whose title contains crest, badge, logo, emblem or
    coat of arms is downloaded as a CANDIDATE older crest (for the "crest in use at each date" option), never drawn
    until chosen by name in kits/rtt-101/crests.json.
The API gives each file's URL, SHA-1, size, licence, non-free flag, description and date; a file is kept only if the
downloaded SHA-1 equals the API's. Writes OUT_DIR/<club_id>.<ext> (today's crest), OUT_DIR/candidates/<club_id>/...,
and OUT_DIR/manifest.csv (one row per file: role lead|candidate). Prints only titles, sizes, licences and hashes.
Exit 1 if a club has no crest at all (it is listed; the design falls back to our own neutral tile for it).
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

UA = ('RaceThroughTime/1.0 (https://github.com/marketmarathon/race-through-time; one-off download of about 50 '
      'football club crests for identification on a chart; contact via the repository)')
SITE = 'en.wikipedia.org'
CREST = re.compile(r'crest|badge|logo|emblem|coat[ _]of[ _]arms|shield|\bf\.?c\b|a\.?f\.?c|club', re.I)
CANDIDATE = re.compile(r'crest|badge|logo|emblem|coat[ _]of[ _]arms', re.I)
NOT_CREST = re.compile(r'premier[ _]league|kit[ _]|_kit|kit\.|flag[ _]of|commons-logo|wiktionary|wikiquote|wikinews|'
                       r'soccerball|football[ _]pictogram|edit-clear|question[ _]book|ambox|symbol[ _]|icon|'
                       r'stadium|ground|photo|\.jpe?g$|uefa|fifa|efl[ _]|football[ _]league|the[ _]fa[ _]|'
                       r'nike|adidas|umbro|puma|sponsor|cup[ _]|trophy|map|location', re.I)


def get(url, tries=8):
    wait = 5
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                ra = e.headers.get('Retry-After')
                time.sleep(int(ra) if ra and ra.isdigit() else wait)
                wait = min(wait * 2, 120)
                continue
            raise
        except urllib.error.URLError:
            if i < tries - 1:
                time.sleep(wait); wait = min(wait * 2, 120); continue
            raise


def api(**p):
    p.update(format='json', formatversion='2')
    time.sleep(1.5)
    return json.loads(get('https://%s/w/api.php?' % SITE + urllib.parse.urlencode(p)))


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s or ''))).strip()


def page_images(title):
    q = api(action='query', titles=title, prop='pageimages|images', piprop='name', imlimit='max', redirects=1)['query']
    pg = q['pages'][0]
    if pg.get('missing'):
        return None, []
    lead = ('File:' + pg['pageimage'].replace('_', ' ')) if pg.get('pageimage') else None
    return lead, [i['title'] for i in pg.get('images', [])]


def info(title):
    pg = api(action='query', titles=title, prop='imageinfo', iiprop='url|sha1|size|mime|extmetadata')['query']['pages'][0]
    if not pg.get('imageinfo'):
        return None
    ii = pg['imageinfo'][0]
    ii['repository'] = pg.get('imagerepository', '')
    return ii


def save(ii, title, path):
    time.sleep(2)
    b = get(ii['url'])
    s1 = hashlib.sha1(b).hexdigest()
    if s1 != ii['sha1']:
        return None, 'downloaded SHA-1 %s, API %s' % (s1, ii['sha1'])
    with open(path, 'wb') as f:
        f.write(b)
    m = ii.get('extmetadata', {})
    shared = ii['repository'] == 'shared'
    host = 'commons.wikimedia.org' if shared else SITE
    return {'title': title, 'host': host,
            'page': 'https://%s/wiki/' % host + urllib.parse.quote(title.replace(' ', '_')),
            'repository': ii['repository'], 'licence': plain(m.get('LicenseShortName', {}).get('value')),
            'nonfree': plain(m.get('NonFree', {}).get('value')) or ('' if shared else 'local file'),
            'author': plain(m.get('Artist', {}).get('value'))[:160],
            'date': plain(m.get('DateTimeOriginal', {}).get('value') or m.get('DateTime', {}).get('value'))[:60],
            'description': plain(m.get('ImageDescription', {}).get('value'))[:300],
            'mime': ii.get('mime', ''), 'sha1': s1, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b),
            'width': ii.get('width'), 'height': ii.get('height')}, None


def main():
    clubs_csv, out = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(out, 'candidates'), exist_ok=True)
    rows, missing, bad = [], [], []
    for c in csv.DictReader(open(clubs_csv, encoding='utf-8')):
        cid, title = c['club_id'], c['wikipedia_title']
        lead, imgs = page_images(title)
        hist_lead, hist = page_images('History of ' + title)
        print('%s: article %s: lead image %s; %d images; "History of" article: %s' % (cid, title, lead, len(imgs), 'yes (%d images)' % len(hist) if hist or hist_lead else 'none'))
        got_lead = False
        if lead and CREST.search(lead) and not NOT_CREST.search(lead):
            ii = info(lead)
            if ii:
                ext = lead.rsplit('.', 1)[1].lower()
                r, err = save(ii, lead, os.path.join(out, '%s.%s' % (cid, ext)))
                if err:
                    bad.append('%s: %s' % (cid, err))
                else:
                    r.update(club_id=cid, role='lead', file='%s.%s' % (cid, ext), found_on=title)
                    rows.append(r); got_lead = True
                    print('%s  %s  %d bytes  %s  repository %s  licence: %s' % (r['sha256'], r['file'], r['bytes'], lead, r['repository'], r['licence']))
        if not got_lead:
            missing.append(cid)
            print('%s: no crest as the lead image (%s)' % (cid, lead))
        seen = {lead}
        n = 0
        for src, lst in ((title, imgs), ('History of ' + title, ([hist_lead] if hist_lead else []) + hist)):
            for t in lst:
                if not t or t in seen or not CANDIDATE.search(t) or NOT_CREST.search(t):
                    continue
                seen.add(t)
                ii = info(t)
                if not ii:
                    continue
                n += 1
                d = os.path.join(out, 'candidates', cid); os.makedirs(d, exist_ok=True)
                slug = re.sub(r'[^A-Za-z0-9]+', '_', t[5:].rsplit('.', 1)[0]).strip('_')[:60]
                name = '%02d_%s.%s' % (n, slug, t.rsplit('.', 1)[1].lower())
                r, err = save(ii, t, os.path.join(d, name))
                if err:
                    print('%s: candidate %s: %s' % (cid, t, err)); continue
                r.update(club_id=cid, role='candidate', file='candidates/%s/%s' % (cid, name), found_on=src)
                rows.append(r)
                print('%s  %s  %d bytes  %s  repository %s  licence: %s' % (r['sha256'], r['file'], r['bytes'], t, r['repository'], r['licence']))
    cols = ['club_id', 'role', 'file', 'title', 'host', 'page', 'found_on', 'repository', 'licence', 'nonfree', 'author',
            'date', 'description', 'mime', 'sha1', 'sha256', 'bytes', 'width', 'height']
    with open(os.path.join(out, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in cols})
    print('%d files; %d clubs without a crest as the lead image: %s' % (len(rows), len(missing), ', '.join(missing) or 'none'))
    for m in bad:
        print('::error::' + m)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
