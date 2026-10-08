#!/usr/bin/env python3
"""RTT-101 (IQ-15): write reports/RTT-101_data_report.md from the built data (deterministic).
Usage: python3 scripts/rtt101_report.py [DATA_DIR] [REPORT_PATH]"""
import csv, json, os, sys, urllib.parse
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
zt = sorted({r["transfer_id"] for r in zero_rej}, key=lambda k: (TI[k]["date"], k))
with open(os.path.join(D, "tier1_max_or_approx_only.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["transfer_id", "player", "from_club", "to_club", "date", "season", "figures_found", "wording_and_why_not_counted"])
    for k in zt:
        t = TI[k]
        figs = sorted({f"{e['fee_text']} ({e['grade']}, {e['url']})" for e in EV[k] if e["amount"]})
        why = sorted({r["note"] for r in zero_rej if r["transfer_id"] == k})
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
          "Gillespie £1m; Manchester United's net is still the £6m cash. *Recommendation:* keep it (it follows the rule Luke approved)."]
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

    def why_of(t, f0, f1):
        k = t["transfer_id"]
        if k in DSR and DSR[k]["fee_amount"] != "":
            return DSR[k]["rule"]
        if k in d404:
            return "DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure"
        if abs(f1 - f0) < 1:
            return DSR[k]["rule"] if k in DSR else ""
        if t["fee_status"].startswith("undisclosed"):
            return "an A/B report calls the fee undisclosed or nominal: only an A/B figure counts (DEC-405 (a), DEC-237 (g))"
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
          "UNVERIFIED, and exist only from summer 2002):\n", "| Window | Gross before | Gross after | Change | Published gross | Net before | Net after |",
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
    QB = [l.strip() for l in open(os.path.join(D, "source", "questions_listB.md"), encoding="utf-8") if l.strip()] \
        if os.path.exists(os.path.join(D, "source", "questions_listB.md")) else []
    R += ["\n**Questions for Luke on list B (each with Claude's recommendation)**\n"] + QB
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n".join(R) + "\n")
    print("section 12:", v0, "->", v1, "VERIFIED of", nB, ";", len(fees), "fees changed;", len(D404), "DEC-404 changes;", len(lead_ch), "leader changes")
