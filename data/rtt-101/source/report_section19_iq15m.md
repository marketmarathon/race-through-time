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
