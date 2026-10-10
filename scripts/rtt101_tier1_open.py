#!/usr/bin/env python3
"""RTT-101 (IQ-15m): every Tier 1 fee still UNVERIFIED, for Cowork's research lists. No fee figures (DEC-419 practice).
why_open: page did not load / quote does not match / no grade A/B source / other (the reason found first, in that order of evidence).
Usage: python3 scripts/rtt101_tier1_open.py   -> data/rtt-101/tier1_open.csv"""
import csv
from collections import defaultdict

D = "data/rtt-101"
T = [t for t in csv.DictReader(open(f"{D}/transfers.csv", encoding="utf-8"))
     if t["tier"] == "1" and t["status"] != "VERIFIED" and float(t["fee_gbp"] or 0) > 0]
names = {c["club_id"]: c["display_name"] for c in csv.DictReader(open(f"{D}/clubs.csv", encoding="utf-8"))}
E = defaultdict(list)
for e in csv.DictReader(open(f"{D}/fee_evidence.csv", encoding="utf-8")):
    E[e["transfer_id"]].append(e)
checks = defaultdict(list)
for c in csv.DictReader(open(f"{D}/source/runner_checks.csv", encoding="utf-8")):
    checks[c["url"]].append(c)
review = {r["check_id"]: r for r in csv.DictReader(open(f"{D}/source/review_decisions.csv", encoding="utf-8"))}
loaded = {r["url"] for r in csv.DictReader(open(f"{D}/source/page_dates.csv", encoding="utf-8"))}  # pages the runner's probes fetched
LEAD = {"manchester_united", "chelsea", "manchester_city"}
out = []
for t in sorted(T, key=lambda t: (not ({t["from_club"], t["to_club"]} & LEAD), t["date"], t["transfer_id"])):
    urls = []
    for e in E[t["transfer_id"]]:
        for u in ([e["url"]] if e["origin"] != "wikipedia_list" else e["cited_urls"].split()):
            if u.startswith("http") and "wikipedia.org" not in u and "transfermarkt" not in u.lower() and u not in urls:
                urls.append(u)
    why, url = "", ""
    for u in urls:
        cs = checks.get(u, [])
        if any(c["result"].startswith("BLOCKED") for c in cs):
            why, url = "page did not load", u
            break
    if not why:
        for u in urls:
            cs = checks.get(u, [])
            if any(c["result"].startswith("NOT CONFIRMED") for c in cs) or any(review.get(c["check_id"], {}).get("decision") == "reject" for c in cs):
                why, url = "quote does not match (figure not found next to the player's name, or rejected on review)", u
                break
    if not why:
        for u in urls:
            if u in loaded and not any(c["status"] == "VERIFIED" for c in checks.get(u, [])):
                why, url = "quote does not match (page loaded; the figure was not found next to the player's name)", u
                break
    if not why:
        for u in urls:
            if not checks.get(u) and u not in loaded:
                why, url = "other (cited page not yet read on the runner)", u
                break
    if not why:
        ab = [e for e in E[t["transfer_id"]] if e["origin"] in ("research_lead", "runner_check", "reported_search", "deal_structure") and e["grade"] in ("A", "B")]
        if not ab:
            why, url = "no grade A/B source (only a Wikipedia pointer or a grade C source)", urls[0] if urls else ""
        else:
            why, url = "other (a grade A/B lead whose page the runner has not confirmed)", ab[0]["url"]
    lead = sorted({t["from_club"], t["to_club"]} & LEAD)
    out.append({"transfer_id": t["transfer_id"], "player": t["player"], "from_club": names.get(t["from_club"], t["from_club"]),
                "to_club": names.get(t["to_club"], t["to_club"]), "date": t["date"], "season": t["season_attributed"],
                "current_grade": t["grade"], "tier_reason": t["tier_reason"], "why_open": why, "cited_url": url,
                "involves_leader": "yes" if lead else "no", "leader_clubs": ";".join(names[c] for c in lead)})
with open(f"{D}/tier1_open.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
    w.writeheader(); w.writerows(out)
from collections import Counter
print(len(out), "open Tier 1 fees;", sum(1 for r in out if r["involves_leader"] == "yes"), "involve a leader;",
      dict(Counter(r["why_open"].split(" (")[0] for r in out)))
