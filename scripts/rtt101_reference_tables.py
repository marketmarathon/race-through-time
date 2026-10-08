#!/usr/bin/env python3
"""RTT-101 (IQ-15): build cpi.csv and fx.csv from files the runner fetched (decoded by rtt101_decode_log.py).
Usage: rtt101_reference_tables.py RUNNER_DIR DATA_DIR
Values are copied exactly as published (text), never interpolated or rounded."""
import csv, datetime, os, sys

RUN, OUT = sys.argv[1], sys.argv[2]
idx = {}
for line in open(os.path.join(RUN, "index.tsv"), encoding="utf-8"):
    name, st, err, sha, n = line.rstrip("\n").split("\t")
    idx[name] = {"status": st, "sha256": sha}
MON = {m: i for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}

# --- ONS D7BT (CPI index 2015 = 100), monthly rows "YYYY MON","value"
ons_url = "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23"
rows = []
meta = {}
for r in csv.reader(open(os.path.join(RUN, "ONS_D7BT.csv"), encoding="utf-8-sig")):
    if len(r) < 2:
        continue
    k, v = r[0].strip(), r[1].strip()
    p = k.split()
    if len(p) == 2 and p[0].isdigit() and p[1] in MON:
        rows.append((f"{p[0]}-{MON[p[1]]:02d}", v))
    elif not (len(p) in (1, 2) and p[0].isdigit()):
        meta[k] = v
with open(os.path.join(OUT, "cpi.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["month", "cpi_d7bt_2015_100", "series", "source_url", "release_date", "retrieved", "file_sha256"])
    for m, v in rows:
        w.writerow([m, v, "D7BT", ons_url, meta.get("Release date", ""), "2026-10-07", idx["ONS_D7BT.csv"]["sha256"]])
print("cpi rows", len(rows), rows[0], rows[-1], "release", meta.get("Release date"), "next", meta.get("Next release"))

# --- Bank of England: monthly averages and daily spot (currency units per £1)
SER = {"XUMADMS": ("DEM", "monthly average"), "XUMAFFS": ("FRF", "monthly average"), "XUMAILS": ("ITL", "monthly average"),
       "XUMASPS": ("ESP", "monthly average"), "XUMANGS": ("NLG", "monthly average"), "XUMAPES": ("PTE", "monthly average"),
       "XUMAUSS": ("USD", "monthly average"), "XUMAERS": ("EUR", "monthly average"), "XUMASFS": ("CHF", "monthly average"),
       "XUMASKS": ("SEK", "monthly average"), "XUMANKS": ("NOK", "monthly average"), "XUMADKS": ("DKK", "monthly average"),
       "XUMABFS": ("BEF", "monthly average"),
       "XUDLERS": ("EUR", "daily spot"), "XUDLUSS": ("USD", "daily spot"), "XUDLSFS": ("CHF", "daily spot"),
       "XUDLSKS": ("SEK", "daily spot"), "XUDLNKS": ("NOK", "daily spot"), "XUDLDKS": ("DKK", "daily spot"),
       "XUDLDMS": ("DEM", "daily spot"), "XUDLFFS": ("FRF", "daily spot")}
fx = []
for fn in ("BOE_MONTHLY.csv", "BOE_DAILY.csv"):
    rd = csv.reader(open(os.path.join(RUN, fn), encoding="utf-8-sig"))
    head = next(rd)
    for r in rd:
        if not r or not r[0].strip():
            continue
        d = datetime.datetime.strptime(r[0].strip(), "%d %b %Y").date().isoformat()
        for code, v in zip(head[1:], r[1:]):
            code, v = code.strip(), v.strip()
            if v and code in SER and d >= "1992-01-01":
                fx.append((code, d, v))
fx.sort()
with open(os.path.join(OUT, "fx.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["series_code", "currency", "kind", "date", "units_per_gbp"])
    for code, d, v in fx:
        cur, kind = SER[code]
        w.writerow([code, cur, kind, d, v])
with open(os.path.join(OUT, "fx_series.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["series_code", "currency", "kind", "unit", "first_date", "last_date", "rows", "source", "fetched_file", "file_sha256", "licence_note"])
    for code in sorted({c for c, _, _ in fx}):
        ds = [d for c, d, _ in fx if c == code]
        cur, kind = SER[code]
        fn = "BOE_MONTHLY.csv" if code.startswith("XUMA") else "BOE_DAILY.csv"
        w.writerow([code, cur, kind, f"{cur} per £1", ds[0], ds[-1], len(ds), "Bank of England database (fetched on a GitHub runner, 7 Oct 2026)",
                    fn, idx[fn]["sha256"], "owner-accepted risk; credited (DEC-239)"])
print("fx rows", len(fx), sorted({c for c, _, _ in fx}))

# --- ECB GBP per EUR monthly reference rate (cross-check only)
ecb = []
for r in csv.DictReader(open(os.path.join(RUN, "ECB_GBP_EUR_M.csv"), encoding="utf-8-sig")):
    ecb.append((r["TIME_PERIOD"], r["OBS_VALUE"]))
with open(os.path.join(OUT, "fx_ecb_crosscheck.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["month", "gbp_per_eur", "series", "source", "file_sha256"])
    for m, v in ecb:
        w.writerow([m, v, "EXR.M.GBP.EUR.SP00.A", "European Central Bank (credited; cross-check only)", idx["ECB_GBP_EUR_M.csv"]["sha256"]])
print("ecb rows", len(ecb), ecb[:1], ecb[-1:])
