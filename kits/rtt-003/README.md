# RTT kit — RTT-003 (Best-Selling Consoles 1985–2026, units shipped) · design pilot IQ-10, round 2

**Round 2 (Luke, 2 Oct 2026, DEC-114 to DEC-121):** 15 rows; the numbers count smoothly and land on the exact data at every quarter end; the maker's logo beside each picture; no separate maker key (the bottom-right panel is the company scoreboard, kept); taller sizing for portrait pictures; callouts at the crown changes plus Game Boy first past 100 million and DS passes Game Boy (Switch passes DS on hold); a final-table line and the PS2 footnote; clip A also at 1.5 s per quarter.

**Pilot only. The full film is not rendered** (IQ-10, `prompts/CODE_SESSION_IQ-10.md`). Approved in principle (DEC-085, Luke's answers of 2 Oct 2026): console name + picture + maker colour on each bar; values in millions with "+" for lower bounds; a maker key with logos; retired consoles fade; a "best-selling console ever" crown; the estimated look (DEC-090) and the analyst-estimate label for Xbox One after 3 Dec 2014 and Xbox Series X|S (DEC-084); a title that says units shipped; quick 1985–88 (DEC-097); RTT-002's pacing approach (DEC-068); callouts at crown changes; a company scoreboard to compare with and without. Claude's working choices are DEC-103 onwards in `state/DECISIONS.md`.

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`), which IQ-10 extended with a quarter-end series mode. Every RTT-003 feature is switched on by a key in these configs and is off for RTT-002; 22 reference frames of three RTT-002 configs are pixel-identical to `main` and the RTT-002 test suite passes unchanged.

| File | What it is |
|---|---|
| `race_rtt003.json` | Player input ("rtt-series/1"), written by `scripts/rtt003_adapter.py` from `data/rtt-003/` (consoles, series, series_by_maker, crown). One event per quarter end; units copied as integers |
| `dataset_hashes.txt` | SHA-256 of the adapter's four inputs and its output (the render checks the output) |
| `config_rtt003_film.json` | The film's settings (not rendered here): 15 rows, counting, pictures, logos on the bars, maker colours, fade, crown, callouts and moments, scoreboard, final-table line and footnote, pacing |
| `config_rtt003_clip_A_1985_1992.json`, `..._1.5x.json` | Clip A at 1.0 s and 1.5 s per quarter (1985–88 at 0.5 s / 0.75 s): the two-console start, NES takes the crown (end-1988), Atari 2600 fades (end-1991) |
| `config_rtt003_clip_B_1996_1999.json` | Clip B: Game Boy takes the crown (end-1997) |
| `config_rtt003_clip_C_2005_2009.json` | Clip C with the scoreboard: PS2 takes the crown (mid-2007), DS passes Game Boy for second (end-2009) |
| `stills.json`, `render_stills.js`, `sheets.js` | The stills (round 2: final table, 31 Mar 2018 with Xbox One, two close-ups of picture + logo drawn at 2×), each also at phone size; `sheets.js` holds round 1's design sheets (maker colours, pictures at icon size) |
| `pictures.json` | Which row of the private reconciled picture list each bar and maker key uses (metadata only) |
| `assets_sha256.txt` | SHA-256 of every private icon and logo the render reads (checked before drawing) |

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
RTT_CONFIG=../rtt-003/config_rtt003_film.json FRAME_COUNT_ONLY=1 node rtt.js        # FRAMES 6309 = 3 min 30 s (1.5 s per quarter: 9193 = 5 min 6 s)
RTT_CONFIG=../rtt-003/config_rtt003_clip_A_1985_1992.json FRAME_COUNT_ONLY=1 node rtt.js   # 939 (1.5x 1304, B 744, C 996)
RTT_LOCAL_ASSETS=<folder with icons/, logos/, rtt_logo.png> RTT_CONFIG=../rtt-003/config_rtt003_clip_B_1996_1999.json SEG_OUT=b.mp4 node rtt.js
RTT_LOCAL_ASSETS=<same> node ../rtt-003/render_stills.js OUT_DIR                    # stills (write them outside the repo)
python scripts/rtt003_adapter.py data/rtt-003 kits/rtt-003/race_rtt003.json --hash-file kits/rtt-003/dataset_hashes.txt
node tests/player/run_tests_rtt003.js ; node tests/player/phone_check_rtt003.js
```

Render on GitHub: `.github/workflows/rtt003_pilot.yml` (its own workflow; `render_pilot.yml` is RTT-002's and is unchanged). It fetches the icons, logos and Luke's logo from the private repo with `RTT_PRIVATE_TOKEN`, checks every SHA-256, renders the four clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Config keys added in IQ-10 (player, series mode)

`board_top` (px; 150 when absent), `pictures` {enabled, dir, height_frac, aspect, gap}, `maker_order` + `palette` (one colour per maker), `maker_names`, `labels` (bar-name overrides, unused), `fade` {enabled, alpha, text_alpha, sec}, `crown` {enabled, colour}, `callout` {enabled, sec, y, size, fade_in, fade_out}, `maker_key` {enabled, x, bottom, w, row_h, size, pad, logos, logo_dir, logo_w, logo_h, legend, scoreboard}, `bar_notes` [{id, mark, text}], `axis_suffix`, `glide.bar_mode` "beat", `pacing.segments` [{to, sec_per_event}], `record_hold.types` ["CROWN"]. Round 2: `count` {enabled}, `bar_logos` {enabled, dir, height_frac, aspect, gap, pad}, `pictures.tall_frac`, `moments` [{type first_past|passes, id, units|other+rank, on_hold}], `final_line` {enabled, id, other, label, other_label}, `final_footnote` {enabled, id, mark, size, dy, text}.

## Not in this kit

No pictures, logos, stills or renders: they live only in the private repo (DEC-006, DEC-060). No music (IQ-10).
