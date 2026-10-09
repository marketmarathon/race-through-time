#!/usr/bin/env python3
"""RTT-101 (IQ-15f): list every transfer whose fee changes because of DEC-404 (a report that the deal was completed beats earlier
reports of bids, agreed fees or expected figures of the same grade). Builds once without the DEC-404 step and once with it, and
writes data/rtt-101/source/dec404_changes.csv with the fee before and after, the two reports and which list the deal is on
(source round 1 list A or B, the phase 2 same-grade conflicts, or other). Leaves the normal build's outputs in place."""
import csv, os, shutil, subprocess, sys, tempfile

D = "data/rtt-101"
env = dict(os.environ, RTT101_NO_DEC404="1", PYTHONHASHSEED="1")
subprocess.run([sys.executable, "scripts/build_rtt101_dataset.py"], env=env, check=True, stdout=subprocess.DEVNULL)
tmp = tempfile.mkdtemp()
for f in ("transfers.csv", "fee_evidence.csv"):
    shutil.copy(f"{D}/{f}", f"{tmp}/{f}")
subprocess.run([sys.executable, "scripts/build_rtt101_dataset.py"], env=dict(os.environ, PYTHONHASHSEED="1"), check=True,
               stdout=subprocess.DEVNULL)
rd = lambda p: list(csv.DictReader(open(p, encoding="utf-8")))
before = {t["transfer_id"]: t for t in rd(f"{tmp}/transfers.csv")}
after = {t["transfer_id"]: t for t in rd(f"{D}/transfers.csv")}
ev_b = {e["evidence_id"]: e for e in rd(f"{tmp}/fee_evidence.csv")}
ev_a = {e["evidence_id"]: e for e in rd(f"{D}/fee_evidence.csv")}
canon = lambda ev, tid: next((e for e in ev.values() if e["transfer_id"] == tid and e["canonical"] == "yes"), None)
lists = {}
for r in rd(f"{D}/source/source_round1_map.csv"):
    lists.setdefault(r["transfer_id"], "source round 1 list " + ("A" if r["deal_id"].startswith("A") else "B"))
if os.path.exists(f"{D}/source/source_round2_map.csv"):
    for r in rd(f"{D}/source/source_round2_map.csv"):
        lists.setdefault(r["transfer_id"], "source round 2")
# the 32 phase 2 same-grade conflicts settled by DEC-277 (conflicts.csv as committed at the end of IQ-15e, c62ca6b)
base = subprocess.run(["git", "show", "c62ca6b:data/rtt-101/conflicts.csv"], capture_output=True, text=True, check=True).stdout
phase2 = {r["transfer_id"] for r in csv.DictReader(base.splitlines()) if r.get("rule_result")}
rows = []
for tid, a in sorted(after.items(), key=lambda kv: (kv[1]["date"], kv[0])):
    b = before.get(tid)
    if not b or b["fee_gbp"] == a["fee_gbp"]:
        continue
    cb, ca = canon(ev_b, tid), canon(ev_a, tid)
    rows.append({"transfer_id": tid, "player": a["player"], "from_club": a["from_club"], "to_club": a["to_club"], "date": a["date"],
                 "fee_without_dec404": b["fee_gbp"], "fee_with_dec404": a["fee_gbp"],
                 "earlier_report": (cb or {}).get("quote", "")[:200], "earlier_url": (cb or {}).get("url", ""),
                 "completion_report": (ca or {}).get("quote", "")[:200], "completion_url": (ca or {}).get("url", ""),
                 "status_after": a["status"], "on_list": "; ".join(x for x in (lists.get(tid), "phase 2 same-grade conflict" if tid in phase2 else "") if x) or "other"})
cols = ["transfer_id", "player", "from_club", "to_club", "date", "fee_without_dec404", "fee_with_dec404", "earlier_report", "earlier_url",
        "completion_report", "completion_url", "status_after", "on_list"]
with open(f"{D}/source/dec404_changes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
print(len(rows), "transfers change fee because of DEC-404")
