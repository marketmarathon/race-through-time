#!/usr/bin/env python3
"""Validate the RTT-002 independent check (ChatGPT deep research output).

The check file itself is PRIVATE and is never committed to this public repo.
This script only reads it and prints/writes a summary of structural and
internal-consistency checks plus the SHA-256 of the file, so the check can be
frozen in state/.

Usage:
    python scripts/validate_independent_check.py <path-to-zip> <out.json>

Checks (per HANDOVER / LAPTOP_SESSION_01 step 4):
  1. Sections A-G present.
  2. Every row of every section CSV has a non-empty source_url.
  3. Every NOT FOUND item listed.
  4. Internal consistency:
     a. Each season's wins in B add up to its rounds, allowing for shared drives.
     b. B totalled per driver matches F (drivers with >= 10 wins).
     c. The G seasons match B (race count and per-driver wins).
     Extra: B summary vs B normalised; D vs B shared wins; E recomputed from
     the race-level file; A vs 2026 rounds; README checksums.
Standard library only.
"""
import csv
import hashlib
import io
import json
import sys
import zipfile
from collections import Counter, defaultdict

SECTION_FILES = {
    "A": "A_data_freeze.csv",
    "B": "B_season_summary.csv",
    "B_norm": "B_season_driver_normalized.csv",
    "C": "C_indianapolis_1950_1960.csv",
    "D": "D_shared_wins.csv",
    "E": "E_wins_record_progression.csv",
    "F": "F_career_wins_10_plus.csv",
    "G": "G_selected_seasons_race_winners.csv",
}
RACE_LEVEL = "full_race_level_reconstruction_1950_2026.csv"


