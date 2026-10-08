# RTT kit — RTT-103 The AI Spending Race (Big Tech's capital spending, last 12 months, 2010–2026, then 2026 plans and 2027–2030 estimates) · design round 3 (IQ-18c)

**Round 3 (IQ-18c): Luke's direction (DEC-371) - after June 2026 the race carries straight on, on the same board, through the 2026 plans and the 2027–2030 estimates; the explanation follows 2030; then the end as built in round 2.** Round 2 (IQ-18b, DEC-353..DEC-370) built Luke's answers into one version. No film yet: the music is chosen (DEC-372) and the film waits for Luke's OK of this look; nothing published (briefs `prompts/CODE_SESSION_IQ-18.md`, `IQ-18b.md`, `IQ-18c.md`, `IQ-18d.md`). Decisions DEC-342 onwards in `state/DECISIONS.md`. **The data is not changed:** `data/rtt-103/` as merged by Luke on 8 Oct 2026 (pull request #20, DEC-345); the forward boards are built at draw time from the look-ahead file already in the race file.

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`) with RTT-001's approved additions brought in by merging pull request #18's branch (DEC-346), extended in IQ-18 with a **money** race kind (DEC-347). Every RTT-103 feature is switched on by a key in these configs or by the race file's `kind: "money"`, and is off for every other episode: 50 frames of RTT-001, RTT-002 and RTT-003 configs are pixel-identical before and after (`tests/player/compare_frames.js`).

| File | What it is |
|---|---|
| `race_rtt103.json` | Player input ("rtt-series/1", kind "money"), written by `scripts/rtt103_adapter.py` from `data/rtt-103/`: one event per quarter end (66), every company's 12-month capital spending in whole US dollars exactly as `AI_SPENDING_RACE_MASTER.csv`; `combined` per quarter (checked to the dollar against `L_aggregate_capex.csv`); Alibaba's gap; the 2026 plans and look-ahead rows, ByteDance's greyed row, the peak views with BCG's chart values to 2030 and the story-moment candidates of G |
| `dataset_hashes.txt` | SHA-256 of the adapter's inputs and output (the render and the tests check them) |
| `config_rtt103_base.json` | The race's look as Luke chose it (DEC-353): all nine companies, "$169.0bn", "12 months to Jun" over the year top right, a logo tile per bar (Baidu's own logo, DEC-354), Tencent "· includes some intangibles" (DEC-356), 1.5 s per quarter (DEC-362) |
| `config_rtt103_film.json` | **The design, round 3 (IQ-18c)**: the base plus Alibaba leaving and returning with a plain line each time (DEC-355), five story cards in the race (DEC-357, DEC-358), the running total as a number with a growing line (DEC-359); then **`forward`** (DEC-371, DEC-373): one race board per year after June 2026 - 2026 company plans (10.8 s, with Alphabet's share-sale card and iCapital's card as story cards), 2027 (3.5 s), 2028 (3 s), 2029 (3 s), 2030 (4 s), each counted in over 1.5 s - built by `rtt_timeline.js` from the race file's look-ahead rows (ranges, notes, the estimated and analyst looks, ByteDance greyed on the 2026 board, `board.fit.max_slots` 10); then `steps`: the explanation (14 s), the combined line (6 s), the peak timeline (8 s) and the final June 2026 table with its one-line summary (10 s). 5,475 frames = 3 min 2.5 s without music; not rendered as a film yet |
| `config_rtt103_clip_2025_end.json` | Round-3 motion clip: 2025 through 2030 into the end (2,235 frames = 74.5 s); `clips.txt` lists it |
| `stills.json`, `render_stills.js` | Round 3: 7 stills (each also at phone size: June 2026, the 2026 board with each card, 2027, 2030, the explanation, the final table) and contact sheet d01; a still dated with a quarter is taken on the frame where that quarter's figures land (Cowork fix (h)); a step still names its step and the second within it |
| `logos.json`, `assets_sha256.txt` | The company logos (wiki title, page, licence, author, SHA-1, SHA-256, status; identification only) and the SHA-256 of every private file the render reads |
| `description_credits.md` | Footer lines as drawn and the draft video description (Cowork fixes (a), (i)) |

Round 1 (IQ-18) showed each question's options from configs and a `steps.js` that are no longer in the kit (git history and the private pre-release `rtt-103-round1-0500062-run2` keep them); the player still supports those options behind their keys. Round 2's separate 2026 plans step and look-ahead boards were removed from `rtt_steps.js` in round 3 (DEC-371; pre-release `rtt-103-round2-aea95a9-run3` keeps them).

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
python scripts/rtt103_adapter.py data/rtt-103 kits/rtt-103/race_rtt103.json --hash-file kits/rtt-103/dataset_hashes.txt   # from the repo root
RTT_CONFIG=../rtt-103/config_rtt103_film.json FRAME_COUNT_ONLY=1 node rtt.js        # FRAMES 5475 = 3 min 2.5 s (race, forward boards and the steps after them)
RTT_LOCAL_ASSETS=<folder with rtt_logo.png and logos/> node ../rtt-103/render_stills.js OUT_DIR   # stills and sheets (outside the repo)
node tests/player/run_tests_rtt103.js ; node tests/player/phone_check_rtt103.js      # from the repo root
node tests/player/compare_frames.js <a checkout of the commit before a player change>
```

Logos: `.github/workflows/rtt103_assets.yml` with `scripts/rtt103_fetch_logos.py` (runner only; Commons refuses this container). Render: `.github/workflows/rtt103_pilot.yml` (its own workflow; a push that changes it on the IQ-18 branch), which fetches Luke's logo and the company logos from the private repo, checks every SHA-256, renders the clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Not in this kit

No logo files, stills or renders (DEC-006, DEC-060): they live only in the private repo. No music file (private repo only, DEC-372).
