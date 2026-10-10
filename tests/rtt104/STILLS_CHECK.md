# RTT-104 design round 1 — still checks (IQ-22)

Written by `kits/rtt-104/render_stills.js`. VALUES: every bar and the 0% group equal `data/rtt-104/boards.csv` and `zero_group.csv` for the year shown. PHONE: on a phone showing the video 390 pt wide, names, values, 0% group and closing-card lines at least 5.9 pt, every other text at least 5.0 pt. OVERLAP: no board text inside the world panel or past its board.

| Still | Option | Frame | Values | Phone (smallest name / value / other) | Overlap | Result |
|---|---|---|---|---|---|---|
| a1_layoutA_left_right_2003 | a | 450 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| a2_layoutB_top_bottom_2003 | a | 450 | PASS | 4.7 / 4.7 / 4.1 pt FAIL | PASS | REPORTED (option B misses the phone sizes): axis 20px = 4.1 pt < 5; name 23px = 4.7 pt < 5.9; value 23px = 4.7 pt < 5.9; zero_head 23px = 4.7 pt < 5.9; zero_names 23px = 4.7 pt < 5.9 |
| a1_layoutA_left_right_2013 | a | 1104 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| a2_layoutB_top_bottom_2013 | a | 1104 | PASS | 4.7 / 4.7 / 4.1 pt FAIL | PASS | REPORTED (option B misses the phone sizes): axis 20px = 4.1 pt < 5; name 23px = 4.7 pt < 5.9; value 23px = 4.7 pt < 5.9 |
| a1_layoutA_left_right_2025 | a | 1932 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| a2_layoutB_top_bottom_2025 | a | 1932 | PASS | 4.7 / 4.7 / 4.1 pt FAIL | PASS | REPORTED (option B misses the phone sizes): axis 20px = 4.1 pt < 5; name 23px = 4.7 pt < 5.9; value 23px = 4.7 pt < 5.9; zero_head 23px = 4.7 pt < 5.9; zero_names 23px = 4.7 pt < 5.9 |
| b2_scaleB_own_scales_2003 | b | 450 | PASS | 6.1 / 6.1 / 5.3 pt | PASS | PASS |
| b2_scaleB_own_scales_2025 | b | 1932 | PASS | 6.1 / 6.1 / 5.3 pt | PASS | PASS |
| c1_zero_group_bar_1997 | c | 0 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| c2_zero_group_strip_1997 | c | 0 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| c3_zero_group_count_1997 | c | 0 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| c1_zero_group_bar_2025 | c | 1932 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| c2_zero_group_strip_2025 | c | 1932 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| c3_zero_group_count_2025 | c | 1932 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| d1_leave_A_fade_Haiti_2019_note | d | 1513 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| d2_leave_B_grey_Haiti_2019_note | d | 1513 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| d3_leave_A_fade_Kuwait_2023_note | d | 1807 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| d4_leave_B_grey_Kuwait_2023_note | d | 1807 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| d5_no_figure_Pakistan_1998_note | d | 145 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| d6_no_figure_Egypt_2012_note | d | 1039 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| e2_names_only_2013 | e | 1104 | PASS | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| g_opening_1997 | g | 0 | n/a | 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| h_closing_card | h | 2121 | n/a | — / — / 5.3 pt | PASS | PASS |

Overall: PASS.
