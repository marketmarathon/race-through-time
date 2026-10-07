# RTT-101 Premier League net transfer spend — data report, phase 1 (IQ-15, 7 Oct 2026)

**Status: UNVERIFIED preview. Not for screen.** Only figures marked VERIFIED may ever be shown, and phase 2 (verification of Tier 1 at source, in batches) comes before any design work. Rules: `reference/metric_contract_RTT-101.md`; decisions DEC-235 to DEC-250 (and the findings recorded with this build).

Rebuild: `python3 scripts/build_rtt101_dataset.py && python3 scripts/rtt101_report.py` (deterministic; the private cross-checks need the private folder: `python3 scripts/rtt101_private_crosschecks.py <private research folder>` first).

## 1. What was built

- **13,015 transfer events** that involve a club in the Premier League that season (1992-93 to the freeze, 1 Sep 2026), of which **3,293 carry a fee** above £0. The rest are loans without a fee (5,330), free transfers (2,045), undisclosed fees with no figure, counted £0 (2,197), and fees not found (150).
- Fee status: **VERIFIED 1,232**, UNVERIFIED 2,061. Grade of the fee used: A 19, B 1,202, C (Wikipedia pointer only) 2,033, D 39.
- Tiers (DEC-248): Tier 1 **2,023**, Tier 2 675, Tier 3 612 (5% sample: 31).
  Tier 1 reasons (a transfer can have several): removal changes the leader or the top 12 1,120; fee >= £20m 544; club or British record (research lead) 526; disputed fee (research section C) 9; alternative fee version changes the leader or the top 12 2.
- 16,442 evidence rows in `fee_evidence.csv`; 2,568 sources in `sources.csv`; 371 transfers with more than one fee version (`conflicts.csv`).
- **Scripted source check** (GitHub runner, 3,707 cited pages): VERIFIED 3,070; page fetched but figure not found near the player's name 559; blocked or gone 78.
  Tier 2 result: 275 of 675 Tier 2 fees VERIFIED by the scripted check.
  Tier 3 sample: 1 of 31 VERIFIED; most Tier 3 rows have no fetchable citation (error rate cannot be published yet: phase 2).

## 2. Checks

| Check | Result | Detail |
|---|---|---|
| 22 clubs per season 1992-95, 20 after (706 club-seasons) | **PASS** | 706 club-seasons in 35 seasons |
| every season has an attribution window | **PASS** | 1992-05-03 to 2026-09-01 |
| 51 clubs, each with at least one PL season | **PASS** | 51 clubs |
| no transfer counted outside its club's PL seasons | **PASS** | 3734 ledger rows frozen (club not in the PL) |
| PL-to-PL deals net to zero (spend - income of PL clubs = net spend with non-PL clubs) | **PASS** | spend £27,635,727,699 − income £14,260,850,732 = £13,374,876,967; net with non-PL clubs £13,374,876,967 |
| no fee without a source row | **PASS** | 3293 fee-bearing transfers |
| no Transfermarkt figure or URL anywhere | **PASS** | none found |
| quotes under 25 words | **PASS** | 16442 evidence rows |
| every conversion has a rate row | **PASS** | 12 conversions |
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
| 1992-07-31 | Blackburn Rovers | £3.9m |
| 1993-07-31 | Liverpool | £5.7m |
| 1993-09-30 | Blackburn Rovers | £8.1m |
| 1995-07-31 | Liverpool | £22.4m |
| 1996-07-31 | Newcastle United | £38.5m |
| 1997-07-31 | Liverpool | £31.8m |
| 1998-02-28 | Newcastle United | £33.1m |
| 1999-07-31 | Liverpool | £55.6m |
| 2000-06-30 | Chelsea | £69.2m |
| 2000-07-31 | Liverpool | £72.7m |
| 2001-07-31 | Manchester United | £81.7m |
| 2001-08-31 | Liverpool | £81.5m |
| 2001-11-30 | Leeds United | £86.0m |
| 2002-07-31 | Manchester United | £89.4m |
| 2003-03-31 | Newcastle United | £91.1m |
| 2003-07-31 | Chelsea | £116.0m |
| 2015-08-31 | Manchester City | £602.1m |
| 2016-07-31 | Chelsea | £638.3m |
| 2016-08-31 | Manchester City | £763.8m |
| 2022-08-31 | Chelsea | £1.17bn |
| 2026-09-01 | Manchester United | £1.72bn |

