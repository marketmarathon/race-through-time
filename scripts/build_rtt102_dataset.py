#!/usr/bin/env python3
"""RTT-102 AI assistant websites race: build the dataset from the public source tables (IQ-17, phase 1).

    python3 scripts/build_rtt102_dataset.py data/rtt-102 reports/RTT-102_data_report.md

Reads only public files in data/rtt-102/source/ and data/rtt-102/identities.csv (the private research is turned into
those tables by scripts/rtt102_import_research.py). Writes points.csv, conflicts.csv, series_monthly.csv,
place_changes.csv, turns.csv, coverage.csv, checks.json, CHECKS.md and manifest.json in the data folder, and the data
report. Deterministic (no clock, no randomness, sorted output); standard library only.

Method: reference/metric_contract_RTT-102.md. Decisions: DEC-500 to DEC-514 in state/DECISIONS.md.
"""
import csv
import hashlib
import json
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

FIRST_MONTH, LAST_MONTH = "2022-12", "2026-09"
ASSISTANTS = ["chatgpt", "gemini", "claude", "copilot", "perplexity", "deepseek", "grok", "meta_ai"]
TITLE = {"chatgpt": "ChatGPT", "gemini": "Gemini (Bard)", "claude": "Claude", "copilot": "Copilot",
         "perplexity": "Perplexity", "deepseek": "DeepSeek", "grok": "Grok", "meta_ai": "Meta AI"}
UNITS = {"billion": Decimal(10) ** 9, "bn": Decimal(10) ** 9, "b": Decimal(10) ** 9, "million": Decimal(10) ** 6,
         "mn": Decimal(10) ** 6, "m": Decimal(10) ** 6, "k": Decimal(10) ** 3, "thousand": Decimal(10) ** 3}
LOWER = ("more than", "topped", "tops", "just over")
UPPER = ("nearly", "almost", "now approaching")
ABOUT = ("about", "around")
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
RELATIVE_MONTHS = {("DIGI_2023", "Last month"): "2023-11"}  # DEC-506: 'Last month' in an article dated 1 Dec 2023


# ---------------------------------------------------------------------------------------------------- helpers
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([r.get(c, "") for c in cols])


def months(a, b):
    y, m = int(a[:4]), int(a[5:])
    out = []
    while f"{y:04d}-{m:02d}" <= b:
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def mindex(m):
    return int(m[:4]) * 12 + int(m[5:]) - 1


def mname(m):
    return f"{MONTH_NAMES[int(m[5:]) - 1]} {m[:4]}"


def fmt_visits(v):
    v = int(v)
    if v >= 10 ** 9:
        return f"{v / 1e9:.2f} bn"
    if v >= 10 ** 6:
        return f"{v / 1e6:.1f} m"
    return f"{v:,}"


def label_proposed(v, bound):
    """Proposed on-screen value label ('~' + rounded, DEC-514): for the design session, not approved."""
    v = Decimal(int(v))
    if v >= 10 ** 9:
        s = f"{(v / Decimal(10) ** 9).quantize(Decimal('0.1'), ROUND_HALF_UP)}bn"
    elif v >= 10 ** 8:
        s = f"{(v / Decimal(10) ** 6).quantize(Decimal('1'), ROUND_HALF_UP)}m"
    elif v >= 10 ** 6:
        s = f"{(v / Decimal(10) ** 6).quantize(Decimal('0.1'), ROUND_HALF_UP)}m"
    else:
        s = f"{(v / Decimal(10) ** 3).quantize(Decimal('1'), ROUND_HALF_UP)}k"
    return s + "+" if bound == "lower" else "~" + s


def parse_visits(text, qualifier):
    """Return (value, step, kind) for a figure as printed, or None. Never repairs a figure (DEC-506)."""
    t = text.lower().replace("–", "-")
    m = re.search(r"(\d[\d,]*(?:\.\d+)?)\s*(billion|million|thousand|bn|mn|b|m|k)?\b", t)
    if not m:
        return None
    num, unit = m.group(1), m.group(2) or ""
    if "," in num:
        if not re.fullmatch(r"\d{1,3}(,\d{3})+", num):
            return None
        num = num.replace(",", "")
    mult = UNITS.get(unit, Decimal(1))
    if "." in num:
        step_digits = Decimal(10) ** -len(num.split(".")[1])
    else:
        trailing = len(num) - len(num.rstrip("0")) if num.strip("0") else 0
        step_digits = Decimal(10) ** (trailing if mult != 1 else 0)
    value = Decimal(num) * mult
    step = step_digits * mult
    words = (qualifier + " " + text).lower()
    kind = "exact"
    if any(w in words for w in LOWER):
        kind = "lower"
    elif any(w in words for w in UPPER):
        kind = "upper"
    elif any(w in words for w in ABOUT):
        kind = "about"
    return value, step, kind


def agree(a, b):
    """Do two printed figures agree (one is the other at a coarser precision, or within its stated bound)?"""
    for x, y in ((a, b), (b, a)):
        if x["kind"] == "lower" and y["kind"] == "lower":
            return True
        if x["kind"] == "lower":
            return y["value"] >= x["value"]
        if x["kind"] == "upper":
            if y["kind"] in ("exact", "about"):
                return x["value"] - x["step"] <= y["value"] <= x["value"]
    return abs(a["value"] - b["value"]) < max(a["step"], b["step"])  # the coarser figure rounded or cut (DEC-508)


def pubnum(r):
    return int(r["publication_date"].replace("-", "")) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["publication_date"]) else 0


def rank_key(r):
    """Order among versions that agree (DEC-508, DEC-523): Luke's rule steps first, then exact over approximate over
    bound, then the most precise, then the later publication."""
    return (r["data_version"] != "current", r["source_type"] != "S", r["preliminary"] == "yes",
            {"exact": 0, "about": 1, "upper": 1, "lower": 2}[r["kind"]], r["step"] / max(r["value"], 1),
            -pubnum(r), r["obs_id"])


