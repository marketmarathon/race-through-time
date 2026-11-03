"""IQ-27 number-format test (RTT-003): which figures may be shown as whole numbers ("155,370,000").

Rule (Claude working choice, a proposal for Luke; owner rule: full numbers only where the source publishes the figure
to that precision, estimates keep their compact form):
  - a console qualifies when the maker's own figures for it are published to 10,000 units (0.01 million) or finer:
    at least half of its quarters that rest on a maker figure (provenance official / held / arithmetic, display style
    official) are NOT whole multiples of 100,000 units. In this dataset that is Nintendo's hardware (its quarterly
    "Dedicated Video Game Sales Units" tables give two decimals of a million) and the original PlayStation (Sony's
    final 102.49 million);
  - within a qualifying console, a quarter is shown in full only when its figure rests on a maker figure (official,
    held or arithmetic provenance with official display style); interpolated, estimated and analyst-estimate quarters
    keep the approved compact label ("27.6m").
Nothing is computed or changed: the figures are series.csv's. Writes kits/rtt-003/config_rtt003_numfmt_B.json's
values.full_digits.points (from data/rtt-003/series.csv) and prints the qualifying consoles.
"""
import csv, json, collections, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / 'data/rtt-003/series.csv', newline='')))
MAKER = lambda r: r['provenance'] in ('official', 'held', 'arithmetic') and r['display_style'] == 'official'
fine = collections.defaultdict(lambda: [0, 0])
for r in rows:
    if MAKER(r):
        fine[r['console_id']][1] += 1
        if int(r['units']) % 100000: fine[r['console_id']][0] += 1
qual = sorted(c for c, (f, n) in fine.items() if n and f / n >= 0.5)
points = collections.defaultdict(list)
for r in rows:
    if r['console_id'] in qual and MAKER(r): points[r['console_id']].append(r['quarter_end'])
out = ROOT / 'kits/rtt-003/config_rtt003_numfmt_B.json'
cfg = json.loads(out.read_text())
cfg['values']['full_digits']['points'] = {k: points[k] for k in sorted(points)}
out.write_text(json.dumps(cfg, indent=1, ensure_ascii=False) + '\n')
print('qualifying consoles:', ', '.join(f'{c} ({fine[c][0]}/{fine[c][1]})' for c in qual))
print('compact (published to 0.1m or coarser):', ', '.join(sorted(c for c in fine if c not in qual)))
print('points written:', sum(len(v) for v in points.values()))
if '--window' in sys.argv:
    a, b = sys.argv[sys.argv.index('--window') + 1:sys.argv.index('--window') + 3]
    for r in rows:
        if a <= r['quarter_end'] <= b:
            print(r['quarter_end'], r['console_id'], r['units'], r['provenance'], r['display_style'], 'FULL' if r['console_id'] in qual and MAKER(r) else 'compact')
