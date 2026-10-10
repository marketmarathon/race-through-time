"""RTT-103 adapter (IQ-18, design round 1): data/rtt-103/ -> the player's input, schema "rtt-series/1", kind "money".

    python scripts/rtt103_adapter.py data/rtt-103 kits/rtt-103/race_rtt103.json --hash-file kits/rtt-103/dataset_hashes.txt

Reads (never writes) the final data merged by Luke on 8 Oct 2026 (pull request #20): AI_SPENDING_RACE_MASTER.csv,
L_aggregate_capex.csv, AI_SPENDING_RACE_LOOKAHEAD.csv, AI_SPENDING_RACE_FORECAST.csv, AI_SPENDING_RACE_PEAK_VIEWS.csv
and G_AI_capex_story_events.csv. No figure is changed, rounded or added.

Race: one event per calendar quarter end (31 Mar 2010 .. 30 Jun 2026, 66). Per company and quarter end: the
trailing-12-month capital spending exactly as the master gives it (capex_TTM_usd, whole US dollars). A company with no
row has no entry (no bar): before its first valid point (late entrants, DEC-295) and inside a gap (Alibaba's TTM points
2016 Q2 - 2017 Q4, definition break; metric contract). Every value is "official" (all rows ACTUAL_VERIFIED_AT_SOURCE).
`combined` per quarter end = the sum of that quarter's bars, checked equal, to the dollar, to L_aggregate_capex.csv
(DEC-324: "Combined capital spending" is the sum of the bars on screen). `gaps` lists each run of missing quarter ends
between a company's first and last value, with the last value before it (for the player's "hold" option, drawn without
a number).

Steps after the race (drawn in round 1 only as design stills, kits/rtt-103/steps.js): the "2026 plans" and look-ahead
rows of AI_SPENDING_RACE_LOOKAHEAD.csv (bounds as printed), ByteDance's greyed 2026 row from the forecast file
(DEC-296, DEC-309), the peak views allowed on screen with BCG's group chart values to 2030, and the story-moment candidates of G (verbatim, with type and
source). Standard library only; deterministic (sorted keys, fixed separators).
"""
import argparse
import csv
import hashlib
import json
import os

ADAPTER = 'rtt103-adapter/1.0'
ORDER = ['Amazon', 'Microsoft', 'Alphabet', 'Meta', 'Oracle', 'Alibaba', 'Tencent', 'Baidu', 'CoreWeave']
INPUTS = ['AI_SPENDING_RACE_MASTER.csv', 'L_aggregate_capex.csv', 'AI_SPENDING_RACE_LOOKAHEAD.csv',
          'AI_SPENDING_RACE_FORECAST.csv', 'AI_SPENDING_RACE_PEAK_VIEWS.csv', 'G_AI_capex_story_events.csv',
          'source/forecast_lookahead_2027_2031.csv']


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def cid(name):
    return name.lower()


