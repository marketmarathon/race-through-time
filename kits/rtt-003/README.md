# RTT kit — RTT-003 (Best-Selling Consoles 1985–2026, units shipped) · design pilot IQ-10, round 4

**Round 4 (Luke, 2 Oct 2026, DEC-130 to DEC-137):** the board is the all-time top 15 again (`live_only` off, `status` on): a bar that is not live stays in place, lightly dimmed, with "· retired" (from a documented end date) or "· latest figure" (stopped without one) after its value, from the data (`series.csv` `status`); the gold record line stays (`record_line`), drawn after the bars with gaps where labels cross it, its label at its foot on the right; crown on the leader's bar; callouts as round 2. Data update DEC-134 (Xbox Series X|S on VGChartz to Jun 2026, Xbox 360 to 85.73m, Atari 2600 to 27.64m, Master System restated, Sega end dates). Full film 5 min 8 s. Stills: 30 Jun 2005 and the final table.

**Round 3 (Luke, 2 Oct 2026, DEC-122 to DEC-129, superseded in part by round 4):** 1.5 s per quarter (1985–88 at 0.75 s); only consoles still adding shipments race (`live_only`): a console carries "· retires" during its retirement quarter (first quarter end on or after its `fade_date`) and then leaves; a gold record line at the all-time record (crown on the holder's bar while it races, on the line's label once it retires); the film ends with a 1.6 s transition into the all-time top 15 (retired consoles included) with the Switch line and the PS2 footnote; scoreboard unchanged. Board: 2–8 bars (median 6). Full film 4 min 42 s.

**Round 2 (Luke, 2 Oct 2026, DEC-114 to DEC-121):** 15 rows; the numbers count smoothly and land on the exact data at every quarter end; the maker's logo beside each picture; no separate maker key (the bottom-right panel is the company scoreboard, kept); taller sizing for portrait pictures; callouts at the crown changes plus Game Boy first past 100 million and DS passes Game Boy (Switch passes DS on hold); a final-table line and the PS2 footnote; clip A also at 1.5 s per quarter.