## 4. Top 12 at key dates (UNVERIFIED preview)

**1993-05-31:** 1. Blackburn Rovers £5.4m; 2. Manchester City £2.5m; 3. Aston Villa £2.5m; 4. Sheffield Wednesday £2.0m; 5. Leeds United £1.9m; 6. Liverpool £0.9m; 7. Oldham Athletic £0.8m; 8. Chelsea £0.6m; 9. Ipswich Town £0.5m; 10. Arsenal £0.3m; 11. Manchester United £0.0m; 12. Newcastle United £0.0m

**1997-05-31:** 1. Newcastle United £36.7m; 2. Aston Villa £20.6m; 3. Everton £20.0m; 4. Liverpool £19.3m; 5. Middlesbrough £16.7m (out of the PL); 6. Arsenal £16.7m; 7. Chelsea £16.1m; 8. Coventry City £14.7m; 9. Leeds United £13.9m; 10. Sheffield Wednesday £12.1m; 11. Blackburn Rovers £10.2m; 12. Tottenham Hotspur £8.4m

**2002-05-31:** 1. Leeds United £86.0m; 2. Chelsea £80.0m; 3. Liverpool £75.1m; 4. Newcastle United £67.6m; 5. Manchester United £61.4m; 6. Tottenham Hotspur £52.5m; 7. Aston Villa £48.2m; 8. Middlesbrough £47.9m; 9. Blackburn Rovers £46.0m; 10. Fulham £37.0m; 11. Arsenal £34.0m; 12. Manchester City £26.4m

**2005-05-31:** 1. Chelsea £284.2m; 2. Manchester United £118.5m; 3. Liverpool £101.4m; 4. Newcastle United £86.2m; 5. Tottenham Hotspur £81.2m; 6. Middlesbrough £77.3m; 7. Aston Villa £54.6m; 8. Manchester City £50.4m; 9. Blackburn Rovers £39.8m; 10. Sunderland £39.1m; 11. Arsenal £38.8m; 12. Birmingham City £28.9m

**2008-08-31:** 1. Chelsea £363.4m; 2. Liverpool £173.8m; 3. Manchester United £160.6m; 4. Middlesbrough £120.8m; 5. Tottenham Hotspur £118.1m; 6. Aston Villa £116.5m; 7. Newcastle United £104.9m; 8. Sunderland £79.3m; 9. Manchester City £75.5m; 10. Everton £50.7m; 11. Fulham £47.1m; 12. Birmingham City £46.9m (out of the PL)

**2012-05-31:** 1. Chelsea £475.5m; 2. Manchester City £336.5m; 3. Liverpool £145.1m; 4. Tottenham Hotspur £131.4m; 5. Manchester United £123.5m; 6. Aston Villa £122.0m; 7. Middlesbrough £120.7m (out of the PL); 8. Sunderland £94.0m; 9. Newcastle United £77.9m; 10. Birmingham City £64.9m (out of the PL); 11. Everton £63.5m; 12. Stoke City £53.4m

**2016-08-31:** 1. Manchester City £763.8m; 2. Chelsea £680.8m; 3. Manchester United £540.4m; 4. Liverpool £272.8m; 5. Arsenal £156.8m; 6. Tottenham Hotspur £156.6m; 7. Sunderland £145.2m; 8. Middlesbrough £138.5m; 9. West Ham United £121.4m; 10. Aston Villa £117.2m (out of the PL); 11. Stoke City £107.7m; 12. Newcastle United £97.0m (out of the PL)

**2020-10-31:** 1. Manchester City £1.10bn; 2. Chelsea £964.3m; 3. Manchester United £842.9m; 4. Liverpool £400.5m; 5. Everton £391.7m; 6. Arsenal £361.2m; 7. Tottenham Hotspur £304.6m; 8. Aston Villa £283.9m; 9. West Ham United £237.9m; 10. Newcastle United £196.7m; 11. West Bromwich Albion £161.1m; 12. Fulham £149.3m

**2023-09-30:** 1. Chelsea £1.68bn; 2. Manchester United £1.29bn; 3. Manchester City £1.18bn; 4. Arsenal £746.8m; 5. Liverpool £609.8m; 6. Newcastle United £560.0m; 7. Tottenham Hotspur £498.9m; 8. West Ham United £427.8m; 9. Aston Villa £377.5m; 10. Everton £366.9m; 11. AFC Bournemouth £242.6m; 12. Fulham £194.0m

