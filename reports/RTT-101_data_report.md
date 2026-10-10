# RTT-101 Premier League net transfer spend — data report, phase 1 (IQ-15, 7 Oct 2026)

**Status: UNVERIFIED preview. Not for screen.** Only figures marked VERIFIED may ever be shown, and phase 2 (verification of Tier 1 at source, in batches) comes before any design work. Rules: `reference/metric_contract_RTT-101.md`; decisions DEC-235 to DEC-250 (and the findings recorded with this build).

Rebuild: `python3 scripts/build_rtt101_dataset.py && python3 scripts/rtt101_report.py` (deterministic; the private cross-checks need the private folder: `python3 scripts/rtt101_private_crosschecks.py <private research folder>` first).

## 1. What was built

- **14,201 transfer events** that involve a club in the Premier League that season (1992-93 to the freeze, 1 Sep 2026), of which **3,526 carry a fee** above £0. The rest are loans without a fee (6,125), free transfers (2,276), undisclosed fees with no figure, counted £0 (2,058), and fees not found (159).
- Fee status: **VERIFIED 2,282**, UNVERIFIED 1,244. Grade of the fee used: A 37, B 2,266, C (Wikipedia pointer only) 1,223, D 0.
- Tiers (DEC-248): Tier 1 **1,985**, Tier 2 823, Tier 3 732 (5% sample: 37).
  Tier 1 reasons (a transfer can have several): removal changes the leader or the top 12 1,054; fee >= £20m 557; club or British record (research lead) 528; alternative fee version changes the leader or the top 12 17; disputed fee (research section C) 10.
- 20,797 evidence rows in `fee_evidence.csv`; 5,207 sources in `sources.csv`; 870 transfers with more than one fee version (`conflicts.csv`).
- **Scripted source check** (GitHub runner, 6,226 cited pages): VERIFIED 5,571; page fetched but figure not found near the player's name 559; blocked or gone 81.
  Tier 2 result: 452 of 823 Tier 2 fees VERIFIED by the scripted check.
  Tier 3 sample: 5 of 37 VERIFIED; most Tier 3 rows have no fetchable citation (error rate cannot be published yet: phase 2).

## 2. Checks

| Check | Result | Detail |
|---|---|---|
| 22 clubs per season 1992-95, 20 after (706 club-seasons) | **PASS** | 706 club-seasons in 35 seasons |
| every season has an attribution window | **PASS** | 1992-05-03 to 2026-09-01 |
| 51 clubs, each with at least one PL season | **PASS** | 51 clubs |
| no transfer counted outside its club's PL seasons | **PASS** | 3984 ledger rows frozen (club not in the PL) |
| PL-to-PL deals net to zero (spend - income of PL clubs = net spend with non-PL clubs) | **PASS** | spend £29,160,249,929 − income £15,254,995,851 = £13,905,254,077; net with non-PL clubs £13,905,254,077 |
| no fee without a source row | **PASS** | 3526 fee-bearing transfers |
| no Transfermarkt figure or URL anywhere | **PASS** | none found |
| quotes under 25 words | **PASS** | 20797 evidence rows |
| every conversion has a rate row | **PASS** | 123 conversions |
| month-end series consistent with the ledger (all-fees preview, and the on-screen series from VERIFIED fees only) | **PASS** | 413 month ends × 51 clubs, two series |
| no window has under half the PL deals of the same-type windows either side (bar documented gaps) | **PASS** | 69 windows compared; documented gaps (DEC-431): none |
| every list-page row has a date (IQ-15j: undated rows are dropped from the build) | **PASS** | 20905 rows |
| Bank of England Jan 1992 monthly averages equal Cowork's V-04 reading | **PASS** | 7 of 7 series compared |
| ECB GBP/EUR 1999-01 equals Cowork's V-06 reading (0.7029125) | **PASS** | 333 months |
| no amount rejection silently removes a research lead that quotes the player with that figure | **PASS** | all such rejections were weighed against the lead |
| runner surname test matches hyphenated and apostrophe surnames | **PASS** | Wright-Phillips, O'Kane, Guivarc'h, Wan-Bissaka, Darmian |
| CPI base month recorded | **PASS** | D7BT 2026-08 = 143.6 (September 2026 not yet published at build time) |

Plus the private cross-checks in `data/rtt-101/CHECKS.md` (membership equals research file part03b; its differences are the two known flag errors and points deductions it ignores).

## 3. Leaders over time (UNVERIFIED preview)

First place at each month end, nominal cumulative net spend; a change is listed when first place changes hands.

| From month end | Leader | Value then |
|---|---|---|
| 1992-05-31 | Arsenal | £0.0m |
| 1992-07-31 | Blackburn Rovers | £4.0m |
| 1993-07-31 | Liverpool | £5.7m |
| 1993-09-30 | Blackburn Rovers | £8.2m |
| 1995-07-31 | Liverpool | £22.9m |
| 1996-07-31 | Newcastle United | £38.6m |
| 1997-12-31 | Liverpool | £33.2m |
| 1998-02-28 | Newcastle United | £34.4m |
| 1999-07-31 | Liverpool | £55.7m |
| 2000-06-30 | Chelsea | £67.7m |
| 2000-07-31 | Liverpool | £73.2m |
| 2001-07-31 | Manchester United | £85.4m |
| 2001-08-31 | Liverpool | £80.3m |
| 2001-11-30 | Leeds United | £82.7m |
| 2002-06-30 | Liverpool | £84.1m |
| 2002-07-31 | Manchester United | £93.7m |
| 2003-07-31 | Chelsea | £108.4m |
| 2015-08-31 | Manchester City | £708.8m |
| 2022-08-31 | Chelsea | £1.20bn |
| 2026-09-01 | Manchester United | £1.68bn |

## 4. Top 12 at key dates (UNVERIFIED preview)

**1993-05-31:** 1. Blackburn Rovers £5.5m; 2. Aston Villa £2.5m; 3. Manchester City £2.5m; 4. Sheffield Wednesday £2.0m; 5. Leeds United £1.9m; 6. Liverpool £0.9m; 7. Oldham Athletic £0.7m; 8. Chelsea £0.7m; 9. Ipswich Town £0.7m; 10. Manchester United £0.4m; 11. Arsenal £0.3m; 12. Newcastle United £0.0m

**1997-05-31:** 1. Newcastle United £37.8m; 2. Everton £20.9m; 3. Liverpool £20.3m; 4. Aston Villa £20.1m; 5. Middlesbrough £16.9m (out of the PL); 6. Chelsea £16.3m; 7. Arsenal £15.0m; 8. Coventry City £14.4m; 9. Leeds United £13.8m; 10. Sheffield Wednesday £12.5m; 11. Blackburn Rovers £9.7m; 12. Leicester City £8.9m

**2002-05-31:** 1. Leeds United £82.7m; 2. Chelsea £78.5m; 3. Liverpool £74.1m; 4. Newcastle United £69.5m; 5. Manchester United £65.7m; 6. Tottenham Hotspur £52.4m; 7. Middlesbrough £48.2m; 8. Aston Villa £47.9m; 9. Blackburn Rovers £44.3m; 10. Fulham £37.0m; 11. Arsenal £30.8m; 12. Sheffield Wednesday £25.5m (out of the PL)

**2005-05-31:** 1. Chelsea £275.8m; 2. Manchester United £130.2m; 3. Liverpool £104.4m; 4. Newcastle United £88.1m; 5. Tottenham Hotspur £82.8m; 6. Middlesbrough £78.4m; 7. Aston Villa £54.8m; 8. Manchester City £43.8m; 9. Sunderland £39.2m; 10. Blackburn Rovers £37.9m; 11. Arsenal £35.6m; 12. Birmingham City £29.2m

**2008-08-31:** 1. Chelsea £356.8m; 2. Liverpool £181.1m; 3. Manchester United £159.3m; 4. Aston Villa £122.6m; 5. Tottenham Hotspur £122.1m; 6. Middlesbrough £109.5m; 7. Newcastle United £107.5m; 8. Sunderland £93.4m; 9. Manchester City £89.9m; 10. Fulham £55.5m; 11. Birmingham City £47.2m (out of the PL); 12. Everton £45.6m

**2012-05-31:** 1. Chelsea £531.8m; 2. Manchester City £441.7m; 3. Liverpool £191.0m; 4. Manchester United £159.6m; 5. Tottenham Hotspur £144.6m; 6. Sunderland £131.9m; 7. Aston Villa £115.3m; 8. Middlesbrough £109.4m (out of the PL); 9. Birmingham City £80.9m (out of the PL); 10. Newcastle United £72.5m; 11. Stoke City £58.4m; 12. Fulham £52.0m

**2016-08-31:** 1. Manchester City £870.4m; 2. Chelsea £779.7m; 3. Manchester United £581.7m; 4. Liverpool £309.8m; 5. Sunderland £187.6m; 6. Tottenham Hotspur £158.7m; 7. Arsenal £129.9m; 8. Middlesbrough £127.2m; 9. Aston Villa £116.6m (out of the PL); 10. Stoke City £111.7m; 11. West Bromwich Albion £103.8m; 12. Leicester City £87.6m

**2020-10-31:** 1. Manchester City £1.19bn; 2. Chelsea £1.02bn; 3. Manchester United £878.8m; 4. Liverpool £441.8m; 5. Everton £366.7m; 6. Tottenham Hotspur £329.6m; 7. Arsenal £326.2m; 8. Aston Villa £295.4m; 9. West Ham United £216.2m; 10. Sunderland £195.1m (out of the PL); 11. Newcastle United £186.8m; 12. West Bromwich Albion £171.2m

**2023-09-30:** 1. Chelsea £1.68bn; 2. Manchester United £1.29bn; 3. Manchester City £1.28bn; 4. Arsenal £696.8m; 5. Liverpool £658.9m; 6. Newcastle United £543.1m; 7. Tottenham Hotspur £535.5m; 8. West Ham United £420.9m; 9. Aston Villa £393.7m; 10. Everton £337.7m; 11. AFC Bournemouth £269.3m; 12. Fulham £225.2m

**2026-09-01:** 1. Manchester United £1.68bn; 2. Chelsea £1.67bn; 3. Manchester City £1.64bn; 4. Arsenal £1.12bn; 5. Liverpool £989.1m; 6. Tottenham Hotspur £981.3m; 7. Newcastle United £703.0m; 8. West Ham United £590.5m (out of the PL); 9. Everton £373.4m; 10. Fulham £367.3m; 11. Sunderland £338.4m; 12. Aston Villa £314.7m

## 5. Coverage by era

Counts are club-sides (a PL-to-PL deal counts once for each club).

| Era | Transfers found | With a fee | Fee grade A/B | Fee VERIFIED | Undisclosed, no figure | Fee not found |
|---|---|---|---|---|---|---|
| 1992-2002 (no window lists) | 2,211 | 1,434 | 951 | 946 | 52 | 91 |
| 2002-2007 | 1,272 | 489 | 149 | 223 | 144 | 14 |
| 2007-2012 | 2,997 | 550 | 357 | 307 | 526 | 14 |
| 2012-2017 | 3,174 | 576 | 406 | 381 | 511 | 18 |
| 2017-2022 | 3,102 | 503 | 386 | 373 | 511 | 32 |
| 2022-2026 | 3,091 | 832 | 732 | 718 | 482 | 4 |

What the eras mean:
- **1992–2002:** no Wikipedia window lists exist (V-10). The finding list is the clubs' season pages (200 of 210 fetched; the ten Leeds United pages are titled "Leeds United A.F.C." and were not fetched in this round) plus the research leads. About a quarter of those pages have no transfer table at all, so this era is the least complete. Transfermarkt was not used (route A says to consult it only to spot omissions; nothing from it is stored).
- **2002–2007:** the early Wikipedia window lists are short (for example summer 2004 has 83 rows involving these clubs, summer 2005 has 76), so many smaller deals are missing.
- **From 2007:** the lists are full (500–800 rows a window), but most fees there are Wikipedia figures (grade C pointers) until the cited source is checked.

## 6. Biggest open conflicts

Transfers whose sources give different fees (never averaged; the canonical fee is the highest grade, then the earliest report). The ones marked for Luke are Tier 1 with a same-grade gap over 10% and £1m (brief §7).

| Player | From → To | Date | Fee used | Range | Tier | For Luke |
|---|---|---|---|---|---|---|
| Georginio Rutter | TSG 1899 Hoffenheim → Leeds United | 2023-01-14 | £0.0m (B) | £0.0m–£35.0m | 1 |  |
| Lucca Brughmans | Genk → Liverpool | 2026-09-01 | £0.0m (B) | £0.0m–£28.3m |  |  |
| Cesc Fàbregas | Arsenal → Barcelona | 2011-08-15 | £25.5m (B) | £12.8m–£35.2m | 1 |  |
| Carlos Tevez | Media Sports Investments → Manchester City | 2009-07-14 | £25.0m (B) | £25.0m–£45.0m | 1 | yes |
| Enzo Fernández | Chelsea → Manchester City | 2026-09-01 | £125.0m (B) | £107.1m–£125.0m | 1 |  |
| José Antonio Reyes | Sevilla → Arsenal | 2004-01-27 | £7.1m (B) | £7.1m–£24.2m | 1 |  |
| Archie Gray | Leeds United → Tottenham Hotspur | 2024-07-02 | £25.0m (B) | £25.0m–£40.0m | 1 |  |
| Michael Olise | Crystal Palace → Bayern Munich | 2024-07-07 | £50.0m (B) | £45.0m–£60.0m | 1 |  |
| Lucas Paquetá | Lyon → West Ham United | 2022-08-29 | £51.0m (B) | £36.5m–£51.0m | 1 |  |
| Andriy Shevchenko | A.C. Milan → Chelsea | 2006-05-31 | £30.8m (B) | £24.7m–£39.0m | 1 |  |
| Rodri | Manchester City → Barcelona | 2026-08-18 | £51.3m (B) | £51.3m–£65.4m | 1 | yes |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £75.8m (B) | £62.0m–£75.8m | 1 | yes |
| Harry Kane | Tottenham Hotspur → Bayern Munich | 2023-08-12 | £86.4m (B) | £86.4m–£100.0m | 1 |  |
| Wilfried Bony | Manchester City → Swansea City | 2017-08-31 | £12.0m (B) | £12.0m–£25.0m | 1 |  |
| Sávio | Troyes → Manchester City | 2024-07-18 | £21.1m (B) | £21.0m–£33.7m | 1 |  |
| Piero Hincapié | Bayer Leverkusen → Arsenal | 2026-06-25 | £34.5m (B) | £34.5m–£44.8m | 1 |  |
| Armando Broja | Chelsea → Burnley | 2025-08-08 | £10.0m (B) | £10.0m–£20.0m | 1 |  |
| Eliaquim Mangala | Porto → Manchester City | 2014-08-11 | £32.0m (B) | £32.0m–£42.0m | 1 |  |
| Sávio | Manchester City → Tottenham Hotspur | 2026-08-25 | £85.0m (B) | £75.0m–£85.0m | 1 |  |
| Morgan Gibbs-White | Wolverhampton Wanderers → Nottingham Forest | 2022-08-19 | £25.0m (B) | £25.0m–£35.0m | 1 |  |
| Richarlison | Everton → Tottenham Hotspur | 2022-07-01 | £50.0m (B) | £50.0m–£60.0m | 1 |  |
| David Luiz | Chelsea → Paris Saint-Germain | 2014-06-13 | £50.0m (B) | £40.0m–£50.0m | 1 | yes |
| Wayne Rooney | Everton → Manchester United | 2004-08-31 | £20.0m (B) | £20.0m–£30.0m | 1 |  |
| Nélson Semedo | Barcelona → Wolverhampton Wanderers | 2020-09-23 | £27.4m (A) | £27.4m–£37.0m | 1 |  |
| Luka Modrić | Tottenham Hotspur → Real Madrid | 2012-08-27 | £27.9m (B) | £23.7m–£33.0m | 1 | yes |

39 conflicts are for Luke in total (`conflicts.csv`, column `for_luke`).

## 7. League-wide window totals: our sums against published totals

Our sums are **fees only, Premier League clubs only, from this preview** (gross = fees paid by PL clubs; net = fees paid to non-PL clubs minus fees received from them). Published totals are research leads (UNVERIFIED). The Premier League's own figures (grade A) are the best comparison; the press figures are mostly Deloitte estimates. **Gaps are expected and are not forced to match.**

