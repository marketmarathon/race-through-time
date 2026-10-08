# Metric contract — RTT-103 The AI Spending Race · v1.1 (IQ-16b, stage 2) · 8 Oct 2026

Owner decisions: DEC-246 (episode and method), DEC-278 (number and order), DEC-279 (research split), DEC-280 (no EODHD upgrade).
Claude working choices, proposals and findings: DEC-281 to DEC-290. Luke's answers: DEC-291 to DEC-301 (8 Oct 2026); stage 2: DEC-302 to DEC-305. Data: `data/rtt-103/` (README there).
**Stages 1–2 are data only. No player, renderer, render or visual change (DEC-069).**

## Universe (DEC-246)
Amazon, Microsoft, Alphabet (Google until 2 Oct 2015), Meta (Facebook until 28 Oct 2021), Oracle, Alibaba, Tencent, Baidu, and **CoreWeave as a late entrant from 2024 Q4** (DEC-295).
ByteDance: never in the historical race; only in the 2026 forecast frame, greyed, as a press report (DEC-296). OpenAI: never a bar, never capex; story moments labelled COMMITMENT only (DEC-301). Nvidia: excluded (supplier).

## Metric and basis
- Trailing-12-month capital expenditure, **nominal US$**, at each calendar quarter end, 2010 Q1 to the latest common complete quarter (**2026 Q2** at the 7 Oct 2026 cutoff).
- **Total corporate capex**, not "AI capex" (brief section 4). Consolidated company figures; never AWS or Google Cloud.
- **Title must name the measure** (total capital spending, e.g. "Big Tech's Capital Spending, 2010–2026"); AI is the story, not the measure (DEC-291).
- Canonical series (option C, approved DEC-291): cash spent on property and equipment as each company prints it — Amazon net of proceeds and incentives; Microsoft, Alphabet, Meta, Oracle gross cash purchases; Baidu and Alibaba their cash capex; Tencent its capex (additions incl. some intangibles, flagged). Finance leases excluded throughout.
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
| Company display name (Amazon; Microsoft; Alphabet (Google); Meta (Facebook); Oracle; Alibaba; Tencent; Baidu; CoreWeave) | `entity_name_history.csv`; renamings keep one bar |
| Bar value: TTM capex, US$ bn (3 d.p. in data; rounding on screen is a design choice) | `AI_SPENDING_RACE_MASTER.csv` |
| Rank and rank change | Master |
| Date label (calendar quarter end) | Master `date` |
| Definition warning per company (e.g. Amazon net; Tencent additions) | Master `definition_warning`; C |
| Tencent on-screen note: "measured differently - additions, including some intangible assets" (DEC-292) | Master `definition_warning` |
| Forecast frames 2026-2028: company guidance as NUMBER / RANGE / DIRECTION ONLY, ranges never as a midpoint alone; ByteDance greyed as a press report (2026 only) | `AI_SPENDING_RACE_FORECAST.csv` (2026 subset: `AI_SPENDING_RACE_2026E.csv`) |
| Annotations (sourced statements) | G (narration only) |
| Logos / colours | Not built in stage 1 (design session, Luke's approval first) |

## Claims this data cannot support
"AI spending" as the bar label or title measure; AWS or Google Cloud capex; any forecast as an actual; research-firm forecasts on screen; ByteDance history; OpenAI as a bar; Alibaba bars for the TTM points 2016 Q2–2017 Q4 (definition break); CoreWeave before 2024 Q4; Tencent cash capex by quarter; Microsoft's "capex including finance leases" history.
