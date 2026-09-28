#!/usr/bin/env python3
"""Build data/rtt-002/driver_nationality.csv and the nationality comparison report
(IQ-05 round 3, prompts/CODE_SESSION_IQ-05c.md step 1; DEC-035, DEC-036).

For each of the 116 drivers in drivers.csv: the country the driver raced under (racing-licence
nationality, following the official Formula 1 treatment, DEC-012).

Inputs (all in data/rtt-002/source/, extracted in Luke's Chrome by
scripts/extract_nationality.browser.js because Wikimedia answers this cloud environment with
HTTP 429; see source/README.md):
  wikipedia_wikidata_nationality.psv
      one row per driver row of "List of Formula One Grand Prix winners" at revision 1376824402
      (the revision source/README.md already records): page ID, canonical title, the flag code and
      flag variant of the row's flag cell, the row's wins, the Wikidata item and its last revision,
      Wikidata P1532 (country for sport; "*" = preferred rank) and P27 (country of citizenship).
  wikidata_countries.psv
      the countries those Wikidata values name: English label and P298 (ISO 3166-1 alpha-3).

Rules:
  - Primary value = the Wikipedia flag code, mapped to ISO 3166-1 alpha-3 with Luke's table
    (UK -> GBR, GER -> DEU, NED -> NLD, SUI -> CHE, MON -> MCO; every other code unchanged).
  - The flag drawn is today's design of that country's flag (DEC-035), from flag-icons, whose
    files are named by ISO 3166-1 alpha-2 (ISO3_TO_ISO2 below; a code table, not driver data).
    Wikipedia's flag variant (e.g. USA 1912 = the 48-star flag) is kept in the CSV for the
    record; it does not change the flag drawn.
  - Cross-check: Wikidata P1532 when the item has it (AGREE if any non-deprecated P1532 value's
    ISO alpha-3 is the primary value); otherwise P27 (same test). A P1532 or P27 value with no
    ISO alpha-3 (Scotland, Kingdom of Italy) cannot agree. Anything else is a DISAGREEMENT,
    listed for Luke and never resolved here: the CSV keeps the Wikipedia value.
  - Nothing is guessed: a missing value is NOT FOUND.

Checks (the build stops if one fails): every row matches a drivers.csv row by page ID and every
driver has exactly one row; every Wikipedia wins value equals career_totals.csv; every flag code
is in the mapping; the source files have the hashes recorded in source/README.md.

Usage: python scripts/rtt002_nationality.py [data/rtt-002] [reports]
Standard library only; same inputs -> byte-identical outputs. Existing dataset files are only read.
"""
import csv
import hashlib
import io
import json
import os
import sys

REVISION = "1376824402"
PAGE = "List of Formula One Grand Prix winners"
SOURCES = {
    "wikipedia_wikidata_nationality.psv": "e041cff55f059f1ece3e91afd84a52a551754eb96546f52dbe448027775e9fb8",
    "wikidata_countries.psv": "083a9cd05d6e18edb62f06bed7905980a6b9aede57699f93a4a09ce8ab43bd5c",
}
# Luke's mapping of Wikipedia flag codes to ISO 3166-1 alpha-3 (all others unchanged)
WP_TO_ISO3 = {"UK": "GBR", "GER": "DEU", "NED": "NLD", "SUI": "CHE", "MON": "MCO"}
# ISO 3166-1 alpha-3 -> (English short name, alpha-2 = flag-icons file name). Only the codes the
# source uses; an unknown code stops the build rather than being guessed.
ISO3 = {
    "ARG": ("Argentina", "ar"), "AUS": ("Australia", "au"), "AUT": ("Austria", "at"),
    "BEL": ("Belgium", "be"), "BRA": ("Brazil", "br"), "CAN": ("Canada", "ca"),
    "CHE": ("Switzerland", "ch"), "COL": ("Colombia", "co"), "DEU": ("Germany", "de"),
    "ESP": ("Spain", "es"), "FIN": ("Finland", "fi"), "FRA": ("France", "fr"),
    "GBR": ("United Kingdom", "gb"), "ITA": ("Italy", "it"), "MCO": ("Monaco", "mc"),
    "MEX": ("Mexico", "mx"), "NLD": ("Netherlands", "nl"), "NZL": ("New Zealand", "nz"),
    "POL": ("Poland", "pl"), "SWE": ("Sweden", "se"), "USA": ("United States", "us"),
    "VEN": ("Venezuela", "ve"), "ZAF": ("South Africa", "za"),
}
# What the flag variants in the source mean (the {{flagcountry|XXX|variant}} argument on
# Wikipedia): the year of the flag design shown there. Recorded for DEC-035's list only.
COLS = ["driver_id", "display_name", "country_iso3", "country", "flag_code",
        "wikipedia_flag_code", "wikipedia_flag_variant", "wikipedia_page", "wikipedia_page_id",
        "wikipedia_revision_id", "wikipedia_retrieved_utc", "wikidata_item", "wikidata_revision_id",
        "wikidata_retrieved_utc", "wikidata_p1532", "wikidata_p1532_labels", "wikidata_p27",
        "wikidata_p27_labels", "comparison_basis", "comparison"]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def psv(path):
    head, rows, meta = None, [], None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("#source|"):
            meta = line[1:].split("|")
        elif line.startswith("#"):
            head = line[1:].split("|")
        elif line:
            rows.append(dict(zip(head, line.split("|"))))
    return meta, rows


