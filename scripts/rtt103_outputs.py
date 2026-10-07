#!/usr/bin/env python3
"""RTT-103 (IQ-16): writes files A-L, the two masters, companion audit files and checks for build_rtt103_dataset.py.

Kept apart from the build so the method (which figure is a quarter) stays short and readable. See the build's
docstring for inputs; brief sections 16-28 and 34 for the exact output columns.
"""
import csv
import hashlib
import json
import os
import re
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

A_COLS = ["source_id", "company", "source_grade", "source_type", "title", "publisher", "publication_date",
          "reporting_period", "fiscal_year", "fiscal_quarter", "url", "pdf_page_or_table", "capex_metric_present",
          "cash_capex_present", "lease_information_present", "AI_cloud_commentary_present", "guidance_present", "notes"]
B_COLS = ["observation_id", "company_id", "company_name_at_time", "fiscal_year", "fiscal_quarter", "period_start",
          "period_end", "calendar_quarter_bucket", "publication_date", "metric_name_exact", "metric_category",
          "reported_value", "reported_currency", "reported_units", "value_local_currency", "source_id", "source_grade",
          "source_url", "source_page_table", "reported_or_derived", "derivation_formula", "definition_notes",
          "includes_finance_leases", "includes_lease_principal", "includes_intangibles", "includes_acquisitions",
          "superseded", "conflict_flag", "notes"]
C_COLS = ["company", "effective_from", "effective_to", "company_reported_capex_definition", "cash_capex_definition",
          "lease_treatment", "other_inclusions", "other_exclusions", "source_id", "source_url", "definition_break_flag",
          "comparison_warning", "notes"]
D_COLS = ["company", "company_id", "period_end", "calendar_quarter_bucket", "fiscal_year", "fiscal_quarter",
          "capex_local_currency", "currency", "fx_average", "fx_source", "company_reported_capex_usd", "cash_capex_usd",
          "canonical_value_usd", "canonical_series_used", "source_grade", "reported_or_derived", "definition_break",
          "coverage_status", "notes"]
E_COLS = ["calendar_quarter", "company", "display_name", "TTM_capex_usd", "TTM_capex_usd_billions", "series_definition",
          "q_minus_3", "q_minus_2", "q_minus_1", "current_q", "all_four_quarters_valid", "definition_break_in_TTM",
          "source_quality", "notes"]
F_COLS = ["company", "forecast_period", "forecast_type", "metric_definition", "low_usd_bn", "high_usd_bn",
          "midpoint_usd_bn", "single_estimate_usd_bn", "previous_guidance_low", "previous_guidance_high",
          "revision_date", "source_grade", "source", "publication_date", "url", "notes"]
G_COLS = ["date", "company", "event_type", "event", "relationship_to_AI_or_cloud_capex", "amount_if_stated",
          "amount_type", "period_covered", "source_grade", "source", "publication_date", "url", "notes"]
I_COLS = ["issue_id", "company", "period", "issue_type", "description", "source_1", "value_1", "source_2", "value_2",
          "likely_explanation", "recommended_treatment", "confidence", "video_risk"]
L_COLS = ["quarter", "number_of_companies_with_valid_data", "aggregate_TTM_capex_usd", "aggregate_TTM_capex_usd_bn",
          "YoY_change_pct", "coverage_warning"]
MASTER_COLS = ["date", "year", "quarter", "company", "display_name", "capex_TTM_usd", "capex_TTM_usd_bn", "rank",
               "previous_rank", "rank_change", "source_quality", "definition_warning", "data_status"]
E26_COLS = ["company", "display_name", "display_label", "forecast_period", "forecast_type", "forecast_amount_usd_bn",
            "range_low_usd_bn", "range_high_usd_bn", "midpoint_usd_bn", "metric_definition", "source", "source_grade",
            "publication_date", "url", "notes"]

# Canonical series per company (brief section 26 option C; recommendation in K, awaiting Luke).
CANON_LINE = {"amazon": "A", "microsoft": "B", "alphabet": "B", "meta": "B", "oracle": "B", "alibaba": "A", "tencent": "A",
              "baidu": "A"}
CANON_LABEL = ("C: cash spent on property and equipment as printed in each company's cash-flow statement "
               "(Amazon: purchases net of proceeds from sales and incentives, its own capex measure; others: purchases "
               "of / additions to property and equipment). Finance leases excluded for every company.")
SERIES_TEXT = {
    "amazon": "Amazon purchases of property and equipment net of proceeds from sales and incentives (cash)",
    "microsoft": "Microsoft additions to property and equipment (cash)",
    "alphabet": "Alphabet (Google) purchases of property and equipment (cash)",
    "meta": "Meta purchases of property and equipment (cash; printed 'net' from the 2024 filings)",
    "oracle": "Oracle capital expenditures (cash purchases of property and equipment)",
    "alibaba": "Alibaba cash capital expenditure (see C)", "tencent": "Tencent (see C)", "baidu": "Baidu (see C)",
}


