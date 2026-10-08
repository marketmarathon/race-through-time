# RTT-101 Premier League net transfer spend — data report, phase 1 (IQ-15, 7 Oct 2026)

**Status: UNVERIFIED preview. Not for screen.** Only figures marked VERIFIED may ever be shown, and phase 2 (verification of Tier 1 at source, in batches) comes before any design work. Rules: `reference/metric_contract_RTT-101.md`; decisions DEC-235 to DEC-250 (and the findings recorded with this build).

Rebuild: `python3 scripts/build_rtt101_dataset.py && python3 scripts/rtt101_report.py` (deterministic; the private cross-checks need the private folder: `python3 scripts/rtt101_private_crosschecks.py <private research folder>` first).

## 1. What was built

- **13,013 transfer events** that involve a club in the Premier League that season (1992-93 to the freeze, 1 Sep 2026), of which **3,297 carry a fee** above £0. The rest are loans without a fee (5,330), free transfers (2,048), undisclosed fees with no figure, counted £0 (2,179), and fees not found (149).
- Fee status: **VERIFIED 1,582**, UNVERIFIED 1,715. Grade of the fee used: A 18, B 1,466, C (Wikipedia pointer only) 1,813, D 0.
- Tiers (DEC-248): Tier 1 **1,987**, Tier 2 674, Tier 3 652 (5% sample: 33).
  Tier 1 reasons (a transfer can have several): removal changes the leader or the top 12 1,077; fee >= £20m 548; club or British record (research lead) 526; disputed fee (research section C) 10; alternative fee version changes the leader or the top 12 5.
- 16,886 evidence rows in `fee_evidence.csv`; 2,943 sources in `sources.csv`; 426 transfers with more than one fee version (`conflicts.csv`).
- **Scripted source check** (GitHub runner, 4,522 cited pages): VERIFIED 3,885; page fetched but figure not found near the player's name 559; blocked or gone 78.
  Tier 2 result: 307 of 674 Tier 2 fees VERIFIED by the scripted check.
  Tier 3 sample: 5 of 33 VERIFIED; most Tier 3 rows have no fetchable citation (error rate cannot be published yet: phase 2).

## 2. Checks

| Check | Result | Detail |
|---|---|---|
| 22 clubs per season 1992-95, 20 after (706 club-seasons) | **PASS** | 706 club-seasons in 35 seasons |
| every season has an attribution window | **PASS** | 1992-05-03 to 2026-09-01 |
| 51 clubs, each with at least one PL season | **PASS** | 51 clubs |
| no transfer counted outside its club's PL seasons | **PASS** | 3734 ledger rows frozen (club not in the PL) |
| PL-to-PL deals net to zero (spend - income of PL clubs = net spend with non-PL clubs) | **PASS** | spend £27,744,593,188 − income £14,325,244,339 = £13,419,348,849; net with non-PL clubs £13,419,348,849 |
| no fee without a source row | **PASS** | 3297 fee-bearing transfers |
| no Transfermarkt figure or URL anywhere | **PASS** | none found |
| quotes under 25 words | **PASS** | 16886 evidence rows |
| every conversion has a rate row | **PASS** | 16 conversions |
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
| 1996-07-31 | Newcastle United | £37.8m |
| 1997-07-31 | Liverpool | £33.2m |
| 1998-03-31 | Newcastle United | £36.4m |
| 1999-07-31 | Liverpool | £57.0m |
| 2000-06-30 | Chelsea | £69.4m |
| 2000-07-31 | Liverpool | £74.0m |
| 2001-07-31 | Manchester United | £83.2m |
| 2001-08-31 | Liverpool | £81.7m |
| 2001-11-30 | Leeds United | £86.2m |
| 2002-07-31 | Manchester United | £91.0m |
| 2003-07-31 | Chelsea | £114.8m |
| 2015-08-31 | Manchester City | £626.7m |
| 2016-07-31 | Chelsea | £662.1m |
| 2016-08-31 | Manchester City | £788.3m |
| 2022-08-31 | Chelsea | £1.19bn |
| 2026-09-01 | Manchester United | £1.73bn |

## 4. Top 12 at key dates (UNVERIFIED preview)

**1993-05-31:** 1. Blackburn Rovers £5.5m; 2. Aston Villa £2.5m; 3. Manchester City £2.5m; 4. Sheffield Wednesday £2.0m; 5. Leeds United £1.9m; 6. Liverpool £0.9m; 7. Oldham Athletic £0.7m; 8. Chelsea £0.7m; 9. Ipswich Town £0.6m; 10. Manchester United £0.4m; 11. Arsenal £0.3m; 12. Newcastle United £0.0m

**1997-05-31:** 1. Newcastle United £37.0m; 2. Everton £20.9m; 3. Liverpool £20.7m; 4. Aston Villa £19.8m; 5. Middlesbrough £16.9m (out of the PL); 6. Chelsea £16.3m; 7. Arsenal £15.5m; 8. Coventry City £14.6m; 9. Leeds United £13.8m; 10. Sheffield Wednesday £12.6m; 11. Blackburn Rovers £9.9m; 12. Leicester City £8.9m

**2002-05-31:** 1. Leeds United £86.2m; 2. Chelsea £78.8m; 3. Liverpool £72.0m; 4. Newcastle United £68.0m; 5. Manchester United £63.0m; 6. Tottenham Hotspur £52.0m; 7. Middlesbrough £48.1m; 8. Aston Villa £45.4m; 9. Blackburn Rovers £45.3m; 10. Fulham £37.0m; 11. Arsenal £30.9m; 12. Manchester City £25.3m

