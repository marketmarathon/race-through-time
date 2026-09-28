#!/usr/bin/env python3
"""Build the RTT-002 dataset (F1 World Championship Grand Prix wins, 1950 -> freeze).

Metric contract: reference/metric_contract_RTT-002.md (v0.2).
Source: English Wikipedia season pages (CC BY-SA 4.0), extracted to
data/rtt-002/source/ with page title, revision ID and retrieval time per season.
Standard library only. Deterministic: same source files -> same outputs.

Usage:  python scripts/build_rtt002_dataset.py [data/rtt-002]

Outputs (all counts are whole numbers; nothing is interpolated):
  races.csv                 one row per completed championship race, with provenance
  win_credits.csv           one row per driver credited with a win (shared drives -> 2 rows)
  cumulative_wins_wide.csv  race-by-race cumulative wins, one column per driver
  career_totals.csv         wins per driver at the freeze, ranked (tie -> reached total first)
  record_progression.csv    every time a driver became/extended/equalled the all-time record
  drivers.csv               stable driver IDs (Wikipedia page ID), titles and display names
  checks.json / CHECKS.md   scripted structural, semantic and cross-page checks
  manifest.json             inputs, outputs and their SHA-256 hashes
"""
import csv
import datetime as dt
import hashlib
import io
import json
import os
import sys
from collections import Counter, defaultdict

