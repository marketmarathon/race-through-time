#!/usr/bin/env python3
"""RTT-101 phase 2 round 6: gap-list pages (DEC-264, sections A v2, B, C) probed with a club-name check, and player-article fee sentences
for gap-list moves, undated gap moves and lead-only pre-2002 transfers. Job A = wiki_fees, job B = probe."""
import csv, hashlib, json, re, subprocess

# skip what round 5 (commit 45613c3) already fetched
_r5a = json.loads(subprocess.check_output(["git", "show", "45613c3:data/rtt-101/runner_job.json"]))
_r5b = json.loads(subprocess.check_output(["git", "show", "45613c3:data/rtt-101/runner_job_b.json"]))
DONE_P = {p["id"] for p in _r5b["probe"]}
DONE_A = set(_r5a["wiki_fees"])

T = {t["transfer_id"]: t for t in csv.DictReader(open("data/rtt-101/transfers.csv", encoding="utf-8"))}
E = list(csv.DictReader(open("data/rtt-101/fee_evidence.csv", encoding="utf-8")))
A = {r["club_id"]: [r["display_name"]] + [x for x in r["other_names"].split("|") if x and "(" not in x]
     for r in csv.DictReader(open("data/rtt-101/source/club_aliases.csv", encoding="utf-8"))}
leads = {r["url"]: r for r in csv.DictReader(open("data/rtt-101/source/leads_evidence.csv", encoding="utf-8")) if r["lead_section"] == "G"}


def names(c):
    if c in A:
        return A[c]
    first = re.split(r"[ .]", c)[0]
    return [c] + ([first] if len(first) > 3 else [])


def surname(p):
    return re.sub(r"\(.*?\)", "", p).strip().split(" ")[-1]


probe, seen = [], set()
for e in E:
    t = T.get(e["transfer_id"])
    if not t or e["origin"] != "research_lead" or e["url"] not in leads:
        continue
    sn = surname(t["player"])
    pid = hashlib.sha256(f"{e['url']}|{sn}|clubs".encode()).hexdigest()[:16]
    if pid in seen or pid in DONE_P or not e["url"].startswith("http"):
        continue
    seen.add(pid)
    probe.append({"id": pid, "url": e["url"], "near": sn, "also": [names(t["from_club"]), names(t["to_club"])], "group": "gap"})
arts = set()
for t in T.values():
    if t["found_via"].startswith(("ChatGPT gap list", "research lead")) and t["season_attributed"] < "2007-08":
        arts.add(t["player_article"] or t["player"])
for r in csv.DictReader(open("data/rtt-101/unmatched_leads.csv", encoding="utf-8")):
    if r["section"] == "G":
        arts.add(r["player"])
arts -= DONE_A
json.dump({"delay": 1.0, "wiki_fees": sorted(arts)}, open("data/rtt-101/runner_job.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump({"delay": 0.8, "probe": probe}, open("data/rtt-101/runner_job_b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(arts), "player articles;", len(probe), "gap-list pages")
