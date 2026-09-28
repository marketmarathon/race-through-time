# HANDOVER — 28 Sep 2026 (session 5, Claude Code cloud session, environment "Race Through Time")

Previous handovers (session 2, Cowork: repo bootstrap, RTT-002 dataset, DATA_AUDIT; session 3: IQ-04; session 4: IQ-05 round 1) are in this file's git history. IQ-05 round 1 (pull request #3) was merged to main as `2aeabc1`.

## Done: IQ-05 round 2, two pilot variants for RTT-002 (branch `claude/stoic-mccarthy-kmbv2a`, pull request open, **not merged**)
Prompt saved as `prompts/CODE_SESSION_IQ-05b.md`. Luke's feedback recorded as DEC-027; Claude working choices DEC-028 to DEC-033. `marketmarathon/bars` was not needed or touched.
- **Two pilots, identical except the board (DEC-028)**: A `kits/rtt-002/config_pilot_2014_2021_top20.json` (20 rows) and B `kits/rtt-002/config_pilot_2014_2021_top10_winner.json` (top ten + "Won by … · n wins" under the date). Both extend `config_pilot_2014_2021_base.json` (round 1's pilot config, renamed); the fast config is deleted. Pace 0.5 s per race, judged on the top ten in both so the timestamps are identical. FRAME_COUNT_ONLY: **A 2,472 frames = 82.4 s, B 2,472 frames = 82.4 s**. Full video unchanged at 16,062 frames.
- **Winner highlight (DEC-030)**: winner's bar brightened 30% towards white with a soft glow, fading over 0.4 s; stays lit through a winning streak (no flicker); nothing for a winner off the board.
- **Record holds (DEC-031)**: 1.5 s on races that equal or take the all-time record (record_progression.csv BECOMES_JOINT / BECOMES_SOLE). In the pilot: 11 Oct 2020 Eifel GP (Hamilton 91, joint) and 25 Oct 2020 Portuguese GP (Hamilton 92, sole).
- **Opening and ending (DEC-032)**: no title card; board with title from frame 0 (2 s on the opening board); final board exactly 10 s, no closing card.
- **Colours (DEC-029)**: top 20 needs 22 colours (up to 22 drivers on screen together); own 22-colour palette, closest pair CIEDE2000 18.2, rule of 18 kept. Top-ten colours unchanged.
- **Sizes and digits (DEC-033)**: A names and values 29 px (5.9 pt on a phone; round 1 names 6.5 pt). B winner line 34 px (6.9 pt). Archivo has tabular figures but canvas cannot turn them on; every number is drawn on fixed-pitch digits (checked).
- **Phone check**: PASS on all eight stills, both variants, thresholds unchanged. Note: the thresholds are relative to the driver names, so A passes partly because its names are smaller; the absolute sizes are reported next to the checks.
- **Tests**: see `tests/player/RESULTS.md` and the pull request.
- **Environment contract** unchanged (FRAME_COUNT_ONLY, SEG_START/SEG_END, REF_PNG_DIR, RASTER_W, NOMUX). With `intro_sec` 0 the driver plans no intro frames. ffmpeg is still not installed here, so no mp4 was made.
- Nothing rendered to video, nothing committed except code, configs and written results; test frames and phone stills stayed in `tests/output/` (gitignored). Nothing uploaded or published.

## Not done / open
- Pilot videos not rendered (no ffmpeg in this container). Luke needs an mp4 of each to choose (blueprint: choose from rendered evidence); needs a render in an environment with ffmpeg, not uploaded anywhere without his say.
- Shard-join edge pixels (inherited from C2-2, see IQ-04) not revisited.

## Questions put to Luke in the pull request
See the pull request: top 20 vs top ten + winner line; the top-20 colours (Hamilton and Verstappen get dark colours there); whether the streak glow is right; keep the record holds; D-05 still open before release.

## Next safe actions
1. Luke reviews the round-2 pull request; render both pilots for viewing once he agrees where.
2. IQ-06 live feasibility for RTT-001, 003–012 (not started). IQ-07 not started.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md` and `reference/metric_contract_RTT-002.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006: code, configs and written results only; test frames, stills and renders stay out of the repo.