BUILD_VERSION = "rtt002-build/1.0"
MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], start=1)}
WIKI = "https://en.wikipedia.org/wiki/"
PERMA = "https://en.wikipedia.org/w/index.php?oldid="


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def read_lines(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().split("\n")


def load(src):
    pages, races = {}, []
    for ln in read_lines(os.path.join(src, "wikipedia_season_extract.psv")):
        if not ln:
            continue
        if ln.startswith("#"):
            y, title, rev, at = ln[1:].split("|")
            pages[int(y)] = {"title": title, "revid": int(rev), "retrieved_utc": at}
            continue
        f = ln.split("|")
        f += [""] * (8 - len(f))
        season, rnd, date_text, race_article, winners, gp_override, cell_diff, cal_gp = f[:8]
        drivers = []
        for w in [w for w in winners.split(";") if w]:
            target, _, text = w.partition("~")
            drivers.append((target, text or target.replace("_", " ")))
        # Display name comes from the race article title minus its year prefix
        # (e.g. "1950_British_Grand_Prix" -> "British Grand Prix"). Table cell
        # text is kept only as a note because it can carry footnote markers.
        art = race_article.replace("_", " ")
        gp = art.split(" ", 1)[1] if art[:4].isdigit() and " " in art else (art or gp_override or cal_gp)
        races.append({"season": int(season), "round": int(rnd), "date_text": date_text,
                      "race_article": race_article, "grand_prix": gp, "drivers": drivers,
                      "note_cell_text": cell_diff, "calendar_name": cal_gp})
    ids = {}
    for ln in read_lines(os.path.join(src, "wikipedia_driver_ids.psv")):
        if ln:
            target, canon, pageid = ln.split("|")
            ids[target] = (canon, int(pageid))
    lst = {}
    for ln in read_lines(os.path.join(src, "wikipedia_list_of_gp_winners.psv")):
        if ln:
            canon, wins, first, last = ln.split("|")
            lst[canon] = {"wins": int(wins), "first": first, "last": last}
    return pages, races, ids, lst


def iso_date(season, text):
    day, month = text.split(" ")
    return dt.date(season, MONTHS[month], int(day))


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def main(out_dir):
    src = os.path.join(out_dir, "source")
    pages, races, ids, lst = load(src)
    checks, problems = {}, []

    # ---- structural checks -------------------------------------------------
    seen = set()
    for r in races:
        key = (r["season"], r["round"])
        if key in seen:
            problems.append(f"duplicate race {key}")
        seen.add(key)
        try:
            r["date"] = iso_date(r["season"], r["date_text"])
        except Exception:
            r["date"] = None
            problems.append(f"unparseable date {key} {r['date_text']!r}")
        for target, _ in r["drivers"]:
            if target not in ids:
                problems.append(f"driver link not resolved {key} {target}")
    by_season = defaultdict(list)
    for r in races:
        by_season[r["season"]].append(r)
    contiguous = all(sorted(x["round"] for x in v) == list(range(1, len(v) + 1)) for v in by_season.values())
    chrono = all(all(a["date"] < b["date"] for a, b in zip(sorted(v, key=lambda x: x["round"]),
                                                          sorted(v, key=lambda x: x["round"])[1:]))
                 for v in by_season.values())
    checks["seasons_present_1950_to_2026"] = sorted(by_season) == list(range(1950, 2027))
    checks["rounds_contiguous_per_season"] = contiguous
    checks["dates_increase_with_round"] = chrono
    checks["no_duplicate_races"] = not any(p.startswith("duplicate") for p in problems)
    checks["all_dates_parse"] = not any(p.startswith("unparseable") for p in problems)
    checks["all_winner_links_resolve"] = not any(p.startswith("driver link") for p in problems)

    # ---- freeze: last completed race --------------------------------------
    completed = [r for r in races if r["drivers"]]
    future = [r for r in races if not r["drivers"]]
    completed.sort(key=lambda r: (r["date"], r["round"]))
    freeze = completed[-1]
    today = dt.date(2026, 9, 28)
    checks["no_completed_race_after_build_date"] = all(r["date"] <= today for r in completed)
    checks["no_winner_gap_before_freeze"] = all(r["date"] > freeze["date"] for r in future)
    checks["future_rounds_without_winner"] = [f"{r['season']} R{r['round']} {r['grand_prix']} ({r['date']})" for r in future]

    # ---- identities ---------------------------------------------------------
    def did(target):
        canon, pageid = ids[target]
        return f"wp{pageid}", canon

    names = defaultdict(Counter)
    for r in completed:
        for target, text in r["drivers"]:
            names[did(target)][text] += 1
    drivers = {}
    for (d, canon), c in names.items():
        drivers[d] = {"driver_id": d, "wikipedia_title": canon, "display_name": c.most_common(1)[0][0],
                      "name_variants": sorted(c)}
    checks["driver_link_targets"] = len(ids)
    checks["distinct_drivers_after_redirects"] = len(drivers)
    checks["redirect_merges"] = [f"{t} -> {c}" for t, (c, _) in ids.items() if t != c]

    # ---- per-race rows and win credits -------------------------------------
    race_rows, credits = [], []
    for i, r in enumerate(completed, start=1):
        p = pages[r["season"]]
        prov = [p["title"], WIKI + p["title"].replace(" ", "_"), p["revid"], PERMA + str(p["revid"]), p["retrieved_utc"]]
        ds = [did(t) for t, _ in r["drivers"]]
        race_rows.append([i, r["season"], r["round"], r["date"].isoformat(), r["grand_prix"], r["race_article"],
                          ";".join(d for d, _ in ds), ";".join(drivers[d]["display_name"] for d, _ in ds),
                          "yes" if len(ds) > 1 else "no", *prov])
        for d, _ in ds:
            credits.append((i, r, d, len(ds) > 1, prov))

    # ---- semantic checks ----------------------------------------------------
    per_season_credits = Counter(r["season"] for _, r, _, _, _ in credits)
    per_season_races = Counter(r["season"] for r in completed)
    per_season_shared = Counter(r["season"] for r in completed if len(r["drivers"]) > 1)
    bad = [s for s in per_season_races
           if per_season_credits[s] != per_season_races[s] + per_season_shared[s]]
    checks["wins_equal_races_plus_shared_every_season"] = not bad
    checks["shared_wins"] = [f"{r['season']} {r['grand_prix']} ({r['date']}): " + " + ".join(
        drivers[did(t)[0]]["display_name"] for t, _ in r["drivers"]) for r in completed if len(r["drivers"]) > 1]
    indy = [r for r in completed if "Indianapolis_500" in r["race_article"]]
    checks["indianapolis_500_rounds_included"] = f"{len(indy)} ({min(x['season'] for x in indy)}-{max(x['season'] for x in indy)})"

    # cumulative, record progression, totals
    tally = Counter()
    first_reach = {}
    record, holders = 0, set()
    progression, credit_rows = [], []
    cum_by_race = []
    last_idx = 0
    for n, (i, r, d, shared, prov) in enumerate(credits, start=1):
        tally[d] += 1
        k = tally[d]
        first_reach[(d, k)] = (i, n)
        credit_rows.append([n, i, r["season"], r["round"], r["date"].isoformat(), r["grand_prix"], d,
                            drivers[d]["display_name"], "yes" if shared else "no", k, *prov])
        if k > record:
            event = "EXTENDS_SOLE" if holders == {d} else "BECOMES_SOLE"
            record, holders = k, {d}
            progression.append([r["date"].isoformat(), r["season"], r["round"], r["grand_prix"], d,
                                drivers[d]["display_name"], k, event, drivers[d]["display_name"]])
        elif k == record:
            holders = holders | {d}
            progression.append([r["date"].isoformat(), r["season"], r["round"], r["grand_prix"], d,
                                drivers[d]["display_name"], k, "BECOMES_JOINT",
                                "; ".join(sorted(drivers[h]["display_name"] for h in holders))])
        if i != last_idx:
            last_idx = i
    # wide cumulative table, drivers ordered by first win
    order = sorted(drivers, key=lambda d: first_reach[(d, 1)])
    running = Counter()
    wide = []
    for i, r in enumerate(completed, start=1):
        for t, _ in r["drivers"]:
            running[did(t)[0]] += 1
        wide.append([i, r["season"], r["round"], r["date"].isoformat(), r["grand_prix"]] + [running[d] for d in order])
    checks["cumulative_monotonic_integers"] = all(
        all(isinstance(v, int) for v in row[5:]) for row in wide) and all(
        all(b >= a for a, b in zip(wide[j][5:], wide[j + 1][5:])) for j in range(len(wide) - 1))
    checks["final_cumulative_equals_totals"] = dict(zip(order, wide[-1][5:])) == {d: tally[d] for d in order}

    ranked = sorted(tally, key=lambda d: (-tally[d], first_reach[(d, tally[d])]))
    totals = []
    for pos, d in enumerate(ranked, start=1):
        first_i = first_reach[(d, 1)][0]
        last_i = first_reach[(d, tally[d])][0]
        fr, lr = completed[first_i - 1], completed[last_i - 1]
        totals.append([pos, d, drivers[d]["display_name"], tally[d],
                       f"{fr['season']} {fr['grand_prix']}", fr["date"].isoformat(),
                       f"{lr['season']} {lr['grand_prix']}", lr["date"].isoformat()])

    # ---- cross-page check: Wikipedia "List of Formula One Grand Prix winners"
    mism = []
    for d in drivers:
        canon = drivers[d]["wikipedia_title"]
        lw = lst.get(canon)
        if lw is None or lw["wins"] != tally[d]:
            mism.append({"driver": canon, "season_pages": tally[d], "list_page": lw["wins"] if lw else None})
    extra = [c for c in lst if c not in {v["wikipedia_title"] for v in drivers.values()}]
    checks["career_totals_match_wikipedia_list_page"] = not mism and not extra
    checks["career_totals_list_page_mismatches"] = mism
    checks["list_page_drivers_not_in_build"] = extra
    top20 = ranked[:20]
    checks["top20_match_list_page"] = all(lst.get(drivers[d]["wikipedia_title"], {}).get("wins") == tally[d] for d in top20)

    summary = {
        "seasons": len(by_season), "championship_races_completed": len(completed),
        "win_credits": len(credits), "distinct_winners": len(drivers),
        "shared_wins": sum(per_season_shared.values()), "drivers_10_plus": sum(1 for d in tally if tally[d] >= 10),
        "record_events": len(progression),
        "holder_change_events": sum(1 for p in progression if p[7] == "BECOMES_SOLE"),
        "freeze_race": f"{freeze['season']} {freeze['grand_prix']}", "freeze_date": freeze["date"].isoformat(),
        "freeze_winner": "; ".join(drivers[did(t)[0]]["display_name"] for t, _ in freeze["drivers"]),
        "completed_2026_rounds": per_season_races[2026],
    }

    # ---- write outputs ------------------------------------------------------
    prov_h = ["source_page", "source_page_url", "source_revision_id", "source_permanent_url", "retrieved_utc"]
    write_csv(os.path.join(out_dir, "races.csv"),
              ["race_index", "season", "round", "race_date", "grand_prix", "wikipedia_race_article",
               "winner_driver_ids", "winner_names", "shared_drive"] + prov_h, race_rows)
    write_csv(os.path.join(out_dir, "win_credits.csv"),
              ["credit_index", "race_index", "season", "round", "race_date", "grand_prix", "driver_id",
               "driver_name", "shared_drive", "career_wins_after"] + prov_h, credit_rows)
    write_csv(os.path.join(out_dir, "cumulative_wins_wide.csv"),
              ["race_index", "season", "round", "race_date", "grand_prix"] + [drivers[d]["display_name"] for d in order], wide)
    write_csv(os.path.join(out_dir, "career_totals.csv"),
              ["rank", "driver_id", "driver_name", "wins", "first_win", "first_win_date", "last_win", "last_win_date"], totals)
    write_csv(os.path.join(out_dir, "record_progression.csv"),
              ["race_date", "season", "round", "grand_prix", "driver_id", "driver_name", "career_wins", "event",
               "record_holders_after"], progression)
    write_csv(os.path.join(out_dir, "drivers.csv"),
              ["driver_id", "wikipedia_title", "wikipedia_url", "display_name", "name_variants_seen"],
              [[d, drivers[d]["wikipedia_title"], WIKI + drivers[d]["wikipedia_title"], drivers[d]["display_name"],
                "; ".join(drivers[d]["name_variants"])] for d in order])

    checks["problems"] = problems
    all_pass = all(v for k, v in checks.items() if isinstance(v, bool))
    checks_doc = {"build": BUILD_VERSION, "summary": summary, "checks": checks, "all_boolean_checks_pass": all_pass}
    json.dump(checks_doc, open(os.path.join(out_dir, "checks.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    md = ["# RTT-002 scripted checks", "", f"Build `{BUILD_VERSION}`. All boolean checks pass: **{all_pass}**.", "",
          "| Check | Result |", "|---|---|"]
    for k, v in checks.items():
        if isinstance(v, bool):
            md.append(f"| {k} | {'PASS' if v else 'FAIL'} |")
    md += ["", "## Summary", ""] + [f"- {k}: {v}" for k, v in summary.items()]
    md += ["", "## Notes", ""]
    for k in ("shared_wins", "indianapolis_500_rounds_included", "redirect_merges", "future_rounds_without_winner",
              "career_totals_list_page_mismatches", "list_page_drivers_not_in_build", "problems"):
        md.append(f"- **{k}**: {json.dumps(checks[k], ensure_ascii=False)}")
    open(os.path.join(out_dir, "CHECKS.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")

    outputs = ["races.csv", "win_credits.csv", "cumulative_wins_wide.csv", "career_totals.csv",
               "record_progression.csv", "drivers.csv", "checks.json", "CHECKS.md"]
    manifest = {
        "dataset": "RTT-002 F1 World Championship Grand Prix wins", "build": BUILD_VERSION,
        "metric_contract": "reference/metric_contract_RTT-002.md v0.2",
        "licence": "CC BY-SA 4.0 (derived from English Wikipedia); see ATTRIBUTION.md",
        "freeze": {"race": summary["freeze_race"], "date": summary["freeze_date"]},
        "inputs": {f"source/{n}": sha(os.path.join(src, n)) for n in sorted(os.listdir(src)) if n.endswith(".psv")},
        "wikipedia_pages": [{"season": y, **pages[y], "page_url": WIKI + pages[y]["title"].replace(" ", "_"),
                             "permanent_url": PERMA + str(pages[y]["revid"])} for y in sorted(pages)],
        "outputs": {n: sha(os.path.join(out_dir, n)) for n in outputs},
        "summary": summary,
    }
    json.dump(manifest, open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    print("ALL BOOLEAN CHECKS PASS" if all_pass else "SOME CHECKS FAILED")
    for k, v in checks.items():
        if isinstance(v, bool) and not v:
            print("FAIL", k)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "data/rtt-002"))
