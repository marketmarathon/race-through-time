"""RTT-104 V3 design round (IQ-24d): the player input for the top-20 board and its tags.

Usage: python3 scripts/rtt104_v3_tags.py [data_dir] [race_in] [race_out]
       (defaults data/rtt-104, kits/rtt-104/race_rtt104.json, kits/rtt-104/race_rtt104_v3.json)

Writes a copy of V2's player input (which is NOT changed) with two additions:
  top20  per year, the race's ranks 1-20 in the order of the V2 input's own full ranking (frames[].ranks.top), each with
         series.csv's shown_value_1dp as its text; stops if ranks 1-10 differ from boards.csv's top board;
  continents  each entrant's UN M49 region (IQ-24e), from data/rtt-104/source/fetch_*_m49/m49_entrants.csv;
  tags   one per change row of data/rtt-104/v3_change_events.csv that is visible, big under rule (b) (big = y; rule (a)
         is big_points = y), explained (cause election or other), VERIFIED, with a source URL and a fetched excerpt.
         Unexplained changes get no tag. The tag text uses the true event date, month and year only.
Nothing here computes a figure: values and texts are copied from the data files.
"""
import csv
import glob
import json
import os
import sys

MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
OTHER = {"quota or seat law": "Quota law", "dissolved or suspended": "Parliament dissolved", "appointed seats": "Appointed seats"}


def month(d):
    return MON[int(d[5:7]) - 1], d[:4]


def tag_text(r):
    dates = [d.strip().split(" to ")[0] for d in r["election_date"].split(";")]
    types = [t.strip() for t in r["election_type"].split(");")] if r["election_type"] else [""] * len(dates)
    types = (types + [""] * len(dates))[:len(dates)]
    if r["cause"] == "election":
        gen = [d for d, t in zip(dates, types) if t.startswith("general election")] or dates[:1]
        months = list(dict.fromkeys(month(d)[0] for d in gen))     # one month named once (Tanzania: two dates, Dec 2005)
        if len(months) >= 2 and len({d[:4] for d in gen}) == 1:
            return "Elections · " + " & ".join(months) + " " + gen[0][:4]
        m, y = month(gen[0])
        return f"Election · {m} {y}"
    kind = next((v for k, v in OTHER.items() if types[0].startswith(k)), None)
    if not kind:
        raise SystemExit(f"no tag wording for cause type {types[0]!r} ({r['country']} {r['to_year']})")
    m, y = month(dates[0])
    return f"{kind} · {m} {y}"


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else "data/rtt-104"
    rin = sys.argv[2] if len(sys.argv) > 2 else "kits/rtt-104/race_rtt104.json"
    rout = sys.argv[3] if len(sys.argv) > 3 else "kits/rtt-104/race_rtt104_v3.json"
    race = json.load(open(rin, encoding="utf-8"))
    series = {(r["iso3"], int(r["year"])): r for r in csv.DictReader(open(os.path.join(data, "series.csv"), encoding="utf-8"))}
    boards = [r for r in csv.DictReader(open(os.path.join(data, "boards.csv"), encoding="utf-8")) if r["board"] == "top"]
    top20 = {}
    for fr in race["frames"]:
        y = fr["year"]
        rows = [{"id": b["id"], "v": b["v"], "t": series[(b["id"], y)]["shown_value_1dp"]} for b in fr["ranks"]["top"][:20]]
        want = [(r["iso3"], r["value_1dp"]) for r in sorted((r for r in boards if int(r["year"]) == y), key=lambda r: int(r["rank"]))]
        if [(x["id"], x["t"]) for x in rows[:10]] != want:
            raise SystemExit(f"{y}: ranks 1-10 differ from boards.csv")
        top20[str(y)] = rows
    tags = []
    for r in csv.DictReader(open(os.path.join(data, "v3_change_events.csv"), encoding="utf-8")):
        if not (r["visible"] == "y" and r["big"] == "y" and r["cause"] in ("election", "other")):
            continue
        if r["status"] != "VERIFIED" or not r["excerpt"].strip() or not r["source_url"].strip():
            raise SystemExit(f"explained big change without a VERIFIED row and excerpt: {r['country']} {r['to_year']}")
        first = r["election_date"].split(";")[0].strip()[:10]
        tags.append({"id": r["iso3"], "to_year": int(r["to_year"]), "text": tag_text(r), "date": first,
                     "rule_a": r["big_points"] == "y", "rule_b": True, "cause": r["cause"],
                     "points": r["change_points"], "ranks": f"{r['old_rank']}->{r['new_rank']}",
                     "late": int(first[:4]) < int(r["to_year"]), "source_url": r["source_url"]})
    race["top20"] = top20
    race["tags"] = tags
    # IQ-24e: each entrant's UN M49 region (Africa, Americas, Asia, Europe, Oceania), from the runner's fetch of the
    # M49 table (FETCH_SET=m49); stops if any entrant has none
    m49 = sorted(glob.glob(os.path.join(data, "source", "fetch_*_m49", "m49_entrants.csv")))
    if len(m49) != 1:
        raise SystemExit(f"expected one M49 fetch, found {m49}")
    reg = {r["iso3"]: r["region_name"] for r in csv.DictReader(open(m49[0], encoding="utf-8"))}
    missing = [e["id"] for e in race["entrants"] if reg.get(e["id"]) not in ("Africa", "Americas", "Asia", "Europe", "Oceania")]
    if missing:
        raise SystemExit(f"no M49 region for {missing}")
    race["continents"] = {e["id"]: reg[e["id"]] for e in race["entrants"]}
    race["source"] = race["source"] + "; top20 and tags added by scripts/rtt104_v3_tags.py (IQ-24d)"
    with open(rout, "w", encoding="utf-8") as f:
        json.dump(race, f, ensure_ascii=False, sort_keys=True, indent=1)
        f.write("\n")
    a = sum(t["rule_a"] for t in tags)
    print(f"wrote {rout}: {len(top20)} years of top 20, {len(tags)} tags (rule a {a}, rule b {len(tags)}), "
          f"{sum(t['late'] for t in tags)} with the event in the year before the jump")


if __name__ == "__main__":
    main()
