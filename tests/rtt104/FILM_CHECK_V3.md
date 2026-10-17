# RTT-104 V3 whole-film check (IQ-24g)

Written by `tests/rtt104/film_check_v3.js config_rtt104_v3_film.json`. Every frame 0–5234 (174.5 s): tags and layout; every landing frame: values.

- Landing frames: ranks 1–20 = `v3_change_events.csv` 29/29; ranks 1–10 = `boards.csv` 29/29.
- Tags shown: 46 (each a VERIFIED row with a fetched excerpt, rule a).
- Tag and layout checks, every frame: PASS.

| Phone still | Frame | Smallest name / value / tag / other | Result |
|---|---|---|---|
| 1997 | 0 (0.0 s) | 6.1 / 6.1 / — / 5.1 pt | PASS |
| 2008 | 2025 (67.5 s) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS |
| 2019 | 4005 (133.5 s) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS |
| 2025 | 5085 (169.5 s) | 6.1 / 6.1 / 6.1 / 5.1 pt | PASS |

Overall: PASS.
