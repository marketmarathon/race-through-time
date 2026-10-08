# RTT-103 — The AI Spending Race: How Big Tech Started Spending Hundreds of Billions (data, stages 1–2)

Status: **DATA BUILD stage 1 (IQ-16, 7 Oct 2026), stage 2 after Luke's answers (IQ-16b, 8 Oct 2026) and stage 3, forecasts and OpenAI (IQ-16c, 8 Oct 2026) — pull request #20 open, not merged (DEC-057). Nothing rendered or published.**
Owner decisions: DEC-246 (episode, method), DEC-278 to DEC-280, DEC-291 to DEC-301 and DEC-306 to DEC-310 (Luke's answers). Claude working choices, proposals and findings: DEC-281 to DEC-290, DEC-302 to DEC-305, DEC-311 to DEC-315.
Report for Luke: `reports/RTT-103_data_report.md`. Contract: `reference/metric_contract_RTT-103.md`. Briefs: `prompts/CODE_SESSION_IQ-16.md`, `IQ-16b.md`, `IQ-16c.md`.

**Metric:** trailing-12-month capital expenditure, nominal US$, by calendar quarter, 2010 Q1 to **2026 Q2** (the latest quarter every race company has reported). Nine companies: Amazon, Microsoft, Alphabet, Meta, Oracle, Alibaba, Tencent, Baidu, and CoreWeave from 2024 Q4 (late entrant, DEC-295). The bars are total capital spending, not AI-only spending; the title must say so (DEC-291). ByteDance only in the 2026 forecast frame, greyed (DEC-296); OpenAI never a bar (DEC-301).

## Files (brief sections 16–28 and 34; exact columns)

| File | What it is |
|---|---|
| `A_source_catalogue.csv` | Every source Claude opened (SEC filings and releases, HKEXnews announcements, Alibaba IR releases, FX, guidance pages), with SHA-256. Research-catalogue IDs are kept where the same document was used. ChatGPT's full catalogue, with Claude's rows appended, is private (DEC-285). |
| `B_capex_observations.csv` | One row per sourced figure: every capex-related cash-flow line of each 10-Q/10-K (quarter, year-to-date, year), Meta's release figures, the China-listed figures, and each derived quarter with its formula. Restated values kept side by side (`superseded`). Companion `B_capex_observations_audit.csv`: accession, XBRL tag, the printed statement row, text check. |
| `C_capex_definitions.csv` | Definition history per company with breaks flagged. |
| `D_quarterly_capex_clean.csv` | One row per company per fiscal quarter: local value, FX, series A (company-reported), series B (cash purchases of property and equipment), canonical value (option C), status. |
| `E_capex_TTM_race.csv` | TTM per company per calendar quarter, only from four consecutive valid quarters, with the four components. |
| `F_2026_capex_forecasts.csv` | Company guidance and estimates for 2026 onwards in the brief's exact columns: superseded ranges kept, unverified items labelled, press-reported company guidance (`GUIDANCE_REPORTED_BY_PRESS`), "no outlook" statements, and Alibaba's multi-year plan (`MULTI_YEAR_PLAN`, never split into years). |
| `G_AI_capex_story_events.csv` | Sourced management statements and commitments (verbatim), for narration only. OpenAI rows are labelled COMMITMENT: never capex, never a bar, never summed (DEC-301, DEC-315). |
| `H_coverage_matrix.csv` | Canonical status per quarter and company (A_REPORTED = printed in a grade-A filing; B_REPORTED = printed in a grade-B release; DERIVED_PRIMARY; NOT_FOUND; NOT_YET_EXISTED; DEFINITION_BREAK). `H_coverage_by_series.csv` gives series A and B separately. |
| `I_conflicts_and_warnings.csv` | Every restatement, definition change, source disagreement, currency, period and missing-data issue. |
| `J_QA_report.md` | PASS/FAIL per company: financial QA, independent cross-checks, file-format checks. |
| `K_recommended_dataset.md` | Recommended series and chart label (Claude proposal, awaiting Luke). |
| `L_aggregate_capex.csv`, `L_aggregate_capex_constant_company.csv` | Race total and the constant-company total (companies present for the whole race). |
| `AI_SPENDING_RACE_MASTER.csv` | Video-ready: QA-passed actuals only, rank and rank change. |
| `AI_SPENDING_RACE_FORECAST.csv`, `AI_SPENDING_RACE_2026E.csv` | Forecast frames 2026–2031 (DEC-306, DEC-314): latest company guidance (number, range, direction or "no outlook"; Amazon and Oracle as reported by Reuters), ByteDance greyed in 2026, and, once checked, named analyst, consensus or research-firm forecasts for the look-ahead. Extra columns: forecaster, forecaster_type, forecast_date, measure, scope, selected_for_screen. The 2026E file is the 2026 subset. |
| `source/forecast_lookahead_2027_2031.csv` | Input for the look-ahead: one row per forecaster, company (or group) and year as the source states it, with its verbatim quote and VERIFIED/UNVERIFIED status. Empty until ChatGPT's look-ahead results are checked at source. |
| `source/alibaba_rescope_components.csv` | Alibaba's own re-presented figures used to rebuild its FY2018 quarters and June 2018 on its later scope (DEC-303). |
| `entity_name_history.csv`, `eligibility_additional_companies.csv`, `narrative_checkpoints.csv` | Name history; CoreWeave/ByteDance/Nvidia eligibility; turning points computed from the master. |
| `checks.json`, `manifest.json` | All checks; SHA-256 of every output. |

## How it was built (and how to rebuild)
1. `scripts/rtt103_fetch_sec.py` — SEC submissions + XBRL company facts (snapshot and manifest in the private repo, 28 MB).
2. `scripts/rtt103_sec_docs.py` — every 10-Q/10-K primary document from 2009; its cash-flow statement kept as text (private repo); URL and SHA-256 in `source/sec_filing_documents.csv`.
3. `scripts/rtt103_us_extract.py` — each line identified by its **printed label**; an XBRL value is used only if that exact number is printed on that row (`text_check = PASS`); untagged lines take the period of the purchases row's column. → `source/us_cashflow_observations.csv`.
4. `scripts/rtt103_sec_releases.py`, `scripts/rtt103_release_extract.py` — earnings releases (8-K exhibit 99) → Meta's capex figure, guidance and story candidates.
5. `.github/workflows/rtt103_sources.yml` + `scripts/rtt103_fetch_sources.py` — on a GitHub runner (no artifacts), the documents this container cannot reach (HKEXnews, Alibaba IR, Federal Reserve, company IR pages, TrendForce, SCMP); PDFs kept as text in the private repo with each file's SHA-256.
6. `scripts/rtt103_china_extract.py` — Baidu, Alibaba and Tencent figures read in those documents → `source/china_observations.csv`. `scripts/rtt103_fx.py` → `source/fx_cny_per_usd_daily.csv`.
7. `python scripts/build_rtt103_dataset.py data/rtt-103` — standard library only; same inputs give byte-identical outputs. Tests: `python tests/rtt103/run_tests_rtt103.py`.

## Rules in one paragraph
A quarter is the 3-month figure printed for it, or an exact year-to-date difference inside one definition, using the figures as first reported (later re-presentations kept and listed; a rounded first print gives way to a later exact print only within its rounding). No averaging, interpolation, dividing of annual totals, filling or zeros. TTM only from four consecutive valid quarters. RMB is converted quarter by quarter at the mean of the Federal Reserve H.10 daily rates over the actual fiscal quarter; company USD convenience translations are never used. Each fiscal quarter goes in the calendar quarter containing its end date; dates are never shifted. Guidance and estimates never enter the historical files.

## Rights
Public repo: SEC, HKEXnews and company figures with short verbatim quotes, Federal Reserve FX (public domain). Private repo only: the research catalogues (ChatGPT), the Sharadar extract and its cross-check (licensed; never published or shown), fetched documents and SEC snapshots (size).