**2026-09-01:** 1. Manchester United £1.72bn; 2. Chelsea £1.62bn; 3. Manchester City £1.59bn; 4. Arsenal £1.17bn; 5. Liverpool £968.3m; 6. Tottenham Hotspur £946.9m; 7. Newcastle United £681.1m; 8. West Ham United £541.4m (out of the PL); 9. Everton £409.6m; 10. Fulham £344.8m; 11. Sunderland £305.6m; 12. Aston Villa £267.7m

## 5. Coverage by era

Counts are club-sides (a PL-to-PL deal counts once for each club).

| Era | Transfers found | With a fee | Fee grade A/B | Fee VERIFIED | Undisclosed, no figure | Fee not found |
|---|---|---|---|---|---|---|
| 1992-2002 (no window lists) | 2,179 | 1,468 | 310 | 391 | 37 | 94 |
| 2002-2007 | 1,180 | 476 | 76 | 60 | 143 | 13 |
| 2007-2012 | 2,972 | 399 | 114 | 103 | 690 | 10 |
| 2012-2017 | 3,052 | 522 | 232 | 212 | 568 | 10 |
| 2017-2022 | 2,120 | 417 | 270 | 257 | 486 | 20 |
| 2022-2026 | 3,091 | 779 | 576 | 567 | 533 | 20 |

What the eras mean:
- **1992–2002:** no Wikipedia window lists exist (V-10). The finding list is the clubs' season pages (200 of 210 fetched; the ten Leeds United pages are titled "Leeds United A.F.C." and were not fetched in this round) plus the research leads. About a quarter of those pages have no transfer table at all, so this era is the least complete. Transfermarkt was not used (route A says to consult it only to spot omissions; nothing from it is stored).
- **2002–2007:** the early Wikipedia window lists are short (for example summer 2004 has 83 rows involving these clubs, summer 2005 has 76), so many smaller deals are missing.
- **From 2007:** the lists are full (500–800 rows a window), but most fees there are Wikipedia figures (grade C pointers) until the cited source is checked.

## 6. Biggest open conflicts

Transfers whose sources give different fees (never averaged; the canonical fee is the highest grade, then the earliest report). The ones marked for Luke are Tier 1 with a same-grade gap over 10% and £1m (brief §7).

