# RTT kit — RTT-003 (Best-Selling Consoles 1985–2026, units shipped) · design pilot IQ-10

**Pilot only. The full film is not rendered** (IQ-10, `prompts/CODE_SESSION_IQ-10.md`). Approved in principle (DEC-085, Luke's answers of 2 Oct 2026): console name + picture + maker colour on each bar; values in millions with "+" for lower bounds; a maker key with logos; retired consoles fade; a "best-selling console ever" crown; the estimated look (DEC-090) and the analyst-estimate label for Xbox One after 3 Dec 2014 and Xbox Series X|S (DEC-084); a title that says units shipped; quick 1985–88 (DEC-097); RTT-002's pacing approach (DEC-068); callouts at crown changes; a company scoreboard to compare with and without. Claude's working choices are DEC-103 onwards in `state/DECISIONS.md`.

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`), which IQ-10 extended with a quarter-end series mode. Every RTT-003 feature is switched on by a key in these configs and is off for RTT-002; 22 reference frames of three RTT-002 configs are pixel-identical to `main` and the RTT-002 test suite passes unchanged.

| File | What it is |
|---|---|
| `race_rtt003.json` | Player input ("rtt-series/1"), written by `scripts/rtt003_adapter.py` from `data/rtt-003/` (consoles, series, series_by_maker, crown). One event per quarter end; units copied as integers |
| `dataset_hashes.txt` | SHA-256 of the adapter's four inputs and its output (the render checks the output) |
| `config_rtt003_film.json` | The film's settings (not rendered here): 12 rows, pictures, maker colours, fade, crown, callouts, maker key, pacing |
| `config_rtt003_clip_A_1985_1992.json` | Clip A: the two-console start, 1985–88 at 0.5 s per quarter, NES takes the crown (31 Dec 1988), Atari 2600 fades (31 Dec 1991) |
| `config_rtt003_clip_B_1996_1999.json` | Clip B: Game Boy takes the crown (31 Dec 1997) |
| `config_rtt003_clip_C_2005_2009.json`, `..._scoreboard.json` | Clip C without and with the company scoreboard: PS2 takes the crown (30 Jun 2007) |
| `config_rtt003_still_2015_top20.json` | Still only: 20 rows at 31 Dec 2015 so Xbox One's analyst-estimate look is on screen |
| `config_rtt003_still_ps2_note.json` | Still only: the PS2 155m / 160m note candidate (DEC-094) |
| `stills.json`, `render_stills.js`, `sheets.js` | The stills (board stills and two design sheets: maker colours, pictures at icon size), each at 1920 × 1080 and at phone size |
| `pictures.json` | Which row of the private reconciled picture list each bar and maker key uses (metadata only) |
| `assets_sha256.txt` | SHA-256 of every private icon and logo the render reads (checked before drawing) |

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
RTT_CONFIG=../rtt-003/config_rtt003_film.json FRAME_COUNT_ONLY=1 node rtt.js        # FRAMES 6042 = 3 min 21 s
RTT_CONFIG=../rtt-003/config_rtt003_clip_A_1985_1992.json FRAME_COUNT_ONLY=1 node rtt.js   # 918 (B 702, C 930)
RTT_LOCAL_ASSETS=<folder with icons/, logos/, rtt_logo.png> RTT_CONFIG=../rtt-003/config_rtt003_clip_B_1996_1999.json SEG_OUT=b.mp4 node rtt.js
RTT_LOCAL_ASSETS=<same> node ../rtt-003/render_stills.js OUT_DIR                    # stills (write them outside the repo)
python scripts/rtt003_adapter.py data/rtt-003 kits/rtt-003/race_rtt003.json --hash-file kits/rtt-003/dataset_hashes.txt
node tests/player/run_tests_rtt003.js ; node tests/player/phone_check_rtt003.js
```

Render on GitHub: `.github/workflows/rtt003_pilot.yml` (its own workflow; `render_pilot.yml` is RTT-002's and is unchanged). It fetches the icons, logos and Luke's logo from the private repo with `RTT_PRIVATE_TOKEN`, checks every SHA-256, renders the four clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Config keys added in IQ-10 (player, series mode)

`board_top` (px; 150 when absent), `pictures` {enabled, dir, height_frac, aspect, gap}, `maker_order` + `palette` (one colour per maker), `maker_names`, `labels` (bar-name overrides, unused), `fade` {enabled, alpha, text_alpha, sec}, `crown` {enabled, colour}, `callout` {enabled, sec, y, size, fade_in, fade_out}, `maker_key` {enabled, x, bottom, w, row_h, size, pad, logos, logo_dir, logo_w, logo_h, legend, scoreboard}, `bar_notes` [{id, mark, text}], `axis_suffix`, `glide.bar_mode` "beat", `pacing.segments` [{to, sec_per_event}], `record_hold.types` ["CROWN"].

## Not in this kit

No pictures, logos, stills or renders: they live only in the private repo (DEC-006, DEC-060). No music (IQ-10).
