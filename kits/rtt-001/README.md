# RTT kit — RTT-001 Browser Wars (share of web browsing by browser, January 1994 – September 2026, all devices) · design pilot 1 (IQ-13)

**Pilot only: stills and short clips for Luke to choose from. No film is rendered** (DEC-069; brief `prompts/CODE_SESSION_IQ-13.md`). Everything new in this round is an option, listed as a question (DEC-169 to DEC-179 in `state/DECISIONS.md`).

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`), extended in IQ-13 with a monthly **share** kind of its quarter-end series mode (RTT-003, IQ-10). Every RTT-001 feature is switched on by a key in these configs or by the race file's `kind: "share"`, and is off for RTT-002 and RTT-003: 21 reference frames of five RTT-002 and RTT-003 configs are pixel-identical before and after, and both test suites pass unchanged.

**The data is not changed** (DEC-167). `data/rtt-001/series.csv` is read as built; the smoothing options are drawn by the player (`rtt_timeline.js` `shareRace`), and the tests check `series.csv` against the build manifest.

| File | What it is |
|---|---|
| `race_rtt001.json` | Player input ("rtt-series/1", kind "share"), written by `scripts/rtt001_adapter.py` from `data/rtt-001/`: one event per month end (393), every share as whole hundredths of a percent exactly as `series.csv`, the estimated style before 2009, the source line, plus (for drawing only) the published figures each pre-2009 line rests on and the five hand-overs |
| `dataset_hashes.txt` | SHA-256 of the adapter's inputs and output (the render checks the output) |
| `config_rtt001_film.json` | The **as-built reference**: straight lines exactly as `series.csv`, one decimal, estimated look before 2009 with the source named, top 10, browser logos on light tiles (DEC-180) or the name only, browser colours. Not a film |
| `config_rtt001_opt_A.json`, `_B`, `_C` | Smoothing options A, B and C of DEC-167 (each extends the one before) |
| `config_rtt001_clip_*.json`, `clips.txt` | The 17 pilot clips: the two big hand-overs × {as built, A, B, C}; the two flagged stretches as built and smoothed; 2010–2013 at 0.40 / 0.50 / 0.65 s per month; 2013–2026 at the film pace and with the proposed faster pace from January 2014 |
| `stills.json`, `render_stills.js`, `sheets.js` | 28 stills (each also at phone size) and 7 side-by-side comparison sheets; `sheets.js` draws the palette, title and logo sheets |
| `palette_search.js`, `palette_targets.json` | How the browser colours were found (DEC-173) |
| `logos.json` | The 15 browser logos (Commons file page, licence, author, SHA-1, SHA-256, private path) and the browsers shown by name only (DEC-180, DEC-181) |
| `assets_sha256.txt` | SHA-256 of every private file drawn (Luke's logo and the 15 browser logos) |
| `description_credits.md` | Draft credits for the YouTube description (DEC-166; StatCounter CC BY-SA 3.0 with link) |

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
python scripts/rtt001_adapter.py data/rtt-001 kits/rtt-001/race_rtt001.json --hash-file kits/rtt-001/dataset_hashes.txt   # from the repo root
RTT_CONFIG=../rtt-001/config_rtt001_opt_C.json FRAME_COUNT_ONLY=1 node rtt.js      # FRAMES 6630 = 3 min 41 s at 0.5 s per month
RTT_LOCAL_ASSETS=<folder with rtt_logo.png> RTT_CONFIG=../rtt-001/config_rtt001_clip_h1_ews_statmarket_C.json SEG_OUT=h1c.mp4 node rtt.js
RTT_LOCAL_ASSETS=<same> node ../rtt-001/render_stills.js OUT_DIR                  # stills and sheets (write them outside the repo)
node tests/player/run_tests_rtt001.js ; node tests/player/phone_check_rtt001.js  # from the repo root
```

Logos: `.github/workflows/rtt001_assets.yml` (with `scripts/rtt001_fetch_logos.py`) downloads the files in `logos.json` from Wikimedia Commons on a GitHub runner, checks each SHA-1, and commits them to the private repo (Commons rate-limits this container).

Render on GitHub: `.github/workflows/rtt001_pilot.yml` (its own workflow, triggered only by a push that changes it on the IQ-13 branch). It fetches Luke's logo and the browser logos from the private repo with `RTT_PRIVATE_TOKEN`, checks its SHA-256 and the player input's, renders the clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Config keys added in IQ-13 (player, share kind)

`values` {decimals 1|2, approx} ("~85%" / "<1%" for estimated values when approx), `smoothing` {mode "none"|"eased", handover_months, include_flagged}, `source_line` {enabled, y, size, prefix, names, short, measure, estimated, changing}, `marker` {enabled, sec, text, size}, `notes_at` [{date, text}] with `note_line` {y, size, sec}, `callout.texts` {crown, crown_extra, passes, passes_extra, estimated}, `time_label.format` "month", `pictures.placeholder` / `placeholder_only` (empty picture boxes, render run 1), `pictures.files` + `tile` (one logo per browser on a light tile, run 2), `pacing.segments[].from` (a faster fixed pace from a named month). Bars that start or stop in the data fade in at their value or fade out over one month's count (`rtt_timeline.js` `shareFrame`).

## Not in this kit

No logo files, stills or renders (DEC-006, DEC-060): logos live only in the private repo. No music this round.
