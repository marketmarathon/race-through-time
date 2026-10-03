#!/usr/bin/env python3
"""RTT-001 Browser Wars: deterministic data build (IQ-12). Standard library only.

Usage: python scripts/build_rtt001_dataset.py data/rtt-001 reports/RTT-001_data_report.md

Inputs (data/rtt-001/source/):
  browsers_curated.csv          one row per browser family (display attributes; StatCounter labels it covers)
  observations_curated.csv      every pre-2009 figure used or considered, checked at its source (or marked UNVERIFIED)
  statcounter_browser_ww_all_monthly_200901-202609.csv   StatCounter's raw export (CC BY-SA 3.0), byte for byte
  statcounter.source.txt        URL, retrieval date and SHA-256 of that export
  report_notes.md               hand-written parts of the report (summary, questions for Luke)
Outputs: browsers.csv, observations.csv, series.csv, leaders.csv, CHECKS.md, checks.json, manifest.json; and the report.

Rules (reference/metric_contract_RTT-001.md): one source per period (DEC-152); straight lines between dated figures,
including across each hand-over (DEC-153); all devices (DEC-154); browser families and arithmetic (DEC-155); hand-over
rule (DEC-156); a browser not reported at a source date has no value on either side of it (DEC-157); dating (DEC-158);
"Other" is never a bar (DEC-159). Only VERIFIED figures are used. Nothing is averaged, held or carried across.
"""
import calendar
import csv
import datetime as dt
import hashlib
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

BUILD = "rtt001-build/1.0"
FIRST_MONTH, LAST_MONTH = (1994, 1), (2026, 9)
SC_FILE = "statcounter_browser_ww_all_monthly_200901-202609.csv"

# Eras (DEC-152). Era 3 has two sources one after the other: StatMarket, then OneStat.
SOURCES = {
    "GVU": {"era": "1", "name": "GVU WWW User Surveys (Georgia Tech)", "short": "GVU survey"},
    "EWS": {"era": "2", "name": "University of Illinois EWS web server", "short": "Illinois EWS server"},
    "STATMARKET": {"era": "3a", "name": "WebSideStory StatMarket", "short": "StatMarket"},
    "ONESTAT": {"era": "3b", "name": "OneStat.com", "short": "OneStat"},
    "W3COUNTER": {"era": "4", "name": "W3Counter", "short": "W3Counter"},
    "STATCOUNTER": {"era": "5", "name": "StatCounter Global Stats", "short": "StatCounter"},
}
ERA_ORDER = ["GVU", "EWS", "STATMARKET", "ONESTAT", "W3COUNTER", "STATCOUNTER"]
# Era windows by brief (DEC-152): points of a source must fall inside its window.
ERA_WINDOWS = {
    "GVU": (dt.date(1994, 1, 1), dt.date(1995, 12, 31)),
    "EWS": (dt.date(1996, 4, 1), dt.date(2000, 12, 31)),
    "STATMARKET": (dt.date(2001, 1, 1), dt.date(2007, 4, 30)),
    "ONESTAT": (dt.date(2001, 1, 1), dt.date(2007, 4, 30)),
    "W3COUNTER": (dt.date(2007, 5, 1), dt.date(2008, 12, 31)),
    "STATCOUNTER": (dt.date(2009, 1, 1), dt.date(2026, 9, 30)),
}
BOARD_MONTHS = ["1994-01", "1994-11", "1996-04", "1998-10", "2001-01", "2004-01", "2007-01", "2008-12", "2009-01",
                "2012-05", "2016-01", "2020-01", "2026-09"]


def d(s):
    return dt.date.fromisoformat(s)


def month_end(y, m):
    return dt.date(y, m, calendar.monthrange(y, m)[1])


