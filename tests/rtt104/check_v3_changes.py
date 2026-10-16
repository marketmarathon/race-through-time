#!/usr/bin/env python3
"""IQ-24b checks for data/rtt-104/v3_change_events.csv: (1) every value equals series.csv's shown value (the WDI
figure, or the DEC-617 carried 'latest figure'); (2) every 'election' row has a Parline URL and an excerpt holding its
date; (3) the approved V2 film config and the film workflow are byte-identical to c379631 (DEC-658)."""
import csv
import subprocess
import sys

ok = True
S = {(r["iso3"], r["year"]): r for r in csv.DictReader(open("data/rtt-104/series.csv", encoding="utf-8"))}
rows = list(csv.DictReader(open("data/rtt-104/v3_change_events.csv", encoding="utf-8")))
bad = [(r["iso3"], y) for r in rows for y, v in ((r["from_year"], r["old_value"]), (r["to_year"], r["new_value"]))
       if v != S[(r["iso3"], y)]["shown_value"]]
print(f"values equal series.csv (WDI): {len(rows) * 2 - len(bad)}/{len(rows) * 2}", "PASS" if not bad else f"FAIL {bad[:5]}")
ok &= not bad
el = [r for r in rows if r["cause"] == "election"]
badel = [r["iso3"] + r["to_year"] for r in el if "data.ipu.org" not in r["source_url"] or not r["excerpt"]
         or not any(p in r["excerpt"] for p in (r["election_date"], r["election_date"].replace("-", "")))]
print(f"election rows with a Parline URL and a dated excerpt: {len(el) - len(badel)}/{len(el)}", "PASS" if not badel else f"FAIL {badel}")
ok &= not badel
for p in ("kits/rtt-104/config_rtt104_film_v2.json", ".github/workflows/rtt104_film.yml", "kits/rtt-104/music_rtt104.json"):
    same = subprocess.run(["git", "diff", "--quiet", "c379631", "--", p]).returncode == 0
    print(f"{p} byte-identical to c379631:", "PASS" if same else "FAIL")
    ok &= same
sys.exit(0 if ok else 1)
