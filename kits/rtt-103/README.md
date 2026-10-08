# RTT kit — RTT-103 The AI Spending Race (Big Tech's capital spending, last 12 months, 2010–2026) · design round 1 (IQ-18)

**Round 1 only: option stills, side-by-side contact sheets (c01–c13) and three pace clips for Luke to choose from.** No full film, no music, nothing published (brief `prompts/CODE_SESSION_IQ-18.md`; DEC-069). Decisions DEC-342 onwards in `state/DECISIONS.md`. **The data is not changed:** `data/rtt-103/` as merged by Luke on 8 Oct 2026 (pull request #20, DEC-345).

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`) with RTT-001's approved additions brought in by merging pull request #18's branch (DEC-346), extended in IQ-18 with a **money** race kind (DEC-347). Every RTT-103 feature is switched on by a key in these configs or by the race file's `kind: "money"`, and is off for every other episode: 50 frames of RTT-001, RTT-002 and RTT-003 configs are pixel-identical before and after (`tests/player/compare_frames.js`).

| File | What it is |
|---|---|
| `race_rtt103.json` | Player input ("rtt-series/1", kind "money"), written by `scripts/rtt103_adapter.py` from `data/rtt-103/`: one event per quarter end (66), every company's 12-month capital spending in whole US dollars exactly as `AI_SPENDING_RACE_MASTER.csv`; `combined` per quarter (checked to the dollar against `L_aggregate_capex.csv`); Alibaba's gap; and, for the step stills, the 2026 plans and look-ahead rows, ByteDance's greyed row, the peak views with BCG's chart values to 2030 and the story-moment candidates of G |
| `dataset_hashes.txt` | SHA-256 of the adapter's inputs and output (the render and the tests check them) |
| `config_rtt103_base.json` | Option A of everything (recommended unless a question says otherwise): RTT-001's approved layout, all nine companies, "$169.0bn", "12 months to Jun" over the year top right, logo tiles (Baidu: our own tile), "· measured differently" after Tencent's value, the running total as a number, 1.5 s per quarter. Every other config extends it |
| `config_rtt103_values_B/C`, `date_B/C`, `title_B/C`, `names_only` | Item a and b options: "$169bn" / "US$169.0bn"; "Q2" / a small date line; two other titles; name only |
| `config_rtt103_entry_B`, `gap_hold`, `gap_leave` | Item c: "· joins the race" for 3 s; Alibaba held dimmed with no number / leaving and returning with one plain line |
| `config_rtt103_tencent_B` | Item d: a mark and a footnote instead of the in-line note |
| `config_rtt103_story_line/card/marker` | Item e: seven shortlisted story moments as one line under the title / a small card / a marker under the date (the eighth, Alphabet's share sale, does not fit before the race ends, DEC-350) |
| `config_rtt103_comb_line/bar` | Item f: the running total as a growing line / one bar split by company |
| `config_rtt103_clip_pace_2020_2026_1p0/1p5/2p0` | Item k: 2020–2026 (Amazon takes the lead in the 12 months to September 2020) at 1.0, 1.5 and 2.0 s per quarter; `clips.txt` lists them |
| `steps.js` | Items g–j and l: the steps after the race, drawn as option stills in the player page (2026 plans A/B, look-ahead A/B, peaks A/B, iCapital A/B/C, final table A/B) |
| `stills.json`, `render_stills.js` | 51 stills (each also at phone size) and 13 contact sheets c01–c13 (copied from RTT-001's still renderer; a step may be drawn over a board frame) |
| `logos.json`, `assets_sha256.txt` | The company logos (Commons title, page, licence, author, SHA-1, SHA-256, status; identification only) and the SHA-256 of every private file the render reads |

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
python scripts/rtt103_adapter.py data/rtt-103 kits/rtt-103/race_rtt103.json --hash-file kits/rtt-103/dataset_hashes.txt   # from the repo root
RTT_CONFIG=../rtt-103/config_rtt103_base.json FRAME_COUNT_ONLY=1 node rtt.js        # FRAMES 3861 = 2 min 9 s (race incl. 10 s hold)
RTT_LOCAL_ASSETS=<folder with rtt_logo.png and logos/> node ../rtt-103/render_stills.js OUT_DIR   # stills and sheets (outside the repo)
node tests/player/run_tests_rtt103.js ; node tests/player/phone_check_rtt103.js      # from the repo root
node tests/player/compare_frames.js <a checkout of the commit before a player change>
```

Logos: `.github/workflows/rtt103_assets.yml` with `scripts/rtt103_fetch_logos.py` (runner only; Commons refuses this container). Render: `.github/workflows/rtt103_pilot.yml` (its own workflow; a push that changes it on the IQ-18 branch), which fetches Luke's logo and the company logos from the private repo, checks every SHA-256, renders the clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Not in this kit

No logo files, stills or renders (DEC-006, DEC-060): they live only in the private repo. No music this round.
