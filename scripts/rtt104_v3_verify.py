#!/usr/bin/env python3
"""RTT-104 V3 Part 1 (IQ-24c): check the to-check list's claimed dates against the pages our runner fetched, in code,
and match the VERIFIED events to the visible changes.

  python3 -I scripts/rtt104_v3_verify.py <to-check list CSV, kept OFF the repo> <runner fetch dir>

The to-check list (Cowork, from ChatGPT; DEC-006) is read only to learn which date to look for on which page. Nothing
from it is written to the repo except, for rows that fail, the country, kind and claimed date with the failure reason
(the validation result). A row is VERIFIED only when a date parsed from the fetched page's excerpt lines equals the
claimed date (every day of a claimed range's two ends), and, for a non-election event, a word naming that kind of
event stands in the same excerpt line.

Writes: data/rtt-104/v3_verified_events.csv (VERIFIED rows: country, kind, date, URL, our runner's excerpt),
data/rtt-104/source/v3_causes.csv (one row per visible change: cause, window, borderline, evidence),
data/rtt-104/source/v3_verify_results.json (counts and every failed row with its reason).
"""
import csv
import datetime as dt
import hashlib
import json
import os
import re
import sys

MON = {}
for i, names in enumerate([
        "jan january janvier janeiro januar enero", "feb february fevrier février fevereiro februar febrero",
        "mar march mars março marco märz marz marzo", "apr april avril abril", "may mai maio mayo",
        "jun june juin junho juni junio", "jul july juillet julho juli julio", "aug august août aout agosto",
        "sep sept september septembre setembro septiembre", "oct october octobre outubro oktober octubre",
        "nov november novembre novembro noviembre", "dec december décembre decembre dezembro dezember diciembre"], 1):
    for n in names.split():
        MON[n] = i
JOIN = {"and", "to", "y", "e", "et", "und", "bis", "de", "al", "au", "a", "&", "st", "nd", "rd", "th", "of", "from"}
TOK = re.compile(r"\d{4}|\d{1,2}|[^\W\d_]+", re.U)
ELECTION_KINDS = {"general election", "partial renewal"}
KIND_WORDS = {
    "dissolved or suspended": r"dissol|suspen|coup|seiz|takeover|military|interim|transition",
    "quota or seat law": r"quota|reserved|parity|parit|paridad|women|seats|law|act|amend",
    "appointed seats": r"appoint|nominat|designat",
    "newly formed": r"constituent|transitional|new|first|establish|formed|inaugurat|install",
    "other": r"law|reform|amend|seat|quota|appoint|dissol|suspen|vacan|replac|constitution|transition|resign",
}
NON_PRIMARY = ("wikipedia.org",)


def parse_dates(text):
    """Every calendar date written in the text, as ISO strings (day-month-year in several languages, month-day-year,
    day lists and ranges before one month, ISO and dd/mm/yyyy)."""
    out = set()
    for y, m, d in re.findall(r"\b((?:19|20)\d\d)-(\d\d)-(\d\d)\b", text):
        out.add(f"{y}-{m}-{d}")
    for d, m, y in re.findall(r"\b(\d{1,2})[./](\d{1,2})[./]((?:19|20)\d\d)\b", text):
        if 1 <= int(m) <= 12 and 1 <= int(d) <= 31:
            out.add(f"{y}-{int(m):02d}-{int(d):02d}")
    toks = [t.lower() for t in TOK.findall(text)]
    for k, t in enumerate(toks):
        m = MON.get(t.rstrip("."))
        if not m:
            continue
        days, j = [], k - 1
        while j >= 0 and len(days) < 4 and (toks[j] in JOIN or (len(toks[j]) <= 2 and toks[j].isdigit())):
            if toks[j].isdigit():
                days.append(int(toks[j]))
            j -= 1
        year, j = None, k + 1
        after = []
        while j < len(toks) and j <= k + 8:
            if len(toks[j]) == 4 and toks[j].isdigit():
                year = toks[j]
                break
            if toks[j].isdigit():
                after.append(int(toks[j]))
            elif toks[j] not in JOIN and toks[j] not in MON:
                break
            j += 1
        if not year:
            continue
        if not days:  # month-day-year
            days = after[:3]
        for d in days:
            try:
                out.add(dt.date(int(year), m, d).isoformat())
            except ValueError:
                pass
    return out


