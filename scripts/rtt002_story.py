#!/usr/bin/env python3
"""RTT-002 story moments: the races the full film emphasises, each backed by the audited data.

Reads only files already in data/rtt-002/ (none is changed) and writes ONE new file,
data/rtt-002/story_moments.csv, plus a readable list, reports/RTT-002_story_moments.md.

Which races are moments (rules fixed here, not chosen race by race):
  FIRST_RACE  race_index 1 in races.csv: the first World Championship Grand Prix.
  LEADER      every change of all-time leader. The leader is the driver ranked first on the
              board: most wins, ties to whoever reached the total first (DEC-012). From
              record_progression.csv: the leader changes when a driver other than the current
              leader BECOMES_SOLE record holder (a BECOMES_JOINT never changes the leader under
              the tie rule). Race 1 (the first leader) is FIRST_RACE, not a change.
  EQUALS      a driver equals the record (BECOMES_JOINT) and his next record row is taking the
              lead (LEADER): the "level, then ahead" moments (e.g. Hamilton 91 at the 2020 Eifel
              GP, then 92 and the lead at the next race).
  MILESTONE   the first driver to reach 50 and 100 wins (the record_progression row whose
              career_wins is that number; it is always BECOMES_SOLE or EXTENDS_SOLE).
  TOPTEN      the day each driver of today's top ten (topten_at_freeze.csv) entered the all-time
              top ten (topten_entries.csv, independently checked: 0 discrepancies).
  FREEZE      the last race in races.csv: the data freeze, stated on screen (metric contract).

Captions use only names, numbers and dates from these files, in fixed wording. Every moment is
re-derived from win_credits.csv alone (running counts, tie rule by credit_index) and the build
stops if the two ever disagree, so a caption can never say something the counts do not.

Deterministic, standard library only.
Usage: python scripts/rtt002_story.py [data/rtt-002] [reports/RTT-002_story_moments.md]
"""
import csv
import os
import sys

MILESTONES = (50, 100)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
FIELDS = ["moment", "kind", "race_index", "race_date", "season", "grand_prix", "driver_id", "driver_name",
          "career_wins", "caption_1", "caption_2", "caption_3", "source"]


def fail(msg):
    sys.exit("rtt002_story: ERROR: " + msg)


