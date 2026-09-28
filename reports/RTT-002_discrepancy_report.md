# RTT-002 discrepancy report: Wikipedia build vs frozen independent check

Independent check file SHA-256 `0ac442475cc89f977ce927887cb019f85c2499c73e4709a024d5a21a027cddd2` matches the frozen record (state/RTT-002_independent_check_freeze.json).
Disagreements are listed, not resolved.

| Section | What was compared | Result |
|---|---|---|
| A | Data freeze race, date, winner, 2026 rounds | agree |
| B | Rounds and wins per driver, 77 seasons | agree |
| E | Record progression (118 check rows vs 118 build rows) | agree |
| F | Career wins for every driver with 10+ | agree |
| G | Race-by-race winners and dates, seasons 1959, 1965, 1980, 1990, 2001, 2012, 2013, 2021 | agree |

**Discrepancies: 0**


## Name matches that were not exact (please confirm same person)

- Carlos Sainz -> Carlos Sainz Jr. (Carlos_Sainz_Jr.)

## Names in the check that could not be matched

- none

Race-name label differences in G (naming style only, e.g. 'Great Britain' vs 'British Grand Prix'): 57.


## Coverage against the contract's DATA_AUDIT checks (metric_contract_RTT-002.md v0.2)

| Contract check | Status |
|---|---|
| Wins per season = championship races (shared drives explicit) | PASS in the build for all 77 seasons; agrees with check section B |
| Final table matches official career-win totals for the top 20 | Top 20 agree with the Wikipedia list page and with check section F (built from Formula 1's race archive, totals cross-checked on StatsF1). **An official F1/FIA career-total table was not consulted** (formula1.com is eyeball-only, never scraped) — open |
| Every change of all-time leader reconstructed independently | PASS — all 118 record events agree (section E), including the 12 moments a driver became sole holder |
| Every top-ten entry reconstructed independently | **NOT COVERED** — the check prompt did not ask for top-ten entries — open |
| Seeded random sample ≥ 10% of remaining race winners | PASS — 127 of 1,164 races (10.9%) in the eight seeded seasons agree on date and winner. The sample is whole seasons, not individual races |
| No row created by interpolation; missing = NOT FOUND | PASS — no missing values; the eight 2026 rounds after the freeze are excluded, not zero-filled |

## Other notes

- The check itself records 22 NOT FOUND cells: for the 11 Indianapolis 500 winners (1950–1960) it could not find a separately published F1/FIA career-total table, nor an explicit F1/FIA rule that those wins count in career totals. The build includes them under contract default D-04 ("follow the official results classification"). NOT FOUND does not mean no.
- The check reported a date conflict for the 2014 Russian Grand Prix (F1 archive 21 Oct vs StatsF1 12 Oct). Wikipedia gives 12 October 2014, the same as the date the check used. Outside the compared sample seasons.
