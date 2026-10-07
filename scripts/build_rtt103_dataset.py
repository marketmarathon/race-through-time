#!/usr/bin/env python3
"""RTT-103 The AI Spending Race: deterministic dataset build (IQ-16, stage 1).

Usage:  python scripts/build_rtt103_dataset.py data/rtt-103 [private_rtt103_dir]

Inputs (data/rtt-103/source/, all committed and public):
  us_cashflow_observations.csv  every capex-related cash-flow figure of Amazon, Microsoft, Alphabet/Google, Meta, Oracle
                                10-Qs/10-Ks from 2009, each checked as PRINTED in the filing's cash-flow statement
                                (scripts/rtt103_us_extract.py)
  meta_release_capex.csv        Meta's own quarterly "Capital expenditures" figure from each earnings release
  release_statements.csv        candidate sentences for F and G (scripts/rtt103_release_extract.py)
  sec_filing_documents.csv, sec_release_documents.csv   URL + SHA-256 of every SEC document read
  china_observations.csv        China-listed companies' figures transcribed from their filings (RMB), with quotes
  fx_cny_per_usd_daily.csv      Federal Reserve H.10 noon buying rates, CNY per USD (FRED DEXCHUS)
  guidance_2026.csv             2026 capex guidance and estimates (file F), each with its verbatim quote
  story_events.csv              AI / cloud capex statements and commitments (file G)
  definitions.csv               capex definition history per company (file C)
  entities.csv                  entity / name history (Google -> Alphabet, Facebook -> Meta)
  extra_sources.csv             sources Claude opened that are not SEC filings (issuer PDFs, HKEXnews, FX, guidance)
  manual_warnings.csv           hand-written conflicts / warnings (file I) in addition to the generated ones
Optional (private repo, never written to public files): Sharadar extract for the cross-check summary.

Outputs (data/rtt-103/): A..L files and the two masters with the brief's exact columns, companion audit files,
checks.json and manifest.json. Standard library only; the same inputs give byte-identical outputs.
"""
import csv
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

BUILD = "rtt103-build/1.0"
CUTOFF = "2026-10-07"
FIRST_BUCKET = (2010, 1)          # first race quarter (TTM needs 2009 Q2 onwards)
LAST_BUCKET_CANDIDATE = (2026, 3)  # nothing later is considered at all

COMPANIES = {
    # company_id: display, legal name history, fiscal-year-end month, currency, data source keys, race candidate
    "amazon": {"name": "Amazon", "display": "Amazon", "fye": 12, "ccy": "USD", "src": ["amazon"]},
    "microsoft": {"name": "Microsoft", "display": "Microsoft", "fye": 6, "ccy": "USD", "src": ["microsoft"]},
    "alphabet": {"name": "Alphabet", "display": "Alphabet (Google)", "fye": 12, "ccy": "USD", "src": ["google", "alphabet"]},
    "meta": {"name": "Meta", "display": "Meta (Facebook)", "fye": 12, "ccy": "USD", "src": ["meta"]},
    "oracle": {"name": "Oracle", "display": "Oracle", "fye": 5, "ccy": "USD", "src": ["oracle"]},
    "alibaba": {"name": "Alibaba", "display": "Alibaba", "fye": 3, "ccy": "CNY", "src": ["alibaba"]},
    "tencent": {"name": "Tencent", "display": "Tencent", "fye": 12, "ccy": "CNY", "src": ["tencent"]},
    "baidu": {"name": "Baidu", "display": "Baidu", "fye": 12, "ccy": "CNY", "src": ["baidu"]},
}
H_COLUMNS = ["Amazon", "Microsoft", "Alphabet", "Meta", "Oracle", "Alibaba", "Tencent", "Baidu", "ByteDance"]
US = ["amazon", "microsoft", "alphabet", "meta", "oracle"]
CN = ["alibaba", "tencent", "baidu"]

# Amazon re-presented its cash-flow statement from the FY2017 10-K: purchases of property and equipment GROSS, with
# "proceeds from property and equipment incentives" (later "sales and incentives") on their own line. Before that the
# single line was net of incentives (its label gained ", net" in 2016). Filing date decides which line a figure is.
AMAZON_GROSS_FROM = "2018-02-01"  # the FY2017 10-K (filed 2 Feb 2018) is the first gross presentation


