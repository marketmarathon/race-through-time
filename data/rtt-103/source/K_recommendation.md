# K. Recommended final dataset — RTT-103 The AI Spending Race (stage 1)

**Status: Claude's recommendation (Claude proposal, DEC-283), awaiting Luke. Nothing is rendered or published.**

## Recommendation: option C — cash capital expenditure as each company prints it

| Company | Series used in the race | Why |
|---|---|---|
| Amazon | Purchases of property and equipment, **net of proceeds from sales and incentives** (Amazon's own capex measure) | Continuous 2009–2026. Amazon printed gross purchases only from 2017; the gross series (B) would leave Amazon out of the race until 2017. Net was 2.3% below gross for the year to June 2026 (US$169.0bn vs 173.0bn). |
| Microsoft | Additions to property and equipment (cash) | Microsoft publishes no company-defined capex figure in SEC documents (series A NOT FOUND); its call-quoted capex adds finance leases. |
| Alphabet, Oracle | Purchases of property and equipment / capital expenditures (cash) | The company's own capex measure is the same line (A = B). |
| Meta | Purchases of property and equipment (cash) as printed in the statement | Meta's own measure adds finance-lease principal from 2019 (US$92.4bn vs 89.3bn for the year to June 2026). |
| Baidu | Capital expenditures (cash; equals "acquisition of fixed assets" in every 20-F year checked) | Comparable cash measure, every quarter 2009–2026. |
| Alibaba | Capital expenditures (cash, incl. campus land use rights and construction in progress) | Comparable apart from five quarters (Jan 2017–Mar 2018) printed on a broader scope (DEFINITION_BREAK, not spliced). |
| Tencent | Capital expenditures = **additions** (accrual) incl. some intangible assets | The only quarterly measure Tencent prints. Not strictly comparable: shown with a definition warning, or excluded (question for Luke). |

Finance leases are excluded for every company, so nothing is double counted.

## How the three options compare (H_coverage_by_series.csv)
- **A, company-reported capex:** Microsoft NOT FOUND for every quarter, so A cannot power an eight-company race. Definitions differ widely (Meta adds lease principal, Amazon nets incentives, Tencent is accrual).
- **B, strict cash purchases of property and equipment:** Amazon NOT FOUND for 2010–2016 (28 quarters); Tencent NOT FOUND for every quarter (half-yearly only).
- **C (recommended):** every US company complete from its first public quarter (Meta from 2012), Baidu complete, Tencent from 2011 Q4, Alibaba from 2014 Q1 with a gap 2017 Q1–2019 Q1.

Chosen on the brief's criteria in order: coverage, comparability, consistency, source quality (every US figure printed in the 10-Q/10-K; China figures read in the companies' own filings), understandability and reproducibility (the build re-derives every number from committed inputs). Not chosen for size: C is smaller than A for Meta and Amazon.

## Precise chart label (recommended)
**"Capital expenditure, trailing 12 months (US$ billions, nominal)"**, with a source line such as *"Cash spent on property and equipment as reported by each company; Tencent: additions including some intangible assets; Chinese companies converted at quarterly average exchange rates (Federal Reserve H.10)."* The wording of any on-screen note is a design question for Luke (DEC-069).

## What is not supported
- "AI spending" as a bar label: the bars are **total** capital expenditure (brief section 4); AI attribution is only in sourced statements (G).
- AWS or Google Cloud capex: not disclosed; never relabel the company totals.
- 2026 figures inside the historical race: guidance and estimates stay in `AI_SPENDING_RACE_2026E.csv`, labelled.
