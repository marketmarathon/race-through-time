"""RTT-003 adapter (IQ-10): data/rtt-003/ -> the player's input, schema "rtt-series/1".

    python scripts/rtt003_adapter.py data/rtt-003 kits/rtt-003/race_rtt003.json --hash-file kits/rtt-003/dataset_hashes.txt

Reads (never writes) consoles.csv, series.csv, series_by_maker.csv and crown.csv. One event per
quarter end (31 Mar 1985 .. 30 Jun 2026). Every number is copied from the data as an integer number
of units; nothing is interpolated, rounded or invented here. Per console and quarter end it carries
the units, the display style (official / estimated / analyst_estimate, the DEC-090 rule, decided in
the data build) and the lower-bound flag ("+"). Per maker it carries the total from
series_by_maker.csv, a "+" if any of that maker's consoles carries one, and a style: the least
certain style among that maker's consoles at that quarter end (analyst_estimate > estimated >
official), so a company total that contains an analyst estimate is labelled as one (DEC-084).
Standard library only; deterministic (sorted keys, fixed separators).
"""
import argparse
import csv
import hashlib
import json
import os

ADAPTER = 'rtt003-adapter/1.0'
RANK = {'official': 0, 'estimated': 1, 'analyst_estimate': 2}


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data'); ap.add_argument('out'); ap.add_argument('--hash-file')
    a = ap.parse_args()
    files = {k: os.path.join(a.data, k + '.csv') for k in ('consoles', 'series', 'series_by_maker', 'crown')}
    cons = [r for r in rows(files['consoles']) if r['in_scope'] == 'yes']
    maker_of = {r['console_id']: r['maker_key'] for r in cons}
    makers, seen = [], set()
    for r in sorted(cons, key=lambda r: (r['launch_date'], r['console_id'])):
        if r['maker_key'] not in seen:
            seen.add(r['maker_key']); makers.append({'key': r['maker_key'], 'label': r['maker'], 'first_launch': r['launch_date']})
    entrants = [{'id': r['console_id'], 'label': r['display_name'], 'maker': r['maker_key'], 'type': r['type'],
                 'launch_date': r['launch_date'], 'fade_date': r['fade_date'] or None, 'fade_basis': r['fade_basis']}
                for r in cons]

    ev = {}
    for r in rows(files['series']):
        if r['console_id'] not in maker_of:
            raise SystemExit('series.csv has a console that is not in scope: ' + r['console_id'])
        e = ev.setdefault(r['quarter_end'], {'date': r['quarter_end'], 'values': {}, 'style': {}, 'plus': []})
        u = int(r['units'])
        if str(u) != r['units'] or u < 0:
            raise SystemExit('not a whole number of units: ' + r['quarter_end'] + ' ' + r['console_id'])
        e['values'][r['console_id']] = u
        e['style'][r['console_id']] = r['display_style']
        if r['display_style'] not in RANK:
            raise SystemExit('unknown display_style ' + r['display_style'])
        if r['plus_flag'] == 'yes':
            e['plus'].append(r['console_id'])
        elif r['plus_flag'] != 'no':
            raise SystemExit('plus_flag must be yes or no')
    for r in rows(files['series_by_maker']):
        e = ev[r['quarter_end']]
        e.setdefault('maker_totals', {})[r['maker_key']] = int(r['units'])
    events = []
    for d in sorted(ev):
        e = ev[d]
        e['plus'].sort()
        ms, mp = {}, []
        for m in sorted(e['maker_totals']):
            ids = [i for i in e['values'] if maker_of[i] == m]
            if sum(e['values'][i] for i in ids) != e['maker_totals'][m]:
                raise SystemExit(f'{d} {m}: series_by_maker.csv total does not equal the sum of series.csv')
            ms[m] = max((e['style'][i] for i in ids), key=lambda s: RANK[s])
            if any(i in e['plus'] for i in ids):
                mp.append(m)
        e['maker_style'] = ms; e['maker_plus'] = mp
        events.append(e)
    crown = [{'date': r['quarter_end'], 'id': r['new_leader'], 'previous': r['previous_leader'] or None,
              'style': r['display_style']} for r in rows(files['crown'])]
    out = {'schema': 'rtt-series/1', 'adapter': ADAPTER, 'dataset_id': 'RTT-003', 'unit': 'units',
           'entrants': entrants, 'makers': makers, 'events': events, 'crown': crown}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        f.write('\n')
    print(f'{len(entrants)} consoles, {len(makers)} makers, {len(events)} quarter ends, {len(crown)} crown rows -> {a.out}')
    if a.hash_file:
        lines = ['# RTT-003 player input - SHA-256 record (written by scripts/rtt003_adapter.py; do not edit)',
                 '# adapter: ' + ADAPTER, '# schema: rtt-series/1', '# dataset_id: RTT-003']
        for k in ('consoles', 'series', 'series_by_maker', 'crown'):
            lines.append(f'{sha256(files[k])}  input  {files[k].replace(os.sep, "/")}')
        lines.append(f'{sha256(a.out)}  output {a.out.replace(os.sep, "/")}')
        with open(a.hash_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
