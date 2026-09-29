# HANDOVER — 29 Sep 2026 (session 10, Claude Code cloud session, environment "Race Through Time")

Previous handovers (session 2, Cowork: repo bootstrap, RTT-002 dataset, DATA_AUDIT; session 3: IQ-04; sessions 4–8: IQ-05 rounds 1–5; session 9: independent check 3, DEC-058/DEC-059) are in this file's git history. Session 9's pull request #8 was merged to main as `19b1b03`.

## Done (branch `claude/cool-mccarthy-kf9mow`, from main @ `19b1b03`; pull request against main, **not merged**)
- **DEC-060 (owner, Luke in the claude.ai chat):** private asset store `marketmarathon/race-through-time-private`. `assets/rtt-002/rtt_logo.png` SHA-256 `e3db4611…0eeca` (885 × 885) and `rtt_car.png` SHA-256 `4be74e67…aa5bb` (3435 × 936): both read back here, both match. Actions secret `RTT_PRIVATE_TOKEN` (fine-grained, that repo only, Contents read and write) **expires 28 Sep 2027 — renew before then**. The Claude GitHub App also has access. `reference/rights_ledger.md` now says where each asset lives.
- **DEC-061 (Claude working choice):** `.github/workflows/render_pilot.yml` fetches both pictures with the secret into the runner's temporary folder, checks both hashes (stop on mismatch), checks the player input hash, renders `config_pilot_2014_2021_top20.json` at **3840 × 2160** plus a **1920 × 1080 viewing copy**, checks size and frame count with ffprobe, and saves both only as a **pre-release in the private repo**. No workflow artifact (on a public repo anyone signed in can download them), no cache, pictures and videos deleted from the runner at the end; the log shows the secret only as `***`.
- **Rendered.** It ran from the branch (a push that changes the workflow file triggers it; a by-hand run needs the file on main): run https://github.com/marketmarathon/race-through-time/actions/runs/36600844509, success in 6 min 15 s, 0 artifacts. Release: https://github.com/marketmarathon/race-through-time-private/releases/tag/rtt-002-pilot5-5f797d3-run1 — 2,502 frames = 83.4 s; master SHA-256 `a05d4ee3…49cd9`, viewing copy `23bfbdf3…9b732` (full hashes in `state/STATE.json` and the release notes). Claude has not watched the full video; a 120-frame 4K test with the real logo and car was checked in the container and deleted.
- `marketmarathon/bars` untouched. Nothing uploaded to YouTube or published.

## Not done / open
- Luke watches the pilot (the release page needs him signed in to GitHub; it is private).
- Seen on the test frame, pre-existing, not changed: on short bars the driver's name runs past the end of the bar (e.g. "Jenson Button", "Jack Brabham" at 14–15 wins). Luke to say if that matters.
- Still open: the 3 nationality disagreements, the footer in YouTube's controls strip, D-05 (publication risk, incl. the car's trademarks), the DEC-059 note for the video description.

## Next safe actions
1. Luke reviews and merges this pull request (then the workflow can also be run by hand: Actions → render-pilot → Run workflow).
2. Luke's feedback on the rendered pilot.
3. IQ-06 live feasibility for RTT-001, 003–012 (not started). IQ-07 not started. New metric contracts follow DEC-036.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md`, `reference/metric_contract_RTT-002.md` and `reference/rights_ledger.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006: code, configs, data and written results only in this public repo; logos, pictures, test frames, stills and renders live only in the private repo (DEC-060). Never upload workflow artifacts from this repo and never print `RTT_PRIVATE_TOKEN` (DEC-061). New data goes in new files; the audited wins files stay unchanged; starts corrections go only through `starts_corrections.csv`.
