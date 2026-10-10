#!/usr/bin/env python3
"""RTT-101 (IQ-15): write reports/RTT-101_data_report.md from the built data (deterministic).
Usage: python3 scripts/rtt101_report.py [DATA_DIR] [REPORT_PATH]"""
import csv, json, os, re, sys, urllib.parse
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
RF = [r for r in rd("reported_fees.csv", os.path.join(D, "source")) if not r["candidate_id"].startswith("G-")]  # G- rows: guaranteed part of a total
UL = rd("unmatched_leads.csv")
P2 = []
p = P2.append
fee_t = [t for t in T if t["fee_gbp"] and float(t["fee_gbp"]) > 0]
t1 = [t for t in fee_t if t["tier"] == "1"]
p("\n## 10. Phase 2 (IQ-15b): verification at source\n")
v1 = [t for t in t1 if t["status"] == "VERIFIED"]
p(f"- **Tier 1 (DEC-256):** {len(t1):,} fee-bearing Tier 1 transfers; **{len(v1):,} VERIFIED at source** "
  f"({sum(1 for t in v1 if t['grade'] in ('A', 'B')):,} by a club, league or press source, grade A/B; {sum(1 for t in v1 if t['grade'] == 'C'):,} only by a "
  f"database such as Soccerbase, grade C; {sum(1 for t in v1 if t['grade'] == 'D'):,} only by a grade D site), "
  f"each quote read by Claude ({sum(1 for r in RV if r['decision'] == 'accept'):,} quotes accepted, {sum(1 for r in RV if r['decision'] == 'reject')} rejected; "
  "`source/review_decisions.csv`). The rest have no page that states the figure next to the player's name yet (mostly 1990s–2000s deals whose only "
  "sources are Wikipedia figures or dead links).")
p(f"- **Tier 2:** {sum(1 for t in fee_t if t['tier'] == '2' and t['status'] == 'VERIFIED'):,} of {sum(1 for t in fee_t if t['tier'] == '2'):,} VERIFIED by the scripted check. "
  f"**Tier 3 sample:** {sum(1 for t in T if t['tier3_sample'] == 'yes' and t['status'] == 'VERIFIED')} of {sum(1 for t in T if t['tier3_sample'] == 'yes')} VERIFIED.")
p(f"- **Undisclosed fees (DEC-257):** {sum(1 for r in RF if r['decision'] == 'accept')} grade A/B reported figures found at the cited source and read by Claude, "
  f"used and flagged \"reported\" ({len({r.get('transfer_id') or r['candidate_id'] for r in RF if r['decision'] == 'accept'})} transfers; "
  f"{sum(1 for r in RF if r['decision'] != 'accept')} close candidates rejected on reading: another deal, grade D, not a fee, or a total with add-ons; "
  "`source/reported_fees.csv`); every other candidate figure on those pages belonged to another deal, a wage, an offer or a fine.")
gap = [t for t in T if t["found_via"].startswith("ChatGPT gap list")]
p(f"- **1992–2007 gap list (DEC-264), sections A v2, B and C (1992–2007):** {len(gap)} new moves added, {sum(1 for t in gap if t['status'] == 'VERIFIED')} VERIFIED "
  "(the page names the player, both clubs and the fee); the rest matched transfers already in the build. "
  f"{sum(1 for u in UL if u['section'] == 'G')} gap rows have no transfer date (retrospective articles only) and are listed in `unmatched_leads.csv`.")
p("- **Leeds United 1992–2002** pages added; **last 1991–92 First Division matchday 2 May 1992** confirmed by eight club fixture lists (pointers, grade C).")
p("- **Root causes found by reading the batches, and fixed in the build** (each fix applies to every row, not only the one seen): player names inside "
  "Wikipedia sort templates; the same deal listed twice; research leads matched on surname only (Kylian Hazard had been given Eden Hazard's fee); "
  "club-season tables whose direction was read from prose, plus a Wikipedia table labelled \"From\" in an \"Out\" section (Newcastle 1998–99); "
  "figures that are maxima, offers, valuations, instalments, combined fees or totals including add-ons; a regression that had dropped "
  "pre-2002 research-lead transfers (restored); accented names not matched (ø, æ, ß and others); Soccerbase \"Totals\" lines and other rows of a "
  "career table read as this deal's fee (a Soccerbase figure now counts only from the row whose joining date is the transfer's); the same deal "
  "reported at two stages with a non-PL club not merged (Yobo, Baros); a reported figure attached to the same player's other moves.")
open_c = [c for c in C if c["for_luke"]]
p(f"\n### Same-grade fee conflicts not settled at source (DEC-261): {len(open_c)}, each settled by the contract's rule (DEC-277)\n")
p("Settled at source = the fee used is confirmed at source and no differing same-grade figure is (totals including add-ons are not rivals). "
  "The deals below were not; Luke decided (DEC-277) that the existing rule settles them: best grade first, then the earliest report (a contemporary "
  "sterling figure from a grade A/B source preferred, contract §5). The last column says which step decided. Where no figure is confirmed at source yet, "
  "the fee stays UNVERIFIED (not on screen) and the deal is in the next research round.\n")
p("| Player | From → To | Date | Fee used | Other confirmed figure(s) | Why not settled at source | Result under the rule (DEC-277) |\n|---|---|---|---|---|---|---|")
for c in open_c:
    others = sorted({v.split(" (")[0] for v in c["versions_detail"].split(" | ") if " V " in v and not v.startswith("C ")})
    p(f"| {c['player']} | {clubs.get(c['from_club'], c['from_club'])} → {clubs.get(c['to_club'], c['to_club'])} | {c['date']} | "
      f"{m(c['canonical_gbp'])} ({c['canonical_grade']}) | {'; '.join(o[:60] for o in others[:3])} | {c['settled_at_source'][4:]} | {c['rule_result']} |")
with open(OUT, "a", encoding="utf-8") as f:
    f.write("\n".join(P2) + "\n")

# ---------------------------------------------------------------- effect of the gap list (DEC-264) on 1997-2007 window totals
BEF = {w["window"]: w for w in rd("window_totals_before_gap_list_v2.csv", os.path.join(D, "source"))}
G = []
g = G.append
g("\n### Effect of the 1992–2007 gap list (sections A v2, B, C) on window totals, 1997–2007\n")
g("Our sums count fees paid by PL clubs (gross) and fees paid to minus received from non-PL clubs (net); undisclosed fees count £0. "
  "\"Before\" = the build just before sections A v2, B and C were added (`source/window_totals_before_gap_list_v2.csv`). Published totals are research leads "
  "(part17b, UNVERIFIED); none exist for windows before summer 2002 (no window system).\n")
g("\"Change\" also includes the corrections made by reading the sources since that snapshot (for example a maximum replaced by the guaranteed fee); "
  "\"of which gap list\" is the gross paid by PL clubs in all moves the gap list created (section A's first version, part18b, was already in the "
  "snapshot, so this column can exceed the change).\n")
g("| Window | Gross before | Gross after | Change | of which gap list | Published gross (first A/B source) | Gap left | Net before | Net after |\n|---|---|---|---|---|---|---|---|---|")
gap_ids = {t["transfer_id"] for t in T if t["found_via"].startswith("ChatGPT gap list")}
gap_win = {}
for r in rd("club_ledger.csv"):
    if r["transfer_id"] in gap_ids and r["side"] == "buyer" and r["counted"] == "yes" and r["net_gbp"]:
        mo, yr = int(r["date"][5:7]), int(r["date"][:4])
        w = f"summer {yr}" if 4 <= mo <= 10 else (f"January {yr}" if mo <= 3 else f"January {yr + 1}")
        gap_win[w] = gap_win.get(w, 0.0) + float(r["net_gbp"])
tot_b = tot_a = tot_g = 0.0
for win in sorted(set(WT) | set(BEF), key=wkey):
    y = int(win.split()[1])
    if not (1997 <= y <= 2007):
        continue
    b, a = BEF.get(win, {}), WT.get(win, {})
    gb, ga = float(b.get("gross_spend_gbp") or 0), float(a.get("gross_spend_gbp") or 0)
    tot_b += gb; tot_a += ga; tot_g += gap_win.get(win, 0.0)
    pub = next((r for r in sorted(lead_by.get(win, []), key=lambda r: r["grade"]) if r["gross_gbp"]), None)
    gap_left = (m(float(pub["gross_gbp"]) - ga) if pub else "—")
    g(f"| {win} | {m(gb)} | {m(ga)} | {m(ga - gb)} | {m(gap_win.get(win, 0.0))} | {(m(pub['gross_gbp']) + ' (' + pub['grade'] + ', ' + pub['publisher'][:22] + ')') if pub else '—'} | {gap_left} | "
      f"{m(b.get('net_spend_gbp'))} | {m(a.get('net_spend_gbp'))} |")
g(f"\nTotal gross 1997–2007: {m(tot_b)} before, {m(tot_a)} after ({m(tot_a - tot_b)} net change, of which {m(tot_g)} paid in moves the gap list added). "
  "Where a published total exists, our sum stays below it mainly because undisclosed fees count £0 and the early Wikipedia window lists are short; "
  "the gap list narrows the gap but does not close it, and no figure is forced to match.")
with open(OUT, "a", encoding="utf-8") as f:
    f.write("\n".join(G) + "\n")

# ---------------------------------------------------------------- list for the next research round (no fees from Transfermarkt; derived data only)
need = [t for t in T if t["tier"] == "1" and t["fee_gbp"] and float(t["fee_gbp"]) > 0
        and not (t["status"] == "VERIFIED" and t["grade"] in ("A", "B"))]
