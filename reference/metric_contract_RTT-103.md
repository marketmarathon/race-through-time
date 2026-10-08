# Metric contract — RTT-103 The AI Spending Race · v1.4 (IQ-16e, stage 5) · 8 Oct 2026

Owner decisions: DEC-246 (episode and method), DEC-278 (number and order), DEC-279 (research split), DEC-280 (no EODHD upgrade).
Claude working choices, proposals and findings: DEC-281 to DEC-290. Luke's answers: DEC-291 to DEC-301, DEC-306 to DEC-310 and DEC-321 to DEC-328 (8 Oct 2026); Claude, stages 2–5: DEC-302 to DEC-305, DEC-311 to DEC-320, DEC-329, DEC-330. Data: `data/rtt-103/` (README there).
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
| Forecast frames 2026: latest company guidance (NUMBER / RANGE; Amazon and Oracle "as reported by Reuters", DEC-311; Oracle's fiscal year to May 2027 in the 2026 frame, DEC-314); ranges never as a midpoint alone; ByteDance greyed as a press report | `AI_SPENDING_RACE_FORECAST.csv` (2026 subset: `AI_SPENDING_RACE_2026E.csv`) |
| Look-ahead 2027–2031 (owner exception DEC-306): company directions as stated (Alphabet, Microsoft; Meta: no outlook) and, where a company gives no figure, named consensus, analyst or research-firm forecasts, each with forecaster, forecaster type, forecast date and measure; never averaged, blended or extended; visibly different from the race; one figure per company per year chosen by a rule Luke approves. Verified so far (DEC-316..DEC-320): FactSet consensus 2026–2030 for the US five (capex definition and calendarisation not stated by the source), Visible Alpha 2026–2027 (cash-flow lines as ours; Microsoft calendarised by averaging fiscal years), Citi on Alibaba FY2027–29, group and industry views; nothing per company for 2031 | `AI_SPENDING_RACE_FORECAST.csv` (input for third-party rows: `source/forecast_lookahead_2027_2031.csv`) |
| Story moments: OpenAI infrastructure commitments labelled COMMITMENT (never capex, never a bar, never summed); companies' own statements that most capex is for AI (COMPANY STATEMENT, DEC-322); iCapital's 70–75% AI-share estimate, once, never applied (DEC-323) | G |
| Running total "Combined capital spending" = sum of the bars on screen, start to end of the look-ahead; no AI-only forecast in it (DEC-324) | L (history); `AI_SPENDING_RACE_LOOKAHEAD_DRAFT.csv` (look-ahead) |
| Look-ahead 2027–2030 bars: Race Through Time estimates (owner exception DEC-326), 2026 base x one named growth source, 2030 marked least reliable (DEC-327); DRAFT until Luke answers DEC-330's questions | `AI_SPENDING_RACE_LOOKAHEAD_DRAFT.csv` |
| Peak views side by side (DEC-328) | `AI_SPENDING_RACE_PEAK_VIEWS.csv` |
| Annotations (sourced statements) | G (narration only) |
| Logos / colours | Not built in stage 1 (design session, Luke's approval first) |

## Claims this data cannot support
An AI-only capex figure for any company or year (none is reported, DEC-321); any look-ahead figure as official or as a company's own when it is an analyst's; an average of forecasters; Alibaba's multi-year plan as annual spending; OpenAI commitments as capex or as a total; "AI spending" as the bar label or title measure; AWS or Google Cloud capex; any forecast as an actual; research-firm forecasts on screen; ByteDance history; OpenAI as a bar; Alibaba bars for the TTM points 2016 Q2–2017 Q4 (definition break); CoreWeave before 2024 Q4; Tencent cash capex by quarter; Microsoft's "capex including finance leases" history.
