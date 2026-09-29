# RTT-002 starts — scripted checks

Build `rtt002-starts/1.0` (`scripts/rtt002_starts.py`). All checks pass: **True**. Definition, source and rounding: `reference/metric_contract_RTT-002.md`, Display attributes (DEC-053).

| Check | Result | Detail |
|---|---|---|
| same_revisions_as_wins_data | PASS | 77 of 77 season pages at the revision races.csv records |
| round_count_equals_races_csv | PASS | every season after dropping empty-header columns (1967: 1 dropped, 1968: 1 dropped, 1969: 1 dropped, 1970: 1 dropped, 1972: 1 dropped, 1975: 1 dropped, 1976: 1 dropped, 1979: 1 dropped); 2026: 23 listed, 15 run |
| every_row_resolves_to_a_page_id | PASS | every driver row resolved through the T lines; 5 'Formula Two' separator rows skipped |
| every_cell_classified | PASS | (empty) 15871, DNA 17, DNP 11, DNPQ 338, DNQ 1047, DNS 364, DSQ 155, EX 25, NC 192, Ret 8971, WD 37, number 16479 |
| every_win_credit_has_a_start | PASS | 1167 of 1167 win credits |
| every_driver_has_starts | PASS | 116 of 116 drivers |
| starts_at_least_wins | PASS | 116 of 116 drivers |
| indianapolis_500_1950_1960_counted | PASS | 11 Indianapolis 500 races, 72 starts by drivers of drivers.csv |
| win_rate_rounding_half_up | PASS | decimal ROUND_HALF_UP equals exact-fraction rounding on every wins <= starts <= 400; half-way cases 1/8 = 12.5, 1/16 = 6.25 -> 6.3, 3/16 = 18.75 -> 18.8, 1/80 = 1.25 -> 1.3 |
| career_starts_vs_list_of_f1_drivers_as_prototype | PASS | 115 of 116 agree with the List page (rev. 1377016608); disagreements (kept at the season-table value, listed for Luke, not resolved): Rubens Barrichello season tables 323, list 322 |
| list_page_wins_equal_career_totals | PASS | 116 of 116 drivers |
| luke_example_schumacher | PASS | Michael Schumacher 91 wins · 306 starts · 29.7% |

## Summary

- 14480 starts rows (drivers of `drivers.csv` only) over 1164 races
- career starts at the freeze vs List of Formula One drivers rev. 1377016608 (retrieved 2026-09-29T04:51:53Z): 115 agree, 1 disagree
- drivers with more than one row in a season's table (one start per race still): none
- races where one driver had more than one starting cell part (counted once): none

## Disagreements with the List page (for Luke; not resolved, the season-table value is kept)

**Rubens Barrichello**: 323 starts from the season tables, 322 in "List of Formula One drivers" (rev. 1377016608). The candidates are the 94 counted starts whose cell shows no classified position (Ret, NC or DSQ): if the List page is right, one of these was not a start.