def consistent(rows):
    """True when every pair of versions agrees (no transitive chains, DEC-523)."""
    return all(agree(a, b) for i, a in enumerate(rows) for b in rows[i + 1:])


def _keep(pred):
    return lambda rows: [r for r in rows if pred(r)]


def _latest(rows):
    top = max(pubnum(r) for r in rows)
    return [r for r in rows if pubnum(r) == top]


def _chart_in_one_publication(rows):
    """Step 5 (Claude proposal, DEC-524): within ONE publication, its labelled month-by-month chart or table over its prose."""
    if len({r["pub_id"] for r in rows}) != 1:
        return rows
    return [r for r in rows if r["quote_as_recorded"] == "IMAGE"] or rows


STEPS = [("1: current data version over older", _keep(lambda r: r["data_version"] == "current")),
         ("2: Similarweb's own publication over press", _keep(lambda r: r["source_type"] == "S")),
         ("3: final over preliminary", _keep(lambda r: r["preliminary"] != "yes")),
         ("4: the later publication over the earlier (DEC-517)", _latest),
         ("5: within one publication, its labelled chart over its prose (Claude proposal, DEC-524)", _chart_in_one_publication)]


def apply_rule(rows):
    """Luke's rule (DEC-502 (2), DEC-517) plus Claude's proposed step 5. Returns (status, chosen_row_or_None, rule_text, rows_left)."""
    if not rows:
        return "none", None, "", []
    if consistent(rows):
        return "agree", min(rows, key=rank_key), "one figure, or every version agrees", rows
    cur, used = list(rows), "no step needed"
    for name, step in STEPS:
        kept = step(cur)
        if kept and len(kept) < len(cur):
            cur, used = kept, name
        if consistent(cur):
            return "settled", min(cur, key=rank_key), f"step {used}", cur
    return "leftover", None, "unresolved after every step", cur


# ---------------------------------------------------------------------------------------------------- load
def load(data):
    src = os.path.join(data, "source")
    pubs = {p["pub_id"]: p for p in read_csv(os.path.join(src, "publications.csv")) + read_csv(os.path.join(src, "publications_manual.csv"))}
    ident = read_csv(os.path.join(data, "identities.csv"))
    vmap = {v["obs_id"]: v for v in read_csv(os.path.join(src, "verification_map.csv"))}
    excl = {e["obs_id"]: e for e in read_csv(os.path.join(src, "exclusions.csv"))}
    raw = read_csv(os.path.join(src, "observations_research.csv")) + read_csv(os.path.join(src, "observations_manual.csv"))
    runner = read_csv(os.path.join(src, "runner_checks.csv"))
    return pubs, ident, vmap, excl, raw, runner


def identity_at(ident, aid, month):
    """The counted identity (name, domain) in force at the end of the month (DEC-511)."""
    best = None
    for r in ident:
        if r["assistant_id"] != aid or r["counted"] != "yes":
            continue
        if r["from"] <= f"{month}-31" and (r["to"] or "9999-12-31") >= f"{month}-28":
            best = r
    return best


def start_month(ident, aid):
    return min(r["from"][:7] for r in ident if r["assistant_id"] == aid and r["counted"] == "yes")


DOMAIN_RE = re.compile(r"[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|ai|org)\b")


def build_points(pubs, ident, vmap, excl, raw):
    counted = {r["assistant_id"] for r in ident if r["counted"] == "yes"}
    pts = []
    for o in raw:
        p = pubs[o["pub_id"]]
        r = dict(obs_id=o["obs_id"], origin=o["origin"], assistant_id=o["assistant_id"], pub_id=o["pub_id"],
                 publisher=p["publisher"], source_type=p["source_type"], publication_date=p["publication_date"],
                 data_version=p["data_version"], url=p["url"], site_as_recorded=o["site_as_recorded"],
                 visits_as_published=o["visits_as_published"], qualifier=o["qualifier"],
                 measure=o.get("measure") or "monthly visits", quote_as_recorded=o["quote_as_recorded"],
                 note=o.get("note", ""))
        month, basis = o["month"], "as published"
        if (o["pub_id"], o["relative_label"]) in RELATIVE_MONTHS:
            month, basis = RELATIVE_MONTHS[(o["pub_id"], o["relative_label"])], f"read from '{o['relative_label']}' (publication dated {p['publication_date']}; DEC-506)"
        r["month"], r["month_basis"] = month, basis
        r["preliminary"] = "yes" if "preliminary" in o["qualifier"].lower() else "no"
        if o["origin"].startswith("2025 table"):
            r.update(verification_id="V01", status="VERIFIED", wording_seen_at_source="table cell",
                     verified_by="Cowork in Luke's Chrome (all 84 cells, V01)")
        elif o["obs_id"] in vmap:
            v = vmap[o["obs_id"]]
            r.update(verification_id=v["verification_id"], status=v["status"],
                     wording_seen_at_source=v["wording_seen_at_source"], verified_by=v["basis"])
        else:
            r.update(verification_id="", status="UNVERIFIED", wording_seen_at_source="", verified_by="")
        parsed = parse_visits(o["visits_as_published"], o["qualifier"])
        r["value"], r["step"], r["kind"] = (parsed if parsed else (None, None, ""))
        r["bound"] = {"lower": "lower", "upper": "upper"}.get(r["kind"], "")
        # eligibility (DEC-506, DEC-507, DEC-509)
        reason = ""
        idn = identity_at(ident, r["assistant_id"], month) if re.fullmatch(r"\d{4}-\d{2}", month) else None
        if r["measure"] == "projection" or "projection" in o["qualifier"].lower():
            reason = "forecast or projection (no forecasts)"
        elif r["measure"] != "monthly visits":
            reason = f"other measure ({r['measure']})"
        elif r["assistant_id"] not in counted:
            reason = "assistant left out (Le Chat, DEC-501)"
        elif not re.fullmatch(r"\d{4}-\d{2}", month):
            reason = "month not stated"
        elif o["obs_id"] in excl:
            reason = excl[o["obs_id"]]["reason"] + f" ({excl[o['obs_id']]['dec']})"
        elif parsed is None:
            reason = "figure cannot be read as printed"
        elif month < start_month(ident, r["assistant_id"]):
            reason = "before the site's start"
        elif idn is None:
            reason = "no counted address for this month"
        else:
            doms = set(DOMAIN_RE.findall(o["site_as_recorded"].lower()))
            if idn["domain"] in doms:
                r["domain_basis"] = "address as recorded"
            elif doms:
                reason = f"address {', '.join(sorted(doms))} is not the bar's address ({idn['domain']}) in {month}"
            elif r["assistant_id"] == "deepseek":
                reason = "DeepSeek press figure without a stated address (two Similarweb addresses; DEC-507)"
            else:
                r["domain_basis"] = f"product name mapped to {idn['domain']} (DEC-507)"
        r["domain"] = idn["domain"] if idn else ""
        r["name_at_month"] = idn["name"] if idn else ""
        if not reason and r["assistant_id"] == "deepseek" and r["source_type"] == "S" and "deepseek.com" not in o["site_as_recorded"]:
            r["domain_basis"] = "Similarweb's own 'DeepSeek' = deepseek.com (DEC-507)"
        r["eligible"] = "no" if reason else "yes"
        r["exclusion_reason"] = reason
        r.setdefault("domain_basis", "")
        pts.append(r)
    return pts


