# RTT kit — RTT-002 (F1 Grand Prix wins) · player RTT-1 · IQ-04

The Race Through Time player, copied from Market Marathon's Format C2-2 renderer. **Not greenlit for render**; this kit exists so IQ-05 (design pilot) can start.

Copied from `marketmarathon/bars` @ `2a10877695e83683c3caae651cad61fc686614eb` (22 Sep 2026), kit `MarketMarathon_RaceKit_RF_US_C2_v3.zip`: `player_formatc2.html` (sha256 `39e32a54…64b7`) → `player_rtt.html`, `formatc.js` (sha256 `4609799a…b7a`) → `rtt.js`. Nothing in `bars` was changed (DEC-002).

| File | What it is |
|---|---|
| `player_rtt.html` | The drawing (canvas, 1920×1080 space, scaled by `RASTER_W`) |
| `rtt_timeline.js` | Event rules: counts after each race, tie order, pacing, frame of every event. Loaded by both the page and the driver |
| `rtt.js` | Driver. Same environment contract as `formatc.js` |
| `config.json` | Everything RTT-specific: words, unit, palette, pacing, window, layout tokens |
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
`PW_CHROME=/path/to/chromium` picks the browser (as in `formatc.js`). `RTT_CONFIG=other.json` selects another config, e.g. a quieter variant or a short passage (`"window": {"from": "1984-01-01", "to": "1989-12-31"}`).

Rebuild the input (deterministic; compare with `dataset_hashes.txt`):
```
python scripts/rtt_adapter.py data/rtt-002 kits/rtt-002/race_rtt002.json --dataset-id RTT-002 --hash-file kits/rtt-002/dataset_hashes.txt
```

Tests: `node tests/player/run_tests.js` (results in `tests/player/RESULTS.md`), phone check `node tests/player/phone_check.js`.

## What is not in this kit
No music, logo, flags, icons, pictures or Market Marathon fonts. RTT has no logo yet (NOT FOUND). There is no render workflow: none was asked for, and none may upload or publish.