Named in the task (prompts/CODE_SESSION_IQ-05e.md) as an example candidate: 2002 Spanish Grand Prix (cell "Ret", revision 1371249242). Which race is the extra one cannot be decided from these two Wikipedia sources; it needs a third source (Luke's decision). Until then the season-table value is used.

| Race | Date | Season-table cell | Season page revision |
|---|---|---|---|
| 1993 South African Grand Prix | 1993-03-14 | Ret | 1375412761 |
| 1993 Brazilian Grand Prix | 1993-03-28 | Ret | 1375412761 |
| 1993 San Marino Grand Prix | 1993-04-25 | Ret | 1375412761 |
| 1993 Canadian Grand Prix | 1993-06-13 | Ret | 1375412761 |
| 1993 German Grand Prix | 1993-07-25 | Ret | 1375412761 |
| 1993 Hungarian Grand Prix | 1993-08-15 | Ret | 1375412761 |
| 1993 Belgian Grand Prix | 1993-08-29 | Ret | 1375412761 |
| 1993 Italian Grand Prix | 1993-09-12 | Ret | 1375412761 |
| 1994 Monaco Grand Prix | 1994-05-15 | Ret | 1373068999 |
| 1994 Spanish Grand Prix | 1994-05-29 | Ret | 1373068999 |
| 1994 French Grand Prix | 1994-07-03 | Ret | 1373068999 |
| 1994 German Grand Prix | 1994-07-31 | Ret | 1373068999 |
| 1994 Hungarian Grand Prix | 1994-08-14 | Ret | 1373068999 |
| 1994 Belgian Grand Prix | 1994-08-28 | Ret | 1373068999 |
| 1994 Japanese Grand Prix | 1994-11-06 | Ret | 1373068999 |
| 1995 Brazilian Grand Prix | 1995-03-26 | Ret | 1375309886 |
| 1995 Argentine Grand Prix | 1995-04-09 | Ret | 1375309886 |
| 1995 San Marino Grand Prix | 1995-04-30 | Ret | 1375309886 |
| 1995 Monaco Grand Prix | 1995-05-28 | Ret | 1375309886 |
| 1995 German Grand Prix | 1995-07-30 | Ret | 1375309886 |
| 1995 Italian Grand Prix | 1995-09-10 | Ret | 1375309886 |
| 1995 Pacific Grand Prix | 1995-10-22 | Ret | 1375309886 |
| 1995 Japanese Grand Prix | 1995-10-29 | Ret | 1375309886 |
| 1995 Australian Grand Prix | 1995-11-12 | Ret | 1375309886 |
| 1996 Australian Grand Prix | 1996-03-10 | Ret | 1376170380 |
| 1996 Brazilian Grand Prix | 1996-03-31 | Ret | 1376170380 |
| 1996 Monaco Grand Prix | 1996-05-19 | Ret | 1376170380 |
| 1996 Spanish Grand Prix | 1996-06-02 | Ret | 1376170380 |
| 1996 Canadian Grand Prix | 1996-06-16 | Ret | 1376170380 |
| 1996 Belgian Grand Prix | 1996-08-25 | Ret | 1376170380 |
| 1996 Portuguese Grand Prix | 1996-09-22 | Ret | 1376170380 |
| 1997 Australian Grand Prix | 1997-03-09 | Ret | 1371597287 |
| 1997 Brazilian Grand Prix | 1997-03-30 | Ret | 1371597287 |
| 1997 Argentine Grand Prix | 1997-04-13 | Ret | 1371597287 |
| 1997 San Marino Grand Prix | 1997-04-27 | Ret | 1371597287 |
| 1997 Spanish Grand Prix | 1997-05-25 | Ret | 1371597287 |
| 1997 Canadian Grand Prix | 1997-06-15 | Ret | 1371597287 |
| 1997 French Grand Prix | 1997-06-29 | Ret | 1371597287 |
| 1997 British Grand Prix | 1997-07-13 | Ret | 1371597287 |
| 1997 German Grand Prix | 1997-07-27 | Ret | 1371597287 |
| 1997 Hungarian Grand Prix | 1997-08-10 | Ret | 1371597287 |
| 1997 Belgian Grand Prix | 1997-08-24 | Ret | 1371597287 |
| 1997 Luxembourg Grand Prix | 1997-09-28 | Ret | 1371597287 |
| 1997 Japanese Grand Prix | 1997-10-12 | Ret | 1371597287 |
| 1997 European Grand Prix | 1997-10-26 | Ret | 1371597287 |
| 1998 Australian Grand Prix | 1998-03-08 | Ret | 1372421349 |
| 1998 Brazilian Grand Prix | 1998-03-29 | Ret | 1372421349 |
| 1998 San Marino Grand Prix | 1998-04-26 | Ret | 1372421349 |
| 1998 Monaco Grand Prix | 1998-05-24 | Ret | 1372421349 |
| 1998 British Grand Prix | 1998-07-12 | Ret | 1372421349 |
| 1998 Austrian Grand Prix | 1998-07-26 | Ret | 1372421349 |
| 1998 German Grand Prix | 1998-08-02 | Ret | 1372421349 |
| 1998 Hungarian Grand Prix | 1998-08-16 | Ret | 1372421349 |
| 1998 Japanese Grand Prix | 1998-11-01 | Ret | 1372421349 |
| 1999 Brazilian Grand Prix | 1999-04-11 | Ret | 1369387987 |
| 1999 Spanish Grand Prix | 1999-05-30 | DSQ | 1369387987 |
| 1999 Canadian Grand Prix | 1999-06-13 | Ret | 1369387987 |
| 1999 Austrian Grand Prix | 1999-07-25 | Ret | 1369387987 |
| 1999 German Grand Prix | 1999-08-01 | Ret | 1369387987 |
| 2000 Brazilian Grand Prix | 2000-03-26 | Ret | 1371597275 |
| 2000 British Grand Prix | 2000-04-23 | Ret | 1371597275 |
| 2000 Belgian Grand Prix | 2000-08-27 | Ret | 1371597275 |
| 2000 Italian Grand Prix | 2000-09-10 | Ret | 1371597275 |
| 2001 Brazilian Grand Prix | 2001-04-01 | Ret | 1375812110 |
| 2001 Spanish Grand Prix | 2001-04-29 | Ret | 1375812110 |
| 2001 Canadian Grand Prix | 2001-06-10 | Ret | 1375812110 |
| 2002 Australian Grand Prix | 2002-03-03 | Ret | 1371249242 |
| 2002 Malaysian Grand Prix | 2002-03-17 | Ret | 1371249242 |
| 2002 Brazilian Grand Prix | 2002-03-31 | Ret | 1371249242 |
| 2002 Spanish Grand Prix | 2002-04-28 | Ret | 1371249242 |
| 2003 Australian Grand Prix | 2003-03-09 | Ret | 1371597264 |
| 2003 Brazilian Grand Prix | 2003-04-06 | Ret | 1371597264 |
| 2003 German Grand Prix | 2003-08-03 | Ret | 1371597264 |
| 2003 Hungarian Grand Prix | 2003-08-24 | Ret | 1371597264 |
| 2003 United States Grand Prix | 2003-09-28 | Ret | 1371597264 |
| 2004 Japanese Grand Prix | 2004-10-10 | Ret | 1371252745 |
| 2005 Malaysian Grand Prix | 2005-03-20 | Ret | 1371249561 |
| 2005 San Marino Grand Prix | 2005-04-24 | Ret | 1371249561 |
| 2006 Canadian Grand Prix | 2006-06-25 | Ret | 1370957708 |
| 2006 French Grand Prix | 2006-07-16 | Ret | 1370957708 |
| 2006 German Grand Prix | 2006-07-30 | Ret | 1370957708 |
| 2007 United States Grand Prix | 2007-06-17 | Ret | 1368924967 |
| 2007 Brazilian Grand Prix | 2007-10-21 | Ret | 1368924967 |
| 2008 Australian Grand Prix | 2008-03-16 | DSQ | 1373003249 |
| 2008 Spanish Grand Prix | 2008-04-27 | Ret | 1373003249 |
| 2008 German Grand Prix | 2008-07-20 | Ret | 1373003249 |
| 2008 Belgian Grand Prix | 2008-09-07 | Ret | 1373003249 |
| 2008 Singapore Grand Prix | 2008-09-28 | Ret | 1373003249 |
| 2009 Turkish Grand Prix | 2009-06-07 | Ret | 1365999807 |
| 2010 Monaco Grand Prix | 2010-05-16 | Ret | 1368835756 |
| 2010 Belgian Grand Prix | 2010-08-29 | Ret | 1368835756 |
| 2011 Australian Grand Prix | 2011-03-27 | Ret | 1376563046 |
| 2011 Malaysian Grand Prix | 2011-04-10 | Ret | 1376563046 |
| 2011 German Grand Prix | 2011-07-24 | Ret | 1376563046 |

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
