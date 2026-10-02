#!/usr/bin/env python3
"""RTT-003 Best-Selling Consoles 1985-2026 (units shipped): deterministic dataset build.

Usage:  python scripts/build_rtt003_dataset.py data/rtt-003 reports/RTT-003_data_report.md

Inputs (all committed, in data/rtt-003/source/):
  consoles_curated.csv       one row per console considered (in scope or not)
  observations_curated.csv   every figure considered, checked against its source by hand
  nintendo_fy_hardware.csv   Nintendo fiscal-year hardware units (scripts/rtt003_extract_nintendo.py)
  sony_business_data.csv     Sony lifetime totals and PS4/PS5 quarterly sell-in (scripts/rtt003_extract_sony.py)
  report_notes.md            hand-written sections included verbatim in the report
Outputs (data/rtt-003/): consoles.csv, observations.csv, series.csv, series_by_maker.csv,
  crown.csv, overtakes.csv, CHECKS.md, checks.json, manifest.json; and the report.
Method: reference/metric_contract_RTT-003.md. Standard library only; same inputs -> byte-identical outputs.
"""
import csv
import hashlib
import re
import json
import os
import sys
from collections import defaultdict
from datetime import date, timedelta
from fractions import Fraction

BUILD = "rtt003-build/1.1"
START = date(1985, 3, 31)
END = date(2026, 6, 30)
GRADE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}
NINTENDO_PLATFORM = {
    "Family Computer/NES": "nes", "Game Boy": "game_boy", "Super Family Computer/SNES": "snes",
    "Nintendo 64": "nintendo_64", "Game Boy Advance": "game_boy_advance", "Nintendo GameCube": "gamecube",
    "Nintendo DS": "nintendo_ds", "Wii": "wii", "Nintendo 3DS": "nintendo_3ds", "Wii U": "wii_u",
    "Nintendo Switch": "nintendo_switch", "Nintendo Switch 2": "nintendo_switch_2",
}
NINTENDO_XLSX_URL = "https://www.nintendo.co.jp/ir/finance/historical_data/xls/consolidated_sales_e2603.xlsx"
SONY_URL = "https://sonyinteractive.com/en/our-company/business-data-sales/"
OBS_FIELDS = ["obs_id", "console_id", "as_of_date", "date_precision", "units", "qualifier", "lower_bound",
              "figure_type", "basis", "geography", "grade", "analyst", "is_forecast", "is_arithmetic",
              "derivation", "source_title", "publisher", "source_url", "quote", "verified", "accessed",
              "used", "use_reason", "disagrees_with", "ledger_rows", "notes"]


def d(s):
    return date.fromisoformat(s)


def quarter_ends():
    out = []
    for y in range(1985, 2027):
        for m, last in ((3, 31), (6, 30), (9, 30), (12, 31)):
            q = date(y, m, last)
            if START <= q <= END:
                out.append(q)
    return out


def fy_end(label):
    # "FY3/1998" -> 1998-03-31 ; "FY3/2015~" / "FY3/2024~" are aggregates up to the file date
    return date(int(label[4:8]), 3, 31)


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def round_half_up(fr):
    return int((fr + Fraction(1, 2)).__floor__())


def mill(units):
    return f"{units / 1e6:.2f}"


# ---------------------------------------------------------------- generated observations
def nintendo_observations(src, in_scope):
    rows = [r for r in read_csv(os.path.join(src, "nintendo_fy_hardware.csv"))
            if r["model"] == "family"]
    fam = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        cid = NINTENDO_PLATFORM[r["platform"]]
        fam[cid][r["region"]][r["period"]] = r
    obs, checks = [], {}
    for cid in sorted(fam):
        if cid not in in_scope:
            continue
        tot = fam[cid]["Total"]
        ltd = int(tot["LTD"]["units"])
        periods = [p for p in tot if p != "LTD"]
        periods.sort(key=lambda p: (int(p[4:8]), p))
        fy_units = [(p, int(tot[p]["units"]), tot[p]["marker"]) for p in periods]
        markers_total = sum(1 for _, _, m in fy_units if m)
        # one March total per individually reported fiscal year end; aggregates ("~") end the list
        first = fy_end(periods[0])
        pre = ltd - sum(u for _, u, _ in fy_units)
        if first.year <= 1998 and pre > 0:
            obs.append(nin_obs(cid, date(first.year - 1, 3, 31), pre,
                               f"life-to-date {ltd} minus all {len(fy_units)} fiscal-year totals FY3/{first.year}..; "
                               f"{markers_total} under-10,000 markers counted as 0",
                               len(fy_units)))
        for i, (p, u, m) in enumerate(fy_units):
            if p.endswith("~"):
                continue
            later = fy_units[i + 1:]
            val = ltd - sum(v for _, v, _ in later)
            nlater = len(later)
            obs.append(nin_obs(cid, fy_end(p), val,
                               f"life-to-date {ltd} minus later fiscal-year totals ({nlater} columns)"
                               if nlater else f"life-to-date {ltd} (fiscal year {p} is the last column)",
                               nlater))
        if not any(o["obs_id"] == f"NIN-{cid}-2026-03-31" for o in obs):
            obs.append(nin_obs(cid, date(2026, 3, 31), ltd, f"life-to-date total {ltd} as of 31 Mar 2026", 0,
                               ltd_row=True))
        # regional sums vs total (life to date)
        regs = [r for r in ("Japan", "The Americas", "Europe", "Other") if "LTD" in fam[cid][r]]
        reg_sum = sum(int(fam[cid][r]["LTD"]["units"]) for r in regs)
        fy_sum = sum(u for _, u, _ in fy_units)
        checks[cid] = {"ltd": ltd, "fy_sum": fy_sum, "pre_fy_base": pre, "n_fy_columns": len(fy_units),
                       "markers": markers_total, "regional_ltd_sum": reg_sum, "regions": regs,
                       "first_fy": periods[0]}
    return obs, checks


