# RTT-104 Women in Parliament — design round 1 (IQ-22, 10 Oct 2026)

Brief: `prompts/CODE_SESSION_IQ-22.md`. Decisions: DEC-624..DEC-627 (Luke's answers to the data report), DEC-628..DEC-633 (Claude). Nothing here is approved: every look is an option for Luke (DEC-069). No music, no film.

**Private pre-release (stills, phone copies, sheets, clips, every SHA-256 in its notes):** RELEASE_URL

## What Luke decided before this round
- Year only on screen, never a day or month (DEC-624).
- A country that loses its parliament while on a board says why on screen at that moment, then leaves (DEC-625). From the data (DEC-628): **Haiti** (bottom board in 2019, no figure from 2020) and **Kuwait** (bottom board in 2023, no figure from 2024). Afghanistan, Bangladesh, Myanmar and Sudan were not on a board in their last year: closing card only. Two more countries leave the bottom board because their figures **pause**, with no reason found at source: **Pakistan** (1999–2001) and **Egypt** (2013–2015) — see question 4.
- Closing card: the six lines under "Not included: no sitting parliament"; Nepal off (DEC-626). "Türkiye" (DEC-627).

## How it is built
RTT-104 has its own page, `kits/rtt-104/player_rtt104.html`, opened through the shared driver (`kits/rtt-002/rtt.js`), so the approved films cannot change: nothing in `kits/rtt-001`, `kits/rtt-002`, `kits/rtt-003`, `tests/player` or another episode's workflow was touched (DEC-629). Every option is a config that changes one setting from `config_rtt104_base.json` (the recommended set).

## Checks
- **Values:** every board still shows exactly `data/rtt-104/boards.csv` for its year (countries, order, one-decimal values) and the 0% group equals `zero_group.csv` (`kits/rtt-104/render_stills.js`, results `tests/rtt104/STILLS_CHECK.md`).
- **Phone (390 pt wide):** layout A names and values 30 px = **6.1 pt**, all other text at least 5.3 pt — PASS. Layout B 23 px = **4.7 pt**, axis 4.1 pt — below RTT-002's approved 5.9 pt.
- **Overlap:** no text inside the world panel or past its board — PASS.
- **WCAG flash** (whole picture, `tests/player/wcag_flash_rtt003.js`, limit 57,600 px in a 10-degree field): 2001–2009 at 2 s per year 51,182 px PASS; at 3 s 48,153 px PASS; Haiti clips 26,873 px PASS. A faster move (1.2 s) failed at 68,833 px when many rows cross in 2002→2003, so the 2 s pace moves for 1.7 s and holds 0.3 s (DEC-631). The whole film needs this check before any film render.
- **Approved films unchanged:** no shared file changed against `main` (DEC-629).
- **Data tests:** `python3 tests/rtt104/run_tests_rtt104.py` 23/23 PASS (now including the player input rebuilt identically from the data).

## Running time (estimate, whole film not rendered)
- 2 s per year: 2,271 frames = **1 min 16 s**.
- 3 s per year: 3,111 frames = **1 min 44 s**.
Each includes a 1.5 s opening on 1997, four 1.8 s leave notes, the 5 s final table (DEC-569) and a 6 s closing card.

## Questions for Luke (each with Claude's recommendation and what happens if there is no answer)
1. **(a) Layout** — sheets `sheet_a_2003`, `_2013`, `_2025`. A: top board left, bottom board right. B: top board above, bottom board below. *Recommendation:* **A**. On a phone its names and values are 6.1 pt; B's are 4.7 pt, too small (21 rows share the height). Both boards are one colour each (teal "Highest", amber "Lowest"), with the flag identifying the country (DEC-630 (a)). *If no answer:* A.
2. **(b) Scale** — `sheet_b_scale`. A: one shared 0–70% scale. B: each board its own fixed scale, the bottom one marked "Zoomed scale 0–15%" with amber axis numbers. *Recommendation:* **A**: it shows the real gulf (Rwanda 63.8% against Papua New Guinea 2.7%) and never makes 5% look like 50%; with B the bottom bars look as long as the top ones, and the world panel no longer fits. *If no answer:* A.
3. **(c) The 0% group** — `sheet_c_1997` (3 countries), `sheet_c_2025` (2). 1: a group bar "No women in parliament: 3 countries" with "0% · Jordan, Kuwait, United Arab Emirates". 2: a strip under the board, "0% no women in parliament", then flag and name chips. 3: "No women: 3 countries" with "0%" and flag and name chips. *Recommendation:* **3**: it is your wording, reads as one more row of the board, and the flags make the countries recognisable. *If no answer:* 3.
4. **(d) Leaving the board** — `sheet_d_Haiti`, `sheet_d_Kuwait`, clips `clip_d_fade_2018_2021` and `clip_d_grey_2018_2021`. A: the note appears on the bar ("— No sitting parliament: deputies' terms expired Jan 2020"), then the bar fades. B: the bar greys out with the note for one beat, then shrinks away. Both hold the note for 1.8 s at the end of the last year with a figure, then move on. *Recommendation:* **B**: the grey shows at once that the country is no longer counted, and the shrink makes the exit unmistakable. Also: **(d2)** Pakistan (1999) and Egypt (2013) leave the bottom board with no reason found at source: show "— No figure 1999–2001" / "— No figure 2013–2015" the same way (stills `d5`, `d6`)? *Recommendation:* yes, so they do not vanish unexplained; nothing beyond the missing figure is claimed. **(d3)** The two lines' wording: "No sitting parliament: deputies' terms expired Jan 2020" (Haiti) and "No sitting parliament: dissolved by the Emir, May 2024" (Kuwait), from the IPU quotes. *If no answer:* B, the "No figure" lines shown, the wording as shown.
5. **(e) Flags** — `sheet_e_2013`. A: a flag left of each bar. B: names only. *Recommendation:* **A**, using the same flag files as RTT-002's approved film (flag-icons, MIT; DEC-630 (g)) rather than downloading new ones from Wikimedia Commons; every file's hash is listed. *If no answer:* A with flag-icons.
6. **(f) World panel** — in every layout-A still (e.g. `a1_layoutA_left_right_2003`, `_2025`): "World average (all countries)", the line from 1997 to the current year on a 0–30% scale, with its value (11.7% in 1997, 27.2% in 2025). *Recommendation:* as shown (it needs the shared scale, question 2). *If no answer:* as shown.
7. **(g) Title and credits** — every still: title "Women in Parliament: Highest vs Lowest (1997–2025)", measure line "Share of seats held by women · lower or single house", footer "Race Through Time · Data: Inter-Parliamentary Union (IPU), via World Bank World Development Indicators (CC BY 4.0)" (5.3 pt on a phone). Opening frame: `g_opening_1997`. *Recommendation:* as shown. *If no answer:* as shown.
8. **(h) Closing card** — `h_closing_card`: the six approved lines with flags, under "Not included: no sitting parliament". I added one line under the heading: "Countries of 4 million people or more with no figure for 2025". *Recommendation:* keep it (it says exactly who is listed). *If no answer:* kept.
9. **(i) Pace** — clips `clip_i_2s_2001_2009` and `clip_i_3s_2001_2009` (Rwanda takes first place in 2003; Saudi Arabia first appears in 2003, in the 0% group; the UAE leaves the 0% group in 2006 at 5.0% and is at 22.5% in 2007). *Recommendation:* **2 s per year** (about 1 min 16 s): most years change little, and the big moves still get 1.7 s. 3 s gives 1 min 44 s. *If no answer:* 2 s.

## Proposals beyond the approved design
All of the above are proposals (DEC-069). Built only as options; no film.
