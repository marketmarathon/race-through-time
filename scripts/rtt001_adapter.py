"""RTT-001 adapter (IQ-13): data/rtt-001/ -> the player's input, schema "rtt-series/1" (share kind).

    python scripts/rtt001_adapter.py data/rtt-001 kits/rtt-001/race_rtt001.json --hash-file kits/rtt-001/dataset_hashes.txt

Reads (never writes) browsers.csv, series.csv, observations.csv and handover_order.csv. Nothing in
data/rtt-001 changes (DEC-167: smoothing is done by the player at draw time, never in series.csv).

One event per month end (31 Jan 1994 .. 30 Sep 2026, 393). Per browser and month end it carries the
share exactly as series.csv gives it, as a whole number of HUNDREDTHS of a percent (the data has at
most two decimals; the conversion is exact and checked), the display style ("estimated" before
January 2009, DEC-153; otherwise "official"), and the provenance letter (o observed, a arithmetic,
i interpolated). A browser with no value in a month has no entry (no bar). Per month: the on-screen
source line exactly as series.csv gives it, the source id and whether it is a hand-over month.

For the player's smoothing options (DEC-167) it also carries, before January 2009, every SOURCE POINT
each browser's line rests on (`knots`: the dated published figures named in series.csv left_point /
right_point, values from observations.csv), and the five hand-overs with the dates of the outgoing
source's last point and the incoming source's first point, flagged where DEC-168 found that the order
or the leader changes (handover_order.csv). These are inputs to drawing only.

Changes of first place come from the data (as built); each is marked `dated` when both browsers'
values that month are published figures (observed or arithmetic), which is the rule for a callout
(DEC-165 (7): no dated callout for Netscape passing Mosaic, which falls on a line with no figure).
Standard library only; deterministic (sorted keys, fixed separators).
"""
import argparse
import csv
import hashlib
import json
import os
from decimal import Decimal

ADAPTER = 'rtt001-adapter/1.0'
SC_START = '2009-01-31'
PROV = {'observed': 'o', 'arithmetic': 'a', 'interpolated': 'i'}
ERA_ORDER = ['GVU', 'EWS', 'STATMARKET', 'ONESTAT', 'W3COUNTER', 'STATCOUNTER']


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def hundredths(text):
    v = Decimal(text) * 100
    if v != v.to_integral_value() or v < 0 or v > 10000:
        raise SystemExit('share %r is not a whole number of hundredths in 0..100' % text)
    return int(v)


