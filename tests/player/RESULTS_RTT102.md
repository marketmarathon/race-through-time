# RTT-102 player tests (IQ-19, design round 1)

Run: node tests/player/run_tests_rtt102.js · ALL PASS

0. Data untouched: PASS (series_monthly.csv and identities.csv as data/rtt-102/manifest.json; race_rtt102.json as dataset_hashes.txt)
9. Colours: closest pair as drawn CIEDE2000 20.0 (gemini/deepseek) PASS (>= 18); colour-blind (protan/deutan simulation) closest 10.2 (copilot/deepseek), reported
11. Eased vs straight lines, month-end order of all places: 1 month(s) differ:
   - 2024-12: chatgpt > gemini > perplexity > claude > copilot > meta_ai  vs eased  chatgpt > gemini > perplexity > copilot > claude > meta_ai

| Case | Config | Frames | Result |
|---|---|---|---|
| base | config_rtt102_base.json | 1752 | PASS |
| eased | config_rtt102_base.json | 1764 | PASS |
| quarter | config_rtt102_base.json | 1872 | PASS |
| between_2dp | config_rtt102_base.json | 1752 | PASS |
| analyst_note_only | config_rtt102_base.json | 1752 | PASS |
| story | config_rtt102_story.json | 1752 | PASS |
| story_bard | config_rtt102_story_bard.json | 1752 | PASS |
| final_line | config_rtt102_base.json | 1752 | PASS |
| clip_e_2024_linear | config_rtt102_clip_e_2024_linear.json | 432 | PASS |
| clip_e_2024_eased | config_rtt102_clip_e_2024_eased.json | 432 | PASS |
| clip_f_month_0p75 | config_rtt102_clip_f_month_0p75.json | 336 | PASS |
| clip_f_month_1p0 | config_rtt102_clip_f_month_1p0.json | 408 | PASS |
| clip_f_month_1p5 | config_rtt102_clip_f_month_1p5.json | 552 | PASS |
| clip_f_quarter_2p25 | config_rtt102_clip_f_quarter_2p25.json | 282 | PASS |
| clip_f_quarter_3p0 | config_rtt102_clip_f_quarter_3p0.json | 336 | PASS |
| clip_f_quarter_4p5 | config_rtt102_clip_f_quarter_4p5.json | 444 | PASS |

Notes:
- story: card 15 Nov 2023 = V35 (VERIFIED (WebFetch))
- story: card 18 Apr 2024 = V37 (VERIFIED (WebFetch))
- story: card 13 May 2024 = V40 (VERIFIED (WebFetch))
- story: card 19 Feb 2025 = V39 (VERIFIED (WebFetch))
- story: card dated 2023-11 first on screen 0.0 s after its month starts
- story: card dated 2024-04 first on screen 0.0 s after its month starts
- story: card dated 2024-05 first on screen 3.0 s after its month starts
- story: card dated 2025-02 first on screen 0.0 s after its month starts
- story_bard: card 15 Nov 2023 = V35 (VERIFIED (WebFetch))
- story_bard: card 8 Feb 2024 = V34 (VERIFIED (WebFetch))
- story_bard: card 18 Apr 2024 = V37 (VERIFIED (WebFetch))
- story_bard: card 13 May 2024 = V40 (VERIFIED (WebFetch))
- story_bard: card 19 Feb 2025 = V39 (VERIFIED (WebFetch))
- story_bard: card dated 2023-11 first on screen 0.0 s after its month starts
- story_bard: card dated 2024-02 first on screen 0.4 s after its month starts
- story_bard: card dated 2024-04 first on screen 2.4 s after its month starts
- story_bard: card dated 2024-05 first on screen 5.4 s after its month starts
- story_bard: card dated 2025-02 first on screen 0.2 s after its month starts