need.sort(key=lambda t: (t["date"], t["player"]))
with open(os.path.join(D, "tier1_needs_press_source.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["transfer_id", "player", "from_club", "to_club", "date", "season", "fee_gbp_used", "grade_used", "status", "found_via"])
    for t in need:
        w.writerow([t["transfer_id"], t["player"], t["from_club"], t["to_club"], t["date"], t["season_attributed"], t["fee_gbp"], t["grade"],
                    t["status"], t["found_via"]])
print("tier1_needs_press_source.csv:", len(need), "Tier 1 transfers without a VERIFIED grade A/B figure")

# ---------------------------------------------------------------- phase 2: leader sequence and questions for Luke
SM = rd("series_monthly.csv")
by_m = defaultdict(dict)
for r in SM:
    if r["rank"]:
        by_m[r["month_end"]][r["club_id"]] = int(r["rank"])
lead_seq, prev = [], None
for mo in sorted(by_m):
    ldr = min(by_m[mo], key=lambda c: by_m[mo][c])
    if ldr != prev:
        lead_seq.append((mo, ldr))
        prev = ldr
NAME = {r["club_id"]: r["display_name"] for r in rd("clubs.csv")}
SRC_URL = {r["source_id"]: r["url"] for r in rd("sources.csv")}
TI = {t["transfer_id"]: t for t in T}
zero_rej = [r for r in RV if r["scope"] == "amount" and any(w in r["note"] for w in ("add-on", "maximum", "up to", "inclusive", "exact", "includes", "excess", "plus"))
            and r["transfer_id"] in {t["transfer_id"] for t in T if not (t["fee_gbp"] and float(t["fee_gbp"]) > 0)}]
Q2 = [
    f"**Database-only Tier 1 figures.** {sum(1 for t in v1 if t['grade'] == 'C'):,} Tier 1 fees are confirmed only by a grade C source "
    f"({sum(1 for t in v1 if t['grade'] == 'C' and 'soccerbase.com' in SRC_URL.get(t['canonical_source_id'], '')):,} of them a Soccerbase row for that move) "
    f"and {sum(1 for t in v1 if t['grade'] == 'D'):,} only by a source graded D (mostly later retrospective articles). May a Soccerbase row count as VERIFIED for screen? "
    "*Recommendation:* yes for Soccerbase rows (they are dated career tables, checked row by row), no for grade D; keep looking for press sources for both.",
    f"**Next research round.** {len(need):,} Tier 1 fees still have no VERIFIED club, league or press source (`data/rtt-101/tier1_needs_press_source.csv`, "
    "mostly 1992–2007). *Recommendation:* one more ChatGPT deep-research round on that list (a press or club URL and a short quote per deal, leads only; "
    "every figure checked at source here), starting with 1992–2002.",
    f"**Fees known only as a maximum or an approximation.** {len({r['transfer_id'] for r in zero_rej})} deals count £0 because every figure found is a "
    "maximum, a total including add-ons, or an approximation (\"just under £30m\", \"in excess of £13m\", \"£40m-plus\"). *Recommendation:* keep £0 "
    "(DEC-237 (e)) and add these deals to the next research round to find the guaranteed fee.",
    f"**Same-grade conflicts.** {len(open_c)} remain (table above). *Recommendation:* use the rule already in the contract (highest grade, then the earliest "
    "contemporary report) for all of them, and list them in the description notes; Luke can overrule any single deal.",
]
P3 = ["\n### Leader sequence after phase 2\n",
      "Leader at each change (month end): " + "; ".join(f"{mo[:7]} {NAME.get(c, c)}" for mo, c in lead_seq) + ".\n",
      "\n### Phase 2 questions — answered by Luke (YES to all four, 7 Oct 2026: DEC-274 to DEC-277)\n"]
P3 += [f"{i}. {q}" for i, q in enumerate(Q2, 1)]
P3 += ["\n**Luke's answers:** (1) a Soccerbase row counts as VERIFIED, grade C, labelled \"database source\" (`transfers.csv` column `verified_by`); "
       "other grade C and grade D sources do not confirm a fee (DEC-274). (2) One more ChatGPT deep-research round on `tier1_needs_press_source.csv`, "
       "starting with 1992–2002; every figure is a lead to check at source here (DEC-275). (3) The deals known only as a maximum or an approximation stay "
       "at £0 and are listed in `data/rtt-101/tier1_max_or_approx_only.csv` for a later round (DEC-276). (4) The same-grade conflicts are settled by the "
       "rule, with the result for each in the table above (DEC-277)."]
# deals known only as a maximum or approximation (DEC-276)
EV = defaultdict(list)
for e in rd("fee_evidence.csv"):
    EV[e["transfer_id"]].append(e)
# plus the deal-structure rows that set a fee to £0 under DEC-276 (source rounds: Sereni, Windass, Magilton)
DS276 = {r["transfer_id"]: r for r in rd("deal_structure.csv", os.path.join(D, "source")) if "DEC-276" in r["rule"] and r["transfer_id"] in TI}
zt = sorted({r["transfer_id"] for r in zero_rej} | set(DS276), key=lambda k: (TI[k]["date"], k))
with open(os.path.join(D, "tier1_max_or_approx_only.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["transfer_id", "player", "from_club", "to_club", "date", "season", "figures_found", "wording_and_why_not_counted"])
    for k in zt:
        t = TI[k]
        figs = sorted({f"{e['fee_text']} ({e['grade']}, {e['url']})" for e in EV[k] if e["amount"]})
        why = sorted({r["note"] for r in zero_rej if r["transfer_id"] == k} | ({DS276[k]["fee_status"] + ": " + DS276[k]["note"]} if k in DS276 else set()))
        w.writerow([k, t["player"], t["from_club"], t["to_club"], t["date"], t["season_attributed"], " | ".join(figs), " | ".join(why)])
print("tier1_max_or_approx_only.csv:", len(zt), "deals")
with open(OUT, "a", encoding="utf-8") as f:
    f.write("\n".join(P3) + "\n")

# ---------------------------------------------------------------- source round 1 (DEC-275): list A, 1992-93 to 1996-97
BASE = rd("source_round1_baseline.csv", os.path.join(D, "source"))
if BASE:
    LA = [b for b in BASE if b["deal_id"].startswith("A")]
    DSR = {r["transfer_id"]: r for r in rd("deal_structure.csv", os.path.join(D, "source"))}
    rows11, chg, up, down = [], [], 0.0, 0.0
    for b in LA:
        t = TI.get(b["transfer_id"])
        if not t:
            continue
        f0, f1 = float(b["fee_gbp"] or 0), float(t["fee_gbp"] or 0)
        if abs(f1 - f0) >= 1 or b["date"] != t["date"]:
            chg.append((b, t, f0, f1))
            up += max(0.0, f1 - f0)
            down += max(0.0, f0 - f1)
    v0 = sum(1 for b in LA if b["status"] == "VERIFIED")
    v1 = sum(1 for b in LA if TI.get(b["transfer_id"], {}).get("status") == "VERIFIED")
    vb = sum(1 for b in LA if TI.get(b["transfer_id"], {}).get("status") == "VERIFIED" and TI[b["transfer_id"]]["grade"] in ("A", "B"))
    fees = [c for c in chg if abs(c[3] - c[2]) >= 1]
    R = ["\n## 11. Source round 1, list A: 1992–93 to 1996–97 (DEC-275, IQ-15d)\n",
         f"- **Deals:** 211 (A0001–A0211), mapped to our transfers by player and date (`source/source_round1_map.csv`). ChatGPT's answers (private part20b/d/f) "
         "were added as leads (`found_via` of each evidence row: \"ChatGPT source round 1 (DEC-264 route)\") and every cited page was read on the GitHub runner: the "
         "figure next to the player's name, and both clubs named on the page.",
         f"- **VERIFIED:** {v1} of the 211 deals now have a fee confirmed at source ({vb} by a club, league or press source; the rest by a Soccerbase row), "
         f"up from {v0} before this round.",
         f"- **Changed:** {len(fees)} fees changed (£{up / 1e6:.1f}m up, £{down / 1e6:.1f}m down; net {m(up - down)}) and "
         f"{sum(1 for c in chg if c[0]['date'] != c[1]['date'])} completion dates moved to the date a grade B report gives.",
         "- **Deal structures** (`source/deal_structure.csv`, one row per transfer with its source, quote and rule): a combined fee is booked once on one transfer "
         "of the pair and the partner counts £0 (no split invented); a part-exchange counts a player valuation on both sides only where a source states it, "
         "otherwise cash only; add-ons count only when reported as payable; a loan fee is a loan fee.\n",
         "| Deal | Player | Move | Date before → after | Fee before | Fee after | Why |", "|---|---|---|---|---|---|---|"]
    for b, t, f0, f1 in sorted(chg, key=lambda c: c[0]["deal_id"]):
        why = DSR[t["transfer_id"]]["rule"] if t["transfer_id"] in DSR else (
            f"higher grade or earlier report ({t['grade']}, {urllib.parse.urlparse(SRC_URL.get(t['canonical_source_id'], '')).netloc})" if abs(f1 - f0) >= 1 else "")
        R.append(f"| {b['deal_id']} | {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | "
                 f"{b['date']}{' → ' + t['date'] if b['date'] != t['date'] else ''} | £{f0:,.0f} | £{f1:,.0f} | {why[:120]} |")
    # smaller same-grade disagreements (below the 10% and £1m threshold of the conflict list): result under the rule (DEC-277)
    CF = {c["transfer_id"]: c for c in C}
    small = []

    def nodate(d):
        return "no date" if d == "9999" else d

    for b in LA:
        t = TI.get(b["transfer_id"])
        if not t or not t["fee_gbp"] or t["status"] != "VERIFIED" or t["transfer_id"] in DSR:
            continue  # deal-structure rows are explained in the table above
        can = next((e for e in EV[t["transfer_id"]] if e["canonical"] == "yes"), None)
        rv = {}
        for e in EV[t["transfer_id"]]:
            if (e["status"] == "VERIFIED" and e["grade"] == t["grade"] and e["gbp"] and abs(float(e["gbp"]) - float(t["fee_gbp"])) >= 1):
                k = round(float(e["gbp"]))
                rv[k] = min(rv.get(k, "9999"), e["published"] or "9999")
        if rv:
            small.append((b, t, sorted(rv.items()), (can or {}).get("published") or ""))
    R += [f"\n**Same-grade disagreements within list A** ({len(small)} deals; all below the 10% and £1m threshold of Luke's conflict list, so the rule settles "
          "them: best grade, then the earliest report, DEC-277; a report with no stated date ranks after a dated one):\n",
          "| Deal | Player | Fee used (report date) | Other confirmed figure(s), same grade (report date) |", "|---|---|---|---|"]
    for b, t, rv, pub in small:
        R.append(f"| {b['deal_id']} | {t['player']} | £{float(t['fee_gbp']):,.0f} ({t['grade']}, {pub or 'no date'}) | "
                 f"{', '.join(f'£{x:,.0f} ({nodate(d)})' for x, d in rv)} |")
    # window totals 1992-97
    WB = {w["window"]: w for w in rd("window_totals_before_source_round1.csv", os.path.join(D, "source"))}
    R += ["\n**League-wide spending by window, 1992–97** (before = commit 111a018; there are no published window totals for these years, "
          "when there were no transfer windows, so nothing to compare against):\n", "| Window | Gross before | Gross after | Change |", "|---|---|---|---|"]
    for win in sorted(set(WB) | set(WT), key=wkey):
        y = int(win.split()[1])
        if 1992 <= y <= 1997 and not (y == 1997 and win.startswith("summer")):
            a, b0 = float(WT.get(win, {}).get("gross_spend_gbp") or 0), float(WB.get(win, {}).get("gross_spend_gbp") or 0)
            R.append(f"| {win} | {m(b0)} | {m(a)} | {m(a - b0)} |")
    # leader and top 12
    TB = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_source_round1.csv", os.path.join(D, "source"))}
    now = defaultdict(list)
    for r in SM:
        if r["rank"] and int(r["rank"]) <= 12:
            now[r["month_end"]].append((int(r["rank"]), r["club_id"]))
    NOW = {mo: [c for _, c in sorted(v)] for mo, v in now.items()}
    lead_ch = [mo for mo in sorted(NOW) if TB.get(mo) and TB[mo][0] != NOW[mo][0]]
    set_ch = [mo for mo in sorted(NOW) if TB.get(mo) and set(TB[mo]) != set(NOW[mo])]
    ord_ch = [mo for mo in sorted(NOW) if TB.get(mo) and TB[mo] != NOW[mo]]
    R.append(f"\n**Effect on the race:** the leader changes at {len(lead_ch)} month ends"
             + (" (" + "; ".join(f"{mo[:7]}: {NAME.get(TB[mo][0], TB[mo][0])} → {NAME.get(NOW[mo][0], NOW[mo][0])}" for mo in lead_ch[:12]) + ")" if lead_ch else "")
             + f"; who is in the top 12 changes at {len(set_ch)} month ends"
             + (" (" + "; ".join(f"{mo[:7]}: in {', '.join(NAME.get(c, c) for c in sorted(set(NOW[mo]) - set(TB[mo])))}, out "
                                 f"{', '.join(NAME.get(c, c) for c in sorted(set(TB[mo]) - set(NOW[mo])))}" for mo in set_ch[:10]) + (" …" if len(set_ch) > 10 else "") + ")" if set_ch else "")
             + f"; the order within the top 12 changes at {len(ord_ch)} month ends.")
    R += ["\n**Questions for Luke on list A (each with Claude's recommendation)**\n",
          "1. **Combined fees.** One payment for two players (Charles and Tommy Johnson £2.9m; McKee and Whitworth £530,000; Billington and McKeever £500,000) "
          "is booked once, on one transfer of the pair, and the partner counts £0. Each club's total is exact and no split is invented. *Recommendation:* keep it.",
          "2. **Parker and Carr (Villa ↔ Leicester, Feb 1995).** The only source values \"the deal\" at £550,000 without saying how much was cash. We count £550,000 "
          "for Parker and £0 for Carr. *Recommendation:* keep it, and ask the next research round for the cash figure.",
          "3. **Andy Cole (Feb 1995).** A grade B source values Keith Gillespie at £1m in the deal, so under DEC-237 (d) Cole counts £7m (£6m cash plus Gillespie) and "
          "Gillespie £1m; Manchester United's net is still the £6m cash. *Recommendation:* keep it (it follows the rule Luke approved).",
          "\n**Answered by Luke (Cowork chat, 8 Oct 2026): yes to all three, kept as built (DEC-405, DEC-406, DEC-407).**"]
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 11:", v0, "->", v1, "VERIFIED;", len(fees), "fees changed;", len(lead_ch), "leader changes")

# ---------------------------------------------------------------- source round 1 (DEC-275): list B, 1997-98 to 2001-02 (IQ-15f), and DEC-404
BASEB = rd("source_round1_baseline_B.csv", os.path.join(D, "source"))
if BASEB:
    LB = [b for b in BASEB if b["deal_id"].startswith("B")]
    DSR = {r["transfer_id"]: r for r in rd("deal_structure.csv", os.path.join(D, "source"))}
    D404 = rd("dec404_changes.csv", os.path.join(D, "source"))
    d404 = {r["transfer_id"]: r for r in D404}
    chg, up, down = [], 0.0, 0.0
    for b in LB:
        t = TI.get(b["transfer_id"])
        if not t:
            continue
        f0, f1 = float(b["fee_gbp"] or 0), float(t["fee_gbp"] or 0)
        if abs(f1 - f0) >= 1 or b["date"] != t["date"]:
            chg.append((b, t, f0, f1))
            up += max(0.0, f1 - f0)
            down += max(0.0, f0 - f1)
    nB = len({b["transfer_id"] for b in LB})
    v0 = sum(1 for b in LB if b["status"] == "VERIFIED")
    v1 = sum(1 for b in LB if TI.get(b["transfer_id"], {}).get("status") == "VERIFIED")
    vb = sum(1 for b in LB if TI.get(b["transfer_id"], {}).get("status") == "VERIFIED" and TI[b["transfer_id"]]["grade"] in ("A", "B"))
    vz = sum(1 for b in LB if TI.get(b["transfer_id"], {}).get("status") != "VERIFIED" and not float(TI.get(b["transfer_id"], {}).get("fee_gbp") or 0))
    fees = [c for c in chg if abs(c[3] - c[2]) >= 1]

    REJ = defaultdict(list)
    for r in rd("review_decisions.csv", os.path.join(D, "source")):
        if r["batch"].startswith("SR1-B") and r["decision"] == "reject" and r["scope"] == "amount":
            REJ[r["transfer_id"]].append(f"£{float(r['amount']):,.0f} not counted: {r['note'].split('; weighed')[0]}")

    def why_of(t, f0, f1):
        k = t["transfer_id"]
        if k in REJ and not (k in DSR and DSR[k]["fee_amount"] != "") and k not in d404:
            return "; ".join(REJ[k])
        if k in DSR and DSR[k]["fee_amount"] != "":
            return DSR[k]["rule"]
        if k in d404:
            return "DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure"
        if abs(f1 - f0) < 1:
            return DSR[k]["rule"] if k in DSR else ""
        if t["fee_status"].startswith("undisclosed"):
            return "an A/B report calls the fee undisclosed or nominal: only an A/B figure counts (DEC-408 (a), DEC-237 (g))"
        return f"confirmed at source: higher grade or earlier report ({t['grade']}, {urllib.parse.urlparse(SRC_URL.get(t['canonical_source_id'], '')).netloc})"

    R = ["\n## 12. Source round 1, list B: 1997–98 to 2001–02 (DEC-275, IQ-15f), and the completion-report rule (DEC-404)\n",
         f"- **Deals:** 342 (B0001–B0342; {nB} of our transfers), mapped by player and date (`source/source_round1_map.csv`). ChatGPT's answers (private "
         "part21a–r, every SHA-256 matched its README) were added as leads (`found_via`: \"ChatGPT source round 1 (DEC-264 route)\") and every cited page was read "
         "on the GitHub runner: the figure next to the player's name, and both clubs named on the page. Wikipedia and Transfermarkt pages are never fee sources and "
         "were not fetched.",
         f"- **VERIFIED:** {v1} of the {nB} transfers now have a fee confirmed at source ({vb} by a club, league or press source; the rest by a Soccerbase row), "
         f"up from {v0} before this round. {vz} more count £0 (undisclosed, nominal, free, or known only as a maximum or approximation).",
         f"- **Changed:** {len(fees)} fees changed (£{up / 1e6:.1f}m up, £{down / 1e6:.1f}m down; net {m(up - down)}) and "
         f"{sum(1 for c in chg if c[0]['date'] != c[1]['date'])} completion dates moved to the date a grade B report gives (`source/deal_structure.csv` "
         "for the dates set by hand).\n",
         "| Deal | Player | Move | Date before → after | Fee before | Fee after | Why |", "|---|---|---|---|---|---|---|"]
    for b, t, f0, f1 in sorted(chg, key=lambda c: c[0]["deal_id"]):
        R.append(f"| {b['deal_id']} | {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | "
                 f"{b['date']}{' → ' + t['date'] if b['date'] != t['date'] else ''} | £{f0:,.0f} | £{f1:,.0f} | {why_of(t, f0, f1)[:140]} |")
    # deal structures applied in list B
    lbt = {b["transfer_id"] for b in LB}
    R += ["\n**Deal structures applied in list B** (one row each in `source/deal_structure.csv`, with source, quote and rule):\n",
          "| Player | Fee booked | Rule | Note |", "|---|---|---|---|"]
    for r in rd("deal_structure.csv", os.path.join(D, "source")):
        if r["lead_row"].startswith("part21") and r["fee_amount"] != "":
            R.append(f"| {r['player']} | £{float(r['fee_amount']):,.0f} | {r['rule']} | {r['note'][:160]} |")
    # DEC-404 effect everywhere
    from collections import Counter as _C
    cnt = _C(r["on_list"] for r in D404)
    R += [f"\n**DEC-404 (Luke, 8 Oct 2026): a report that the deal was completed beats earlier reports of bids, agreed fees or \"expected\" figures of the "
          f"same grade; the earliest report is used only when none says the deal was completed.** Applied to the whole build, it changes **{len(D404)} fees** "
          f"(`source/dec404_changes.csv`): {cnt.get('source round 1 list A', 0)} on list A, {sum(v for k, v in cnt.items() if 'phase 2' in k)} of the 32 "
          f"phase 2 same-grade conflicts, {cnt.get('source round 1 list B', 0)} on list B and {cnt.get('other', 0)} elsewhere. A completion word counts only "
          "next to the player's name; wording such as \"imminent\", \"subject to\" or \"proposed\" means not completed; a figure within 2% of the one already "
          "used (the same fee in another currency) changes nothing.\n",
          "| Date | Player | Move | Fee without DEC-404 | Fee with DEC-404 | On | Completion report |", "|---|---|---|---|---|---|---|"]
    for r in D404:
        R.append(f"| {r['date']} | {r['player']} | {clubs.get(r['from_club'], r['from_club'])} → {clubs.get(r['to_club'], r['to_club'])} | "
                 f"£{float(r['fee_without_dec404']):,.0f} | £{float(r['fee_with_dec404']):,.0f} | {r['on_list']} | {r['completion_report'][:90]} |")
    # same-grade conflicts within list B and the step that settled each
    small = []
    for b in LB:
        t = TI.get(b["transfer_id"])
        if not t or not t["fee_gbp"] or t["status"] != "VERIFIED" or (t["transfer_id"] in DSR and DSR[t["transfer_id"]]["fee_amount"] != ""):
            continue
        can = next((e for e in EV[t["transfer_id"]] if e["canonical"] == "yes"), None)
        rv = {}
        for e in EV[t["transfer_id"]]:
            if e["status"] == "VERIFIED" and e["grade"] == t["grade"] and e["gbp"] and abs(float(e["gbp"]) - float(t["fee_gbp"])) >= 1:
                k = round(float(e["gbp"]))
                rv[k] = min(rv.get(k, "9999"), e["published"] or "9999")
        if rv:
            if t["transfer_id"] in d404:
                step = "DEC-404 (completion report)"
            elif ((can or {}).get("published") or "9999") <= min(rv.values()):
                step = "earliest report (DEC-277), or the completion report when it is also the earliest"
            else:
                step = "sterling figure before a converted one (contract rule)"
            small.append((b, t, sorted(rv.items()), (can or {}).get("published") or "", step))
    R += [f"\n**Same-grade disagreements within list B** ({len(small)} deals) and the step that settled each:\n",
          "| Deal | Player | Fee used (grade, report date) | Other confirmed figure(s), same grade (report date) | Settled by |", "|---|---|---|---|---|"]
    for b, t, rv, pub, step in small:
        R.append(f"| {b['deal_id']} | {t['player']} | £{float(t['fee_gbp']):,.0f} ({t['grade']}, {pub or 'no date'}) | "
                 f"{', '.join(f'£{x:,.0f} ({nodate(d)})' for x, d in rv)} | {step} |")
    # window totals 1997-2002 against part17b
    WB = {w["window"]: w for w in rd("window_totals_before_source_round1_B.csv", os.path.join(D, "source"))}
    R += ["\n**League-wide spending by window, 1997–2002** (before = commit c62ca6b, the end of IQ-15e; published totals from part17b are research leads, "
          "UNVERIFIED; the list has no gross total for any of these windows, so there is nothing to compare against):\n", "| Window | Gross before | Gross after | Change | Published gross | Net before | Net after |",
          "|---|---|---|---|---|---|---|"]
    tb = ta = 0.0
    for win in sorted(set(WB) | set(WT), key=wkey):
        y = int(win.split()[1])
        if (1997 <= y <= 2002) and not (y == 1997 and win.startswith("January")):
            a, b0 = WT.get(win, {}), WB.get(win, {})
            ga, gb = float(a.get("gross_spend_gbp") or 0), float(b0.get("gross_spend_gbp") or 0)
            tb += gb; ta += ga
            pub = next((r for r in sorted(lead_by.get(win, []), key=lambda r: r["grade"]) if r["gross_gbp"]), None)
            R.append(f"| {win} | {m(gb)} | {m(ga)} | {m(ga - gb)} | {(m(pub['gross_gbp']) + ' (' + pub['grade'] + ')') if pub else '—'} | "
                     f"{m(b0.get('net_spend_gbp'))} | {m(a.get('net_spend_gbp'))} |")
    R.append(f"\nTotal gross summer 1997 to summer 2002: {m(tb)} before, {m(ta)} after ({m(ta - tb)}).")
    # leader and top 12 against the snapshot before list B
    TB = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_source_round1_B.csv", os.path.join(D, "source"))}
    now = defaultdict(list)
    for r in SM:
        if r["rank"] and int(r["rank"]) <= 12:
            now[r["month_end"]].append((int(r["rank"]), r["club_id"]))
    NOW = {mo: [c for _, c in sorted(v)] for mo, v in now.items()}
    lead_ch = [mo for mo in sorted(NOW) if TB.get(mo) and TB[mo][0] != NOW[mo][0]]
    set_ch = [mo for mo in sorted(NOW) if TB.get(mo) and set(TB[mo]) != set(NOW[mo])]
    ord_ch = [mo for mo in sorted(NOW) if TB.get(mo) and TB[mo] != NOW[mo]]
    R.append(f"\n**Effect on the race** (against the build at c62ca6b): the leader changes at {len(lead_ch)} month ends"
             + (" (" + "; ".join(f"{mo[:7]}: {NAME.get(TB[mo][0], TB[mo][0])} → {NAME.get(NOW[mo][0], NOW[mo][0])}" for mo in lead_ch[:16]) + (" …" if len(lead_ch) > 16 else "") + ")" if lead_ch else "")
             + f"; who is in the top 12 changes at {len(set_ch)} month ends"
             + (" (" + "; ".join(f"{mo[:7]}: in {', '.join(NAME.get(c, c) for c in sorted(set(NOW[mo]) - set(TB[mo])))}, out "
                                 f"{', '.join(NAME.get(c, c) for c in sorted(set(TB[mo]) - set(NOW[mo])))}" for mo in set_ch[:10]) + (" …" if len(set_ch) > 10 else "") + ")" if set_ch else "")
             + f"; the order within the top 12 changes at {len(ord_ch)} month ends.")
    R += ["\n**Luke's answers to the list A questions (report section 11; Cowork chat, 8 Oct 2026): yes to all three, kept as built.**\n",
          "- **DEC-405:** two players sold for one fee: the fee is booked once, on one transfer of the pair, and the partner counts £0; a split is never "
          "invented (Charles and Tommy Johnson £2.9m; McKee and Whitworth £530,000; Billington and McKeever £500,000). The same rule is applied in list B "
          "(Robinson and Coppinger £500,000; Zúñiga and Zevallos £800,000; the £500,000 cash in the Stuart, Tiler and Ward swap).",
          "- **DEC-406:** Parker and Carr (Aston Villa ↔ Leicester City, Feb 1995): £550,000 for Parker and £0 for Carr; the cash figure goes into the next research round.",
          "- **DEC-407:** Andy Cole (Feb 1995): Cole counts £7m (£6m cash plus Keith Gillespie, valued at £1m by a grade B source) and Gillespie £1m, under the "
          "approved swap rule; Manchester United's net spend still reflects the £6m cash."]
    QB = [l.strip() for l in open(os.path.join(D, "source", "questions_listB.md"), encoding="utf-8") if l.strip()] \
        if os.path.exists(os.path.join(D, "source", "questions_listB.md")) else []
    R += ["\n**Questions for Luke on list B (each with Claude's recommendation)**\n"] + QB
    R += ["\n**Answered by Luke (Cowork chat, 8 Oct 2026): yes to all seven, recommendations applied (DEC-410 to DEC-416).** Murphy now counts the £1.5m "
          "initial payment and Normann £0; the fees resting on a \"reported\"-type completion figure are listed in `source/dec404_soft_figures.csv` "
          "and go to research round 2. Detailed data and method questions are now decided by Claude within the agreed rules (DEC-417)."]
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 12:", v0, "->", v1, "VERIFIED of", nB, ";", len(fees), "fees changed;", len(D404), "DEC-404 changes;", len(lead_ch), "leader changes")


# ---------------------------------------------------------------- research round 2 list (IQ-15g, DEC-418)
R2 = rd("source_round2_list.csv")
if R2:
    from collections import Counter as _C2
    bys = _C2(r["season"] for r in R2)
    why = _C2(w for r in R2 for w in r["what_we_need"].split("; "))
    R = ["\n## 13. Research round 2: the list (IQ-15g, DEC-418)\n",
         f"`data/rtt-101/source_round2_list.csv` holds **{len(R2)} deals** (R0001 onwards, in date order, all seasons 1992–2026) that still need research; "
         "it carries no fee figures. Each deal maps to its transfer(s) in `data/rtt-101/source/source_round2_map.csv`. What each needs:\n"]
    R += [f"- {k}: {v}" for k, v in why.most_common()]
    R += ["\n| Season | Deals |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(bys.items())]
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 13:", len(R2), "round 2 deals")

# ---------------------------------------------------------------- source round 2 (IQ-15h): Claude helper research on the priority list
BASE2 = rd("source_round2_baseline.csv", os.path.join(D, "source"))
if BASE2:
    from collections import Counter as _C3
    LEADS = rd("leads_evidence.csv", os.path.join(D, "source"))
    researched = sorted({re.match(r"part2(?:2b|3g)-(R\d{4})-", l["lead_row"]).group(1) for l in LEADS
                         if re.match(r"part2(?:2b|3g)-(R\d{4})-", l["lead_row"])})
    rs = set(researched)
    B2 = [b for b in BASE2 if b["deal_id"] in rs]
    DSR = {r["transfer_id"]: r for r in rd("deal_structure.csv", os.path.join(D, "source"))}
    D404 = {r["transfer_id"]: r for r in rd("dec404_changes.csv", os.path.join(D, "source"))}
    REJ2 = defaultdict(list)
    for r in rd("review_decisions.csv", os.path.join(D, "source")):
        if r["batch"].startswith("SR2-") and r["decision"] == "reject" and r["scope"] == "amount":
            REJ2[r["transfer_id"]].append(f"£{float(r['amount']):,.0f} not counted: {r['note'].split('; weighed')[0]}")
    rev2 = [r for r in rd("review_decisions.csv", os.path.join(D, "source")) if r["batch"].startswith("SR2-")]
    tids = {b["transfer_id"] for b in B2}
    v0 = sum(1 for b in B2 if b["status"] == "VERIFIED")
    v1 = sum(1 for k in tids if TI.get(k, {}).get("status") == "VERIFIED")
    vab = sum(1 for k in tids if TI.get(k, {}).get("status") == "VERIFIED" and TI[k]["grade"] in ("A", "B"))
    chg, up, down = [], 0.0, 0.0
    for b in B2:
        t = TI.get(b["transfer_id"])
        if not t:
            continue
        f0, f1 = float(b["fee_gbp"] or 0), float(t["fee_gbp"] or 0)
        if abs(f1 - f0) >= 1 or b["date"] != t["date"]:
            chg.append((b, t, f0, f1)); up += max(0.0, f1 - f0); down += max(0.0, f0 - f1)
    fees = [c for c in chg if abs(c[3] - c[2]) >= 1]

    def why2(t, f0, f1):
        k = t["transfer_id"]
        if k in DSR and DSR[k]["fee_amount"] != "" and ("IQ-15h" in DSR[k]["rule"] or "DEC-417" in DSR[k]["rule"]):
            return DSR[k]["rule"]
        if k in REJ2:
            return "; ".join(REJ2[k])
        if k in D404:
            return "DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure"
        if abs(f1 - f0) < 1:
            return "completion date from the grade B report"
        if t["fee_status"].startswith("undisclosed"):
            return "every A/B source calls the fee undisclosed: counted £0 (DEC-237 (g), DEC-408 (a))"
        return f"confirmed at source ({t['grade']}, {urllib.parse.urlparse(SRC_URL.get(t['canonical_source_id'], '')).netloc})" if t["status"] == "VERIFIED" \
            else f"higher-ranked figure now on file (not yet confirmed at source; {t['grade']})"

    R = ["\n## 14. Source round 2: the priority deals (IQ-15h; DEC-419 to DEC-421)\n",
         f"- **Inputs:** ChatGPT instalment 1 (R0001–R0030, private part22b) and the Claude helper research on the 323 priority deals (part23g = part22c + "
         "part23a–f, 992 rows): every data file's SHA-256 matched `00_README.md` (the prompt and the helper instructions have no recorded hash). "
         f"Rows attached to their deals through `source/source_round2_map.csv`; **{len(rs)} deals researched**. Aggregator, scores and blog sites count as "
         "grade C whatever the file says; Ajax's acc-english pages were read at english.ajax.nl.",
         "- **Checked at source:** all 1,015 cited pages read on the runner "
         "(https://github.com/marketmarathon/race-through-time/actions/runs/37888858665): 886 loaded; 42 not found, 41 refused, 13 server errors (including "
         "West Ham's club pages), 15 timed out. A figure counts only when it sits next to the player's name and the page names both clubs, so a helper "
         "quote that the page does not carry is never used.",
         f"- **Quotes read:** {len(rev2)} newly confirmed quotes ({sum(1 for r in rev2 if r['decision'] == 'reject')} rejected: another deal's figure, a "
         "valuation or a garbled currency on the page, a maximum, a total with add-ons, a buy-back clause, a range, or a package including an unvalued player).",
         f"- **VERIFIED:** {v1} of the {len(tids)} researched transfers now have a fee confirmed at source ({vab} by a club, league or press source), "
         f"up from {v0} before this round.",
         f"- **Changed:** {len(fees)} fees changed (£{up / 1e6:.1f}m up, £{down / 1e6:.1f}m down; net {m(up - down)}) and "
         f"{sum(1 for c in chg if c[0]['date'] != c[1]['date'])} completion date(s) moved.\n",
         "| Deal | Player | Move | Date before → after | Fee before | Fee after | Why |", "|---|---|---|---|---|---|---|"]
    for b, t, f0, f1 in sorted(chg, key=lambda c: c[0]["deal_id"]):
        R.append(f"| {b['deal_id']} | {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | "
                 f"{b['date']}{' → ' + t['date'] if b['date'] != t['date'] else ''} | £{f0:,.0f} | £{f1:,.0f} | {why2(t, f0, f1)[:150]} |")
    R += ["\n**Deal structures applied in round 2** (`source/deal_structure.csv`):\n", "| Player | Fee booked | Rule | Note |", "|---|---|---|---|"]
    for r in rd("deal_structure.csv", os.path.join(D, "source")):
        if "IQ-15h" in r["rule"] or "IQ-15h" in r["note"]:
            R.append(f"| {r['player']} | {('£{:,.0f}'.format(float(r['fee_amount']))) if r['fee_amount'] != '' else 'date only: ' + r['date']} | "
                     f"{r['rule']} | {r['note'][:160]} |")
    # maximum/approximation-only deals (DEC-276) on the priority list
    z = [(b, TI[b["transfer_id"]]) for b in B2 if not float(b["fee_gbp"] or 0) and b["transfer_id"] in TI]
    R += [f"\n**Deals counted £0 because only a maximum or an approximation had been found (DEC-276): {len(z)} on the priority list.**\n",
          "| Deal | Player | Now | Status | Basis |", "|---|---|---|---|---|"]
    for b, t in sorted(z, key=lambda x: x[0]["deal_id"]):
        R.append(f"| {b['deal_id']} | {t['player']} | £{float(t['fee_gbp'] or 0):,.0f} | {t['status']} | {t['fee_status'][:110]} |")
    # windows
    WB = {w["window"]: w for w in rd("window_totals_before_source_round2.csv", os.path.join(D, "source"))}
    R += ["\n**League-wide spending by window** (before = commit 4b0f91c; windows that moved by £0.1m or more; published totals from part17b are "
          "research leads, UNVERIFIED):\n", "| Window | Gross before | Gross after | Change | Published gross | Net before | Net after |", "|---|---|---|---|---|---|---|"]
    tb = ta = 0.0
    for win in sorted(set(WB) | set(WT), key=wkey):
        a, b0 = WT.get(win, {}), WB.get(win, {})
        ga, gb = float(a.get("gross_spend_gbp") or 0), float(b0.get("gross_spend_gbp") or 0)
        tb += gb; ta += ga
        if abs(ga - gb) >= 1e5:
            pub = next((r for r in sorted(lead_by.get(win, []), key=lambda r: r["grade"]) if r["gross_gbp"]), None)
            R.append(f"| {win} | {m(gb)} | {m(ga)} | {m(ga - gb)} | {(m(pub['gross_gbp']) + ' (' + pub['grade'] + ')') if pub else '—'} | "
                     f"{m(b0.get('net_spend_gbp'))} | {m(a.get('net_spend_gbp'))} |")
    R.append(f"\nTotal gross, all windows: {m(tb)} before, {m(ta)} after ({m(ta - tb)}).")
    # leader and top 12
    TB = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_source_round2.csv", os.path.join(D, "source"))}
    now = defaultdict(list)
    for r in SM:
        if r["rank"] and int(r["rank"]) <= 12:
            now[r["month_end"]].append((int(r["rank"]), r["club_id"]))
    NOW = {mo: [c for _, c in sorted(v)] for mo, v in now.items()}
    lead_ch = [mo for mo in sorted(NOW) if TB.get(mo) and TB[mo][0] != NOW[mo][0]]
    set_ch = [mo for mo in sorted(NOW) if TB.get(mo) and set(TB[mo]) != set(NOW[mo])]
    R.append(f"\n**Effect on the race** (against the build at 4b0f91c): the leader changes at {len(lead_ch)} month ends"
             + (" (" + "; ".join(f"{mo[:7]}: {NAME.get(TB[mo][0], TB[mo][0])} → {NAME.get(NOW[mo][0], NOW[mo][0])}" for mo in lead_ch[:20]) + (" …" if len(lead_ch) > 20 else "") + ")" if lead_ch else "")
             + f"; who is in the top 12 changes at {len(set_ch)} month ends"
             + (" (" + "; ".join(f"{mo[:7]}: in {', '.join(NAME.get(c, c) for c in sorted(set(NOW[mo]) - set(TB[mo])))}, out "
                                 f"{', '.join(NAME.get(c, c) for c in sorted(set(TB[mo]) - set(NOW[mo])))}" for mo in set_ch[:12]) + (" …" if len(set_ch) > 12 else "") + ")" if set_ch else "")
             + ". " + "Final point: " + ", ".join(f"{NAME.get(c, c)} {m(next(float(r['cum_net_gbp']) for r in SM if r['month_end'] == max(NOW) and r['club_id'] == c))}" for c in NOW[max(NOW)][:3]) + ".")
    # still unverified among the researched deals
    unv = sorted((TI[k] for k in tids if TI.get(k, {}).get("status") != "VERIFIED" and float(TI[k]["fee_gbp"] or 0) > 0),
                 key=lambda t: -float(t["fee_gbp"]))
    R += [f"\n**Still UNVERIFIED among the researched deals: {len(unv)}** (their fee is a preview, not for screen; mostly pages the runner could not "
          "load or that do not name both clubs). The largest:\n", "| Player | Move | Date | Fee in use | Grade |", "|---|---|---|---|---|"]
    for t in unv[:25]:
        R.append(f"| {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | {t['date']} | £{float(t['fee_gbp']):,.0f} | {t['grade']} |")
    # order test on the unresearched deals
    OT = rd("round2_order_test.csv", os.path.join(D, "source"))
    yes = [r for r in OT if r["could_change"] == "yes"]
    R += [f"\n**Order test on the {len(OT)} round 2 deals not researched** (`source/round2_order_test.csv`; the Tier 1 test of DEC-256: does removing the fee, "
          f"or using another version of it, change the leader or who is in the top 12 at any month end?): **{len(yes)} could** "
          f"({sum(1 for r in yes if r['what_changes'] == 'leader')} the leader, the rest a top-12 place) and go to a later round; {len(OT) - len(yes)} could not. "
          "By season: " + ", ".join(f"{k} {v}" for k, v in sorted(_C3(r["season"] for r in yes).items())) + ".\n",
          "Deals that could change the leader:\n", "| Deal | Player | Date | Fee in use | First month end affected |", "|---|---|---|---|---|"]
    for r in sorted((r for r in yes if r["what_changes"] == "leader"), key=lambda r: r["date"]):
        R.append(f"| {r['deal_id']} | {r['player']} | {r['date']} | £{float(r['fee_gbp']):,.0f} | {r['first_month_end']} |")
    R += ["\n**Decided under DEC-417 (Claude, DEC-420; details in `state/DECISIONS.md`)**\n",
          "1. Aggregator, scores and blog sites count as grade C; agency copies and regional papers stay B as the helpers graded them.",
          "2. A rejected figure no longer blocks the same number in another currency (Curtis Jones's guaranteed €30m and Mayenda's €22m had been blocked by "
          "rejections of £30m and £22m totals).",
          "3. Earlier rejections re-weighed against the new leads: Bent, Gyan, Gordon and Brughmans still have only totals or bounds (£0 under DEC-276); "
          "Crouch 2009, Benítez, Ings, Mateus Fernandes and João Pedro to Chelsea keep their guaranteed figures; João Pedro to Brighton now counts the "
          "£30m 'understood' (a reported figure for an undisclosed fee).",
          "4. Guaranteed fee where the completion report gives it: Xhaka £25m initial (was £35m), Sané, Álvarez, Mané, Leon Bailey, Emiliano Martínez (£17m reported, not the £20m with add-ons), Arnautović, "
          "Matić 2017, Strand Larsen, Skipp, Semenyo 2023, Mamardashvili, Ugarte, Šeško, Núñez to Al Hilal, Thiaw, Negredo.",
          "5. Exchanges: Jeffrey counts the whole £60,000 deal with Roche valued at £25,000 (as for Cole, DEC-407); Pitcher counts £50,000 cash with Whyte "
          "and Mortimer at £0; Rutter (initial fee only as a range) and Brughmans (only 'up to') stay £0; Sereni stays £0 (Sky's pre-completion £4.5m against "
          "'exceeded the £4.57m'); Daley's date is the completion report's (31 May 1994).",
          "6. Mikel (2006): kept at £16m on the Manchester United → Chelsea move (£12m to United and £4m to Lyn, one payment for one registration); "
          "Chelsea's spend is exact and United's income is £4m too high until the build can book a payment to a third club.",
          "\n**For Luke (DEC-417 leaves this to him: it changes who leads)**\n",
          "1. **Nastasić (Fiorentina → Manchester City, Aug 2012).** The only figure found is \"£12m — including Stefan Savic as a makeweight\"; Savić is not "
          "valued and City called the fee undisclosed. Under the part-exchange rule the cash is unknown, so the build counts £0 for now, and that puts "
          "Chelsea ahead of Manchester City from September to December 2015 (by £3.5m). *Recommendation:* count the £12m package as Nastasić's fee with "
          "Savić at £0, the closest figure to what City paid (it overstates City's outlay by Savić's unknown value rather than understating it by the cash), "
          "and ask the next round for the cash part.",
          "\n**Answered by Luke (9 Oct 2026, DEC-423): count the £12m package as Nastasić's fee, Savić £0, until a contemporary cash figure is confirmed.**",
          "\n**Worth knowing:** from March to June 2003 Manchester United lead Newcastle United by about £10,000, so any small correction can swap them."]
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 14:", len(rs), "deals researched;", v0, "->", v1, "VERIFIED;", len(fees), "fees changed;", len(lead_ch), "leader changes;", len(yes), "order-test deals")

# ---------------------------------------------------------------- source round 3 (IQ-15i): undisclosed fees and the leader deals
BASE3 = rd("source_round3_baseline.csv", os.path.join(D, "source"))
if BASE3:
    from collections import Counter as _C4
    MAP3 = {r["deal_id"]: r for r in rd("source_round3_map.csv", os.path.join(D, "source"))}
    B3 = {r["deal_id"]: r for r in BASE3}
    LEADS3 = [l for l in rd("leads_evidence.csv", os.path.join(D, "source")) if l["lead_row"].startswith("part24")]
    names3 = {l["lead_row"].split("-")[1] for l in LEADS3}
    ever = {c["club_id"] for c in rd("clubs.csv")}

    def ptype(d):
        m_ = MAP3[d]; t = TI.get(m_["transfer_id"], {})
        if m_["pl_side"] == "buyer+seller":
            return "P1 both clubs in the PL"
        if m_["pl_side"] == "buyer":
            return "P2 PL purchase from an ever-PL club" if t.get("from_club") in ever else "P4 PL purchase from another club"
        return "P3/P5 PL sale"
    rev3 = [r for r in rd("review_decisions.csv", os.path.join(D, "source")) if r["batch"].startswith("SR3-")]
    U_all = list(MAP3)
    # every deal the four sweep files cover (with or without a figure): source/round3_researched.csv (scripts/rtt101_round3_lists.py)
    resd = [r["deal_id"] for r in rd("round3_researched.csv", os.path.join(D, "source"))] or [d for d in U_all if d in names3]
    fig = [d for d in resd if float(TI[MAP3[d]["transfer_id"]]["fee_gbp"] or 0) > 0]
    ver = [d for d in fig if TI[MAP3[d]["transfer_id"]]["status"] == "VERIFIED"]
    bytype = _C4(ptype(d) for d in resd)
    figtype = _C4(ptype(d) for d in fig)
    vertype = _C4(ptype(d) for d in ver)
    add_total = sum(float(TI[MAP3[d]["transfer_id"]]["fee_gbp"] or 0) for d in fig)
    left_all = sum(1 for d in U_all if not float(TI.get(MAP3[d]["transfer_id"], {}).get("fee_gbp") or 0))
    R = ["\n## 15. Source round 3: undisclosed fees and the leader deals (IQ-15i; DEC-422 to DEC-428)\n",
         "- **Why:** 2,205 deals with a Premier League side were counted £0 as \"undisclosed, no figure\" (fe3dd9e), many of them well known; the press printed "
         "a figure for many, and the rule already uses a grade B reported figure for an undisclosed fee (DEC-237 (g)). Luke asked how close our window totals "
         "are to the published ones.",
         f"- **Inputs:** Claude helper research on {len(resd)} of those deals (part24a summer 2009, part24e/f/g: all P1 deals between two clubs both in the PL "
         "that season and all P2 purchases from clubs that have been in the PL), and the 13 leader deals plus Nastasić's cash part read by Cowork in Luke's "
         "Chrome (part24d) and by a helper (part24b). Every data file's SHA-256 matched `00_README.md`.",
         "- **Checked at source:** all 481 cited pages read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/37904336661: 421 "
         "loaded; 16 refused, 14 not found, 11 server errors); 6 pages re-read after the runner learnt to match ð, ø and similar letters "
         "(https://github.com/marketmarathon/race-through-time/actions/runs/37906441423).",
         f"- **Quotes read:** {len(rev3)} newly confirmed quotes ({sum(1 for r in rev3 if r['decision'] == 'reject')} rejected: another deal's figure, a "
         "contract value, a valuation or release clause, a bid or offer, a maximum, a total with add-ons, a combined figure that did not complete, or one "
         "resting on a weaker outlet).",
         f"- **Undisclosed deals now carrying a reported figure:** {len(fig)} of the {len(resd)} researched ({len(ver)} confirmed at source; the rest a grade B "
         f"figure not yet confirmed, counted as a preview), adding {m(add_total)} of fees. By type: "
         + "; ".join(f"{k}: {figtype.get(k, 0)} of {v} ({vertype.get(k, 0)} confirmed)" for k, v in sorted(bytype.items())) + ". "
         f"{len(resd) - len(fig)} researched deals stay £0 (the fee is undisclosed in every source found, a free transfer, a loan, a nominal fee, a swap with no "
         f"stated value, or only a maximum). Of all 2,205, {left_all} are still £0; P4 (purchases from other clubs) and the sales were not researched."]
    # leader deals
    M2 = {r["deal_id"]: r["transfer_id"] for r in rd("source_round2_map.csv", os.path.join(D, "source"))}
    R += ["\n**The 13 leader deals and Nastasić** (order test of IQ-15h):\n", "| Deal | Player | Fee before | Fee after | Status | Basis |", "|---|---|---|---|---|---|"]
    for d in ["R0063", "R0082", "R0117", "R0121", "R0141", "R0150", "R0151", "R0152", "R0171", "R0179", "R0183", "R0202", "R0228", "R0490"]:
        t = TI.get(M2.get(d, ""), {})
        if t:
            R.append(f"| {d} | {t['player']} | £{float(B3.get(d, {}).get('fee_gbp') or 0):,.0f} | £{float(t['fee_gbp'] or 0):,.0f} | {t['status']} | {t['fee_status'][:80]} |")
    # windows against published
    WB = {w["window"]: w for w in rd("window_totals_before_source_round3.csv", os.path.join(D, "source"))}
    R += ["\n**How close we are to the published window totals** (gross spending by PL clubs; before = fe3dd9e; published = the first grade A/B total in part17b, "
          "research leads, UNVERIFIED). \"Share\" is our total as a share of the published one:\n",
          "| Window | Gross before | Gross after | Published | Share before | Share after | Undisclosed still £0 (PL buys) |", "|---|---|---|---|---|---|---|"]
    und_left = _C4()
    for d in U_all:
        t = TI.get(MAP3[d]["transfer_id"], {})
        if t and not float(t["fee_gbp"] or 0) and MAP3[d]["pl_side"] in ("buyer", "buyer+seller"):
            mo, yr = int(t["date"][5:7]), int(t["date"][:4])
            und_left[f"summer {yr}" if 4 <= mo <= 10 else (f"January {yr}" if mo <= 3 else f"January {yr + 1}")] += 1
    shares = []
    for win in sorted(set(WT), key=wkey):
        pub = next((r for r in sorted(lead_by.get(win, []), key=lambda r: r["grade"]) if r["gross_gbp"]), None)
        if not pub:
            continue
        a, b0, p_ = float(WT[win]["gross_spend_gbp"] or 0), float(WB.get(win, {}).get("gross_spend_gbp") or 0), float(pub["gross_gbp"])
        shares.append((win, b0 / p_, a / p_))
        R.append(f"| {win} | {m(b0)} | {m(a)} | {m(p_)} ({pub['grade']}) | {b0 / p_:.0%} | {a / p_:.0%} | {und_left.get(win, 0)} |")
    if shares:
        R.append(f"\nAcross the {len(shares)} windows with a published total, our sum averages {sum(s[1] for s in shares) / len(shares):.0%} of the published "
                 f"figure before this round and {sum(s[2] for s in shares) / len(shares):.0%} after. **What is left:** (1) undisclosed deals still counted £0, "
                 "above all PL purchases from clubs outside the PL (P4, 685 deals, not yet researched) and loans with an obligation booked only when the fee "
                 "is reported; (2) add-ons, which published totals usually include and we count only when reported as paid; (3) figures we count only "
                 "when confirmed or reported in the quality press, while some published totals use agency or club-reported estimates; (4) differences in "
                 "what a window covers (published totals often include deals agreed in the window but completed later, and some count fees in euros at "
                 "other rates).")
    # race effects and standings
    TB = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_source_round3.csv", os.path.join(D, "source"))}
    now = defaultdict(list)
    for r in SM:
        if r["rank"] and int(r["rank"]) <= 12:
            now[r["month_end"]].append((int(r["rank"]), r["club_id"]))
    NOW = {mo: [c for _, c in sorted(v)] for mo, v in now.items()}
    lead_ch = [mo for mo in sorted(NOW) if TB.get(mo) and TB[mo][0] != NOW[mo][0]]
    set_ch = [mo for mo in sorted(NOW) if TB.get(mo) and set(TB[mo]) != set(NOW[mo])]
    R.append(f"\n**Effect on the race** (against fe3dd9e): the leader changes at {len(lead_ch)} month ends"
             + (" (" + "; ".join(f"{mo[:7]}: {NAME.get(TB[mo][0], TB[mo][0])} → {NAME.get(NOW[mo][0], NOW[mo][0])}" for mo in lead_ch[:24]) + (" …" if len(lead_ch) > 24 else "") + ")" if lead_ch else "")
             + f"; who is in the top 12 changes at {len(set_ch)} month ends.")
    SB = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in rd("standings_before_source_round3.csv", os.path.join(D, "source"))}
    last = max(NOW)
    SA = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in SM if r["month_end"] == last and r["rank"]}
    R += [f"\n**Standings at the freeze ({last}), cumulative net spend:**\n", "| Rank after | Club | Net before (rank) | Net after | Change |", "|---|---|---|---|---|"]
    for c, (rk, v) in sorted(SA.items(), key=lambda x: x[1][0])[:20]:
        b_ = SB.get(c, (0, 0.0))
        R.append(f"| {rk} | {NAME.get(c, c)} | {m(b_[1])} ({b_[0]}) | {m(v)} | {m(v - b_[1])} |")
    # order test re-run
    OT = rd("round2_order_test.csv", os.path.join(D, "source"))
    yes = [r for r in OT if r["could_change"] == "yes"]
    R += [f"\n**Order test re-run on the {len(OT)} round 2 deals still not researched** (`source/round2_order_test.csv`): {len(yes)} could change who is in "
          f"the top 12 at some month end, {sum(1 for r in yes if r['what_changes'] == 'leader')} of them the leader:\n",
          "| Deal | Player | Date | Fee in use | First month end affected |", "|---|---|---|---|---|"]
    for r in sorted((r for r in yes if r["what_changes"] == "leader"), key=lambda r: r["date"]):
        R.append(f"| {r['deal_id']} | {r['player']} | {r['date']} | £{float(r['fee_gbp']):,.0f} | {r['first_month_end']} |")
    # still unverified
    unv = sorted((TI[MAP3[d]["transfer_id"]] for d in fig if TI[MAP3[d]["transfer_id"]]["status"] != "VERIFIED"), key=lambda t: -float(t["fee_gbp"]))
    R += [f"\n**Still UNVERIFIED among the round 3 figures: {len(unv)}** (a grade B figure the runner could not confirm: page refused or missing, or the club "
          "names not both on the page). The largest:\n", "| Player | Move | Date | Fee in use |", "|---|---|---|---|"]
    for t in unv[:20]:
        R.append(f"| {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | {t['date']} | £{float(t['fee_gbp']):,.0f} |")
    NF = rd("round3_unreadable.csv", os.path.join(D, "source"))
    if NF:
        R.append(f"\n**For Cowork to read in Luke's Chrome:** {len(NF)} rows the helpers saw only as a search snippet and the runner could not confirm (`source/round3_unreadable.csv`).")
    QB3 = [l.strip() for l in open(os.path.join(D, "source", "decided_round3.md"), encoding="utf-8") if l.strip()] \
        if os.path.exists(os.path.join(D, "source", "decided_round3.md")) else []
    R += QB3
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 15:", len(resd), "researched;", len(fig), "with a figure;", len(ver), "verified;", len(lead_ch), "leader changes;", len(yes), "order-test deals")

# ---- section 16: January 2020 and the window deal-count check (IQ-15j)
BASE16 = rd("standings_before_iq15j.csv", os.path.join(D, "source"))
if BASE16:
    from collections import Counter as _C5
    import subprocess as _sp

    def win_of(d):
        mo, yr = int(d[5:7]), int(d[:4])
        return f"summer {yr}" if 4 <= mo <= 10 else (f"January {yr}" if mo <= 3 else f"January {yr + 1}")
    PLM = {(r["club_id"], r["season"]) for r in rd("pl_membership.csv")}
    WB16 = {w["window"]: w for w in rd("window_totals_before_iq15j.csv", os.path.join(D, "source"))}
    WC = rd("window_deal_counts.csv", os.path.join(D, "source"))
    UNUSED = rd("club_page_rows_unused.csv", os.path.join(D, "source"))
    J20 = [t for t in T if t["date"] and win_of(t["date"]) == "January 2020"
           and any((c, t["season_attributed"]) in PLM for c in (t["from_club"], t["to_club"]))]
    newj = [t for t in J20 if t["found_via"].startswith("Wikipedia: 2019–20 ")]
    J20U = rd("jan2020_unsourced.csv", os.path.join(D, "source"))
    pub = next((r for r in sorted(lead_by.get("January 2020", []), key=lambda r: r["grade"]) if r["gross_gbp"]), None)
    g0, g1 = float(WB16.get("January 2020", {}).get("gross_spend_gbp") or 0), float(WT["January 2020"]["gross_spend_gbp"])
    R = ["\n## 16. January 2020 and the window deal-count check (IQ-15j; DEC-429 to DEC-434)\n",
         "- **Why January 2020 was missing (DEC-430):** the build reads each window's Wikipedia list page. The winter 2019-20 page we use "
         "(rev 1371935139) has 70 transfer rows, only 5 of them in January 2020; its edit history (runner, "
         "https://github.com/marketmarathon/race-through-time/actions/runs/37950422012) shows it never exceeded 67,150 bytes, so Wikipedia never "
         "listed most of that window's deals. A second fault turned up on the way: list tables with four columns (loans without a fee column) lost the "
         "date of every row, so 573 rows of summers 2017 and 2018 were dropped.",
         "- **Fix at the root:** (1) the four-column tables now keep their dates; (2) the 2019-20 club-season page of every PL club (and the 2003-04 and "
         "2004-05 pages) was read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/37950909967) and its In/Out and loan "
         "tables parsed (headings, bold labels, loan tables under season sub-headings, dates spanning rows); a club-page row is used only when no list "
         "page already has that player at that club within 60 days, and only for a window listed in `CLUB_PAGE_WINDOWS` (January 2020, as the brief "
         "approved; DEC-431); every other club-page row is listed in `source/club_page_rows_unused.csv`. Two new build checks: **no window has under "
         "half the PL deals of the same-type windows either side** (documented exceptions only), and **every list-page row has a date**. The 1992-2002 "
         "club-season rows are byte-for-byte unchanged.",
         f"- **January 2020 deals added:** {len(newj)} deals with a PL club (by type: "
         + ", ".join(f"{k} {v}" for k, v in sorted(_C5(t["type"] for t in newj).items())) + f"). The window now has {len(J20)} such deals "
         f"(it had 14; the same-type windows either side have a median of 111.5). With a fee:\n",
         "| Date | Player | Move | Fee in use | Status | Basis |", "|---|---|---|---|---|---|"]
    for t in sorted(J20, key=lambda t: t["date"]):
        if float(t["fee_gbp"] or 0) > 0:
            R.append(f"| {t['date']} | {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | "
                     f"£{float(t['fee_gbp']):,.0f} | {t['status']} | {'added in IQ-15j' if t in newj else 'already in the build'}; {t['fee_status'][:40]} |")
    spot = ["Berge", "Bowen", "Podence", "Pussetto", "Brownhill", "Randolph", "Lamptey", "Eriksen", "Ighalo", "Cédric", "Marí", "Souček", "Lazaro"]
    R += ["\n**Cowork's spot list:** all present now.\n", "| Player | Move | Date | Type | Fee in use | Status |", "|---|---|---|---|---|---|"]
    for s in spot:
        for t in J20:
            if s.lower() in t["player"].lower():
                R.append(f"| {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | {t['date']} | {t['type']} | "
                         f"£{float(t['fee_gbp'] or 0):,.0f} | {t['status']}: {t['fee_status'][:40]} |")
    R += ["\n- **Fees read at source (runner, https://github.com/marketmarathon/race-through-time/actions/runs/37952043572 and /37952723663):** 95 pages "
          "cited for the new deals. Confirmed: Pussetto €8m (Watford Observer, completed signing). Rejected: Louie Barry's BBC figure (\"about 1m euros "
          "(£880,000)\", an approximation; Barcelona's exact €1,048,000 is quoted only on a grade D page), Bowen's \"worth up to £22million\" (a "
          "maximum), and four undisclosed-fee candidates (grade D pages, another player's fee, an earlier move). Lamptey: Chelsea's club-season page "
          "gives £2,970,000 but Chelsea's own announcement gives no figure and Brighton's says undisclosed, so he stays undisclosed at £0 (DEC-433).",
          f"- **Not sourced:** {len(J20U)} January 2020 deals ({', '.join(f'{k} {v}' for k, v in sorted(_C5(r['type'] for r in J20U).items()))}) keep the "
          "build's normal status and are listed for Cowork in `source/jan2020_unsourced.csv` (no figures in the list).",
          "- **Minamino (brief 2(d)):** BBC Sport (grade B, confirmed on the runner) says \"Deal to be completed on 1 January\", and Liverpool's 2019-20 page "
          "gives entry date 1 January 2020. The build now dates the deal **1 January 2020** (was 19 December 2019, the day it was agreed; DEC-432). "
          "Same window and season, so no total changes.",
          f"- **January 2020 total (gross spending by PL clubs):** {m(g0)} before, **{m(g1)} after**"
          + (f"; published {m(float(pub['gross_gbp']))} ({pub['publisher']}, grade {pub['grade']}, research lead): {g0 / float(pub['gross_gbp']):.0%} → "
             f"{g1 / float(pub['gross_gbp']):.0%}" if pub else "")
          + ". The rest of the gap is mainly the undisclosed deals still counted £0 (among the purchases Lo Celso, Podence, Samatta, Brownhill, Mooy "
          "and Randolph) and Bowen's guaranteed fee. Also to check in a later round: Ziyech's £33m is in this window (dated 24 February 2020, when "
          "the deal was agreed), which a published January total may not include."]
    flagged = [w for w in WC if w["flag"]]
    R += ["\n**Windows the deal-count check flags** (deals with a PL club; neighbours = the two same-type windows either side):\n",
          "| Window | Deals | Neighbours' median | Why | Club-page rows listed, not used |", "|---|---|---|---|---|"]
    why = {"January 1993": "early club-season pages read with the old table reading", "January 1994": "early club-season pages read with the old table reading",
           "January 2004": "the winter 2003-04 list page misses most deals", "January 2005": "the winter 2004-05 list page misses most deals"}
    unc = _C5(win_of(r["date"]) for r in UNUSED if r["date"])
    for w in flagged:
        R.append(f"| {w['window']} | {w['deals_with_pl_side']} | {float(w['neighbour_median']):g} | {why.get(w['window'], '?')} | {unc.get(w['window'], 0)} |")
    R += [f"\nAll four would clear the check with their listed club-page rows; they are documented exceptions in the build (`KNOWN_SPARSE`, DEC-431) until "
          "a brief approves adding them. Summer 2017 (175 deals before the date fix, 371 now) clears. Summer 2019 is not flagged, but its club-season "
          f"pages list {unc.get('summer 2019', 0)} moves the list page lacks (mostly releases, loans and youth moves); the page histories show three list pages "
          "much shorter now than at their largest (summer 2007, 2013 and 2019), so those windows are candidates for the same club-page reading."]
    # race effects
    TB16 = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_iq15j.csv", os.path.join(D, "source"))}
    now = defaultdict(list)
    for r in SM:
        if r["rank"] and int(r["rank"]) <= 12:
            now[r["month_end"]].append((int(r["rank"]), r["club_id"]))
    NOW = {mo: [c for _, c in sorted(v)] for mo, v in now.items()}
    # IQ-15k: this section records the race as built at the end of IQ-15j (193580c); section 17 has the current figures
    _T4 = rd("top12_before_round4.csv", os.path.join(D, "source"))
    if _T4:
        NOW = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in _T4}
    lead_ch = [mo for mo in sorted(NOW) if TB16.get(mo) and TB16[mo][0] != NOW[mo][0]]
    set_ch = [mo for mo in sorted(NOW) if TB16.get(mo) and set(TB16[mo]) != set(NOW[mo])]
    ord_ch = [mo for mo in sorted(NOW) if TB16.get(mo) and TB16[mo] != NOW[mo]]
    R.append(f"\n**Effect on the race** (against 398abbf, the end of IQ-15i; as built at the end of IQ-15j, 193580c; section 17 has the current figures): the leader changes at {len(lead_ch)} month ends; who is in the top 12 "
             f"changes at {len(set_ch)} month ends"
             + (" (" + "; ".join(f"{mo[:7]}: {', '.join(NAME.get(c, c) for c in sorted(set(NOW[mo]) - set(TB16[mo])))} in for "
                                  f"{', '.join(NAME.get(c, c) for c in sorted(set(TB16[mo]) - set(NOW[mo])))}" for mo in set_ch[:12]) + (" …" if len(set_ch) > 12 else "") + ")" if set_ch else "")
             + f"; the order within the top 12 changes at {len(ord_ch)} month ends. Wolves' entries (2019 and 2023) come from Jonny's £18m permanent move "
             "(a research lead that had no deal to attach to until his loan row came back with the date fix; dated 31 January 2019, DEC-432).")
    SB16 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in BASE16}
    last = max(NOW)
    SA16 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in SM if r["month_end"] == last and r["rank"]}
    if rd("standings_before_round4.csv", os.path.join(D, "source")):
        SA16 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in rd("standings_before_round4.csv", os.path.join(D, "source"))}
    R += [f"\n**Standings at the freeze ({last}), cumulative net spend, at the end of IQ-15j:**\n", "| Rank after | Club | Net before (rank) | Net after | Change |", "|---|---|---|---|---|"]
    for c, (rk, v) in sorted(SA16.items(), key=lambda x: x[1][0])[:12]:
        b_ = SB16.get(c, (0, 0.0))
        R.append(f"| {rk} | {NAME.get(c, c)} | £{b_[1] / 1e6:,.1f}m ({b_[0]}) | £{v / 1e6:,.1f}m | {m(v - b_[1])} |")
    top3 = [c for c, _ in sorted(SA16.items(), key=lambda x: x[1][0])[:3]]
    R.append(f"\nThe three leaders are now within {m(SA16[top3[0]][1] - SA16[top3[2]][1])} of each other ({m(SB16[top3[0]][1] - min(SB16[c][1] for c in top3))} before): "
             f"{NAME[top3[0]]} lead {NAME[top3[1]]} by {m(SA16[top3[0]][1] - SA16[top3[1]][1])} and {NAME[top3[2]]} by {m(SA16[top3[0]][1] - SA16[top3[2]][1])}. "
             "Chelsea fall from second to third because of three January 2020 sales known only from Chelsea's 2019-20 Wikipedia page: Michael Hector to "
             "Fulham (£5,310,000), Clinton Mola to Stuttgart (£360,000) and Victor Moses's loan to Inter (£190,000), less Bryan Fiabema's £540,000 purchase; "
             "none is confirmed at source yet (all in `source/jan2020_unsourced.csv` or loans). Under DEC-429 the final order is not settled until the "
             "IQ-15k round on the leaders' undisclosed deals. (IQ-15k: Hector's £5.31m was a duplicate of his September 2019 move and is gone, DEC-436.)")
    OT = rd("round2_order_test.csv", os.path.join(D, "source"))
    yes = [r for r in OT if r["could_change"] == "yes"]
    R.append(f"\n**Order test re-run** (`source/round2_order_test.csv`): {len(yes)} of {len(OT)} unresearched round 2 deals could change who is in the top 12 at "
             f"some month end, {sum(1 for r in yes if r['what_changes'] == 'leader')} of them the leader.")
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 16:", len(newj), "January 2020 deals added;", len(lead_ch), "leader changes;", len(set_ch), "top-12 changes")