def num(text):
    t = text.strip().replace(',', '.')
    if t.count('.') > 1 or not t or not all(c.isdigit() or c == '.' for c in t):
        raise SystemExit('knot value %r is not a number' % text)
    return float(Decimal(t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data')
    ap.add_argument('out')
    ap.add_argument('--hash-file')
    a = ap.parse_args()
    files = {k: os.path.join(a.data, k + '.csv') for k in ('browsers', 'series', 'observations', 'handover_order')}
    browsers = rows(files['browsers'])
    series = rows(files['series'])
    obs = {o['obs_id']: o for o in rows(files['observations'])}
    order = rows(files['handover_order'])

    first = {}
    by_month = {}
    for r in series:
        m = by_month.setdefault(r['date'], {'values': {}, 'style': {}, 'prov': {}, 'lines': set(), 'sources': set(), 'handover': False})
        if not r['share']:
            continue
        bid = r['browser_id']
        m['values'][bid] = hundredths(r['share'])
        m['style'][bid] = 'estimated' if r['estimated'] == 'yes' else 'official'
        if (r['estimated'] == 'yes') != (r['date'] < SC_START):
            raise SystemExit('estimated flag does not follow January 2009 at %s %s' % (r['date'], bid))
        m['prov'][bid] = PROV[r['provenance']]
        m['lines'].add(r['source_line'])
        m['sources'].add(r['source_id'])
        m['handover'] = m['handover'] or r['handover'] == 'yes'
        first.setdefault(bid, r['date'])

    events = []
    for date in sorted(by_month):
        m = by_month[date]
        if len(m['lines']) != 1 or len(m['sources']) != 1:
            raise SystemExit('month %s has %d source lines' % (date, len(m['lines'])))
        events.append({'date': date, 'values': m['values'], 'style': m['style'], 'prov': m['prov'], 'plus': [], 'status': {},
                       'maker_totals': {}, 'maker_style': {}, 'maker_plus': [],
                       'source_line': next(iter(m['lines'])), 'source_id': next(iter(m['sources'])), 'handover': m['handover']})
    if len(events) != 393:
        raise SystemExit('expected 393 month ends, got %d' % len(events))

    # source points (knots) each pre-2009 line rests on
    knots = {}
    for r in series:
        if not r['share'] or r['date'] >= SC_START:
            continue
        for pid in (r['left_point'], r['right_point']):
            o = obs[pid]
            if o['used'] != 'yes' or o['verified'] != 'yes':
                raise SystemExit('series rests on %s, which is not a used, verified figure' % pid)
            if o['source_id'] == 'STATCOUNTER':
                continue
            k = knots.setdefault(r['browser_id'], {})
            k[o['date']] = {'date': o['date'], 'v': num(o['value_text']), 'src': o['source_id'], 'id': pid}
    knots = {b: [k[d] for d in sorted(k)] for b, k in sorted(knots.items())}

    # hand-overs: outgoing source's last point date and incoming source's first point date
    handovers = []
    for r in order:
        if r['kind'] != 'hand-over':
            continue
        frm, to = r['sources'].split('>')
        handovers.append({'from': frm, 'to': to, 't_o': r['from'], 't_i': r['to'], 'days': int(r['days']),
                          'flagged': r['flag'].startswith('FLAG'), 'flag': r['flag']})
    if [h['from'] for h in handovers] != ERA_ORDER[:-1]:
        raise SystemExit('hand-overs are not the five expected: %s' % [h['from'] for h in handovers])

    # changes of first place as built (rank: share, ties keep the previous month's order, then alphabetical)
    crown, prev, prev_order = [], None, []
    names = {b['browser_id']: b['display_name'] for b in browsers}
    for ev in events:
        pos = {bid: i for i, bid in enumerate(prev_order)}
        ids = sorted(ev['values'], key=lambda b: (-ev['values'][b], pos.get(b, 1e9), names[b]))
        lead = ids[0]
        if lead != prev:
            dated = prev is not None and ev['prov'][lead] in 'oa' and ev['prov'].get(prev, 'i') in 'oa'
            crown.append({'date': ev['date'], 'id': lead, 'previous': prev, 'style': ev['style'][lead], 'dated': dated})
        prev, prev_order = lead, ids

    entrants = [{'id': b['browser_id'], 'label': b['display_name'], 'maker': b['browser_id'], 'maker_name': b['maker'],
                 'launch_date': first[b['browser_id']], 'fade_date': None}
                for b in browsers if b['browser_id'] in first]
    out = {'schema': 'rtt-series/1', 'kind': 'share', 'adapter': ADAPTER, 'dataset_id': 'RTT-001', 'unit': 'hundredths of a percent',
           'sc_start': SC_START, 'entrants': entrants, 'makers': [{'key': e['id'], 'label': e['label']} for e in entrants],
           'events': events, 'knots': knots, 'handovers': handovers, 'crown': crown}
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        f.write('\n')
    if a.hash_file:
        with open(a.hash_file, 'w', encoding='utf-8') as f:
            f.write('# SHA-256 of the adapter inputs and output (%s)\n' % ADAPTER)
            for k in sorted(files):
                f.write('%s input %s\n' % (sha256(files[k]), os.path.relpath(files[k]).replace(os.sep, '/')))
            f.write('%s output %s\n' % (sha256(a.out), os.path.relpath(a.out).replace(os.sep, '/')))
    print('%s: %d month ends, %d browsers, %d with knots, %d hand-overs (%d flagged), %d changes of first place (%d dated)' % (
        a.out, len(events), len(entrants), len(knots), len(handovers), sum(h['flagged'] for h in handovers), len(crown), sum(c['dated'] for c in crown)))


if __name__ == '__main__':
    main()
