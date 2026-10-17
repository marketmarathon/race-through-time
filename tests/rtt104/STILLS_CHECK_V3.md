# RTT-104 V3 design round — still and clip checks (IQ-24d)

Written by `kits/rtt-104/render_stills_v3.js`. VALUES: bars = ranks 1–N of `data/rtt-104/v3_change_events.csv` with their one-decimal figures. TAGS: every tag drawn is a VERIFIED row of `v3_change_events.csv` with a source URL and a fetched excerpt, big under the rule shown, with the row's month and year, fitting its bar; on a landing still every such row is drawn. PHONE: names, values and tags at least 5.9 pt at 390 pt wide, other text at least 5.0 pt. OVERLAP: nothing inside the world panel or past the board edge.

| Still | Config | Frame | Values | Tags | Phone (smallest name / value / tag / other) | Overlap | Result |
|---|---|---|---|---|---|---|---|
| v3_board_1997 | config_rtt104_v3_base.json | 0 | PASS (20 bars) | PASS (0) | 6.1 / 6.1 / — / 5.1 pt | PASS | PASS |
| v3_board_2014 | config_rtt104_v3_base.json | 1575 | PASS (20 bars) | PASS (1) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| v3_board_2025 | config_rtt104_v3_base.json | 2565 | PASS (20 bars) | PASS (1) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| v3_tag_look1_pill_2019 | config_rtt104_v3_base.json | 2025 | PASS (20 bars) | PASS (4) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| v3_tag_look2_text_2019 | config_rtt104_v3_look_text.json | 2025 | PASS (20 bars) | PASS (4) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| v3_scale_leader_1997 | config_rtt104_v3_scale_leader.json | 0 | PASS (20 bars) | PASS (0) | 6.1 / 6.1 / — / 5.1 pt | PASS | PASS |
| v3_late_election_PROPOSAL_1999 | config_rtt104_v3_base.json | 225 | PASS (20 bars) | PASS (2) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| v3_rows15_2025 | config_rtt104_v3_rows15.json | 2565 | PASS (15 bars) | PASS (1) | 6.9 / 6.9 / 6.1 / 5.1 pt | PASS | PASS |

| Clip | Frames | Tags shown (country-year) | Landing values | Tag and layout checks, every frame |
|---|---|---|---|---|
| config_rtt104_v3_clip_a_2016_2020.json | 450 | 12: AGO 2017, DEU 2017, FRA 2017, NZL 2017, CRI 2018, MEX 2018, ARE 2019, BLR 2019, CHE 2019, FIN 2019, BOL 2020, NZL 2020 | 5/5 PASS | PASS |
| config_rtt104_v3_clip_b_2016_2020.json | 450 | 20: AGO 2017, ARG 2017, DEU 2017, ECU 2017, FRA 2017, NLD 2017, NZL 2017, SEN 2017, CRI 2018, MEX 2018, ARE 2019, ARG 2019, BEL 2019, BLR 2019, CHE 2019, ESP 2019, FIN 2019, MOZ 2019, BOL 2020, NZL 2020 | 5/5 PASS | PASS |

Overall: PASS.