**Pilot only. The full film is not rendered** (IQ-10, `prompts/CODE_SESSION_IQ-10.md`). Approved in principle (DEC-085, Luke's answers of 2 Oct 2026): console name + picture + maker colour on each bar; values in millions with "+" for lower bounds; a maker key with logos; retired consoles fade; a "best-selling console ever" crown; the estimated look (DEC-090) and the analyst-estimate label for Xbox One after 3 Dec 2014 and Xbox Series X|S (DEC-084); a title that says units shipped; quick 1985–88 (DEC-097); RTT-002's pacing approach (DEC-068); callouts at crown changes; a company scoreboard to compare with and without. Claude's working choices are DEC-103 onwards in `state/DECISIONS.md`.

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`), which IQ-10 extended with a quarter-end series mode. Every RTT-003 feature is switched on by a key in these configs and is off for RTT-002; 22 reference frames of three RTT-002 configs are pixel-identical to `main` and the RTT-002 test suite passes unchanged.

| File | What it is |
|---|---|
| `race_rtt003.json` | Player input ("rtt-series/1"), written by `scripts/rtt003_adapter.py` from `data/rtt-003/` (consoles, series, series_by_maker, crown). One event per quarter end; units copied as integers |
| `dataset_hashes.txt` | SHA-256 of the adapter's four inputs and its output (the render checks the output) |
| `config_rtt003_film.json` | The film's settings (not rendered here): 15 rows, counting, pictures, logos on the bars, maker colours, fade, crown, callouts and moments, scoreboard, final-table line and footnote, pacing |
| `config_rtt003_clip_A_1985_1992.json` | Clip A at 1.5 s per quarter (1985–88 at 0.75 s): the two-console start, NES takes the crown (end-1988), the Atari 2600 labelled retired (end-1991) |
| `config_rtt003_clip_B_1996_1999.json` | Clip B: Master System and Game Gear retired (Jun 1996), Mega Drive latest figure (Mar 1996), Game Boy takes the crown (end-1997), Saturn latest figure (Mar 1998) |
| `config_rtt003_clip_C_2005_2009.json` | Clip C with the scoreboard: PS2 takes the crown from Game Boy (mid-2007), DS passes Game Boy for second (end-2009) |
| `config_rtt003_clip_D_2025_2026_final.json` | Clip D: the last quarters and the transition into the all-time top-15 final table |
| `config_rtt003_still_names_as_text.json` | Round 3 still only (not rendered in round 4): the maker's name in type after the console name instead of the logo tile (DEC-126) |
| `stills.json`, `render_stills.js`, `sheets.js` | The stills (round 4: 30 Jun 2005 and the final table), each also at phone size; close-ups (`crop`) supported; `sheets.js` holds round 1's design sheets (maker colours, pictures at icon size) |
| `pictures.json` | Which row of the private reconciled picture list each bar and maker key uses (metadata only) |
| `assets_sha256.txt` | SHA-256 of every private icon and logo the render reads (checked before drawing) |

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
RTT_CONFIG=../rtt-003/config_rtt003_film.json FRAME_COUNT_ONLY=1 node rtt.js        # FRAMES 9247 = 5 min 8 s
RTT_CONFIG=../rtt-003/config_rtt003_clip_A_1985_1992.json FRAME_COUNT_ONLY=1 node rtt.js   # 1286 (B 1011, C 1389, D 639)
RTT_LOCAL_ASSETS=<folder with icons/, logos/, rtt_logo.png> RTT_CONFIG=../rtt-003/config_rtt003_clip_B_1996_1999.json SEG_OUT=b.mp4 node rtt.js
RTT_LOCAL_ASSETS=<same> node ../rtt-003/render_stills.js OUT_DIR                    # stills (write them outside the repo)
python scripts/rtt003_adapter.py data/rtt-003 kits/rtt-003/race_rtt003.json --hash-file kits/rtt-003/dataset_hashes.txt
node tests/player/run_tests_rtt003.js ; node tests/player/phone_check_rtt003.js
```

Render on GitHub: `.github/workflows/rtt003_pilot.yml` (its own workflow; `render_pilot.yml` is RTT-002's and is unchanged). It fetches the icons, logos and Luke's logo from the private repo with `RTT_PRIVATE_TOKEN`, checks every SHA-256, renders the four clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Config keys added in IQ-10 (player, series mode)

`board_top` (px; 150 when absent), `pictures` {enabled, dir, height_frac, aspect, gap}, `maker_order` + `palette` (one colour per maker), `maker_names`, `labels` (bar-name overrides, unused), `fade` {enabled, alpha, text_alpha, sec}, `crown` {enabled, colour}, `callout` {enabled, sec, y, size, fade_in, fade_out}, `maker_key` {enabled, x, bottom, w, row_h, size, pad, logos, logo_dir, logo_w, logo_h, legend, scoreboard}, `bar_notes` [{id, mark, text}], `axis_suffix`, `glide.bar_mode` "beat", `pacing.segments` [{to, sec_per_event}], `record_hold.types` ["CROWN"]. Round 2: `count` {enabled}, `bar_logos` {enabled, dir, height_frac, aspect, gap, pad}, `pictures.tall_frac`, `moments` [{type first_past|passes, id, units|other+rank, on_hold}], `final_line` {enabled, id, other, label, other_label}, `final_footnote` {enabled, id, mark, size, dy, text}. Round 3: `live_only` {enabled, exit_fade_sec, final_transition_sec, final_hold_sec}, `record_label_size`, `maker_in_name` {enabled, sep}. Round 4: `status` {enabled, retired, latest_figure, sec} (needs `fade` for the dim; not with `live_only`), `record_line` {enabled}.

## Not in this kit

No pictures, logos, stills or renders: they live only in the private repo (DEC-006, DEC-060). No music (IQ-10).
