#!/usr/bin/env python3
"""RTT-101 (IQ-15j): probe, on the GitHub runner, every page the Wikipedia rows cite for the deals of one window that are not yet
VERIFIED (club-season or list page citations; never Wikipedia or Transfermarkt), so a stated fee can be confirmed at source and an
undisclosed deal can pick up a reported figure. Writes data/rtt-101/runner_job_b.json and an empty runner_job.json.
Usage: rtt101_make_window_probe.py "January 2020" [MORE WINDOWS ...]"""
import csv, hashlib, json, re, sys


wins = set(sys.argv[1:])
D = "data/rtt-101"
T = {t["transfer_id"]: t for t in csv.DictReader(open(f"{D}/transfers.csv", encoding="utf-8"))}
PL = {(r["club_id"], r["season"]) for r in csv.DictReader(open(f"{D}/pl_membership.csv", encoding="utf-8"))}
A = {r["club_id"]: [r["display_name"]] + [x for x in r["other_names"].split("|") if x and "(" not in x]
     for r in csv.DictReader(open(f"{D}/source/club_aliases.csv", encoding="utf-8"))}
GENERIC = {"united", "city", "town", "rovers", "athletic", "wanderers", "albion", "real", "sporting", "club", "football", "county", "fc", "afc",
           "the", "de", "sc", "bk", "if", "fk", "ac", "cf", "cd", "sv", "vfb", "vfl", "kv"}


def names(c):
    """as in rtt101_make_source_round.py: our aliases for PL clubs, else the name plus its distinctive words"""
    if c in A:
        return A[c]
    words = [w for w in re.split(r"[ .]", c) if len(w) >= 4 and w.lower() not in GENERIC]
    return [c] + [w for w in words if w != c]


def window_of(d):
    m, y = int(d[5:7]), int(d[:4])
    return f"summer {y}" if 4 <= m <= 10 else (f"January {y}" if m <= 3 else f"January {y + 1}")


probe, seen = [], set()
for e in csv.DictReader(open(f"{D}/fee_evidence.csv", encoding="utf-8")):
    t = T.get(e["transfer_id"])
    if not t or t["status"] == "VERIFIED" or window_of(t["date"]) not in wins or t["type"] in ("loan", "loan_return"):
        continue
    if not any((c, t["season_attributed"]) in PL for c in (t["from_club"], t["to_club"])):
        continue
    sn = re.sub(r"\(.*?\)", "", t["player"]).strip().split(" ")[-1]
    for u in e["cited_urls"].split():
        if not u.startswith("http") or "transfermarkt" in u.lower() or "wikipedia.org" in u.lower():
            continue
        pid = hashlib.sha256(f"{u}|{sn}|window".encode()).hexdigest()[:16]
        if pid in seen:
            continue
        seen.add(pid)
        probe.append({"id": pid, "url": u, "near": sn, "also": [names(t["from_club"]), names(t["to_club"])], "group": "window"})
json.dump({"delay": 0.8, "anchored": True, "probe": probe}, open(f"{D}/runner_job_b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump({"delay": 1.0}, open(f"{D}/runner_job.json", "w", encoding="utf-8"), indent=0)
print(len(probe), "pages to probe for", ", ".join(sorted(wins)))
