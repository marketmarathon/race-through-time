# HANDOVER — 28 Sep 2026 (session 6, Claude Code cloud session, environment "Race Through Time")

Previous handovers (session 2, Cowork: repo bootstrap, RTT-002 dataset, DATA_AUDIT; session 3: IQ-04; session 4: IQ-05 round 1; session 5: IQ-05 round 2) are in this file's git history. IQ-05 round 2 (pull request #4) was merged to main as `1cba884`.

## Done: IQ-05 round 3, the top-20 pilot with flags (branch `claude/wizardly-darwin-iv7sgt`, pull request open, **not merged**)
Prompt saved as `prompts/CODE_SESSION_IQ-05c.md`. Luke's feedback = DEC-034; his additional instructions during the session = DEC-035 (modern flags; logo and car overlays) and DEC-036 (display-attributes rule); Claude working choices DEC-037 to DEC-044. `marketmarathon/bars` was not touched.
- **Pilot**: `kits/rtt-002/config_pilot_2014_2021_top20.json` only (variant B's config deleted; the winner line stays a switch). FRAME_COUNT_ONLY **2,502 frames = 83.4 s** (round 2: 2,472; the two record holds are now 2.0 s). Full video unchanged at 16,062 frames.
- **Nationality data**: `data/rtt-002/driver_nationality.csv` (116 drivers), built by `scripts/rtt002_nationality.py` from `data/rtt-002/source/wikipedia_wikidata_nationality.psv` and `wikidata_countries.psv`, which Luke supplied (made in his Chrome with `scripts/extract_nationality.browser.js`; hashes verified). This session's own Wikipedia/Wikidata requests got HTTP 429 throughout and were not worked around. Comparison `reports/RTT-002_nationality_comparison.md`: 113 agree, **3 disagreements for Luke** (Jim Clark: Wikidata P1532 Scotland; Phil Hill: P1532 Dominican Republic, P27 United States; Luigi Fagioli: no P1532, P27 Kingdom of Italy). CSV keeps the Wikipedia value. `data/rtt-002/source/README.md` gained a section for the two files (Luke asked for it); no other existing dataset file changed.
- **Flags (DEC-035, DEC-037)**: today's design, npm `flag-icons` 7.5.0 (MIT), no flag file committed; column just left of the bars; 45 × 34 px = 9.1 × 6.9 pt on a phone.
- **Layout (DEC-038, DEC-040)**: bars to about 70% of the width; season / Grand Prix / date block left-aligned at x 820, next to the lower bars, checked on every frame against everything else.
- **Event label (DEC-039)**: "92 wins · Portuguese GP", with the winner glow, until the next race lands, then a 0.3 s fade.
- **Colours (DEC-041)**: top-ten drivers choose first; Hamilton, Schumacher, Verstappen, Senna, Prost (and Vettel, Alonso) have bright colours; rule of CIEDE2000 18 kept.
- **Overlays (DEC-035, DEC-042)**: logo box 124 × 124 top right, car box 440 × 200 bottom right; pictures only from the git-ignored `kits/rtt-002/local_assets/` (`rtt_logo.png`, `rtt_car.png`); missing file = empty box. Tests use plain rectangles made at test time.
- **Rights**: new `reference/rights_ledger.md` (Archivo OFL 1.1, flag-icons MIT, data licences; car picture's licence NOT FOUND until supplied).
- **Process rule (DEC-036)**: `reference/metric_contract_RTT-002.md` has a "Display attributes" section; every future metric contract must list displayed attributes and sources before the data build.
- **Tests / phone**: see `tests/player/RESULTS.md` and the pull request. Tesseract 5.3.4 installed in this container for the OCR read-back.
- Nothing rendered to video, nothing uploaded or published; test frames and phone stills stayed in `tests/output/` (gitignored).

## Not done / open
- Pilot video not rendered (no ffmpeg here). Luke needs an mp4 to judge; render where ffmpeg exists, with the real logo and car files in `local_assets/`, not uploaded without his say.
- The car picture's source and licence must be recorded in the rights ledger before anything using it is published.
- The 3 nationality disagreements, the YouTube-controls strip (footer and date line sit in it), D-05: questions in the pull request.

## Next safe actions
1. Luke reviews the round-3 pull request and answers its questions.
2. Render the pilot for viewing once he agrees where (Cowork supplies logo and car files).
3. IQ-06 live feasibility for RTT-001, 003–012 (not started). IQ-07 not started. New metric contracts follow DEC-036.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md` and `reference/metric_contract_RTT-002.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006: code, configs, data and written results only; logos, pictures, test frames, stills and renders stay out of the repo.