# ---- section 17: source round 4, the three leaders' undisclosed deals (IQ-15k)
BASE4 = rd("source_round4_baseline.csv", os.path.join(D, "source"))
if BASE4:
    from collections import Counter as _C6
    B4 = {r["transfer_id"]: r for r in BASE4}
    MAP4 = rd("source_round4_map.csv", os.path.join(D, "source"))
    rev4 = [r for r in rd("review_decisions.csv", os.path.join(D, "source")) if r["batch"] == "SR4-01"]
    J6 = [r for r in BASE4 if r["deal_id"].startswith("T")]
    cnt, amt = _C6(), _C6()
    for r in MAP4:
        t = TI.get(r["transfer_id"], {})
        club, side = r["leader_side"].split(":")
        f = float(t.get("fee_gbp") or 0)
        cnt[(club, side, "all")] += 1
        if f > 0:
            cnt[(club, side, "fig")] += 1
            amt[(club, side)] += f
            if t.get("status") == "VERIFIED":
                cnt[(club, side, "ver")] += 1
    nfig = len({r["transfer_id"] for r in MAP4 if float(TI.get(r["transfer_id"], {}).get("fee_gbp") or 0) > 0})
    nver = len({r["transfer_id"] for r in MAP4 if float(TI.get(r["transfer_id"], {}).get("fee_gbp") or 0) > 0 and TI[r["transfer_id"]]["status"] == "VERIFIED"})
    R = ["\n## 17. Source round 4: the three leaders' undisclosed deals (IQ-15k; DEC-435 to DEC-439)\n",
         "- **Why:** Luke's DEC-429: the order at the freeze is not settled while the three leaders' undisclosed deals are counted £0.",
         "- **Inputs:** the work list of 258 deals (Manchester United 16 purchases and 61 sales, Chelsea 24 and 63, Manchester City 27 and 67; "
         "`source/source_round4_map.csv`), Claude helper research on all of them (part25a, part25c), the six January 2020 leader deals (part25d) and "
         "Cowork's Chrome reads of the 12 round 3 pages the runner could not read (part25b). Every file's SHA-256 matched `00_README.md`.",
         "- **Checked at source:** the 213 pages cited read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/37962899786: "
         "186 loaded; 15 refused, 6 not found, the rest server errors or redirects).",
         f"- **Quotes read:** {len(rev4)} newly confirmed quotes ({sum(1 for r in rev4 if r['decision'] == 'reject')} rejected: a pre-completion figure "
         "where a completion report exists, a lower bound, an asking price, a total with add-ons, a maximum, and the Mikel settlement booked elsewhere).",
         f"- **Result (as now built, after round 5 too; at the end of IQ-15k: 43 with a figure, 30 confirmed): {nfig} of the 258 deals carry a figure ({nver} confirmed at source); none did before; {258 - nfig} stay £0** (undisclosed in "
         "every source found, free, a loan, training compensation, a nominal fee, or only a maximum, lower bound or grade C figure). By leader and side "
         "(a deal between two leaders counts on both sides):\n",
         "| Club | Side | Deals | With a figure | Confirmed at source | Fees added |", "|---|---|---|---|---|---|"]
    for club in ("manchester_united", "chelsea", "manchester_city"):
        for side, lab in (("buyer", "purchases"), ("seller", "sales")):
            R.append(f"| {NAME.get(club, club)} | {lab} | {cnt[(club, side, 'all')]} | {cnt[(club, side, 'fig')]} | {cnt[(club, side, 'ver')]} | {m(amt[(club, side)])} |")
    R.append("\n**The figures now in use** (largest first):\n")
    R += ["| Deal | Player | Move | Date | Fee in use | Status | Basis |", "|---|---|---|---|---|---|---|"]
    for r in sorted(MAP4, key=lambda r: -float(TI.get(r["transfer_id"], {}).get("fee_gbp") or 0)):
        t = TI.get(r["transfer_id"], {})
        if float(t.get("fee_gbp") or 0) > 0:
            R.append(f"| {r['deal_id']} | {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | {t['date']} | "
                     f"£{float(t['fee_gbp']):,.0f} | {t['status']} ({t['grade']}) | {t['fee_status'][:60]} |")
    R.append(f"\n**The six January 2020 leader deals (part25d):** "
             + "; ".join(f"{TI[r['transfer_id']]['player']} {('£' + format(float(TI[r['transfer_id']]['fee_gbp'] or 0), ',.0f')) if float(TI[r['transfer_id']]['fee_gbp'] or 0) else '£0'} ({TI[r['transfer_id']]['fee_status'][:30]})"
                         for r in J6 if r["transfer_id"] in TI)
             + ". Hector's duplicate (Tf8a5f7e6ee) is gone; his one move is T6403be737e. No grade A/B figure was found for any of them; Fiabema, Mola "
             "and Moses keep their Wikipedia figures as unconfirmed.")
    # race
    TB4 = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_round4.csv", os.path.join(D, "source"))}
    now = defaultdict(list)
    for r in SM:
        if r["rank"] and int(r["rank"]) <= 12:
            now[r["month_end"]].append((int(r["rank"]), r["club_id"]))
    NOW = {mo: [c for _, c in sorted(v)] for mo, v in now.items()}
    # IQ-15l: this section records the race as built at the end of IQ-15k (1b01d81); section 18 has the current figures
    if rd("top12_before_round5.csv", os.path.join(D, "source")):
        NOW = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_round5.csv", os.path.join(D, "source"))}

    def crowns(seqmap):
        out = []
        for mo in sorted(seqmap):
            if not out or out[-1][1] != seqmap[mo][0]:
                out.append((mo[:7], seqmap[mo][0]))
        return out
    cb, ca = crowns(TB4), crowns(NOW)
    lead_ch = [mo for mo in sorted(NOW) if TB4.get(mo) and TB4[mo][0] != NOW[mo][0]]
    set_ch = [mo for mo in sorted(NOW) if TB4.get(mo) and set(TB4[mo]) != set(NOW[mo])]
    R += ["\n**Who leads, through time** (month the lead changes hands; from 2003):\n",
          "- Before (193580c): " + " → ".join(f"{NAME.get(c, c)} ({mo})" for mo, c in cb if mo >= "2003"),
          "- After (end of IQ-15k, 1b01d81; section 18 has the current figures): " + " → ".join(f"{NAME.get(c, c)} ({mo})" for mo, c in ca if mo >= "2003"),
          f"\nThe leader differs at {len(lead_ch)} month ends; who is in the top 12 differs at {len(set_ch)} month ends"
          + (" (" + "; ".join(f"{mo[:7]}: {', '.join(NAME.get(c, c) for c in sorted(set(NOW[mo]) - set(TB4[mo])))} in for "
                                f"{', '.join(NAME.get(c, c) for c in sorted(set(TB4[mo]) - set(NOW[mo])))}" for mo in set_ch[:10]) + ")" if set_ch else "")
          + ". The top-12 changes are Wolves leaving it again in 2019 and 2023: Jonny's £18m no longer has a deal (DEC-436)."]
    SB4 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in rd("standings_before_round4.csv", os.path.join(D, "source"))}
    last = max(NOW)
    SA4 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in SM if r["month_end"] == last and r["rank"]}
    if rd("standings_before_round5.csv", os.path.join(D, "source")):
        SA4 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in rd("standings_before_round5.csv", os.path.join(D, "source"))}
    R += [f"\n**Standings at the freeze ({last}), cumulative net spend, at the end of IQ-15k:**\n", "| Rank after | Club | Net before (rank) | Net after | Change |", "|---|---|---|---|---|"]
    for c, (rk, v) in sorted(SA4.items(), key=lambda x: x[1][0])[:12]:
        b_ = SB4.get(c, (0, 0.0))
        R.append(f"| {rk} | {NAME.get(c, c)} | £{b_[1] / 1e6:,.1f}m ({b_[0]}) | £{v / 1e6:,.1f}m | {m(v - b_[1])} |")
    t3 = [c for c, _ in sorted(SA4.items(), key=lambda x: x[1][0])[:3]]
    b3 = [c for c, _ in sorted(SB4.items(), key=lambda x: x[1][0])[:3]]
    R.append(f"\n**Gaps between the three leaders:** after, {NAME[t3[0]]} lead {NAME[t3[1]]} by {m(SA4[t3[0]][1] - SA4[t3[1]][1])} and {NAME[t3[2]]} by "
             f"{m(SA4[t3[0]][1] - SA4[t3[2]][1])}; before, {NAME[b3[0]]} led {NAME[b3[1]]} by {m(SB4[b3[0]][1] - SB4[b3[1]][1])} and {NAME[b3[2]]} by "
             f"{m(SB4[b3[0]][1] - SB4[b3[2]][1])}. Manchester United take the lead only in the final month (the summer 2026 window).")
    OT = rd("round2_order_test.csv", os.path.join(D, "source"))
    yes = [r for r in OT if r["could_change"] == "yes"]
    R.append(f"\n**Order test re-run** (at the end of IQ-15k): 206 of 392 unresearched round 2 deals could change who is in the top 12 "
             f"at some month end, 14 of them the leader (201 and 5 before this round): with the "
             "finish this close, the P4 sweep (DEC-429) can still matter.")
    unv = sorted((TI[r["transfer_id"]] for r in MAP4 if float(TI.get(r["transfer_id"], {}).get("fee_gbp") or 0) > 0 and TI[r["transfer_id"]]["status"] != "VERIFIED"),
                 key=lambda t: -float(t["fee_gbp"]))
    R += [f"\n**Still UNVERIFIED among the round 4 figures: {len(unv)}** (a grade B figure the runner could not confirm: page refused, gone or "
          "changed, or the clubs not both named):\n", "| Player | Move | Date | Fee in use |", "|---|---|---|---|"]
    for t in unv:
        R.append(f"| {t['player']} | {clubs.get(t['from_club'], t['from_club'])} → {clubs.get(t['to_club'], t['to_club'])} | {t['date']} | £{float(t['fee_gbp']):,.0f} |")
    QB4 = [l.rstrip("\n") for l in open(os.path.join(D, "source", "decided_round4.md"), encoding="utf-8")] \
        if os.path.exists(os.path.join(D, "source", "decided_round4.md")) else []
    R += QB4
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 17:", nfig, "with a figure;", nver, "verified;", len(lead_ch), "leader changes;", len(yes), "order-test deals")