def nin_obs(cid, when, units, derivation, nlater, ltd_row=False):
    tol = nlater * 5000
    return {
        "obs_id": f"NIN-{cid}-{when.isoformat()}", "console_id": cid, "as_of_date": when.isoformat(),
        "date_precision": "day", "units": str(units), "qualifier": "exact", "lower_bound": "no",
        "figure_type": "cumulative", "basis": "consolidated hardware sales units (shipments)",
        "geography": "worldwide", "grade": "A", "analyst": "no", "is_forecast": "no",
        "is_arithmetic": "no" if ltd_row else "yes",
        "derivation": derivation + ("" if ltd_row else f"; rounding tolerance +/-{tol} units"),
        "source_title": "Nintendo Co., Ltd. Consolidated Sales Transition by Region (as of 31 Mar 2026)",
        "publisher": "Nintendo", "source_url": NINTENDO_XLSX_URL,
        "quote": "", "verified": "yes", "accessed": "2026-10-01", "used": "yes",
        "use_reason": "official March year-end total (DEC-086 method)" if not ltd_row else "official life-to-date",
        "notes": "transcribed in source/nintendo_fy_hardware.csv; quote not applicable (spreadsheet cell values)",
    }


def sony_observations(src):
    rows = read_csv(os.path.join(src, "sony_business_data.csv"))
    obs, checks = [], {}
    q_end = {"Q1": (6, 30, 0), "Q2": (9, 30, 0), "Q3": (12, 31, 0), "Q4": (3, 31, 1)}
    for cid in ("playstation_4", "playstation_5"):
        qs = [r for r in rows if r["console_id"] == cid and r["kind"] == "quarterly"]
        fys = {r["fiscal_year"]: Fraction(r["value_millions"]) for r in rows
               if r["console_id"] == cid and r["kind"] == "fiscal_year"}
        run = Fraction(0)
        by_fy = defaultdict(Fraction)
        for r in qs:
            fy = int(r["fiscal_year"][2:])
            m, dd, add = q_end[r["quarter"]]
            when = date(fy + add, m, dd)
            v = Fraction(r["value_millions"])
            run += v
            by_fy[r["fiscal_year"]] += v
            units = round_half_up(run * 1_000_000)
            obs.append({
                "obs_id": f"SONY-QSUM-{cid}-{when.isoformat()}", "console_id": cid,
                "as_of_date": when.isoformat(), "date_precision": "day", "units": str(units),
                "qualifier": "exact", "lower_bound": "no", "figure_type": "cumulative",
                "basis": "sell-in (including returned and refurbished products)", "geography": "worldwide",
                "grade": "A", "analyst": "no", "is_forecast": "no", "is_arithmetic": "yes",
                "derivation": f"running sum of Sony's quarterly sell-in table to {r['fiscal_year']} {r['quarter']} "
                              f"(Sony prints 0.1 million precision: up to +/-0.05m rounding per quarter)",
                "source_title": "Sony Interactive Entertainment - Business Data & Sales", "publisher": "Sony Interactive Entertainment",
                "source_url": SONY_URL, "quote": "", "verified": "yes", "accessed": "2026-10-01", "used": "yes",
                "use_reason": "official quarterly sell-in, summed", "notes": "transcribed in source/sony_business_data.csv",
            })
        checks[cid] = {"quarter_sum_millions": str(run), "fiscal_year_check": {
            fy: {"quarters": str(by_fy[fy]), "printed_fy": str(fys.get(fy, ""))} for fy in sorted(by_fy)}}
    life = {r["console_id"]: r for r in rows if r["kind"] == "lifetime"}
    return obs, checks, life


# ---------------------------------------------------------------- series
def anchors_for(cid, obs_by_console, launch):
    an = [{"date": launch, "units": 0, "grade": "", "obs_id": f"LAUNCH-{cid}", "lower_bound": "no",
           "analyst": "no", "verified": "yes", "is_arithmetic": "no"}]
    seen = {}
    for o in obs_by_console.get(cid, []):
        if o["used"] != "yes":
            continue
        when = d(o["as_of_date"])
        if when in seen:
            raise SystemExit(f"two used figures for {cid} on {when}: {seen[when]} and {o['obs_id']}")
        seen[when] = o["obs_id"]
        an.append({"date": when, "units": int(o["units"]), "grade": o["grade"], "obs_id": o["obs_id"],
                   "lower_bound": o["lower_bound"], "analyst": o["analyst"], "verified": o["verified"],
                   "is_arithmetic": o["is_arithmetic"]})
    an.sort(key=lambda a: a["date"])
    return an


def worst_grade(anchors):
    gs = [a["grade"] for a in anchors if a["grade"]]
    return max(gs, key=lambda g: GRADE_ORDER[g]) if gs else ""