def read(d, name):
    with open(os.path.join(d, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def date_text(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, MONTHS[m - 1], y)


def gp_short(name):
    return name.replace("Grand Prix", "GP")


def wins(n):
    return "%d %s" % (n, "win" if n == 1 else "wins")


def recount(races, credits):
    """Board after every race from win_credits.csv alone: order (tie rule) and totals."""
    by_race = {}
    for c in credits:
        by_race.setdefault(c["race_index"], []).append(c)
    totals, reached, after = {}, {}, {}
    for r in races:
        for c in sorted(by_race.get(r["race_index"], []), key=lambda c: int(c["credit_index"])):
            totals[c["driver_id"]] = totals.get(c["driver_id"], 0) + 1
            if totals[c["driver_id"]] != int(c["career_wins_after"]):
                fail("win_credits.csv credit %s: career_wins_after does not add up" % c["credit_index"])
            reached[c["driver_id"]] = int(c["credit_index"])
        order = sorted(totals, key=lambda i: (-totals[i], reached[i]))
        after[r["race_index"]] = (order, dict(totals))
    return after


def build(d):
    races = read(d, "races.csv")
    credits = read(d, "win_credits.csv")
    names = {r["driver_id"]: r["display_name"] for r in read(d, "drivers.csv")}
    prog = read(d, "record_progression.csv")
    entries = read(d, "topten_entries.csv")
    freeze_top = read(d, "topten_at_freeze.csv")
    race_by_date = {}
    for r in races:
        if r["race_date"] in race_by_date:
            fail("two races on " + r["race_date"])
        race_by_date[r["race_date"]] = r
    after = recount(races, credits)
    pos = {r["race_index"]: i for i, r in enumerate(races)}

    def prev_board(r):
        i = pos[r["race_index"]]
        return after[races[i - 1]["race_index"]] if i else ([], {})

    out = []

    def add(kind, r, did, n, c1, c2, c3, source):
        out.append({"kind": kind, "race_index": r["race_index"], "race_date": r["race_date"], "season": r["season"],
                    "grand_prix": r["grand_prix"], "driver_id": did, "driver_name": names[did], "career_wins": n,
                    "caption_1": c1, "caption_2": c2, "caption_3": c3, "source": source})

    # FIRST_RACE
    first = races[0]
    fw = first["winner_driver_ids"].split(";")
    if len(fw) != 1:
        fail("the first race has a shared win")
    add("FIRST_RACE", first, fw[0], 1, "The first World Championship Grand Prix", "Won by " + names[fw[0]], "",
        "races.csv race_index 1; record_progression.csv row 1")

    # LEADER and EQUALS from record_progression.csv
    leader, leaders = None, []
    for i, p in enumerate(prog):
        r = race_by_date.get(p["race_date"])
        if r is None or r["grand_prix"] != p["grand_prix"]:
            fail("record_progression.csv row %d: no such race" % (i + 2))
        if p["event"] == "BECOMES_SOLE" and p["driver_id"] != leader:
            if leader is not None:
                leaders.append((i, p, r, leader))
            leader = p["driver_id"]
    for i, p, r, was in leaders:
        board = after[r["race_index"]]
        pb = prev_board(r)
        if board[0][0] != p["driver_id"] or pb[0][0] != was or board[1][p["driver_id"]] != int(p["career_wins"]):
            fail("leader change %s: record_progression.csv and the recount disagree" % p["race_date"])
        add("LEADER", r, p["driver_id"], int(p["career_wins"]), "New all-time leader",
            "%s · %s" % (names[p["driver_id"]], wins(int(p["career_wins"]))),
            "passes %s (%s)" % (names[was], wins(pb[1][was])),
            "record_progression.csv row %d (BECOMES_SOLE)" % (i + 2))
    lead_rows = {i for i, _, _, _ in leaders}
    for i, p in enumerate(prog):
        if p["event"] != "BECOMES_JOINT":
            continue
        nxt = next((j for j in range(i + 1, len(prog)) if prog[j]["driver_id"] == p["driver_id"]), None)
        if nxt is None or nxt not in lead_rows:
            continue
        r = race_by_date[p["race_date"]]
        others = [h.strip() for h in p["record_holders_after"].split(";") if h.strip() != p["driver_name"]]
        board = after[r["race_index"]]
        n = int(p["career_wins"])
        ids = [x for x in board[0] if board[1][x] == n]
        if board[1][p["driver_id"]] != n or sorted(names[x] for x in ids if x != p["driver_id"]) != sorted(others) or board[1][board[0][0]] != n:
            fail("record equalled %s: record_progression.csv and the recount disagree" % p["race_date"])
        add("EQUALS", r, p["driver_id"], n, "Record equalled", "%s · %s" % (names[p["driver_id"]], wins(n)),
            "level with " + " and ".join(others), "record_progression.csv row %d (BECOMES_JOINT)" % (i + 2))

    # MILESTONE
    for m in MILESTONES:
        rows = [(i, p) for i, p in enumerate(prog) if int(p["career_wins"]) == m]
        if len(rows) != 1 or rows[0][1]["event"] not in ("BECOMES_SOLE", "EXTENDS_SOLE"):
            fail("milestone %d: expected one sole record row" % m)
        i, p = rows[0]
        r = race_by_date[p["race_date"]]
        board = after[r["race_index"]]
        if board[1][p["driver_id"]] != m or any(v >= m for x, v in prev_board(r)[1].items()):
            fail("milestone %d: the recount disagrees" % m)
        add("MILESTONE", r, p["driver_id"], m, "First driver to %d wins" % m, names[p["driver_id"]], "",
            "record_progression.csv row %d (%s, career_wins %d)" % (i + 2, p["event"], m))

    # TOPTEN: today's top ten, the day each entered the all-time top ten
    now_top = {t["driver_id"] for t in freeze_top}
    last_order = after[races[-1]["race_index"]][0][:10]
    if set(last_order) != now_top or len(now_top) != 10:
        fail("topten_at_freeze.csv and the recount disagree")
    seen = set()
    for i, e in enumerate(entries):
        if e["driver_id"] not in now_top:
            continue
        if e["driver_id"] in seen:
            fail("%s enters the top ten twice in topten_entries.csv" % e["driver_name"])
        seen.add(e["driver_id"])
        r = race_by_date[e["race_date"]]
        board, pb = after[r["race_index"]], prev_board(r)
        n = int(e["career_wins"])
        if e["driver_id"] not in board[0][:10] or e["driver_id"] in pb[0][:10] or board[1][e["driver_id"]] != n \
                or board[0].index(e["driver_id"]) + 1 != int(e["position_entered"]):
            fail("top-ten entry %s %s: topten_entries.csv and the recount disagree" % (e["driver_name"], e["race_date"]))
        add("TOPTEN", r, e["driver_id"], n, "Into the all-time top ten", "%s · %s" % (names[e["driver_id"]], wins(n)), "",
            "topten_entries.csv row %d" % (i + 2))
    if seen != now_top:
        fail("not every driver of today's top ten has an entry row")

    # FREEZE
    last = races[-1]
    lw = last["winner_driver_ids"].split(";")[0]
    add("FREEZE", last, lw, after[last["race_index"]][1][lw], "Standings at the data freeze",
        "%s %s · %s" % (last["season"], gp_short(last["grand_prix"]), date_text(last["race_date"])), "",
        "races.csv race_index %s (last row); data/rtt-002/README.md freeze" % last["race_index"])

    out.sort(key=lambda m: int(m["race_index"]))
    for a, b in zip(out, out[1:]):
        if a["race_index"] == b["race_index"]:
            fail("two moments on race %s (%s, %s)" % (a["race_index"], a["kind"], b["kind"]))
    for i, m in enumerate(out):
        m["moment"] = i + 1
    return out


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "data/rtt-002"
    rep = sys.argv[2] if len(sys.argv) > 2 else "reports/RTT-002_story_moments.md"
    rows = build(d)
    with open(os.path.join(d, "story_moments.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    L = ["# RTT-002 story moments (full film)", "",
         "Written by `scripts/rtt002_story.py` from the audited files in `data/rtt-002/` (none changed); "
         "the same rows are in `data/rtt-002/story_moments.csv`, which the player reads for its captions. "
         "Every moment is re-derived from `win_credits.csv` alone and the build stops on any disagreement. "
         "The tests (`tests/player/run_tests.js`, case `rtt002_film`) check every caption as drawn against these files.", "",
         "Rules: every change of all-time leader; a record equalled on the way to taking the lead; the first driver to 50 and to 100 wins; the day each driver of today's top ten "
         "entered the all-time top ten; the first race and the data freeze. Nothing else is captioned.", "",
         "| # | Kind | Date | Grand Prix | Caption | Source |", "|---|---|---|---|---|---|"]
    for m in rows:
        cap = " / ".join(x for x in (m["caption_1"], m["caption_2"], m["caption_3"]) if x)
        L.append("| %d | %s | %s | %s %s | %s | %s |" % (m["moment"], m["kind"], date_text(m["race_date"]), m["season"],
                                                        m["grand_prix"], cap, m["source"]))
    os.makedirs(os.path.dirname(rep), exist_ok=True)
    with open(rep, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("%d story moments -> %s, %s" % (len(rows), os.path.join(d, "story_moments.csv"), rep))


if __name__ == "__main__":
    main()
