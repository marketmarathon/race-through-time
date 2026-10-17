#!/usr/bin/env python3
"""RTT-104 Women in Parliament (IQ-20): build the data for the top 10 vs bottom 10 split race, 1997-2025.

Usage: python3 scripts/build_rtt104_dataset.py <data_dir> <report_path>
       (normally: python3 scripts/build_rtt104_dataset.py data/rtt-104 reports/RTT-104_data_report.md)

Deterministic: reads only files under <data_dir>/source/ and <data_dir>/config.json; writes no timestamps.
Standard library only. Every figure comes from the World Bank WDI API files fetched on a GitHub runner
(SG.GEN.PARL.ZS, producer the Inter-Parliamentary Union; SP.POP.TOTL). Nothing is filled, averaged or forecast:
the only shown value that is not that year's own WDI figure is a single missing year inside a run, which shows the
previous year's figure marked "latest figure" (DEC-617). Rules: DEC-600..DEC-605, DEC-611..DEC-613 (owner),
DEC-616..DEC-620 (Claude working choices under DEC-417).
"""
import csv
import hashlib
import io
import json
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

ZERO = Decimal(0)


# ---------------------------------------------------------------- inputs
def load_json(path):
    # numbers kept as their exact text, so every value can be traced to the raw file (check C1)
    with open(path, encoding="utf-8") as f:
        return json.load(f, parse_float=str, parse_int=str)


def load_inputs(data_dir):
    cfg = json.load(open(os.path.join(data_dir, "config.json"), encoding="utf-8"))
    raw = os.path.join(data_dir, cfg["source_raw_dir"])
    ctry = load_json(os.path.join(raw, "wdi_country_list.json"))[1]
    economies = {}
    for c in ctry:
        if c["region"]["id"] == "NA":  # aggregates (World, regions, income groups) have no region
            continue
        economies[c["id"]] = {"iso3": c["id"], "iso2": c["iso2Code"], "wb_name": c["name"],
                              "region": c["region"]["value"].strip(), "income": c["incomeLevel"]["value"].strip()}
    parl, pop = {}, {}
    for r in load_json(os.path.join(raw, "wdi_SG.GEN.PARL.ZS_all_1997-2025.json"))[1]:
        if r["countryiso3code"] in economies and r["value"] is not None:
            parl.setdefault(r["countryiso3code"], {})[int(r["date"])] = r["value"]
    for r in load_json(os.path.join(raw, "wdi_SP.POP.TOTL_all_1997-2026.json"))[1]:
        if r["countryiso3code"] in economies and r["value"] is not None:
            pop.setdefault(r["countryiso3code"], {})[int(r["date"])] = r["value"]
    wld = {int(r["date"]): r["value"] for r in load_json(os.path.join(raw, "wdi_SG.GEN.PARL.ZS_WLD_1997-2025.json"))[1]
           if r["value"] is not None}
    wld_all = {int(r["date"]): r["value"] for r in load_json(os.path.join(raw, "wdi_SG.GEN.PARL.ZS_all_1997-2025.json"))[1]
               if r["countryiso3code"] == "WLD" and r["value"] is not None}
    owid = list(csv.DictReader(open(os.path.join(raw, "owid_share-of-women-in-parliament-ipu.csv"), encoding="utf-8")))
    names = {r["iso3"]: r for r in csv.DictReader(open(os.path.join(data_dir, "source", "short_names.csv"), encoding="utf-8"))}
    reasons = {r["iso3"]: r for r in csv.DictReader(open(os.path.join(data_dir, "source", "closing_card_reasons.csv"), encoding="utf-8"))}
    for iso3, e in economies.items():
        n = names.get(iso3)
        if n and n["wb_name"] != e["wb_name"]:
            raise SystemExit(f"short_names.csv: {iso3} World Bank name is {e['wb_name']!r}, file says {n['wb_name']!r}")
        e["short_name"] = n["short_name"] if n else e["wb_name"]
    return cfg, raw, economies, parl, pop, wld, wld_all, owid, reasons