# ---------------------------------------------------------------------------------------------------- resolve
def resolve(pts):
    by = {}
    for r in pts:
        if re.fullmatch(r"\d{4}-\d{2}", r["month"]) and r["measure"] == "monthly visits" and r["value"] is not None \
                and "forecast" not in r["exclusion_reason"] and "Le Chat" not in r["exclusion_reason"]:
            by.setdefault((r["assistant_id"], r["month"]), []).append(r)
    used, conflicts = {}, []
    for key in sorted(by):
        cands = by[key]
        elig = [r for r in cands if r["eligible"] == "yes"]
        ver = [r for r in elig if r["status"] == "VERIFIED"]
        vstat, vrow, vrule, _ = apply_rule(ver)
        astat, arow, arule, _ = apply_rule(elig)
        for r in cands:
            r["used"] = "no"
            r["used_rule"] = ""
        if vrow is not None:
            vrow["used"] = "yes"
            vrow["used_rule"] = vrule if vstat == "settled" else ("only verified figure" if len(ver) == 1 else "versions agree; most reliable and most precise version used (DEC-508)")
            used[key] = vrow
        if not consistent(cands):
            if vstat == "leftover":
                status = "LEFTOVER for Luke (no figure used; straight line across)"
            elif vrow is None:
                status = "PENDING verification (no verified figure; straight line across)" if elig else "NOT USED (no eligible figure)"
            elif astat == "leftover" or (arow is not None and not agree(arow, vrow)):
                status = "PENDING verification (an unverified version would contest or replace the figure used)"
            else:
                status = "SETTLED"
            conflicts.append(dict(
                assistant_id=key[0], month=key[1], status=status,
                rule_on_verified=f"{vstat}: {vrule}" if vstat != "none" else "no verified eligible figure",
                rule_on_all_versions=f"{astat}: {arule}" if astat != "none" else "no eligible figure",
                used_point=vrow["obs_id"] if vrow else "", used_value=int(vrow["value"]) if vrow else "",
                if_all_verified=(arow["obs_id"] + " " + arow["visits_as_published"]) if arow else ("leftover" if astat == "leftover" else ""),
                versions=" ; ".join(f"{r['obs_id']} {r['pub_id']} {r['visits_as_published']} [{r['source_type']}, {r['data_version']}, "
                                    f"{'preliminary' if r['preliminary'] == 'yes' else 'final'}, {r['status']}"
                                    f"{'' if r['eligible'] == 'yes' else ', not eligible: ' + r['exclusion_reason'].split(' (')[0]}]"
                                    for r in sorted(cands, key=lambda x: (x['publication_date'], x['obs_id'])))))
    for i, c in enumerate(conflicts, 1):
        c["case_id"] = f"C{i:02d}"
    return used, conflicts


# ---------------------------------------------------------------------------------------------------- series
def build_series(ident, used):
    rows = []
    for aid in ASSISTANTS:
        pts = sorted((m, r) for (a, m), r in used.items() if a == aid)
        if not pts:
            continue
        for (m0, p0), (m1, p1) in zip(pts, pts[1:] + [pts[-1]]):
            span = months(m0, m1) if m1 > m0 else [m0]
            for m in (span[:-1] if m1 > m0 else span):
                idn = identity_at(ident, aid, m)
                if m == m0:
                    v, prov, left, right = p0["value"], "published", p0["obs_id"], p0["obs_id"]
                    dv = p0["data_version"]
                    older = dv == "older"
                    prel = p0["preliminary"]
                    bound = p0["bound"]
                else:
                    k = Decimal(mindex(m) - mindex(m0)) / Decimal(mindex(m1) - mindex(m0))
                    v = (p0["value"] + (p1["value"] - p0["value"]) * k).quantize(Decimal(1), ROUND_HALF_UP)
                    prov, left, right = "interpolated", p0["obs_id"], p1["obs_id"]
                    dv = p0["data_version"] if p0["data_version"] == p1["data_version"] else f"{p0['data_version']}->{p1['data_version']}"
                    older = "older" in (p0["data_version"], p1["data_version"])
                    prel = "no"
                    bound = ""
                rows.append(dict(month=m, assistant_id=aid, bar_label=idn["name"], domain=idn["domain"], visits=int(v),
                                 provenance=prov, point_id=left if prov == "published" else "", left_point=left,
                                 right_point=right, data_version=dv, older_estimate="yes" if older else "no",
                                 preliminary=prel, rests_on_preliminary="yes" if "yes" in (p0["preliminary"], p1["preliminary"] if prov == "interpolated" else "no") else "no",
                                 bound=bound, source_type=p0["source_type"] if prov == "published" else "",
                                 value_label_proposed=label_proposed(v, bound)))
    rows.sort(key=lambda r: (r["month"], ASSISTANTS.index(r["assistant_id"])))
    return rows


