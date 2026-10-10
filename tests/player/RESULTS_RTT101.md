# RTT-101 player tests (IQ-21, design round 1)

Run: node tests/player/run_tests_rtt101.js · ALL PASS

0. Data untouched: PASS (series_onscreen.csv, clubs.csv, pl_membership.csv, seasons.csv as data/rtt-101/manifest.json; race_rtt101.json as dataset_hashes.txt; every race figure = series_onscreen.csv in pence)

| Config | Frames | Film length | 1-5, 7: landing values, ranks, eased frames checked, frozen bars, ending, pacing |
|---|---|---|---|
| config_rtt101_base.json | 6360 | 212.0 s | PASS: 412 landing boards (July 1992 to the freeze), 249,900 eased bar-frames between month ends |
| config_rtt101_pace_B.json | 6969 | 232.3 s | PASS: 412 landing boards (July 1992 to the freeze), 269,946 eased bar-frames between month ends |
| config_rtt101_pace_C.json | 5385 | 179.5 s | PASS: 412 landing boards (July 1992 to the freeze), 207,028 eased bar-frames between month ends |

6. Drawn landing frames: PASS - config_rtt101_base.json: 46 landing frames drawn, 552 value labels checked

