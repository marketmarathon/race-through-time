# RTT-104 V3 design round round2 — still and clip checks (IQ-24d, IQ-24e)

Written by `kits/rtt-104/render_stills_v3.js`. VALUES: bars = ranks 1–N of `data/rtt-104/v3_change_events.csv` with their one-decimal figures. TAGS: every tag drawn is a VERIFIED row of `v3_change_events.csv` with a source URL and a fetched excerpt, big under the rule shown, with the row's month and year, fitting its bar; on a landing still every such row is drawn. PHONE: names, values and tags at least 5.9 pt at 390 pt wide, other text at least 5.0 pt. OVERLAP: nothing inside the world panel or past the board edge.

| Still | Config | Frame | Values | Tags | Phone (smallest name / value / tag / other) | Overlap | Result |
|---|---|---|---|---|---|---|---|
| v3r2_continents_2019 | config_rtt104_v3_continents.json | 2025 | PASS (20 bars) | PASS (4) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS | PASS |
| v3r2_round1_teal_2019 | config_rtt104_v3_base.json | 2025 | PASS (20 bars) | PASS (4) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS | PASS |

| Clip | Frames | Tags shown (country-year) | Landing values | Tag and layout checks, every frame |
|---|---|---|---|---|
| config_rtt104_v3_clip_continents_4_5s_2016_2020.json | 630 | 12: AGO 2017, DEU 2017, FRA 2017, NZL 2017, CRI 2018, MEX 2018, ARE 2019, BLR 2019, CHE 2019, FIN 2019, BOL 2020, NZL 2020 | 5/5 PASS | PASS |
| config_rtt104_v3_clip_continents_6_0s_2016_2020.json | 810 | 12: AGO 2017, DEU 2017, FRA 2017, NZL 2017, CRI 2018, MEX 2018, ARE 2019, BLR 2019, CHE 2019, FIN 2019, BOL 2020, NZL 2020 | 5/5 PASS | PASS |

Overall: PASS.
