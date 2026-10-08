#!/usr/bin/env python3
"""RTT-103 (IQ-16): download each 10-Q / 10-K primary document and keep its cash-flow statement as text.

Inputs: the SEC snapshot made by rtt103_fetch_sec.py (submissions JSON). For every 10-Q, 10-K, 10-KT and amendment
filed from 1 Apr 2009 by the listed companies, the primary document is fetched from www.sec.gov, its SHA-256 recorded,
converted to plain text (one table row per line, cells separated by " | ") and the cash-flow statement section(s)
kept under <cf_dir>/<company>/<accession>.txt. The raw document and its text are cached (gzip) in <cache_dir> for later checks.
A CSV index of every document (URL, SHA-256, bytes, where the cash-flow statement was found) is written to <index_csv>.

Usage: rtt103_sec_docs.py <snapshot_dir> <cache_dir> <cf_dir> <index_csv> [company ...]
"""
import csv
import glob
import gzip
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.request

UA = "Race Through Time research luke@marketmarathon.com"
FORMS = {"10-Q", "10-K", "10-KT", "10-Q/A", "10-K/A", "20-F", "20-F/A"}
COMPANY_CIKS = {"amazon": "1018724", "microsoft": "789019", "alphabet": "1652044", "google": "1288776",
                "meta": "1326801", "oracle": "1341439", "coreweave": "1769628"}
CF_HEAD = re.compile(r"(STATEMENTS?OF(CONSOLIDATED)?CASHFLOWS?|CASHFLOWS?STATEMENTS?)", re.I)  # matched with spaces removed


def get(url):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
            time.sleep(0.15)
            return body
        except Exception:
            time.sleep(2 ** (i + 1))
    raise RuntimeError(url)


def to_text(raw):
    t = raw.decode("utf-8", errors="replace")
    t = re.sub(r"\s+", " ", t)  # line breaks in the HTML source are not line breaks in the document
    t = re.sub(r"(?is)<(script|style|ix:header)[^>]*>.*?</\1>", " ", t)
    # inside a table row, paragraph and line-break tags must not split the row into several lines
    t = re.sub(r"(?is)<tr\b.*?</tr\s*>", lambda m: re.sub(r"(?i)<(/p|/div|br)\b[^>]*>", " ", m.group(0)), t)
    t = re.sub(r"(?i)</t[dh]\s*>", " | ", t)
    t = re.sub(r"(?i)<(/tr|br|/p|/div|/h\d|/li)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("\xa0", " ").replace("​", "")
    lines = []
    for ln in t.split("\n"):
        ln = re.sub(r"[ \t]+", " ", ln)
        ln = re.sub(r"(\|\s*)+\|", "|", ln).strip(" |")
        if ln:
            lines.append(ln)
    return "\n".join(lines)


def cf_sections(text):
    """Every block that starts at a cash-flow heading and holds numbers (skips table-of-contents mentions)."""
    lines = text.split("\n")
    out = []
    for i, ln in enumerate(lines):
        if CF_HEAD.search(re.sub(r"\s", "", ln)) and len(ln) < 200:
            block = lines[i:i + 320]
            seen_inv = False
            for j, b in enumerate(block):
                seen_inv = seen_inv or bool(re.search(r"investing", b, re.I))
                if seen_inv and j > 20 and re.search(r"accompanying notes", b, re.I):
                    block = block[:j + 1]
                    break
            nums = sum(1 for b in block if re.search(r"\d{1,3},\d{3}", b))
            if nums >= 8 and any(re.search(r"^investing|investing activities", b, re.I) for b in block):
                out.append((i, "\n".join(block)))
    return out


def filings(snapshot, cid):
    rows = []
    for f in sorted(glob.glob(os.path.join(snapshot, f"submissions_{cid}*.json"))):
        d = json.load(open(f))
        r = d["filings"]["recent"] if "filings" in d else d
        for k in range(len(r["accessionNumber"])):
            rows.append({key: r[key][k] for key in ("accessionNumber", "form", "filingDate", "reportDate", "primaryDocument")})
    return [x for x in rows if x["form"] in FORMS and x["filingDate"] >= "2009-04-01"]


def main():
    snapshot, cache, cfdir, index_csv = sys.argv[1:5]
    comps = sys.argv[5:] or list(COMPANY_CIKS)
    os.makedirs(cache, exist_ok=True)
    old = {}
    if os.path.exists(index_csv):
        old = {(r["company"], r["accession"]): r for r in csv.DictReader(open(index_csv))}
    out = dict(old)
    for cid in comps:
        cik = COMPANY_CIKS[cid]
        os.makedirs(os.path.join(cfdir, cid), exist_ok=True)
        for fl in filings(snapshot, cid):
            acc = fl["accessionNumber"]
            if (cid, acc) in old and old[(cid, acc)]["cf_found"] != "":
                continue
            url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{fl['primaryDocument']}"
            cpath = os.path.join(cache, f"{cid}_{acc}.raw.gz")
            if os.path.exists(cpath):
                raw = gzip.open(cpath, "rb").read()
            else:
                raw = get(url)
                with gzip.open(cpath, "wb") as g:
                    g.write(raw)
            sha, size = hashlib.sha256(raw).hexdigest(), str(len(raw))
            text = to_text(raw)
            with gzip.open(os.path.join(cache, f"{cid}_{acc}.txt.gz"), "wt") as g:
                g.write(text)
            secs = cf_sections(text)
            if secs:
                with open(os.path.join(cfdir, cid, f"{acc}.txt"), "w") as g:
                    g.write(f"# {cid} {fl['form']} accession {acc} filed {fl['filingDate']} period {fl['reportDate']}\n"
                            f"# {url}\n# document SHA-256 {sha}, {size} bytes; cash-flow section(s) as plain text\n")
                    for i, s in secs:
                        g.write(f"\n### section at text line {i}\n{s}\n")
            out[(cid, acc)] = {"company": cid, "accession": acc, "form": fl["form"], "filed": fl["filingDate"],
                               "period": fl["reportDate"], "url": url, "sha256": sha, "bytes": size,
                               "cf_found": "yes" if secs else "no", "cf_sections": len(secs)}
            print(cid, fl["form"], fl["reportDate"], acc, "cf" if secs else "NO CF", flush=True)
    with open(index_csv, "w", newline="") as g:
        w = csv.DictWriter(g, fieldnames=["company", "accession", "form", "filed", "period", "url", "sha256", "bytes",
                                          "cf_found", "cf_sections"])
        w.writeheader()
        for k in sorted(out):
            w.writerow(out[k])
    return 0


if __name__ == "__main__":
    sys.exit(main())
