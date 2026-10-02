#!/usr/bin/env python3
"""RTT-003: transcribe Sony Interactive Entertainment's "Business Data & Sales" page
(https://sonyinteractive.com/en/our-company/business-data-sales/) into
data/rtt-003/source/sony_business_data.csv.

Rows:
  kind=lifetime   console, value_millions, qualifier ("more_than"), as_of (YYYY-MM-DD)
  kind=quarterly  console (PS4/PS5), fiscal year (April-March), quarter Q1..Q4, value_millions
                  (sell-in, "Including returned and refurbished products")

The saved HTML page is not committed (third-party page); its SHA-256 goes in the
.source.txt file next to the output. Standard library only.

Usage: python scripts/rtt003_extract_sony.py <saved-page.html> data/rtt-003/source
"""
import csv
import hashlib
import html
import os
import re
import sys
from datetime import datetime

URL = "https://sonyinteractive.com/en/our-company/business-data-sales/"
NAMES = {"PlayStation 5": "playstation_5", "PlayStation 4": "playstation_4", "PlayStation 3": "playstation_3",
         "PSP (PlayStation Portable)": "psp", "PlayStation 2": "playstation_2", "PlayStation": "playstation"}


def page_text(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)), hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main():
    page, outdir = sys.argv[1], sys.argv[2]
    text, sha = page_text(page)
    rows = []
    hw = text.split("Cumulative Worldwide Hardware Unit Sales (Sell-in)")[1].split("*Sales data on PlayStation Vita")[0]
    for m in re.finditer(r"(PlayStation 5|PlayStation 4|PlayStation 3|PSP \(PlayStation Portable\)|PlayStation 2|PlayStation)"
                         r" More than ([\d.]+) million \(As of ([A-Za-z]+ \d+, \d{4})\)", hw):
        as_of = datetime.strptime(m.group(3), "%B %d, %Y").strftime("%Y-%m-%d")
        rows.append({"kind": "lifetime", "console_id": NAMES[m.group(1)], "fiscal_year": "", "quarter": "",
                     "value_millions": m.group(2), "qualifier": "more_than", "as_of": as_of,
                     "basis": "sell-in"})
    for console, title in (("playstation_5", "Worldwide PlayStation 5 Hardware Unit Sales"),
                           ("playstation_4", "Worldwide PlayStation 4 Hardware Unit Sales")):
        block = text.split(title)[1].split("*Including returned and refurbished products")[0]
        if "Sell-in" not in block[:40]:
            raise SystemExit(f"{console}: table is not labelled sell-in")
        for m in re.finditer(r"FY(\d{4})((?: (?:[\d.]+|–)){1,5})", block):
            fy = int(m.group(1))
            vals = m.group(2).split()
            for q, v in zip(("Q1", "Q2", "Q3", "Q4", "FY"), vals):
                if v == "–":
                    continue
                rows.append({"kind": "quarterly" if q != "FY" else "fiscal_year", "console_id": console,
                             "fiscal_year": f"FY{fy}", "quarter": q, "value_millions": v, "qualifier": "exact",
                             "as_of": "", "basis": "sell-in incl. returned and refurbished"})
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "sony_business_data.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(outdir, "sony_business_data.source.txt"), "w", encoding="utf-8") as f:
        f.write(f"source_url: {URL}\n")
        f.write("title: Sony Interactive Entertainment - Business Data & Sales\n")
        f.write(f"sha256_of_saved_html: {sha}\n")
        f.write("downloaded_utc: 2026-10-01 (Claude Code cloud session, IQ-09)\n")
        f.write("note: the PlayStation Vita line reads 'Sales data on PlayStation Vita are not disclosed'\n")
    print(f"{len(rows)} rows -> {out}")


if __name__ == "__main__":
    main()
