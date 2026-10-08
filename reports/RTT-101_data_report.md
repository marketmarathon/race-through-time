# RTT-101 Premier League net transfer spend — data report, phase 1 (IQ-15, 7 Oct 2026)

**Status: UNVERIFIED preview. Not for screen.** Only figures marked VERIFIED may ever be shown, and phase 2 (verification of Tier 1 at source, in batches) comes before any design work. Rules: `reference/metric_contract_RTT-101.md`; decisions DEC-235 to DEC-250 (and the findings recorded with this build).

Rebuild: `python3 scripts/build_rtt101_dataset.py && python3 scripts/rtt101_report.py` (deterministic; the private cross-checks need the private folder: `python3 scripts/rtt101_private_crosschecks.py <private research folder>` first).

## 1. What was built

- **13,013 transfer events** that involve a club in the Premier League that season (1992-93 to the freeze, 1 Sep 2026), of which **3,282 carry a fee** above £0. The rest are loans without a fee (5,331), free transfers (2,030), undisclosed fees with no figure, counted £0 (2,201), and fees not found (131).
- Fee status: **VERIFIED 1,801**, UNVERIFIED 1,481. Grade of the fee used: A 18, B 1,779, C (Wikipedia pointer only) 1,485, D 0.
- Tiers (DEC-248): Tier 1 **2,041**, Tier 2 663, Tier 3 595 (5% sample: 30).
  Tier 1 reasons (a transfer can have several): removal changes the leader or the top 12 1,122; fee >= £20m 548; club or British record (research lead) 526; alternative fee version changes the leader or the top 12 14; disputed fee (research section C) 10.
- 17,551 evidence rows in `fee_evidence.csv`; 3,361 sources in `sources.csv`; 579 transfers with more than one fee version (`conflicts.csv`).
- **Scripted source check** (GitHub runner, 5,080 cited pages): VERIFIED 4,443; page fetched but figure not found near the player's name 559; blocked or gone 78.
  Tier 2 result: 320 of 663 Tier 2 fees VERIFIED by the scripted check.
  Tier 3 sample: 6 of 30 VERIFIED; most Tier 3 rows have no fetchable citation (error rate cannot be published yet: phase 2).

## 2. Checks

| Check | Result | Detail |
|---|---|---|
| 22 clubs per season 1992-95, 20 after (706 club-seasons) | **PASS** | 706 club-seasons in 35 seasons |
| every season has an attribution window | **PASS** | 1992-05-03 to 2026-09-01 |
| 51 clubs, each with at least one PL season | **PASS** | 51 clubs |
| no transfer counted outside its club's PL seasons | **PASS** | 3734 ledger rows frozen (club not in the PL) |
| PL-to-PL deals net to zero (spend - income of PL clubs = net spend with non-PL clubs) | **PASS** | spend £27,737,831,834 − income £14,298,520,202 = £13,439,311,632; net with non-PL clubs £13,439,311,632 |
| no fee without a source row | **PASS** | 3282 fee-bearing transfers |
| no Transfermarkt figure or URL anywhere | **PASS** | none found |
| quotes under 25 words | **PASS** | 17551 evidence rows |
| every conversion has a rate row | **PASS** | 18 conversions |
| month-end series consistent with the ledger | **PASS** | 413 month ends × 51 clubs |
| Bank of England Jan 1992 monthly averages equal Cowork's V-04 reading | **PASS** | 7 of 7 series compared |
| ECB GBP/EUR 1999-01 equals Cowork's V-06 reading (0.7029125) | **PASS** | 333 months |
| no amount rejection silently removes a research lead that quotes the player with that figure | **PASS** | all such rejections were weighed against the lead |
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
| 1995-07-31 | Liverpool | £23.3m |
| 1996-07-31 | Newcastle United | £38.6m |
| 1997-08-31 | Liverpool | £32.8m |
| 1998-02-28 | Newcastle United | £34.5m |
| 1999-07-31 | Liverpool | £56.3m |
| 2001-07-31 | Manchester United | £82.9m |
| 2001-08-31 | Liverpool | £80.9m |
| 2001-11-30 | Leeds United | £82.7m |
| 2002-06-30 | Liverpool | £84.7m |
| 2002-07-31 | Manchester United | £91.2m |
| 2003-03-31 | Newcastle United | £92.7m |
| 2003-07-31 | Chelsea | £114.5m |
| 2015-08-31 | Manchester City | £626.4m |
| 2016-07-31 | Chelsea | £661.1m |
| 2016-08-31 | Manchester City | £788.0m |
| 2022-08-31 | Chelsea | £1.20bn |
| 2026-09-01 | Manchester United | £1.74bn |

## 4. Top 12 at key dates (UNVERIFIED preview)

**1993-05-31:** 1. Blackburn Rovers £5.5m; 2. Aston Villa £2.5m; 3. Manchester City £2.5m; 4. Sheffield Wednesday £2.0m; 5. Leeds United £1.9m; 6. Liverpool £0.9m; 7. Oldham Athletic £0.7m; 8. Chelsea £0.7m; 9. Ipswich Town £0.6m; 10. Manchester United £0.4m; 11. Arsenal £0.3m; 12. Newcastle United £0.0m

**1997-05-31:** 1. Newcastle United £37.8m; 2. Everton £20.9m; 3. Liverpool £20.7m; 4. Aston Villa £19.8m; 5. Middlesbrough £16.9m (out of the PL); 6. Chelsea £16.3m; 7. Arsenal £15.0m; 8. Coventry City £14.4m; 9. Leeds United £13.8m; 10. Sheffield Wednesday £12.6m; 11. Blackburn Rovers £9.7m; 12. Leicester City £8.9m

**2002-05-31:** 1. Leeds United £82.7m; 2. Chelsea £78.5m; 3. Liverpool £74.7m; 4. Newcastle United £69.2m; 5. Manchester United £63.2m; 6. Tottenham Hotspur £52.3m; 7. Middlesbrough £48.2m; 8. Aston Villa £47.7m; 9. Blackburn Rovers £44.3m; 10. Fulham £37.0m; 11. Arsenal £30.8m; 12. Sheffield Wednesday £25.5m (out of the PL)

**2005-05-31:** 1. Chelsea £285.9m; 2. Manchester United £120.2m; 3. Liverpool £105.0m; 4. Newcastle United £87.9m; 5. Tottenham Hotspur £79.8m; 6. Middlesbrough £78.4m; 7. Aston Villa £54.6m; 8. Manchester City £49.0m; 9. Sunderland £39.2m; 10. Blackburn Rovers £38.1m; 11. Arsenal £35.6m; 12. Birmingham City £28.9m

**2008-08-31:** 1. Chelsea £364.6m; 2. Liverpool £176.4m; 3. Manchester United £161.6m; 4. Tottenham Hotspur £124.2m; 5. Middlesbrough £121.8m; 6. Aston Villa £116.5m; 7. Newcastle United £106.4m; 8. Sunderland £79.4m; 9. Manchester City £79.2m; 10. Birmingham City £46.9m (out of the PL); 11. Fulham £46.6m; 12. Everton £46.1m

**2012-05-31:** 1. Chelsea £476.8m; 2. Manchester City £364.3m; 3. Liverpool £161.7m; 4. Tottenham Hotspur £131.5m; 5. Manchester United £123.6m; 6. Aston Villa £123.5m; 7. Middlesbrough £121.8m (out of the PL); 8. Sunderland £94.1m; 9. Birmingham City £75.4m (out of the PL); 10. Newcastle United £73.4m; 11. Everton £64.5m; 12. Stoke City £58.4m

