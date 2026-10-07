# Metric contract — RTT-101 Premier League net transfer spend · v1.0 (data build IQ-15, phase 1) · 7 Oct 2026

Written before the data build (DEC-036). Owner decisions: DEC-235 to DEC-240 (Luke, 4–7 Oct 2026) and DEC-245 (no contact about data). Claude's working choices, each a question for Luke: DEC-247 to DEC-250. Brief: `prompts/CODE_SESSION_IQ-15.md`.

**Public claim (title wording, DEC-237 (f)):** cumulative net spend on **reported transfer fees** by every Premier League club, month by month, from the start of the first Premier League season (1992–93) to the close of the summer 2026 transfer window (1 Sep 2026, 11pm BST). Figures will be updated after the January 2027 window (on-screen/description note, DEC-237 (b)).

**Unit (main bars):** pounds sterling, **nominal** (never inflation-adjusted), fees paid minus fees received, cumulative. May be negative.
**Secondary statistic:** average CPI-adjusted net spend per PL season played, in "2026 £" (label "(2026 £)").
**Timeline:** one value per club at every month end from 31 May 1992 to 31 Aug 2026, plus a final point at the freeze, 1 Sep 2026 23:00 BST (DEC-250 (b)).
**Rank:** descending cumulative nominal net at each month end; ties: the club that reached the value earlier ranks higher. Bars are frozen outside the PL.

## 1. What counts (DEC-235, DEC-237, DEC-238, DEC-240)

| Item | Counted? | Rule |
|---|---|---|
| Permanent transfer fee | yes | guaranteed fee, on the transfer date |
| Explicit loan fee | yes | on the loan date |
| Purchase after a loan (option or obligation exercised) | yes | separate row, dated when exercised (`parent_transfer_id` = the loan) |
| Transfer / registration compensation, tribunal fee | yes | at the decision date (or the agreement date) |
| Add-ons | only when payable | only when a club or grade B source reports them triggered/payable, dated when payable; "up to £X" is never the fee (DEC-237 (e)) |
| Sell-on payment to a former club | yes, when stated | deducted from the seller's receipt only when a club or grade B source states the amount; otherwise the headline fee counts. If the former club is in the PL on that date it is that club's income on the date reported (DEC-238) |
| Part-exchange | valuation if stated | a stated player valuation counts on both sides; otherwise cash only (DEC-237 (d)) |
| Free transfer | £0 | counted as a transfer with fee £0 |
| Undisclosed fee | reported or £0 | a grade B reported figure is used and flagged "reported"; otherwise £0 and counted in the per-club undisclosed report (DEC-237 (g)) |
| Wages, agents' fees, signing bonuses, levies, market values | **no** | never |

**PL activity only.** A transfer counts for a club only if that club plays in the PL in the season the transfer is attributed to. PL-to-PL deals count at both ends; deals with non-PL or foreign clubs count only for the PL club.

## 2. Season attribution and dating (DEC-237 (c))
- **Season N** runs from the day after the last PL matchday of season N−1 to the last PL matchday of season N. 1992–93 starts on the day after the last 1991–92 First Division matchday. 2015–16 ends 17 May 2016 (the replayed match). 2026–27 runs to the freeze (1 Sep 2026, 23:00 BST). Windows: `data/rtt-101/seasons.csv`.
- **Date:** completion/registration date; else official announcement; else first grade A/B report. Recorded in `date_basis`. A month-only date goes to that month's last day, never spread.
- Transfers dated after the freeze are excluded; transfers before the start of 1992–93 are not counted (every bar starts at £0, DEC-250 (a)).

## 3. Evidence grades and the canonical fee
- **A** = the club's or the league's own statement. **B** = high-quality contemporary press (BBC, Sky, Guardian, Times, Telegraph, Independent, PA, Reuters…). UEFA.com news reporting another party's fee = **B**. Any row a source itself calls "reported"/"thought to be" is reported (B), whatever grade a research file gave it. **C** = specialist databases and Wikipedia (pointers only). **D** = secondary or reconstructed.
- **Canonical fee** when sources disagree: highest grade; within a grade, the earliest contemporary report. **Never averaged.** Every version is kept in `fee_evidence.csv`; same-grade disagreements over 10% and £1m on Tier 1 transfers are listed for Luke.
- **Transfermarkt is never a source** (DEC-236): nothing from it is stored; a Wikipedia fee whose only citation is Transfermarkt is not used (DEC-250 (c)).
- **Status:** VERIFIED (the figure was seen at its source by a script, a runner or Claude in Cowork, with a quote) / UNVERIFIED / NOT FOUND. **Only VERIFIED figures go on screen.** Phase 1 builds an UNVERIFIED preview series (not for screen); phase 2 verifies Tier 1 at source.

