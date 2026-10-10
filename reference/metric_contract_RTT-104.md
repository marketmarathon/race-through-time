# Metric contract — RTT-104 Women in Parliament: Highest vs Lowest (1997–2025) · v1.0 (data build IQ-20) · 10 Oct 2026

Written for the data build (DEC-036). Owner decisions: DEC-600..DEC-605 (brief), DEC-611..DEC-613 (Luke's answers, IQ-20b). Cowork for Luke: DEC-614, DEC-615. Rights: DEC-623 (owner). Claude findings and working choices: DEC-606..DEC-610, DEC-616..DEC-622. **Rights settled (DEC-623): used under the World Bank's CC BY 4.0 licence as an owner-accepted risk; the IPU's own site terms are non-commercial; credit the IPU and the World Bank; taken down if the IPU objects.** Design waits on Luke's approval (DEC-069).

**Public claim:** for every year 1997–2025, the 10 countries with the highest and the 10 with the lowest share of seats held by women in the national parliament (lower or single house), among countries of 4 million people or more.
**Measure:** World Bank WDI indicator SG.GEN.PARL.ZS, "Proportion of seats held by women in national parliaments (%)": "the number of seats held by women members in single or lower chambers of national parliaments, expressed as a percentage of all occupied seats". Seats may be elected, appointed or indirectly elected (WDI definition). Producer: the Inter-Parliamentary Union (IPU), "Monthly ranking of women in national parliaments". Licence shown by the World Bank: CC BY-4.0 (the IPU's own terms differ: DEC-608; owner-accepted risk, DEC-623).
**Unit and precision:** percent, shown to one decimal (half up); order uses the full-precision WDI value.
**Timeline:** one value per country per WDI year 1997–2025 (29 years). A WDI year is not one fixed date (DEC-621): the year alone is shown.

## Rules
1. **Who is in the race (owner, DEC-611, DEC-612).** A country is in for the whole race if its WDI population (SP.POP.TOTL, midyear estimate) in the latest year with a figure (2025) is **4,000,000 or more**; otherwise it is out for the whole race. Setting `population_threshold` in `data/rtt-104/config.json`. Every country stays in `series.csv` and `countries.csv` (DEC-600). 126 countries are in the race.
2. **All political systems (owner, DEC-600).** No democracy filter.
3. **Values.** The WDI value of that country and year, exactly as in the fetched WDI file. Nothing is averaged, filled or forecast.
4. **Missing years (Claude, DEC-617).** One missing year with a figure on both sides shows the previous year's figure, marked "latest figure". Two or more missing years: off the board until the next figure. A missing final run: off the board; on the closing card only with a VERIFIED reason (rule 7).
5. **Boards (Claude, DEC-618, DEC-619).** Top: the 10 highest values. Bottom: the 10 lowest values **above 0%**. Countries at exactly 0% are the separate 0% group (owner, DEC-602). Order by full precision; an exact tie keeps alphabetical order and is listed in `ties.csv`.
6. **World panel (Claude, DEC-620).** WDI's World aggregate (WLD) for the same series, covering all countries (not only those in the race), labelled as such.
7. **Closing card (owner, DEC-603, DEC-613).** Countries in the race with no figure in 2025 are named only when the reason is VERIFIED at source with a quote; anything else stays off the card. No generic "no parliament" claim.

## Display attributes (DEC-036; built only after Luke's approval, DEC-069)

| Attribute | Source | File / column |
|---|---|---|
| Bar value (% to one decimal) | WDI SG.GEN.PARL.ZS | `boards.csv` `value_1dp` (full value `value`) |
| Country name (one short English name per country) | World Bank country name, shortened where listed | `countries.csv` `short_name`; the shortenings in `source/short_names.csv` (DEC-616) |
| Year label | WDI year; the year only, no day or month (DEC-621, report question 2) | `boards.csv` `year` |
| 0% group bar: count and names (design option, owner DEC-602) | WDI values exactly 0 | `zero_group.csv` `count`, `countries` |
| Population rule and source | WDI SP.POP.TOTL, latest year 2025, CC BY-4.0 | `countries.csv` `population_latest`, `population_year`, `in_race` |
| World panel | WDI SG.GEN.PARL.ZS for WLD ("Weighted average" over all countries) | `world.csv` `value_1dp`, `label` "World (all countries)" |
| "Latest figure" marking | rule 4 | `boards.csv` `latest_figure`, `carried_from_year`; `series.csv` `shown_as` |
| Closing card list | IPU Parline pages read on the runner, quote per country | `closing_card.csv` (`on_card` yes only when `status` VERIFIED), from `source/closing_card_reasons.csv` |
| Title and measure line | owner DEC-601: working title "Women in Parliament: Highest vs Lowest (1997–2025)"; measure line names "Proportion of seats held by women in national parliaments (%)", lower or single house | — |
| Credits (on screen and in the description, DEC-623) | both the IPU and the World Bank: proposed "Data: Inter-Parliamentary Union (IPU), via World Bank World Development Indicators (CC BY 4.0)"; population "World Bank WDI (UN World Population Prospects and others), CC BY 4.0"; exact wording and placement in the design session | — |

## Files
`data/rtt-104/`: `config.json`, `countries.csv`, `series.csv` (every economy × year, with status VERIFIED/MISSING and flags missing, zero, below_threshold, shown_as), `boards.csv`, `boards_2_5m_comparison.csv` (comparison only), `zero_group.csv`, `ties.csv`, `world.csv`, `closing_card.csv`, `events.csv`, `wdi_owid_differences.csv`, `checks.json`, `manifest.json`; inputs in `source/`. Build: `python3 scripts/build_rtt104_dataset.py data/rtt-104 reports/RTT-104_data_report.md`. Tests: `python3 tests/rtt104/run_tests_rtt104.py`.

## Not used
Our World in Data's copy (cross-check only; it agrees with WDI to rounding in every cell); any forecast; any figure not in the WDI file.
