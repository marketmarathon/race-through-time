# Claude Code session prompt — IQ-04 RTT player (28 Sep 2026)
Start a Claude Code **cloud** session with repository `marketmarathon/race-through-time` and environment **Race Through Time**, then paste everything between the lines.

---
You are working on Race Through Time (RTT), a YouTube data-storytelling channel. Task: IQ-04, the RTT player. Work in small, reviewable steps. The owner, Luke, is not technical: finish with a short plain-English summary for him.

Read first: state/STATE.json, state/HANDOVER.md, state/DECISIONS.md (especially DEC-002, DEC-006, DEC-010, DEC-012), reference/environment_audit.md, reference/reconciliation.md, reference/metric_contract_RTT-002.md, data/rtt-002/README.md.

Hard rules
- marketmarathon/bars is Market Marathon's repo. Read it only: never commit, push, open issues or pull requests there. Its Format C2-2 files are the protected baseline.
- This repo is public (DEC-006). Commit code and configs only. Do not copy fonts, logos, images, music or market data from bars unless you confirm a licence that allows public redistribution; if unsure, leave it out and list it for Luke.
- No secrets, no workflows that upload or publish, no renders uploaded anywhere.
- Never invent data. Missing information is NOT FOUND.

Steps
1. Read-only copy from bars @ 2a10877 (or current HEAD; record the commit). A partial/shallow clone is fine (the repo is about 650 MB). The C2-2 player lives inside the kit zips; baseline kit: MarketMarathon_RaceKit_RF_US_C2_v3.zip (formatc.js drives player_formatc2.html in Playwright Chromium). Workflow reference: .github/workflows/render-rf-us-c2-v1-split.yml.
2. Create an RTT kit in this repo (e.g. kits/rtt-002/) with player_rtt.html and an RTT driver copied from C2-2. Keep the existing environment contract (FRAME_COUNT_ONLY, SEG_START/SEG_END/SEG_OUT, RASTER_W, NOMUX, REF_PNG_DIR).
3. Change only the copy, for RTT:
   a. Whole-number labels with a unit ("wins"): no bn/tn, no decimals.
   b. Step at event: a driver's number changes only at the race where the win happened, never showing in-between values. Bars may glide smoothly to new lengths and positions between events.
   c. No country flags, sub-sector icons or merger lineage rows.
   d. Time label shows season, Grand Prix and date instead of a year or quarter. Pacing configurable, adaptive within 0.8–1.4x (blueprint); quiet stretches compress.
   e. Ties: equal wins -> whoever reached that total first ranks higher (credit order in data/rtt-002/win_credits.csv).
   f. Everything RTT-specific in a config file, not hard-coded. Keep the C2-2 look as the default so a quieter variant can be tried later.
4. Adapter script: data/rtt-002 (win_credits.csv, races.csv, drivers.csv) -> the player's input format. Deterministic; record the SHA-256 of its output.
5. Stress fixtures under tests/fixtures/: very long names; a three-way tie; two winners at one event (shared drive); a driver entering and leaving the visible top N; a long quiet stretch; an opening with fewer than N entrants.
6. Tests: for each fixture and for a short RTT-002 slice (1984–1989), render headless at 1920 preview width, grab frames at event boundaries and assert every label is a whole number equal to the data at that event. If Chromium/Playwright cannot be installed in this environment, report NOT AVAILABLE; do not work around it.
7. Phone check: two 1920 stills plus a phone-scale crop; note whether the smallest label is readable.
8. Update state/STATE.json (IQ-04 status), state/HANDOVER.md (what you did, what is open) and add any Claude working choices to state/DECISIONS.md.
9. Push a branch and open a pull request. Do not merge. The PR description must list: what changed from C2-2 and why, test results, the bars commit copied from, anything left out for licence reasons, and questions for Luke.

Stop after opening the pull request. Do not start the design pilot (IQ-05).
---
