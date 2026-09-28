# RTT-002 scripted checks

Build `rtt002-build/1.0`. All boolean checks pass: **True**.

| Check | Result |
|---|---|
| seasons_present_1950_to_2026 | PASS |
| rounds_contiguous_per_season | PASS |
| dates_increase_with_round | PASS |
| no_duplicate_races | PASS |
| all_dates_parse | PASS |
| all_winner_links_resolve | PASS |
| no_completed_race_after_build_date | PASS |
| no_winner_gap_before_freeze | PASS |
| wins_equal_races_plus_shared_every_season | PASS |
| cumulative_monotonic_integers | PASS |
| final_cumulative_equals_totals | PASS |
| career_totals_match_wikipedia_list_page | PASS |
| top20_match_list_page | PASS |

## Summary

- seasons: 77
- championship_races_completed: 1164
- win_credits: 1167
- distinct_winners: 116
- shared_wins: 3
- drivers_10_plus: 36
- record_events: 118
- holder_change_events: 12
- freeze_race: 2026 Azerbaijan Grand Prix
- freeze_date: 2026-09-26
- freeze_winner: George Russell
- completed_2026_rounds: 15

## Notes

- **shared_wins**: ["1951 French Grand Prix (1951-07-01): Juan Manuel Fangio + Luigi Fagioli", "1956 Argentine Grand Prix (1956-01-22): Luigi Musso + Juan Manuel Fangio", "1957 British Grand Prix (1957-07-20): Tony Brooks + Stirling Moss"]
- **indianapolis_500_rounds_included**: "11 (1950-1960)"
- **redirect_merges**: ["Jim_Rathmann_(race_car_driver) -> Jim_Rathmann", "Pedro_Rodriguez_(racing_driver) -> Pedro_Rodríguez_(racing_driver)"]
- **future_rounds_without_winner**: ["2026 R16 Bahrain Grand Prix (2026-10-04)", "2026 R17 Singapore Grand Prix (2026-10-11)", "2026 R18 United States Grand Prix (2026-10-25)", "2026 R19 Mexico City Grand Prix (2026-11-01)", "2026 R20 São Paulo Grand Prix (2026-11-08)", "2026 R21 Las Vegas Grand Prix (2026-11-21)", "2026 R22 Qatar Grand Prix (2026-11-29)", "2026 R23 Abu Dhabi Grand Prix (2026-12-06)"]
- **career_totals_list_page_mismatches**: []
- **list_page_drivers_not_in_build**: []
- **problems**: []
