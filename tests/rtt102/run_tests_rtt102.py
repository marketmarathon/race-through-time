#!/usr/bin/env python3
"""RTT-102 tests (IQ-17): the brief's checks, re-done independently of the build, plus two clean rebuilds.

    python3 tests/rtt102/run_tests_rtt102.py

Exit code 0 only if every test passes. Standard library only.
"""
import csv
import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data", "rtt-102")
REPORT = os.path.join(ROOT, "reports", "RTT-102_data_report.md")
BUILD = os.path.join(ROOT, "scripts", "build_rtt102_dataset.py")
IMPORT = os.path.join(ROOT, "scripts", "rtt102_import_research.py")
PRIVATE = os.environ.get("RTT102_PRIVATE_RESEARCH", os.path.join(os.path.dirname(ROOT), "race-through-time-private", "research", "rtt-102"))
OUTPUTS = ["points.csv", "conflicts.csv", "series_monthly.csv", "place_changes.csv", "turns.csv", "checks.json", "CHECKS.md", "manifest.json"]
results = []


def test(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mi(m):
    return int(m[:4]) * 12 + int(m[5:]) - 1


def rebuild(tmp):
    d = os.path.join(tmp, "data")
    shutil.copytree(os.path.join(DATA, "source"), os.path.join(d, "source"))
    shutil.copy(os.path.join(DATA, "identities.csv"), d)
    r = subprocess.run([sys.executable, BUILD, d, os.path.join(tmp, "report.md")], capture_output=True, text=True)
    return d, r


# T01 two clean rebuilds are identical, and equal to the committed files
with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
    da, ra = rebuild(a)
    db, rb = rebuild(b)
    same = all(filecmp.cmp(os.path.join(da, f), os.path.join(db, f), shallow=False) for f in OUTPUTS) and \
        filecmp.cmp(os.path.join(a, "report.md"), os.path.join(b, "report.md"), shallow=False)
    test("T01 two clean rebuilds are byte-identical", same and ra.returncode == 0 and rb.returncode == 0, ra.stdout.strip())
    committed = all(filecmp.cmp(os.path.join(da, f), os.path.join(DATA, f), shallow=False) for f in OUTPUTS) and \
        filecmp.cmp(os.path.join(a, "report.md"), REPORT, shallow=False)
    test("T02 committed outputs equal a fresh rebuild (nothing edited by hand)", committed)

pts = rows("points.csv")
ser = rows("series_monthly.csv")
ident = [r for r in rows("identities.csv") if r["counted"] == "yes"]
checks = json.load(open(os.path.join(DATA, "checks.json"), encoding="utf-8"))
used = {(r["assistant_id"], r["month"]): r for r in pts if r["used"] == "yes"}
byid = {r["obs_id"]: r for r in pts}
test("T03 the build's own checks all PASS", all(c["result"] == "PASS" for c in checks), f"{len(checks)} checks")

bad = [s["assistant_id"] + s["month"] for s in ser if s["provenance"] == "published" and not (
    byid[s["point_id"]]["status"] == "VERIFIED" and byid[s["point_id"]]["url"].startswith("http")
    and byid[s["point_id"]]["exact_quote"] and not byid[s["point_id"]]["exact_quote"].startswith("[research"))]
test("T04 every on-screen value is VERIFIED with a URL and the wording seen at source", not bad, str(bad[:5]))

bad = []
for s in ser:
    if s["provenance"] == "interpolated":
        l, r = byid[s["left_point"]], byid[s["right_point"]]
        exp = int(l["visits"]) + (int(r["visits"]) - int(l["visits"])) * (mi(s["month"]) - mi(l["month"])) / (mi(r["month"]) - mi(l["month"]))
        if abs(int(s["visits"]) - exp) > 0.5 + 1e-6:
            bad.append(s["assistant_id"] + s["month"])
        if not (l["month"] < s["month"] < r["month"]):
            bad.append("order " + s["assistant_id"] + s["month"])
test("T05 straight lines: every interpolated month lies on the line between its two published points", not bad, str(bad[:5]))

printed = {}
for r in pts:
    if r["visits"]:
        printed.setdefault((r["assistant_id"], r["month"]), set()).add(int(r["visits"]))
bad = [s["assistant_id"] + s["month"] for s in ser if s["provenance"] == "published" and int(s["visits"]) not in printed[(s["assistant_id"], s["month"])]]
test("T06 no averaging: every published month shows a figure exactly as printed by one publication", not bad, str(bad))

start = {}
for r in ident:
    start[r["assistant_id"]] = min(start.get(r["assistant_id"], "9999"), r["from"][:7])
bad = [s["assistant_id"] + s["month"] for s in ser if s["month"] < start[s["assistant_id"]]]
test("T07 no point before the site's start date", not bad, str(bad))

keys = [(s["assistant_id"], s["month"]) for s in ser]
test("T08 one row and one address per assistant per month", len(keys) == len(set(keys)))

ds = [r for r in used.values() if r["assistant_id"] == "deepseek"]
bad = [r["obs_id"] for r in ds if r["domain"] != "deepseek.com" or "chat.deepseek.com" in r["site_as_recorded"]
       or (r["source_type"] == "P" and "deepseek.com" not in r["site_as_recorded"])]
chat = [r["obs_id"] for r in pts if "chat.deepseek.com" in r["site_as_recorded"] and r["used"] == "yes"]
test("T09 DeepSeek uses deepseek.com only, never with chat.deepseek.com added", not bad and not chat and ds, f"{len(ds)} points")

proj = [r for r in pts if "projection" in (r["qualifier"] + r["measure"]).lower()]
jun = next(s for s in ser if s["assistant_id"] == "chatgpt" and s["month"] == "2024-06")
test("T10 no forecast: projections never used (ChatGPT June 2024 is a straight line)", proj and all(r["used"] == "no" for r in proj) and jun["provenance"] == "interpolated")

test("T11 data_version set on every point and series row", all(r["data_version"] in ("older", "current") for r in pts) and all(s["data_version"] for s in ser))
test("T12 data_version follows the 28 Jul 2024 rule", all((r["data_version"] == "older") == (r["publication_date"] < "2024-07-28") for r in pts if r["publication_date"][:2] == "20"))

test("T13 ChatGPT May 2024 = 2.2 billion (current version beats 2.5 billion)", used[("chatgpt", "2024-05")]["visits"] == "2200000000")
names = {(s["assistant_id"], s["month"]): s for s in ser}
test("T14 Bard until Jan 2024, Gemini from Feb 2024; chatgpt.com from May 2024",
     names[("gemini", "2024-01")]["bar_label"] == "Bard" and names[("gemini", "2024-02")]["bar_label"] == "Gemini"
     and names[("chatgpt", "2024-04")]["domain"] == "chat.openai.com" and names[("chatgpt", "2024-05")]["domain"] == "chatgpt.com")
test("T15 Le Chat, Bing Chat and Grok inside X have no bar", not {s["assistant_id"] for s in ser} - {"chatgpt", "gemini", "claude", "copilot", "perplexity", "deepseek", "grok", "meta_ai"})
first = {}
for (a, m) in used:
    first[a] = min(first.get(a, m), m)
bad = [s["assistant_id"] + s["month"] for s in ser if s["month"] < first[s["assistant_id"]] or s["month"] > max(m for (x, m) in used if x == s["assistant_id"])]
test("T16 no extrapolation: bars run only between their first and last published month", not bad, str(bad))
confl = rows("conflicts.csv")
test("T17 leftover conflicts use no figure", all(not c["used_point"] for c in confl if c["status"].startswith("LEFTOVER")))

listed = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
private_names = ("part01_", "part02_", "part03_", "part04a_", "part04b_", "part05a_", "part05b_", "part05c_", "cowork_", "RTT-102_chatgpt_", "00_README.md")
bad = [p for p in listed if os.path.basename(p).startswith(private_names) and "rtt-102" in p]
test("T18 no private research file is committed (DEC-006)", not bad, str(bad))

if os.path.isdir(PRIVATE):
    with tempfile.TemporaryDirectory() as t:
        r = subprocess.run([sys.executable, IMPORT, PRIVATE, t], capture_output=True, text=True)
        same = r.returncode == 0 and all(filecmp.cmp(os.path.join(t, f), os.path.join(DATA, "source", f), shallow=False)
                                         for f in ("publications.csv", "observations_research.csv", "verification.csv", "inputs_sha256.csv"))
        test("T19 the private inputs still match their SHA-256 and re-import to the committed source tables", same, r.stderr.strip()[-200:])
else:
    results.append(("T19 private re-import (skipped: private research folder not present)", True, "skipped"))

fails = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
print(f"\n{len(results) - len(fails)}/{len(results)} PASS")
sys.exit(1 if fails else 0)
