# HANDOVER — 29 Sep 2026 (session 11, Claude Code cloud session, environment "Race Through Time")

Previous handovers are in this file's git history. Session 10's pull request #9 (private asset store, pilot render workflow) was merged to main as `c378ea7`.

## Done (branch `claude/festive-wright-ljiwlo`, from main @ `c378ea7`; pull request #10 against main, **not merged**: Luke merges once checks pass, DEC-057)
- **DEC-062 (owner):** Luke watched the round-5 pilot (`rtt-002-pilot5-5f797d3-run1`) and approved it ("I think it's great"). The RTT visual direction is approved (blueprint milestone 3). Names that run past short bars are accepted.
- **The full RTT-002 film (DEC-063):** `kits/rtt-002/config_rtt002_film.json` extends the approved pilot config unchanged. It covers all 1,164 races from the 1950 British GP (13 May 1950) to the **data freeze, the 2026 Azerbaijan GP (26 Sep 2026)**. **20,033 frames = 667.8 s (11 min 8 s)**, including a 10 s final table. No title card and no closing card.
- **Pacing:** smooth speed curve, 0.4–0.7 s per race (0.8–1.4 × 0.5 s), slowed around every story moment and top-ten entry. Story races are held 2.5–3 s.
- **Story moments:** 30 (`data/rtt-002/story_moments.csv`, `reports/RTT-002_story_moments.md`, `scripts/rtt002_story.py`), with captions above the car box: the first race, 8 leader changes, 8 records equalled, the first to 50 and to 100 wins, 10 top-ten entries (today's top ten) and the freeze.
- **Tests 17/17 PASS** (`tests/player/RESULTS.md`), including the new `rtt002_film` case (checks 29–32). Phone check PASS.
- **Audio:** none. Video only, as the pilot. The workflow now fails on any audio stream. No music has been chosen or licensed.
- **Render:** `.github/workflows/render_pilot.yml` (config selectable, default the film) ran on the push of `e4dbeda`: RENDER_RESULT
- `marketmarathon/bars` untouched. Nothing uploaded to YouTube or published. The audited data files are unchanged.

## Not done / open
- Luke watches the full film (the private release page needs him signed in to GitHub).
- Claude has not watched the rendered film. It was checked frame by frame through the draw calls, with OCR at the 30 story moments, and one 150-frame 4K test segment was encoded in the container to estimate file size (deleted).
- Questions for Luke: are the caption wording and choice of moments right (e.g. whether to caption all 40 top-ten entries or only today's top ten)? Should the 1950 "record equalled" caption (Fangio level with Farina on 2 wins) stay?
- Still open: the 3 nationality disagreements, the footer in YouTube's controls strip, D-05 (publication risk, incl. the car's trademarks), the DEC-059 note for the video description, music for RTT.

## Next safe actions
1. Luke reviews and merges pull request #10 once its checks pass.
2. Luke's feedback on the full film.
3. IQ-06 live feasibility for RTT-001, 003–012; IQ-07 uploader (private-only). New metric contracts follow DEC-036.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md`, `reference/metric_contract_RTT-002.md` and `reference/rights_ledger.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006: code, configs, data and written results only in this public repo; logos, pictures, test frames, stills and renders live only in the private repo (DEC-060). Never upload workflow artifacts from this repo and never print `RTT_PRIVATE_TOKEN` (DEC-061). New data goes in new files; the audited wins files stay unchanged; starts corrections go only through `starts_corrections.csv`. Pushing a change to `.github/workflows/render_pilot.yml` on the branch named in its `push` trigger starts a render.
