# RTT-101 design inputs (for the design session; built by `scripts/rtt101_design_inputs.py`)

Nothing here is approved design. No visual feature or change to the approved look is built or rendered without Luke's approval (DEC-069). Figures are as built; the order at the freeze is not settled until Cowork's Tier 1 round (DEC-445).

## What the player reads

| File | Columns the player uses | Notes |
|---|---|---|
| `series_onscreen.csv` | `month_end`, `club_id`, `cum_net_gbp` (bar length and value), `rank`, `in_pl` (frozen-bar look), `pl_seasons_played`, `avg_real_net_per_season_gbp2026` (secondary statistic) | VERIFIED fees only (contract v1.5 §8, DEC-448); 413 month ends from 1992-05-31 to the freeze 2026-09-01 (1 Sep 2026, 23:00 BST); `rank` is blank before a club's first PL season |
| `clubs.csv` | `club_id`, `display_name` (bar label), `colour_key`, `logo_ref` | logos and colours: rights ledger and house style first |
| `pl_membership.csv`, `seasons.csv` | season windows, who is in the PL each season | a club out of the PL keeps its value, frozen |
| `coverage.csv` | undisclosed-fee count per club | for the "Undisclosed fees not included" note (DEC-429) |
| `club_ledger.csv` | `notes` (conversions), `fee_status` | for any "reported" or converted-fee note |
| `series_monthly.csv` | — | the all-fees preview: **not for screen** |

## Who leads (on screen)

- Arsenal: from 1992-05 to 1992-06
- Blackburn Rovers: from 1992-07 to 1995-06
- Liverpool: from 1995-07 to 1996-06
- Newcastle United: from 1996-07 to 1997-11
- Liverpool: from 1997-12 to 1998-01
- Newcastle United: from 1998-02 to 1999-06
- Liverpool: from 1999-07 to 2001-06
- Manchester United: from 2001-07 to 2001-07
- Liverpool: from 2001-08 to 2001-10
- Leeds United: from 2001-11 to 2002-05
- Liverpool: from 2002-06 to 2002-06
- Manchester United: from 2002-07 to 2003-06
- Chelsea: from 2003-07 to 2015-07
- Manchester City: from 2015-08 to 2022-07
- Chelsea: from 2022-08 to the freeze

Leader changes on screen: 14. In the preview (all fees) the sequence differs; see report section 19.

## Close calls on screen (leader ahead of second by under £3m at a month end)

- 1992-07 to 1992-10: Blackburn Rovers over Leeds United, smallest gap £1.26m
- 1992-11 to 1993-06: Blackburn Rovers over Manchester City, smallest gap £1.48m
- 1993-07: Blackburn Rovers over Manchester United, smallest gap £0.56m
- 1993-08: Blackburn Rovers over Aston Villa, smallest gap £0.01m
- 1993-09: Blackburn Rovers over Liverpool, smallest gap £1.33m
- 1995-03 to 1995-05: Blackburn Rovers over Liverpool, smallest gap £2.86m
- 1995-06: Blackburn Rovers over Arsenal, smallest gap £2.48m
- 1996-01: Liverpool over Blackburn Rovers, smallest gap £2.44m
- 1996-03 to 1996-06: Liverpool over Blackburn Rovers, smallest gap £2.24m
- 1997-07 to 1997-11: Newcastle United over Liverpool, smallest gap £0.84m
- 1997-12 to 1998-01: Liverpool over Newcastle United, smallest gap £0.46m
- 1998-02: Newcastle United over Liverpool, smallest gap £1.34m
- 1998-07: Newcastle United over Liverpool, smallest gap £1.14m
- 1998-10: Newcastle United over Everton, smallest gap £1.66m
- 2000-06: Liverpool over Chelsea, smallest gap £0.17m
- 2001-11 to 2002-05: Leeds United over Chelsea, smallest gap £2.82m

None after 2002-05.

## Negative bars in the top 12

On screen: none.
Preview: 1993-09 Oldham Athletic £-0.1m (a bar can go below zero only when a club's sales exceed its purchases; the axis must allow it).

## Clubs that reach the top 12 on screen: 30

AFC Bournemouth, Arsenal, Aston Villa, Birmingham City, Blackburn Rovers, Charlton Athletic, Chelsea, Coventry City, Crystal Palace, Everton, Fulham, Ipswich Town, Leeds United, Leicester City, Liverpool, Manchester City, Manchester United, Middlesbrough, Newcastle United, Nottingham Forest, Oldham Athletic, Queens Park Rangers, Sheffield Wednesday, Stoke City, Sunderland, Swindon Town, Tottenham Hotspur, West Bromwich Albion, West Ham United, Wolverhampton Wanderers.

## At the freeze (2026-09-01), on screen

| Rank | Club | Cumulative net spend | Average CPI-adjusted net per PL season (secondary) | PL seasons |
|---|---|---|---|---|
| 1 | Chelsea | £1,710.9m | £73.3m | 35 |
| 2 | Manchester City | £1,699.8m | £71.7m | 30 |
| 3 | Manchester United | £1,635.6m | £61.2m | 35 |
| 4 | Arsenal | £1,029.4m | £34.9m | 35 |
| 5 | Liverpool | £911.0m | £34.0m | 35 |
| 6 | Tottenham Hotspur | £841.9m | £28.4m | 35 |
| 7 | Newcastle United | £636.8m | £25.6m | 32 |
| 8 | West Ham United | £487.8m | £19.7m | 30 |
| 9 | Fulham | £381.9m | £24.0m | 20 |
| 10 | Aston Villa | £256.6m | £11.2m | 32 |
| 11 | Ipswich Town | £255.4m | £34.3m | 7 |
| 12 | Leeds United | £245.3m | £17.9m | 17 |

## What may still change

- **334 Tier 1 fees are UNVERIFIED** (`tier1_open.csv`; 42 involve Manchester United, Chelsea or Manchester City). Each one confirmed joins the on-screen bars; if all the leaders' unconfirmed fees were confirmed, Chelsea would fall by £56.1m, Manchester City by £52.9m and Manchester United rise by £40.3m, which would put United first at the freeze (as in the preview).
- Tier 2 and Tier 3 fees not yet confirmed stay off screen (DEC-448); further checks can add them.
- The 2,057 undisclosed fees stay £0 (no figure reported); the on-screen note covers them.
- CPI base: ONS D7BT August 2026; September 2026 is due on 21 Oct 2026 and would move the secondary statistic slightly if the build is re-run.
- Luke's open question (report section 19): confirmed fees only on screen, every tier.
