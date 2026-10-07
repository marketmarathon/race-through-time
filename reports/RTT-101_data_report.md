# RTT-101 Premier League net transfer spend — data report, phase 1 (IQ-15, 7 Oct 2026)

**Status: UNVERIFIED preview. Not for screen.** Only figures marked VERIFIED may ever be shown, and phase 2 (verification of Tier 1 at source, in batches) comes before any design work. Rules: `reference/metric_contract_RTT-101.md`; decisions DEC-235 to DEC-250 (and the findings recorded with this build).

Rebuild: `python3 scripts/build_rtt101_dataset.py && python3 scripts/rtt101_report.py` (deterministic; the private cross-checks need the private folder: `python3 scripts/rtt101_private_crosschecks.py <private research folder>` first).

## 1. What was built

- **12,824 transfer events** that involve a club in the Premier League that season (1992-93 to the freeze, 1 Sep 2026), of which **3,123 carry a fee** above £0. The rest are loans without a fee (5,327), free transfers (2,015), undisclosed fees with no figure, counted £0 (2,212), and fees not found (147).
- Fee status: **VERIFIED 1,055**, UNVERIFIED 2,068. Grade of the fee used: A 17, B 1,038, C (Wikipedia pointer only) 2,015, D 53.
- Tiers (DEC-248): Tier 1 **1,892**, Tier 2 661, Tier 3 580 (5% sample: 29).
  Tier 1 reasons (a transfer can have several): removal changes the leader or the top 12 944; fee >= £20m 576; club or British record (research lead) 537; disputed fee (research section C) 24; alternative fee version changes the leader or the top 12 1.
- 14,917 evidence rows in `fee_evidence.csv`; 1,782 sources in `sources.csv`; 272 transfers with more than one fee version (`conflicts.csv`).
- **Scripted source check** (GitHub runner, 2,049 cited pages): VERIFIED 1,470; page fetched but figure not found near the player's name 501; blocked or gone 78.
  Tier 2 result: 222 of 661 Tier 2 fees VERIFIED by the scripted check.
  Tier 3 sample: 0 of 29 VERIFIED; most Tier 3 rows have no fetchable citation (error rate cannot be published yet: phase 2).

## 2. Checks

| Check | Result | Detail |
|---|---|---|
| 22 clubs per season 1992-95, 20 after (706 club-seasons) | **PASS** | 706 club-seasons in 35 seasons |
| every season has an attribution window | **PASS** | 1992-05-03 to 2026-09-01 |
| 51 clubs, each with at least one PL season | **PASS** | 51 clubs |
| no transfer counted outside its club's PL seasons | **PASS** | 3677 ledger rows frozen (club not in the PL) |
| PL-to-PL deals net to zero (spend - income of PL clubs = net spend with non-PL clubs) | **PASS** | spend £28,529,156,326 − income £15,030,779,580 = £13,498,376,746; net with non-PL clubs £13,498,376,746 |
| no fee without a source row | **PASS** | 3123 fee-bearing transfers |
| no Transfermarkt figure or URL anywhere | **PASS** | none found |
| quotes under 25 words | **PASS** | 14917 evidence rows |
| every conversion has a rate row | **PASS** | 30 conversions |
| month-end series consistent with the ledger | **PASS** | 413 month ends × 51 clubs |
| Bank of England Jan 1992 monthly averages equal Cowork's V-04 reading | **PASS** | 7 of 7 series compared |
| ECB GBP/EUR 1999-01 equals Cowork's V-06 reading (0.7029125) | **PASS** | 333 months |
| CPI base month recorded | **PASS** | D7BT 2026-08 = 143.6 (September 2026 not yet published at build time) |

Plus the private cross-checks in `data/rtt-101/CHECKS.md` (membership equals research file part03b; its differences are the two known flag errors and points deductions it ignores).

## 3. Leaders over time (UNVERIFIED preview)

First place at each month end, nominal cumulative net spend; a change is listed when first place changes hands.