def month_ends():
    out, (y, m) = [], FIRST_MONTH
    while (y, m) <= LAST_MONTH:
        out.append(month_end(y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def num(text):
    """A published percentage read as text: decimal comma -> point, '.8' -> 0.8. Malformed -> None."""
    t = text.strip().replace(",", ".")
    if t.count(".") > 1 or not t or not all(c.isdigit() or c == "." for c in t):
        return None
    return Decimal(t)


def q2(x):
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def fmt(x):
    if x is None:
        return ""
    s = format(x, "f")
    return s


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ---------------------------------------------------------------- inputs
def load_statcounter(src, browsers):
    path = os.path.join(src, SC_FILE)
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], [r for r in rows[1:] if r]
    label_to_id = {}
    for b in browsers:
        for lab in filter(None, b["statcounter_labels"].split("|")):
            label_to_id[lab] = b["browser_id"]
    obs, raw_cells = [], {}
    for r in body:
        ym = r[0].strip()
        y, m = int(ym[:4]), int(ym[5:7])
        when = month_end(y, m)
        for lab, cell in zip(header[1:], r[1:]):
            raw_cells[(when, lab)] = cell
            bid = label_to_id.get(lab, "")
            obs.append({"obs_id": f"SC-{ym}-{lab}", "source_id": "STATCOUNTER", "date": when.isoformat(),
                        "date_basis": "month end of the StatCounter month", "browser_label": lab, "browser_id": bid,
                        "value_text": cell, "measure": "page views, all platforms", "geography": "Worldwide",
                        "url": "data/rtt-001/source/" + SC_FILE, "quote": f"{ym} {lab} {cell}", "verified": "yes",
                        "verified_by": "raw export (statcounter.source.txt)", "used": "", "why": "", "parts": ""})
    # StatCounter zeros before a browser's first non-zero month or after its last are 'not reported', not a share
    by_bid = {}
    for o in obs:
        if o["browser_id"]:
            by_bid.setdefault(o["browser_id"], []).append(o)
    for o in obs:
        if not o["browser_id"]:
            o["used"], o["why"] = "no", "not a browser bar (Other / unknown, DEC-159)"
    for bid, lst in by_bid.items():
        dates_nonzero = sorted({x["date"] for x in lst if num(x["value_text"]) and num(x["value_text"]) > 0})
        for x in lst:
            v = num(x["value_text"])
            if v is None:
                x["used"], x["why"] = "no", "value not a number"
            elif not dates_nonzero or x["date"] < dates_nonzero[0] or x["date"] > dates_nonzero[-1]:
                x["used"], x["why"] = "no", "zero before the browser's first or after its last reported month (not reported)"
            else:
                x["used"], x["why"] = "yes", "era 5 source (DEC-152)"
    return header, body, obs, raw_cells


def points_from(obs_rows):
    """Used observations -> points {browser_id: {date: point}}; arithmetic rows carry their parts."""
    pts = {}
    for o in obs_rows:
        if o["used"] != "yes":
            continue
        v = num(o["value_text"])
        when = d(o["date"])
        p = {"value": v, "obs_id": o["obs_id"], "source_id": o["source_id"],
             "provenance": "arithmetic" if o["parts"] else "observed", "date": when}
        pts.setdefault(o["browser_id"], {})
        if when in pts[o["browser_id"]]:
            raise SystemExit(f"two used points for {o['browser_id']} on {when}: {pts[o['browser_id']][when]['obs_id']} and {o['obs_id']}")
        pts[o["browser_id"]][when] = p
    return pts


def source_dates(pts):
    """Every point date with the source that owns it (one source per date is checked separately)."""
    owners = {}
    for bp in pts.values():
        for when, p in bp.items():
            owners.setdefault(when, set()).add(p["source_id"])
    return owners


def first_last_dates(owners):
    """First and last source date of each source (for the hand-over rule)."""
    fl = {}
    for w, own in owners.items():
        for sid in own:
            a, b = fl.get(sid, (w, w))
            fl[sid] = (min(a, w), max(b, w))
    return fl


def joinable(a, z, fl):
    """DEC-153/156/157: a straight line joins two consecutive points of one browser if both come from the same source,
    or if they are the outgoing source's last date and the next source's first date (a hand-over)."""
    if a["source_id"] == z["source_id"]:
        return True
    i, j = ERA_ORDER.index(a["source_id"]), ERA_ORDER.index(z["source_id"])
    return j == i + 1 and a["date"] == fl[a["source_id"]][1] and z["date"] == fl[z["source_id"]][0]


def build_series(browsers, pts, owners, months):
    dates = sorted(owners)
    src_of = {w: sorted(s)[0] for w, s in owners.items()}
    fl = first_last_dates(owners)
    rows = []
    for b in browsers:
        bid = b["browser_id"]
        bp = pts.get(bid, {})
        bdates = sorted(bp)
        for me in months:
            row = {"month": me.strftime("%Y-%m"), "date": me.isoformat(), "browser_id": bid,
                   "display_name": b["display_name"], "share": "", "provenance": "not_found",
                   "era": "", "source_id": "", "source_line": "", "handover": "", "estimated": "yes" if me < dt.date(2009, 1, 1) else "no",
                   "left_point": "", "right_point": ""}
            left_any = max((x for x in dates if x < me), default=None)
            right_any = min((x for x in dates if x > me), default=None)
            if me in bp:
                p = bp[me]
                row.update(share=fmt(p["value"]), provenance=p["provenance"], left_point=p["obs_id"], right_point=p["obs_id"],
                           source_id=p["source_id"], era=SOURCES[p["source_id"]]["era"], handover="no",
                           source_line=SOURCES[p["source_id"]]["name"])
            else:
                left = max((x for x in bdates if x < me), default=None)
                right = min((x for x in bdates if x > me), default=None)
                if left and right and joinable(bp[left], bp[right], fl):
                    a, z = bp[left], bp[right]
                    frac = Decimal((me - left).days) / Decimal((right - left).days)
                    v = q2(a["value"] + (z["value"] - a["value"]) * frac)
                    hand = a["source_id"] != z["source_id"]
                    if hand:
                        line = f"Estimate between {SOURCES[a['source_id']]['short']} ({left:%b %Y}) and {SOURCES[z['source_id']]['short']} ({right:%b %Y})"
                        era, sid = f"{SOURCES[a['source_id']]['era']}>{SOURCES[z['source_id']]['era']}", f"{a['source_id']}>{z['source_id']}"
                    else:
                        line, era, sid = SOURCES[a["source_id"]]["name"], SOURCES[a["source_id"]]["era"], a["source_id"]
                    row.update(share=fmt(v), provenance="interpolated", left_point=a["obs_id"], right_point=z["obs_id"],
                               source_id=sid, era=era, handover="yes" if hand else "no", source_line=line)
                elif left_any and right_any:
                    # era context even where this browser has no value (for the on-screen source line)
                    s1, s2 = src_of[left_any], src_of[right_any]
                    row.update(era=SOURCES[s1]["era"] if s1 == s2 else f"{SOURCES[s1]['era']}>{SOURCES[s2]['era']}",
                               handover="no" if s1 == s2 else "yes")
            rows.append(row)
    return rows


def boards(series, months, names):
    by_month = {}
    for r in series:
        if r["share"] != "":
            by_month.setdefault(r["month"], []).append(r)
    out, prev_order = {}, []
    for me in months:
        ym = me.strftime("%Y-%m")
        lst = by_month.get(ym, [])
        rank_prev = {b: i for i, b in enumerate(prev_order)}
        lst.sort(key=lambda r: (-Decimal(r["share"]), rank_prev.get(r["browser_id"], 999), names[r["browser_id"]]))
        out[ym] = lst
        prev_order = [r["browser_id"] for r in lst]
    return out


def leader_changes(bd):
    changes, prev = [], None
    for ym, lst in bd.items():
        if not lst:
            continue
        top = lst[0]
        if prev is None or top["browser_id"] != prev["browser_id"]:
            changes.append({"month": ym, "leader": top["browser_id"], "leader_share": top["share"],
                            "previous_leader": prev["browser_id"] if prev else "", "previous_share_this_month":
                            next((r["share"] for r in lst if prev and r["browser_id"] == prev["browser_id"]), ""),
                            "provenance": top["provenance"], "handover": top["handover"], "era": top["era"],
                            "source_line": top["source_line"], "left_point": top["left_point"], "right_point": top["right_point"]})
        prev = top
    return changes


# ---------------------------------------------------------------- checks
def run_checks(browsers, obs, pts, owners, series, months, sc_header, sc_body, raw_cells):
    checks, notes = [], {}
    ids = {b["browser_id"] for b in browsers}

    def add(name, ok, detail, review=False):
        checks.append({"check": name, "result": "PASS" if ok else ("REVIEW" if review else "FAIL"), "detail": detail})

    bad = [r for r in series if r["share"] != "" and not (Decimal(0) <= Decimal(r["share"]) <= Decimal(100))]
    add("values_within_0_100", not bad, f"{sum(1 for r in series if r['share'] != '')} values; outside: {len(bad)}")

    # per source date, the shown browsers' total
    breaches, sums = [], []
    for when in sorted(owners):
        parts = [(bid, bp[when]) for bid, bp in pts.items() if when in bp]
        tot = sum(p["value"] for _, p in parts)
        prec = max((-(p["value"].as_tuple().exponent) for _, p in parts), default=0)
        allow = Decimal(len(parts)) * (Decimal(5) / (Decimal(10) ** (prec + 1)))
        sums.append((when, tot, allow, len(parts)))
        if tot > Decimal(100) + allow:
            breaches.append(f"{when} {','.join(sorted(owners[when]))}: {tot} (allowance {allow})")
    notes["totals"] = breaches
    add("source_date_totals_at_most_100", not breaches,
        f"{len(sums)} source dates; max total {max(t for _, t, _, _ in sums)}; breaches beyond the source's rounding: {len(breaches)}",
        review=True)

    missing = [r for r in series if r["share"] != "" and r["provenance"] not in ("observed", "arithmetic", "interpolated")]
    add("every_point_has_provenance", not missing, f"{sum(1 for r in series if r['share'] != '')} values checked; missing: {len(missing)}")

    two = {str(w): sorted(s) for w, s in owners.items() if len(s) > 1}
    add("one_source_per_date", not two, f"{len(owners)} source dates; dates with two sources: {two}")

    spans = []
    for s in ERA_ORDER:
        ds = sorted(w for w, own in owners.items() if s in own)
        if ds:
            spans.append((s, ds[0], ds[-1]))
    overlap = [f"{a[0]} {a[1]}..{a[2]} vs {b[0]} {b[1]}..{b[2]}" for a, b in zip(spans, spans[1:]) if b[1] <= a[2]]
    outside = [f"{s} {w}" for s in ERA_ORDER for w, own in owners.items() if s in own and not (ERA_WINDOWS[s][0] <= w <= ERA_WINDOWS[s][1])]
    notes["spans"] = spans
    add("eras_do_not_overlap", not overlap and not outside,
        "; ".join(f"{s} {a}..{b}" for s, a, b in spans) + f"; overlaps: {overlap}; points outside their era window: {outside}")

    # StatCounter values in series equal the raw cells (or the recorded sum of one browser's labels)
    lab = {b["browser_id"]: [x for x in b["statcounter_labels"].split("|") if x] for b in browsers}
    mism, n = [], 0
    for r in series:
        if r["source_id"] == "STATCOUNTER" and r["provenance"] in ("observed", "arithmetic"):
            when = d(r["date"])
            labs = lab[r["browser_id"]]
            if len(labs) == 1:
                ok = r["share"] == raw_cells[(when, labs[0])]
            else:
                ok = Decimal(r["share"]) == sum(num(raw_cells[(when, x)]) for x in labs)
            n += 1
            if not ok:
                mism.append(f"{r['month']} {r['browser_id']}")
    sc_months = {r[0] for r in sc_body}
    add("statcounter_equals_raw_csv", not mism and len(sc_months) == 213,
        f"{n} StatCounter values compared with the raw export ({len(sc_months)} months, {len(sc_header) - 1} columns); mismatches: {mism[:10]}")

    used_bad = [o["obs_id"] for o in obs if o["used"] == "yes" and o["verified"] != "yes"]
    add("no_unverified_or_not_found_used", not used_bad,
        f"{sum(1 for o in obs if o['used'] == 'yes')} used figures; used but not VERIFIED: {used_bad}")

    early = []
    for bid, bp in pts.items():
        first, last = min(bp), max(bp)
        for r in series:
            if r["browser_id"] == bid and r["share"] != "" and not (first <= d(r["date"]) <= last):
                early.append(f"{bid} {r['month']}")
    nobar = [b for b in pts if b not in ids or not b]
    add("nothing_before_first_or_after_last_source_date", not early and not nobar,
        f"{len(pts)} browsers with points; values outside their first..last point: {early[:10]}; points without a browser row: {nobar}")

    grid = {r["month"] for r in series}
    add("month_grid_complete", len(grid) == len(months) == 393 and len(series) == len(months) * len(browsers),
        f"{len(months)} month ends {months[0]}..{months[-1]} x {len(browsers)} browsers = {len(series)} rows")

    # arithmetic rows equal the sum of their parts; parts are the same source, same date, same browser family
    byid = {o["obs_id"]: o for o in obs}
    arith_bad = []
    for o in obs:
        if o["parts"]:
            ps = [byid[p] for p in o["parts"].split("+")]
            same = all(p["source_id"] == o["source_id"] and p["date"] == o["date"] and p["browser_id"] == o["browser_id"] for p in ps)
            if any(num(p["value_text"]) is None for p in ps) or sum(num(p["value_text"]) for p in ps) != num(o["value_text"]) or not same:
                arith_bad.append(o["obs_id"])
    add("arithmetic_rows_equal_their_parts", not arith_bad,
        f"{sum(1 for o in obs if o['parts'])} arithmetic rows; problems: {arith_bad}")

    other = [r for r in series if r["share"] != "" and r["browser_id"] in ("other", "unknown")]
    add("other_is_never_a_bar", not other and not any(b["browser_id"] in ("other", "unknown") for b in browsers),
        f"'Other'/'unknown' rows in series: {len(other)}")
    return checks, notes


def write_checks(out, checks, notes):
    allok = all(c["result"] == "PASS" for c in checks)
    with open(os.path.join(out, "checks.json"), "w", encoding="utf-8") as f:
        json.dump({"build": BUILD, "all_pass": allok, "checks": checks, "totals_beyond_rounding": notes["totals"]},
                  f, indent=1, ensure_ascii=False)
        f.write("\n")
    lines = ["# RTT-001 scripted checks", "",
             f"Build `{BUILD}`. All checks PASS: **{allok}**. A check marked REVIEW found something that is reported in full below, not hidden or fixed.",
             "", "| Check | Result | Detail |", "|---|---|---|"]
    lines += [f"| {c['check']} | {c['result']} | {c['detail'].replace('|', '/')} |" for c in checks]
    lines += ["", "## Source dates whose shown browsers total more than 100 (beyond the source's own rounding)", ""]
    lines += [f"- {x}" for x in notes["totals"]] or ["- none"]
    lines += ["", "## Era spans (first and last point of each source)", ""]
    lines += [f"- {s}: {a} to {b}" for s, a, b in notes["spans"]]
    with open(os.path.join(out, "CHECKS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return allok


# ---------------------------------------------------------------- report
def write_report(path, src, browsers, obs, pts, owners, series, bd, changes, checks):
    names = {b["browser_id"]: b["display_name"] for b in browsers}
    byid = {o["obs_id"]: o for o in obs}
    L = ["# RTT-001 Browser Wars — data report for Luke", "",
         f"Build `{BUILD}` (`scripts/build_rtt001_dataset.py`). Contract: `reference/metric_contract_RTT-001.md`. Data: `data/rtt-001/`.", ""]
    with open(os.path.join(src, "report_notes.md"), encoding="utf-8") as f:
        notes = f.read().split("<!-- QUESTIONS -->")
    L += [notes[0].strip(), ""]
    L += ["## Checks", "", "| Check | Result |", "|---|---|"] + [f"| {c['check']} | {c['result']} |" for c in checks] + [""]

    L += ["## Changes of first place", "",
          "| Month | New leader | Share | Previous leader (share that month) | How the month's value is made | Source line |",
          "|---|---|---|---|---|---|"]
    for c in changes:
        how = c["provenance"]
        if c["handover"] == "yes":
            how += ", on a hand-over stretch (no figure: the date is set only by the straight line)"
        elif c["provenance"] == "interpolated":
            how += " between two figures of the same source"
        prev = f"{names.get(c['previous_leader'], '—')} ({c['previous_share_this_month'] or 'no value'})" if c["previous_leader"] else "—"
        L.append(f"| {c['month']} | {names[c['leader']]} | {c['leader_share']}% | {prev} | {how} | {c['source_line']} |")
    L.append("")

    L += ["## Top-ten boards", ""]
    for ym in BOARD_MONTHS:
        lst = bd.get(ym, [])
        L += [f"### {dt.date(int(ym[:4]), int(ym[5:]), 1):%B %Y}", "",
              f"Source line: {lst[0]['source_line'] if lst else '—'}{' · estimated look' if ym < '2009-01' else ''}", "",
              "| # | Browser | Share | Provenance |", "|---|---|---|---|"]
        L += [f"| {i} | {names[r['browser_id']]} | {r['share']}% | {r['provenance']} |" for i, r in enumerate(lst[:10], 1)]
        L.append("")

    # seam table: last point of the outgoing source, first point of the incoming one, same-month cross-checks
    L += ["## Seam table (hand-overs between sources)", "",
          "Each hand-over joins the outgoing source's last figure to the incoming source's first figure with a straight line (DEC-153, DEC-156). Cross-check figures are never on screen; they show how far apart the measures are.", ""]
    spans = []
    for s in ERA_ORDER:
        ds = sorted(w for w, own in owners.items() if s in own)
        if ds:
            spans.append((s, ds[0], ds[-1]))
    for (s1, _, last), (s2, first, _) in zip(spans, spans[1:]):
        bids = sorted({b for b, bp in pts.items() if last in bp or first in bp}, key=lambda b: names[b])
        L += [f"### {SOURCES[s1]['name']} → {SOURCES[s2]['name']}", "",
              f"Outgoing last point {last}; incoming first point {first}; {(first - last).days} days of straight line.", "",
              "| Browser | Outgoing value | Incoming value |", "|---|---|---|"]
        for b in bids:
            a = pts[b].get(last)
            z = pts[b].get(first)
            L.append(f"| {names[b]} | {fmt(a['value']) + '%' if a else 'not reported'} | {fmt(z['value']) + '%' if z else 'not reported'} |")
        xs = [o for o in obs if o.get("seam") == f"{s1}>{s2}" and num(o["value_text"]) and
              min(abs((d(o["date"]) - last).days), abs((d(o["date"]) - first).days)) <= 45]
        if xs:
            L += ["", "Cross-checks within 45 days of either hand-over date, non-zero values (never on screen; all are in `observations.csv`):", "", "| Source | Date | Browser (as published) | Value | Verified |", "|---|---|---|---|---|"]
            L += [f"| {o['source_id']} | {o['date']} | {o['browser_label']} | {o['value_text']} | {o['verified']} |" for o in xs]
        L.append("")

    dis = [o for o in obs if o.get("disagrees_with")]
    L += ["## Disagreements (recorded, never averaged)", "", "| Figure | Source | Date | Value | Disagrees with | Note |", "|---|---|---|---|---|---|"]
    for o in dis:
        L.append(f"| {o['obs_id']} | {o['source_id']} | {o['date']} | {o['browser_label']} {o['value_text']} | {o['disagrees_with']} | {o['why']} |")
    L.append("")
    unv = [o for o in obs if o["verified"] != "yes"]
    L += ["## UNVERIFIED and NOT FOUND items (listed, never used)", "", "| Figure | Source | Date | Browser | Value | Status | Why |", "|---|---|---|---|---|---|---|"]
    L += [f"| {o['obs_id']} | {o['source_id']} | {o['date']} | {o['browser_label']} | {o['value_text']} | {o['verified']} | {o['why']} |" for o in unv]
    L.append("")
    if len(notes) > 1:
        L += [notes[1].strip(), ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def write_manifest(out, report_path):
    files = {}
    for root, _, fs in os.walk(out):
        for fn in sorted(fs):
            if fn == "manifest.json":
                continue
            p = os.path.join(root, fn)
            files[os.path.relpath(p, out)] = sha(p)
    files["../../" + report_path] = sha(report_path)
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"build": BUILD, "sha256": dict(sorted(files.items()))}, f, indent=1)
        f.write("\n")


def main():
    out, report_path = sys.argv[1], sys.argv[2]
    src = os.path.join(out, "source")
    browsers = read_csv(os.path.join(src, "browsers_curated.csv"))
    names = {b["browser_id"]: b["display_name"] for b in browsers}
    cur = read_csv(os.path.join(src, "observations_curated.csv"))
    sc_header, sc_body, sc_obs, raw_cells = load_statcounter(src, browsers)
    # StatCounter: a browser covered by two labels is the recorded sum of its own labels (DEC-155)
    multi = {b["browser_id"]: [x for x in b["statcounter_labels"].split("|") if x] for b in browsers}
    for bid, labs in multi.items():
        if len(labs) > 1:
            for r in sc_body:
                when = month_end(int(r[0][:4]), int(r[0][5:7])).isoformat()
                parts = [o for o in sc_obs if o["date"] == when and o["browser_label"] in labs]
                for o in parts:
                    o["used"], o["why"] = "no", "part of the sum " + bid
                vals = [num(o["value_text"]) for o in parts]
                if sum(vals) == 0:
                    continue
                sc_obs.append({**parts[0], "obs_id": f"SC-{r[0]}-{bid}-sum", "browser_label": "+".join(labs),
                               "value_text": fmt(sum(vals)), "quote": " + ".join(f"{o['browser_label']} {o['value_text']}" for o in parts),
                               "used": "yes", "why": "sum of one browser's StatCounter labels (DEC-155)",
                               "parts": "+".join(o["obs_id"] for o in parts)})
    obs = cur + sc_obs
    for o in obs:
        o.setdefault("seam", "")
        o.setdefault("disagrees_with", "")
    pts = points_from(obs)
    owners = source_dates(pts)
    months = month_ends()
    series = build_series(browsers, pts, owners, months)
    bd = boards(series, months, names)
    changes = leader_changes(bd)
    checks, notes = run_checks(browsers, obs, pts, owners, series, months, sc_header, sc_body, raw_cells)

    best = {}
    for ym, lst in bd.items():
        for i, r in enumerate(lst, 1):
            best[r["browser_id"]] = min(best.get(r["browser_id"], 999), i)
    b_out = []
    for b in browsers:
        bp = pts.get(b["browser_id"], {})
        b_out.append({**b, "first_point": min(bp).isoformat() if bp else "", "last_point": max(bp).isoformat() if bp else "",
                      "best_rank": best.get(b["browser_id"], "")})
    bfields = list(browsers[0].keys()) + ["first_point", "last_point", "best_rank"]
    write_csv(os.path.join(out, "browsers.csv"), b_out, bfields)
    ofields = ["obs_id", "source_id", "era", "date", "date_basis", "browser_label", "browser_id", "value_text", "measure",
               "geography", "url", "page_sha256", "quote", "verified", "verified_by", "used", "why", "parts", "seam", "disagrees_with"]
    for o in obs:
        o["era"] = SOURCES.get(o["source_id"], {}).get("era", "cross-check")
    obs_sorted = sorted(obs, key=lambda o: (o["date"], o["source_id"], o["obs_id"]))
    write_csv(os.path.join(out, "observations.csv"), obs_sorted, ofields)
    sfields = ["month", "date", "browser_id", "display_name", "share", "provenance", "estimated", "era", "source_id",
               "source_line", "handover", "left_point", "right_point"]
    write_csv(os.path.join(out, "series.csv"), series, sfields)
    write_csv(os.path.join(out, "leaders.csv"), changes, list(changes[0].keys()))
    allok = write_checks(out, checks, notes)
    write_report(report_path, src, browsers, obs, pts, owners, series, bd, changes, checks)
    write_manifest(out, report_path)
    print(f"{BUILD}: {len(series)} series rows, {len(obs)} observations, checks all PASS: {allok}")
    for c in checks:
        print(f"  {c['result']:6} {c['check']}: {c['detail'][:160]}")


if __name__ == "__main__":
    main()