def build_series(consoles, obs_by_console, qends):
    rows = []
    for c in consoles:
        if c["in_scope"] != "yes":
            continue
        cid, launch = c["console_id"], d(c["launch_date"])
        an = anchors_for(cid, obs_by_console, launch)
        for q in qends:
            if q < launch:
                continue
            exact = [a for a in an if a["date"] == q]
            left = [a for a in an if a["date"] <= q][-1]
            right = next((a for a in an if a["date"] > q), None)
            if exact:
                a = exact[0]
                units, gov = a["units"], [a]
                if a["grade"] in ("A", "B"):
                    prov = "arithmetic" if a["is_arithmetic"] == "yes" else "official"
                else:
                    prov = "estimate"
                la, ra, plus = a, None, a["lower_bound"] == "yes"
            elif right is None:
                units, gov, prov, la, ra = left["units"], [left], "held", left, None
                plus = left["lower_bound"] == "yes"
            else:
                span = (right["date"] - left["date"]).days
                frac = Fraction(right["units"] - left["units"]) * (q - left["date"]).days / span
                units = round_half_up(left["units"] + frac)
                gov = [x for x in (left, right) if x["grade"]]
                if right["units"] == left["units"]:
                    prov, plus = "held", left["lower_bound"] == "yes"
                else:
                    prov, plus = "interpolated", False
                la, ra = left, right
            if any(x["analyst"] == "yes" for x in gov):
                style = "analyst_estimate"
            elif any(x["grade"] in ("C", "D") for x in gov):
                style = "estimated"
            elif prov == "interpolated" and (q < date(1994, 1, 1) or (ra["date"] - la["date"]).days > 366):
                style = "estimated"
            else:
                style = "official"
            if style == "official" and c.get("display_override") == "estimated":
                style = "estimated"  # DEC-089: whole bar flagged as estimated
            rows.append({
                "quarter_end": q.isoformat(), "console_id": cid, "units": units, "millions": mill(units),
                "provenance": prov, "grade": worst_grade(gov), "display_style": style,
                "plus_flag": "yes" if plus else "no",
                "unverified_anchor": "yes" if any(x["verified"] != "yes" for x in gov) else "no",
                "left_anchor": la["obs_id"], "left_anchor_date": la["date"].isoformat(),
                "right_anchor": ra["obs_id"] if ra else "", "right_anchor_date": ra["date"].isoformat() if ra else "",
            })
    rows.sort(key=lambda r: (r["quarter_end"], r["console_id"]))
    return rows


def rank_board(series_rows, consoles):
    launch = {c["console_id"]: c["launch_date"] for c in consoles}
    by_q = defaultdict(list)
    for r in series_rows:
        by_q[r["quarter_end"]].append(r)
    first_reach = {}  # (cid, units) -> first quarter it held that value
    hist = defaultdict(list)
    for q in sorted(by_q):
        for r in by_q[q]:
            hist[r["console_id"]].append((q, r["units"]))
    def reached(cid, units, q):
        for qq, u in hist[cid]:
            if u >= units:
                return qq
        return q
    boards = {}
    for q in sorted(by_q):
        rs = [r for r in by_q[q] if r["units"] > 0]
        rs.sort(key=lambda r: (-r["units"], reached(r["console_id"], r["units"], q), launch[r["console_id"]]))
        boards[q] = rs
    return boards


def crown_and_overtakes(boards, top=10):
    qs = sorted(boards)
    crown, overt = [], []
    prev_leader = None
    for i, q in enumerate(qs):
        b = boards[q]
        leader = b[0]
        if prev_leader is None or leader["console_id"] != prev_leader:
            crown.append({"quarter_end": q, "new_leader": leader["console_id"], "previous_leader": prev_leader or "",
                          "leader_millions": leader["millions"], "display_style": leader["display_style"],
                          "provenance": leader["provenance"], "grade": leader["grade"],
                          "unverified_anchor": leader["unverified_anchor"],
                          "previous_leader_millions": next((r["millions"] for r in b if r["console_id"] == prev_leader), ""),
                          "previous_leader_style": next((r["display_style"] for r in b if r["console_id"] == prev_leader), "")})
        prev_leader = leader["console_id"]
        if i == 0:
            continue
        pb = boards[qs[i - 1]]
        prank = {r["console_id"]: k for k, r in enumerate(pb)}
        rank = {r["console_id"]: k for k, r in enumerate(b)}
        rowq = {r["console_id"]: r for r in b}
        prow = {r["console_id"]: r for r in pb}
        for a in b[:top]:
            for x in b[:top]:
                ca, cx = a["console_id"], x["console_id"]
                if rank[ca] < rank[cx] and ca in prank and cx in prank and prank[ca] > prank[cx]:
                    styles = {rowq[ca]["display_style"], rowq[cx]["display_style"],
                              prow[ca]["display_style"], prow[cx]["display_style"]}
                    flag = ("analyst_estimate" if "analyst_estimate" in styles else
                            "estimated" if "estimated" in styles else "official")
                    unv = "yes" if "yes" in (rowq[ca]["unverified_anchor"], rowq[cx]["unverified_anchor"],
                                             prow[ca]["unverified_anchor"], prow[cx]["unverified_anchor"]) else "no"
                    overt.append({"quarter_end": q, "passer": ca, "passed": cx,
                                  "passer_rank_after": rank[ca] + 1, "passed_rank_after": rank[cx] + 1,
                                  "passer_millions": rowq[ca]["millions"], "passed_millions": rowq[cx]["millions"],
                                  "rests_on": flag, "unverified_anchor": unv})
    return crown, overt


