# RTT-103 The AI Spending Race — data report (IQ-16 stage 1, 7 Oct 2026; IQ-16b stage 2, 8 Oct 2026)

**Stage 2 (8 Oct 2026) is at the top; the stage-1 report follows unchanged below it.**

## Stage 2 (IQ-16b, 8 Oct 2026): Luke's answers applied

**In plain English.** All ten answers are recorded (DEC-291 to DEC-301) and applied. The race now has nine companies, with CoreWeave joining at the end of 2024. Alibaba's gap is smaller and its 2017–2018 figures are now rebuilt from Alibaba's own numbers. The forecast frames hold only the companies' own guidance, plus ByteDance greyed as a press report. Nothing is rendered or published.

### What each answer led to
| # | Your answer | What was done |
|---|---|---|
| 1 | Option C; the title names total capital spending (DEC-291) | K marked APPROVED; title rule added to the metric contract and `reference/house_style.md` (example: "Big Tech's Capital Spending, 2010–2026"). |
| 2 | Tencent kept with a note (DEC-292) | Every Tencent row in the master carries the note "measured differently - additions, including some intangible assets". Exact on-screen wording is a design question. |
| 3 | Amazon net (DEC-293) | No change needed. |
| 4 | Alibaba: its own re-presented figures (DEC-294) | Found and used (see below, DEC-303). |
| 5 | CoreWeave as a late entrant (DEC-295) | Added from its first published quarter (Q1 2024); first bar at **2024 Q4**, once four quarters exist. Eligibility table says ADDED. |
| 6 | ByteDance only in the 2026 frame, greyed, after reading the SCMP article (DEC-296) | The article was read at source (9 May 2026): "more than 200 billion yuan (US$30 billion), according to two people familiar with the matter". In the 2026 frame only, greyed, as "more than US$29.3bn" (converted at the 2026 average H.10 rate to date). Never in the historical race. |
| 7 | 2026 frame with ranges; roll forward to 2027–2028 with companies' own forecasts (DEC-297) | New `AI_SPENDING_RACE_FORECAST.csv` (DEC-304); `AI_SPENDING_RACE_2026E.csv` is its 2026 part. Ranges always carry both ends. 2027 holds only Alphabet ("increase significantly") and Microsoft (year to June 2027, "grow year-over-year"); 2028 is empty until company statements are checked. No analyst forecasts. |
| 8 | H.10, everything in US$ (DEC-298) | Confirmed; no change. |
| 9 | Catalogue private (DEC-299) | Confirmed; no change. |
| 10 | Cowork's checks (DEC-300) | Alphabet 2026 guidance now **$195–205bn** (22 Jul 2026 call); $175–185bn and $180–190bn kept as superseded. Amazon stays "about $200 billion". |
| — | OpenAI never a bar or capex (DEC-301) | A new format check fails the build if OpenAI or ByteDance ever appears as a bar. |

### Alibaba: stage 1 got the dates wrong, now corrected (DEC-303)
- Alibaba's capex included licensed copyrights (from the Youku deal) from **April 2016**, not January 2017 as stage 1 said.
- Alibaba's FY2019 annual report (20-F) re-presents FY2017 and FY2018 on its later, narrower scope. Its quarterly releases from Sep 2018 to Jun 2019 re-present each earlier quarter the same way. From these, the five quarters Jun 2017 to Jun 2018 are rebuilt exactly; they add up to Alibaba's own FY2018 total (RMB19,628m).
- The four quarters Apr 2016–Mar 2017 cannot be split, so they stay out. **Alibaba now has no bar for seven TTM points (2016 Q2 to 2017 Q4)**, instead of stage 1’s eight (2017 Q1 to 2018 Q4). Stage 1 wrongly showed bars for 2016 Q2–Q4; the four 2018 points now have bars.
- Before April 2016, Alibaba's figure also includes small intangible purchases (5.2% in FY2015, 6.6% in FY2016). These quarters are kept and flagged (DEC-302; question A below).

### Alphabet's equity raise (DEC-305)
- Alphabet's 8-K of 4 Jun 2026 was read at source. It describes an equity raise "to fund investments in its world-class AI compute infrastructure", priced on 2 Jun 2026 at **$84.75bn** in total (this includes a $40bn at-the-market programme sold over time).
- It is added to the story moments (G) as financing, not capex.

