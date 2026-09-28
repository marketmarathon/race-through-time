# HANDOVER — 28 Sep 2026 (session 4, Claude Code cloud session, environment "Race Through Time")

Previous handovers (session 2, Cowork: repo bootstrap, RTT-002 dataset, DATA_AUDIT; session 3: IQ-04) are in this file's git history. IQ-04 (pull request #2) was merged to main as `4f22b1a`.

## Done: IQ-05, the RTT-002 design pilot (branch `claude/lucid-cannon-l1fo7a`, pull request open, **not merged**)
Prompt saved as `prompts/CODE_SESSION_IQ-05.md`. Implements Luke's DEC-022; Claude working choices DEC-023 to DEC-026. `marketmarathon/bars` was not needed or touched.
- **Colours (DEC-023)**: one colour per driver for the whole video, computed over all 1,164 races (`rtt_timeline.js` `assignColours()`), so the pilot and the full video match. 40 drivers ever reach the top ten; counting rows still fading out (3 races), at most 12 are on screen together, so 12 colours are needed. IQ-04's 12 were not clearly distinct once drawn (three purples, two greens, two blues; closest pair CIEDE2000 9.6), so the palette was replaced by 12 colours chosen to be as far apart as possible (closest pair 18.5) with white names still readable on every bar (contrast ≥ 3.2:1). Rule enforced: drivers on screen together never share a colour and are ≥ 18 apart. No team or nationality colours.
- **Phone sizes (DEC-024)**: axis numbers 20 → 34 px, date 28 → 34 px, footer 17 → 26 px (config `sizes`). On a phone 390 pt wide: axis and date 6.9 pt (names 6.5 pt), footer 5.3 pt. `tests/player/phone_check.js` now prints PASS/FAIL per still (1988, final board, pilot 2020 Portuguese GP): all PASS.
- **Top-ten entries (DEC-025)**: slide-in kept, but an entering row starts just under the board and glides in with `glide.entry_sec` 0.1 s. Clearly visible (opacity ≥ 0.8, name and value drawn) within 5 frames at worst in every case run; rule is < 8 frames. IQ-04's worst was 22 frames.
- **Pilot configs (DEC-026)**: `kits/rtt-002/config_pilot_2014_2021.json` (0.5 s per race) and `config_pilot_2014_2021_fast.json` (0.35 s per race), both built on `config.json` through a new `"extends"` key. Normal title card (range "2014 – 2021"), 3 s hold on the final board, no closing card. FRAME_COUNT_ONLY: **2,277 frames = 75.9 s** (inside the 60–90 s target) and **1,657 frames = 55.2 s**. Full video unchanged at 16,062 frames.
- **Milestones confirmed** from the drawn labels in both pilots: 2020 Eifel GP Hamilton 91, level with Schumacher (Schumacher stays P1: he reached 91 first); 2020 Portuguese GP Hamilton 92, P1.
- **Tests** (`node tests/player/run_tests.js`, results in `tests/player/RESULTS.md`): **11/11 PASS** in 13 min (Playwright 1.56.1 Chromium, tesseract 5.3.4 installed from the Ubuntu archive). All IQ-04 cases still pass. New: both pilots (every value label equal to the data on every frame; OCR 785/785 and 842/842, 0 mismatches), the full RTT-002 run checked on every one of its frames by draw calls (156,008 value labels), top-ten entry visibility in every case, the colour rule on every drawn frame and on every race of the full dataset (computed from `win_credits.csv` alone). Baseline: the unchanged IQ-04 suite on main also passed 7/7 in this container before any change. OCR on the fixtures differs slightly from IQ-04 (e.g. enter_leave 85 read, 40 skipped vs 87/36) only because rows now move differently; labels on rows less than one row apart are not OCR-read, as in IQ-04.
- **Environment contract** unchanged: FRAME_COUNT_ONLY, REF_PNG_DIR at 1920 and 3840 (pilot configs), RASTER_W 2000 refused. The mp4 path (SEG_OUT, ffmpeg) was **not run**: ffmpeg is not installed in this container; that code is unchanged from IQ-04.
- Nothing rendered to video, nothing committed except code, configs and written results; test frames and phone stills stayed in `tests/output/` (gitignored). Nothing uploaded or published.

## Not done / open
- Pilot videos were not rendered: the tests draw and check every frame of both pilots, which was enough to verify them. Luke will need an mp4 of each to judge pace by eye (needs a render in an environment with ffmpeg; not uploaded anywhere without his say).
- The "quieter look" variant from the original IQ-05 line in STATE.json was not made: DEC-022 did not ask for it.
- Shard-join edge pixels (inherited from C2-2, see IQ-04) not revisited.

## Questions put to Luke in the pull request
1. Palette: the new 12 colours are clearly distinct but include some earthier shades (mustard, forest green, brown, khaki). Keep, or accept closer colours for a softer look?
2. Pace: 75.9 s at 0.5 s per race sits in the target; the fast version is 55.2 s. Which one (after watching)?
3. Key moments: the pacing rule gives the 2020 Eifel GP (Hamilton equals 91) the short "quiet" beat, because nobody changes place; and at the Portuguese GP the overtake is still gliding when the next race lands. Hold key milestones longer?
4. D-05 publication risk is still open (before release only).

## Next safe actions
1. Luke reviews the IQ-05 pull request and answers the questions; render the two pilots for viewing once he agrees where.
2. IQ-06 live feasibility for RTT-001, 003–012 (not started, as instructed). IQ-07 not started.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md` and `reference/metric_contract_RTT-002.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006: code, configs and written results only; test frames, stills and renders stay out of the repo.