| Player | From → To | Date | Fee used | Range | Tier | For Luke |
|---|---|---|---|---|---|---|
| Philippe Coutinho | Liverpool → Barcelona | 2018-01-08 | £105.0m (B) | £105.0m–£142.0m | 1 |  |
| Anthony Martial | Monaco → Manchester United | 2015-09-01 | £36.0m (B) | £8.5m–£36.0m | 1 |  |
| Mykhailo Mudryk | Shakhtar Donetsk → Chelsea | 2023-01-15 | £88.5m (B) | £61.7m–£89.0m | 1 |  |
| Carlos Tevez | Media Sports Investments → Manchester City | 2009-07-14 | £25.0m (B) | £25.0m–£47.0m | 1 | yes |
| Casemiro | Real Madrid → Manchester United | 2022-08-22 | £60.0m (B) | £50.7m–£70.0m | 1 |  |
| Cesc Fàbregas | Arsenal → Barcelona | 2011-08-15 | £25.4m (B) | £12.8m–£30.0m | 1 | yes |
| José Antonio Reyes | Sevilla → Arsenal | 2004-01-27 | £7.1m (B) | £7.1m–£24.2m | 1 |  |
| Julián Álvarez | Manchester City → Atlético Madrid | 2024-08-12 | £64.4m (B) | £64.4m–£81.0m | 1 | yes |
| Michael Olise | Crystal Palace → Bayern Munich | 2024-07-07 | £50.0m (B) | £45.0m–£60.0m | 1 |  |
| Lucas Paquetá | Lyon → West Ham United | 2022-08-29 | £51.0m (B) | £36.5m–£51.0m | 1 |  |
| Andriy Shevchenko | A.C. Milan → Chelsea | 2006-05-31 | £30.8m (B) | £24.7m–£39.0m | 1 |  |
| Rodri | Manchester City → Barcelona | 2026-08-18 | £65.4m (B) | £51.3m–£65.4m | 1 | yes |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £75.8m (B) | £62.0m–£75.8m | 1 | yes |
| Harry Kane | Tottenham Hotspur → Bayern Munich | 2023-08-12 | £100.0m (B) | £86.4m–£100.0m | 1 |  |
| Alisson | Roma → Liverpool | 2018-07-19 | £55.8m (A) | £55.8m–£67.0m | 1 |  |
| Luis Suárez | Liverpool → Barcelona | 2014-07-16 | £65.0m (B) | £64.0m–£75.0m | 1 |  |
| James Milner | Aston Villa → Manchester City | 2010-08-18 | £26.0m (B) | £15.0m–£26.0m | 1 |  |
| Eliaquim Mangala | Porto → Manchester City | 2014-08-11 | £32.0m (B) | £32.0m–£42.0m | 1 |  |
| Richarlison | Everton → Tottenham Hotspur | 2022-07-01 | £50.0m (B) | £50.0m–£60.0m | 1 |  |
| David Luiz | Chelsea → Paris Saint-Germain | 2014-06-13 | £40.0m (B) | £40.0m–£50.0m | 1 | yes |
| Wayne Rooney | Everton → Manchester United | 2004-08-31 | £20.0m (B) | £20.0m–£30.0m | 1 |  |
| Michael Turner | Hull City → Sunderland | 2009-08-31 | £12.0m (B) | £2.8m–£12.0m | 1 | yes |
| Martín Zubimendi | Real Sociedad → Arsenal | 2025-07-06 | £60.0m (B) | £51.0m–£60.0m | 1 | yes |
| Gareth Bale | Tottenham Hotspur → Real Madrid | 2013-09-01 | £85.3m (B) | £76.6m–£85.3m | 1 | yes |
| Roberto Firmino | TSG Hoffenheim → Liverpool | 2015-06-24 | £29.0m (B) | £21.0m–£29.5m | 1 |  |

36 conflicts are for Luke in total (`conflicts.csv`, column `for_luke`).

## 7. League-wide window totals: our sums against published totals

Our sums are **fees only, Premier League clubs only, from this preview** (gross = fees paid by PL clubs; net = fees paid to non-PL clubs minus fees received from them). Published totals are research leads (UNVERIFIED). The Premier League's own figures (grade A) are the best comparison; the press figures are mostly Deloitte estimates. **Gaps are expected and are not forced to match.**

