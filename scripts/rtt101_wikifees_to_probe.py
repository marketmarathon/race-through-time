#!/usr/bin/env python3
"""RTT-101 phase 2: player-article fee sentences (Wikipedia pointers, grade C) -> cited pages to probe.
A sentence is linked to a transfer when it names the other club and mentions a year within one of the transfer date.
Writes data/rtt-101/source/player_article_citations.csv (pointers only) and the probe job runner_job_b.json.
Usage: rtt101_wikifees_to_probe.py WIKIFEES_JSONL"""
import csv, hashlib, json, re, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rtt101_lib as L  # noqa: E402

src = sys.argv[1]
T = list(csv.DictReader(open("data/rtt-101/transfers.csv", encoding="utf-8")))
S = list(csv.DictReader(open("data/rtt-101/series_monthly.csv", encoding="utf-8")))
top12 = {r["club_id"] for r in S if r["rank"] and int(r["rank"]) <= 12 and r["month_end"] >= "1992-07-31"}
alias = {}
for r in csv.DictReader(open("data/rtt-101/source/club_aliases.csv", encoding="utf-8")):
    alias[r["club_id"]] = [r["display_name"]] + [x for x in r["other_names"].split("|") if x and "(" not in x]
arts = {}
for line in open(src, encoding="utf-8"):
    rec = json.loads(line)
    arts[rec["title"]] = rec
want = [t for t in T if (t["tier"] == "1" and t["status"] != "VERIFIED") or (t["tier"] == "2" and t["status"] != "VERIFIED")
        or (t["fee_status"].startswith("undisclosed") and (t["from_club"] in top12 or t["to_club"] in top12))]
cit, probe, seen = [], [], set()
for t in want:
    a = arts.get(t["player_article"])
    if not a or not t["date"]:
        continue
    y = int(t["date"][:4])
    names = []
    for c in (t["from_club"], t["to_club"]):
        names += alias.get(c, [c])
    names = [n for n in names if n and len(n) > 2]
    sn = re.sub(r"\(.*?\)", "", t["player"]).strip().split(" ")[-1]
    for s in a["sentences"]:
        txt = s["text"]
        yrs = [int(x) for x in re.findall(r"\b(19\d\d|20\d\d)\b", txt)]
        if not any(n.lower() in txt.lower() for n in names) or (yrs and not any(abs(v - y) <= 1 for v in yrs)):
            continue
        for u in s["urls"]:
            if not u.startswith("http") or "transfermarkt" in u.lower() or "wikipedia.org" in u:
                continue
            cit.append({"transfer_id": t["transfer_id"], "player_article": t["player_article"], "revid": a["revid"], "sentence": txt[:300], "url": u})
            pid = hashlib.sha256(f"{u}|{sn}".encode()).hexdigest()[:16]
            if pid not in seen:
                seen.add(pid)
                probe.append({"id": pid, "url": u, "near": sn, "group": "article"})
with open("data/rtt-101/source/player_article_citations.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["transfer_id", "player_article", "revid", "sentence", "url"], lineterminator="\n")
    w.writeheader(); w.writerows(sorted(cit, key=lambda r: (r["transfer_id"], r["url"])))
json.dump({"delay": 0.8, "probe": probe}, open("data/rtt-101/runner_job_b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(want), "transfers wanted;", len({c['transfer_id'] for c in cit}), "with article citations;", len(probe), "pages to probe")
