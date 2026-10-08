# RTT kit — RTT-103 The AI Spending Race (Big Tech's capital spending, last 12 months, 2010–2026) · design round 2 (IQ-18b)

**Round 2: Luke's answers built into one version (DEC-353..DEC-365), reviewed as stills and one clip.** No film and no music yet (Luke picks the track next), nothing published (briefs `prompts/CODE_SESSION_IQ-18.md`, `prompts/CODE_SESSION_IQ-18b.md`). Decisions DEC-342 onwards in `state/DECISIONS.md`. **The data is not changed:** `data/rtt-103/` as merged by Luke on 8 Oct 2026 (pull request #20, DEC-345).

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`) with RTT-001's approved additions brought in by merging pull request #18's branch (DEC-346), extended in IQ-18 with a **money** race kind (DEC-347). Every RTT-103 feature is switched on by a key in these configs or by the race file's `kind: "money"`, and is off for every other episode: 50 frames of RTT-001, RTT-002 and RTT-003 configs are pixel-identical before and after (`tests/player/compare_frames.js`).

| File | What it is |
|---|---|
| `race_rtt103.json` | Player input ("rtt-series/1", kind "money"), written by `scripts/rtt103_adapter.py` from `data/rtt-103/`: one event per quarter end (66), every company's 12-month capital spending in whole US dollars exactly as `AI_SPENDING_RACE_MASTER.csv`; `combined` per quarter (checked to the dollar against `L_aggregate_capex.csv`); Alibaba's gap; the 2026 plans and look-ahead rows, ByteDance's greyed row, the peak views with BCG's chart values to 2030 and the story-moment candidates of G |
| `dataset_hashes.txt` | SHA-256 of the adapter's inputs and output (the render and the tests check them) |
| `config_rtt103_base.json` | The race's look as Luke chose it (DEC-353): all nine companies, "$169.0bn", "12 months to Jun" over the year top right, a logo tile per bar (Baidu's own logo, DEC-354), Tencent "· includes some intangibles" (DEC-356), 1.5 s per quarter (DEC-362) |
| `config_rtt103_film.json` | **The design, round 2 (IQ-18b)**: the base plus Alibaba leaving and returning with a plain line each time (DEC-355), five story cards in the race (DEC-357, DEC-358), the running total as a number with a growing line (DEC-359), and the steps after the race inside the player (`steps`, drawn by `kits/rtt-002/rtt_steps.js`): the 2026 plans step with Alphabet's share-sale card then iCapital's card (DEC-358, DEC-361), the look-ahead boards 2027–2030 then the combined line (DEC-360), the peak timeline, and the final table with its one-line summary held 10 s (DEC-363). 5,106 frames = 2 min 50 s without music; not rendered as a film yet |
| `config_rtt103_clip_2025_end.json` | Round-2 motion clip: 2025 into the end; `clips.txt` lists it |
| `stills.json`, `render_stills.js` | Round 2: 12 stills (each also at phone size) and contact sheets d01 (race) and d02 (steps); a still dated with a quarter is taken on the frame where that quarter's figures land (Cowork fix (h)); a step still names its step and the second within it |
| `logos.json`, `assets_sha256.txt` | The company logos (wiki title, page, licence, author, SHA-1, SHA-256, status; identification only) and the SHA-256 of every private file the render reads |
| `description_credits.md` | Footer lines as drawn and the draft video description (Cowork fixes (a), (i)) |

Round 1 (IQ-18) showed each question's options from configs and a `steps.js` that are no longer in the kit (git history and the private pre-release `rtt-103-round1-0500062-run2` keep them); the player still supports those options behind their keys.

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
python scripts/rtt103_adapter.py data/rtt-103 kits/rtt-103/race_rtt103.json --hash-file kits/rtt-103/dataset_hashes.txt   # from the repo root
RTT_CONFIG=../rtt-103/config_rtt103_film.json FRAME_COUNT_ONLY=1 node rtt.js        # FRAMES 5106 = 2 min 50 s (race and the steps after it)
RTT_LOCAL_ASSETS=<folder with rtt_logo.png and logos/> node ../rtt-103/render_stills.js OUT_DIR   # stills and sheets (outside the repo)
node tests/player/run_tests_rtt103.js ; node tests/player/phone_check_rtt103.js      # from the repo root
node tests/player/compare_frames.js <a checkout of the commit before a player change>
```

Logos: `.github/workflows/rtt103_assets.yml` with `scripts/rtt103_fetch_logos.py` (runner only; Commons refuses this container). Render: `.github/workflows/rtt103_pilot.yml` (its own workflow; a push that changes it on the IQ-18 branch), which fetches Luke's logo and the company logos from the private repo, checks every SHA-256, renders the clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Not in this kit

No logo files, stills or renders (DEC-006, DEC-060): they live only in the private repo. No music this round.
