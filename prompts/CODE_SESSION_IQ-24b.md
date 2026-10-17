# IQ-24b — RTT-104 V3, Part 1 only: what caused each big change (data only, no design)

v1, 16 Oct 2026 (Cowork). This is a fresh session replacing the paused IQ-24 session, which did no work and pushed nothing. Luke is not technical: finish with a short plain-English summary. **Keep this lean: Luke is saving allowance.** Read only what you need: `state/HANDOVER.md`, `state/STATE.json`, the RTT-104 parts of `reports/RTT-104_data_report.md`, and the specific DECs cited (DEC-608, DEC-621, DEC-623, DEC-625, DEC-658). Do not read DECISIONS.md in full.

## Set-up
1. Work on branch `claude/nifty-brown-hrl2yi` (pull request #24). It is at c379631 (V2 approved, DEC-658). Merge `main` (f12dbb1, which includes pull request #26) into it first.
2. Save this exact prompt as `prompts/CODE_SESSION_IQ-24b.md`.
3. Use the RTT-104 DEC block. The next free number is after DEC-659; check across main and the open pull requests.
4. Hard rules as in CLAUDE.md. The approved V2 film, its configs and its workflow must not change. Do not merge.

## Decisions to record
- **Owner DEC** (Luke, Cowork, 10 Oct 2026 ~10:46 BST). Luke asked for a V3:
  - top 20 only, the classic bar-chart-race look with bigger bars;
  - each change explained on screen (e.g. an election) "so people can see what makes the change in the stats".

  V2 stays approved.
- **Owner DEC** (Luke, Cowork, 10 Oct 2026 12:25 BST). Luke chose to run Part 1 first, the data on causes, and stop before any design work. He waited for his weekly allowance to reset before starting.
- **Claude DEC** (Cowork recommendation, not an owner decision). Cause look-ups are limited to the "big" changes defined below. These are the only ones the quieter tag option would label on screen. Smaller changes are listed but not researched.

## Part 1 — data only (no player, stills, clip or render in this session)
1. **List the changes (cheap, from our own data).** Use the 4 m rule, fixed by latest-year population, and the same figures as `boards.csv`.
   - Rank every country by year as a top-20 board.
   - For every country ever in the top 20, list every year-to-year change: old value, new value, change in points, and old and new top-20 rank.
   - Mark a change **visible** if the country is in the top 20 in either year.
   - Mark it **big** if it is visible AND (the change is at least 5.0 points OR the rank moves by 3 or more places).
2. **Cost check before fetching.**
   - Count the big changes and the distinct country-and-election pages they need.
   - If more than about 80 Parline pages are needed, stop, push what you have, and report the count for Luke before fetching anything.
3. **Find elections, for big changes only.** On a GitHub runner, as in IQ-20, fetch the dated election records for the lower or single house from IPU Parline (data.ipu.org, the chamber's election pages). Record:
   - election date(s);
   - the type as Parline states it (general, by-election or other);
   - the URL and a short excerpt.

   Keep excerpts only, not raw pages, in the public repo.
4. **Match each big change to a cause.**
   - **Election:** only if a general election of that chamber falls inside the window between the two years' reference points. The reference date varies by year (DEC-621); record how each window was set and flag every borderline case.
   - **Other:** only where a source states it (a quota or seat law, appointed seats, a newly formed or reconstituted parliament, by-elections or replacements).
   - **Unexplained:** everything else. Never guess a cause.
   - If a country loses its parliament while in the top 20, note it (DEC-625).
5. **Output.**
   - `data/rtt-104/v3_change_events.csv`, one row per change (all changes, not only big ones), with:
     - country, from year, to year, old value, new value, change in points, old rank, new rank;
     - visible (y/n), big (y/n);
     - cause (election / other / unexplained / not researched), election date and type;
     - source URL, excerpt;
     - status (VERIFIED / UNVERIFIED / NOT FOUND).
   - A short report, `reports/RTT-104_v3_part1.md`, giving:
     - the counts: visible changes; big changes; the share of big changes explained by an election, by another sourced cause, and unexplained;
     - the 10 largest unexplained big changes;
     - tags per year and the most in any one year (this shows how busy the screen would be);
     - every borderline window.
6. **Checks.**
   - Every value in the CSV equals the WDI figures already in the branch.
   - Every "election" row has a Parline URL and an excerpt that shows the date.
   - The V2 config and workflow are byte-identical to c379631.

Update `state/`, push to pull request #24, and do not merge.

## Questions for Luke (put them in the summary, numbered, each with your recommendation and the default if he does not answer)
1. **Rights:** may the V3 tags use IPU Parline election dates? Parline sits under the same non-commercial IPU website terms as DEC-608. This would be on the same owner-accepted-risk basis as DEC-623, credited "IPU Parline". V3 is not published before he answers.
2. **Go on to Part 2 (design: top-20 board, tags, scale, pace)?** Recommend based on what Part 1 found. For example: go ahead if most big changes are explained; rethink the tags if most are unexplained.

Finish with a short plain-English summary for Luke: what was found, how many changes have a sourced cause, and the two questions.
