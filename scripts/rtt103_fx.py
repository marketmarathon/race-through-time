#!/usr/bin/env python3
"""RTT-103 (IQ-16): Federal Reserve H.10 daily CNY per USD (noon buying rates in New York) to a CSV.

Input: the Board's historical page https://www.federalreserve.gov/releases/h10/hist/dat00_ch.htm as fetched on a
GitHub runner (FRED's DEXCHUS, the same series redistributed, timed out from the runner). "ND" (no data: holidays)
is kept as an empty rate, never filled.
Usage: rtt103_fx.py <h10_html> <out_csv> <page_url> <page_sha256>
"""
import csv
import datetime as dt
import html
import re
import sys

MON = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


def main():
    src, out, url, sha = sys.argv[1:5]
    t = html.unescape(re.sub(r"<[^>]+>", " ", open(src, encoding="utf-8", errors="replace").read()))
    rows = []
    for d, v in re.findall(r"(\d{1,2}-[A-Z]{3}-\d{2})\s+([\d.]+|ND)", t):
        dd, mm, yy = d.split("-")
        day = dt.date(2000 + int(yy), MON[mm], int(dd))
        rows.append({"date": day.isoformat(), "cny_per_usd": "" if v == "ND" else v,
                     "status": "ND (no data)" if v == "ND" else "rate"})
    rows.sort(key=lambda r: r["date"])
    with open(out, "w", newline="") as f:
        f.write(f"# Federal Reserve H.10, China (CNY per USD), noon buying rates in New York. Source {url} ; page SHA-256 {sha}\n")
        w = csv.DictWriter(f, fieldnames=["date", "cny_per_usd", "status"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(len(rows), rows[0], rows[-1], sum(1 for r in rows if not r["cny_per_usd"]), "ND days")
    return 0


if __name__ == "__main__":
    sys.exit(main())
