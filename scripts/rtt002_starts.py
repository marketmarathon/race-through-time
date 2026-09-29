#!/usr/bin/env python3
"""Build the RTT-002 race STARTS files (IQ-05 round 5, prompts/CODE_SESSION_IQ-05e.md; DEC-053).

Luke's decision (DEC-053): the text after every bar shows wins, starts and win rate,
"91 wins · 306 starts · 29.7%". Definition and rounding: reference/metric_contract_RTT-002.md,
"Display attributes".

Input (data/rtt-002/source/, extracted in Luke's Chrome by scripts/extract_starts.browser.js
because Wikimedia answers the cloud sandboxes with HTTP 429; see source/README.md):
  wikipedia_starts_extract.psv
    #season|<year>|<page>|<revision>|<retrieved>|<round headers separated by ;>
    S|<year>|<driver link title>|<one cell per round header>     (World Drivers' Championship table)
    #list_of_f1_drivers|<page>|<revision>|<retrieved>
    L|<driver link title>|<race entries>|<race starts>|<race wins>  ("List of Formula One drivers")
    #titles|link_title|canonical_title|pageid
    T|<link title>|<canonical title>|<page ID>
The audited dataset files races.csv, win_credits.csv, drivers.csv and career_totals.csv are only
read; nothing in them is changed.

Rules (DEC-053):
  - A driver has a START at a championship race when that season's Drivers' Championship table
    cell for that round shows a classified position (a number), Ret, NC or DSQ, including any
    part of a shared or swapped-car cell such as "2†/ Ret". DNS, DNQ, DNPQ, WD, EX, DNA, DNP or
    an empty cell is not a start. Any other value stops the build (nothing is guessed).
  - Before classifying: drop the "Race: …; Sprint: …" annotation (the race result is the first
    token), strip brackets and the marks † ‡ * ^ ~, split on "/", classify the first token of
    each part.
  - Columns with an empty header are dropped (1967-1979 tables have one separator column); the
    remaining round columns map to races.csv by order; for 2026 only the completed rounds (15).
  - The Indianapolis 500 of 1950-1960 counts (DEC-012). One start per driver per race even with
    several cars (several rows or several parts of one cell).
  - Rows match drivers through the T lines (driver_id = "wp" + page ID); the "Formula Two"
    separator rows are not drivers. Only the 116 drivers of drivers.csv are written (the video's
    universe); every other row must still resolve to a page ID.
  - Win rate = wins / starts after that race, a percentage with one decimal, rounded half up
    (decimal arithmetic, never binary floating point).

Outputs (data/rtt-002/; new files, standard library only, same inputs -> byte-identical files):
  starts.csv                 one row per driver (of drivers.csv) per started race, race order,
                             with the source cell and the driver's career starts after the race
  career_starts.csv          per driver at the freeze: wins, starts, win rate, first start, and
                             the "List of Formula One drivers" entries/starts for comparison
  starts_checks.json         scripted checks (the build stops if one fails, except the listed
  STARTS_CHECKS.md           disagreements with the List page, which are reported, never resolved)
  starts_manifest.json       input and output SHA-256 hashes, revisions

Usage: python scripts/rtt002_starts.py [data/rtt-002]
"""
import csv
import hashlib
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