def places(series):
    bym = {}
    for r in series:
        bym.setdefault(r["month"], []).append(r)
    prev_order, prev_hold, changes, ranks = [], {}, [], {}
    for m in months(FIRST_MONTH, LAST_MONTH):
        live = bym.get(m, [])
        order = sorted(live, key=lambda r: (-r["visits"], prev_order.index(r["assistant_id"]) if r["assistant_id"] in prev_order else 99, r["assistant_id"]))
        ids = [r["assistant_id"] for r in order]
        ranks[m] = ids
        prov = {r["assistant_id"]: r["provenance"] for r in live}
        for place in (1, 2, 3):
            new = ids[place - 1] if len(ids) >= place else ""
            old = prev_hold.get(place, "")
            if new and new != old:
                if not old:
                    kind = "first holder"
                elif old not in ids:
                    kind = "previous holder's figures end"
                else:
                    kind = "overtake"
                changes.append(dict(month=m, place=place, new_holder=new, previous_holder=old, kind=kind,
                                    new_holder_provenance=prov.get(new, ""), previous_holder_provenance=prov.get(old, "not on the board"),
                                    on_published_months="yes" if prov.get(new) == "published" and prov.get(old, "published") == "published" else "no",
                                    bars_live=len(ids)))
            prev_hold[place] = new
        prev_order = ids
    return changes, ranks


def turns(used):
    out = []
    for aid in ASSISTANTS:
        pts = sorted((m, r) for (a, m), r in used.items() if a == aid)
        for i in range(1, len(pts) - 1):
            (m0, a), (m1, b), (m2, c) = pts[i - 1], pts[i], pts[i + 1]
            l_in, l_out = mindex(m1) - mindex(m0), mindex(m2) - mindex(m1)
            s_in, s_out = (b["value"] - a["value"]) / l_in, (c["value"] - b["value"]) / l_out
            if max(l_in, l_out) < 3:
                continue
            big = abs(s_out - s_in) >= Decimal("0.03") * b["value"]
            flip = (s_in > 0) != (s_out > 0) and s_in != 0 and s_out != 0
            ratio = (abs(s_out) / abs(s_in)) if s_in != 0 else Decimal(99)
            if big and (flip or ratio >= 3 or ratio <= Decimal(1) / 3):
                out.append(dict(assistant_id=aid, at_month=m1, months_before=l_in, months_after=l_out,
                                slope_before_per_month=int(s_in), slope_after_per_month=int(s_out),
                                why="direction reverses" if flip else ("speeds up sharply" if ratio >= 3 else "slows sharply"),
                                version_change="yes" if a["data_version"] != c["data_version"] else "no"))
    return out