### At the end of June 2026 (12 months to the latest quarter)
| Rank | Company | US$ bn |
|---|---|---|
| 1 | Amazon | 169.0 |
| 2 | Alphabet | 132.4 |
| 3 | Microsoft | 115.9 |
| 4 | Meta | 89.3 |
| 5 | Oracle | 55.7 |
| 6 | Alibaba | 22.3 |
| 7 | CoreWeave | 20.6 |
| 8 | Tencent | 17.0 |
| 9 | Baidu | 3.3 |

- **Race total:** US$625.5bn, up 80.0% on a year earlier. CoreWeave pushes Tencent and Baidu down one place each; the order of the top six is unchanged.
- **Turning points:**
  - The leader and first-past-the-mark moments are unchanged from stage 1.
  - The total passed US$100bn at the end of 2020, US$250bn at the end of 2024 (US$264.3bn, with CoreWeave's first bar) and US$500bn in Q1 2026 (US$526.7bn).

### Checks
- **Financial QA:** PASS for all nine companies, 81 of 81 checks.
- **File-format checks:** PASS, 24 of 24. The four new checks are:
  - every cited source is listed in A;
  - OpenAI and ByteDance never appear as bars;
  - the forecast frames hold company guidance only, plus the greyed ByteDance row;
  - every range has both a low and a high.
- **Tests:** 19 of 19 pass (`python tests/rtt103/run_tests_rtt103.py`), including a byte-identical rebuild.
- **Master:** 496 bars.
- **Cross-checks** (for information): unchanged. The same two intra-year restatements are listed in I. Private vendor data agrees for all five CoreWeave quarters.

### Questions for Luke (stage 2)
- **A. Alibaba before April 2016** (DEC-302): its figure includes 5–7% intangible purchases, which cannot be split by quarter. Should these quarters be kept, flagged?
  - *Recommendation:* keep them with the data flag. The effect is small, and leaving them out would remove Alibaba from 2014 to 2016.
  - *If unanswered:* kept, flagged.
- **B. How absent bars look** (Alibaba 2016 Q2–2017 Q4) and how a late entrant arrives (CoreWeave at 2024 Q4): this is a design question (DEC-069).
  - *Recommendation:* decide it in the design session, with options side by side.
  - *If unanswered:* nothing is built.
- **C. ByteDance's figure in the frame:** show "more than US$29.3bn" (converted by us) or SCMP's own "US$30 billion"?
  - *Recommendation:* US$29.3bn. It uses the same exchange-rate method as every other figure (DEC-298), and the note quotes the yuan figure.
  - *If unanswered:* US$29.3bn.

### Still to do
- **ChatGPT's results** (2026–2028 company forecasts, OpenAI commitments): awaited. When they arrive, each will be checked at source before any row is filled. 2028 is empty until then.
- **The design session:** logos, colours, notes, absent bars, frames. Nothing is built without your approval.

---

# Stage 1 report (IQ-16, 7 Oct 2026)

**For Luke, in plain English.** The data for the AI Spending Race is built for all eight companies, from 2010 to the end of June 2026, and every figure in the race was read in the company's own filing. Nothing has been rendered or published. Below: what was built, what passed, what is missing, and ten questions (each with Claude's recommendation).

## What was built
- **The race:** trailing-12-month capital expenditure in US dollars for Amazon, Microsoft, Alphabet (Google), Meta (Facebook), Oracle, Alibaba, Tencent and Baidu, quarter by quarter from 2010 Q1 to **2026 Q2**, the last quarter every company has reported. 488 bars in `data/rtt-103/AI_SPENDING_RACE_MASTER.csv`.
- **Where the numbers come from:**
  - US companies: 339 quarterly and annual SEC reports (2009–2026). Each number was taken from the cash-flow statement *as printed* (2,133 printed values matched; values not printed in the statement were never used).
  - Baidu: its quarterly results on sec.gov (2009–2026).
  - Alibaba: its quarterly results from Alibaba's investor site and sec.gov (2013–2026).
  - Tencent: its HKEXnews announcements (2011–2026).
  - Exchange rate: the Federal Reserve's daily rates (H.10), averaged over each company quarter.
