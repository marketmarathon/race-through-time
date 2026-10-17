#!/usr/bin/env python3
"""RTT-104 V3 Part 1 (IQ-24b): every year-to-year change for the countries ever in a top-20 board, from our own data.

Same figures and the same rules as data/rtt-104/boards.csv (DEC-604/DEC-611 4 m threshold, DEC-612 latest-year
population, DEC-617 single-gap carry), ranked with the same sort as build_rtt104_dataset.build_boards (value
descending, then short name). Ranks are full ranks among every country on the race that year; 'visible' means rank
<= 20 in either year; 'big' (rule b) means visible AND (|change| >= 5.0 points OR the rank moves by 3 or more);
'big_points' (rule a, IQ-24c working default) means visible AND |change| >= 5.0 points.

  python3 scripts/rtt104_v3_changes.py data/rtt-104 [causes.csv]

Without causes.csv every big change is 'not yet researched'. With it (data/rtt-104/source/v3_causes.csv, written by
scripts/rtt104_v3_verify.py from our runner's excerpts, IQ-24c), every visible change gets its matched cause, date,
type, window, borderline flags, URL, excerpt and status.
Writes data/rtt-104/v3_change_events.csv and prints the counts used by the cost check.
"""
import csv
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_rtt104_dataset as b  # noqa: E402

TOP_N, BIG_POINTS, BIG_RANKS = 20, Decimal("5.0"), 3
FIELDS = ["iso3", "country", "from_year", "to_year", "old_value", "new_value", "old_value_1dp", "new_value_1dp",
          "change_points", "old_rank", "new_rank", "visible", "big", "big_points", "cause", "election_date", "election_type",
          "window", "borderline", "source_url", "excerpt", "status", "note"]


def rankings(cfg, economies, disp, elig, years):
    out = {}
    for y in years:
        cand = [(Decimal(disp[c][y][0]), economies[c]["short_name"], c) for c in economies
                if elig[c] and disp[c][y][0] is not None]
        out[y] = {c: (i, v) for i, (v, _, c) in enumerate(sorted(cand, key=lambda t: (-t[0], t[1])), 1)}
    return out


def main(data_dir, causes_path=None):
    cfg, raw, economies, parl, pop, *_ = b.load_inputs(data_dir)
    years = list(range(cfg["first_year"], cfg["last_year"] + 1))
    disp = {c: b.display_values(parl.get(c, {}), years) for c in economies}
    elig = b.eligible(economies, pop, Decimal(cfg["population_threshold"]))
    rk = rankings(cfg, economies, disp, elig, years)
    # check: the top 10 here equal boards.csv's top board, rank for rank
    with open(os.path.join(data_dir, "boards.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["board"] == "top":
                y, c = int(r["year"]), r["iso3"]
                if rk[y].get(c, (None,))[0] != int(r["rank"]) or disp[c][y][0] != r["value"]:
                    raise SystemExit(f"top-20 ranking disagrees with boards.csv at {y} {c}")
    causes = {}
    if causes_path:
        with open(causes_path, encoding="utf-8") as f:
            causes = {(r["iso3"], r["to_year"]): r for r in csv.DictReader(f)}
    ever = sorted({c for y in years for c, (i, _) in rk[y].items() if i <= TOP_N}, key=lambda c: economies[c]["short_name"])
    rows = []
    for c in ever:
        for y0, y1 in zip(years, years[1:]):
            a, z = rk[y0].get(c), rk[y1].get(c)
            if a is None and z is None:
                continue
            r = {"iso3": c, "country": economies[c]["short_name"], "from_year": y0, "to_year": y1,
                 "old_value": disp[c][y0][0] or "", "new_value": disp[c][y1][0] or "",
                 "old_value_1dp": b.one_dp(disp[c][y0][0]) if a else "", "new_value_1dp": b.one_dp(disp[c][y1][0]) if z else "",
                 "old_rank": a[0] if a else "", "new_rank": z[0] if z else "",
                 "visible": "y" if (a and a[0] <= TOP_N) or (z and z[0] <= TOP_N) else "n"}
            notes = [f"{yy} is a 'latest figure' carried from {disp[c][yy][2]} (DEC-617)"
                     for yy in (y0, y1) if disp[c][yy][1] == "latest_figure"]
            if a and z:
                d = z[1] - a[1]
                r["change_points"] = str(d.quantize(Decimal("0.01")))
                r["big"] = "y" if r["visible"] == "y" and (abs(d) >= BIG_POINTS or abs(z[0] - a[0]) >= BIG_RANKS) else "n"
                r["big_points"] = "y" if r["visible"] == "y" and abs(d) >= BIG_POINTS else "n"
            else:
                r["change_points"], r["big"], r["big_points"] = "", "n", "n"
                gone = y1 if not z else y0
                notes.append(f"no figure in {gone} ({disp[c][gone][1]}): {'leaves' if not z else 'joins'} the race")
            k = causes.get((c, str(y1)))
            if r["visible"] == "y" and causes:  # IQ-24c: every visible change is matched (DEC-666 onwards)
                for f in ("cause", "election_date", "election_type", "window", "borderline", "source_url", "excerpt", "status"):
                    r[f] = k[f] if k else ""
                notes.append(k.get("note", "") if k else "")
            elif r["big"] == "y":
                if k:
                    for f in ("cause", "election_date", "election_type", "window", "borderline", "source_url", "excerpt", "status"):
                        r[f] = k[f]
                    notes.append(k.get("note", ""))
                else:
                    r["cause"], r["status"] = "not yet researched", ""
            else:
                r["cause"] = "not researched"
            r["note"] = "; ".join(n for n in notes if n)
            rows.append(r)
    with open(os.path.join(data_dir, "v3_change_events.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    big = [r for r in rows if r["big"] == "y"]
    print(f"countries ever in top {TOP_N}: {len(ever)}; changes: {len(rows)}; visible: "
          f"{sum(r['visible'] == 'y' for r in rows)}; big: {len(big)}; countries with a big change: "
          f"{len({r['iso3'] for r in big})}")
    return rows


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
