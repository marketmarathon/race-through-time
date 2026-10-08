# K. Recommended final dataset — RTT-103 The AI Spending Race (stages 1–2)

**Status: APPROVED by Luke on 8 Oct 2026 (DEC-291, confirming Claude's proposal DEC-283), with CoreWeave added as a late entrant (DEC-295) and Tencent kept with an on-screen note (DEC-292). Nothing is rendered or published.**

## Recommendation: option C — cash capital expenditure as each company prints it

| Company | Series used in the race | Why |
|---|---|---|
| Amazon | Purchases of property and equipment, **net of proceeds from sales and incentives** (Amazon's own capex measure) | Continuous 2009–2026. Amazon printed gross purchases only from 2017; the gross series (B) would leave Amazon out of the race until 2017. Net was 2.3% below gross for the year to June 2026 (US$169.0bn vs 173.0bn). |
| Microsoft | Additions to property and equipment (cash) | Microsoft publishes no company-defined capex figure in SEC documents (series A NOT FOUND); its call-quoted capex adds finance leases. |
| Alphabet, Oracle | Purchases of property and equipment / capital expenditures (cash) | The company's own capex measure is the same line (A = B). |
| Meta | Purchases of property and equipment (cash) as printed in the statement | Meta's own measure adds finance-lease principal from 2019 (US$92.4bn vs 89.3bn for the year to June 2026). |
| Baidu | Capital expenditures (cash; equals "acquisition of fixed assets" in every 20-F year checked) | Comparable cash measure, every quarter 2009–2026. |
| Alibaba | Capital expenditures (cash, incl. campus land use rights and construction in progress), on its scope from Sep 2018 | FY2018 quarters rebuilt exactly on that scope from Alibaba's own re-presented figures (DEC-303); the four FY2017 quarters (Apr 2016–Mar 2017) included licensed copyrights and cannot be split (DEFINITION_BREAK); before Apr 2016 small intangibles (5–7%) are included, kept as reported and flagged, with a note for the video description; no deduction (DEC-302, DEC-307). |
| Tencent | Capital expenditures = **additions** (accrual) incl. some intangible assets | The only quarterly measure Tencent prints. Kept with an on-screen note that it is measured differently (DEC-292). |
| CoreWeave | Purchase of property and equipment, including capitalized internal-use software (cash) | Late entrant from 2024 Q4, its first four published quarters (DEC-295). |

Finance leases are excluded for every company, so nothing is double counted.

## How the three options compare (H_coverage_by_series.csv)
- **A, company-reported capex:** Microsoft NOT FOUND for every quarter, so A cannot power an eight-company race. Definitions differ widely (Meta adds lease principal, Amazon nets incentives, Tencent is accrual).
- **B, strict cash purchases of property and equipment:** Amazon NOT FOUND for 2010–2016 (28 quarters); Tencent NOT FOUND for every quarter (half-yearly only).
- **C (approved):** every US company complete from its first public quarter (Meta from 2012), Baidu complete, Tencent from 2011 Q4, Alibaba from 2014 Q1 with no bar for the TTM points 2016 Q2–2017 Q4, CoreWeave from 2024 Q4.

Chosen on the brief's criteria in order: coverage, comparability, consistency, source quality (every US figure printed in the 10-Q/10-K; China figures read in the companies' own filings), understandability and reproducibility (the build re-derives every number from committed inputs). Not chosen for size: C is smaller than A for Meta and Amazon.

## Title and chart label
The title must name the measure, total capital spending (DEC-291), e.g. **"Big Tech's Capital Spending, 2010–2026"**; AI is the story told around it. Chart label: **"Capital expenditure, trailing 12 months (US$ billions, nominal)"**, with a source line such as *"Cash spent on property and equipment as reported by each company; Tencent: additions including some intangible assets; Chinese companies converted at quarterly average exchange rates (Federal Reserve H.10)."* The wording of any on-screen note is a design question for Luke (DEC-069).

## What is not supported
- "AI spending" as a bar label: the bars are **total** capital expenditure (brief section 4); AI attribution is only in sourced statements (G).
- AWS or Google Cloud capex: not disclosed; never relabel the company totals.
- 2026 figures inside the historical race: guidance and estimates stay in `AI_SPENDING_RACE_2026E.csv`, labelled.

## Notes for the video description (DEC-307)
- Alibaba before April 2016: "Alibaba's figures before April 2016 also include small purchases of intangible assets (about 5–7% of the total in its fiscal years 2015 and 2016), which Alibaba did not report separately by quarter." Wording to be confirmed with Luke when the description is written.
- Alibaba April 2016 – December 2017: no bar, because Alibaba's figures then included licensed copyrights and cannot be split (DEC-303).
- Tencent: its figure is additions (including some intangible assets), not cash (DEC-292).
