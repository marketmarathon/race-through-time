# RTT-104 Women in Parliament — data (IQ-20, 10 Oct 2026)

**Status: data built; episode BLOCKED** for design, render and publishing until Luke answers the rights question (DEC-614; `reports/RTT-104_data_report.md` question 1).

- Contract: `reference/metric_contract_RTT-104.md`. Report: `reports/RTT-104_data_report.md`.
- Build: `python3 scripts/build_rtt104_dataset.py data/rtt-104 reports/RTT-104_data_report.md` (deterministic; reads only `config.json` and `source/`).
- Tests: `python3 tests/rtt104/run_tests_rtt104.py` (two clean rebuilds identical, traceability, threshold, no 0% where missing, no forecast, closing-card quotes).
- Sources: fetched on a GitHub runner by `.github/workflows/rtt104_sources.yml` (`scripts/rtt104_fetch_sources.py`), committed to this branch:
  - `source/fetch_2026-10-10_run38029495926/` — round 1: WDI API JSON (SG.GEN.PARL.ZS, WLD, SP.POP.TOTL, country list, metadata), OWID CSV and metadata (all byte for byte in `raw/`), plus excerpts of the terms and metadata pages.
  - `source/fetch_2026-10-10_run38029895756_parline/` — round 2: IPU Parline pages for the economies with no 2025 figure (excerpts only).
  - `source/fetch_2026-10-10_run38030108879_archive/` — round 3: IPU archived monthly rankings (rows for the test countries only), for the reference-date test.
  - Every file's URL, UTC time, HTTP status, bytes and SHA-256: each folder's `fetch_manifest.json`. Web pages are never kept whole.
- Hand-written inputs: `source/short_names.csv` (DEC-616), `source/closing_card_reasons.csv` (DEC-613, DEC-622), `source/reference_date_findings.md` (DEC-621), `source/report_questions.md`.
- The fetch workflow runs on a push that changes it or its script on this branch; `FETCH_SET` picks the round (empty = round 1).
