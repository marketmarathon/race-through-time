#!/usr/bin/env python3
"""RTT-101 (IQ-15): write reports/RTT-101_data_report.md from the built data (deterministic).
Usage: python3 scripts/rtt101_report.py [DATA_DIR] [REPORT_PATH]"""
import csv, json, os, sys
from collections import Counter, defaultdict

D = sys.argv[1] if len(sys.argv) > 1 else "data/rtt-101"
OUT = sys.argv[2] if len(sys.argv) > 2 else "reports/RTT-101_data_report.md"


def rd(n, base=D):
    p = os.path.join(base, n)
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def m(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    s = "−" if v < 0 else ""
    v = abs(v)
    return f"{s}£{v / 1e9:.2f}bn" if v >= 1e9 else f"{s}£{v / 1e6:.1f}m"


clubs = {c["club_id"]: c["display_name"] for c in rd("clubs.csv")}
T = rd("transfers.csv")
S = rd("series_monthly.csv")
E = rd("fee_evidence.csv")
C = rd("conflicts.csv")
COV = rd("coverage.csv")
WT = {w["window"]: w for w in rd("window_totals.csv")}
WL = rd("window_totals_leads.csv", os.path.join(D, "source"))
RC = rd("runner_checks.csv", os.path.join(D, "source"))
summ = json.load(open(os.path.join(D, "source", "build_summary.json")))
checks = summ["checks"]
by_month = defaultdict(list)
for r in S:
    if r["rank"]:
        by_month[r["month_end"]].append(r)
months = sorted(by_month)
L = []
w = L.append
w("# RTT-101 Premier League net transfer spend — data report, phase 1 (IQ-15, 7 Oct 2026)\n")
w("**Status: UNVERIFIED preview. Not for screen.** Only figures marked VERIFIED may ever be shown, and phase 2 (verification of Tier 1 at source, in batches) comes before any design work. Rules: `reference/metric_contract_RTT-101.md`; decisions DEC-235 to DEC-250 (and the findings recorded with this build).\n")
w("Rebuild: `python3 scripts/build_rtt101_dataset.py && python3 scripts/rtt101_report.py` (deterministic; the private cross-checks need the private folder: `python3 scripts/rtt101_private_crosschecks.py <private research folder>` first).\n")

w("## 1. What was built\n")
fee = [t for t in T if t["fee_gbp"] and float(t["fee_gbp"]) > 0]
w(f"- **{len(T):,} transfer events** that involve a club in the Premier League that season (1992-93 to the freeze, 1 Sep 2026), of which **{len(fee):,} carry a fee** above £0. The rest are loans without a fee ({sum(1 for t in T if t['fee_status'].startswith('loan')):,}), free transfers ({sum(1 for t in T if t['fee_status'] == 'free'):,}), undisclosed fees with no figure, counted £0 ({sum(1 for t in T if t['fee_status'].startswith('undisclosed')):,}), and fees not found ({sum(1 for t in T if t['fee_status'].startswith('NOT FOUND')):,}).")
st = Counter(t["status"] for t in fee)
gr = Counter(t["grade"] for t in fee)
w(f"- Fee status: **VERIFIED {st.get('VERIFIED', 0):,}**, UNVERIFIED {st.get('UNVERIFIED', 0):,}. Grade of the fee used: A {gr.get('A', 0):,}, B {gr.get('B', 0):,}, C (Wikipedia pointer only) {gr.get('C', 0):,}, D {gr.get('D', 0):,}.")
tc = Counter(t["tier"] for t in T)
w(f"- Tiers (DEC-248): Tier 1 **{tc.get('1', 0):,}**, Tier 2 {tc.get('2', 0):,}, Tier 3 {tc.get('3', 0):,} (5% sample: {sum(1 for t in T if t['tier3_sample'] == 'yes')}).")
tr = Counter()
for t in T:
    if t["tier"] == "1":
        for r in t["tier_reason"].split("; "):
            tr[r] += 1
w("  Tier 1 reasons (a transfer can have several): " + "; ".join(f"{k} {v:,}" for k, v in tr.most_common()) + ".")
w(f"- {len(E):,} evidence rows in `fee_evidence.csv`; {len(rd('sources.csv')):,} sources in `sources.csv`; {summ['n_conflicts']:,} transfers with more than one fee version (`conflicts.csv`).")
if RC:
    rc = Counter(r["result"][:13] for r in RC)
    w(f"- **Scripted source check** (GitHub runner, {len(RC):,} cited pages): VERIFIED {rc.get('VERIFIED', 0):,}; page fetched but figure not found near the player's name {rc.get('NOT CONFIRMED', 0):,}; blocked or gone {sum(v for k, v in rc.items() if k.startswith('BLOCKED'))}.")
    t2 = [t for t in T if t["tier"] == "2"]
    w(f"  Tier 2 result: {sum(1 for t in t2 if t['status'] == 'VERIFIED')} of {len(t2)} Tier 2 fees VERIFIED by the scripted check.")
    t3 = [t for t in T if t["tier3_sample"] == "yes"]
    w(f"  Tier 3 sample: {sum(1 for t in t3 if t['status'] == 'VERIFIED')} of {len(t3)} VERIFIED; most Tier 3 rows have no fetchable citation (error rate cannot be published yet: phase 2).")
w("")

w("## 2. Checks\n")
w("| Check | Result | Detail |\n|---|---|---|")
for n, r, d in checks:
    w(f"| {n} | **{r}** | {d} |")
w("\nPlus the private cross-checks in `data/rtt-101/CHECKS.md` (membership equals research file part03b; its differences are the two known flag errors and points deductions it ignores).\n")

w("## 3. Leaders over time (UNVERIFIED preview)\n")
w("First place at each month end, nominal cumulative net spend; a change is listed when first place changes hands.\n")
w("| From month end | Leader | Value then |\n|---|---|---|")
prev = None
for me in months:
    top = min(by_month[me], key=lambda r: int(r["rank"]))
    if top["club_id"] != prev:
        w(f"| {me} | {clubs[top['club_id']]} | {m(top['cum_net_gbp'])} |")
        prev = top["club_id"]
w("")
w("## 4. Top 12 at key dates (UNVERIFIED preview)\n")
keys = ["1993-05-31", "1997-05-31", "2002-05-31", "2005-05-31", "2008-08-31", "2012-05-31", "2016-08-31", "2020-10-31", "2023-09-30", "2026-09-01"]
for me in keys:
    rows = sorted(by_month.get(me, []), key=lambda r: int(r["rank"]))[:12]
    w(f"**{me}:** " + "; ".join(f"{r['rank']}. {clubs[r['club_id']]} {m(r['cum_net_gbp'])}{'' if r['in_pl'] == 'yes' else ' (out of the PL)'}" for r in rows) + "\n")

w("## 5. Coverage by era\n")
era = defaultdict(Counter)
for c in COV:
    for k in ("transfers_found", "fee_bearing", "fee_grade_A_or_B", "fee_verified", "fee_unverified", "undisclosed_no_figure", "fee_not_found"):
        era[c["era"]][k] += int(c[k])
w("Counts are club-sides (a PL-to-PL deal counts once for each club).\n")
w("| Era | Transfers found | With a fee | Fee grade A/B | Fee VERIFIED | Undisclosed, no figure | Fee not found |\n|---|---|---|---|---|---|---|")
for e in sorted(era):
    c = era[e]
    w(f"| {e} | {c['transfers_found']:,} | {c['fee_bearing']:,} | {c['fee_grade_A_or_B']:,} | {c['fee_verified']:,} | {c['undisclosed_no_figure']:,} | {c['fee_not_found']:,} |")
w("""
What the eras mean:
- **1992–2002:** no Wikipedia window lists exist (V-10). The finding list is the clubs' season pages (200 of 210 fetched; the ten Leeds United pages are titled "Leeds United A.F.C." and were not fetched in this round) plus the research leads. About a quarter of those pages have no transfer table at all, so this era is the least complete. Transfermarkt was not used (route A says to consult it only to spot omissions; nothing from it is stored).
- **2002–2007:** the early Wikipedia window lists are short (for example summer 2004 has 83 rows involving these clubs, summer 2005 has 76), so many smaller deals are missing.
- **From 2007:** the lists are full (500–800 rows a window), but most fees there are Wikipedia figures (grade C pointers) until the cited source is checked.
""")

w("## 6. Biggest open conflicts\n")
w("Transfers whose sources give different fees (never averaged; the canonical fee is the highest grade, then the earliest report). The ones marked for Luke are Tier 1 with a same-grade gap over 10% and £1m (brief §7).\n")
w("| Player | From → To | Date | Fee used | Range | Tier | For Luke |\n|---|---|---|---|---|---|---|")
for c in C[:25]:
    w(f"| {c['player']} | {clubs.get(c['from_club'], c['from_club'])} → {clubs.get(c['to_club'], c['to_club'])} | {c['date']} | {m(c['canonical_gbp'])} ({c['canonical_grade']}) | {m(c['min_gbp'])}–{m(c['max_gbp'])} | {c['tier']} | {c['for_luke']} |")
w(f"\n{sum(1 for c in C if c['for_luke'])} conflicts are for Luke in total (`conflicts.csv`, column `for_luke`).\n")

w("## 7. League-wide window totals: our sums against published totals\n")
w("Our sums are **fees only, Premier League clubs only, from this preview** (gross = fees paid by PL clubs; net = fees paid to non-PL clubs minus fees received from them). Published totals are research leads (UNVERIFIED). The Premier League's own figures (grade A) are the best comparison; the press figures are mostly Deloitte estimates. **Gaps are expected and are not forced to match.**\n")
w("| Window | Our gross | Our net | Premier League gross (A) | PL net (A) | Press gross / net (B, first listed) |\n|---|---|---|---|---|---|")
lead_by = defaultdict(list)
for r in WL:
    lead_by[r["window"]].append(r)


def wkey(x):
    a, y = x.split()
    return (int(y), 0 if a == "January" else 1)


for win in sorted(lead_by, key=wkey):
    o = WT.get(win, {})
    a = next((r for r in lead_by[win] if r["grade"] == "A"), None)
    b = next((r for r in lead_by[win] if r["grade"] == "B"), None)
    w(f"| {win} | {m(o.get('gross_spend_gbp'))} | {m(o.get('net_spend_gbp'))} | {m(a['gross_gbp']) if a else '—'} | {m(a['net_gbp']) if a else '—'} | "
      f"{(b['gross_as_reported'][:30] + ' / ' + b['net_as_reported'][:30] + ' (' + b['publisher'][:20] + ')') if b else '—'} |")
w("""
Why the totals differ:
1. **Undisclosed fees count £0 here** (DEC-237 (g)); publishers estimate them. This is the biggest reason our gross is lower, especially in January windows and before 2010.
2. **Wikipedia's early lists are incomplete** (2002–2007), so whole deals are missing there.
3. **Add-ons, instalments and loan fees:** publishers often include "up to" totals or add-ons; we count only the guaranteed fee until add-ons are reported payable (DEC-237 (e)).
4. **Window boundaries:** we group by transfer date (April–October = summer, November–March = January); publishers use the window's legal dates and sometimes include deals agreed before the window.
5. **"Net" is measured differently:** the Premier League's net is spend minus receipts from clubs outside the PL; Deloitte's and the press's definitions vary (one source's "net £40m profit" for January 2017 against the League's −£4.0m).
""")

w("## 8. Blocked or missing sources\n")
w("""- **Wikipedia** rate-limits the Claude Code container (HTTP 429), so every page was fetched on a GitHub runner (`rtt101_sources.yml`; no secrets, no artifacts; each page's revision ID is in `source/wiki_pages.csv`).
- **ONS, Bank of England, ECB, BBC, Sky, the Guardian and Transfermarkt** are blocked from the container; the reference data and the scripted check ran on the runner.
- **1991–92 last First Division matchday** (it sets the start of 1992–93's attribution window): Wikipedia's First Division page gives no end date; 2 May 1992 is a research lead, UNVERIFIED (`source/fixed_dates.csv`). It only matters for transfers between early May and mid-August 1992.
- **Leeds United 1992–2002 club-season pages:** not fetched in this round (wrong page title); next runner job.
- **Pages the scripted check could not read** (paywalls, dead links, robots) are listed in `source/runner_checks.csv` with their HTTP status; Claude in Cowork can open many of them in Luke's Chrome in phase 2.
- **Transfermarkt:** not used, not fetched, nothing stored (DEC-236). Phase 2 can use it in Luke's browser only to spot omissions, per route A.
""")
open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("report written:", OUT, len(L), "lines")

Q = []
q = Q.append
nl = sum(1 for c in C if c["for_luke"])
q(f"**Tier 1 is too big as worded (DEC-253).** {tc.get('1', 0):,} transfers are Tier 1, mostly because of the \"changes the top-12 order\" test. "
  "*Recommendation:* keep £20m+, records and disputed fees, and narrow the order test to \"changes the leader, or who is in the top 12, at any month end\"; the rest get Tier 2's scripted check.")
q("**Undisclosed fees count £0 (DEC-237 (g)).** " + f"{sum(1 for t in T if t['fee_status'].startswith('undisclosed')):,} transfers have no reported figure. "
  "*Recommendation:* keep the rule, say on screen \"Undisclosed fees not included\", and give each club's undisclosed count in the description.")
q("**The early years are the least complete (1992–2007).** *Recommendation:* in phase 2, Claude in Cowork uses Transfermarkt in your Chrome only as a finding list (route A, nothing stored) to spot missing 1992–2007 deals involving the bigger fees, and takes each fee from a press or club source.")
q("**Relegated clubs keep their frozen bar and their rank** (contract §1; e.g. a relegated club can sit 8th at the freeze). *Recommendation:* keep them in the ranking; how a frozen bar looks is a design question for the pilot (DEC-069).")
q("**Start of the race.** At 31 May 1992 every bar is £0 (the leader that month is only a tie-break). *Recommendation:* the film starts at the first month end with a fee (July 1992); the data stay as they are.")
q(f"**Same-grade fee disagreements on Tier 1 transfers:** {nl} are listed in `conflicts.csv` (column `for_luke`). *Recommendation:* phase 2 settles each at source; the ones still open after that come back to you as a short list.")
q("**Claude's working choices** DEC-247 (finding list), DEC-248 (tiers), DEC-249 (board size later), DEC-250 (build details) and DEC-254 (how the scripted check marks a fee VERIFIED, and publisher grades). *Recommendation:* confirm them.")
q("**Phase 2 first batch.** *Recommendation:* verify the Tier 1 fees of the clubs that lead or reach the top 3 (Chelsea, Manchester United, Manchester City, Arsenal, Liverpool, Newcastle, Blackburn, Everton) first, in batches of 50 (`tier1_list.csv`, column `batch`).")
with open(OUT, "a", encoding="utf-8") as f:
    f.write("\n## 9. Questions for Luke (each with Claude's recommendation)\n\n")
    for i, s in enumerate(Q, 1):
        f.write(f"{i}. {s}\n")

# ---------------------------------------------------------------- phase 2 (IQ-15b)
RV = rd("review_decisions.csv", os.path.join(D, "source"))
RF = rd("reported_fees.csv", os.path.join(D, "source"))
UL = rd("unmatched_leads.csv")
P2 = []
p = P2.append
fee_t = [t for t in T if t["fee_gbp"] and float(t["fee_gbp"]) > 0]
t1 = [t for t in fee_t if t["tier"] == "1"]
p("\n## 10. Phase 2 (IQ-15b): verification at source\n")
p(f"- **Tier 1 (DEC-256):** {len(t1):,} fee-bearing Tier 1 transfers; **{sum(1 for t in t1 if t['status'] == 'VERIFIED'):,} VERIFIED at source**, "
  f"each quote read by Claude ({sum(1 for r in RV if r['decision'] == 'accept'):,} quotes accepted, {sum(1 for r in RV if r['decision'] == 'reject')} rejected; "
  "`source/review_decisions.csv`). The rest have no page that states the figure next to the player's name yet (mostly 1990s–2000s deals whose only "
  "sources are Wikipedia figures or dead links).")
p(f"- **Tier 2:** {sum(1 for t in fee_t if t['tier'] == '2' and t['status'] == 'VERIFIED'):,} of {sum(1 for t in fee_t if t['tier'] == '2'):,} VERIFIED by the scripted check. "
  f"**Tier 3 sample:** {sum(1 for t in T if t['tier3_sample'] == 'yes' and t['status'] == 'VERIFIED')} of {sum(1 for t in T if t['tier3_sample'] == 'yes')} VERIFIED.")
p(f"- **Undisclosed fees (DEC-257):** {len(RF)} grade A/B reported figures found at the cited source and read by Claude, used and flagged \"reported\" "
  "(`source/reported_fees.csv`); every other candidate figure on those pages belonged to another deal, a wage, an offer or a fine.")
gap = [t for t in T if t["found_via"].startswith("ChatGPT gap list")]
p(f"- **1992–2007 gap list (DEC-264), section A (1992–97):** {len(gap)} new moves added, {sum(1 for t in gap if t['status'] == 'VERIFIED')} VERIFIED "
  "(the page names the player, both clubs and the fee); the rest matched transfers already in the build. "
  f"{sum(1 for u in UL if u['section'] == 'G')} gap rows have no transfer date (retrospective articles only) and are listed in `unmatched_leads.csv`.")
p("- **Leeds United 1992–2002** pages added; **last 1991–92 First Division matchday 2 May 1992** confirmed by eight club fixture lists (pointers, grade C).")
p("- **Root causes found by reading the batches, and fixed in the build** (each fix applies to every row, not only the one seen): player names inside "
  "Wikipedia sort templates; the same deal listed twice; research leads matched on surname only (Kylian Hazard had been given Eden Hazard's fee); "
  "club-season tables whose direction was read from prose, plus a Wikipedia table labelled \"From\" in an \"Out\" section (Newcastle 1998–99); "
  "figures that are maxima, offers, valuations, instalments, combined fees or totals including add-ons; a regression that had dropped "
  "pre-2002 research-lead transfers (restored).")
open_c = [c for c in C if c["for_luke"]]
p(f"\n### Same-grade fee conflicts still open (DEC-261): {len(open_c)}\n")
p("Settled at source = the fee used is confirmed at source and no differing same-grade figure is (totals including add-ons are not rivals). "
  "Still open = two same-grade sources confirm different figures, or the fee used is not yet confirmed.\n")
p("| Player | From → To | Date | Fee used | Other confirmed figure(s) | Why open |\n|---|---|---|---|---|---|")
for c in open_c:
    others = sorted({v.split(" (")[0] for v in c["versions_detail"].split(" | ") if " V " in v and not v.startswith("C ")})
    p(f"| {c['player']} | {clubs.get(c['from_club'], c['from_club'])} → {clubs.get(c['to_club'], c['to_club'])} | {c['date']} | "
      f"{m(c['canonical_gbp'])} ({c['canonical_grade']}) | {'; '.join(o[:60] for o in others[:3])} | {c['settled_at_source'][4:]} |")
with open(OUT, "a", encoding="utf-8") as f:
    f.write("\n".join(P2) + "\n")
