# HANDOVER — 29 Sep 2026 (session 9, Claude Code cloud session, environment "Race Through Time")

Previous handovers (session 2, Cowork: repo bootstrap, RTT-002 dataset, DATA_AUDIT; session 3: IQ-04; sessions 4–8: IQ-05 rounds 1–5) are in this file's git history. IQ-05 round 5 (race starts, the "91 wins · 306 starts · 29.7%" label; pull request #7) was merged to main as `ee0d4c2`.

## Done: independent check 3 recorded; starts corrected (branch `claude/awesome-planck-etvdg7`, restarted from main @ `ee0d4c2`; pull request against main, **not merged**)
- **Check 3 is done.** Luke ran `prompts/RTT-002_independent_check3_starts.md` in ChatGPT deep research on 29 Sep 2026; Claude in Cowork transcribed the answer into private files on Luke's laptop (`Data/F1_Starts_Check_2026-09-29/`, never committed), froze them and compared them with main @ `ee0d4c2`. Freeze record with the five SHA-256 hashes (as supplied; the files were not in this container): `state/RTT-002_independent_check3_freeze.json`. Report (verbatim from Claude in Cowork): `reports/RTT-002_starts_check3_report.md`. Results: K wins 116/116, starts 102 agree / 7 NOT FOUND / 7 disagree; L 34/36; M 25/26; N 16/16.
- **DEC-058 (owner):** Rubens Barrichello's 2002 Spanish GP (race_index 685) is NOT a start. Documented correction `data/rtt-002/starts_corrections.csv`, applied by `scripts/rtt002_starts.py` (build 1.1) after classification and reported in its checks; the source extract is unchanged. Barrichello 323 → 322; career starts = "List of Formula One drivers" for **116 of 116**; checks **13/13 PASS**; `starts.csv` 14,479 rows. The audited wins files (`races.csv`, `win_credits.csv`, `drivers.csv`, `career_totals.csv`, `cumulative_wins_wide.csv`, `record_progression.csv`) and `driver_nationality.csv` are byte-identical.
- **DEC-059 (owner):** Wikipedia's counting convention is kept (relief drives and Formula 2 cars in championship Grands Prix count as starts): recorded in `reference/metric_contract_RTT-002.md` and `data/rtt-002/STARTS_README.md`, with the video-description note "Starts and win rates follow Wikipedia's Formula One driver statistics; relief drives and Formula 2 entries in championship Grands Prix count as starts."
- **Starts data audit: PASSED** with the DEC-058 correction and the DEC-059 convention.
- **Adapter** rerun (still 1.1): `kits/rtt-002/race_rtt002.json` SHA-256 `7b7ac6e5e1088468e3d30d09f9e4981cc479514669c125625084e11c2ca05b60` (`dataset_hashes.txt`). **Tests** rerun: `tests/player/RESULTS.md`; phone check rerun. Nothing rendered, uploaded or published; `marketmarathon/bars` untouched.

## Not done / open
- Pilot video not rendered (no ffmpeg here); render where ffmpeg and the real `local_assets/` files exist, not uploaded without Luke's say.
- Still open from earlier rounds: the 3 nationality disagreements, the footer in YouTube's controls strip, D-05 (publication risk, incl. the car's trademarks). Add the DEC-059 methodology note to the video description when it is written.

## Next safe actions
1. Luke reviews and merges this pull request.
2. Render the pilot for viewing once he agrees where.
3. IQ-06 live feasibility for RTT-001, 003–012 (not started). IQ-07 not started. New metric contracts follow DEC-036.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md`, `reference/metric_contract_RTT-002.md` and `reference/rights_ledger.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006: code, configs, data and written results only; logos, pictures, test frames, stills and renders stay out of the repo. New data goes in new files; the audited wins files in `data/rtt-002/` stay unchanged; starts corrections go only through `starts_corrections.csv`.
