#!/usr/bin/env python3
"""RTT-101 phase 2 (IQ-15b): turn decoded runner probe results into
  data/rtt-101/source/runner_checks.csv   (appended: VERIFIED where a figure on the page, near the player's surname,
                                            equals an evidence amount for a transfer that cites the page)
  data/rtt-101/source/page_dates.csv       (publication date per page, when the page states one)
  data/rtt-101/source/undisclosed_candidates.csv (money figures near the surname on pages cited by undisclosed deals,
                                            for Claude's review; only reviewed rows in reported_fees.csv are used)
Usage: rtt101_ingest_probe.py JOB_JSON PROBE_JSONL RETRIEVED_DATE"""
import csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rtt101_lib as L  # noqa: E402
from rtt101_lib import grade_of  # noqa: E402

job, log, day = sys.argv[1], sys.argv[2], sys.argv[3]
D = "data/rtt-101"
items = {i["id"]: i for i in json.load(open(job, encoding="utf-8"))["probe"]}
T = {t["transfer_id"]: t for t in csv.DictReader(open(f"{D}/transfers.csv", encoding="utf-8"))}
E = list(csv.DictReader(open(f"{D}/fee_evidence.csv", encoding="utf-8")))
by_url = {}
for e in E:
    for u in ([e["url"]] if e["origin"] != "wikipedia_list" else e["cited_urls"].split()):
        by_url.setdefault(u, set()).add(e["transfer_id"])
amounts = {}
for e in E:
    if e["amount"] and e["currency"]:
        amounts.setdefault(e["transfer_id"], set()).add((round(float(e["amount"]) / 1e4), e["currency"]))
SKIP = re.compile(r"a week|a-week|per week|weekly|wages?|salary|release clause|buy-out|buyout|rejected|turned down|valued at|"
                  r"market value|turnover|revenue|profit|loss|debt|takeover|stadium|broadcast|tv deal", re.I)


def short(ex, money):
    words = ex.split()
    k = next((n for n, w in enumerate(words) if money.split()[0] in w), len(words) // 2)
    return " ".join(words[max(0, k - 10): k + 12])


def surname(p):
    return L.norm(re.sub(r"\(.*?\)", "", p)).split(" ")[-1] if p else ""


chk_path = f"{D}/source/runner_checks.csv"
checks = {r["check_id"]: r for r in csv.DictReader(open(chk_path, encoding="utf-8"))} if os.path.exists(chk_path) else {}
dates, cands = {}, []
for line in open(log, encoding="utf-8"):
    rec = json.loads(line)
    it = items.get(rec["id"])
    if not it:
        continue
    if rec.get("published"):
        dates[it["url"]] = {"url": it["url"], "published": rec["published"][:25], "page_sha256": rec["sha256"], "retrieved": day}
    near = L.norm(it["near"])
    tids = [tid for tid in by_url.get(it["url"], ()) if tid in T and surname(T[tid]["player"]) == near]
    for s in rec.get("snips", []):
        p = L.parse_fee(s["money"])
        if p["amount"] is None:
            continue
        key = (round(p["amount"] / 1e4), p["currency"])
        q = short(s["excerpt"], s["money"])
        for tid in tids:
            if key in amounts.get(tid, set()):
                cid = f"P{rec['id']}-{key[0]}{key[1]}"
                checks[cid] = {"check_id": cid, "transfer_id": tid, "near": it["near"], "url": it["url"], "amount": f"{p['amount']:.2f}",
                               "currency": p["currency"], "http_status": rec["status"], "result": "VERIFIED", "status": "VERIFIED",
                               "needle": s["money"], "quote": q, "quote_words": len(q.split()), "grade_by_publisher": grade_of(it["url"]),
                               "page_sha256": rec["sha256"], "retrieved": day}
            elif T[tid]["fee_status"].startswith("undisclosed") and not SKIP.search(s["excerpt"]):
                cands.append({"candidate_id": f"U{rec['id']}-{key[0]}{key[1]}", "transfer_id": tid, "player": T[tid]["player"],
                              "from_club": T[tid]["from_club"], "to_club": T[tid]["to_club"], "date": T[tid]["date"], "url": it["url"],
                              "grade_by_publisher": grade_of(it["url"]), "money": s["money"], "amount": f"{p['amount']:.2f}",
                              "currency": p["currency"], "quote": q, "published": rec.get("published", "")[:25]})
cols = ["check_id", "transfer_id", "near", "url", "amount", "currency", "http_status", "result", "status", "needle", "quote", "quote_words",
        "grade_by_publisher", "page_sha256", "retrieved"]
with open(chk_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore"); w.writeheader()
    for k in sorted(checks):
        w.writerow(checks[k])
dp = f"{D}/source/page_dates.csv"
old = {r["url"]: r for r in csv.DictReader(open(dp, encoding="utf-8"))} if os.path.exists(dp) else {}
old.update(dates)
with open(dp, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["url", "published", "page_sha256", "retrieved"], lineterminator="\n"); w.writeheader()
    for k in sorted(old):
        w.writerow(old[k])
cp = f"{D}/source/undisclosed_candidates.csv"
oldc = {r["candidate_id"]: r for r in csv.DictReader(open(cp, encoding="utf-8"))} if os.path.exists(cp) else {}
for c in cands:
    oldc[c["candidate_id"]] = c
if oldc:
    with open(cp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(next(iter(oldc.values())).keys()), lineterminator="\n"); w.writeheader()
        for k in sorted(oldc):
            w.writerow(oldc[k])
print(len(checks), "checks;", sum(1 for c in checks.values() if c["check_id"].startswith("P")), "from probes;", len(old), "page dates;",
      len(oldc), "undisclosed candidates")