# ---------------------------------------------------------------- main
def main():
    out, report_path = sys.argv[1], sys.argv[2]
    src = os.path.join(out, "source")
    consoles = read_csv(os.path.join(src, "consoles_curated.csv"))
    in_scope = {c["console_id"] for c in consoles if c["in_scope"] == "yes"}
    curated = read_csv(os.path.join(src, "observations_curated.csv"))
    nobs, nchecks = nintendo_observations(src, in_scope)
    sobs, schecks, sony_life = sony_observations(src)
    obs = curated + nobs + sobs
    for o in obs:
        for k in OBS_FIELDS:
            o.setdefault(k, "")
    obs.sort(key=lambda o: (o["console_id"], o["as_of_date"], o["obs_id"]))
    ids = [o["obs_id"] for o in obs]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate obs_id")
    obs_by_console = defaultdict(list)
    for o in obs:
        obs_by_console[o["console_id"]].append(o)

    qends = quarter_ends()
    series = build_series(consoles, obs_by_console, qends)
    boards = rank_board(series, consoles)
    crown, overt = crown_and_overtakes(boards)

    # fade dates (DEC-086)
    by_c = defaultdict(list)
    for r in series:
        by_c[r["console_id"]].append(r)
    cons_out = []
    for c in consoles:
        c = dict(c)
        rs = by_c.get(c["console_id"], [])
        if rs:
            c["first_quarter_end"] = rs[0]["quarter_end"]
            c["end_units_2026_06_30"] = str(rs[-1]["units"])
            c["end_provenance"] = rs[-1]["provenance"]
            c["end_display_style"] = rs[-1]["display_style"]
            last_add = None
            for prev, cur in zip(rs, rs[1:]):
                if cur["units"] - prev["units"] >= 10000:
                    last_add = cur["quarter_end"]
            c["last_quarter_adding_shipments"] = last_add or ""
            if c["on_sale_2026"] == "yes":
                c["fade_date"], c["fade_basis"] = "", "still on sale at 30 Jun 2026: no fade"
            elif c["end_event_date"]:
                c["fade_date"] = c["end_event_date"]
                c["fade_basis"] = f"{c['end_event']} ({c['end_event_date']}); DEC-086 rule 1"
            else:
                c["fade_date"] = last_add or ""
                c["fade_basis"] = ("no documented end date: last quarter in this series in which it added at least "
                                   "10,000 units; DEC-086 rule 2")
            best = 99
            for q, b in boards.items():
                for k, r in enumerate(b):
                    if r["console_id"] == c["console_id"]:
                        best = min(best, k + 1)
            c["best_rank"] = str(best)
        cons_out.append(c)

    # bar status (DEC-131, DEC-132, DEC-135): live / latest_figure / retired, per console and quarter end
    qset = [q.isoformat() for q in qends]
    last_fig = defaultdict(str)
    for o in obs:
        if o["used"] == "yes" and len(o["as_of_date"]) == 10:
            last_fig[o["console_id"]] = max(last_fig[o["console_id"]], o["as_of_date"])
    status_of = {}
    for c in cons_out:
        rs = by_c.get(c["console_id"], [])
        c["latest_figure_from"] = c["retired_from"] = c["status_basis"] = ""
        if not rs or c["on_sale_2026"] == "yes":
            if rs:
                c["status_basis"] = "on sale at 30 Jun 2026: live throughout"
            continue
        ret = next((q for q in qset if c["end_event_date"] and q >= c["end_event_date"]), "")
        stop = c["last_quarter_adding_shipments"]
        lat = stop if stop and (not ret or stop < ret) else ""
        c["retired_from"], c["latest_figure_from"] = ret, lat
        why = []
        if lat:
            if last_fig[c["console_id"]] <= lat:
                why.append(f"latest figure from {lat}: our figures run out (last figure {last_fig[c['console_id']]})")
            else:
                why.append(f"latest figure from {lat}: the maker's figures continue (to {last_fig[c['console_id']]}) "
                           "but add under 10,000 units a quarter; no documented end date")
        if ret:
            why.append(f"retired from {ret}: {c['end_event']} ({c['end_event_date']})")
        c["status_basis"] = "; ".join(why)
        status_of[c["console_id"]] = (lat, ret)
    for r in series:
        lat, ret = status_of.get(r["console_id"], ("", ""))
        q = r["quarter_end"]
        r["status"] = "retired" if ret and q >= ret else "latest_figure" if lat and q >= lat else "live"

    # per-maker totals (company scoreboard input)
    maker = {c["console_id"]: c["maker_key"] for c in consoles}
    agg = defaultdict(int)
    for r in series:
        agg[(r["quarter_end"], maker[r["console_id"]])] += r["units"]
    maker_rows = [{"quarter_end": q, "maker_key": m, "units": u, "millions": mill(u)}
                  for (q, m), u in sorted(agg.items())]

    checks, notes = run_checks(consoles, obs, series, qends, nchecks, schecks, sony_life, cons_out)

    os.makedirs(out, exist_ok=True)
    cons_fields = list(consoles[0].keys()) + ["first_quarter_end", "end_units_2026_06_30", "end_provenance",
                                              "end_display_style", "last_quarter_adding_shipments", "fade_date",
                                              "fade_basis", "best_rank", "latest_figure_from", "retired_from",
                                              "status_basis"]
    write_csv(os.path.join(out, "consoles.csv"), cons_out, cons_fields)
    write_csv(os.path.join(out, "observations.csv"), obs, OBS_FIELDS)
    ser_fields = ["quarter_end", "console_id", "units", "millions", "provenance", "grade", "display_style",
                  "plus_flag", "unverified_anchor", "left_anchor", "left_anchor_date", "right_anchor",
                  "right_anchor_date", "status"]
    write_csv(os.path.join(out, "series.csv"), series, ser_fields)
    write_csv(os.path.join(out, "series_by_maker.csv"), maker_rows, ["quarter_end", "maker_key", "units", "millions"])
    write_csv(os.path.join(out, "crown.csv"), crown, list(crown[0].keys()))
    write_csv(os.path.join(out, "overtakes.csv"), overt, list(overt[0].keys()) if overt else ["quarter_end"])
    write_checks(out, checks, notes)
    write_report(report_path, src, consoles, cons_out, obs, series, boards, crown, overt, checks)
    write_manifest(out, report_path)
    ok = all(v["status"] == "PASS" for v in checks.values())
    print(f"{BUILD}: {len(series)} series rows, {len(obs)} observations, crown changes {len(crown) - 1}, "
          f"top-ten overtakes {len(overt)}; checks all PASS: {ok}")


