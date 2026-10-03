IQ-11 (3 Oct 2026): add the repo's CLAUDE.md and reference/house_style.md. Luke approved both in the Cowork chat on 3 Oct 2026.

Do this on the current branch (claude/sweet-mendel-faig7w, pull request #13) as its own commit, after round 5 is finished. Using the same branch avoids a second pull request editing state/ at the same time.

Rules for this task:
- First save this message, word for word, as prompts/CODE_SESSION_IQ-11.md.
- Render nothing. Do not change any data, player code or workflow.
- Do not merge.
- Finish with a short plain-English summary for Luke.

1. Create CLAUDE.md at the repo root with exactly the text between "BEGIN CLAUDE.md" and "END CLAUDE.md" below.

2. Create reference/house_style.md with exactly the text between "BEGIN house_style.md" and "END house_style.md" below. Then check it:
   - Check every DEC citation in it against state/DECISIONS.md on this branch.
   - Check every number in it against the configs: kits/rtt-002/config_rtt002_film.json and kits/rtt-003/config_rtt003_film.json.
   - Correct anything that does not match, and list each correction in the pull request description.
   - Do not add new design rules. Anything you think is missing goes in the pull request description as a question for Luke.
   - This file was drafted before round 5. Bring it up to date with round 5's decisions (for example the "latest figure" / "retired" rule and the open questions in section 8), citing their DEC numbers.

3. Fix the "Also" list in README.md. It predates DEC-060 and DEC-061: it says there are no GitHub Releases for unreleased films and talks about workflow-artifact retention.
   - Correct it to the current rules: renders go only to private pre-releases in marketmarathon/race-through-time-private, and this repo uploads no workflow artifacts.
   - Add one line pointing to CLAUDE.md for the full rules.

4. Record two decisions from the next free DEC number (check main and every open pull request):
   a. Owner (Luke, Cowork chat, 2 Oct 2026). RTT-001 Browser Wars is the next video after RTT-003. It covers the full browser wars, including the Netscape-vs-Internet Explorer era before StatCounter's series begins. Figures for the early years are built from the best available historical sources and shown on screen as estimates. Open question for Luke, not blocking: desktop only, or all devices from the smartphone era. The ChatGPT deep research prompt is with Luke; no answer has arrived yet.
   b. Owner (Luke, Cowork chat, 3 Oct 2026).
      - CLAUDE.md carries the standing rules for every Code session.
      - reference/house_style.md holds the approved design defaults.
      - Sections 1–6 of house_style.md apply to new episodes without asking Luke again, unless the subject makes a default wrong.
      - Section 7 lists approved features that a new episode may propose in its first pilot round, for Luke to confirm. DEC-069 is unchanged.
      - When Luke approves a reusable choice, it is added to house_style.md in the same pull request.

5. Update the state files:
   - state/STATE.json: add IQ-11 to implementation_queue. Add a pointer to CLAUDE.md in rules_all_sessions. Record RTT-001 as the next episode, wherever STATE.json keeps that.
   - state/HANDOVER.md: add a short IQ-11 note.

6. Add an IQ-11 section to pull request #13's description.

BEGIN CLAUDE.md
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
- Run the episode's test suite before any render (`node tests/player/run_tests.js` for RTT-002, `node tests/player/run_tests_rtt003.js` for RTT-003). If you change shared player code, show that RTT-002's approved output is unchanged.
- **Previews:** use stills to check layout, text, styling and readability. Use clips only to check motion, overtakes, pacing, timing or audio. Check every still at phone size too (`tests/player/phone_check*.js`).
- When a design question is open, show the options side by side in the same round rather than building one into the film.

## Recording the work
- Record decisions from the next free DEC number, checking `main` **and** every open pull request. Label each one as Owner, Claude working choice, Claude proposal or Claude finding.
- Update `state/STATE.json` and `state/HANDOVER.md`: status, open items for Luke, and rules for the next session.
- When Luke approves a design choice that later episodes should reuse, add it to `reference/house_style.md` in the same pull request.
- The pull request description lists: what was built, links to every private release, test results, numbered questions for Luke (each with Claude's recommendation), proposals beyond the approved design, and anything blocked.
- When something fails twice, turn the lesson into a check or a test.

END CLAUDE.md

BEGIN house_style.md
# Race Through Time: house style

**What this is:** the design and production choices Luke has approved, collected so that each new episode starts from them instead of deciding them again. Drafted in Cowork on 3 Oct 2026 from `state/DECISIONS.md` up to DEC-137 (pull request #13). Every line cites its DEC. A line is owner-approved unless it is marked *(working choice, standing)*, which means a Claude choice that Luke has seen in an approved render and not objected to.

**How to use it**
- **Sections 1–6 are defaults for every new episode.** Use them without asking. Raise one with Luke only when the subject makes it wrong, and say why.
- **Section 7 is a menu of approved features** from earlier episodes. A new episode may propose them in its first pilot round. Luke confirms them for that episode (DEC-069 still applies).
- **Defaults are a starting point, not a template.** Each episode still gets its own story, pacing and board-size judgement (project principle 8: videos must not feel like a different CSV in the same template).
- **Keep this file current.** When Luke approves a reusable choice, or changes one listed here, update this file in the same pull request.

## 1. Shape of a film
- **No intro or title screen, and no outro or closing card** (DEC-070). Frame 0 is the board with its title (DEC-032, *working choice, standing*).
- **The final table holds for 10 s** at the end, and YouTube's end-screen elements sit over it (DEC-070).
- **No running story captions** over the race: the viewer can see what is happening (DEC-068).
- **Callouts are rare,** used only at the biggest moments: changes of leader plus at most a handful of others, approved per episode (DEC-085, DEC-117). Each is one line under the title for about 3 s (DEC-111, kept by DEC-114).
- **No fixed length.** Pace follows the drama (project principle 12). Luke chose a faster film over the 8-minute mid-roll threshold for RTT-002 (DEC-076), so do not stretch a film to reach a length.
- **The title states the measure and its basis,** e.g. "Best-Selling Consoles (units shipped)" (DEC-111, kept by DEC-114).

## 2. Pacing
- **Calm in quiet periods, with brief emphasis at big moments** (DEC-068).
- **Event data** (races, matches): one beat per event, multiplied by:
  - ×1.4 when the visible top-ten order or membership changes;
  - ×1.0 when a visible bar grows;
  - ×0.8 when nothing visible changes.

  There is a 2.0 s pause on record moments. RTT-002 runs at 0.333 s per race (DEC-018, DEC-034, DEC-068, DEC-076).
- **Period data** (quarters, years): RTT-003 runs at 1.5 s per quarter, with its thin early years (1985–88) at half that (DEC-122, DEC-133), and a 2 s pause after each change of leader (DEC-125 (c)).
- **Choosing the speed:** render the same passage at two or three speeds and let Luke pick (DEC-071, DEC-076, DEC-118).
- **Not approved:** a smooth speed curve that slows around entries. It is an open question (DEC-068).

## 3. Board and frame
The reference frame is 1920 × 1080. Masters are rendered at 3840 × 2160.
- **Board size is set per episode, for phone readability.** Approved so far: top 20 (RTT-002, DEC-034) and top 15 (RTT-003, DEC-114, DEC-131).
- **How numbers move:**
  - Counts of discrete events step on the event and hold until the next one (DEC-017, *working choice, standing*).
  - Continuous measures count smoothly between data points and show the exact data value at each data point (DEC-115).
- **Values follow the bar.** Shown in the episode's unit with "+" where the figure is a lower bound, e.g. "118.7m+" (DEC-111, DEC-115). RTT-002 shows "91 wins · 306 starts · 29.7%" (DEC-053).
- **A small date line is always visible** near the title and changes at every data point (DEC-045 (3)).
- **The RTT logo** is the round globe badge, top right, in a square box of about 154 px (DEC-051, DEC-052).
- **One picture per bar,** matching the name on the bar (DEC-114 (a)). Tall pictures must not look narrow; fix the sizing rather than swapping the picture (DEC-114 (e)). RTT-002 used today's design of each national flag (DEC-035 (1)).
- **The bottom strip** (about 130 px; Claude's estimate of what YouTube's controls cover) holds nothing important. The footer credits sit there (DEC-042, DEC-065).
- **The footer carries the data and photo credits.** The same credits go in the video description (DEC-065).

## 4. Colour and motion
- **Colours:**
  - Each entity keeps one colour for the whole film.
  - No two entities on screen together share a colour, or come closer than CIEDE2000 18 (DEC-023, *working choice, standing*).
  - Where a group matters more than the entity (e.g. console makers), colour by group. Check the group colours under simulated colour blindness (DEC-107, approved DEC-114).
- **No flashes or strobing.** An event highlight is one gentle brightening with a soft glow, fading over 0.4 s (DEC-027, DEC-030). At most 3 highlight starts in any second. More needs Luke's knowing acceptance after a WCAG flash check, as for RTT-002 (DEC-077).

## 5. Evidence on screen
- **Estimated points** get dark diagonal stripes. **Analyst estimates** get the colour at half strength, a dashed outline and "· analyst estimate" after the value (DEC-090, DEC-099, DEC-111, kept by DEC-114). Never present an analyst estimate as official (DEC-084).
- **Bars that stop growing:**
  - The bar stays on the board, lightly dimmed (alpha 0.55, text 0.8) (DEC-131; values DEC-135, *working choice*).
  - It reads "· retired" only from a documented end date. Otherwise it reads "· latest figure" (DEC-132).
- **A source disagreement worth mentioning** gets a short footnote on the final table only, not during the race. Example: RTT-003's PS2 note (DEC-117).

## 6. Sound, delivery and approval
- **Music:**
  - Luke chooses an exciting, fast, dramatic YouTube Audio Library track; Claude does not choose it (DEC-072).
  - The track is hash-checked, looped on the beat with crossfades, and faded out over the final table. It is mixed to −16 LUFS integrated with true peak ≤ −1 dBTP (DEC-072, DEC-074).
  - The file lives only in the private repo (DEC-073).
  - RTT-003 reuses this approach with a new track (DEC-114 (d)).
- **No narration** has been approved so far.
- **Phone first:**
  - Every still is checked at phone size (a video 390 pt wide).
  - Names and values are no smaller than RTT-002's approved 5.9 pt (DEC-108; `tests/player/phone_check*.js`). RTT-003's labels are 6.7 pt.
- **Rendering:**
  - Rendered on GitHub runners as a 3840 × 2160 master plus a 1920 × 1080 viewing copy (DEC-061, DEC-076).
  - Saved only as a private pre-release in the private repo, with a SHA-256 for every file.
  - Luke approves the exact files by their SHA-256 (DEC-078).
- **Upload:**
  - For now Luke uploads by hand in YouTube Studio (DEC-080).
  - RTT-002's settings were: category matching the subject (Sports), Shorts remixing off (music licence), comments on, not made for kids, and a custom thumbnail (DEC-080).
  - Thumbnails start from Luke's thumbnail prompt template, kept in the Cowork project and in his Race Through Time folder.

## 7. Approved features to propose for new episodes
Luke approved each of these for the episode named. Propose any of them in a new episode's first pilot round.
- **Winner highlight** on the bar whose count just rose (RTT-002; DEC-027, DEC-030).
- **Record pause:** 2.0 s when a record is equalled or broken (RTT-002; DEC-034).
- **Gold record line** at the all-time leader's figure, with its label, plus a **crown** on the leader's bar (RTT-003; DEC-125 (c), DEC-130, DEC-131).
- **Group scoreboard:** a small panel of group totals, e.g. maker totals (RTT-003; DEC-114, DEC-123).
- **A one-line summary on the final table,** e.g. "Switch is at least 3.4 million behind the PS2" (RTT-003; DEC-117).
- **Group logo beside the picture on each bar** (RTT-003; DEC-116, DEC-126). The open question about legibility is in section 8.
- **A subject picture box** in the bottom-right corner, e.g. RTT-002's car photo (DEC-045 (4)).

## 8. Open questions (not defaults yet)
- Should a smooth speed curve ever come back? (DEC-068, DEC-069)
- Small text logos versus the group name in type, e.g. "Game Gear · Sega" (DEC-126, DEC-133).
- For consoles whose maker figures continue but stop growing, is "latest figure" right, or should documented end dates be found? (DEC-135)

END house_style.md