| From month end | Leader | Value then |
|---|---|---|
| 1992-05-31 | Arsenal | £0.0m |
| 1992-07-31 | Blackburn Rovers | £4.6m |
| 1995-07-31 | Liverpool | £17.8m |
| 1996-03-31 | Blackburn Rovers | £22.4m |
| 1996-07-31 | Newcastle United | £26.5m |
| 1997-05-31 | Everton | £29.1m |
| 1998-06-30 | Newcastle United | £30.8m |
| 2000-06-30 | Chelsea | £56.3m |
| 2000-07-31 | Newcastle United | £53.6m |
| 2000-10-31 | Chelsea | £52.0m |
| 2000-11-30 | Newcastle United | £47.6m |
| 2000-12-31 | Chelsea | £47.8m |
| 2001-07-31 | Manchester United | £81.2m |
| 2001-12-31 | Newcastle United | £60.1m |
| 2002-01-31 | Manchester United | £61.3m |
| 2002-02-28 | Newcastle United | £64.7m |
| 2002-07-31 | Manchester United | £88.9m |
| 2003-07-31 | Chelsea | £89.7m |
| 2015-08-31 | Manchester City | £575.2m |
| 2016-07-31 | Chelsea | £621.1m |
| 2016-08-31 | Manchester City | £728.5m |
| 2022-09-30 | Manchester United | £1.27bn |
| 2023-01-31 | Chelsea | £1.37bn |
| 2023-07-31 | Manchester United | £1.36bn |
| 2023-08-31 | Chelsea | £1.54bn |
| 2024-09-30 | Manchester United | £1.62bn |

## 4. Top 12 at key dates (UNVERIFIED preview)

**1993-05-31:** 1. Blackburn Rovers £6.1m; 2. Aston Villa £2.5m; 3. Liverpool £0.9m; 4. Leeds United £0.8m; 5. Oldham Athletic £0.8m; 6. Chelsea £0.6m; 7. Ipswich Town £0.5m; 8. Manchester United £0.1m; 9. Queens Park Rangers £0.1m; 10. Crystal Palace £0.0m (out of the PL); 11. Everton £0.0m; 12. Manchester City £0.0m

**1997-05-31:** 1. Everton £29.1m; 2. Newcastle United £25.5m; 3. Aston Villa £18.6m; 4. Liverpool £14.4m; 5. Chelsea £14.1m; 6. Coventry City £11.7m; 7. Leicester City £8.3m; 8. Leeds United £8.1m; 9. Blackburn Rovers £7.5m; 10. Sheffield Wednesday £6.7m; 11. Nottingham Forest £6.6m (out of the PL); 12. Wimbledon £5.6m

**2002-05-31:** 1. Newcastle United £64.5m; 2. Manchester United £61.6m; 3. Chelsea £53.7m; 4. Leeds United £47.0m; 5. Aston Villa £46.1m; 6. Tottenham Hotspur £42.8m; 7. Blackburn Rovers £40.1m; 8. Middlesbrough £36.6m; 9. Liverpool £35.5m; 10. Fulham £35.3m; 11. Charlton Athletic £23.4m; 12. Sunderland £19.9m

**2005-05-31:** 1. Chelsea £253.3m; 2. Manchester United £125.6m; 3. Newcastle United £82.2m; 4. Middlesbrough £72.5m; 5. Tottenham Hotspur £69.8m; 6. Liverpool £68.0m; 7. Aston Villa £49.6m; 8. Sunderland £40.1m; 9. Manchester City £39.5m; 10. Blackburn Rovers £32.5m; 11. Birmingham City £25.1m; 12. Fulham £21.6m

**2008-08-31:** 1. Chelsea £347.6m; 2. Manchester United £172.6m; 3. Liverpool £122.8m; 4. Tottenham Hotspur £115.7m; 5. Aston Villa £111.4m; 6. Middlesbrough £107.2m; 7. Newcastle United £100.5m; 8. Sunderland £81.3m; 9. Manchester City £66.4m; 10. Fulham £47.4m; 11. West Ham United £44.1m; 12. Birmingham City £40.1m (out of the PL)