def one_dp(v):
    return str(Decimal(v).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def pop_latest(pop_c):
    if not pop_c:
        return None, None
    y = max(pop_c)
    return y, pop_c[y]


# ---------------------------------------------------------------- rules
def display_values(parl_c, years):
    """year -> (value text or None, kind, carried_from). DEC-617: one missing year with a figure on both sides shows the
    previous figure marked 'latest figure'; any other gap is off the board."""
    out = {}
    have = sorted(parl_c)
    for y in years:
        if y in parl_c:
            out[y] = (parl_c[y], "figure", "")
        elif (y - 1) in parl_c and (y + 1) in parl_c:
            out[y] = (parl_c[y - 1], "latest_figure", str(y - 1))
        elif not have:
            out[y] = (None, "no_figures", "")
        elif y < have[0]:
            out[y] = (None, "before_first_figure", "")
        elif y > have[-1]:
            out[y] = (None, "after_last_figure", "")
        else:
            out[y] = (None, "gap_off_board", "")
    return out


def eligible(economies, pop, threshold):
    out = {}
    for iso3 in economies:
        y, p = pop_latest(pop.get(iso3, {}))
        out[iso3] = p is not None and Decimal(p) >= threshold
    return out


def build_boards(cfg, economies, disp, elig, years):
    n = cfg["board_size"]
    boards, zero_groups, ties = [], [], []
    for y in years:
        cand = [(Decimal(disp[c][y][0]), economies[c]["short_name"], c) for c in economies
                if elig[c] and disp[c][y][0] is not None]
        zeros = sorted((c for c in cand if c[0] == ZERO), key=lambda t: t[1])
        top = sorted(cand, key=lambda t: (-t[0], t[1]))
        bottom = sorted((c for c in cand if c[0] > ZERO), key=lambda t: (t[0], t[1]))
        zero_groups.append((y, zeros, len(cand)))
        for board, lst in (("top", top), ("bottom", bottom)):
            for i, (v, name, c) in enumerate(lst[:n], 1):
                kind, frm = disp[c][y][1], disp[c][y][2]
                boards.append({"year": y, "board": board, "rank": i, "iso3": c, "country": name,
                               "value": disp[c][y][0], "value_1dp": one_dp(disp[c][y][0]),
                               "latest_figure": "yes" if kind == "latest_figure" else "no", "carried_from_year": frm})
            for i in range(min(len(lst), n + 1) - 1):  # ranks 1..11: any exact tie that could change order or membership
                if lst[i][0] == lst[i + 1][0]:
                    ties.append({"year": y, "board": board, "ranks": f"{i + 1}-{i + 2}", "value": str(lst[i][0]),
                                 "countries": f"{lst[i][1]}; {lst[i + 1][1]}",
                                 "effect": "membership (rank 10/11)" if i + 1 == n else "order only"})
    return boards, zero_groups, ties


def events(boards, years):
    rows = []
    by = {}
    for b in boards:
        by.setdefault((b["board"], b["year"]), []).append(b)
    for board in ("top", "bottom"):
        prev_first, prev_set = None, set()
        for y in years:
            lst = by.get((board, y), [])
            first = lst[0]["country"] if lst else ""
            cur = {b["country"] for b in lst}
            if first != prev_first:
                rows.append({"year": y, "board": board, "event": "first_place", "country": first,
                             "detail": f"{'highest' if board == 'top' else 'lowest above 0%'}; was {prev_first or '-'}",
                             "value": lst[0]["value_1dp"] if lst else ""})
            if y != years[0]:
                for c in sorted(cur - prev_set):
                    v = next(b for b in lst if b["country"] == c)
                    rows.append({"year": y, "board": board, "event": "enters", "country": c,
                                 "detail": f"rank {v['rank']}", "value": v["value_1dp"]})
                for c in sorted(prev_set - cur):
                    rows.append({"year": y, "board": board, "event": "leaves", "country": c, "detail": "", "value": ""})
            prev_first, prev_set = first, cur
    return rows


def compare_owid(economies, parl, wld, owid):
    """Every cell where WDI (World Bank API) and OWID's grapher CSV differ. OWID prints 6 decimals."""
    vcol = "Proportion of seats held by women in national parliaments (%)"
    ow = {}
    for r in owid:
        code = "WLD" if r["Code"] == "OWID_WRL" else r["Code"]
        if r[vcol] != "":
            ow[(code, int(r["Year"]))] = r[vcol]
    wb = {(c, y): v for c, ys in parl.items() for y, v in ys.items()}
    wb.update({("WLD", y): v for y, v in wld.items()})
    diffs = []
    for k in sorted(set(wb) | set(ow)):
        code, y = k
        if code not in economies and code != "WLD":
            continue  # OWID's own aggregates and entities with no World Bank code
        a, b = wb.get(k), ow.get(k)
        if a is None or b is None:
            diffs.append({"iso3": code, "year": y, "wdi": a or "", "owid": b or "",
                          "difference": "only in WDI" if b is None else "only in OWID", "amount": ""})
        elif abs(Decimal(a) - Decimal(b)) > Decimal("0.0000005"):
            d = Decimal(a) - Decimal(b)
            diffs.append({"iso3": code, "year": y, "wdi": a, "owid": b,
                          "difference": "rounding" if abs(d) < Decimal("0.00001") else "value",
                          "amount": format(d.normalize(), "f")})
    owid_only_codes = sorted({c for (c, y) in ow if c not in economies and c != "WLD"})
    return diffs, owid_only_codes, len([k for k in wb if k in ow])


# ---------------------------------------------------------------- output helpers
def write_csv(path, rows, fields):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# ---------------------------------------------------------------- main build
def build(data_dir, report_path):
    cfg, raw, economies, parl, pop, wld, wld_all, owid, reasons = load_inputs(data_dir)
    years = list(range(cfg["first_year"], cfg["last_year"] + 1))
    T = Decimal(cfg["population_threshold"])
    T2 = Decimal(cfg["population_threshold_alternative"])
    disp = {c: display_values(parl.get(c, {}), years) for c in economies}
    elig = eligible(economies, pop, T)
    elig2 = eligible(economies, pop, T2)

    # countries.csv
    crow = []
    for c in sorted(economies, key=lambda c: economies[c]["short_name"]):
        e = economies[c]
        py, pv = pop_latest(pop.get(c, {}))
        ys = sorted(parl.get(c, {}))
        crow.append({"iso3": c, "iso2": e["iso2"], "short_name": e["short_name"], "wb_name": e["wb_name"],
                     "region": e["region"], "income": e["income"], "population_latest": pv or "",
                     "population_year": py or "", "in_race": "yes" if elig[c] else "no",
                     "in_race_at_2_5m": "yes" if elig2[c] else "no",
                     "first_figure_year": ys[0] if ys else "", "last_figure_year": ys[-1] if ys else "",
                     "years_with_figure": len(ys)})
    write_csv(os.path.join(data_dir, "countries.csv"), crow, list(crow[0]))

    # boards (4 m = the rule; 2.5 m comparison only)
    boards, zgroups, ties = build_boards(cfg, economies, disp, elig, years)
    boards2, zgroups2, ties2 = build_boards(cfg, economies, disp, elig2, years)
    on_board = {(b["iso3"], b["year"]): b["board"] for b in boards}
    write_csv(os.path.join(data_dir, "boards.csv"), boards, list(boards[0]))
    write_csv(os.path.join(data_dir, "boards_2_5m_comparison.csv"), boards2, list(boards2[0]))
    zg_rows = [{"year": y, "count": len(z), "countries": "; ".join(t[1] for t in z), "countries_with_a_value": n}
               for y, z, n in zgroups]
    write_csv(os.path.join(data_dir, "zero_group.csv"), zg_rows, list(zg_rows[0]))
    tie_fields = ["year", "board", "ranks", "value", "countries", "effect"]
    write_csv(os.path.join(data_dir, "ties.csv"), ties, tie_fields)

    # series.csv: every economy x year
    srows = []
    for c in sorted(economies, key=lambda c: economies[c]["short_name"]):
        for y in years:
            v = parl.get(c, {}).get(y)
            dv, kind, frm = disp[c][y]
            py = pop.get(c, {}).get(y)
            srows.append({
                "iso3": c, "country": economies[c]["short_name"], "year": y,
                "wdi_value": v if v is not None else "", "status": "VERIFIED" if v is not None else "MISSING",
                "shown_value": dv if dv is not None else "", "shown_value_1dp": one_dp(dv) if dv is not None else "",
                "shown_as": kind, "carried_from_year": frm,
                "missing": "yes" if v is None else "no", "zero": "yes" if (v is not None and Decimal(v) == ZERO) else "no",
                "below_threshold": "no" if elig[c] else "yes",
                "population_that_year": py or "",
                "below_threshold_that_year": "" if py is None else ("yes" if Decimal(py) < T else "no"),
                "on_board": on_board.get((c, y), ""),
                "in_zero_group": "yes" if elig[c] and dv is not None and Decimal(dv) == ZERO else "no"})
    write_csv(os.path.join(data_dir, "series.csv"), srows, list(srows[0]))

    # world panel
    wrows = [{"year": y, "label": "World (all countries)", "wdi_value": wld.get(y, ""),
              "value_1dp": one_dp(wld[y]) if y in wld else ""} for y in years]
    write_csv(os.path.join(data_dir, "world.csv"), wrows, list(wrows[0]))

    # closing card (DEC-603, DEC-613): in the race, no figure in the last year, at least one earlier figure
    last = cfg["last_year"]
    cc = []
    for c in sorted(economies, key=lambda c: economies[c]["short_name"]):
        ys = sorted(parl.get(c, {}))
        if not elig[c] or not ys or last in parl[c]:
            continue
        r = reasons.get(c, {})
        status = r.get("status", "NOT FOUND") or "NOT FOUND"
        cc.append({"iso3": c, "country": economies[c]["short_name"], "last_figure_year": ys[-1],
                   "last_figure_1dp": one_dp(parl[c][ys[-1]]), "on_card": "yes" if status == "VERIFIED" else "no",
                   "card_wording": r.get("card_wording", ""), "status": status, "source_url": r.get("source_url", ""),
                   "quote": r.get("quote", ""), "note": r.get("note", "")})
    write_csv(os.path.join(data_dir, "closing_card.csv"), cc,
              ["iso3", "country", "last_figure_year", "last_figure_1dp", "on_card", "card_wording", "status",
               "source_url", "quote", "note"])

    ev = events(boards, years)
    write_csv(os.path.join(data_dir, "events.csv"), ev, ["year", "board", "event", "country", "detail", "value"])

    diffs, owid_only, n_common = compare_owid(economies, parl, wld, owid)
    write_csv(os.path.join(data_dir, "wdi_owid_differences.csv"), diffs, ["iso3", "year", "wdi", "owid", "difference", "amount"])

    checks = run_checks(raw, economies, parl, pop, srows, boards, zgroups, wrows, wld, wld_all, T, years)
    json.dump(checks, open(os.path.join(data_dir, "checks.json"), "w", encoding="utf-8"), indent=1, sort_keys=True)

    write_report(report_path, cfg, raw, economies, parl, pop, disp, elig, elig2, boards, boards2, zgroups, zgroups2,
                 ties, ties2, ev, wrows, cc, diffs, owid_only, n_common, checks, years, T, T2)

    outputs = ["countries.csv", "series.csv", "boards.csv", "boards_2_5m_comparison.csv", "zero_group.csv", "ties.csv",
               "world.csv", "closing_card.csv", "events.csv", "wdi_owid_differences.csv", "checks.json"]
    inputs = sorted(os.path.join(cfg["source_raw_dir"], f) for f in os.listdir(raw)) + \
        ["config.json", "source/short_names.csv", "source/closing_card_reasons.csv"]
    manifest = {"build": "scripts/build_rtt104_dataset.py", "inputs": {p: sha(os.path.join(data_dir, p)) for p in inputs},
                "outputs": {p: sha(os.path.join(data_dir, p)) for p in outputs},
                "report": sha(report_path)}
    json.dump(manifest, open(os.path.join(data_dir, "manifest.json"), "w", encoding="utf-8"), indent=1, sort_keys=True)
    failed = [k for k, v in checks.items() if not v["pass"]]
    print(f"RTT-104 build: {len(srows)} series rows, {len(boards)} board rows; checks "
          f"{len(checks) - len(failed)}/{len(checks)} PASS" + (f"; FAILED: {failed}" if failed else ""))
    return 1 if failed else 0


def run_checks(raw, economies, parl, pop, srows, boards, zgroups, wrows, wld, wld_all, T, years):
    c = {}
    # C1 every value traceable to the WDI file: re-read the raw text independently
    rawv = {}
    for r in load_json(os.path.join(raw, "wdi_SG.GEN.PARL.ZS_all_1997-2025.json"))[1]:
        if r["value"] is not None:
            rawv[(r["countryiso3code"], int(r["date"]))] = r["value"]
    bad = [s for s in srows if s["wdi_value"] != "" and rawv.get((s["iso3"], s["year"])) != s["wdi_value"]]
    bad += [s for s in srows if s["shown_as"] == "figure" and s["shown_value"] != rawv.get((s["iso3"], s["year"]))]
    bad += [s for s in srows if s["shown_as"] == "latest_figure" and
            s["shown_value"] != rawv.get((s["iso3"], int(s["carried_from_year"])))]
    bad += [b for b in boards if b["latest_figure"] == "no" and rawv.get((b["iso3"], b["year"])) != b["value"]]
    bad += [b for b in boards if b["latest_figure"] == "yes" and rawv.get((b["iso3"], int(b["carried_from_year"]))) != b["value"]]
    c["C1_every_value_traceable_to_wdi"] = {"pass": not bad, "detail": f"{len(bad)} untraceable"}
    # C2 no 0% shown where the data is missing; a shown value is never invented
    bad = [s for s in srows if s["missing"] == "yes" and s["shown_as"] != "latest_figure" and s["shown_value"] != ""]
    zero_names = {(y, t[2]) for y, z, n in zgroups for t in z}
    bad += [k for k in zero_names if rawv.get((k[1], k[0])) is None and
            next(s for s in srows if s["iso3"] == k[1] and s["year"] == k[0])["shown_as"] != "latest_figure"]
    bad += [s for s in srows if s["missing"] == "yes" and s["zero"] == "yes"]
    c["C2_no_zero_where_missing"] = {"pass": not bad, "detail": f"{len(bad)} cases"}
    # C3 no country below the threshold on a board or in the 0% group
    below = {e for e in economies if not (pop.get(e) and Decimal(pop[e][max(pop[e])]) >= T)}
    bad = [b for b in boards if b["iso3"] in below] + [k for k in zero_names if k[1] in below]
    c["C3_no_country_below_threshold"] = {"pass": not bad, "detail": f"{len(bad)} cases"}
    # C4 no forecast: no year after the last WDI year with figures; population year used is a WDI year with a figure
    maxy = max(y for (_, y) in rawv)
    bad = [s for s in srows if s["year"] > maxy] + [b for b in boards if b["year"] > maxy]
    c["C4_no_forecast"] = {"pass": not bad and years[-1] <= maxy, "detail": f"last WDI year with figures {maxy}"}
    # C5 boards: 10 each side when available, ordered by full precision, 0% never on the bottom board
    bad = []
    for y in years:
        for bd in ("top", "bottom"):
            lst = [b for b in boards if b["year"] == y and b["board"] == bd]
            vals = [Decimal(b["value"]) for b in lst]
            if vals != sorted(vals, reverse=(bd == "top")) or len(lst) != 10:
                bad.append((y, bd))
            if bd == "bottom" and any(v == ZERO for v in vals):
                bad.append((y, "zero on bottom"))
        if {b["iso3"] for b in boards if b["year"] == y and b["board"] == "top"} & \
                {b["iso3"] for b in boards if b["year"] == y and b["board"] == "bottom"}:
            bad.append((y, "on both boards"))
    c["C5_boards_well_formed"] = {"pass": not bad, "detail": str(bad[:5])}
    # C6 the world panel is the WLD aggregate, the same in both WDI files
    bad = [y for y in years if wld.get(y) != wld_all.get(y)] + [w for w in wrows if w["wdi_value"] == ""]
    c["C6_world_panel_is_wld"] = {"pass": not bad, "detail": f"{len(bad)} years differ or missing"}
    # C7 no carried value without a figure on both sides, never two carried years in a row
    bad = [s for s in srows if s["shown_as"] == "latest_figure" and not (
        (s["iso3"], s["year"] - 1) in rawv and (s["iso3"], s["year"] + 1) in rawv)]
    c["C7_latest_figure_rule"] = {"pass": not bad, "detail": f"{len(bad)} cases"}
    return c


# ---------------------------------------------------------------- report
def write_report(path, cfg, raw, economies, parl, pop, disp, elig, elig2, boards, boards2, zgroups, zgroups2, ties, ties2,
                 ev, wrows, cc, diffs, owid_only, n_common, checks, years, T, T2):
    from rtt104_report import report_text  # kept in its own file for readability
    text = report_text(cfg=cfg, raw=raw, economies=economies, parl=parl, pop=pop, disp=disp, elig=elig, elig2=elig2,
                       boards=boards, boards2=boards2, zgroups=zgroups, zgroups2=zgroups2, ties=ties, ties2=ties2, ev=ev,
                       wrows=wrows, cc=cc, diffs=diffs, owid_only=owid_only, n_common=n_common, checks=checks,
                       years=years, T=T, T2=T2, one_dp=one_dp, pop_latest=pop_latest)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(build(sys.argv[1], sys.argv[2]))
