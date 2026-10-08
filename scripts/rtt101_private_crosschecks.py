#!/usr/bin/env python3
"""RTT-101 (IQ-15): cross-checks against the PRIVATE research files (never committed, DEC-006).
Writes only results (counts, differences, file SHA-256) to data/rtt-101/source/private_crosschecks.md,
which the build appends to CHECKS.md. Usage: rtt101_private_crosschecks.py PRIVATE_DIR"""
import csv, hashlib, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rtt101_lib as L  # noqa: E402

P = sys.argv[1]
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "rtt-101")
out = ["## Cross-checks against the private research files (results only; the files stay private, DEC-006)\n"]


def h(fn):
    return hashlib.sha256(open(os.path.join(P, fn), "rb").read()).hexdigest()


f3 = "part03b_premier_league_membership_C_1992-2026.csv"
ours = {(r["season"], r["club_id"]): r for r in csv.DictReader(open(os.path.join(D, "pl_membership.csv"), encoding="utf-8"))}
theirs = {}
for r in csv.DictReader(open(os.path.join(P, f3), encoding="utf-8-sig")):
    theirs[(r["season"], L.club_id(r["club_as_named_in_extraction_source"]))] = r
only_ours = sorted(set(ours) - set(theirs))
only_theirs = sorted(set(theirs) - set(ours))
pos_diff = [k for k in set(ours) & set(theirs) if ours[k]["final_position"] and theirs[k]["final_position"].isdigit()
            and int(ours[k]["final_position"]) != int(theirs[k]["final_position"])]
rel_diff = sorted(k for k in set(ours) & set(theirs) if k[0] != "2026-27"
                  and (ours[k]["relegated"] == "yes") != (theirs[k]["relegated"].strip().lower() == "yes"))
ok = not only_ours and not only_theirs
known = [("1992-93", "oldham_athletic"), ("1993-94", "ipswich_town")]
out.append(f"| Membership (club-seasons) matches part03b (SHA-256 `{h(f3)[:16]}…`) | **{'PASS' if ok else 'FAIL'}** | "
           f"{len(ours)} ours vs {len(theirs)} theirs; only ours {only_ours[:3]}; only theirs {only_theirs[:3]} |\n")
out.append(f"| Relegated flags: part03b differs only in the two known errors plus 1996-97 | **{'PASS' if [k for k in rel_diff if k not in known and k[0] != '1996-97'] == [] else 'FAIL'}** | "
           f"differences {rel_diff}. Ours is derived from membership (in the PL in N, not in N+1). 1996-97: Middlesbrough went down after a points deduction and Coventry stayed up; part03b has them the other way round (finding: it ignores points deductions) |\n")
out.append(f"| Final positions: part03b differs only where a points deduction applied | **{'PASS' if all(k[0] in ('1996-97', '2023-24') for k in pos_diff) else 'FAIL'}** | "
           f"{len(pos_diff)} differences, all in 1996-97 (Middlesbrough deduction) and 2023-24 (Everton deduction): {sorted(pos_diff)} |\n")
f4 = "part04b_premier_league_calendar_D_1991-2027.csv"
seas = {r["season"]: r for r in csv.DictReader(open(os.path.join(D, "seasons.csv"), encoding="utf-8"))}
diff = []
for r in csv.DictReader(open(os.path.join(P, f4), encoding="utf-8-sig")):
    s = seas.get(r["season"])
    if s and s["last_matchday"] != r["last_league_matchday_date"]:
        diff.append((r["season"], s["last_matchday"], r["last_league_matchday_date"]))
expected = [("2015-16", "2016-05-17", "2016-05-15")]
out.append(f"| Last PL matchday per season agrees with part04b (SHA-256 `{h(f4)[:16]}…`) | **{'PASS' if diff == expected else 'DIFFERENCES'}** | "
           f"{len(seas)} seasons compared; differences (season, ours, research): {diff}. 2015-16 ends 17 May 2016, the replayed match (brief section 7); part04b gives the scheduled last day |\n")
open(os.path.join(D, "source", "private_crosschecks.md"), "w", encoding="utf-8").write("| Check | Result | Detail |\n|---|---|---|\n".join([out[0], ""]) + "".join(out[1:]))
print("".join(out))