- **Every brief file:** A to L and both master files, with the brief's exact columns, in `data/rtt-103/` (see its README).
- **Also built:** the CoreWeave eligibility table, 2026 guidance (F) and the 2026 end frame, 20 sourced AI/cloud statements (G), and 13 turning points calculated from the data.

### At the end of June 2026 (12 months to the latest quarter)
| Rank | Company | US$ bn | Basis |
|---|---|---|---|
| 1 | Amazon | 169.0 | cash, net of proceeds and incentives |
| 2 | Alphabet | 132.4 | cash purchases of property and equipment |
| 3 | Microsoft | 115.9 | cash additions to property and equipment |
| 4 | Meta | 89.3 | cash purchases of property and equipment |
| 5 | Oracle | 55.7 | cash capital expenditures (year to 31 May 2026) |
| 6 | Alibaba | 22.3 | cash capex (RMB, converted quarter by quarter) |
| 7 | Tencent | 17.0 | additions incl. some intangible assets (RMB) |
| 8 | Baidu | 3.3 | cash purchases of fixed assets (RMB) |
Race total: US$604.9bn, up 78.5% on a year earlier. CoreWeave, not in the race, would rank 7th (US$20.6bn).

### Turning points (from `narrative_checkpoints.csv`)
- Microsoft led in early 2010.
- Alphabet led from the end of 2010.
- Amazon led briefly in late 2012, then again from Q3 2020 onwards.
- Alphabet was first above US$25bn (end of 2018); Amazon was first above US$50bn (Q3 2021), above US$100bn (Q2 2025) and above US$150bn (Q2 2026).
- The eight-company total passed US$100bn in 2020, US$250bn in 2024 and US$500bn in Q1 2026.

