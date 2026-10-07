#!/usr/bin/env python3
"""RTT-103 (IQ-16): US companies - capex-related cash-flow lines from SEC filings, each XBRL value checked in the filing.

Method (brief sections 7, 9, 17; CODE_SESSION_IQ-16 "every XBRL value is checked against the filing text"):
 1. For each filing (10-Q / 10-K, from 2009), the cash-flow statement section kept by rtt103_sec_docs.py is split
    into rows: printed label + printed numbers.
 2. Each line we need (ROLES below) is identified by its PRINTED LABEL (regex), never by the XBRL tag alone.
 3. Every XBRL duration fact of that filing (company facts snapshot; any tag) whose value, in the statement's units,
    is printed on that row is taken as an observation of that line for the fact's period. The XBRL fact supplies the
    period; the printed row supplies the evidence. text_check = PASS.
 4. Every XBRL fact whose tag is a known capex-line tag (TAGS_TO_CHECK) but whose value is NOT printed on a matching
    row of that filing's statement is recorded with text_check = FAIL (and never used).
Output: one CSV row per (company, line, period, filing) - the audit list behind B_capex_observations.csv.

Usage: rtt103_us_extract.py <snapshot_dir> <cf_dir> <docs_index_csv> <out_csv> <text_cache_dir>
A fact not on the statement but printed elsewhere in the same filing (for example the MD&A) on a line about property
and equipment, capex or finance leases gets text_check = NOT_IN_CF_STATEMENT_PRINTED_ELSEWHERE: cross-check only.
"""
import csv
import datetime as dt
import gzip
import json
import os
import re
import sys

# line role -> (printed-label regex, metric_category). Checked in this order; first match wins for a row.
# Amazon before ASC 842 (2019): "Principal repayments of finance lease obligations" were build-to-suit FINANCING
# obligations (renamed "financing obligations" from 2019), while "capital lease obligations" became "finance leases".
ROLES = [
    ("ppe_proceeds_incentives", r"^proceeds from property and equipment (sales and )?incentives|^proceeds from property and equipment sales",
     "ppe_sale_proceeds_and_incentives"),
    ("ppe_noncash_note", r"^(purchases of property and equipment|property and equipment purchases).*(included in|accrued|unpaid|not yet paid)",
     "ppe_purchases_unpaid_noncash"),
    ("financing_obligation_principal", r"^principal repayments? of financing obligations|^repayments? of financing obligations|"
                                       r"^principal repayments? of finance lease obligations",
     "financing_obligation_principal_payments"),
    ("ppe_purchases", r"^(purchases of (property and equipment|fixed assets|property, plant and equipment)|"
                      r"additions to property and equipment|capital expenditures$|payments for property and equipment)",
     "cash_purchases_of_ppe"),
    ("finance_lease_principal", r"^(principal (re)?payments? (on|of) (finance|capital) lease|"
                                r"repayments? of (finance|capital) lease|principal payments on finance and capital lease|"
                                r"payments? (on|of) (finance|capital) lease|principal repayments of capital and finance lease)",
     "finance_lease_principal_payments"),
    ("debt_and_capital_lease_repayments", r"^repayments? of (long-term )?debt and capital lease", "debt_and_capital_lease_repayments"),
    ("ppe_acquired_finance_leases", r"^(property and equipment|fixed assets) acquired under (finance|capital) leases",
     "ppe_acquired_under_finance_leases_noncash"),
    ("ppe_acquired_build_to_suit", r"^(property and equipment|fixed assets) (acquired|recognized) (under|during construction in) build-to-suit",
     "ppe_build_to_suit_noncash"),
    ("ppe_proceeds", r"^proceeds from (the )?sales? of property and equipment|^proceeds from disposal of property|"
                     r"^proceeds relating to property and equipment",
     "ppe_sale_proceeds"),
]
TAGS_TO_CHECK = {"PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets",
                 "PaymentsForProceedsFromProductiveAssets", "FinanceLeasePrincipalPayments",
                 "RepaymentsOfLongTermCapitalLeaseObligations"}
SNAP_NAME = {"amazon": "amazon", "microsoft": "microsoft", "alphabet": "alphabet", "google": "google", "meta": "meta",
             "oracle": "oracle"}
CF_TAG = re.compile(r"Payments|Repayments|Proceeds|Productive|PropertyPlant|Lease|Capital|Financing", re.I)
NUM = re.compile(r"(?<![\d.])(\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![\d,])")


def rows_of(section_text):
    """Rows of one statement: (label, raw line, [(number, printed_in_parentheses), ...])."""
    rows = []
    for ln in section_text.split("\n"):
        cells = [c.strip() for c in ln.split("|")]
        label = cells[0]
        if not re.search(r"[A-Za-z]{3}", label):
            continue
        nums = []
        for c in cells[1:]:
            if re.fullmatch(r"\$?\s*[—–-]+\s*", c):
                nums.append((0, False))  # a dash is a printed zero and keeps the columns aligned
                continue
            for n in NUM.findall(c):
                nums.append((int(n.replace(",", "")), "(" in c))
        rows.append((label, ln, nums))
    return rows


def role_of(label):
    lab = re.sub(r"\s+", " ", label.lower().replace("’", "'")).strip(" :")
    lab = re.sub(r"\(\d\)|\(\w\)$", "", lab).strip()
    for role, rx, cat in ROLES:
        if re.search(rx, lab):
            return role, cat
    return None, None


ELSEWHERE_KEY = re.compile(r"property and equipment|capital expenditure|finance lease|fixed assets", re.I)