# ---------------------------------------------------------------- checks
def run_checks(consoles, obs, series, qends, nchecks, schecks, sony_life, cons_out):
    checks, notes = {}, {}
    by_c = defaultdict(list)
    for r in series:
        by_c[r["console_id"]].append(r)
    cmap = {c["console_id"]: c for c in consoles}

    # 1 non-decreasing
    dec, big = [], 0
    tol_of = {}
    for o in obs:
        m = re.search(r"rounding tolerance \+/-(\d+)", o["derivation"])
        tol_of[o["obs_id"]] = int(m.group(1)) if m else 0
    for cid, rs in sorted(by_c.items()):
        for a, b in zip(rs, rs[1:]):
            if b["units"] < a["units"]:
                drop = a["units"] - b["units"]
                tol = max(tol_of.get(b["left_anchor"], 0), tol_of.get(a["left_anchor"], 0))
                within = drop <= tol
                big += 0 if within else 1
                dec.append(f"{cid}: {a['quarter_end']} {a['units']} -> {b['quarter_end']} {b['units']} "
                           f"({b['units'] - a['units']} units; anchors {a['left_anchor']} / {b['left_anchor']}; "
                           f"{'within the rebuilt total' + chr(39) + 's rounding tolerance +/-' + str(tol) if within else 'OUTSIDE rounding'})")
    checks["series_non_decreasing"] = {"status": "PASS" if big == 0 else "REVIEW",
                                       "detail": f"{len(dec)} decreases, {len(dec) - big} within documented rounding (listed below), {big} outside"}
    notes["decreases"] = dec

    # 2 Nintendo fiscal-year sums vs life-to-date
    nfail, ndet = [], []
    for cid, ch in sorted(nchecks.items()):
        tol = 5000 * ch["n_fy_columns"]
        if int(ch["first_fy"][4:8]) > 1998:
            diff = ch["fy_sum"] - ch["ltd"]
            ok = abs(diff) <= tol
            ndet.append(f"{cid}: sum of {ch['n_fy_columns']} fiscal-year totals {ch['fy_sum']} vs life-to-date "
                        f"{ch['ltd']} (difference {diff}, tolerance +/-{tol}) {'OK' if ok else 'OUTSIDE'}")
            if not ok:
                nfail.append(cid)
        else:
            ndet.append(f"{cid}: life-to-date {ch['ltd']} minus {ch['n_fy_columns']} fiscal years from "
                        f"{ch['first_fy']} = {ch['pre_fy_base']} at 31 Mar {int(ch['first_fy'][4:8]) - 1} "
                        f"(compared with older figures in the report)")
        rdiff = ch["regional_ltd_sum"] - ch["ltd"]
        rtol = 5000 * len(ch["regions"])
        okr = abs(rdiff) <= rtol
        ndet.append(f"{cid}: regions {'+'.join(ch['regions'])} = {ch['regional_ltd_sum']} vs total {ch['ltd']} "
                    f"(difference {rdiff}, tolerance +/-{rtol}) {'OK' if okr else 'OUTSIDE'}")
        if not okr:
            nfail.append(cid + " regions")
    checks["nintendo_fiscal_years_vs_lifetime"] = {"status": "PASS" if not nfail else "FAIL",
                                                   "detail": f"{len(nchecks)} families; outside rounding: {nfail}"}
    notes["nintendo"] = ndet

    # 3 Sony PS4/PS5 sums vs headlines
    sfail, sdet = [], []
    for cid, ch in schecks.items():
        tot = Fraction(ch["quarter_sum_millions"])
        head = Fraction(sony_life[cid]["value_millions"])
        ok = tot > head and tot - head < Fraction(1)
        sdet.append(f"{cid}: quarterly sell-in sums to {float(tot):.1f}m; Sony headline 'More than "
                    f"{sony_life[cid]['value_millions']} million' (as of {sony_life[cid]['as_of']}) {'OK' if ok else 'FAIL'}")
        if not ok:
            sfail.append(cid)
        for fy, v in ch["fiscal_year_check"].items():
            if v["printed_fy"] and Fraction(v["quarters"]) != Fraction(v["printed_fy"]):
                sdet.append(f"{cid} {fy}: quarters sum {float(Fraction(v['quarters'])):.1f} vs printed fiscal year {float(Fraction(v['printed_fy'])):.1f} (Sony's rounding)")
    checks["sony_ps4_ps5_sums_vs_headlines"] = {"status": "PASS" if not sfail else "FAIL", "detail": "; ".join(sdet[:2])}
    notes["sony"] = sdet

    # 4 no value before launch
    bad = [f"{r['console_id']} {r['quarter_end']}" for r in series if d(r["quarter_end"]) < d(cmap[r["console_id"]]["launch_date"])]
    checks["no_value_before_launch"] = {"status": "PASS" if not bad else "FAIL", "detail": f"{len(bad)} rows"}

    # 5 every point has provenance and an anchor
    badp = [r for r in series if r["provenance"] not in ("official", "arithmetic", "interpolated", "estimate", "held")
            or not r["left_anchor"] or r["display_style"] not in ("official", "estimated", "analyst_estimate")]
    checks["every_point_has_provenance"] = {"status": "PASS" if not badp else "FAIL", "detail": f"{len(series)} rows checked"}

    # 6 end values equal the latest official figures
    end_det, end_fail = [], []
    for cid, rs in sorted(by_c.items()):
        end = rs[-1]["units"]
        offs = [o for o in obs if o["console_id"] == cid and o["grade"] in ("A", "B") and o["is_forecast"] != "yes"
                and o["figure_type"] in ("cumulative", "lifetime") and o["as_of_date"][:4].isdigit()
                and len(o["as_of_date"]) == 10 and o["verified"] == "yes"]
        if not offs:
            end_det.append(f"{cid}: no verified official dated figure (end {end}, {rs[-1]['display_style']})")
            continue
        latest_date = max(o["as_of_date"] for o in offs)
        latest = [o for o in offs if o["as_of_date"] == latest_date]
        lo = sorted(latest, key=lambda o: (o["used"] != "yes", o["obs_id"]))[0]
        v = int(lo["units"])
        if lo["lower_bound"] == "yes":
            ok = end >= v
            rel = ">="
        else:
            ok = end == v
            rel = "=="
        if cmap[cid].get("analyst_after") and latest_date <= cmap[cid]["analyst_after"] and end >= v:
            end_det.append(f"{cid}: end {end} rests on the analyst estimate {rs[-1]['left_anchor']} (DEC-084); "
                           f"latest official figure {v} ({lo['obs_id']}, {latest_date}) is below it: consistent")
            continue
        end_det.append(f"{cid}: end {end} {rel} latest official {v} ({lo['obs_id']}, {latest_date}) "
                       f"{'OK' if ok else 'MISMATCH'}")
        if not ok:
            end_fail.append(cid)
    checks["end_values_equal_latest_official"] = {"status": "PASS" if not end_fail else "FAIL",
                                                  "detail": f"mismatches: {end_fail}"}
    notes["end_values"] = end_det

    # 7 excluded consoles absent
    excl = {c["console_id"] for c in consoles if c["in_scope"] != "yes"}
    present = sorted({r["console_id"] for r in series} & excl)
    checks["excluded_consoles_absent"] = {"status": "PASS" if not present else "FAIL",
                                          "detail": f"{len(excl)} excluded; present in series: {present}"}

    # 8 observation integrity
    probs = []
    for o in obs:
        if o["used"] == "yes":
            if o["is_forecast"] == "yes":
                probs.append(f"{o['obs_id']} forecast used")
            if o["figure_type"] not in ("cumulative", "lifetime"):
                probs.append(f"{o['obs_id']} non-cumulative used")
            if len(o["as_of_date"]) != 10:
                probs.append(f"{o['obs_id']} undated used")
            if o["console_id"] not in {c["console_id"] for c in consoles if c["in_scope"] == "yes"}:
                probs.append(f"{o['obs_id']} out-of-scope console used")
        if o["verified"] not in ("yes", "no", "UNVERIFIED"):
            probs.append(f"{o['obs_id']} verified={o['verified']}")
        if not o["source_url"]:
            probs.append(f"{o['obs_id']} no source URL")
        if o["used"] not in ("yes", "no") or not o["use_reason"]:
            probs.append(f"{o['obs_id']} used/why missing")
        if o["grade"] not in GRADE_ORDER:
            probs.append(f"{o['obs_id']} grade {o['grade']}")
        if len(o["quote"].split()) > 24:
            probs.append(f"{o['obs_id']} quote over 24 words")
    checks["observations_integrity"] = {"status": "PASS" if not probs else "FAIL", "detail": f"{len(obs)} observations; {len(probs)} problems"}
    notes["observation_problems"] = probs

    # 9 grid complete
    gaps = []
    for c in consoles:
        if c["in_scope"] != "yes":
            continue
        want = [q.isoformat() for q in qends if q >= d(c["launch_date"])]
        have = [r["quarter_end"] for r in by_c[c["console_id"]]]
        if want != have:
            gaps.append(c["console_id"])
    checks["quarter_grid_complete"] = {"status": "PASS" if not gaps else "FAIL",
                                       "detail": f"{len(qends)} quarter ends {qends[0]}..{qends[-1]}; incomplete: {gaps}"}

    # 10 bar status (DEC-131, DEC-132): retired only from a documented end date; live while on sale; never back to live
    sbad, moved = [], []
    cout = {c["console_id"]: c for c in cons_out}
    for cid, rs in sorted(by_c.items()):
        c = cout[cid]
        prev = "live"
        for r in rs:
            st = r["status"]
            if st == "retired" and not (c["end_event_date"] and r["quarter_end"] >= c["end_event_date"]):
                sbad.append(f"{cid} {r['quarter_end']} retired without a documented end date")
            if c["on_sale_2026"] == "yes" and st != "live":
                sbad.append(f"{cid} {r['quarter_end']} on sale but {st}")
            if prev != "live" and st == "live":
                sbad.append(f"{cid} {r['quarter_end']} back to live")
            if prev == "retired" and st == "latest_figure":
                sbad.append(f"{cid} {r['quarter_end']} retired -> latest figure")
            prev = st
        first = next((r for r in rs if r["status"] != "live"), None)
        if first and rs[-1]["units"] != first["units"]:
            moved.append(f"{cid}: {first['status']} from {first['quarter_end']} at {first['units']} units; "
                         f"{rs[-1]['units'] - first['units']} more units by {rs[-1]['quarter_end']} (each quarter under 10,000)")
    checks["bar_status_rules"] = {"status": "PASS" if not sbad else "FAIL",
                                  "detail": f"{sum(1 for r in series if r['status'] == 'latest_figure')} latest-figure rows, "
                                            f"{sum(1 for r in series if r['status'] == 'retired')} retired rows; problems: {sbad[:5]}"}
    notes["status_moves"] = moved
    return checks, notes