# ---- section 18: source round 5, the fees that decide the finish (IQ-15l)
BASE5 = rd("source_round5_baseline.csv", os.path.join(D, "source"))
if BASE5:
    SRCS = {s["source_id"]: s for s in rd("sources.csv")}
    MAP5 = {r["deal_id"]: r for r in rd("source_round5_map.csv", os.path.join(D, "source"))}
    rev5 = [r for r in rd("review_decisions.csv", os.path.join(D, "source")) if r["batch"] == "SR5-01"]
    chrome = [c for c in rd("runner_checks.csv", os.path.join(D, "source")) if c["check_id"].startswith("C26b-")]
    v0 = sum(1 for r in BASE5 if r["status"] == "VERIFIED")
    v1 = sum(1 for r in BASE5 if TI.get(r["transfer_id"], {}).get("status") == "VERIFIED")
    BAT = {"c01": "Sporting Life fees", "c02": "Sporting Life and single-source fees", "c03": "round 4 UNVERIFIED",
           "c04": "round 2 leader-test deals", "c05": "round 2 leader-test deals"}
    R = ["\n## 18. Source round 5: the fees that decide the finish (IQ-15l; DEC-440 to DEC-444)\n",
         "- **Why:** Luke's DEC-440: keep Sporting Life at grade B, find other sources for the Sporting Life fees that decide the finish, re-try the "
         "13 unconfirmed round 4 figures and research the 14 round 2 deals that could change the leader; treat the order at the freeze as settled "
         "only once those are checked.",
         "- **Inputs:** the 34-deal work list (`source/source_round5_map.csv`), Claude helper research on all 34 (part26a) and 41 page reads by Cowork "
         "in Luke's Chrome (part26b). Every file's SHA-256 matched `00_README.md`.",
         "- **Checked at source:** the 73 pages cited read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/38000399943: "
         f"61 loaded; 6 refused, 3 server errors, 1 gone, 1 not found, 1 still loading); {len(chrome)} pages the runner could not read or could not read "
         "the figure on were taken from Cowork's Chrome reads.",
         f"- **Quotes read:** {len(rev5)} newly confirmed quotes ({sum(1 for r in rev5 if r['decision'] == 'reject')} rejected: totals with add-ons, a "
         "maximum, another move's fee, and a figure that includes a friendly match).",
         f"- **Result: {v1} of the 34 deals are now VERIFIED ({v0} before).** Each deal, before and after:\n",
         "| Group | Player | Move | Date | Before | After | Status | Source of the figure in use |", "|---|---|---|---|---|---|---|---|"]
    for r in BASE5:
        t = TI.get(r["transfer_id"], {})
        s = SRCS.get(t.get("canonical_source_id", ""), {})
        amt = f"{t['currency']} {float(t['original_amount']):,.0f} = £{float(t['fee_gbp']):,.0f}" if t.get("currency") and t["currency"] != "GBP" and t.get("original_amount") else f"£{float(t.get('fee_gbp') or 0):,.0f}"
        R.append(f"| {BAT.get(MAP5.get(r['transfer_id'], {}).get('batch', ''), '')} | {t.get('player', '')} | {clubs.get(t.get('from_club'), t.get('from_club'))} → "
                 f"{clubs.get(t.get('to_club'), t.get('to_club'))} | {t.get('date', '')} | £{float(r['fee_gbp'] or 0):,.0f} ({r['status']}) | {amt} | "
                 f"{t.get('status', '')} ({t.get('grade', '')}) | {s.get('publisher', '') or t.get('fee_status', '')[:40]} |")
    R.append("\nWhere the figure in use still rests on Sporting Life (Courtois, Henderson, Guéhi, Aké), the same figure is now confirmed by the BBC "
             "(Henderson £15m, Aké £20m), The Independent (Guéhi £18m) or Reuters and AFP (Courtois €35m, £31.47m).")
    TB5 = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_round5.csv", os.path.join(D, "source"))}
    now = defaultdict(list)
    for r in SM:
        if r["rank"] and int(r["rank"]) <= 12:
            now[r["month_end"]].append((int(r["rank"]), r["club_id"]))
    NOW = {mo: [c for _, c in sorted(v)] for mo, v in now.items()}
    # IQ-15m: this section records the race as built at the end of IQ-15l (13173a4); section 19 has the current figures
    if rd("top12_before_iq15m.csv", os.path.join(D, "source")):
        NOW = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_iq15m.csv", os.path.join(D, "source"))}

    def crowns5(seqmap):
        out = []
        for mo in sorted(seqmap):
            if not out or out[-1][1] != seqmap[mo][0]:
                out.append((mo[:7], seqmap[mo][0]))
        return out
    lead_ch = [mo for mo in sorted(NOW) if TB5.get(mo) and TB5[mo][0] != NOW[mo][0]]
    set_ch = [mo for mo in sorted(NOW) if TB5.get(mo) and set(TB5[mo]) != set(NOW[mo])]
    R += ["\n**Who leads, through time** (month the lead changes hands; from 2003):\n",
          "- Before (1b01d81): " + " → ".join(f"{NAME.get(c, c)} ({mo})" for mo, c in crowns5(TB5) if mo >= "2003"),
          "- After (end of IQ-15l, 13173a4; section 19 has the current figures): " + " → ".join(f"{NAME.get(c, c)} ({mo})" for mo, c in crowns5(NOW) if mo >= "2003"),
          f"\nThe leader differs at {len(lead_ch)} month end{'' if len(lead_ch) == 1 else 's'}" + (" (" + ", ".join(mo[:7] for mo in lead_ch) + ")" if lead_ch else "")
          + f"; who is in the top 12 differs at {len(set_ch)} month end{'' if len(set_ch) == 1 else 's'}" + (" (" + "; ".join(f"{mo[:7]}: {', '.join(NAME.get(c, c) for c in sorted(set(NOW[mo]) - set(TB5[mo])))} in for "
                                f"{', '.join(NAME.get(c, c) for c in sorted(set(TB5[mo]) - set(NOW[mo])))}" for mo in set_ch[:8]) + ")" if set_ch else "") + "."]
    SB5 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in rd("standings_before_round5.csv", os.path.join(D, "source"))}
    last = max(NOW)
    SA5 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in SM if r["month_end"] == last and r["rank"]}
    if rd("standings_before_iq15m.csv", os.path.join(D, "source")):
        SA5 = {r["club_id"]: (int(r["rank"]), float(r["cum_net_gbp"])) for r in rd("standings_before_iq15m.csv", os.path.join(D, "source"))}
    R += [f"\n**Standings at the freeze ({last}), cumulative net spend, at the end of IQ-15l:**\n", "| Rank after | Club | Net before (rank) | Net after | Change |", "|---|---|---|---|---|"]
    for c, (rk, v) in sorted(SA5.items(), key=lambda x: x[1][0])[:12]:
        b_ = SB5.get(c, (0, 0.0))
        R.append(f"| {rk} | {NAME.get(c, c)} | £{b_[1] / 1e6:,.2f}m ({b_[0]}) | £{v / 1e6:,.2f}m | {m(v - b_[1])} |")
    t3 = [c for c, _ in sorted(SA5.items(), key=lambda x: x[1][0])[:3]]
    b3 = [c for c, _ in sorted(SB5.items(), key=lambda x: x[1][0])[:3]]
    R.append(f"\n**Gaps between the three leaders:** after, {NAME[t3[0]]} lead {NAME[t3[1]]} by £{(SA5[t3[0]][1] - SA5[t3[1]][1]) / 1e6:,.2f}m and "
             f"{NAME[t3[2]]} by £{(SA5[t3[0]][1] - SA5[t3[2]][1]) / 1e6:,.2f}m; before, {NAME[b3[0]]} led {NAME[b3[1]]} by "
             f"£{(SB5[b3[0]][1] - SB5[b3[1]][1]) / 1e6:,.2f}m and {NAME[b3[2]]} by £{(SB5[b3[0]][1] - SB5[b3[2]][1]) / 1e6:,.2f}m.")
    OT = rd("round2_order_test.csv", os.path.join(D, "source"))
    yes = [r for r in OT if r["could_change"] == "yes"]
    R.append(f"\n**Order test re-run** (`source/round2_order_test.csv`, the round 5 deals now counted as researched; at the end of IQ-15l: 188 of 378): {len(yes)} of {len(OT)} unresearched "
             f"round 2 deals could change who is in the top 12 at some month end, **{sum(1 for r in yes if r['what_changes'] == 'leader')} the leader** "
             "(14 before this round). Of the five round 5 deals with no grade A/B source, only Guivarc'h (Newcastle → Rangers, 1998, £3.5m) changes the "
             "leader if removed, at August 1999 (tested in a scratch copy). Undisclosed fees counted £0 cannot be tested this way: there is no figure to try.")
    unv = [TI[r["transfer_id"]] for r in BASE5 if TI.get(r["transfer_id"], {}).get("status") != "VERIFIED" and float(TI[r["transfer_id"]]["fee_gbp"] or 0) > 0]
    R += [f"\n**Still UNVERIFIED among the 34: {len(unv)}** (no grade A/B page found): "
          + "; ".join(f"{t['player']} £{float(t['fee_gbp']):,.0f} ({t['date'][:4]})" for t in unv) + ". Hernández and David James now count £0."]
    QB5 = [l.rstrip("\n") for l in open(os.path.join(D, "source", "decided_round5.md"), encoding="utf-8")] \
        if os.path.exists(os.path.join(D, "source", "decided_round5.md")) else []
    R += QB5
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 18:", v1, "of 34 verified;", len(lead_ch), "leader changes;", sum(1 for r in yes if r["what_changes"] == "leader"), "order-test leader deals")

