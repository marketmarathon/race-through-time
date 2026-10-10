#!/usr/bin/env python3
"""RTT-103 (IQ-16): snapshot SEC EDGAR filing indexes and XBRL company facts.

For each company: data.sec.gov submissions JSON (plus its older "files" pages) and XBRL companyfacts JSON, saved
byte-for-byte under <out_dir>/ with a SHA-256 manifest. SEC fair-access policy: a declared User-Agent with a contact
address and no more than 10 requests per second (this script makes at most about 4).

Usage: rtt103_fetch_sec.py <out_dir>
"""
import hashlib
import json
import os
import sys
import time
import urllib.request

UA = "Race Through Time research luke@marketmarathon.com"
COMPANIES = {  # company_id: (CIK, name as filed today)
    "amazon": ("0001018724", "Amazon.com, Inc."),
    "microsoft": ("0000789019", "Microsoft Corporation"),
    "alphabet": ("0001652044", "Alphabet Inc."),
    "google": ("0001288776", "Google Inc. (Alphabet's predecessor registrant, now Google LLC)"),
    "meta": ("0001326801", "Meta Platforms, Inc. (formerly Facebook, Inc.)"),
    "oracle": ("0001341439", "Oracle Corporation"),
    "baidu": ("0001329099", "Baidu, Inc."),
    "alibaba": ("0001577552", "Alibaba Group Holding Limited"),
    "coreweave": ("0001769628", "CoreWeave, Inc."),
}


def get(url):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
            time.sleep(0.25)
            return body
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 ** (i + 1))
        except Exception:
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"failed: {url}")


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    manifest = []

    def save(name, url, body):
        open(os.path.join(out, name), "wb").write(body)
        manifest.append({"file": name, "url": url, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                         "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        print(f"{name} {len(body)} bytes")

    for cid, (cik, _) in COMPANIES.items():
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        body = get(url)
        save(f"submissions_{cid}.json", url, body)
        for f in json.loads(body).get("filings", {}).get("files", []):
            u = f"https://data.sec.gov/submissions/{f['name']}"
            save(f"submissions_{cid}_{f['name']}", u, get(u))
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        body = get(url)
        if body is None:
            manifest.append({"file": None, "url": url, "note": "HTTP 404: no XBRL company facts"})
            print(f"{cid}: no company facts")
        else:
            save(f"companyfacts_{cid}.json", url, body)
    json.dump({"made_by": "scripts/rtt103_fetch_sec.py", "user_agent": UA, "companies": COMPANIES,
               "files": manifest}, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
