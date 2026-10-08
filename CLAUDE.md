# Race Through Time: rules for every Claude Code session

This repo builds the Race Through Time YouTube channel (@racethroughtime). The owner is Luke, who is not technical. **Finish every session with a short plain-English summary for him:** what was done (with links), what needs his decision, and the next step.

These are the standing rules. The detail and history are in `state/DECISIONS.md`; the DEC numbers below point there.

## Read first
1. **Open pull requests and non-main branches.** `main` often lags behind; work can sit on an unmerged branch (lesson of 30 Sep 2026).
2. `state/HANDOVER.md`, then `state/STATE.json`.
3. `state/DECISIONS.md` is very long. Do not read it all: look up the DEC numbers your brief and the handover cite, and search it for your episode.
4. For the episode you are working on: `reference/metric_contract_RTT-###.md`, `kits/rtt-###/README.md`, and `data/rtt-###/README.md` if there is one.
5. For any design or render work: `reference/house_style.md`. For any picture, logo, music or dataset: `reference/rights_ledger.md`.
6. Save your brief, word for word, as `prompts/CODE_SESSION_<task>.md`.

## Hard rules
- **Never touch `marketmarathon/bars`** or any Market Marathon (C2-2) file.
- **This repo is public (DEC-006).** It holds code, configs, data and written results only. Pictures, logos, music, test frames, stills and renders live only in the private repo `marketmarathon/race-through-time-private` (DEC-060, DEC-073). Private research inputs (for example ChatGPT check files) are never committed: only their SHA-256 and validation results.
- **Never print `RTT_PRIVATE_TOKEN`.** Workflows in this repo upload no artifacts and use no cache (DEC-061).
- **Nothing goes to YouTube and nothing is published.** Renders go to a private pre-release in the private repo, with a SHA-256 for every file. Luke approves the exact file by its SHA-256 (DEC-078); any change after that needs a fresh approval.
- **No new visual feature or change to the approved look is built or rendered without Luke's approval first (DEC-069).** Proposals are listed as questions for him.
- **Do not merge pull requests (DEC-057).** Push a branch, open a pull request, stop.
- **Do not change an episode's data unless your brief approves it.** If you find a data problem, stop and list it. Approved changes go through the episode's source files and build script; then re-run every check and report any change to the leader/crown sequence and the top-ten overtakes.
- Do not change credentials, repo settings or permissions.

## Evidence rules
- Every figure has a status: **VERIFIED** (confirmed at its source), **UNVERIFIED** (found but not yet seen at its source) or **NOT FOUND**. Record the source URL and a short verbatim quote. Only VERIFIED figures are used.
- **Never average or guess between disagreeing sources.** Record each version as a disagreement and list it for Luke.
- **Never use a forecast. Never present an analyst estimate as official.** Estimates look like estimates on screen and are labelled.
- A series that stops because our figures run out is a **"latest figure"**, never "retired". "Retired" needs a documented end date (DEC-132).
- No non-commercial data (for example Jolpica/Ergast, DEC-003). Never scrape formula1.com.
- Before a data build, the metric contract lists every attribute the video will display and its source (DEC-036).
- If a source site is blocked from this container, do not guess. Check it from a GitHub runner the way `.github/workflows/rtt003_sources.yml` does (no secrets, no artifacts), or mark it UNVERIFIED and list it for Luke.

## Building and rendering
- **Reuse and extend the existing player** (`kits/rtt-002/` is the base; RTT-003 extended it rather than copying it, DEC-105). Do not rebuild it.
- **Each episode renders through its own workflow.** Never start another episode's render. A push that changes `.github/workflows/render_pilot.yml` renders RTT-002 clips, so leave that file alone when working on any other episode.
- Run the episode's test suite before any render (`node tests/player/run_tests.js` for RTT-002, `node tests/player/run_tests_rtt003.js` for RTT-003, `node tests/player/run_tests_rtt001.js` for RTT-001). If you change shared player code, show that RTT-002's approved output is unchanged.
- **Previews:** use stills to check layout, text, styling and readability. Use clips only to check motion, overtakes, pacing, timing or audio. Check every still at phone size too (`tests/player/phone_check*.js`).
- When a design question is open, show the options side by side in the same round rather than building one into the film.

## Recording the work
- Record decisions from the next free DEC number, checking `main` **and** every open pull request. Label each one as Owner, Claude working choice, Claude proposal or Claude finding.
- **Detailed data and method questions are Claude's to decide (DEC-417):** which source or figure, deal structures, same-grade conflicts, dates, what goes to the next research round. Apply the recommendation within the agreed rules, record it as a Claude decision citing DEC-417, and list it in the summary under "Decided for you". Ask Luke only about what the video shows or claims, title and scope, rights, money, anything irreversible, or a choice the rules do not settle that would change who leads.
- Update `state/STATE.json` and `state/HANDOVER.md`: status, open items for Luke, and rules for the next session.
- When Luke approves a design choice that later episodes should reuse, add it to `reference/house_style.md` in the same pull request.
- The pull request description lists: what was built, links to every private release, test results, numbered questions for Luke (each with Claude's recommendation), proposals beyond the approved design, and anything blocked.
- When something fails twice, turn the lesson into a check or a test.
