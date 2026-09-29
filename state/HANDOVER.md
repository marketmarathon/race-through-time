# HANDOVER — 29 Sep 2026 (session 8, Claude Code cloud session, environment "Race Through Time")

Previous handovers (session 2, Cowork: repo bootstrap, RTT-002 dataset, DATA_AUDIT; session 3: IQ-04; sessions 4–7: IQ-05 rounds 1–4) are in this file's git history. IQ-05 round 4 (pull request #6) was merged to main as `d00e5fb`.

## Done: IQ-05 round 5 (branch `claude/awesome-planck-etvdg7`, based on `origin/marketmarathon-patch-1`; pull request against main, **not merged**)
Prompt saved as `prompts/CODE_SESSION_IQ-05e.md`. Luke's decision = DEC-053 (owner); Claude working choices DEC-054 (bar length, on the session's instruction) to DEC-056. `marketmarathon/bars` was not touched; no existing file in `data/rtt-002/` was changed. Both source hashes verified before work (`wikipedia_starts_extract.psv` `b26c0ed4…`, `extract_starts.browser.js` `ac8edfdb…`).
- **Contract first (DEC-036)**: starts and win rate added to "Display attributes" in `reference/metric_contract_RTT-002.md` (definition, source, half-up rounding), committed before the data build.
- **Starts data**: `scripts/rtt002_starts.py` → new files `data/rtt-002/starts.csv` (14,480 rows), `career_starts.csv`, `STARTS_CHECKS.md`, `starts_checks.json`, `starts_manifest.json`, `STARTS_README.md`. 12/12 checks pass and reproduce the prototype exactly: round counts = `races.csv` in all 77 seasons (2026: 23 listed, 15 run); every one of 1,167 win credits has a start; career starts = "List of Formula One drivers" (rev. 1377016608) for 115 of 116. **Open: Rubens Barrichello 323 (season tables) vs 322 (List page)**, kept at 323; 94 candidate races listed, the 2002 Spanish GP ("Ret") the named example (D-08).
- **Adapter** 1.0 → **1.1** (starts per race); `race_rtt002.json` SHA-256 `0fc72b84f41ad0b589a8094173d9aebc5ae1e1554c8241a70e31e4be3d5d1e52` (`kits/rtt-002/dataset_hashes.txt`).
- **Pilot** (`config_pilot_2014_2021_top20.json`): stats label on every bar, "92 wins · 262 starts · 35.1%" (win count bold, rest caption grey, 29 px = 5.9 pt on a phone); event label off; winner glow, date line, logo and car boxes, footer unchanged. `barend` back to **1420** (round 3's bars, DEC-054): nothing needed shortening. FRAME_COUNT_ONLY **2,502 frames = 83.4 s** (unchanged). Full video unchanged: 16,062 frames, `config.json` draws as before.
- **Tests / phone**: `tests/player/RESULTS.md` (new checks 26–28, new case `shared_drive_round5`); phone check PASS, thresholds unchanged. tesseract 5.3.4 was installed in this container for the OCR read-back.
- Nothing rendered to video, nothing uploaded or published; test frames and phone stills stayed in `tests/output/` (git-ignored).

## Not done / open
- Pilot video not rendered (no ffmpeg here); render where ffmpeg and the real `local_assets/` files exist, not uploaded without Luke's say.
- Questions for Luke (in the pull request): D-08 Barrichello 323 vs 322; D-09 a second independent check of the starts; still open from earlier rounds: the 3 nationality disagreements, the footer in YouTube's controls strip, D-05 (incl. the car's trademarks).

## Next safe actions
1. Luke reviews the round-5 pull request and answers its questions.
2. Render the pilot for viewing once he agrees where.
3. IQ-06 live feasibility for RTT-001, 003–012 (not started). IQ-07 not started. New metric contracts follow DEC-036.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md`, `reference/metric_contract_RTT-002.md` and `reference/rights_ledger.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006: code, configs, data and written results only; logos, pictures, test frames, stills and renders stay out of the repo. New data goes in new files; existing files in `data/rtt-002/` stay unchanged.
