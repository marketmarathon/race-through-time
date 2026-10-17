# IQ-20 — RTT-104 Women in Parliament (top 10 vs bottom 10, 1997–2025): data build

v1, 10 Oct 2026 (Cowork). DATA ONLY: no player, renderer, frames or visual changes (DEC-069). Luke is not technical: finish with a short plain-English summary.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-20.md`.

READ FIRST: `CLAUDE.md`, `state/HANDOVER.md`, `state/STATE.json`, and only the DECs you need (DEC-036, DEC-057, DEC-069, DEC-417 on PR #19). Check main AND every open pull request and branch (#18, #19, #21, #22, #23 at least) before choosing numbers. **Your DEC block: DEC-600 to DEC-699** (the highest seen on 10 Oct was DEC-573 on PR #23; confirm 600+ is free everywhere). Base your branch on main. Leave the other open PRs alone.

Hard rules (as in CLAUDE.md): never touch `marketmarathon/bars`; nothing uploaded or published; never invent, average, guess or forecast a figure; only VERIFIED figures on screen; no new visual feature before Luke approves it; never print RTT_PRIVATE_TOKEN; do not install software or change settings without asking. Data that the cloud container cannot reach is fetched on a GitHub runner, as in earlier builds.

## What the video is
A split-screen bar-chart race: the 10 countries with the HIGHEST share of parliamentary seats held by women and the 10 with the LOWEST, every year 1997–2025. Measure: "Proportion of seats held by women in national parliaments (%)", the lower or single house only, as a share of occupied seats. Seats may be appointed or indirectly elected as well as elected (WDI definition). Producer: Inter-Parliamentary Union (IPU), via World Bank WDI indicator SG.GEN.PARL.ZS.

## Owner decisions to record as DECs (Luke, Cowork chat, 10 Oct 2026)
1. New episode RTT-104: the top 10 vs bottom 10 split race, 1997–2025. All countries regardless of political system (no democracy filter). Every country is kept in the underlying data, so that a change of format needs no new research.
2. The title says "parliament", not "government" (working title "Women in Parliament: Highest vs Lowest (1997–2025)"). The measure is named under the title.
3. Countries at exactly 0% share ONE group bar on the bottom board (e.g. "No women: 3 countries", listing them) rather than being picked alphabetically. This is a new visual feature: it is shown to Luke as a design option before use (DEC-069). Not built here.
4. Countries with no figure because their parliament was dissolved or suspended are not in the race. They are named on a closing card at the end ("not included: no sitting parliament"). The wording on that card must be VERIFIED per country.
5. NEW RULE: only countries with a population of at least **4 million** are in the race. Luke may have said 2.5 million, and Cowork is confirming. So build the threshold as a setting with default 4,000,000 and report the result at both 4 m and 2.5 m.
6. Go-ahead for this build.

## Facts found by Cowork on 10 Oct (Our World in Data's copy, read in Luke's Chrome; UNVERIFIED until you read them at source)
- OWID grapher `share-of-women-in-parliament-ipu`: WDI 129, published 15 Jul 2026; OWID update 27 Jul 2026; licence shown CC BY 4.0; 1997–2025; 193 countries; 153–192 countries a year. Citation: "Inter-Parliamentary Union (IPU) monthly ranking of women in national parliaments, via World Bank (2026) – processed by Our World in Data".
- No 2025 figure (last year in brackets): Afghanistan (2021), Bangladesh (2023), Eritrea (2019), Guinea-Bissau (2024), Haiti (2019), Kuwait (2023), Myanmar (2021), Nepal (2024), Sudan (2018). 108 countries miss at least one year.
- With a 4 m threshold applied to 2023 population (OWID/UN WPP 2024, used only for this preview): 126 countries; 101–125 a year; at most 3 countries at 0% in any year (2.5 m: 140 countries). Leader: Sweden 1997–2002, then Rwanda 2003–2025. UAE 0% (1997–2005) to 50% (2019+). Saudi Arabia 0% to 19.9% (2013). Japan in the bottom 10 in 2023.
- Countries that cross 4 m during 1997–2023: Croatia, Georgia, Bosnia and Herzegovina and Moldova fall below it; Kuwait and Panama rise above it.
- ChatGPT's 2025 table (184 countries, via worldgovdata.com) equals OWID's 2025 values to one decimal for all 184. That is agreement only, not a check. It stays on Luke's laptop and is not needed here.

## Build
1. DECs for the owner decisions above, then one DEC per working choice (marked as Claude's choice).
2. Fetch on a runner:
   - SG.GEN.PARL.ZS for all countries 1997–2025 from the World Bank API (primary), plus OWID's grapher CSV as a cross-check.
   - Population SP.POP.TOTL (WDI, CC BY 4.0) 1997–latest.
   - The World aggregate (WLD) for SG.GEN.PARL.ZS.

   Record each file's URL, date fetched and SHA-256. Keep the raw files in `data/rtt-104/source/`. Compare WDI with OWID cell by cell and report every difference.
3. Terms of use: read the World Bank data terms and the IPU's own terms (IPU Parline / data.ipu.org) at source, quote them, and add a rights-ledger entry. If the IPU's terms forbid commercial reuse, stop and report.
4. Reference date: find out which date in each year the annual WDI figure refers to (WDI metadata, or IPU's notes) and quote it. The date label on screen depends on it.
5. Metric contract `reference/metric_contract_RTT-104.md` (DEC-036). It lists every attribute shown, with its source:
   - bar value (% to one decimal)
   - country name (one short English name per country, listed)
   - year label
   - the 0% group bar's count and names
   - population rule and population source
   - world average panel (WLD, all countries, so it is labelled as such)
   - "latest figure" marking
   - closing-card list
   - title and measure line
   - credits
6. Population rule. Working choice to propose:
   - The list is fixed by the latest available population year, so bars do not flicker in and out as a country crosses the line.
   - Report every country within ±10% of the threshold, and which countries enter or leave under the alternative "population in that year" rule.
7. Series `data/rtt-104/series.csv`: every country × year with value, status and flags (missing, zero, below threshold). Nothing is ever filled, averaged or carried silently.

   Gaps (working choice under DEC-417, report it):
   - A single missing year inside a run may show the previous figure, marked "latest figure".
   - A longer gap means the country is off the board until its next figure.
   - A missing final run caused by a dissolved or suspended parliament goes to the closing card (decision 4).
8. Boards `data/rtt-104/boards.csv`:
   - Each year: ranks 1–10 top and bottom, using full precision for order.
   - The 0% group is reported separately (count and names), and the bottom board is built from the countries above 0%.
   - List every tie that full precision does not break.
9. Closing-card list: countries at or above the threshold with no figure in 2025. For each, give the reason with source URL and a quote (IPU or another official source) and mark it VERIFIED, UNVERIFIED or NOT FOUND. Do not claim "no parliament" without a source.
10. Checks as tests:
    - every value traceable to the WDI file
    - no 0% shown where the data is missing
    - no country below the threshold on a board
    - no forecast
    - two clean rebuilds identical
11. Report `reports/RTT-104_data_report.md`:
    - top and bottom 10 for every year at 4 m and at 2.5 m
    - every change of first place, and every entry to and exit from each board
    - candidate story moments (e.g. Rwanda 2003, UAE, Saudi Arabia 2013), with year and figure only, all VERIFIED
    - the 0% group size by year
    - the WDI vs OWID differences
    - terms
    - the reference date
    - an estimate of running time at 2 and 3 seconds per year
    - numbered questions for Luke, each with your recommendation and what happens if he does not answer. Ask only about on-screen claims, scope, rights or leader-changing choices (DEC-417).

STATE: update `state/STATE.json`, `state/HANDOVER.md`, `state/DECISIONS.md`. Push a branch and open a pull request against main. **Do not merge** (DEC-057). Stop there and give Luke a short plain-English summary: what was built, what is still unverified, what needs his decision, and the next step.