def iso_time(t):
    """'2026-09-28T18:10:25.706Z' -> '2026-09-28T18:10:25Z' (the dataset's format)."""
    return t[:19] + "Z"


def build(data_dir, report_dir):
    src = os.path.join(data_dir, "source")
    for f, h in SOURCES.items():
        got = sha(os.path.join(src, f))
        if got != h:
            raise SystemExit(f"{f}: SHA-256 {got} != {h} recorded in source/README.md")
    meta, nat = psv(os.path.join(src, "wikipedia_wikidata_nationality.psv"))
    _, countries = psv(os.path.join(src, "wikidata_countries.psv"))
    label = {c["qid"]: c["label_en"] for c in countries}
    iso3_of = {c["qid"]: c["iso3_P298"] for c in countries}
    if meta[1] != PAGE or meta[2] != "revision " + REVISION:
        raise SystemExit(f"source header names {meta[1]} {meta[2]}, expected {PAGE} revision {REVISION}")
    wp_time = iso_time(meta[3].replace("retrieved ", ""))
    wd_time = iso_time(meta[4].replace("wikidata retrieved ", ""))

    drivers = read_csv(os.path.join(data_dir, "drivers.csv"))
    totals = {r["driver_id"]: r for r in read_csv(os.path.join(data_dir, "career_totals.csv"))}
    by_pid = {}
    for r in nat:
        did = "wp" + r["pageid"]
        if did in by_pid:
            raise SystemExit(f"page ID {r['pageid']} appears twice in the source")
        by_pid[did] = r
    ids = [d["driver_id"] for d in drivers]
    checks = []
    missing, extra = [i for i in ids if i not in by_pid], [i for i in by_pid if i not in ids]
    checks.append(("every drivers.csv driver has exactly one source row, matched by page ID",
                   not missing and not extra, f"{len(nat)} rows, {len(drivers)} drivers; missing {missing or 'none'}, extra {extra or 'none'}"))
    wins_col = next(c for c in ("career_wins", "wins", "total_wins") if c in next(iter(totals.values())))
    bad_wins = [(i, by_pid[i]["wp_wins"], totals[i][wins_col]) for i in ids if i in by_pid and by_pid[i]["wp_wins"] != totals[i][wins_col]]
    checks.append(("every Wikipedia wins value equals career_totals.csv", not bad_wins, f"{len(ids) - len(bad_wins)}/{len(ids)} equal; differences {bad_wins or 'none'}"))
    unknown = sorted({by_pid[i]["wp_flag_code"] for i in ids if i in by_pid and WP_TO_ISO3.get(by_pid[i]["wp_flag_code"], by_pid[i]["wp_flag_code"]) not in ISO3 and by_pid[i]["wp_flag_code"]})
    checks.append(("every Wikipedia flag code maps to a known ISO 3166-1 alpha-3 code", not unknown, f"unknown: {unknown or 'none'}"))
    for name, ok, detail in checks:
        if not ok:
            raise SystemExit(f"CHECK FAILED: {name}: {detail}")

    rows, issues, notes, variants = [], [], [], []
    basis_count = {}
    for d in drivers:
        r = by_pid[d["driver_id"]]
        code = r["wp_flag_code"]
        iso3 = WP_TO_ISO3.get(code, code) if code else ""
        country, iso2 = ISO3.get(iso3, ("NOT FOUND", "NOT FOUND")) if iso3 else ("NOT FOUND", "NOT FOUND")
        p1532 = [q for q in r["P1532"].split(";") if q]
        p27 = [q for q in r["P27"].split(";") if q]
        qs = lambda vals: [q.rstrip("*") for q in vals]
        labs = lambda vals: ";".join(label.get(q, "NOT FOUND") for q in qs(vals))
        if not iso3:
            basis, cmp_ = "none", "NO PRIMARY"
        elif p1532:
            basis = "P1532"
            cmp_ = "AGREE" if iso3 in [iso3_of.get(q, "") for q in qs(p1532)] else "DISAGREE"
        elif p27:
            basis = "P27 (no P1532)"
            cmp_ = "AGREE" if iso3 in [iso3_of.get(q, "") for q in qs(p27)] else "DISAGREE"
        else:
            basis, cmp_ = "none", "NOT FOUND (no P1532 or P27)"
        basis_count[(basis, cmp_)] = basis_count.get((basis, cmp_), 0) + 1
        row = {"driver_id": d["driver_id"], "display_name": d["display_name"], "country_iso3": iso3 or "NOT FOUND",
               "country": country, "flag_code": iso2, "wikipedia_flag_code": code or "NOT FOUND",
               "wikipedia_flag_variant": r["wp_flag_variant"], "wikipedia_page": PAGE, "wikipedia_page_id": r["pageid"],
               "wikipedia_revision_id": REVISION, "wikipedia_retrieved_utc": wp_time, "wikidata_item": r["wikidata_qid"] or "NOT FOUND",
               "wikidata_revision_id": r["wikidata_lastrevid"] or "NOT FOUND", "wikidata_retrieved_utc": wd_time,
               "wikidata_p1532": ";".join(p1532) or "NOT FOUND", "wikidata_p1532_labels": labs(p1532) or "NOT FOUND",
               "wikidata_p27": ";".join(p27) or "NOT FOUND", "wikidata_p27_labels": labs(p27) or "NOT FOUND",
               "comparison_basis": basis, "comparison": cmp_}
        rows.append(row)
        if cmp_ != "AGREE":
            ev = (f"Wikipedia flag {code} → {iso3} ({country}); Wikidata {r['wikidata_qid']} (revision {r['wikidata_lastrevid']}): "
                  f"P1532 {', '.join(f'{q} {label.get(q, chr(63))}' for q in qs(p1532)) or 'none'}; "
                  f"P27 {', '.join(f'{q} {label.get(q, chr(63))}' for q in qs(p27)) or 'none'}")
            issues.append((d["display_name"], d["driver_id"], cmp_, basis, ev))
        elif basis == "P1532" and len(p1532) > 1:
            notes.append(f"{d['display_name']}: P1532 lists {', '.join(label.get(q, '?') for q in qs(p1532))}; one of them is {country}, so it counts as AGREE")
        if r["wp_flag_variant"]:
            variants.append((d["display_name"], code, r["wp_flag_variant"]))

    out = os.path.join(data_dir, "driver_nationality.csv")
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    open(out, "w", encoding="utf-8", newline="").write(buf.getvalue())

    by_country = {}
    for r in rows:
        by_country.setdefault((r["country"], r["country_iso3"], r["flag_code"]), []).append(r["display_name"])
    disagree = [i for i in issues if i[2] == "DISAGREE"]
    rep = {"page": PAGE, "revision": REVISION, "wikipedia_retrieved_utc": wp_time, "wikidata_retrieved_utc": wd_time,
           "sources": SOURCES, "csv_sha256": sha(out), "drivers": len(rows),
           "checks": [{"check": n, "pass": ok, "detail": dt} for n, ok, dt in checks],
           "comparison": {f"{b} / {c}": n for (b, c), n in sorted(basis_count.items())},
           "disagreements_and_missing": [dict(zip(["driver", "driver_id", "result", "basis", "evidence"], i)) for i in issues],
           "wikipedia_flag_variants": [dict(zip(["driver", "wikipedia_code", "variant"], v)) for v in variants]}
    os.makedirs(report_dir, exist_ok=True)
    json.dump(rep, open(os.path.join(report_dir, "RTT-002_nationality_comparison.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    agree = sum(n for (b, c), n in basis_count.items() if c == "AGREE")
    L = ["# RTT-002 driver nationality — comparison report", "",
         "Written by `python scripts/rtt002_nationality.py` (deterministic). Output: `data/rtt-002/driver_nationality.csv` "
         f"(SHA-256 `{rep['csv_sha256']}`).", "",
         f"- Primary source: the flag in each driver's row of Wikipedia's \"{PAGE}\", revision {REVISION} (the revision recorded in "
         f"`data/rtt-002/source/README.md`), retrieved {wp_time}. Codes mapped to ISO 3166-1 alpha-3 with Luke's table (UK→GBR, GER→DEU, NED→NLD, SUI→CHE, MON→MCO; others unchanged).",
         f"- Cross-check: Wikidata P1532 (country for sport) on each driver's item; where an item has no P1532, P27 (country of citizenship). Retrieved {wd_time}.",
         "- Extraction: `scripts/extract_nationality.browser.js`, run in Luke's Chrome by Claude in Cowork, because Wikimedia answered this cloud environment with HTTP 429 "
         "(Claude Code's own requests on 28 Sep 2026, 17:59–18:2x UTC: Wikipedia API 429 on every content request, Wikidata API 429 on every request; not worked around).", "",
         "## Checks", ""]
    L += [f"- {'PASS' if ok else 'FAIL'}: {n} — {dt}" for n, ok, dt in checks]
    L += ["", "## Result", "",
          f"{len(rows)} drivers; primary value found for {sum(1 for r in rows if r['country_iso3'] != 'NOT FOUND')}; Wikidata agrees for {agree}, disagrees for {len(disagree)}, other {len(issues) - len(disagree)}.", "",
          "| Compared on | Result | Drivers |", "|---|---|---|"]
    L += [f"| {b} | {c} | {n} |" for (b, c), n in sorted(basis_count.items())]
    L += ["", "## Disagreements and missing values (for Luke; not resolved — the CSV keeps the Wikipedia value)", ""]
    if issues:
        L += ["| Driver | ID | Result | Compared on | Evidence |", "|---|---|---|---|---|"]
        L += [f"| {n} | `{i}` | {c} | {b} | {e} |" for n, i, c, b, e in issues]
    else:
        L.append("None.")
    if notes:
        L += ["", "Several Wikidata values, one of which matches (counted as AGREE, listed for completeness):", ""] + [f"- {n}" for n in notes]
    L += ["", "## Historical flag variants in the Wikipedia source (for the record; DEC-035: today's design is drawn for everyone)", "",
          "The Wikipedia rows below show a dated flag variant (the flag of that year). The video draws today's flag for these drivers too.", "",
          "| Driver | Wikipedia code | Variant |", "|---|---|---|"]
    L += [f"| {n} | {c} | {v} |" for n, c, v in variants]
    L += ["", "## By country (primary value; flag = flag-icons file, today's design)", "", "| Country | ISO alpha-3 | Flag file | Drivers |", "|---|---|---|---|"]
    for (c, i3, fc), names in sorted(by_country.items(), key=lambda x: (-len(x[1]), x[0][0])):
        L.append(f"| {c} | {i3} | `{fc}` | {len(names)}: {', '.join(names)} |")
    open(os.path.join(report_dir, "RTT-002_nationality_comparison.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    for n, ok, dt in checks:
        print(("PASS " if ok else "FAIL ") + n + " — " + dt)
    print(f"{len(rows)} drivers; AGREE {agree}; DISAGREE {len(disagree)}; other {len(issues) - len(disagree)}")
    for n, i, c, b, e in issues:
        print(f"  {c}: {n} ({b}) — {e}")
    print(f"flag variants in the source: {len(variants)}")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "data/rtt-002", sys.argv[2] if len(sys.argv) > 2 else "reports")