**2012-05-31:** 1. Chelsea £460.0m; 2. Manchester City £327.4m; 3. Manchester United £136.3m; 4. Tottenham Hotspur £129.7m; 5. Aston Villa £117.2m; 6. Middlesbrough £107.1m (out of the PL); 7. Sunderland £104.0m; 8. Liverpool £74.2m; 9. Birmingham City £74.2m (out of the PL); 10. Newcastle United £73.5m; 11. Everton £49.4m; 12. Fulham £48.6m

**2016-08-31:** 1. Manchester City £728.5m; 2. Chelsea £663.6m; 3. Manchester United £553.2m; 4. Liverpool £189.1m; 5. Sunderland £168.8m; 6. Arsenal £130.0m; 7. Middlesbrough £124.9m; 8. West Ham United £117.5m; 9. West Bromwich Albion £104.7m; 10. Aston Villa £103.4m (out of the PL); 11. Stoke City £97.7m; 12. Newcastle United £92.7m (out of the PL)

**2020-10-31:** 1. Manchester City £1.10bn; 2. Manchester United £884.7m; 3. Chelsea £807.7m; 4. Everton £402.6m; 5. Liverpool £344.8m; 6. Arsenal £342.6m; 7. Aston Villa £270.2m; 8. Tottenham Hotspur £225.7m; 9. West Ham United £220.0m; 10. Newcastle United £172.4m; 11. Sunderland £168.8m (out of the PL); 12. West Bromwich Albion £168.1m

**2023-09-30:** 1. Chelsea £1.57bn; 2. Manchester United £1.51bn; 3. Manchester City £1.21bn; 4. Arsenal £736.0m; 5. Liverpool £539.4m; 6. Newcastle United £508.7m; 7. Tottenham Hotspur £430.0m; 8. West Ham United £426.4m; 9. Aston Villa £348.8m; 10. Everton £325.8m; 11. AFC Bournemouth £230.6m; 12. Fulham £192.8m

**2026-09-01:** 1. Manchester United £1.92bn; 2. Chelsea £1.63bn; 3. Manchester City £1.51bn; 4. Arsenal £1.17bn; 5. Liverpool £1.07bn; 6. Tottenham Hotspur £963.0m; 7. Newcastle United £591.1m; 8. West Ham United £580.0m (out of the PL); 9. Fulham £385.5m; 10. Everton £371.5m; 11. Sunderland £310.0m; 12. Nottingham Forest £287.4m

## 5. Coverage by era

Counts are club-sides (a PL-to-PL deal counts once for each club).

| Era | Transfers found | With a fee | Fee grade A/B | Fee VERIFIED | Undisclosed, no figure | Fee not found |
|---|---|---|---|---|---|---|
| 1992-2002 (no window lists) | 1,948 | 1,269 | 203 | 242 | 28 | 95 |
| 2002-2007 | 1,165 | 454 | 69 | 72 | 145 | 13 |
| 2007-2012 | 2,994 | 414 | 134 | 130 | 688 | 9 |
| 2012-2017 | 3,072 | 521 | 139 | 122 | 577 | 12 |
| 2017-2022 | 2,133 | 418 | 221 | 212 | 497 | 21 |
| 2022-2026 | 3,070 | 796 | 601 | 597 | 540 | 14 |

What the eras mean:
- **1992–2002:** no Wikipedia window lists exist (V-10). The finding list is the clubs' season pages (200 of 210 fetched; the ten Leeds United pages are titled "Leeds United A.F.C." and were not fetched in this round) plus the research leads. About a quarter of those pages have no transfer table at all, so this era is the least complete. Transfermarkt was not used (route A says to consult it only to spot omissions; nothing from it is stored).
- **2002–2007:** the early Wikipedia window lists are short (for example summer 2004 has 83 rows involving these clubs, summer 2005 has 76), so many smaller deals are missing.
- **From 2007:** the lists are full (500–800 rows a window), but most fees there are Wikipedia figures (grade C pointers) until the cited source is checked.

