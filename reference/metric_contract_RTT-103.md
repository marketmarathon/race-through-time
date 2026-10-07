# Metric contract — RTT-103 The AI Spending Race · v1.0 (data build IQ-16, stage 1) · 7 Oct 2026

Owner decisions: DEC-246 (episode and method), DEC-278 (number and order), DEC-279 (research split), DEC-280 (no EODHD upgrade).
Claude working choices, proposals and findings: DEC-281 to DEC-290. Data: `data/rtt-103/` (README there).
**Stage 1 is data only. No player, renderer, render or visual change (DEC-069).**

## Universe (DEC-246)
Amazon, Microsoft, Alphabet (Google until 2 Oct 2015), Meta (Facebook until 28 Oct 2021), Oracle, Alibaba, Tencent, Baidu.
ByteDance: not in the historical race (private; no quarterly evidence) — estimates only, labelled, in the 2026E frame if Luke agrees.
CoreWeave: candidate only (eligibility table); not added without Luke's approval. Nvidia: excluded (supplier).

## Metric and basis
- Trailing-12-month capital expenditure, **nominal US$**, at each calendar quarter end, 2010 Q1 to the latest common complete quarter (**2026 Q2** at the 7 Oct 2026 cutoff).
- **Total corporate capex**, not "AI capex" (brief section 4). Consolidated company figures; never AWS or Google Cloud.
- Canonical series (proposed, option C, awaiting Luke): cash spent on property and equipment as each company prints it — Amazon net of proceeds and incentives; Microsoft, Alphabet, Meta, Oracle gross cash purchases; Baidu and Alibaba their cash capex; Tencent its capex (additions incl. some intangibles, flagged). Finance leases excluded throughout.
- Series A (company-reported capex) and B (strict cash purchases of property and equipment) are kept in D for comparison.

## Evidence grades (per observation)
A: SEC 10-K/10-Q/20-F/F-1/6-K results, HKEX filings. B: company earnings releases, call transcripts, IR releases. C: original third-party research (TrendForce). D: press (Reuters, SCMP). Only figures read at their source (VERIFIED) enter D, E and the master; UNVERIFIED items are listed, never used.

## Method (deterministic: `scripts/build_rtt103_dataset.py`)
1. Quarter = printed 3-month figure; else exact year-to-date difference from figures as first reported, inside one definition (formula and both sources recorded). No division of annual totals, interpolation, filling or zeros.
2. US figures: XBRL locates the period; the number must be printed on the identified row of the filing's cash-flow statement.
3. RMB quarters converted at the mean of Federal Reserve H.10 daily CNY-per-USD rates over the actual fiscal quarter (no-data days excluded, never filled). TTM US$ = sum of four converted quarters.
4. Calendar bucket = calendar quarter containing the fiscal period end (Oracle's May quarter is Q2; Microsoft's June year; Alibaba's March year).
5. TTM only from four consecutive valid quarters; a window spanning a definition change is flagged.

## Display attributes (DEC-036) — what the video would show, and its source
| Attribute | Source |
|---|---|
| Company display name (Amazon; Microsoft; Alphabet (Google); Meta (Facebook); Oracle; Alibaba; Tencent; Baidu) | `entity_name_history.csv`; renamings keep one bar |
| Bar value: TTM capex, US$ bn (3 d.p. in data; rounding on screen is a design choice) | `AI_SPENDING_RACE_MASTER.csv` |
| Rank and rank change | Master |
| Date label (calendar quarter end) | Master `date` |
| Definition warning per company (e.g. Amazon net; Tencent additions) | Master `definition_warning`; C |
| 2026 GUIDANCE / 2026 ESTIMATE labels, ranges (never a midpoint alone) | `AI_SPENDING_RACE_2026E.csv` |
| Annotations (sourced statements) | G (narration only) |
| Logos / colours | Not built in stage 1 (design session, Luke's approval first) |

## Claims this data cannot support
"AI spending" as the bar label; AWS or Google Cloud capex; any 2026 figure as an actual; ByteDance history; Alibaba bars for the TTM points 2017 Q1–2019 Q1 (definition break); Tencent cash capex by quarter; Microsoft's "capex including finance leases" history.