# ----------------------------------------------------------------------------------------------- small helpers
def d(s):
    return date.fromisoformat(s)


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="raise")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})


def bucket_of(end):
    e = d(end) if isinstance(end, str) else end
    return (e.year, (e.month - 1) // 3 + 1)


def bucket_label(b):
    return f"{b[0]}-Q{b[1]}"


def prev_bucket(b, n=1):
    y, q = b
    for _ in range(n):
        y, q = (y, q - 1) if q > 1 else (y - 1, 4)
    return (y, q)


def bucket_end(b):
    y, q = b
    m = 3 * q
    return (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).isoformat()


def buckets(first, last):
    out, b = [], first
    while b <= last:
        out.append(b)
        b = (b[0], b[1] + 1) if b[1] < 4 else (b[0] + 1, 1)
    return out


def month_end(y, m):
    return date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)


def fiscal_quarters(fye):
    """Every fiscal quarter (fy, fq, start, end) whose end falls 2008-01-01..2026-12-31."""
    months = sorted({(fye - 1 - 3 * k) % 12 + 1 for k in range(4)})
    ends = sorted(month_end(y, m) for y in range(2007, 2027) for m in months)
    out = []
    for i in range(1, len(ends)):
        e = ends[i]
        fq = ((e.month - fye - 1) % 12) // 3 + 1
        fy = e.year if e.month <= fye else e.year + 1
        out.append({"fy": fy, "fq": fq, "start": (ends[i - 1] + timedelta(days=1)).isoformat(), "end": e.isoformat()})
    return [q for q in out if "2008-01-01" <= q["end"] <= "2026-12-31"]


def fy_start(quarters, fy):
    return min(q["start"] for q in quarters if q["fy"] == fy)


def money(v, places=0):
    q = Decimal(1).scaleb(-places)
    return str(Decimal(v).quantize(q, rounding=ROUND_HALF_UP))


def bn(v):
    return money(Decimal(v) / Decimal(10 ** 9), 3)


# ------------------------------------------------------------------------------------------- US observations
def load_us(src):
    """Printed cash-flow figures that passed the text check, grouped by line and period, first report first."""
    rows = [r for r in read_csv(os.path.join(src, "us_cashflow_observations.csv"))
            if r["text_check"] in ("PASS", "PASS_PRINTED_UNTAGGED")]
    elsewhere = [r for r in read_csv(os.path.join(src, "us_cashflow_observations.csv"))
                 if r["text_check"] == "NOT_IN_CF_STATEMENT_PRINTED_ELSEWHERE"]
    to_company = {s: c for c, v in COMPANIES.items() for s in v["src"]}
    obs = defaultdict(list)  # (company, line, start, end) -> [row,...]
    for r in rows:
        if r["company_id"] not in to_company:
            continue  # CoreWeave: eligibility table only (brief section 2), never in the race
        cid = to_company[r["company_id"]]
        role = r["line_role"]
        if role == "ppe_purchases":
            if cid == "amazon":
                line = "amazon_ppe_gross" if r["filed"] >= AMAZON_GROSS_FROM else "amazon_ppe_net_of_incentives"
            else:
                line = "cash_ppe"
        elif role in ("ppe_proceeds_incentives", "finance_lease_principal", "financing_obligation_principal",
                      "ppe_acquired_finance_leases", "ppe_proceeds"):
            line = role
        else:
            continue
        r = dict(r, company=cid, line=line, value=int(r["value_usd"]))
        obs[(cid, line, r["period_start"], r["period_end"])].append(r)
    for k in obs:
        # first report first; the same accession can hold the same period twice (two statements) - keep one
        seen, uniq = set(), []
        for r in sorted(obs[k], key=lambda r: (r["filed"], r["accession"], r["value"])):
            if (r["accession"], r["value"]) in seen:
                continue
            seen.add((r["accession"], r["value"]))
            uniq.append(r)
        obs[k] = uniq
    printed_elsewhere = defaultdict(list)
    for r in elsewhere:
        if r["company_id"] not in to_company:
            continue
        cid = to_company[r["company_id"]]
        printed_elsewhere[(cid, r["xbrl_tag"], r["period_start"], r["period_end"])].append(r)
    return obs, printed_elsewhere