**2016-08-31:** 1. Manchester City £788.0m; 2. Chelsea £707.6m; 3. Manchester United £547.2m; 4. Liverpool £281.7m; 5. Arsenal £158.5m; 6. Tottenham Hotspur £156.4m; 7. Sunderland £145.3m; 8. Middlesbrough £139.6m; 9. West Ham United £119.1m; 10. Aston Villa £118.7m (out of the PL); 11. Stoke City £112.7m; 12. Everton £96.1m

**2020-10-31:** 1. Manchester City £1.12bn; 2. Chelsea £986.0m; 3. Manchester United £849.6m; 4. Liverpool £415.2m; 5. Everton £392.7m; 6. Arsenal £362.9m; 7. Tottenham Hotspur £304.4m; 8. Aston Villa £285.4m; 9. West Ham United £235.6m; 10. Newcastle United £192.3m; 11. West Bromwich Albion £160.7m; 12. Fulham £148.8m

**2023-09-30:** 1. Chelsea £1.68bn; 2. Manchester United £1.30bn; 3. Manchester City £1.20bn; 4. Arsenal £748.5m; 5. Liverpool £624.5m; 6. Newcastle United £553.6m; 7. Tottenham Hotspur £512.3m; 8. West Ham United £425.5m; 9. Aston Villa £379.0m; 10. Everton £367.9m; 11. AFC Bournemouth £242.6m; 12. Fulham £183.5m

**2026-09-01:** 1. Manchester United £1.74bn; 2. Chelsea £1.67bn; 3. Manchester City £1.62bn; 4. Arsenal £1.18bn; 5. Liverpool £983.0m; 6. Tottenham Hotspur £960.3m; 7. Newcastle United £674.7m; 8. West Ham United £539.1m (out of the PL); 9. Everton £410.6m; 10. Fulham £334.3m; 11. Sunderland £305.7m; 12. Aston Villa £269.3m

## 5. Coverage by era

Counts are club-sides (a PL-to-PL deal counts once for each club).

| Era | Transfers found | With a fee | Fee grade A/B | Fee VERIFIED | Undisclosed, no figure | Fee not found |
|---|---|---|---|---|---|---|
| 1992-2002 (no window lists) | 2,178 | 1,435 | 929 | 915 | 52 | 92 |
| 2002-2007 | 1,179 | 473 | 92 | 177 | 150 | 13 |
| 2007-2012 | 2,972 | 419 | 179 | 165 | 671 | 7 |
| 2012-2017 | 3,052 | 523 | 269 | 247 | 568 | 10 |
| 2017-2022 | 2,120 | 418 | 272 | 256 | 487 | 17 |
| 2022-2026 | 3,091 | 779 | 577 | 553 | 533 | 6 |

What the eras mean:
- **1992–2002:** no Wikipedia window lists exist (V-10). The finding list is the clubs' season pages (200 of 210 fetched; the ten Leeds United pages are titled "Leeds United A.F.C." and were not fetched in this round) plus the research leads. About a quarter of those pages have no transfer table at all, so this era is the least complete. Transfermarkt was not used (route A says to consult it only to spot omissions; nothing from it is stored).
- **2002–2007:** the early Wikipedia window lists are short (for example summer 2004 has 83 rows involving these clubs, summer 2005 has 76), so many smaller deals are missing.
- **From 2007:** the lists are full (500–800 rows a window), but most fees there are Wikipedia figures (grade C pointers) until the cited source is checked.

## 6. Biggest open conflicts

Transfers whose sources give different fees (never averaged; the canonical fee is the highest grade, then the earliest report). The ones marked for Luke are Tier 1 with a same-grade gap over 10% and £1m (brief §7).

| Player | From → To | Date | Fee used | Range | Tier | For Luke |
|---|---|---|---|---|---|---|
| Carlos Tevez | Media Sports Investments → Manchester City | 2009-07-14 | £25.0m (B) | £25.0m–£45.0m | 1 | yes |
| Cesc Fàbregas | Arsenal → Barcelona | 2011-08-15 | £25.4m (B) | £12.8m–£30.0m | 1 | yes |
| José Antonio Reyes | Sevilla → Arsenal | 2004-01-27 | £7.1m (B) | £7.1m–£24.2m | 1 |  |
| Julián Álvarez | Manchester City → Atlético Madrid | 2024-08-12 | £64.4m (B) | £64.4m–£81.0m | 1 | yes |
| Michael Olise | Crystal Palace → Bayern Munich | 2024-07-07 | £50.0m (B) | £45.0m–£60.0m | 1 |  |
| Lucas Paquetá | Lyon → West Ham United | 2022-08-29 | £51.0m (B) | £36.5m–£51.0m | 1 |  |
| Andriy Shevchenko | A.C. Milan → Chelsea | 2006-05-31 | £30.8m (B) | £24.7m–£39.0m | 1 |  |
| Rodri | Manchester City → Barcelona | 2026-08-18 | £51.3m (B) | £51.3m–£65.4m | 1 | yes |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £75.8m (B) | £62.0m–£75.8m | 1 | yes |
| Harry Kane | Tottenham Hotspur → Bayern Munich | 2023-08-12 | £86.4m (B) | £86.4m–£100.0m | 1 |  |
| Eliaquim Mangala | Porto → Manchester City | 2014-08-11 | £32.0m (B) | £32.0m–£42.0m | 1 |  |
| Richarlison | Everton → Tottenham Hotspur | 2022-07-01 | £50.0m (B) | £50.0m–£60.0m | 1 |  |
| David Luiz | Chelsea → Paris Saint-Germain | 2014-06-13 | £50.0m (B) | £40.0m–£50.0m | 1 | yes |
| Wayne Rooney | Everton → Manchester United | 2004-08-31 | £20.0m (B) | £20.0m–£30.0m | 1 |  |
| Casemiro | Real Madrid → Manchester United | 2022-08-22 | £60.0m (B) | £50.7m–£60.0m | 1 |  |
| Martín Zubimendi | Real Sociedad → Arsenal | 2025-07-06 | £60.0m (B) | £51.0m–£60.0m | 1 | yes |
| Gareth Bale | Tottenham Hotspur → Real Madrid | 2013-09-01 | £85.3m (B) | £76.6m–£85.3m | 1 | yes |
| Roberto Firmino | TSG Hoffenheim → Liverpool | 2015-06-24 | £21.3m (B) | £21.0m–£29.5m | 1 | yes |
| Viktor Gyökeres | Sporting CP → Arsenal | 2025-07-26 | £55.1m (B) | £55.0m–£63.5m | 1 |  |
| Álvaro Morata | Chelsea → Atlético Madrid | 2020-07-01 | £58.8m (B) | £50.4m–£58.8m | 1 |  |
| James Milner | Aston Villa → Manchester City | 2010-08-18 | £26.0m (B) | £18.0m–£26.0m | 1 |  |
| Fernando Torres | Atlético Madrid → Liverpool | 2007-07-04 | £26.5m (B) | £18.5m–£26.5m | 1 |  |
| Diego Costa | Chelsea → Atlético Madrid | 2017-09-21 | £57.0m (B) | £50.0m–£58.0m | 1 |  |
| Michael Turner | Hull City → Sunderland | 2009-08-31 | £12.0m (B) | £4.0m–£12.0m | 1 | yes |
| Rasmus Højlund | Atalanta → Manchester United | 2023-08-05 | £64.0m (B) | £64.0m–£72.0m | 1 |  |

