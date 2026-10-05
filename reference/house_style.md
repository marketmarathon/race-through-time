# Race Through Time: house style

**What this is:** the design and production choices Luke has approved, collected so that each new episode starts from them instead of deciding them again. Drafted in Cowork on 3 Oct 2026 from `state/DECISIONS.md` up to DEC-137 (pull request #13); checked against the decisions and the two film configs and brought up to date with round 5 (DEC-138 to DEC-143) by Claude Code in IQ-11, 3 Oct 2026 (corrections listed in pull request #13). Every line cites its DEC. A line is owner-approved unless it is marked *(working choice, standing)*, which means a Claude choice that Luke has seen in an approved render and not objected to.

**How to use it**
- **Sections 1–6 are defaults for every new episode.** Use them without asking. Raise one with Luke only when the subject makes it wrong, and say why.
- **Section 7 is a menu of approved features** from earlier episodes. A new episode may propose them in its first pilot round. Luke confirms them for that episode (DEC-069 still applies).
- **Defaults are a starting point, not a template.** Each episode still gets its own story, pacing and board-size judgement (project principle 8: videos must not feel like a different CSV in the same template).
- **Keep this file current.** When Luke approves a reusable choice, or changes one listed here, update this file in the same pull request.

## 1. Shape of a film
- **No intro or title screen, and no outro or closing card** (DEC-070). Frame 0 is the board with its title (DEC-032, *working choice, standing*).
- **The final table holds for 10 s** at the end, and YouTube's end-screen elements sit over it (DEC-070).
- **No running story captions** over the race: the viewer can see what is happening (DEC-068).
- **Callouts are rare,** used only at the biggest moments: changes of leader plus at most a handful of others, approved per episode (DEC-085, DEC-117). Each is one line under the title for about 3 s (DEC-111, kept by DEC-114). **Where viewers can see the change happen, leave the label out:** RTT-001 has no callouts at all, not even at its changes of leader (DEC-193, DEC-194; project principle 9). Propose callouts only where they add something the board does not show.
- **No fixed length.** Pace follows the drama (project principle 12). Luke chose a faster film over the 8-minute mid-roll threshold for RTT-002 (DEC-076), so do not stretch a film to reach a length.
- **The title states the measure and its basis,** e.g. "Best-Selling Consoles (units shipped)" (DEC-111, kept by DEC-114).

## 2. Pacing
- **Calm in quiet periods, with brief emphasis at big moments** (DEC-068).
- **Event data** (races, matches): one beat per event, multiplied by (judged on the top ten in RTT-002, on all 15 rows in RTT-003):
  - ×1.4 when the visible top-ten order or membership changes;
  - ×1.0 when a visible bar grows;
  - ×0.8 when nothing visible changes, or after more than three visible-but-unchanged beats in a row.

  There is a 2.0 s pause on record moments. RTT-002 runs at 0.333 s per race (DEC-018, DEC-034, DEC-068, DEC-076).
- **Period data** (quarters, years): RTT-003 runs at 1.5 s per quarter, with its thin early years (1985–88) at half that (DEC-122, DEC-133), and a 2 s pause after each change of leader (DEC-125 (c)). RTT-001 (monthly shares) runs at 0.5 s per month with the same multipliers (DEC-195), with no pause at its changes of leader, because it has no callouts (DEC-206).
- **Speed up when there isn't much going on:** a long calm stretch may run at one named faster fixed pace from a clean boundary, e.g. RTT-001 at 0.3 s per month from January 2014, once Chrome's lead is settled (DEC-196). This is one change of pace, not a speed curve.
- **Choosing the speed:** render the same passage at two or three speeds and let Luke pick (DEC-071, DEC-076, DEC-118).
- **Not approved:** a smooth speed curve that slows around entries. It is an open question (DEC-068).

## 3. Board and frame
The reference frame is 1920 × 1080. Masters are rendered at 3840 × 2160.
- **Board size is set per episode, for phone readability.** Approved so far: top 20 (RTT-002, DEC-034), top 15 (RTT-003, DEC-114, DEC-131) and top 10 (RTT-001, DEC-188).
- **When few entities exist, the board adapts instead of leaving empty slots:** rows are sized to the number of bars on the board, never more than twice the board's normal thickness, settling at the episode's board size; only row height and bar thickness change (text, pictures and the bars' left edge stay put), and each resize eases over about 2 s, opening room before new bars arrive (RTT-001; DEC-188, DEC-202, DEC-204, DEC-205; player key `board.fit`).
- **How numbers move:**
  - Counts of discrete events step on the event and hold until the next one (DEC-017, *working choice, standing*).
  - Continuous measures count smoothly between data points and show the exact data value at each data point (DEC-115).
- **Values follow the bar.** Shown in the episode's unit with "+" where the figure is a lower bound, e.g. "118.7m+" (DEC-111, DEC-115). RTT-002 shows "91 wins · 306 starts · 29.7%" (DEC-053). Shares of a total show one decimal, e.g. "44.0%" (RTT-001, DEC-189).
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
- **A moving bar must not carry a moving pattern:** striped (estimated) bars that glide up or down draw their stripes anchored to the frame, not the bar, or the stripes flicker; RTT-001's whole-film check failed until this was done (DEC-212). Every film gets the whole-picture WCAG flash check before its render (`tests/player/wcag_flash_rtt003.js`; RTT-003 DEC-149, RTT-001 DEC-213).
- **No flashes or strobing.** An event highlight is one gentle brightening with a soft glow, fading over 0.4 s (DEC-027, DEC-030). At most 3 highlight starts in any second. More needs Luke's knowing acceptance after a WCAG flash check, as for RTT-002 (DEC-077).

## 5. Evidence on screen
- **Estimated points** get dark diagonal stripes. **Analyst estimates** get the colour at half strength, a dashed outline and "· analyst estimate" after the value (DEC-090, DEC-099, DEC-111, kept by DEC-114). Never present an analyst estimate as official (DEC-084).
- **Bars that stop growing:**
  - The bar stays on the board, lightly dimmed (alpha 0.55, text 0.8) (DEC-131; values DEC-135, *working choice*).
  - It reads "· retired" when the bar ends on the manufacturer's own final total, or from a documented end of production. It reads "· latest figure" only where our figures run out with neither (DEC-140, refining DEC-132). A bar counts as stopped from the last period in which it added at least 10,000 units (DEC-142, *working choice*).
- **A source disagreement worth mentioning** gets a short footnote on the final table only, not during the race. Example: RTT-003's PS2 note (DEC-117).
- **A series stitched from several sources** (RTT-001): one source line under the title names the month's source, ending " · estimated" while the figures are estimates (DEC-153, DEC-187); a small "New source" marker for 3 s when a new source starts; the changes of source are smoothed at draw time with the data unchanged, and smoothed estimated values read as whole-percent estimates, "~85%" or "<1%" (DEC-184, DEC-185). A one-line dated note may explain a change in what a source counted (DEC-186).

## 6. Sound, delivery and approval
- **Music:**
  - Luke chooses an exciting, fast, dramatic YouTube Audio Library track; Claude does not choose it (DEC-072).
  - The track is hash-checked, looped on the beat with crossfades, and faded out over the final table. It is mixed to −16 LUFS integrated with true peak ≤ −1 dBTP (DEC-072, DEC-074).
  - The file lives only in the private repo (DEC-073).
  - RTT-003 reuses this approach with a new track (DEC-114 (d)): "Powerup!" by Jeremy Blake (DEC-147), loop points found with `scripts/rtt_music_loop.py` (DEC-148, *working choice*).
- **No narration** has been approved so far.
- **Phone first:**
  - Every still is checked at phone size (a video 390 pt wide).
  - Names and values are no smaller than RTT-002's approved 5.9 pt (DEC-108, *working choice, standing*; `tests/player/phone_check*.js`). RTT-003's labels are 6.7 pt.
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
- **Gold record line** at the all-time leader's figure, with its label, plus a **crown** on the leader's bar (RTT-003; DEC-125 (c), DEC-130, DEC-131). The crown alone on the leader's bar (RTT-001; DEC-192).
- **A logo per bar, purely to identify it,** on a light tile left of the bar, with the name on the bar; non-free logo files accepted by Luke for identification, each file's source and status in the rights ledger; crop only where Luke allows it, never redrawn; our own neutral tile (name and launch year in the bar colour) where no real logo exists (RTT-001; DEC-180, DEC-182, DEC-191, DEC-198, DEC-199).
- **Group scoreboard:** a small panel of group totals, e.g. maker totals (RTT-003; DEC-114, DEC-123).
- **A one-line summary on the final table,** e.g. "Switch is at least 3.4 million behind the PS2" (RTT-003; DEC-117).
- **Group logo beside the picture on each bar**, with the name on the bar (RTT-003; DEC-116, DEC-126; settled by DEC-138). RTT-003's tile is the picture box's height, 2:1, with the logo artwork trimmed to its own edges (DEC-142, *working choice*). Small text logos stay hard to read on a phone (RTT-003: SEGA 5.8 pt, Atari 2.6 pt, Nintendo 1.9 pt; DEC-142).
- **A subject picture box** in the bottom-right corner, e.g. RTT-002's car photo (DEC-045 (4)).

## 8. Open questions (not defaults yet)
- Should a smooth speed curve ever come back? (DEC-068, DEC-069)

Closed for RTT-001 (5 Oct 2026): board sized to the bars on it — approved (DEC-204, section 3).

Closed in round 5: logos versus the group name in type — logos kept (DEC-138); and how to label bars whose maker figures continue but stop growing — "retired" on the manufacturer's final total (DEC-140, section 5).