def load_fetch(fetch_dir):
    man = json.load(open(os.path.join(fetch_dir, "fetch_manifest.json"), encoding="utf-8"))
    pages = {}
    for p in man["pages"]:
        rec = dict(p, dated=[], kinds=[])
        if p.get("excerpt_file"):
            for ln in open(os.path.join(fetch_dir, p["excerpt_file"]), encoding="utf-8"):
                if ln.startswith("D: "):
                    rec["dated"].append(ln[3:].rstrip("\n"))
                elif ln.startswith("K: "):
                    rec["kinds"].append(ln[3:].rstrip("\n"))
        pages[p["url"]] = rec
    return man, pages


def check(row, page):
    """-> (status, reason, page_dates_shown, excerpt, page_type)"""
    kind, claim = row["event_type"], row["claimed_date"].strip()
    if not re.match(r"\d{4}-\d\d-\d\d", claim):
        return "NOT FOUND", "no date in the to-check list", "", "", ""
    if page is None:
        return "UNVERIFIED", "URL not fetched", "", "", ""
    if not page.get("status"):
        return "UNVERIFIED", f"page did not open ({page.get('error', '')})", "", "", ""
    want = re.findall(r"\d{4}-\d\d-\d\d", claim)
    m = re.search(r"E(\d{8})/?$", page["url"])
    fm = re.search(r"E(\d{8})/?$", page.get("final_url") or "")
    if m and (not fm or fm.group(1) != m.group(1)):
        return "UNVERIFIED", "page redirected to another page", "", "", ""
    hits = {w: [ln for ln in page["dated"] if w in parse_dates(ln)] for w in want}
    ptype = next((re.sub(r"\s*\|.*", "", ln) for ln in page["kinds"]
                  if re.match(r"(?i)(full|partial) renewal\b", ln)), "")
    if not ptype:
        ptype = next((ln[:120] for ln in page["kinds"] if re.match(r"(?i)purpose of", ln)), "")
    if all(hits.values()):
        ex = " … ".join(dict.fromkeys(h[0] for h in hits.values()))[:400]
        if any(d in page["url"] for d in NON_PRIMARY):
            return "UNVERIFIED", "date shown, but on Wikipedia (not a primary source)", "", ex, ptype
        if kind not in ELECTION_KINDS and not re.search(KIND_WORDS.get(kind, KIND_WORDS["other"]), ex, re.I):
            return "UNVERIFIED", "date shown, but no word naming the event beside it", "", ex, ptype
        return "VERIFIED", "", "", ex, ptype
    yrs = {w[:4] for w in want}
    shown = sorted({d for ln in page["dated"] for d in parse_dates(ln) if d[:4] in yrs})
    if any(hits.values()):
        return "UNVERIFIED", "date partly found (one end of the claimed range)", "; ".join(shown[:6]), "", ptype
    if shown:
        ex = next((ln for ln in page["dated"] if parse_dates(ln) & set(shown)), "")[:300]
        return "UNVERIFIED", "date differs (page shows another date that year)", "; ".join(shown[:6]), ex, ptype
    return "UNVERIFIED", "date not found on the page", "", "", ptype


def window(y1):
    if y1 == 1998:
        return dt.date(1997, 1, 2), dt.date(1998, 8, 10)
    if y1 == 1999:
        return dt.date(1998, 8, 11), dt.date(1999, 12, 31)
    return dt.date(y1, 1, 1), dt.date(y1, 12, 31)


