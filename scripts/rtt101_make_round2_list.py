#!/usr/bin/env python3
"""RTT-101 (IQ-15g): the list of deals for ChatGPT research round 2 (DEC-275 route), all seasons 1992-2026.
A deal is on the list when (a) it is a Tier 1 transfer with a fee but no confirmed club, league or press source (a Soccerbase row alone
is not enough: tier1_needs_press_source.csv), (b) every figure found is a maximum, a total with add-ons or an approximation
(tier1_max_or_approx_only.csv), (c) the fee used comes from a completion report whose figure is only "reported", "believed to be",
"understood" or "thought to be" (DEC-404 changes; also written to source/dec404_soft_figures.csv), or (d) Luke's answers put it there
(Kanu, Normann, the cash part of Parker/Carr; DEC-413, DEC-414, DEC-406), or (e) it was on source round 1 (lists A and B) and still has
no confirmed club, league or press source, even if it has since left Tier 1. No fee figure is written to the list.
Writes data/rtt-101/source_round2_list.csv, data/rtt-101/source/source_round2_map.csv and data/rtt-101/source/dec404_soft_figures.csv."""
import csv, re

D = "data/rtt-101"
rd = lambda p: list(csv.DictReader(open(p, encoding="utf-8")))
T = {t["transfer_id"]: t for t in rd(f"{D}/transfers.csv")}
NAME = {c["club_id"]: c["display_name"] for c in rd(f"{D}/clubs.csv")}
SOFT = re.compile(r"\b(reported(ly)?|believed to be|believed|understood|thought to be)\b", re.I)

need = {}  # transfer_id -> list of needs (a deal can need more than one thing)


def add(tid, what):
    if tid in T and what not in need.setdefault(tid, []):
        need[tid].append(what)


for r in rd(f"{D}/tier1_needs_press_source.csv"):
    t = T.get(r["transfer_id"])
    if not t:
        continue
    add(r["transfer_id"], "press or club source for the fee (only a database confirms it)" if t["status"] == "VERIFIED"
        else "fee from a page naming both clubs")
for r in rd(f"{D}/tier1_max_or_approx_only.csv"):
    add(r["transfer_id"], "exact guaranteed fee, only a maximum or approximation found")
soft = []
for r in rd(f"{D}/source/dec404_changes.csv"):
    if SOFT.search(r["completion_report"]) and T.get(r["transfer_id"], {}).get("fee_gbp") == r["fee_with_dec404"]:
        soft.append(r)
        add(r["transfer_id"], "firmer figure than 'reported'")
for r in rd(f"{D}/source/source_round1_map.csv"):
    t = T.get(r["transfer_id"])
    if t and float(t["fee_gbp"] or 0) > 0 and not (t["status"] == "VERIFIED" and t["grade"] in ("A", "B")):
        add(r["transfer_id"], "press or club source for the fee (only a database confirms it)" if t["status"] == "VERIFIED"
            else "fee from a page naming both clubs")
add("T8a33680cd3", "firmer figure, reports disagree")                       # Kanu (DEC-413)
add("T2b24256749", "fee, one report says undisclosed and another gives a figure")  # Normann (DEC-414)
PAIRS = {"T1a5ab511b5": "T452fd91ab6"}                                      # Parker/Carr: one deal, both transfers (DEC-406)
add("T1a5ab511b5", "cash part of a part-exchange")

# one deal per transfer, except a part-exchange pair, which is one deal mapped to both transfers
deals = sorted(need, key=lambda k: (T[k]["date"], k))
with open(f"{D}/source_round2_list.csv", "w", newline="", encoding="utf-8") as f, \
        open(f"{D}/source/source_round2_map.csv", "w", newline="", encoding="utf-8") as g:
    w = csv.writer(f, lineterminator="\n")
    m = csv.writer(g, lineterminator="\n")
    w.writerow(["deal_id", "season", "approx_date", "player", "from_club", "to_club", "what_we_need"])
    m.writerow(["deal_id", "transfer_id", "player", "date"])
    for n, k in enumerate(deals, 1):
        t = T[k]
        did = f"R{n:04d}"
        player = t["player"] + (" and " + T[PAIRS[k]]["player"] + " (exchange)" if k in PAIRS else "")
        w.writerow([did, t["season_attributed"], t["date"], player, NAME.get(t["from_club"], t["from_club"]), NAME.get(t["to_club"], t["to_club"]),
                    "; ".join(need[k])])
        for tid in [k] + ([PAIRS[k]] if k in PAIRS else []):
            m.writerow([did, tid, T[tid]["player"], T[tid]["date"]])
with open(f"{D}/source/dec404_soft_figures.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["transfer_id", "player", "date", "fee_used_gbp", "fee_without_dec404_gbp", "wording", "completion_report", "completion_url"])
    for r in soft:
        w.writerow([r["transfer_id"], r["player"], r["date"], r["fee_with_dec404"], r["fee_without_dec404"],
                    SOFT.search(r["completion_report"]).group(0), r["completion_report"], r["completion_url"]])
print(len(deals), "deals for round 2;", len(soft), "DEC-404 fees resting on a 'reported' figure")