def read_csv(z, name):
    text = z.read(name).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def main(zip_path, out_path):
    raw = open(zip_path, "rb").read()
    result = {
        "file": zip_path.replace("\\", "/").split("/")[-1],
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "checks": {},
        "not_found": [],
        "problems": [],
    }
    z = zipfile.ZipFile(io.BytesIO(raw))
    names = set(z.namelist())
    result["members"] = {n: hashlib.sha256(z.read(n)).hexdigest() for n in sorted(names)}

    # 1. sections present
    missing = [k for k, f in SECTION_FILES.items() if f not in names]
    result["checks"]["sections_A_to_G_present"] = {"pass": not missing, "missing": missing}
    data = {k: read_csv(z, f) for k, f in SECTION_FILES.items() if f in names}
    races = read_csv(z, RACE_LEVEL) if RACE_LEVEL in names else []

    # 2. source_url on every row
    no_url = []
    for k, rows in list(data.items()) + [("race_level", races)]:
        for i, r in enumerate(rows, start=2):
            if not (r.get("source_url") or "").strip():
                no_url.append(f"{k} line {i}")
    result["checks"]["every_row_has_source_url"] = {
        "pass": not no_url, "rows_checked": sum(len(v) for v in data.values()) + len(races),
        "rows_missing": no_url}

    # 3. NOT FOUND items
    for k, rows in list(data.items()) + [("race_level", races)]:
        for i, r in enumerate(rows, start=2):
            for col, val in r.items():
                if val and "NOT FOUND" in val.upper():
                    ident = "; ".join(f"{c}={r[c]}" for c in list(r)[:4])
                    result["not_found"].append({"section": k, "line": i, "column": col, "row": ident})
    result["checks"]["not_found_count"] = len(result["not_found"])

    # parse B summary
    b_rounds, b_wins, b_shared = {}, defaultdict(Counter), defaultdict(int)
    for r in data.get("B", []):
        s = int(r["season"])
        b_rounds[s] = int(r["championship_rounds"])
        for part in r["wins_by_driver"].split(";"):
            part = part.strip()
            if part:
                d, n = part.rsplit("=", 1)
                b_wins[s][d.strip()] += int(n)
        sw = r["shared_wins"].strip()
        if sw and sw.upper() != "NONE":
            b_shared[s] = len([x for x in sw.split("|") if x.strip()])

    # 4a. wins add up to rounds + shared
    bad = []
    for s in sorted(b_rounds):
        total = sum(b_wins[s].values())
        if total != b_rounds[s] + b_shared[s]:
            bad.append({"season": s, "rounds": b_rounds[s], "shared": b_shared[s], "win_credits": total})
    result["checks"]["B_wins_equal_rounds_plus_shared"] = {"pass": not bad, "seasons": len(b_rounds), "failures": bad}

    # B summary vs normalised
    norm = defaultdict(Counter)
    for r in data.get("B_norm", []):
        norm[int(r["season"])][r["driver"].strip()] += int(r["wins"])
    diff = [s for s in set(norm) | set(b_wins) if norm[s] != b_wins[s]]
    result["checks"]["B_summary_equals_B_normalised"] = {"pass": not diff, "differing_seasons": sorted(diff)}

    # 4b. B per driver vs F
    career = Counter()
    for s in b_wins:
        career.update(b_wins[s])
    f = {r["driver"].strip(): int(r["career_wins"]) for r in data.get("F", [])}
    b10 = {d: n for d, n in career.items() if n >= 10}
    mism = [{"driver": d, "B_total": career.get(d), "F": f.get(d)}
            for d in sorted(set(f) | set(b10)) if career.get(d) != f.get(d)]
    result["checks"]["B_totals_match_F"] = {"pass": not mism, "drivers_in_F": len(f), "drivers_10plus_in_B": len(b10), "mismatches": mism}

    # 4c. G seasons vs B
    g_count, g_wins = Counter(), defaultdict(Counter)
    for r in data.get("G", []):
        s = int(r["season"])
        g_count[s] += 1
        for d in r["winner"].split(";"):
            g_wins[s][d.strip()] += 1
    gbad = []
    for s in sorted(g_count):
        if g_count[s] != b_rounds.get(s) or g_wins[s] != b_wins.get(s):
            gbad.append({"season": s, "G_races": g_count[s], "B_rounds": b_rounds.get(s),
                         "only_in_G": dict(g_wins[s] - b_wins.get(s, Counter())),
                         "only_in_B": dict(b_wins.get(s, Counter()) - g_wins[s])})
    result["checks"]["G_matches_B"] = {"pass": not gbad, "seasons": sorted(g_count), "failures": gbad}

    # D vs B shared
    d_by_season = Counter(int(r["race_date"][:4]) for r in data.get("D", []))
    result["checks"]["D_matches_B_shared"] = {"pass": dict(d_by_season) == {k: v for k, v in b_shared.items() if v},
                                              "D": dict(d_by_season), "B": {k: v for k, v in b_shared.items() if v}}

    # race level vs B, and E recomputed
    rl = defaultdict(Counter)
    rl_rounds = Counter()
    ordered = []
    for r in races:
        s = int(r["season"])
        rl_rounds[s] += 1
        winners = [w.strip() for w in r["credited_winners"].split(";") if w.strip()]
        for w in winners:
            rl[s][w] += 1
        ordered.append((r["race_date"], int(r["round"]), r["race"], winners))
    rlbad = [s for s in set(rl) | set(b_wins) if rl[s] != b_wins[s] or rl_rounds[s] != b_rounds.get(s)]
    result["checks"]["race_level_matches_B"] = {"pass": not rlbad, "differing_seasons": sorted(rlbad)}

    ordered.sort(key=lambda x: (x[0], x[1]))
    tally, record, holders, events = Counter(), 0, set(), []
    for date, rnd, race, winners in ordered:
        for w in winners:
            tally[w] += 1
            n = tally[w]
            if n > record:
                ev = "EXTENDS_SOLE" if holders == {w} else "BECOMES_SOLE"
                record, holders = n, {w}
                events.append((date, race, w, n, ev))
            elif n == record:
                holders = holders | {w}
                events.append((date, race, w, n, "BECOMES_JOINT"))
    e_rows = [(r["race_date"], r["race"], r["driver"].strip(), int(r["career_wins"]), r["event"].strip())
              for r in data.get("E", [])]
    e_diff = [list(x) for x in set(events) ^ set(e_rows)]
    result["checks"]["E_matches_recomputed_progression"] = {
        "pass": not e_diff, "E_rows": len(e_rows), "recomputed": len(events), "differences": sorted(e_diff)[:40]}

    # A vs 2026
    a = data.get("A", [{}])[0]
    result["freeze"] = {k: a.get(k) for k in ("freeze_race", "race_date", "winner", "completed_2026_rounds")}
    result["checks"]["A_rounds_match_B_2026"] = {
        "pass": str(b_rounds.get(2026)) == str(a.get("completed_2026_rounds")),
        "A": a.get("completed_2026_rounds"), "B_2026": b_rounds.get(2026)}

    result["summary"] = {
        "seasons": len(b_rounds), "championship_rounds": sum(b_rounds.values()),
        "win_credits": sum(career.values()), "distinct_winners": len(career),
        "shared_wins": sum(b_shared.values()), "drivers_10_plus": len(b10)}
    result["all_structural_and_consistency_checks_pass"] = all(
        v.get("pass", True) for v in result["checks"].values() if isinstance(v, dict))
    json.dump(result, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(json.dumps({k: (v["pass"] if isinstance(v, dict) and "pass" in v else v)
                      for k, v in result["checks"].items()}, indent=1))
    print("summary", result["summary"])
    print("ALL PASS" if result["all_structural_and_consistency_checks_pass"] else "SOME CHECKS FAILED")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
