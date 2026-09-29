# RTT kit — RTT-002 (F1 Grand Prix wins) · player RTT-1 · IQ-04, IQ-05 pilots (round 4)

The Race Through Time player, copied from Market Marathon's Format C2-2 renderer. **Not greenlit for render.** IQ-05 added the design-pilot changes (DEC-022 to DEC-025): one colour per driver with no two drivers on screen together in the same or a similar colour, larger axis numbers / date / footer for phones, a faster slide-in for drivers entering the top ten, and two pilot configs. IQ-05 round 2 (DEC-027 to DEC-033) replaced the pilots with two variants that differ only in the board (A: top 20; B: top ten plus a winner line), and added, all switched by config: a gentle winner highlight, record-moment holds, an opening on the board instead of a title card, an exact final-board hold, and a configurable board geometry. `config.json` draws exactly as before. IQ-05 round 3 (DEC-034 to DEC-044): Luke chose A (top 20); variant B's config is deleted (the winner line stays a switch). Added, all switched by config: nationality flags in a column left of the bars, the Grand Prix after a winner's value ("92 wins · Portuguese GP"), wider bars, the season/Grand Prix/date block next to the board, colour priority for the drivers who reach the top ten, 2.0 s record holds, and reserved boxes for Luke's logo and a car picture (loaded only from the git-ignored `local_assets/`). IQ-05 round 4 (DEC-045 to DEC-050): the logo box takes Luke's logo as a round badge with RACE THROUGH TIME inside the globe (154 × 154, 1 : 1, DEC-051), the car box the real car photo (600 × 163, about 3.67 : 1, CC BY 4.0, credit in the footer, `reference/rights_ledger.md`), the event label carries the race date ("92 wins · Portuguese GP · 25 October 2020"), the big season/Grand Prix/date block is replaced by one small date line next to the title ("25 October 2020 · Portuguese GP"), and the bars are 12% shorter so the longest dated label still fits.

Copied from `marketmarathon/bars` @ `2a10877695e83683c3caae651cad61fc686614eb` (22 Sep 2026), kit `MarketMarathon_RaceKit_RF_US_C2_v3.zip`: `player_formatc2.html` (sha256 `39e32a54…64b7`) → `player_rtt.html`, `formatc.js` (sha256 `4609799a…b7a`) → `rtt.js`. Nothing in `bars` was changed (DEC-002).