def read_csv_skip_comments(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def first_report(obs, key):
    lst = obs.get(key)
    return lst[0] if lst else None


def quarter_value(obs, cid, line, quarters, q):
    """A quarter's value for one line: printed 3-month figure, else exact YTD subtraction within one definition."""
    direct = first_report(obs, (cid, line, q["start"], q["end"]))
    if direct:
        return {"value": direct["value"], "how": "REPORTED", "inputs": [direct], "formula": ""}
    fys = fy_start(quarters, q["fy"])
    ytd = first_report(obs, (cid, line, fys, q["end"]))
    if not ytd:
        return None
    if q["fq"] == 1:
        return {"value": ytd["value"], "how": "REPORTED", "inputs": [ytd], "formula": ""}
    prev = [p for p in quarters if p["fy"] == q["fy"] and p["fq"] == q["fq"] - 1][0]
    prior = first_report(obs, (cid, line, fys, prev["end"]))
    if not prior:
        return None
    dur = {2: "six months", 3: "nine months", 4: "fiscal year"}[q["fq"]]
    pdur = {1: "three months", 2: "six months", 3: "nine months"}[q["fq"] - 1]
    return {"value": ytd["value"] - prior["value"], "how": "DERIVED", "inputs": [ytd, prior],
            "formula": f"{dur} to {q['end']} ({ytd['value']}) minus {pdur} to {prev['end']} ({prior['value']})"}


def restatements(obs):
    """(company, line, start, end) where a later filing prints a different value for the same line and period."""
    out = {}
    for k, lst in obs.items():
        vals = []
        for r in lst:
            if r["value"] not in [v["value"] for v in vals]:
                vals.append(r)
        if len(vals) > 1:
            out[k] = vals
    return out


# ---------------------------------------------------------------------------------------- China-listed companies
ALIBABA_CANON_SCOPE = "capex_ppe_incl_land_use_rights_and_cip"


def rounding_tolerance(printed_value):
    """Half a unit of the last printed digit: 'RMB2.0 billion' -> RMB50m; 'RMB81.7 million' -> RMB0.05m."""
    m = re.search(r"([\d,]+)(?:\.(\d+))?\s*(billion|million)", printed_value)
    if not m:
        return 0
    places = len(m.group(2) or "")
    unit = 1e9 if m.group(3) == "billion" else 1e6
    return 0.5 * unit / (10 ** places)


def load_china(src):
    obs = defaultdict(list)
    for r in read_csv(os.path.join(src, "china_observations.csv")):
        if r["verified"] != "VERIFIED" or not r["value_local"]:
            continue
        line = r["line"]
        if r["company_id"] == "alibaba":
            scope = re.search(r"scope=(\w+)", r["notes"]).group(1)
            if scope != ALIBABA_CANON_SCOPE:
                line = "company_capex_broader_scope"
        rec = dict(r, company=r["company_id"], line=line, value=int(r["value_local"]), filed=r["publication_date"],
                   doc_url=r["source_url"], accession=r["source_id"], printed_label=r["metric_name_exact"], text_check="PASS",
                   rounded="rounded" in r["printed_units"], printed_negative="")
        obs[(r["company_id"], line, r["period_start"], r["period_end"])].append(rec)
    for k, lst in obs.items():
        seen, uniq = set(), []
        for r in sorted(lst, key=lambda r: (r["filed"], r["rounded"] is False, r["source_id"])):
            if (r["source_id"], r["value"]) in seen:
                continue
            seen.add((r["source_id"], r["value"]))
            uniq.append(r)
        # a rounded first print gives way to a later exact print of the same figure (within the rounding)
        if uniq[0]["rounded"]:
            tol = rounding_tolerance(uniq[0]["printed_value"])
            exact = [r for r in uniq[1:] if not r["rounded"] and abs(r["value"] - uniq[0]["value"]) <= tol]
            if exact:
                e = dict(exact[0], precision_note=f"First printed rounded as {uniq[0]['printed_value']} ({uniq[0]['source_id']}, "
                                                  f"{uniq[0]['filed']}); exact figure from a later filing used.")
                uniq = [e] + [r for r in uniq if r is not exact[0]]
        obs[k] = uniq
    return obs


def china_quarter(obs, cid, line, qs, q):
    v = quarter_value(obs, cid, line, qs, q)
    if v:
        return v
    # a year-to-date figure minus the other quarters of that year-to-date, each printed (Alibaba June 2013)
    fys = fy_start(qs, q["fy"])
    for later in [p for p in qs if p["fy"] == q["fy"] and p["fq"] > q["fq"]]:
        ytd = first_report(obs, (cid, line, fys, later["end"]))
        if not ytd:
            continue
        others = [p for p in qs if p["fy"] == q["fy"] and p["fq"] <= later["fq"] and p is not q]
        parts = [first_report(obs, (cid, line, p["start"], p["end"])) for p in others]
        if all(parts):
            val = ytd["value"] - sum(x["value"] for x in parts)
            return {"value": val, "how": "DERIVED", "inputs": [ytd] + parts,
                    "formula": f"year-to-date to {later['end']} ({ytd['value']}) minus " +
                               " minus ".join(f"quarter to {p['end']} ({x['value']})" for p, x in zip(others, parts))}
    return None


def fx_rates(rows):
    return [(r["date"], Decimal(r["cny_per_usd"])) for r in rows if r.get("cny_per_usd")]


def fx_mean(fx, start, end):
    vals = [v for dte, v in fx if start <= dte <= end]
    if not vals:
        return None
    mean = (sum(vals) / len(vals)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
    return {"rate": str(mean), "days": len(vals), "source": "Federal Reserve H.10 (CNY per USD, noon buying rates in New York), "
            f"mean of {len(vals)} daily rates {start} to {end}; days without a rate (ND) excluded, never filled",
            "rate_dec": mean}


# ------------------------------------------------------------------------------------------------------ main
def main():
    out = sys.argv[1]
    private = sys.argv[2] if len(sys.argv) > 2 else ""
    src = os.path.join(out, "source")
    obs, elsewhere = load_us(src)
    restated = restatements(obs)
    meta_rel = {r["quarter_end"]: r for r in read_csv(os.path.join(src, "meta_release_capex.csv"))}
    china = read_csv(os.path.join(src, "china_observations.csv"))
    fx_daily = read_csv(os.path.join(src, "fx_cny_per_usd_daily.csv"))
    docs = {r["url"]: r for r in read_csv(os.path.join(src, "sec_filing_documents.csv"))}

    quarters = {cid: fiscal_quarters(c["fye"]) for cid, c in COMPANIES.items()}
    cobs = load_china(src)
    obs.update(cobs)
    fx = fx_rates([r for r in read_csv_skip_comments(os.path.join(src, "fx_cny_per_usd_daily.csv"))])
    china_status = {}
    series = {}  # (cid, series 'A'|'B', fy, fq) -> record
    for cid in US:
        qs = quarters[cid]
        for q in qs:
            b = bucket_of(q["end"])
            if b < prev_bucket(FIRST_BUCKET, 3) or b > LAST_BUCKET_CANDIDATE:
                continue
            base = {"company_id": cid, "fy": q["fy"], "fq": q["fq"], "start": q["start"], "end": q["end"], "bucket": b}
            # ---- Series B: cash purchases of property and equipment (gross where the company prints it gross)
            bline = "amazon_ppe_gross" if cid == "amazon" else "cash_ppe"
            v = quarter_value(obs, cid, bline, qs, q)
            series[(cid, "B", q["fy"], q["fq"])] = dict(base, series="B", line=bline, qv=v)
            # ---- Series A: the company's own "capital expenditures" measure
            if cid in ("alphabet", "oracle"):
                a = quarter_value(obs, cid, "cash_ppe", qs, q)
                series[(cid, "A", q["fy"], q["fq"])] = dict(base, series="A", line="cash_ppe", qv=a)
            elif cid == "microsoft":
                series[(cid, "A", q["fy"], q["fq"])] = dict(base, series="A", line="", qv=None,
                                                            why="NOT_FOUND: no company-defined capex figure in SEC filings or SEC-furnished releases")
            elif cid == "meta":
                rel = meta_rel.get(q["end"])
                if rel:
                    a = {"value": int(rel["value_usd"]), "how": "REPORTED_RELEASE", "inputs": [rel], "formula": ""}
                elif q["end"] < "2019-01-01":
                    a = quarter_value(obs, cid, "cash_ppe", qs, q)  # before 2019 Meta's capex = purchases of P&E
                else:
                    a = None
                series[(cid, "A", q["fy"], q["fq"])] = dict(base, series="A", line="meta_capex_release", qv=a)
            elif cid == "amazon":
                if q["end"] < "2017-01-01":
                    a = quarter_value(obs, cid, "amazon_ppe_net_of_incentives", qs, q)
                else:
                    g = quarter_value(obs, cid, "amazon_ppe_gross", qs, q)
                    p = quarter_value(obs, cid, "ppe_proceeds_incentives", qs, q)
                    a = None
                    if g and p:
                        how = "DERIVED_SAME_FILING" if g["how"] == p["how"] == "REPORTED" else "DERIVED"
                        a = {"value": g["value"] - p["value"], "how": how, "inputs": g["inputs"] + p["inputs"],
                             "formula": f"purchases of property and equipment ({g['value']}{'; ' + g['formula'] if g['formula'] else ''}) "
                                        f"minus proceeds from property and equipment sales and incentives ({p['value']}"
                                        f"{'; ' + p['formula'] if p['formula'] else ''}), same quarter, same definition"}
                    if q["end"] < AMAZON_GROSS_FROM:  # 2017: first printed net (as Amazon's single line at the time)
                        n = quarter_value(obs, cid, "amazon_ppe_net_of_incentives", qs, q)
                        if n:
                            n["crosscheck"] = a
                            a = n
                series[(cid, "A", q["fy"], q["fq"])] = dict(base, series="A", line="amazon_ppe_net_of_incentives", qv=a)

    for cid in CN:
        qs = quarters[cid]
        for q in qs:
            b = bucket_of(q["end"])
            if b < prev_bucket(FIRST_BUCKET, 3) or b > LAST_BUCKET_CANDIDATE:
                continue
            base = {"company_id": cid, "fy": q["fy"], "fq": q["fq"], "start": q["start"], "end": q["end"], "bucket": b}
            a = china_quarter(obs, cid, "company_capex", qs, q)
            broad = None if a else china_quarter(obs, cid, "company_capex_broader_scope", qs, q)
            rate = fx_mean(fx, q["start"], q["end"])
            for v in (a, broad):
                if v and rate:
                    v["value_usd"] = int((Decimal(v["value"]) / rate["rate_dec"]).quantize(Decimal(1), rounding=ROUND_HALF_UP))
                    if v["how"] == "REPORTED" and v["inputs"][0].get("grade") == "B":
                        v["how"] = "REPORTED_RELEASE"
            rec = dict(base, series="A", line="company_capex", qv=a, fx=rate)
            if broad:
                rec["why"] = ("DEFINITION_BREAK: Alibaba printed 'capital expenditures and (acquisition of) intangible assets"
                              f"{' and licensed copyrights' if 'licensed' in broad['inputs'][0]['printed_label'].lower() else ''}' "
                              f"of RMB{broad['value']:,} for this quarter, a broader scope than its capex before and after; not spliced")
                rec["broad"] = broad
                china_status[(cid, b)] = "DEFINITION_BREAK"
            series[(cid, "A", q["fy"], q["fq"])] = rec
            if cid in ("baidu", "alibaba"):
                series[(cid, "B", q["fy"], q["fq"])] = dict(base, series="B", line="company_capex", qv=a, fx=rate)
            else:
                series[(cid, "B", q["fy"], q["fq"])] = dict(base, series="B", line="", qv=None, fx=rate,
                                                            why="NOT_FOUND quarterly: Tencent prints cash purchases of PP&E half-yearly only")
    assemble(out, src, private, quarters, series, obs, elsewhere, restated, meta_rel, china, fx_daily, docs, china_status)
    return 0


from rtt103_outputs import assemble  # noqa: E402  (outputs A-L, masters, checks)


if __name__ == "__main__":
    sys.exit(main())
