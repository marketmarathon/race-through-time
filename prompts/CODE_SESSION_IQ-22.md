# IQ-22 — RTT-104 Women in Parliament: design round 1

v1, 10 Oct 2026 (Cowork). Continue on your IQ-20 branch (PR #24), DEC block 600–699 (next free after DEC-623; check). Luke is not technical: finish with a short plain-English summary.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-22.md`.

Read `reference/house_style.md` and the approved RTT-001/102/103 design DECs on their branches. House defaults apply without asking, e.g.:
- dark navy background
- "~" only for estimates (none here)
- the bottom-right panel for one small chart
- no story cards unless Luke asks (he dislikes them)
- no closing line that repeats what the board shows
- a 5 s final table (DEC-569)
- logo or picture tile to the left of the bar where rights allow

Hard rules as in CLAUDE.md. No music, no full film. Stills, sheets and clips go to a PRIVATE pre-release in `race-through-time-private` with SHA-256 for each; the public repo holds code and config only. Do not merge.

## Owner decisions to record first (Luke, Cowork chat, 10 Oct 2026, answers to report §16)
1. **Year label:** show the year only (e.g. "2019"), never a day or month. The description says "annual figures as published by the World Bank (World Development Indicators), from the IPU's monthly ranking of women in national parliaments".
2. **Countries that lose their parliament while on a board:** this must be made clear ON SCREEN at that moment, not only at the end. The bar shows a short reason, then leaves the board (Luke: "probably disappear… it needs to be made clear why"). This is a new visual feature: show options in this round (DEC-069).

   From your data, the in-race countries whose figures stop:
   - Haiti: last 2019, 2.5%, on the bottom board. Reason: deputies' terms expired in January 2020 with no election.
   - Kuwait: last 2023, 3.1%. Check whether it was on the bottom board in 2023. Reason: dissolved by the Emir in May 2024.

   Confirm from `boards.csv` which of the six were on a board in their last year. Those not on a board stay closing-card only.

   Wording uses the VERIFIED IPU quotes in `closing_card.csv` (e.g. Sudan: "dissolved following a coup d'état in April 2019").
3. **Closing card approved:** the six lines (Afghanistan, Bangladesh, Haiti, Kuwait, Myanmar, Sudan) under the heading "Not included: no sitting parliament". Nepal stays off.
4. **Name: "Türkiye"** (the UN and World Bank name).

## Round 1: options side by side (stills plus a phone copy of each; questions only on what is new)
a. **Split layout.** A: top board on the left, bottom board on the right. B: top board above, bottom board below. Show 2003, 2013 and 2025 in each, plus phone copies. Recommend one on phone readability.

b. **Scale.** A: both boards on ONE shared 0–70% scale (honest: shows the gulf; bottom bars are short). B: each board with its own scale, labelled. Principle 21 applies: the screen must not make 5% look like 50%. If you show B, its scale must be unmistakable.

c. **The 0% group bar** (DEC-602), e.g. "No women in parliament: Oman, Yemen". Show 2–3 looks at the bottom of the bottom board, for 1997 (3 countries) and 2025 (2).

d. **Leaving-the-board note** (decision 2) for Haiti 2020 (and Kuwait 2024 if it was on a board):
   - A: a short label on the bar, e.g. "Haiti: parliament's term expired, no election", then the bar fades out.
   - B: the bar greys out with the label for one beat, then leaves.

   Give one still per option and one short clip if the motion matters.

e. **Picture tile per country.** A: national flag (Wikimedia Commons; record the licence of each file in the rights ledger; flags only, no emblems). B: names only. Recommend one.

f. **Bottom-right panel:** the world average line (WDI WLD), labelled "World average (all countries)". Show 2003 and 2025.

g. **Title and credits:**
   - Title: "Women in Parliament: Highest vs Lowest (1997–2025)".
   - Measure line, e.g. "Share of seats held by women · lower or single house".
   - Credit line: "Data: Inter-Parliamentary Union (IPU), via World Bank World Development Indicators (CC BY 4.0)".

h. **Closing card** (decision 3), as one still.

i. **Pace:** one clip of 2001–2009 (Rwanda takes first place, the UAE rises, Saudi Arabia appears) at 2 s and at 3 s per year, eased, with the estimated running time of the whole film for each.

## Checks and report
- Every value on every still equals `boards.csv`.
- Phone check of every still.
- WCAG flash check of each clip.
- Approved films (RTT-001/002/003/102/103) frame-identical.
- Release notes list every file's SHA-256.
- Add numbered questions for Luke, each with your recommendation and the default if he does not answer. Ask only about a–i.

Update `state/`, push to PR #24, do not merge. Finish with the plain-English summary.
