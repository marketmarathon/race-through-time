"""RTT-101 adapter (IQ-21, design round 1): data/rtt-101/ -> the player's input, schema "rtt-series/1", kind "net".

    python3 scripts/rtt101_adapter.py data/rtt-101 kits/rtt-101/race_rtt101.json --hash-file kits/rtt-101/dataset_hashes.txt

Reads (never writes) the data built by the IQ-15 sessions (pull request #19): series_onscreen.csv (VERIFIED fees only,
contract v1.5 section 8, DEC-448; never the all-fees preview series_monthly.csv), clubs.csv, pl_membership.csv and
seasons.csv, after checking each one's SHA-256 against data/rtt-101/manifest.json. No figure is changed, rounded or added.

Race: one event per month end from July 1992 (DEC-260: the first month end with a fee; the film's first board) to
31 August 2026, plus the freeze point, 1 September 2026 23:00 BST (DEC-250 (b)): 411 events. A club has a bar from its
first Premier League season (series rank no longer blank) and keeps it to the end (DEC-259: out of the PL, its bar is
frozen and keeps its rank).

Per event and club:
  values   cum_net_gbp in whole PENCE (the series has two decimals; pence keep every figure exact); may be negative;
  order    the series' own rank (descending cumulative net; ties: the club that reached the value first);
  status   "out" while the club is not in the PL (in_pl = no), with `rel` = the year its last PL season ended
           ("relegated 2009"), for the frozen-bar look;
  avg      avg_real_net_per_season_gbp2026 in whole pence (the secondary statistic, 2026 pounds) and `seasons` =
           pl_seasons_played;
  combined the sum of every club's cumulative net that month (pence): all PL clubs' net spend with clubs outside the PL
           (PL-to-PL deals net to zero; contract section 10), frozen bars included.
Standard library only; deterministic (sorted keys, fixed separators).
"""
import argparse
import csv
import hashlib
import json
import os
from decimal import Decimal

ADAPTER = 'rtt101-adapter/1.0'
INPUTS = ['series_onscreen.csv', 'clubs.csv', 'pl_membership.csv', 'seasons.csv']
FIRST = '1992-07-31'          # DEC-260
FREEZE = '2026-09-01'


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def pence(s):
    p = Decimal(s) * 100
    if p != p.to_integral_value():
        raise SystemExit('not a whole number of pence: ' + s)
    return int(p)


def build(d):
    files = json.load(open(os.path.join(d, 'manifest.json'), encoding='utf-8'))['files']
    for name in INPUTS:
        if files.get(name) != sha(os.path.join(d, name)):
            raise SystemExit('%s: SHA-256 does not match data/rtt-101/manifest.json' % name)
    clubs = rows(os.path.join(d, 'clubs.csv'))
    label = {c['club_id']: c['display_name'] for c in clubs}
    member = {}
    for r in rows(os.path.join(d, 'pl_membership.csv')):
        member.setdefault(r['club_id'], set()).add(r['season'])
    wins = [(r['attribution_start'], r['season']) for r in rows(os.path.join(d, 'seasons.csv'))]
    season_of = lambda dt: max(s for a, s in wins if a <= dt)       # the season whose attribution window has begun
    by = {}
    for r in rows(os.path.join(d, 'series_onscreen.csv')):
        if r['month_end'] < FIRST or not r['rank']:
            continue
        if r['club_id'] not in label:
            raise SystemExit('unknown club ' + r['club_id'])
        by.setdefault(r['month_end'], []).append(r)
    dates = sorted(by)
    if dates[0] != FIRST or dates[-1] != FREEZE:
        raise SystemExit('series runs %s .. %s, expected %s .. %s' % (dates[0], dates[-1], FIRST, FREEZE))
    events, first = [], {}
    seen = set()
    for dt in dates:
        rs = sorted(by[dt], key=lambda r: int(r['rank']))
        if [int(r['rank']) for r in rs] != list(range(1, len(rs) + 1)):
            raise SystemExit(dt + ': ranks are not 1..n')
        if not seen <= {r['club_id'] for r in rs}:
            raise SystemExit(dt + ': a club lost its bar (DEC-259 keeps it)')
        ev = {'date': dt, 'values': {}, 'order': [], 'status': {}, 'rel': {}, 'avg': {}, 'seasons': {}, 'style': {},
              'prov': {}, 'plus': [], 'combined': 0}
        if dt == FREEZE:
            ev['freeze'] = True
        for r in rs:
            c = r['club_id']
            seen.add(c); first.setdefault(c, dt)
            v = pence(r['cum_net_gbp'])
            ev['values'][c] = v
            ev['order'].append(c)
            ev['style'][c] = 'official'
            ev['prov'][c] = 'p'
            ev['combined'] += v
            ev['avg'][c] = pence(r['avg_real_net_per_season_gbp2026'])
            ev['seasons'][c] = int(r['pl_seasons_played'])
            if r['in_pl'] == 'no':
                past = sorted(s for s in member[c] if s < season_of(dt))
                if not past:
                    raise SystemExit('%s %s: out of the PL with no PL season before' % (dt, c))
                ev['status'][c] = 'out'
                ev['rel'][c] = int(past[-1][:4]) + 1
            elif r['in_pl'] != 'yes':
                raise SystemExit('%s %s: in_pl %s' % (dt, c, r['in_pl']))
        events.append(ev)
    entrants = [{'id': c['club_id'], 'label': c['display_name'], 'maker': c['club_id'],
                 'launch_date': first.get(c['club_id'], FREEZE), 'first_pl_season': c['first_pl_season']}
                for c in clubs]
    makers = [{'key': c['club_id'], 'label': c['display_name']} for c in clubs]
    return {'schema': 'rtt-series/1', 'kind': 'net', 'adapter': ADAPTER,
            'measure': 'cumulative net spend on reported transfer fees, VERIFIED fees only (series_onscreen.csv)',
            'unit': 'pence', 'freeze': FREEZE, 'entrants': entrants, 'makers': makers, 'events': events}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data_dir')
    ap.add_argument('out')
    ap.add_argument('--hash-file')
    a = ap.parse_args()
    race = build(a.data_dir)
    with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(race, f, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        f.write('\n')
    if a.hash_file:
        lines = ['# SHA-256 of the adapter inputs and output (%s)' % ADAPTER]
        for name in INPUTS + ['manifest.json']:
            p = os.path.join(a.data_dir, name)
            lines.append('%s input %s' % (sha(p), os.path.relpath(p)))
        lines.append('%s output %s' % (sha(a.out), os.path.relpath(a.out)))
        with open(a.hash_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')
    ev = race['events']
    print('%s: %d events (%s .. %s), %d clubs with a bar at the freeze, %d bar-months out of the PL (frozen)' % (
        a.out, len(ev), ev[0]['date'], ev[-1]['date'], len(ev[-1]['values']), sum(len(e['status']) for e in ev)))


if __name__ == '__main__':
    main()
