# RTT-103 The AI Spending Race — data report (IQ-16, stage 1) · 7 Oct 2026

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
