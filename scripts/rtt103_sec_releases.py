#!/usr/bin/env python3
"""RTT-103 (IQ-16): earnings releases furnished to the SEC (8-K item 2.02, exhibit 99.x) for the US companies.

For each 8-K whose items include 2.02 (Results of Operations), filed from 1 Apr 2009, the filing index is read and every
EX-99 exhibit document fetched. Raw documents are cached (gzip) in <cache_dir>; an index CSV records URL, SHA-256 and
bytes. These releases are used for: each company's own definition of "capital expenditures" (Series A), capex guidance
(file F) and management statements on AI / cloud infrastructure (file G).

Usage: rtt103_sec_releases.py <snapshot_dir> <cache_dir> <index_csv> [company ...]
"""
import csv
import glob
import gzip
import hashlib
import json
import os
import re
import sys
import time
import urllib.request

UA = "Race Through Time research luke@marketmarathon.com"
CIKS = {"amazon": "1018724", "microsoft": "789019", "alphabet": "1652044", "google": "1288776", "meta": "1326801",
        "oracle": "1341439", "coreweave": "1769628"}


def get(url):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
            time.sleep(0.15)
            return body
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 ** (i + 1))
        except Exception:
            time.sleep(2 ** (i + 1))
    raise RuntimeError(url)


def main():
    snap, cache, index_csv = sys.argv[1:4]
    comps = sys.argv[4:] or list(CIKS)
    os.makedirs(cache, exist_ok=True)
    rows = []
    if os.path.exists(index_csv):
        rows = list(csv.DictReader(open(index_csv)))
    done = {(r["company"], r["accession"]) for r in rows}
    for cid in comps:
        cik = CIKS[cid]
        fl = []
        for f in sorted(glob.glob(os.path.join(snap, f"submissions_{cid}*.json"))):
            d = json.load(open(f))
            r = d["filings"]["recent"] if "filings" in d else d
            for k in range(len(r["accessionNumber"])):
                if r["form"][k] == "8-K" and "2.02" in (r["items"][k] or "") and r["filingDate"][k] >= "2009-04-01":
                    fl.append((r["accessionNumber"][k], r["filingDate"][k], r["reportDate"][k]))
        for acc, filed, rep in sorted(fl):
            if (cid, acc) in done:
                continue
            base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/"
            idx = get(base + "index.json")
            if idx is None:
                continue
            items = json.loads(idx)["directory"]["item"]
            exhibits = [it["name"] for it in items if re.search(r"(ex-?99|ex99|exhibit99|dex99)", it["name"], re.I)
                        and it["name"].lower().endswith((".htm", ".html", ".txt"))]
            for name in exhibits:
                raw = get(base + name)
                if raw is None:
                    continue
                cpath = os.path.join(cache, f"{cid}_{acc}_{name}.gz")
                with gzip.open(cpath, "wb") as g:
                    g.write(raw)
                rows.append({"company": cid, "accession": acc, "filed": filed, "report_date": rep, "document": name,
                             "url": base + name, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
                print(cid, filed, acc, name, len(raw), flush=True)
            with open(index_csv, "w", newline="") as g:
                w = csv.DictWriter(g, fieldnames=["company", "accession", "filed", "report_date", "document", "url",
                                                  "sha256", "bytes"])
                w.writeheader()
                w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
