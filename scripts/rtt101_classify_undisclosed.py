#!/usr/bin/env python3
"""RTT-101 phase 2: pre-sort undisclosed-fee candidates for Claude's reading (DEC-257). Only the deal's own figure counts:
a BBC round-up line "Player [From - To] £Xm", or prose that ties the figure to this deal ("believed to be", "thought to be
worth", "for a fee of", "undisclosed ... around") with the surname shortly before it. Everything else is 'other_deal'.
Writes data/rtt-101/source/undisclosed_presort.csv; Claude's decisions go to reported_fees.csv."""
import csv, re, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rtt101_lib as L  # noqa: E402

rows = list(csv.DictReader(open("data/rtt-101/source/undisclosed_candidates.csv", encoding="utf-8")))
FEEWORD = re.compile(r"(believed to be|thought to be|understood to be|reported(ly)?|in the region of|for a fee of|fee of|undisclosed fee|"
                     r"a deal worth|deal worth|worth|around|about|for)\s*(an?\s+)?(initial\s+|reported\s+|fee\s+of\s+)?$", re.I)
out = []
for c in rows:
    q = c["quote"]
    sn = L.norm(c["player"]).split(" ")[-1]
    qn = L.norm(q)
    money = c["money"].strip(" ,.")
    i = q.find(money)
    before = q[:i] if i >= 0 else q
    kind = "other_deal"
    if re.search(r"\[[^\]]+\]\s*(reported\s*)?$", before, re.I) and sn in L.norm(before.split("]")[-2] if "]" in before else ""):
        kind = "roundup_line"
    elif sn in L.norm(before) and FEEWORD.search(before.strip()) and not re.search(r"\b(in|since) (19|20)\d\d\b|previous|earlier|cost .* in|joined .* from .* for", q[i:i + 60] + before[-80:], re.I):
        kind = "prose"
    if c["grade_by_publisher"] not in ("A", "B"):
        kind += "_gradeD"
    out.append(dict(c, presort=kind))
with open("data/rtt-101/source/undisclosed_presort.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(out)
from collections import Counter
print(Counter(o["presort"] for o in out))
