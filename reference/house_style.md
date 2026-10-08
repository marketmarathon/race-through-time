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
- **Callouts are rare,** used only at the biggest moments: changes of leader plus at most a handful of others, approved per episode (DEC-085, DEC-117). Each is one line under the title for about 3 s (DEC-111, kept by DEC-114).
- **No fixed length.** Pace follows the drama (project principle 12). Luke chose a faster film over the 8-minute mid-roll threshold for RTT-002 (DEC-076), so do not stretch a film to reach a length.
- **The title states the measure and its basis,** e.g. "Best-Selling Consoles (units shipped)" (DEC-111, kept by DEC-114).

## 2. Pacing
- **Calm in quiet periods, with brief emphasis at big moments** (DEC-068).
- **Event data** (races, matches): one beat per event, multiplied by (judged on the top ten in RTT-002, on all 15 rows in RTT-003):
  - ×1.4 when the visible top-ten order or membership changes;
  - ×1.0 when a visible bar grows;
  - ×0.8 when nothing visible changes, or after more than three visible-but-unchanged beats in a row.

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
  - It reads "· retired" when the bar ends on the manufacturer's own final total, or from a documented end of production. It reads "· latest figure" only where our figures run out with neither (DEC-140, refining DEC-132). A bar counts as stopped from the last period in which it added at least 10,000 units (DEC-142, *working choice*).
- **A source disagreement worth mentioning** gets a short footnote on the final table only, not during the race. Example: RTT-003's PS2 note (DEC-117).
- **Name the measure in the title** when the story is about something narrower: RTT-103's bars are total capital spending, so the title says so (e.g. "The AI Spending Race: Big Tech's Capital Spending") and AI is the story told around it (DEC-291, DEC-321). A narrower share (e.g. "AI") is never invented or multiplied into the bars: the companies' own statements appear as dated story moments, and a third-party share estimate at most once, labelled as an estimate (DEC-322, DEC-323).
- **Running totals are named for what they add up**: RTT-103's is "Combined capital spending", the sum of the bars on screen, never mixed with a narrower forecast (DEC-324). **Our own estimates** (RTT-103 look-ahead, owner exception DEC-326) are labelled "Race Through Time estimate" with the source of their growth assumption named, and the least reliable year is marked (DEC-327). Where forecasters disagree (e.g. on a peak), show the disagreement rather than one closing figure (DEC-328).
- **Late entrants** join the race at their first valid point from their own figures, with nothing before it (RTT-103: Meta 2012, Alibaba 2014, CoreWeave 2024 Q4; DEC-295).
- **A company measured differently** stays in the race with a short on-screen note saying how (RTT-103: Tencent, DEC-292).
- **Forecast frames** come after the historical race, clearly labelled ("2026 GUIDANCE"), from the companies' own forecasts first; ranges are shown as ranges, never as a midpoint alone. A look-ahead beyond the company forecasts (RTT-103 to 2031, owner exception DEC-306) may use named analyst, consensus or research-firm forecasts where a company gives no figure: it must look visibly different from the historical race, name each figure's forecaster and type, never be presented as official, never average or blend forecasters, and never extend beyond the years a source gives. A company figure that exists in writing only as a press report of a named executive is labelled "as reported by" the outlet (DEC-311). A fiscal year sits in the frame of the calendar year holding most of its months (DEC-314). A multi-year plan is never divided into years (DEC-313). A press report from unnamed sources may appear only greyed out and labelled as such, after the article has been read at source (RTT-103; DEC-296, DEC-297, DEC-306). How these frames look is still a design question for Luke (DEC-069).

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
- **Gold record line** at the all-time leader's figure, with its label, plus a **crown** on the leader's bar (RTT-003; DEC-125 (c), DEC-130, DEC-131).
- **Group scoreboard:** a small panel of group totals, e.g. maker totals (RTT-003; DEC-114, DEC-123).
- **A one-line summary on the final table,** e.g. "Switch is at least 3.4 million behind the PS2" (RTT-003; DEC-117).
- **Group logo beside the picture on each bar**, with the name on the bar (RTT-003; DEC-116, DEC-126; settled by DEC-138). RTT-003's tile is the picture box's height, 2:1, with the logo artwork trimmed to its own edges (DEC-142, *working choice*). Small text logos stay hard to read on a phone (RTT-003: SEGA 5.8 pt, Atari 2.6 pt, Nintendo 1.9 pt; DEC-142).
- **A subject picture box** in the bottom-right corner, e.g. RTT-002's car photo (DEC-045 (4)).

## 8. Open questions (not defaults yet)
- Should a smooth speed curve ever come back? (DEC-068, DEC-069)

Closed in round 5: logos versus the group name in type — logos kept (DEC-138); and how to label bars whose maker figures continue but stop growing — "retired" on the manufacturer's final total (DEC-140, section 5).