def main(tocheck, fetch_dir, data_dir="data/rtt-104"):
    man, pages = load_fetch(fetch_dir)
    rows = list(csv.DictReader(open(tocheck, encoding="utf-8-sig")))
    res = []
    for r in rows:
        st, why, shown, ex, ptype = check(r, pages.get(r["claimed_url"].strip()))
        res.append(dict(r, status=st, reason=why, page_dates=shown, excerpt=ex, page_type=ptype,
                        fetch_id=(pages.get(r["claimed_url"].strip()) or {}).get("id", "")))
    ver = [x for x in res if x["status"] == "VERIFIED"]
    with open(os.path.join(data_dir, "v3_verified_events.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["country", "chamber", "kind", "date", "type_on_page", "source_url", "fetch_id", "excerpt", "status"])
        for x in sorted(ver, key=lambda x: (x["country"], x["claimed_date"])):
            w.writerow([x["country"], x["chamber"], x["event_type"], x["claimed_date"], x["page_type"],
                        x["claimed_url"].strip(), x["fetch_id"], x["excerpt"], "VERIFIED"])
    by_c = {}
    for x in res:
        if re.match(r"\d{4}", x["claimed_date"]):
            end = dt.date.fromisoformat(re.findall(r"\d{4}-\d\d-\d\d", x["claimed_date"])[-1])
            by_c.setdefault(x["country"], []).append((end, x))
    changes = list(csv.DictReader(open(os.path.join(data_dir, "v3_change_events.csv"), encoding="utf-8")))
    causes = []
    for c in changes:
        if c["visible"] != "y":
            continue
        y1 = int(c["to_year"])
        a, b = window(y1)
        inside = [(d, x) for d, x in by_c.get(c["country"], []) if a <= d <= b]
        near = [(d, x) for d, x in by_c.get(c["country"], []) if not a <= d <= b
                and (abs((d - a).days) <= 61 or abs((d - b).days) <= 61)]
        el = [(d, x) for d, x in inside if x["status"] == "VERIFIED" and x["event_type"] in ELECTION_KINDS]
        ot = [(d, x) for d, x in inside if x["status"] == "VERIFIED" and x["event_type"] not in ELECTION_KINDS]
        pick = el or ot
        notes = []
        border = [f"{d} {x['event_type']} within 2 months of the window edge" for d, x in (el + ot)
                  if (d - a).days <= 61 or (b - d).days <= 61]
        border += [f"{d} {x['event_type']} just outside the window ({x['status']})" for d, x in near]
        unv = [f"{d} {x['event_type']} in the window but {x['status']}: {x['reason']}" for d, x in inside
               if x["status"] != "VERIFIED"]
        notes += unv
        if pick:
            cause = "election" if el else "other"
            ev = pick
        else:
            cause, ev = "unexplained", []
        causes.append({"iso3": c["iso3"], "to_year": c["to_year"], "cause": cause,
                       "election_date": "; ".join(x["claimed_date"] for _, x in ev),
                       "election_type": "; ".join((x["event_type"] + (f" (page: {x['page_type']})" if x["page_type"] else ""))
                                                  for _, x in ev),
                       "window": f"{a}..{b}" + (" (WDI 1998 = 10 Aug 1998)" if y1 in (1998, 1999) else " (calendar year, DEC-665)"),
                       "borderline": "; ".join(border), "source_url": "; ".join(x["claimed_url"].strip() for _, x in ev),
                       "excerpt": " || ".join(x["excerpt"] for _, x in ev)[:600],
                       "status": "VERIFIED" if ev else "NOT FOUND", "note": "; ".join(notes)})
    with open(os.path.join(data_dir, "source", "v3_causes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, list(causes[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(causes)
    fails = [{"country": x["country"], "kind": x["event_type"], "claimed_date": x["claimed_date"], "reason": x["reason"],
              "page_dates": x["page_dates"], "url": x["claimed_url"].strip()} for x in res if x["status"] != "VERIFIED"]
    out = {"to_check_list_sha256": hashlib.sha256(open(tocheck, "rb").read()).hexdigest(), "rows": len(res),
           "verified": len(ver), "fetch": man.get("summary", ""), "run_url": man.get("run_url", ""), "failed": fails}
    json.dump(out, open(os.path.join(data_dir, "source", "v3_verify_results.json"), "w", encoding="utf-8"), indent=1)
    print(f"rows {len(res)}; VERIFIED {len(ver)}; fetch: {out['fetch']}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
