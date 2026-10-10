# Thumbnails (IQ-23; owner DEC-800, DEC-801; how: DEC-803)

A real board from the approved film on the left, 2–4 big words and the years on the right, a row of the film's own logos or pictures, a bright background. One config per episode; a new episode needs only a new `rtt-###.json`.

**This folder holds code and configs only.** The images are private (DEC-006, DEC-060): they are rendered on a GitHub runner by `.github/workflows/thumbnails.yml` and saved only as a pre-release in `marketmarathon/race-through-time-private`, with every file's SHA-256 in the notes. `tests/player/run_tests_thumbnails.js` fails if an image file appears here.

## Run it
- **On GitHub (the normal way):** Actions → `thumbnails` → Run workflow (optionally list episodes, e.g. `rtt-001 rtt-104`), or push a change to `.github/workflows/thumbnails.yml` on the branch it names. No film or clip workflow is touched.
- **Locally:** `cd kits/rtt-002 && npm ci`, gather each episode's private files under one folder (`<root>/rtt-001/logos/...`, the same layout as that episode's film workflow), then
  `RTT_ASSETS_ROOT=<root> node kits/thumbnails/render_thumbnails.js <out dir outside the repo> [rtt-001 ...]`.

## What it does
1. Draws the episode's approved film config frame by frame at 3840 × 2160 to the frame where the chosen period's figures land, lets the rows settle, and crops the frame (never edits it). It refuses the final period, so the ending is not spoiled.
2. Checks every bar on the crop against the episode's own data file: the figure, the value label at its own precision, the order, and one common scale for the bar lengths (within 1 px). Any difference stops the render.
3. If `overrides` switches off a side panel the crop would cut through, it also draws the unmodified film config and stops unless the board is identical.
4. Lays out each option at 1280 × 720 and saves PNG and JPG (JPG under 2 MB), plus 320 × 180 (phone feed) and 168 × 94 (sidebar) copies, and `<episode>_check.json` (frame, period, every bar's figure, label and data value).

## A config (`rtt-###.json`)
| Key | Meaning |
|---|---|
| `episode`, `kit`, `film_config` | name for the notes; the kit folder; the approved film config in it |
| `private_ref`, `assets_list` | the private repo branch holding the episode's files (main is tried next); the list of private files with SHA-256 (usually `kits/<kit>/assets_sha256.txt`) |
| `at` | the period (an event date of the film's data: month end, quarter end or race date); never the last |
| `crop` | the part of the 1920 × 1080 frame to show (x, y, w, h); keep the whole of every bar and its label |
| `overrides` | optional, only to switch off side panels (merged into the film config key by key) |
| `min_bars` | the render stops if fewer bars are on the crop |
| `check` | the data file and columns: `file`, `date_col`, `id_col` (`id_lower`), `value_col`, `units_per_value` (data unit → the bar's figure), `label_units` (e.g. `{"m": 1e6, "bn": 1e9}`), `period: "month"` for YYYY-MM; or `type: "f1_wins"` for RTT-002 |
| `words`, `word_sizes`, `years` | the big words (one line each, shrunk only as needed to fit), their sizes in px, the year range |
| `rows` | picture rows: `{top, tile_w, tile_h, gap, pad, plain, items: [{file, crop_id}]}`; `file` relative to the episode's private folder; `crop_id` uses the film's own `pictures.crop` for that id; `plain` = no tile (a cut-out photo). Rows and words are centred top to bottom together |
| `layout` | optional positions (`board_w`, `board_x`, `words_x`, `words_top`, `centre_offset`) |
| `options` | `{name, background: "white" | "bright" | "dark", words?, word_sizes?}` — one thumbnail each |

Every picture must already be in `reference/rights_ledger.md` and on the episode's private-file list (the test checks the list).
