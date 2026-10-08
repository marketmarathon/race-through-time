#!/usr/bin/env python3
"""RTT-103 (IQ-16): figures and statements from the US companies' earnings releases (8-K exhibit 99, on sec.gov).

Outputs (public: SEC-furnished company text, short verbatim quotes only):
  <out_dir>/meta_release_capex.csv   Meta's own quarterly "Capital expenditures" figure from every release (Series A),
                                     with the definition wording and a verbatim quote.
  <out_dir>/release_statements.csv   Candidate sentences for files F (capex guidance) and G (AI / cloud / data-centre
                                     capex statements) from every US release: company, date, URL, SHA-256, sentence.
                                     Curated by hand into F and G; nothing here is used as a capex figure.

Quarter of a release = the latest fiscal quarter end before its filing date (checked against the quarter named in the
sentence where there is one).

Usage: rtt103_release_extract.py <releases_index_csv> <release_cache_dir> <out_dir>
"""
import csv
import datetime as dt
import gzip
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rtt103_sec_docs import to_text  # noqa: E402

FYE_MONTH = {"amazon": 12, "google": 12, "alphabet": 12, "meta": 12, "microsoft": 6, "oracle": 5, "coreweave": 12}
ORDINAL = {"first": 1, "second": 2, "third": 3, "fourth": 4}


def quarter_ends(year_from=2008, year_to=2027):
    out = []
    for y in range(year_from, year_to + 1):
        for m in (2, 3, 5, 6, 8, 9, 11, 12):
            last = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1))
            out.append(last)
    return sorted(out)


def last_quarter_end(company, filed):
    f = dt.date.fromisoformat(filed)
    fye = FYE_MONTH[company]
    months = sorted({(fye - 1 - 3 * k) % 12 + 1 for k in range(4)})
    cands = [d for d in quarter_ends() if d.month in months and d < f]
    return cands[-1].isoformat()


def amount(txt):
    m = re.match(r"\$\s*([\d,.]+)\s*(billion|million)", txt)
    if not m:
        return None, None
    v = float(m.group(1).replace(",", ""))
    if m.group(2) == "billion":
        decimals = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
        return round(v * 1e9), f"USD billions, {decimals} d.p."
    return round(v * 1e6), "USD millions"


GUIDE = re.compile(r"(capital expenditures|capex).{0,160}(range of|expect|anticipate|outlook)|"
                   r"(expect|anticipate|outlook).{0,160}(capital expenditures|capex)", re.I)
STORY = re.compile(r"(capital expenditures|capex|data cent|servers|infrastructure|capacity).{0,200}"
                   r"(\bAI\b|artificial intelligence|generative|machine learning|cloud|compute|superintelligence|GPU)|"
                   r"(\bAI\b|artificial intelligence|generative|cloud|compute|superintelligence).{0,200}"
                   r"(capital expenditures|capex|data cent|servers|infrastructure investment)", re.I)


def main():
    index_csv, cache, out_dir = sys.argv[1:4]
    os.makedirs(out_dir, exist_ok=True)
    rel = sorted(csv.DictReader(open(index_csv)), key=lambda r: (r["company"], r["filed"]))
    meta_rows, stmts = [], []
    for r in rel:
        text = to_text(gzip.open(os.path.join(cache, f"{r['company']}_{r['accession']}_{r['document']}.gz")).read())
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z\"“•])|\n", text)
        q_end = last_quarter_end(r["company"], r["filed"])
        if r["company"] == "meta":
            for s in sentences:
                m = re.search(r"(?:Capital expenditures|Purchases of property and equipment)\s*(,\s*including principal payments on finance leases\s*,)?\s*"
                              r"(for the (?:(\w+) )?quarter(?: of (\d{4}))?\s*)?were\s*(\$\s*[\d,.]+\s*(?:billion|million))", s)
                if not m:
                    continue
                val, prec = amount(m.group(5))
                named = ""
                if m.group(3) and m.group(4):
                    named = f"{m.group(4)} Q{ORDINAL.get(m.group(3).lower(), '?')}"
                qm = re.search(r"for the (\w+) quarter( and full year)? (of )?(\d{4})", s)
                if qm and not named:
                    named = f"{qm.group(4)} Q{ORDINAL.get(qm.group(1).lower(), '?')}"
                meta_rows.append({"company_id": "meta", "release_filed": r["filed"], "accession": r["accession"],
                                  "url": r["url"], "doc_sha256": r["sha256"], "quarter_end": q_end,
                                  "quarter_named_in_text": named,
                                  "includes_finance_lease_principal": "yes" if m.group(1) else "no",
                                  "value_usd": val, "precision": prec,
                                  "quote": re.sub(r"\s+", " ", s.strip(" •|"))[:300]})
                break
        for s in sentences:
            s2 = re.sub(r"\s+", " ", s.strip(" •|"))
            if len(s2) < 40 or len(s2) > 700:
                continue
            kind = []
            if GUIDE.search(s2):
                kind.append("guidance_candidate")
            if STORY.search(s2):
                kind.append("story_candidate")
            if kind:
                stmts.append({"company_id": r["company"], "release_filed": r["filed"], "accession": r["accession"],
                              "url": r["url"], "doc_sha256": r["sha256"], "kind": ";".join(kind), "sentence": s2})
    for name, rows in (("meta_release_capex.csv", meta_rows), ("release_statements.csv", stmts)):
        with open(os.path.join(out_dir, name), "w", newline="") as g:
            w = csv.DictWriter(g, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(name, len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
