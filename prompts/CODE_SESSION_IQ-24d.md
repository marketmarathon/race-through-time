# IQ-24d — RTT-104 V3 Part 2: design round (top-20 board and election tags)

v1, 17 Oct 2026 (Cowork). This is a fresh session to keep the cost down. Work on branch `claude/nifty-brown-hrl2yi` (pull request #24). The next DEC is after DEC-671; check across main and the open pull requests. Luke is not technical: finish with a short plain-English summary. **Keep it lean: Luke is saving allowance.**

Read only what you need:
- `state/HANDOVER.md` and `state/STATE.json`
- `reports/RTT-104_v3_part1.md`, section 8
- `data/rtt-104/v3_change_events.csv`
- the V2 player and configs in `kits/rtt-104/`, to reuse what works
- the DECs you need: DEC-621, DEC-623, DEC-654/655, DEC-658, DEC-660–671

Do not read DECISIONS.md in full.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-24d.md`. Hard rules as in CLAUDE.md. Stills and clips go to a PRIVATE pre-release in `race-through-time-private`, with a SHA-256 for each file. The approved V2 film, its configs and its workflow must not change. Do not merge.

## Owner decisions to record (Luke, Cowork, 17 Oct 2026 09:38 BST)
1. Go ahead with the V3 design round.
2. Tag rule: Luke wants to **see both rules in action** before choosing:
   - (a) only changes of 5 points or more;
   - (b) also moves of 3 or more places.

   Show them side by side. Neither is chosen yet.
3. Late-year elections: Luke asked why a November or December election would count towards the next year. Cowork has explained it to him: the year's figure is a snapshot taken before the election, so the jump shows up in the next year's figure. His answer is pending.
   - Show the proposal on one real case: the tag shows the true election date (e.g. "Election · Nov 2001") and lands on the jump it caused.
   - Mark it as a proposal. Only use cases where the figure's reference date is known to fall before the election.

## Unchanged from approved rules
- 4 m population rule
- year only on screen
- "Türkiye"
- flags (flag-icons)
- credit "Data: IPU via World Bank WDI (CC BY 4.0)", plus "Election dates: IPU Parline"
- smooth motion through every year (DEC-654/655)
- music "No.10 A New Beginning"
- no country loses its parliament while in the top 20

## Design round (options side by side; ask only about what is new)
a. **Board.** One full-width board with the top 20, and much bigger bars, in the classic look of the approved RTT-001/RTT-003 films:
   - flag to the left of the bar
   - name and value on the bar
   - big year
   - world-average panel bottom right ("World average (all countries)")
   - title "Women in Parliament: The Top 20 (1997–2025)"
   - measure line "Share of seats held by women · lower or single house"

   Phone check: if 20 rows read below about 5.9 pt on a phone, say so and also show a top-15 still.
b. **Tag look.** A short tag beside the bar, e.g. "Election · Oct 2019", held about 2 s while the bar moves. Tags come only from VERIFIED rows. Unexplained changes get no tag. Show 2 looks of the tag on the same still.
c. **Scale.** 0–70% fixed vs the scale following the leader. One still each; recommend one.

## What to make (cheapest that answers the questions)
- **Stills, each with a phone copy:**
  - 1997, 2014 and 2025 boards with the recommended tag look;
  - the tag-look sheet;
  - the scale pair;
  - the late-election case.
- **Two short clips of the same busy stretch** (around 2017–2020, which includes 2019, the busiest year), at 3 s per year as V2:
  - one with tag rule (a);
  - one with tag rule (b).

  Run a WCAG flash check on both.
- No full film.

## Checks
- Every value equals the data.
- Every tag maps to a VERIFIED row of `v3_change_events.csv` with a fetched excerpt.
- V2 is byte-identical to c379631.

Update `state/`, push to pull request #24, and do not merge.

## Questions for Luke (numbered; give your recommendation and the default for each)
1. Board size: 20 or 15.
2. Tag look.
3. Tag rule (a) or (b), after watching both clips.
4. Scale.
5. Late-year elections: tag the jump they caused, with the true date (proposal), or leave those jumps untagged.

Finish with the plain-English summary.