# ---------------------------------------------------------------------------------------------------- checks
def run_checks(pts, used, series, ident, conflicts):
    res = []

    def check(cid, name, ok, detail):
        res.append(dict(id=cid, name=name, result="PASS" if ok else "FAIL", detail=detail))

    usedrows = list(used.values())
    bad = [r["obs_id"] for r in usedrows if not (r["status"] == "VERIFIED" and r["url"].startswith("http") and r["wording_seen_at_source"])]
    check("K01", "Every on-screen value rests on a VERIFIED figure with its URL and the wording seen at source", not bad, f"{len(usedrows)} points used; problems: {bad or 'none'}")
    pv = {(r["assistant_id"], r["month"]): r for r in usedrows}
    byid = {r["obs_id"]: r for r in usedrows}
    bad = []
    for s in series:
        if s["provenance"] == "published":
            ok = Decimal(s["visits"]) == pv[(s["assistant_id"], s["month"])]["value"]
        else:
            a, b = byid[s["left_point"]], byid[s["right_point"]]
            k = Decimal(mindex(s["month"]) - mindex(a["month"])) / Decimal(mindex(b["month"]) - mindex(a["month"]))
            ok = Decimal(s["visits"]) == (a["value"] + (b["value"] - a["value"]) * k).quantize(Decimal(1), ROUND_HALF_UP)
        if not ok:
            bad.append(s["assistant_id"] + s["month"])
    vals = {}
    for r in pts:
        if r["value"] is not None:
            vals.setdefault((r["assistant_id"], r["month"]), set()).add(r["value"])
    notpub = [k for k, r in pv.items() if r["value"] not in vals[k]]
    check("K02", "No averaging: each published month shows one printed figure exactly; each other month is the straight line between its two points", not bad and not notpub, f"{len(series)} series rows; mismatches: {bad or 'none'}; used values not printed: {notpub or 'none'}")
    bad = [r["obs_id"] for r in usedrows if r["month"] < start_month(ident, r["assistant_id"])]
    bad += [s["assistant_id"] + s["month"] for s in series if s["month"] < start_month(ident, s["assistant_id"])]
    check("K03", "No point or bar before the site's start date", not bad, f"problems: {bad or 'none'}")
    keys = [(s["assistant_id"], s["month"]) for s in series]
    doms = {}
    for s in series:
        doms.setdefault((s["assistant_id"], s["month"]), set()).add(s["domain"])
    bad = [k for k in doms if len(doms[k]) != 1] + ([1] if len(keys) != len(set(keys)) else [])
    bad += [r["obs_id"] for r in usedrows if r["domain"] != identity_at(ident, r["assistant_id"], r["month"])["domain"]]
    check("K04", "One address per assistant per month", not bad, f"problems: {bad or 'none'}")
    ds = [r for r in usedrows if r["assistant_id"] == "deepseek"]
    bad = [r["obs_id"] for r in ds if "chat.deepseek.com" in r["site_as_recorded"] or r["domain"] != "deepseek.com"
           or (r["source_type"] == "P" and "deepseek.com" not in r["site_as_recorded"])]
    sums = {a["value"] + b["value"] for a in pts for b in pts if a["assistant_id"] == b["assistant_id"] == "deepseek"
            and a["month"] == b["month"] and a["obs_id"] < b["obs_id"] and a["value"] is not None and b["value"] is not None}
    bad += [s["month"] for s in series if s["assistant_id"] == "deepseek" and Decimal(s["visits"]) in sums]
    check("K05", "DeepSeek: deepseek.com only; never deepseek.com + chat.deepseek.com", not bad, f"{len(ds)} DeepSeek points used; problems: {bad or 'none'}")
    bad = [r["obs_id"] for r in usedrows if "projection" in (r["qualifier"] + r["measure"]).lower()]
    proj = [r["obs_id"] for r in pts if "projection" in (r["qualifier"] + r["measure"]).lower()]
    check("K06", "No forecast: projections (Similarweb's June 2024 and October 2023 projections) are never used", not bad and all(r["used"] == "no" for r in pts if r["obs_id"] in proj), f"projection rows {proj}, all excluded")
    bad = [r["obs_id"] for r in pts if r["data_version"] not in ("older", "current")] + [s["assistant_id"] + s["month"] for s in series if not s["data_version"]]
    check("K07", "data_version set on every point and every series row", not bad, f"problems: {bad or 'none'}")
    first_last = {}
    for r in usedrows:
        f, l = first_last.get(r["assistant_id"], (r["month"], r["month"]))
        first_last[r["assistant_id"]] = (min(f, r["month"]), max(l, r["month"]))
    bad = [s["assistant_id"] + s["month"] for s in series if not first_last[s["assistant_id"]][0] <= s["month"] <= first_last[s["assistant_id"]][1]]
    check("K08", "No extrapolation beyond a bar's first or last published point", not bad, f"problems: {bad or 'none'}")
    bad = [r["obs_id"] for r in pts if r["used"] == "yes" and (r["eligible"] != "yes" or r["status"] != "VERIFIED")]
    check("K09", "Only eligible VERIFIED figures are used; UNVERIFIED and NOT FOUND never", not bad, f"problems: {bad or 'none'}")
    left = [c for c in conflicts if c["status"].startswith("LEFTOVER")]
    bad = [c["case_id"] for c in left if c["used_point"]]
    check("K10", "Leftover conflicts use no figure until Luke decides", not bad, f"{len(left)} leftovers; problems: {bad or 'none'}")
    bad = [s for s in series if s["assistant_id"] not in ASSISTANTS]
    check("K11", "Le Chat and uncounted sites (Bing Chat in bing.com, Grok in x.com) have no bar", not bad, "none on the board" if not bad else str(bad))
    return res