39 conflicts are for Luke in total (`conflicts.csv`, column `for_luke`).

## 7. League-wide window totals: our sums against published totals

Our sums are **fees only, Premier League clubs only, from this preview** (gross = fees paid by PL clubs; net = fees paid to non-PL clubs minus fees received from them). Published totals are research leads (UNVERIFIED). The Premier League's own figures (grade A) are the best comparison; the press figures are mostly Deloitte estimates. **Gaps are expected and are not forced to match.**

| Window | Our gross | Our net | Premier League gross (A) | PL net (A) | Press gross / net (B, first listed) |
|---|---|---|---|---|---|
| January 2003 | £39.8m | £17.2m | — | — | £35m / NOT FOUND (The Independent) |
| summer 2003 | £204.9m | £119.2m | — | — | £215m / NOT FOUND (The Independent) |
| summer 2005 | £229.4m | £112.3m | — | — | £235m / NOT FOUND (The Independent) |
| summer 2006 | £240.9m | £122.0m | — | — | £300m / NOT FOUND (BBC News) |
| summer 2008 | £338.6m | £162.6m | — | — | 500 million pounds / NOT FOUND (Reuters (via Rediff)) |
| January 2009 | £92.9m | £6.3m | — | — | about £160m / NOT FOUND (The Guardian (report) |
| summer 2009 | £239.1m | £7.5m | — | — | £460.4m / NOT FOUND (The Guardian) |
| January 2010 | £26.0m | £9.9m | £36.0m | £7.0m | £30m / NOT FOUND (The Guardian (report) |
| summer 2010 | £181.8m | £108.4m | — | — | around £350million / NOT FOUND (Sky Sports (reportin) |
| January 2011 | £195.4m | £76.1m | £209.3m | £77.3m | £225m / NOT FOUND (The Guardian (table ) |
| summer 2011 | £205.3m | £96.5m | — | — | NOT FOUND / £194m (The Guardian) |
| January 2012 | £42.7m | £0.7m | £67.4m | £24.5m | — |
| summer 2012 | £325.9m | £147.7m | — | — | around £490m / NOT FOUND (Sky News (reporting ) |
| January 2013 | £80.6m | £44.6m | £123.4m | £72.5m | £120m / £70m (Press Association (v) |
| summer 2013 | £559.0m | £353.2m | — | — | £630m / NOT FOUND (BBC Sport) |
| January 2014 | £118.8m | £36.0m | £128.8m | £26.9m | — |
| summer 2014 | £638.9m | £292.6m | £809.6m | £386.5m | £835m / £410m (Press Association (v) |
| January 2015 | £90.6m | £29.8m | £118.2m | £36.4m | £130million / around £40million (The Independent (Age) |
| summer 2015 | £735.5m | £373.5m | £858.6m | £432.6m | £870m / £460m (BBC Sport) |
| January 2016 | £103.6m | £43.6m | £177.5m | £108.9m | £175m / NOT FOUND (BBC Sport) |
| summer 2016 | £1.08bn | £713.0m | £1.12bn | £635.6m | £1.165bn / NOT FOUND (Sky Sports (reportin) |
| January 2017 | £140.5m | −£64.2m | £236.7m | −£4.0m | £215m / net £40m profit (Sky Sports) |
| summer 2017 | £1.32bn | £643.1m | £1.41bn | £665.0m | £1.43bn / NOT FOUND (Sky News) |
| January 2018 | £346.2m | £98.2m | £419.5m | £147.6m | £430m / NOT FOUND (BBC Sport / Deloitte) |
| summer 2018 | £907.9m | £706.9m | — | — | £1.23bn / £865m (Sky News) |
| January 2019 | £109.6m | £54.5m | — | — | £180m / NOT FOUND (Sky Sports) |
| summer 2019 | £1.07bn | £483.9m | — | — | £1.41billion / £625m (PA, syndicated by Ex) |
| January 2020 | £121.0m | £119.7m | — | — | £230m / £165m (BBC Sport) |
| summer 2020 | £1.07bn | £688.1m | — | — | £1.24bn / £813million (PA (Tom White), synd) |
| January 2021 | £45.0m | £24.8m | — | — | £70m / NOT FOUND (Sky News) |
| summer 2021 | £829.4m | £435.1m | — | — | £1.1billion / £560m (PA, syndicated by Fo) |
| January 2022 | £188.0m | £78.7m | — | — | £295m / £180m (Sky News) |
| summer 2022 | £1.73bn | £986.3m | — | — | Estimates from Deloitte’s spor / NOT FOUND (The Guardian / Deloi) |
| January 2023 | £654.8m | £570.5m | — | — | around £780.1m / £675m (Sky Sports) |
| summer 2023 | £2.15bn | £990.9m | — | — | £2.44bn / £1.07bn (Sky Sports) |
| January 2024 | £86.0m | £75.2m | — | — | £96.2m / NOT FOUND (Sky Sports) |
| summer 2024 | £1.81bn | £592.4m | — | — | £2.08bn / £627.4m (Sky Sports) |
| January 2025 | £343.5m | £213.6m | — | — | around £370m / NOT FOUND (BBC Sport) |
| summer 2025 | £2.83bn | £1.19bn | — | — | surpassed £3bn; £3.087bn / NOT FOUND (BBC Sport) |
| January 2026 | £341.6m | £111.3m | — | — | £397m / NOT FOUND (BBC Sport) |
| summer 2026 | £3.07bn | £1.26bn | — | — | around £3.46 billion / NOT FOUND (Reuters, syndicated ) |

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

1. **Tier 1 is too big as worded (DEC-253).** 2,041 transfers are Tier 1, mostly because of the "changes the top-12 order" test. *Recommendation:* keep £20m+, records and disputed fees, and narrow the order test to "changes the leader, or who is in the top 12, at any month end"; the rest get Tier 2's scripted check.
2. **Undisclosed fees count £0 (DEC-237 (g)).** 2,201 transfers have no reported figure. *Recommendation:* keep the rule, say on screen "Undisclosed fees not included", and give each club's undisclosed count in the description.
3. **The early years are the least complete (1992–2007).** *Recommendation:* in phase 2, Claude in Cowork uses Transfermarkt in your Chrome only as a finding list (route A, nothing stored) to spot missing 1992–2007 deals involving the bigger fees, and takes each fee from a press or club source.
4. **Relegated clubs keep their frozen bar and their rank** (contract §1; e.g. a relegated club can sit 8th at the freeze). *Recommendation:* keep them in the ranking; how a frozen bar looks is a design question for the pilot (DEC-069).
5. **Start of the race.** At 31 May 1992 every bar is £0 (the leader that month is only a tie-break). *Recommendation:* the film starts at the first month end with a fee (July 1992); the data stay as they are.
6. **Same-grade fee disagreements on Tier 1 transfers:** 39 are listed in `conflicts.csv` (column `for_luke`). *Recommendation:* phase 2 settles each at source; the ones still open after that come back to you as a short list.
7. **Claude's working choices** DEC-247 (finding list), DEC-248 (tiers), DEC-249 (board size later), DEC-250 (build details) and DEC-254 (how the scripted check marks a fee VERIFIED, and publisher grades). *Recommendation:* confirm them.
8. **Phase 2 first batch.** *Recommendation:* verify the Tier 1 fees of the clubs that lead or reach the top 3 (Chelsea, Manchester United, Manchester City, Arsenal, Liverpool, Newcastle, Blackburn, Everton) first, in batches of 50 (`tier1_list.csv`, column `batch`).

## 10. Phase 2 (IQ-15b): verification at source

- **Tier 1 (DEC-256):** 2,024 fee-bearing Tier 1 transfers; **1,381 VERIFIED at source** (1,314 by a club, league or press source, grade A/B; 67 only by a database such as Soccerbase, grade C; 0 only by a grade D site), each quote read by Claude (2,040 quotes accepted, 253 rejected; `source/review_decisions.csv`). The rest have no page that states the figure next to the player's name yet (mostly 1990s–2000s deals whose only sources are Wikipedia figures or dead links).
- **Tier 2:** 320 of 663 VERIFIED by the scripted check. **Tier 3 sample:** 6 of 30 VERIFIED.
- **Undisclosed fees (DEC-257):** 47 grade A/B reported figures found at the cited source and read by Claude, used and flagged "reported" (45 transfers; 33 close candidates rejected on reading: another deal, grade D, not a fee, or a total with add-ons; `source/reported_fees.csv`); every other candidate figure on those pages belonged to another deal, a wage, an offer or a fine.
- **1992–2007 gap list (DEC-264), sections A v2, B and C (1992–2007):** 137 new moves added, 99 VERIFIED (the page names the player, both clubs and the fee); the rest matched transfers already in the build. 6 gap rows have no transfer date (retrospective articles only) and are listed in `unmatched_leads.csv`.
- **Leeds United 1992–2002** pages added; **last 1991–92 First Division matchday 2 May 1992** confirmed by eight club fixture lists (pointers, grade C).
- **Root causes found by reading the batches, and fixed in the build** (each fix applies to every row, not only the one seen): player names inside Wikipedia sort templates; the same deal listed twice; research leads matched on surname only (Kylian Hazard had been given Eden Hazard's fee); club-season tables whose direction was read from prose, plus a Wikipedia table labelled "From" in an "Out" section (Newcastle 1998–99); figures that are maxima, offers, valuations, instalments, combined fees or totals including add-ons; a regression that had dropped pre-2002 research-lead transfers (restored); accented names not matched (ø, æ, ß and others); Soccerbase "Totals" lines and other rows of a career table read as this deal's fee (a Soccerbase figure now counts only from the row whose joining date is the transfer's); the same deal reported at two stages with a non-PL club not merged (Yobo, Baros); a reported figure attached to the same player's other moves.

### Same-grade fee conflicts not settled at source (DEC-261): 39, each settled by the contract's rule (DEC-277)

Settled at source = the fee used is confirmed at source and no differing same-grade figure is (totals including add-ons are not rivals). The deals below were not; Luke decided (DEC-277) that the existing rule settles them: best grade first, then the earliest report (a contemporary sterling figure from a grade A/B source preferred, contract §5). The last column says which step decided. Where no figure is confirmed at source yet, the fee stays UNVERIFIED (not on screen) and the deal is in the next research round.

| Player | From → To | Date | Fee used | Other confirmed figure(s) | Why not settled at source | Result under the rule (DEC-277) |
|---|---|---|---|---|---|---|
| Carlos Tevez | Media Sports Investments → Manchester City | 2009-07-14 | £25.0m (B) | B V according to reliable sources, £45m; B V around £25million; £45million claim denied; B V £25.5m | two same-grade sources confirm different figures | £25.0m (B, www.skysports.com): same grade; earliest report (2009-09-12) |
| Cesc Fàbregas | Arsenal → Barcelona | 2011-08-15 | £25.4m (B) |  | the fee used is not yet confirmed at source | £25.4m (B, www.bbc.co.uk): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Julián Álvarez | Manchester City → Atlético Madrid | 2024-08-12 | £64.4m (B) |  | the fee used is not yet confirmed at source | £64.4m (B, www.bbc.co.uk): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Rodri | Manchester City → Barcelona | 2026-08-18 | £51.3m (B) | B V £65.4m; B V £65m; B V €60m | two same-grade sources confirm different figures | £51.3m (B, www.theguardian.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2026-08-18) |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £75.8m (B) | B V £62m; B V £75.8m; B V €80m plus €20m in add-ons; £89m | two same-grade sources confirm different figures | £75.8m (B, www.skysports.com): same grade; the contemporary sterling figure is preferred (contract §5) |
| David Luiz | Chelsea → Paris Saint-Germain | 2014-06-13 | £50.0m (B) | B V £40m; B V £50m | two same-grade sources confirm different figures | £50.0m (B, www1.skysports.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2014-06-13) |
| Martín Zubimendi | Real Sociedad → Arsenal | 2025-07-06 | £60.0m (B) | B V almost £60m; B V £51m; B V £60m | two same-grade sources confirm different figures | £60.0m (B, www.bbc.co.uk): same grade; earliest report (2025-07-06) |
| Gareth Bale | Tottenham Hotspur → Real Madrid | 2013-09-01 | £85.3m (B) | B V 100m euros; B V Real claimed €91m; B V thought to be a world record figure of €100m | two same-grade sources confirm different figures | £85.3m (B, www.bbc.co.uk): same grade; the contemporary sterling figure is preferred (contract §5) |
| Roberto Firmino | TSG Hoffenheim → Liverpool | 2015-06-24 | £21.3m (B) | B V about £29m; B V £21.3m now; could eventually rise to £28m; B V £29.5m | two same-grade sources confirm different figures | £21.3m (B, www.skysports.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2015-06-24) |
| Michael Turner | Hull City → Sunderland | 2009-08-31 | £12.0m (B) | B V £12m; B V £12m; believed to be in the region of £12m; B V £12million | two same-grade sources confirm different figures | £12.0m (B, www.theguardian.com): same grade; earliest report (2009-08-31) |
| André-Frank Zambo Anguissa | Marseille → Fulham | 2018-08-09 | £30.0m (B) | B V Sky Sports News understands to be £22.3m; B V around £30m | two same-grade sources confirm different figures | £30.0m (B, www.theguardian.com): same grade; earliest report (2018-08-09) |
| Aleksandar Mitrović | Fulham → Al Hilal | 2023-08-19 | £50.0m (B) | B V 50 million euros; B V £50m | two same-grade sources confirm different figures | £50.0m (B, www.bbc.co.uk): same grade; earliest report (2023-08-19) |
| Willian | Anzhi Makhachkala → Chelsea | 2013-08-28 | £32.0m (B) | B V thought to be in the region of £25.5m; B V £32m | two same-grade sources confirm different figures | £32.0m (B, www.theguardian.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2013-08-28) |
| Matteo Sereni | Sampdoria → Ipswich Town | 2001-08-17 | £0.0m (B) | B V around £6m; B V believed to be around £4.5 million sterling | two same-grade sources confirm different figures | £0.0m (B, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Timo Werner | RB Leipzig → Chelsea | 2020-07-01 | £53.0m (B) | B V £47.5m; B V £53m release clause | two same-grade sources confirm different figures | £53.0m (B, www.theguardian.com): same grade; earliest report (2020-06-04) |
| Alexander Hleb | VfB Stuttgart → Arsenal | 2005-06-27 | £11.2m (C) |  | the fee used is not yet confirmed at source | £11.2m (C, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Granit Xhaka | Borussia Mönchengladbach → Arsenal | 2016-05-25 | £35.0m (B) | B V in the region of £30m; B V reported £35m | two same-grade sources confirm different figures | £35.0m (B, www.bbc.co.uk): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2016-05-25) |
| Arjen Robben | PSV → Chelsea | 2004-06-08 | £7.0m (C) |  | the fee used is not yet confirmed at source | £7.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Richarlison | Watford → Everton | 2018-07-24 | £35.0m (B) | B V around £40m; B V potential £50m deal | two same-grade sources confirm different figures | £35.0m (B, www.bbc.co.uk): same grade; earliest report (2018-07-24) |
| Fred | Shakhtar Donetsk → Manchester United | 2018-06-21 | £47.0m (B) | B V believed to be £52m; B V £47m | two same-grade sources confirm different figures | £47.0m (B, www.bbc.co.uk): same grade; earliest report (2018-06-21) |
| Petr Čech | Rennes → Chelsea | 2004-06-08 | £12.0m (C) |  | the fee used is not yet confirmed at source | £12.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Sofiane Boufal | Lille → Southampton | 2016-08-29 | £21.0m (B) | B V Sky sources understand the fee to be a club-record £16m; B V £21m according to sources at the south-coast club | two same-grade sources confirm different figures | £21.0m (B, www.skysports.com): same grade; earliest report (2016-08-25) |
| Álvaro Negredo | Manchester City → Valencia | 2015-06-08 | £21.3m (B) | B V £20m; B V £21.3m; B V £23.7m | two same-grade sources confirm different figures | £21.3m (B, www.skysports.com): same grade; earliest report (2015-07-01) |
| David Luiz | Paris Saint-Germain → Chelsea | 2016-08-31 | £34.0m (B) | B V around £34m; B V believed to be in the region of £30m; B V £34m, with further fees due in future | two same-grade sources confirm different figures | £34.0m (B, www.theguardian.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2016-08-31) |
| Shaun Wright-Phillips | Manchester City → Chelsea | 2005-07-18 | £21.0m (B) |  | the fee used is not yet confirmed at source | £21.0m (B, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Henrikh Mkhitaryan | Borussia Dortmund → Manchester United | 2016-07-06 | £30.0m (B) | B V undisclosed fee believed to be £30m; B V £26.3m | two same-grade sources confirm different figures | £30.0m (B, www.theguardian.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 2016-07-06) |
| Cesc Fàbregas | Barcelona → Chelsea | 2014-06-12 | £27.0m (B) |  | the fee used is not yet confirmed at source | £27.0m (B, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Christian Bassedas | Vélez Sársfield → Newcastle United | 2000-06-01 | £3.5m (B) | B V £0.5m; B V £3.5m | two same-grade sources confirm different figures | £3.5m (B, www.theguardian.com): same grade; earliest report (2000-06-01) |
| Mustapha Hadji | Coventry City → Aston Villa | 2001-07-07 | £2.0m (B) | B V £4.5m part-exchange; B V £4.5m part-exchange; £2m cash; B V £4m | two same-grade sources confirm different figures | £2.0m (B, www.theguardian.com): same grade; earliest report (2001-08-02) |
| Matthew Upson | Arsenal → Birmingham City | 2003-01-22 | £3.0m (C) |  | the fee used is not yet confirmed at source | £3.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| James Milner | Newcastle United → Aston Villa | 2008-08-29 | £12.0m (B) | B V believed to be in the region of £10m; B V £12m | two same-grade sources confirm different figures | £12.0m (B, www.theguardian.com): same grade; earliest report (2008-08-29) |
| Igor Biscan | Dinamo Zagreb → Liverpool | 2000-12-07 | £7.0m (B) | B V £5.5m; B V £5m; B V £7m | two same-grade sources confirm different figures | £7.0m (B, www.theguardian.com): same grade; earliest report (2000-10-13) |
| Pascal Chimbonda | Wigan Athletic → Tottenham Hotspur | 2006-08-31 | £6.0m (C) |  | the fee used is not yet confirmed at source | £6.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Steve Howey | Newcastle United → Manchester City | 2000-08-31 | £2.0m (B) | B V £2m; The fee could rise to £3m; B V £3.5m | two same-grade sources confirm different figures | £2.0m (B, www.independent.co.uk): same grade; earliest report (2000-08-11) |
| Nwankwo Kanu | Internazionale → Arsenal | 1999-01-15 | £3.0m (B) | B V believed to be around pounds 4.5m; B V pounds 3m; B V pounds 4.5m | two same-grade sources confirm different figures | £3.0m (B, www.the-independent.com): same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; 1999-01-29) |
| Kevin Campbell | Nottingham Forest → Trabzonspor | 1998-07-29 | £2.5m (B) | B V pounds 2.5m; B V pounds 4m; B V £3 million | two same-grade sources confirm different figures | £2.5m (B, www.independent.co.uk): same grade; earliest report (1998-08-08) |
| Faustino Asprilla | Newcastle United → Parma | 1998-01-31 | £7.3m (B) | B V pounds 6m; B V pounds 7.3m | two same-grade sources confirm different figures | £7.3m (B, www.independent.co.uk): same grade; earliest report (1998-01-15) |
| Nick Barmby | Middlesbrough → Everton | 1996-10-30 | £5.7m (B) | B V pounds 4.5m; B V pounds 5.3m; B V pounds 5.75m | two same-grade sources confirm different figures | £5.7m (B, www.the-independent.com): same grade; earliest report (1996-11-17) |
| Christos Tzolis | PAOK → Norwich City | 2021-08-12 | £8.8m (B) | B V around £10m; B V £8.8m | two same-grade sources confirm different figures | £8.8m (B, www.bbc.co.uk): same grade; earliest report (2021-08-12) |

### Effect of the 1992–2007 gap list (sections A v2, B, C) on window totals, 1997–2007

Our sums count fees paid by PL clubs (gross) and fees paid to minus received from non-PL clubs (net); undisclosed fees count £0. "Before" = the build just before sections A v2, B and C were added (`source/window_totals_before_gap_list_v2.csv`). Published totals are research leads (part17b, UNVERIFIED); none exist for windows before summer 2002 (no window system).

"Change" also includes the corrections made by reading the sources since that snapshot (for example a maximum replaced by the guaranteed fee); "of which gap list" is the gross paid by PL clubs in all moves the gap list created (section A's first version, part18b, was already in the snapshot, so this column can exceed the change).

| Window | Gross before | Gross after | Change | of which gap list | Published gross (first A/B source) | Gap left | Net before | Net after |
|---|---|---|---|---|---|---|---|---|
| January 1997 | £41.5m | £44.2m | £2.8m | £15.4m | — | — | £12.4m | £13.5m |
| summer 1997 | £116.2m | £141.7m | £25.4m | £26.1m | — | — | £30.9m | £56.4m |
| January 1998 | £49.6m | £49.7m | £0.1m | £1.0m | — | — | £10.5m | £15.0m |
| summer 1998 | £128.7m | £163.6m | £34.9m | £33.4m | — | — | £49.4m | £82.8m |
| January 1999 | £82.6m | £92.0m | £9.4m | £9.6m | — | — | £28.6m | £34.3m |
| summer 1999 | £136.1m | £167.2m | £31.1m | £35.7m | — | — | £28.6m | £53.4m |
| January 2000 | £42.1m | £37.2m | −£4.8m | £1.0m | — | — | £19.5m | £18.3m |
| summer 2000 | £241.3m | £243.0m | £1.7m | £17.5m | — | — | £97.1m | £92.0m |
| January 2001 | £58.6m | £67.0m | £8.4m | £7.0m | — | — | −£11.9m | −£5.1m |
| summer 2001 | £264.2m | £280.2m | £16.0m | £32.8m | — | — | £150.2m | £166.7m |
| January 2002 | £56.1m | £64.1m | £8.1m | £6.3m | — | — | £22.2m | £33.8m |
| summer 2002 | £174.2m | £174.7m | £0.5m | £0.0m | — | — | £114.4m | £115.4m |
| January 2003 | £36.8m | £39.8m | £3.0m | £3.0m | £35.0m (B, The Independent) | −£4.8m | £14.2m | £17.2m |
| summer 2003 | £212.4m | £204.9m | −£7.6m | £0.0m | £215.0m (B, The Independent) | £10.1m | £120.3m | £119.2m |
| January 2004 | £61.1m | £44.0m | −£17.1m | £0.0m | — | — | £34.6m | £17.4m |
| summer 2004 | £172.0m | £207.2m | £35.2m | £33.0m | — | — | £99.3m | £134.7m |
| January 2005 | £41.2m | £44.0m | £2.8m | £2.8m | — | — | £12.8m | £15.6m |
| summer 2005 | £195.3m | £229.4m | £34.0m | £28.4m | £235.0m (B, The Independent) | £5.6m | £81.4m | £112.3m |
| January 2006 | £51.2m | £51.1m | −£0.1m | £0.0m | — | — | £41.7m | £41.6m |
| summer 2006 | £239.8m | £240.9m | £1.1m | £4.7m | £300.0m (B, BBC News) | £59.0m | £118.4m | £122.0m |
| January 2007 | £37.5m | £39.8m | £2.4m | £3.0m | — | — | £17.9m | £17.2m |
| summer 2007 | £324.6m | £320.5m | −£4.1m | £0.0m | — | — | £166.2m | £162.1m |

Total gross 1997–2007: £2.76bn before, £2.95bn after (£183.1m net change, of which £260.7m paid in moves the gap list added). Where a published total exists, our sum stays below it mainly because undisclosed fees count £0 and the early Wikipedia window lists are short; the gap list narrows the gap but does not close it, and no figure is forced to match.

### Leader sequence after phase 2

Leader at each change (month end): 1992-05 Arsenal; 1992-07 Blackburn Rovers; 1993-07 Liverpool; 1993-09 Blackburn Rovers; 1995-07 Liverpool; 1996-07 Newcastle United; 1997-08 Liverpool; 1998-02 Newcastle United; 1999-07 Liverpool; 2001-07 Manchester United; 2001-08 Liverpool; 2001-11 Leeds United; 2002-06 Liverpool; 2002-07 Manchester United; 2003-03 Newcastle United; 2003-07 Chelsea; 2015-08 Manchester City; 2016-07 Chelsea; 2016-08 Manchester City; 2022-08 Chelsea; 2026-09 Manchester United.


### Phase 2 questions — answered by Luke (YES to all four, 7 Oct 2026: DEC-274 to DEC-277)

1. **Database-only Tier 1 figures.** 67 Tier 1 fees are confirmed only by a grade C source (67 of them a Soccerbase row for that move) and 0 only by a source graded D (mostly later retrospective articles). May a Soccerbase row count as VERIFIED for screen? *Recommendation:* yes for Soccerbase rows (they are dated career tables, checked row by row), no for grade D; keep looking for press sources for both.
2. **Next research round.** 710 Tier 1 fees still have no VERIFIED club, league or press source (`data/rtt-101/tier1_needs_press_source.csv`, mostly 1992–2007). *Recommendation:* one more ChatGPT deep-research round on that list (a press or club URL and a short quote per deal, leads only; every figure checked at source here), starting with 1992–2002.
3. **Fees known only as a maximum or an approximation.** 16 deals count £0 because every figure found is a maximum, a total including add-ons, or an approximation ("just under £30m", "in excess of £13m", "£40m-plus"). *Recommendation:* keep £0 (DEC-237 (e)) and add these deals to the next research round to find the guaranteed fee.
4. **Same-grade conflicts.** 39 remain (table above). *Recommendation:* use the rule already in the contract (highest grade, then the earliest contemporary report) for all of them, and list them in the description notes; Luke can overrule any single deal.

**Luke's answers:** (1) a Soccerbase row counts as VERIFIED, grade C, labelled "database source" (`transfers.csv` column `verified_by`); other grade C and grade D sources do not confirm a fee (DEC-274). (2) One more ChatGPT deep-research round on `tier1_needs_press_source.csv`, starting with 1992–2002; every figure is a lead to check at source here (DEC-275). (3) The deals known only as a maximum or an approximation stay at £0 and are listed in `data/rtt-101/tier1_max_or_approx_only.csv` for a later round (DEC-276). (4) The same-grade conflicts are settled by the rule, with the result for each in the table above (DEC-277).

## 11. Source round 1, list A: 1992–93 to 1996–97 (DEC-275, IQ-15d)

- **Deals:** 211 (A0001–A0211), mapped to our transfers by player and date (`source/source_round1_map.csv`). ChatGPT's answers (private part20b/d/f) were added as leads (`found_via` of each evidence row: "ChatGPT source round 1 (DEC-264 route)") and every cited page was read on the GitHub runner: the figure next to the player's name, and both clubs named on the page.
- **VERIFIED:** 158 of the 211 deals now have a fee confirmed at source (145 by a club, league or press source; the rest by a Soccerbase row), up from 41 before this round.
- **Changed:** 56 fees changed (£7.2m up, £12.6m down; net −£5.5m) and 14 completion dates moved to the date a grade B report gives.
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
| A0030 | Alex Mathie | Greenock Morton → Newcastle United | 1993-07-30 | £250,000 | £285,000 | higher grade or earlier report (C, www.independent.co.uk) |
| A0031 | Jason Dozzell | Ipswich Town → Tottenham Hotspur | 1993-08-01 | £1,900,000 | £1,750,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0032 | Guy Whittingham | Portsmouth → Aston Villa | 1993-08-03 → 1993-08-04 | £1,200,000 | £875,000 | part-exchange (DEC-237 (d)): a stated player valuation counts on both sides, otherwise cash only |
| A0036 | David Kerslake | Leeds United → Tottenham Hotspur | 1993-09-01 | £450,000 | £500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0044 | Darren Ferguson | Manchester United → Wolverhampton Wanderers | 1994-01-13 | £320,000 | £250,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0046 | Liam O'Brien | Newcastle United → Tranmere Rovers | 1994-01-21 | £300,000 | £250,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0049 | Peter Beagrie | Everton → Manchester City | 1994-03-31 | £1,100,000 | £1,000,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0050 | Julian Dicks | Liverpool → West Ham United | 1994-05-20 → 1994-10-20 | £1,000,000 | £100,000 | add-ons only when reported as triggered (DEC-237 (e)) |
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
| summer 1993 | £39.6m | £39.2m | −£0.4m |
| January 1994 | £16.2m | £16.1m | −£0.1m |
| summer 1994 | £73.3m | £71.4m | −£1.9m |
| January 1995 | £41.6m | £41.1m | −£0.5m |
| summer 1995 | £109.4m | £108.1m | −£1.3m |
| January 1996 | £54.6m | £53.9m | −£0.7m |
| summer 1996 | £102.8m | £103.1m | £0.3m |
| January 1997 | £41.5m | £44.2m | £2.8m |

**Effect on the race:** the leader changes at 5 month ends (1997-07: Liverpool → Newcastle United; 2000-01: Newcastle United → Liverpool; 2000-02: Newcastle United → Liverpool; 2000-06: Chelsea → Liverpool; 2002-06: Leeds United → Liverpool); who is in the top 12 changes at 67 month ends (1992-08: in Manchester United, out Everton; 1992-09: in Manchester United, out Sheffield United; 1992-10: in Manchester United, out Sheffield United; 1993-06: in Manchester United, out Swindon Town; 1993-08: in Ipswich Town, out Oldham Athletic; 1994-06: in Swindon Town, out West Ham United; 1994-07: in Crystal Palace, out West Ham United; 1994-08: in Leicester City, out West Ham United; 1994-09: in Leicester City, out West Ham United; 1995-03: in Sheffield Wednesday, out Newcastle United …); the order within the top 12 changes at 218 month ends.

**Questions for Luke on list A (each with Claude's recommendation)**

1. **Combined fees.** One payment for two players (Charles and Tommy Johnson £2.9m; McKee and Whitworth £530,000; Billington and McKeever £500,000) is booked once, on one transfer of the pair, and the partner counts £0. Each club's total is exact and no split is invented. *Recommendation:* keep it.
2. **Parker and Carr (Villa ↔ Leicester, Feb 1995).** The only source values "the deal" at £550,000 without saying how much was cash. We count £550,000 for Parker and £0 for Carr. *Recommendation:* keep it, and ask the next research round for the cash figure.
3. **Andy Cole (Feb 1995).** A grade B source values Keith Gillespie at £1m in the deal, so under DEC-237 (d) Cole counts £7m (£6m cash plus Gillespie) and Gillespie £1m; Manchester United's net is still the £6m cash. *Recommendation:* keep it (it follows the rule Luke approved).

**Answered by Luke (Cowork chat, 8 Oct 2026): yes to all three, kept as built (DEC-405, DEC-406, DEC-407).**

## 12. Source round 1, list B: 1997–98 to 2001–02 (DEC-275, IQ-15f), and the completion-report rule (DEC-404)

- **Deals:** 342 (B0001–B0342; 342 of our transfers), mapped by player and date (`source/source_round1_map.csv`). ChatGPT's answers (private part21a–r, every SHA-256 matched its README) were added as leads (`found_via`: "ChatGPT source round 1 (DEC-264 route)") and every cited page was read on the GitHub runner: the figure next to the player's name, and both clubs named on the page. Wikipedia and Transfermarkt pages are never fee sources and were not fetched.
- **VERIFIED:** 299 of the 342 transfers now have a fee confirmed at source (290 by a club, league or press source; the rest by a Soccerbase row), up from 81 before this round. 9 more count £0 (undisclosed, nominal, free, or known only as a maximum or approximation).
- **Changed:** 117 fees changed (£16.9m up, £46.4m down; net −£29.5m) and 11 completion dates moved to the date a grade B report gives (`source/deal_structure.csv` for the dates set by hand).

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
| B0023 | Danny Murphy | Crewe Alexandra → Liverpool | 1997-07-15 | £3,000,000 | £2,000,000 | confirmed at source: higher grade or earlier report (B, www.independent.co.uk) |
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
| B0269 | Clarence Acuña | Universidad de Chile → Newcastle United | 2000-10-31 | £1,000,000 | £700,000 | confirmed at source: higher grade or earlier report (B, www.theguardian.com) |
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

**DEC-404 (Luke, 8 Oct 2026): a report that the deal was completed beats earlier reports of bids, agreed fees or "expected" figures of the same grade; the earliest report is used only when none says the deal was completed.** Applied to the whole build, it changes **48 fees** (`source/dec404_changes.csv`): 5 on list A, 6 of the 32 phase 2 same-grade conflicts, 17 on list B and 20 elsewhere. A completion word counts only next to the player's name; wording such as "imminent", "subject to" or "proposed" means not completed; a figure within 2% of the one already used (the same fee in another currency) changes nothing.

| Date | Player | Move | Fee without DEC-404 | Fee with DEC-404 | On | Completion report |
|---|---|---|---|---|---|---|
| 1992-07-13 | David Lowe | Ipswich Town → Leicester City | £250,000 | £200,000 | source round 1 list A | David Lowe, Leicester City's recent pounds 200,000 signing from Ipswich Town |
| 1994-09-26 | Paul Kitson | Derby County → Newcastle United | £2,500,000 | £2,250,000 | source round 1 list A | Paul Kitson, their recent pounds 2.25m signing from Derby County, |
| 1994-10-14 | Efan Ekoku | Norwich City → Wimbledon | £920,000 | £900,000 | source round 1 list A | Efan Ekoku […] a pounds 900,000 deal |
| 1995-10-01 | Lars Bohinen | Nottingham Forest → Blackburn Rovers | £700,000 | £750,000 | other | otland's Billy McKinlay arrived from Dundee United for pounds 1.75m while Norway's Lars Bo |
| 1996-02-08 | Faustino Asprilla | Parma → Newcastle United | £6,700,000 | £7,500,000 | other | international, who joined Newcastle from Parma in February 1996 for pounds 7.5m, went abou |
| 1996-02-24 | David Batty | Blackburn Rovers → Newcastle United | £3,750,000 | £4,000,000 | source round 1 list A | David Batty […] pounds 4m signing of the Blackburn midfielder. |
| 1996-07-10 | Ronny Johnsen | Beşiktaş → Manchester United | £1,200,000 | £1,500,000 | other | Ronny Johnsen Defender Nationality: Norwegian Age: 26 Arrived from: Besiktas (pounds 1.5m) |
| 1997-01-07 | Ramon Vega | Cagliari → Tottenham Hotspur | £3,000,000 | £3,750,000 | source round 1 list A | Ramon Vega, […] The pounds 3.75m recruit from Cagliari |
| 1997-07-08 | Martin Dahlin | Roma → Blackburn Rovers | £2,500,000 | £2,000,000 | source round 1 list B | Martin Dahlin, the Swedish international signed in the summer for pounds 2m from Roma |
| 1997-07-31 | David Ginola | Newcastle United → Tottenham Hotspur | £2,600,000 | £2,000,000 | source round 1 list B | David Ginola completed his pounds 2m move to Spurs yesterday |
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
| 2001-03-07 | Chris Makin | Sunderland → Ipswich Town | £2,000,000 | £1,250,000 | source round 1 list B | Ipswich completed the signing of the Sunderland defender Chris Makin for £1.25m. |
| 2001-08-01 | Laurent Robert | PSG → Newcastle United | £10,500,000 | £10,000,000 | source round 1 list B | Laurent Robert has completed his £10m move to Newcastle United. |
| 2001-08-17 | Michael Ball | Everton → Rangers | £7,000,000 | £6,000,000 | source round 1 list B | Ball has completed his protracted £6m move |
| 2001-09-09 | Allan Johnston | Rangers → Middlesbrough | £1,000,000 | £600,000 | source round 1 list B | Allan Johnston today joined Middlesbrough from Rangers in a £600,000 deal. |
| 2004-07-27 | Ricardo Carvalho | Porto → Chelsea | £16,500,000 | £19,838,646 | other | signed the Portuguese international defender Ricardo Carvalho from Porto for €30m (£19.8m) |
| 2004-08-30 | Robert Earnshaw | Cardiff City → West Bromwich Albion | £3,400,000 | £3,000,000 | other | Wanderers 2-1. This they achieved without Robert Earnshaw, their record £3m signing from C |
| 2007-07-10 | Florent Malouda | Lyon → Chelsea | £13,500,000 | £13,000,000 | other | the Frenchman, who moved to Stamford Bridge from Lyon for £13million in July, said: "I jus |
| 2010-08-11 | Craig Cathcart | Manchester United → Blackpool | £350,000 | £500,000 | other | Craig Cathcart (Man Utd, £500k) |
| 2012-06-10 | Jay Rodriguez | Burnley → Southampton | £7,000,000 | £6,000,000 | other | not been officially disclosed but is understood to be worth £6m, which breaks Southampton' |
| 2013-08-14 | Tom Huddlestone | Tottenham Hotspur → Hull City | £5,000,000 | £5,250,000 | other | news: Tottenham midfielder Tom Huddlestone completes Hull City switch in £5.25m deal | The |
| 2013-08-28 | Willian | Anzhi Makhachkala → Chelsea | £25,500,000 | £32,000,000 | phase 2 same-grade conflict | has secured his work permit to join Chelsea in a £32m deal from Anzhi Makhachkala. Photogr |
| 2014-06-13 | David Luiz | Chelsea → Paris Saint-Germain | £40,000,000 | £50,000,000 | phase 2 same-grade conflict | move from Chelsea to PSG David Luiz has completed his £50m move from Chelsea to Paris Sain |
| 2014-06-27 | Luke Shaw | Southampton → Manchester United | £27,000,000 | £30,000,000 | phase 2 same-grade conflict | week Luke Shaw has joined Manchester United in a reported £30m switch from Southampton, ma |
| 2015-06-24 | Roberto Firmino | TSG Hoffenheim → Liverpool | £29,000,000 | £21,300,000 | other | Image: Roberto Firmino: Will join Liverpool for initial fee of £21.3m Liverpool have compl |
| 2016-05-25 | Granit Xhaka | Borussia Mönchengladbach → Arsenal | £30,000,000 | £35,000,000 | phase 2 same-grade conflict | caps and captained the German club, joins for a reported £35m on a long-term contract. "I' |
| 2016-07-06 | Henrikh Mkhitaryan | Borussia Dortmund → Manchester United | £26,300,000 | £30,000,000 | phase 2 same-grade conflict | old Armenia midfielder joins for undisclosed fee believed to be £30m Mkhitaryan: ‘This mov |
| 2016-08-31 | David Luiz | Paris Saint-Germain → Chelsea | £30,000,000 | £34,000,000 | other | David Luiz completes shock return to Chelsea from PSG for £34m This article is more than 1 |
| 2016-08-31 | Islam Slimani | Sporting CP → Leicester City | £29,000,000 | £28,000,000 | other | Islam Slimani to Leicester City: Premier League champions confirm club-record £28m signing |
| 2017-07-21 | Álvaro Morata | Real Madrid → Chelsea | £58,000,000 | £60,000,000 | other | 20 caps for Spain Chelsea have completed the club record £60m signing of striker Alvaro Mo |
| 2019-07-04 | Rodri | Atlético Madrid → Manchester City | £68,200,000 | £62,800,000 | other | team after moving from Atletico Madrid for a club record £62.8m. Rodri, 23, joins on a fiv |
| 2020-09-19 | Diogo Jota | Wolverhampton Wanderers → Liverpool | £40,000,000 | £41,000,000 | other | signing of Portugal forward Diogo Jota from Wolves in a £41m deal that could rise to £45m  |
| 2022-07-04 | Kalvin Phillips | Leeds United → Manchester City | £42,000,000 | £45,000,000 | other | Manchester City have signed Leeds United midfielder Kalvin Phillips for £45m. The 26-year- |
| 2022-07-13 | Raheem Sterling | Manchester City → Chelsea | £47,500,000 | £50,000,000 | other | of England forward Raheem Sterling from Manchester City in a £50m deal. Sterling, 27, has  |
| 2022-08-26 | Alexander Isak | Real Sociedad → Newcastle United | £60,000,000 | £58,000,000 | other | Sociedad frontman completed a move understood to be worth around £58million on Friday afte |
| 2023-08-12 | Harry Kane | Tottenham Hotspur → Bayern Munich | £100,000,000 | £86,400,000 | other | at Tottenham. The striker signs for an initial 100m euros (£86.4m) plus add-ons and could  |
| 2026-01-09 | Antoine Semenyo | AFC Bournemouth → Manchester City | £65,000,000 | £62,500,000 | other | had to be activated before Saturday, and they will pay £62.5m across 24 monthly instalment |
| 2026-08-18 | Rodri | Manchester City → Barcelona | £65,400,000 | £51,308,363 | phase 2 same-grade conflict | Barcelona transfer Show The Spain midfielder Rodri has completed his €60m move from Manche |

**Same-grade disagreements within list B** (87 deals) and the step that settled each:

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
| B0023 | Danny Murphy | £2,000,000 (B, 1997-07-03) | £1,500,000 (1997-07-09), £2,750,000 (1997-08-06) | earliest report (DEC-277), or the completion report when it is also the earliest |
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
| B0269 | Clarence Acuña | £700,000 (B, 2000-09-29) | £1,000,000 (2000-10-10) | earliest report (DEC-277), or the completion report when it is also the earliest |
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
| summer 1997 | £144.4m | £141.7m | −£2.7m | — | £59.0m | £56.4m |
| January 1998 | £51.2m | £49.7m | −£1.5m | — | £12.1m | £15.0m |
| summer 1998 | £162.6m | £163.6m | £1.0m | — | £80.7m | £82.8m |
| January 1999 | £93.7m | £92.0m | −£1.7m | — | £36.2m | £34.3m |
| summer 1999 | £172.5m | £167.2m | −£5.3m | — | £56.7m | £53.4m |
| January 2000 | £43.8m | £37.2m | −£6.5m | — | £21.2m | £18.3m |
| summer 2000 | £245.8m | £243.0m | −£2.8m | — | £92.3m | £92.0m |
| January 2001 | £64.3m | £67.0m | £2.7m | — | −£8.4m | −£5.1m |
| summer 2001 | £289.4m | £280.2m | −£9.2m | — | £173.7m | £166.7m |
| January 2002 | £60.2m | £64.1m | £3.9m | — | £29.6m | £33.8m |
| summer 2002 | £174.7m | £174.7m | £0.0m | — | £115.4m | £115.4m |

Total gross summer 1997 to summer 2002: £1.50bn before, £1.48bn after (−£22.1m).

**Effect on the race** (against the build at c62ca6b): the leader changes at 8 month ends (1997-07: Liverpool → Newcastle United; 1998-02: Liverpool → Newcastle United; 2000-06: Chelsea → Liverpool; 2002-06: Leeds United → Liverpool; 2003-03: Manchester United → Newcastle United; 2003-04: Manchester United → Newcastle United; 2003-05: Manchester United → Newcastle United; 2003-06: Manchester United → Newcastle United); who is in the top 12 changes at 57 month ends (1995-03: in Ipswich Town, out Newcastle United; 1995-04: in Ipswich Town, out Newcastle United; 1995-05: in Ipswich Town, out Newcastle United; 1998-07: in West Ham United, out Coventry City; 1998-09: in West Ham United, out Coventry City; 1998-10: in Coventry City, out Blackburn Rovers; 1999-08: in Coventry City, out Arsenal; 1999-09: in Coventry City, out Arsenal; 1999-10: in Coventry City, out Arsenal; 1999-11: in Coventry City, out Arsenal …); the order within the top 12 changes at 193 month ends.

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