| Window | Our gross | Our net | Premier League gross (A) | PL net (A) | Press gross / net (B, first listed) |
|---|---|---|---|---|---|
| January 2003 | £44.3m | £21.7m | — | — | £35m / NOT FOUND (The Independent) |
| summer 2003 | £209.9m | £116.8m | — | — | £215m / NOT FOUND (The Independent) |
| summer 2005 | £229.9m | £112.3m | — | — | £235m / NOT FOUND (The Independent) |
| summer 2006 | £244.6m | £123.1m | — | — | £300m / NOT FOUND (BBC News) |
| summer 2008 | £330.6m | £154.6m | — | — | 500 million pounds / NOT FOUND (Reuters (via Rediff)) |
| January 2009 | £92.9m | £6.3m | — | — | about £160m / NOT FOUND (The Guardian (report) |
| summer 2009 | £217.1m | −£9.4m | — | — | £460.4m / NOT FOUND (The Guardian) |
| January 2010 | £26.0m | £9.9m | £36.0m | £7.0m | £30m / NOT FOUND (The Guardian (report) |
| summer 2010 | £157.7m | £84.4m | — | — | around £350million / NOT FOUND (Sky Sports (reportin) |
| January 2011 | £191.9m | £76.4m | £209.3m | £77.3m | £225m / NOT FOUND (The Guardian (table ) |
| summer 2011 | £187.3m | £90.5m | — | — | NOT FOUND / £194m (The Guardian) |
| January 2012 | £42.2m | £6.7m | £67.4m | £24.5m | — |
| summer 2012 | £301.9m | £123.7m | — | — | around £490m / NOT FOUND (Sky News (reporting ) |
| January 2013 | £80.6m | £44.6m | £123.4m | £72.5m | £120m / £70m (Press Association (v) |
| summer 2013 | £552.2m | £346.8m | — | — | £630m / NOT FOUND (BBC Sport) |
| January 2014 | £118.8m | £36.0m | £128.8m | £26.9m | — |
| summer 2014 | £635.9m | £302.6m | £809.6m | £386.5m | £835m / £410m (Press Association (v) |
| January 2015 | £90.6m | £29.8m | £118.2m | £36.4m | £130million / around £40million (The Independent (Age) |
| summer 2015 | £746.6m | £384.7m | £858.6m | £432.6m | £870m / £460m (BBC Sport) |
| January 2016 | £103.6m | £43.6m | £177.5m | £108.9m | £175m / NOT FOUND (BBC Sport) |
| summer 2016 | £1.07bn | £701.3m | £1.12bn | £635.6m | £1.165bn / NOT FOUND (Sky Sports (reportin) |
| January 2017 | £140.5m | −£64.2m | £236.7m | −£4.0m | £215m / net £40m profit (Sky Sports) |
| summer 2017 | £1.31bn | £635.1m | £1.41bn | £665.0m | £1.43bn / NOT FOUND (Sky News) |
| January 2018 | £346.2m | £98.2m | £419.5m | £147.6m | £430m / NOT FOUND (BBC Sport / Deloitte) |
| summer 2018 | £907.9m | £706.9m | — | — | £1.23bn / £865m (Sky News) |
| January 2019 | £109.6m | £54.5m | — | — | £180m / NOT FOUND (Sky Sports) |
| summer 2019 | £1.08bn | £489.3m | — | — | £1.41billion / £625m (PA, syndicated by Ex) |
| January 2020 | £121.0m | £119.7m | — | — | £230m / £165m (BBC Sport) |
| summer 2020 | £1.07bn | £696.5m | — | — | £1.24bn / £813million (PA (Tom White), synd) |
| January 2021 | £45.0m | £24.8m | — | — | £70m / NOT FOUND (Sky News) |
| summer 2021 | £829.4m | £435.1m | — | — | £1.1billion / £560m (PA, syndicated by Fo) |
| January 2022 | £188.0m | £78.7m | — | — | £295m / £180m (Sky News) |
| summer 2022 | £1.74bn | £988.3m | — | — | Estimates from Deloitte’s spor / NOT FOUND (The Guardian / Deloi) |
| January 2023 | £681.3m | £597.0m | — | — | around £780.1m / £675m (Sky Sports) |
| summer 2023 | £2.15bn | £978.4m | — | — | £2.44bn / £1.07bn (Sky Sports) |
| January 2024 | £86.0m | £75.2m | — | — | £96.2m / NOT FOUND (Sky Sports) |
| summer 2024 | £1.81bn | £592.4m | — | — | £2.08bn / £627.4m (Sky Sports) |
| January 2025 | £343.5m | £213.6m | — | — | around £370m / NOT FOUND (BBC Sport) |
| summer 2025 | £2.77bn | £1.19bn | — | — | surpassed £3bn; £3.087bn / NOT FOUND (BBC Sport) |
| January 2026 | £344.1m | £111.3m | — | — | £397m / NOT FOUND (BBC Sport) |
| summer 2026 | £3.07bn | £1.24bn | — | — | around £3.46 billion / NOT FOUND (Reuters, syndicated ) |

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

1. **Tier 1 is too big as worded (DEC-253).** 2,023 transfers are Tier 1, mostly because of the "changes the top-12 order" test. *Recommendation:* keep £20m+, records and disputed fees, and narrow the order test to "changes the leader, or who is in the top 12, at any month end"; the rest get Tier 2's scripted check.
2. **Undisclosed fees count £0 (DEC-237 (g)).** 2,197 transfers have no reported figure. *Recommendation:* keep the rule, say on screen "Undisclosed fees not included", and give each club's undisclosed count in the description.
3. **The early years are the least complete (1992–2007).** *Recommendation:* in phase 2, Claude in Cowork uses Transfermarkt in your Chrome only as a finding list (route A, nothing stored) to spot missing 1992–2007 deals involving the bigger fees, and takes each fee from a press or club source.
4. **Relegated clubs keep their frozen bar and their rank** (contract §1; e.g. a relegated club can sit 8th at the freeze). *Recommendation:* keep them in the ranking; how a frozen bar looks is a design question for the pilot (DEC-069).
5. **Start of the race.** At 31 May 1992 every bar is £0 (the leader that month is only a tie-break). *Recommendation:* the film starts at the first month end with a fee (July 1992); the data stay as they are.
6. **Same-grade fee disagreements on Tier 1 transfers:** 36 are listed in `conflicts.csv` (column `for_luke`). *Recommendation:* phase 2 settles each at source; the ones still open after that come back to you as a short list.
7. **Claude's working choices** DEC-247 (finding list), DEC-248 (tiers), DEC-249 (board size later), DEC-250 (build details) and DEC-254 (how the scripted check marks a fee VERIFIED, and publisher grades). *Recommendation:* confirm them.
8. **Phase 2 first batch.** *Recommendation:* verify the Tier 1 fees of the clubs that lead or reach the top 3 (Chelsea, Manchester United, Manchester City, Arsenal, Liverpool, Newcastle, Blackburn, Everton) first, in batches of 50 (`tier1_list.csv`, column `batch`).

## 10. Phase 2 (IQ-15b): verification at source

- **Tier 1 (DEC-256):** 2,006 fee-bearing Tier 1 transfers; **935 VERIFIED at source**, each quote read by Claude (858 quotes accepted, 57 rejected; `source/review_decisions.csv`). The rest have no page that states the figure next to the player's name yet (mostly 1990s–2000s deals whose only sources are Wikipedia figures or dead links).
- **Tier 2:** 275 of 675 VERIFIED by the scripted check. **Tier 3 sample:** 1 of 31 VERIFIED.
- **Undisclosed fees (DEC-257):** 31 grade A/B reported figures found at the cited source and read by Claude, used and flagged "reported" (30 transfers; 20 close candidates rejected on reading: another deal, grade D, not a fee, or a total with add-ons; `source/reported_fees.csv`); every other candidate figure on those pages belonged to another deal, a wage, an offer or a fine.
- **1992–2007 gap list (DEC-264), sections A v2, B and C (1992–2007):** 139 new moves added, 32 VERIFIED (the page names the player, both clubs and the fee); the rest matched transfers already in the build. 6 gap rows have no transfer date (retrospective articles only) and are listed in `unmatched_leads.csv`.
- **Leeds United 1992–2002** pages added; **last 1991–92 First Division matchday 2 May 1992** confirmed by eight club fixture lists (pointers, grade C).
- **Root causes found by reading the batches, and fixed in the build** (each fix applies to every row, not only the one seen): player names inside Wikipedia sort templates; the same deal listed twice; research leads matched on surname only (Kylian Hazard had been given Eden Hazard's fee); club-season tables whose direction was read from prose, plus a Wikipedia table labelled "From" in an "Out" section (Newcastle 1998–99); figures that are maxima, offers, valuations, instalments, combined fees or totals including add-ons; a regression that had dropped pre-2002 research-lead transfers (restored).

### Same-grade fee conflicts still open (DEC-261): 36

Settled at source = the fee used is confirmed at source and no differing same-grade figure is (totals including add-ons are not rivals). Still open = two same-grade sources confirm different figures, or the fee used is not yet confirmed.

| Player | From → To | Date | Fee used | Other confirmed figure(s) | Why open |
|---|---|---|---|---|---|
| Carlos Tevez | Media Sports Investments → Manchester City | 2009-07-14 | £25.0m (B) | B V according to reliable sources, £45m; B V around £25million; £45million claim denied; B V £25.5m | two same-grade sources confirm different figures |
| Cesc Fàbregas | Arsenal → Barcelona | 2011-08-15 | £25.4m (B) |  | the fee used is not yet confirmed at source |
| Julián Álvarez | Manchester City → Atlético Madrid | 2024-08-12 | £64.4m (B) |  | the fee used is not yet confirmed at source |
| Rodri | Manchester City → Barcelona | 2026-08-18 | £65.4m (B) | B V £65.4m; B V £65m; B V €60m | two same-grade sources confirm different figures |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £75.8m (B) | B V £62m; B V £71m; B V £75.8m | two same-grade sources confirm different figures |
| David Luiz | Chelsea → Paris Saint-Germain | 2014-06-13 | £40.0m (B) | B V £40m; B V £50m | two same-grade sources confirm different figures |
| Michael Turner | Hull City → Sunderland | 2009-08-31 | £12.0m (B) | B V £12m; B V £12m; believed to be in the region of £12m; B V £12million | two same-grade sources confirm different figures |
| Martín Zubimendi | Real Sociedad → Arsenal | 2025-07-06 | £60.0m (B) | B V almost £60m; B V £51m; B V £60m | two same-grade sources confirm different figures |
| Gareth Bale | Tottenham Hotspur → Real Madrid | 2013-09-01 | £85.3m (B) | B V 100m euros; B V Real claimed €91m; B V thought to be a world record figure of €100m | two same-grade sources confirm different figures |
| André-Frank Zambo Anguissa | Marseille → Fulham | 2018-08-09 | £30.0m (B) | B V Sky Sports News understands to be £22.3m; B V around £30m | two same-grade sources confirm different figures |
| Aleksandar Mitrović | Fulham → Al Hilal | 2023-08-19 | £50.0m (B) | B V 50 million euros; B V £50m | two same-grade sources confirm different figures |
| Willian | Anzhi Makhachkala → Chelsea | 2013-08-28 | £25.5m (B) | B V thought to be in the region of £25.5m; B V £32m | two same-grade sources confirm different figures |
| Alexander Hleb | VfB Stuttgart → Arsenal | 2005-06-27 | £11.2m (C) |  | the fee used is not yet confirmed at source |
| Granit Xhaka | Borussia Mönchengladbach → Arsenal | 2016-05-25 | £30.0m (B) | B V in the region of £30m; B V reported £35m; B V £35m | two same-grade sources confirm different figures |
| Arjen Robben | PSV → Chelsea | 2004-06-08 | £7.0m (C) |  | the fee used is not yet confirmed at source |
| Richarlison | Watford → Everton | 2018-07-24 | £35.0m (B) | B V around £40m; B V potential £50m deal | two same-grade sources confirm different figures |
| Fred | Shakhtar Donetsk → Manchester United | 2018-06-21 | £47.0m (B) | B V believed to be £52m; B V £47m | two same-grade sources confirm different figures |
| Petr Čech | Rennes → Chelsea | 2004-06-08 | £12.0m (C) |  | the fee used is not yet confirmed at source |
| Sofiane Boufal | Lille → Southampton | 2016-08-29 | £21.0m (B) | B V Sky sources understand the fee to be a club-record £16m; B V £21m according to sources at the south-coast club | two same-grade sources confirm different figures |
| Shaun Wright-Phillips | Manchester City → Chelsea | 2005-07-18 | £21.0m (B) |  | the fee used is not yet confirmed at source |
| Don Hutchison | Liverpool → West Ham United | 1994-08-30 | £1.5m (B) | B V pounds 1.5m; B V £5.3m | two same-grade sources confirm different figures |
| Henrikh Mkhitaryan | Borussia Dortmund → Manchester United | 2016-07-06 | £26.3m (B) | B V undisclosed fee believed to be £30m; B V £26.3m | two same-grade sources confirm different figures |
| Caleb Yirenkyi | Nordsjælland → Coventry City | 2026-08-07 | £23.0m (B) | B V £23.1m; B V £23m; B V £26m | two same-grade sources confirm different figures |
| Cesc Fàbregas | Barcelona → Chelsea | 2014-06-12 | £27.0m (B) |  | the fee used is not yet confirmed at source |
| Luke Shaw | Southampton → Manchester United | 2014-06-27 | £27.0m (B) | B V reported £30m; B V £27m; B V £27m; could rise to £31m | two same-grade sources confirm different figures |
| Christian Bassedas | Vélez Sársfield → Newcastle United | 2000-06-01 | £3.5m (B) |  | the fee used is not yet confirmed at source |
| Joseph Yobo | Marseille → Everton | 2003-05-23 | £1.0m (B) |  | the fee used is not yet confirmed at source |
| Matthew Upson | Arsenal → Birmingham City | 2003-01-22 | £3.0m (C) |  | the fee used is not yet confirmed at source |
| James Milner | Newcastle United → Aston Villa | 2008-08-29 | £12.0m (B) | B V believed to be in the region of £10m; B V £12m | two same-grade sources confirm different figures |
| Mustapha Hadji | Coventry City → Aston Villa | 2001-07-07 | £4.5m (C) |  | the fee used is not yet confirmed at source |
| Graeme Le Saux | Blackburn Rovers → Chelsea | 1997-08-08 | £5.0m (B) | B V pounds 5m; B V pounds 7m | two same-grade sources confirm different figures |
| Paolo Di Canio | Celtic → Sheffield Wednesday | 1997-08-06 | £4.5m (B) | B V pounds 3m; B V pounds 4.5m player-plus-cash deal | two same-grade sources confirm different figures |
| Didier Deschamps | Chelsea → Valencia | 2000-07-28 | £2.3m (C) |  | the fee used is not yet confirmed at source |
| Faustino Asprilla | Newcastle United → Parma | 1998-01-31 | £7.3m (B) | B V pounds 6m; B V pounds 7.3m | two same-grade sources confirm different figures |
| Nick Barmby | Middlesbrough → Everton | 1996-10-30 | £5.7m (B) | B V pounds 4.5m; B V pounds 5.3m; B V pounds 5.75m | two same-grade sources confirm different figures |
| Christos Tzolis | PAOK → Norwich City | 2021-08-12 | £8.8m (B) | B V around £10m; B V £8.8m | two same-grade sources confirm different figures |

### Effect of the 1992–2007 gap list (sections A v2, B, C) on window totals, 1997–2007

Our sums count fees paid by PL clubs (gross) and fees paid to minus received from non-PL clubs (net); undisclosed fees count £0. "Before" = the build just before sections A v2, B and C were added (`source/window_totals_before_gap_list_v2.csv`). Published totals are research leads (part17b, UNVERIFIED); none exist for windows before summer 2002 (no window system).

| Window | Gross before | Gross after | Change | Published gross (first A/B source) | Gap left | Net before | Net after |
|---|---|---|---|---|---|---|---|
| January 1997 | £41.5m | £41.5m | £0.0m | — | — | £12.4m | £12.4m |
| summer 1997 | £116.2m | £146.9m | £30.6m | — | — | £30.9m | £61.5m |
| January 1998 | £49.6m | £50.6m | £1.0m | — | — | £10.5m | £11.5m |
| summer 1998 | £128.7m | £161.6m | £32.9m | — | — | £49.4m | £80.0m |
| January 1999 | £82.6m | £93.7m | £11.1m | — | — | £28.6m | £36.2m |
| summer 1999 | £136.1m | £172.5m | £36.4m | — | — | £28.6m | £56.7m |
| January 2000 | £42.1m | £44.1m | £2.0m | — | — | £19.5m | £21.5m |
| summer 2000 | £241.3m | £246.7m | £5.4m | — | — | £97.1m | £94.2m |
| January 2001 | £58.6m | £64.2m | £5.5m | — | — | −£11.9m | −£6.4m |
| summer 2001 | £264.2m | £290.0m | £25.8m | — | — | £150.2m | £175.3m |
| January 2002 | £56.1m | £63.6m | £7.5m | — | — | £22.2m | £33.0m |
| summer 2002 | £174.2m | £173.0m | −£1.2m | — | — | £114.4m | £113.1m |
| January 2003 | £36.8m | £44.3m | £7.5m | £35.0m (B, The Independent) | −£9.3m | £14.2m | £21.7m |
| summer 2003 | £212.4m | £209.9m | −£2.5m | £215.0m (B, The Independent) | £5.1m | £120.3m | £116.8m |
| January 2004 | £61.1m | £44.0m | −£17.1m | — | — | £34.6m | £17.4m |
| summer 2004 | £172.0m | £206.0m | £34.0m | — | — | £99.3m | £129.5m |
| January 2005 | £41.2m | £44.0m | £2.8m | — | — | £12.8m | £15.6m |
| summer 2005 | £195.3m | £229.9m | £34.5m | £235.0m (B, The Independent) | £5.1m | £81.4m | £112.3m |
| January 2006 | £51.2m | £51.2m | £0.0m | — | — | £41.7m | £41.7m |
| summer 2006 | £239.8m | £244.6m | £4.7m | £300.0m (B, BBC News) | £55.5m | £118.4m | £123.1m |
| January 2007 | £37.5m | £40.5m | £3.0m | — | — | £17.9m | £17.9m |
| summer 2007 | £324.6m | £317.6m | −£7.0m | — | — | £166.2m | £159.2m |

Total gross 1997–2007: £2.76bn before, £2.98bn after (£216.8m added by the gap list). Where a published total exists, our sum stays below it mainly because undisclosed fees count £0 and the early Wikipedia window lists are short; the gap list narrows the gap but does not close it, and no figure is forced to match.