**2005-05-31:** 1. Chelsea £282.9m; 2. Manchester United £120.0m; 3. Liverpool £102.3m; 4. Newcastle United £86.6m; 5. Tottenham Hotspur £79.5m; 6. Middlesbrough £78.3m; 7. Aston Villa £52.3m; 8. Manchester City £49.3m; 9. Sunderland £39.6m; 10. Blackburn Rovers £39.2m; 11. Arsenal £35.6m; 12. Birmingham City £28.9m

**2008-08-31:** 1. Chelsea £362.1m; 2. Liverpool £173.6m; 3. Manchester United £161.4m; 4. Tottenham Hotspur £124.0m; 5. Middlesbrough £121.8m; 6. Aston Villa £114.2m; 7. Newcastle United £105.2m; 8. Sunderland £79.7m; 9. Manchester City £79.5m; 10. Everton £49.1m; 11. Birmingham City £46.9m (out of the PL); 12. Fulham £46.6m

**2012-05-31:** 1. Chelsea £474.3m; 2. Manchester City £364.6m; 3. Liverpool £159.0m; 4. Tottenham Hotspur £131.3m; 5. Manchester United £123.5m; 6. Middlesbrough £121.7m (out of the PL); 7. Aston Villa £121.2m; 8. Sunderland £94.4m; 9. Birmingham City £75.4m (out of the PL); 10. Newcastle United £72.2m; 11. Everton £67.4m; 12. Stoke City £58.4m

**2016-08-31:** 1. Manchester City £788.3m; 2. Chelsea £704.6m; 3. Manchester United £540.4m; 4. Liverpool £286.6m; 5. Tottenham Hotspur £156.4m; 6. Arsenal £153.6m; 7. Sunderland £145.7m; 8. Middlesbrough £139.5m; 9. West Ham United £117.9m; 10. Aston Villa £116.3m (out of the PL); 11. Stoke City £112.7m; 12. Everton £99.0m

**2020-10-31:** 1. Manchester City £1.12bn; 2. Chelsea £981.0m; 3. Manchester United £842.8m; 4. Liverpool £419.1m; 5. Everton £395.6m; 6. Arsenal £358.0m; 7. Tottenham Hotspur £304.4m; 8. Aston Villa £283.1m; 9. West Ham United £234.4m; 10. Newcastle United £191.0m; 11. West Bromwich Albion £161.1m; 12. Fulham £148.8m

**2023-09-30:** 1. Chelsea £1.67bn; 2. Manchester United £1.30bn; 3. Manchester City £1.21bn; 4. Arsenal £743.6m; 5. Liverpool £628.4m; 6. Newcastle United £554.3m; 7. Tottenham Hotspur £498.7m; 8. West Ham United £424.3m; 9. Aston Villa £376.7m; 10. Everton £370.8m; 11. AFC Bournemouth £242.6m; 12. Fulham £183.5m

**2026-09-01:** 1. Manchester United £1.73bn; 2. Chelsea £1.67bn; 3. Manchester City £1.62bn; 4. Arsenal £1.17bn; 5. Liverpool £986.9m; 6. Tottenham Hotspur £946.7m; 7. Newcastle United £675.4m; 8. West Ham United £537.9m (out of the PL); 9. Everton £413.5m; 10. Fulham £334.3m; 11. Sunderland £306.0m; 12. Nottingham Forest £267.6m

## 5. Coverage by era

Counts are club-sides (a PL-to-PL deal counts once for each club).

| Era | Transfers found | With a fee | Fee grade A/B | Fee VERIFIED | Undisclosed, no figure | Fee not found |
|---|---|---|---|---|---|---|
| 1992-2002 (no window lists) | 2,178 | 1,454 | 540 | 653 | 33 | 94 |
| 2002-2007 | 1,179 | 473 | 92 | 177 | 143 | 13 |
| 2007-2012 | 2,972 | 419 | 179 | 165 | 670 | 10 |
| 2012-2017 | 3,052 | 523 | 269 | 247 | 567 | 10 |
| 2017-2022 | 2,120 | 418 | 272 | 256 | 486 | 19 |
| 2022-2026 | 3,091 | 779 | 577 | 553 | 533 | 20 |

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
| Rodri | Manchester City → Barcelona | 2026-08-18 | £65.4m (B) | £51.3m–£65.4m | 1 | yes |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £75.8m (B) | £62.0m–£75.8m | 1 | yes |
| Harry Kane | Tottenham Hotspur → Bayern Munich | 2023-08-12 | £100.0m (B) | £86.4m–£100.0m | 1 |  |
| Eliaquim Mangala | Porto → Manchester City | 2014-08-11 | £32.0m (B) | £32.0m–£42.0m | 1 |  |
| Richarlison | Everton → Tottenham Hotspur | 2022-07-01 | £50.0m (B) | £50.0m–£60.0m | 1 |  |
| David Luiz | Chelsea → Paris Saint-Germain | 2014-06-13 | £40.0m (B) | £40.0m–£50.0m | 1 | yes |
| Wayne Rooney | Everton → Manchester United | 2004-08-31 | £20.0m (B) | £20.0m–£30.0m | 1 |  |
| Casemiro | Real Madrid → Manchester United | 2022-08-22 | £60.0m (B) | £50.7m–£60.0m | 1 |  |
| Martín Zubimendi | Real Sociedad → Arsenal | 2025-07-06 | £60.0m (B) | £51.0m–£60.0m | 1 | yes |
| Gareth Bale | Tottenham Hotspur → Real Madrid | 2013-09-01 | £85.3m (B) | £76.6m–£85.3m | 1 | yes |
| Roberto Firmino | TSG Hoffenheim → Liverpool | 2015-06-24 | £29.0m (B) | £21.0m–£29.5m | 1 |  |
| Viktor Gyökeres | Sporting CP → Arsenal | 2025-07-26 | £55.1m (B) | £55.0m–£63.5m | 1 |  |
| Álvaro Morata | Chelsea → Atlético Madrid | 2020-07-01 | £58.8m (B) | £50.4m–£58.8m | 1 |  |
| James Milner | Aston Villa → Manchester City | 2010-08-18 | £26.0m (B) | £18.0m–£26.0m | 1 |  |
| Fernando Torres | Atlético Madrid → Liverpool | 2007-07-04 | £26.5m (B) | £18.5m–£26.5m | 1 |  |
| Diego Costa | Chelsea → Atlético Madrid | 2017-09-21 | £57.0m (B) | £50.0m–£58.0m | 1 |  |
| Michael Turner | Hull City → Sunderland | 2009-08-31 | £12.0m (B) | £4.0m–£12.0m | 1 | yes |
| Rasmus Højlund | Atalanta → Manchester United | 2023-08-05 | £64.0m (B) | £64.0m–£72.0m | 1 |  |

