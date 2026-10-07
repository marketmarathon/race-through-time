#!/usr/bin/env python3
"""RTT-103 data build tests (IQ-16). Run: python tests/rtt103/run_tests_rtt103.py

1. SYNTHETIC fixture: an HTML cash-flow table whose cells contain source line breaks and <p> tags must come out as one
   text row per table row (this parsing failed twice during IQ-16).
2. The build is deterministic: building twice gives identical manifests.
3. Known values that must hold (each checked at source during IQ-16).
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from rtt103_sec_docs import to_text, cf_sections  # noqa: E402
from rtt103_us_extract import rows_of, role_of  # noqa: E402

results = []


def t(name, ok, detail=""):
    results.append((name, ok, detail))


SYNTHETIC_HTML = b"""<html><body><p>SYNTHETIC TEST FIXTURE - not real data</p>
<p>CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS</p><p>(In millions)</p>
<table><tr><td><p>Cash flows from investing
activities</p></td></tr>
<tr><td><p>Purchases of property
and equipment</p></td><td>(1,234</td><td>)</td><td>(567</td><td>)</td></tr>
<tr><td>Principal payments on finance leases</td><td>&#8212;</td><td>(89</td><td>)</td></tr>
""" + b"".join(b"<tr><td>Line %d</td><td>1,%03d</td></tr>\n" % (i, i) for i in range(20)) + b"""
<tr><td>See accompanying notes</td></tr></table></body></html>"""

text = to_text(SYNTHETIC_HTML)
row = [ln for ln in text.split("\n") if ln.startswith("Purchases of property")]
t("SYNTHETIC: a wrapped label and its numbers stay on one row", len(row) == 1 and "1,234" in row[0] and "567" in row[0], row[:1])
secs = cf_sections(text)
t("SYNTHETIC: the cash-flow section is found", len(secs) == 1)
parsed = {role_of(lb)[0]: nums for lb, _, nums in rows_of(secs[0][1]) if role_of(lb)[0]}
t("SYNTHETIC: purchases row parsed as two negative numbers", parsed.get("ppe_purchases") == [(1234, True), (567, True)], parsed.get("ppe_purchases"))
t("SYNTHETIC: a dash keeps its column", parsed.get("finance_lease_principal") == [(0, False), (89, True)], parsed.get("finance_lease_principal"))

# 2. determinism
tmp = tempfile.mkdtemp()
try:
    for k in (1, 2):
        d = os.path.join(tmp, f"b{k}")
        shutil.copytree(os.path.join(ROOT, "data", "rtt-103", "source"), os.path.join(d, "source"))
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_rtt103_dataset.py"), d], check=True)
    m1 = json.load(open(os.path.join(tmp, "b1", "manifest.json")))
    m2 = json.load(open(os.path.join(tmp, "b2", "manifest.json")))
    t("build is deterministic (two builds, identical manifests)", m1 == m2)
    committed = json.load(open(os.path.join(ROOT, "data", "rtt-103", "manifest.json")))
    t("committed outputs equal a fresh build", committed == m1,
      sorted(k for k in m1["files"] if committed["files"].get(k) != m1["files"][k])[:5])
finally:
    shutil.rmtree(tmp)


# 3. known values
def rows(name):
    return list(csv.DictReader(open(os.path.join(ROOT, "data", "rtt-103", name), encoding="utf-8")))


e = {(r["calendar_quarter"], r["company"]): r for r in rows("E_capex_TTM_race.csv")}
t("Amazon TTM to 31 Mar 2010 = 458m (Amazon's own printed twelve-month figure)", e[("2010-Q1", "Amazon")]["TTM_capex_usd"] == "458000000")
d = {(r["company_id"], r["period_end"]): r for r in rows("D_quarterly_capex_clean.csv")}
t("Amazon Q1 2017: gross 2,148 minus proceeds 287 = net 1,861 as first printed", d[("amazon", "2017-03-31")]["company_reported_capex_usd"] == "1861000000"
  and d[("amazon", "2017-03-31")]["cash_capex_usd"] == "2148000000")
fy26 = sum(int(d[("alibaba", e_)]["capex_local_currency"]) for e_ in ("2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31"))
t("Alibaba FY2026 quarters sum to the printed RMB126,063m", fy26 == 126063000000, fy26)
t("Alibaba Mar 2017 - Mar 2018 are DEFINITION_BREAK (five quarters)",
  sum(1 for r in rows("H_coverage_matrix.csv") if r["Alibaba"] == "DEFINITION_BREAK") == 5)
master = rows("AI_SPENDING_RACE_MASTER.csv")
t("Master ends at the latest common complete quarter (2026-06-30)", max(r["date"] for r in master) == "2026-06-30")
t("Master holds no 2026 estimate", all(r["data_status"] == "ACTUAL_VERIFIED_AT_SOURCE" for r in master))
checks = json.load(open(os.path.join(ROOT, "data", "rtt-103", "checks.json")))
t("Every financial and file-format check passes", all(c["result"] == "PASS" for c in checks["checks"] if c["kind"] != "crosscheck"))

for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  [{detail}]"))
n_ok = sum(1 for _, ok, _ in results if ok)
print(f"{n_ok}/{len(results)} PASS")
sys.exit(0 if n_ok == len(results) else 1)