# ---------------------------------------------------------------------------------------------------- report
def report(path, pts, used, conflicts, series, changes, ranks, trn, checks, runner):
    usedrows = list(used.values())
    L = []
    w = L.append
    w("# RTT-102 AI assistant websites race: data report (phase 1, IQ-17)")
    w("")
    w("Built by `python3 scripts/build_rtt102_dataset.py data/rtt-102 reports/RTT-102_data_report.md` (deterministic). Method: `reference/metric_contract_RTT-102.md`. Decisions DEC-500 to DEC-514. **Data only: nothing designed or rendered (DEC-069).**")
    w("")
    w("**What the race shows:** Similarweb's published estimates of monthly website visits, worldwide, to eight AI assistant websites, December 2022 to September 2026. Not market share and not users. Every bar value rests on a figure seen at its source (Cowork in Luke's Chrome, or a GitHub runner reading the page); straight lines join published months.")
    w("")
    nver = sum(1 for r in pts if r["status"] == "VERIFIED")
    w(f"**In numbers:** {len(pts)} figure rows from {len({r['pub_id'] for r in pts})} publications; {nver} VERIFIED, {sum(1 for r in pts if r['status'] == 'UNVERIFIED')} UNVERIFIED, {sum(1 for r in pts if r['status'] == 'NOT FOUND')} NOT FOUND. {len(usedrows)} points used on bars ({sum(1 for r in usedrows if r['source_type'] == 'S')} from Similarweb's own publications, {sum(1 for r in usedrows if r['source_type'] == 'P')} from press quoting Similarweb). {len(series)} bar-months, of which {sum(1 for s in series if s['provenance'] == 'published')} published and {sum(1 for s in series if s['provenance'] == 'interpolated')} on straight lines. Checks: {sum(1 for c in checks if c['result'] == 'PASS')}/{len(checks)} PASS.")
    w("")
    # coverage
    w("## 1. Coverage grid (assistant × month)")
    w("")
    w("`●` published and used · `○` straight line between two published months · `?` an UNVERIFIED figure exists but no verified one (on Cowork's list) · `!` leftover conflict for Luke · blank: no bar. Bars appear from their first published month; none is extended past its last.")
    w("")
    cmap = {(c["assistant_id"], c["month"]): c for c in conflicts}
    unv = {(r["assistant_id"], r["month"]) for r in pts if r["eligible"] == "yes" and r["status"] != "VERIFIED"}
    smap = {(s["assistant_id"], s["month"]): s for s in series}
    w("| Month | " + " | ".join(TITLE[a] for a in ASSISTANTS) + " |")
    w("|---|" + "---|" * len(ASSISTANTS))
    for m in months(FIRST_MONTH, LAST_MONTH):
        cells = []
        for a in ASSISTANTS:
            s = smap.get((a, m))
            c = cmap.get((a, m))
            if c and c["status"].startswith("LEFTOVER"):
                cells.append("!")
            elif s and s["provenance"] == "published":
                cells.append("●")
            elif (a, m) in unv and (a, m) not in used:
                cells.append("?" + ("○" if s else ""))
            elif s:
                cells.append("○")
            else:
                cells.append("")
        w(f"| {mname(m)} | " + " | ".join(cells) + " |")
    w("")
    w("**First and last published month of each bar** (a bar that ends before September 2026 is a \"latest figure\", never \"retired\", DEC-132):")
    w("")
    w("| Bar | First | Last | Published months | Latest figure? |")
    w("|---|---|---|---|---|")
    for a in ASSISTANTS:
        ms = sorted(m for (x, m) in used if x == a)
        if ms:
            w(f"| {TITLE[a]} | {mname(ms[0])} ({fmt_visits(used[(a, ms[0])]['value'])}) | {mname(ms[-1])} ({fmt_visits(used[(a, ms[-1])]['value'])}) | {len(ms)} | {'no' if ms[-1] == LAST_MONTH else 'yes, from ' + mname(ms[-1])} |")
    w("")
    live = {m: len(ranks[m]) for m in ranks}
    thin = [m for m in months("2026-07", LAST_MONTH) if live[m] < 3]
    if thin:
        w(f"**Warning:** in {', '.join(mname(m) for m in thin)} fewer than three bars have a verified figure (only {', '.join(sorted({TITLE[a] for (a, m) in used if m in thin}))}). The other sites' September 2026 website profiles are not yet read (Similarweb's free search limit, V85); Cowork reads them on a fresh day (DEC-515). Until then no bar is extended past its last published month.")
        w("")
    # places
    w("## 2. Changes of first, second and third place")
    w("")
    w("Ranked on live bars each month (a bar whose figures have ended is not counted here). \"Published\" = both bars have a published figure that month; otherwise the crossing falls on a straight line and its exact month is not a dated fact.")
    w("")
    w("| Month | Place | New holder | Previous holder | Kind | On published months? |")
    w("|---|---|---|---|---|---|")
    for c in changes:
        w(f"| {mname(c['month'])} | {c['place']} | {TITLE[c['new_holder']]} ({c['new_holder_provenance']}) | {TITLE.get(c['previous_holder'], '—')} ({c['previous_holder_provenance'] if c['previous_holder'] else '—'}) | {c['kind']} | {c['on_published_months']} |")
    w("")
    w("Copilot (site open from 15 Nov 2023) and Meta AI (from 18 Apr 2024) join only in September 2024, their first published figures; Claude (from 11 Jul 2023) joins in November 2023. Before that their absence is missing figures, not zero visits.")
    w("")
    # conflicts
    w("## 3. Conflicts: what Luke's rule settles, what is pending, what is left over")
    w("")
    w("Rule (DEC-502 (2), DEC-517): Similarweb's current data version (published on or after 28 Jul 2024) over the older one; then Similarweb's own publication over press quoting it; then final over preliminary; then the later publication over the earlier. **Step 5 is Claude's proposal (DEC-524, question 1):** within one publication, its labelled month-by-month chart or table over a figure in its prose. Never averaged. Applied to VERIFIED, eligible figures only; the same rule over every version (verified or not) shows what would change once the rest is checked. Versions that are the same number printed at a coarser precision (rounded or cut, e.g. 2.6 billion and 2.595B) agree and are not conflicts; agreement is tested between every pair (DEC-523).")
    w("")
    w("| Case | Bar, month | Status | Used | Rule on verified figures | If every version were verified | Versions |")
    w("|---|---|---|---|---|---|---|")
    for c in conflicts:
        w(f"| {c['case_id']} | {TITLE[c['assistant_id']]}, {mname(c['month'])} | {c['status']} | {c['used_point']} {fmt_visits(c['used_value']) if c['used_value'] != '' else '—'} | {c['rule_on_verified']} | {c['if_all_verified'] or '—'} | {c['versions']} |")
    w("")
    w("**The cases named in the briefs:**")
    w("")
    w("- **ChatGPT, May 2024:** 2.2 billion (Nov 2024 post, current version, VERIFIED) is used. The June 2024 post's \"2.5 billion\" is NOT FOUND (V54: no printed figure, chart without labels); it would lose at step 1 anyway.")
    w("- **DeepSeek, February 2026:** Similarweb's own 273.2M for deepseek.com (February table, VERIFIED V62) is used. The Decoder's 246.4 million names no address, so it does not count for DeepSeek (DEC-507).")
    w("- **Claude, February and January 2026:** February = 290.3M (Similarweb's dated February table, +43.07% month on month, V61; The Decoder and the IPO report's 290M agree; DEC-516). The IPO blog's \"203 million\" for February is set aside as January's figure (DEC-525); January 2026 = 203M from the IPO report, \"between January and April 2026 (203M to 824M visits a month)\" (V86).")
    w("- **ChatGPT, December 2022 and January 2023:** the birthday post prints 265M and 615M in its infographic and \"266 million\" and \"617 million\" in its text (the March 2023 post says 616 million for January). Step 4 keeps the birthday post (the latest); step 5, Claude's proposal, picks its infographic (question 1).")
    w("- **Small differences:** Claude May 2026 952.6M (Sep newsletter, later) over 952.5M (Jul newsletter image); Claude June 2026 946.8M (Sep newsletter) over the July image's 946.7M; ChatGPT September 2025 Similarweb's 2025 table (5,904,115,522, Jan 2026) over Carr's 5.6 billion (Oct 2025), all by step 4; Perplexity December 2023: Reuters' 45.6 million and 45 million agree (45.6 cut to 45), so the more precise one is used.")
    w("- **Bard, April and May 2023, ChatGPT July 2023:** \"visitors\" in Similarweb's text, used as visits (DEC-518).")
    w("- **Copilot, September 2024:** only Digiday's 37 million (press quoting Similarweb, VERIFIED V25) exists and is used. It fits Similarweb's own October post (\"growth of 87.6% MoM to 69.4 million\"). Copilot and Meta AI are not in the IPO report, so their last figures stay September 2025 and December 2025 until the September 2026 profiles are read.")
    w("- **July 2026:** no figure for ChatGPT or Gemini is printed in anything checked; the line runs from June to August. Nothing is derived from percentage changes or from the IPO report's quarter-to-date sums.")
    w("")
    # turns
    w("## 4. Long straight lines that may look like a sudden turn")
    w("")
    w("Points where the line's slope reverses or changes at least threefold, with at least one side spanning three months or more (a design-session item: the motion must look smooth, DEC-502 (1)).")
    w("")
    w("| Bar | At | Months before / after | Visits per month before → after | Why | Crosses the data-version change? |")
    w("|---|---|---|---|---|---|")
    for t in trn:
        w(f"| {TITLE[t['assistant_id']]} | {mname(t['at_month'])} | {t['months_before']} / {t['months_after']} | {fmt_visits(abs(t['slope_before_per_month']))}{' down' if t['slope_before_per_month'] < 0 else ' up'} → {fmt_visits(abs(t['slope_after_per_month']))}{' down' if t['slope_after_per_month'] < 0 else ' up'} | {t['why']} | {t['version_change']} |")
    w("")
    gaps = []
    for a in ASSISTANTS:
        ms = sorted(m for (x, m) in used if x == a)
        for m0, m1 in zip(ms, ms[1:]):
            if mindex(m1) - mindex(m0) >= 4:
                gaps.append(f"{TITLE[a]} {mname(m0)} → {mname(m1)} ({mindex(m1) - mindex(m0)} months)")
    w("**Gaps of four months or more between published figures:** " + "; ".join(gaps) + ".")
    w("")
    w("**The data-version change (28 Jul 2024):** Gemini goes from 433.5 million (March 2024, older version) to 247.3 million (September 2024, current version). The straight line shows a 43% fall that may be partly or wholly Similarweb's re-estimate, not real; the same applies, less visibly, to every bar that crosses mid-2024. Similarweb's own current-version posts restate ChatGPT's 2023 peak as \"1.9 billion\" (Oct 2024 post, month not stated) against 1.8 billion in the older version. Luke keeps the published figures, with the older-estimate note at the revision, checked in the design session (DEC-522).")
    w("")
    # unverified
    w("## 5. UNVERIFIED figures for Cowork to check in Luke's Chrome")
    w("")
    w(f"Checked so far: Cowork in Luke's Chrome (V01–V101, 7–8 Oct; the IPO report PDF opened with Luke's OK) and runner round R1 ({runner[0]['run_url']}; {sum(1 for r in runner if r['outcome'] == 'fetched')} of {len(runner)} pages; LinkedIn closed to it by robots.txt). Still to check, highest value first (NOT FOUND figures are listed below the table):")
    w("")
    todo = [r for r in pts if r["status"] == "UNVERIFIED" and r["eligible"] == "yes"]

    def prio(r):
        return (0 if r["pub_id"].startswith("S26_") else 1 if (r["assistant_id"], r["month"]) not in used else 2,
                r["month"], r["assistant_id"], r["obs_id"])
    w("| # | Figure | Month | Publication | URL | Why it matters |")
    w("|---|---|---|---|---|---|")
    for i, r in enumerate(sorted(todo, key=prio), 1):
        k = (r["assistant_id"], r["month"])
        why = "fills a month with no verified figure" if k not in used else (
            "confirms, or is a more precise version of, the figure used" if agree(r, used[k]) else "would contest the figure used")
        w(f"| {i} | {TITLE[r['assistant_id']]} {r['visits_as_published']} | {mname(r['month'])} | {r['pub_id']} | {r['url']} | {why} |")
    w("")
    w("Read the September 2026 profiles as **that month's** figure (\"last month\" tooltip, dossier F12). NOT FOUND after checking: " + "; ".join(f"{TITLE[r['assistant_id']]} {mname(r['month'])} {r['visits_as_published']} ({r['pub_id']}, {r['verified_by']})" for r in pts if r["status"] == "NOT FOUND") + ".")
    w("")
    # leads
    w("## 6. Publications not yet mined for every month (owner decision: every published month)")
    w("")
    w("Known to hold months not yet recorded (a later research round, or Cowork, could add them):")
    w("")
    w("- **Q26_IPO_PDF**, Exhibit 3 (p13): rows for January and June 2026 for claude.ai (not recorded with their wording; both months are covered by other figures); its charts for other sites carry no labels.")
    w("- **Q26_FEB_NEWS** (Similarweb newsletter, 12 Mar 2026): its ranking images may list chatgpt.com, gemini.google.com and others for February 2026 (only claude.ai and deepseek.com recorded).")
    w("- **SW24_JUL** (Jul 2024) and **S24_CUSTOM** (Jan 2024): bars and graphs without printed labels (never read off a bar's height).")
    w("- **Similarweb's free profiles**: show only the latest month; Copilot and Meta AI have no figure after September 2025 and December 2025 except there.")
    w("")
    # credits
    w("## 7. Press credits (description)")
    w("")
    w("Press articles whose figures reach a bar (DEC-244 credits Similarweb on screen and in the description; these are credited in the description too):")
    w("")
    press = {}
    for r in usedrows:
        if r["source_type"] == "P":
            press.setdefault(r["pub_id"], []).append(r)
    for pid in sorted(press, key=lambda k: press[k][0]["publication_date"]):
        rs = sorted(press[pid], key=lambda r: (r["month"], r["assistant_id"]))
        w(f"- **{rs[0]['publisher']}**, {rs[0]['publication_date']} ({rs[0]['url']}): " + "; ".join(f"{TITLE[r['assistant_id']]} {mname(r['month'])} {r['visits_as_published']}" for r in rs) + ".")
    w("")
    # checks
    w("## 8. Checks")
    w("")
    for c in checks:
        w(f"- **{c['id']} {c['result']}** {c['name']}. {c['detail']}")
    w("")
    w("Tests: `python3 tests/rtt102/run_tests_rtt102.py` (rebuilds twice into empty folders and compares every byte, then re-checks the rules independently).")
    w("")
    w(QUESTIONS)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L).rstrip() + "\n")


