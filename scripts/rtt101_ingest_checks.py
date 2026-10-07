#!/usr/bin/env python3
"""RTT-101 (IQ-15): turn a decoded runner check log into data/rtt-101/source/runner_checks.csv.
VERIFIED = the runner fetched the cited page and found the figure within 400 characters of the player's surname;
the quote is a short excerpt (under 25 words) around the figure. Anything else stays UNVERIFIED, with the reason.
Usage: rtt101_ingest_checks.py JOB_JSON CHECKS_JSONL RETRIEVED_DATE   (appends; the newest result per check wins)"""
import csv, json, os, re, sys, urllib.parse

job, log, day = sys.argv[1], sys.argv[2], sys.argv[3]
OUT = "data/rtt-101/source/runner_checks.csv"
items = {i["id"]: i for i in json.load(open(job, encoding="utf-8"))["check"]}
B = ("bbc.co.uk", "bbc.com", "theguardian.com", "guardian.co.uk", "observer", "skysports.com", "sky.com", "independent.co.uk",
     "the-independent.com", "telegraph.co.uk", "thetimes.co.uk", "timesonline", "reuters.com", "uefa.com", "nytimes.com",
     "theathletic.com", "espn.", "ft.com", "pa.media")
A = ("premierleague.com", "fc.com", "fc.co.uk", "arsenal.com", "mancity.com", "manutd.com", "tottenhamhotspur.com", "nufc.co.uk",
     "evertonfc.com", "whufc.com", "avfc.co.uk", "lcfc.com", "wolves.co.uk", "afcb.co.uk", "brightonandhovealbion.com", "cpfc.co.uk",
     "fulhamfc.com", "nottinghamforest.co.uk", "brentfordfc.com", "leedsunited.com", "burnleyfootballclub.com", "sunderlandafc.com",
     "ipswichtown.co.uk", "coventrycity.co.uk", "hullcitytigers.com", "londonstockexchange.com", "juventus.com", "realmadrid.com",
     "fcbarcelona.com", "slbenfica.pt", "sporting.pt", "bvb.de", "psg.fr")
C = ("soccerbase.com", "wikipedia.org", "worldfootball.net")


def grade_of(url):
    h = urllib.parse.urlparse(url).netloc.lower()
    if any(x in h for x in C):
        return "C"
    if any(x in h for x in A):
        return "A"
    if any(x in h for x in B):
        return "B"
    return "D"


def short(ex, needle):
    words = ex.split()
    k = next((n for n, w in enumerate(words) if needle.split()[0] in w), len(words) // 2)
    return " ".join(words[max(0, k - 10): k + 12])


rows = {}
if os.path.exists(OUT):
    for r in csv.DictReader(open(OUT, encoding="utf-8")):
        rows[r["check_id"]] = r
for line in open(log, encoding="utf-8"):
    rec = json.loads(line)
    it = items.get(rec["id"])
    if not it:
        continue
    st = rec["status"]
    if rec["needle"]:
        res = "VERIFIED"
    elif st == 200:
        res = "NOT CONFIRMED (page fetched; figure not found near the player's name)"
    else:
        res = f"BLOCKED or gone ({rec['err'] or st})"
    q = short(rec["excerpt"], rec["needle"]) if rec["needle"] else ""
    rows[rec["id"]] = {"check_id": rec["id"], "transfer_id": it["transfer_id"], "url": it["url"], "amount": it["amount"],
                       "currency": it["currency"], "http_status": st, "result": res, "status": "VERIFIED" if res == "VERIFIED" else "UNVERIFIED",
                       "needle": rec["needle"], "quote": q, "quote_words": len(q.split()), "grade_by_publisher": grade_of(it["url"]),
                       "page_sha256": rec["sha256"], "retrieved": day}
cols = ["check_id", "transfer_id", "url", "amount", "currency", "http_status", "result", "status", "needle", "quote", "quote_words",
        "grade_by_publisher", "page_sha256", "retrieved"]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader()
    for k in sorted(rows):
        w.writerow(rows[k])
from collections import Counter
print(len(rows), "checks;", Counter(r["result"][:13] for r in rows.values()))
