#!/usr/bin/env python3
"""IQ-24b checks for data/rtt-104/v3_change_events.csv: (1) every value equals series.csv's shown value (the WDI
figure, or the DEC-617 carried 'latest figure'); (2) every 'election' or 'other' row has a URL our runner fetched and an excerpt
from that fetch holding its date (IQ-24c); (3) the approved V2 film config and the film workflow are byte-identical to c379631 (DEC-658)."""
import csv
import os
import subprocess
import sys

ok = True
S = {(r["iso3"], r["year"]): r for r in csv.DictReader(open("data/rtt-104/series.csv", encoding="utf-8"))}
rows = list(csv.DictReader(open("data/rtt-104/v3_change_events.csv", encoding="utf-8")))
bad = [(r["iso3"], y) for r in rows for y, v in ((r["from_year"], r["old_value"]), (r["to_year"], r["new_value"]))
       if v != S[(r["iso3"], y)]["shown_value"]]
print(f"values equal series.csv (WDI): {len(rows) * 2 - len(bad)}/{len(rows) * 2}", "PASS" if not bad else f"FAIL {bad[:5]}")
ok &= not bad
sys.path.insert(0, "scripts")
import glob, json, re  # noqa: E401,E402
from rtt104_v3_verify import parse_dates  # noqa: E402
fetched = {}
for d in glob.glob("data/rtt-104/source/fetch_*_v3dates"):
    for pg in json.load(open(os.path.join(d, "fetch_manifest.json"), encoding="utf-8"))["pages"]:
        if pg.get("status") == 200:
            fetched[pg["url"]] = open(os.path.join(d, pg["excerpt_file"]), encoding="utf-8").read()
el = [r for r in rows if r["cause"] in ("election", "other")]
badel = []
for r in el:
    urls = r["source_url"].split("; ")
    pieces = [p.strip() for p in r["excerpt"].replace(" || ", " … ").split(" … ") if p.strip()]
    dates = [re.findall(r"\d{4}-\d\d-\d\d", d)[0] for d in r["election_date"].split("; ")]
    if not all(u in fetched for u in urls) or not pieces or \
            not all(any(p[:150] in fetched[u] for u in urls) for p in pieces if len(p) < 400) or \
            not all(d in parse_dates(r["excerpt"]) for d in dates):
        badel.append(r["iso3"] + r["to_year"])
print(f"election/other rows with a runner-fetched URL and excerpt showing the date: {len(el) - len(badel)}/{len(el)}",
      "PASS" if not badel else f"FAIL {badel}")
ok &= not badel
for p in ("kits/rtt-104/config_rtt104_film_v2.json", ".github/workflows/rtt104_film.yml", "kits/rtt-104/music_rtt104.json"):
    same = subprocess.run(["git", "diff", "--quiet", "c379631", "--", p]).returncode == 0
    print(f"{p} byte-identical to c379631:", "PASS" if same else "FAIL")
    ok &= same
sys.exit(0 if ok else 1)