def printed_elsewhere(full_text, value_millions):
    """True if the number (thousands separators) is printed on a line about PP&E / capex / finance leases."""
    s = f"{value_millions:,}"
    for ln in full_text.split("\n"):
        if s in ln and ELSEWHERE_KEY.search(ln) and re.search(r"(?<![\d,.])" + re.escape(s) + r"(?![\d,])", ln):
            return True
    return False


def facts_by_accn(cf):
    out = {}
    for ns, tags in cf["facts"].items():
        for tag, v in tags.items():
            for unit, vals in v["units"].items():
                if unit != "USD":
                    continue
                for x in vals:
                    if "start" not in x:
                        continue
                    out.setdefault(x["accn"], []).append(dict(x, tag=tag, ns=ns))
    return out


def sections_of(path):
    if not os.path.exists(path):
        return []
    return [p for p in re.split(r"\n### section at text line \d+\n", open(path).read())[1:]]


def scale_of(section):
    head = section[:600].lower()
    return 1e3 if "in thousands" in head else 1e6


def main():
    snap, cfdir, index_csv, out_csv, cache = sys.argv[1:6]
    index = {(r["company"], r["accession"]): r for r in csv.DictReader(open(index_csv))}
    out = []
    for cid in SNAP_NAME:
        facts = facts_by_accn(json.load(open(os.path.join(snap, f"companyfacts_{cid}.json"))))
        for (c, acc), meta in sorted(index.items()):
            if c != cid:
                continue
            fs = [f for f in facts.get(acc, []) if f["tag"] in TAGS_TO_CHECK or CF_TAG.search(f["tag"])]
            base = {"company_id": cid, "accession": acc, "form": meta["form"], "filed": meta["filed"],
                    "report_period": meta["period"], "doc_url": meta["url"], "doc_sha256": meta["sha256"]}
            emitted = {}
            secs = sections_of(os.path.join(cfdir, cid, f"{acc}.txt"))
            for sec in secs:
                scale = scale_of(sec)
                rows = [(role_of(lb), lb, ln, nums) for lb, ln, nums in rows_of(sec)]
                rows = [(r[0], r[1], lb, ln, nums) for r, lb, ln, nums in rows if r[0]]

                def matches(val, prefer_ppe):
                    m = [f for f in fs if abs(f["val"]) == val * scale]
                    if prefer_ppe:
                        m = sorted(m, key=lambda f: 0 if "PropertyPlant" in f["tag"] or "ProductiveAssets" in f["tag"] else 1)
                    return m

                ref = next((r for r in rows if r[0] == "ppe_purchases"), None)
                colmap = []
                if ref:
                    for val, _ in ref[4]:
                        m = matches(val, True)
                        colmap.append((m[0]["start"], m[0]["end"]) if m else None)
                for role, cat, label, line, nums in rows:
                    aligned = ref is not None and len(nums) == len(colmap)
                    for i, (val, paren) in enumerate(nums):
                        if val == 0 and not aligned:
                            continue
                        own = matches(val, role == "ppe_purchases") if val else []
                        period = colmap[i] if aligned and colmap[i] else ((own[0]["start"], own[0]["end"]) if own else None)
                        if period is None:
                            continue
                        tagged = [f for f in own if (f["start"], f["end"]) == period]
                        key = (role, period[0], period[1], val)
                        if key in emitted:
                            continue
                        d0, d1 = dt.date.fromisoformat(period[0]), dt.date.fromisoformat(period[1])
                        rec = dict(base, xbrl_tag=(f"{tagged[0]['ns']}:{tagged[0]['tag']}" if tagged else ""),
                                   xbrl_fy=(tagged[0].get("fy") if tagged else ""), xbrl_fp=(tagged[0].get("fp") if tagged else ""),
                                   period_start=period[0], period_end=period[1], days=(d1 - d0).days + 1,
                                   value_usd=int(val * scale), printed_negative=paren, line_role=role, metric_category=cat,
                                   printed_label=label, printed_row=line[:400],
                                   printed_units="thousands" if scale == 1e3 else "millions",
                                   period_from="xbrl_fact" if tagged else "column_of_purchases_row",
                                   text_check="PASS" if tagged else "PASS_PRINTED_UNTAGGED")
                        emitted[key] = rec
                        for f in tagged:
                            f["_used"] = True
            out.extend(emitted.values())
            for f in facts.get(acc, []):
                if f["tag"] not in TAGS_TO_CHECK or f.get("_used"):
                    continue
                d0, d1 = dt.date.fromisoformat(f["start"]), dt.date.fromisoformat(f["end"])
                status = "FAIL" if secs else "FAIL_NO_CF_SECTION"
                tpath = os.path.join(cache, f"{cid}_{acc}.txt.gz")
                v = abs(f["val"]) / 1e6
                if os.path.exists(tpath) and v == int(v) and printed_elsewhere(gzip.open(tpath, "rt").read(), int(v)):
                    status = "NOT_IN_CF_STATEMENT_PRINTED_ELSEWHERE"
                f["_used"] = True
                out.append(dict(base, xbrl_tag=f"{f['ns']}:{f['tag']}", xbrl_fy=f.get("fy"), xbrl_fp=f.get("fp"),
                                period_start=f["start"], period_end=f["end"], days=(d1 - d0).days + 1,
                                value_usd=f["val"], printed_negative="", line_role="", metric_category="",
                                printed_label="", printed_row="", printed_units="", period_from="xbrl_fact",
                                text_check=status))
    fields = list(out[0].keys())
    with open(out_csv, "w", newline="") as g:
        w = csv.DictWriter(g, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} rows; PASS {sum(r['text_check'] == 'PASS' for r in out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