## 6. Biggest open conflicts

Transfers whose sources give different fees (never averaged; the canonical fee is the highest grade, then the earliest report). The ones marked for Luke are Tier 1 with a same-grade gap over 10% and £1m (brief §7).

| Player | From → To | Date | Fee used | Range | Tier | For Luke |
|---|---|---|---|---|---|---|
| Eberechi Eze | Crystal Palace → Arsenal | 2025-08-23 | £67.5m (B) | £6.0m–£67.5m | 1 | yes |
| Erling Haaland | Borussia Dortmund → Manchester City | 2022-07-01 | £51.0m (B) | £2.5m–£52.0m | 1 |  |
| Philippe Coutinho | Liverpool → Barcelona | 2018-01-08 | £142.0m (B) | £105.0m–£142.0m | 1 | yes |
| Anthony Martial | Monaco → Manchester United | 2015-09-01 | £36.0m (B) | £8.5m–£36.0m | 1 | yes |
| Mykhailo Mudryk | Shakhtar Donetsk → Chelsea | 2023-01-15 | £88.5m (B) | £61.7m–£89.0m | 1 | yes |
| Romelu Lukaku | Everton → Manchester United | 2017-07-10 | £100.0m (B) | £75.0m–£100.0m | 1 | yes |
| Carlos Tevez | Media Sports Investments → Manchester City | 2009-07-14 | £25.0m (B) | £25.0m–£47.0m | 1 | yes |
| Darwin Núñez | Benfica → Liverpool | 2022-06-14 | £64.0m (B) | £64.0m–£85.0m | 1 | yes |
| Cesc Fàbregas | Arsenal → Barcelona | 2011-08-15 | £12.8m (B) | £12.8m–£30.0m | 1 |  |
| Julián Álvarez | Manchester City → Atlético Madrid | 2024-08-12 | £81.5m (B) | £64.4m–£81.5m | 1 |  |
| Florian Wirtz | Bayer Leverkusen → Liverpool | 2025-06-20 | £116.0m (B) | £100.0m–£116.5m | 1 | yes |
| Michael Olise | Crystal Palace → Bayern Munich | 2024-07-07 | £50.0m (B) | £45.0m–£60.0m | 1 | yes |
| Jean Michaël Seri | Nice → Fulham | 2018-07-12 | £25.0m (B) | £10.6m–£25.0m | 1 | yes |
| Andriy Shevchenko | A.C. Milan → Chelsea | 2006-05-31 | £30.9m (B) | £24.7m–£39.0m | 1 | yes |
| Rodri}} | Manchester City → Barcelona | 2026-08-18 | £65.4m (B) | £51.3m–£65.4m | 1 | yes |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £72.0m (B) | £62.0m–£75.8m | 1 | yes |
| José Antonio Reyes | Sevilla → Arsenal | 2004-01-27 | £24.2m (B) | £10.5m–£24.2m | 1 |  |
| Harry Kane | Tottenham Hotspur → Bayern Munich | 2023-08-12 | £100.0m (B) | £86.4m–£100.0m | 1 | yes |
| Anderson | F.C. Porto → Manchester United | 2007-07-02 | £20.4m (B) | £17.0m–£30.0m | 1 | yes |
| Nani | Sporting → Manchester United | 2007-07-02 | £17.3m (B) | £17.3m–£30.0m | 1 | yes |
| Antony | Ajax → Manchester United | 2022-09-01 | £81.3m (B) | £70.1m–£81.9m | 1 |  |
| Luis Suárez | Liverpool → Barcelona | 2014-07-16 | £65.0m (B) | £64.0m–£75.0m | 1 | yes |
| James Milner | Aston Villa → Manchester City | 2010-08-18 | £26.0m (B) | £15.0m–£26.0m | 1 | yes |
| Eliaquim Mangala | Porto → Manchester City | 2014-08-11 | £32.0m (B) | £32.0m–£42.0m | 1 |  |
| Dominic Solanke | AFC Bournemouth → Tottenham Hotspur | 2024-08-10 | £55.0m (B) | £55.0m–£65.0m | 1 | yes |

