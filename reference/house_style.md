# Race Through Time: house style

**What this is:** the design and production choices Luke has approved, collected so that each new episode starts from them instead of deciding them again. Drafted in Cowork on 3 Oct 2026 from `state/DECISIONS.md` up to DEC-137 (pull request #13); checked against the decisions and the two film configs and brought up to date with round 5 (DEC-138 to DEC-143) by Claude Code in IQ-11, 3 Oct 2026 (corrections listed in pull request #13). Every line cites its DEC. A line is owner-approved unless it is marked *(working choice, standing)*, which means a Claude choice that Luke has seen in an approved render and not objected to.

**How to use it**
- **Sections 1–6 are defaults for every new episode.** Use them without asking. Raise one with Luke only when the subject makes it wrong, and say why.
- **Section 7 is a menu of approved features** from earlier episodes. A new episode may propose them in its first pilot round. Luke confirms them for that episode (DEC-069 still applies).
- **Defaults are a starting point, not a template.** Each episode still gets its own story, pacing and board-size judgement (project principle 8: videos must not feel like a different CSV in the same template).
- **Keep this file current.** When Luke approves a reusable choice, or changes one listed here, update this file in the same pull request.

## 1. Shape of a film
- **No intro or title screen, and no outro or closing card** (DEC-070). Frame 0 is the board with its title (DEC-032, *working choice, standing*).
- **The final table holds for 5 s** at the end, from the frame where the last figures land to the last frame: YouTube's minimum end-screen window (YouTube Help, "Add end screens to videos": "End screens can be added to the last 5–20 seconds of a video"), so the end-screen elements sit over it (owner DEC-569, 9 Oct 2026, from RTT-102 onwards: "Yeah, I think cut it to five seconds"; replaces DEC-070's 10 s for later films). The approved films RTT-001, RTT-002, RTT-003 and RTT-103 keep their 10 s as approved. Set it so the time is counted from the landing frame (RTT-102: `pacing.final_board_sec` counts from the start of the last move, so `pacing.final_after_landing_sec` records the target and the episode's test checks it, DEC-567).
- **No running story captions** over the race: the viewer can see what is happening (DEC-068).
- **Callouts are rare,** used only at the biggest moments: changes of leader plus at most a handful of others, approved per episode (DEC-085, DEC-117). Each is one line under the title for about 3 s (DEC-111, kept by DEC-114). **Where viewers can see the change happen, leave the label out:** RTT-001 has no callouts at all, not even at its changes of leader (DEC-193, DEC-194; project principle 9). Propose callouts only where they add something the board does not show.
- **Story cards (RTT-103, owner DEC-357, DEC-358):** a dated story moment that the board cannot show (a company's own words, a commitment, a financing) appears as a small card on the right for about 3.5 s: its date, who, the quote trimmed to its essential words but word for word ("…" where cut), and a label ("company statement", "commitment · not capital spending", "financing · not capital spending", "estimate"); card text at least the size of the bar names (5.9 pt on a phone); never over a value label; never two at once (a later one waits, keeping its own date; no pause in the race); none on the final table. RTT-103 uses six. Commitments are never added together. **Luke is not keen on cards (RTT-102, DEC-549):** he prefers what our films usually have bottom right, a picture or one small piece of statistics (e.g. a running total with its line); propose cards only where nothing else can carry the moment.
- **No fixed length.** Pace follows the drama (project principle 12). Luke chose a faster film over the 8-minute mid-roll threshold for RTT-002 (DEC-076), so do not stretch a film to reach a length.
- **The title states the measure and its basis,** e.g. "Best-Selling Consoles (units shipped)" (DEC-111, kept by DEC-114). A title may instead name the contest in viewers' own words, with the measure in the line under it, as long as it claims no more than the data shows: RTT-102 "ChatGPT vs Its Rivals (2022–2026)" over "Monthly website visits · Similarweb estimates, worldwide" (DEC-552; "AI tools" was the most-searched term but would have claimed every AI site).

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
- **Big date, top right (RTT-001 onwards, DEC-222, DEC-229):** the year in extra-bold 112 px with the month in 40 px above it, right-aligned directly left of the RTT logo, replacing the small date line; the year rolls like an odometer over half a second when it changes (player key `date_block`, `time_label.mode` "none").
- **Era photo, bottom right (RTT-001, DEC-221, DEC-227 to DEC-229, DEC-231):** a real photograph of the typical device of the period (never a drawing), commercial-use licence only (public domain, CC0, CC BY, CC BY-SA), on a rounded 480 × 360 px tile (about 98 × 73 pt on a phone) that keeps at least 40 px clear of everything on the board on every frame; photos crossfade over 2 s at the era's switch dates; the device should belong to its era (no anachronisms). Credits go in the description only, not on screen (DEC-230). Player key `era` with `eras[].file`, files only in the private repo.
- **The RTT logo** is the round globe badge, top right, in a square box of about 154 px (DEC-051, DEC-052).
- **One picture per bar,** matching the name on the bar (DEC-114 (a)). Tall pictures must not look narrow; fix the sizing rather than swapping the picture (DEC-114 (e)). RTT-002 used today's design of each national flag (DEC-035 (1)).
- **The bottom strip** (about 130 px; Claude's estimate of what YouTube's controls cover) holds nothing important. The footer credits sit there (DEC-042, DEC-065).
- **The footer carries the data and photo credits.** The same credits go in the video description (DEC-065). Exception: the RTT-001 era photos and the music are credited in the description only (DEC-230).

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
- **A monthly flow that stops before the end** (RTT-102, DEC-545, DEC-535): the bar stays, dimmed, at its last published figure with "· latest figure, Sep 2025" (the month, because a monthly figure is not a running total), ranked below every bar that has a figure for the month and left out of any running total, with one plain line under the title when it drops out (DEC-558).
- **Numbers that are not published figures** (RTT-102, DEC-545, DEC-555, DEC-557): a value between two published months, or any value while the bars count, shows two significant figures ("~80m", "~3.9bn"); a published month shows its usual precision ("~73.0m"). The same idea as RTT-001's smoothed "~85%".
- **Older and newer versions of an estimate** (RTT-102, DEC-544, DEC-556): the stretch resting on the supplier's older version is striped until the first newer figure lands, and the one-line note explaining the stripes is on screen only while stripes are.
- **A source disagreement worth mentioning** gets a short footnote on the final table only, not during the race. Example: RTT-003's PS2 note (DEC-117).
- **Name the measure in the title** when the story is about something narrower: RTT-103's bars are total capital spending, so the title says so (e.g. "The AI Spending Race: Big Tech's Capital Spending") and AI is the story told around it (DEC-291, DEC-321). A narrower share (e.g. "AI") is never invented or multiplied into the bars: the companies' own statements appear as dated story moments, and a third-party share estimate at most once, labelled as an estimate (DEC-322, DEC-323).
- **Running totals are named for what they add up**: RTT-103's is "Combined capital spending", the sum of the bars on screen, never mixed with a narrower forecast (DEC-324). **Our own estimates** (RTT-103 look-ahead, owner exception DEC-326) are labelled "Race Through Time estimate" with the source of their growth assumption named, and the least reliable year is marked (DEC-327). Where forecasters disagree (e.g. on a peak), show the disagreement rather than one closing figure (DEC-328). A narrower forecast (e.g. AI-only spending) may sit in that comparison only under its own label, e.g. "AI capex (Allianz)", and is never added to a running total (DEC-344). An expected change that a chosen rule does not show (e.g. CoreWeave's 2027 dip in the rating agencies' views) goes in the notes or narration, not on the bar (DEC-342).
- **Late entrants** join the race at their first valid point from their own figures, with nothing before it (RTT-103: Meta 2012, Alibaba 2014, CoreWeave 2024 Q4; DEC-295).
- **A company whose figures are not comparable for a stretch** leaves the board and returns, with one plain line under the title each time (RTT-103 Alibaba, DEC-355); the running total says it is left out meanwhile.
- **Notes say how**, briefly, next to the bar (RTT-103 Tencent "· includes some intangibles"; DEC-292, DEC-356). **A company's own "approximately"** shows as "~" ("~$175bn"); a sum of plans given in whole billions is shown in whole billions ("$903–937bn"); an analyst's figure keeps the analyst-estimate look wherever it is the bar, forecast steps included (DEC-365 (b), (c)).
- **A company measured differently** stays in the race with a short on-screen note saying how (RTT-103: Tencent, DEC-292).
- **Forecast frames** come after the historical race, clearly labelled ("2026 GUIDANCE"), from the companies' own forecasts first; ranges are shown as ranges, never as a midpoint alone. A look-ahead beyond the company forecasts (RTT-103 to 2031, owner exception DEC-306) may use named analyst, consensus or research-firm forecasts where a company gives no figure: it must be marked as estimates **in the race's own style, not by a different look** (below, DEC-371), name each figure's forecaster and type, never be presented as official, never average or blend forecasters, and never extend beyond the years a source gives. A company figure that exists in writing only as a press report of a named executive is labelled "as reported by" the outlet (DEC-311). A fiscal year sits in the frame of the calendar year holding most of its months (DEC-314). A multi-year plan is never divided into years (DEC-313). A press report from unnamed sources may appear only greyed out and labelled as such, after the article has been read at source (RTT-103; DEC-296, DEC-297, DEC-306). **How they look (owner DEC-371, RTT-103; replaces DEC-306's "visibly different" and DEC-360's separate steps):** the race carries straight on after its last real period, on the same board - same title, logos, colours, big date top right, running-total panel - with one board per forward year counted in from the year before, bars moving and re-ranking as in the race, no title cards and no header changes. The company-plans year is one more board: ranges as ranges (solid to the bottom, half strength with a dashed outline to the top), each bar's short period or source note after its value ("· plan, as reported by Reuters", "· year to May 2027", "· Citi estimate, year to Mar 2027"), a press report greyed and marked "press report" and never counted in the total. Estimates use RTT-001's estimated look (dark diagonal stripes anchored to the frame, DEC-212; "~" values; an analyst's figure in the analyst-estimate look); one source line under the title while plans or estimates are on screen ("Race Through Time estimates · growth: FactSet consensus"); the date block reads "estimate" over the year; the least reliable year says so in that line; a "probably high" note sits beside the bar it concerns. One scale holds across the forward boards, so the bars grow into it. What a board cannot carry readably on a phone goes into one short explanation page after the last forward year, before the closing views. **Pacing (owner DEC-376, RTT-103):** no stop-and-go after the last real period - the race slows down markedly and flows straight on, each forward year a smooth, continuous move of about 6 s (values counting, bars re-ranking all the way; the company-plans year longer when it carries story cards, RTT-103 10.8 s), with a short hold (3 s) only on the last year, then the explanation page (short enough to read on a phone in the time shown: RTT-103 about 55 words for 16 s, the full wording in the description) and the closing views. The crown stays on the leader through the estimates (DEC-377). Luke: "just jumping to that other thing is just not what you would expect in a bar chart race." 
- **A series stitched from several sources** (RTT-001): one source line under the title names the month's source, ending " · estimated" while the figures are estimates (DEC-153, DEC-187); a small "New source" marker for 3 s when a new source starts; the changes of source are smoothed at draw time with the data unchanged, and smoothed estimated values read as whole-percent estimates, "~85%" or "<1%" (DEC-184, DEC-185). A one-line dated note may explain a change in what a source counted (DEC-186).

## 6. Sound, delivery and approval
- **Music:**
  - Luke chooses an exciting, fast, dramatic YouTube Audio Library track; Claude does not choose it (DEC-072).
  - The track is hash-checked, looped on the beat with crossfades, and faded out over the final table. It is mixed to −16 LUFS integrated with true peak ≤ −1 dBTP (DEC-072, DEC-074).
  - A track longer than the film is played once from where it gets going: a quiet intro or a long build-up is skipped to a strong beat (RTT-102 "Glitcher" from 10.5 s, on its drop, DEC-570).
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
  - **Stills are taken on the frame where a quarter's (or month's) figures land, never mid-move**, so the figures on a still are that period's; a test checks every still dated with a period against the data (RTT-103, DEC-365 (h)). In motion the date label changes at the start of each count while the values travel to it, as approved in RTT-003 and RTT-001.
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
- **Running total, bottom right: the number plus a small line that grows** (RTT-103 "Combined capital spending", DEC-324, DEC-359): it counts with the bars, marks a company's arrival with a dot and a gap with a shaded band, and says in one short line what is left out. RTT-102 "Combined monthly visits (sites shown)" (DEC-553, DEC-558): the sum of the bars with a figure that month, held bars left out.
- **Smooth motion through published points** (RTT-102, DEC-546): with sparse monthly figures the bars move on a monotone curve through the published figures (exact at each, never beyond them), not on straight lines; the data keeps its straight lines.
- **A one-line summary on the final table,** e.g. "Switch is at least 3.4 million behind the PS2" (RTT-003; DEC-117). Only if it says something the board cannot show: Luke dislikes lines that state what the board already shows (RTT-102, DEC-550); RTT-102 has none (DEC-554).
- **Group logo beside the picture on each bar**, with the name on the bar (RTT-003; DEC-116, DEC-126; settled by DEC-138). RTT-003's tile is the picture box's height, 2:1, with the logo artwork trimmed to its own edges (DEC-142, *working choice*). Small text logos stay hard to read on a phone (RTT-003: SEGA 5.8 pt, Atari 2.6 pt, Nintendo 1.9 pt; DEC-142).
- **A subject picture box** in the bottom-right corner, e.g. RTT-002's car photo (DEC-045 (4)).

## 8. Open questions (not defaults yet)
- Should a smooth speed curve ever come back? (DEC-068, DEC-069)

Closed for RTT-001 (5 Oct 2026): board sized to the bars on it — approved (DEC-204, section 3).

Closed in round 5: logos versus the group name in type — logos kept (DEC-138); and how to label bars whose maker figures continue but stop growing — "retired" on the manufacturer's final total (DEC-140, section 5).
