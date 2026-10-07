#!/usr/bin/env python3
"""RTT-103 (IQ-16): cross-check of the quarterly series against Market Marathon's Sharadar extract (8 Aug 2026).

Sharadar is licensed vendor data: a finding list and cross-check only, never evidence and never published. This script
writes the full comparison (with Sharadar's values) to the PRIVATE repo and prints only counts and match rates, which
are what the public files (I, J) carry.

Sharadar's `capex` is compared, quarter by quarter (dimension ARQ, as reported; matched on the fiscal period end), with
the build's series A (company-reported) and B (cash purchases of property and equipment) in reporting currency.
Usage: rtt103_sharadar_check.py <sharadar_csv> <data_dir (D file)> <private_out_csv>
"""
import csv
import sys
from collections import defaultdict

TICKER = {"AMZN": "amazon", "MSFT": "microsoft", "GOOGL": "alphabet", "META": "meta", "ORCL": "oracle",
          "BABA": "alibaba", "BIDU": "baidu"}


def main():
    shar, data_dir, out = sys.argv[1:4]
    d = defaultdict(dict)
    for r in csv.DictReader(open(f"{data_dir}/D_quarterly_capex_clean.csv")):
        d[r["company_id"]][r["period_end"]] = r
    rows, summary = [], defaultdict(lambda: defaultdict(int))
    for s in csv.DictReader(open(shar)):
        if s["dimension"] != "ARQ" or s["ticker"] not in TICKER or not s["capex"]:
            continue
        cid = TICKER[s["ticker"]]
        q = d[cid].get(s["reportperiod"])
        if not q:
            summary[cid]["no_matching_quarter"] += 1
            continue
        sv = abs(float(s["capex"]))
        a = float(q["company_reported_capex_usd"]) if q["company_reported_capex_usd"] else None
        b = float(q["cash_capex_usd"]) if q["cash_capex_usd"] else None
        local = float(q["capex_local_currency"]) if q["capex_local_currency"] else None
        cand = {"A": a, "B": b, "local": local if q["currency"] != "USD" else None}
        hit = [k for k, x in cand.items() if x is not None and abs(x - sv) <= max(1e6, 0.0005 * x)]
        verdict = "equals " + "/".join(hit) if hit else "differs"
        summary[cid][verdict] += 1
        ref = cand["local"] if q["currency"] != "USD" else (b if b is not None else a)
        rows.append({"company_id": cid, "period_end": s["reportperiod"], "sharadar_capex_abs": int(sv),
                     "sharadar_lastupdated": s["lastupdated"], "ours_A": a or "", "ours_B": b or "",
                     "ours_local": local or "", "verdict": verdict,
                     "diff_vs_reference_pct": round(100 * (sv - ref) / ref, 2) if ref else ""})
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for cid, c in sorted(summary.items()):
        print(cid, dict(c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
