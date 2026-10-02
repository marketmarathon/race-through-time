#!/usr/bin/env python3
"""RTT-003: transcribe Nintendo's "Consolidated Sales Transition by Region" (hardware rows)
into data/rtt-003/source/nintendo_fy_hardware.csv.

Input: the spreadsheet downloaded from Nintendo IR
  https://www.nintendo.co.jp/ir/finance/historical_data/xls/consolidated_sales_e2603.xlsx
(as of 31 Mar 2026). The spreadsheet itself is NOT committed (DEC-006: third-party file);
its SHA-256 is recorded in the output header comment file and in manifest.json.

Nintendo prints units in ten thousands, rounded to the nearest ten thousand. Amounts under
10,000 units are printed as markers 0.1 (small positive) or -0.1 (small negative); they are
kept as printed in `raw` and counted as 0 in `units` with `marker` set.

Usage: python scripts/rtt003_extract_nintendo.py <path-to-xlsx> data/rtt-003/source
Needs openpyxl (not in the standard library; only this extraction step needs it).
"""
import csv
import hashlib
import os
import sys
from decimal import Decimal

import openpyxl

SOURCE_URL = "https://www.nintendo.co.jp/ir/finance/historical_data/xls/consolidated_sales_e2603.xlsx"


def norm_period(label):
    label = str(label).replace("\n", " ").strip()
    if label.lower().startswith("life"):
        return "LTD"
    return label.replace(" ", "")  # "FY3/2024 ~" -> "FY3/2024~"


def main():
    xlsx, outdir = sys.argv[1], sys.argv[2]
    sha = hashlib.sha256(open(xlsx, "rb").read()).hexdigest()
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    rows_out = []
    for ws in wb.worksheets:
        periods = {}
        platform = released = None
        kind = None
        model = None
        kind_col = None
        for row in ws.iter_rows(values_only=True):
            cells = list(row)
            # header row with fiscal-year labels
            if any(isinstance(c, str) and c.startswith("FY3/") for c in cells):
                periods = {i: norm_period(c) for i, c in enumerate(cells)
                           if isinstance(c, str) and (c.startswith("FY3/") or c.lower().startswith("life"))}
                continue
            if isinstance(cells[0], str) and cells[0].startswith(" ") and all(c is None for c in cells[1:]):
                platform = cells[0].strip()
                kind = model = None
                continue
            if len(cells) > 1 and isinstance(cells[1], str) and cells[1].startswith("released on"):
                released = cells[1].strip()
                continue
            if any(c in ("Hardware", "Software") for c in cells):
                kind_col = next(i for i, c in enumerate(cells) if c in ("Hardware", "Software"))
                kind = cells[kind_col]
                model = "family"
            labels = [c for c in cells if isinstance(c, str) and c.startswith("of which")]
            if labels:
                model = labels[0].replace("of which", "").strip()
            if kind != "Hardware" or kind_col is None:
                continue
            region = cells[kind_col + 1]
            if region not in ("Japan", "The Americas", "Europe", "Other", "Total"):
                continue
            for i, period in sorted(periods.items()):
                raw = cells[i] if i < len(cells) else None
                if raw is None:
                    continue
                d = Decimal(str(raw))
                if abs(d) < 1 and d != 0:
                    units, marker = 0, ("lt10k_pos" if d > 0 else "lt10k_neg")
                else:
                    units, marker = int(d * 10000), ""
                rows_out.append({
                    "sheet": ws.title, "platform": platform, "released": released, "model": model,
                    "region": region, "period": period, "raw_ten_thousands": str(raw),
                    "units": units, "marker": marker,
                })
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "nintendo_fy_hardware.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows_out)
    with open(os.path.join(outdir, "nintendo_fy_hardware.source.txt"), "w", encoding="utf-8") as f:
        f.write(f"source_url: {SOURCE_URL}\n")
        f.write("title: Nintendo Co., Ltd. Consolidated Sales Transition by Region (as of March 31, 2026)\n")
        f.write(f"sha256_of_downloaded_xlsx: {sha}\n")
        f.write("downloaded_utc: 2026-10-01 (Claude Code cloud session, IQ-09)\n")
        f.write("note: units in ten thousands as printed; figures rounded by Nintendo to the nearest ten thousand; "
                "0.1/-0.1 markers = under 10,000 units (counted as 0)\n")
    print(f"{len(rows_out)} rows -> {out}; xlsx sha256 {sha}")


if __name__ == "__main__":
    main()