| File | What it is |
|---|---|
| `player_rtt.html` | The drawing (canvas, 1920×1080 space, scaled by `RASTER_W`) |
| `rtt_timeline.js` | Event rules: counts after each race, tie order, pacing, frame of every event. Loaded by both the page and the driver |
| `rtt.js` | Driver. Same environment contract as `formatc.js` |
| `config.json` | Everything RTT-specific: words, unit, palette and colour rule, pacing, window, sizes, layout tokens |
| `config_pilot_2014_2021_base.json` | Shared pilot settings: `config.json` + window 2014–2021, 0.5 s per race judged on the top ten, board from the first frame (no title card), record holds (2.0 s), winner highlight, final board 10 s, no closing card. Not rendered on its own |
| `config_pilot_2014_2021_top20.json` | The pilot (round 4): the base + 20 rows, flags, dated event label, date line next to the title, overlay boxes for the round logo badge and the car photo, car credit in the footer, its own 22-colour palette with colour priority |
| `local_assets/` | **Git-ignored.** Private pictures for the overlays (`rtt_logo.png`: Luke's logo as a round badge, 885 × 885, transparent outside the circle; `rtt_car.png`: the car photo with its background removed, 3435 × 936), supplied at render time by Claude in Cowork; never committed (DEC-006). Missing file = empty box, the render goes on |
| `race_rtt002.json` | Player input, written by `scripts/rtt_adapter.py` from `data/rtt-002/` (CC BY-SA 4.0, see `data/rtt-002/ATTRIBUTION.md`) |
| `dataset_hashes.txt` | SHA-256 of the adapter's three inputs and its output |
| `package.json`, `package-lock.json` | Playwright 1.56.1, `@fontsource/archivo` 5.3.0 (Archivo, SIL OFL 1.1) and `flag-icons` 7.5.0 (MIT); licences in `reference/rights_ledger.md` |

## Run

```
cd kits/rtt-002
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
FRAME_COUNT_ONLY=1 node rtt.js                                   # FRAMES <n>
SEG_START=0 SEG_END=300 REF_PNG_DIR=out node rtt.js              # lossless PNGs, 1920 preview
SEG_START=0 SEG_END=300 SEG_OUT=seg.mp4 RASTER_W=3840 node rtt.js  # needs ffmpeg on PATH
```
`PW_CHROME=/path/to/chromium` picks the browser (as in `formatc.js`). `RTT_CONFIG=other.json` selects another config, e.g. a quieter variant or a short passage (`"window": {"from": "1984-01-01", "to": "1989-12-31"}`). A config can start from another with `"extends": "config.json"` and change only some keys (objects merge key by key; lists and values replace).

Pilot (IQ-05 round 4):
```
RTT_CONFIG=config_pilot_2014_2021_top20.json FRAME_COUNT_ONLY=1 node rtt.js   # FRAMES 2502 = 83.4 s
```
Put `rtt_logo.png` and `rtt_car.png` in `local_assets/` (or point `RTT_LOCAL_ASSETS` at a folder) before a real render; without them the boxes stay empty.
Config keys added in round 2 (all optional; absent = IQ-05 behaviour): `board` {bar_gap, name_frac, value_frac}; `highlight` {enabled, sec, mix, glow}; `winner_line` {enabled}; `record_hold` {enabled, sec, types}; `pacing.judge_rows`; `pacing.final_board_sec`; `sizes.winner`. Round 3: `flags` {enabled, column, height_frac, gap, csv}; `event_label` {enabled, fade_sec}; `time_label.mode` "block" {x, date_y, align}; `overlays` [{name, file, x, y, w, h}]; `local_assets`; `colour_rule.priority` {rows, bright}. Round 4: `time_label.mode` "line" {x, y, align, size} (one date line; `winner_line` cannot be combined with it); `event_label.date`; `overlay_gap` (axis grid lines stop this far short of every overlay box). With `intro_sec` 0 there is no title card and the board (title on it) is the first frame.

Numbers: Archivo has tabular figures (`tnum`, checked in every weight with fontTools), but Chrome's canvas cannot switch OpenType features on, so every number (values, axis, season, date, date line, event label, winner line) is drawn digit by digit on the widest digit's width, as C2-2 did. The tests check this on every label.

Colours: `rtt_timeline.js` `assignColours()` gives each driver one palette colour over the WHOLE race file (never the window), so a pilot and the full video agree. Drivers who can be on screen together (the top ten after a race and the `colour_rule.fade_races` races before it, covering rows still fading out) never get the same colour or two colours closer than `colour_rule.min_delta_e` (CIEDE2000 on the colour as drawn). If the palette runs out the player refuses to render. RTT-002 needs 12 colours on a top-ten board (at most 12 drivers can be on screen together); the 12 in `config.json` are all at least CIEDE2000 18.5 apart. A 20-row board needs 22 (up to 22 on screen together); `config_pilot_2014_2021_top20.json` has 22 at least 18.2 apart. Every driver's colour on each board is listed in `tests/player/RESULTS.md`.

Rebuild the input (deterministic; compare with `dataset_hashes.txt`):
```
python scripts/rtt_adapter.py data/rtt-002 kits/rtt-002/race_rtt002.json --dataset-id RTT-002 --hash-file kits/rtt-002/dataset_hashes.txt
```

Tests: `node tests/player/run_tests.js` (results in `tests/player/RESULTS.md`), phone check `node tests/player/phone_check.js`.

## What is not in this kit
No music, logo, pictures, flag files or Market Marathon fonts are committed. Flags come from the npm package at install time; Luke's logo and the car picture live only in the git-ignored `local_assets/`. There is no render workflow: none was asked for, and none may upload or publish.
