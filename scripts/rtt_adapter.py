#!/usr/bin/env python3
"""RTT adapter: an RTT event dataset -> the input file the RTT player reads (IQ-04).

Reads three CSVs in the RTT-002 layout (data/rtt-002/README.md):
  races.csv        race_index, season, round, race_date, grand_prix, winner_driver_ids
  win_credits.csv  credit_index, race_index, driver_id, career_wins_after
  drivers.csv      driver_id, display_name
and, when present (IQ-05e, DEC-053), a fourth:
  starts.csv       start_index, race_index, driver_id, career_starts_after
Extra columns (provenance and so on) are ignored. Test fixtures under tests/fixtures/ use the
same files with only these columns.

Writes one JSON file, schema "rtt-race/1":
  entrants  [{id, label}]                          in drivers.csv order (stable colours)
  events    [{race_index, season, round, date, grand_prix,
              credits: [{id, total, credit_index}],
              starts:  [{id, total}]}]            in race order; "starts" only with starts.csv
                                                  (every driver who started that race, with the
                                                  career starts the data gives after it)
Every total is copied from win_credits.csv (career_wins_after) after checking it equals the
running count of credits. Nothing is interpolated, smoothed or filled in: a race with no
credit, a credit with no race, a driver with no display name, a non-integer or a count that
does not add up stops the adapter with an error. With starts.csv the same holds for starts, and
every credited winner must have a start at the race they won.

Deterministic: sorted keys, fixed separators, no timestamps. The SHA-256 of the output is
printed and, with --hash-file, written next to the input hashes.

Usage:
  python scripts/rtt_adapter.py IN_DIR OUT_JSON [--dataset-id ID] [--hash-file PATH]
Standard library only.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys

SCHEMA = "rtt-race/1"
ADAPTER_VERSION = "rtt-adapter/1.1"   # 1.1 (IQ-05e): optional starts.csv -> events[].starts
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(msg):
    sys.exit("rtt_adapter: ERROR: " + msg)


def read_csv(path, need):
    if not os.path.isfile(path):
        fail("missing " + path)
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        fail(path + " has no rows")
    missing = [c for c in need if c not in rows[0]]
    if missing:
        fail(path + " lacks column(s) " + ", ".join(missing))
    return rows


def whole(value, what):
    if not re.fullmatch(r"\d+", value or ""):
        fail(what + " is not a whole number: " + repr(value))
    return int(value)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def build(in_dir):
    races = read_csv(os.path.join(in_dir, "races.csv"),
                     ["race_index", "season", "round", "race_date", "grand_prix", "winner_driver_ids"])
    credits = read_csv(os.path.join(in_dir, "win_credits.csv"),
                       ["credit_index", "race_index", "driver_id", "career_wins_after"])
    drivers = read_csv(os.path.join(in_dir, "drivers.csv"), ["driver_id", "display_name"])

    entrants, known = [], set()
    for d in drivers:
        did, name = d["driver_id"].strip(), d["display_name"].strip()
        if not did or not name:
            fail("drivers.csv row with an empty id or display_name: " + repr(d))
        if did in known:
            fail("duplicate driver_id in drivers.csv: " + did)
        known.add(did)
        entrants.append({"id": did, "label": name})

    events, by_race = [], {}
    last_index, last_date = 0, ""
    for r in races:
        ri = whole(r["race_index"], "race_index")
        if ri != last_index + 1:
            fail("race_index not consecutive from 1 at " + str(ri))
        date = r["race_date"].strip()
        if not DATE_RE.match(date):
            fail("race %d: race_date %r is not YYYY-MM-DD" % (ri, date))
        if date < last_date:
            fail("race %d: date %s is earlier than the race before" % (ri, date))
        last_index, last_date = ri, date
        ev = {"race_index": ri, "season": whole(r["season"], "season"),
              "round": whole(r["round"], "round"), "date": date,
              "grand_prix": r["grand_prix"].strip(), "credits": [],
              "_winners": [w for w in r["winner_driver_ids"].split(";") if w.strip()]}
        if not ev["grand_prix"]:
            fail("race %d has no grand_prix name" % ri)
        events.append(ev)
        by_race[ri] = ev

    running, last_ci = {}, 0
    for c in credits:
        ci = whole(c["credit_index"], "credit_index")
        if ci != last_ci + 1:
            fail("credit_index not consecutive from 1 at " + str(ci))
        last_ci = ci
        ri = whole(c["race_index"], "race_index")
        did = c["driver_id"].strip()
        if ri not in by_race:
            fail("credit %d names race %d, which is not in races.csv" % (ci, ri))
        if did not in known:
            fail("credit %d names driver %s, who is not in drivers.csv" % (ci, did))
        total = whole(c["career_wins_after"], "career_wins_after")
        running[did] = running.get(did, 0) + 1
        if total != running[did]:
            fail("credit %d: career_wins_after %d but %d credits counted for %s"
                 % (ci, total, running[did], did))
        by_race[ri]["credits"].append({"id": did, "total": total, "credit_index": ci})

    for ev in events:
        got = [c["id"] for c in ev["credits"]]
        want = [w.strip() for w in ev.pop("_winners")]
        if not got:
            fail("race %d (%s %s) has no win credit" % (ev["race_index"], ev["season"], ev["grand_prix"]))
        if sorted(got) != sorted(want):
            fail("race %d: credits %s do not match winner_driver_ids %s" % (ev["race_index"], got, want))

    starts_path = os.path.join(in_dir, "starts.csv")
    has_starts = os.path.isfile(starts_path)
    if has_starts:
        for ev in events:
            ev["starts"] = []
        srows = read_csv(starts_path, ["start_index", "race_index", "driver_id", "career_starts_after"])
        sran, last_si, seen = {}, 0, set()
        for srow in srows:
            si = whole(srow["start_index"], "start_index")
            if si != last_si + 1:
                fail("start_index not consecutive from 1 at " + str(si))
            last_si = si
            ri = whole(srow["race_index"], "race_index")
            did = srow["driver_id"].strip()
            if ri not in by_race:
                fail("start %d names race %d, which is not in races.csv" % (si, ri))
            if did not in known:
                fail("start %d names driver %s, who is not in drivers.csv" % (si, did))
            if (ri, did) in seen:
                fail("start %d: %s has two starts at race %d" % (si, did, ri))
            seen.add((ri, did))
            total = whole(srow["career_starts_after"], "career_starts_after")
            sran[did] = sran.get(did, 0) + 1
            if total != sran[did]:
                fail("start %d: career_starts_after %d but %d starts counted for %s" % (si, total, sran[did], did))
            by_race[ri]["starts"].append({"id": did, "total": total})
        order = [s2["race_index"] for s2 in srows]
        if [int(x) for x in order] != sorted(int(x) for x in order):
            fail("starts.csv is not in race order")
        for ev in events:
            started = {x["id"] for x in ev["starts"]}
            for c in ev["credits"]:
                if c["id"] not in started:
                    fail("race %d: winner %s has no start in starts.csv" % (ev["race_index"], c["id"]))

    counts = {"events": len(events), "credits": last_ci, "entrants": len(entrants)}
    if has_starts:
        counts["starts"] = last_si
    return {
        "schema": SCHEMA,
        "adapter": ADAPTER_VERSION,
        "entrants": entrants,
        "events": events,
        "counts": counts,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("in_dir")
    ap.add_argument("out_json")
    ap.add_argument("--dataset-id", default=None)
    ap.add_argument("--hash-file", default=None)
    a = ap.parse_args()

    out = build(a.in_dir)
    if a.dataset_id:
        out["dataset_id"] = a.dataset_id
    text = json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1, separators=(",", ": ")) + "\n"
    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    with open(a.out_json, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    digest = sha256_file(a.out_json)
    print("%s  %s  (%d events, %d credits, %d entrants%s)"
          % (digest, a.out_json, out["counts"]["events"], out["counts"]["credits"], out["counts"]["entrants"],
             ", %d starts" % out["counts"]["starts"] if "starts" in out["counts"] else ""))

    if a.hash_file:
        lines = ["# RTT player input - SHA-256 record (written by scripts/rtt_adapter.py; do not edit)",
                 "# adapter: " + ADAPTER_VERSION,
                 "# schema: " + SCHEMA]
        if a.dataset_id:
            lines.append("# dataset_id: " + a.dataset_id)
        for name in ("races.csv", "win_credits.csv", "drivers.csv", "starts.csv"):
            p = os.path.join(a.in_dir, name)
            if name == "starts.csv" and not os.path.isfile(p):
                continue
            lines.append("%s  input  %s" % (sha256_file(p), os.path.relpath(p).replace(os.sep, "/")))
        lines.append("%s  output %s" % (digest, os.path.relpath(a.out_json).replace(os.sep, "/")))
        with open(a.hash_file, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