## What passed
**Financial QA** (the brief's section 25; `J_QA_report.md`): **PASS for all eight companies**, 71 of 71 checks. The checks were:
- the quarters add up to each printed year;
- every TTM recalculated;
- quarter lengths and calendar placement;
- signs, units and wrong lines (free cash flow, depreciation, acquisitions);
- no zero or negative quarters;
- exchange-rate range and direction;
- every input read at its source.

**File-format checks:** PASS, 20 of 20. These cover exact columns, allowed H values, one row per key, sort order and the 2026E labels. The tests (`tests/rtt103/run_tests_rtt103.py`) pass 13 of 13; they include a rebuild that matches the committed files byte for byte.

**Independent cross-checks** (for information; every difference is listed in file I):
- **Agree:**
  - Amazon's own printed 12-month figures, all 50.
  - Meta's release figures, 55 of 56.
  - Alphabet's quarterly figures printed in its reports, 9 of 10.
  - The licensed vendor data, which stays private: Amazon 69/69, Microsoft 69/69 and Oracle 67/69 quarters equal.
- **Differ:** two quarters, where a company restated an earlier figure during the year: Alphabet Q3 2016 by 1.1% and Meta Q4 2018 by 1.6%.
- **The vendor's differences** (Meta, Alphabet 2009–2015, Alibaba) are explained in file I. In every case the filing value stands.

## What is missing or weak (all in `I_conflicts_and_warnings.csv`)
- **Alibaba 2017–2018:** for five quarters (Jan 2017 to Mar 2018) Alibaba reported capex together with intangible assets. These are not mixed in, so Alibaba has no bar for the TTM points 2017 Q1 to 2019 Q1.
- **Tencent's measure is different:** it is *additions* (an accounting measure, not cash) and includes some intangible assets. Tencent prints its cash figure only half-yearly.
- **Microsoft's own "capex including finance leases"** is quoted only on its earnings calls. The race uses its cash figure, like the other US companies.
- **Amazon:** its cash figure is net of incentives for the whole period, because Amazon printed gross purchases only from 2017. The difference is about 2% now and 13% in 2017.
- **Missing quarters:**
  - Not public: Tencent before 2011, Alibaba before mid-2013 and Meta before 2012.
  - So the race starts with 5 companies in 2010; Meta joins in 2012, Tencent in 2011 Q4 and Alibaba in 2014 Q1.
- **2026 guidance not yet checked at source:**
  - Alphabet's reported raise to $180–190bn. TrendForce reports it; Alphabet's own site refused the download.
  - Amazon's and Alphabet's later updates on their calls.
  - Any 2026 guidance from Oracle, Tencent, Alibaba and Baidu.
  - Reuters items, which refused access.

## Questions for Luke (Claude's recommendation; what happens if unanswered)
1. **Which series powers the race?**
   - *Recommendation:* option C, "cash spent on property and equipment as each company reports it" (see `K_recommended_dataset.md`). Series A cannot be used because Microsoft has no published figure, and series B would leave Amazon out until 2017.
   - *If unanswered:* stage 2 continues on C as a working assumption; nothing is rendered.
2. **Tencent:** keep it in the race with an on-screen note ("additions, including some intangible assets"), or leave it out?
   - *Recommendation:* keep it with the note (it is one of the nine companies the industry tracks, and its definition is printed in every announcement).
   - *If unanswered:* it stays in the data, flagged, and the design session asks again.
3. **Amazon's net figure:** OK to show Amazon net of incentives for the whole race (its own capex measure; about 2% below gross today)?
   - *Recommendation:* yes.
   - *If unanswered:* as recommended.
4. **Alibaba's 2017–2019 gap:**
   - *Recommendation:* stage 2 looks for Alibaba's own re-presented figures (its FY2019 annual report) to close the gap. Until then its bar is absent for those points. How to show an absence is a design question for you (DEC-069).
   - *If unanswered:* the gap stays.
5. **CoreWeave** (US$20.6bn in the year to June 2026, but quarterly figures only from 2024):
   - *Recommendation:* keep it out of the race and mention it in narration.
   - *If unanswered:* out.
6. **ByteDance in the 2026 end frame** (a press report from unnamed sources: "more than 200 billion yuan"):
   - *Recommendation:* leave it out of the on-screen frame, or show it only as "press report".
   - *If unanswered:* out of the frame, kept in F.
7. **The 2026 end frame at all?** Company guidance uses different definitions: Meta adds lease payments, Microsoft adds finance leases and uses a calendar year.
   - *Recommendation:* show it as a separate, clearly labelled "2026 guidance" frame with ranges, never midpoints alone.
   - *If unanswered:* no 2026 frame.
8. **Exchange rate method** (working choice DEC-281: Federal Reserve daily rates averaged over each quarter):
   - *Recommendation:* confirm.
   - *If unanswered:* stays.
9. **Public source list** (DEC-285): the brief asks for ChatGPT's catalogue rows to be appended to file A unchanged. Your rule DEC-006 keeps research inputs private. Claude kept the full catalogue private and listed only the sources it opened in the public file A.
   - *Recommendation:* confirm.
   - *If unanswered:* stays private.
10. **Unchecked 2026 guidance:**
    - *Recommendation:* ask Cowork to open Alphabet's Q1/Q2 2026 call pages and Amazon's latest call in your Chrome and record the figures. Alphabet's site refuses GitHub runners.
    - *If unanswered:* 2026E uses the last verified figures (Alphabet $175–185bn, Amazon about $200bn).

## Working choices and findings recorded
- **Working choices:** DEC-281 (exchange rates), DEC-282 (Sharadar as cross-check only), DEC-284 (quarters as first reported; rounded first prints) and DEC-285 (public source list).
- **Proposal:** DEC-283 (option C).
- **Findings:** DEC-286 (definitions by company) and DEC-287 (source access).
- **Also recorded:** DEC-288 (latest common quarter), DEC-289 (Sharadar's definition) and DEC-290 (tests).

## COMPLETED / STILL TO DO
- **COMPLETED:** sections A to L, both master files, the CoreWeave eligibility table and the narrative checkpoints, for all eight companies.
- **STILL TO DO** (stage 2, after Luke's answers):
  - close Alibaba's 2017–2018 gap if a re-presented source exists;
  - the 2026 guidance checks in question 10;
  - Microsoft's call-quoted capex history (only if wanted);
  - the design session (logos, colours, labels) — nothing is built without Luke's approval.
