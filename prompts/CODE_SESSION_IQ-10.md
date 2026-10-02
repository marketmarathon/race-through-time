You are working on Race Through Time (RTT). Task: IQ-10, the RTT-003 design pilot — "Best-Selling Consoles 1985–2026 (units shipped)". This session builds the RTT-003 player configuration, prepares the pictures and logos, and renders short PILOT CLIPS AND STILLS for Luke to judge. It does NOT render the full film. Luke, the owner, is not technical: finish with a short plain-English summary for him. First, save this exact prompt as prompts/CODE_SESSION_IQ-10.md.

BEFORE ANYTHING ELSE: check open pull requests and non-main branches in marketmarathon/race-through-time for existing RTT-003 player work, so nothing is duplicated (lesson from 30 Sep 2026). Then read state/STATE.json, state/HANDOVER.md, state/DECISIONS.md (especially DEC-006, DEC-036, DEC-057, DEC-060, DEC-061, DEC-068 to DEC-071, DEC-081 to DEC-102), reference/metric_contract_RTT-003.md, data/rtt-003/README.md, reports/RTT-003_data_report.md, reference/rights_ledger.md, and the approved RTT-002 player kit, config, render workflow and tests (kits/rtt-002/, .github/workflows/render_pilot.yml, tests/player/) — they are the model. Reuse and extend the existing player; do not rebuild it.

HARD RULES: never touch marketmarathon/bars. This repo is public (DEC-006): code, configs, data and written results only; pictures, logos, music, test frames, stills and renders live only in the private repo marketmarathon/race-through-time-private (DEC-060). Never print RTT_PRIVATE_TOKEN and never upload workflow artifacts from this repo (DEC-061). Nothing is uploaded to YouTube or published. Do not change the RTT-002 kit's approved behaviour, and do not trigger an RTT-002 render: the existing rule says a push that changes .github/workflows/render_pilot.yml renders the RTT-002 speed clips, so give RTT-003 its own workflow or job, or otherwise make sure no RTT-002 render starts. DEC-069: the features below are approved in principle only; anything not listed is a proposal for Luke, not something to build. Do not change the data in data/rtt-003/; if you find a data problem, stop and list it.

PICTURES AND LOGOS (private repo only):
- The checked list is research/rtt-003-images/RTT-003_images_reconciled_2026-09-30.csv in the private repo (49 rows: console, role PICK / SPARE / BACKUP / REJECT, Commons file title and page URL, licence, author, attribution, credit line, size, Commons SHA-1, notes). Use only the PICK rows (and BACKUP only if a PICK cannot be downloaded); never use REJECT rows.
- Download each file from Wikimedia Commons, check its SHA-1 against the CSV, and store it in the private repo under assets/rtt-003/ with a manifest (file, source URL, licence, author, credit line, SHA-1, SHA-256). If Commons (commons.wikimedia.org / upload.wikimedia.org) is blocked in this environment, stop that part, list the blocked hosts for Luke, and carry on with placeholders.
- Xbox Series X|S: the PICK is a CC BY 2.0 photo (Ian Hughes) with a background; cut the background out cleanly and record the credit line. It is the only picture that needs credit. Add every credit to reference/rights_ledger.md. Logos (public-domain text logos) may be used only to identify the maker, never to suggest endorsement.
- One picture per bar. Game Boy (including Game Boy Color) uses the original Game Boy picture. Where a family has two regional designs, the picture matches the name on the bar.

THE APPROVED DESIGN TO BUILD (DEC-085 and Luke's 2 Oct answers):
- Each bar: console name + console picture + maker colour. Value in millions, with "+" where the figure is a lower bound.
- A maker key with the logos (Nintendo, Sony/PlayStation, Microsoft/Xbox, Sega, Atari, NEC if any NEC console is in scope).
- Retired consoles fade, using the fade dates in the data (Atari 2600 from 31 Dec 1991).
- A "best-selling console ever" crown on the leader.
- Estimated stretches look estimated, using the DEC-090 rule; Xbox One after 3 Dec 2014 and Xbox Series X|S are labelled on screen as analyst estimates with a distinct look (DEC-084).
- Title on screen must say units shipped.
- Pacing: move quickly through 1985–88 (DEC-097). Otherwise follow the approved RTT-002 pacing approach (DEC-068): calm in quiet periods, brief emphasis at big moments. No fixed duration.
- Rare callouts at big moments only (crown changes and at most a handful of others). Propose the list; render only the crown changes in the pilot.
- Small company scoreboard (DEC-085): render it in one clip WITH and WITHOUT, so Luke can compare.
- PS2 note candidate (DEC-094): propose the wording for a short on-screen note about Sony's 155m vs 160m figures, and show it in one still; do not put it in the clips.
- Phone first: everything must be readable on a phone. Check every still at phone size and report on it.

WORKING CHOICES (make them, record them, and list each as a question for Luke):
(a) Bar names: use the names in data/rtt-003/consoles.csv, with Western names where a console had two (NES, Super NES). For Sega's 16-bit console use "Mega Drive / Genesis" if it fits at phone size, otherwise "Genesis". The picture matches the name.
(b) Maker colours: propose one colour per maker that is readable on the RTT-002 background and distinct for colour-blind viewers; show them in a still.
(c) Number of bars on screen: propose (e.g. top 10 or 12) and justify for phone readability.
(d) Music: none in the pilot. Ask Luke whether to reuse the RTT-002 approach with a new track.
(e) Pictures that may read poorly at icon size (Wii U, Switch docked, portrait shapes such as Xbox 360, PS5, Series X): show them and suggest fixes; do not swap pictures without listing it.

PILOT OUTPUT (render through GitHub Actions as for RTT-002; results as a private pre-release in the private repo, with SHA-256 for every file; 1080p; no music):
1. Clip A — the opening, 31 Mar 1985 to end-1992: thin two-console start, fast pacing, NES taking the crown (end-1988), Atari 2600 fading.
2. Clip B — 1996 to 1999: Game Boy takes the crown (end-1997).
3. Clip C — 2005 to 2009: PS2 takes the crown (mid-2007), Xbox One not yet; render twice, with and without the company scoreboard.
4. Stills: the board at 30 Jun 2026 (final table), at 2015 showing the Xbox analyst-estimate look, the maker colour key, the PS2 note still, and every still also at phone size.
5. tests: extend tests/player with checks for RTT-003 (no value before launch on screen, fade dates, crown matches data/rtt-003/crown.csv, "+" shown where the data says lower bound, estimate styling where the data says estimated).

STATE: record decisions from the next free number in state/DECISIONS.md (it should be DEC-103; check main and open pull requests first). Update state/STATE.json (RTT-003 episode and IQ-10) and state/HANDOVER.md. Push your branch and open a pull request against main; do not merge. The pull request description lists: what was built, links to the private pre-release and each clip/still, test results, the working choices as questions for Luke, any proposals beyond the approved design, the estimated full-film length, and anything blocked. Stop after opening the pull request.