QUESTIONS = """## 9. Questions for Luke

Luke's answers to the eight questions of 8 Oct are recorded as DEC-515 to DEC-522 ("All as recommended"). Still open, each with Claude's recommendation and what happens if there is no answer:

1. **Step 5 of the conflict rule (Claude's proposal, DEC-524): "within one publication, its labelled month-by-month chart or table over a figure in its prose".** It decides two months that your fourth step cannot, because both versions are in the same post: ChatGPT **December 2022 = 265M** (infographic) rather than \"266 million\" (text, also in three earlier posts), and **January 2023 = 615M** rather than \"617 million\" (the March 2023 post's 616 million loses at step 4). The infographic is the post's own month-by-month series, labelled \"Monthly Visits | All Traffic | Worldwide\", and it supplies all eleven months to October 2023. *Recommendation:* approve. *If no answer:* it stays applied. If you say no, both months become leftovers and ChatGPT's bar starts in February 2023 (1.00B).
2. **Perplexity from December 2022.** Reuters (4 Jan 2024, via Investing.com) quotes Similarweb: \"45 million visits in December, up from 2.2 million when the service became available in December 2022\" (website and mobile web; \"worldwide\" is not stated). With it, Perplexity's bar starts at 2.2 million in December 2022: second place until Bard arrives in March 2023, then third until January 2025. *Recommendation:* keep it (press quoting Similarweb, checked at source, and consistent with Similarweb's own March 2024 figure). *If no answer:* kept.
3. **If the September 2026 profiles still cannot be read.** Six bars are verified to August 2026 (the IPO report and the September newsletter); Copilot and Meta AI end in September 2025 and December 2025. *Recommendation:* if Cowork cannot read the profiles on 9 Oct, end the race at **August 2026** and show Copilot and Meta AI as \"latest figure\". *If no answer:* the build keeps ChatGPT's September 2026 point, and the design session ends the film in August 2026.
"""


