#!/usr/bin/env python3
"""Write the IQ-04 stress fixtures for the RTT player (tests/fixtures/<name>/).

Every fixture is FICTIONAL: invented drivers ("Test Driver ...") and invented races on invented
dates, in the RTT-002 CSV layout (the columns scripts/rtt_adapter.py reads, nothing else). They
exist only to push the player into awkward shapes; they are not data and must never be shown
as data. Deterministic: running this again writes byte-identical files.

  long_names        very long display names, on a long bar and on a short one
  three_way_tie     three drivers level on the same count; the tie rule decides the order
  shared_drive      two winners credited at one event (both step at the same frame)
  enter_leave       a driver enters and then leaves the visible top N (rows = 5)
  quiet_stretch     a long run of events with no visible change, then a change
  short_opening     fewer entrants than rows for the whole opening

fixture.json in each folder gives the config overrides the test applies and what to expect.
Usage: python tests/fixtures/make_fixtures.py
"""
import csv
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def write(name, drivers, races, overrides, expect):
    """drivers: [(id, name)]; races: [(date, gp, [winner ids])]"""
    d = os.path.join(HERE, name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "drivers.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["driver_id", "display_name"])
        w.writerows(drivers)
    counts, credit = {}, 0
    rrows, crows = [], []
    season_round = {}
    for i, (date, gp, winners) in enumerate(races, 1):
        season = int(date[:4])
        season_round[season] = season_round.get(season, 0) + 1
        rrows.append([i, season, season_round[season], date, gp, ";".join(winners)])
        for wid in winners:
            credit += 1
            counts[wid] = counts.get(wid, 0) + 1
            crows.append([credit, i, wid, counts[wid]])
    with open(os.path.join(d, "races.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["race_index", "season", "round", "race_date", "grand_prix", "winner_driver_ids"])
        w.writerows(rrows)
    with open(os.path.join(d, "win_credits.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["credit_index", "race_index", "driver_id", "career_wins_after"])
        w.writerows(crows)
    with open(os.path.join(d, "fixture.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"fictional": True, "overrides": overrides, "expect": expect}, f, indent=1, sort_keys=True)
        f.write("\n")


def dates(start, n, step_days=14):
    d0 = dt.date.fromisoformat(start)
    return [(d0 + dt.timedelta(days=step_days * i)).isoformat() for i in range(n)]


def gp(i):
    return "Test Grand Prix %d" % i


def main():
    # 1. long names -----------------------------------------------------------------------
    drv = [("L1", "Wolfgang Bartholomäus von Hohenzollern-Sigmaringen-Oberstdorf der Jüngere"),
           ("L2", "Test Driver Short"),
           ("L3", "María de los Ángeles Fernández-Castellanos y Rodríguez de la Fuente"),
           ("L4", "Test Driver Two")]
    seq = ["L1"] * 9 + ["L2", "L2", "L3", "L4", "L1", "L3"]
    write("long_names", drv, [(d, gp(i + 1), [w]) for i, (d, w) in enumerate(zip(dates("2001-03-04", len(seq)), seq))],
          {"rows": 10},
          {"note": "the longest name must fit on the frame with its value label; one name size for the whole video"})

    # 2. three-way tie ----------------------------------------------------------------------
    drv = [("TA", "Test Driver Alpha"), ("TB", "Test Driver Bravo"), ("TC", "Test Driver Charlie"), ("TD", "Test Driver Delta")]
    seq = ["TC", "TA", "TB", "TA", "TC", "TB", "TD", "TD", "TD", "TA"]
    # after event 6: TA=2 (reached at credit 4), TC=2 (credit 5), TB=2 (credit 6) -> order TA, TC, TB
    write("three_way_tie", drv, [(d, gp(i + 1), [w]) for i, (d, w) in enumerate(zip(dates("2002-03-03", len(seq)), seq))],
          {"rows": 10},
          {"after_race": {"3": ["TC", "TA", "TB"], "6": ["TA", "TC", "TB"], "9": ["TD", "TA", "TC", "TB"], "10": ["TD", "TA", "TC", "TB"]}})

    # 3. shared drive -----------------------------------------------------------------------
    drv = [("SA", "Test Driver Anna"), ("SB", "Test Driver Ben"), ("SC", "Test Driver Cleo")]
    races = [("2003-04-06", gp(1), ["SC"]), ("2003-04-20", gp(2), ["SB"]),
             ("2003-05-04", gp(3), ["SA", "SB"]),       # shared drive: SA credit 3, SB credit 4
             ("2003-05-18", gp(4), ["SA"]), ("2003-06-01", gp(5), ["SC", "SA"])]
    write("shared_drive", drv, races, {"rows": 10},
          {"after_race": {"3": ["SB", "SC", "SA"], "4": ["SB", "SA", "SC"], "5": ["SA", "SB", "SC"]},
           "same_frame_step": 3})

    # 4. enter and leave the visible top N ------------------------------------------------------
    drv = [("E%d" % i, "Test Driver E%d" % i) for i in range(1, 9)]
    seq = ["E1", "E2", "E3", "E4", "E5", "E1", "E2", "E3", "E4", "E5",   # E1..E5 on 2 each
           "E6", "E6", "E6",                                            # E6 enters top 5 at 3
           "E7", "E7", "E7", "E7", "E8", "E8", "E8", "E8",               # E7, E8 pass E6 ...
           "E1", "E1", "E2", "E2", "E3", "E3"]                           # ... and E6 drops out
    write("enter_leave", drv, [(d, gp(i + 1), [w]) for i, (d, w) in enumerate(zip(dates("2004-02-29", len(seq), 10), seq))],
          {"rows": 5},
          {"enters": "E6", "leaves": "E6", "rows": 5})

    # 5. long quiet stretch -------------------------------------------------------------------
    drv = [("Q%d" % i, "Test Driver Q%d" % i) for i in range(1, 31)]
    seq = ["Q%d" % i for i in range(1, 11)] * 2                 # a board of 10, two wins each
    seq += ["Q%d" % i for i in range(11, 31)]                   # 20 single wins nobody can see
    seq += ["Q1"] * 12                                          # then Q1 alone: settles, compresses
    seq += ["Q2"] * 5                                           # and a change at the end
    ds = dates("2005-03-06", 30) + dates("2009-04-05", len(seq) - 30)   # with a 3-year gap
    write("quiet_stretch", drv, [(d, gp(i + 1), [w]) for i, (d, w) in enumerate(zip(ds, seq))],
          {"rows": 10},
          {"note": "races 21-40 are won by drivers who stay off a 10-row board; they and the later settled run take pacing.mult.quiet",
           "quiet_from_race": 21, "quiet_to_race": 40})

    # 6. opening with fewer than N entrants ------------------------------------------------------
    drv = [("F1x", "Test Driver Foxtrot"), ("F2x", "Test Driver Golf"), ("F3x", "Test Driver Hotel")]
    seq = ["F1x", "F1x", "F2x", "F1x", "F3x", "F2x"]
    write("short_opening", drv, [(d, gp(i + 1), [w]) for i, (d, w) in enumerate(zip(dates("2006-03-12", len(seq)), seq))],
          {"rows": 10},
          {"max_visible": 3})


if __name__ == "__main__":
    main()
