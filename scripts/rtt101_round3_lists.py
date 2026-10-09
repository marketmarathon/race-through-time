#!/usr/bin/env python3
"""RTT-101 (IQ-15i): from the private round 3 files, list (1) every U deal the undisclosed sweep covered, with or without a figure
(data/rtt-101/source/round3_researched.csv), and (2) the rows the helpers could only see as a search snippet (no readable quote) and the runner did not
confirm either (data/rtt-101/source/round3_unreadable.csv), for Cowork to read in Luke's Chrome. Only deal IDs, players and URLs are written.
Usage: rtt101_round3_lists.py PRIVATE_FOLDER"""
import csv, glob, os, sys

PRIV, D = sys.argv[1], "data/rtt-101"
rows = []
for f in sorted(glob.glob(os.path.join(PRIV, "part24[aefg]_*.csv"))):
    rows += [dict(r, _file=os.path.basename(f)[:7]) for r in csv.DictReader(open(f, encoding="utf-8-sig"))]
ids = sorted({r["deal_id"] for r in rows if r["deal_id"].startswith("U")})
with open(f"{D}/source/round3_researched.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(["deal_id"]); w.writerows([[d] for d in ids])
checked = {(c["url"]) for c in csv.DictReader(open(f"{D}/source/runner_checks.csv", encoding="utf-8")) if c["status"] == "VERIFIED"}
out = [r for r in rows if ((r.get("exact_quote") or "").strip().upper().startswith("NOT FOUND") or "snippet" in (r.get("notes") or "").lower())
       and (r.get("fee_as_reported") or "").strip().upper() not in ("", "NOT FOUND") and r["source_url"] not in checked]
with open(f"{D}/source/round3_unreadable.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(["deal_id", "player", "from_club", "to_club", "url", "file"])
    for r in out:
        w.writerow([r["deal_id"], r["player"], r["from_club"], r["to_club"], r["source_url"], r["_file"]])
print(len(ids), "U deals covered;", len(out), "rows with no readable quote and no runner confirmation")