# ---------------------------------------------------------------------------------------------------- main
def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    data, report_path = sys.argv[1], sys.argv[2]
    pubs, ident, vmap, excl, raw, runner = load(data)
    pts = build_points(pubs, ident, vmap, excl, raw)
    used, conflicts = resolve(pts)
    for r in pts:
        r.setdefault("used", "no")
        r.setdefault("used_rule", "")
    series = build_series(ident, used)
    changes, ranks = places(series)
    trn = turns(used)
    checks = run_checks(pts, used, series, ident, conflicts)

    pcols = ["obs_id", "assistant_id", "name_at_month", "domain", "site_as_recorded", "domain_basis", "month", "month_basis",
             "visits", "visits_as_published", "qualifier", "bound", "preliminary", "measure", "source_type", "pub_id", "publisher",
             "publication_date", "data_version", "url", "exact_quote", "verification_id", "verified_by", "status", "eligible",
             "exclusion_reason", "used", "used_rule", "origin", "note"]
    for r in pts:
        r["visits"] = int(r["value"]) if r["value"] is not None else ""
        r["exact_quote"] = r["wording_seen_at_source"] or (f"[research, not seen at source] {r['quote_as_recorded']}" if r["quote_as_recorded"] else "")
    pts.sort(key=lambda r: (ASSISTANTS.index(r["assistant_id"]) if r["assistant_id"] in ASSISTANTS else 99, r["month"], r["publication_date"], r["obs_id"]))
    write_csv(os.path.join(data, "points.csv"), pcols, pts)
    write_csv(os.path.join(data, "conflicts.csv"), ["case_id", "assistant_id", "month", "status", "used_point", "used_value",
              "rule_on_verified", "rule_on_all_versions", "if_all_verified", "versions"], conflicts)
    scols = ["month", "assistant_id", "bar_label", "domain", "visits", "provenance", "point_id", "left_point", "right_point",
             "data_version", "older_estimate", "preliminary", "rests_on_preliminary", "bound", "source_type", "value_label_proposed"]
    write_csv(os.path.join(data, "series_monthly.csv"), scols, series)
    write_csv(os.path.join(data, "place_changes.csv"), ["month", "place", "new_holder", "previous_holder", "kind",
              "new_holder_provenance", "previous_holder_provenance", "on_published_months", "bars_live"], changes)
    write_csv(os.path.join(data, "turns.csv"), ["assistant_id", "at_month", "months_before", "months_after",
              "slope_before_per_month", "slope_after_per_month", "why", "version_change"], trn)
    with open(os.path.join(data, "checks.json"), "w", encoding="utf-8") as f:
        json.dump(checks, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(data, "CHECKS.md"), "w", encoding="utf-8") as f:
        f.write("# RTT-102 checks (written by scripts/build_rtt102_dataset.py)\n\n")
        for c in checks:
            f.write(f"- **{c['id']} {c['result']}** {c['name']}. {c['detail']}\n")
    report(report_path, pts, used, conflicts, series, changes, ranks, trn, checks, runner)
    files = sorted(os.path.join(dp, fn) for dp, _, fns in os.walk(data) for fn in fns if fn not in ("manifest.json", "README.md"))
    man = {"builder": "scripts/build_rtt102_dataset.py", "files": {os.path.relpath(p, data): hashlib.sha256(open(p, "rb").read()).hexdigest() for p in files}}
    with open(os.path.join(data, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1, sort_keys=True)
        f.write("\n")
    fails = [c["id"] for c in checks if c["result"] != "PASS"]
    print(f"points {len(pts)} (used {len(used)}), conflicts {len(conflicts)}, series rows {len(series)}, place changes {len(changes)}, checks {len(checks) - len(fails)}/{len(checks)} PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