def build(d):
    master = rows(os.path.join(d, 'AI_SPENDING_RACE_MASTER.csv'))
    dates = sorted({r['date'] for r in master})
    names, first, warn = {}, {}, {}
    vals = {}
    for r in master:
        if r['data_status'] != 'ACTUAL_VERIFIED_AT_SOURCE':
            raise SystemExit('unexpected data_status ' + r['data_status'])
        c = r['company']
        if c not in ORDER:
            raise SystemExit('unknown company ' + c)
        v = r['capex_TTM_usd']
        if not v.isdigit():
            raise SystemExit('%s %s: TTM is not a whole number of dollars' % (r['date'], c))
        if r['capex_TTM_usd_bn'] != '%.3f' % (int(v) / 1e9):
            raise SystemExit('%s %s: bn column disagrees with the dollar column' % (r['date'], c))
        vals.setdefault(r['date'], {})[cid(c)] = int(v)
        names[cid(c)] = r['display_name']
        first[cid(c)] = min(first.get(cid(c), r['date']), r['date'])
        if r['definition_warning'].startswith('ON-SCREEN NOTE'):
            warn[cid(c)] = r['definition_warning']
    agg = {r['quarter']: r for r in rows(os.path.join(d, 'L_aggregate_capex.csv'))}
    events = []
    for dt in dates:
        v = vals[dt]
        q = '%s-Q%d' % (dt[:4], (int(dt[5:7]) - 1) // 3 + 1)
        a = agg[q]
        if sum(v.values()) != int(a['aggregate_TTM_capex_usd']) or len(v) != int(a['number_of_companies_with_valid_data']):
            raise SystemExit('%s: sum of bars %d (%d companies) differs from L_aggregate_capex.csv %s (%s)' % (dt, sum(v.values()), len(v), a['aggregate_TTM_capex_usd'], a['number_of_companies_with_valid_data']))
        ids = sorted(v)
        events.append({'date': dt, 'quarter': q, 'values': {k: v[k] for k in ids}, 'style': {k: 'official' for k in ids},
                       'prov': {k: 'o' for k in ids}, 'plus': [], 'combined': sum(v.values())})
    gaps = []
    for c in map(cid, ORDER):
        have = [i for i, e in enumerate(events) if c in e['values']]
        for a, b in zip(have, have[1:]):
            if b > a + 1:
                gaps.append({'id': c, 'last': events[a]['date'], 'last_value': events[a]['values'][c],
                             'from': events[a + 1]['date'], 'to': events[b - 1]['date'], 'returns': events[b]['date'], 'points': b - a - 1})
    entrants = [{'id': cid(c), 'label': names[cid(c)], 'maker': cid(c), 'launch_date': first[cid(c)]} for c in ORDER]
    makers = [{'key': cid(c), 'label': c} for c in ORDER]

    look = rows(os.path.join(d, 'AI_SPENDING_RACE_LOOKAHEAD.csv'))
    keep = ['frame_year', 'step', 'company', 'display_name', 'row_type', 'estimate_low_usd_bn', 'estimate_high_usd_bn',
            'label', 'period_label', 'growth_source', 'reliability', 'notes']
    steps = [{k: r[k] for k in keep} for r in look]
    fc = [r for r in rows(os.path.join(d, 'AI_SPENDING_RACE_FORECAST.csv'))
          if r['company'] == 'ByteDance' and r['forecast_year'] == '2026' and r['display_style'] == 'greyed']
    if len(fc) != 1:
        raise SystemExit('expected one greyed ByteDance 2026 row, found %d' % len(fc))
    bytedance = {k: fc[0][k] for k in ['display_name', 'forecast_amount_usd_bn', 'display_note', 'forecaster', 'forecast_date', 'measure']}
    peaks = [{k: r[k] for k in ['forecaster', 'scope', 'view', 'peak_year', 'measure', 'status', 'notes']}
             for r in rows(os.path.join(d, 'AI_SPENDING_RACE_PEAK_VIEWS.csv')) if r['on_screen_allowed'] == 'YES' and r['status'] == 'VERIFIED']
    # BCG's group chart (read by eye by Cowork, DEC-340), only for the peak step (DEC-328), to 2030 (DEC-337)
    bcg = [{'year': r['forecast_year'], 'value_usd_bn': r['single']} for r in rows(os.path.join(d, 'source', 'forecast_lookahead_2027_2031.csv'))
           if r['forecaster'] == 'BCG' and r['verification'].startswith('VERIFIED') and not r['superseded_by'] and r['forecast_year'] <= '2030']
    story = [{k: r[k] for k in ['date', 'company', 'event_type', 'event', 'amount_if_stated', 'amount_type', 'source_grade', 'source']}
             for r in rows(os.path.join(d, 'G_AI_capex_story_events.csv'))]
    return {'schema': 'rtt-series/1', 'kind': 'money', 'unit': 'usd', 'adapter': ADAPTER,
            'measure': 'trailing-12-month capital expenditure (cash purchases of property and equipment as each company prints it), nominal US$',
            'entrants': entrants, 'makers': makers, 'events': events, 'gaps': gaps, 'notes': warn,
            'steps': {'lookahead': steps, 'bytedance_2026': bytedance, 'peaks': peaks, 'bcg_group': sorted(bcg, key=lambda r: r['year'])}, 'story': story}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data_dir'); ap.add_argument('out'); ap.add_argument('--hash-file')
    a = ap.parse_args()
    race = build(a.data_dir)
    s = json.dumps(race, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n'
    with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)
    print('%s: %d quarter ends, %d companies, %d gap(s), %d look-ahead rows, %d peak views, %d story rows' % (
        a.out, len(race['events']), len(race['entrants']), len(race['gaps']), len(race['steps']['lookahead']), len(race['steps']['peaks']), len(race['story'])))
    if a.hash_file:
        h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
        lines = ['# SHA-256 of the adapter inputs and output (%s)' % ADAPTER]
        lines += ['%s input data/rtt-103/%s' % (h(os.path.join(a.data_dir, n)), n) for n in INPUTS]
        lines.append('%s output kits/rtt-103/%s' % (h(a.out), os.path.basename(a.out)))
        with open(a.hash_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
