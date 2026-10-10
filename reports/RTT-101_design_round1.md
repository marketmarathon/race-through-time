# RTT-101 Premier League net transfer spend — design round 1 (IQ-21, 10 Oct 2026)

Brief: `prompts/CODE_SESSION_IQ-21.md`. Decisions: DEC-700 (owner: crests) and DEC-701 to DEC-713 (Claude). Kit: `kits/rtt-101/README.md`. Private pre-release with every still, sheet and clip: see DEC-713 and `state/STATE.json` (`episodes[RTT-101].design_round1`). **Preview figures**: `series_onscreen.csv` (VERIFIED fees only, DEC-448) as merged from pull request #19 at IQ-15n (413b60a); the Tier 1 checks may still change them. Nothing here is approved (DEC-069).

## What the round shows (one contact sheet per item)

| Item | Options shown | Claude's recommendation |
|---|---|---|
| a. Title | A "Premier League Net Transfer Spend (1992–2026)"; B "The Premier League's Biggest Spenders (1992–2026)"; C "Premier League Spending Race (1992–2026)"; each with the measure and "undisclosed fees not included" in the line under it; and A with "undisclosed…" in the footer instead | A, with "undisclosed fees not included" in the line under the title (readable on a phone, 6.1 pt; in the footer it is 5.3 pt and sits where YouTube's controls are) |
| b. Board size | 10, 12 and 15 bars at phone size on June 2003, August 2015 and the freeze | 12 (DEC-704): 30 clubs ever reach it; no bar below zero (15 bars: 33 bar-months below zero in 1992–93) |
| c. Value labels | compact "£1.74bn" / "£683m" / "£45.3m" vs millions with one decimal "£1,740.4m"; near-ties with and without extra decimals | compact; extra decimals is Luke's call (DEC-705) |
| d. Out of the PL | dimmed + "· relegated 2009"; dimmed + "· not in the PL"; dimmed only; the return in 2010 (and a clip, May 2009 to Sep 2010) | dimmed + "· relegated 2009" (exact; the year is the end of the club's last PL season) |
| e. Colours, crests | kit colours (shaded, second-colour edge) vs a distinct palette on the busiest board (Aug 2017) and the freeze; colour-blind simulations; today's crest vs the crest in use at the date; tile vs no tile | Luke's call on colours (DEC-706); today's crest on the light tile |
| f. Pacing | clips of June 2003 – September 2004 at A 0.5 s a month, B house multipliers, C 0.25 s in months with no open window | C (DEC-707): A 3 min 32 s, B 3 min 52 s, C 2 min 59.5 s |
| g. Panel | A all PL clubs' net spend with its line; B the leader's average per PL season (2026 £); C nothing | A |
| h. Secondary statistic | A one closing view after the final table (6 s); B the panel (g B); C description only | A, ranking the final table's 12 clubs (DEC-709) |
| i. Story moments | RTT-103's card vs one line under the title (3 s) vs none; five candidates (DEC-708), layout only | none until they are VERIFIED; then the line for the two ownership changes that start the biggest surges (Abramovich 2003, ADUG 2008), if Luke wants any |
| j. Final table | with "Figures will be updated after the January 2027 window" vs without (description only) | without: the date block already says 1 September 2026 and the note is not something the board shows |
| k. Footer | the contract's wording, 26 px = 5.3 pt on a phone, inside the bottom strip | as drawn; no ECB credit (DEC-710) |

## House defaults applied without asking

No intro or outro; the final table holds 5 s after the freeze lands; no running captions; big date top right beside the RTT logo ("1 September" over 2026 at the freeze); board sized to its bars; values follow the bar, counting on a curve through every month end and landing exactly on it; one colour per club; stills on landing frames with a phone copy and the phone check; WCAG flash check on every clip; credits in the footer and description; crown on the leader's bar (proposed: the lead changes hands 15 times on screen, the last on the freeze day itself).

## Tests and checks

- `tests/player/RESULTS_RTT101.md`: data untouched; on every landing frame of every config every club's value equals `series_onscreen.csv` to the penny and the order equals its rank; eased frames never leave the two month-end figures; frozen bars keep their figure and rank and are "out" exactly while `in_pl` = no; 5 s ending; pacing within the multipliers; drawn labels match the series in the chosen format, the crown is on the leader, no label over the date block or the panel.
- `tests/player/PHONE_RTT101.md`: every still at phone size (names and values ≥ 5.9 pt, other text ≥ 5.0 pt) and its month's figures.
- `tests/player/COLOURS_RTT101.md`: every pair that shares the board, per option.
- `tests/player/compare_frames.js`: RTT-001, RTT-002, RTT-003, RTT-102 and RTT-103's approved configs pixel-identical before and after the player change.
- WCAG flash check: every clip (release notes).

## Story-moment candidates still UNVERIFIED (for Cowork to read in Luke's Chrome)

From `data/rtt-101/moments.csv` (every row is UNVERIFIED; quote as recorded there):

1. Transfer windows from 2002–03 — UEFA, "UEFA has recommended adopting uniform domestic and international transfer windows from 2002/03." https://www.uefa.com/news-media/news/0181-0f8435d76a61-7e1dbc3088ef-1000--transfer-windows-recommended/
2. Abramovich buys Chelsea (1 Jul 2003) — UEFA.com, "have been sold to Russian businessman Roman Abramovich" https://www.uefa.com/uefachampionsleague/news/0193-0e6a6632f70f-ab1404cbaa55-1000--russian-businessman-buys-chelsea/
3. ADUG and Manchester City (1 Sep 2008) — Sky Sports, "a Memorandum of Understanding has been signed" https://www.skysports.com/football/news/4078332/city-takeover-confirmed
4. Newcastle takeover (7 Oct 2021) — Newcastle United, "the acquisition was completed on 7 October 2021" https://www.newcastleunited.com/en/news/pif-pcp-capital-partners-and-rb-sports-media-acquire-newcastle-united-football-club
5. Chelsea sale (30 May 2022) — Chelsea FC, "today announced completion of the ownership transfer" https://www.chelseafc.com/en/news/article/consortium-led-by-todd-boehly-and-clearlake-capital-completes-ac
6. Not proposed, also UNVERIFIED: Bosman (EUR-Lex, https://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:61993CJ0415:EN:PDF); Glazer control (GOV.UK, https://www.gov.uk/cma-cases/red-football-ltd-manchester-united-plc).

The Manchester City Premier League case is not on the board in any option (brief).