# ---- section 19: wrap-up before design (IQ-15m)
B19 = rd("standings_before_iq15m.csv", os.path.join(D, "source"))
if B19:
    def bymonth(rows):
        out = defaultdict(list)
        for r in rows:
            if r["rank"]:
                out[r["month_end"]].append(r)
        for mo in out:
            out[mo].sort(key=lambda r: int(r["rank"]))
        return out
    PRE, ONS = bymonth(SM), bymonth(rd("series_onscreen.csv"))
    last = max(ONS)

    def crowns19(bm):
        out = []
        for mo in sorted(bm):
            if not out or out[-1][1] != bm[mo][0]["club_id"]:
                out.append((mo[:7], bm[mo][0]["club_id"]))
        return out

    def close19(bm, since="2002-07", lim=10e6):
        return [(mo[:7], bm[mo][0]["club_id"], bm[mo][1]["club_id"], float(bm[mo][0]["cum_net_gbp"]) - float(bm[mo][1]["cum_net_gbp"]))
                for mo in sorted(bm) if mo >= since and float(bm[mo][0]["cum_net_gbp"]) - float(bm[mo][1]["cum_net_gbp"]) < lim]
    TO = rd("tier1_open.csv")
    FEE = [t for t in T if float(t["fee_gbp"] or 0) > 0]

    def share(rows):
        s = sum(float(t["fee_gbp"]) for t in rows)
        return (sum(float(t["fee_gbp"]) for t in rows if t["status"] == "VERIFIED") / s) if s else 0.0
    WB19 = {w["window"]: float(w["gross_spend_gbp"] or 0) for w in rd("window_totals_before_iq15m.csv", os.path.join(D, "source"))}
    pubs = {w: next((r for r in sorted(v, key=lambda r: r["grade"]) if r["gross_gbp"]), None) for w, v in lead_by.items()}
    pubs = {w: float(p["gross_gbp"]) for w, p in pubs.items() if p}
    def wshare(W):
        ws = [W.get(w, 0.0) / p for w, p in pubs.items()]
        return sum(ws) / len(ws), sum(W.get(w, 0.0) for w in pubs) / sum(pubs.values())
    wb_avg, wb_money = wshare(WB19)
    wa_avg, wa_money = wshare({w: float(v["gross_spend_gbp"] or 0) for w, v in WT.items()})
    OT = rd("round2_order_test.csv", os.path.join(D, "source"))
    yes = [r for r in OT if r["could_change"] == "yes"]
    TU = rd("thin_windows_unsourced.csv", os.path.join(D, "source"))
    R = ["\n## 19. Wrap-up before design (IQ-15m; DEC-445 to DEC-449)\n",
         "**What changed**\n",
         "- **Luke's DEC-445:** RTT-101 keeps being built from our own deal-by-deal data; no Transfermarkt or press club totals anywhere; the P4 sweep "
         "is not run now. Section 18's question 1 stays open: on VERIFIED fees only the order at the freeze is different.",
         "- **Guivarc'h (1998):** £3.5m confirmed from Cowork's Chrome read of The Independent's weekly round-up (DEC-446).",
         f"- **Thin windows (DEC-447):** 604 deals the list pages miss added from club-season pages (January 1993, 1994, 2004, 2005; summers 2007, 2013, "
         f"2019); 23 carry a Wikipedia figure (£49.2m), none yet confirmed; {len(TU)} undisclosed or unconfirmed ones listed in "
         "`source/thin_windows_unsourced.csv`. The deal-count check passes for every window and `KNOWN_SPARSE` is empty.",
         "- **The on-screen series (DEC-448):** `series_onscreen.csv`, built from VERIFIED fees only (every tier), beside the all-fees preview "
         "`series_monthly.csv`; contract v1.5 §8 points the player at it.",
         f"\n**Window totals against part17b** (gross spending by PL clubs; {len(pubs)} windows with a published total; research leads, UNVERIFIED, "
         "a comparison only): our totals average "
         f"{wb_avg:.1%} of the published figure before IQ-15m and {wa_avg:.1%} after; as a share of the money, {wb_money:.1%} before and {wa_money:.1%} after "
         "(the thin windows add mostly loans, free transfers and undisclosed fees).",
         f"\n**Standings at the freeze ({last}), top 12:**\n",
         "| Rank | On screen (VERIFIED fees only) | Net | Gap to the leader | Preview (all fees) | Net |", "|---|---|---|---|---|---|"]
    lead_v = float(ONS[last][0]["cum_net_gbp"])
    for i in range(12):
        a, b = ONS[last][i], PRE[last][i]
        R.append(f"| {i + 1} | {NAME.get(a['club_id'], a['club_id'])} | £{float(a['cum_net_gbp']) / 1e6:,.1f}m | "
                 f"{'–' if i == 0 else '£' + format((lead_v - float(a['cum_net_gbp'])) / 1e6, ',.1f') + 'm'} | {NAME.get(b['club_id'], b['club_id'])} | £{float(b['cum_net_gbp']) / 1e6:,.1f}m |")
    R += ["\n**Who leads, through time** (month the lead changes hands):\n",
          "- On screen: " + " → ".join(f"{NAME.get(c, c)} ({mo})" for mo, c in crowns19(ONS)),
          "- Preview: " + " → ".join(f"{NAME.get(c, c)} ({mo})" for mo, c in crowns19(PRE))]
    cs, cp = close19(ONS), close19(PRE)
    R.append("\n**Close calls since July 2002** (leader ahead by under £10m at a month end): on screen, "
             + ("; ".join(f"{mo} {NAME.get(a, a)} over {NAME.get(b, b)} by £{g / 1e6:.2f}m" for mo, a, b, g in cs) if cs else "none")
             + "; in the preview, " + ("; ".join(f"{mo} {NAME.get(a, a)} over {NAME.get(b, b)} by £{g / 1e6:.2f}m" for mo, a, b, g in cp) if cp else "none")
             + ". The one-month Chelsea lead of July 2016 and the March–June 2003 near-tie (United over Newcastle) exist only in the preview. "
             "Before 2002 the race is close for long stretches on both bases (Blackburn, Liverpool and Newcastle within £3m of each other in "
             "many months of 1992–2000).")
    TB19 = {r["month_end"]: r["top12_in_rank_order"].split(";") for r in rd("top12_before_iq15m.csv", os.path.join(D, "source"))}
    pre_set = [mo for mo in sorted(PRE) if TB19.get(mo) and set(TB19[mo]) != {r["club_id"] for r in PRE[mo][:12]}]
    pre_lead = [mo for mo in sorted(PRE) if TB19.get(mo) and TB19[mo][0] != PRE[mo][0]["club_id"]]
    diff_lead = [mo for mo in sorted(ONS) if ONS[mo][0]["club_id"] != PRE[mo][0]["club_id"]]
    R.append(f"\n**Top-12 changes and the order test:** against 13173a4 the preview's leader changes at {len(pre_lead)} month ends and who is in its "
             f"top 12 at {len(pre_set)}; the on-screen series differs from the preview in the leader at {len(diff_lead)} month ends. Order test "
             f"(`source/round2_order_test.csv`): {len(yes)} of {len(OT)} unresearched round 2 deals could change a top-12 place, "
             f"{sum(1 for r in yes if r['what_changes'] == 'leader')} the leader.")
    R.append(f"\n**VERIFIED share of fee money:** {share(FEE):.1%} of £{sum(float(t['fee_gbp']) for t in FEE) / 1e9:,.2f}bn of fees "
             f"({sum(1 for t in FEE if t['status'] == 'VERIFIED')} of {len(FEE)} fees); Tier 1 {share([t for t in FEE if t['tier'] == '1']):.1%}, "
             f"Tier 2 {share([t for t in FEE if t['tier'] == '2']):.1%}, Tier 3 {share([t for t in FEE if t['tier'] == '3']):.1%}.")
    wy = _C6 = None
    from collections import Counter as _C9
    R.append(f"\n**Still UNVERIFIED:** {len(TO)} Tier 1 fees (`tier1_open.csv`, no figures; {sum(1 for r in TO if r['involves_leader'] == 'yes')} "
             "involve Manchester United, Chelsea or Manchester City; why open: "
             + ", ".join(f"{k} {v}" for k, v in _C9(r['why_open'].split(' (')[0] for r in TO).most_common()) + "). If every unconfirmed fee "
             "were confirmed, Chelsea would lose £56.1m on screen, City £52.9m and United gain £40.3m: the gap between the two bases, so the order at "
             "the freeze waits for Cowork's Tier 1 round (DEC-445). Tier 2 and Tier 3 fees not confirmed stay off screen (DEC-448).")
    R.append("\n**Question for Luke (what the video shows):**\n1. **On screen, should a bar count only fees confirmed at source, including the "
             "small ones under £2m?** That is what the contract says (§8) and what `series_onscreen.csv` does; the approved tiers had small fees "
             "counted on the strength of a sample, but the sample cannot yet give an error rate. Counting the small unconfirmed fees as well changes no "
             "leader (Chelsea still lead at the freeze, by £8.1m instead of £11.0m). **Recommendation:** yes, confirmed fees only, every tier.")
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 19:", len(TO), "Tier 1 open;", len(crowns19(ONS)), "on-screen leader spells")
