#!/usr/bin/env python3
"""RTT-104 (IQ-22): write the player input kits/rtt-104/race_rtt104.json from the built data in data/rtt-104/.

Usage: python3 scripts/rtt104_player_input.py data/rtt-104 kits/rtt-104/race_rtt104.json kits/rtt-104/dataset_hashes.txt

Deterministic, standard library only. Nothing is computed here that changes a figure: every board value, its one-decimal
text, the 0% group, the world line and the closing card are copied from the build's own files. The only extra input is
data/rtt-104/source/leave_notes.csv (the on-screen line for a country whose figures stop or pause while it is on a
board, owner decision DEC-625), whose wording rests on the VERIFIED quote in closing_card_reasons.csv or, for a pause, on
its own VERIFIED source; a row that is not VERIFIED is not passed to the player.
"""
import csv
import hashlib
import json
import os
import sys


def rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(data_dir, out, hashes):
    files = ["boards.csv", "zero_group.csv", "world.csv", "closing_card.csv", "countries.csv", "series.csv",
             "source/leave_notes.csv"]
    boards = rows(os.path.join(data_dir, "boards.csv"))
    countries = {r["iso3"]: r for r in rows(os.path.join(data_dir, "countries.csv"))}
    series = {(r["iso3"], int(r["year"])): r for r in rows(os.path.join(data_dir, "series.csv"))}
    years = sorted({int(b["year"]) for b in boards})
    used = sorted({b["iso3"] for b in boards})
    zero = {int(r["year"]): r for r in rows(os.path.join(data_dir, "zero_group.csv"))}
    for r in series.values():   # the 0% group's members by id, from the series flags (the CSV lists names)
        if r["in_zero_group"] == "yes":
            used.append(r["iso3"])
    for r in rows(os.path.join(data_dir, "closing_card.csv")):   # the closing card shows each country's flag too
        if r["on_card"] == "yes":
            used.append(r["iso3"])
    used = sorted(set(used))
    out_years = []
    for y in years:
        yb = [b for b in boards if int(b["year"]) == y]
        def side(name):
            return [{"id": b["iso3"], "v": b["value"], "t": b["value_1dp"], "latest": b["latest_figure"] == "yes",
                     "from": b["carried_from_year"]} for b in sorted((b for b in yb if b["board"] == name), key=lambda b: int(b["rank"]))]
        zids = sorted((r["iso3"] for r in series.values() if int(r["year"]) == y and r["in_zero_group"] == "yes"),
                      key=lambda c: countries[c]["short_name"])
        if len(zids) != int(zero[y]["count"]) or "; ".join(countries[c]["short_name"] for c in zids) != zero[y]["countries"]:
            raise SystemExit(f"0% group {y} does not match zero_group.csv")
        # every rank on each side (in the race, shown value; same order as the build: full precision, then name; IQ-22d: all ranks, for V2's smooth curves), so the
        # player can bring a country up from below the board and take one down out of it; ranks 1-10 must equal boards.csv
        cand = [(r["iso3"], r["shown_value"]) for (c, yy), r in series.items() if yy == y and r["shown_value"] != ""
                and countries[c]["in_race"] == "yes"]
        from decimal import Decimal
        topo = sorted(cand, key=lambda t: (-Decimal(t[1]), countries[t[0]]["short_name"]))
        boto = sorted((t for t in cand if Decimal(t[1]) > 0), key=lambda t: (Decimal(t[1]), countries[t[0]]["short_name"]))
        for name, lst in (("top", topo), ("bottom", boto)):
            if [t[0] for t in lst[:10]] != [b["id"] for b in side(name)]:
                raise SystemExit(f"{y} {name}: ranks 1-10 differ from boards.csv")
        for t in topo + boto:
            used.append(t[0])
        out_years.append({"year": y, "top": side("top"), "bottom": side("bottom"), "zero": zids,
                          "ranks": {"top": [{"id": c, "v": v} for c, v in topo], "bottom": [{"id": c, "v": v} for c, v in boto]}})
    used = sorted(set(used))
    entrants = [{"id": c, "label": countries[c]["short_name"], "flag": countries[c]["iso2"].lower(),
                 "region": countries[c]["region"]} for c in used]
    world = [{"year": int(r["year"]), "v": r["wdi_value"], "t": r["value_1dp"]} for r in rows(os.path.join(data_dir, "world.csv"))]
    card = [{"id": r["iso3"], "label": r["country"], "line": r["card_wording"], "last_year": int(r["last_figure_year"])}
            for r in rows(os.path.join(data_dir, "closing_card.csv")) if r["on_card"] == "yes"]
    leaves = []
    for r in rows(os.path.join(data_dir, "source", "leave_notes.csv")):
        if r["status"] != "VERIFIED":
            continue
        y = int(r["leaves_in"])
        prev = [b for b in boards if int(b["year"]) == y - 1 and b["iso3"] == r["iso3"]]
        if not prev or series[(r["iso3"], y)]["shown_value"] != "":
            raise SystemExit(f"leave_notes.csv: {r['iso3']} is not on a board in {y - 1} with no figure in {y}")
        leaves.append({"id": r["iso3"], "year": y, "board": prev[0]["board"], "rank": int(prev[0]["rank"]),
                       "note": r["note"], "returns": int(r["returns"]) if r["returns"] else None})
    doc = {"dataset": "RTT-104", "kind": "split_share", "unit": "percent", "years": years, "entrants": entrants,
           "frames": out_years, "world": world, "closing_card": card, "leaves": leaves,
           "source": "data/rtt-104 (scripts/build_rtt104_dataset.py); written by scripts/rtt104_player_input.py"}
    # the flag list read by the shared driver's loader (kits/rtt-002/rtt.js loadFlags: driver_id, flag_code)
    with open(os.path.join(os.path.dirname(out), "flags.csv"), "w", encoding="utf-8", newline="") as f:
        f.write("driver_id,flag_code\n" + "".join(f"{e['id']},{e['flag']}\n" for e in entrants))
    text = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    lines = [f"{sha(os.path.join(data_dir, p))}  input   data/rtt-104/{p}" for p in files]
    lines.append(f"{sha(out)}  output  kits/rtt-104/{os.path.basename(out)}")
    with open(hashes, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{out}: {len(years)} years, {len(entrants)} countries, {len(leaves)} leave notes, {len(card)} closing-card lines")


if __name__ == "__main__":
    main(*sys.argv[1:4])