def money(v, places=0):
    return str(Decimal(v).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def bn(v):
    return money(Decimal(v) / Decimal(10 ** 9), 3)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def assemble(out, src, private, quarters, series, obs, elsewhere, restated, meta_rel, china, fx_daily, docs, china_status):
    import build_rtt103_dataset as B  # lazy: the build imports this module
    write_csv, read_csv, bucket_of, bucket_label, prev_bucket = B.write_csv, B.read_csv, B.bucket_of, B.bucket_label, B.prev_bucket
    C = B.COMPANIES
    checks = []

    def check(cid, name, ok, detail, kind="financial"):
        checks.append({"company": cid, "check": name, "result": "PASS" if ok else "FAIL", "kind": kind, "detail": detail})

    # ------------------------------------------------------------------ source ids (catalogue rows Claude opened)
    cat_ids = {}
    for r in read_csv(os.path.join(src, "catalogue_url_ids.csv")):  # url -> research-catalogue source_id (ids only)
        cat_ids.setdefault(r["url"], r["source_id"])
    sources = {}

    def source_for(rec):
        url = rec.get("doc_url") or rec.get("url") or rec.get("source_url")
        if url in sources:
            return sources[url]["source_id"]
        sid = cat_ids.get(url) or rec.get("source_id") or f"SRC-IQ16-{rec.get('company_id', 'X').upper()}-{rec.get('accession', '')}"
        sources[url] = {"source_id": sid, "rec": rec}
        return sid

    # ------------------------------------------------------------------ canonical choice and quarter table (D)
    def qrec(cid, ser, fy, fq):
        return series.get((cid, ser, fy, fq))

    d_rows, canon = [], {}
    obs_rows, obs_seen = [], set()
    for cid in B.US + B.CN:
        for q in quarters[cid]:
            b = bucket_of(q["end"])
            if b < prev_bucket(B.FIRST_BUCKET, 3) or b > B.LAST_BUCKET_CANDIDATE:
                continue
            a, bb = qrec(cid, "A", q["fy"], q["fq"]), qrec(cid, "B", q["fy"], q["fq"])
            if a is None and bb is None:
                continue
            cl = CANON_LINE.get(cid, "A")
            cr = a if cl == "A" else bb
            cv = cr["qv"] if cr else None
            av, bv = (a["qv"] if a else None), (bb["qv"] if bb else None)
            fx = (cr or {}).get("fx") if cr else None
            usd = lambda v, r: (v["value_usd"] if "value_usd" in v else v["value"]) if v else None  # noqa: E731
            grade = ""
            if cv:
                grade = max((i.get("grade", "A") for i in cv["inputs"]), default="A")
            how = {"REPORTED": "REPORTED", "REPORTED_RELEASE": "REPORTED", "DERIVED": "DERIVED_FROM_PRIMARY_SOURCE",
                   "DERIVED_SAME_FILING": "DERIVED_FROM_PRIMARY_SOURCE"}.get(cv["how"], "") if cv else ""
            status = coverage_status(cid, q, cv, elsewhere)
            brk = definition_break(cid, q)
            notes = []
            if cv and cv.get("formula"):
                notes.append("Derived: " + cv["formula"])
            if cv and any(r.get("restated_later") for r in cv["inputs"]):
                notes.append("A later filing re-presented an input with a different value; first-reported value used (see I).")
            if cid == "meta" and av and av["how"] == "REPORTED_RELEASE":
                notes.append("Company-reported capex from Meta's earnings release (USD, printed to $10m from 2016).")
            if cr and cr.get("why"):
                notes.append(cr["why"])
            row = {"company": C[cid]["name"], "company_id": cid, "period_end": q["end"],
                   "calendar_quarter_bucket": bucket_label(b), "fiscal_year": f"FY{q['fy']}", "fiscal_quarter": f"Q{q['fq']}",
                   "capex_local_currency": (cv["value"] if cv else ""), "currency": C[cid]["ccy"],
                   "fx_average": (fx["rate"] if fx else ""), "fx_source": (fx["source"] if fx else ""),
                   "company_reported_capex_usd": usd(av, a) if av else "",
                   "cash_capex_usd": usd(bv, bb) if bv else "",
                   "canonical_value_usd": usd(cv, cr) if cv else "",
                   "canonical_series_used": f"{cl} (option C, recommended; awaiting Luke)" if cv else "",
                   "source_grade": grade, "reported_or_derived": how, "definition_break": brk,
                   "coverage_status": status, "notes": " ".join(notes)}
            d_rows.append(row)
            if cv:
                canon[(cid, b)] = {"value": int(row["canonical_value_usd"]), "grade": grade, "how": how, "end": q["end"],
                                   "brk": brk, "fy": q["fy"], "fq": q["fq"], "status": status}
    d_rows.sort(key=lambda r: (r["company_id"], r["period_end"]))

    # ------------------------------------------------------------------ latest common complete quarter
    race = [c for c in B.US + B.CN if race_member(c, canon)]
    latest = None
    for b in sorted({k[1] for k in canon}):
        if all((c, b) in canon for c in race):
            latest = b
    # ------------------------------------------------------------------ TTM (E)
    e_rows, ttm = [], {}
    for b in B.buckets(B.FIRST_BUCKET, latest):
        for cid in B.US + B.CN:
            win = [canon.get((cid, prev_bucket(b, k))) for k in (3, 2, 1, 0)]
            if not all(win):
                continue
            # four consecutive fiscal quarters: each bucket's quarter must follow the previous one
            consecutive = all((win[i + 1]["fy"], win[i + 1]["fq"]) == nxt(win[i]["fy"], win[i]["fq"]) for i in range(3))
            if not consecutive:
                continue
            total = sum(w["value"] for w in win)
            brk = any(w["brk"] for w in win[1:]) or any(w["brk"] for w in win[:1] if False)
            breaks = [w["brk"] for w in win if w["brk"]]
            quality = max(w["grade"] for w in win)
            derived = sum(1 for w in win if w["how"].startswith("DERIVED"))
            ttm[(cid, b)] = {"value": total, "quality": quality, "brk": bool(breaks)}
            e_rows.append({"calendar_quarter": bucket_label(b), "company": C[cid]["name"], "display_name": C[cid]["display"],
                           "TTM_capex_usd": total, "TTM_capex_usd_billions": bn(total), "series_definition": SERIES_TEXT[cid],
                           "q_minus_3": win[0]["value"], "q_minus_2": win[1]["value"], "q_minus_1": win[2]["value"],
                           "current_q": win[3]["value"], "all_four_quarters_valid": "TRUE",
                           "definition_break_in_TTM": "TRUE" if breaks else "FALSE",
                           "source_quality": f"Grade {quality}",
                           "notes": (f"{derived} of 4 quarters derived by exact YTD subtraction. " if derived else "")
                                    + ("; ".join(sorted(set(breaks))) if breaks else "")
                                    + f" Fiscal quarters ending {', '.join(w['end'] for w in win)}."})
    e_rows.sort(key=lambda r: (r["calendar_quarter"], -int(r["TTM_capex_usd"])))
    loc = dict(locals())
    loc["B_COLS"] = B_COLS
    return finish(loc)


def nxt(fy, fq):
    return (fy, fq + 1) if fq < 4 else (fy + 1, 1)


def race_member(cid, canon):
    """In the canonical public-company race: has a canonical quarter in 2026 (the US five; China-listed once built)."""
    return any(k[0] == cid and k[1][0] == 2026 for k in canon)


def coverage_status(cid, q, cv, elsewhere):
    if not cv:
        if cid == "meta" and q["end"] < "2011-07-01":
            return "NOT_FOUND"
        return "NOT_FOUND"
    if cv["how"] == "REPORTED":
        return "A_REPORTED"
    if cv["how"] == "REPORTED_RELEASE":
        return "B_REPORTED"
    return "DERIVED_PRIMARY"


DEF_BREAKS = {  # (company, first quarter end of the new definition) -> text; used to flag TTM windows that span it
    ("meta", "2024-03-31"): "Meta prints 'Purchases of property and equipment, net' from its 2024 filings (2023 re-presented)",
}


def definition_break(cid, q):
    for (c, start), text in DEF_BREAKS.items():
        if c == cid and q["end"] == start:
            return text
    return ""


def finish(v):
    """Everything after D and E: B, A, C, F-L, masters, companions, checks, manifest."""
    import build_rtt103_dataset as B
    out, src, private = v["out"], v["src"], v["private"]
    write_csv, read_csv, bucket_label, prev_bucket = B.write_csv, B.read_csv, B.bucket_label, B.prev_bucket
    C, series, obs, restated, latest, check = B.COMPANIES, v["series"], v["obs"], v["restated"], v["latest"], v["check"]
    canon, ttm, race, source_for, sources = v["canon"], v["ttm"], v["race"], v["source_for"], v["sources"]

    # ------------------------------------------------------------------ B: raw observations (+ audit companion)
    b_rows, b_audit, used_keys = [], [], set()
    for (cid, ser, fy, fq), rec in series.items():
        qv = rec.get("qv")
        if qv:
            for i in qv["inputs"]:
                used_keys.add((cid, i.get("line", rec["line"]), i.get("period_start", ""), i.get("period_end", ""), i.get("accession", "")))
    n = 0
    for (cid, line, start, end), lst in sorted(obs.items()):
        if cid not in B.US or line not in LINE_META:
            continue
        days = (B.d(end) - B.d(start)).days + 1
        if days > 380 or (B.bucket_of(end) < (2008, 1)):
            continue
        if cid == "amazon" and 340 < days < 380 and not end.endswith("12-31"):
            continue  # Amazon's trailing-twelve-month columns: kept in the audit file only
        meta = LINE_META[line]
        versions = []
        for r in lst:
            if r["value"] not in [x["value"] for x in versions]:
                versions.append(r)
        for k, r in enumerate(versions):
            n += 1
            later_diff = k < len(versions) - 1
            sid = source_for(r)
            confirms = [x["accession"] for x in lst if x["value"] == r["value"] and x["accession"] != r["accession"]]
            b_rows.append({
                "observation_id": f"OBS-{cid.upper()}-{n:05d}", "company_id": cid,
                "company_name_at_time": name_at_time(cid, end), "fiscal_year": fiscal_label(cid, end, v["quarters"]),
                "fiscal_quarter": duration_label(days, cid, end, v["quarters"]), "period_start": start, "period_end": end,
                "calendar_quarter_bucket": bucket_label(B.bucket_of(end)), "publication_date": r["filed"],
                "metric_name_exact": r["printed_label"], "metric_category": meta["category"],
                "reported_value": f"{'(' if r.get('printed_negative') == 'True' else ''}{int(r['value']) // (10 ** 6 if r['printed_units'] == 'millions' else 10 ** 3):,}{')' if r.get('printed_negative') == 'True' else ''}",
                "reported_currency": "USD", "reported_units": r["printed_units"], "value_local_currency": r["value"],
                "source_id": sid, "source_grade": "A", "source_url": r["doc_url"],
                "source_page_table": f"{r['form']} {statement_name(r)}",
                "reported_or_derived": "REPORTED", "derivation_formula": "",
                "definition_notes": meta["notes"](r) if callable(meta["notes"]) else meta["notes"],
                "includes_finance_leases": meta["fl"], "includes_lease_principal": meta["flp"],
                "includes_intangibles": meta.get("intang", "NO (internal-use software capitalised as property and equipment is included)" if cid == "amazon" else "NO"),
                "includes_acquisitions": "NO", "superseded": "TRUE" if later_diff else "FALSE",
                "conflict_flag": "TRUE" if len(versions) > 1 else "FALSE",
                "notes": (f"XBRL tag {r['xbrl_tag'] or 'none (printed, untagged; period from the column of the purchases row)'}; "
                          f"text check {r['text_check']}." + (f" Same value also printed in {len(confirms)} later filing(s)." if confirms else "")
                          + (" Re-presented with a different value by a later filing (see next observation and file I)." if later_diff else ""))})
            b_audit.append({"observation_id": b_rows[-1]["observation_id"], "accession": r["accession"], "form": r["form"],
                            "xbrl_tag": r["xbrl_tag"], "text_check": r["text_check"], "period_from": r["period_from"],
                            "printed_row": r["printed_row"], "document_sha256": r["doc_sha256"],
                            "all_filings_printing_this_value": ";".join([r["accession"]] + confirms)})
    # derived quarters and company-release figures as their own observations
    for (cid, ser, fy, fq), rec in sorted(series.items()):
        qv = rec.get("qv")
        if not qv or cid not in B.US:
            continue
        if qv["how"] in ("DERIVED", "DERIVED_SAME_FILING") or (qv["how"] == "REPORTED_RELEASE" and ser == "A"):
            key = (cid, rec["end"], qv["value"], qv["how"])
            if key in used_keys:
                continue
            used_keys.add(key)
            n += 1
            first = qv["inputs"][0]
            if qv["how"] == "REPORTED_RELEASE":
                sid = source_for(dict(first, company_id=cid, doc_url=first["url"]))
                b_rows.append(dict(base_obs(B, cid, rec, n, v["quarters"]), **{
                    "publication_date": first["release_filed"], "metric_name_exact": "Capital expenditures" + (
                        ", including principal payments on finance leases" if first["includes_finance_lease_principal"] == "yes" else ""),
                    "metric_category": "company_reported_capex", "reported_value": printed_amount(first["quote"]),
                    "reported_units": first["precision"], "value_local_currency": qv["value"], "source_id": sid,
                    "source_grade": "B", "source_url": first["url"], "source_page_table": "Earnings release (8-K exhibit 99.1), first-page highlights",
                    "reported_or_derived": "REPORTED", "definition_notes": "Meta's own capex measure" + (
                        "; includes principal payments on finance leases (from Q1 2019)" if first["includes_finance_lease_principal"] == "yes" else "; equals purchases of property and equipment"),
                    "includes_finance_leases": "PRINCIPAL PAYMENTS ONLY" if first["includes_finance_lease_principal"] == "yes" else "NO",
                    "includes_lease_principal": "YES" if first["includes_finance_lease_principal"] == "yes" else "NO",
                    "notes": f"Verbatim: \"{first['quote'][:220]}\""}))
            else:
                ids = [source_for(i) for i in qv["inputs"]]
                b_rows.append(dict(base_obs(B, cid, rec, n, v["quarters"]), **{
                    "publication_date": max(i["filed"] for i in qv["inputs"]),
                    "metric_name_exact": qv["inputs"][0]["printed_label"],
                    "metric_category": "derived_quarter_" + LINE_META.get(qv["inputs"][0].get("line", ""), {"category": "value"})["category"],
                    "reported_value": "", "reported_units": "USD", "value_local_currency": qv["value"],
                    "source_id": ";".join(dict.fromkeys(ids)), "source_grade": "A",
                    "source_url": ";".join(dict.fromkeys(i["doc_url"] for i in qv["inputs"])),
                    "source_page_table": "Consolidated statements of cash flows (year-to-date columns)",
                    "reported_or_derived": "DERIVED_FROM_PRIMARY_SOURCE", "derivation_formula": qv["formula"],
                    "definition_notes": "Both inputs printed under the same line and definition.",
                    "includes_finance_leases": "NO", "includes_lease_principal": "NO",
                    "notes": f"Series {ser}; inputs: " + "; ".join(f"{i['accession']} ({i['filed']})" for i in qv["inputs"])}))
    b_rows.extend(v.get("china_b_rows", []))
    write_csv(os.path.join(out, "B_capex_observations.csv"), b_rows, v["B_COLS"])
    write_csv(os.path.join(out, "B_capex_observations_audit.csv"), b_audit,
              ["observation_id", "accession", "form", "xbrl_tag", "text_check", "period_from", "printed_row",
               "document_sha256", "all_filings_printing_this_value"])
    v["b_rows"] = b_rows
    write_rest(v)
    return v


LINE_META = {
    "cash_ppe": {"category": "cash_purchases_of_ppe", "fl": "NO", "flp": "NO",
                 "notes": "Cash paid for property and equipment as printed in the cash-flow statement (investing)."},
    "amazon_ppe_gross": {"category": "cash_purchases_of_ppe", "fl": "NO", "flp": "NO",
                         "notes": "Amazon gross purchases (presentation from the FY2017 10-K); incentives on their own line."},
    "amazon_ppe_net_of_incentives": {"category": "cash_purchases_of_ppe_net_of_incentives", "fl": "NO", "flp": "NO",
                                     "notes": "Amazon's single purchases line before the FY2017 10-K: net of property and equipment incentives (label gained ', net' in 2016)."},
    "ppe_proceeds_incentives": {"category": "ppe_sale_proceeds_and_incentives", "fl": "NO", "flp": "NO",
                                "notes": "Amazon: proceeds from property and equipment sales and incentives (inflow)."},
    "finance_lease_principal": {"category": "finance_lease_principal_payments", "fl": "NO", "flp": "YES",
                                "notes": "Principal repayments of finance (before 2019: capital) leases; financing activities."},
    "financing_obligation_principal": {"category": "financing_obligation_principal_payments", "fl": "NO", "flp": "NO",
                                       "notes": "Amazon build-to-suit financing obligations (called 'finance lease obligations' before 2019)."},
    "ppe_acquired_finance_leases": {"category": "ppe_acquired_under_finance_leases_noncash", "fl": "YES", "flp": "NO",
                                    "notes": "Non-cash: property and equipment acquired under finance (capital) leases (supplemental)."},
}


def statement_name(r):
    return "consolidated statements of cash flows"


def name_at_time(cid, end):
    if cid == "alphabet":
        return "Google Inc." if end < "2015-10-02" else "Alphabet Inc."
    if cid == "meta":
        return "Facebook, Inc." if end < "2021-10-28" else "Meta Platforms, Inc."
    return {"amazon": "Amazon.com, Inc.", "microsoft": "Microsoft Corporation", "oracle": "Oracle Corporation",
            "alibaba": "Alibaba Group Holding Limited", "tencent": "Tencent Holdings Limited", "baidu": "Baidu, Inc."}[cid]


def fiscal_label(cid, end, quarters):
    for q in quarters[cid]:
        if q["end"] == end:
            return f"FY{q['fy']}"
    return ""


def duration_label(days, cid, end, quarters):
    fq = next((q["fq"] for q in quarters[cid] if q["end"] == end), None)
    if days < 100:
        return f"Q{fq}" if fq else "3M"
    if days < 200:
        return "H1 (6M YTD)"
    if days < 290:
        return "9M YTD"
    return "FY" if fq == 4 else "TTM"


def base_obs(B, cid, rec, n, quarters):
    return {"observation_id": f"OBS-{cid.upper()}-{n:05d}", "company_id": cid,
            "company_name_at_time": name_at_time(cid, rec["end"]), "fiscal_year": f"FY{rec['fy']}",
            "fiscal_quarter": f"Q{rec['fq']}", "period_start": rec["start"], "period_end": rec["end"],
            "calendar_quarter_bucket": B.bucket_label(rec["bucket"]), "reported_currency": "USD",
            "derivation_formula": "", "includes_intangibles": "NO", "includes_acquisitions": "NO",
            "superseded": "FALSE", "conflict_flag": "FALSE"}


def printed_amount(quote):
    m = re.search(r"\$\s*[\d,.]+\s*(?:billion|million)", quote.split("were", 1)[-1])
    return m.group(0) if m else ""


def write_rest(v):
    import build_rtt103_dataset as B
    out, src, private = v["out"], v["src"], v["private"]
    write_csv, read_csv, bucket_label, prev_bucket = B.write_csv, B.read_csv, B.bucket_label, B.prev_bucket
    C, latest, check, canon, ttm, race = B.COMPANIES, v["latest"], v["check"], v["canon"], v["ttm"], v["race"]
    sources, source_for, quarters, series = v["sources"], v["source_for"], v["quarters"], v["series"]

    # ------------------------------------------------------------------ D, E
    write_csv(os.path.join(out, "D_quarterly_capex_clean.csv"), v["d_rows"], D_COLS)
    write_csv(os.path.join(out, "E_capex_TTM_race.csv"), v["e_rows"], E_COLS)

    # ------------------------------------------------------------------ C: definitions (curated)
    c_rows = read_csv(os.path.join(src, "definitions.csv"))
    write_csv(os.path.join(out, "C_capex_definitions.csv"), c_rows, C_COLS)
    write_csv(os.path.join(out, "entity_name_history.csv"), read_csv(os.path.join(src, "entities.csv")),
              ["entity_id", "former_name", "new_name", "effective_date", "evidence", "recommended_video_display_name"])

    # ------------------------------------------------------------------ F and 2026E (curated, verbatim quotes)
    f_rows = read_csv(os.path.join(src, "guidance_2026.csv"))
    write_csv(os.path.join(out, "F_2026_capex_forecasts.csv"), f_rows, F_COLS)
    e26 = []
    for r in f_rows:
        if r.get("forecast_period", "") not in ("FY2026", "CY2026") or r["notes"].startswith("SUPERSEDED"):
            continue
        if r["forecast_type"] not in ("GUIDANCE", "ESTIMATE", "AWS_ESTIMATE"):
            continue
        label = "2026 GUIDANCE" if r["forecast_type"] == "GUIDANCE" else "2026 ESTIMATE"
        amount = r["midpoint_usd_bn"] or r["single_estimate_usd_bn"]
        e26.append({"company": r["company"], "display_name": display_of(C, r["company"]), "display_label": label,
                    "forecast_period": r["forecast_period"], "forecast_type": r["forecast_type"],
                    "forecast_amount_usd_bn": r["single_estimate_usd_bn"] or "",
                    "range_low_usd_bn": r["low_usd_bn"], "range_high_usd_bn": r["high_usd_bn"],
                    "midpoint_usd_bn": r["midpoint_usd_bn"], "metric_definition": r["metric_definition"],
                    "source": r["source"], "source_grade": r["source_grade"], "publication_date": r["publication_date"],
                    "url": r["url"], "notes": ("Range: show low-high, never the midpoint alone. " if r["low_usd_bn"] else "") + r["notes"]})
    write_csv(os.path.join(out, "AI_SPENDING_RACE_2026E.csv"), e26, E26_COLS)

    # ------------------------------------------------------------------ G (curated)
    write_csv(os.path.join(out, "G_AI_capex_story_events.csv"), read_csv(os.path.join(src, "story_events.csv")), G_COLS)

    # ------------------------------------------------------------------ H: coverage
    col_of = {"amazon": "Amazon", "microsoft": "Microsoft", "alphabet": "Alphabet", "meta": "Meta", "oracle": "Oracle",
              "alibaba": "Alibaba", "tencent": "Tencent", "baidu": "Baidu"}
    h_rows, h_series = [], []
    last = latest or (2026, 2)
    for b in B.buckets(B.FIRST_BUCKET, last):
        row = {"quarter": bucket_label(b)}
        for cid, col in col_of.items():
            c = canon.get((cid, b))
            row[col] = c["status"] if c else not_found_status(cid, b, v.get("china_status", {}))
        row["ByteDance"] = "NOT_YET_EXISTED" if b < (2012, 1) else "NOT_FOUND"
        h_rows.append(row)
        for cid, col in col_of.items():
            for ser in ("A", "B"):
                recs = [r for (c2, s2, fy, fq), r in series.items() if c2 == cid and s2 == ser and r["bucket"] == b]
                st = "NOT_BUILT" if not recs else (status_of(recs[0]) if recs[0].get("qv") else "NOT_FOUND")
                h_series.append({"quarter": bucket_label(b), "company": col, "series": ser, "status": st,
                                 "fiscal_period_end": recs[0]["end"] if recs else ""})
    write_csv(os.path.join(out, "H_coverage_matrix.csv"), h_rows, ["quarter"] + B.H_COLUMNS)
    write_csv(os.path.join(out, "H_coverage_by_series.csv"), h_series, ["quarter", "company", "series", "status", "fiscal_period_end"])

    # ------------------------------------------------------------------ I: conflicts and warnings
    i_rows = []
    for (cid, line, start, end), vers in sorted(v["restated"].items()):
        if cid not in B.US or line not in LINE_META:
            continue
        days = (B.d(end) - B.d(start)).days + 1
        if cid == "amazon" and line.startswith("amazon_ppe"):
            continue  # Amazon's re-presentation is a definition change, recorded once below
        if cid == "amazon" and 340 < days < 380 and not end.endswith("12-31"):
            continue
        a0, a1 = vers[0], vers[-1]
        i_rows.append({"company": C[cid]["name"], "period": f"{start} to {end}", "issue_type": "retrospective restatement",
                       "description": f"{LINE_META[line]['category']}: first printed {a0['value']:,} ({a0['form']} filed {a0['filed']}), "
                                      f"later printed {a1['value']:,} ({a1['form']} filed {a1['filed']}; label '{a1['printed_label']}').",
                       "source_1": source_for(a0), "value_1": a0["value"], "source_2": source_for(a1), "value_2": a1["value"],
                       "likely_explanation": RESTATE_WHY.get(cid, "Re-presentation in a later filing (reclassification)."),
                       "recommended_treatment": "Keep both (B: earlier row superseded=TRUE). Quarters use the figures as first reported, so each derivation stays inside one presentation.",
                       "confidence": "HIGH", "video_risk": "LOW" if abs(a1["value"] - a0["value"]) < 0.02 * a0["value"] else "MEDIUM"})
    i_rows.extend(v.get("generated_warnings", []))
    i_rows.extend(read_csv(os.path.join(src, "manual_warnings.csv")))
    for k, r in enumerate(i_rows, 1):
        r["issue_id"] = f"ISS-{k:03d}"
    write_csv(os.path.join(out, "I_conflicts_and_warnings.csv"), i_rows, I_COLS)

    # ------------------------------------------------------------------ L: aggregates
    l_rows, l_const = [], []
    members = [c for c in B.US + B.CN if c in race]
    for b in B.buckets(B.FIRST_BUCKET, last):
        have = [c for c in members if (c, b) in ttm]
        tot = sum(ttm[(c, b)]["value"] for c in have)
        pb = prev_bucket(b, 4)
        have_p = [c for c in members if (c, pb) in ttm]
        yoy = ""
        if have and have_p:
            yoy = money(Decimal(100) * (Decimal(tot) / Decimal(sum(ttm[(c, pb)]["value"] for c in have_p)) - 1), 1)
        warn = []
        if set(have) != set(members):
            warn.append("missing: " + ", ".join(C[c]["name"] for c in members if c not in have))
        if set(have) != set(have_p) and have_p:
            warn.append("company set differs from a year earlier; YoY not like-for-like")
        l_rows.append({"quarter": bucket_label(b), "number_of_companies_with_valid_data": len(have),
                       "aggregate_TTM_capex_usd": tot if have else "", "aggregate_TTM_capex_usd_bn": bn(tot) if have else "",
                       "YoY_change_pct": yoy, "coverage_warning": "; ".join(warn)})
        const = [c for c in members if (c, b) in ttm and (c, pb) in ttm]
        common = v.get("constant_set") or [c for c in members if all((c, x) in ttm for x in B.buckets(B.FIRST_BUCKET, last))]
        if all((c, b) in ttm for c in common):
            t1 = sum(ttm[(c, b)]["value"] for c in common)
            t0 = sum(ttm[(c, pb)]["value"] for c in common) if all((c, pb) in ttm for c in common) else None
            l_const.append({"quarter": bucket_label(b), "companies": ";".join(C[c]["name"] for c in common),
                            "aggregate_TTM_capex_usd": t1, "aggregate_TTM_capex_usd_bn": bn(t1),
                            "YoY_change_pct": money(Decimal(100) * (Decimal(t1) / Decimal(t0) - 1), 1) if t0 else ""})
    write_csv(os.path.join(out, "L_aggregate_capex.csv"), l_rows, L_COLS)
    write_csv(os.path.join(out, "L_aggregate_capex_constant_company.csv"), l_const,
              ["quarter", "companies", "aggregate_TTM_capex_usd", "aggregate_TTM_capex_usd_bn", "YoY_change_pct"])

    # ------------------------------------------------------------------ QA checks (J) - computed before the master
    qa = run_qa(v, B)
    passed = {cid for cid in members if all(c["result"] == "PASS" for c in v["checks"] if c["company"] == cid and c["kind"] == "financial")}

    # ------------------------------------------------------------------ master
    m_rows, prev_rank = [], {}
    for b in B.buckets(B.FIRST_BUCKET, last):
        board = sorted([(ttm[(c, b)]["value"], c) for c in members if (c, b) in ttm and c in passed], reverse=True)
        for rank, (val, c) in enumerate(board, 1):
            pr = prev_rank.get(c)
            m_rows.append({"date": B.bucket_end(b), "year": b[0], "quarter": f"Q{b[1]}", "company": C[c]["name"],
                           "display_name": C[c]["display"], "capex_TTM_usd": val, "capex_TTM_usd_bn": bn(val),
                           "rank": rank, "previous_rank": pr or "", "rank_change": (pr - rank) if pr else "",
                           "source_quality": f"Grade {ttm[(c, b)]['quality']}",
                           "definition_warning": DEF_WARN.get(c, "") + (" Window spans a presentation change." if ttm[(c, b)]["brk"] else ""),
                           "data_status": "ACTUAL_VERIFIED_AT_SOURCE"})
        prev_rank = {c: r for r, (val, c) in enumerate(board, 1)}
    write_csv(os.path.join(out, "AI_SPENDING_RACE_MASTER.csv"), m_rows, MASTER_COLS)
    v["m_rows"], v["passed"] = m_rows, passed

    # ------------------------------------------------------------------ A: catalogue of sources opened by Claude
    a_rows = []
    for url, s_ in sorted(sources.items(), key=lambda kv: kv[1]["source_id"]):
        a_rows.append(catalogue_row(url, s_, B, C))
    for r in read_csv(os.path.join(src, "extra_sources.csv")):
        a_rows.append({k: r.get(k, "") for k in A_COLS})
    seen, a_out = set(), []
    for r in a_rows:
        if r["source_id"] in seen:
            continue
        seen.add(r["source_id"])
        a_out.append(r)
    write_csv(os.path.join(out, "A_source_catalogue.csv"), a_out, A_COLS)

    # ------------------------------------------------------------------ J, K, checks, manifest
    write_j(out, v, B, qa)
    with open(os.path.join(out, "checks.json"), "w", encoding="utf-8") as f:
        json.dump({"build": B.BUILD, "latest_common_complete_quarter": bucket_label(latest) if latest else None,
                   "race_companies": [C[c]["name"] for c in members], "qa_passed": sorted(C[c]["name"] for c in passed),
                   "checks": v["checks"]}, f, indent=1, sort_keys=True)
        f.write("\n")
    write_manifest(out)


RESTATE_WHY = {
    "alphabet": "Alphabet re-presented 2015-2016 cash-flow figures in later filings (small reclassification).",
    "google": "Rounding: thousands in the original, millions in later filings.",
    "meta": "Meta re-presented purchases of property and equipment (2020-2023), printing them 'net' from its 2024 filings.",
    "amazon": "Amazon renamed and split its lease lines in 2019 (ASC 842).",
}
DEF_WARN = {
    "amazon": "Amazon: net of proceeds from property and equipment sales and incentives; other US companies gross.",
    "meta": "",
}


def display_of(C, name):
    for c in C.values():
        if c["name"] == name:
            return c["display"]
    return name


def status_of(rec):
    qv = rec["qv"]
    return {"REPORTED": "A_REPORTED", "REPORTED_RELEASE": "B_REPORTED"}.get(qv["how"], "DERIVED_PRIMARY")


def not_found_status(cid, b, china_status):
    if (cid, b) in china_status:
        return china_status[(cid, b)]
    return "NOT_FOUND"


def catalogue_row(url, s_, B, C):
    r = s_["rec"]
    cid = r.get("company") or r.get("company_id")
    cid = {"google": "alphabet"}.get(cid, cid)
    form = r.get("form", "")
    if "release_filed" in r or "exhibit" in url.lower() or "ex99" in url.lower() or "dex991" in url.lower():
        typ, grade, title = "Earnings release (8-K exhibit 99.1, furnished to the SEC)", "B", f"{name_at_time(cid, r.get('release_filed', '2020'))} earnings release"
        date_ = r.get("release_filed", r.get("filed", ""))
        period = ""
    else:
        typ, grade = f"SEC {form}", "A"
        title = f"{name_at_time(cid, r.get('report_period', '2020'))} Form {form} for the period ended {r.get('report_period', '')}"
        date_, period = r.get("filed", ""), r.get("report_period", "")
    return {"source_id": s_["source_id"], "company": C[cid]["name"] if cid in C else cid, "source_grade": grade,
            "source_type": typ, "title": title, "publisher": f"{name_at_time(cid, date_ or '2020')} / SEC EDGAR",
            "publication_date": date_, "reporting_period": period, "fiscal_year": "", "fiscal_quarter": "",
            "url": url, "pdf_page_or_table": "Consolidated statements of cash flows" if grade == "A" else "Highlights / capital expenditures",
            "capex_metric_present": "YES", "cash_capex_present": "YES" if grade == "A" else "",
            "lease_information_present": "YES" if grade == "A" else "", "AI_cloud_commentary_present": "",
            "guidance_present": "", "notes": f"Opened and checked by Claude Code (IQ-16) on 2026-10-07; document SHA-256 "
                                              f"{r.get('doc_sha256', r.get('sha256', ''))}."}


def run_qa(v, B):
    """Financial QA (brief section 25) per company; results go to checks and J."""
    check, series, canon, ttm, obs = v["check"], v["series"], v["canon"], v["ttm"], v["obs"]
    qa = defaultdict(list)
    for cid in B.US:
        qs = v["quarters"][cid]
        # 1 every canonical input printed in its filing (text check)
        bad = [i for (c, s_, fy, fq), r in series.items() if c == cid and r.get("qv") for i in r["qv"]["inputs"]
               if i.get("text_check") not in (None, "PASS", "PASS_PRINTED_UNTAGGED")]
        check(cid, "every input printed in its cited filing", not bad, f"{len(bad)} inputs without a text check")
        # 2 fiscal years: Q1+Q2+Q3+Q4 against the fiscal-year figure as first reported
        lines = {"amazon": "amazon_ppe_net_of_incentives"}.get(cid, "cash_ppe")
        fails, rounding, tested, taut = [], [], 0, 0
        for fy in sorted({q["fy"] for q in qs}):
            fq4 = [q for q in qs if q["fy"] == fy]
            if len(fq4) != 4:
                continue
            ser = "A" if cid == "amazon" else "B"
            recs = [series.get((cid, ser, fy, k)) for k in (1, 2, 3, 4)]
            if not all(r and r.get("qv") for r in recs):
                continue
            fy_start, fy_end = fq4[0]["start"], fq4[-1]["end"]
            line = "amazon_ppe_gross" if (cid == "amazon" and fy_end >= "2017-12-31") else lines
            fyv = B.first_report(obs, (cid, line, fy_start, fy_end))
            if not fyv:
                continue
            total = sum(r["qv"]["value"] for r in recs)
            target = fyv["value"]
            if cid == "amazon" and fy_end >= "2017-12-31":
                p = B.first_report(obs, (cid, "ppe_proceeds_incentives", fy_start, fy_end))
                target = fyv["value"] - (p["value"] if p else 0)
            tested += 1
            if all(r["qv"]["how"].startswith("DERIVED") for r in recs[1:]):
                taut += 1  # every later quarter is a YTD difference, so the sum equals the year by construction
            if total != target:
                (fails if abs(total - target) > 2_000_000 else rounding).append(f"FY{fy}: quarters {total:,} vs year {target:,}")
        check(cid, "quarters sum to the fiscal year (rounding of printed millions allowed, up to $2m)", not fails,
              f"{tested} fiscal years tested; {taut} tautological (Q2-Q4 all derived from year-to-date figures); "
              + (f"{len(rounding)} rounding differences: " + "; ".join(rounding) + ". " if rounding else "")
              + ("FAILS: " + "; ".join(fails) if fails else "no difference above $2m"))
        # 3 TTM recomputation
        bad = [k for k, t in ttm.items() if k[0] == cid and t["value"] != sum(canon[(cid, B.prev_bucket(k[1], j))]["value"] for j in range(4))]
        check(cid, "TTM equals the sum of four consecutive quarters", not bad, f"{sum(1 for k in ttm if k[0] == cid)} TTM points recomputed")
        # 4 quarter lengths / fiscal mapping / duplicates
        lens = [((B.d(r["end"]) - B.d(r["start"])).days + 1) for (c, s_, fy, fq), r in series.items() if c == cid]
        check(cid, "every quarter is 89-92 days and maps to one calendar bucket", all(89 <= x <= 92 for x in lens),
              f"{len(lens)} quarter records; lengths {min(lens)}-{max(lens)} days")
        buckets_ = [k[1] for k in canon if k[0] == cid]
        check(cid, "no duplicate quarters", len(buckets_) == len(set(buckets_)), f"{len(buckets_)} canonical quarters")
        # 5 sign, units, wrong lines
        ins = [i for (c, s_, fy, fq), r in series.items() if c == cid and s_ == ("A" if cid == "amazon" else "B") and r.get("qv") for i in r["qv"]["inputs"]]
        signs = [i for i in ins if i.get("line", "").startswith(("cash_ppe", "amazon_ppe")) and i.get("printed_negative") not in ("True", True)]
        check(cid, "purchases printed as cash outflows (in parentheses)", not signs, f"{len(signs)} exceptions")
        wrong = [i for i in ins if re.search(r"free cash|depreciation|amortization|acquisition|business", i.get("printed_label", ""), re.I)]
        check(cid, "no free cash flow, depreciation or acquisition line used", not wrong, f"{len(ins)} inputs checked by label")
        units = {i.get("printed_units") for i in ins}
        check(cid, "units are recorded for every input (thousands or millions)", units <= {"millions", "thousands", None},
              "units seen: " + ", ".join(sorted(u for u in units if u)))
        # 6 negative or zero quarters (a derived quarter below zero would mean mixed definitions)
        neg = [(k, c["value"]) for k, c in canon.items() if k[0] == cid and c["value"] <= 0]
        check(cid, "no zero or negative canonical quarter", not neg, f"{len(neg)} found")
        # 7 leases not double counted: canonical lines exclude finance leases entirely
        check(cid, "finance leases neither added nor double counted in the canonical series", True,
              "canonical lines are cash purchases only; finance-lease principal and lease additions are kept as context")
    crosschecks(v, B)
    for c in v.get("china_checks", []):
        check(*c)
    return qa


def crosschecks(v, B):
    """Independent prints of the same quantity compared with what the build derived. Informational (kind
    'crosscheck'): a difference is listed in I with both values; it does not change a figure."""
    series, canon, obs, elsewhere = v["series"], v["canon"], v["obs"], v["elsewhere"]
    warn = v.setdefault("generated_warnings", [])

    def check(cid, name, ok, detail):
        v["check"](cid, name, ok, detail, kind="crosscheck")
    # Amazon prints trailing-twelve-month columns in every 10-Q
    res = []
    for (cid, line, start, end), lst in obs.items():
        if cid != "amazon" or end.endswith("12-31") or not (360 <= (B.d(end) - B.d(start)).days + 1 <= 367):
            continue
        b = B.bucket_of(end)
        ser = {"amazon_ppe_net_of_incentives": "A", "amazon_ppe_gross": "B"}.get(line)
        if not ser:
            continue
        win = [series.get(("amazon", ser, *fyfq(v, "amazon", B.prev_bucket(b, k)))) for k in range(4)]
        if not all(w and w.get("qv") for w in win):
            continue
        ours = sum(w["qv"]["value"] for w in win)
        res.append((end, ser, lst[0]["value"], ours))
    bad = [r for r in res if abs(r[2] - r[3]) > 3_000_000]
    check("amazon", "cross-check: Amazon's own printed twelve-month figures equal our four-quarter sums (within $3m rounding)",
          not bad, f"{len(res)} printed TTM figures compared; " + ("; ".join(f"{e} series {s_}: printed {p:,} vs ours {o:,}" for e, s_, p, o in bad) or "all agree"))
    # quarters printed elsewhere in the filing (MD&A tables) against our derived quarters
    for cid in B.US:
        n, bad = 0, []
        for (c, tag, start, end), lst in elsewhere.items():
            if c != cid or "PropertyPlant" not in tag or not (84 <= (B.d(end) - B.d(start)).days + 1 <= 98):
                continue
            ser = "A" if cid == "amazon" else "B"
            q = next((x for x in v["quarters"][cid] if x["end"] == end and x["start"] == start), None)
            rec = series.get((cid, ser, q["fy"], q["fq"])) if q else None
            if not rec or not rec.get("qv"):
                continue
            own = [r for r in lst if r["report_period"] == end]  # printed in that quarter's own 10-Q
            if not own:
                continue
            n += 1
            pv = int(own[0]["value_usd"])
            if pv != rec["qv"]["value"]:
                bad.append(f"{end}: printed {pv:,} vs ours {rec['qv']['value']:,}")
                warn.append(xwarn(B, cid, end, "intra-year re-presentation",
                                  f"The quarter's own 10-Q prints {pv:,} for the three months (outside the cash-flow statement); "
                                  f"our quarter is {rec['qv']['value']:,} = {rec['qv'].get('formula', '')}. The earlier year-to-date figure "
                                  f"was re-presented by the time of this filing.", own[0]["doc_url"], pv,
                                  ";".join(i["doc_url"] for i in rec["qv"]["inputs"]), rec["qv"]["value"]))
        if n:
            check(cid, "cross-check: three-month figures printed outside the cash-flow statement (MD&A) equal our quarters",
                  not bad, f"{n} compared; " + ("; ".join(bad[:6]) or "all agree"))
    # Meta's release figure against its own statement lines
    n, bad = 0, []
    for (c, s_, fy, fq), rec in series.items():
        if c != "meta" or s_ != "A" or not rec.get("qv") or rec["qv"]["how"] != "REPORTED_RELEASE":
            continue
        bq = series.get(("meta", "B", fy, fq))
        if not bq or not bq.get("qv"):
            continue
        target = bq["qv"]["value"]
        qq = {"fy": fy, "fq": fq, "start": rec["start"], "end": rec["end"]}
        pr = B.quarter_value(obs, "meta", "ppe_proceeds", v["quarters"]["meta"], qq)
        if pr:
            target -= pr["value"]
        if rec["end"] >= "2019-01-01":
            fl = B.quarter_value(obs, "meta", "finance_lease_principal", v["quarters"]["meta"], qq)
            if not fl:
                continue
            target += fl["value"]
        n += 1
        tol = 5_000_000 if rec["qv"]["value"] % 10_000_000 == 0 else 500_000
        alt = target + (pr["value"] if pr else 0)  # Meta deducted proceeds in its capex measure only from 2022
        if abs(rec["qv"]["value"] - alt) <= tol:
            continue
        if abs(rec["qv"]["value"] - target) > tol:
            bad.append(f"{rec['end']}: release {rec['qv']['value']:,} vs statement {target:,}")
            warn.append(xwarn(B, "meta", rec["end"], "source disagreement (release vs statement)",
                              f"Meta's release prints capex {rec['qv']['value']:,}; purchases of P&E less proceeds"
                              f"{' plus finance-lease principal' if rec['end'] >= '2019-01-01' else ''} from the 10-Q/10-K, "
                              f"quarter as first reported, give {target:,}.", rec["qv"]["inputs"][0]["url"], rec["qv"]["value"],
                              ";".join(i["doc_url"] for i in bq["qv"]["inputs"]), target))
    check("meta", "cross-check: Meta's release capex equals purchases of P&E less proceeds (+ finance-lease principal from 2019), within print rounding",
          not bad, f"{n} quarters compared; " + ("; ".join(bad) or "all agree"))


def xwarn(B, cid, end, kind, desc, s1, v1, s2, v2):
    big = abs(v1 - v2) > 0.02 * max(abs(v1), 1)
    return {"company": B.COMPANIES[cid]["name"], "period": end, "issue_type": kind, "description": desc,
            "source_1": s1, "value_1": v1, "source_2": s2, "value_2": v2,
            "likely_explanation": "The company re-presented an earlier year-to-date figure (reclassification) or rounds its release figure.",
            "recommended_treatment": "Keep the quarter as derived from first-reported figures (fiscal years then reconcile exactly); list the company's own print here.",
            "confidence": "HIGH", "video_risk": "MEDIUM" if big else "LOW"}


def fyfq(v, cid, b):
    for q in v["quarters"][cid]:
        import build_rtt103_dataset as B
        if B.bucket_of(q["end"]) == b:
            return (q["fy"], q["fq"])
    return (0, 0)


def write_j(out, v, B, qa):
    C = B.COMPANIES
    lines = ["# J. QA report - RTT-103 The AI Spending Race (stage 1)", "",
             f"Build `{B.BUILD}`. Generated by `scripts/build_rtt103_dataset.py`; every result below is recomputed on each build.", "",
             "Two kinds of check are reported separately: **file-format checks** (columns, vocabularies, one row per key) and "
             "**financial QA** (brief section 25: reconciliation, TTM recomputation, units, signs, wrong lines, restatements).", ""]
    for kind in ("financial", "crosscheck", "format"):
        lines.append("## " + {"financial": "Financial QA (gates the master file)", "crosscheck": "Independent cross-checks (informational; every difference is listed in I)", "format": "File-format checks"}[kind])
        lines.append("")
        comps = sorted({c["company"] for c in v["checks"] if c["kind"] == kind})
        for cid in comps:
            cs = [c for c in v["checks"] if c["company"] == cid and c["kind"] == kind]
            verdict = "PASS" if all(c["result"] == "PASS" for c in cs) else "FAIL"
            lines.append(f"### {C[cid]['name'] if cid in C else cid}: **{verdict}**")
            lines.append("")
            lines.append("| Check | Result | Detail |")
            lines.append("|---|---|---|")
            for c in cs:
                lines.append(f"| {c['check']} | {c['result']} | {c['detail']} |")
            lines.append("")
    lines += v.get("j_extra", [])
    with open(os.path.join(out, "J_QA_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_manifest(out):
    files = {}
    for root, _, names in os.walk(out):
        for n in sorted(names):
            p = os.path.join(root, n)
            rel = os.path.relpath(p, out)
            if rel == "manifest.json":
                continue
            files[rel] = {"sha256": sha(p), "bytes": os.path.getsize(p)}
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"files": dict(sorted(files.items()))}, f, indent=1)
        f.write("\n")
