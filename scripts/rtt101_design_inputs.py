#!/usr/bin/env python3
"""RTT-101 (IQ-15m): write data/rtt-101/DESIGN_INPUTS.md for the design session from the built files (deterministic).
Usage: python3 scripts/rtt101_design_inputs.py"""
import csv
from collections import defaultdict

D = "data/rtt-101"


def rd(n):
    return list(csv.DictReader(open(f"{D}/{n}", encoding="utf-8")))


NAME = {c["club_id"]: c["display_name"] for c in rd("clubs.csv")}


def bymonth(rows):
    out = defaultdict(list)
    for r in rows:
        if r["rank"]:
            out[r["month_end"]].append(r)
    for mo in out:
        out[mo].sort(key=lambda r: int(r["rank"]))
    return out


ONS, PRE = bymonth(rd("series_onscreen.csv")), bymonth(rd("series_monthly.csv"))
ms = sorted(ONS)
last = ms[-1]


def m(v):
    return f"£{float(v) / 1e6:,.1f}m"


def crowns(bm):
    out = []
    for mo in sorted(bm):
        if not out or out[-1][1] != bm[mo][0]["club_id"]:
            out.append((mo, bm[mo][0]["club_id"]))
    return out


L = ["# RTT-101 design inputs (for the design session; built by `scripts/rtt101_design_inputs.py`)", "",
     "Nothing here is approved design. No visual feature or change to the approved look is built or rendered without Luke's approval "
     "(DEC-069). Figures are as built; the order at the freeze is not settled until Cowork's Tier 1 round (DEC-445).", "",
     "## What the player reads", "",
     "| File | Columns the player uses | Notes |", "|---|---|---|",
     "| `series_onscreen.csv` | `month_end`, `club_id`, `cum_net_gbp` (bar length and value), `rank`, `in_pl` (frozen-bar look), "
     "`pl_seasons_played`, `avg_real_net_per_season_gbp2026` (secondary statistic) | VERIFIED fees only (contract v1.5 §8, DEC-448); "
     f"{len(ms)} month ends from {ms[0]} to the freeze {last} (1 Sep 2026, 23:00 BST); `rank` is blank before a club's first PL season |",
     "| `clubs.csv` | `club_id`, `display_name` (bar label), `colour_key`, `logo_ref` | logos and colours: rights ledger and house style first |",
     "| `pl_membership.csv`, `seasons.csv` | season windows, who is in the PL each season | a club out of the PL keeps its value, frozen |",
     "| `coverage.csv` | undisclosed-fee count per club | for the \"Undisclosed fees not included\" note (DEC-429) |",
     "| `club_ledger.csv` | `notes` (conversions), `fee_status` | for any \"reported\" or converted-fee note |",
     "| `series_monthly.csv` | — | the all-fees preview: **not for screen** |", "",
     "## Who leads (on screen)", ""]
cr = crowns(ONS)
for i, (mo, c) in enumerate(cr):
    end = cr[i + 1][0] if i + 1 < len(cr) else None
    L.append(f"- {NAME.get(c, c)}: from {mo[:7]}" + (f" to {ms[ms.index(end) - 1][:7]}" if end else " to the freeze"))
L += ["", "Leader changes on screen: " + str(len(cr) - 1) + ". In the preview (all fees) the sequence differs; see report section 19.", "",
      "## Close calls on screen (leader ahead of second by under £3m at a month end)", ""]
cc = [(mo, ONS[mo][0]["club_id"], ONS[mo][1]["club_id"], float(ONS[mo][0]["cum_net_gbp"]) - float(ONS[mo][1]["cum_net_gbp"]))
      for mo in ms if float(ONS[mo][0]["cum_net_gbp"]) > 0 and float(ONS[mo][0]["cum_net_gbp"]) - float(ONS[mo][1]["cum_net_gbp"]) < 3e6]
spans, cur = [], None
for mo, a, b, g in cc:
    if cur and cur[1] == a and cur[2] == b and ms.index(mo) == ms.index(cur[4]) + 1:
        cur[4], cur[3] = mo, min(cur[3], g)
    else:
        cur = [mo, a, b, g, mo]
        spans.append(cur)
for s0, a, b, g, s1 in spans:
    L.append(f"- {s0[:7]}" + (f" to {s1[:7]}" if s1 != s0 else "") + f": {NAME.get(a, a)} over {NAME.get(b, b)}, smallest gap £{g / 1e6:.2f}m")
L += ["", f"None after {max(s[4] for s in spans)[:7]}." if spans else "None.", "",
      "## Negative bars in the top 12", ""]
neg = [(mo, r["club_id"], float(r["cum_net_gbp"])) for mo in ms for r in ONS[mo][:12] if float(r["cum_net_gbp"]) < 0]
L.append("On screen: none." if not neg else "On screen: " + "; ".join(f"{mo[:7]} {NAME.get(c, c)} {m(v)}" for mo, c, v in neg))
negp = [(mo, r["club_id"], float(r["cum_net_gbp"])) for mo in sorted(PRE) for r in PRE[mo][:12] if float(r["cum_net_gbp"]) < 0]
L.append("Preview: " + ("none." if not negp else "; ".join(f"{mo[:7]} {NAME.get(c, c)} {m(v)}" for mo, c, v in negp)) + " (a bar can go below zero only "
         "when a club's sales exceed its purchases; the axis must allow it).")
top = sorted({r["club_id"] for mo in ms for r in ONS[mo][:12]}, key=lambda c: NAME.get(c, c))
L += ["", f"## Clubs that reach the top 12 on screen: {len(top)}", "", ", ".join(NAME.get(c, c) for c in top) + ".", "",
      f"## At the freeze ({last}), on screen", "",
      "| Rank | Club | Cumulative net spend | Average CPI-adjusted net per PL season (secondary) | PL seasons |", "|---|---|---|---|---|"]
for r in ONS[last][:12]:
    L.append(f"| {r['rank']} | {NAME.get(r['club_id'], r['club_id'])} | {m(r['cum_net_gbp'])} | {m(r['avg_real_net_per_season_gbp2026'] or 0)} | {r['pl_seasons_played']} |")
TO = rd("tier1_open.csv")
L += ["", "## What may still change", "",
      f"- **{len(TO)} Tier 1 fees are UNVERIFIED** (`tier1_open.csv`; {sum(1 for r in TO if r['involves_leader'] == 'yes')} involve Manchester United, "
      "Chelsea or Manchester City). Each one confirmed joins the on-screen bars; if all the leaders' unconfirmed fees were confirmed, Chelsea would "
      "fall by £56.1m, Manchester City by £52.9m and Manchester United rise by £40.3m, which would put United first at the freeze (as in the preview).",
      "- Tier 2 and Tier 3 fees not yet confirmed stay off screen (DEC-448); further checks can add them.",
      f"- The {sum(1 for t in rd('transfers.csv') if t['fee_status'].startswith('undisclosed')):,} undisclosed fees stay £0 (no figure reported); the on-screen note covers them.",
      "- CPI base: ONS D7BT August 2026; September 2026 is due on 21 Oct 2026 and would move the secondary statistic slightly if the build is re-run.",
      "- Luke's open question (report section 19): confirmed fees only on screen, every tier.", ""]
open(f"{D}/DESIGN_INPUTS.md", "w", encoding="utf-8").write("\n".join(L))
print("DESIGN_INPUTS.md:", len(cr) - 1, "leader changes;", len(spans), "close spans;", len(top), "clubs in the top 12")
