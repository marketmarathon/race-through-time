# RTT-102 AI assistant websites race: data report (phase 1, IQ-17)

Built by `python3 scripts/build_rtt102_dataset.py data/rtt-102 reports/RTT-102_data_report.md` (deterministic). Method: `reference/metric_contract_RTT-102.md`. Decisions DEC-500 to DEC-514. **Data only: nothing designed or rendered (DEC-069).**

**What the race shows:** Similarweb's published estimates of monthly website visits, worldwide, to eight AI assistant websites, December 2022 to September 2026. Not market share and not users. Every bar value rests on a figure seen at its source (Cowork in Luke's Chrome, or a GitHub runner reading the page); straight lines join published months.

**In numbers:** 256 figure rows from 53 publications; 242 VERIFIED, 13 UNVERIFIED, 1 NOT FOUND. 153 points used on bars (139 from Similarweb's own publications, 14 from press quoting Similarweb). 236 bar-months, of which 153 published and 83 on straight lines. Checks: 11/11 PASS.

## 1. Coverage grid (assistant × month)

`●` published and used · `○` straight line between two published months · `?` an UNVERIFIED figure exists but no verified one (on Cowork's list) · `!` leftover conflict for Luke · blank: no bar. Bars appear from their first published month; none is extended past its last.

| Month | ChatGPT | Gemini (Bard) | Claude | Copilot | Perplexity | DeepSeek | Grok | Meta AI |
|---|---|---|---|---|---|---|---|---|
| Dec 2022 | ● |  |  |  | ● |  |  |  |
| Jan 2023 | ● |  |  |  | ○ |  |  |  |
| Feb 2023 | ● |  |  |  | ○ |  |  |  |
| Mar 2023 | ● | ● |  |  | ○ |  |  |  |
| Apr 2023 | ● | ● |  |  | ○ |  |  |  |
| May 2023 | ● | ● |  |  | ○ |  |  |  |
| Jun 2023 | ● | ○ |  |  | ○ |  |  |  |
| Jul 2023 | ● | ○ |  |  | ○ |  |  |  |
| Aug 2023 | ● | ○ |  |  | ○ |  |  |  |
| Sep 2023 | ● | ● |  |  | ○ |  |  |  |
| Oct 2023 | ● | ○ |  |  | ○ |  |  |  |
| Nov 2023 | ● | ● | ● |  | ○ |  |  |  |
| Dec 2023 | ○ | ○ | ○ |  | ● |  |  |  |
| Jan 2024 | ○ | ○ | ○ |  | ○ |  |  |  |
| Feb 2024 | ● | ○ | ○ |  | ○ |  |  |  |
| Mar 2024 | ● | ● | ○ |  | ● |  |  |  |
| Apr 2024 | ● | ○ | ○ |  | ● |  |  |  |
| May 2024 | ● | ○ | ○ |  | ○ |  |  |  |
| Jun 2024 | ○ | ○ | ○ |  | ○ |  |  |  |
| Jul 2024 | ○ | ○ | ○ |  | ○ |  |  |  |
| Aug 2024 | ○ | ○ | ○ |  | ○ |  |  |  |
| Sep 2024 | ● | ● | ● | ● | ● |  |  | ● |
| Oct 2024 | ● | ● | ● | ● | ● |  |  | ○ |
| Nov 2024 | ○ | ○ | ○ | ○ | ○ |  |  | ○ |
| Dec 2024 | ● | ○ | ○ | ○ | ○ |  |  | ○ |
| Jan 2025 | ● | ● | ● | ○ | ● | ● | ● | ● |
| Feb 2025 | ● | ● | ● | ○ | ● | ● | ● | ● |
| Mar 2025 | ● | ● | ● | ○ | ● | ● | ● | ● |
| Apr 2025 | ● | ● | ● | ○ | ● | ● | ● | ● |
| May 2025 | ● | ● | ● | ○ | ● | ● | ● | ● |
| Jun 2025 | ● | ● | ● | ○ | ● | ● | ● | ● |
| Jul 2025 | ● | ● | ● | ○ | ● | ● | ● | ● |
| Aug 2025 | ● | ● | ● | ○ | ● | ● | ● | ● |
| Sep 2025 | ● | ● | ● | ● | ● | ● | ● | ● |
| Oct 2025 | ● | ● | ● |  | ● | ● | ● | ● |
| Nov 2025 | ● | ● | ● |  | ● | ● | ● | ● |
| Dec 2025 | ● | ● | ● |  | ● | ● | ● | ● |
| Jan 2026 | ○ | ○ | ● |  | ○ | ○ | ○ |  |
| Feb 2026 | ● | ● | ● |  | ● | ● | ● |  |
| Mar 2026 | ● | ● | ● |  | ○ | ○ | ● |  |
| Apr 2026 | ● | ● | ● |  | ○ | ● | ● |  |
| May 2026 | ○ | ● | ● |  | ○ | ○ | ○ |  |
| Jun 2026 | ● | ● | ● |  | ○ | ○ | ○ |  |
| Jul 2026 | ○ | ○ | ● |  | ○ | ○ | ○ |  |
| Aug 2026 | ● | ● | ● |  | ● | ● | ● |  |
| Sep 2026 | ● | ? | ? | ? | ? | ? | ? | ? |

**First and last published month of each bar** (a bar that ends before September 2026 is a "latest figure", never "retired", DEC-132):

| Bar | First | Last | Published months | Latest figure? |
|---|---|---|---|---|
| ChatGPT | Dec 2022 (265.0 m) | Sep 2026 (5.90 bn) | 37 | no |
| Gemini (Bard) | Mar 2023 (30.6 m) | Aug 2026 (2.62 bn) | 26 | yes, from Aug 2026 |
| Claude | Nov 2023 (26.0 m) | Aug 2026 (950.2 m) | 23 | yes, from Aug 2026 |
| Copilot | Sep 2024 (37.0 m) | Sep 2025 (99.6 m) | 3 | yes, from Sep 2025 |
| Perplexity | Dec 2022 (2.2 m) | Aug 2026 (95.2 m) | 20 | yes, from Aug 2026 |
| DeepSeek | Jan 2025 (277.9 m) | Aug 2026 (354.0 m) | 15 | yes, from Aug 2026 |
| Grok | Jan 2025 (1.2 m) | Aug 2026 (210.0 m) | 16 | yes, from Aug 2026 |
| Meta AI | Sep 2024 (7.8 m) | Dec 2025 (21.6 m) | 13 | yes, from Dec 2025 |

**Warning:** in Sep 2026 fewer than three bars have a verified figure (only ChatGPT). The other sites' September 2026 website profiles are not yet read (Similarweb's free search limit, V85); Cowork reads them on a fresh day (DEC-515). Until then no bar is extended past its last published month.

## 2. Changes of first, second and third place

Ranked on live bars each month (a bar whose figures have ended is not counted here). "Published" = both bars have a published figure that month; otherwise the crossing falls on a straight line and its exact month is not a dated fact.

| Month | Place | New holder | Previous holder | Kind | On published months? |
|---|---|---|---|---|---|
| Dec 2022 | 1 | ChatGPT (published) | — (—) | first holder | yes |
| Dec 2022 | 2 | Perplexity (published) | — (—) | first holder | yes |
| Mar 2023 | 2 | Gemini (Bard) (published) | Perplexity (interpolated) | overtake | no |
| Mar 2023 | 3 | Perplexity (interpolated) | — (—) | first holder | no |
| Jan 2025 | 2 | DeepSeek (published) | Gemini (Bard) (published) | overtake | yes |
| Jan 2025 | 3 | Gemini (Bard) (published) | Perplexity (published) | overtake | yes |
| May 2025 | 2 | Gemini (Bard) (published) | DeepSeek (published) | overtake | yes |
| May 2025 | 3 | DeepSeek (published) | Gemini (Bard) (published) | overtake | yes |
| Feb 2026 | 3 | Grok (published) | DeepSeek (published) | overtake | yes |
| Mar 2026 | 3 | Claude (published) | Grok (published) | overtake | yes |

Copilot (site open from 15 Nov 2023) and Meta AI (from 18 Apr 2024) join only in September 2024, their first published figures; Claude (from 11 Jul 2023) joins in November 2023. Before that their absence is missing figures, not zero visits.

## 3. Conflicts: what Luke's rule settles, what is pending, what is left over

Rule (DEC-502 (2), DEC-517): Similarweb's current data version (published on or after 28 Jul 2024) over the older one; then Similarweb's own publication over press quoting it; then final over preliminary; then the later publication over the earlier. then (step 5, Claude's proposal approved by Luke, DEC-528) within one publication, its labelled month-by-month chart or table over a figure in its prose. Never averaged. Applied to VERIFIED, eligible figures only; the same rule over every version (verified or not) shows what would change once the rest is checked. Versions that are the same number printed at a coarser precision (rounded or cut, e.g. 2.6 billion and 2.595B) agree and are not conflicts; agreement is tested between every pair (DEC-523).

| Case | Bar, month | Status | Used | Rule on verified figures | If every version were verified | Versions |
|---|---|---|---|---|---|---|
| C01 | ChatGPT, Dec 2022 | SETTLED | B003 265.0 m | settled: step 5: within one publication, its labelled chart over its prose (DEC-528) | B003 265M | B005 S23_BILLION 266 million [S, older, final, VERIFIED] ; B002 S23_APRIL about 266 million [S, older, final, VERIFIED] ; B003 S23_BDAY 265M [S, older, final, VERIFIED] ; B004 S23_BDAY 266 million [S, older, final, VERIFIED] ; B001 DIGI_2023 266 million [P, older, final, VERIFIED] |
| C02 | ChatGPT, Jan 2023 | SETTLED | M068 615.0 m | settled: step 5: within one publication, its labelled chart over its prose (DEC-528) | M068 615M | M046 S23_BILLION 616 million [S, older, final, VERIFIED] ; M002 S23_BDAY 617 million [S, older, final, VERIFIED] ; M068 S23_BDAY 615M [S, older, final, VERIFIED] |
| C03 | ChatGPT, Apr 2023 | SETTLED | M053 1.77 bn | settled: step 4: the later publication over the earlier (DEC-517) | M053 1.77 billion | M050 S23_APRIL about 1.76 billion [S, older, final, VERIFIED] ; M051 S23_MAY 1.76 billion [S, older, final, VERIFIED] ; M052 S23_COMEBACK nearly 1.7 billion [S, older, final, VERIFIED] ; M053 S23_BDAY 1.77 billion [S, older, final, VERIFIED] ; M070 S23_BDAY 1.77B [S, older, final, VERIFIED] |
| C04 | ChatGPT, May 2024 | SETTLED | B025 2.20 bn | agree: one figure, or every version agrees | B025 2.2 billion | B024 SW24_JUN_PROJECT 2.5 billion [S, older, final, NOT FOUND] ; B025 SW24_OCT 2.2 billion [S, current, final, VERIFIED] |
| C05 | ChatGPT, Sep 2025 | SETTLED | T2025-09-chatgpt 5.90 bn | settled: step 4: the later publication over the earlier (DEC-517) | T2025-09-chatgpt 5,904,115,522 | B041 S25_CARR_SEP 5.6 billion [S, current, final, VERIFIED] ; B040 P25_DIGI 5.9 billion [P, current, final, VERIFIED] ; T2025-09-chatgpt S25_TABLE 5,904,115,522 [S, current, final, VERIFIED] |
| C06 | ChatGPT, Oct 2025 | SETTLED | T2025-10-chatgpt 6.17 bn | agree: one figure, or every version agrees | T2025-10-chatgpt 6,165,610,531 | M008 S25_CARR_OCT topped 6 billion [S, current, final, VERIFIED] ; M009 S25_CARR_OCT 6.2M [S, current, final, VERIFIED, not eligible: Unit inconsistent within its post] ; T2025-10-chatgpt S25_TABLE 6,165,610,531 [S, current, final, VERIFIED] ; M011 Q26_IPO_PDF 6.17B [S, current, final, VERIFIED] |
| C07 | ChatGPT, Sep 2026 | SETTLED | B068 5.90 bn | agree: one figure, or every version agrees | B068 5.9B | B068 S26_GPT 5.9B [S, current, final, VERIFIED] ; B069 S26_GPT_OLD 34.4M [S, current, final, UNVERIFIED, not eligible: address chat.openai.com is not the bar's address] |
| C08 | Claude, Feb 2026 | SETTLED | M018 290.3 m | agree: one figure, or every version agrees | M018 290.3M | M018 Q26_FEB_NEWS 290.3M [S, current, final, VERIFIED] ; M023 Q26_DECODER 290.3 million [P, current, final, VERIFIED] ; M019 Q26_IPO_PDF 290M [S, current, final, VERIFIED] ; M017 Q26_IPO_BLOG 203 million [S, current, final, VERIFIED, not eligible: January's figure under February's name: Similarweb's own dated February table shows claude.ai 290.3M] |
| C09 | Claude, May 2026 | SETTLED | M075 952.6 m | settled: step 4: the later publication over the earlier (DEC-517) | M075 952.6M | M030 Q26_JUNE_NEWS 952.5M [S, current, final, VERIFIED] ; M031 Q26_CLAUDE_COMPARE 953 million [S, current, final, VERIFIED] ; M032 Q26_IPO_PDF 953M [S, current, final, VERIFIED] ; M075 Q26_SEP_NEWS 952.6M [S, current, final, VERIFIED] |
| C10 | Claude, Jun 2026 | SETTLED | M076 946.8 m | settled: step 4: the later publication over the earlier (DEC-517) | M076 946.8M | B064 Q26_JUNE_NEWS 946.7M [S, current, final, VERIFIED] ; B065 Q26_JUNE_NEWS 946.8M [S, current, final, VERIFIED] ; M076 Q26_SEP_NEWS 946.8M [S, current, final, VERIFIED] |
| C11 | DeepSeek, Dec 2025 | SETTLED | T2025-12-deepseek 328.9 m | agree: one figure, or every version agrees | T2025-12-deepseek 328,865,716 | M014 P25_ET_DEC 282 million [P, current, final, VERIFIED, not eligible: DeepSeek press figure without a stated address] ; T2025-12-deepseek S25_TABLE 328,865,716 [S, current, final, VERIFIED] |
| C12 | DeepSeek, Feb 2026 | SETTLED | B059 273.2 m | agree: one figure, or every version agrees | B059 273.2M | B059 Q26_FEB_NEWS 273.2M [S, current, final, VERIFIED] ; M024 Q26_DECODER 246.4 million [P, current, final, VERIFIED, not eligible: DeepSeek press figure without a stated address] |
| C13 | DeepSeek, Sep 2026 | PENDING verification (no verified figure; straight line across) |  — | no verified eligible figure | B075 357.4M | B075 S26_DS 357.4M [S, current, final, UNVERIFIED] ; B076 S26_DS_CHAT 313.1M [S, current, final, UNVERIFIED, not eligible: address chat.deepseek.com is not the bar's address] |
| C14 | Gemini (Bard), Oct 2025 | SETTLED | T2025-10-gemini 1.18 bn | agree: one figure, or every version agrees | T2025-10-gemini 1,182,055,658 | M010 S25_CARR_OCT 1.2M [S, current, final, VERIFIED, not eligible: Unit inconsistent within its post] ; T2025-10-gemini S25_TABLE 1,182,055,658 [S, current, final, VERIFIED] |
| C15 | Gemini (Bard), Sep 2026 | PENDING verification (no verified figure; straight line across) |  — | no verified eligible figure | B071 2.6B | B070 S26_BARD 549K [S, current, final, UNVERIFIED, not eligible: address bard.google.com is not the bar's address] ; B071 S26_GEM 2.6B [S, current, final, UNVERIFIED] |
| C16 | Grok, Jul 2025 | SETTLED | T2025-07-grok 201.5 m | agree: one figure, or every version agrees | T2025-07-grok 201,518,109 | M006 S25_MONTHLY 201M [S, current, final, VERIFIED] ; M007 S25_MONTHLY 38K [S, current, final, VERIFIED, not eligible: Contradicted by the same page: its prose gives Grok 201M for July 2025, as does Similarweb's 2025 table; the 38K table cell is set aside] ; T2025-07-grok S25_TABLE 201,518,109 [S, current, final, VERIFIED] |
| C17 | Grok, Dec 2025 | SETTLED | T2025-12-grok 271.2 m | settled: step 2: Similarweb's own publication over press | T2025-12-grok 271,154,744 | M013 P25_ET_DEC 247 million [P, current, final, VERIFIED] ; T2025-12-grok S25_TABLE 271,154,744 [S, current, final, VERIFIED] |
| C18 | Perplexity, Dec 2025 | SETTLED | T2025-12-perplexity 179.6 m | settled: step 2: Similarweb's own publication over press | T2025-12-perplexity 179,583,644 | M012 P25_ET_DEC 154.9 million [P, current, final, VERIFIED] ; T2025-12-perplexity S25_TABLE 179,583,644 [S, current, final, VERIFIED] |

**The cases named in the briefs:**

- **ChatGPT, May 2024:** 2.2 billion (Nov 2024 post, current version, VERIFIED) is used. The June 2024 post's "2.5 billion" is NOT FOUND (V54: no printed figure, chart without labels); it would lose at step 1 anyway.
- **DeepSeek, February 2026:** Similarweb's own 273.2M for deepseek.com (February table, VERIFIED V62) is used. The Decoder's 246.4 million names no address, so it does not count for DeepSeek (DEC-507).
- **Claude, February and January 2026:** February = 290.3M (Similarweb's dated February table, +43.07% month on month, V61; The Decoder and the IPO report's 290M agree; DEC-516). The IPO blog's "203 million" for February is set aside as January's figure (DEC-525); January 2026 = 203M from the IPO report, "between January and April 2026 (203M to 824M visits a month)" (V86).
- **ChatGPT, December 2022 and January 2023:** the birthday post prints 265M and 615M in its infographic and "266 million" and "617 million" in its text (the March 2023 post says 616 million for January). Step 4 keeps the birthday post (the latest); step 5 (DEC-528) picks its infographic.
- **Small differences:** Claude May 2026 952.6M (Sep newsletter, later) over 952.5M (Jul newsletter image); Claude June 2026 946.8M (Sep newsletter) over the July image's 946.7M; ChatGPT September 2025 Similarweb's 2025 table (5,904,115,522, Jan 2026) over Carr's 5.6 billion (Oct 2025), all by step 4; Perplexity December 2023: Reuters' 45.6 million and 45 million agree (45.6 cut to 45), so the more precise one is used.
- **Bard, April and May 2023, ChatGPT July 2023:** "visitors" in Similarweb's text, used as visits (DEC-518).
- **Copilot, September 2024:** only Digiday's 37 million (press quoting Similarweb, VERIFIED V25) exists and is used. It fits Similarweb's own October post ("growth of 87.6% MoM to 69.4 million"). Copilot and Meta AI are not in the IPO report, so their last figures stay September 2025 and December 2025 until the September 2026 profiles are read.
- **July 2026:** no figure for ChatGPT or Gemini is printed in anything checked; the line runs from June to August. Nothing is derived from percentage changes or from the IPO report's quarter-to-date sums.

## 4. Long straight lines that may look like a sudden turn

Points where the line's slope reverses or changes at least threefold, with at least one side spanning three months or more (a design-session item: the motion must look smooth, DEC-502 (1)).

| Bar | At | Months before / after | Visits per month before → after | Why | Crosses the data-version change? |
|---|---|---|---|---|---|
| ChatGPT | Feb 2024 | 3 / 1 | 23.3 m down → 170.0 m up | direction reverses | no |
| Gemini (Bard) | May 2023 | 1 / 4 | 92.9 m up → 19.2 m up | slows sharply | no |
| Gemini (Bard) | Mar 2024 | 4 / 6 | 41.6 m up → 31.0 m down | direction reverses | yes |
| Gemini (Bard) | Sep 2024 | 6 / 1 | 31.0 m down → 44.3 m up | direction reverses | yes |
| Gemini (Bard) | Oct 2024 | 1 / 3 | 44.3 m up → 8.0 m down | direction reverses | no |
| Gemini (Bard) | Jan 2025 | 3 / 1 | 8.0 m down → 16.4 m up | direction reverses | no |
| Claude | Sep 2024 | 10 / 1 | 4.4 m up → 13.7 m up | speeds up sharply | yes |
| Claude | Oct 2024 | 1 / 3 | 13.7 m up → 2.4 m down | direction reverses | no |
| Copilot | Oct 2024 | 1 / 11 | 32.4 m up → 2.7 m up | slows sharply | no |
| Perplexity | Apr 2024 | 1 / 5 | 9.0 m up → 360,000 up | slows sharply | yes |
| Perplexity | Sep 2024 | 5 / 1 | 360,000 up → 18.5 m up | speeds up sharply | yes |
| Perplexity | Oct 2024 | 1 / 3 | 18.5 m up → 2.9 m up | slows sharply | no |
| Perplexity | Jan 2025 | 3 / 1 | 2.9 m up → 10.9 m up | speeds up sharply | no |
| DeepSeek | Apr 2026 | 2 / 4 | 68.9 m up → 14.2 m down | direction reverses | no |
| Meta AI | Jan 2025 | 4 / 1 | 52,266 up → 845,349 down | direction reverses | no |

**Gaps of four months or more between published figures:** ChatGPT May 2024 → Sep 2024 (4 months); Gemini (Bard) May 2023 → Sep 2023 (4 months); Gemini (Bard) Nov 2023 → Mar 2024 (4 months); Gemini (Bard) Mar 2024 → Sep 2024 (6 months); Claude Nov 2023 → Sep 2024 (10 months); Copilot Oct 2024 → Sep 2025 (11 months); Perplexity Dec 2022 → Dec 2023 (12 months); Perplexity Apr 2024 → Sep 2024 (5 months); Perplexity Feb 2026 → Aug 2026 (6 months); DeepSeek Apr 2026 → Aug 2026 (4 months); Grok Apr 2026 → Aug 2026 (4 months); Meta AI Sep 2024 → Jan 2025 (4 months).

**The data-version change (28 Jul 2024):** Gemini goes from 433.5 million (March 2024, older version) to 247.3 million (September 2024, current version). The straight line shows a 43% fall that may be partly or wholly Similarweb's re-estimate, not real; the same applies, less visibly, to every bar that crosses mid-2024. Similarweb's own current-version posts restate ChatGPT's 2023 peak as "1.9 billion" (Oct 2024 post, month not stated) against 1.8 billion in the older version. Luke keeps the published figures, with the older-estimate note at the revision, checked in the design session (DEC-522).

## 5. UNVERIFIED figures for Cowork to check in Luke's Chrome

Checked so far: Cowork in Luke's Chrome (V01–V101, 7–8 Oct; the IPO report PDF opened with Luke's OK) and runner round R1 (https://github.com/marketmarathon/race-through-time/actions/runs/37790576703; 28 of 41 pages; LinkedIn closed to it by robots.txt). Still to check, highest value first (NOT FOUND figures are listed below the table):

| # | Figure | Month | Publication | URL | Why it matters |
|---|---|---|---|---|---|
| 1 | Claude 1B | Sep 2026 | S26_CLAUDE | https://www.similarweb.com/website/claude.ai/ | fills a month with no verified figure |
| 2 | Copilot 64.4M | Sep 2026 | S26_COPILOT | https://www.similarweb.com/website/copilot.microsoft.com/ | fills a month with no verified figure |
| 3 | DeepSeek 357.4M | Sep 2026 | S26_DS | https://www.similarweb.com/website/deepseek.com/ | fills a month with no verified figure |
| 4 | Gemini (Bard) 2.6B | Sep 2026 | S26_GEM | https://www.similarweb.com/website/gemini.google.com/ | fills a month with no verified figure |
| 5 | Grok 205.5M | Sep 2026 | S26_GROK | https://www.similarweb.com/website/grok.com/ | fills a month with no verified figure |
| 6 | Meta AI 34.4M | Sep 2026 | S26_META | https://www.similarweb.com/website/meta.ai/ | fills a month with no verified figure |
| 7 | Perplexity 91.7M | Sep 2026 | S26_PERP | https://www.similarweb.com/website/perplexity.ai/ | fills a month with no verified figure |

Read the September 2026 profiles as **that month's** figure ("last month" tooltip, dossier F12). NOT FOUND after checking: ChatGPT May 2024 2.5 billion (SW24_JUN_PROJECT, Cowork in Luke's Chrome (8 Oct, IQ-17b): no printed 2.5 billion; chart without labels).

## 6. Publications not yet mined for every month (owner decision: every published month)

Known to hold months not yet recorded (a later research round, or Cowork, could add them):

- **Q26_IPO_PDF**, Exhibit 3 (p13): rows for January and June 2026 for claude.ai (not recorded with their wording; both months are covered by other figures); its charts for other sites carry no labels.
- **Q26_FEB_NEWS** (Similarweb newsletter, 12 Mar 2026): its ranking images may list chatgpt.com, gemini.google.com and others for February 2026 (only claude.ai and deepseek.com recorded).
- **SW24_JUL** (Jul 2024) and **S24_CUSTOM** (Jan 2024): bars and graphs without printed labels (never read off a bar's height).
- **Similarweb's free profiles**: show only the latest month; Copilot and Meta AI have no figure after September 2025 and December 2025 except there.

## 7. Press credits (description)

Press articles whose figures reach a bar (DEC-244 credits Similarweb on screen and in the description; these are credited in the description too):

- **Digiday**, 2023-12-01 (https://digiday.com/media-buying/chatgpt-turns-a-year-old-marking-a-major-milestone-for-generative-ai/): ChatGPT Nov 2023 1.67 billion; Claude Nov 2023 26 million; Gemini (Bard) Nov 2023 267 million.
- **Reuters / Investing.com syndication**, 2024-01-04 (https://www.investing.com/news/stock-market-news/search-startup-perplexity-ai-valued-at-520-million-in-funding-from-bezos-nvidia-3267562): Perplexity Dec 2022 2.2 million.
- **Reuters**, 2024-02-26 (https://www.reuters.com/technology/sk-telecom-partners-with-ai-search-startup-perplexity-korea-2024-02-26/): Perplexity Dec 2023 45.6 million.
- **Digiday**, 2025-10-20 (https://digiday.com/media/in-graphic-detail-how-ai-search-is-changing-publisher-visibility/): Claude Sep 2024 70.4 million; Copilot Sep 2024 37 million; Meta AI Sep 2024 7.8 million; Perplexity Sep 2024 72.3 million; Copilot Sep 2025 99.6 million.
- **The Decoder**, 2026-03-12 (https://the-decoder.com/chatgpt-still-leads-the-chatbot-market-but-its-dominance-is-slipping-as-googles-gemini-gains-ground/): ChatGPT Feb 2026 5.35 billion; Gemini (Bard) Feb 2026 2.11 billion; Grok Feb 2026 298.5 million; Perplexity Feb 2026 153.8 million.

## 8. Checks

- **K01 PASS** Every on-screen value rests on a VERIFIED figure with its URL and the wording seen at source. 153 points used; problems: none
- **K02 PASS** No averaging: each published month shows one printed figure exactly; each other month is the straight line between its two points. 236 series rows; mismatches: none; used values not printed: none
- **K03 PASS** No point or bar before the site's start date. problems: none
- **K04 PASS** One address per assistant per month. problems: none
- **K05 PASS** DeepSeek: deepseek.com only; never deepseek.com + chat.deepseek.com. 15 DeepSeek points used; problems: none
- **K06 PASS** No forecast: projections (Similarweb's June 2024 and October 2023 projections) are never used. projection rows ['M040', 'M062'], all excluded
- **K07 PASS** data_version set on every point and every series row. problems: none
- **K08 PASS** No extrapolation beyond a bar's first or last published point. problems: none
- **K09 PASS** Only eligible VERIFIED figures are used; UNVERIFIED and NOT FOUND never. problems: none
- **K10 PASS** Leftover conflicts use no figure until Luke decides. 0 leftovers; problems: none
- **K11 PASS** Le Chat and uncounted sites (Bing Chat in bing.com, Grok in x.com) have no bar. none on the board

Tests: `python3 tests/rtt102/run_tests_rtt102.py` (rebuilds twice into empty folders and compares every byte, then re-checks the rules independently).

## 9. Questions for Luke

All answered "as recommended" (8 Oct 2026): the first eight as DEC-515 to DEC-522; the three IQ-17b questions as DEC-528 (step 5: within one publication, its labelled chart beats its text), DEC-529 (Perplexity from December 2022 at 2.2 million) and DEC-530 (if the September 2026 profiles cannot be read, the race ends in August 2026, with Copilot and Meta AI as "latest figure"). No question is open. Next: Cowork reads the seven September 2026 profiles (9 Oct), then a small rebuild.
