# RTT-002 starts — scripted checks

Build `rtt002-starts/1.1` (`scripts/rtt002_starts.py`). All checks pass: **True**. Definition, source and rounding: `reference/metric_contract_RTT-002.md`, Display attributes (DEC-053, DEC-058, DEC-059).

| Check | Result | Detail |
|---|---|---|
| same_revisions_as_wins_data | PASS | 77 of 77 season pages at the revision races.csv records |
| round_count_equals_races_csv | PASS | every season after dropping empty-header columns (1967: 1 dropped, 1968: 1 dropped, 1969: 1 dropped, 1970: 1 dropped, 1972: 1 dropped, 1975: 1 dropped, 1976: 1 dropped, 1979: 1 dropped); 2026: 23 listed, 15 run |
| every_row_resolves_to_a_page_id | PASS | every driver row resolved through the T lines; 5 'Formula Two' separator rows skipped |
| every_cell_classified | PASS | (empty) 15871, DNA 17, DNP 11, DNPQ 338, DNQ 1047, DNS 364, DSQ 155, EX 25, NC 192, Ret 8971, WD 37, number 16479 |
| documented_corrections_applied | PASS | 1 applied: Rubens Barrichello, 2002 Spanish Grand Prix (table cell "Ret") -> not_a_start |
| every_win_credit_has_a_start | PASS | 1167 of 1167 win credits |
| every_driver_has_starts | PASS | 116 of 116 drivers |
| starts_at_least_wins | PASS | 116 of 116 drivers |
| indianapolis_500_1950_1960_counted | PASS | 11 Indianapolis 500 races, 72 starts by drivers of drivers.csv |
| win_rate_rounding_half_up | PASS | decimal ROUND_HALF_UP equals exact-fraction rounding on every wins <= starts <= 400; half-way cases 1/8 = 12.5, 1/16 = 6.25 -> 6.3, 3/16 = 18.75 -> 18.8, 1/80 = 1.25 -> 1.3 |
| career_starts_vs_list_of_f1_drivers_as_prototype | PASS | 116 of 116 agree with the List page (rev. 1377016608); disagreements (kept at the season-table value, listed for Luke, not resolved): none |
| list_page_wins_equal_career_totals | PASS | 116 of 116 drivers |
| luke_example_schumacher | PASS | Michael Schumacher 91 wins · 306 starts · 29.7% |

## Summary

- 14479 starts rows (drivers of `drivers.csv` only) over 1164 races
- career starts at the freeze vs List of Formula One drivers rev. 1377016608 (retrieved 2026-09-29T04:51:53Z): 116 agree, 0 disagree
- drivers with more than one row in a season's table (one start per race still): none
- races where one driver had more than one starting cell part (counted once): none

## Documented corrections (`starts_corrections.csv`)

Applied after classification; the source extract is not edited.

| Driver | Race | Table cell | Action | Reason | Evidence |
|---|---|---|---|---|---|
| Rubens Barrichello | 2002 Spanish Grand Prix (race_index 685) | Ret | not_a_start | The 2002 season table shows "Ret", but Barrichello did not take the start (electrical failure before the start) | Wikipedia "List of Formula One drivers" rev. 1377016608 gives 322 starts; independent check 3 section M (StatsF1 non-participation record: did not start, electrical failure); GP Racing Stats 322; decided by Luke DEC-058 |

## Disagreements with the List page (for Luke; not resolved, the season-table value is kept)

None: all 116 drivers agree.

## Round columns per season