| Window | Our gross | Our net | Premier League gross (A) | PL net (A) | Press gross / net (B, first listed) |
|---|---|---|---|---|---|
| January 2003 | £36.6m | £17.0m | — | — | £35m / NOT FOUND (The Independent) |
| summer 2003 | £195.1m | £113.2m | — | — | £215m / NOT FOUND (The Independent) |
| summer 2005 | £227.2m | £110.8m | — | — | £235m / NOT FOUND (The Independent) |
| summer 2006 | £239.5m | £122.0m | — | — | £300m / NOT FOUND (BBC News) |
| summer 2008 | £404.2m | £175.2m | — | — | 500 million pounds / NOT FOUND (Reuters (via Rediff)) |
| January 2009 | £110.4m | £9.8m | — | — | about £160m / NOT FOUND (The Guardian (report) |
| summer 2009 | £404.4m | £57.3m | — | — | £460.4m / NOT FOUND (The Guardian) |
| January 2010 | £28.5m | £9.9m | £36.0m | £7.0m | £30m / NOT FOUND (The Guardian (report) |
| summer 2010 | £225.8m | £130.9m | — | — | around £350million / NOT FOUND (Sky Sports (reportin) |
| January 2011 | £199.1m | £79.8m | £209.3m | £77.3m | £225m / NOT FOUND (The Guardian (table ) |
| summer 2011 | £390.4m | £146.2m | — | — | NOT FOUND / £194m (The Guardian) |
| January 2012 | £48.2m | £5.5m | £67.4m | £24.5m | — |
| summer 2012 | £374.5m | £187.5m | — | — | around £490m / NOT FOUND (Sky News (reporting ) |
| January 2013 | £92.6m | £49.6m | £123.4m | £72.5m | £120m / £70m (Press Association (v) |
| summer 2013 | £558.6m | £351.0m | — | — | £630m / NOT FOUND (BBC Sport) |
| January 2014 | £120.0m | £36.2m | £128.8m | £26.9m | — |
| summer 2014 | £669.3m | £301.7m | £809.6m | £386.5m | £835m / £410m (Press Association (v) |
| January 2015 | £96.8m | £28.7m | £118.2m | £36.4m | £130million / around £40million (The Independent (Age) |
| summer 2015 | £744.0m | £377.1m | £858.6m | £432.6m | £870m / £460m (BBC Sport) |
| January 2016 | £124.0m | £51.0m | £177.5m | £108.9m | £175m / NOT FOUND (BBC Sport) |
| summer 2016 | £1.09bn | £724.6m | £1.12bn | £635.6m | £1.165bn / NOT FOUND (Sky Sports (reportin) |
| January 2017 | £163.5m | −£53.2m | £236.7m | −£4.0m | £215m / net £40m profit (Sky Sports) |
| summer 2017 | £1.40bn | £684.3m | £1.41bn | £665.0m | £1.43bn / NOT FOUND (Sky News) |
| January 2018 | £375.8m | £109.8m | £419.5m | £147.6m | £430m / NOT FOUND (BBC Sport / Deloitte) |
| summer 2018 | £963.5m | £721.5m | — | — | £1.23bn / £865m (Sky News) |
| January 2019 | £111.6m | £56.5m | — | — | £180m / NOT FOUND (Sky Sports) |
| summer 2019 | £1.16bn | £509.7m | — | — | £1.41billion / £625m (PA, syndicated by Ex) |
| January 2020 | £165.4m | £160.5m | — | — | £230m / £165m (BBC Sport) |
| summer 2020 | £1.09bn | £684.6m | — | — | £1.24bn / £813million (PA (Tom White), synd) |
| January 2021 | £50.0m | £14.0m | — | — | £70m / NOT FOUND (Sky News) |
| summer 2021 | £887.7m | £422.7m | — | — | £1.1billion / £560m (PA, syndicated by Fo) |
| January 2022 | £189.0m | £79.7m | — | — | £295m / £180m (Sky News) |
| summer 2022 | £1.76bn | £1.01bn | — | — | Estimates from Deloitte’s spor / NOT FOUND (The Guardian / Deloi) |
| January 2023 | £663.3m | £567.0m | — | — | around £780.1m / £675m (Sky Sports) |
| summer 2023 | £2.26bn | £1.03bn | — | — | £2.44bn / £1.07bn (Sky Sports) |
| January 2024 | £87.7m | £76.9m | — | — | £96.2m / NOT FOUND (Sky Sports) |
| summer 2024 | £1.88bn | £617.7m | — | — | £2.08bn / £627.4m (Sky Sports) |
| January 2025 | £341.4m | £217.5m | — | — | around £370m / NOT FOUND (BBC Sport) |
| summer 2025 | £2.89bn | £1.26bn | — | — | surpassed £3bn; £3.087bn / NOT FOUND (BBC Sport) |
| January 2026 | £336.6m | £110.3m | — | — | £397m / NOT FOUND (BBC Sport) |
| summer 2026 | £3.12bn | £1.22bn | — | — | around £3.46 billion / NOT FOUND (Reuters, syndicated ) |

Why the totals differ:
1. **Undisclosed fees count £0 here** (DEC-237 (g)); publishers estimate them. This is the biggest reason our gross is lower, especially in January windows and before 2010.
2. **Wikipedia's early lists are incomplete** (2002–2007), so whole deals are missing there.
3. **Add-ons, instalments and loan fees:** publishers often include "up to" totals or add-ons; we count only the guaranteed fee until add-ons are reported payable (DEC-237 (e)).
4. **Window boundaries:** we group by transfer date (April–October = summer, November–March = January); publishers use the window's legal dates and sometimes include deals agreed before the window.
5. **"Net" is measured differently:** the Premier League's net is spend minus receipts from clubs outside the PL; Deloitte's and the press's definitions vary (one source's "net £40m profit" for January 2017 against the League's −£4.0m).

## 8. Blocked or missing sources

- **Wikipedia** rate-limits the Claude Code container (HTTP 429), so every page was fetched on a GitHub runner (`rtt101_sources.yml`; no secrets, no artifacts; each page's revision ID is in `source/wiki_pages.csv`).
- **ONS, Bank of England, ECB, BBC, Sky, the Guardian and Transfermarkt** are blocked from the container; the reference data and the scripted check ran on the runner.
- **1991–92 last First Division matchday** (it sets the start of 1992–93's attribution window): Wikipedia's First Division page gives no end date; 2 May 1992 is a research lead, UNVERIFIED (`source/fixed_dates.csv`). It only matters for transfers between early May and mid-August 1992.
- **Leeds United 1992–2002 club-season pages:** not fetched in this round (wrong page title); next runner job.
- **Pages the scripted check could not read** (paywalls, dead links, robots) are listed in `source/runner_checks.csv` with their HTTP status; Claude in Cowork can open many of them in Luke's Chrome in phase 2.
- **Transfermarkt:** not used, not fetched, nothing stored (DEC-236). Phase 2 can use it in Luke's browser only to spot omissions, per route A.


## 9. Questions for Luke (each with Claude's recommendation)

1. **Tier 1 is too big as worded (DEC-253).** 1,985 transfers are Tier 1, mostly because of the "changes the top-12 order" test. *Recommendation:* keep £20m+, records and disputed fees, and narrow the order test to "changes the leader, or who is in the top 12, at any month end"; the rest get Tier 2's scripted check.
2. **Undisclosed fees count £0 (DEC-237 (g)).** 2,058 transfers have no reported figure. *Recommendation:* keep the rule, say on screen "Undisclosed fees not included", and give each club's undisclosed count in the description.
3. **The early years are the least complete (1992–2007).** *Recommendation:* in phase 2, Claude in Cowork uses Transfermarkt in your Chrome only as a finding list (route A, nothing stored) to spot missing 1992–2007 deals involving the bigger fees, and takes each fee from a press or club source.
4. **Relegated clubs keep their frozen bar and their rank** (contract §1; e.g. a relegated club can sit 8th at the freeze). *Recommendation:* keep them in the ranking; how a frozen bar looks is a design question for the pilot (DEC-069).
5. **Start of the race.** At 31 May 1992 every bar is £0 (the leader that month is only a tie-break). *Recommendation:* the film starts at the first month end with a fee (July 1992); the data stay as they are.
6. **Same-grade fee disagreements on Tier 1 transfers:** 39 are listed in `conflicts.csv` (column `for_luke`). *Recommendation:* phase 2 settles each at source; the ones still open after that come back to you as a short list.
7. **Claude's working choices** DEC-247 (finding list), DEC-248 (tiers), DEC-249 (board size later), DEC-250 (build details) and DEC-254 (how the scripted check marks a fee VERIFIED, and publisher grades). *Recommendation:* confirm them.
8. **Phase 2 first batch.** *Recommendation:* verify the Tier 1 fees of the clubs that lead or reach the top 3 (Chelsea, Manchester United, Manchester City, Arsenal, Liverpool, Newcastle, Blackburn, Everton) first, in batches of 50 (`tier1_list.csv`, column `batch`).

## 10. Phase 2 (IQ-15b): verification at source

- **Tier 1 (DEC-256):** 1,971 fee-bearing Tier 1 transfers; **1,659 VERIFIED at source** (1,607 by a club, league or press source, grade A/B; 52 only by a database such as Soccerbase, grade C; 0 only by a grade D site), each quote read by Claude (2,751 quotes accepted, 352 rejected; `source/review_decisions.csv`). The rest have no page that states the figure next to the player's name yet (mostly 1990s–2000s deals whose only sources are Wikipedia figures or dead links).
- **Tier 2:** 452 of 823 VERIFIED by the scripted check. **Tier 3 sample:** 5 of 37 VERIFIED.
- **Undisclosed fees (DEC-257):** 47 grade A/B reported figures found at the cited source and read by Claude, used and flagged "reported" (45 transfers; 37 close candidates rejected on reading: another deal, grade D, not a fee, or a total with add-ons; `source/reported_fees.csv`); every other candidate figure on those pages belonged to another deal, a wage, an offer or a fine.
- **1992–2007 gap list (DEC-264), sections A v2, B and C (1992–2007):** 137 new moves added, 102 VERIFIED (the page names the player, both clubs and the fee); the rest matched transfers already in the build. 6 gap rows have no transfer date (retrospective articles only) and are listed in `unmatched_leads.csv`.
- **Leeds United 1992–2002** pages added; **last 1991–92 First Division matchday 2 May 1992** confirmed by eight club fixture lists (pointers, grade C).
- **Root causes found by reading the batches, and fixed in the build** (each fix applies to every row, not only the one seen): player names inside Wikipedia sort templates; the same deal listed twice; research leads matched on surname only (Kylian Hazard had been given Eden Hazard's fee); club-season tables whose direction was read from prose, plus a Wikipedia table labelled "From" in an "Out" section (Newcastle 1998–99); figures that are maxima, offers, valuations, instalments, combined fees or totals including add-ons; a regression that had dropped pre-2002 research-lead transfers (restored); accented names not matched (ø, æ, ß and others); Soccerbase "Totals" lines and other rows of a career table read as this deal's fee (a Soccerbase figure now counts only from the row whose joining date is the transfer's); the same deal reported at two stages with a non-PL club not merged (Yobo, Baros); a reported figure attached to the same player's other moves.

### Same-grade fee conflicts not settled at source (DEC-261): 39, each settled by the contract's rule (DEC-277)

Settled at source = the fee used is confirmed at source and no differing same-grade figure is (totals including add-ons are not rivals). The deals below were not; Luke decided (DEC-277) that the existing rule settles them: best grade first, then the earliest report (a contemporary sterling figure from a grade A/B source preferred, contract §5). The last column says which step decided. Where no figure is confirmed at source yet, the fee stays UNVERIFIED (not on screen) and the deal is in the next research round.

| Player | From → To | Date | Fee used | Other confirmed figure(s) | Why not settled at source | Result under the rule (DEC-277) |
|---|---|---|---|---|---|---|
| Carlos Tevez | Media Sports Investments → Manchester City | 2009-07-14 | £25.0m (B) | B V according to reliable sources, £45m; B V around £25million; £45million claim denied; B V £25.5m | two same-grade sources confirm different figures | £25.0m (B, www.skysports.com): same grade; earliest report (2009-09-12) |
| Rodri | Manchester City → Barcelona | 2026-08-18 | £51.3m (B) | B V £65.4m; B V £65m; B V €60m | two same-grade sources confirm different figures | £51.3m (B, www.theguardian.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2026-08-18) |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £75.8m (B) | B V £62m; B V £75.8m; B V €80m plus €20m in add-ons; £89m | two same-grade sources confirm different figures | £75.8m (B, www.skysports.com): same grade; the contemporary sterling figure is preferred (contract §5) |
| David Luiz | Chelsea → Paris Saint-Germain | 2014-06-13 | £50.0m (B) | B V £40m; B V £50m | two same-grade sources confirm different figures | £50.0m (B, www1.skysports.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2014-06-13) |
| Luka Modrić | Tottenham Hotspur → Real Madrid | 2012-08-27 | £27.9m (B) | B V Spanish media reported Real would pay $43.81m plus a pos; B V in the region of €35m according to reports; B V €30 million | two same-grade sources confirm different figures | £27.9m (B, www.aljazeera.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2012-08-27) |
| Martín Zubimendi | Real Sociedad → Arsenal | 2025-07-06 | £60.0m (B) | B V almost £60m; B V £51m; B V £60m | two same-grade sources confirm different figures | £60.0m (B, www.bbc.co.uk): same grade; earliest report (2025-07-06) |
| Gareth Bale | Tottenham Hotspur → Real Madrid | 2013-09-01 | £85.3m (B) | B V 100m euros; B V Real claimed €91m; B V thought to be a world record figure of €100m | two same-grade sources confirm different figures | £85.3m (B, www.bbc.co.uk): same grade; the contemporary sterling figure is preferred (contract §5) |
| Viktor Gyökeres | Sporting CP → Arsenal | 2025-07-26 | £55.1m (B) |  | the fee used is not yet confirmed at source | £55.1m (B, www.skysports.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Roberto Firmino | TSG Hoffenheim → Liverpool | 2015-06-24 | £21.3m (B) | B V about £29m; B V £21.3m now; could eventually rise to £28m; B V £29.5m | two same-grade sources confirm different figures | £21.3m (B, www.skysports.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2015-06-24) |
| Henrikh Mkhitaryan | Borussia Dortmund → Manchester United | 2016-07-06 | £26.3m (B) | B V understood to have cost £26million, although the fee has; B V undisclosed fee believed to be £30m; B V £26.3m | two same-grade sources confirm different figures | £26.3m (B, www.foxnews.com): same grade; earliest report (2016-06-27) |
| Michael Turner | Hull City → Sunderland | 2009-08-31 | £12.0m (B) | B V £12m; B V £12m; believed to be in the region of £12m; B V £12million | two same-grade sources confirm different figures | £12.0m (B, www.theguardian.com): same grade; earliest report (2009-08-31) |
| André-Frank Zambo Anguissa | Marseille → Fulham | 2018-08-09 | £30.0m (B) | B V Sky Sports News understands to be £22.3m; B V around £30m | two same-grade sources confirm different figures | £30.0m (B, www.theguardian.com): same grade; earliest report (2018-08-09) |
| Aleksandar Mitrović | Fulham → Al Hilal | 2023-08-19 | £50.0m (B) | B V 50 million euros; B V £50m | two same-grade sources confirm different figures | £50.0m (B, www.bbc.co.uk): same grade; earliest report (2023-08-19) |
| Willian | Anzhi Makhachkala → Chelsea | 2013-08-28 | £32.0m (B) | B V thought to be in the region of £25.5m; B V £32m | two same-grade sources confirm different figures | £32.0m (B, www.theguardian.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2013-08-28) |
| Matteo Sereni | Sampdoria → Ipswich Town | 2001-08-17 | £0.0m (B) | B V around £6m; B V believed to be around £4.5 million sterling; B V £4.5 million | two same-grade sources confirm different figures | £0.0m (B, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Timo Werner | RB Leipzig → Chelsea | 2020-07-01 | £53.0m (B) | B V £47.5m; B V £53m release clause | two same-grade sources confirm different figures | £53.0m (B, www.theguardian.com): same grade; earliest report (2020-06-04) |
| Richarlison | Watford → Everton | 2018-07-24 | £35.0m (B) | B V around £40m; B V potential £50m deal | two same-grade sources confirm different figures | £35.0m (B, www.bbc.co.uk): same grade; earliest report (2018-07-24) |
| Fred | Shakhtar Donetsk → Manchester United | 2018-06-21 | £47.0m (B) | B V believed to be £52m; B V £47m | two same-grade sources confirm different figures | £47.0m (B, www.bbc.co.uk): same grade; earliest report (2018-06-21) |
| Sofiane Boufal | Lille → Southampton | 2016-08-29 | £21.0m (B) | B V Sky sources understand the fee to be a club-record £16m; B V £21m according to sources at the south-coast club | two same-grade sources confirm different figures | £21.0m (B, www.skysports.com): same grade; earliest report (2016-08-25) |
| Álvaro Negredo | Manchester City → Valencia | 2015-06-08 | £21.3m (B) | B V £20m; B V £21.3m; B V £23.7m | two same-grade sources confirm different figures | £21.3m (B, www.skysports.com): same grade; earliest report (2015-07-01) |
| Stevan Jovetić | Fiorentina → Manchester City | 2013-07-19 | £22.0m (B) | B V about $40m; B V £22million | two same-grade sources confirm different figures | £22.0m (B, mancunianmatters.co.uk): same grade; the contemporary sterling figure is preferred (contract §5) |
| David Luiz | Paris Saint-Germain → Chelsea | 2016-08-31 | £34.0m (B) | B V around £34m; B V believed to be in the region of £30m; B V £34m, with further fees due in future | two same-grade sources confirm different figures | £34.0m (B, www.theguardian.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2016-08-31) |
| Jeremain Lens | Dynamo Kyiv → Sunderland | 2015-07-15 | £8.0m (B) |  | the fee used is not yet confirmed at source | £8.0m (B, english.ahram.org.eg): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Robbie Fowler | Leeds United → Manchester City | 2003-01-30 | £3.0m (B) | B V around £7million; B V £3m cash [€4.5m] agreed fee with further payments of up ; B V €9m | two same-grade sources confirm different figures | £3.0m (B, www.uefa.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2003-01-30) |
| Robbie Keane | Liverpool → Tottenham Hotspur | 2009-02-02 | £15.0m (B) |  | the fee used is not yet confirmed at source | £15.0m (B, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Matthew Upson | Arsenal → Birmingham City | 2003-01-22 | £3.0m (C) |  | the fee used is not yet confirmed at source | £3.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| James Milner | Newcastle United → Aston Villa | 2008-08-29 | £12.0m (B) | B V believed to be in the region of £10m; B V £12m | two same-grade sources confirm different figures | £12.0m (B, www.theguardian.com): same grade; earliest report (2008-08-29) |
| Igor Biscan | Dinamo Zagreb → Liverpool | 2000-12-07 | £7.0m (B) | B V £5.5m; B V £5m; B V £7m | two same-grade sources confirm different figures | £7.0m (B, www.theguardian.com): same grade; earliest report (2000-10-13) |
| Emanuele Giaccherini | Juventus → Sunderland | 2013-07-16 | £6.5m (B) |  | the fee used is not yet confirmed at source | £6.5m (B, www.foxnews.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Abdoulaye Doucouré | Stade Rennais → Watford | 2016-02-01 | £8.0m (B) |  | the fee used is not yet confirmed at source | £8.0m (B, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Pascal Chimbonda | Wigan Athletic → Tottenham Hotspur | 2006-08-31 | £4.5m (C) |  | the fee used is not yet confirmed at source | £4.5m (C, www.skysports.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Steve Howey | Newcastle United → Manchester City | 2000-08-31 | £2.0m (B) | B V £2m; The fee could rise to £3m; B V £3.5m | two same-grade sources confirm different figures | £2.0m (B, www.independent.co.uk): same grade; earliest report (2000-08-11) |
| Nwankwo Kanu | Internazionale → Arsenal | 1999-01-15 | £3.0m (B) | B V believed to be around pounds 4.5m; B V pounds 3m; B V pounds 4.5m | two same-grade sources confirm different figures | £3.0m (B, www.the-independent.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 1999-01-29) |
| Danny Murphy | Crewe Alexandra → Liverpool | 1997-07-15 | £1.5m (B) | B V could eventually be worth Pounds 3 million; B V initial payment of Pounds 1.5 million; B V pounds 1.5m down payment plus another pounds 3m in insta | two same-grade sources confirm different figures | £1.5m (B, www.irishtimes.com): same grade; earliest report (1997-07-09) |
| Nampalys Mendy | Nice → Leicester City | 2016-07-03 | £12.0m (B) | B V around €16 million; B V close to £12 million | two same-grade sources confirm different figures | £12.0m (B, www.balls.ie): same grade; the contemporary sterling figure is preferred (contract §5) |
| Didier Deschamps | Chelsea → Valencia | 2000-07-28 | £2.3m (B) | B V £2.3m; B V £3.7m | two same-grade sources confirm different figures | £2.3m (B, www.theguardian.com): same grade; earliest report (2000-07-29) |
| Faustino Asprilla | Newcastle United → Parma | 1998-01-31 | £7.3m (B) | B V pounds 6m; B V pounds 7.3m | two same-grade sources confirm different figures | £7.3m (B, www.independent.co.uk): same grade; earliest report (1998-01-15) |
| Nick Barmby | Middlesbrough → Everton | 1996-10-30 | £5.7m (B) | B V pounds 4.5m; B V pounds 5.3m; B V pounds 5.75m | two same-grade sources confirm different figures | £5.7m (B, www.the-independent.com): same grade; earliest report (1996-11-17) |
| Christos Tzolis | PAOK → Norwich City | 2021-08-12 | £8.8m (B) | B V around £10m; B V £8.8m | two same-grade sources confirm different figures | £8.8m (B, www.bbc.co.uk): same grade; earliest report (2021-08-12) |

### Effect of the 1992–2007 gap list (sections A v2, B, C) on window totals, 1997–2007

Our sums count fees paid by PL clubs (gross) and fees paid to minus received from non-PL clubs (net); undisclosed fees count £0. "Before" = the build just before sections A v2, B and C were added (`source/window_totals_before_gap_list_v2.csv`). Published totals are research leads (part17b, UNVERIFIED); none exist for windows before summer 2002 (no window system).

"Change" also includes the corrections made by reading the sources since that snapshot (for example a maximum replaced by the guaranteed fee); "of which gap list" is the gross paid by PL clubs in all moves the gap list created (section A's first version, part18b, was already in the snapshot, so this column can exceed the change).

| Window | Gross before | Gross after | Change | of which gap list | Published gross (first A/B source) | Gap left | Net before | Net after |
|---|---|---|---|---|---|---|---|---|
| January 1997 | £41.5m | £44.2m | £2.8m | £15.4m | — | — | £12.4m | £13.5m |
| summer 1997 | £116.2m | £141.2m | £24.9m | £25.6m | — | — | £30.9m | £55.9m |
| January 1998 | £49.6m | £50.0m | £0.4m | £1.3m | — | — | £10.5m | £15.3m |
| summer 1998 | £128.7m | £163.6m | £34.9m | £33.4m | — | — | £49.4m | £82.8m |
| January 1999 | £82.6m | £92.0m | £9.4m | £9.6m | — | — | £28.6m | £34.3m |
| summer 1999 | £136.1m | £166.2m | £30.1m | £35.7m | — | — | £28.6m | £52.4m |
| January 2000 | £42.1m | £37.2m | −£4.8m | £1.0m | — | — | £19.5m | £18.3m |
| summer 2000 | £241.3m | £243.3m | £2.0m | £17.5m | — | — | £97.1m | £92.3m |
| January 2001 | £58.6m | £67.0m | £8.4m | £7.0m | — | — | −£11.9m | −£5.1m |
| summer 2001 | £264.2m | £282.7m | £18.5m | £32.8m | — | — | £150.2m | £169.2m |
| January 2002 | £56.1m | £64.1m | £8.1m | £6.3m | — | — | £22.2m | £33.8m |
| summer 2002 | £174.2m | £174.7m | £0.5m | £0.0m | — | — | £114.4m | £115.3m |
| January 2003 | £36.8m | £36.6m | −£0.2m | £3.0m | £35.0m (B, The Independent) | −£1.6m | £14.2m | £17.0m |
| summer 2003 | £212.4m | £195.1m | −£17.4m | £0.0m | £215.0m (B, The Independent) | £19.9m | £120.3m | £113.2m |
| January 2004 | £61.1m | £45.8m | −£15.3m | £0.0m | — | — | £34.6m | £18.8m |
| summer 2004 | £172.0m | £210.1m | £38.1m | £33.0m | — | — | £99.3m | £134.6m |
| January 2005 | £41.2m | £44.0m | £2.8m | £2.8m | — | — | £12.8m | £14.6m |
| summer 2005 | £195.3m | £227.2m | £31.8m | £28.4m | £235.0m (B, The Independent) | £7.8m | £81.4m | £110.8m |
| January 2006 | £51.2m | £58.1m | £6.9m | £0.0m | — | — | £41.7m | £41.6m |
| summer 2006 | £239.8m | £239.5m | −£0.4m | £4.7m | £300.0m (B, BBC News) | £60.5m | £118.4m | £122.0m |
| January 2007 | £37.5m | £41.3m | £3.9m | £3.0m | — | — | £17.9m | £17.2m |
| summer 2007 | £324.6m | £349.6m | £25.0m | £0.0m | — | — | £166.2m | £161.7m |

Total gross 1997–2007: £2.76bn before, £2.97bn after (£210.3m net change, of which £260.5m paid in moves the gap list added). Where a published total exists, our sum stays below it mainly because undisclosed fees count £0 and the early Wikipedia window lists are short; the gap list narrows the gap but does not close it, and no figure is forced to match.

### Leader sequence after phase 2

Leader at each change (month end): 1992-05 Arsenal; 1992-07 Blackburn Rovers; 1993-07 Liverpool; 1993-09 Blackburn Rovers; 1995-07 Liverpool; 1996-07 Newcastle United; 1997-12 Liverpool; 1998-02 Newcastle United; 1999-07 Liverpool; 2000-06 Chelsea; 2000-07 Liverpool; 2001-07 Manchester United; 2001-08 Liverpool; 2001-11 Leeds United; 2002-06 Liverpool; 2002-07 Manchester United; 2003-07 Chelsea; 2015-08 Manchester City; 2022-08 Chelsea; 2026-09 Manchester United.


### Phase 2 questions — answered by Luke (YES to all four, 7 Oct 2026: DEC-274 to DEC-277)

1. **Database-only Tier 1 figures.** 52 Tier 1 fees are confirmed only by a grade C source (52 of them a Soccerbase row for that move) and 0 only by a source graded D (mostly later retrospective articles). May a Soccerbase row count as VERIFIED for screen? *Recommendation:* yes for Soccerbase rows (they are dated career tables, checked row by row), no for grade D; keep looking for press sources for both.
2. **Next research round.** 364 Tier 1 fees still have no VERIFIED club, league or press source (`data/rtt-101/tier1_needs_press_source.csv`, mostly 1992–2007). *Recommendation:* one more ChatGPT deep-research round on that list (a press or club URL and a short quote per deal, leads only; every figure checked at source here), starting with 1992–2002.
3. **Fees known only as a maximum or an approximation.** 11 deals count £0 because every figure found is a maximum, a total including add-ons, or an approximation ("just under £30m", "in excess of £13m", "£40m-plus"). *Recommendation:* keep £0 (DEC-237 (e)) and add these deals to the next research round to find the guaranteed fee.
4. **Same-grade conflicts.** 39 remain (table above). *Recommendation:* use the rule already in the contract (highest grade, then the earliest contemporary report) for all of them, and list them in the description notes; Luke can overrule any single deal.

**Luke's answers:** (1) a Soccerbase row counts as VERIFIED, grade C, labelled "database source" (`transfers.csv` column `verified_by`); other grade C and grade D sources do not confirm a fee (DEC-274). (2) One more ChatGPT deep-research round on `tier1_needs_press_source.csv`, starting with 1992–2002; every figure is a lead to check at source here (DEC-275). (3) The deals known only as a maximum or an approximation stay at £0 and are listed in `data/rtt-101/tier1_max_or_approx_only.csv` for a later round (DEC-276). (4) The same-grade conflicts are settled by the rule, with the result for each in the table above (DEC-277).

## 11. Source round 1, list A: 1992–93 to 1996–97 (DEC-275, IQ-15d)

- **Deals:** 211 (A0001–A0211), mapped to our transfers by player and date (`source/source_round1_map.csv`). ChatGPT's answers (private part20b/d/f) were added as leads (`found_via` of each evidence row: "ChatGPT source round 1 (DEC-264 route)") and every cited page was read on the GitHub runner: the figure next to the player's name, and both clubs named on the page.
- **VERIFIED:** 165 of the 211 deals now have a fee confirmed at source (153 by a club, league or press source; the rest by a Soccerbase row), up from 41 before this round.
- **Changed:** 57 fees changed (£7.2m up, £13.0m down; net −£5.8m) and 14 completion dates moved to the date a grade B report gives.
- **Deal structures** (`source/deal_structure.csv`, one row per transfer with its source, quote and rule): a combined fee is booked once on one transfer of the pair and the partner counts £0 (no split invented); a part-exchange counts a player valuation on both sides only where a source states it, otherwise cash only; add-ons count only when reported as payable; a loan fee is a loan fee.

| Deal | Player | Move | Date before → after | Fee before | Fee after | Why |
|---|---|---|---|---|---|---|
| A0001 | Darren Anderton | Portsmouth → Tottenham Hotspur | 1992-07-01 | £1,750,000 | £1,700,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0004 | Mal Donaghy | Manchester United → Chelsea | 1992-07-01 | £100,800 | £150,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0006 | Scott Sellars | Blackburn Rovers → Leeds United | 1992-07-01 | £800,000 | £720,000 | sell-on (DEC-238): the buyer was the former club holding the sell-on share, so the cash both clubs saw was £720,000 |
| A0007 | Jason Cundy | Chelsea → Tottenham Hotspur | 1992-07-02 | £850,000 | £800,000 | higher grade or earlier report (C, www.independent.co.uk) |
| A0009 | David Lowe | Ipswich Town → Leicester City | 1992-07-13 | £300,000 | £200,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0014 | Mark Robins | Manchester United → Norwich City | 1992-08-14 | £850,000 | £800,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0015 | Derek Brazil | Manchester United → Cardiff City | 1992-08-24 | £185,000 | £85,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0021 | Kieran Toal | Manchester United → Motherwell | 1993-03-19 | £320,000 | £0 | higher grade or earlier report (B, www.independent.co.uk) |
| A0026 | Russell Beardsmore | Manchester United → AFC Bournemouth | 1993-06-29 | £210,000 | £0 | higher grade or earlier report (B, www.the-independent.com) |
| A0030 | Alex Mathie | Greenock Morton → Newcastle United | 1993-07-30 | £250,000 | £285,000 | higher grade or earlier report (B, www.the-independent.com) |
| A0031 | Jason Dozzell | Ipswich Town → Tottenham Hotspur | 1993-08-01 | £1,900,000 | £1,750,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0032 | Guy Whittingham | Portsmouth → Aston Villa | 1993-08-03 → 1993-08-04 | £1,200,000 | £875,000 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0036 | David Kerslake | Leeds United → Tottenham Hotspur | 1993-09-01 | £450,000 | £500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0044 | Darren Ferguson | Manchester United → Wolverhampton Wanderers | 1994-01-13 | £320,000 | £250,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0046 | Liam O'Brien | Newcastle United → Tranmere Rovers | 1994-01-21 | £300,000 | £250,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0049 | Peter Beagrie | Everton → Manchester City | 1994-03-31 | £1,100,000 | £1,000,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0050 | Julian Dicks | Liverpool → West Ham United | 1994-05-20 → 1994-10-20 | £1,000,000 | £100,000 | add-ons only when reported as triggered (DEC-237 (e)) |
| A0051 | Michael Stensgaard | Hvidovre IF → Liverpool | 1994-06-01 | £400,000 | £20,000 | higher grade or earlier report (B, www.the-independent.com) |
| A0052 | Peter Atherton | Coventry City → Sheffield Wednesday | 1994-06-01 → 1994-07-13 | £800,000 | £800,000 | completion date from a grade B report (contract §2) |
| A0055 | Joey Beauchamp | Oxford United → West Ham United | 1994-06-22 → 1994-06-21 | £1,000,000 | £1,000,000 | completion date from a grade B report (contract §2) |
| A0058 | Nicky Mohan | Middlesbrough → Leicester City | 1994-07-07 → 1994-08-16 | £330,000 | £330,000 | completion date from a grade B report (contract §2) |
| A0067 | Jürgen Klinsmann | Monaco → Tottenham Hotspur | 1994-08-03 | £2,300,000 | £2,000,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0070 | Dan Petrescu | Genoa → Sheffield Wednesday | 1994-08-06 → 1994-08-07 | £1,300,000 | £1,300,000 | completion date from a grade B report (contract §2) |
| A0071 | Philippe Albert | Anderlecht → Newcastle United | 1994-08-10 | £2,700,000 | £2,650,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0072 | David Rocastle | Manchester City → Chelsea | 1994-08-12 → 1994-08-11 | £1,250,000 | £1,250,000 | completion date from a grade B report (contract §2) |
| A0073 | Adrian Whitbread | Swindon Town → West Ham United | 1994-08-17 | £500,000 | £750,000 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0075 | Joey Beauchamp | West Ham United → Swindon Town | 1994-08-18 | £850,000 | £1,100,000 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0076 | Klas Ingesson | PSV Eindhoven → Sheffield Wednesday | 1994-09-01 | £800,000 | £2,000,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0078 | Colin McKee | Manchester United → Kilmarnock | 1994-09-05 | £350,000 | £530,000 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |
| A0079 | David Burrows | West Ham United → Everton | 1994-09-06 | £1,100,000 | £0 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0080 | Tony Cottee | Everton → West Ham United | 1994-09-07 | £1,000,000 | £0 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0089 | Guy Whittingham | Aston Villa → Sheffield Wednesday | 1994-12-21 | £700,000 | £0 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0090 | Ian Taylor | Sheffield Wednesday → Aston Villa | 1994-12-21 | £1,000,000 | £250,000 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0092 | Gary Charles | Derby County → Aston Villa | 1995-01-06 | £1,450,000 | £2,900,000 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |
| A0093 | Jamie Lawrence | Doncaster Rovers → Leicester City | 1995-01-06 | £125,000 | £175,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0094 | Neil Shipperley | Chelsea → Southampton | 1995-01-06 | £1,250,000 | £1,200,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0095 | Tommy Johnson | Derby County → Aston Villa | 1995-01-06 | £1,450,000 | £0 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |
| A0101 | Franz Carr | Leicester City → Aston Villa | 1995-02-10 | £250,000 | £0 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0102 | Garry Parker | Aston Villa → Leicester City | 1995-02-10 | £300,000 | £550,000 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0106 | John Filan | Cambridge United → Coventry City | 1995-03-02 | £300,000 | £350,000 | higher grade or earlier report (C, www.independent.co.uk) |
| A0110 | Brett Angell | Everton → Sunderland | 1995-03-23 | £600,000 | £500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0111 | Chris Swailes | Doncaster Rovers → Ipswich Town | 1995-03-23 | £225,000 | £150,000 | guaranteed fee where the other figure is the 'rising to' total (DEC-265 (d)) |
| A0113 | Calita | Farense → Coventry City | 1995-06-07 | £250,000 | £125,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0117 | Chris Bart-Williams | Sheffield Wednesday → Nottingham Forest | 1995-07-01 → 1995-08-08 | £2,500,000 | £2,500,000 | completion date from a grade B report (contract §2) |
| A0126 | Gary Rowett | Everton → Derby County | 1995-07-20 | £300,000 | £0 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0133 | Sean Flynn | Coventry City → Derby County | 1995-08-11 | £225,000 | £250,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0134 | Robbie Slater | Blackburn Rovers → West Ham United | 1995-08-14 | £600,000 | £0 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0135 | Matty Holmes | West Ham United → Blackburn Rovers | 1995-08-15 | £1,200,000 | £600,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0137 | Jeroen Boere | West Ham United → Crystal Palace | 1995-09-07 | £375,000 | £350,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0138 | Iain Dowie | Crystal Palace → West Ham United | 1995-09-08 → 1995-09-04 | £500,000 | £475,000 | completion date from a grade B report (contract §2) |
| A0153 | Noel Whelan | Leeds United → Coventry City | 1995-12-16 → 1995-12-11 | £2,000,000 | £2,000,000 | completion date from a grade B report (contract §2) |
| A0154 | Chris Coleman | Crystal Palace → Blackburn Rovers | 1995-12-21 → 1995-12-14 | £2,800,000 | £2,800,000 | completion date from a grade B report (contract §2) |
| A0155 | Darko Kovačević | Red Star Belgrade → Sheffield Wednesday | 1995-12-22 | £3,000,000 | £2,500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0159 | Nigel Clough | Liverpool → Manchester City | 1996-01-24 | £1,500,000 | £1,000,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0160 | Slaven Bilic | Karlsruhe → West Ham United | 1996-02-04 | £1,300,000 | £1,200,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0164 | David Batty | Blackburn Rovers → Newcastle United | 1996-02-24 | £3,750,000 | £4,000,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0165 | Julian Joachim | Leicester City → Aston Villa | 1996-02-24 | £1,890,000 | £1,500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0171 | Garry Flitcroft | Manchester City → Blackburn Rovers | 1996-03-28 | £3,500,000 | £3,200,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0173 | Alex Rae | Millwall → Sunderland | 1996-06-01 | £1,000,000 | £750,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0174 | Gary Speed | Leeds United → Everton | 1996-07-01 → 1996-06-21 | £3,500,000 | £3,500,000 | completion date from a grade B report (contract §2) |
| A0176 | Ben Thatcher | Millwall → Wimbledon | 1996-07-05 → 1996-07-03 | £1,700,000 | £1,700,000 | completion date from a grade B report (contract §2) |
| A0177 | Matt Clarke | Rotherham United → Sheffield Wednesday | 1996-07-11 | £325,000 | £300,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0184 | Scott Oakes | Luton Town → Sheffield Wednesday | 1996-08-07 | £425,000 | £700,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0191 | Steffen Iversen | Rosenborg → Tottenham Hotspur | 1996-12-02 → 1996-12-05 | £2,500,000 | £2,600,000 | completion date from a grade B report (contract §2) |
| A0205 | John Hartson | Arsenal → West Ham United | 1997-02-14 | £3,300,000 | £5,000,000 | higher grade or earlier report (B, www.the-independent.com) |
| A0208 | Des Hamilton | Bradford City → Newcastle United | 1997-03-27 | £1,500,000 | £2,500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0211 | Mark McKeever | Peterborough United → Sheffield Wednesday | 1997-04-15 | £500,000 | £0 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |

**Same-grade disagreements within list A** (9 deals; all below the 10% and £1m threshold of Luke's conflict list, so the rule settles them: best grade, then the earliest report, DEC-277; a report with no stated date ranks after a dated one):

| Deal | Player | Fee used (report date) | Other confirmed figure(s), same grade (report date) |
|---|---|---|---|
| A0009 | David Lowe | £200,000 (B, 1992-08-07) | £250,000 (1992-07-21) |
| A0056 | Andy Preece | £350,000 (B, 1994-06-24) | £275,000 (1994-10-24) |
| A0082 | Paul Kitson | £2,250,000 (B, 1994-10-24) | £2,500,000 (1994-09-24) |
| A0110 | Brett Angell | £500,000 (B, 1995-03-23) | £600,000 (1995-03-24) |
| A0160 | Slaven Bilic | £1,200,000 (B, 1996-01-04) | £1,650,000 (1996-01-18) |
| A0164 | David Batty | £4,000,000 (B, 1996-03-01) | £3,750,000 (1996-02-26) |
| A0169 | Ilie Dumitrescu | £1,500,000 (B, 1996-01-19) | £1,200,000 (1996-02-27) |
| A0180 | Nigel Martyn | £2,250,000 (B, 1996-07-25) | £2,100,000 (1996-07-30) |
| A0194 | Ramon Vega | £3,750,000 (B, 1997-01-20) | £3,000,000 (1997-01-07), £3,700,000 (1997-01-13) |

**League-wide spending by window, 1992–97** (before = commit 111a018; there are no published window totals for these years, when there were no transfer windows, so nothing to compare against):

| Window | Gross before | Gross after | Change |
|---|---|---|---|
| summer 1992 | £34.1m | £33.9m | −£0.2m |
| January 1993 | £9.1m | £9.1m | £0.0m |
| summer 1993 | £39.6m | £39.1m | −£0.5m |
| January 1994 | £16.2m | £16.1m | −£0.1m |
| summer 1994 | £73.3m | £70.4m | −£2.9m |
| January 1995 | £41.6m | £41.1m | −£0.5m |
| summer 1995 | £109.4m | £108.1m | −£1.3m |
| January 1996 | £54.6m | £53.9m | −£0.7m |
| summer 1996 | £102.8m | £103.1m | £0.3m |
| January 1997 | £41.5m | £44.2m | £2.8m |

**Effect on the race:** the leader changes at 13 month ends (1997-07: Liverpool → Newcastle United; 1997-08: Liverpool → Newcastle United; 1997-09: Liverpool → Newcastle United; 1997-10: Liverpool → Newcastle United; 1997-11: Liverpool → Newcastle United; 2000-01: Newcastle United → Liverpool; 2000-02: Newcastle United → Liverpool; 2002-06: Leeds United → Liverpool; 2003-03: Newcastle United → Manchester United; 2003-04: Newcastle United → Manchester United; 2003-05: Newcastle United → Manchester United; 2003-06: Newcastle United → Manchester United); who is in the top 12 changes at 166 month ends (1992-08: in Manchester United, out Everton; 1992-09: in Manchester United, out Sheffield United; 1992-10: in Manchester United, out Sheffield United; 1993-06: in Manchester United, out Swindon Town; 1993-08: in Ipswich Town, out Oldham Athletic; 1994-06: in Swindon Town, out West Ham United; 1994-07: in Crystal Palace, out West Ham United; 1994-08: in Leicester City, out West Ham United; 1994-09: in Leicester City, out West Ham United; 1995-02: in Ipswich Town, out Newcastle United …); the order within the top 12 changes at 375 month ends.

**Questions for Luke on list A (each with Claude's recommendation)**

1. **Combined fees.** One payment for two players (Charles and Tommy Johnson £2.9m; McKee and Whitworth £530,000; Billington and McKeever £500,000) is booked once, on one transfer of the pair, and the partner counts £0. Each club's total is exact and no split is invented. *Recommendation:* keep it.
2. **Parker and Carr (Villa ↔ Leicester, Feb 1995).** The only source values "the deal" at £550,000 without saying how much was cash. We count £550,000 for Parker and £0 for Carr. *Recommendation:* keep it, and ask the next research round for the cash figure.
3. **Andy Cole (Feb 1995).** A grade B source values Keith Gillespie at £1m in the deal, so under DEC-237 (d) Cole counts £7m (£6m cash plus Gillespie) and Gillespie £1m; Manchester United's net is still the £6m cash. *Recommendation:* keep it (it follows the rule Luke approved).

**Answered by Luke (Cowork chat, 8 Oct 2026): yes to all three, kept as built (DEC-405, DEC-406, DEC-407).**

## 12. Source round 1, list B: 1997–98 to 2001–02 (DEC-275, IQ-15f), and the completion-report rule (DEC-404)

- **Deals:** 342 (B0001–B0342; 342 of our transfers), mapped by player and date (`source/source_round1_map.csv`). ChatGPT's answers (private part21a–r, every SHA-256 matched its README) were added as leads (`found_via`: "ChatGPT source round 1 (DEC-264 route)") and every cited page was read on the GitHub runner: the figure next to the player's name, and both clubs named on the page. Wikipedia and Transfermarkt pages are never fee sources and were not fetched.
- **VERIFIED:** 304 of the 342 transfers now have a fee confirmed at source (296 by a club, league or press source; the rest by a Soccerbase row), up from 81 before this round. 10 more count £0 (undisclosed, nominal, free, or known only as a maximum or approximation).
- **Changed:** 117 fees changed (£16.9m up, £47.6m down; net −£30.7m) and 11 completion dates moved to the date a grade B report gives (`source/deal_structure.csv` for the dates set by hand).

| Deal | Player | Move | Date before → after | Fee before | Fee after | Why |
|---|---|---|---|---|---|---|
| B0002 | Simon Haworth | Cardiff City → Coventry City | 1997-05-21 | £500,000 | £300,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0004 | Øyvind Leonhardsen | Wimbledon → Liverpool | 1997-06-02 | £3,500,000 | £4,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0008 | Jimmy Floyd Hasselbaink | Boavista → Leeds United | 1997-06-12 | £2,000,000 | £1,600,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0009 | Luis Boa Morte | Sporting Lisbon → Arsenal | 1997-06-14 | £1,750,000 | £1,800,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0016 | Eoin Jess | Coventry City → Aberdeen | 1997-07-04 | £700,000 | £650,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0017 | Kyle Lightbourne | Walsall → Coventry City | 1997-07-04 | £500,000 | £750,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0019 | Martin Dahlin | Roma → Blackburn Rovers | 1997-07-08 | £2,500,000 | £2,000,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0020 | Paul Ince | Internazionale → Liverpool | 1997-07-10 | £4,200,000 | £4,250,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0022 | Peter Ndlovu | Coventry City → Birmingham City | 1997-07-14 | £1,600,000 | £1,750,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0023 | Danny Murphy | Crewe Alexandra → Liverpool | 1997-07-15 | £3,000,000 | £1,500,000 | guaranteed fee only; add-ons count only when reported as paid (DEC-412, Luke's answer to list B question 3) |
| B0031 | Jon Dahl Tomasson | Heerenveen → Newcastle United | 1997-07-31 | £2,200,000 | £2,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0032 | Brian Deane | Leeds United → Sheffield United | 1997-08-01 | £1,500,000 | £1,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0034 | Nelson Vivas | Boca Juniors → Arsenal | 1997-08-05 → 1998-08-06 | £1,600,000 | £2,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0041 | Marc Rieper | West Ham United → Celtic | 1997-09-12 | £1,400,000 | £1,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0043 | Carlton Palmer | Leeds United → Southampton | 1997-09-23 | £1,300,000 | £1,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0049 | Samassi Abou | Cannes → West Ham United | 1997-10-28 | £250,000 | £400,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0051 | David Curtolo | Västerås → Aston Villa | 1997-11-27 | £315,000 | £0 | an A/B report calls the fee undisclosed or nominal: only an A/B figure counts (DEC-408 (a), DEC-237 (g)) |
| B0053 | Graham Stuart | Everton → Sheffield United | 1997-11-28 | £500,000 | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player |
| B0054 | Chris Coleman | Blackburn Rovers → Fulham | 1997-12-01 | £2,000,000 | £2,100,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0056 | Karel Poborský | Manchester United → Benfica | 1997-12-30 | £2,000,000 | £0 | an A/B report calls the fee undisclosed or nominal: only an A/B figure counts (DEC-408 (a), DEC-237 (g)) |
| B0062 | Iain Dowie | West Ham United → Queens Park Rangers | 1998-01-29 | £1,600,000 | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player |
| B0063 | Trevor Sinclair | Queens Park Rangers → West Ham United | 1998-01-29 | £2,300,000 | £2,000,000 | part-exchange (DEC-237 (d)): cash only unless a source values the player |
| B0070 | Goce Sedloski | Hajduk Split → Sheffield Wednesday | 1998-02-19 → 1997-12-17 | £750,000 | £1,750,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0073 | Martin Hiden | Rapid Vienna → Leeds United | 1998-02-25 | £1,300,000 | £1,500,000 | confirmed at source: higher grade or earlier report (B, www.the-independent.com) |
| B0077 | Andy Roberts | Crystal Palace → Wimbledon | 1998-03-09 | £2,000,000 | £1,600,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0082 | James Coppinger | Darlington → Newcastle United | 1998-03-31 | £250,000 | £0 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |
| B0083 | Paul Robinson | Darlington → Newcastle United | 1998-03-31 | £250,000 | £500,000 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |
| B0084 | Stephen Glass | Aberdeen → Newcastle United | 1998-03-31 → 1998-09-22 | £650,000 | £650,000 | tribunal fee (IQ-15f): the fee is booked when the tribunal sets it |
| B0085 | Clyde Wijnhard | Willem II → Leeds United | 1998-05-16 | £1,500,000 | £2,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0088 | Alan Thompson | Bolton Wanderers → Aston Villa | 1998-06-05 | £4,500,000 | £4,800,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0090 | Chris Powell | Derby County → Charlton Athletic | 1998-06-22 | £800,000 | £825,000 | confirmed at source: higher grade or earlier report (B, www.the-independent.com) |
| B0091 | Georgios Georgiadis | Panathinaikos → Newcastle United | 1998-06-30 | £500,000 | £420,000 | confirmed at source: higher grade or earlier report (B, www.irishtimes.com) |
| B0095 | Dean Gordon | Crystal Palace → Middlesbrough | 1998-07-06 | £900,000 | £800,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0096 | Gary Pallister | Manchester United → Middlesbrough | 1998-07-09 | £2,500,000 | £2,300,000 | confirmed at source: higher grade or earlier report (B, www.irishtimes.com) |
| B0097 | Marco Materazzi | Perugia → Everton | 1998-07-15 | £2,800,000 | £3,200,000 | confirmed at source: higher grade or earlier report (B, www.irishtimes.com) |
| B0099 | Jesper Blomqvist | Parma → Manchester United | 1998-07-21 | £4,400,000 | £5,000,000 | confirmed at source: higher grade or earlier report (B, www.irishtimes.com) |
| B0102 | Olivier Dacourt | Strasbourg → Everton | 1998-07-27 | £4,000,000 | £3,800,000 | confirmed at source: higher grade or earlier report (B, www.irishtimes.com) |
| B0104 | Javier Margas | Universidad Católica → West Ham United | 1998-07-30 | £1,800,000 | £2,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0105 | Carl Serrant | Oldham Athletic → Newcastle United | 1998-07-31 | £500,000 | £600,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0106 | Garry Brady | Tottenham Hotspur → Newcastle United | 1998-07-31 → 1998-11-03 | £650,000 | £650,000 | tribunal fee (IQ-15f): the fee is booked when the tribunal sets it |
| B0107 | Laurent Charvet | Cannes → Newcastle United | 1998-07-31 | £750,000 | £520,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0109 | John Collins | Monaco → Everton | 1998-08-01 | £2,500,000 | £2,300,000 | confirmed at source: higher grade or earlier report (B, www.irishtimes.com) |
| B0115 | Robert Jarni | Coventry City → Real Madrid | 1998-08-15 | £3,400,000 | £3,150,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0118 | Marc Edworthy | Crystal Palace → Coventry City | 1998-08-26 | £1,200,000 | £850,000 | £1,300,000 not counted: £1.3m includes the conditional sum: the same day's report gives an initial £850,000 plus £350,000 after 60 appearanc |
| B0119 | Dietmar Hamann | Bayern Munich → Newcastle United | 1998-08-31 | £5,250,000 | £4,500,000 | confirmed at source: higher grade or earlier report (B, www.irishtimes.com) |
| B0120 | Fredrik Ljungberg | Halmstad → Arsenal | 1998-09-12 | £3,000,000 | £1,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0126 | Brian Deane | Benfica → Middlesbrough | 1998-10-12 | £3,000,000 | £3,500,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0135 | Ashley Ward | Barnsley → Blackburn Rovers | 1998-12-29 | £4,500,000 | £4,250,000 | £4,500,000 not counted: £4.5m includes the appearance add-on: the deal was £4.25m rising to £4.5m (guaranteed fee only) |
| B0138 | Nwankwo Kanu | Internazionale → Arsenal | 1999-01-15 | £4,500,000 | £3,000,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0142 | Paolo Di Canio | Sheffield Wednesday → West Ham United | 1999-01-27 | £1,750,000 | £1,500,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0143 | Didier Domi | PSG → Newcastle United | 1999-01-31 | £4,000,000 | £3,250,000 | £4,000,000 not counted: £4m is the figure if the appearance add-ons are paid: the deal was £3.25m rising to £4m (guaranteed fee only) |
| B0149 | Mark Delaney | Cardiff City → Aston Villa | 1999-03-09 | £250,000 | £500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0150 | Steve Stone | Nottingham Forest → Aston Villa | 1999-03-11 | £5,500,000 | £6,000,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0152 | Jim Magilton | Sheffield Wednesday → Ipswich Town | 1999-03-22 | £682,500 | £0 | maximum or approximation only (DEC-276) |
| B0153 | Lee Carsley | Derby County → Blackburn Rovers | 1999-03-22 | £3,400,000 | £3,375,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0154 | Colin Calderwood | Tottenham Hotspur → Aston Villa | 1999-03-23 | £230,000 | £225,000 | confirmed at source: higher grade or earlier report (B, www.the-independent.com) |
| B0157 | Richard Cresswell | York City → Sheffield Wednesday | 1999-03-25 | £950,000 | £1,000,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0158 | Silvio Marić | Croatia Zagreb → Newcastle United | 1999-03-31 | £3,650,000 | £3,300,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0159 | Terry Cooke | Manchester United → Manchester City | 1999-04-16 | £1,000,000 | £600,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0163 | Eirik Bakke | Sogndal → Leeds United | 1999-05-25 | £1,750,000 | £1,000,000 | £1,750,000 not counted: £1.75m is the total: the same page says Leeds will initially pay £1m (guaranteed fee only) |
| B0168 | Alain Goma | Paris Saint-Germain → Newcastle United | 1999-06-15 | £4,700,000 | £4,750,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0169 | Danny Mills | Charlton Athletic → Leeds United | 1999-06-15 | £4,000,000 | £3,800,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0171 | David James | Liverpool → Aston Villa | 1999-06-17 | £1,700,000 | £1,800,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0175 | Philippe Clement | Coventry City → Club Brugge | 1999-06-29 | £800,000 | £770,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0177 | Vladimir Smicer | Lens → Liverpool | 1999-07-01 | £4,200,000 | £4,000,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0178 | Lee Clark | Sunderland → Fulham | 1999-07-07 | £3,000,000 | £2,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0190 | Craig Short | Everton → Blackburn Rovers | 1999-07-30 | £1,700,000 | £2,100,000 | confirmed at source: higher grade or earlier report (B, www.the-independent.com) |
| B0192 | Tim Flowers | Blackburn Rovers → Leicester City | 1999-07-30 | £2,100,000 | £1,100,000 | confirmed at source: higher grade or earlier report (B, www.the-independent.com) |
| B0194 | Runar Normann | Lillestrøm → Coventry City | 1999-07-31 | £1,000,000 | £0 | a same-grade source disputes the only figure: counted £0 until a figure is confirmed (DEC-414, Luke's answer to list B question 5) |
| B0196 | John Oster | Everton → Sunderland | 1999-08-06 | £1,000,000 | £750,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0197 | Øyvind Leonhardsen | Liverpool → Tottenham Hotspur | 1999-08-06 | £3,000,000 | £2,500,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0199 | Gabriele Ambrosetti | Vicenza → Chelsea | 1999-08-14 | £3,500,000 | £3,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0202 | Mikaël Silvestre | Inter Milan → Manchester United | 1999-09-10 | £4,000,000 | £3,250,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0203 | Carlton Palmer | Nottingham Forest → Coventry City | 1999-09-17 → 1999-12-19 | £500,000 | £500,000 | completion date from the grade B report (IQ-15f) |
| B0204 | Benito Carbone | Sheffield Wednesday → Aston Villa | 1999-10-20 | £800,000 | £0 | an A/B report calls the fee undisclosed or nominal: only an A/B figure counts (DEC-408 (a), DEC-237 (g)) |
| B0206 | Carlos Marinelli | Boca Juniors → Middlesbrough | 1999-10-27 → 1999-09-12 | £1,500,000 | £1,500,000 | completion date from the grade B report (IQ-15f) |
| B0208 | Guy Branston | Leicester City → Rotherham United | 1999-11-18 | £500,000 | £30,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0209 | Tomas Gustafsson | AIK → Coventry City | 1999-12-08 | £250,000 | £0 | an A/B report calls the fee undisclosed or nominal: only an A/B figure counts (DEC-408 (a), DEC-237 (g)) |
| B0210 | Darren Eadie | Norwich City → Leicester City | 1999-12-10 | £3,200,000 | £3,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0211 | Kevin Kilbane | West Bromwich Albion → Sunderland | 1999-12-15 | £2,200,000 | £2,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0212 | Jason Wilcox | Blackburn Rovers → Leeds United | 1999-12-17 | £3,000,000 | £0 | £3,000,000 not counted: the whole £3m 'depends on appearances and goals scored as well as Leeds' success': a figure including conditional su |
| B0214 | Emerson Thome | Sheffield Wednesday → Chelsea | 1999-12-23 | £2,700,000 | £2,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0219 | Ysrael Zúñiga | FBC Melgar → Coventry City | 2000-01-21 | £750,000 | £800,000 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |
| B0220 | Diego Gavilan | Cerro Porteno → Newcastle United | 2000-01-28 | £2,000,000 | £1,000,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0221 | Colin Hendry | Rangers → Coventry City | 2000-02-24 | £750,000 | £1,000,000 | confirmed at source: higher grade or earlier report (B, www.irishtimes.com) |
| B0222 | Stephen Hughes | Arsenal → Everton | 2000-03-07 | £3,000,000 | £0 | £3,000,000 not counted: a maximum ('could ultimately be worth'), not the guaranteed fee (DEC-276) |
| B0225 | Frederic Kanoute | Lyon → West Ham United | 2000-05-15 | £3,700,000 | £4,000,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0229 | Darren Holloway | Sunderland → Wimbledon | 2000-06-01 → 2000-10-03 | £1,200,000 | £1,300,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0234 | Mario Stanić | Parma → Chelsea | 2000-06-28 | £5,600,000 | £4,600,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0243 | Alex Nyarko | RC Lens → Everton | 2000-07-13 | £4,500,000 | £4,600,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0248 | Thomas Gravesen | Hamburg → Everton | 2000-07-24 | £2,500,000 | £2,800,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0249 | Julio Arca | Argentinos Juniors → Sunderland | 2000-07-25 | £3,500,000 | £3,000,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0252 | Didier Deschamps | Chelsea → Valencia | 2000-07-28 | £3,700,000 | £2,300,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0254 | Jonatan Johansson | Rangers → Charlton Athletic | 2000-07-31 | £3,750,000 | £3,250,000 | £3,750,000 not counted: £3.75m includes the £500,000 rise: the initial fee was £3.25m 'with the fee rising by £500,000' (guaranteed fee only |
| B0256 | Noel Whelan | Coventry City → Middlesbrough | 2000-07-31 | £2,000,000 | £2,500,000 | £5,000,000 not counted: £5m is the combined spending on Noel Whelan and Joseph-Désiré Job |
| B0258 | David Thompson | Liverpool → Coventry City | 2000-08-02 | £3,000,000 | £2,500,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0261 | Duncan Ferguson | Newcastle United → Everton | 2000-08-17 | £3,750,000 | £3,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0264 | Steve Howey | Newcastle United → Manchester City | 2000-08-31 | £3,000,000 | £2,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0267 | Lomana LuaLua | Colchester United → Newcastle United | 2000-09-30 | £2,200,000 | £2,250,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0270 | Mark Fish | Bolton Wanderers → Charlton Athletic | 2000-11-08 | £700,000 | £1,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0272 | Rigobert Song | Liverpool → West Ham United | 2000-11-28 | £2,500,000 | £3,000,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0274 | Igor Biscan | Dinamo Zagreb → Liverpool | 2000-12-07 | £5,500,000 | £7,000,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0277 | Titi Camara | Liverpool → West Ham United | 2000-12-21 | £2,200,000 | £1,500,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0278 | Darren Huckerby | Leeds United → Manchester City | 2000-12-29 | £2,500,000 | £3,200,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0282 | Didier Domi | Newcastle United → Paris Saint-Germain | 2001-01-31 | £4,000,000 | £3,500,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0284 | Wayne Quinn | Sheffield United → Newcastle United | 2001-02-28 | £1,000,000 | £1,500,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0286 | Dean Windass | Bradford City → Middlesbrough | 2001-03-08 → 2001-03-16 | £600,000 | £0 | maximum or approximation only (DEC-276) |
| B0297 | John Arne Riise | Monaco → Liverpool | 2001-06-20 | £4,000,000 | £4,500,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0301 | Craig Bellamy | Coventry City → Newcastle United | 2001-06-30 | £6,000,000 | £6,500,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0303 | Mustapha Hadji | Coventry City → Aston Villa | 2001-07-07 | £2,500,000 | £2,000,000 | part-exchange (DEC-237 (d)): cash only unless a source values the player |
| B0308 | Juan Sebastián Verón | Lazio → Manchester United | 2001-07-12 | £28,100,000 | £25,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0311 | Olof Mellberg | Racing Santander → Aston Villa | 2001-07-19 | £5,000,000 | £5,600,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0313 | Milan Baroš | Baník Ostrava → Liverpool | 2001-07-26 → 2001-12-23 | £3,200,000 | £3,500,000 | £2,500,000 not counted: The Fiver's own guess ('we reckon'), not a reported fee |
| B0316 | Laurent Robert | PSG → Newcastle United | 2001-08-01 | £9,500,000 | £10,000,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0321 | Matteo Sereni | Sampdoria → Ipswich Town | 2001-08-17 | £4,500,000 | £0 | maximum or approximation only (DEC-276) |
| B0322 | Michael Ball | Everton → Rangers | 2001-08-17 | £6,500,000 | £6,000,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| B0323 | Boško Balaban | Dinamo Zagreb → Aston Villa | 2001-08-24 | £5,800,000 | £6,000,000 | confirmed at source: higher grade or earlier report (B, www.irishexaminer.com) |
| B0324 | Don Hutchison | Sunderland → West Ham United | 2001-08-30 | £5,000,000 | £5,300,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
| B0328 | Sylvain Distin | PSG → Newcastle United | 2001-09-11 → 2001-09-12 | £500,000 | £500,000 | a loan fee is a loan fee (IQ-15f) |
| B0330 | Tomáš Řepka | Fiorentina → West Ham United | 2001-09-14 | £5,500,000 | £5,000,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
| B0332 | Thomas Myhre | Everton → Beşiktaş | 2001-11-15 → 2001-11-07 | £375,000 | £300,000 | confirmed at source: higher grade or earlier report (B, www.the-independent.com) |
| B0336 | Diego Forlán | Independiente → Manchester United | 2002-01-22 | £6,900,000 | £7,500,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |

**Deal structures applied in list B** (one row each in `source/deal_structure.csv`, with source, quote and rule):

| Player | Fee booked | Rule | Note |
|---|---|---|---|
| Paul Robinson | £500,000 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented | Newcastle paid Darlington £500,000 for both players (the initial fee; any later sum was not reported as paid); James Coppinger's transfer counts £0 |
| James Coppinger | £0 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented | the £500,000 figure is the pair's joint fee, not Coppinger's alone |
| Ysrael Zúñiga | £800,000 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented | Coventry paid Melgar £800,000 for both players; Walter Zevallos has no transfer in the build (no Coventry first-team record on the club-season page), so nothing |
| Trevor Sinclair | £2,000,000 | part-exchange (DEC-237 (d)): cash only unless a source values the player | West Ham gave QPR Iain Dowie, Keith Rowland and £2m; the £3m and £3.5m figures value the whole package, and no source values Dowie or Rowland on their own, so t |
| Iain Dowie | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player | the C figure £1.6m for Dowie is a database valuation, not a cash fee |
| Keith Rowland | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player |  |
| Carl Tiler | £500,000 | part-exchange (DEC-237 (d)): cash only unless a source values the player; combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented | the £500,000 cash is booked once, on Tiler's move; Mitch Ward and Graham Stuart count £0 (no grade A/B source values either player; the C estimate of £850,000 f |
| Mitch Ward | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player; combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |  |
| Graham Stuart | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player | our earlier £500,000 on Stuart's move had the cash going the wrong way |
| Mustapha Hadji | £2,000,000 | part-exchange (DEC-237 (d)): cash only unless a source values the player | Aston Villa gave Coventry Julian Joachim plus £2m; the £4m and £4.5m figures value the whole package; Joachim's move counts £0 |
| Julian Joachim | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player |  |
| Sylvain Distin | £500,000 | a loan fee is a loan fee (IQ-15f) | the £4m option was not taken up in 2001-02 (not reported as paid); the earlier £300,000 was a proposed term in a rumour round-up |
| Matteo Sereni | £0 | maximum or approximation only (DEC-276) | every figure found is an approximation ('believed to be around £4.5 million', 'around £6m', 'around £5m') or a bound ('exceeded the £4.57m') |
| Dean Windass | £0 | maximum or approximation only (DEC-276) | the completion report gives only a maximum; the earlier '£1m transfer' was a prospective figure |
| Stephen Glass | £650,000 | tribunal fee (IQ-15f): the fee is booked when the tribunal sets it | Glass joined on a free under freedom of contract; the tribunal later set the compensation |
| Garry Brady | £650,000 | tribunal fee (IQ-15f): the fee is booked when the tribunal sets it | Brady joined on a free under freedom of contract; the tribunal later set the compensation |
| Jim Magilton | £0 | maximum or approximation only (DEC-276) | the press gives only the maximum (£1m); the £682,500 on the Wikipedia list cites no source and was not found at any source |
| Peter Crouch | £5,000,000 | DEC-404 with DEC-277: both reports say the deal was completed, so the earlier one is used | the Guardian's 27 Mar report ('have completed the signing … for an initial fee of £5m') comes before 'sealed the £4.5m signing' (28 Mar); the runner's 22-word q |
| Danny Murphy | £1,500,000 | guaranteed fee only; add-ons count only when reported as paid (DEC-412, Luke's answer to list B question 3) | the completion report says the deal 'could eventually be worth £3m'; the £2m was the fee Crewe agreed with both clubs before Murphy chose Liverpool; no source s |
| Runar Normann | £0 | a same-grade source disputes the only figure: counted £0 until a figure is confirmed (DEC-414, Luke's answer to list B question 5) | the Guardian's season list gives £1m; the Independent says the fee was undisclosed and 'way below' that figure; research round 2 |

**DEC-404 (Luke, 8 Oct 2026): a report that the deal was completed beats earlier reports of bids, agreed fees or "expected" figures of the same grade; the earliest report is used only when none says the deal was completed.** Applied to the whole build, it changes **62 fees** (`source/dec404_changes.csv`): 5 on list A, 4 of the 32 phase 2 same-grade conflicts, 18 on list B and 21 elsewhere. A completion word counts only next to the player's name; wording such as "imminent", "subject to" or "proposed" means not completed; a figure within 2% of the one already used (the same fee in another currency) changes nothing.

| Date | Player | Move | Fee without DEC-404 | Fee with DEC-404 | On | Completion report |
|---|---|---|---|---|---|---|
| 1992-07-13 | David Lowe | Ipswich Town → Leicester City | £250,000 | £200,000 | source round 1 list A | David Lowe, Leicester City's recent pounds 200,000 signing from Ipswich Town |
| 1994-05-31 | Tony Daley | Aston Villa → Wolverhampton Wanderers | £1,300,000 | £1,250,000 | source round 2 | Tony Daley, Villa's former England winger, completed his move to Molineux for a pounds 1.2 |
| 1994-09-26 | Paul Kitson | Derby County → Newcastle United | £2,500,000 | £2,250,000 | source round 1 list A | Paul Kitson, their recent pounds 2.25m signing from Derby County, |
| 1994-10-14 | Efan Ekoku | Norwich City → Wimbledon | £920,000 | £900,000 | source round 1 list A | Efan Ekoku […] a pounds 900,000 deal |
| 1995-10-01 | Lars Bohinen | Nottingham Forest → Blackburn Rovers | £700,000 | £750,000 | other | otland's Billy McKinlay arrived from Dundee United for pounds 1.75m while Norway's Lars Bo |
| 1996-02-08 | Faustino Asprilla | Parma → Newcastle United | £6,700,000 | £7,500,000 | other | international, who joined Newcastle from Parma in February 1996 for pounds 7.5m, went abou |
| 1996-02-24 | David Batty | Blackburn Rovers → Newcastle United | £3,750,000 | £4,000,000 | source round 1 list A | David Batty […] pounds 4m signing of the Blackburn midfielder. |
| 1996-07-10 | Ronny Johnsen | Beşiktaş → Manchester United | £1,200,000 | £1,500,000 | other | Ronny Johnsen Defender Nationality: Norwegian Age: 26 Arrived from: Besiktas (pounds 1.5m) |
| 1997-01-07 | Ramon Vega | Cagliari → Tottenham Hotspur | £3,000,000 | £3,750,000 | source round 1 list A | Ramon Vega, […] The pounds 3.75m recruit from Cagliari |
| 1997-07-08 | Martin Dahlin | Roma → Blackburn Rovers | £2,500,000 | £2,000,000 | source round 1 list B | Martin Dahlin, the Swedish international signed in the summer for pounds 2m from Roma |
| 1997-07-31 | David Ginola | Newcastle United → Tottenham Hotspur | £2,600,000 | £2,000,000 | source round 1 list B | David Ginola completed his pounds 2m move to Spurs yesterday |
| 1997-12-19 | Brad Friedel | Columbus Crew → Liverpool | £1,000,000 | £1,300,000 | source round 2 | Friedel has yet to appear for Liverpool since his pounds 1.3m move from the Major League S |
| 1998-08-15 | Robert Jarni | Coventry City → Real Madrid | £3,350,000 | £3,150,000 | source round 1 list B | Coventry yesterday completed the £3.15 million sale of Robert Jarni to Real Madrid |
| 1998-10-12 | Brian Deane | Benfica → Middlesbrough | £3,000,000 | £3,500,000 | source round 1 list B | Brian Deane, Boro's pounds 3.5m signing from Benfica, |
| 1999-01-15 | Nwankwo Kanu | Internazionale → Arsenal | £4,500,000 | £3,000,000 | source round 1 list B | The Arsenal manager signed Kanu for pounds 3m from Internazionale two weeks ago |
| 1999-01-27 | Paolo Di Canio | Sheffield Wednesday → West Ham United | £2,000,000 | £1,500,000 | source round 1 list B | West Ham sign £1.5m Di Canio |
| 1999-03-22 | Lee Carsley | Derby County → Blackburn Rovers | £3,300,000 | £3,375,000 | source round 1 list B | Carsley […] pounds 3.375m. |
| 1999-03-25 | Richard Cresswell | York City → Sheffield Wednesday | £950,000 | £1,000,000 | source round 1 list B | Richard Cresswell, bought on deadline-day from York for pounds 1m, |
| 1999-06-30 | David Wetherall | Leeds United → Bradford City | £2,000,000 | £1,400,000 | source round 1 list B | Bradford have completed the £1.4m signing of David Wetherall from Leeds |
| 1999-07-08 | Eyal Berkovic | West Ham United → Celtic | £5,500,000 | £5,750,000 | source round 1 list B | Eyal Berkovic completed his pounds 5.75m move from West Ham to Celtic yesterday. |
| 2000-07-05 | Christian Karembeu | Real Madrid → Middlesbrough | £2,250,000 | £2,100,000 | source round 1 list B | Karembeu, 29, has joined Boro from Real Madrid for £2.1m |
| 2000-08-02 | David Thompson | Liverpool → Coventry City | £2,750,000 | £2,500,000 | source round 1 list B | Coventry have bought David Thompson from Liverpool for £2.5m. |
| 2000-10-03 | Darren Holloway | Sunderland → Wimbledon | £500,000 | £1,300,000 | source round 1 list B | the new £1.3m signing Darren Holloway |
| 2000-10-31 | Clarence Acuña | Universidad de Chile → Newcastle United | £700,000 | £1,000,000 | source round 1 list B | Clarence Acuna was on Tyneside yesterday undergoing a medical, and will complete his £1m m |
| 2001-03-07 | Chris Makin | Sunderland → Ipswich Town | £2,000,000 | £1,250,000 | source round 1 list B | Ipswich completed the signing of the Sunderland defender Chris Makin for £1.25m. |
| 2001-08-01 | Laurent Robert | PSG → Newcastle United | £10,500,000 | £10,000,000 | source round 1 list B | Laurent Robert has completed his £10m move to Newcastle United. |
| 2001-08-17 | Michael Ball | Everton → Rangers | £7,000,000 | £6,000,000 | source round 1 list B | Ball has completed his protracted £6m move |
| 2001-09-09 | Allan Johnston | Rangers → Middlesbrough | £1,000,000 | £600,000 | source round 1 list B | Allan Johnston today joined Middlesbrough from Rangers in a £600,000 deal. |
| 2003-01-30 | Robbie Fowler | Leeds United → Manchester City | £7,000,000 | £3,000,000 | source round 2 | "The transfer was completed today for an agreed fee of £3m cash [€4.5m] with further payme |
| 2004-07-27 | Ricardo Carvalho | Porto → Chelsea | £16,500,000 | £19,838,646 | other | signed the Portuguese international defender Ricardo Carvalho from Porto for €30m (£19.8m) |
| 2004-08-30 | Robert Earnshaw | Cardiff City → West Bromwich Albion | £3,400,000 | £3,000,000 | other | Wanderers 2-1. This they achieved without Robert Earnshaw, their record £3m signing from C |
| 2007-07-10 | Florent Malouda | Lyon → Chelsea | £13,500,000 | £13,000,000 | other | the Frenchman, who moved to Stamford Bridge from Lyon for £13million in July, said: "I jus |
| 2008-04-29 | Luka Modrić | Dinamo Zagreb → Tottenham Hotspur | £16,625,762 | £18,209,168 | source round 2 | Singing the contract where Dinamo receives €23 million in compensation from Tottenham comp |
| 2010-08-11 | Craig Cathcart | Manchester United → Blackpool | £350,000 | £500,000 | other | Craig Cathcart (Man Utd, £500k) |
| 2011-08-31 | Bryan Ruiz | FC Twente → Fulham | £10,600,000 | £9,949,638 | source round 2 | Ruiz, who has joined Fulham for an undisclosed fee reported in sections of the British med |
| 2012-06-10 | Jay Rodriguez | Burnley → Southampton | £7,000,000 | £6,000,000 | source round 2 | not been officially disclosed but is understood to be worth £6m, which breaks Southampton' |
| 2012-06-26 | Olivier Giroud | Montpellier → Arsenal | £13,000,000 | £12,000,000 | source round 2 | Olivier Giroud has joined Arsenal ... The club did not disclose the transfer fee but media |
| 2012-08-27 | Luka Modrić | Tottenham Hotspur → Real Madrid | £23,666,772 | £27,870,730 | source round 2 | Spanish media reported Real would pay $43.81m, plus a possible eight million in add-ons, f |
| 2013-08-14 | Tom Huddlestone | Tottenham Hotspur → Hull City | £5,000,000 | £5,250,000 | other | news: Tottenham midfielder Tom Huddlestone completes Hull City switch in £5.25m deal | The |
| 2013-08-28 | Willian | Anzhi Makhachkala → Chelsea | £25,500,000 | £32,000,000 | phase 2 same-grade conflict | has secured his work permit to join Chelsea in a £32m deal from Anzhi Makhachkala. Photogr |
| 2014-06-13 | David Luiz | Chelsea → Paris Saint-Germain | £40,000,000 | £50,000,000 | phase 2 same-grade conflict | move from Chelsea to PSG David Luiz has completed his £50m move from Chelsea to Paris Sain |
| 2014-06-27 | Luke Shaw | Southampton → Manchester United | £27,000,000 | £30,000,000 | source round 2; phase 2 same-grade conflict | week Luke Shaw has joined Manchester United in a reported £30m switch from Southampton, ma |
| 2015-06-24 | Roberto Firmino | TSG Hoffenheim → Liverpool | £29,000,000 | £21,300,000 | other | Image: Roberto Firmino: Will join Liverpool for initial fee of £21.3m Liverpool have compl |
| 2015-09-01 | Papy Djilobodji | Nantes → Chelsea | £2,700,000 | £4,000,000 | other | Djilobodji has now signed a four-year deal with Chelsea after completing a transfer worth  |
| 2016-07-06 | Matt Phillips | Queens Park Rangers → West Bromwich Albion | £5,500,000 | £5,000,000 | source round 2 | New-boy Matt Phillips has impressed the West Brom coaching staff so far ... his £5million  |
| 2016-08-31 | David Luiz | Paris Saint-Germain → Chelsea | £30,000,000 | £34,000,000 | other | David Luiz completes shock return to Chelsea from PSG for £34m This article is more than 1 |
| 2016-08-31 | Islam Slimani | Sporting CP → Leicester City | £29,000,000 | £28,000,000 | other | Islam Slimani to Leicester City: Premier League champions confirm club-record £28m signing |
| 2017-07-09 | Antonio Rüdiger | Roma → Chelsea | £29,000,000 | £31,025,618 | source round 2 | clinched a deal worth an initial €35 million to sign German defender Antonio Rudiger from  |
| 2017-07-21 | Álvaro Morata | Real Madrid → Chelsea | £58,000,000 | £60,000,000 | other | 20 caps for Spain Chelsea have completed the club record £60m signing of striker Alvaro Mo |
| 2018-07-10 | Lucas Torreira | Sampdoria → Arsenal | £26,000,000 | £25,000,000 | source round 2 | Arsenal has officially completed the transfer of Lucas Torreira ... signing the Uruguay st |
| 2019-07-02 | Jack Clarke | Leeds United → Tottenham Hotspur | £10,000,000 | £9,000,000 | other | Tottenham Hotspur have completed the permanent signing of Leeds United winger Jack Clarke  |
| 2019-07-04 | Rodri | Atlético Madrid → Manchester City | £68,200,000 | £62,800,000 | other | team after moving from Atletico Madrid for a club record £62.8m. Rodri, 23, joins on a fiv |
| 2020-01-31 | Clinton Mola | Chelsea → Stuttgart | £360,000 | £168,110 | other | joined the German club for a fee believed to be €200,000, beating off interest from AC Mil |
| 2020-09-19 | Diogo Jota | Wolverhampton Wanderers → Liverpool | £40,000,000 | £41,000,000 | other | signing of Portugal forward Diogo Jota from Wolves in a £41m deal that could rise to £45m  |
| 2021-07-21 | Kristoffer Ajer | Celtic → Brentford | £13,000,000 | £13,500,000 | source round 2 | Premier League side Brentford have signed Kristoffer Ajer from Celtic for £13.5 million. |
| 2022-07-04 | Kalvin Phillips | Leeds United → Manchester City | £42,000,000 | £45,000,000 | other | Manchester City have signed Leeds United midfielder Kalvin Phillips for £45m. The 26-year- |
| 2022-07-13 | Raheem Sterling | Manchester City → Chelsea | £47,500,000 | £50,000,000 | other | of England forward Raheem Sterling from Manchester City in a £50m deal. Sterling, 27, has  |
| 2022-08-26 | Alexander Isak | Real Sociedad → Newcastle United | £60,000,000 | £58,000,000 | source round 2 | Sociedad frontman completed a move understood to be worth around £58million on Friday afte |
| 2022-08-31 | Saša Kalajdžić | VfB Stuttgart → Wolverhampton Wanderers | £15,400,000 | £15,000,000 | source round 2 | Wolverhampton Wanderers have completed the signing of Austrian centre-forward Sasa Kalajdz |
| 2023-08-12 | Harry Kane | Tottenham Hotspur → Bayern Munich | £100,000,000 | £86,400,000 | other | at Tottenham. The striker signs for an initial 100m euros (£86.4m) plus add-ons and could  |
| 2026-01-09 | Antoine Semenyo | AFC Bournemouth → Manchester City | £65,000,000 | £62,500,000 | other | had to be activated before Saturday, and they will pay £62.5m across 24 monthly instalment |
| 2026-08-18 | Rodri | Manchester City → Barcelona | £65,400,000 | £51,308,363 | phase 2 same-grade conflict | Barcelona transfer Show The Spain midfielder Rodri has completed his €60m move from Manche |

**Same-grade disagreements within list B** (86 deals) and the step that settled each:

| Deal | Player | Fee used (grade, report date) | Other confirmed figure(s), same grade (report date) | Settled by |
|---|---|---|---|---|
| B0002 | Simon Haworth | £300,000 (B, 1997-06-07) | £900,000 (1997-08-06) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0004 | Øyvind Leonhardsen | £4,000,000 (B, 1997-06-01) | £3,250,000 (1997-08-02), £3,500,000 (1997-08-02) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0008 | Jimmy Floyd Hasselbaink | £1,600,000 (B, 1997-08-02) | £2,000,000 (1997-08-09) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0009 | Luis Boa Morte | £1,800,000 (B, 1997-06-14) | £1,750,000 (1997-06-17) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0016 | Eoin Jess | £650,000 (B, 1997-07-03) | £600,000 (1997-08-06), £700,000 (1997-08-02) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0017 | Kyle Lightbourne | £750,000 (B, 1997-08-02) | £500,000 (1997-08-05) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0019 | Martin Dahlin | £2,000,000 (B, 1997-08-31) | £2,500,000 (1997-07-08) | DEC-404 (completion report) |
| B0022 | Peter Ndlovu | £1,750,000 (B, 1997-07-07) | £1,600,000 (1997-07-12) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0030 | David Ginola | £2,000,000 (B, 1997-07-15) | £2,600,000 (1997-07-14) | DEC-404 (completion report) |
| B0041 | Marc Rieper | £1,500,000 (B, 1997-09-12) | £1,400,000 (1997-09-13) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0060 | Valérien Ismaël | £2,750,000 (B, 1998-02-14) | £2,800,000 (1998-03-16) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0064 | Andy Hinchcliffe | £3,000,000 (B, 1998-01-31) | £2,900,000 (1998-01-31) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0067 | Gary Speed | £5,500,000 (B, 1998-02-07) | £5,600,000 (1998-02-08) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0069 | Kyle Lightbourne | £500,000 (B, 1998-02-18) | £423,053 (1998-02-17) | sterling figure before a converted one (contract rule) |
| B0072 | Moussa Saïb | £2,300,000 (B, 1998-02-24) | £2,500,000 (1998-02-24) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0078 | Jamie Pollock | £1,000,000 (B, 1998-03-20) | £800,000 (1998-03-22) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0086 | Jimmy Corbett | £525,000 (B, 1998-05-23) | £500,000 (1998-06-12), £1,000,000 (1998-08-13) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0088 | Alan Thompson | £4,800,000 (B, 1998-06-05) | £4,500,000 (1998-06-06) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0089 | Danny Granville | £1,600,000 (B, 1998-06-19) | £1,500,000 (1998-09-20) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0090 | Chris Powell | £825,000 (B, 1998-06-22) | £830,000 (1998-09-20) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0092 | Jon Dahl Tomasson | £2,500,000 (B, 1998-06-19) | £2,000,000 (1998-08-08) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0095 | Dean Gordon | £800,000 (B, 1998-08-02) | £900,000 (1998-08-13) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0096 | Gary Pallister | £2,300,000 (B, 1998-07-09) | £2,500,000 (1998-08-13) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0097 | Marco Materazzi | £3,200,000 (B, 1998-07-27) | £2,500,000 (1998-08-15) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0102 | Olivier Dacourt | £3,800,000 (B, 1998-07-27) | £4,000,000 (1998-12-01) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0103 | Kevin Campbell | £2,500,000 (B, 1998-08-08) | £3,000,000 (1998-08-15), £4,000,000 (1998-08-13) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0105 | Carl Serrant | £600,000 (B, 1998-08-08) | £500,000 (1998-08-13) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0109 | John Collins | £2,300,000 (B, 1998-07-27) | £2,500,000 (1998-08-15) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0115 | Robert Jarni | £3,150,000 (B, 1998-08-20) | £3,350,000 (1998-08-19) | DEC-404 (completion report) |
| B0119 | Dietmar Hamann | £4,500,000 (B, 1998-08-05) | £5,000,000 (1998-08-08), £5,250,000 (1998-08-15) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0122 | Steve Simonsen | £3,300,000 (B, 1998-09-23) | £3,000,000 (1998-10-04) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0126 | Brian Deane | £3,500,000 (B, 1998-10-24) | £3,000,000 (1998-10-17) | DEC-404 (completion report) |
| B0138 | Nwankwo Kanu | £3,000,000 (B, 1999-01-29) | £4,500,000 (1999-01-16) | DEC-404 (completion report) |
| B0140 | Rigobert Song | £2,600,000 (B, 1999-01-23) | £2,700,000 (1999-01-26) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0142 | Paolo Di Canio | £1,500,000 (B, 1999-01-28) | £2,000,000 (1999-01-27) | DEC-404 (completion report) |
| B0150 | Steve Stone | £6,000,000 (B, 1999-03-11) | £5,500,000 (1999-03-14) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0153 | Lee Carsley | £3,375,000 (B, 1999-03-23) | £3,300,000 (1999-03-20), £3,400,000 (1999-03-28) | DEC-404 (completion report) |
| B0157 | Richard Cresswell | £1,000,000 (B, 1999-04-04) | £950,000 (1999-03-26) | DEC-404 (completion report) |
| B0158 | Silvio Marić | £3,300,000 (B, 1999-02-05) | £3,500,000 (1999-02-07), £3,650,000 (1999-02-26) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0161 | Sami Hyypia | £3,000,000 (B, 1999-05-18) | £2,800,000 (1999-07-20) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0168 | Alain Goma | £4,750,000 (B, 1999-06-15) | £4,700,000 (1999-06-19) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0169 | Danny Mills | £3,800,000 (B, 1999-06-15) | £4,000,000 (1999-06-19) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0176 | David Wetherall | £1,400,000 (B, 1999-07-01) | £2,000,000 (1999-06-30) | DEC-404 (completion report) |
| B0177 | Vladimir Smicer | £4,000,000 (B, 1999-06-17) | £4,200,000 (1999-07-20) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0178 | Lee Clark | £2,500,000 (B, 1999-07-10) | £3,000,000 (1999-08-07) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0179 | Eyal Berkovic | £5,750,000 (B, 1999-07-09) | £5,500,000 (1999-07-08) | DEC-404 (completion report) |
| B0185 | Clyde Wijnhard | £750,000 (B, 1999-08-04) | £1,000,000 (1999-08-06) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0190 | Craig Short | £2,100,000 (B, 1999-08-02) | £2,000,000 (1999-08-07) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0196 | John Oster | £750,000 (B, 1999-08-02) | £1,000,000 (1999-08-07) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0197 | Øyvind Leonhardsen | £2,500,000 (B, 1999-08-05) | £3,000,000 (1999-08-07) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0198 | Darren Huckerby | £4,000,000 (B, 1999-08-11) | £4,500,000 (1999-09-10) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0199 | Gabriele Ambrosetti | £3,000,000 (B, 1999-08-12) | £3,500,000 (1999-08-14) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0229 | Darren Holloway | £1,300,000 (B, 2000-10-14) | £500,000 (2000-10-03) | DEC-404 (completion report) |
| B0231 | Alf-Inge Haaland | £2,500,000 (B, 2000-07-09) | £2,800,000 (2000-07-27) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0237 | Steve Watson | £2,500,000 (B, 2000-06-29) | £2,000,000 (2000-08-18) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0238 | Christian Karembeu | £2,100,000 (B, 2000-07-06) | £2,250,000 (2000-06-15), £2,500,000 (2000-08-19) | DEC-404 (completion report) |
| B0243 | Alex Nyarko | £4,600,000 (B, 2000-07-14) | £4,500,000 (2000-07-14) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0244 | Don Hutchison | £2,500,000 (B, 2000-07-14) | £2,250,000 (2000-07-27) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0246 | Niclas Alexandersson | £2,500,000 (B, 2000-07-19) | £2,250,000 (2000-07-27) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0248 | Thomas Gravesen | £2,800,000 (B, 2000-07-23) | £2,500,000 (2000-07-25) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0249 | Julio Arca | £3,000,000 (B, 2000-07-22) | £3,500,000 (2000-08-18) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0251 | Alpay Özalan | £5,600,000 (B, 2000-07-20) | £4,700,000 (2000-07-20) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0252 | Didier Deschamps | £2,300,000 (B, 2000-07-29) | £3,700,000 (2000-08-18) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0256 | Noel Whelan | £2,500,000 (B, 2000-07-28) | £2,000,000 (2000-08-19) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0258 | David Thompson | £2,500,000 (B, 2000-08-02) | £2,750,000 (2000-07-28) | DEC-404 (completion report) |
| B0259 | Alen Bokšić | £2,500,000 (B, 2000-08-04) | £2,000,000 (2000-08-18) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0261 | Duncan Ferguson | £3,500,000 (B, 2000-08-11) | £3,700,000 (2000-08-11), £3,750,000 (2000-08-18) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0264 | Steve Howey | £2,000,000 (B, 2000-08-11) | £3,500,000 (2001-02-26) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0269 | Clarence Acuña | £1,000,000 (B, 2000-10-10) | £700,000 (2000-09-29) | DEC-404 (completion report) |
| B0270 | Mark Fish | £1,500,000 (B, 2000-10-18) | £850,000 (2000-11-07) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0274 | Igor Biscan | £7,000,000 (B, 2000-10-13) | £5,000,000 (2000-12-05), £5,500,000 (2000-12-08) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0282 | Didier Domi | £3,500,000 (B, 2001-01-16) | £4,000,000 (2001-01-20) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0284 | Wayne Quinn | £1,500,000 (B, 2001-01-16) | £800,000 (2001-02-20) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0285 | Chris Makin | £1,250,000 (B, 2001-03-08) | £2,000,000 (2001-03-06) | DEC-404 (completion report) |
| B0290 | William Gallas | £6,200,000 (B, 2001-05-21) | £6,900,000 (2001-07-27) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0294 | Luis Boa Morte | £1,700,000 (B, 2001-06-15) | £1,600,000 (2001-08-01) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0295 | Corrado Grabbi | £7,000,000 (B, 2001-07-27) | £6,700,000 (2001-08-01), £6,750,000 (2001-08-20) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0297 | John Arne Riise | £4,500,000 (B, 2001-06-18) | £4,600,000 (2001-08-01) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0313 | Milan Baroš | £3,500,000 (B, 2001-08-07) | £3,400,000 (2001-12-07) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0316 | Laurent Robert | £10,000,000 (B, 2001-08-01) | £10,500,000 (2001-07-25) | DEC-404 (completion report) |
| B0322 | Michael Ball | £6,000,000 (B, 2001-08-18) | £6,500,000 (2001-08-09), £7,000,000 (2001-08-01) | DEC-404 (completion report) |
| B0327 | Allan Johnston | £600,000 (B, 2001-08-31) | £1,000,000 (2001-07-30) | DEC-404 (completion report) |
| B0336 | Diego Forlán | £7,500,000 (B, 2002-01-23) | £6,918,705 (2002-01-18), £7,412,898 (2002-01-18) | sterling figure before a converted one (contract rule) |
| B0337 | Joachim Björklund | £1,500,000 (B, 2002-01-28) | £1,528,491 (2002-01-28) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0338 | Abel Xavier | £800,000 (B, 2002-01-30) | £792,876 (2002-01-30) | earliest report (DEC-277), or the completion report when it is also the earliest |
| B0340 | Ade Akinbiyi | £2,200,000 (B, 2002-02-05) | £2,449,629 (2002-02-05) | earliest report (DEC-277), or the completion report when it is also the earliest |

**League-wide spending by window, 1997–2002** (before = commit c62ca6b, the end of IQ-15e; published totals from part17b are research leads, UNVERIFIED; the list has no gross total for any of these windows, so there is nothing to compare against):

| Window | Gross before | Gross after | Change | Published gross | Net before | Net after |
|---|---|---|---|---|---|---|
| summer 1997 | £144.4m | £141.2m | −£3.2m | — | £59.0m | £55.9m |
| January 1998 | £51.2m | £50.0m | −£1.2m | — | £12.1m | £15.3m |
| summer 1998 | £162.6m | £163.6m | £1.0m | — | £80.7m | £82.8m |
| January 1999 | £93.7m | £92.0m | −£1.7m | — | £36.2m | £34.3m |
| summer 1999 | £172.5m | £166.2m | −£6.3m | — | £56.7m | £52.4m |
| January 2000 | £43.8m | £37.2m | −£6.5m | — | £21.2m | £18.3m |
| summer 2000 | £245.8m | £243.3m | −£2.5m | — | £92.3m | £92.3m |
| January 2001 | £64.3m | £67.0m | £2.7m | — | −£8.4m | −£5.1m |
| summer 2001 | £289.4m | £282.7m | −£6.7m | — | £173.7m | £169.2m |
| January 2002 | £60.2m | £64.1m | £3.9m | — | £29.6m | £33.8m |
| summer 2002 | £174.7m | £174.7m | −£0.0m | — | £115.4m | £115.3m |

Total gross summer 1997 to summer 2002: £1.50bn before, £1.48bn after (−£20.5m).

**Effect on the race** (against the build at c62ca6b): the leader changes at 8 month ends (1997-07: Liverpool → Newcastle United; 1997-08: Liverpool → Newcastle United; 1997-09: Liverpool → Newcastle United; 1997-10: Liverpool → Newcastle United; 1997-11: Liverpool → Newcastle United; 1998-02: Liverpool → Newcastle United; 2002-06: Leeds United → Liverpool; 2016-07: Chelsea → Manchester City); who is in the top 12 changes at 156 month ends (1995-02: in Ipswich Town, out Newcastle United; 1995-03: in Ipswich Town, out Newcastle United; 1995-04: in Ipswich Town, out Newcastle United; 1995-05: in Ipswich Town, out Newcastle United; 1998-07: in West Ham United, out Coventry City; 1998-09: in West Ham United, out Coventry City; 1998-10: in Coventry City, out Blackburn Rovers; 1999-12: in Leicester City, out Arsenal; 2000-01: in Everton, out Arsenal; 2000-02: in Everton, out Arsenal …); the order within the top 12 changes at 354 month ends.

**Luke's answers to the list A questions (report section 11; Cowork chat, 8 Oct 2026): yes to all three, kept as built.**

- **DEC-405:** two players sold for one fee: the fee is booked once, on one transfer of the pair, and the partner counts £0; a split is never invented (Charles and Tommy Johnson £2.9m; McKee and Whitworth £530,000; Billington and McKeever £500,000). The same rule is applied in list B (Robinson and Coppinger £500,000; Zúñiga and Zevallos £800,000; the £500,000 cash in the Stuart, Tiler and Ward swap).
- **DEC-406:** Parker and Carr (Aston Villa ↔ Leicester City, Feb 1995): £550,000 for Parker and £0 for Carr; the cash figure goes into the next research round.
- **DEC-407:** Andy Cole (Feb 1995): Cole counts £7m (£6m cash plus Keith Gillespie, valued at £1m by a grade B source) and Gillespie £1m, under the approved swap rule; Manchester United's net spend still reflects the £6m cash.

**Questions for Luke on list B (each with Claude's recommendation)**

1. **Your completion-report rule (DEC-404) outside the lists you named.** Applied to the whole build, it also changes 20 fees after 2002 (for example Carvalho £16.5m → £19.8m, Kane £100m → £86.4m initial, Rodri 2019 £68.2m → £62.8m), all listed in `source/dec404_changes.csv`. *Recommendation:* keep it everywhere, so one rule settles every same-grade conflict.
2. **"Undisclosed" or "nominal" in the quality press (DEC-408 (a)).** When a club or quality-press report names the player and calls the fee undisclosed or nominal, only a club or press figure can now be the fee (as already for Wikipedia "undisclosed", DEC-237 (g)), and a nominal fee counts as undisclosed, not free. Carbone, Poborský, Gustafsson, Curtolo and Barton now count £0, and Nevland gets the press figure of £1.5m. *Recommendation:* keep it.
3. **Danny Murphy (Crewe → Liverpool, 1997).** The fee in use is £2m, the fee Crewe agreed with both clubs (earliest report). The completion reports say Liverpool paid an initial £1.5m in a deal "which could eventually be worth £3m" ("£1.5m down plus instalments that could almost double the fee"). Lists give £1.5m and £2.75m. *Recommendation:* count the £1.5m initial payment, the only guaranteed figure (your add-ons rule), and keep the rest out until a source says it was paid.
4. **Kanu (Internazionale → Arsenal, 1999).** Under DEC-404 the fee is £3m ("signed Kanu for £3m … two weeks ago"). The earlier reports and a season list give about £4.5m ("not disclosed but believed to be around £4.5m"). *Recommendation:* keep £3m under your rule, but flag it for the next research round because it is a large gap.
5. **Runar Normann (Lillestrøm → Coventry, 1999).** The Guardian's list gives £1m; the Independent says the fee was undisclosed and "way below" £1m. The build now uses £1m (the only figure; neither page is confirmed at source yet). *Recommendation:* count £0 (undisclosed) because a source of the same grade disputes the £1m; ask round 2 for the figure.
6. **Jim Magilton (Sheffield Wednesday → Ipswich, 1999).** The press gives only a maximum ("could eventually be worth £1m"), and the £682,500 on the Wikipedia list cites no source and was not found anywhere. Counted £0 under DEC-276. *Recommendation:* keep £0 and add it to round 2.
7. **34 list B deals still not confirmed at source** (listed in `tier1_needs_press_source.csv`). Most are weekly transfer lists that name the player and his new club but not the old one, so they fail the both-clubs check you set for source rounds. *Recommendation:* keep the rule, and carry these deals into round 2 with a request for a page naming both clubs.

**Answered by Luke (Cowork chat, 8 Oct 2026): yes to all seven, recommendations applied (DEC-410 to DEC-416).** Murphy now counts the £1.5m initial payment and Normann £0; the fees resting on a "reported"-type completion figure are listed in `source/dec404_soft_figures.csv` and go to research round 2. Detailed data and method questions are now decided by Claude within the agreed rules (DEC-417).

## 13. Research round 2: the list (IQ-15g, DEC-418)

`data/rtt-101/source_round2_list.csv` holds **755 deals** (R0001 onwards, in date order, all seasons 1992–2026) that still need research; it carries no fee figures. Each deal maps to its transfer(s) in `data/rtt-101/source/source_round2_map.csv`. What each needs:

- fee from a page naming both clubs: 658
- press or club source for the fee (only a database confirms it): 72
- exact guaranteed fee, only a maximum or approximation found: 18
- firmer figure than 'reported': 5
- cash part of a part-exchange: 1
- firmer figure, reports disagree: 1
- fee, one report says undisclosed and another gives a figure: 1

| Season | Deals |
|---|---|
| 1992-93 | 9 |
| 1993-94 | 13 |
| 1994-95 | 24 |
| 1995-96 | 31 |
| 1996-97 | 28 |
| 1997-98 | 21 |
| 1998-99 | 24 |
| 1999-00 | 20 |
| 2000-01 | 18 |
| 2001-02 | 11 |
| 2002-03 | 42 |
| 2003-04 | 24 |
| 2004-05 | 31 |
| 2005-06 | 39 |
| 2006-07 | 33 |
| 2007-08 | 41 |
| 2008-09 | 28 |
| 2009-10 | 12 |
| 2010-11 | 10 |
| 2011-12 | 12 |
| 2012-13 | 22 |
| 2013-14 | 18 |
| 2014-15 | 16 |
| 2015-16 | 37 |
| 2016-17 | 25 |
| 2017-18 | 23 |
| 2018-19 | 8 |
| 2019-20 | 9 |
| 2020-21 | 10 |
| 2021-22 | 8 |
| 2022-23 | 15 |
| 2023-24 | 17 |
| 2024-25 | 24 |
| 2025-26 | 24 |
| 2026-27 | 28 |

## 14. Source round 2: the priority deals (IQ-15h; DEC-419 to DEC-421)

- **Inputs:** ChatGPT instalment 1 (R0001–R0030, private part22b) and the Claude helper research on the 323 priority deals (part23g = part22c + part23a–f, 992 rows): every data file's SHA-256 matched `00_README.md` (the prompt and the helper instructions have no recorded hash). Rows attached to their deals through `source/source_round2_map.csv`; **352 deals researched**. Aggregator, scores and blog sites count as grade C whatever the file says; Ajax's acc-english pages were read at english.ajax.nl.
- **Checked at source:** all 1,015 cited pages read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/37888858665): 886 loaded; 42 not found, 41 refused, 13 server errors (including West Ham's club pages), 15 timed out. A figure counts only when it sits next to the player's name and the page names both clubs, so a helper quote that the page does not carry is never used.
- **Quotes read:** 402 newly confirmed quotes (41 rejected: another deal's figure, a valuation or a garbled currency on the page, a maximum, a total with add-ons, a buy-back clause, a range, or a package including an unvalued player).
- **VERIFIED:** 285 of the 352 researched transfers now have a fee confirmed at source (275 by a club, league or press source), up from 24 before this round.
- **Changed:** 163 fees changed (£291.8m up, £250.8m down; net £41.1m) and 1 completion date(s) moved.

| Deal | Player | Move | Date before → after | Fee before | Fee after | Why |
|---|---|---|---|---|---|---|
| R0009 | Glenn Pennyfather | Ipswich Town → Bristol City | 1993-03-01 | £80,000 | £50,000 | confirmed at source (B, www.the-independent.com) |
| R0012 | Nikki Papavasiliou | OFI → Newcastle United | 1993-07-31 | £120,000 | £125,000 | confirmed at source (B, www.the-independent.com) |
| R0015 | Paul Allen | Tottenham Hotspur → Southampton | 1993-09-16 | £550,000 | £500,000 | confirmed at source (C, www.soccerbase.com) |
| R0018 | Mike Jeffrey | Doncaster Rovers → Newcastle United | 1993-10-04 | £85,000 | £60,000 | part-exchange (DEC-237 (d)): cash only unless a source values the player; decided under DEC-417 (IQ-15h) |
| R0023 | Michael Stensgaard | Hvidovre IF → Liverpool | 1994-06-01 | £400,000 | £20,000 | confirmed at source (B, www.the-independent.com) |
| R0024 | Nigel Worthington | Sheffield Wednesday → Leeds United | 1994-07-04 | £325,000 | £350,000 | confirmed at source (B, www.the-independent.com) |
| R0025 | Darren Pitcher | Charlton Athletic → Crystal Palace | 1994-07-05 | £700,000 | £50,000 | confirmed at source (B, www.the-independent.com) |
| R0026 | Tony Daley | Aston Villa → Wolverhampton Wanderers | 1994-07-06 → 1994-05-31 | £1,250,000 | £1,250,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| R0028 | Neil Cox | Aston Villa → Middlesbrough | 1994-07-19 | £1,000,000 | £750,000 | confirmed at source (B, www.the-independent.com) |
| R0236 | Robbie Fowler | Leeds United → Manchester City | 2003-01-30 | £6,000,000 | £3,000,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| R0243 | David Dunn | Blackburn Rovers → Birmingham City | 2003-07-07 | £5,500,000 | £5,773,990 | confirmed at source (B, www.uefa.com) |
| R0245 | Glen Johnson | West Ham United → Chelsea | 2003-07-15 | £6,000,000 | £0 | every A/B source calls the fee undisclosed: counted £0 (DEC-237 (g), DEC-408 (a)) |
| R0248 | Wayne Bridge | Southampton → Chelsea | 2003-07-21 | £7,000,000 | £6,948,876 | confirmed at source (B, www.uefa.com) |
| R0255 | Juan Sebastián Verón | Manchester United → Chelsea | 2003-08-06 | £15,000,000 | £11,000,000 | confirmed at source (B, archive.thedailystar.net) |
| R0269 | Arjen Robben | PSV → Chelsea | 2004-06-08 | £7,000,000 | £12,000,000 | confirmed at source (B, archive.thedailystar.net) |
| R0270 | Petr Čech | Rennes → Chelsea | 2004-06-08 | £12,000,000 | £6,884,567 | confirmed at source (B, www.uefa.com) |
| R0303 | Asier del Horno | Athletic Bilbao → Chelsea | 2005-06-21 | £8,000,000 | £7,973,952 | confirmed at source (B, uefa.com) |
| R0304 | Per Krøldrup | Udinese → Everton | 2005-06-27 | £5,000,000 | £4,528,503 | confirmed at source (B, www.uefa.com) |
| R0306 | Alexander Hleb | VfB Stuttgart → Arsenal | 2005-06-27 | £11,200,000 | £9,989,345 | confirmed at source (B, uefa.com) |
| R0308 | Mateja Kežman | Chelsea → Atlético Madrid | 2005-06-29 | £5,300,000 | £5,685,238 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0311 | Yakubu | Portsmouth → Middlesbrough | 2005-07-07 | £6,000,000 | £7,500,000 | confirmed at source (B, www.gazettelive.co.uk) |
| R0314 | Shaun Wright-Phillips | Manchester City → Chelsea | 2005-07-18 | £21,000,000 | £17,000,000 | confirmed at source (B, www.theguardian.com) |
| R0321 | Tiago Mendes | Chelsea → Olympique Lyonnais | 2005-08-27 | £6,500,000 | £6,000,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0336 | Tomáš Rosický | Borussia Dortmund → Arsenal | 2006-05-23 | £6,800,000 | £6,825,007 | confirmed at source (B, www.uefa.com) |
| R0340 | Eiður Guðjohnsen | Chelsea → Barcelona | 2006-06-14 | £8,000,000 | £7,995,626 | confirmed at source (B, www.uefa.com) |
| R0357 | Pascal Chimbonda | Wigan Athletic → Tottenham Hotspur | 2006-08-31 | £6,000,000 | £4,500,000 | higher-ranked figure now on file (not yet confirmed at source; C) |
| R0372 | Joey Barton | Manchester City → Newcastle United | 2007-06-14 | £5,800,000 | £5,500,000 | confirmed at source (B, www.channel4.com) |
| R0392 | Alan Smith | Manchester United → Newcastle United | 2007-08-03 | £6,000,000 | £6,076,565 | confirmed at source (B, www.uefa.com) |
| R0395 | José Enrique Sánchez | Villarreal → Newcastle United | 2007-08-06 | £6,300,000 | £6,315,789 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0397 | Kieron Dyer | Newcastle United → West Ham United | 2007-08-16 | £6,000,000 | £5,000,000 | higher-ranked figure now on file (not yet confirmed at source; A) |
| R0400 | Yakubu | Middlesbrough → Everton | 2007-08-29 | £11,250,000 | £11,248,137 | confirmed at source (B, www.uefa.com) |
| R0404 | James McFadden | Everton → Birmingham City | 2008-01-18 | £5,000,000 | £5,015,721 | confirmed at source (B, www.uefa.com) |
| R0409 | Luka Modrić | Dinamo Zagreb → Tottenham Hotspur | 2008-04-29 | £16,625,762 | £18,209,168 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| R0413 | Jô | CSKA Moscow → Manchester City | 2008-07-02 | £19,000,000 | £18,077,566 | confirmed at source (B, www.uefa.com) |
| R0418 | Peter Crouch | Liverpool → Portsmouth | 2008-07-11 | £9,000,000 | £8,750,000 | confirmed at source (B, www.dailypost.co.uk) |
| R0420 | Alexander Hleb | Arsenal → Barcelona | 2008-07-16 | £11,800,000 | £11,900,000 | confirmed at source (B, cityam.com) |
| R0424 | Sulley Muntari | Portsmouth → Internazionale | 2008-07-28 | £12,700,000 | £11,065,444 | confirmed at source (B, www.uefa.com) |
| R0438 | Christian Benítez | Santos Laguna → Birmingham City | 2009-06-03 | £7,000,000 | £6,200,000 | confirmed at source (B, www.expressandstar.com) |
| R0459 | Luis Suárez | Ajax → Liverpool | 2011-01-31 | £23,000,000 | £22,677,323 | confirmed at source (B, www.aljazeera.com) |
| R0463 | Cesc Fàbregas | Arsenal → Barcelona | 2011-08-15 | £25,400,000 | £25,539,410 | confirmed at source (B, www.deseret.com) |
| R0466 | Bryan Ruiz | FC Twente → Fulham | 2011-08-31 | £10,600,000 | £9,949,638 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| R0471 | Marko Marin | Werder Bremen → Chelsea | 2012-04-28 | £7,000,000 | £6,578,406 | confirmed at source (B, www.uefa.com) |
| R0472 | Niko Kranjčar | Tottenham Hotspur → Dynamo Kyiv | 2012-06-07 | £5,750,000 | £5,500,000 | confirmed at source (B, www.portsmouth.co.uk) |
| R0483 | César Azpilicueta | Marseille → Chelsea | 2012-08-24 | £6,500,000 | £7,000,000 | confirmed at source (B, amp.foxsports.com) |
| R0484 | Luka Modrić | Tottenham Hotspur → Real Madrid | 2012-08-27 | £30,000,000 | £27,870,730 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| R0486 | Rafael van der Vaart | Tottenham Hotspur → Hamburg SV | 2012-08-31 | £10,000,000 | £10,317,460 | confirmed at source (B, www.thelocal.de) |
| R0487 | Pablo Hernández | Valencia → Swansea City | 2012-08-31 | £5,550,000 | £5,666,793 | confirmed at source (B, www.foxnews.com) |
| R0488 | Charlie Adam | Liverpool → Stoke City | 2012-08-31 | £5,000,000 | £4,000,000 | confirmed at source (B, www.yorkshireeveningpost.co.uk) |
| R0490 | Matija Nastasić | Fiorentina → Manchester City | 2012-08-31 | £10,000,000 | £12,000,000 | confirmed at source (B, gulfnews.com) |
| R0496 | Andreas Cornelius | Copenhagen → Cardiff City | 2013-07-01 | £7,500,000 | £8,000,000 | confirmed at source (B, www.nbcsports.com) |
| R0497 | Marco van Ginkel | Vitesse Arnhem → Chelsea | 2013-07-05 | £8,000,000 | £9,054,846 | confirmed at source (B, uefa.com) |
| R0500 | Álvaro Negredo | Sevilla → Manchester City | 2013-07-19 | £20,000,000 | £16,336,828 | £28,000,000 not counted: 'around €28 million' is a total with add-ons; British media give £16.4m rising to about £20m (guaranteed fee only); £24,000,0 |
| R0503 | Gervinho | Arsenal → Roma | 2013-08-08 | £8,000,000 | £6,884,089 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0505 | Mesut Özil | Real Madrid → Arsenal | 2013-09-02 | £42,400,000 | £42,500,000 | confirmed at source (B, www.gulf-times.com) |
| R0508 | Nemanja Matić | Benfica → Chelsea | 2014-01-15 | £21,000,000 | £20,800,000 | confirmed at source (B, the42.ie) |
| R0509 | Nikica Jelavić | Everton → Hull City | 2014-01-15 | £6,500,000 | £7,500,000 | confirmed at source (B, www.thescore.com) |
| R0510 | Kurt Zouma | Saint-Étienne → Chelsea | 2014-01-31 | £12,000,000 | £12,388,219 | confirmed at source (B, www.uefa.com) |
| R0512 | Cesc Fàbregas | Barcelona → Chelsea | 2014-06-12 | £27,000,000 | £30,000,000 | confirmed at source (B, morningstaronline.co.uk) |
| R0515 | Lazar Marković | Benfica → Liverpool | 2014-07-15 | £20,000,000 | £19,787,874 | confirmed at source (B, irishtimes-irishtimes-prod.cdn.arcpublishing.com) |
| R0516 | Filipe Luís | Atlético Madrid → Chelsea | 2014-07-18 | £15,800,000 | £16,000,000 | confirmed at source (B, www.cityam.com) |
| R0519 | Abel Hernández | Palermo → Hull City | 2014-09-01 | £10,000,000 | £9,500,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0520 | Sandro | Tottenham Hotspur → Queens Park Rangers | 2014-09-01 | £6,000,000 | £10,000,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0525 | André Schürrle | Chelsea → VfL Wolfsburg | 2015-02-02 | £22,000,000 | £24,600,000 | confirmed at source (B, www.skysports.com) |
| R0528 | Memphis Depay | PSV → Manchester United | 2015-06-12 | £31,000,000 | £22,000,000 | confirmed at source (B, capitalfm.africa) |
| R0533 | Paulinho | Tottenham Hotspur → Guangzhou Evergrande | 2015-06-29 | £9,900,000 | £9,800,000 | confirmed at source (B, www.insideworldfootball.com) |
| R0536 | Thorgan Hazard | Chelsea → Borussia Mönchengladbach | 2015-07-01 | £5,900,000 | £5,685,048 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0542 | Filipe Luís | Chelsea → Atlético Madrid | 2015-07-28 | £11,100,000 | £11,000,000 | confirmed at source (B, www.tntsports.co.uk) |
| R0548 | Adama Traoré | Barcelona → Aston Villa | 2015-08-14 | £7,000,000 | £7,120,478 | confirmed at source (A, www.fcbarcelona.com) |
| R0550 | Roberto Soldado | Tottenham Hotspur → Villarreal | 2015-08-18 | £10,000,000 | £7,000,000 | confirmed at source (B, www.tntsports.co.uk) |
| R0553 | Pedro | Barcelona → Chelsea | 2015-08-20 | £21,400,000 | £21,442,356 | confirmed at source (A, www.fcbarcelona.com) |
| R0554 | Kenedy | Fluminense → Chelsea | 2015-08-22 | £6,300,000 | £6,700,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0556 | Glenn Murray | Crystal Palace → AFC Bournemouth | 2015-08-31 | £5,000,000 | £4,000,000 | confirmed at source (B, skysports.com) |
| R0558 | Michael Hector | Reading → Chelsea | 2015-09-01 | £5,400,000 | £4,000,000 | confirmed at source (B, www.graphic.com.gh) |
| R0561 | Lewis Grabban | Norwich City → AFC Bournemouth | 2016-01-11 | £7,000,000 | £8,000,000 | confirmed at source (B, www.tntsports.co.uk) |
| R0565 | Granit Xhaka | Borussia Mönchengladbach → Arsenal | 2016-05-25 | £35,000,000 | £25,000,000 | £35,000,000 not counted: £35m is a reported total; the completion report gives the initial fee as £25m (guaranteed fee only; decided under DEC-417); £ |
| R0570 | Nampalys Mendy | Nice → Leicester City | 2016-07-03 | £13,000,000 | £12,000,000 | confirmed at source (B, www.balls.ie) |
| R0572 | Henrikh Mkhitaryan | Borussia Dortmund → Manchester United | 2016-07-06 | £30,000,000 | £26,300,000 | confirmed at source (B, www.foxnews.com) |
| R0573 | Matt Phillips | Queens Park Rangers → West Bromwich Albion | 2016-07-06 | £5,500,000 | £5,000,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| R0574 | N'Golo Kanté | Leicester City → Chelsea | 2016-07-16 | £32,000,000 | £30,000,000 | confirmed at source (B, www.graphic.com.gh) |
| R0582 | Borja | Atlético Madrid → Swansea City | 2016-08-11 | £15,000,000 | £15,424,958 | confirmed at source (B, www.tsn.ca) |
| R0589 | Jeffrey Schlupp | Leicester City → Crystal Palace | 2017-01-13 | £12,000,000 | £12,500,000 | confirmed at source (B, www.fourfourtwo.com) |
| R0590 | Victor Lindelöf | Benfica → Manchester United | 2017-06-14 | £31,000,000 | £30,700,000 | confirmed at source (B, skysports.com) |
| R0591 | Mathew Ryan | Valencia → Brighton & Hove Albion | 2017-06-16 | £5,000,000 | £0 | every A/B source calls the fee undisclosed: counted £0 (DEC-237 (g), DEC-408 (a)) |
| R0595 | Steve Mounié | Montpellier → Huddersfield Town | 2017-07-05 | £11,440,000 | £11,500,000 | confirmed at source (B, www.sportinglife.com) |
| R0597 | Antonio Rüdiger | Roma → Chelsea | 2017-07-09 | £29,000,000 | £31,025,618 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| R0604 | Nemanja Matić | Chelsea → Manchester United | 2017-07-31 | £40,000,000 | £35,000,000 | £40,000,000 not counted: £40m includes add-ons: the completion reports give £35m plus £5m in add-ons (guaranteed fee only) |
| R0607 | Davinson Sánchez | Ajax → Tottenham Hotspur | 2017-08-23 | £42,000,000 | £36,937,852 | confirmed at source (B, www.tntsports.co.uk) |
| R0611 | Emerson | Roma → Chelsea | 2018-01-30 | £20,000,000 | £17,600,000 | confirmed at source (B, en.tempo.co) |
| R0615 | Lucas Torreira | Sampdoria → Arsenal | 2018-07-10 | £26,400,000 | £25,000,000 | DEC-404: the report that the deal was completed beats an earlier bid, agreed or expected figure |
| R0619 | Yerry Mina | Barcelona → Everton | 2018-08-09 | £27,190,000 | £27,203,237 | confirmed at source (A, www.fcbarcelona.com) |
| R0622 | Mateo Kovačić | Real Madrid → Chelsea | 2019-07-01 | £40,000,000 | £40,300,000 | confirmed at source (B, www.goal.com) |
| R0624 | Trézéguet | Kasımpaşa → Aston Villa | 2019-07-24 | £8,750,000 | £8,500,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0626 | Allan Saint-Maximin | Nice → Newcastle United | 2019-08-02 | £20,000,000 | £16,500,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0627 | Steven Bergwijn | PSV Eindhoven → Tottenham Hotspur | 2020-01-30 | £26,700,000 | £25,000,000 | confirmed at source (B, www.goal.com) |
| R0628 | Hakim Ziyech | Ajax → Chelsea | 2020-02-24 | £40,000,000 | £33,599,328 | confirmed at source (A, eredivisie.com) |
| R0631 | Timothy Castagne | Atalanta → Leicester City | 2020-09-03 | £25,000,000 | £21,000,000 | confirmed at source (B, www.sportinglife.com) |
| R0635 | Sergio Reguilón | Real Madrid → Tottenham Hotspur | 2020-09-19 | £29,000,000 | £27,290,094 | £27,500,000 not counted: £27.5m is Real Madrid's buy-back clause, not the fee; the fee reported is €30m plus €5m in add-ons |
| R0637 | Nélson Semedo | Barcelona → Wolverhampton Wanderers | 2020-09-23 | £27,600,000 | £27,427,318 | confirmed at source (A, www.fcbarcelona.com) |
| R0638 | Sébastien Haller | West Ham United → Ajax | 2021-01-08 | £20,200,000 | £20,292,208 | confirmed at source (B, dutchnews.nl) |
| R0639 | Saïd Benrahma | Brentford → West Ham United | 2021-01-29 | £20,000,000 | £25,000,000 | confirmed at source (B, www.sportinglife.com) |
| R0641 | Ibrahima Konaté | RB Leipzig → Liverpool | 2021-07-01 | £35,000,000 | £35,299,182 | confirmed at source (B, www.freemalaysiatoday.com) |
| R0643 | Leon Bailey | Bayer Leverkusen → Aston Villa | 2021-08-04 | £30,000,000 | £25,000,000 | £30,000,000 not counted: £30m includes add-ons: the initial fee was about £25m (guaranteed fee only) |
| R0645 | Rafa Mir | Wolverhampton Wanderers → Sevilla | 2021-08-20 | £13,000,000 | £13,726,836 | confirmed at source (B, www.expressandstar.com) |
| R0648 | Brenden Aaronson | Red Bull Salzburg → Leeds United | 2022-05-26 | £25,000,000 | £24,720,825 | confirmed at source (B, www.skysports.com) |
| R0650 | Sadio Mané | Liverpool → Bayern Munich | 2022-06-22 | £35,000,000 | £27,472,527 | £35,100,000 not counted: €41m (£35.1m) includes add-ons: the deal was €32m plus add-ons (guaranteed fee only); £43,000,000 not counted: about €41m inc |
| R0651 | Steven Bergwijn | Tottenham Hotspur → Ajax | 2022-07-08 | £26,400,000 | £26,436,004 | confirmed at source (A, english.ajax.nl) |
| R0652 | Andreas Pereira | Manchester United → Fulham | 2022-07-11 | £0 | £8,000,000 | confirmed at source (B, www.skysports.com) |
| R0654 | Djed Spence | Middlesbrough → Tottenham Hotspur | 2022-07-19 | £20,000,000 | £12,500,000 | confirmed at source (B, irishtimes.com) |
| R0655 | Lisandro Martínez | Ajax → Manchester United | 2022-07-27 | £57,000,000 | £48,262,808 | confirmed at source (A, english.ajax.nl) |
| R0660 | Danny Ings | Aston Villa → West Ham United | 2023-01-20 | £0 | £12,000,000 | confirmed at source (B, www.skysports.com) |
| R0661 | Jhon Durán | Chicago Fire → Aston Villa | 2023-01-23 | £18,000,000 | £14,750,000 | confirmed at source (B, www.offalyexpress.ie) |
| R0662 | Antoine Semenyo | Bristol City → AFC Bournemouth | 2023-01-27 | £10,000,000 | £9,000,000 | £10,500,000 not counted: £10.5m includes the £1.5m in add-ons: the fee was £9m plus £1.5m (guaranteed fee only) |
| R0663 | João Pedro | Watford → Brighton & Hove Albion | 2023-06-14 | £0 | £30,000,000 | confirmed at source (B, www.brightonandhovenews.org) |
| R0665 | Pedro Porro | Sporting CP → Tottenham Hotspur | 2023-07-01 | £34,500,000 | £40,000,000 | confirmed at source (B, uk.sports.yahoo.com) |
| R0666 | Conor Coady | Wolverhampton Wanderers → Leicester City | 2023-07-01 | £7,500,000 | £8,500,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0667 | Raúl Jiménez | Wolverhampton Wanderers → Fulham | 2023-07-25 | £5,000,000 | £5,500,000 | confirmed at source (B, expressandstar.com) |
| R0668 | Sam Surridge | Nottingham Forest → Nashville | 2023-07-25 | £5,000,000 | £5,056,005 | confirmed at source (B, www.mlssoccer.com) |
| R0669 | Calvin Bassey | Ajax → Fulham | 2023-07-28 | £19,000,000 | £21,000,000 | confirmed at source (B, supersport.com) |
| R0670 | Axel Disasi | Monaco → Chelsea | 2023-08-04 | £38,570,000 | £38,500,000 | confirmed at source (B, breakingnews.ie) |
| R0674 | Edson Álvarez | Ajax → West Ham United | 2023-08-10 | £35,000,000 | £32,874,816 | confirmed at source (A, english.ajax.nl) |
| R0676 | Beto | Udinese → Everton | 2023-08-29 | £30,000,000 | £25,750,000 | confirmed at source (B, www.skysports.com) |
| R0679 | Radu Drăgușin | Genoa → Tottenham Hotspur | 2024-01-11 | £25,000,000 | £26,700,000 | confirmed at source (B, www.skysports.com) |
| R0682 | Douglas Luiz | Aston Villa → Juventus | 2024-06-30 | £42,400,000 | £42,350,000 | confirmed at source (B, expressandstar.com) |
| R0683 | Enzo Barrenechea | Juventus → Aston Villa | 2024-07-01 | £6,800,000 | £6,787,714 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0684 | Samuel Iling-Junior | Juventus → Aston Villa | 2024-07-01 | £11,900,000 | £11,878,500 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0686 | Archie Gray | Leeds United → Tottenham Hotspur | 2024-07-02 | £40,000,000 | £25,000,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0688 | Mason Greenwood | Manchester United → Marseille | 2024-07-18 | £0 | £27,000,000 | confirmed at source (B, sports.yahoo.com) |
| R0689 | Sávio | Troyes → Manchester City | 2024-07-18 | £30,800,000 | £21,100,000 | confirmed at source (B, uk.sports.yahoo.com) |
| R0691 | Moussa Diaby | Aston Villa → Al-Ittihad | 2024-07-24 | £50,400,000 | £50,317,387 | confirmed at source (B, www.tsn.ca) |
| R0695 | Julián Álvarez | Manchester City → Atlético Madrid | 2024-08-12 | £64,400,000 | £64,137,661 | £82,000,000 not counted: £82m is the headline including add-ons: the deal was €75m initial plus up to €20m (guaranteed fee only); £81,000,000 not coun |
| R0698 | Ferdi Kadıoğlu | Fenerbahçe → Brighton & Hove Albion | 2024-08-27 | £25,000,000 | £25,357,008 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0699 | Manuel Ugarte | Paris Saint-Germain → Manchester United | 2024-08-30 | £50,000,000 | £42,105,263 | £50,500,000 not counted: 'a fee that could reach £50.5m' is a maximum (guaranteed fee only) |
| R0700 | Donyell Malen | Borussia Dortmund → Aston Villa | 2025-01-14 | £21,500,000 | £19,407,645 | confirmed at source (B, capitalfm.africa) |
| R0702 | Jhon Durán | Aston Villa → Al Nassr | 2025-01-31 | £71,000,000 | £65,000,000 | confirmed at source (B, www.tntsports.co.uk) |
| R0704 | Giorgi Mamardashvili | Valencia → Liverpool | 2025-06-01 | £29,000,000 | £25,492,862 | £25,600,000 not counted: £29.9m is the total including £4.3m in add-ons; the initial fee was £25.6m (€30m); £39,770,000 not counted: 'around 30 millio |
| R0705 | Yasin Özcan | Kasımpaşa → Aston Villa | 2025-06-01 | £5,830,000 | £7,000,000 | higher-ranked figure now on file (not yet confirmed at source; C) |
| R0708 | Jean-Clair Todibo | Nice → West Ham United | 2025-07-01 | £32,800,000 | £26,800,000 | £32,900,000 not counted: £32.9m (€39m) is a total reported later, not the purchase price paid |
| R0713 | Luis Díaz | Liverpool → Bayern Munich | 2025-07-30 | £65,500,000 | £65,000,000 | confirmed at source (B, www.expressandstar.com) |
| R0714 | Kiernan Dewsbury-Hall | Chelsea → Everton | 2025-08-06 | £25,000,000 | £24,000,000 | confirmed at source (B, thefinancialexpress.com.bd) |
| R0715 | Lesley Ugochukwu | Chelsea → Burnley | 2025-08-06 | £25,000,000 | £23,000,000 | confirmed at source (B, www.beinsports.com) |
| R0716 | Armando Broja | Chelsea → Burnley | 2025-08-08 | £20,000,000 | £10,000,000 | confirmed at source (B, www.thescore.com) |
| R0717 | Benjamin Šeško | RB Leipzig → Manchester United | 2025-08-09 | £66,300,000 | £66,233,766 | £99,000,000 not counted: 'up to 85 million euros' is a maximum; the deal was €76.5m plus €8.5m in add-ons (guaranteed fee only) |
| R0718 | Darwin Núñez | Liverpool → Al Hilal | 2025-08-09 | £46,300,000 | £46,000,000 | £65,600,000 not counted: 'worth up to' is a maximum; the initial fee was £46m (€53m) (guaranteed fee only) |
| R0719 | Malick Thiaw | AC Milan → Newcastle United | 2025-08-12 | £0 | £30,250,648 | £46,690,000 not counted: about £34.6m is the total with add-ons; the initial fee was €35m (guaranteed fee only) |
| R0720 | Bafodé Diakité | Lille → AFC Bournemouth | 2025-08-13 | £30,300,000 | £30,224,525 | confirmed at source (B, www.malaymail.com) |
| R0721 | Amine Adli | Bayer Leverkusen → AFC Bournemouth | 2025-08-21 | £25,100,000 | £25,000,000 | confirmed at source (B, supersport.com) |
| R0723 | Mateus Fernandes | Southampton → West Ham United | 2025-08-29 | £0 | £38,000,000 | confirmed at source (B, www.skysports.com) |
| R0726 | Lucas Paquetá | West Ham United → Flamengo | 2026-01-30 | £35,500,000 | £36,500,000 | confirmed at source (B, www.beinsports.com) |
| R0727 | Jørgen Strand Larsen | Wolverhampton Wanderers → Crystal Palace | 2026-02-02 | £48,000,000 | £43,000,000 | £48,000,000 not counted: £48m is the package with add-ons: an initial £43m rising to £48m (guaranteed fee only) |
| R0731 | Rasmus Højlund | Manchester United → Napoli | 2026-06-29 | £38,000,000 | £37,947,391 | confirmed at source (B, citizen.digital) |
| R0732 | Donyell Malen | Aston Villa → Roma | 2026-06-29 | £21,600,000 | £25,000,000 | higher-ranked figure now on file (not yet confirmed at source; B) |
| R0733 | Emmanuel Emegha | Strasbourg → Chelsea | 2026-07-01 | £22,000,000 | £0 | every A/B source calls the fee undisclosed: counted £0 (DEC-237 (g), DEC-408 (a)) |
| R0735 | Eliezer Mayenda | Sunderland → Rennes | 2026-07-05 | £0 | £17,073,587 | confirmed at source (B, ligue1.com) |
| R0736 | Bazoumana Touré | TSG Hoffenheim → Newcastle United | 2026-07-05 | £42,000,000 | £43,000,000 | confirmed at source (B, www.newcastleworld.com) |
| R0737 | Álvaro Rodríguez | Elche → AFC Bournemouth | 2026-07-14 | £25,700,000 | £21,343,806 | confirmed at source (B, www.elgoldigital.com) |
| R0738 | Luka Vušković | Tottenham Hotspur → Brighton & Hove Albion | 2026-07-14 | £46,000,000 | £45,878,404 | confirmed at source (B, www.foxsports.com) |
| R0739 | Tarik Muharemović | Sassuolo → Leeds United | 2026-07-17 | £34,100,000 | £34,000,000 | confirmed at source (B, www.yorkshirepost.co.uk) |
| R0741 | António Silva | Benfica → AFC Bournemouth | 2026-08-01 | £25,700,000 | £25,000,000 | confirmed at source (B, thescore.com) |
| R0743 | Gonzalo García | Real Madrid → Fulham | 2026-08-03 | £34,000,000 | £34,272,984 | confirmed at source (B, www.arise.tv) |
| R0745 | James Trafford | Manchester City → Leeds United | 2026-08-06 | £0 | £40,000,000 | confirmed at source (B, www.skysports.com) |
| R0747 | Amar Dedić | Benfica → Newcastle United | 2026-08-18 | £30,000,000 | £29,500,000 | confirmed at source (B, skysports.com) |
| R0748 | Curtis Jones | Liverpool → Inter Milan | 2026-08-21 | £0 | £25,600,000 | confirmed at source (B, www.expressandstar.com) |
| R0749 | Sávio | Manchester City → Tottenham Hotspur | 2026-08-25 | £75,000,000 | £85,000,000 | confirmed at source (B, www.skysports.com) |
| R0750 | Nico González | Manchester City → Newcastle United | 2026-08-26 | £52,000,000 | £50,000,000 | confirmed at source (B, www.skysports.com) |

**Deal structures applied in round 2** (`source/deal_structure.csv`):

| Player | Fee booked | Rule | Note |
|---|---|---|---|
| Mike Jeffrey | £60,000 | part-exchange (DEC-237 (d)): cash only unless a source values the player; decided under DEC-417 (IQ-15h) | the same page values Roche at £25,000, so Jeffrey counts the whole £60,000 (£35,000 cash plus Roche) and Roche £25,000, as for Cole and Gillespie (DEC-407) |
| David Roche | £25,000 | part-exchange (DEC-237 (d)): cash only unless a source values the player; decided under DEC-417 (IQ-15h) | Cowork read the valuation on this page in Luke's Chrome (8 Oct); the runner's quote for this page is Jeffrey's sentence |
| Paul Mortimer | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player; decided under DEC-417 (IQ-15h) | Mortimer and David Whyte went to Charlton in the exchange for Pitcher with no stated value; Palace paid £50,000 cash |
| David Whyte | £0 | part-exchange (DEC-237 (d)): cash only unless a source values the player; decided under DEC-417 (IQ-15h) | see Paul Mortimer |
| Georginio Rutter | £0 | maximum or approximation only (DEC-276); decided under DEC-417 (IQ-15h) | the initial fee is reported only as a range and the other figures are totals ('rising to', '£35.5m'); a range is never chosen between |
| Lucca Brughmans | £0 | maximum or approximation only (DEC-276); decided under DEC-417 (IQ-15h) | every A/B report gives only the maximum; the '€35m deal' is on a grade C page |
| Tony Daley | date only: 1994-05-31 | completion date from the grade B report (IQ-15h) |  |

**Deals counted £0 because only a maximum or an approximation had been found (DEC-276): 18 on the priority list.**

| Deal | Player | Now | Status | Basis |
|---|---|---|---|---|
| R0148 | Jim Magilton | £0 | UNVERIFIED | maximum only: counted £0 (DEC-276) |
| R0169 | Stephen Hughes | £0 | UNVERIFIED | only a maximum, a total with add-ons or a combined fee found: counted £0 (DEC-276) |
| R0187 | Dean Windass | £0 | UNVERIFIED | maximum only: counted £0 (DEC-276) |
| R0193 | Matteo Sereni | £0 | UNVERIFIED | approximation only: counted £0 (DEC-276) |
| R0379 | Darren Bent | £0 | UNVERIFIED | only a maximum, a total with add-ons or a combined fee found: counted £0 (DEC-276) |
| R0457 | Asamoah Gyan | £0 | UNVERIFIED | only a maximum, a total with add-ons or a combined fee found: counted £0 (DEC-276) |
| R0652 | Andreas Pereira | £8,000,000 | VERIFIED | reported |
| R0659 | Georginio Rutter | £0 | UNVERIFIED | approximation only: counted £0 (DEC-276) |
| R0660 | Danny Ings | £12,000,000 | VERIFIED | stated |
| R0663 | João Pedro | £30,000,000 | VERIFIED | reported |
| R0688 | Mason Greenwood | £27,000,000 | VERIFIED | reported |
| R0719 | Malick Thiaw | £30,250,648 | VERIFIED | reported |
| R0723 | Mateus Fernandes | £38,000,000 | VERIFIED | stated |
| R0734 | Anthony Gordon | £0 | UNVERIFIED | only a maximum, a total with add-ons or a combined fee found: counted £0 (DEC-276) |
| R0735 | Eliezer Mayenda | £17,073,587 | VERIFIED | reported |
| R0745 | James Trafford | £40,000,000 | VERIFIED | stated |
| R0748 | Curtis Jones | £25,600,000 | VERIFIED | stated |
| R0753 | Lucca Brughmans | £0 | UNVERIFIED | maximum only: counted £0 (DEC-276) |

**League-wide spending by window** (before = commit 4b0f91c; windows that moved by £0.1m or more; published totals from part17b are research leads, UNVERIFIED):

| Window | Gross before | Gross after | Change | Published gross | Net before | Net after |
|---|---|---|---|---|---|---|
| summer 1994 | £71.4m | £70.4m | −£1.0m | — | £31.2m | £31.1m |
| January 1998 | £49.7m | £50.0m | £0.3m | — | £15.0m | £15.3m |
| summer 2000 | £243.0m | £243.3m | £0.3m | — | £92.0m | £92.3m |
| summer 2001 | £280.2m | £282.7m | £2.5m | — | £166.7m | £169.2m |
| January 2003 | £39.8m | £36.6m | −£3.2m | £35.0m (B) | £17.2m | £17.0m |
| summer 2003 | £204.9m | £195.1m | −£9.8m | £215.0m (B) | £119.2m | £113.2m |
| January 2004 | £44.0m | £45.8m | £1.9m | — | £17.4m | £18.8m |
| summer 2004 | £207.2m | £210.1m | £2.9m | — | £134.7m | £134.6m |
| summer 2005 | £229.4m | £227.2m | −£2.2m | £235.0m (B) | £112.3m | £110.8m |
| January 2006 | £51.1m | £58.1m | £7.0m | — | £41.6m | £41.6m |
| summer 2006 | £240.9m | £239.5m | −£1.5m | £300.0m (B) | £122.0m | £122.0m |
| January 2007 | £39.8m | £41.3m | £1.5m | — | £17.2m | £17.2m |
| summer 2007 | £320.5m | £349.6m | £29.1m | — | £162.1m | £161.7m |
| January 2008 | £92.2m | £119.1m | £26.9m | — | £51.6m | £60.2m |
| summer 2008 | £338.6m | £404.2m | £65.5m | £500.0m (B) | £162.6m | £175.2m |
| January 2009 | £92.9m | £110.4m | £17.5m | £160.0m (B) | £6.3m | £9.8m |
| summer 2009 | £239.1m | £404.4m | £165.3m | £460.4m (B) | £7.5m | £57.3m |
| January 2010 | £26.0m | £28.5m | £2.5m | £36.0m (A) | £9.9m | £9.9m |
| summer 2010 | £181.8m | £225.8m | £44.0m | £350.0m (B) | £108.4m | £130.9m |
| January 2011 | £195.4m | £199.1m | £3.7m | £209.3m (A) | £76.1m | £79.8m |
| summer 2011 | £205.3m | £390.4m | £185.0m | — | £96.5m | £146.2m |
| January 2012 | £42.7m | £48.2m | £5.5m | £67.4m (A) | £0.7m | £5.5m |
| summer 2012 | £325.9m | £374.5m | £48.7m | £490.0m (B) | £147.7m | £187.5m |
| January 2013 | £80.6m | £92.6m | £12.0m | £123.4m (A) | £44.6m | £49.6m |
| summer 2013 | £559.0m | £558.6m | −£0.3m | £630.0m (B) | £353.2m | £351.0m |
| January 2014 | £118.8m | £120.0m | £1.2m | £128.8m (A) | £36.0m | £36.2m |
| summer 2014 | £638.9m | £669.3m | £30.5m | £809.6m (A) | £292.6m | £301.7m |
| January 2015 | £90.6m | £96.8m | £6.2m | £118.2m (A) | £29.8m | £28.7m |
| summer 2015 | £735.5m | £744.0m | £8.5m | £858.6m (A) | £373.5m | £377.1m |
| January 2016 | £103.6m | £124.0m | £20.4m | £177.5m (A) | £43.6m | £51.0m |
| summer 2016 | £1.08bn | £1.09bn | £10.6m | £1.12bn (A) | £713.0m | £724.6m |
| January 2017 | £140.5m | £163.5m | £23.0m | £236.7m (A) | −£64.2m | −£53.2m |
| summer 2017 | £1.32bn | £1.40bn | £84.7m | £1.41bn (A) | £643.1m | £684.3m |
| January 2018 | £346.2m | £375.8m | £29.6m | £419.5m (A) | £98.2m | £109.8m |
| summer 2018 | £907.9m | £963.5m | £55.6m | £1.23bn (B) | £706.9m | £721.5m |
| January 2019 | £109.6m | £111.6m | £2.0m | £180.0m (B) | £54.5m | £56.5m |
| summer 2019 | £1.07bn | £1.16bn | £86.7m | £1.41bn (B) | £483.9m | £509.7m |
| January 2020 | £121.0m | £165.4m | £44.4m | £230.0m (B) | £119.7m | £160.5m |
| summer 2020 | £1.07bn | £1.09bn | £23.2m | £1.24bn (B) | £688.1m | £684.6m |
| January 2021 | £45.0m | £50.0m | £5.0m | £70.0m (B) | £24.8m | £14.0m |
| summer 2021 | £829.4m | £887.7m | £58.3m | £1.10bn (B) | £435.1m | £422.7m |
| January 2022 | £188.0m | £189.0m | £1.0m | £295.0m (B) | £78.7m | £79.7m |
| summer 2022 | £1.73bn | £1.76bn | £28.7m | £1.90bn (B) | £986.3m | £1.01bn |
| January 2023 | £654.8m | £663.3m | £8.5m | £780.1m (B) | £570.5m | £567.0m |
| summer 2023 | £2.15bn | £2.26bn | £108.1m | £2.44bn (B) | £990.9m | £1.03bn |
| January 2024 | £86.0m | £87.7m | £1.7m | £96.2m (B) | £75.2m | £76.9m |
| summer 2024 | £1.81bn | £1.88bn | £71.7m | £2.08bn (B) | £592.4m | £617.7m |
| January 2025 | £343.5m | £341.4m | −£2.1m | £370.0m (B) | £213.6m | £217.5m |
| summer 2025 | £2.83bn | £2.89bn | £62.0m | £3.00bn (B) | £1.19bn | £1.26bn |
| January 2026 | £341.6m | £336.6m | −£5.0m | £397.0m (B) | £111.3m | £110.3m |
| summer 2026 | £3.07bn | £3.12bn | £55.5m | £3.46bn (B) | £1.26bn | £1.22bn |

Total gross, all windows: £27.74bn before, £29.16bn after (£1.42bn).

**Effect on the race** (against the build at 4b0f91c): the leader changes at 5 month ends (2003-03: Newcastle United → Manchester United; 2003-04: Newcastle United → Manchester United; 2003-05: Newcastle United → Manchester United; 2003-06: Newcastle United → Manchester United; 2016-07: Chelsea → Manchester City); who is in the top 12 changes at 137 month ends (1995-02: in Ipswich Town, out Newcastle United; 2005-01: in Leeds United, out Birmingham City; 2005-02: in Leeds United, out Birmingham City; 2005-03: in Leeds United, out Birmingham City; 2005-08: in Everton, out Manchester City; 2005-09: in Everton, out Manchester City; 2005-10: in Everton, out Manchester City; 2005-11: in Everton, out Manchester City; 2005-12: in Everton, out Manchester City; 2006-05: in Birmingham City, out Manchester City; 2006-06: in Blackburn Rovers, out Manchester City; 2006-07: in Blackburn Rovers, out Manchester City …). Final point: Manchester United £1.68bn, Chelsea £1.67bn, Manchester City £1.64bn.

**Still UNVERIFIED among the researched deals: 55** (their fee is a preview, not for screen; mostly pages the runner could not load or that do not name both clubs). The largest:

| Player | Move | Date | Fee in use | Grade |
|---|---|---|---|---|
| Viktor Gyökeres | Sporting CP → Arsenal | 2025-07-26 | £55,100,000 | B |
| Nemanja Matić | Chelsea → Manchester United | 2017-07-31 | £35,000,000 | B |
| Martin Ødegaard | Real Madrid → Arsenal | 2021-08-20 | £30,000,000 | B |
| Dilane Bakwa | RC Strasbourg → Nottingham Forest | 2025-09-01 | £30,000,000 | C |
| Yeremy Pino | Villarreal → Crystal Palace | 2025-08-29 | £26,000,000 | C |
| Ferdi Kadıoğlu | Fenerbahçe → Brighton & Hove Albion | 2024-08-27 | £25,357,008 | B |
| Donyell Malen | Aston Villa → Roma | 2026-06-29 | £25,000,000 | B |
| Archie Gray | Leeds United → Tottenham Hotspur | 2024-07-02 | £25,000,000 | B |
| Son Heung-min | Bayer Leverkusen → Tottenham Hotspur | 2015-08-28 | £22,000,000 | B |
| Enzo Le Fée | Roma → Sunderland | 2025-07-01 | £20,000,000 | B |
| Allan Saint-Maximin | Nice → Newcastle United | 2019-08-02 | £16,500,000 | B |
| Robbie Keane | Liverpool → Tottenham Hotspur | 2009-02-02 | £15,000,000 | B |
| Didier N'Dong | Lorient → Sunderland | 2016-08-31 | £13,600,000 | B |
| Samuel Iling-Junior | Juventus → Aston Villa | 2024-07-01 | £11,878,500 | B |
| Sandro | Tottenham Hotspur → Queens Park Rangers | 2014-09-01 | £10,000,000 | B |
| Abel Hernández | Palermo → Hull City | 2014-09-01 | £9,500,000 | B |
| Andrej Kramarić | Rijeka → Leicester City | 2015-01-16 | £9,000,000 | B |
| Nigel Reo-Coker | West Ham United → Aston Villa | 2007-07-05 | £8,500,000 | A |
| Trézéguet | Kasımpaşa → Aston Villa | 2019-07-24 | £8,500,000 | B |
| Conor Coady | Wolverhampton Wanderers → Leicester City | 2023-07-01 | £8,500,000 | B |
| Jeremain Lens | Dynamo Kyiv → Sunderland | 2015-07-15 | £8,000,000 | B |
| Abdoulaye Doucouré | Stade Rennais → Watford | 2016-02-01 | £8,000,000 | B |
| Craig Bellamy | Liverpool → West Ham United | 2007-07-10 | £7,500,000 | A |
| Yasin Özcan | Kasımpaşa → Aston Villa | 2025-06-01 | £7,000,000 | C |
| Libor Kozák | Lazio → Aston Villa | 2013-09-02 | £7,000,000 | C |

**Order test on the 369 round 2 deals not researched** (`source/round2_order_test.csv`; the Tier 1 test of DEC-256: does removing the fee, or using another version of it, change the leader or who is in the top 12 at any month end?): **197 could** (0 the leader, the rest a top-12 place) and go to a later round; 172 could not. By season: 1994-95 9, 1995-96 14, 1996-97 17, 1997-98 9, 1998-99 9, 1999-00 7, 2000-01 4, 2001-02 4, 2002-03 15, 2003-04 7, 2004-05 18, 2005-06 17, 2006-07 14, 2007-08 12, 2008-09 12, 2009-10 6, 2010-11 4, 2011-12 3, 2012-13 4, 2013-14 3, 2014-15 2, 2015-16 5, 2016-17 2.

Deals that could change the leader:

| Deal | Player | Date | Fee in use | First month end affected |
|---|---|---|---|---|

**Decided under DEC-417 (Claude, DEC-420; details in `state/DECISIONS.md`)**

1. Aggregator, scores and blog sites count as grade C; agency copies and regional papers stay B as the helpers graded them.
2. A rejected figure no longer blocks the same number in another currency (Curtis Jones's guaranteed €30m and Mayenda's €22m had been blocked by rejections of £30m and £22m totals).
3. Earlier rejections re-weighed against the new leads: Bent, Gyan, Gordon and Brughmans still have only totals or bounds (£0 under DEC-276); Crouch 2009, Benítez, Ings, Mateus Fernandes and João Pedro to Chelsea keep their guaranteed figures; João Pedro to Brighton now counts the £30m 'understood' (a reported figure for an undisclosed fee).
4. Guaranteed fee where the completion report gives it: Xhaka £25m initial (was £35m), Sané, Álvarez, Mané, Leon Bailey, Emiliano Martínez (£17m reported, not the £20m with add-ons), Arnautović, Matić 2017, Strand Larsen, Skipp, Semenyo 2023, Mamardashvili, Ugarte, Šeško, Núñez to Al Hilal, Thiaw, Negredo.
5. Exchanges: Jeffrey counts the whole £60,000 deal with Roche valued at £25,000 (as for Cole, DEC-407); Pitcher counts £50,000 cash with Whyte and Mortimer at £0; Rutter (initial fee only as a range) and Brughmans (only 'up to') stay £0; Sereni stays £0 (Sky's pre-completion £4.5m against 'exceeded the £4.57m'); Daley's date is the completion report's (31 May 1994).
6. Mikel (2006): kept at £16m on the Manchester United → Chelsea move (£12m to United and £4m to Lyn, one payment for one registration); Chelsea's spend is exact and United's income is £4m too high until the build can book a payment to a third club.

**For Luke (DEC-417 leaves this to him: it changes who leads)**

1. **Nastasić (Fiorentina → Manchester City, Aug 2012).** The only figure found is "£12m — including Stefan Savic as a makeweight"; Savić is not valued and City called the fee undisclosed. Under the part-exchange rule the cash is unknown, so the build counts £0 for now, and that puts Chelsea ahead of Manchester City from September to December 2015 (by £3.5m). *Recommendation:* count the £12m package as Nastasić's fee with Savić at £0, the closest figure to what City paid (it overstates City's outlay by Savić's unknown value rather than understating it by the cash), and ask the next round for the cash part.

**Answered by Luke (9 Oct 2026, DEC-423): count the £12m package as Nastasić's fee, Savić £0, until a contemporary cash figure is confirmed.**

**Worth knowing:** from March to June 2003 Manchester United lead Newcastle United by about £10,000, so any small correction can swap them.

## 15. Source round 3: undisclosed fees and the leader deals (IQ-15i; DEC-422 to DEC-428)

- **Why:** 2,205 deals with a Premier League side were counted £0 as "undisclosed, no figure" (fe3dd9e), many of them well known; the press printed a figure for many, and the rule already uses a grade B reported figure for an undisclosed fee (DEC-237 (g)). Luke asked how close our window totals are to the published ones.
- **Inputs:** Claude helper research on 507 of those deals (part24a summer 2009, part24e/f/g: all P1 deals between two clubs both in the PL that season and all P2 purchases from clubs that have been in the PL), and the 13 leader deals plus Nastasić's cash part read by Cowork in Luke's Chrome (part24d) and by a helper (part24b). Every data file's SHA-256 matched `00_README.md`.
- **Checked at source:** all 481 cited pages read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/37904336661: 421 loaded; 16 refused, 14 not found, 11 server errors); 6 pages re-read after the runner learnt to match ð, ø and similar letters (https://github.com/marketmarathon/race-through-time/actions/runs/37906441423).
- **Quotes read:** 230 newly confirmed quotes (25 rejected: another deal's figure, a contract value, a valuation or release clause, a bid or offer, a maximum, a total with add-ons, a combined figure that did not complete, or one resting on a weaker outlet).
- **Undisclosed deals now carrying a reported figure:** 172 of the 507 researched (134 confirmed at source; the rest a grade B figure not yet confirmed, counted as a preview), adding £1.20bn of fees. By type: P1 both clubs in the PL: 88 of 260 (70 confirmed); P2 PL purchase from an ever-PL club: 75 of 191 (56 confirmed); P3/P5 PL sale: 2 of 27 (2 confirmed); P4 PL purchase from another club: 7 of 29 (6 confirmed). 335 researched deals stay £0 (the fee is undisclosed in every source found, a free transfer, a loan, a nominal fee, a swap with no stated value, or only a maximum). Of all 2,205, 1990 are still £0; P4 (purchases from other clubs) and the sales were not researched.

**The 13 leader deals and Nastasić** (order test of IQ-15h):

| Deal | Player | Fee before | Fee after | Status | Basis |
|---|---|---|---|---|---|
| R0063 | Ruel Fox | £4,200,000 | £4,200,000 | VERIFIED | stated |
| R0082 | Karel Poborský | £3,500,000 | £3,500,000 | VERIFIED | stated |
| R0117 | Peter Beardsley | £450,000 | £450,000 | UNVERIFIED | stated |
| R0121 | Brad Friedel | £1,000,000 | £1,300,000 | VERIFIED | stated |
| R0141 | Stephane Guivarc'h | £3,500,000 | £3,500,000 | VERIFIED | stated |
| R0150 | Terry Cooke | £600,000 | £600,000 | UNVERIFIED | stated |
| R0151 | Stephane Henchoz | £3,500,000 | £3,500,000 | VERIFIED | stated |
| R0152 | Sander Westerveld | £4,000,000 | £4,000,000 | VERIFIED | stated |
| R0171 | Eiður Guðjohnsen | £4,000,000 | £4,000,000 | VERIFIED | stated |
| R0179 | Temur Ketsbaia | £900,000 | £900,000 | VERIFIED | stated |
| R0183 | Alex Notman | £250,000 | £250,000 | UNVERIFIED | stated |
| R0202 | Bruno Cheyrou | £4,000,000 | £4,000,000 | VERIFIED | reported |
| R0228 | Ricardo | £1,500,000 | £1,500,000 | VERIFIED | stated |
| R0490 | Matija Nastasić | £0 | £12,000,000 | VERIFIED | stated: package including an unvalued player (Luke, DEC-423) |

**How close we are to the published window totals** (gross spending by PL clubs; before = fe3dd9e; published = the first grade A/B total in part17b, research leads, UNVERIFIED). "Share" is our total as a share of the published one:

| Window | Gross before | Gross after | Published | Share before | Share after | Undisclosed still £0 (PL buys) |
|---|---|---|---|---|---|---|
| January 2003 | £36.8m | £36.6m | £35.0m (B) | 105% | 105% | 2 |
| summer 2003 | £195.1m | £195.1m | £215.0m (B) | 91% | 91% | 14 |
| summer 2005 | £229.2m | £227.2m | £235.0m (B) | 98% | 97% | 4 |
| summer 2006 | £239.5m | £239.5m | £300.0m (B) | 80% | 80% | 19 |
| summer 2008 | £339.0m | £404.2m | £500.0m (B) | 68% | 81% | 42 |
| January 2009 | £92.9m | £110.4m | £160.0m (B) | 58% | 69% | 19 |
| summer 2009 | £238.3m | £404.4m | £460.4m (B) | 52% | 88% | 38 |
| January 2010 | £26.0m | £28.5m | £36.0m (A) | 72% | 79% | 8 |
| summer 2010 | £181.8m | £225.8m | £350.0m (B) | 52% | 65% | 44 |
| January 2011 | £195.1m | £199.1m | £209.3m (A) | 93% | 95% | 10 |
| January 2012 | £42.7m | £48.2m | £67.4m (A) | 63% | 71% | 17 |
| summer 2012 | £315.0m | £374.5m | £490.0m (B) | 64% | 76% | 36 |
| January 2013 | £80.6m | £92.6m | £123.4m (A) | 65% | 75% | 18 |
| summer 2013 | £556.9m | £558.6m | £630.0m (B) | 88% | 89% | 33 |
| January 2014 | £120.0m | £120.0m | £128.8m (A) | 93% | 93% | 16 |
| summer 2014 | £645.3m | £669.3m | £809.6m (A) | 80% | 83% | 50 |
| January 2015 | £90.6m | £96.8m | £118.2m (A) | 77% | 82% | 12 |
| summer 2015 | £724.6m | £744.0m | £858.6m (A) | 84% | 87% | 24 |
| January 2016 | £104.6m | £124.0m | £177.5m (A) | 59% | 70% | 19 |
| summer 2016 | £1.07bn | £1.09bn | £1.12bn (A) | 95% | 98% | 25 |
| January 2017 | £141.0m | £163.5m | £236.7m (A) | 60% | 69% | 10 |
| summer 2017 | £1.30bn | £1.40bn | £1.41bn (A) | 92% | 99% | 25 |
| January 2018 | £343.8m | £375.8m | £419.5m (A) | 82% | 90% | 9 |
| summer 2018 | £906.5m | £963.5m | £1.23bn (B) | 74% | 78% | 37 |
| January 2019 | £109.6m | £111.6m | £180.0m (B) | 61% | 62% | 4 |
| summer 2019 | £1.08bn | £1.16bn | £1.41bn (B) | 76% | 82% | 23 |
| January 2020 | £112.2m | £165.4m | £230.0m (B) | 49% | 72% | 1 |
| summer 2020 | £1.07bn | £1.09bn | £1.24bn (B) | 86% | 88% | 22 |
| January 2021 | £50.0m | £50.0m | £70.0m (B) | 71% | 71% | 3 |
| summer 2021 | £824.7m | £887.7m | £1.10bn (B) | 75% | 81% | 24 |
| January 2022 | £187.0m | £189.0m | £295.0m (B) | 63% | 64% | 15 |
| summer 2022 | £1.72bn | £1.76bn | £1.90bn (B) | 91% | 93% | 23 |
| January 2023 | £662.5m | £663.3m | £780.1m (B) | 85% | 85% | 11 |
| summer 2023 | £2.18bn | £2.26bn | £2.44bn (B) | 89% | 93% | 28 |
| January 2024 | £87.7m | £87.7m | £96.2m (B) | 91% | 91% | 9 |
| summer 2024 | £1.79bn | £1.88bn | £2.08bn (B) | 86% | 91% | 23 |
| January 2025 | £341.4m | £341.4m | £370.0m (B) | 92% | 92% | 12 |
| summer 2025 | £2.88bn | £2.89bn | £3.00bn (B) | 96% | 96% | 22 |
| January 2026 | £336.6m | £336.6m | £397.0m (B) | 85% | 85% | 9 |
| summer 2026 | £3.09bn | £3.12bn | £3.46bn (B) | 89% | 90% | 35 |

Across the 40 windows with a published total, our sum averages 78% of the published figure before this round and 84% after. **What is left:** (1) undisclosed deals still counted £0, above all PL purchases from clubs outside the PL (P4, 685 deals, not yet researched) and loans with an obligation booked only when the fee is reported; (2) add-ons, which published totals usually include and we count only when reported as paid; (3) figures we count only when confirmed or reported in the quality press, while some published totals use agency or club-reported estimates; (4) differences in what a window covers (published totals often include deals agreed in the window but completed later, and some count fees in euros at other rates).

**Effect on the race** (against fe3dd9e): the leader changes at 5 month ends (2015-09: Chelsea → Manchester City; 2015-10: Chelsea → Manchester City; 2015-11: Chelsea → Manchester City; 2015-12: Chelsea → Manchester City; 2016-07: Chelsea → Manchester City); who is in the top 12 changes at 129 month ends.

**Standings at the freeze (2026-09-01), cumulative net spend:**

| Rank after | Club | Net before (rank) | Net after | Change |
|---|---|---|---|---|
| 1 | Manchester United | £1.67bn (1) | £1.68bn | £7.5m |
| 2 | Chelsea | £1.65bn (2) | £1.67bn | £19.8m |
| 3 | Manchester City | £1.56bn (3) | £1.64bn | £78.8m |
| 4 | Arsenal | £1.16bn (4) | £1.12bn | −£40.1m |
| 5 | Liverpool | £962.4m (5) | £989.1m | £26.8m |
| 6 | Tottenham Hotspur | £947.9m (6) | £981.3m | £33.4m |
| 7 | Newcastle United | £700.3m (7) | £703.0m | £2.7m |
| 8 | West Ham United | £583.9m (8) | £590.5m | £6.6m |
| 9 | Everton | £404.6m (9) | £373.4m | −£31.3m |
| 10 | Fulham | £344.4m (10) | £367.3m | £22.9m |
| 11 | Sunderland | £288.6m (11) | £338.4m | £49.8m |
| 12 | Aston Villa | £250.9m (13) | £314.7m | £63.8m |
| 13 | Nottingham Forest | £267.0m (12) | £299.2m | £32.3m |
| 14 | Ipswich Town | £215.4m (16) | £280.4m | £65.0m |
| 15 | AFC Bournemouth | £233.4m (15) | £249.1m | £15.7m |
| 16 | Leeds United | £238.5m (14) | £239.5m | £1.0m |
| 17 | Crystal Palace | £141.3m (22) | £198.0m | £56.8m |
| 18 | Burnley | £144.1m (21) | £175.4m | £31.4m |
| 19 | West Bromwich Albion | £160.7m (19) | £171.2m | £10.5m |
| 20 | Brentford | £163.5m (18) | £163.5m | £0.0m |

**Order test re-run on the 369 round 2 deals still not researched** (`source/round2_order_test.csv`): 197 could change who is in the top 12 at some month end, 0 of them the leader:

| Deal | Player | Date | Fee in use | First month end affected |
|---|---|---|---|---|

**Still UNVERIFIED among the round 3 figures: 38** (a grade B figure the runner could not confirm: page refused or missing, or the club names not both on the page). The largest:

| Player | Move | Date | Fee in use |
|---|---|---|---|
| Alex Oxlade-Chamberlain | Southampton → Arsenal | 2011-08-08 | £15,000,000 |
| Craig Bellamy | West Ham United → Manchester City | 2009-01-19 | £14,000,000 |
| Cameron Archer | Sheffield United → Aston Villa | 2024-06-14 | £14,000,000 |
| John O'Shea | Manchester United → Sunderland | 2011-07-07 | £12,000,000 |
| Wes Brown | Manchester United → Sunderland | 2011-07-07 | £12,000,000 |
| Andros Townsend | Tottenham Hotspur → Newcastle United | 2016-01-27 | £12,000,000 |
| Fernando Llorente | Swansea City → Tottenham Hotspur | 2017-08-31 | £12,000,000 |
| Dara O'Shea | Burnley → Ipswich Town | 2024-08-25 | £12,000,000 |
| Matt Targett | Southampton → Aston Villa | 2019-07-01 | £11,500,000 |
| Matěj Vydra | Derby County → Burnley | 2018-08-07 | £11,000,000 |
| Nick Pope | Burnley → Newcastle United | 2022-06-23 | £10,000,000 |
| Charles N'Zogbia | Wigan Athletic → Aston Villa | 2011-07-29 | £9,500,000 |
| Shaun Wright-Phillips | Chelsea → Manchester City | 2008-08-28 | £9,000,000 |
| Chris Smalling | Fulham → Manchester United | 2010-07-01 | £8,000,000 |
| Charlie Adam | Blackpool → Liverpool | 2011-07-07 | £7,500,000 |
| Sorba Thomas | Leicester City → Hull City | 2026-09-01 | £7,000,000 |
| Rudy Gestede | Blackburn Rovers → Aston Villa | 2015-07-31 | £6,000,000 |
| Craig Dawson | West Bromwich Albion → Watford | 2019-07-01 | £6,000,000 |
| Yossi Benayoun | West Ham United → Liverpool | 2007-07-12 | £5,000,000 |
| Nicky Shorey | Reading → Aston Villa | 2008-08-07 | £4,000,000 |

**For Cowork to read in Luke's Chrome:** 12 rows the helpers saw only as a search snippet and the runner could not confirm (`source/round3_unreadable.csv`).
**Decided under DEC-417 (Claude, DEC-427; details in `state/DECISIONS.md`)**
1. Combined fees are booked once, with the partner at £0 (DEC-405): Naughton £8m (Walker £0); Zamora €8m (Paintsil £0); Toffolo £10m (O'Brien £0); Eagles about £3m (Mears £0); Oviedo £7.5m initial (Gibson £0); Sean Davis about £7m (Mendes and Pamarot £0). Mouyokolo and Hunt keep their separate figures.
2. Not counted: Sunderland's "joint fee of around £23 million" for Malbranque, Tainio and Chimbonda (it included Kaboul, who went to Portsmouth instead); Bogle and Lowe (a £15m figure "agreed in principle" against a report that Sheffield United "paid considerably less" than £12m: never chosen between, so £0); Jordan Henderson's £20m (also reported as "up to £20m": £0 under DEC-276); bids that were not the fee (Bowler, Foster 2018, Osborn); Ireland's "£26m", which is the whole Milner deal (Milner keeps the confirmed £26m with Ireland £0, as Luke ruled for Nastasić).
3. DEC-404 now also reads "his £1.3m move" as a completed deal (Friedel 1997: £1.3m, not the earlier £1m), and "has yet to appear" no longer counts as "not completed". Glen Johnson stays at the £18.5m accepted bid: no report says the deal was completed at £17m.
4. Terry Cooke stays at £600,000: the Independent's page says "£600,000 up front with a possible further £400,000"; the £1m is the total (guaranteed fee only).
5. Swaps with no stated value (Crouch and Vokes, Becchio and Morison) stay £0 on both sides.
6. Sorba Thomas: our list names Leicester as the seller and the press names Stoke City; neither was a PL club in 2026–27, so no total changes. Noted for the next data check.
7. The runner now matches ð, ø, æ and similar letters (Guðjohnsen's £4m confirmed on the Guardian's list).
**For Luke (DEC-417 leaves this to him: what the video claims on screen)**
1. **The finish is a photo finish.** At the freeze Manchester United (£1,659.0m), Chelsea (£1,652.5m) and Manchester City (£1,650.6m) are within £8.3m of each other, and United take the lead only at the very last point. About 2,000 undisclosed deals are still counted £0 (above all purchases from clubs outside the PL, not yet researched), so the final order can still change. *Recommendation:* run the P4 sweep (PL purchases from other clubs) before the final order is treated as settled, and keep the on-screen label "Undisclosed fees not included".

## 16. January 2020 and the window deal-count check (IQ-15j; DEC-429 to DEC-434)

- **Why January 2020 was missing (DEC-430):** the build reads each window's Wikipedia list page. The winter 2019-20 page we use (rev 1371935139) has 70 transfer rows, only 5 of them in January 2020; its edit history (runner, https://github.com/marketmarathon/race-through-time/actions/runs/37950422012) shows it never exceeded 67,150 bytes, so Wikipedia never listed most of that window's deals. A second fault turned up on the way: list tables with four columns (loans without a fee column) lost the date of every row, so 573 rows of summers 2017 and 2018 were dropped.
- **Fix at the root:** (1) the four-column tables now keep their dates; (2) the 2019-20 club-season page of every PL club (and the 2003-04 and 2004-05 pages) was read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/37950909967) and its In/Out and loan tables parsed (headings, bold labels, loan tables under season sub-headings, dates spanning rows); a club-page row is used only when no list page already has that player at that club within 60 days, and only for a window listed in `CLUB_PAGE_WINDOWS` (January 2020, as the brief approved; DEC-431); every other club-page row is listed in `source/club_page_rows_unused.csv`. Two new build checks: **no window has under half the PL deals of the same-type windows either side** (documented exceptions only), and **every list-page row has a date**. The 1992-2002 club-season rows are byte-for-byte unchanged.
- **January 2020 deals added:** 238 deals with a PL club (by type: free 11, loan 171, permanent 8, undisclosed 48). The window now has 253 such deals (it had 14; the same-type windows either side have a median of 111.5). With a fee:

| Date | Player | Move | Fee in use | Status | Basis |
|---|---|---|---|---|---|
| 2020-01-01 | Takumi Minamino | Red Bull Salzburg → Liverpool | £7,250,000 | VERIFIED | already in the build; stated |
| 2020-01-01 | Bryan Fiabema | Tromsø → Chelsea | £540,000 | UNVERIFIED | added in IQ-15j; stated |
| 2020-01-09 | Liam Smith | Kilmarnock → Manchester City | £250,000 | UNVERIFIED | added in IQ-15j; stated |
| 2020-01-09 | Allan | Liverpool → Atlético Mineiro | £3,200,000 | UNVERIFIED | added in IQ-15j; stated |
| 2020-01-14 | Ignacio Pussetto | Udinese → Watford | £6,838,776 | VERIFIED | added in IQ-15j; stated |
| 2020-01-17 | Ashley Young | Manchester United → Inter Milan | £1,280,000 | VERIFIED | already in the build; reported |
| 2020-01-23 | Victor Moses | Chelsea → Inter Milan | £190,000 | UNVERIFIED | added in IQ-15j; stated |
| 2020-01-23 | Louie Barry | Barcelona → Aston Villa | £880,000 | VERIFIED | added in IQ-15j; stated |
| 2020-01-30 | Sander Berge | Genk → Sheffield United | £22,000,000 | VERIFIED | added in IQ-15j; reported |
| 2020-01-30 | Steven Bergwijn | PSV Eindhoven → Tottenham Hotspur | £25,000,000 | VERIFIED | already in the build; reported |
| 2020-01-30 | Bruno Fernandes | Sporting Lisbon → Manchester United | £47,000,000 | VERIFIED | already in the build; reported |
| 2020-01-31 | Jarrod Bowen | Hull City → West Ham United | £22,000,000 | UNVERIFIED | added in IQ-15j; stated |
| 2020-01-31 | Clinton Mola | Chelsea → Stuttgart | £168,110 | UNVERIFIED | added in IQ-15j; reported |
| 2020-02-24 | Hakim Ziyech | Ajax → Chelsea | £33,599,328 | VERIFIED | already in the build; reported |

**Cowork's spot list:** all present now.

| Player | Move | Date | Type | Fee in use | Status |
|---|---|---|---|---|---|
| Sander Berge | Genk → Sheffield United | 2020-01-30 | permanent | £22,000,000 | VERIFIED: reported |
| Jarrod Bowen | Hull City → West Ham United | 2020-01-31 | permanent | £22,000,000 | UNVERIFIED: stated |
| Daniel Podence | Olympiacos → Wolverhampton Wanderers | 2020-01-30 | undisclosed | £0 | UNVERIFIED: undisclosed, no figure: counted £0 |
| Ignacio Pussetto | Udinese → Watford | 2020-01-14 | permanent | £6,838,776 | VERIFIED: stated |
| Josh Brownhill | Bristol City → Burnley | 2020-01-30 | undisclosed | £0 | UNVERIFIED: undisclosed, no figure: counted £0 |
| Darren Randolph | Middlesbrough → West Ham United | 2020-01-15 | undisclosed | £0 | UNVERIFIED: undisclosed, no figure: counted £0 |
| Tariq Lamptey | Chelsea → Brighton & Hove Albion | 2020-01-31 | undisclosed | £0 | UNVERIFIED: undisclosed, no figure: counted £0 |
| Christian Eriksen | Tottenham Hotspur → Inter Milan | 2020-01-28 | undisclosed | £0 | UNVERIFIED: undisclosed, no figure: counted £0 |
| Odion Ighalo | Shanghai Shenhua → Manchester United | 2020-02-01 | loan | £0 | UNVERIFIED: loan, no fee stated |
| Cédric Soares | Southampton → Arsenal | 2020-01-31 | loan | £0 | UNVERIFIED: loan, no fee stated |
| Pablo Marí | Flamengo → Arsenal | 2020-01-29 | loan | £0 | UNVERIFIED: loan, no fee stated |
| Tomáš Souček | Slavia Prague → West Ham United | 2020-01-29 | loan | £0 | UNVERIFIED: loan, no fee stated |
| Valentino Lazaro | Inter Milan → Newcastle United | 2020-01-24 | loan | £0 | UNVERIFIED: loan, no fee stated |

- **Fees read at source (runner, https://github.com/marketmarathon/race-through-time/actions/runs/37952043572 and /37952723663):** 95 pages cited for the new deals. Confirmed: Pussetto €8m (Watford Observer, completed signing). Rejected: Louie Barry's BBC figure ("about 1m euros (£880,000)", an approximation; Barcelona's exact €1,048,000 is quoted only on a grade D page), Bowen's "worth up to £22million" (a maximum), and four undisclosed-fee candidates (grade D pages, another player's fee, an earlier move). Lamptey: Chelsea's club-season page gives £2,970,000 but Chelsea's own announcement gives no figure and Brighton's says undisclosed, so he stays undisclosed at £0 (DEC-433).
- **Not sourced:** 56 January 2020 deals (permanent 3, undisclosed 53) keep the build's normal status and are listed for Cowork in `source/jan2020_unsourced.csv` (no figures in the list).
- **Minamino (brief 2(d)):** BBC Sport (grade B, confirmed on the runner) says "Deal to be completed on 1 January", and Liverpool's 2019-20 page gives entry date 1 January 2020. The build now dates the deal **1 January 2020** (was 19 December 2019, the day it was agreed; DEC-432). Same window and season, so no total changes.
- **January 2020 total (gross spending by PL clubs):** £112.2m before, **£165.4m after**; published £230.0m (BBC Sport, grade B, research lead): 49% → 72%. The rest of the gap is mainly the undisclosed deals still counted £0 (among the purchases Lo Celso, Podence, Samatta, Brownhill, Mooy and Randolph) and Bowen's guaranteed fee. Also to check in a later round: Ziyech's £33m is in this window (dated 24 February 2020, when the deal was agreed), which a published January total may not include.

**Windows the deal-count check flags** (deals with a PL club; neighbours = the two same-type windows either side):

| Window | Deals | Neighbours' median | Why | Club-page rows listed, not used |
|---|---|---|---|---|

All four would clear the check with their listed club-page rows; they are documented exceptions in the build (`KNOWN_SPARSE`, DEC-431) until a brief approves adding them. Summer 2017 (175 deals before the date fix, 371 now) clears. Summer 2019 is not flagged, but its club-season pages list 0 moves the list page lacks (mostly releases, loans and youth moves); the page histories show three list pages much shorter now than at their largest (summer 2007, 2013 and 2019), so those windows are candidates for the same club-page reading.

**Effect on the race** (against 398abbf, the end of IQ-15i; as built at the end of IQ-15j, 193580c; section 17 has the current figures): the leader changes at 0 month ends; who is in the top 12 changes at 4 month ends (2019-04: Wolverhampton Wanderers in for West Bromwich Albion; 2019-05: Wolverhampton Wanderers in for West Bromwich Albion; 2023-06: Wolverhampton Wanderers in for AFC Bournemouth; 2023-08: Wolverhampton Wanderers in for Fulham); the order within the top 12 changes at 36 month ends. Wolves' entries (2019 and 2023) come from Jonny's £18m permanent move (a research lead that had no deal to attach to until his loan row came back with the date fix; dated 31 January 2019, DEC-432).

**Standings at the freeze (2026-09-01), cumulative net spend, at the end of IQ-15j:**

| Rank after | Club | Net before (rank) | Net after | Change |
|---|---|---|---|---|
| 1 | Manchester United | £1,659.0m (1) | £1,659.0m | £0.0m |
| 2 | Manchester City | £1,650.6m (3) | £1,650.9m | £0.2m |
| 3 | Chelsea | £1,652.4m (2) | £1,647.1m | −£5.3m |
| 4 | Arsenal | £1,126.9m (4) | £1,126.9m | £0.0m |
| 5 | Liverpool | £992.1m (5) | £988.9m | −£3.2m |
| 6 | Tottenham Hotspur | £985.0m (6) | £985.0m | £0.0m |
| 7 | Newcastle United | £702.6m (7) | £702.6m | £0.0m |
| 8 | West Ham United | £568.5m (8) | £590.5m | £22.0m |
| 9 | Everton | £376.1m (9) | £376.1m | £0.0m |
| 10 | Fulham | £367.3m (10) | £367.3m | £0.0m |
| 11 | Sunderland | £338.4m (11) | £338.4m | £0.0m |
| 12 | Aston Villa | £312.2m (12) | £313.1m | £0.9m |

The three leaders are now within £11.8m of each other (£8.3m before): Manchester United lead Manchester City by £8.1m and Chelsea by £11.8m. Chelsea fall from second to third because of three January 2020 sales known only from Chelsea's 2019-20 Wikipedia page: Michael Hector to Fulham (£5,310,000), Clinton Mola to Stuttgart (£360,000) and Victor Moses's loan to Inter (£190,000), less Bryan Fiabema's £540,000 purchase; none is confirmed at source yet (all in `source/jan2020_unsourced.csv` or loans). Under DEC-429 the final order is not settled until the IQ-15k round on the leaders' undisclosed deals. (IQ-15k: Hector's £5.31m was a duplicate of his September 2019 move and is gone, DEC-436.)

**Order test re-run** (`source/round2_order_test.csv`): 197 of 369 unresearched round 2 deals could change who is in the top 12 at some month end, 0 of them the leader.

## 17. Source round 4: the three leaders' undisclosed deals (IQ-15k; DEC-435 to DEC-439)

- **Why:** Luke's DEC-429: the order at the freeze is not settled while the three leaders' undisclosed deals are counted £0.
- **Inputs:** the work list of 258 deals (Manchester United 16 purchases and 61 sales, Chelsea 24 and 63, Manchester City 27 and 67; `source/source_round4_map.csv`), Claude helper research on all of them (part25a, part25c), the six January 2020 leader deals (part25d) and Cowork's Chrome reads of the 12 round 3 pages the runner could not read (part25b). Every file's SHA-256 matched `00_README.md`.
- **Checked at source:** the 213 pages cited read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/37962899786: 186 loaded; 15 refused, 6 not found, the rest server errors or redirects).
- **Quotes read:** 37 newly confirmed quotes (6 rejected: a pre-completion figure where a completion report exists, a lower bound, an asking price, a total with add-ons, a maximum, and the Mikel settlement booked elsewhere).
- **Result (as now built, after round 5 too; at the end of IQ-15k: 43 with a figure, 30 confirmed): 42 of the 258 deals carry a figure (42 confirmed at source); none did before; 216 stay £0** (undisclosed in every source found, free, a loan, training compensation, a nominal fee, or only a maximum, lower bound or grade C figure). By leader and side (a deal between two leaders counts on both sides):

| Club | Side | Deals | With a figure | Confirmed at source | Fees added |
|---|---|---|---|---|---|
| Manchester United | purchases | 16 | 7 | 7 | £48.2m |
| Manchester United | sales | 61 | 7 | 7 | £34.7m |
| Chelsea | purchases | 24 | 8 | 8 | £92.0m |
| Chelsea | sales | 63 | 7 | 7 | £80.0m |
| Manchester City | purchases | 27 | 5 | 5 | £34.7m |
| Manchester City | sales | 67 | 8 | 8 | £39.7m |

**The figures now in use** (largest first):

| Deal | Player | Move | Date | Fee in use | Status | Basis |
|---|---|---|---|---|---|---|
| U1427 | Thibaut Courtois | Chelsea → Real Madrid | 2018-08-09 | £31,500,000 | VERIFIED (B) | reported |
| U1318 | Davide Zappacosta | Torino → Chelsea | 2017-08-31 | £23,000,000 | VERIFIED (B) | reported |
| U0662 | Romelu Lukaku | Anderlecht → Chelsea | 2011-08-18 | £20,000,000 | VERIFIED (B) | reported |
| U0612 | David de Gea | Atlético Madrid → Manchester United | 2011-06-29 | £18,000,000 | VERIFIED (B) | reported |
| U0535 | Ramires | Benfica → Chelsea | 2010-08-13 | £17,000,000 | VERIFIED (B) | reported |
| U1812 | Édouard Mendy | Chelsea → Al Ahli | 2023-06-28 | £16,000,000 | VERIFIED (B) | reported |
| U1595 | Angeliño | Manchester City → RB Leipzig | 2021-02-13 | £15,697,218 | VERIFIED (B) | reported |
| U1758 | Manuel Akanji | Borussia Dortmund → Manchester City | 2022-09-01 | £15,000,000 | VERIFIED (B) | stated |
| U0655 | Yuri Zhirkov | Chelsea → Anzhi Makhachkala | 2011-08-06 | £13,132,551 | VERIFIED (B) | reported |
| U0633 | Jérôme Boateng | Manchester City → Bayern Munich | 2011-07-18 | £12,258,121 | VERIFIED (B) | reported |
| U0738 | Shinji Kagawa | Borussia Dortmund → Manchester United | 2012-06-22 | £12,000,000 | VERIFIED (B) | reported |
| U1279 | Douglas Luiz | Vasco da Gama → Manchester City | 2017-07-15 | £10,700,000 | VERIFIED (B) | stated |
| U1940 | Willy Kambwala | Manchester United → Villarreal | 2024-07-15 | £9,900,000 | VERIFIED (B) | stated |
| U0255 | Branislav Ivanović | Lokomotiv Moscow → Chelsea | 2008-01-16 | £8,967,940 | VERIFIED (B) | reported |
| U1452 | Ola Aina | Chelsea → Torino | 2019-06-11 | £8,900,000 | VERIFIED (B) | stated |
| U1661 | Davide Zappacosta | Chelsea → Atalanta | 2021-08-24 | £8,563,843 | VERIFIED (B) | stated |
| U0644 | Thibaut Courtois | Racing Genk → Chelsea | 2011-07-26 | £7,954,746 | VERIFIED (B) | reported |
| U0289 | Deco | Barcelona → Chelsea | 2008-06-30 | £7,916,403 | VERIFIED (B) | reported |
| U0209 | Giuseppe Rossi | Manchester United → Villarreal | 2007-07-31 | £6,700,000 | VERIFIED (B) | reported |
| U0998 | Shinji Kagawa | Manchester United → Borussia Dortmund | 2014-08-31 | £6,300,000 | VERIFIED (B) | stated |
| U1835 | Alex Telles | Manchester United → Al Nassr | 2023-07-23 | £6,000,000 | VERIFIED (B) | reported |
| U1298 | Fernando | Manchester City → Galatasaray | 2017-08-04 | £4,700,000 | VERIFIED (B) | reported |
| U1861 | Matěj Kovář | Manchester United → Bayer Leverkusen | 2023-08-15 | £4,292,582 | VERIFIED (B) | stated |
| U0806 | Maicon | Internazionale → Manchester City | 2012-08-31 | £4,000,000 | VERIFIED (B) | stated |
| U0735 | Nick Powell | Crewe Alexandra → Manchester United | 2012-06-12 | £4,000,000 | VERIFIED (B) | stated |
| U0784 | Alexander Büttner | Vitesse Arnhem → Manchester United | 2012-08-21 | £3,900,000 | VERIFIED (B) | stated |
| U0226 | Juliano Belletti | FC Barcelona → Chelsea | 2007-08-23 | £3,722,504 | VERIFIED (B) | reported |
| U0813 | Ángelo Henríquez | Universidad de Chile → Manchester United | 2012-09-05 | £3,500,000 | VERIFIED (B) | stated |
| U0570 | Anders Lindegaard | Aalesund → Manchester United | 2010-11-27 | £3,500,000 | VERIFIED (B) | reported |
| U1132 | Matt Miazga | New York Red Bulls → Chelsea | 2016-01-30 | £3,477,293 | VERIFIED (B) | reported |
| U2034 | Diego León | Cerro Porteño → Manchester United | 2025-07-05 | £3,300,000 | VERIFIED (B) | stated |
| U0976 | Bruno Zuculini | Racing Club → Manchester City | 2014-08-08 | £3,000,000 | VERIFIED (B) | reported |
| U0874 | Maicon | Manchester City → Roma | 2013-07-18 | £3,000,000 | VERIFIED (B) | reported |
| U2188 | Issa Kaboré | Manchester City → Wrexham | 2026-08-27 | £2,000,000 | VERIFIED (B) | stated |
| U1063 | Enes Ünal | Bursaspor → Manchester City | 2015-07-06 | £2,000,000 | VERIFIED (B) | reported |
| U0303 | Georgios Samaras | Manchester City → Celtic | 2008-07-15 | £1,500,000 | VERIFIED (B) | stated |
| U0990 | George Saville | Chelsea → Wolverhampton Wanderers | 2014-08-26 | £1,000,000 | VERIFIED (B) | reported |
| U1635 | Olivier Giroud | Chelsea → AC Milan | 2021-07-17 | £856,384 | VERIFIED (B) | reported |
| U1808 | Zidane Iqbal | Manchester United → Utrecht | 2023-06-26 | £850,000 | VERIFIED (B) | stated |
| U0728 | Ravel Morrison | Manchester United → West Ham United | 2012-01-31 | £650,000 | VERIFIED (B) | stated |
| U1509 | Jeremie Frimpong | Manchester City → Celtic | 2019-09-01 | £350,000 | VERIFIED (B) | reported |
| U1070 | Jordy Hiwula | Manchester City → Huddersfield Town | 2015-07-17 | £150,000 | VERIFIED (B) | stated |

**The six January 2020 leader deals (part25d):** Bryan Fiabema £540,000 (stated); Henri Ogunby £0 (undisclosed, no figure: counte); Clinton Mola £168,110 (reported); Nathan Bishop £0 (undisclosed, no figure: counte); Tariq Lamptey £0 (undisclosed, no figure: counte). Hector's duplicate (Tf8a5f7e6ee) is gone; his one move is T6403be737e. No grade A/B figure was found for any of them; Fiabema, Mola and Moses keep their Wikipedia figures as unconfirmed.

**Who leads, through time** (month the lead changes hands; from 2003):

- Before (193580c): Chelsea (2003-07) → Manchester City (2011-07) → Chelsea (2011-08) → Manchester City (2015-07) → Chelsea (2023-01) → Manchester United (2026-09)
- After (end of IQ-15k, 1b01d81; section 18 has the current figures): Chelsea (2003-07) → Manchester City (2015-08) → Chelsea (2022-08) → Manchester United (2026-09)

The leader differs at 7 month ends; who is in the top 12 differs at 4 month ends (2019-04: West Bromwich Albion in for Wolverhampton Wanderers; 2019-05: West Bromwich Albion in for Wolverhampton Wanderers; 2023-06: AFC Bournemouth in for Wolverhampton Wanderers; 2023-08: Fulham in for Wolverhampton Wanderers). The top-12 changes are Wolves leaving it again in 2019 and 2023: Jonny's £18m no longer has a deal (DEC-436).

**Standings at the freeze (2026-09-01), cumulative net spend, at the end of IQ-15k:**

| Rank after | Club | Net before (rank) | Net after | Change |
|---|---|---|---|---|
| 1 | Manchester United | £1,659.0m (1) | £1,679.3m | £20.3m |
| 2 | Chelsea | £1,647.1m (3) | £1,664.8m | £17.7m |
| 3 | Manchester City | £1,650.9m (2) | £1,645.3m | −£5.6m |
| 4 | Arsenal | £1,126.9m (4) | £1,126.9m | £0.0m |
| 5 | Liverpool | £988.9m (5) | £988.9m | £0.0m |
| 6 | Tottenham Hotspur | £985.0m (6) | £985.0m | £0.0m |
| 7 | Newcastle United | £702.6m (7) | £702.6m | £0.0m |
| 8 | West Ham United | £590.5m (8) | £590.5m | £0.0m |
| 9 | Everton | £376.1m (9) | £376.1m | £0.0m |
| 10 | Fulham | £367.3m (10) | £367.3m | £0.0m |
| 11 | Sunderland | £338.4m (11) | £338.4m | £0.0m |
| 12 | Aston Villa | £313.1m (12) | £313.1m | £0.0m |

**Gaps between the three leaders:** after, Manchester United lead Chelsea by £14.4m and Manchester City by £34.0m; before, Manchester United led Manchester City by £8.1m and Chelsea by £11.8m. Manchester United take the lead only in the final month (the summer 2026 window).

**Order test re-run** (at the end of IQ-15k): 206 of 392 unresearched round 2 deals could change who is in the top 12 at some month end, 14 of them the leader (201 and 5 before this round): with the finish this close, the P4 sweep (DEC-429) can still matter.

**Still UNVERIFIED among the round 4 figures: 0** (a grade B figure the runner could not confirm: page refused, gone or changed, or the clubs not both named):

| Player | Move | Date | Fee in use |
|---|---|---|---|

**Decided under DEC-417 (Claude, DEC-436 and DEC-437):**
- **Grading (DEC-420 (a)):** Goal, 90min, FourFourTwo, theScore, Football España and TeamTalk rows are grade C whatever the research file says, as are SI pages carrying 90min copy; SI's own reporting and pages that are syndicated agency copy (Courtois 2011, Reuters) keep their grade. Sporting Life stays B, as for the 15 fees already in the build that rest on it (Aké, Ziyech, Guéhi, Henderson, Bony and others): see question 1.
- **DEC-404 as written:** a report that the deal was completed beats a bid, an agreed or an expected figure of the same grade; where no report of that grade says the deal was completed, the earliest report stands. So Zhirkov's sale (£13m, City AM, "poised to rake in"), Miazga's purchase ($5m, "expected", the only grade B figure) and Boateng's sale to Bayern (€14m agreed, UEFA.com) count, and Courtois 2011 counts Reuters' "nine million euro" (signed) instead of the £8m from the day of his medical. Louie Barry's BBC "about 1m euros (£880,000)" is now accepted too (reversing IQ-15j): a reported "about"/"around" figure counts as a reported figure; DEC-276 covers maxima, totals with add-ons and lower bounds.
- **Not the fee:** Lukaku "at least €20m" (a lower bound; the completion report's £20m counts), Muric £3m (an asking price), Akanji £17m (total with add-ons; the initial £15m counts), Vítek "up to £14m" and Rafael "up to £2.5m" (maxima), Robbie Brady "in excess of £2million" (a lower bound), Kalas "$7.8m" (what Olomouc "could get"; the radio.cz $8m page refused the runner), Tošić 2009 "?3.5 million" (currency lost; never guessed) and the $40m for Tošić and Ljajić together (a combined figure, DEC-405), Boateng to City 2010 "12.5m" (no currency on the page), Collyer's "guaranteed £3million" (Football365 only, grade C), Angeliño's €12m and £5.3m buy-back figures (both grade C; kept as versions).
- **Mikel 2006:** the Irish Times figure (£12m to Manchester United and £4m to Lyn) stays booked once, as £16m on the Manchester United → Chelsea move (DEC-420 (h)); the Lyn → Chelsea row stays £0.
- **Corrections applied:** Huws to Wigan 2014 (club statement), Cameron Stewart to Hull 2011 and Matt Smith to MK Dons 2022 (Yorkshire Post over a grade C "permanent") are loans; Billy Gee to Norwich 2024 is a free transfer plus add-ons; Josh Harrop to Preston 2017 is undisclosed training compensation (£0).
- **Corrections that change nothing:** Torres to Milan 2015, Razak to Anzhi 2013, Simpson to Newcastle 2010 and Bellion to Nice 2006 are the permanent steps of moves that began as loans, at undisclosed fees (£0); Bailly 2023, Mikel to Tianjin 2017 and Miazga 2022 were already free; Rojo 2021 "free" rests on a grade C page only (stays undisclosed, £0); Arzani 2018 a nominal fee with no figure (£0); Michael Ball 2007 a six-month contract, no fee (£0); Delač keeps the list date, 31 August 2010 (no source dates the completion; the 18 September 2009 announcement was of an agreement for a later move; £0 either way, the date goes to the next round); Samuels-Smith's £6.5m is already on the July 2025 sale, and his return stays £0.
- **The 12 pages read in Luke's Chrome (part25b):** none gives a grade A/B figure (`source/round4_chrome_reads.csv`); Crouch keeps his confirmed £9m (City AM).
- **IQ-15j clean-up (DEC-436):** Hector's club-page row (£5,310,000) was a duplicate of his Chelsea → Fulham move: one deal now, undisclosed (Fulham's and Chelsea's statements), dated 1 January 2020 (completed in the January window); Sporting Life's later "£8million" is not used. The widened duplicate test (same player, same two clubs, both loans or both not, within 180 days or the season) found three more among the club-page rows, all loans: Charlie Brown to Union SG, Nat Phillips to Stuttgart, Ryan Giles to Coventry. The four-column tables of summers 2017 and 2018 sit under a "Loans" heading: their 621 rows are now loans (Hector to Hull 2017 and Sheffield Wednesday 2018 among them). Jonny's £18m (Wolves, January 2019) again has no deal to attach to: his permanent move is not on Wikipedia's lists; it is listed for the next round.

**Question for Luke (it decides who leads at the freeze; the rules do not settle it):**
1. **Should Sporting Life count as quality press (grade B)?** The build has always graded it B, and 15 fees in use rest on it. Round 4 adds Courtois's sale to Real Madrid (2018, £31.5m), whose only figure is on Sporting Life. With Sporting Life as B, Manchester United lead at the freeze by £14.45m over Chelsea (£1,679.29m to £1,664.85m); as C everywhere (rebuilt in a scratch copy), Chelsea lead by £0.35m (£1,694.65m to £1,694.29m); as C for round 4 only, Chelsea lead by about £17m (inconsistent, not recommended). **Recommendation:** keep it B for now, as the build always has, and have Cowork find a BBC, Sky, PA or club source for the Sporting Life figures that decide the finish (Courtois 2018 first, then Henderson, Aké, Guéhi, Ziyech) before the order at the freeze is treated as settled. A second single-source figure matters too: Zhirkov's £13m sale (City AM, before completion): without it United still lead, by £1.45m.

## 18. Source round 5: the fees that decide the finish (IQ-15l; DEC-440 to DEC-444)

- **Why:** Luke's DEC-440: keep Sporting Life at grade B, find other sources for the Sporting Life fees that decide the finish, re-try the 13 unconfirmed round 4 figures and research the 14 round 2 deals that could change the leader; treat the order at the freeze as settled only once those are checked.
- **Inputs:** the 34-deal work list (`source/source_round5_map.csv`), Claude helper research on all 34 (part26a) and 41 page reads by Cowork in Luke's Chrome (part26b). Every file's SHA-256 matched `00_README.md`.
- **Checked at source:** the 73 pages cited read on the runner (https://github.com/marketmarathon/race-through-time/actions/runs/38000399943: 61 loaded; 6 refused, 3 server errors, 1 gone, 1 not found, 1 still loading); 13 pages the runner could not read or could not read the figure on were taken from Cowork's Chrome reads.
- **Quotes read:** 48 newly confirmed quotes (6 rejected: totals with add-ons, a maximum, another move's fee, and a figure that includes a friendly match).
- **Result: 28 of the 34 deals are now VERIFIED (10 before).** Each deal, before and after:

| Group | Player | Move | Date | Before | After | Status | Source of the figure in use |
|---|---|---|---|---|---|---|---|
| Sporting Life fees | Thibaut Courtois | Chelsea → Real Madrid | 2018-08-09 | £31,500,000 (VERIFIED) | £31,500,000 | VERIFIED (B) | Sporting Life (no author named) |
| Sporting Life fees | Dean Henderson | Manchester United → Crystal Palace | 2023-08-31 | £15,000,000 (VERIFIED) | £15,000,000 | VERIFIED (B) | Sporting Life |
| Sporting Life fees | Hakim Ziyech | Ajax → Chelsea | 2020-02-24 | £33,000,000 (VERIFIED) | EUR 40,000,000 = £33,599,328 | VERIFIED (A) | Ajax club statement as reproduced on eredivisie.com (credited '(Ajax.nl)') |
| Sporting Life fees | Marc Guéhi | Chelsea → Crystal Palace | 2021-07-18 | £18,000,000 (VERIFIED) | £18,000,000 | VERIFIED (B) | Sporting Life |
| Sporting Life and single-source fees | Nathan Aké | Chelsea → AFC Bournemouth | 2017-06-30 | £20,000,000 (VERIFIED) | £20,000,000 | VERIFIED (B) | Sporting Life |
| Sporting Life and single-source fees | Wilfried Bony | Manchester City → Swansea City | 2017-08-31 | £12,000,000 (VERIFIED) | £12,000,000 | VERIFIED (B) | BBC Sport |
| Sporting Life and single-source fees | Yuri Zhirkov | Chelsea → Anzhi Makhachkala | 2011-08-06 | £13,000,000 (VERIFIED) | EUR 15,000,000 = £13,132,551 | VERIFIED (B) | UEFA.com |
| Sporting Life and single-source fees | David de Gea | Atlético Madrid → Manchester United | 2011-06-29 | £18,000,000 (UNVERIFIED) | £18,000,000 | VERIFIED (B) | Ahram Online (Reuters) |
| Sporting Life and single-source fees | Shinji Kagawa | Borussia Dortmund → Manchester United | 2012-06-22 | £11,826,713 (UNVERIFIED) | £12,000,000 | VERIFIED (B) | Ahram Online (AFP) |
| Sporting Life and single-source fees | Javier Hernández | Guadalajara → Manchester United | 2010-05-27 | £7,000,000 (UNVERIFIED) | £0 | UNVERIFIED (B) | only a maximum, a total with add-ons or  |
| round 4 UNVERIFIED | Angeliño | Manchester City → RB Leipzig | 2021-02-13 | £16,300,000 (UNVERIFIED) | EUR 18,000,000 = £15,697,218 | VERIFIED (B) | TNT Sports (Eurosport) |
| round 4 UNVERIFIED | Douglas Luiz | Vasco da Gama → Manchester City | 2017-07-15 | £10,700,000 (UNVERIFIED) | £10,700,000 | VERIFIED (B) | The Telegraph (James Ducker) |
| round 4 UNVERIFIED | Giuseppe Rossi | Manchester United → Villarreal | 2007-07-31 | £6,700,000 (UNVERIFIED) | £6,700,000 | VERIFIED (B) | BBC Sport |
| round 4 UNVERIFIED | Alex Telles | Manchester United → Al Nassr | 2023-07-23 | £6,000,000 (UNVERIFIED) | £6,000,000 | VERIFIED (B) | Reuters (copy on Malay Mail) |
| round 4 UNVERIFIED | Matěj Kovář | Manchester United → Bayer Leverkusen | 2023-08-15 | £4,292,582 (UNVERIFIED) | EUR 5,000,000 = £4,292,582 | VERIFIED (B) | České noviny (ČTK, Czech news agency) |
| round 4 UNVERIFIED | Ángelo Henríquez | Universidad de Chile → Manchester United | 2012-09-05 | £3,500,000 (UNVERIFIED) | £3,500,000 | VERIFIED (B) | The Express Tribune (AFP) |
| round 4 UNVERIFIED | Anders Lindegaard | Aalesund → Manchester United | 2010-11-27 | £3,500,000 (UNVERIFIED) | £3,500,000 | VERIFIED (B) | Ahram Online (Reuters) |
| round 4 UNVERIFIED | Bruno Zuculini | Racing Club → Manchester City | 2014-08-08 | £3,000,000 (UNVERIFIED) | £3,000,000 | VERIFIED (B) | Gulf News (AFP) |
| round 4 UNVERIFIED | Ravel Morrison | Manchester United → West Ham United | 2012-01-31 | £650,000 (UNVERIFIED) | £650,000 | VERIFIED (B) | Romford Recorder |
| round 4 UNVERIFIED | Jeremie Frimpong | Manchester City → Celtic | 2019-09-01 | £350,000 (UNVERIFIED) | £350,000 | VERIFIED (B) | The Scotsman (byline David Gunn) |
| round 2 leader-test deals | Paul Furlong | Chelsea → Birmingham City | 1996-07-17 | £1,500,000 (UNVERIFIED) | £1,500,000 | UNVERIFIED (C) | Wikipedia: 1996–97 Chelsea F.C. season |
| round 2 leader-test deals | Gavin Peacock | Chelsea → Queens Park Rangers | 1996-12-23 | £800,000 (UNVERIFIED) | £800,000 | UNVERIFIED (C) | Wikipedia: 1996–97 Chelsea F.C. season |
| round 2 leader-test deals | Stephane Guivarc'h | Newcastle United → Rangers | 1998-11-06 | £3,500,000 (UNVERIFIED) | £3,500,000 | VERIFIED (B) | The Independent |
| round 2 leader-test deals | Andy Myers | Chelsea → Bradford City | 1999-07-08 | £800,000 (UNVERIFIED) | £800,000 | UNVERIFIED (C) | Wikipedia: 1999–2000 Bradford City A.F.C. season |
| round 2 leader-test deals | Mikkel Bischoff | AB → Manchester City | 2002-05-15 | £700,000 (UNVERIFIED) | £700,000 | UNVERIFIED (C) | Wikipedia: List of English football transfers summer 2002 |
| round 2 leader-test deals | Sylvain Distin | Paris Saint-Germain → Manchester City | 2002-05-20 | £4,000,000 (VERIFIED) | EUR 6,300,000 = £3,978,529 | VERIFIED (B) | UEFA.com |
| round 2 leader-test deals | Vicente Matías Vuoso | Independiente → Manchester City | 2002-06-06 | £3,500,000 (UNVERIFIED) | £3,500,000 | VERIFIED (B) | Sky Sports (by Mark Kendall) |
| round 2 leader-test deals | David Sommeil | Bordeaux → Manchester City | 2003-01-24 | £3,500,000 (UNVERIFIED) | EUR 5,000,000 = £3,315,870 | VERIFIED (B) | UEFA.com |
| round 2 leader-test deals | Trevor Sinclair | West Ham United → Manchester City | 2003-07-21 | £2,500,000 (VERIFIED) | EUR 3,500,000 = £2,481,741 | VERIFIED (B) | UEFA.com |
| round 2 leader-test deals | Antoine Sibierski | Lens → Manchester City | 2003-08-04 | £700,000 (UNVERIFIED) | EUR 1,000,000 = £704,077 | VERIFIED (B) | UEFA.com |
| round 2 leader-test deals | Claudio Reyna | Sunderland → Manchester City | 2003-08-29 | £2,500,000 (VERIFIED) | EUR 3,600,000 = £2,498,092 | VERIFIED (B) | UEFA.com |
| round 2 leader-test deals | David James | West Ham United → Manchester City | 2004-01-14 | £2,000,000 (UNVERIFIED) | £0 | UNVERIFIED (B) | undisclosed, no figure: counted £0 |
| round 2 leader-test deals | Darius Vassell | Aston Villa → Manchester City | 2005-07-27 | £2,000,000 (UNVERIFIED) | £2,000,000 | VERIFIED (A) | Manchester City FC (mancity.com) |
| round 2 leader-test deals | Andreas Isaksson | Rennes → Manchester City | 2006-08-15 | £2,000,000 (UNVERIFIED) | £2,000,000 | VERIFIED (A) | Manchester City FC (mancity.com) |

Where the figure in use still rests on Sporting Life (Courtois, Henderson, Guéhi, Aké), the same figure is now confirmed by the BBC (Henderson £15m, Aké £20m), The Independent (Guéhi £18m) or Reuters and AFP (Courtois €35m, £31.47m).

**Who leads, through time** (month the lead changes hands; from 2003):

- Before (1b01d81): Chelsea (2003-07) → Manchester City (2015-08) → Chelsea (2022-08) → Manchester United (2026-09)
- After (end of IQ-15l, 13173a4; section 19 has the current figures): Chelsea (2003-07) → Manchester City (2015-08) → Chelsea (2016-07) → Manchester City (2016-08) → Chelsea (2022-08) → Manchester United (2026-09)

The leader differs at 1 month end (2016-07); who is in the top 12 differs at 0 month ends.

**Standings at the freeze (2026-09-01), cumulative net spend, at the end of IQ-15l:**

| Rank after | Club | Net before (rank) | Net after | Change |
|---|---|---|---|---|
| 1 | Manchester United | £1,679.29m (1) | £1,672.47m | −£6.8m |
| 2 | Chelsea | £1,664.85m (2) | £1,665.31m | £0.5m |
| 3 | Manchester City | £1,645.33m (3) | £1,643.71m | −£1.6m |
| 4 | Arsenal | £1,126.89m (4) | £1,126.89m | £0.0m |
| 5 | Liverpool | £988.92m (5) | £988.92m | £0.0m |
| 6 | Tottenham Hotspur | £984.98m (6) | £984.98m | £0.0m |
| 7 | Newcastle United | £702.59m (7) | £702.59m | £0.0m |
| 8 | West Ham United | £590.46m (8) | £590.46m | £0.0m |
| 9 | Everton | £376.12m (9) | £376.12m | £0.0m |
| 10 | Fulham | £367.32m (10) | £367.32m | £0.0m |
| 11 | Sunderland | £338.41m (11) | £338.41m | £0.0m |
| 12 | Aston Villa | £313.10m (12) | £313.10m | £0.0m |

**Gaps between the three leaders:** after, Manchester United lead Chelsea by £7.15m and Manchester City by £28.76m; before, Manchester United led Chelsea by £14.45m and Manchester City by £33.96m.

**Order test re-run** (`source/round2_order_test.csv`, the round 5 deals now counted as researched; at the end of IQ-15l: 188 of 378): 197 of 369 unresearched round 2 deals could change who is in the top 12 at some month end, **0 the leader** (14 before this round). Of the five round 5 deals with no grade A/B source, only Guivarc'h (Newcastle → Rangers, 1998, £3.5m) changes the leader if removed, at August 1999 (tested in a scratch copy). Undisclosed fees counted £0 cannot be tested this way: there is no figure to try.

**Still UNVERIFIED among the 34: 4** (no grade A/B page found): Paul Furlong £1,500,000 (1996); Gavin Peacock £800,000 (1996); Andy Myers £800,000 (1999); Mikkel Bischoff £700,000 (2002). Hernández and David James now count £0.

**Decided under DEC-417 (Claude, DEC-441 and DEC-442):**
- **Grading:** agency copy on a foreign site (Oman Observer, Jakarta Post, TSN, SuperSport, Malay Mail, Morung Express, Ahram, Gulf News, IOL, Channels TV, Al Jazeera, Mail & Guardian, Express Tribune) keeps the agency's grade B only where the helper's or Cowork's note says the page credits the agency; The Star (Kenya), which shows no credit, is C. Ajax's own statement, reproduced word for word on eredivisie.com with its credit, is the club's statement: grade A (contract §3). Sporting Life stays B (Luke, DEC-440).
- **Where the runner was refused** (Ahram, Express Tribune) or could not read the figure (a broken £ sign, a Czech figure in words, a page needing scripts), Cowork's read in Luke's Chrome (part26b) is the page read: 13 checks recorded as such in `runner_checks.csv` (De Gea, Kagawa, Lindegaard, Henríquez, Telles, Zuculini ×2, Morrison, Kovář, Rossi, Angeliño, Frimpong, Hernández).
- **DEC-404:** a completion report with a figure beats an agreed or expected figure of the same grade: Zhirkov counts UEFA.com's €15m (after he joined) instead of City AM's £13m (before); Distin counts UEFA.com's €6.3m ("completed the €6.3m signing") over a later Sapa-AP summary list (£4m); Vuoso keeps £3.5m (Sky, after he joined) over UEFA.com's €6.3m ("hoping to complete"); Courtois keeps Sporting Life's completed £31.5m (Reuters' and AFP's €35m are agreement-stage versions, kept). Where the completion report has no figure, the earliest grade B figure stands: Douglas Luiz £10.7m (Telegraph, agreed; the Premier League said undisclosed), Henríquez £3.5m (AFP, before his medical; the Reuters completion report says undisclosed), De Gea £18m and Kagawa £12m (agreement-stage agency estimates).
- **Not the fee (DEC-276, DEC-237 (d)):** Henderson's £20m (a total including £5m add-ons; BBC: "£15m plus £5m in add-ons", so £15m counts); Guéhi's "up to £20m" (Guardian, Evening Standard: maxima; the Independent's completed £18m counts); Courtois's "up to £35m" (BBC); Ziyech's €44m (a maximum; Ajax's guaranteed €40m counts); Kovář's "up to €3 million" bonuses (his €5m counts); Frimpong's "as much as £1 million" (his initial £350,000 counts); Hernández's "around £7 million", which includes United playing a friendly in Mexico (a part of the deal with no stated value): £0; Bony's £25m (his 2015 move).
- **Currencies as published:** Kagawa counts the page's "around 12 million pounds", not its dollar conversion; Ziyech €40m, Zhirkov €15m, Angeliño €18m (the buy option, TNT Sports; Sky's £16.3m page is gone), Kovář €5m, and the UEFA.com euro figures for Distin, Sommeil, Sinclair, Sibierski and Reyna are converted at the transfer date.
- **A grade B euro figure beside a grade C pound figure (contract §3, highest grade):** the euro figure wins for Distin (€6.3m over Soccerbase £4m), Sommeil (€5m over Wikipedia £3.5m), Sinclair (€3.5m over Soccerbase £2.5m), Sibierski (around €1m over Wikipedia £0.7m) and Reyna (€3.6m over Soccerbase £2.5m).
- **David James (2004):** the Irish Times reports the fee as undisclosed and West Ham's £1.3m is a later feature (grade C), so the undisclosed rule gives £0 (was £2m from Wikipedia).
- **A one-month change of leader:** Chelsea now lead Manchester City at the end of July 2016, by £1.6m (City had led that month); it comes mainly from David James's £2m now counting £0. The rules settle it; it is a knife edge to show with care.
- **Nothing at grade A/B:** Furlong, Peacock, Guivarc'h, Myers and Bischoff keep their figures as UNVERIFIED pointers. Of these only Guivarc'h (Newcastle → Rangers, 1998, £3.5m, an Independent round-up) changes the leader if removed: at August 1999. It goes to the next round.
- **Sporting Life as C everywhere (scratch copy):** Manchester United still lead at the freeze (£1,672.47m against Chelsea's £1,665.34m) and the leader sequence is unchanged; Courtois then counts the agencies' €35m (£31.47m). Sporting Life no longer decides the finish.

**Question for Luke (an on-screen claim):**
1. **Can the order at the freeze now be treated as settled?** Your three conditions (DEC-440) are met: the Sporting Life fees that decided the finish have BBC, Independent, agency or club sources; the 13 unconfirmed round 4 figures were re-tried (12 now confirmed, Hernández's excluded); the 14 round 2 deals were researched, and no unresearched round 2 deal can now change the leader. Manchester United finish £7.16m ahead of Chelsea, with Manchester City £28.8m behind; 2,009 undisclosed fees across the league (274 of them involving the three leaders) are still counted £0 because no figure was found. **Recommendation:** yes, treat Manchester United as the leader at the freeze, with the label "Undisclosed fees not included" on screen (DEC-429); keep the gap shown as a figure rather than calling it decisive, since £7m is within what undisclosed fees could move.

## 19. Wrap-up before design (IQ-15m; DEC-445 to DEC-449)

*Recorded as built at the end of IQ-15m (aa6bf3c); section 20 has the figures after source round 6.*

**What changed**

- **Luke's DEC-445:** RTT-101 keeps being built from our own deal-by-deal data; no Transfermarkt or press club totals anywhere; the P4 sweep is not run now. Section 18's question 1 stays open: on VERIFIED fees only the order at the freeze is different.
- **Guivarc'h (1998):** £3.5m confirmed from Cowork's Chrome read of The Independent's weekly round-up (DEC-446).
- **Thin windows (DEC-447):** 604 deals the list pages miss added from club-season pages (January 1993, 1994, 2004, 2005; summers 2007, 2013, 2019); 23 carry a Wikipedia figure (£49.2m), none yet confirmed; 90 undisclosed or unconfirmed ones listed in `source/thin_windows_unsourced.csv`. The deal-count check passes for every window and `KNOWN_SPARSE` is empty.
- **The on-screen series (DEC-448):** `series_onscreen.csv`, built from VERIFIED fees only (every tier), beside the all-fees preview `series_monthly.csv`; contract v1.5 §8 points the player at it.

**Window totals against part17b** (gross spending by PL clubs; 40 windows with a published total; research leads, UNVERIFIED, a comparison only): our totals average 83.5% of the published figure before IQ-15m and 83.6% after; as a share of the money, 88.2% before and 88.3% after (the thin windows add mostly loans, free transfers and undisclosed fees).

**Standings at the freeze (2026-09-01), top 12:**

| Rank | On screen (VERIFIED fees only) | Net | Gap to the leader | Preview (all fees) | Net |
|---|---|---|---|---|---|
| 1 | Chelsea | £1,710.9m | – | Manchester United | £1,676.0m |
| 2 | Manchester City | £1,699.8m | £11.0m | Chelsea | £1,654.8m |
| 3 | Manchester United | £1,635.6m | £75.2m | Manchester City | £1,646.9m |
| 4 | Arsenal | £1,029.4m | £681.4m | Arsenal | £1,123.8m |
| 5 | Liverpool | £911.0m | £799.9m | Liverpool | £990.6m |
| 6 | Tottenham Hotspur | £841.9m | £869.0m | Tottenham Hotspur | £980.3m |
| 7 | Newcastle United | £636.8m | £1,074.1m | Newcastle United | £702.6m |
| 8 | West Ham United | £487.8m | £1,223.1m | West Ham United | £590.5m |
| 9 | Fulham | £381.9m | £1,328.9m | Everton | £376.1m |
| 10 | Aston Villa | £256.6m | £1,454.3m | Fulham | £367.3m |
| 11 | Ipswich Town | £255.4m | £1,455.5m | Sunderland | £338.4m |
| 12 | Leeds United | £245.3m | £1,465.5m | Aston Villa | £312.8m |

**Who leads, through time** (month the lead changes hands):

- On screen: Arsenal (1992-05) → Blackburn Rovers (1992-07) → Liverpool (1995-07) → Newcastle United (1996-07) → Liverpool (1997-12) → Newcastle United (1998-02) → Liverpool (1999-07) → Manchester United (2001-07) → Liverpool (2001-08) → Leeds United (2001-11) → Liverpool (2002-06) → Manchester United (2002-07) → Chelsea (2003-07) → Manchester City (2015-08) → Chelsea (2022-08)
- Preview: Arsenal (1992-05) → Blackburn Rovers (1992-07) → Liverpool (1993-07) → Blackburn Rovers (1993-09) → Liverpool (1995-07) → Newcastle United (1996-07) → Liverpool (1997-12) → Newcastle United (1998-02) → Liverpool (1999-07) → Chelsea (2000-06) → Liverpool (2000-07) → Manchester United (2001-07) → Liverpool (2001-08) → Leeds United (2001-11) → Liverpool (2002-06) → Manchester United (2002-07) → Chelsea (2003-07) → Manchester City (2015-08) → Chelsea (2016-07) → Manchester City (2016-08) → Chelsea (2022-08) → Manchester United (2026-09)

**Close calls since July 2002** (leader ahead by under £10m at a month end): on screen, none; in the preview, 2002-07 Manchester United over Liverpool by £9.57m; 2003-01 Manchester United over Newcastle United by £3.21m; 2003-02 Manchester United over Newcastle United by £3.21m; 2003-03 Manchester United over Newcastle United by £2.21m; 2003-04 Manchester United over Newcastle United by £2.21m; 2003-05 Manchester United over Newcastle United by £2.21m; 2003-06 Manchester United over Newcastle United by £2.21m; 2015-09 Manchester City over Chelsea by £9.87m; 2015-10 Manchester City over Chelsea by £9.87m; 2015-11 Manchester City over Chelsea by £9.87m; 2015-12 Manchester City over Chelsea by £9.87m; 2016-07 Chelsea over Manchester City by £1.60m. The one-month Chelsea lead of July 2016 and the March–June 2003 near-tie (United over Newcastle) exist only in the preview. Before 2002 the race is close for long stretches on both bases (Blackburn, Liverpool and Newcastle within £3m of each other in many months of 1992–2000).

**Top-12 changes and the order test:** against 13173a4 the preview's leader changes at 0 month ends and who is in its top 12 at 11; the on-screen series differs from the preview in the leader at 5 month ends. Order test (`source/round2_order_test.csv`): 191 of 378 unresearched round 2 deals could change a top-12 place, 0 the leader.

**VERIFIED share of fee money:** 86.3% of £34.74bn of fees (2229 of 3530 fees); Tier 1 93.3%, Tier 2 59.7%, Tier 3 30.9%.

**Still UNVERIFIED:** 334 Tier 1 fees (`tier1_open.csv`, no figures; 42 involve Manchester United, Chelsea or Manchester City; why open: no grade A/B source 176, quote does not match 106, other 49, page did not load 3). If every unconfirmed fee were confirmed, Chelsea would lose £56.1m on screen, City £52.9m and United gain £40.3m: the gap between the two bases, so the order at the freeze waits for Cowork's Tier 1 round (DEC-445). Tier 2 and Tier 3 fees not confirmed stay off screen (DEC-448).

**Question for Luke (what the video shows):**
1. **On screen, should a bar count only fees confirmed at source, including the small ones under £2m?** That is what the contract says (§8) and what `series_onscreen.csv` does; the approved tiers had small fees counted on the strength of a sample, but the sample cannot yet give an error rate. Counting the small unconfirmed fees as well changes no leader (Chelsea still lead at the freeze, by £8.1m instead of £11.0m). **Recommendation:** yes, confirmed fees only, every tier.

## 20. Source round 6: the leaders' open Tier 1 fees (IQ-15n; DEC-450 to DEC-453)

Luke's DEC-450: the 53 open Tier 1 fees involving Manchester United, Chelsea or Manchester City at 13173a4 were checked in Cowork (`part27a`, `part27b`); the other open Tier 1 fees go to a ChatGPT prompt Luke runs (`RTT-101_source_round6_map.csv`). Every page cited was read on the GitHub runner (99 pages, then 4 again); a quote counts only where the runner, or Cowork's Chrome read, found it word for word.

**The 53 deals, before and after** (fee in pounds at the transfer date; grade; status):

| L ID | Deal | Date | Before | After | What settled it |
|---|---|---|---|---|---|
| L6001 | Jason Cundy: Chelsea → Tottenham Hotspur | 1992-07-02 | £0.80m C UNVERIFIED | £0.80m C UNVERIFIED | only a feature three years later says 'Bought for pounds 800,000': not contemporary press, so grade C (contract §3) |
| L6002 | Pat McGibbon: Portadown → Manchester United | 1992-08-01 | £0.10m C UNVERIFIED | £0.10m C UNVERIFIED | no grade A or B source read |
| L6003 | Scott Minto: Charlton Athletic → Chelsea | 1994-05-28 | £0.78m C UNVERIFIED | £0.78m C UNVERIFIED | no grade A or B source read |
| L6004 | Keith Gillespie: Manchester United → Newcastle United | 1995-01-10 | £1.00m B UNVERIFIED | £1.00m B VERIFIED | £1m 'makeweight' (The Independent; Cowork's Chrome read, as the page does not name United) (DEC-407) |
| L6005 | Tony Coton: Manchester City → Manchester United | 1996-01-31 | £0.50m C UNVERIFIED | £0.50m C UNVERIFIED | no grade A or B source read |
| L6006 | Muzzy Izzet: Chelsea → Leicester City | 1996-07-08 | £0.65m C UNVERIFIED | £0.65m C UNVERIFIED | no grade A or B source read |
| L6007 | Ed de Goey: Feyenoord → Chelsea | 1997-06-11 | £2.25m C UNVERIFIED | £2.25m C UNVERIFIED | no grade A or B source read |
| L6008 | John O'Kane: Manchester United → Everton | 1998-01-28 | £0.40m B UNVERIFIED | £0.40m B VERIFIED | 'around pounds 400,000' agreed, then 'his pounds 400,000 move' (The Independent); the December 1998 list's £250,000 rising to £500,000 (grade C) kept as a version |
| L6009 | Albert Ferrer: Barcelona → Chelsea | 1998-06-09 | £2.20m C UNVERIFIED | £2.20m C UNVERIFIED | no grade A or B source read |
| L6010 | Slaviša Jokanović: Deportivo → Chelsea | 2000-10-10 | £1.70m C UNVERIFIED | £1.70m C UNVERIFIED | no grade A or B source read |
| L6011 | Dwight Yorke: Manchester United → Blackburn Rovers | 2002-07-26 | £2.00m C UNVERIFIED | £2.00m B VERIFIED | '£2million deal; fee could rise to £2.6million depending on appearances and how well Rovers do' (irishexaminer.com) |
| L6012 | Claude Makélélé: Real Madrid → Chelsea | 2003-09-01 | £16.60m B UNVERIFIED | £16.60m B VERIFIED | 'his £16.6m fee' (The Guardian); UEFA.com's 'in the region of €23m' kept as a same-grade version |
| L6013 | Jesper Grønkjær: Chelsea → Birmingham City | 2004-07-12 | £2.20m C UNVERIFIED | £2.20m B VERIFIED | '€3.3m' (uefa.com) |
| L6014 | Mateja Kežman: PSV → Chelsea | 2004-07-12 | £5.30m C UNVERIFIED | £5.00m B VERIFIED | 'around £5 million (believed); headline says £5m' (irishexaminer.com) |
| L6015 | Mikael Forssell: Chelsea → Birmingham City | 2005-06-10 | £3.00m C UNVERIFIED | £3.01m B VERIFIED | '€4.5m' (uefa.com) |
| L6016 | Shaun Wright-Phillips: Manchester City → Chelsea | 2005-07-18 | £21.00m B UNVERIFIED | £17.00m B VERIFIED | £17m up front (The Guardian); the £21m and UEFA's €30.4m include appearance payments (DEC-276, DEC-420 (e)) |
| L6017 | Eiður Guðjohnsen: Chelsea → Barcelona | 2006-06-14 | £8.00m B UNVERIFIED | £8.00m B VERIFIED | '€11.7m ("reported")' (uefa.com) |
| L6018 | Martin Petrov: Atlético Madrid → Manchester City | 2007-07-26 | £4.70m C UNVERIFIED | £4.70m A VERIFIED | '£4.7million' (mancity.com) |
| L6019 | Franco Di Santo: Audax Italiano → Chelsea | 2008-01-01 | £3.40m C UNVERIFIED | £2.99m B VERIFIED | the page reads 'a reported €4m fee' (the helper's 'in excess of' is not on it) |
| L6020 | Shaun Wright-Phillips: Chelsea → Manchester City | 2008-08-28 | £9.00m B UNVERIFIED | £9.00m B UNVERIFIED | City AM's 'around £9m' refused the runner (403); the 2008 report's 21 million pounds is the 2005 fee (rejected) |
| L6021 | Craig Bellamy: West Ham United → Manchester City | 2009-01-19 | £14.00m B UNVERIFIED | £14.00m B UNVERIFIED | only 'at least 14 million pounds' (a lower bound) and an offer with no currency; UEFA.com says undisclosed |
| L6022 | Chris Smalling: Fulham → Manchester United | 2010-07-01 | £8.00m B UNVERIFIED | £8.00m B UNVERIFIED | '£8m-rated' is a valuation at the agreement stage, not a reported fee |
| L6023 | Yossi Benayoun: Liverpool → Chelsea | 2010-07-02 | £5.00m B UNVERIFIED | £6.50m B VERIFIED | '£6.5m' (thejc.com) |
| L6024 | Ashley Young: Aston Villa → Manchester United | 2011-06-23 | £16.90m B UNVERIFIED | £15.00m B VERIFIED | 'around 15 million pounds' (Khaleej Times; Al Jazeera's $24m is the same estimate); Ahram's £17m refused the runner |
| L6025 | Wilfried Zaha: Crystal Palace → Manchester United | 2013-01-25 | £10.00m C UNVERIFIED | £15.00m B VERIFIED | '15 million pounds ($23.6 million)' (SI.com); £10m up front plus £5m appears only in grade C sources |
| L6026 | Cristián Cuevas: O'Higgins → Chelsea | 2013-07-23 | £3.00m C UNVERIFIED | £2.58m B UNVERIFIED | only 'reportedly worth more than €3m' (a lower bound) |
| L6027 | Gareth Barry: Manchester City → Everton | 2014-07-08 | £2.00m C UNVERIFIED | free B VERIFIED | free: his City contract 'expired in June' (Reuters copy); Wikipedia's £2m dropped |
| L6028 | Nathan: Atlético Paranaense → Chelsea | 2015-05-14 | £4.50m C UNVERIFIED | £4.50m B VERIFIED | 'reportedly agreed a deal worth £4.5m' (skysports.com) |
| L6029 | Marcos Lopes: Manchester City → Monaco | 2015-08-29 | £3.90m C UNVERIFIED | £9.00m B VERIFIED | 'around £9million' (The Irish News); completion date moved to 29 Aug 2015 |
| L6030 | Karim Rekik: Manchester City → Marseille | 2015-06-30 | £3.90m C UNVERIFIED | £0.00m B UNVERIFIED | undisclosed (Eurosport's page now gone); counted £0 |
| L6031 | Matteo Darmian: Torino → Manchester United | 2015-07-11 | £12.70m C UNVERIFIED | £14.15m B VERIFIED | the completion report's €20m (Eurosport) over the agreed £12.9m; the met 'asking price of £12.7m' rejected (DEC-404) |
| L6032 | Bastian Schweinsteiger: Bayern Munich → Manchester United | 2015-07-13 | £14.40m C UNVERIFIED | £14.00m B VERIFIED | 'around £14m (Dh79.9m), per German and UK media' (gulfnews.com) |
| L6033 | Kenedy: Fluminense → Chelsea | 2015-08-22 | £6.70m B UNVERIFIED | £6.70m B UNVERIFIED | TNT Sports' '£6.7m' was read but the page does not name Fluminense; Fox says undisclosed |
| L6034 | Jonny Evans: Manchester United → West Bromwich Albion | 2015-08-29 | £6.00m B UNVERIFIED | £6.00m B VERIFIED | 'reported to have cost Albion £6 million (Dh34 million), plus a potential £2 million in add-ons' (gulfnews.com) |
| L6035 | Papy Djilobodji: Nantes → Chelsea | 2015-09-01 | £2.70m C UNVERIFIED | £4.00m B VERIFIED | the completion report's 'reported £4 million' over the pre-completion £2.7m (DEC-404) |
| L6036 | Seko Fofana: Manchester City → Udinese | 2016-06-21 | £3.80m C UNVERIFIED | £3.80m C UNVERIFIED | no grade A or B source read |
| L6037 | Juan Cuadrado: Chelsea → Juventus | 2017-05-22 | £17.00m C UNVERIFIED | £17.28m B VERIFIED | 'EUR 20 million paid in three annual instalments starting from 2017/2018 financial year' (tntsports.co.uk) |
| L6038 | Ethan Ampadu: Exeter City → Chelsea | 2017-07-01 | £1.30m B UNVERIFIED | £1.30m B VERIFIED | £1.3m guaranteed (Sky Sports on the tribunal); £850,000 initial and 'up to £2.5m' rejected (DEC-276) |
| L6039 | Nemanja Matić: Chelsea → Manchester United | 2017-07-31 | £35.00m B UNVERIFIED | £35.00m B UNVERIFIED | ITV's £35m (plus up to £5m) timed out twice on the runner; the Premier League says undisclosed |
| L6040 | Aaron Wan-Bissaka: Crystal Palace → Manchester United | 2019-06-28 | £50.00m B UNVERIFIED | £45.00m B VERIFIED | £45m up front (BBC); the £50m includes add-ons (DEC-276, DEC-420 (e)) |
| L6041 | Mario Pašalić: Chelsea → Atalanta | 2020-09-01 | £13.40m C UNVERIFIED | £12.57m B UNVERIFIED | both cited pages refused or gone (403, 404) |
| L6042 | Kalidou Koulibaly: Chelsea → Al Hilal | 2023-06-25 | £17.00m C UNVERIFIED | £17.00m B VERIFIED | 'GBP 17million' (sg.news.yahoo.com) |
| L6043 | Ruben Loftus-Cheek: Chelsea → AC Milan | 2023-06-30 | £15.00m C UNVERIFIED | £14.00m B VERIFIED | an initial £14million (Yahoo, PA copy); the 21 million euros (£18m) total rejected (DEC-420 (e)) |
| L6044 | Christian Pulisic: Chelsea → AC Milan | 2023-07-13 | £19.00m C UNVERIFIED | £17.08m B VERIFIED | 'believed to be worth up to EUR 22 million (GBP 18.8m): initial EUR 20m plus EUR 2m in add-ons' (tntsports.co.uk) |
| L6045 | Rasmus Højlund: Atalanta → Manchester United | 2023-08-05 | £64.00m B UNVERIFIED | £64.00m B VERIFIED | an initial £64m (Sky Sports); the £72m includes add-ons (DEC-420 (e)) |
| L6046 | Taylor Harwood-Bellis: Manchester City → Southampton | 2024-06-14 | £20.00m B UNVERIFIED | £20.00m B VERIFIED | the play-off win 'triggers £20m move' (BBC) |
| L6047 | Kiernan Dewsbury-Hall: Leicester City → Chelsea | 2024-07-02 | £30.00m B UNVERIFIED | £30.00m B VERIFIED | 'around £30million' (breakingnews.ie) |
| L6048 | Sávio: Troyes → Manchester City | 2024-07-18 | £33.64m B UNVERIFIED | £21.10m B VERIFIED | an initial £21.1 million (The Telegraph, Yahoo copy); the €40m and £33.7m include add-ons; the runner missed it at first because the page says Savinho |
| L6049 | Rayan Aït-Nouri: Wolverhampton Wanderers → Manchester City | 2025-06-09 | £31.00m B UNVERIFIED | £31.00m B VERIFIED | 'a reported £31 million'; the £33.7m includes add-ons (DEC-420 (e)) |
| L6050 | Kiernan Dewsbury-Hall: Chelsea → Everton | 2025-08-06 | £24.75m B UNVERIFIED | £24.00m B VERIFIED | an initial £24 million (BBC Sport, credited, 4 Aug 2025), the earliest dated report; Sky Sports' initial £25m kept as a same-grade version |
| L6051 | Rasmus Højlund: Manchester United → Napoli | 2026-06-29 | £43.85m B UNVERIFIED | £37.95m B VERIFIED | '44 million euros ($51 million)' (agency copy); the dollars are the page's conversion |
| L6052 | Tynan Thompson: Tottenham Hotspur → Manchester United | 2026-07-20 | £8.00m C UNVERIFIED | £4.00m C UNVERIFIED | only beIN Sports (grade C): £4m guaranteed, up to £8m |
| L6053 | Tosin Adarabioyo: Chelsea → Tottenham Hotspur | 2026-09-01 | £10.00m C UNVERIFIED | £7.00m B VERIFIED | 'set to join for a fee of £7m' (Irish News, deadline day); the BBC's 'up to £12m' is a maximum |

35 of the 53 are now VERIFIED. **The leaders' open Tier 1 fees:** 42 at the end of IQ-15m; 25 of them are now VERIFIED, 12 are still open and 5 have left Tier 1. Because the race at the freeze has changed, 17 other leader deals are now Tier 1 ('removal changes the leader or the top 12'), so 29 leader fees are open now (`tier1_open.csv`, 312 open Tier 1 fees in all, 334 before): Jason Cundy (Chelsea → Tottenham Hotspur, 1992); Pat McGibbon (Portadown → Manchester United, 1992); Scott Minto (Charlton Athletic → Chelsea, 1994); Tony Coton (Manchester City → Manchester United, 1996); Muzzy Izzet (Chelsea → Leicester City, 1996); Ed de Goey (Feyenoord → Chelsea, 1997); Albert Ferrer (Barcelona → Chelsea, 1998); Shaun Goater (Manchester City → Reading, 2003); Kevin Horlock (Manchester City → West Ham United, 2003); Gabriel Heinze (Paris Saint-Germain → Manchester United, 2004); Paulo Wanchope (Manchester City → Málaga CF, 2004); Mateja Kežman (Chelsea → Atlético Madrid, 2005); Tiago Mendes (Chelsea → Olympique Lyonnais, 2005); Lee Croft (Manchester City → Norwich City, 2006); David James (Manchester City → Portsmouth, 2006); Shaun Wright-Phillips (Chelsea → Manchester City, 2008); Craig Bellamy (West Ham United → Manchester City, 2009); Chris Smalling (Fulham → Manchester United, 2010); Park Ji-Sung (Manchester United → Queens Park Rangers, 2012); Thorgan Hazard (Chelsea → Borussia Mönchengladbach, 2015); Enes Ünal (Manchester City → Villarreal, 2017); Nolito (Manchester City → Sevilla, 2017); Nemanja Matić (Chelsea → Manchester United, 2017); Jadon Sancho (Manchester City → Borussia Dortmund, 2017); Angus Gunn (Manchester City → Southampton, 2018); Tomáš Kalas (Chelsea → Bristol City, 2019); Félix Correia (Manchester City → Juventus, 2020); Mario Pašalić (Chelsea → Atalanta, 2020); Deivid Washington (Chelsea → Strasborug, 2026).

**Finding: hyphens and apostrophes in surnames (DEC-452).** The runner's surname test compared one word, so 'Wright-Phillips', 'Wan-Bissaka' or 'O'Kane' never matched and figures the runner had already found were never attached. Fixed in `rtt101_ingest_probe.py` and the build. It touched 21 deals outside this round's 53 as well: 19 are now VERIFIED at the figure they already showed or at the page's own figure (Hwang £14m, was £13m; Fernández-Pardo £51.4m, was £51m), and two figures were rejected on review (Hudson-Odoi's 'under £5m' is an upper bound; Samuels-Smith 'was valued at £6.5m'), so those two count £0 (`source/round6_namefix_deals.csv`). Sávio's page calls him Savinho: the runner read it, and the check was added by hand.

**On-screen standings at the freeze (2026-09-01), top 12** (VERIFIED fees only; before = end of IQ-15m):

| Rank | Club | Net | Gap to the leader | Before | Rank before |
|---|---|---|---|---|---|
| 1 | Manchester United | £1,740.4m | – | £1,635.6m | 3 |
| 2 | Manchester City | £1,710.6m | £29.8m | £1,699.8m | 2 |
| 3 | Chelsea | £1,689.2m | £51.2m | £1,710.9m | 1 |
| 4 | Arsenal | £994.4m | £746.0m | £1,029.4m | 4 |
| 5 | Liverpool | £931.1m | £809.4m | £911.0m | 5 |
| 6 | Tottenham Hotspur | £831.9m | £908.5m | £841.9m | 6 |
| 7 | Newcastle United | £683.2m | £1,057.2m | £636.8m | 7 |
| 8 | West Ham United | £532.8m | £1,207.6m | £487.8m | 8 |
| 9 | Fulham | £381.9m | £1,358.5m | £381.9m | 9 |
| 10 | Everton | £285.0m | £1,455.4m | £244.2m | 13 |
| 11 | Aston Villa | £263.1m | £1,477.4m | £256.6m | 10 |
| 12 | Ipswich Town | £255.4m | £1,485.0m | £255.4m | 11 |

**On-screen leader, through time** (month the lead changes hands):

- Section 19 (before): Arsenal (1992-05) → Blackburn Rovers (1992-07) → Liverpool (1995-07) → Newcastle United (1996-07) → Liverpool (1997-12) → Newcastle United (1998-02) → Liverpool (1999-07) → Manchester United (2001-07) → Liverpool (2001-08) → Leeds United (2001-11) → Liverpool (2002-06) → Manchester United (2002-07) → Chelsea (2003-07) → Manchester City (2015-08) → Chelsea (2022-08)
- Now: Arsenal (1992-05) → Blackburn Rovers (1992-07) → Liverpool (1995-07) → Newcastle United (1996-07) → Liverpool (1998-01) → Newcastle United (1998-02) → Liverpool (1999-07) → Manchester United (2001-07) → Liverpool (2001-08) → Leeds United (2001-11) → Liverpool (2002-06) → Manchester United (2002-07) → Chelsea (2003-07) → Manchester City (2016-08) → Chelsea (2022-08) → Manchester United (2026-09)
- The leader differs at 14 month ends, from 1997-12 to 2026-09.

**Close calls on screen since July 2002** (leader ahead by under £10m at a month end): 2002-07 Manchester United over Liverpool by £8.86m; 2003-06 Manchester United over Liverpool by £6.86m; 2016-06 Chelsea over Manchester City by £2.65m; 2022-07 Manchester City over Chelsea by £8.61m.

**Order test** (`source/round2_order_test.csv`; the round 6 deals now count as researched): 197 of 369 unresearched round 2 deals could change a top-12 place, 0 the leader (section 19: 191 of 378, none).

**Section 19's bound, now.** Section 19 said that if every unconfirmed fee were confirmed, Chelsea would lose £56.1m on screen, City £52.9m and United gain £40.3m. Now the same comparison (preview minus on screen, at the freeze) gives United −£63.4m, Chelsea −£18.0m and City −£71.4m. The preview's own order is United £1,677.0m, Chelsea £1,671.2m, City £1,639.2m.

**VERIFIED share of fee money:** 88.8% of £34.70bn (2282 of 3526 fees); Tier 1 95.5%, Tier 2 60.3%, Tier 3 30.4% (section 19: 86.3%; Tier 1 93.3%).

**For the next research round:** 32 open Tier 1 deals at 13173a4 were missing from ChatGPT's round 6 map (`source/round6_map_missing.csv`), and the leaders' fees still open above. Section 19's question 1 is still with Luke; `series_onscreen.csv` is built as before.
