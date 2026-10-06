# RTT kit — RTT-001 Browser Wars (share of web browsing by browser, January 1994 – September 2026, all devices) · design pilots 1 and 2 (IQ-13, IQ-13 answers)

**Pilots only: stills and short clips for Luke to choose from. The full film is rendered (DEC-213: private pre-release `rtt-001-film-c3c8c72-run4`) from `config_rtt001_approved_fit.json` with `.github/workflows/rtt001_film.yml`, music "All In" by Everet Almond (`music_rtt001.json`); it awaits Luke's approval by SHA-256** (DEC-069; brief `prompts/CODE_SESSION_IQ-13.md`). Everything new in this round is an option, listed as a question (DEC-169 to DEC-179 in `state/DECISIONS.md`).

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`), extended in IQ-13 with a monthly **share** kind of its quarter-end series mode (RTT-003, IQ-10). Every RTT-001 feature is switched on by a key in these configs or by the race file's `kind: "share"`, and is off for RTT-002 and RTT-003: 21 reference frames of five RTT-002 and RTT-003 configs are pixel-identical before and after, and both test suites pass unchanged.

**The data is not changed** (DEC-167). `data/rtt-001/series.csv` is read as built; the smoothing options are drawn by the player (`rtt_timeline.js` `shareRace`), and the tests check `series.csv` against the build manifest.

| File | What it is |
|---|---|
| `race_rtt001.json` | Player input ("rtt-series/1", kind "share"), written by `scripts/rtt001_adapter.py` from `data/rtt-001/`: one event per month end (393), every share as whole hundredths of a percent exactly as `series.csv`, the estimated style before 2009, the source line, plus (for drawing only) the published figures each pre-2009 line rests on and the five hand-overs |
| `dataset_hashes.txt` | SHA-256 of the adapter's inputs and output (the render checks the output) |
| `config_rtt001_film.json` | The **as-built reference**: straight lines exactly as `series.csv`, one decimal, estimated look before 2009 with the source named, top 10, browser logos on light tiles (DEC-180) or the name only, browser colours. Not a film |
| `config_rtt001_opt_A.json`, `_B`, `_C` | Smoothing options A, B and C of DEC-167 (each extends the one before) |
| `config_rtt001_approved.json` | **Luke's answers to pilot 1 (DEC-184 to DEC-200):** option C, both flagged stretches smoothed, the June 1996 note, crown, no callouts, 0.5 s per month and 0.3 s from January 2014, the chosen title, QQ Browser cropped to its icon; fixed 10 slots. 5,529 frames = 3 min 4 s |
| `config_rtt001_approved_fit.json` | **THE FILM** (Luke, DEC-204 to DEC-207): as approved, with the rows sized to the browsers on the board (`board.fit`, at most twice as thick) |
| `config_rtt001_era_A.json`, `config_rtt001_era_B.json` | Date and era-picture options for Luke (DEC-214 to DEC-218): A = a big year with the month beside our own era picture, bottom right (recommended); B = the year on the device's screen. Player keys `date_block`, `era`, `time_label.mode` "none"; the pictures are drawn in code (DEC-219). Superseded by the photo round below (Luke wants real photographs, DEC-221) |
| `config_rtt001_photos.json`, `era_photos.json`, `config_rtt001_photo_sheet.json`, `config_rtt001_clip_photos_2008_2009.json` | Photo round (pilot 4, DEC-221 to DEC-225): the date top right beside the channel logo (year 112 px, month 40 px, half-second roll) and a real photograph of each era's device bottom right (300 × 225 px rounded tile, 2 s crossfade; player key `era.eras[].file` / `crop` / `bg`, files read from `<assets>/photos/`). `era_photos.json` = the 15 shortlisted Commons photos with page, author, licence, SHA-256 and the attribution line; `recommended` marks Claude's pick. Photos only in the private repo (`assets/rtt-001/photos/candidates/`), hashes in `assets_sha256.txt`. Awaiting Luke's picks |
| `music_rtt001.json` | The film's music record: waiting for Luke's track (`ready: false`); `.github/workflows/rtt001_film.yml` renders nothing until it is ready (DEC-208) |
| `config_rtt001_clip_*.json`, `clips.txt` | The 18 pilot clips (pilot 2 added `clip_fit_2008_2009`, the resize across January 2009): the two big hand-overs × {as built, A, B, C}; the two flagged stretches as built and smoothed; 2010–2013 at 0.40 / 0.50 / 0.65 s per month; 2013–2026 at the film pace and with the proposed faster pace from January 2014 |
| `stills.json`, `render_stills.js`, `sheets.js` | 41 stills (each also at phone size) and 9 side-by-side comparison sheets (s16–s20 and c08 are the logo round, run 3; b01–b04, s21 and c09 are pilot 2, the board-size option); `sheets.js` draws the palette, title and logo sheets |
| `palette_search.js`, `palette_targets.json` | How the browser colours were found (DEC-173) |
| `logos.json` | The browser logos (file page on Commons, en.wikipedia or Apple, licence or non-free status, author, SHA-1, SHA-256, private path, IE crop), our own neutral tiles for Lynx and NetFront, and the pages for Claude in Cowork (DEC-180 to DEC-183) |
| `assets_sha256.txt` | SHA-256 of every private file drawn (Luke's logo and the 26 browser logo files) |
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

Logos: `.github/workflows/rtt001_assets.yml` (with `scripts/rtt001_fetch_logos.py`) downloads the files in `logos.json` (Wikimedia Commons, English Wikipedia or a direct URL) on a GitHub runner, checks each SHA-1 or SHA-256, and commits them to the private repo (Wikimedia rate-limits and then blocks this container).

Render on GitHub: `.github/workflows/rtt001_pilot.yml` (its own workflow, triggered only by a push that changes it on the IQ-13 branch). It fetches Luke's logo and the browser logos from the private repo with `RTT_PRIVATE_TOKEN`, checks its SHA-256 and the player input's, renders the clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Config keys added in IQ-13 (player, share kind)

`values` {decimals 1|2, approx} ("~85%" / "<1%" for estimated values when approx), `smoothing` {mode "none"|"eased", handover_months, include_flagged}, `source_line` {enabled, y, size, prefix, names, short, measure, estimated, changing}, `marker` {enabled, sec, text, size}, `notes_at` [{date, text}] with `note_line` {y, size, sec}, `callout.texts` {crown, crown_extra, passes, passes_extra, estimated}, `time_label.format` "month", `pictures.placeholder` / `placeholder_only` (empty picture boxes, render run 1), `pictures.files` + `tile` (one logo per browser on a light tile, run 2), `pictures.crop` (draw part of a file, e.g. IE6's "e" without the wordmark) and `pictures.own` (our own neutral tile: name and launch year in the bar colour, run 3), `board.fit` {enabled, min_slots, sec} (pilot 2: rows sized to the bars on the board, DEC-202), `pacing.segments[].from` (a faster fixed pace from a named month). Bars that start or stop in the data fade in at their value or fade out over one month's count (`rtt_timeline.js` `shareFrame`).

## Not in this kit

No logo files, stills or renders (DEC-006, DEC-060): logos live only in the private repo. No music this round.
