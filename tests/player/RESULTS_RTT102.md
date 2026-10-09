# RTT-102 player tests (IQ-19, design round 1)

Run: node tests/player/run_tests_rtt102.js · ALL PASS

0. Data untouched: PASS (series_monthly.csv and identities.csv as data/rtt-102/manifest.json; race_rtt102.json as dataset_hashes.txt)
9. Colours: closest pair as drawn CIEDE2000 20.0 (gemini/deepseek) PASS (>= 18); colour-blind (protan/deutan simulation) closest 10.2 (copilot/deepseek), reported
11. Eased vs straight lines, month-end order of all places: 1 month(s) differ:
   - 2024-12: chatgpt > gemini > perplexity > claude > copilot > meta_ai  vs eased  chatgpt > gemini > perplexity > copilot > claude > meta_ai

| Case | Config | Frames | Result |
|---|---|---|---|
| film | config_rtt102_film.json | 2466 | PASS |
| film_linear | config_rtt102_film.json | 2448 | PASS |
| clip_r2_oct2024_end | config_rtt102_clip_r2_oct2024_end.json | 1557 | PASS |

Notes:
- film: panel on landing frames: 2023-01 ~620m; 2023-07 ~1.7bn; 2024-01 ~2.1bn; 2024-07 ~3.0bn; 2025-01 ~4.7bn; 2025-07 ~7.3bn; 2026-01 ~8.3bn (not counting Copilot, Meta AI); 2026-07 ~9.9bn (not counting Copilot, Meta AI); 2026-08 ~9.9bn (not counting Copilot, Meta AI)
- film_linear: panel on landing frames: 2023-01 ~620m; 2023-07 ~1.7bn; 2024-01 ~2.1bn; 2024-07 ~3.1bn; 2025-01 ~4.7bn; 2025-07 ~7.3bn; 2026-01 ~8.3bn (not counting Copilot, Meta AI); 2026-07 ~9.9bn (not counting Copilot, Meta AI); 2026-08 ~9.9bn (not counting Copilot, Meta AI)
- clip_r2_oct2024_end: panel on landing frames: 2024-10 ~4.2bn; 2025-04 ~6.5bn; 2025-10 ~8.3bn (Copilot not counted after Sep 2025); 2026-04 ~9.9bn (not counting Copilot, Meta AI); 2026-08 ~9.9bn (not counting Copilot, Meta AI)
