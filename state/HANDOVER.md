# HANDOVER — 28 Sep 2026 (session 7, Claude Code cloud session, environment "Race Through Time")

Previous handovers (session 2, Cowork: repo bootstrap, RTT-002 dataset, DATA_AUDIT; session 3: IQ-04; sessions 4–6: IQ-05 rounds 1–3) are in this file's git history. IQ-05 round 3 (pull request #5) was merged to main as `d772f45`.

## Done: IQ-05 round 4 (branch `claude/charming-dirac-d7g4up`, pull request open, **not merged**)
Prompt saved as `prompts/CODE_SESSION_IQ-05d.md`. Luke's feedback on round 3 = DEC-045 (owner); Claude working choices DEC-046 to DEC-050. `marketmarathon/bars` was not touched; nothing in `data/rtt-002/` was changed.
- **Pilot**: `kits/rtt-002/config_pilot_2014_2021_top20.json`. FRAME_COUNT_ONLY **2,502 frames = 83.4 s** (unchanged from round 3). Full video unchanged at 16,062 frames and still passes every test.
- **Logo (DEC-045 (1), DEC-048)**: box 330 × 132 (2.5 : 1) at x 1526, y 18, for Luke's full logo with its wordmark (`local_assets/rtt_logo.png`, 1983 × 793).
- **Event label (DEC-045 (2), DEC-047)**: "92 wins · Portuguese GP · 25 October 2020". To keep the longest label (the leader's "· Emilia Romagna GP · 1 November 2020") inside the 64 px margin, `barend` 1420 → 1265: bars **12% shorter**, leader's bar ends at 62% of the width (round 3: 70%). Furthest label edge x 1853 (limit 1856).
- **Date line (DEC-045 (3), DEC-046)**: big season/Grand Prix/date block gone; one line "25 October 2020 · Portuguese GP" on the title's baseline at x 860, 34 px (6.9 pt on a phone), every frame, including the 49 of 160 races (31%) won by a driver off the board.
- **Car photo (DEC-045 (4), DEC-048, DEC-050)**: box 600 × 163 at x 1256, y 787 (bottom edge y 950, above the 130 px controls strip), for `local_assets/rtt_car.png` (3435 × 936). Licence checked with one Commons API request (SHA-1, author, CC BY 4.0 match). Recorded in `reference/rights_ledger.md`; footer credit added; trademark note added under D-05. Axis grid lines now stop 12 px short of both boxes.
- **Tests / phone**: `tests/player/RESULTS.md`; phone check PASS (thresholds unchanged). Placeholders have the real files' shapes, made at test time, never committed.
- Nothing rendered to video, nothing uploaded or published; test frames and phone stills stayed in `tests/output/` (gitignored). The real logo and car files were not in this container, so they were not seen.

## Not done / open
- Pilot video not rendered (no ffmpeg here). Render where ffmpeg exists with the real `rtt_logo.png` and `rtt_car.png` in `local_assets/`; not uploaded without Luke's say.
- Questions for Luke in the pull request: bars at 62% (below the blueprint's two-thirds) or an alternative; the 3 nationality disagreements (still open from round 3); the footer sits in the bottom strip YouTube's controls can cover; D-05 (now including the car's trademarks).

## Next safe actions
1. Luke reviews the round-4 pull request and answers its questions.
2. Render the pilot for viewing once he agrees where (Cowork supplies logo and car files).
3. IQ-06 live feasibility for RTT-001, 003–012 (not started). IQ-07 not started. New metric contracts follow DEC-036.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md`, `reference/metric_contract_RTT-002.md` and `reference/rights_ledger.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006: code, configs, data and written results only; logos, pictures, test frames, stills and renders stay out of the repo.
