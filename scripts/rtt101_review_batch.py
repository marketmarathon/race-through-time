#!/usr/bin/env python3
"""RTT-101 phase 2: record Claude's reading of a Tier 1 batch's VERIFIED quotes in data/rtt-101/source/review_decisions.csv.
Usage: rtt101_review_batch.py BATCH 'Player A=reason' 'Player B=reason' ...  (named players' current quotes are rejected,
every other VERIFIED canonical quote in the batch is accepted as read). Rerun after a rebuild until the batch is clean."""
import csv, os, sys

batch, rejects = sys.argv[1], dict(a.split("=", 1) for a in sys.argv[2:])
P = "data/rtt-101/source/review_decisions.csv"
rows = {r["check_id"]: r for r in csv.DictReader(open(P, encoding="utf-8"))} if os.path.exists(P) else {}
E = {e["transfer_id"]: e for e in csv.DictReader(open("data/rtt-101/fee_evidence.csv", encoding="utf-8")) if e["canonical"] == "yes"}
n = 0
for x in csv.DictReader(open("data/rtt-101/tier1_list.csv", encoding="utf-8")):
    e = E.get(x["transfer_id"])
    if x["batch"] != batch or not e or not e["check_id"] or x["status"] != "VERIFIED":
        continue
    rej = (rejects.get(x["player"] + "@" + x["from_club"] + ">" + x["to_club"]) or rejects.get(x["player"] + "@" + x["to_club"])
           or rejects.get(x["player"]))
    scope = "amount" if rej and rej.startswith("amount:") else "check"
    rows[e["check_id"]] = {"check_id": e["check_id"], "batch": batch, "transfer_id": x["transfer_id"], "player": x["player"],
                           "amount": e["amount"], "quote": e["quote"], "decision": "reject" if rej else "accept", "scope": scope,
                           "note": (rej[7:].strip() if scope == "amount" else rej) if rej else "quote read: the figure is this deal's fee",
                           "reviewed_by": "Claude Code (IQ-15b)"}
    n += 1
with open(P, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["check_id", "batch", "transfer_id", "player", "amount", "quote", "decision", "scope", "note", "reviewed_by"], lineterminator="\n")
    w.writeheader()
    for k in sorted(rows):
        w.writerow({c: rows[k].get(c, "") for c in w.fieldnames})
print(batch, n, "quotes recorded;", sum(1 for r in rows.values() if r["decision"] == "reject"), "rejected in total")
