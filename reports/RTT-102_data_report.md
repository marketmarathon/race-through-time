# RTT-102 AI assistant websites race: data report (phase 1, IQ-17)

Built by `python3 scripts/build_rtt102_dataset.py data/rtt-102 reports/RTT-102_data_report.md` (deterministic). Method: `reference/metric_contract_RTT-102.md`. Decisions DEC-500 to DEC-514. **Data only: nothing designed or rendered (DEC-069).**

**What the race shows:** Similarweb's published estimates of monthly website visits, worldwide, to eight AI assistant websites, December 2022 to September 2026. Not market share and not users. Every bar value rests on a figure seen at its source (Cowork in Luke's Chrome, or a GitHub runner reading the page); straight lines join published months.

**In numbers:** 233 figure rows from 52 publications; 183 VERIFIED, 50 UNVERIFIED. 137 points used on bars (125 from Similarweb's own publications, 12 from press quoting Similarweb). 203 bar-months, of which 137 published and 66 on straight lines. Checks: 11/11 PASS.

## 1. Coverage grid (assistant × month)

`●` published and used · `○` straight line between two published months · `?` an UNVERIFIED figure exists but no verified one (on Cowork's list) · `!` leftover conflict for Luke · blank: no bar. Bars appear from their first published month; none is extended past its last.

| Month | ChatGPT | Gemini (Bard) | Claude | Copilot | Perplexity | DeepSeek | Grok | Meta AI |
|---|---|---|---|---|---|---|---|---|
| Dec 2022 | ● |  |  |  | ? |  |  |  |
| Jan 2023 | ! |  |  |  |  |  |  |  |
| Feb 2023 | ● |  |  |  |  |  |  |  |
| Mar 2023 | ● | ● |  |  |  |  |  |  |
| Apr 2023 | ! | ● |  |  |  |  |  |  |
| May 2023 | ● | ● |  |  |  |  |  |  |
| Jun 2023 | ● | ○ |  |  |  |  |  |  |
| Jul 2023 | ● | ○ |  |  |  |  |  |  |
| Aug 2023 | ● | ○ |  |  |  |  |  |  |
| Sep 2023 | ● | ● |  |  |  |  |  |  |
| Oct 2023 | ● | ○ |  |  |  |  |  |  |
| Nov 2023 | ● | ● | ● |  |  |  |  |  |
| Dec 2023 | ○ | ○ | ○ |  | ? |  |  |  |
| Jan 2024 | ○ | ○ | ○ |  |  |  |  |  |
| Feb 2024 | ● | ○ | ○ |  |  |  |  |  |
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
| Jan 2026 | ○ | ○ | ?○ |  | ○ | ○ | ○ |  |
| Feb 2026 | ● | ● | ● |  | ● | ?○ | ● |  |
| Mar 2026 | ● | ● | ● |  |  | ○ | ?○ |  |
| Apr 2026 | ○ | ● | ● |  |  | ● | ● |  |
| May 2026 | ○ | ?○ | ● |  |  |  |  |  |
| Jun 2026 | ● | ● | ● |  |  |  |  |  |
| Jul 2026 | ○ |  |  |  |  |  |  |  |
| Aug 2026 | ○ |  |  |  |  |  |  |  |
| Sep 2026 | ● | ? | ? | ? | ? | ? | ? | ? |

**First and last published month of each bar** (a bar that ends before September 2026 is a "latest figure", never "retired", DEC-132):

| Bar | First | Last | Published months | Latest figure? |
|---|---|---|---|---|
| ChatGPT | Dec 2022 (266.0 m) | Sep 2026 (5.90 bn) | 33 | no |
| Gemini (Bard) | Mar 2023 (30.6 m) | Jun 2026 (2.86 bn) | 24 | yes, from Jun 2026 |
| Claude | Nov 2023 (26.0 m) | Jun 2026 (946.8 m) | 20 | yes, from Jun 2026 |
| Copilot | Sep 2024 (37.0 m) | Sep 2025 (99.6 m) | 3 | yes, from Sep 2025 |
| Perplexity | Mar 2024 (61.5 m) | Feb 2026 (153.8 m) | 17 | yes, from Feb 2026 |
| DeepSeek | Jan 2025 (277.9 m) | Apr 2026 (411.0 m) | 13 | yes, from Apr 2026 |
| Grok | Jan 2025 (1.2 m) | Apr 2026 (279.0 m) | 14 | yes, from Apr 2026 |
| Meta AI | Sep 2024 (7.8 m) | Dec 2025 (21.6 m) | 13 | yes, from Dec 2025 |

**Warning:** after June 2026 only ChatGPT has a verified figure, so Jul 2026, Aug 2026, Sep 2026 show fewer than three live bars. The September 2026 website profiles of the other sites are UNVERIFIED (Similarweb's free search limit, V42); see question 1.

## 2. Changes of first, second and third place

Ranked on live bars each month (a bar whose figures have ended is not counted here). "Published" = both bars have a published figure that month; otherwise the crossing falls on a straight line and its exact month is not a dated fact.

| Month | Place | New holder | Previous holder | Kind | On published months? |
|---|---|---|---|---|---|
| Dec 2022 | 1 | ChatGPT (published) | — (—) | first holder | yes |
| Mar 2023 | 2 | Gemini (Bard) (published) | — (—) | first holder | yes |
| Nov 2023 | 3 | Claude (published) | — (—) | first holder | yes |
| Mar 2024 | 3 | Perplexity (published) | Claude (interpolated) | overtake | no |
| Jan 2025 | 2 | DeepSeek (published) | Gemini (Bard) (published) | overtake | yes |
| Jan 2025 | 3 | Gemini (Bard) (published) | Perplexity (published) | overtake | yes |
| May 2025 | 2 | Gemini (Bard) (published) | DeepSeek (published) | overtake | yes |
| May 2025 | 3 | DeepSeek (published) | Gemini (Bard) (published) | overtake | yes |
| Mar 2026 | 3 | Claude (published) | DeepSeek (interpolated) | overtake | no |

Before March 2024 the board holds only two or three bars because Perplexity, Copilot and the others have no verified figure yet (Perplexity existed from December 2022). Claude's "third place" from November 2023 to February 2024 is therefore an artefact of missing figures, not a result; Reuters' 45 million for Perplexity in December 2023 (UNVERIFIED) would put Perplexity ahead of Claude's 26 million.

## 3. Conflicts: what Luke's rule settles, what is pending, what is left over

Rule (DEC-502 (2)): Similarweb's current data version (published on or after 28 Jul 2024) over the older one; then Similarweb's own publication over press quoting it; then final over preliminary. Never averaged. Applied to VERIFIED, eligible figures only; the same rule over every version (verified or not) shows what would happen once Cowork checks the rest. Versions that are the same figure printed at different precision (e.g. 2.6 billion and 2.595B) agree and are not conflicts (DEC-508).

| Case | Bar, month | Status | Used | Rule on verified figures | If every version were verified | Versions |
|---|---|---|---|---|---|---|
| C01 | ChatGPT, Dec 2022 | PENDING verification (an unverified version would contest or replace the figure used) | B005 266.0 m | agree: one figure, or every version agrees | leftover | B005 S23_BILLION 266 million [S, older, final, VERIFIED] ; B002 S23_APRIL about 266 million [S, older, final, VERIFIED] ; B003 S23_BDAY 265M [S, older, final, UNVERIFIED] ; B004 S23_BDAY 266 million [S, older, final, VERIFIED] ; B001 DIGI_2023 266 million [P, older, final, VERIFIED] |
| C02 | ChatGPT, Jan 2023 | LEFTOVER for Luke (no figure used; straight line across) |  — | leftover: unresolved after the three steps | leftover | M046 S23_BILLION 616 million [S, older, final, VERIFIED] ; M002 S23_BDAY 617 million [S, older, final, VERIFIED] |
| C03 | ChatGPT, Apr 2023 | LEFTOVER for Luke (no figure used; straight line across) |  — | leftover: unresolved after the three steps | leftover | M050 S23_APRIL about 1.76 billion [S, older, final, VERIFIED] ; M051 S23_MAY 1.76 billion [S, older, final, VERIFIED] ; M052 S23_COMEBACK nearly 1.7 billion [S, older, final, VERIFIED] ; M053 S23_BDAY 1.77 billion [S, older, final, VERIFIED] |
| C04 | ChatGPT, May 2024 | SETTLED | B025 2.20 bn | agree: one figure, or every version agrees | B025 2.2 billion | B024 SW24_JUN_PROJECT 2.5 billion [S, older, final, UNVERIFIED] ; B025 SW24_OCT 2.2 billion [S, current, final, VERIFIED] |
| C05 | ChatGPT, Sep 2025 | PENDING verification (an unverified version would contest or replace the figure used) | T2025-09-chatgpt 5.90 bn | agree: one figure, or every version agrees | leftover | B041 S25_CARR_SEP 5.6 billion [S, current, final, UNVERIFIED] ; B040 P25_DIGI 5.9 billion [P, current, final, VERIFIED] ; T2025-09-chatgpt S25_TABLE 5,904,115,522 [S, current, final, VERIFIED] |
| C06 | ChatGPT, Oct 2025 | SETTLED | T2025-10-chatgpt 6.17 bn | agree: one figure, or every version agrees | T2025-10-chatgpt 6,165,610,531 | M008 S25_CARR_OCT topped 6 billion [S, current, final, UNVERIFIED] ; M009 S25_CARR_OCT 6.2M [S, current, final, UNVERIFIED, not eligible: Unit inconsistent within its post] ; T2025-10-chatgpt S25_TABLE 6,165,610,531 [S, current, final, VERIFIED] ; M011 Q26_IPO_PDF 6.17B [S, current, final, UNVERIFIED] |
| C07 | ChatGPT, Sep 2026 | SETTLED | B068 5.90 bn | agree: one figure, or every version agrees | B068 5.9B | B068 S26_GPT 5.9B [S, current, final, VERIFIED] ; B069 S26_GPT_OLD 34.4M [S, current, final, UNVERIFIED, not eligible: address chat.openai.com is not the bar's address] |
| C08 | Claude, Feb 2026 | PENDING verification (an unverified version would contest or replace the figure used) | M017 203.0 m | settled: step 2: Similarweb's own publication over press | leftover | M018 Q26_FEB_NEWS 290.3M [S, current, final, UNVERIFIED] ; M023 Q26_DECODER 290.3 million [P, current, final, VERIFIED] ; M019 Q26_IPO_PDF 290M [S, current, final, UNVERIFIED] ; M017 Q26_IPO_BLOG 203 million [S, current, final, VERIFIED] |
| C09 | Claude, Jun 2026 | PENDING verification (an unverified version would contest or replace the figure used) | B065 946.8 m | agree: one figure, or every version agrees | leftover | B064 Q26_JUNE_NEWS 946.7M [S, current, final, UNVERIFIED] ; B065 Q26_JUNE_NEWS 946.8M [S, current, final, VERIFIED] |
| C10 | DeepSeek, Dec 2025 | SETTLED | T2025-12-deepseek 328.9 m | agree: one figure, or every version agrees | T2025-12-deepseek 328,865,716 | M014 P25_ET_DEC 282 million [P, current, final, VERIFIED, not eligible: DeepSeek press figure without a stated address] ; T2025-12-deepseek S25_TABLE 328,865,716 [S, current, final, VERIFIED] |
| C11 | DeepSeek, Feb 2026 | PENDING verification (no verified figure; straight line across) |  — | no verified eligible figure | B059 273.2M | B059 Q26_FEB_NEWS 273.2M [S, current, final, UNVERIFIED] ; M024 Q26_DECODER 246.4 million [P, current, final, VERIFIED, not eligible: DeepSeek press figure without a stated address] |
| C12 | DeepSeek, Sep 2026 | PENDING verification (no verified figure; straight line across) |  — | no verified eligible figure | B075 357.4M | B075 S26_DS 357.4M [S, current, final, UNVERIFIED] ; B076 S26_DS_CHAT 313.1M [S, current, final, UNVERIFIED, not eligible: address chat.deepseek.com is not the bar's address] |
| C13 | Gemini (Bard), Oct 2025 | SETTLED | T2025-10-gemini 1.18 bn | agree: one figure, or every version agrees | T2025-10-gemini 1,182,055,658 | M010 S25_CARR_OCT 1.2M [S, current, final, UNVERIFIED, not eligible: Unit inconsistent within its post] ; T2025-10-gemini S25_TABLE 1,182,055,658 [S, current, final, VERIFIED] |
| C14 | Gemini (Bard), Sep 2026 | PENDING verification (no verified figure; straight line across) |  — | no verified eligible figure | B071 2.6B | B070 S26_BARD 549K [S, current, final, UNVERIFIED, not eligible: address bard.google.com is not the bar's address] ; B071 S26_GEM 2.6B [S, current, final, UNVERIFIED] |
| C15 | Grok, Jul 2025 | SETTLED | T2025-07-grok 201.5 m | agree: one figure, or every version agrees | T2025-07-grok 201,518,109 | M006 S25_MONTHLY 201M [S, current, final, VERIFIED] ; M007 S25_MONTHLY 38K [S, current, final, VERIFIED, not eligible: Contradicted by the same page: its prose gives Grok 201M for July 2025, as does Similarweb's 2025 table; the 38K table cell is set aside] ; T2025-07-grok S25_TABLE 201,518,109 [S, current, final, VERIFIED] |
| C16 | Grok, Dec 2025 | SETTLED | T2025-12-grok 271.2 m | settled: step 2: Similarweb's own publication over press | T2025-12-grok 271,154,744 | M013 P25_ET_DEC 247 million [P, current, final, VERIFIED] ; T2025-12-grok S25_TABLE 271,154,744 [S, current, final, VERIFIED] |
| C17 | Perplexity, Dec 2025 | SETTLED | T2025-12-perplexity 179.6 m | settled: step 2: Similarweb's own publication over press | T2025-12-perplexity 179,583,644 | M012 P25_ET_DEC 154.9 million [P, current, final, VERIFIED] ; T2025-12-perplexity S25_TABLE 179,583,644 [S, current, final, VERIFIED] |

**The four known cases in the brief:**

- **ChatGPT, May 2024:** 2.2 billion (Nov 2024 post, current version, VERIFIED V07 and runner) is used; 2.5 billion (Jun 2024 post, older version, UNVERIFIED: the runner read the page but the figure is not in its text) loses at step 1 even if verified.
- **DeepSeek, February 2026:** Similarweb's own 273.2M for deepseek.com (Feb newsletter image, UNVERIFIED) against The Decoder's 246.4 million (VERIFIED, but no address stated). The press figure is not used for DeepSeek because DeepSeek has two Similarweb addresses (DEC-507); until Cowork reads 273.2M, February 2026 is a straight line from December 2025 to April 2026. If 273.2M is verified it is used (step 2 would pick it anyway).
- **Bard, May 2023 (and April 2023):** the same Similarweb post calls 142.6 million both "visits" and "visitors" (and April's 49.7 million "visitors"). Used as visits (DEC-510): the post's own "up 187.2% from April" is stated for visits, and a unique-visitor count that size would imply over a billion visits, against 219.3 million visits in September 2023. Question 4.
- **Copilot, September 2024:** only Digiday's 37 million (press quoting Similarweb, VERIFIED V25) exists, so it is used (no conflict). It fits Similarweb's own October post ("growth of 87.6% MoM to 69.4 million"). Copilot's bar rests on three verified figures in all (Sep 2024, Oct 2024, Sep 2025).

## 4. Long straight lines that may look like a sudden turn

Points where the line's slope reverses or changes at least threefold, with at least one side spanning three months or more (a design-session item: the motion must look smooth, DEC-502 (1)).

| Bar | At | Months before / after | Visits per month before → after | Why | Crosses the data-version change? |
|---|---|---|---|---|---|
| ChatGPT | Feb 2024 | 3 / 1 | 23.3 m down → 170.0 m up | direction reverses | no |
| ChatGPT | Mar 2026 | 1 / 3 | 350.0 m up → 106.0 m down | direction reverses | no |
| ChatGPT | Jun 2026 | 3 / 3 | 106.0 m down → 172.7 m up | direction reverses | no |
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
| DeepSeek | Dec 2025 | 1 / 4 | 16.8 m down → 20.5 m up | direction reverses | no |
| Meta AI | Jan 2025 | 4 / 1 | 52,266 up → 845,349 down | direction reverses | no |

**Gaps of four months or more between published figures:** ChatGPT May 2024 → Sep 2024 (4 months); Gemini (Bard) May 2023 → Sep 2023 (4 months); Gemini (Bard) Nov 2023 → Mar 2024 (4 months); Gemini (Bard) Mar 2024 → Sep 2024 (6 months); Claude Nov 2023 → Sep 2024 (10 months); Copilot Oct 2024 → Sep 2025 (11 months); Perplexity Apr 2024 → Sep 2024 (5 months); DeepSeek Dec 2025 → Apr 2026 (4 months); Meta AI Sep 2024 → Jan 2025 (4 months).

**The data-version change (28 Jul 2024):** Gemini goes from 433.5 million (March 2024, older version) to 247.3 million (September 2024, current version). The straight line shows a 43% fall that may be partly or wholly Similarweb's re-estimate, not real; the same applies, less visibly, to every bar that crosses mid-2024. Similarweb's own current-version posts restate ChatGPT's 2023 peak as "1.9 billion" (Oct 2024 post, month not stated) against 1.8 billion in the older version.

## 5. UNVERIFIED figures for Cowork to check in Luke's Chrome

The runner (round R1, https://github.com/marketmarathon/race-through-time/actions/runs/37790576703) fetched 28 of 41 pages; LinkedIn (11 posts and newsletters) is closed to it by LinkedIn's robots.txt, and Rest of World and Investing.com refused it (HTTP 403). Similarweb's website profiles and its IPO report (PDF) were not fetched (free search limit and robots.txt; not worked around). Highest value first:

| # | Figure | Month | Publication | URL | Why it matters |
|---|---|---|---|---|---|
| 1 | Claude 1B | Sep 2026 | S26_CLAUDE | https://www.similarweb.com/website/claude.ai/ | fills a month with no verified figure |
| 2 | Copilot 64.4M | Sep 2026 | S26_COPILOT | https://www.similarweb.com/website/copilot.microsoft.com/ | fills a month with no verified figure |
| 3 | DeepSeek 357.4M | Sep 2026 | S26_DS | https://www.similarweb.com/website/deepseek.com/ | fills a month with no verified figure |
| 4 | Gemini (Bard) 2.6B | Sep 2026 | S26_GEM | https://www.similarweb.com/website/gemini.google.com/ | fills a month with no verified figure |
| 5 | Grok 205.5M | Sep 2026 | S26_GROK | https://www.similarweb.com/website/grok.com/ | fills a month with no verified figure |
| 6 | Meta AI 34.4M | Sep 2026 | S26_META | https://www.similarweb.com/website/meta.ai/ | fills a month with no verified figure |
| 7 | Perplexity 91.7M | Sep 2026 | S26_PERP | https://www.similarweb.com/website/perplexity.ai/ | fills a month with no verified figure |
| 8 | Perplexity 2.2 million | Dec 2022 | R24_PERP_JAN | https://www.investing.com/news/stock-market-news/search-startup-perplexity-ai-valued-at-520-million-in-funding-from-bezos-nvidia-3267562 | fills a month with no verified figure |
| 9 | Perplexity 45 million | Dec 2023 | R24_PERP_JAN | https://www.investing.com/news/stock-market-news/search-startup-perplexity-ai-valued-at-520-million-in-funding-from-bezos-nvidia-3267562 | fills a month with no verified figure |
| 10 | Perplexity 45.6 million | Dec 2023 | R24_PERP_FEB | https://www.reuters.com/technology/sk-telecom-partners-with-ai-search-startup-perplexity-korea-2024-02-26/ | fills a month with no verified figure |
| 11 | Claude 203M | Jan 2026 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | fills a month with no verified figure |
| 12 | DeepSeek 273.2M | Feb 2026 | Q26_FEB_NEWS | https://www.linkedin.com/pulse/short-month-long-trends-similarweb-6iitc | fills a month with no verified figure |
| 13 | Grok 326M | Mar 2026 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | fills a month with no verified figure |
| 14 | Gemini (Bard) 2.903B | May 2026 | Q26_JUNE_NEWS | https://www.linkedin.com/pulse/did-ai-take-summer-vacation-similarweb-cukgf | fills a month with no verified figure |
| 15 | Gemini (Bard) 2.90B | May 2026 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | fills a month with no verified figure |
| 16 | ChatGPT 265M | Dec 2022 | S23_BDAY | https://www.similarweb.com/blog/insights/ai-news/chatgpt-birthday/ | would contest the figure used |
| 17 | ChatGPT 1.56B | Mar 2023 | S23_BDAY | https://www.similarweb.com/blog/insights/ai-news/chatgpt-birthday/ | confirms, or is a more precise version of, the figure used |
| 18 | ChatGPT 1.63B | Jun 2023 | S23_BDAY | https://www.similarweb.com/blog/insights/ai-news/chatgpt-birthday/ | confirms, or is a more precise version of, the figure used |
| 19 | ChatGPT 1.49B | Sep 2023 | S23_BDAY | https://www.similarweb.com/blog/insights/ai-news/chatgpt-birthday/ | confirms, or is a more precise version of, the figure used |
| 20 | ChatGPT 1.70B | Oct 2023 | S23_BDAY | https://www.similarweb.com/blog/insights/ai-news/chatgpt-birthday/ | confirms, or is a more precise version of, the figure used |
| 21 | ChatGPT 2.5 billion | May 2024 | SW24_JUN_PROJECT | https://www.similarweb.com/blog/insights/ai-news/chatgpt-beats-summer-slump/ | would contest the figure used |
| 22 | ChatGPT 3.1B | Sep 2024 | SW24_SEP | https://www.similarweb.com/blog/insights/ai-news/chatgpt-topped-3-billion-visits-in-september/ | confirms, or is a more precise version of, the figure used |
| 23 | ChatGPT 5.6 billion | Sep 2025 | S25_CARR_SEP | https://www.linkedin.com/posts/davidfcarr_googles-gemini-ai-chatbot-got-more-than-activity-7381367902047838208-PBkM | would contest the figure used |
| 24 | Gemini (Bard) 1.1 billion | Sep 2025 | S25_CARR_SEP | https://www.linkedin.com/posts/davidfcarr_googles-gemini-ai-chatbot-got-more-than-activity-7381367902047838208-PBkM | confirms, or is a more precise version of, the figure used |
| 25 | Gemini (Bard) more than 1 billion | Sep 2025 | S25_CARR_SEP | https://www.linkedin.com/posts/davidfcarr_googles-gemini-ai-chatbot-got-more-than-activity-7381367902047838208-PBkM | confirms, or is a more precise version of, the figure used |
| 26 | ChatGPT topped 6 billion | Oct 2025 | S25_CARR_OCT | https://www.linkedin.com/posts/davidfcarr_chatgpt-topped-6-billion-visits-for-the-first-activity-7391508422426316800-dpZt | confirms, or is a more precise version of, the figure used |
| 27 | ChatGPT 6.17B | Oct 2025 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | confirms, or is a more precise version of, the figure used |
| 28 | Claude 173M | Dec 2025 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | confirms, or is a more precise version of, the figure used |
| 29 | Gemini (Bard) 1.735B | Dec 2025 | S25_GEM_DEC | https://www.linkedin.com/posts/similarweb_google-gemini-in-december-2025-1735b-activity-7416454327948435456-wavH | confirms, or is a more precise version of, the figure used |
| 30 | Claude 290.3M | Feb 2026 | Q26_FEB_NEWS | https://www.linkedin.com/pulse/short-month-long-trends-similarweb-6iitc | would contest the figure used |
| 31 | Claude 290M | Feb 2026 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | would contest the figure used |
| 32 | Claude 613.7 million | Mar 2026 | Q26_APRIL_NEWS | https://www.linkedin.com/pulse/tiktoks-web-takeover-claudes-continued-surge-metas-ai-moment-n8gvc | confirms, or is a more precise version of, the figure used |
| 33 | Claude 614M | Mar 2026 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | confirms, or is a more precise version of, the figure used |
| 34 | Claude 613.7 million | Mar 2026 | Q26_MARCH_NEWS | https://www.linkedin.com/pulse/claude-gemini-apple-middle-east-conflict-reshuffled-news-prediction-bewhf | confirms, or is a more precise version of, the figure used |
| 35 | Gemini (Bard) 2.595B | Mar 2026 | Q26_MARCH_NEWS | https://www.linkedin.com/pulse/claude-gemini-apple-middle-east-conflict-reshuffled-news-prediction-bewhf | confirms, or is a more precise version of, the figure used |
| 36 | Gemini (Bard) now approaching 2.6 billion | Mar 2026 | Q26_MARCH_NEWS | https://www.linkedin.com/pulse/claude-gemini-apple-middle-east-conflict-reshuffled-news-prediction-bewhf | confirms, or is a more precise version of, the figure used |
| 37 | Claude 824M | Apr 2026 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | confirms, or is a more precise version of, the figure used |
| 38 | Gemini (Bard) 2.761B | Apr 2026 | Q26_APRIL_NEWS | https://www.linkedin.com/pulse/tiktoks-web-takeover-claudes-continued-surge-metas-ai-moment-n8gvc | confirms, or is a more precise version of, the figure used |
| 39 | Claude 952.5M | May 2026 | Q26_JUNE_NEWS | https://www.linkedin.com/pulse/did-ai-take-summer-vacation-similarweb-cukgf | confirms, or is a more precise version of, the figure used |
| 40 | Claude 953M | May 2026 | Q26_IPO_PDF | https://www.similarweb.com/corp/wp-content/uploads/2026/09/attachment-Anthropic-IPO-Special-Report-September-2026.pdf | confirms, or is a more precise version of, the figure used |
| 41 | Claude 946.7M | Jun 2026 | Q26_JUNE_NEWS | https://www.linkedin.com/pulse/did-ai-take-summer-vacation-similarweb-cukgf | would contest the figure used |
| 42 | Gemini (Bard) 2.859B | Jun 2026 | Q26_JUNE_NEWS | https://www.linkedin.com/pulse/did-ai-take-summer-vacation-similarweb-cukgf | confirms, or is a more precise version of, the figure used |

Also for Cowork: the September 2026 profiles must be read as **that month's** figure ("last month" tooltip, dossier F12); the S23_BDAY infographic labels every month of ChatGPT's first year (only five are listed above); and the IPO PDF has labelled monthly totals for several sites from September 2023 to August 2026.

## 6. Publications not yet mined for every month (owner decision: every published month)

The quarter-end prompt collected one month per quarter. These publications are known to hold other months that were not extracted; a further research round (or Cowork reading them) could add points:

- **Q26_IPO_PDF** (Similarweb, Sep 2026): labelled monthly totals for claude.ai and others, Sep 2023 – Aug 2026 (would fill Jul–Aug 2026 and 2024 gaps).
- **Q26_FEB_NEWS** (Similarweb newsletter, Mar 2026): Jan 2025, Feb 2025, Jan 2026 and Feb 2026 for deepseek.com, chatgpt.com and claude.ai.
- **Q26_JUNE_NEWS / Q26_MARCH_NEWS / Q26_APRIL_NEWS** (newsletters): May 2026 for Claude and Gemini, other months in charts.
- **SW24_JUL** (Jul 2024 post): bars for character.ai, chatgpt.com, claude.ai, gemini.google.com and copilot.microsoft.com, without printed labels (dossier F13: never read off a bar's height).
- **S24_CUSTOM** (Jan 2024): 2023 graphs without exact labels.
- **Similarweb's free profiles**: only the latest month is shown, so earlier months cannot be added this way.

## 7. Press credits (description)

Press articles whose figures reach a bar (DEC-244 credits Similarweb on screen and in the description; these are credited in the description too):

- **Digiday**, 2023-12-01 (https://digiday.com/media-buying/chatgpt-turns-a-year-old-marking-a-major-milestone-for-generative-ai/): ChatGPT Nov 2023 1.67 billion; Claude Nov 2023 26 million; Gemini (Bard) Nov 2023 267 million.
- **Digiday**, 2025-10-20 (https://digiday.com/media/in-graphic-detail-how-ai-search-is-changing-publisher-visibility/): Claude Sep 2024 70.4 million; Copilot Sep 2024 37 million; Meta AI Sep 2024 7.8 million; Perplexity Sep 2024 72.3 million; Copilot Sep 2025 99.6 million.
- **The Decoder**, 2026-03-12 (https://the-decoder.com/chatgpt-still-leads-the-chatbot-market-but-its-dominance-is-slipping-as-googles-gemini-gains-ground/): ChatGPT Feb 2026 5.35 billion; Gemini (Bard) Feb 2026 2.11 billion; Grok Feb 2026 298.5 million; Perplexity Feb 2026 153.8 million.

## 8. Checks

- **K01 PASS** Every on-screen value rests on a VERIFIED figure with its URL and the wording seen at source. 137 points used; problems: none
- **K02 PASS** No averaging: each published month shows one printed figure exactly; each other month is the straight line between its two points. 203 series rows; mismatches: none; used values not printed: none
- **K03 PASS** No point or bar before the site's start date. problems: none
- **K04 PASS** One address per assistant per month. problems: none
- **K05 PASS** DeepSeek: deepseek.com only; never deepseek.com + chat.deepseek.com. 13 DeepSeek points used; problems: none
- **K06 PASS** No forecast: projections (Similarweb's June 2024 and October 2023 projections) are never used. projection rows ['M040', 'M062'], all excluded
- **K07 PASS** data_version set on every point and every series row. problems: none
- **K08 PASS** No extrapolation beyond a bar's first or last published point. problems: none
- **K09 PASS** Only eligible VERIFIED figures are used; UNVERIFIED and NOT FOUND never. problems: none
- **K10 PASS** Leftover conflicts use no figure until Luke decides. 2 leftovers; problems: none
- **K11 PASS** Le Chat and uncounted sites (Bing Chat in bing.com, Grok in x.com) have no bar. none on the board

Tests: `python3 tests/rtt102/run_tests_rtt102.py` (rebuilds twice into empty folders and compares every byte, then re-checks the rules independently).

## 9. Questions for Luke

Each has Claude's recommendation and what happens if there is no answer.

1. **The end of the race (July–September 2026).** Only ChatGPT has a verified figure after June 2026; the other sites' September 2026 profiles are UNVERIFIED because Similarweb's free search limit stopped Cowork. *Recommendation:* Cowork reads the eight September profiles on a fresh day (and the IPO PDF's labelled July–August totals), then the race runs to September 2026. *If no answer:* the build keeps every bar's own last verified month; the design session would then end the film at June 2026, the last month with every leading bar live.
2. **Claude, February 2026: 203 million or 290.3 million?** Similarweb's IPO blog says visits rose "from 203 million to 824 million" between February and April 2026, so Luke's rule (Similarweb over press) picks 203 million over The Decoder's 290.3 million. But Similarweb's own IPO report (PDF) puts 203M in **January** and 290M in February, and its February newsletter shows 290.3M (both UNVERIFIED). *Recommendation:* Cowork checks the PDF and the newsletter image; if they confirm, use 290.3 million (two Similarweb publications and the press agree; the blog's "between February and April" reads as loose prose). *If no answer:* the rule's 203 million stays.
3. **Two small 2023 leftovers for ChatGPT.** January 2023: 616 million (Mar 2023 post) or 617 million (Nov 2023 post). April 2023: about 1.76 billion (May 2023 post, twice), nearly 1.7 billion (Oct 2023 post) or 1.77 billion (Nov 2023 post). All are Similarweb, older version, final, so the rule cannot choose. *Recommendation:* add a fourth step to the rule, "then the later publication over the earlier", which gives 617 million and 1.77 billion (both from the year-in-review post that also supplies May, June, August, September and October 2023). *If no answer:* neither month is used; the straight line runs across (about 633 million and 1.70 billion), and both stay listed.
4. **"Visitors" wording (Bard April and May 2023, ChatGPT July 2023).** Similarweb's text says "visitors" where the figures are clearly visits (DEC-510). *Recommendation:* use them as visits. *If no answer:* they stay in use.
5. **Lower bounds.** ChatGPT February 2023 is published only as "more than 1 billion" (and "just over", "tops"). *Recommendation:* use 1 billion with the house "+" ("1bn+", house style 3). *If no answer:* used as 1 billion with a lower-bound flag; the design session shows the "+".
6. **Set-asides (DEC-509):** Similarweb's November 2024 round-up ("November traffic hit ... 3.7 billion", probably October's figure), a "38K" table cell for Grok that its own page contradicts, two unit slips ("6.2M", "1.2M") and DataReportal's June 2024 figures (published three days after the data-version change, but matching the older version). *Recommendation:* keep them out. *If no answer:* they stay out.
7. **Similarweb's figures in the public repository.** `data/rtt-102/` now holds about 200 of Similarweb's published figures with their sources (DEC-244 accepts the risk for the video; the brief puts the tables here). *Recommendation:* keep them public, credited, like the other episodes' data. *If no answer:* they stay; say if you would rather move the figure tables to the private repo.
8. **Gemini's fall across the data-version change.** The line from 433.5 million (Mar 2024, older) to 247.3 million (Sep 2024, current) shows a 43% fall that may be Similarweb's re-estimate. *Recommendation:* keep the published figures (owner decision DEC-501 already marks older estimates and adds a note at the revision); the design session should show the note at August 2024 and check how the fall looks. *If no answer:* as recommended.
