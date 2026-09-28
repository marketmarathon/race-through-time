# RTT kit — RTT-002 (F1 Grand Prix wins) · player RTT-1 · IQ-04, IQ-05 pilot

The Race Through Time player, copied from Market Marathon's Format C2-2 renderer. **Not greenlit for render.** IQ-05 added the design-pilot changes (DEC-022 to DEC-025): one colour per driver with no two drivers on screen together in the same or a similar colour, larger axis numbers / date / footer for phones, a faster slide-in for drivers entering the top ten, and two pilot configs.

Copied from `marketmarathon/bars` @ `2a10877695e83683c3caae651cad61fc686614eb` (22 Sep 2026), kit `MarketMarathon_RaceKit_RF_US_C2_v3.zip`: `player_formatc2.html` (sha256 `39e32a54…64b7`) → `player_rtt.html`, `formatc.js` (sha256 `4609799a…b7a`) → `rtt.js`. Nothing in `bars` was changed (DEC-002).

| File | What it is |
|---|---|
| `player_rtt.html` | The drawing (canvas, 1920×1080 space, scaled by `RASTER_W`) |
| `rtt_timeline.js` | Event rules: counts after each race, tie order, pacing, frame of every event. Loaded by both the page and the driver |
| `rtt.js` | Driver. Same environment contract as `formatc.js` |
| `config.json` | Everything RTT-specific: words, unit, palette and colour rule, pacing, window, sizes, layout tokens |
| `config_pilot_2014_2021.json` | IQ-05 pilot: `config.json` + window 2014–2021, 0.5 s per race, no closing card (3 s hold on the final board) |
| `config_pilot_2014_2021_fast.json` | Same pilot at 0.35 s per race |
| `race_rtt002.json` | Player input, written by `scripts/rtt_adapter.py` from `data/rtt-002/` (CC BY-SA 4.0, see `data/rtt-002/ATTRIBUTION.md`) |
| `dataset_hashes.txt` | SHA-256 of the adapter's three inputs and its output |
| `package.json`, `package-lock.json` | Playwright 1.56.1 and `@fontsource/archivo` 5.3.0 (Archivo, SIL OFL 1.1) |

## Run

```
cd kits/rtt-002
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
FRAME_COUNT_ONLY=1 node rtt.js                                   # FRAMES <n>
SEG_START=0 SEG_END=300 REF_PNG_DIR=out node rtt.js              # lossless PNGs, 1920 preview
SEG_START=0 SEG_END=300 SEG_OUT=seg.mp4 RASTER_W=3840 node rtt.js  # needs ffmpeg on PATH
```
`PW_CHROME=/path/to/chromium` picks the browser (as in `formatc.js`). `RTT_CONFIG=other.json` selects another config, e.g. a quieter variant or a short passage (`"window": {"from": "1984-01-01", "to": "1989-12-31"}`). A config can start from another with `"extends": "config.json"` and change only some keys (objects merge key by key; lists and values replace).

Pilots (IQ-05):
```
RTT_CONFIG=config_pilot_2014_2021.json      FRAME_COUNT_ONLY=1 node rtt.js   # FRAMES 2277 = 75.9 s
RTT_CONFIG=config_pilot_2014_2021_fast.json FRAME_COUNT_ONLY=1 node rtt.js   # FRAMES 1657 = 55.2 s
```

Colours: `rtt_timeline.js` `assignColours()` gives each driver one palette colour over the WHOLE race file (never the window), so a pilot and the full video agree. Drivers who can be on screen together (the top ten after a race and the `colour_rule.fade_races` races before it, covering rows still fading out) never get the same colour or two colours closer than `colour_rule.min_delta_e` (CIEDE2000 on the colour as drawn). If the palette runs out the player refuses to render. RTT-002 needs 12 colours (at most 12 drivers can be on screen together); the 12 in `config.json` are all at least CIEDE2000 18.5 apart, and every driver's colour is listed in `tests/player/RESULTS.md`.

Rebuild the input (deterministic; compare with `dataset_hashes.txt`):
```
python scripts/rtt_adapter.py data/rtt-002 kits/rtt-002/race_rtt002.json --dataset-id RTT-002 --hash-file kits/rtt-002/dataset_hashes.txt
```

Tests: `node tests/player/run_tests.js` (results in `tests/player/RESULTS.md`), phone check `node tests/player/phone_check.js`.

## What is not in this kit
No music, logo, flags, icons, pictures or Market Marathon fonts. RTT has no logo yet (NOT FOUND). There is no render workflow: none was asked for, and none may upload or publish.