70 conflicts are for Luke in total (`conflicts.csv`, column `for_luke`).

## 7. League-wide window totals: our sums against published totals

Our sums are **fees only, Premier League clubs only, from this preview** (gross = fees paid by PL clubs; net = fees paid to non-PL clubs minus fees received from them). Published totals are research leads (UNVERIFIED). The Premier League's own figures (grade A) are the best comparison; the press figures are mostly Deloitte estimates. **Gaps are expected and are not forced to match.**

| Window | Our gross | Our net | Premier League gross (A) | PL net (A) | Press gross / net (B, first listed) |
|---|---|---|---|---|---|
| January 2003 | £36.8m | £14.2m | — | — | £35m / NOT FOUND (The Independent) |
| summer 2003 | £212.5m | £120.4m | — | — | £215m / NOT FOUND (The Independent) |
| summer 2005 | £201.3m | £81.4m | — | — | £235m / NOT FOUND (The Independent) |
| summer 2006 | £258.4m | £134.5m | — | — | £300m / NOT FOUND (BBC News) |
| summer 2008 | £333.3m | £155.3m | — | — | 500 million pounds / NOT FOUND (Reuters (via Rediff)) |
| January 2009 | £92.9m | £6.3m | — | — | about £160m / NOT FOUND (The Guardian (report) |
| summer 2009 | £198.7m | −£24.4m | — | — | £460.4m / NOT FOUND (The Guardian) |
| January 2010 | £29.5m | £9.9m | £36.0m | £7.0m | £30m / NOT FOUND (The Guardian (report) |
| summer 2010 | £179.0m | £100.6m | — | — | around £350million / NOT FOUND (Sky Sports (reportin) |
| January 2011 | £192.9m | £72.4m | £209.3m | £77.3m | £225m / NOT FOUND (The Guardian (table ) |
| summer 2011 | £187.3m | £103.1m | — | — | NOT FOUND / £194m (The Guardian) |
| January 2012 | £43.4m | £7.9m | £67.4m | £24.5m | — |
| summer 2012 | £307.9m | £130.2m | — | — | around £490m / NOT FOUND (Sky News (reporting ) |
| January 2013 | £80.6m | £44.6m | £123.4m | £72.5m | £120m / £70m (Press Association (v) |
| summer 2013 | £550.3m | £344.9m | — | — | £630m / NOT FOUND (BBC Sport) |
| January 2014 | £106.8m | £36.0m | £128.8m | £26.9m | — |
| summer 2014 | £633.9m | £266.9m | £809.6m | £386.5m | £835m / £410m (Press Association (v) |
| January 2015 | £96.3m | £32.5m | £118.2m | £36.4m | £130million / around £40million (The Independent (Age) |
| summer 2015 | £719.6m | £352.6m | £858.6m | £432.6m | £870m / £460m (BBC Sport) |
| January 2016 | £96.1m | −£38.6m | £177.5m | £108.9m | £175m / NOT FOUND (BBC Sport) |
| summer 2016 | £1.11bn | £736.4m | £1.12bn | £635.6m | £1.165bn / NOT FOUND (Sky Sports (reportin) |
| January 2017 | £140.5m | −£64.2m | £236.7m | −£4.0m | £215m / net £40m profit (Sky Sports) |
| summer 2017 | £1.42bn | £673.4m | £1.41bn | £665.0m | £1.43bn / NOT FOUND (Sky News) |
| January 2018 | £346.2m | £61.2m | £419.5m | £147.6m | £430m / NOT FOUND (BBC Sport / Deloitte) |
| summer 2018 | £978.4m | £774.4m | — | — | £1.23bn / £865m (Sky News) |
| January 2019 | £130.6m | £75.5m | — | — | £180m / NOT FOUND (Sky Sports) |
| summer 2019 | £1.05bn | £320.4m | — | — | £1.41billion / £625m (PA, syndicated by Ex) |
| January 2020 | £142.3m | £142.3m | — | — | £230m / £165m (BBC Sport) |
| summer 2020 | £1.05bn | £673.4m | — | — | £1.24bn / £813million (PA (Tom White), synd) |
| January 2021 | £46.5m | £24.8m | — | — | £70m / NOT FOUND (Sky News) |
| summer 2021 | £787.2m | £417.9m | — | — | £1.1billion / £560m (PA, syndicated by Fo) |
| January 2022 | £188.0m | £79.1m | — | — | £295m / £180m (Sky News) |
| summer 2022 | £1.80bn | £1.05bn | — | — | Estimates from Deloitte’s spor / NOT FOUND (The Guardian / Deloi) |
| January 2023 | £847.5m | £723.2m | — | — | around £780.1m / £675m (Sky Sports) |
| summer 2023 | £2.29bn | £1.07bn | — | — | £2.44bn / £1.07bn (Sky Sports) |
| January 2024 | £78.1m | £67.3m | — | — | £96.2m / NOT FOUND (Sky Sports) |
| summer 2024 | £1.84bn | £575.5m | — | — | £2.08bn / £627.4m (Sky Sports) |
| January 2025 | £336.9m | £207.0m | — | — | around £370m / NOT FOUND (BBC Sport) |
| summer 2025 | £3.12bn | £1.43bn | — | — | surpassed £3bn; £3.087bn / NOT FOUND (BBC Sport) |
| January 2026 | £459.9m | £224.1m | — | — | £397m / NOT FOUND (BBC Sport) |
| summer 2026 | £3.22bn | £1.15bn | — | — | around £3.46 billion / NOT FOUND (Reuters, syndicated ) |

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

1. **Tier 1 is too big as worded (DEC-253).** 1,892 transfers are Tier 1, mostly because of the "changes the top-12 order" test. *Recommendation:* keep £20m+, records and disputed fees, and narrow the order test to "changes the leader, or who is in the top 12, at any month end"; the rest get Tier 2's scripted check.
2. **Undisclosed fees count £0 (DEC-237 (g)).** 2,212 transfers have no reported figure. *Recommendation:* keep the rule, say on screen "Undisclosed fees not included", and give each club's undisclosed count in the description.
3. **The early years are the least complete (1992–2007).** *Recommendation:* in phase 2, Claude in Cowork uses Transfermarkt in your Chrome only as a finding list (route A, nothing stored) to spot missing 1992–2007 deals involving the bigger fees, and takes each fee from a press or club source.
4. **Relegated clubs keep their frozen bar and their rank** (contract §1; e.g. a relegated club can sit 8th at the freeze). *Recommendation:* keep them in the ranking; how a frozen bar looks is a design question for the pilot (DEC-069).
5. **Start of the race.** At 31 May 1992 every bar is £0 (the leader that month is only a tie-break). *Recommendation:* the film starts at the first month end with a fee (July 1992); the data stay as they are.
6. **Same-grade fee disagreements on Tier 1 transfers:** 70 are listed in `conflicts.csv` (column `for_luke`). *Recommendation:* phase 2 settles each at source; the ones still open after that come back to you as a short list.
7. **Claude's working choices** DEC-247 (finding list), DEC-248 (tiers), DEC-249 (board size later), DEC-250 (build details) and DEC-254 (how the scripted check marks a fee VERIFIED, and publisher grades). *Recommendation:* confirm them.
8. **Phase 2 first batch.** *Recommendation:* verify the Tier 1 fees of the clubs that lead or reach the top 3 (Chelsea, Manchester United, Manchester City, Arsenal, Liverpool, Newcastle, Blackburn, Everton) first, in batches of 50 (`tier1_list.csv`, column `batch`).
