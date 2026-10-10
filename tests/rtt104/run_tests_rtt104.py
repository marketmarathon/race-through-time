#!/usr/bin/env python3
"""RTT-104 data build tests (IQ-20). Run: python3 tests/rtt104/run_tests_rtt104.py

1. Two clean rebuilds (fresh copies of data/rtt-104 inputs only) are byte-identical, and equal the committed outputs.
2. Every value in series.csv and boards.csv is traceable to the raw WDI file (read independently here).
3. No 0% is shown where the data is missing; no value is shown that is not that year's figure or the previous year's
   figure across a single missing year (DEC-617).
4. No country below the population threshold is on a board or in the 0% group (owner rule, DEC-611, DEC-612).
5. No forecast: no year after the last WDI year with figures.
6. Closing card: only VERIFIED reasons are on the card, and every quote is found in its fetched excerpt (DEC-613).
7. SYNTHETIC checks of the missing-year rule, and known values checked against the raw file.
"""
import csv
import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from build_rtt104_dataset import display_values  # noqa: E402

DATA = os.path.join(ROOT, "data", "rtt-104")
OUTPUTS = ["countries.csv", "series.csv", "boards.csv", "boards_2_5m_comparison.csv", "zero_group.csv", "ties.csv",
           "world.csv", "closing_card.csv", "events.csv", "wdi_owid_differences.csv", "checks.json", "manifest.json"]
results = []


def t(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def rows(name, base=DATA):
    return list(csv.DictReader(open(os.path.join(base, name), encoding="utf-8")))


def clean_build(dst):
    os.makedirs(dst)
    shutil.copy(os.path.join(DATA, "config.json"), dst)
    shutil.copytree(os.path.join(DATA, "source"), os.path.join(dst, "source"))
    rep = os.path.join(dst, "report.md")
    p = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_rtt104_dataset.py"), dst, rep],
                       capture_output=True, text=True)
    return p.returncode, rep


# 1 determinism
tmp = tempfile.mkdtemp()
try:
    r1, rep1 = clean_build(os.path.join(tmp, "a"))
    r2, rep2 = clean_build(os.path.join(tmp, "b"))
    t("build exits 0 (all build checks pass)", r1 == 0 and r2 == 0, f"{r1} {r2}")
    same = all(filecmp.cmp(os.path.join(tmp, "a", f), os.path.join(tmp, "b", f), shallow=False) for f in OUTPUTS)
    t("two clean rebuilds byte-identical", same and filecmp.cmp(rep1, rep2, shallow=False))
    committed = all(filecmp.cmp(os.path.join(tmp, "a", f), os.path.join(DATA, f), shallow=False) for f in OUTPUTS)
    committed = committed and filecmp.cmp(rep1, os.path.join(ROOT, "reports", "RTT-104_data_report.md"), shallow=False)
    t("committed outputs equal a clean rebuild", committed)
finally:
    shutil.rmtree(tmp)

cfg = json.load(open(os.path.join(DATA, "config.json")))
raw = os.path.join(DATA, cfg["source_raw_dir"])
rawv = {}
for r in json.load(open(os.path.join(raw, "wdi_SG.GEN.PARL.ZS_all_1997-2025.json")), parse_float=str, parse_int=str)[1]:
    if r["value"] is not None:
        rawv[(r["countryiso3code"], int(r["date"]))] = r["value"]
pops = {}
for r in json.load(open(os.path.join(raw, "wdi_SP.POP.TOTL_all_1997-2026.json")), parse_float=str, parse_int=str)[1]:
    if r["value"] is not None:
        pops.setdefault(r["countryiso3code"], {})[int(r["date"])] = Decimal(r["value"])
series = rows("series.csv")
boards = rows("boards.csv")

# 2 traceability
bad = [s for s in series if s["wdi_value"] and rawv.get((s["iso3"], int(s["year"]))) != s["wdi_value"]]
bad += [s for s in series if not s["wdi_value"] and (s["iso3"], int(s["year"])) in rawv]
t("every series value equals the raw WDI text (and none is dropped)", not bad, f"{len(bad)}")
bad = [b for b in boards if rawv.get((b["iso3"], int(b["carried_from_year"] or b["year"]))) != b["value"]]
t("every board value traceable to the WDI file", not bad, f"{len(bad)}")

# 3 no invented values, no 0% where missing
bad = [s for s in series if s["missing"] == "yes" and s["shown_value"] and s["shown_as"] != "latest_figure"]
bad += [s for s in series if s["shown_as"] == "latest_figure" and not (
    (s["iso3"], int(s["year"]) - 1) in rawv and (s["iso3"], int(s["year"]) + 1) in rawv)]
t("nothing shown where missing except a single-year 'latest figure'", not bad, f"{len(bad)}")
bad = [s for s in series if s["missing"] == "yes" and (s["zero"] == "yes" or
       (s["in_zero_group"] == "yes" and s["shown_as"] != "latest_figure"))]
t("no 0% where the data is missing", not bad, f"{len(bad)}")