BUILD_VERSION = "rtt002-starts/1.0"
SOURCE = "wikipedia_starts_extract.psv"
SOURCE_SHA256 = "b26c0ed439d09b247462343c176c48964951291ec7058d8f476ef65ecdac9b64"
EXTRACTOR = "scripts/extract_starts.browser.js"
EXTRACTOR_SHA256 = "ac8edfdb347fbf84a683ab570cbf14889797573afbf2127fac545034371d5845"
START = {"Ret", "NC", "DSQ"}                                   # plus any whole number
NOT_START = {"DNS", "DNQ", "DNPQ", "WD", "EX", "DNA", "DNP", ""}
MARKS = "()[]†‡*^~"
F2_ROW = "Formula Two"
PERMA = "https://en.wikipedia.org/w/index.php?oldid="
WIKI = "https://en.wikipedia.org/wiki/"
# the prototype results the build must reproduce exactly (prompts/CODE_SESSION_IQ-05e.md)
EXPECT_LIST_AGREE, EXPECT_LIST_DISAGREE = 115, {"Rubens Barrichello": (323, 322)}
# races named in the task as example candidates for a disagreement (reported, never acted on)
NAMED_CANDIDATES = {"Rubens Barrichello": ["2002 Spanish Grand Prix"]}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def csv_text(cols, rows):
    s = io.StringIO()
    w = csv.DictWriter(s, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return s.getvalue()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def win_rate(wins, starts):
    """wins / starts as a percentage with one decimal, rounded half up: '29.7'."""
    return str((Decimal(100 * wins) / Decimal(starts)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def win_rate_check(wins, starts):
    """The same number by exact fractions (independent of decimal's context): tenths of a percent,
    floor(x + 1/2) with x = 1000 * wins / starts."""
    t = Fraction(1000 * wins, starts) + Fraction(1, 2)
    t = t.numerator // t.denominator
    return "%d.%d" % (t // 10, t % 10)


def classify(cell):
    """-> (is_start, [tokens]). Raises ValueError on a value the rules do not name."""
    s = re.sub(r"\s*Race:.*$", "", cell)                        # "4 Race: 4; Sprint: 4" -> "4"
    for m in MARKS:
        s = s.replace(m, "")
    toks = []
    for part in s.split("/"):
        words = part.split()
        toks.append(words[0] if words else "")
    for t in toks:
        if not (t.isdigit() or t in START or t in NOT_START):
            raise ValueError("unclassified value %r (token %r)" % (cell, t))
    return any(t.isdigit() or t in START for t in toks), toks


def parse_source(path):
    seasons, rows, lst, titles = {}, defaultdict(list), [], {}
    list_meta, header = None, None
    for ln in open(path, encoding="utf-8").read().split("\n"):
        if not ln:
            continue
        p = ln.split("|")
        if p[0] == "#rtt002_starts_extract":
            header = p
        elif p[0] == "#season":
            y = int(p[1])
            if p[5] == "NOT FOUND":
                raise SystemExit("season %d: no Drivers' Championship table in the source" % y)
            seasons[y] = {"title": p[2], "revid": p[3], "retrieved": p[4], "headers": p[5].split(";")}
        elif p[0] == "#list_of_f1_drivers":
            list_meta = {"title": p[1], "revid": p[2], "retrieved": p[3]}
        elif p[0] == "#titles":
            pass
        elif p[0] == "S":
            y = int(p[1])
            if len(p) - 3 != len(seasons[y]["headers"]):
                raise SystemExit("season %d row %s: %d cells for %d headers" % (y, p[2], len(p) - 3, len(seasons[y]["headers"])))
            rows[y].append((p[2], p[3:]))
        elif p[0] == "L":
            lst.append({"link": p[1], "entries": p[2], "starts": p[3], "wins": p[4]})
        elif p[0] == "T":
            titles[p[1]] = (p[2], p[3])
        else:
            raise SystemExit("unexpected source line: " + ln[:80])
    return header, seasons, rows, lst, list_meta, titles


def iso(t):
    return t[:19] + "Z"


def build(data_dir):
    src = os.path.join(data_dir, "source", SOURCE)
    root = os.path.dirname(os.path.dirname(os.path.abspath(data_dir)))
    got = sha(src)
    if got != SOURCE_SHA256:
        raise SystemExit("%s: SHA-256 %s != %s (recorded in source/README.md)" % (SOURCE, got, SOURCE_SHA256))
    ext = os.path.join(root, EXTRACTOR)
    if os.path.exists(ext) and sha(ext) != EXTRACTOR_SHA256:
        raise SystemExit("%s: SHA-256 differs from %s" % (EXTRACTOR, EXTRACTOR_SHA256))
    header, seasons, srows, lst, list_meta, titles = parse_source(src)

    races = read_csv(os.path.join(data_dir, "races.csv"))
    credits = read_csv(os.path.join(data_dir, "win_credits.csv"))
    drivers = read_csv(os.path.join(data_dir, "drivers.csv"))
    totals = {r["driver_id"]: int(r["wins"]) for r in read_csv(os.path.join(data_dir, "career_totals.csv"))}
    name = {d["driver_id"]: d["display_name"] for d in drivers}
    order = [d["driver_id"] for d in drivers]
    known = set(order)
    by_season = defaultdict(list)
    for r in races:
        by_season[int(r["season"])].append(r)

    checks, notes, failures = {}, [], []

    def check(key, ok, detail=None):
        checks[key] = {"pass": bool(ok)}
        if detail is not None:
            checks[key]["detail"] = detail
        if not ok:
            failures.append(key)

    # 1. the same revisions as the wins data; round counts after dropping empty-header columns
    rev_bad, count_rows, count_bad, dropped = [], [], [], {}
    col_map = {}                                   # season -> [(column index, races.csv row)]
    for y in sorted(by_season):
        s = seasons.get(y)
        if s is None:
            raise SystemExit("season %d missing from the starts source" % y)
        if s["revid"] != by_season[y][0]["source_revision_id"]:
            rev_bad.append("%d: %s vs races.csv %s" % (y, s["revid"], by_season[y][0]["source_revision_id"]))
        keep = [i for i, h in enumerate(s["headers"]) if h.strip()]
        if len(keep) != len(s["headers"]):
            dropped[y] = len(s["headers"]) - len(keep)
        n_run = len(by_season[y])
        listed = len(keep)
        ok = listed == n_run if y != 2026 else (listed == 23 and n_run == 15)
        count_rows.append({"season": y, "columns": len(s["headers"]), "empty_header_dropped": dropped.get(y, 0),
                           "rounds_listed": listed, "races_csv": n_run})
        if not ok:
            count_bad.append("%d: %d round columns, races.csv %d" % (y, listed, n_run))
        col_map[y] = list(zip(keep[:n_run], sorted(by_season[y], key=lambda r: int(r["round"]))))
    if set(seasons) - set(by_season):
        rev_bad.append("extra seasons in source: %s" % sorted(set(seasons) - set(by_season)))
    check("same_revisions_as_wins_data", not rev_bad, rev_bad or "77 of 77 season pages at the revision races.csv records")
    check("round_count_equals_races_csv", not count_bad,
          count_bad or "every season after dropping empty-header columns (%s); 2026: 23 listed, 15 run"
          % ", ".join("%d: %d dropped" % (y, n) for y, n in sorted(dropped.items())))

    # 2. rows -> drivers; classify every cell
    unresolved, f2_rows, tok_count, bad_cells = [], 0, Counter(), []
    started = defaultdict(dict)                    # race_index -> driver_id -> [cells]
    driver_rows = Counter()
    for y in sorted(srows):
        for link, cells in srows[y]:
            if link == F2_ROW:
                f2_rows += 1
                continue
            t = titles.get(link)
            if not t or not t[1].isdigit():
                unresolved.append("%d %s" % (y, link))
                continue
            did = "wp" + t[1]
            for ci, race in col_map[y]:
                cell = cells[ci]
                try:
                    is_start, toks = classify(cell)
                except ValueError as e:
                    bad_cells.append("%d %s round %s: %s" % (y, link, race["round"], e))
                    continue
                for tk in toks:
                    tok_count["number" if tk.isdigit() else (tk or "(empty)")] += 1
                if is_start and did in known:
                    started[race["race_index"]].setdefault(did, []).append(cell)
            if did in known:
                driver_rows[(y, did)] += 1
    check("every_row_resolves_to_a_page_id", not unresolved,
          unresolved or "every driver row resolved through the T lines; %d 'Formula Two' separator rows skipped" % f2_rows)
    check("every_cell_classified", not bad_cells, bad_cells[:40] or dict(sorted(tok_count.items())))
    multi_rows = sorted("%d %s (%d rows)" % (y, name[d], n) for (y, d), n in driver_rows.items() if n > 1)
    multi_cells = sorted({"%s %s" % (ri, name[d]) for ri, m in started.items() for d, c in m.items() if len(c) > 1})

    # 3. starts.csv
    race_by_index = {r["race_index"]: r for r in races}
    s_meta = {y: seasons[y] for y in seasons}
    rows_out, running = [], Counter()
    first_start = {}
    for r in races:
        ri = r["race_index"]
        for did in order:
            if did not in started.get(ri, {}):
                continue
            running[did] += 1
            first_start.setdefault(did, r)
            s = s_meta[int(r["season"])]
            rows_out.append({
                "start_index": len(rows_out) + 1, "race_index": ri, "season": r["season"], "round": r["round"],
                "race_date": r["race_date"], "grand_prix": r["grand_prix"], "driver_id": did,
                "driver_name": name[did], "source_cells": " + ".join(started[ri][did]),
                "career_starts_after": running[did], "source_page": s["title"],
                "source_page_url": WIKI + s["title"].replace(" ", "_"), "source_revision_id": s["revid"],
                "source_permanent_url": PERMA + s["revid"], "retrieved_utc": iso(s["retrieved"])})
    starts_cols = ["start_index", "race_index", "season", "round", "race_date", "grand_prix", "driver_id",
                   "driver_name", "source_cells", "career_starts_after", "source_page", "source_page_url",
                   "source_revision_id", "source_permanent_url", "retrieved_utc"]

    # 4. every win credit's driver has a start at that race
    no_start = ["%s %s %s" % (c["season"], c["grand_prix"], c["driver_name"]) for c in credits
                if c["driver_id"] not in started.get(c["race_index"], {})]
    check("every_win_credit_has_a_start", not no_start, no_start or "%d of %d win credits" % (len(credits), len(credits)))
    check("every_driver_has_starts", all(running[d] > 0 for d in order),
          [name[d] for d in order if not running[d]] or "116 of 116 drivers")
    check("starts_at_least_wins", all(running[d] >= totals[d] for d in order),
          ["%s %d starts < %d wins" % (name[d], running[d], totals[d]) for d in order if running[d] < totals[d]] or "116 of 116 drivers")
    indy = [r for r in races if "Indianapolis" in r["grand_prix"]]
    indy_ok = len(indy) == 11 and all(started.get(r["race_index"]) for r in indy)
    check("indianapolis_500_1950_1960_counted", indy_ok,
          "%d Indianapolis 500 races, %d starts by drivers of drivers.csv" % (len(indy), sum(len(started.get(r["race_index"], {})) for r in indy)))

    # 5. win rate: the decimal rounding against exact fractions on every pair that can occur,
    #    and the half-way cases named in the contract
    wins_after = {}
    for c in credits:
        wins_after[(c["race_index"], c["driver_id"])] = int(c["career_wins_after"])
    rate_bad = []
    for w in range(0, 401):
        for s in range(max(1, w), 401):
            if win_rate(w, s) != win_rate_check(w, s):
                rate_bad.append("%d/%d: %s vs %s" % (w, s, win_rate(w, s), win_rate_check(w, s)))
    halves = {(1, 8): "12.5", (1, 16): "6.3", (3, 16): "18.8", (1, 80): "1.3", (1, 3): "33.3", (2, 3): "66.7",
              (91, 306): "29.7", (1, 1): "100.0", (1, 400): "0.3", (1, 2000): "0.1"}
    for (w, s), want in halves.items():
        if win_rate(w, s) != want:
            rate_bad.append("%d/%d: %s, expected %s" % (w, s, win_rate(w, s), want))
    check("win_rate_rounding_half_up", not rate_bad,
          rate_bad[:20] or "decimal ROUND_HALF_UP equals exact-fraction rounding on every wins <= starts <= 400; "
          "half-way cases 1/8 = 12.5, 1/16 = 6.25 -> 6.3, 3/16 = 18.75 -> 18.8, 1/80 = 1.25 -> 1.3")

    # 6. career starts at the freeze against "List of Formula One drivers"
    by_pid_list = {}
    for L in lst:
        t = titles.get(L["link"])
        if t and t[1].isdigit():
            by_pid_list.setdefault("wp" + t[1], []).append(L)
    career, agree, disagree, list_wins_bad = [], 0, [], []
    for did in order:
        L = by_pid_list.get(did, [])
        entry = L[0] if len(L) == 1 else None
        ls = entry["starts"] if entry and entry["starts"].isdigit() else "NOT FOUND"
        le = entry["entries"] if entry and entry["entries"].isdigit() else "NOT FOUND"
        if entry and entry["wins"].isdigit() and int(entry["wins"]) != totals[did]:
            list_wins_bad.append("%s: list %s, career_totals %d" % (name[did], entry["wins"], totals[did]))
        if ls != "NOT FOUND" and int(ls) == running[did]:
            cmp_ = "AGREE"
            agree += 1
        else:
            cmp_ = "DISAGREE"
            disagree.append({"driver_id": did, "driver_name": name[did], "season_tables": running[did], "list": ls})
        fs = first_start[did]
        career.append({"driver_id": did, "driver_name": name[did], "wins": totals[did], "starts": running[did],
                       "win_rate_pct": win_rate(totals[did], running[did]),
                       "first_start": "%s %s" % (fs["season"], fs["grand_prix"]), "first_start_date": fs["race_date"],
                       "list_race_entries": le, "list_race_starts": ls, "list_revision_id": list_meta["revid"],
                       "list_comparison": cmp_})
    career_cols = ["driver_id", "driver_name", "wins", "starts", "win_rate_pct", "first_start", "first_start_date",
                   "list_race_entries", "list_race_starts", "list_revision_id", "list_comparison"]
    got_dis = {d["driver_name"]: (d["season_tables"], int(d["list"]) if str(d["list"]).isdigit() else d["list"]) for d in disagree}
    check("career_starts_vs_list_of_f1_drivers_as_prototype", agree == EXPECT_LIST_AGREE and got_dis == EXPECT_LIST_DISAGREE,
          "%d of 116 agree with the List page (rev. %s); disagreements (kept at the season-table value, listed "
          "for Luke, not resolved): %s" % (agree, list_meta["revid"],
                                          "; ".join("%s season tables %s, list %s" % (k, v[0], v[1]) for k, v in got_dis.items()) or "none"))
    check("list_page_wins_equal_career_totals", not list_wins_bad, list_wins_bad or "116 of 116 drivers")
    schu = next(c for c in career if c["driver_name"] == "Michael Schumacher")
    check("luke_example_schumacher", (schu["wins"], schu["starts"], schu["win_rate_pct"]) == (91, 306, "29.7"),
          "Michael Schumacher %d wins · %d starts · %s%%" % (schu["wins"], schu["starts"], schu["win_rate_pct"]))

    # 7. evidence for each disagreement: every counted start from a non-finishing cell
    evidence = {}
    for d in disagree:
        did = d["driver_id"]
        cand = [x for x in rows_out if x["driver_id"] == did and not any(
            classify(c)[1] and any(t.isdigit() for t in classify(c)[1]) for c in x["source_cells"].split(" + "))]
        evidence[d["driver_name"]] = [{"race": "%s %s" % (x["season"], x["grand_prix"]), "date": x["race_date"],
                                       "cell": x["source_cells"], "revision": x["source_revision_id"]} for x in cand]

    if failures:
        raise SystemExit("rtt002_starts: checks FAILED: " + ", ".join(failures) + "\n" +
                         json.dumps({k: checks[k] for k in failures}, ensure_ascii=False, indent=1)[:4000])

    starts_csv = csv_text(starts_cols, rows_out)
    career_csv = csv_text(career_cols, career)
    write(os.path.join(data_dir, "starts.csv"), starts_csv)
    write(os.path.join(data_dir, "career_starts.csv"), career_csv)
    summary = {"starts_rows": len(rows_out), "drivers": len(order), "races": len(races),
               "list_page": "%s rev. %s (retrieved %s)" % (list_meta["title"], list_meta["revid"], iso(list_meta["retrieved"])),
               "list_agree": agree, "list_disagree": len(disagree),
               "drivers_with_several_rows_in_one_season": multi_rows,
               "races_where_one_driver_has_several_starting_cells_counted_once": multi_cells}
    cj = {"build": BUILD_VERSION, "summary": summary, "checks": checks, "disagreements": disagree,
          "disagreement_evidence": evidence, "round_counts": count_rows}
    write(os.path.join(data_dir, "starts_checks.json"), json.dumps(cj, ensure_ascii=False, indent=1, sort_keys=True) + "\n")

    md = ["# RTT-002 starts — scripted checks", "",
          "Build `%s` (`scripts/rtt002_starts.py`). All checks pass: **True**. Definition, source and rounding: "
          "`reference/metric_contract_RTT-002.md`, Display attributes (DEC-053)." % BUILD_VERSION, "",
          "| Check | Result | Detail |", "|---|---|---|"]
    for k, v in checks.items():
        det = v.get("detail")
        if isinstance(det, dict):
            det = ", ".join("%s %d" % kv for kv in det.items())
        elif isinstance(det, list):
            det = "; ".join(det)
        md.append("| %s | %s | %s |" % (k, "PASS" if v["pass"] else "FAIL", det))
    md += ["", "## Summary", "",
           "- %d starts rows (drivers of `drivers.csv` only) over %d races" % (len(rows_out), len(races)),
           "- career starts at the freeze vs %s: %d agree, %d disagree" % (summary["list_page"], agree, len(disagree)),
           "- drivers with more than one row in a season's table (one start per race still): %s" % (", ".join(multi_rows) or "none"),
           "- races where one driver had more than one starting cell part (counted once): %s" % (", ".join(multi_cells) or "none"),
           "", "## Disagreements with the List page (for Luke; not resolved, the season-table value is kept)", ""]
    for d in disagree:
        ev = evidence[d["driver_name"]]
        md.append("**%s**: %d starts from the season tables, %s in \"List of Formula One drivers\" (rev. %s). "
                  "The candidates are the %d counted starts whose cell shows no classified position (Ret, NC or DSQ): "
                  "if the List page is right, one of these was not a start." % (d["driver_name"], d["season_tables"], d["list"],
                                                                                list_meta["revid"], len(ev)))
        named = [e for e in ev if e["race"] in NAMED_CANDIDATES.get(d["driver_name"], [])]
        if named:
            md.append("")
            md.append("Named in the task (prompts/CODE_SESSION_IQ-05e.md) as an example candidate: %s. Which race "
                      "is the extra one cannot be decided from these two Wikipedia sources; it needs a third source "
                      "(Luke's decision). Until then the season-table value is used." % "; ".join(
                          "%s (cell \"%s\", revision %s)" % (e["race"], e["cell"], e["revision"]) for e in named))
        md.append("")
        md.append("| Race | Date | Season-table cell | Season page revision |")
        md.append("|---|---|---|---|")
        for e in ev:
            md.append("| %s | %s | %s | %s |" % (e["race"], e["date"], e["cell"], e["revision"]))
        md.append("")
    md += ["## Round columns per season", "", "| Season | Columns | Empty-header columns dropped | Rounds listed | races.csv |", "|---|---|---|---|---|"]
    for c in count_rows:
        md.append("| %d | %d | %d | %d | %d |" % (c["season"], c["columns"], c["empty_header_dropped"], c["rounds_listed"], c["races_csv"]))
    write(os.path.join(data_dir, "STARTS_CHECKS.md"), "\n".join(md) + "\n")

    outs = ["starts.csv", "career_starts.csv", "starts_checks.json", "STARTS_CHECKS.md"]
    reads = ["races.csv", "win_credits.csv", "drivers.csv", "career_totals.csv"]
    man = {"build": BUILD_VERSION, "script": "scripts/rtt002_starts.py",
           "metric_contract": "reference/metric_contract_RTT-002.md (Display attributes, DEC-053)",
           "licence": "CC BY-SA 4.0 (derived from English Wikipedia); see ATTRIBUTION.md",
           "source": {"file": "source/" + SOURCE, "sha256": SOURCE_SHA256, "extractor": EXTRACTOR,
                      "extractor_sha256": EXTRACTOR_SHA256, "extract_header": "|".join(header[1:]),
                      "season_pages": "77 season articles at the revisions in races.csv (same as the wins data)",
                      "list_page": {"title": list_meta["title"], "revid": list_meta["revid"], "retrieved_utc": iso(list_meta["retrieved"]),
                                    "permanent_url": PERMA + list_meta["revid"]}},
           "inputs_read_only": {n: sha(os.path.join(data_dir, n)) for n in reads},
           "outputs": {n: sha(os.path.join(data_dir, n)) for n in outs}}
    write(os.path.join(data_dir, "starts_manifest.json"), json.dumps(man, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    for n in outs + ["starts_manifest.json"]:
        print("%s  %s" % (sha(os.path.join(data_dir, n)), os.path.join(data_dir, n)))
    print("checks: %d/%d PASS; List page: %d agree, %d disagree (%s)" % (
        len(checks), len(checks), agree, len(disagree), ", ".join("%s %s vs %s" % (d["driver_name"], d["season_tables"], d["list"]) for d in disagree)))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "data/rtt-002")
