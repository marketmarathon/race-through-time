#!/usr/bin/env python3
"""RTT-002: every entry into the all-time top ten for career Grand Prix wins.

Reads data/rtt-002/win_credits.csv (race order). After each race (all credits of
a shared drive applied together), drivers are ranked by career wins descending;
among equal totals, whoever reached that total first ranks higher (DEC-012 tie
display rule). An entry event is a driver in the top ten after a race who was not
in it before; the displaced driver is whoever was in it before and is not after.

Usage:
  python scripts/rtt002_topten.py data/rtt-002                      # writes topten_entries.csv, topten_at_freeze.csv
  python scripts/rtt002_topten.py data/rtt-002 <H.csv> <I.csv> <out.md>   # also compares with a private check
"""
import csv
import sys
import unicodedata
from collections import OrderedDict


def key(n):
    s = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().casefold()
    return " ".join(s.replace(" jr.", "").replace(".", "").replace("-", " ").split())


def compute(ddir):
    credits = list(csv.DictReader(open(f"{ddir}/win_credits.csv", encoding="utf-8")))
    races = OrderedDict()
    for c in credits:
        races.setdefault(int(c["race_index"]), []).append(c)
    wins, reached, names = {}, {}, {}
    top_before, events = [], []
    for ri, cs in races.items():
        for c in cs:
            d = c["driver_id"]
            names[d] = c["driver_name"]
            wins[d] = wins.get(d, 0) + 1
            reached[d] = int(c["credit_index"])  # moment this total was reached
        order = sorted(wins, key=lambda d: (-wins[d], reached[d]))
        top = order[:10]
        new = [d for d in top if d not in top_before]
        gone = [d for d in top_before if d not in top]
        for d in new:
            events.append({"race_date": cs[0]["race_date"], "season": cs[0]["season"], "round": cs[0]["round"],
                           "grand_prix": cs[0]["grand_prix"], "driver_id": d, "driver_name": names[d],
                           "career_wins": wins[d], "position_entered": top.index(d) + 1,
                           "dropped_out_id": ";".join(gone), "dropped_out": ";".join(names[g] for g in gone) or "NONE"})
        top_before = top
    final = [{"rank": i + 1, "driver_id": d, "driver_name": names[d], "wins": wins[d]} for i, d in enumerate(top_before)]
    return events, final


def main():
    ddir = sys.argv[1]
    events, final = compute(ddir)
    with open(f"{ddir}/topten_entries.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(events[0]), lineterminator="\n")
        w.writeheader(); w.writerows(events)
    with open(f"{ddir}/topten_at_freeze.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(final[0]), lineterminator="\n")
        w.writeheader(); w.writerows(final)
    print(f"{len(events)} top-ten entry events; top ten at freeze:", ", ".join(f"{r['driver_name']} {r['wins']}" for r in final))
    if len(sys.argv) < 5:
        return
    h = list(csv.DictReader(open(sys.argv[2], encoding="utf-8-sig")))
    i = list(csv.DictReader(open(sys.argv[3], encoding="utf-8-sig")))
    aliases = {"nino farina": "giuseppe farina"}  # the check notes these are the same driver
    k = lambda n: aliases.get(key(n), key(n))
    ours = {(e["race_date"], k(e["driver_name"])): e for e in events}
    theirs = {(r["date"], k(r["driver"])): r for r in h}
    disc = []
    for kk in sorted(set(ours) | set(theirs)):
        o, t = ours.get(kk), theirs.get(kk)
        if o is None or t is None:
            disc.append(("H", f"{kk[0]} {kk[1]}", "present" if o else "absent", "present" if t else "absent"))
            continue
        for label, ov, tv in (("career wins", str(o["career_wins"]), t["career_wins_at_moment"]),
                              ("position entered", str(o["position_entered"]), t["position_entered"]),
                              ("dropped out", k(o["dropped_out"]) if o["dropped_out"] != "NONE" else "none",
                               k(t["driver_dropped_out"]) if t["driver_dropped_out"] != "NONE" else "none")):
            if ov != tv:
                disc.append(("H", f"{kk[0]} {o['driver_name']} {label}", ov, tv))
    for r in i:
        o = final[int(r["rank"]) - 1]
        if k(o["driver_name"]) != k(r["driver"]) or str(o["wins"]) != r["career_grand_prix_wins"]:
            disc.append(("I", f"rank {r['rank']}", f"{o['driver_name']} {o['wins']}", f"{r['driver']} {r['career_grand_prix_wins']}"))
    md = ["# RTT-002 second independent check: top-ten entries (H) and top ten at freeze (I)", "",
          f"Build events: {len(events)}; check rows: {len(h)}. Top ten at freeze compared: {len(i)} ranks.",
          "Disagreements are listed, not resolved.", "", f"**Discrepancies: {len(disc)}**", ""]
    if disc:
        md += ["| Section | Item | Wikipedia build | Independent check |", "|---|---|---|---|"]
        md += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in disc]
    md += ["", "Name alias used: Nino Farina (check) = Giuseppe Farina (Wikipedia), as the check itself notes.", ""]
    open(sys.argv[4], "w", encoding="utf-8").write("\n".join(md))
    print("DISCREPANCIES:", len(disc))
    for d in disc:
        print(" ", d)


if __name__ == "__main__":
    main()
