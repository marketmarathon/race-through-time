#!/usr/bin/env python3
"""RTT-101 source rounds (DEC-275): probe every page ChatGPT cited for a named deal (lead section "S"), with the check that
the page also names both clubs. Writes the probe job to data/rtt-101/runner_job_b.json and an empty runner_job.json.
Usage: rtt101_make_source_round.py [LEAD_FILE_PREFIX ...]   e.g. part20b part20d part20f"""
import csv, hashlib, json, re, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rtt101_lib as L  # noqa: E402

prefixes = tuple(sys.argv[1:])
T = {t["transfer_id"]: t for t in csv.DictReader(open("data/rtt-101/transfers.csv", encoding="utf-8"))}
A = {r["club_id"]: [r["display_name"]] + [x for x in r["other_names"].split("|") if x and "(" not in x]
     for r in csv.DictReader(open("data/rtt-101/source/club_aliases.csv", encoding="utf-8"))}


GENERIC = {"united", "city", "town", "rovers", "athletic", "wanderers", "albion", "real", "sporting", "club", "football", "county", "fc", "afc",
           "the", "de", "sc", "bk", "if", "fk", "ac", "cf", "cd", "sv", "vfb", "vfl", "kv"}


def names(c):
    """The club as a page may name it: our aliases for PL clubs; for others the full name plus each distinctive word of four or more
    letters (AC Milan -> Milan, Red Star Belgrade -> Belgrade/Star, FC Sion -> Sion), so a short form on the page still counts."""
    if c in A:
        return A[c]
    words = [w for w in re.split(r"[ .]", c) if len(w) >= 4 and w.lower() not in GENERIC]
    return [c] + [w for w in words if w != c]


def near_word(player, quote):
    """The player's surname as the page spells it: our surname if the quote has it, else the quote's word that shares its first
    four letters (Stensgaard/Steensgaard), else our surname."""
    sn = re.sub(r"\(.*?\)", "", player).strip().split(" ")[-1]
    qn = L.norm(quote)
    if L.norm(sn) in qn.split():
        return sn
    for w in re.findall(r"[A-Z][\w'’-]+", quote):
        if L.norm(w)[:4] == L.norm(sn)[:4]:
            return w
    return sn


probe, seen = [], set()
for r in csv.DictReader(open("data/rtt-101/source/leads_evidence.csv", encoding="utf-8")):
    if r["lead_section"] != "S" or (prefixes and not r["lead_row"].startswith(prefixes)):
        continue
    t = T.get(r["transfer_ref"])
    if not t:
        continue
    nw = near_word(t["player"], r["quote"])
    for u in (r["url"], r["archive_url"]):
        if not u.startswith("http") or "transfermarkt" in u.lower() or "wikipedia.org" in u.lower():
            continue
        pid = hashlib.sha256(f"{u}|{nw}|clubs".encode()).hexdigest()[:16]
        if pid in seen:
            continue
        seen.add(pid)
        probe.append({"id": pid, "url": u, "near": nw, "also": [names(t["from_club"]), names(t["to_club"])], "group": "src"})
json.dump({"delay": 0.8, "probe": probe}, open("data/rtt-101/runner_job_b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump({"delay": 1.0}, open("data/rtt-101/runner_job.json", "w", encoding="utf-8"), indent=0)
print(len(probe), "pages to probe")
