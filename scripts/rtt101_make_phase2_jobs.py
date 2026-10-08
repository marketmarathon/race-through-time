#!/usr/bin/env python3
"""RTT-101 phase 2 (IQ-15b): runner jobs.
Job A (runner_job.json): Wikipedia pages (Leeds United A.F.C. 1992-2002 seasons; 1991-92 club seasons for the last
First Division matchday) and, for player articles, only the sentences that mention a fee with their citations.
Job B (runner_job_b.json): probe cited press/club pages for every money figure near the player's surname:
Tier 1 fees not yet VERIFIED, and undisclosed deals involving a club that is ever in the top 12 (DEC-257)."""
import csv, hashlib, json, re

T = list(csv.DictReader(open("data/rtt-101/transfers.csv", encoding="utf-8")))
E = list(csv.DictReader(open("data/rtt-101/fee_evidence.csv", encoding="utf-8")))
S = list(csv.DictReader(open("data/rtt-101/series_monthly.csv", encoding="utf-8")))
top12 = {r["club_id"] for r in S if r["rank"] and int(r["rank"]) <= 12 and r["month_end"] >= "1992-07-31"}
ev = {}
for e in E:
    ev.setdefault(e["transfer_id"], []).append(e)


def surname(p):
    return re.sub(r"\(.*?\)", "", p).strip().split(" ")[-1]


t1u = [t for t in T if t["tier"] == "1" and t["status"] != "VERIFIED"]
und = [t for t in T if t["fee_status"].startswith("undisclosed") and (t["from_club"] in top12 or t["to_club"] in top12)]
wiki = [f"{y}–{(y + 1) % 100:02d} Leeds United A.F.C. season" if y != 1999 else "1999–2000 Leeds United A.F.C. season" for y in range(1992, 2002)]
wiki += [f"1991–92 {c} season" for c in ("Leeds United A.F.C.", "Manchester United F.C.", "Sheffield Wednesday F.C.", "Arsenal F.C.",
                                          "Liverpool F.C.", "Norwich City F.C.", "Luton Town F.C.", "West Ham United F.C.")]
arts = sorted({t["player_article"] for t in t1u + und if t["player_article"]})
json.dump({"delay": 1.0, "wiki": wiki, "wiki_fees": arts}, open("data/rtt-101/runner_job.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
probe, seen = [], set()
for group, rows in (("t1", t1u), ("und", und)):
    for t in rows:
        sn = surname(t["player"])
        urls = []
        for e in ev.get(t["transfer_id"], []):
            urls += [e["url"]] if e["origin"] in ("research_lead", "runner_check") else e["cited_urls"].split()
        for u in urls:
            if not u.startswith("http") or "wikipedia.org" in u or "transfermarkt" in u.lower():
                continue
            pid = hashlib.sha256(f"{u}|{sn}".encode()).hexdigest()[:16]
            if pid in seen:
                continue
            seen.add(pid)
            probe.append({"id": pid, "url": u, "near": sn, "group": group})
json.dump({"delay": 0.8, "probe": probe}, open("data/rtt-101/runner_job_b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(wiki), "wiki pages;", len(arts), "player articles;", len(probe), "probe pages (", sum(1 for p in probe if p["group"] == "t1"), "Tier 1,",
      sum(1 for p in probe if p["group"] == "und"), "undisclosed )")
