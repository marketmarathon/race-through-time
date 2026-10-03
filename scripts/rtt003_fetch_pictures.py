"""RTT-003 (IQ-10): download the console pictures and maker logos from Wikimedia Commons.

Runs on a GitHub-hosted runner (.github/workflows/rtt003_assets.yml), because Commons answers
HTTP 429 to the Claude Code cloud container (commons.wikimedia.org and upload.wikimedia.org,
2 Oct 2026). Standard library only.

    python scripts/rtt003_fetch_pictures.py PICTURE_LIST.csv kits/rtt-003/pictures.json OUT_DIR

PICTURE_LIST.csv is the private reconciled list (race-through-time-private,
research/rtt-003-images/RTT-003_images_reconciled_2026-09-30.csv); pictures.json (this repo) says
which row each bar and maker key uses. For every entry: ask the Commons API for the file's current
URL and SHA-1, download it, and keep it only if its SHA-1 equals BOTH the list's commons_sha1 and
the API's. A PICK that cannot be downloaded or does not match falls back to the list's BACKUP row
for that console (flagged); a REJECT row is never used. Writes OUT_DIR/originals/<id>.<ext>,
OUT_DIR/logos/<maker>.svg and OUT_DIR/manifest.csv (file, source URL, licence, author, credit line,
SHA-1, SHA-256, ...). Prints only names, sizes and hashes. Exit 1 if anything is missing.
"""
import csv
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

UA = 'RaceThroughTime/1.0 (https://github.com/marketmarathon/race-through-time; one-off download of 33 files)'
API = 'https://commons.wikimedia.org/w/api.php'


def get(url, tries=6):
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


def info(title):
    q = urllib.parse.urlencode({'action': 'query', 'titles': 'File:' + title, 'prop': 'imageinfo',
                                'iiprop': 'url|sha1|size|mime', 'format': 'json', 'formatversion': '2'})
    page = json.loads(get(API + '?' + q))['query']['pages'][0]
    if 'imageinfo' not in page:
        raise RuntimeError('no imageinfo for ' + title)
    return page['imageinfo'][0]


def fetch(row, stem, out_dir):
    ii = info(row['file_title'])
    if ii['sha1'] != row['commons_sha1']:
        raise RuntimeError(f"{row['file_title']}: Commons API SHA-1 {ii['sha1']} != list {row['commons_sha1']}")
    data = get(ii['url'])
    sha1 = hashlib.sha1(data).hexdigest()
    if sha1 != row['commons_sha1']:
        raise RuntimeError(f"{row['file_title']}: downloaded SHA-1 {sha1} != list {row['commons_sha1']}")
    ext = os.path.splitext(row['file_title'])[1].lower()
    path = os.path.join(out_dir, stem + ext)
    with open(path, 'wb') as f:
        f.write(data)
    time.sleep(1.5)                                   # polite: one file at a time
    return path, ii, sha1, hashlib.sha256(data).hexdigest(), len(data)


def main(list_csv, map_json, out_dir):
    rows = list(csv.DictReader(open(list_csv, encoding='utf-8')))
    m = json.load(open(map_json, encoding='utf-8'))
    os.makedirs(os.path.join(out_dir, 'originals'), exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'logos'), exist_ok=True)
    jobs = [('console', k, v, 'originals') for k, v in m['consoles'].items()] + \
           [('logo', k, v, 'logos') for k, v in m['logos'].items()]
    manifest, failed = [], []
    for kind, key, ent, sub in jobs:
        pick = [r for r in rows if r['console'] == ent['csv_console'] and r['file_title'] == ent['file_title']]
        if len(pick) != 1 or not pick[0]['role'].startswith('PICK'):
            failed.append(f'{key}: PICK row not found in the list'); continue
        cands = pick + [r for r in rows if r['console'] == ent['csv_console'] and r['role'] == 'BACKUP']
        done = None
        for r in cands:
            if r['role'].startswith('REJECT'):
                continue
            try:
                done = (r,) + fetch(r, os.path.join(sub, key), out_dir)
                break
            except Exception as e:                    # noqa: BLE001 - report and try the backup
                print(f'{key}: {r["role"]} {r["file_title"]} not used: {e}')
        if not done:
            failed.append(f'{key}: no PICK or BACKUP could be downloaded'); continue
        r, path, ii, sha1, sha256, n = done
        print(f'{key}: {r["role"].split(" ")[0]} {r["file_title"]} {ii["width"]}x{ii["height"]} {n} bytes sha1 {sha1} sha256 {sha256}')
        manifest.append({'id': key, 'kind': kind, 'file': os.path.relpath(path, out_dir).replace(os.sep, '/'),
                         'role': r['role'], 'commons_title': r['file_title'], 'source_url': r['file_page_url'],
                         'download_url': ii['url'], 'licence': r['licence_verified'], 'author': r['author'],
                         'attribution_needed': r['attribution_needed'], 'credit_line': r['credit_line'],
                         'width': ii['width'], 'height': ii['height'], 'bytes': n, 'sha1': sha1, 'sha256': sha256,
                         'downloaded_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    with open(os.path.join(out_dir, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()) if manifest else ['id'])
        w.writeheader(); w.writerows(manifest)
    print(f'{len(manifest)} of {len(jobs)} files downloaded and SHA-1 checked')
    for x in failed:
        print('FAILED ' + x)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
