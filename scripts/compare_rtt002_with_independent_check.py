#!/usr/bin/env python3
"""Compare the RTT-002 Wikipedia build with the frozen independent check.

The independent check (ChatGPT deep research, run blind by Luke) is PRIVATE and
never committed. Its SHA-256 must match state/RTT-002_independent_check_freeze.json
before any comparison runs. Disagreements are LISTED, never resolved: no
averaging, no picking a side, no guessing.

Usage:
  python scripts/compare_rtt002_with_independent_check.py <check.zip> <data/rtt-002> <out.md> <out.json>

Compared sections: A (freeze), B (season rounds and wins per driver),
E (record progression), F (career wins >= 10), G (race winners and dates for
the seeded sample seasons). Driver names are matched by exact name first, then
by an accent/case/punctuation-insensitive key; every non-exact match is
listed so a human can confirm it is the same person.
"""
import csv
import hashlib
import io
import json
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict

FREEZE_RECORD = "state/RTT-002_independent_check_freeze.json"


def key(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().casefold()
    s = s.replace(" jr.", "").replace(" jr", "").replace(".", "").replace("-", " ")
    return " ".join(s.split())


def rd(z, name):
    return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8-sig"))))


def main(zpath, ddir, out_md, out_json):
    raw = open(zpath, "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    frozen = json.load(open(FREEZE_RECORD, encoding="utf-8"))["sha256"]
    if got != frozen:
        sys.exit(f"STOP: check file hash {got} does not match frozen {frozen}")
    z = zipfile.ZipFile(io.BytesIO(raw))

    # ours
    drivers = {r["driver_id"]: r for r in csv.DictReader(open(f"{ddir}/drivers.csv", encoding="utf-8"))}
    races = list(csv.DictReader(open(f"{ddir}/races.csv", encoding="utf-8")))
    totals = {r["driver_id"]: int(r["wins"]) for r in csv.DictReader(open(f"{ddir}/career_totals.csv", encoding="utf-8"))}
    prog = list(csv.DictReader(open(f"{ddir}/record_progression.csv", encoding="utf-8")))
    checks = json.load(open(f"{ddir}/checks.json", encoding="utf-8"))["summary"]

    by_exact = {d["display_name"]: i for i, d in drivers.items()}
    by_key = defaultdict(set)
    for i, d in drivers.items():
        for n in [d["display_name"]] + [v for v in d["name_variants_seen"].split("; ") if v]:
            by_key[key(n)].add(i)
    mapping_notes, unmatched = {}, set()

    def ident(name):
        name = name.strip()
        if name in by_exact:
            return by_exact[name]
        c = by_key.get(key(name), set())
        if len(c) == 1:
            i = next(iter(c))
            mapping_notes[name] = f"{drivers[i]['display_name']} ({drivers[i]['wikipedia_title']})"
            return i
        unmatched.add(name)
        return None

    disc = []  # (section, item, ours, theirs, their_source)

    # A
    a = rd(z, "A_data_freeze.csv")[0]
    ours_a = (checks["freeze_race"].split(" ", 1)[1], checks["freeze_date"], checks["freeze_winner"], str(checks["completed_2026_rounds"]))
    theirs_a = (a["freeze_race"], a["race_date"], a["winner"], a["completed_2026_rounds"])
    if (ours_a[1], ident(ours_a[2]), ours_a[3]) != (theirs_a[1], ident(theirs_a[2]), theirs_a[3]) or key(ours_a[0]) != key(theirs_a[0]):
        disc.append(("A", "data freeze", " / ".join(ours_a), " / ".join(theirs_a), a["source_url"]))

    # B
    our_rounds = Counter(int(r["season"]) for r in races)
    our_wins = defaultdict(Counter)
    for r in races:
        for d in r["winner_driver_ids"].split(";"):
            our_wins[int(r["season"])][d] += 1
    b_rows = rd(z, "B_season_driver_normalized.csv")
    their_rounds = {int(r["season"]): int(r["championship_rounds"]) for r in b_rows}
    their_wins = defaultdict(Counter)
    for r in b_rows:
        their_wins[int(r["season"])][ident(r["driver"]) or ("?" + r["driver"])] += int(r["wins"])
    b_src = {int(r["season"]): r["source_url"] for r in b_rows}
    for s in sorted(set(our_rounds) | set(their_rounds)):
        if our_rounds.get(s) != their_rounds.get(s):
            disc.append(("B", f"{s} championship rounds", our_rounds.get(s), their_rounds.get(s), b_src.get(s, "")))
        for d in sorted(set(our_wins[s]) | set(their_wins[s]), key=str):
            if our_wins[s].get(d, 0) != their_wins[s].get(d, 0):
                nm = drivers[d]["display_name"] if d in drivers else d
                disc.append(("B", f"{s} wins for {nm}", our_wins[s].get(d, 0), their_wins[s].get(d, 0), b_src.get(s, "")))

    # F
    for r in rd(z, "F_career_wins_10_plus.csv"):
        d = ident(r["driver"])
        if d is None or totals.get(d) != int(r["career_wins"]):
            disc.append(("F", f"career wins {r['driver']}", totals.get(d), int(r["career_wins"]), r["source_url"]))
    f_names = {ident(r["driver"]) for r in rd(z, "F_career_wins_10_plus.csv")}
    for d, n in totals.items():
        if n >= 10 and d not in f_names:
            disc.append(("F", f"career wins {drivers[d]['display_name']} missing from F", n, "absent", ""))

    # E
    ours_e = {(p["race_date"], p["driver_id"], int(p["career_wins"]), p["event"]) for p in prog}
    e_rows = rd(z, "E_wins_record_progression.csv")
    theirs_e = {(r["race_date"], ident(r["driver"]), int(r["career_wins"]), r["event"].strip()) for r in e_rows}
    e_src = {(r["race_date"], ident(r["driver"])): r["source_url"] for r in e_rows}
    for x in sorted(ours_e - theirs_e, key=str):
        disc.append(("E", f"{x[0]} {drivers[x[1]]['display_name']} {x[2]} wins {x[3]}", "present", "absent", ""))
    for x in sorted(theirs_e - ours_e, key=str):
        nm = drivers[x[1]]["display_name"] if x[1] in drivers else str(x[1])
        disc.append(("E", f"{x[0]} {nm} {x[2]} wins {x[3]}", "absent", "present", e_src.get((x[0], x[1]), "")))

    # G
    ours_g = {(int(r["season"]), int(r["round"])): r for r in races}
    g_rows = rd(z, "G_selected_seasons_race_winners.csv")
    label_diffs = 0
    for r in g_rows:
        k = (int(r["season"]), int(r["round"]))
        o = ours_g.get(k)
        tw = sorted(filter(None, (ident(w) for w in r["winner"].split(";"))))
        if o is None:
            disc.append(("G", f"{k[0]} round {k[1]} {r['race']}", "absent", f"{r['race_date']} {r['winner']}", r["source_url"]))
            continue
        ow = sorted(o["winner_driver_ids"].split(";"))
        if o["race_date"] != r["race_date"]:
            disc.append(("G", f"{k[0]} R{k[1]} {o['grand_prix']} date", o["race_date"], r["race_date"], r["source_url"]))
        if ow != tw:
            disc.append(("G", f"{k[0]} R{k[1]} {o['grand_prix']} winner", o["winner_names"], r["winner"], r["source_url"]))
        if key(o["grand_prix"]).replace(" grand prix", "") not in key(r["race"]) and key(r["race"]) not in key(o["grand_prix"]):
            label_diffs += 1
    g_seasons = sorted({int(r["season"]) for r in g_rows})
    for s in g_seasons:
        n_ours = sum(1 for k in ours_g if k[0] == s)
        n_theirs = sum(1 for r in g_rows if int(r["season"]) == s)
        if n_ours != n_theirs:
            disc.append(("G", f"{s} race count", n_ours, n_theirs, ""))

    result = {
        "check_file_sha256": got, "hash_matches_frozen_record": True,
        "sections_compared": ["A", "B", "E", "F", "G"],
        "counts": {"B_seasons": len(their_rounds), "E_rows_theirs": len(e_rows), "E_rows_ours": len(prog),
                   "F_rows": len(rd(z, "F_career_wins_10_plus.csv")), "G_rows": len(g_rows), "G_seasons": g_seasons},
        "discrepancies": [dict(zip(("section", "item", "wikipedia_build", "independent_check", "check_source"), d)) for d in disc],
        "name_matches_needing_confirmation": mapping_notes,
        "unmatched_names": sorted(unmatched),
        "race_label_differences_G": label_diffs,
    }
    json.dump(result, open(out_json, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    md = ["# RTT-002 discrepancy report: Wikipedia build vs frozen independent check", "",
          f"Independent check file SHA-256 `{got}` matches the frozen record ({FREEZE_RECORD}).",
          "Disagreements are listed, not resolved.", "",
          "| Section | What was compared | Result |", "|---|---|---|"]
    per = Counter(d[0] for d in disc)
    desc = {"A": "Data freeze race, date, winner, 2026 rounds", "B": f"Rounds and wins per driver, {len(their_rounds)} seasons",
            "E": f"Record progression ({len(e_rows)} check rows vs {len(prog)} build rows)",
            "F": "Career wins for every driver with 10+", "G": f"Race-by-race winners and dates, seasons {', '.join(map(str, g_seasons))}"}
    for s in "ABEFG":
        md.append(f"| {s} | {desc[s]} | {'agree' if not per[s] else str(per[s]) + ' discrepancies'} |")
    md += ["", f"**Discrepancies: {len(disc)}**", ""]
    if disc:
        md += ["| Section | Item | Wikipedia build | Independent check | Check's source |", "|---|---|---|---|---|"]
        md += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in disc]
    md += ["", "## Name matches that were not exact (please confirm same person)", ""]
    md += [f"- {k} -> {v}" for k, v in sorted(mapping_notes.items())] or ["- none"]
    md += ["", "## Names in the check that could not be matched", ""]
    md += [f"- {n}" for n in sorted(unmatched)] or ["- none"]
    md += ["", f"Race-name label differences in G (naming style only, e.g. 'Great Britain' vs 'British Grand Prix'): {label_diffs}.", ""]
    open(out_md, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "discrepancies"}, indent=1, ensure_ascii=False))
    print("DISCREPANCIES:", len(disc))
    for d in disc:
        print(" ", d)


if __name__ == "__main__":
    main(*sys.argv[1:5])