def write_checks(out, checks, notes):
    with open(os.path.join(out, "checks.json"), "w", encoding="utf-8") as f:
        json.dump({"build": BUILD, "checks": checks, "notes": notes}, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    allpass = all(v["status"] == "PASS" for v in checks.values())
    L = [f"# RTT-003 scripted checks", "", f"Build `{BUILD}`. All checks PASS: **{allpass}**. "
         "A check marked REVIEW found something that is reported in full below, not hidden.", "",
         "| Check | Result | Detail |", "|---|---|---|"]
    for k, v in checks.items():
        L.append(f"| {k} | {v['status']} | {v['detail']} |")
    titles = {"decreases": "Decreases in any series (reported, not hidden)",
              "nintendo": "Nintendo fiscal-year sums and regional sums vs life-to-date",
              "sony": "Sony PS4 / PS5 quarterly sums vs Sony's headlines",
              "end_values": "End values (30 Jun 2026) vs the latest verified official figure",
              "observation_problems": "Observation integrity problems",
              "status_moves": "Bars that still add a little after they are labelled (latest figure / retired)"}
    for k, t in titles.items():
        L += ["", f"## {t}", ""]
        items = notes.get(k, [])
        L += [f"- {x}" for x in items] if items else ["- none"]
    with open(os.path.join(out, "CHECKS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


# ---------------------------------------------------------------- report
STYLE_WORD = {"official": "official", "estimated": "estimated", "analyst_estimate": "analyst estimate"}


def write_report(path, src, consoles, cons_out, obs, series, boards, crown, overt, checks):
    name = {c["console_id"]: c["display_name"].replace("|", "\\|") for c in consoles}   # "Xbox Series X|S" inside tables
    L = ["# RTT-003 data report — Best-Selling Consoles 1985–2026 (units shipped)", "",
         f"Generated by `scripts/build_rtt003_dataset.py` ({BUILD}). Data: `data/rtt-003/`. "
         "Contract: `reference/metric_contract_RTT-003.md`. Figures in millions of units shipped (sell-in).", "",
         "Key: **official** = the bar rests only on manufacturer figures; **estimated** = it rests on a press "
         "or estimated figure, or on a straight line across a long or pre-1994 gap; **analyst estimate** = Xbox "
         "One / Series X|S figures from analysts (DEC-084). `+` = lower bound (\"more than\"). "
         "`(U)` = rests on a figure whose source was blocked (UNVERIFIED).", ""]
    notes_md = open(os.path.join(src, "report_notes.md"), encoding="utf-8").read()
    parts = notes_md.split("<!-- SPLIT -->")
    L += [parts[0].strip(), ""]

    L += ["## Checks", "", "| Check | Result |", "|---|---|"]
    L += [f"| {k} | {v['status']} — {v['detail']} |" for k, v in checks.items()]
    L += ["", "Full detail: `data/rtt-003/CHECKS.md`.", ""]

    L += ["## Top-12 boards", "",
          "Opening board 31 Mar 1985 (the race starts there), then 31 December of each year shown, then the last "
          "quarter, 30 Jun 2026.", ""]
    dates = ["1985-03-31", "1990-12-31", "1995-12-31", "2000-12-31", "2005-12-31", "2010-12-31", "2015-12-31",
             "2020-12-31", "2026-06-30"]
    for q in dates:
        L += [f"### {q}", "", "| # | Console | Millions | Shown as | Rests on |", "|---|---|---|---|---|"]
        for k, r in enumerate(boards[q][:12]):
            plus = "+" if r["plus_flag"] == "yes" else ""
            u = " (U)" if r["unverified_anchor"] == "yes" else ""
            L.append(f"| {k + 1} | {name[r['console_id']]} | {r['millions']}{plus} | "
                     f"{STYLE_WORD[r['display_style']]}{u} | {r['provenance']}, grade {r['grade'] or '-'} |")
        if len(boards[q]) < 12:
            L.append(f"| | ({len(boards[q])} consoles in scope on sale by this date) | | | |")
        L.append("")

    L += ["## Crown: every change of first place", "",
          "| Quarter end | New leader | Millions | Previous leader | Its millions | Rests on |", "|---|---|---|---|---|---|"]
    for c in crown:
        rest = STYLE_WORD[c["display_style"]]
        if c["previous_leader_style"] and c["previous_leader_style"] != c["display_style"]:
            rest += f" / {STYLE_WORD[c['previous_leader_style']]}"
        if c["unverified_anchor"] == "yes":
            rest += " (U)"
        L.append(f"| {c['quarter_end']} | {name[c['new_leader']]} | {c['leader_millions']} | "
                 f"{name.get(c['previous_leader'], '— (race start)')} | {c['previous_leader_millions'] or '—'} | {rest} |")
    L += ["", "## Overtakes inside the top ten", "",
          "Every quarter in which one console passed another and both were in the top ten afterwards.", "",
          "| Quarter end | Passer | Passed | Ranks after | Millions | Rests on |", "|---|---|---|---|---|---|"]
    for o in overt:
        u = " (U)" if o["unverified_anchor"] == "yes" else ""
        L.append(f"| {o['quarter_end']} | {name[o['passer']]} | {name[o['passed']]} | {o['passer_rank_after']} / "
                 f"{o['passed_rank_after']} | {o['passer_millions']} vs {o['passed_millions']} | "
                 f"{STYLE_WORD[o['rests_on']]}{u} |")
    n_off = sum(1 for o in overt if o["rests_on"] == "official")
    L += ["", f"{len(overt)} overtakes: {n_off} official, {len(overt) - n_off} resting on estimated or analyst figures.", ""]

    L += ["## Disagreements between sources", "",
          "Figures recorded but not used because a higher-grade source for the same date (or a consistent series) "
          "says something else. Never averaged.", "",
          "| Console | Date | Not used | Used instead / compared with | Grade | Source | Why |", "|---|---|---|---|---|---|---|"]
    obs_id = {o["obs_id"]: o for o in obs}
    for o in obs:
        if o["used"] == "no" and o["use_reason"].startswith("disagreement"):
            other = obs_id.get(o["disagrees_with"])
            ov = f"{mill(int(other['units']))} ({other['obs_id']})" if other and other["units"] else o["disagrees_with"]
            L.append(f"| {name.get(o['console_id'], o['console_id'])} | {o['as_of_date']} | {mill(int(o['units']))} | "
                     f"{ov} | {o['grade']} | {o['publisher']} | {o['use_reason']} |")
    L += ["", "## UNVERIFIED items (source blocked from this environment)", "",
          f"`used = yes` means a bar rests on it: {sum(1 for o in obs if o['verified'] == 'UNVERIFIED' and o['used'] == 'yes')} "
          "at present. The others are recorded for completeness (superseded, consistent, out of scope or not needed).", "",
          "| Obs | Console | Date | Millions | Used | Source URL |", "|---|---|---|---|---|---|"]
    for o in obs:
        if o["verified"] == "UNVERIFIED":
            L.append(f"| {o['obs_id']} | {name.get(o['console_id'], o['console_id'])} | {o['as_of_date']} | "
                     f"{mill(int(o['units'])) if o['units'] else '—'} | {o['used']} | {o['source_url']} |")
    L += ["", "## What each console's bar is based on", "",
          "| Console | Launch | Anchors used (date: millions, grade) | End 30 Jun 2026 | Fade |", "|---|---|---|---|---|"]
    for c in cons_out:
        if c["in_scope"] != "yes":
            continue
        an = [o for o in obs if o["console_id"] == c["console_id"] and o["used"] == "yes"]
        if len(an) > 8:
            txt = (f"{len(an)} anchors, {an[0]['as_of_date']} to {an[-1]['as_of_date']}; grades "
                   + ",".join(sorted({o['grade'] for o in an})))
        else:
            txt = "; ".join(f"{o['as_of_date']}: {mill(int(o['units']))}{'+' if o['lower_bound'] == 'yes' else ''} "
                            f"{o['grade']}{' (U)' if o['verified'] == 'UNVERIFIED' else ''}" for o in an)
        L.append(f"| {name[c['console_id']]} | {c['launch_date']} | {txt} | {mill(int(c['end_units_2026_06_30']))} "
                 f"({STYLE_WORD[c['end_display_style']]}) | {c['fade_date'] or '—'} |")
    L += ["", "## Retired and latest-figure bars (DEC-131, DEC-132)", "",
          "A bar is labelled **retired** only from the first quarter end on or after a documented end date. A bar that "
          "stops without a documented end date is labelled **latest figure** from the last quarter in which it added at "
          "least 10,000 units (DEC-135). Both are lightly dimmed. Consoles on sale at 30 Jun 2026 are live throughout.", "",
          "| Console | Latest figure | Retired | Basis |", "|---|---|---|---|"]
    for c in cons_out:
        if c["in_scope"] != "yes" or not (c.get("latest_figure_from") or c.get("retired_from")):
            continue
        lat, ret = c["latest_figure_from"], c["retired_from"]
        span = ((f"{lat} only" if qprev(ret) == lat else f"{lat} to {qprev(ret)}") if ret else f"from {lat}") if lat else "—"
        L.append(f"| {name[c['console_id']]} | {span} | {('from ' + ret) if ret else '—'} | {c['status_basis']} |")
    spl = [o for o in obs if "SPLICE" in o["use_reason"]]
    if spl:
        L += ["", "## Splices (a change of source or basis inside one bar)", "", "| Console | Date | Figure | Source | Note |", "|---|---|---|---|---|"]
        for o in spl:
            L.append(f"| {name.get(o['console_id'], o['console_id'])} | {o['as_of_date']} | {mill(int(o['units']))} | "
                     f"{o['publisher']} | {o['use_reason']} |")
    L += ["", "## Consoles considered and left out", "", "| Console | Why |", "|---|---|"]
    for c in cons_out:
        if c["in_scope"] != "yes":
            L.append(f"| {c['display_name']} | {c['scope_reason']} |")
    if len(parts) > 1:
        L += ["", parts[1].strip()]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def qprev(q):
    """The quarter end before q (q is a quarter end, ISO)."""
    y, m = int(q[:4]), int(q[5:7])
    y, m = (y - 1, 12) if m == 3 else (y, m - 3)
    return date(y, m, {3: 31, 6: 30, 9: 30, 12: 31}[m]).isoformat()


def write_manifest(out, report_path):
    def h(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    src = os.path.join(out, "source")
    m = {"dataset": "RTT-003 Best-Selling Consoles 1985-2026 (units shipped)", "build": BUILD,
         "metric_contract": "reference/metric_contract_RTT-003.md v1.0",
         "range": {"first_quarter_end": START.isoformat(), "last_quarter_end": END.isoformat()},
         "inputs": {f"source/{n}": h(os.path.join(src, n)) for n in sorted(os.listdir(src))},
         "outputs": {n: h(os.path.join(out, n)) for n in
                     ("consoles.csv", "observations.csv", "series.csv", "series_by_maker.csv", "crown.csv",
                      "overtakes.csv", "CHECKS.md", "checks.json")},
         "report": {report_path: h(report_path)}}
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
