#!/usr/bin/env python3
"""RTT-103 (IQ-16): fetch the www.sec.gov documents cited in the private research catalogues (Section A files).

The catalogues stay in the private repo (DEC-006); this script reads them there and caches each sec.gov document
(raw, gzip) in <cache_dir>, writing an index CSV (source_ids, URL, SHA-256, bytes). SEC fair access: declared
User-Agent, well under 10 requests per second.

Usage: rtt103_fetch_catalogue_sec.py <private_rtt103_dir> <cache_dir> <index_csv>
"""
import csv
import gzip
import hashlib
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rtt103_fetch_sources import INPUTS, catalogue_rows  # noqa: E402

UA = "Race Through Time research luke@marketmarathon.com"


def main():
    src, cache, index_csv = sys.argv[1:4]
    os.makedirs(cache, exist_ok=True)
    urls = {}
    for name in INPUTS:
        for row in catalogue_rows(os.path.join(src, name)):
            for u in re.findall(r"https?://[^\s;\"]+", row.get("url", "")):
                if urllib.parse.urlparse(u).hostname == "www.sec.gov":
                    urls.setdefault(u, []).append(row["source_id"])
    out = []
    for u, sids in sorted(urls.items(), key=lambda kv: kv[1][0]):
        path = os.path.join(cache, re.sub(r"[^A-Za-z0-9_.-]", "_", sids[0]) + ".raw.gz")
        rec = {"source_ids": ";".join(sids), "url": u}
        if not os.path.exists(path):
            body = None
            for i in range(3):
                try:
                    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=120) as r:
                        body = r.read()
                    break
                except urllib.error.HTTPError as e:
                    rec["error"] = f"HTTP {e.code}"
                    if e.code == 404:
                        break
                    time.sleep(3 * (i + 1))
                except Exception as e:
                    rec["error"] = type(e).__name__
                    time.sleep(3 * (i + 1))
            time.sleep(0.2)
            if body is None:
                out.append(rec)
                print(sids[0], "FAILED", rec.get("error"), flush=True)
                continue
            with gzip.open(path, "wb") as g:
                g.write(body)
        body = gzip.open(path, "rb").read()
        rec.update({"error": "", "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                    "cache_file": os.path.basename(path)})
        out.append(rec)
        print(sids[0], len(body), flush=True)
    with open(index_csv, "w", newline="") as g:
        w = csv.DictWriter(g, fieldnames=["source_ids", "url", "error", "sha256", "bytes", "cache_file"])
        w.writeheader()
        w.writerows(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
