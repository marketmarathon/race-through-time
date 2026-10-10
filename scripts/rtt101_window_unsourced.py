#!/usr/bin/env python3
"""RTT-101 (IQ-15j): list one window's deals with a PL club whose fee is not confirmed at source (undisclosed, or a figure only Wikipedia
gives), for the next research round. No fee figures in the list (as with source_round2_list.csv). Loans, free transfers and releases
are left out. Usage: rtt101_window_unsourced.py "January 2020" data/rtt-101/source/jan2020_unsourced.csv
       rtt101_window_unsourced.py "January 1993;summer 2007" OUT --club-pages-only   (several windows; only deals found on club-season
       pages, i.e. the ones the list pages miss; a window column is added) (IQ-15m)"""
import csv, re, sys

wins, out_path = set(sys.argv[1].split(";")), sys.argv[2]
club_only = "--club-pages-only" in sys.argv[3:]
D = "data/rtt-101"
T = list(csv.DictReader(open(f"{D}/transfers.csv", encoding="utf-8")))
PL = {(r["club_id"], r["season"]) for r in csv.DictReader(open(f"{D}/pl_membership.csv", encoding="utf-8"))}
names = {r["club_id"]: r["display_name"] for r in csv.DictReader(open(f"{D}/source/club_aliases.csv", encoding="utf-8"))}


def window_of(d):
    m, y = int(d[5:7]), int(d[:4])
    return f"summer {y}" if 4 <= m <= 10 else (f"January {y}" if m <= 3 else f"January {y + 1}")


out = []
for t in sorted(T, key=lambda t: (t["date"], t["player"])):
    if window_of(t["date"]) not in wins or (club_only and not re.search(r"^Wikipedia: \d{4}–\d{2,4} .* season", t["found_via"])) or t["status"] == "VERIFIED" or t["type"] in ("loan", "free", "loan_return") or t["to_club"] == "Free agent":
        continue
    if not any((c, t["season_attributed"]) in PL for c in (t["from_club"], t["to_club"])):
        continue
    if t["type"] == "undisclosed":
        need = "a reported fee from club/league or grade A/B press (the clubs did not disclose it)"
    elif float(t["fee_gbp"] or 0) > 0:
        need = "the fee confirmed at a club/league or grade A/B source (only Wikipedia gives it now)"
    else:
        need = "the fee, or confirmation that there was none, from club/league or grade A/B press"
    out.append({**({"window": window_of(t["date"])} if len(wins) > 1 else {}), "deal_id": t["transfer_id"], "date": t["date"], "player": t["player"], "from_club": names.get(t["from_club"], t["from_club"]),
                "to_club": names.get(t["to_club"], t["to_club"]), "type": t["type"], "what_we_need": need})
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=(["window"] if len(wins) > 1 else []) + ["deal_id", "date", "player", "from_club", "to_club", "type", "what_we_need"], lineterminator="\n")
    w.writeheader(); w.writerows(out)
print(len(out), "deals listed for", "; ".join(sorted(wins)))