## 4. Verification tiers (DEC-237 (f), DEC-248)
| Tier | Which transfers | Check |
|---|---|---|
| 1 | fee ≥ £20m nominal; every club or British record; every disputed fee; every transfer whose removal or alternative version changes the top-12 order in any month (computed) | at source by hand (phase 2, batches from `tier1_list.csv`) |
| 2 | £2m to under £20m | scripted: the cited source is fetched and must state the figure |
| 3 | under £2m | 5% random sample (fixed seed), error rate published |

## 5. Currency (DEC-239, DEC-240)
- A contemporary GBP figure from a grade A/B source is always preferred.
- Otherwise: convert at the Bank of England daily spot for the transfer date (monthly average if no daily); store original amount, currency, rate, rate date and series code. Pre-1999 legacy currencies: Bank of England rate for the date or month; only the GBP result is shown, with a note of the rate. ECB GBP/EUR (from Jan 1999) is a cross-check only. A modern reconstructed euro figure is never converted at today's rate.
- Series codes: `data/rtt-101/fx.csv`.

## 6. CPI (secondary statistic only)
`fee_real = fee × CPI(base) ÷ CPI(month of transfer)`, ONS D7BT (CPI index, 2015 = 100). Base = the latest D7BT month published at the freeze (August 2026 unless September 2026 is published when the build runs; the build records which). Main bars are never adjusted.

**PL seasons played:** the seasons whose attribution window has begun while the club is in the PL. The average is shown once a club has at least one season: `sum(real net in its PL seasons) ÷ seasons played`.

## 7. Clubs and identity
One `club_id` per club; other names in `clubs.csv`. **Wimbledon FC (PL 1992–2000) is a different club from AFC Wimbledon and Milton Keynes Dons**; neither inherits Wimbledon FC's total. 51 PL clubs to 2026–27 (V-11, Wikipedia; checked against our own membership table). The dataset keeps all 51 clubs; the board size is a design question (DEC-249, DEC-069).

## 8. Display attributes (DEC-036; built in a later player session only — DEC-069)

| Attribute | Source | File / column |
|---|---|---|
| Club name (bar label) | club's common English name | `clubs.csv` `display_name` |
| Other names (search, matching) | Wikipedia article titles, earlier names | `clubs.csv` `other_names` |
| Cumulative net spend, nominal (bar length and value) | method above, from VERIFIED fees only on screen | `series_monthly.csv` `cum_net_gbp` |
| Average CPI-adjusted net per PL season (secondary) | method §6; ONS D7BT (OGL v3) | `series_monthly.csv` `avg_real_net_per_season_gbp2026` |
| PL seasons played | `pl_membership.csv`, `seasons.csv` | `series_monthly.csv` `pl_seasons_played` |
| In / out of the PL (frozen bar look) | `pl_membership.csv` | `series_monthly.csv` `in_pl` |
| Month / date shown | month end, final point at the freeze | `series_monthly.csv` `month_end` |
| Rank | method above | `series_monthly.csv` `rank` |
| Source line (on screen and description) | "Reported transfer fees from club statements and press reports; CPI: ONS; exchange rates: Bank of England" — wording for a design round | — |
| Notes for "reported" and converted fees | `transfers.csv` `fee_status`, `fx_*` | `club_ledger.csv` `notes` |
| Undisclosed-fee count per club | `transfers.csv` | `coverage.csv` |
| Moments (callouts) | dated events, each with a grade A/B source and neutral wording | `moments.csv` |
| Colour key, crest/logo reference | not chosen (DEC-069); crests are not in scope | `clubs.csv` `colour_key`, `logo_ref` (**empty**) |

## 9. Files (`data/rtt-101/`)
`clubs.csv`, `pl_membership.csv`, `seasons.csv`, `cpi.csv`, `fx.csv`, `transfers.csv`, `fee_evidence.csv`, `sources.csv`, `club_ledger.csv`, `club_season.csv`, `series_monthly.csv`, `moments.csv`, `conflicts.csv`, `tier1_list.csv`, `coverage.csv`, `CHECKS.md`, `manifest.json`. Build: `python3 scripts/build_rtt101_dataset.py` (deterministic).

## 10. Checks (`data/rtt-101/CHECKS.md`)
No transfer counted outside its club's PL seasons; PL-to-PL deals net to zero across the league (spend − income of PL clubs = net spend with non-PL clubs); no fee without a source row; no Transfermarkt figure or URL anywhere; quotes under 25 words; every conversion has a rate row; the month-end series equals the ledger; totals reproduce from a clean run; 22 clubs per season 1992–95 and 20 after; every season has an attribution window.