32 conflicts are for Luke in total (`conflicts.csv`, column `for_luke`).

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
| summer 2010 | £181.7m | £108.4m | — | — | around £350million / NOT FOUND (Sky Sports (reportin) |
| January 2011 | £195.4m | £76.1m | £209.3m | £77.3m | £225m / NOT FOUND (The Guardian (table ) |
| summer 2011 | £205.3m | £96.5m | — | — | NOT FOUND / £194m (The Guardian) |
| January 2012 | £42.7m | £0.7m | £67.4m | £24.5m | — |
| summer 2012 | £326.9m | £148.7m | — | — | around £490m / NOT FOUND (Sky News (reporting ) |
| January 2013 | £80.6m | £44.6m | £123.4m | £72.5m | £120m / £70m (Press Association (v) |
| summer 2013 | £552.2m | £346.8m | — | — | £630m / NOT FOUND (BBC Sport) |
| January 2014 | £118.8m | £36.0m | £128.8m | £26.9m | — |
| summer 2014 | £635.9m | £302.6m | £809.6m | £386.5m | £835m / £410m (Press Association (v) |
| January 2015 | £90.6m | £29.8m | £118.2m | £36.4m | £130million / around £40million (The Independent (Age) |
| summer 2015 | £743.1m | £381.2m | £858.6m | £432.6m | £870m / £460m (BBC Sport) |
| January 2016 | £103.6m | £43.6m | £177.5m | £108.9m | £175m / NOT FOUND (BBC Sport) |
| summer 2016 | £1.07bn | £701.3m | £1.12bn | £635.6m | £1.165bn / NOT FOUND (Sky Sports (reportin) |
| January 2017 | £140.5m | −£64.2m | £236.7m | −£4.0m | £215m / net £40m profit (Sky Sports) |
| summer 2017 | £1.31bn | £641.1m | £1.41bn | £665.0m | £1.43bn / NOT FOUND (Sky News) |
| January 2018 | £346.2m | £98.2m | £419.5m | £147.6m | £430m / NOT FOUND (BBC Sport / Deloitte) |
| summer 2018 | £907.9m | £706.9m | — | — | £1.23bn / £865m (Sky News) |
| January 2019 | £109.6m | £54.5m | — | — | £180m / NOT FOUND (Sky Sports) |
| summer 2019 | £1.08bn | £489.3m | — | — | £1.41billion / £625m (PA, syndicated by Ex) |
| January 2020 | £121.0m | £119.7m | — | — | £230m / £165m (BBC Sport) |
| summer 2020 | £1.07bn | £688.1m | — | — | £1.24bn / £813million (PA (Tom White), synd) |
| January 2021 | £45.0m | £24.8m | — | — | £70m / NOT FOUND (Sky News) |
| summer 2021 | £829.4m | £435.1m | — | — | £1.1billion / £560m (PA, syndicated by Fo) |
| January 2022 | £188.0m | £78.7m | — | — | £295m / £180m (Sky News) |
| summer 2022 | £1.73bn | £988.3m | — | — | Estimates from Deloitte’s spor / NOT FOUND (The Guardian / Deloi) |
| January 2023 | £654.8m | £570.5m | — | — | around £780.1m / £675m (Sky Sports) |
| summer 2023 | £2.15bn | £977.3m | — | — | £2.44bn / £1.07bn (Sky Sports) |
| January 2024 | £86.0m | £75.2m | — | — | £96.2m / NOT FOUND (Sky Sports) |
| summer 2024 | £1.81bn | £592.4m | — | — | £2.08bn / £627.4m (Sky Sports) |
| January 2025 | £343.5m | £213.6m | — | — | around £370m / NOT FOUND (BBC Sport) |
| summer 2025 | £2.83bn | £1.19bn | — | — | surpassed £3bn; £3.087bn / NOT FOUND (BBC Sport) |
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

1. **Tier 1 is too big as worded (DEC-253).** 1,987 transfers are Tier 1, mostly because of the "changes the top-12 order" test. *Recommendation:* keep £20m+, records and disputed fees, and narrow the order test to "changes the leader, or who is in the top 12, at any month end"; the rest get Tier 2's scripted check.
2. **Undisclosed fees count £0 (DEC-237 (g)).** 2,179 transfers have no reported figure. *Recommendation:* keep the rule, say on screen "Undisclosed fees not included", and give each club's undisclosed count in the description.
3. **The early years are the least complete (1992–2007).** *Recommendation:* in phase 2, Claude in Cowork uses Transfermarkt in your Chrome only as a finding list (route A, nothing stored) to spot missing 1992–2007 deals involving the bigger fees, and takes each fee from a press or club source.
4. **Relegated clubs keep their frozen bar and their rank** (contract §1; e.g. a relegated club can sit 8th at the freeze). *Recommendation:* keep them in the ranking; how a frozen bar looks is a design question for the pilot (DEC-069).
5. **Start of the race.** At 31 May 1992 every bar is £0 (the leader that month is only a tie-break). *Recommendation:* the film starts at the first month end with a fee (July 1992); the data stay as they are.
6. **Same-grade fee disagreements on Tier 1 transfers:** 32 are listed in `conflicts.csv` (column `for_luke`). *Recommendation:* phase 2 settles each at source; the ones still open after that come back to you as a short list.
7. **Claude's working choices** DEC-247 (finding list), DEC-248 (tiers), DEC-249 (board size later), DEC-250 (build details) and DEC-254 (how the scripted check marks a fee VERIFIED, and publisher grades). *Recommendation:* confirm them.
8. **Phase 2 first batch.** *Recommendation:* verify the Tier 1 fees of the clubs that lead or reach the top 3 (Chelsea, Manchester United, Manchester City, Arsenal, Liverpool, Newcastle, Blackburn, Everton) first, in batches of 50 (`tier1_list.csv`, column `batch`).

## 10. Phase 2 (IQ-15b): verification at source

- **Tier 1 (DEC-256):** 1,971 fee-bearing Tier 1 transfers; **1,216 VERIFIED at source** (1,078 by a club, league or press source, grade A/B; 138 only by a database such as Soccerbase, grade C; 0 only by a grade D site), each quote read by Claude (1,621 quotes accepted, 199 rejected; `source/review_decisions.csv`). The rest have no page that states the figure next to the player's name yet (mostly 1990s–2000s deals whose only sources are Wikipedia figures or dead links).
- **Tier 2:** 307 of 674 VERIFIED by the scripted check. **Tier 3 sample:** 5 of 33 VERIFIED.
- **Undisclosed fees (DEC-257):** 47 grade A/B reported figures found at the cited source and read by Claude, used and flagged "reported" (45 transfers; 33 close candidates rejected on reading: another deal, grade D, not a fee, or a total with add-ons; `source/reported_fees.csv`); every other candidate figure on those pages belonged to another deal, a wage, an offer or a fine.
- **1992–2007 gap list (DEC-264), sections A v2, B and C (1992–2007):** 137 new moves added, 72 VERIFIED (the page names the player, both clubs and the fee); the rest matched transfers already in the build. 6 gap rows have no transfer date (retrospective articles only) and are listed in `unmatched_leads.csv`.
- **Leeds United 1992–2002** pages added; **last 1991–92 First Division matchday 2 May 1992** confirmed by eight club fixture lists (pointers, grade C).
- **Root causes found by reading the batches, and fixed in the build** (each fix applies to every row, not only the one seen): player names inside Wikipedia sort templates; the same deal listed twice; research leads matched on surname only (Kylian Hazard had been given Eden Hazard's fee); club-season tables whose direction was read from prose, plus a Wikipedia table labelled "From" in an "Out" section (Newcastle 1998–99); figures that are maxima, offers, valuations, instalments, combined fees or totals including add-ons; a regression that had dropped pre-2002 research-lead transfers (restored); accented names not matched (ø, æ, ß and others); Soccerbase "Totals" lines and other rows of a career table read as this deal's fee (a Soccerbase figure now counts only from the row whose joining date is the transfer's); the same deal reported at two stages with a non-PL club not merged (Yobo, Baros); a reported figure attached to the same player's other moves.

### Same-grade fee conflicts not settled at source (DEC-261): 32, each settled by the contract's rule (DEC-277)

Settled at source = the fee used is confirmed at source and no differing same-grade figure is (totals including add-ons are not rivals). The deals below were not; Luke decided (DEC-277) that the existing rule settles them: best grade first, then the earliest report (a contemporary sterling figure from a grade A/B source preferred, contract §5). The last column says which step decided. Where no figure is confirmed at source yet, the fee stays UNVERIFIED (not on screen) and the deal is in the next research round.

| Player | From → To | Date | Fee used | Other confirmed figure(s) | Why not settled at source | Result under the rule (DEC-277) |
|---|---|---|---|---|---|---|
| Carlos Tevez | Media Sports Investments → Manchester City | 2009-07-14 | £25.0m (B) | B V according to reliable sources, £45m; B V around £25million; £45million claim denied; B V £25.5m | two same-grade sources confirm different figures | £25.0m (B, www.skysports.com): same grade; earliest report (2009-09-12) |
| Cesc Fàbregas | Arsenal → Barcelona | 2011-08-15 | £25.4m (B) |  | the fee used is not yet confirmed at source | £25.4m (B, www.bbc.co.uk): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Julián Álvarez | Manchester City → Atlético Madrid | 2024-08-12 | £64.4m (B) |  | the fee used is not yet confirmed at source | £64.4m (B, www.bbc.co.uk): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Rodri | Manchester City → Barcelona | 2026-08-18 | £65.4m (B) | B V £65.4m; B V £65m; B V €60m | two same-grade sources confirm different figures | £65.4m (B, www.skysports.com): same grade; the contemporary sterling figure is preferred (contract §5) |
| Kai Havertz | Bayer Leverkusen → Chelsea | 2020-09-04 | £75.8m (B) | B V £62m; B V £75.8m; B V €80m plus €20m in add-ons; £89m | two same-grade sources confirm different figures | £75.8m (B, www.skysports.com): same grade; the contemporary sterling figure is preferred (contract §5) |
| David Luiz | Chelsea → Paris Saint-Germain | 2014-06-13 | £40.0m (B) | B V £40m; B V £50m | two same-grade sources confirm different figures | £40.0m (B, www.bbc.co.uk): same grade; earliest report (2014-05-23) |
| Martín Zubimendi | Real Sociedad → Arsenal | 2025-07-06 | £60.0m (B) | B V almost £60m; B V £51m; B V £60m | two same-grade sources confirm different figures | £60.0m (B, www.bbc.co.uk): same grade; earliest report (2025-07-06) |
| Gareth Bale | Tottenham Hotspur → Real Madrid | 2013-09-01 | £85.3m (B) | B V 100m euros; B V Real claimed €91m; B V thought to be a world record figure of €100m | two same-grade sources confirm different figures | £85.3m (B, www.bbc.co.uk): same grade; the contemporary sterling figure is preferred (contract §5) |
| Michael Turner | Hull City → Sunderland | 2009-08-31 | £12.0m (B) | B V £12m; B V £12m; believed to be in the region of £12m; B V £12million | two same-grade sources confirm different figures | £12.0m (B, www.theguardian.com): same grade; earliest report (2009-08-31) |
| André-Frank Zambo Anguissa | Marseille → Fulham | 2018-08-09 | £30.0m (B) | B V Sky Sports News understands to be £22.3m; B V around £30m | two same-grade sources confirm different figures | £30.0m (B, www.theguardian.com): same grade; earliest report (2018-08-09) |
| Aleksandar Mitrović | Fulham → Al Hilal | 2023-08-19 | £50.0m (B) | B V 50 million euros; B V £50m | two same-grade sources confirm different figures | £50.0m (B, www.bbc.co.uk): same grade; earliest report (2023-08-19) |
| Willian | Anzhi Makhachkala → Chelsea | 2013-08-28 | £25.5m (B) | B V thought to be in the region of £25.5m; B V £32m | two same-grade sources confirm different figures | £25.5m (B, www.skysports.com): same grade; earliest report (2013-08-28) |
| Timo Werner | RB Leipzig → Chelsea | 2020-07-01 | £53.0m (B) | B V £47.5m; B V £53m release clause | two same-grade sources confirm different figures | £53.0m (B, www.theguardian.com): same grade; earliest report (2020-06-04) |
| Alexander Hleb | VfB Stuttgart → Arsenal | 2005-06-27 | £11.2m (C) |  | the fee used is not yet confirmed at source | £11.2m (C, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Granit Xhaka | Borussia Mönchengladbach → Arsenal | 2016-05-25 | £30.0m (B) | B V in the region of £30m; B V reported £35m | two same-grade sources confirm different figures | £30.0m (B, www.skysports.com): same grade; earliest report (2016-05-25) |
| Arjen Robben | PSV → Chelsea | 2004-06-08 | £7.0m (C) |  | the fee used is not yet confirmed at source | £7.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Richarlison | Watford → Everton | 2018-07-24 | £35.0m (B) | B V around £40m; B V potential £50m deal | two same-grade sources confirm different figures | £35.0m (B, www.bbc.co.uk): same grade; earliest report (2018-07-24) |
| Fred | Shakhtar Donetsk → Manchester United | 2018-06-21 | £47.0m (B) | B V believed to be £52m; B V £47m | two same-grade sources confirm different figures | £47.0m (B, www.bbc.co.uk): same grade; earliest report (2018-06-21) |
| Petr Čech | Rennes → Chelsea | 2004-06-08 | £12.0m (C) |  | the fee used is not yet confirmed at source | £12.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Sofiane Boufal | Lille → Southampton | 2016-08-29 | £21.0m (B) | B V Sky sources understand the fee to be a club-record £16m; B V £21m according to sources at the south-coast club | two same-grade sources confirm different figures | £21.0m (B, www.skysports.com): same grade; earliest report (2016-08-25) |
| Álvaro Negredo | Manchester City → Valencia | 2015-06-08 | £21.3m (B) | B V £20m; B V £21.3m; B V £23.7m | two same-grade sources confirm different figures | £21.3m (B, www.skysports.com): same grade; earliest report (2015-07-01) |
| Shaun Wright-Phillips | Manchester City → Chelsea | 2005-07-18 | £21.0m (B) |  | the fee used is not yet confirmed at source | £21.0m (B, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Henrikh Mkhitaryan | Borussia Dortmund → Manchester United | 2016-07-06 | £26.3m (B) | B V undisclosed fee believed to be £30m; B V £26.3m | two same-grade sources confirm different figures | £26.3m (B, www.skysports.com): same grade; earliest report (2016-07-06) |
| Cesc Fàbregas | Barcelona → Chelsea | 2014-06-12 | £27.0m (B) |  | the fee used is not yet confirmed at source | £27.0m (B, www.theguardian.com): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Luke Shaw | Southampton → Manchester United | 2014-06-27 | £27.0m (B) | B V reported £30m; B V £27m; B V £27m; could rise to £31m | two same-grade sources confirm different figures | £27.0m (B, www.bbc.co.uk): same grade; earliest report (2014-06-26) |
| Christian Bassedas | Vélez Sársfield → Newcastle United | 2000-06-01 | £3.5m (B) | B V £0.5m; B V £3.5m | two same-grade sources confirm different figures | £3.5m (B, www.theguardian.com): same grade; earliest report (2000-06-01) |
| Matthew Upson | Arsenal → Birmingham City | 2003-01-22 | £3.0m (C) |  | the fee used is not yet confirmed at source | £3.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| James Milner | Newcastle United → Aston Villa | 2008-08-29 | £12.0m (B) | B V believed to be in the region of £10m; B V £12m | two same-grade sources confirm different figures | £12.0m (B, www.theguardian.com): same grade; earliest report (2008-08-29) |
| Pascal Chimbonda | Wigan Athletic → Tottenham Hotspur | 2006-08-31 | £6.0m (C) |  | the fee used is not yet confirmed at source | £6.0m (C, en.wikipedia.org): no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is |
| Faustino Asprilla | Newcastle United → Parma | 1998-01-31 | £7.3m (B) | B V pounds 6m; B V pounds 7.3m | two same-grade sources confirm different figures | £7.3m (B, www.independent.co.uk): same grade; earliest report (1998-01-15) |
| Nick Barmby | Middlesbrough → Everton | 1996-10-30 | £5.7m (B) | B V pounds 4.5m; B V pounds 5.3m; B V pounds 5.75m | two same-grade sources confirm different figures | £5.7m (B, www.the-independent.com): same grade; earliest report (1996-11-17) |
| Christos Tzolis | PAOK → Norwich City | 2021-08-12 | £8.8m (B) | B V around £10m; B V £8.8m | two same-grade sources confirm different figures | £8.8m (B, www.bbc.co.uk): same grade; earliest report (2021-08-12) |

### Effect of the 1992–2007 gap list (sections A v2, B, C) on window totals, 1997–2007

Our sums count fees paid by PL clubs (gross) and fees paid to minus received from non-PL clubs (net); undisclosed fees count £0. "Before" = the build just before sections A v2, B and C were added (`source/window_totals_before_gap_list_v2.csv`). Published totals are research leads (part17b, UNVERIFIED); none exist for windows before summer 2002 (no window system).

"Change" also includes the corrections made by reading the sources since that snapshot (for example a maximum replaced by the guaranteed fee); "of which gap list" is the gross paid by PL clubs in all moves the gap list created (section A's first version, part18b, was already in the snapshot, so this column can exceed the change).

| Window | Gross before | Gross after | Change | of which gap list | Published gross (first A/B source) | Gap left | Net before | Net after |
|---|---|---|---|---|---|---|---|---|
| January 1997 | £41.5m | £43.5m | £2.0m | £14.7m | — | — | £12.4m | £12.7m |
| summer 1997 | £116.2m | £144.4m | £28.1m | £28.6m | — | — | £30.9m | £59.0m |
| January 1998 | £49.6m | £51.2m | £1.6m | £1.0m | — | — | £10.5m | £12.1m |
| summer 1998 | £128.7m | £162.6m | £33.9m | £32.9m | — | — | £49.4m | £80.7m |
| January 1999 | £82.6m | £93.7m | £11.1m | £11.1m | — | — | £28.6m | £36.2m |
| summer 1999 | £136.1m | £172.5m | £36.4m | £36.4m | — | — | £28.6m | £56.7m |
| January 2000 | £42.1m | £43.8m | £1.7m | £2.0m | — | — | £19.5m | £21.2m |
| summer 2000 | £241.3m | £245.8m | £4.5m | £17.2m | — | — | £97.1m | £92.3m |
| January 2001 | £58.6m | £64.3m | £5.7m | £5.5m | — | — | −£11.9m | −£8.4m |
| summer 2001 | £264.2m | £289.4m | £25.2m | £32.8m | — | — | £150.2m | £173.7m |
| January 2002 | £56.1m | £60.2m | £4.2m | £6.3m | — | — | £22.2m | £29.6m |
| summer 2002 | £174.2m | £174.7m | £0.5m | £0.0m | — | — | £114.4m | £115.4m |
| January 2003 | £36.8m | £39.8m | £3.0m | £3.0m | £35.0m (B, The Independent) | −£4.8m | £14.2m | £17.2m |
| summer 2003 | £212.4m | £204.9m | −£7.6m | £0.0m | £215.0m (B, The Independent) | £10.1m | £120.3m | £119.2m |
| January 2004 | £61.1m | £44.0m | −£17.1m | £0.0m | — | — | £34.6m | £17.4m |
| summer 2004 | £172.0m | £204.3m | £32.3m | £33.0m | — | — | £99.3m | £131.8m |
| January 2005 | £41.2m | £44.0m | £2.8m | £2.8m | — | — | £12.8m | £15.6m |
| summer 2005 | £195.3m | £229.4m | £34.0m | £28.4m | £235.0m (B, The Independent) | £5.6m | £81.4m | £112.3m |
| January 2006 | £51.2m | £51.1m | −£0.1m | £0.0m | — | — | £41.7m | £41.6m |
| summer 2006 | £239.8m | £240.9m | £1.1m | £4.7m | £300.0m (B, BBC News) | £59.0m | £118.4m | £122.0m |
| January 2007 | £37.5m | £39.8m | £2.4m | £3.0m | — | — | £17.9m | £17.2m |
| summer 2007 | £324.6m | £321.0m | −£3.6m | £0.0m | — | — | £166.2m | £162.6m |

Total gross 1997–2007: £2.76bn before, £2.97bn after (£202.0m net change, of which £263.3m paid in moves the gap list added). Where a published total exists, our sum stays below it mainly because undisclosed fees count £0 and the early Wikipedia window lists are short; the gap list narrows the gap but does not close it, and no figure is forced to match.

### Leader sequence after phase 2

Leader at each change (month end): 1992-05 Arsenal; 1992-07 Blackburn Rovers; 1993-07 Liverpool; 1993-09 Blackburn Rovers; 1995-07 Liverpool; 1996-07 Newcastle United; 1997-07 Liverpool; 1998-03 Newcastle United; 1999-07 Liverpool; 2000-06 Chelsea; 2000-07 Liverpool; 2001-07 Manchester United; 2001-08 Liverpool; 2001-11 Leeds United; 2002-07 Manchester United; 2003-07 Chelsea; 2015-08 Manchester City; 2016-07 Chelsea; 2016-08 Manchester City; 2022-08 Chelsea; 2026-09 Manchester United.


### Phase 2 questions — answered by Luke (YES to all four, 7 Oct 2026: DEC-274 to DEC-277)

1. **Database-only Tier 1 figures.** 138 Tier 1 fees are confirmed only by a grade C source (138 of them a Soccerbase row for that move) and 0 only by a source graded D (mostly later retrospective articles). May a Soccerbase row count as VERIFIED for screen? *Recommendation:* yes for Soccerbase rows (they are dated career tables, checked row by row), no for grade D; keep looking for press sources for both.
2. **Next research round.** 893 Tier 1 fees still have no VERIFIED club, league or press source (`data/rtt-101/tier1_needs_press_source.csv`, mostly 1992–2007). *Recommendation:* one more ChatGPT deep-research round on that list (a press or club URL and a short quote per deal, leads only; every figure checked at source here), starting with 1992–2002.
3. **Fees known only as a maximum or an approximation.** 14 deals count £0 because every figure found is a maximum, a total including add-ons, or an approximation ("just under £30m", "in excess of £13m", "£40m-plus"). *Recommendation:* keep £0 (DEC-237 (e)) and add these deals to the next research round to find the guaranteed fee.
4. **Same-grade conflicts.** 32 remain (table above). *Recommendation:* use the rule already in the contract (highest grade, then the earliest contemporary report) for all of them, and list them in the description notes; Luke can overrule any single deal.

**Luke's answers:** (1) a Soccerbase row counts as VERIFIED, grade C, labelled "database source" (`transfers.csv` column `verified_by`); other grade C and grade D sources do not confirm a fee (DEC-274). (2) One more ChatGPT deep-research round on `tier1_needs_press_source.csv`, starting with 1992–2002; every figure is a lead to check at source here (DEC-275). (3) The deals known only as a maximum or an approximation stay at £0 and are listed in `data/rtt-101/tier1_max_or_approx_only.csv` for a later round (DEC-276). (4) The same-grade conflicts are settled by the rule, with the result for each in the table above (DEC-277).

## 11. Source round 1, list A: 1992–93 to 1996–97 (DEC-275, IQ-15d)

- **Deals:** 211 (A0001–A0211), mapped to our transfers by player and date (`source/source_round1_map.csv`). ChatGPT's answers (private part20b/d/f) were added as leads (`found_via` of each evidence row: "ChatGPT source round 1 (DEC-264 route)") and every cited page was read on the GitHub runner: the figure next to the player's name, and both clubs named on the page.
- **VERIFIED:** 155 of the 211 deals now have a fee confirmed at source (141 by a club, league or press source; the rest by a Soccerbase row), up from 41 before this round.
- **Changed:** 59 fees changed (£7.7m up, £13.3m down; net −£5.6m) and 14 completion dates moved to the date a grade B report gives.
- **Deal structures** (`source/deal_structure.csv`, one row per transfer with its source, quote and rule): a combined fee is booked once on one transfer of the pair and the partner counts £0 (no split invented); a part-exchange counts a player valuation on both sides only where a source states it, otherwise cash only; add-ons count only when reported as payable; a loan fee is a loan fee.

| Deal | Player | Move | Date before → after | Fee before | Fee after | Why |
|---|---|---|---|---|---|---|
| A0001 | Darren Anderton | Portsmouth → Tottenham Hotspur | 1992-07-01 | £1,750,000 | £1,700,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0004 | Mal Donaghy | Manchester United → Chelsea | 1992-07-01 | £100,800 | £150,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0006 | Scott Sellars | Blackburn Rovers → Leeds United | 1992-07-01 | £800,000 | £720,000 | sell-on (DEC-238): the buyer was the former club holding the sell-on share, so the cash both clubs saw was £720,000 |
| A0007 | Jason Cundy | Chelsea → Tottenham Hotspur | 1992-07-02 | £850,000 | £800,000 | higher grade or earlier report (C, www.independent.co.uk) |
| A0009 | David Lowe | Ipswich Town → Leicester City | 1992-07-13 | £300,000 | £250,000 | higher grade or earlier report (B, www.the-independent.com) |
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
| A0082 | Paul Kitson | Derby County → Newcastle United | 1994-09-26 | £2,250,000 | £2,500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0085 | Efan Ekoku | Norwich City → Wimbledon | 1994-10-14 | £900,000 | £920,000 | higher grade or earlier report (C, www.independent.co.uk) |
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
| A0165 | Julian Joachim | Leicester City → Aston Villa | 1996-02-24 | £1,890,000 | £1,500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0171 | Garry Flitcroft | Manchester City → Blackburn Rovers | 1996-03-28 | £3,500,000 | £3,200,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0173 | Alex Rae | Millwall → Sunderland | 1996-06-01 | £1,000,000 | £750,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0174 | Gary Speed | Leeds United → Everton | 1996-07-01 → 1996-06-21 | £3,500,000 | £3,500,000 | completion date from a grade B report (contract §2) |
| A0176 | Ben Thatcher | Millwall → Wimbledon | 1996-07-05 → 1996-07-03 | £1,700,000 | £1,700,000 | completion date from a grade B report (contract §2) |
| A0177 | Matt Clarke | Rotherham United → Sheffield Wednesday | 1996-07-11 | £325,000 | £300,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0184 | Scott Oakes | Luton Town → Sheffield Wednesday | 1996-08-07 | £425,000 | £700,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0189 | Patrick Vieira | AC Milan → Arsenal | 1996-08-31 | £3,500,000 | £4,000,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0191 | Steffen Iversen | Rosenborg → Tottenham Hotspur | 1996-12-02 → 1996-12-05 | £2,500,000 | £2,600,000 | completion date from a grade B report (contract §2) |
| A0194 | Ramon Vega | Cagliari → Tottenham Hotspur | 1997-01-07 | £3,750,000 | £3,000,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0205 | John Hartson | Arsenal → West Ham United | 1997-02-14 | £3,300,000 | £5,000,000 | higher grade or earlier report (B, www.the-independent.com) |
| A0208 | Des Hamilton | Bradford City → Newcastle United | 1997-03-27 | £1,500,000 | £2,500,000 | higher grade or earlier report (B, www.independent.co.uk) |
| A0211 | Mark McKeever | Peterborough United → Sheffield Wednesday | 1997-04-15 | £500,000 | £0 | combined fee (DEC-237 (e)): booked once on one transfer of the pair; no split is invented |

**Same-grade disagreements within list A** (9 deals; all below the 10% and £1m threshold of Luke's conflict list, so the rule settles them: best grade, then the earliest report, DEC-277; a report with no stated date ranks after a dated one):

| Deal | Player | Fee used (report date) | Other confirmed figure(s), same grade (report date) |
|---|---|---|---|
| A0009 | David Lowe | £250,000 (B, 1992-07-21) | £200,000 (1992-08-07) |
| A0056 | Andy Preece | £350,000 (B, 1994-06-24) | £275,000 (1994-10-24) |
| A0082 | Paul Kitson | £2,500,000 (B, 1994-09-24) | £2,250,000 (1994-10-24) |
| A0110 | Brett Angell | £500,000 (B, 1995-03-23) | £600,000 (1995-03-24) |
| A0160 | Slaven Bilic | £1,200,000 (B, 1996-01-04) | £1,650,000 (1996-01-18) |
| A0164 | David Batty | £3,750,000 (B, 1996-02-26) | £4,000,000 (1996-03-01) |
| A0169 | Ilie Dumitrescu | £1,500,000 (B, 1996-01-19) | £1,200,000 (1996-02-27) |
| A0180 | Nigel Martyn | £2,250,000 (B, 1996-07-25) | £2,100,000 (1996-07-30) |
| A0194 | Ramon Vega | £3,000,000 (B, 1997-01-07) | £3,700,000 (1997-01-13), £3,750,000 (1997-01-20) |

**League-wide spending by window, 1992–97** (before = commit 111a018; there are no published window totals for these years, when there were no transfer windows, so nothing to compare against):

| Window | Gross before | Gross after | Change |
|---|---|---|---|
| summer 1992 | £34.1m | £33.9m | −£0.2m |
| January 1993 | £9.1m | £9.1m | £0.0m |
| summer 1993 | £39.6m | £39.2m | −£0.4m |
| January 1994 | £16.2m | £16.1m | −£0.1m |
| summer 1994 | £73.3m | £71.7m | −£1.6m |
| January 1995 | £41.6m | £41.1m | −£0.5m |
| summer 1995 | £109.4m | £108.1m | −£1.4m |
| January 1996 | £54.6m | £52.8m | −£1.8m |
| summer 1996 | £102.8m | £103.3m | £0.5m |
| January 1997 | £41.5m | £43.5m | £2.0m |

**Effect on the race:** the leader changes at 7 month ends (1998-02: Newcastle United → Liverpool; 2000-01: Newcastle United → Liverpool; 2000-02: Newcastle United → Liverpool; 2003-03: Newcastle United → Manchester United; 2003-04: Newcastle United → Manchester United; 2003-05: Newcastle United → Manchester United; 2003-06: Newcastle United → Manchester United); who is in the top 12 changes at 30 month ends (1992-08: in Manchester United, out Everton; 1992-09: in Manchester United, out Sheffield United; 1992-10: in Manchester United, out Sheffield United; 1993-06: in Manchester United, out Swindon Town; 1993-08: in Ipswich Town, out Oldham Athletic; 1994-06: in Swindon Town, out West Ham United; 1994-07: in Crystal Palace, out West Ham United; 1994-08: in Leicester City, out West Ham United; 1994-09: in Leicester City, out West Ham United; 1995-03: in Sheffield Wednesday, out Ipswich Town …); the order within the top 12 changes at 154 month ends.

**Questions for Luke on list A (each with Claude's recommendation)**

1. **Combined fees.** One payment for two players (Charles and Tommy Johnson £2.9m; McKee and Whitworth £530,000; Billington and McKeever £500,000) is booked once, on one transfer of the pair, and the partner counts £0. Each club's total is exact and no split is invented. *Recommendation:* keep it.
2. **Parker and Carr (Villa ↔ Leicester, Feb 1995).** The only source values "the deal" at £550,000 without saying how much was cash. We count £550,000 for Parker and £0 for Carr. *Recommendation:* keep it, and ask the next research round for the cash figure.
3. **Andy Cole (Feb 1995).** A grade B source values Keith Gillespie at £1m in the deal, so under DEC-237 (d) Cole counts £7m (£6m cash plus Gillespie) and Gillespie £1m; Manchester United's net is still the £6m cash. *Recommendation:* keep it (it follows the rule Luke approved).
