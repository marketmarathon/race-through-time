# RTT kit — RTT-102 AI assistant websites race (Similarweb's published estimates of monthly website visits, Dec 2022 – Aug 2026) · design round 1 (IQ-19)

**IQ-19 (9 Oct 2026): the first design round - options side by side for Luke, no full film, no music** (brief `prompts/CODE_SESSION_IQ-19.md`; decisions DEC-531 onwards in `state/DECISIONS.md`). **The data is not changed:** `data/rtt-102/` as built in IQ-17 (pull request #21). The race ends in August 2026 (DEC-530, DEC-531): ChatGPT's verified September 2026 figure is not shown because the other bars stop at August.

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`) with RTT-001's approved additions (big date top right, board sized to its bars, logo tiles, frame-anchored stripes) and RTT-103's story card, brought in by merging pull request #22's branch (which contains #18). IQ-19 adds a **visits** race kind (DEC-534): every RTT-102 feature is switched on by the race file's `kind: "visits"` or by a config key, and is off for every other episode: frames of RTT-001, RTT-002, RTT-003 and RTT-103 configs are pixel-identical before and after (`tests/player/compare_frames.js`).

| File | What it is |
|---|---|
| `race_rtt102.json` | Player input ("rtt-series/1", kind "visits"), written by `scripts/rtt102_adapter.py` from `data/rtt-102/series_monthly.csv` and `identities.csv` (their SHA-256 checked against `data/rtt-102/manifest.json` first): one event per month end, December 2022 to August 2026 (45), whole visits exactly as the series; each bar's name at that date; Similarweb's older estimates flagged; each bar's published months (`knots`, for the eased option); after a bar's last published month (Copilot from October 2025, Meta AI from January 2026) the bar is held at that figure, marked "latest_figure" |
| `dataset_hashes.txt` | SHA-256 of the adapter's inputs and output (the render and the tests check them) |
| `config_rtt102_base.json` | The base look (Claude's recommendation for each item): house defaults (sections 1-6), title A, estimates said once in the source line with solid bars and "~" values, Similarweb's older estimates striped with the dated note at August 2024, values "~5.6bn" / "~950m" / "~84.1m", held bars ranked below the live ones and dimmed "· latest figure, Sep 2025", one colour per assistant, a logo tile per bar (Bard's logo while the bar is "Bard"), monthly clock at 1.0 s per month, straight lines (as decided, DEC-501 (4)) |
| `config_rtt102_story.json`, `config_rtt102_story_bard.json` | Item i: the four recommended story cards, and the same with Bard's renaming as a fifth |
| `config_rtt102_clip_e_2024_*.json` | Item e: January–December 2024 with straight lines and eased (a monotone cubic through the same published figures) |
| `config_rtt102_clip_f_*.json` | Item f: October 2024 – June 2025 with a monthly clock (0.75 / 1.0 / 1.5 s per month) and a quarterly clock (2.25 / 3.0 / 4.5 s per quarter) |
| `stills.json`, `render_stills.js` | 30 option stills (each also at phone size) and one contact sheet per item (a–j); a still dated with a month is taken on the frame where that month's figures land; card stills on the card's own time (`card: true`) |
| `clips.txt` | The eight clips the render workflow makes |
| `logos.json`, `assets_sha256.txt` | The assistant logos (wiki title, page, licence, author, SHA-1, SHA-256; identification only; fetched by `.github/workflows/rtt102_assets.yml` with `scripts/rtt102_fetch_logos.py`) and the SHA-256 of every private file the render reads |
| `description_credits.md` | Footer as drawn and the draft description lines |

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
python3 scripts/rtt102_adapter.py data/rtt-102 kits/rtt-102/race_rtt102.json --hash-file kits/rtt-102/dataset_hashes.txt   # from the repo root
RTT_CONFIG=../rtt-102/config_rtt102_base.json FRAME_COUNT_ONLY=1 node rtt.js        # FRAMES 1752 = 58.4 s (the whole race at 1.0 s per month, 10 s final table)
RTT_LOCAL_ASSETS=<folder with rtt_logo.png and logos/> node kits/rtt-102/render_stills.js OUT_DIR   # stills and sheets (outside the repo)
node tests/player/run_tests_rtt102.js ; node tests/player/phone_check_rtt102.js      # from the repo root
node tests/player/compare_frames.js <a checkout of the commit before a player change>
```

Render: `.github/workflows/rtt102_pilot.yml` (its own workflow; a push that changes it on the IQ-19 branch): fetches Luke's logo and the assistant logos from the private repo, checks every SHA-256, runs the WCAG flash check on the clips with striped bars, renders the clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Not in this kit

No logo files, stills or renders (DEC-006, DEC-060): they live only in the private repo. No music (round 1).
