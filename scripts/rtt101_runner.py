#!/usr/bin/env python3
"""RTT-101 (IQ-15): fetch sources the Claude Code container cannot reach, on a GitHub runner.

Public repo (DEC-006, DEC-061): no secrets, no artifacts, no cache. Output goes to the job log only.
The job is described by data/rtt-101/runner_job.json:
  {"mode": "reference"}                     -> print ONS D7BT, Bank of England FX and ECB GBP/EUR as CSV blocks
  {"mode": "check", "items": [...]}         -> fetch each cited URL and report whether each figure appears
     item = {"id": "...", "url": "...", "needles": ["£35m", "35 million", ...]}
Never fetches transfermarkt (DEC-236).
"""
import hashlib, json, re, sys, time, urllib.request, html

UA = "Mozilla/5.0 (compatible; RTT-research/1.0; +https://github.com/marketmarathon/race-through-time)"
JOB = "data/rtt-101/runner_job.json"


def get(url, timeout=40):
    if "transfermarkt" in url.lower():
        return None, b"", "SKIPPED (Transfermarkt, DEC-236)"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), ""
    except urllib.error.HTTPError as e:
        return e.code, b"", str(e)
    except Exception as e:  # network errors are reported, never guessed
        return None, b"", repr(e)


def block(name, url):
    st, body, err = get(url)
    print(f"=== BEGIN {name} status={st} bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()} url={url} {err}")
    sys.stdout.write(body.decode("utf-8", "replace"))
    print(f"\n=== END {name}")
    time.sleep(2)


BOE = ("https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes"
       "&Datefrom=01/Jan/{y0}&Dateto=31/Dec/{y1}&SeriesCodes={codes}&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N")
MONTHLY = "XUMADMS,XUMAFFS,XUMAILS,XUMASPS,XUMANGS,XUMAPES,XUMAUSS,XUMAERS,XUMASFS,XUMASKS,XUMANKS,XUMADKS,XUMABFS"
DAILY = "XUDLERS,XUDLUSS,XUDLSFS,XUDLSKS,XUDLNKS,XUDLDKS"


def reference():
    block("ONS_D7BT", "https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/d7bt/mm23")
    block("BOE_MONTHLY", BOE.format(y0=1990, y1=2026, codes=MONTHLY))
    for y0, y1 in ((1990, 2001), (2002, 2013), (2014, 2026)):
        block(f"BOE_DAILY_{y0}_{y1}", BOE.format(y0=y0, y1=y1, codes=DAILY))
    block("ECB_GBP_EUR_M", "https://data-api.ecb.europa.eu/service/data/EXR/M.GBP.EUR.SP00.A?format=csvdata")
    block("BOE_LEGAL", "https://www.bankofengland.co.uk/legal")


def text_of(body):
    t = body.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def check(items, delay):
    for it in items:
        st, body, err = get(it["url"])
        t = text_of(body) if body else ""
        found = []
        for n in it.get("needles", []):
            i = t.find(n)
            if i >= 0:
                found.append((n, t[max(0, i - 90): i + len(n) + 60]))
        rec = {"id": it["id"], "status": st, "err": err[:80], "sha256": hashlib.sha256(body).hexdigest() if body else "",
               "bytes": len(body), "found": [f[0] for f in found], "excerpt": found[0][1] if found else ""}
        print("RTT101CHECK " + json.dumps(rec, ensure_ascii=False))
        sys.stdout.flush()
        time.sleep(delay)


if __name__ == "__main__":
    job = json.load(open(JOB, encoding="utf-8"))
    if job["mode"] == "reference":
        reference()
    elif job["mode"] == "check":
        check(job["items"], job.get("delay", 1.5))
