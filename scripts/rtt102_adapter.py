"""RTT-102 adapter (IQ-19, design round 1): data/rtt-102/ -> the player's input, schema "rtt-series/1", kind "visits".

    python3 scripts/rtt102_adapter.py data/rtt-102 kits/rtt-102/race_rtt102.json --hash-file kits/rtt-102/dataset_hashes.txt

Reads (never writes) the data built in IQ-17 (pull request #21): series_monthly.csv, identities.csv and manifest.json
(every input's SHA-256 is checked against the build's own manifest first). No figure is changed, rounded or added.

Race (owner DEC-530 and the IQ-19 owner decision on Similarweb's trial, DEC-531): one event per month end, December 2022
to August 2026 (45). September 2026 is left out: only ChatGPT has a verified figure for it and the other bars stop at
August (brief IQ-19 section 2). Per assistant and month: `visits` exactly as series_monthly.csv gives it (whole visits;
a published month is the figure used, a month between two published months the build's straight line). An assistant
has no bar before its first published month.

After a bar's last published month (Copilot: September 2025, Meta AI: December 2025) the bar stays on the board with
that LAST PUBLISHED FIGURE, marked status "latest_figure" and provenance "h" (held): a display hold, never a figure for
the later month (house style 5, DEC-132; the contract: "any month after a bar's last published figure" is a claim the
data cannot support). The player ranks held bars below every bar with a figure for the month (config status.sink), dims
them and says "latest figure".

Per event and assistant:
  values  whole visits; style "estimated" for Similarweb's older estimates (series older_estimate = yes, i.e. every
          month before the first figure published on or after 28 Jul 2024; the player shows the stripes only in the
          option that marks them) else "official"; prov "p" published, "i" on a straight line, "h" held;
  labels  the bar's name at the end of that month (Bard until January 2024, Gemini from February 2024, DEC-511).
knots: each assistant's published months {date, v} (for the player's eased-motion option, which passes through every
published figure exactly); last: each assistant's last published month and figure (for "latest figure" labels).
Standard library only; deterministic (sorted keys, fixed separators).
"""
import argparse
import calendar
import csv
import hashlib
import json
import os

ADAPTER = 'rtt102-adapter/1.0'
ORDER = ['chatgpt', 'gemini', 'claude', 'copilot', 'perplexity', 'deepseek', 'grok', 'meta_ai']
INPUTS = ['series_monthly.csv', 'identities.csv']
LAST_MONTH = '2026-08'          # DEC-530 / DEC-531: the race ends in August 2026


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def month_end(m):
    y, mo = int(m[:4]), int(m[5:7])
    return '%04d-%02d-%02d' % (y, mo, calendar.monthrange(y, mo)[1])


def build(d):
    man = json.load(open(os.path.join(d, 'manifest.json'), encoding='utf-8'))
    files = man.get('files', man)
    for name in INPUTS:
        want = files.get(name)
        want = want.get('sha256') if isinstance(want, dict) else want
        if want != sha(os.path.join(d, name)):
            raise SystemExit('%s: SHA-256 does not match data/rtt-102/manifest.json' % name)
    series = rows(os.path.join(d, 'series_monthly.csv'))
    ids = rows(os.path.join(d, 'identities.csv'))
    final_label = {}
    for r in ids:
        if r['counted'] == 'yes' and r['assistant_id'] in ORDER and not r['to']:
            final_label[r['assistant_id']] = r['name']
    months = sorted({r['month'] for r in series if r['month'] <= LAST_MONTH})
    by = {}
    for r in series:
        if r['month'] > LAST_MONTH:
            continue
        a = r['assistant_id']
        if a not in ORDER:
            raise SystemExit('unknown assistant ' + a)
        v = r['visits']
        if not v.isdigit():
            raise SystemExit('%s %s: visits is not a whole number' % (r['month'], a))
        if r['provenance'] not in ('published', 'interpolated'):
            raise SystemExit('%s %s: provenance %s' % (r['month'], a, r['provenance']))
        if r['bound']:
            raise SystemExit('%s %s: a lower bound - the "+" label is not built yet (DEC-519)' % (r['month'], a))
        by[(r['month'], a)] = r
    first, last = {}, {}
    for (m, a), r in sorted(by.items()):
        first.setdefault(a, m)
        if r['provenance'] == 'published':
            last[a] = m
    for a in ORDER:
        if a not in first:
            raise SystemExit('no figures for ' + a)
        if by[(first[a], a)]['provenance'] != 'published':
            raise SystemExit(a + ': the first month is not a published figure')
    knots = {a: [] for a in ORDER}
    events = []
    for m in months:
        ev = {'date': month_end(m), 'month': m, 'values': {}, 'style': {}, 'prov': {}, 'labels': {}, 'status': {},
              'plus': [], 'source_id': 'SW'}
        for a in ORDER:
            r = by.get((m, a))
            if r is None:
                if a in last and m > last[a]:          # after the bar's last published month: held, "latest figure"
                    lr = by[(last[a], a)]
                    ev['values'][a] = int(lr['visits'])
                    ev['style'][a] = 'estimated' if lr['older_estimate'] == 'yes' else 'official'
                    ev['prov'][a] = 'h'
                    ev['labels'][a] = lr['bar_label']
                    ev['status'][a] = 'latest_figure'
                continue
            if a in last and m > last[a]:
                raise SystemExit('%s %s: a series row after the last published month' % (m, a))
            ev['values'][a] = int(r['visits'])
            ev['style'][a] = 'estimated' if r['older_estimate'] == 'yes' else 'official'
            ev['prov'][a] = 'p' if r['provenance'] == 'published' else 'i'
            ev['labels'][a] = r['bar_label']
            if r['provenance'] == 'published':
                knots[a].append({'date': ev['date'], 'v': int(r['visits'])})
        events.append(ev)
    entrants = []
    for a in ORDER:
        lm = last[a]
        entrants.append({'id': a, 'label': final_label[a], 'maker': a, 'launch_date': month_end(first[a]),
                         'first_month': first[a], 'last_month': lm, 'last_visits': int(by[(lm, a)]['visits']),
                         'ends_early': lm < LAST_MONTH})
    makers = [{'key': a, 'label': final_label[a]} for a in ORDER]
    return {'schema': 'rtt-series/1', 'kind': 'visits', 'adapter': ADAPTER,
            'measure': "Similarweb's published estimates of monthly website visits, worldwide (desktop and mobile web)",
            'unit': 'visits in the month', 'last_month': LAST_MONTH,
            'entrants': entrants, 'makers': makers, 'events': events, 'knots': knots}


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
        rel = os.path.relpath                      # run from the repo root (paths as the render workflow reads them)
        lines = ['# SHA-256 of the adapter inputs and output (%s)' % ADAPTER]
        for name in INPUTS + ['manifest.json']:
            p = os.path.join(a.data_dir, name)
            lines.append('%s input %s' % (sha(p), rel(p)))
        lines.append('%s output %s' % (sha(a.out), rel(a.out)))
        with open(a.hash_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')
    n = sum(len(e['values']) for e in race['events'])
    print('%s: %d month ends (%s .. %s), %d bar-months, %d held ("latest figure")' % (
        a.out, len(race['events']), race['events'][0]['month'], race['events'][-1]['month'], n,
        sum(1 for e in race['events'] for p in e['prov'].values() if p == 'h')))


if __name__ == '__main__':
    main()