# 4 threshold
T = Decimal(cfg["population_threshold"])
t("owner threshold is 4,000,000 (DEC-611)", T == Decimal(4000000))
inrace = {c for c, p in pops.items() if p[max(p)] >= T}
bad = [b for b in boards if b["iso3"] not in inrace]
bad += [s for s in series if s["in_zero_group"] == "yes" and s["iso3"] not in inrace]
t("no country below the threshold on a board or in the 0% group", not bad, f"{len(bad)}")
yrs = {}
for s in series:
    yrs.setdefault(s["iso3"], set()).add(s["below_threshold"])
t("population rule fixes each country for the whole race (DEC-612)", all(len(v) == 1 for v in yrs.values()))

# 5 no forecast
maxy = max(y for (_, y) in rawv)
t("no year after the last WDI year", all(int(s["year"]) <= maxy for s in series) and all(int(b["year"]) <= maxy for b in boards))

# 6 closing card
cc = rows("closing_card.csv")
reasons = rows(os.path.join("source", "closing_card_reasons.csv"))
bad = [c for c in cc if (c["on_card"] == "yes") != (c["status"] == "VERIFIED")]
t("only VERIFIED reasons on the closing card", not bad and cc, f"{len(bad)}")
bad = []
for r in reasons:
    if r["quote"]:
        text = open(os.path.join(ROOT, r["excerpt_file"]), encoding="utf-8").read()
        parts = [p.strip() for p in r["quote"].replace("... ", "|").split("|") if p.strip()]
        if not all(p in text for p in parts):
            bad.append(r["iso3"])
t("every closing-card quote is in its fetched excerpt", not bad, str(bad))
bad = [c for c in cc if c["iso3"] not in inrace or (c["iso3"], cfg["last_year"]) in rawv]
t("closing card = in the race with no figure in the last year", not bad)

# 7 synthetic rule checks (SYNTHETIC values, not real data)
d = display_values({2000: "5", 2002: "7", 2005: "9", 2006: "0"}, list(range(1999, 2009)))
t("SYNTHETIC: one missing year shows the previous figure as latest figure", d[2001] == ("5", "latest_figure", "2000"))
t("SYNTHETIC: two missing years are off the board", d[2003][0] is None and d[2004][0] is None and d[2003][1] == "gap_off_board")
t("SYNTHETIC: before the first and after the last figure nothing is shown",
  d[1999] == (None, "before_first_figure", "") and d[2007] == (None, "after_last_figure", ""))
t("SYNTHETIC: a real 0 stays 0, a missing year never becomes 0", d[2006] == ("0", "figure", "") and d[2008][0] is None)

# known values (raw WDI file)
lead = {int(b["year"]): b["country"] for b in boards if b["board"] == "top" and b["rank"] == "1"}
t("known: Sweden leads 1997-2002, Rwanda 2003-2025",
  all(lead[y] == "Sweden" for y in range(1997, 2003)) and all(lead[y] == "Rwanda" for y in range(2003, 2026)))
t("known: Rwanda 2003 = 48.75, UAE 2019 = 50, Saudi Arabia 2013 = 19.8675496688742",
  rawv[("RWA", 2003)] == "48.75" and rawv[("ARE", 2019)] == "50" and rawv[("SAU", 2013)] == "19.8675496688742")

# 8 IQ-22: the player input (kits/rtt-104/race_rtt104.json) is rebuilt identically from the data, and every board value in it
#   is the data's own text
tmp = tempfile.mkdtemp()
try:
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "rtt104_player_input.py"), DATA, os.path.join(tmp, "r.json"),
                    os.path.join(tmp, "h.txt")], capture_output=True, check=True)
    kit = os.path.join(ROOT, "kits", "rtt-104")
    t("player input rebuilt identically (race_rtt104.json, flags.csv, dataset_hashes.txt)",
      filecmp.cmp(os.path.join(tmp, "r.json"), os.path.join(kit, "race_rtt104.json"), shallow=False)
      and filecmp.cmp(os.path.join(tmp, "flags.csv"), os.path.join(kit, "flags.csv"), shallow=False)
      and open(os.path.join(tmp, "h.txt")).read().split("output")[0] == open(os.path.join(kit, "dataset_hashes.txt")).read().split("output")[0])
    race = json.load(open(os.path.join(kit, "race_rtt104.json"), encoding="utf-8"))
    bad = [(f["year"], k, b["id"]) for f in race["frames"] for k in ("top", "bottom") for b in f[k]
           if not any(r["iso3"] == b["id"] and int(r["year"]) == f["year"] and r["board"] == k and r["value"] == b["v"]
                      and r["value_1dp"] == b["t"] for r in boards)]
    t("every player-input board value equals boards.csv", not bad, str(bad[:3]))
    notes = rows(os.path.join("source", "leave_notes.csv"))
    t("leave notes only for countries on a board the year before with no figure that year",
      all(any(b["iso3"] == n["iso3"] and int(b["year"]) == int(n["leaves_in"]) - 1 for b in boards)
          and (n["iso3"], int(n["leaves_in"])) not in rawv for n in notes))
finally:
    shutil.rmtree(tmp)

passed = sum(1 for _, ok, _ in results if ok)
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
print(f"RTT-104 tests: {passed}/{len(results)} PASS")
sys.exit(0 if passed == len(results) else 1)