| Season | Columns | Empty-header columns dropped | Rounds listed | races.csv |
|---|---|---|---|---|
| 1950 | 7 | 0 | 7 | 7 |
| 1951 | 8 | 0 | 8 | 8 |
| 1952 | 8 | 0 | 8 | 8 |
| 1953 | 9 | 0 | 9 | 9 |
| 1954 | 9 | 0 | 9 | 9 |
| 1955 | 7 | 0 | 7 | 7 |
| 1956 | 8 | 0 | 8 | 8 |
| 1957 | 8 | 0 | 8 | 8 |
| 1958 | 11 | 0 | 11 | 11 |
| 1959 | 9 | 0 | 9 | 9 |
| 1960 | 10 | 0 | 10 | 10 |
| 1961 | 8 | 0 | 8 | 8 |
| 1962 | 9 | 0 | 9 | 9 |
| 1963 | 10 | 0 | 10 | 10 |
| 1964 | 10 | 0 | 10 | 10 |
| 1965 | 10 | 0 | 10 | 10 |
| 1966 | 9 | 0 | 9 | 9 |
| 1967 | 12 | 1 | 11 | 11 |
| 1968 | 13 | 1 | 12 | 12 |
| 1969 | 12 | 1 | 11 | 11 |
| 1970 | 14 | 1 | 13 | 13 |
| 1971 | 11 | 0 | 11 | 11 |
| 1972 | 13 | 1 | 12 | 12 |
| 1973 | 15 | 0 | 15 | 15 |
| 1974 | 15 | 0 | 15 | 15 |
| 1975 | 15 | 1 | 14 | 14 |
| 1976 | 17 | 1 | 16 | 16 |
| 1977 | 17 | 0 | 17 | 17 |
| 1978 | 16 | 0 | 16 | 16 |
| 1979 | 16 | 1 | 15 | 15 |
| 1980 | 14 | 0 | 14 | 14 |
| 1981 | 15 | 0 | 15 | 15 |
| 1982 | 16 | 0 | 16 | 16 |
| 1983 | 15 | 0 | 15 | 15 |
| 1984 | 16 | 0 | 16 | 16 |
| 1985 | 16 | 0 | 16 | 16 |
| 1986 | 16 | 0 | 16 | 16 |
| 1987 | 16 | 0 | 16 | 16 |
| 1988 | 16 | 0 | 16 | 16 |
| 1989 | 16 | 0 | 16 | 16 |
| 1990 | 16 | 0 | 16 | 16 |
| 1991 | 16 | 0 | 16 | 16 |
| 1992 | 16 | 0 | 16 | 16 |
| 1993 | 16 | 0 | 16 | 16 |
| 1994 | 16 | 0 | 16 | 16 |
| 1995 | 17 | 0 | 17 | 17 |
| 1996 | 16 | 0 | 16 | 16 |
| 1997 | 17 | 0 | 17 | 17 |
| 1998 | 16 | 0 | 16 | 16 |
| 1999 | 16 | 0 | 16 | 16 |
| 2000 | 17 | 0 | 17 | 17 |
| 2001 | 17 | 0 | 17 | 17 |
| 2002 | 17 | 0 | 17 | 17 |
| 2003 | 16 | 0 | 16 | 16 |
| 2004 | 18 | 0 | 18 | 18 |
| 2005 | 19 | 0 | 19 | 19 |
| 2006 | 18 | 0 | 18 | 18 |
| 2007 | 17 | 0 | 17 | 17 |
| 2008 | 18 | 0 | 18 | 18 |
| 2009 | 17 | 0 | 17 | 17 |
| 2010 | 19 | 0 | 19 | 19 |
| 2011 | 19 | 0 | 19 | 19 |
| 2012 | 20 | 0 | 20 | 20 |
| 2013 | 19 | 0 | 19 | 19 |
| 2014 | 19 | 0 | 19 | 19 |
| 2015 | 19 | 0 | 19 | 19 |
| 2016 | 21 | 0 | 21 | 21 |
| 2017 | 20 | 0 | 20 | 20 |
| 2018 | 21 | 0 | 21 | 21 |
| 2019 | 21 | 0 | 21 | 21 |
| 2020 | 17 | 0 | 17 | 17 |
| 2021 | 22 | 0 | 22 | 22 |
| 2022 | 22 | 0 | 22 | 22 |
| 2023 | 22 | 0 | 22 | 22 |
| 2024 | 24 | 0 | 24 | 24 |
| 2025 | 24 | 0 | 24 | 24 |
| 2026 | 23 | 0 | 23 | 15 |
