# CODE SESSION IQ-16 (check the number is still free) — RTT-103 The AI Spending Race: data build, stage 1

Drafted by Cowork 7 Oct 2026. Approved by Luke to send 7 Oct: this build goes first, ahead of the RTT-101 and RTT-102 Code work (both still in research). Cowork checked on 7 Oct that IQ-16 was free (only IQ-15 exists) and that the highest DEC across main and open pull requests was DEC-277 (branch `claude/nice-davinci-guln5e`, PR #19); re-check both before numbering.

---

You are building the data for a Race Through Time episode, RTT-103 "The AI Spending Race — How Big Tech Started Spending Hundreds of Billions": a bar-chart race of trailing-12-month capital expenditure, nominal US$, from about 2010 to the latest common complete quarter. **Data only: no player, renderer, render or visual changes.** Luke is not technical: finish with a short plain-English summary for him.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-16.md` (use the real IQ number if 16 is taken).

## READ FIRST
`CLAUDE.md` (repo), `state/HANDOVER.md`, `state/STATE.json`, then only the DEC numbers you need from `state/DECISIONS.md` (at least DEC-006, DEC-036, DEC-057, DEC-069). Check main AND open pull requests and branches before choosing IQ and DEC numbers.

## INPUTS (private: `marketmarathon/race-through-time-private`, folder `research/rtt-103/`; never copy them into the public repo, DEC-006)
Also there: `CODE_SESSION_IQ-16_RTT-103_data.md` (this message). Check each input's SHA-256 against the values below and `00_README.md` before using it; stop and report any mismatch.
1. `part00_brief_pasted_text.txt` — **the authoritative research brief** (methodology, sections A–L, exact CSV schemas, response order). SHA-256 13d3ba0ee17e0ba5baed55892b8d98b33c9fb4afa3d4e5f71db8d34b7bb657ad, 28,273 bytes. Follow it; where this message is more specific, this message wins; where they conflict, stop and list the conflict for Luke.
2. `part01_sectionA_source_catalogue.csv` — ChatGPT's Section A, 65 sources. SHA-256 61e9420c16878d13cd5e1b45f564ffccb5710fd35d8465e5bcea7d6275023c82. Unchecked leads. Preserve every source_id; add new IDs, never reuse or rewrite old ones.
3. `sharadar_2026-08-08/sharadar_fundamentals_rtt103.csv` + `_manifest.json` — rows for AMZN, MSFT, GOOGL, META, ORCL, BABA, BIDU, CRWV from Market Marathon's Sharadar download of 8 Aug 2026 (licensed vendor data: private only, never published, never on screen). Quarterly as-reported capex present 2009 Q2–2026 Q2: Amazon, Microsoft, Alphabet, Oracle complete; Meta from 2012 Q1; Alibaba 45 quarters (CNY); Baidu capex blank. Use it ONLY as (a) a finding list of periods and filing dates and (b) an independent cross-check. Its `capex` field may be defined differently from cash purchases of PP&E — establish Sharadar's definition before comparing, and log every difference in `I_conflicts_and_warnings.csv`; never let it overwrite a filing value.
4. ChatGPT's Section A expansion for the China-listed companies (received 7 Oct; unchecked leads; the finding list for these three): `part02b_china_prompt_tencent_Section_A_file.txt` (SHA-256 2d6962d9459ed44ff3cfb891178d6564f5a11edc070ea078db28b39b11f86f11; SRC-TENC-007–121, 69-quarter coverage grid, 22 warnings), `part03b_china_prompt_baidu_Section_A_file.txt` (024d5983afd2d069cb14efd2608addd1b90dee30cc41cdc3dadf6d7a305cf342; SRC-BAIDU-009–165, all 69 quarters found, 29 warnings), `part04b_china_prompt_alibaba_Section_A_file.txt` (6273789a3ff750d54227ef27e1f0d418b5e0331359ee34d034a97f3cd70dec5b; SRC-BABA-007–095; 15 pre-IPO quarters NOT PUBLIC, 23 warnings), plus Cowork's check notes `00_README.md`. Each file holds three CSV blocks (catalogue, coverage, conflicts). Append their catalogue rows to Section A unchanged; map "Alibaba Group Holding Limited" and "Alibaba" to one company_id. Key points from Cowork's checks (UNVERIFIED): Tencent quarterly capex only from 2011 (as 2012 comparatives) and its cash PP&E only half-yearly; Baidu quarterly capex every quarter from 2009 Q2 (cash basis explicit only from 2015); Alibaba group quarters from Mar 2013 (component-level for Mar and Jun 2013), with scope breaks in 2017–2019.

## SCOPE OF STAGE 1
- **Full build (sections A–L, both masters) for Amazon, Microsoft, Alphabet (incl. Google, CIK 1288776), Meta, Oracle**, from SEC EDGAR: filing index, XBRL company facts, and the filing documents themselves. data.sec.gov is blocked from the Cowork cloud; use a GitHub Actions runner (declare a User-Agent with luke@marketmarathon.com, respect SEC rate limits). Commit raw SEC snapshots with a SHA-256 manifest (public data; public repo is fine if small, otherwise private repo).
- **Tencent, Baidu and Alibaba: full build too**, using input 4 as the finding list: Baidu and Alibaba from their SEC 6-K/20-F/F-1 filings and issuer PDFs, Tencent from HKEXnews PDFs (fetch on a GitHub runner if blocked from the container). Original RMB only; USD convenience translations are never used. Quarters the lists mark NOT FOUND or NOT PUBLIC stay so in H, never zero. If time runs short, finish the five US companies first and report exactly which China-listed quarters remain.
- **ByteDance:** no historical series (brief §30); estimates only in F/2026E, labelled. **CoreWeave:** eligibility table only (brief §2); not added to the race without Luke's approval.

## HOW TO BUILD (brief §§3–10, 15, 25)
- Two series where disclosures allow: A company-reported capex; B cash purchases of PP&E. Separate cash purchases, finance-lease additions, finance-lease principal, financing obligations, acquisitions and intangibles. Definition history per company in `C_capex_definitions.csv` with breaks flagged.
- Quarters derived from year-to-date figures only by exact subtraction of compatible figures, labelled DERIVED_FROM_PRIMARY_SOURCE with both inputs, both sources and the formula. No derivation across a definition change. Never divide annual totals, interpolate, fill or zero.
- **Every XBRL value is checked against the filing text** (script: find the printed figure in the cash-flow statement of the cited filing; record pass/fail). Restated or amended values are kept side by side with `superseded` set, never overwritten.
- Quarters must sum to the fiscal year (§25). TTM only from four consecutive valid quarters.
- FX for RMB quarters: Federal Reserve H.10 daily CNY per USD (FRED DEXCHUS as distributor), mean of the available daily rates within each actual fiscal quarter; record rate, day count and source; never fill missing days. USD TTM = sum of four converted quarters.
- `calendar_quarter_bucket` = the calendar quarter containing the fiscal period end (brief §6), so Oracle's quarter ending 31 May falls in Q2. Never alter period dates.
- `LATEST_COMMON_COMPLETE_QUARTER` from the companies in the canonical race only; one company's later release never advances it. Candidate from the catalogue: quarter ending 30 Jun 2026 (UNVERIFIED).
- 2026 guidance and estimates only in `F_2026_capex_forecasts.csv` and `AI_SPENDING_RACE_2026E.csv`, every row labelled GUIDANCE or ESTIMATE; prior guidance ranges kept.
- Story events (G): sourced management statements only; commitments (e.g. Anthropic, Reuters 29 Sep 2026) classified as COMMITMENT, never capex.
- Exact file names and columns: brief §§16–28 and §34. Extra audit fields go in companion files (e.g. `B_capex_observations_audit.csv`), never as extra columns in the brief's files.
- Synthetic test fixtures are allowed for tests only, labelled SYNTHETIC in name and content, and kept out of `data/`.

## HARD RULES
Never touch `marketmarathon/bars` or any Market Marathon file. Nothing uploaded or published. Never invent, average, guess between disagreeing sources or use a forecast as an actual: record each version and list it for Luke. Only VERIFIED figures may be marked for the screen. No new visual features (DEC-069). Do not install software or change settings, secrets or permissions without asking. Never print RTT_PRIVATE_TOKEN; no workflow artifacts from the public repo.

## OWNER DECISIONS to record as new DEC entries
1. ALREADY RECORDED by the IQ-15 session on PR #19 (one of DEC-235–246): find it and cite it; do not record it twice. (Luke, Cowork chat, 7 Oct 2026) New episode "The AI Spending Race — How Big Tech Started Spending Hundreds of Billions", taken over from his ChatGPT project, run under the brief above: TTM capex race in nominal US$, about 2010 to the latest common complete quarter; two series kept, canonical chosen after coverage is assessed; ByteDance out of the historical race unless robust quarterly evidence exists; CoreWeave candidate only; no estimated, interpolated or divided quarters; 2026 projections separate and labelled.
2. (Luke, Cowork chat, 7 Oct 2026) Episode number RTT-103. The RTT-103 data build goes first, before the RTT-101 and RTT-102 Code work, which are still in the research phase.
3. (Luke, Cowork chat, 7 Oct 2026) Research split: the US companies from a Sharadar draft checked against their SEC filings by an automated job; Tencent, Baidu and Alibaba's early years from a ChatGPT list of the companies' own reports, then checked at source.
4. (Luke, Cowork chat, 7 Oct 2026) No EODHD upgrade for this episode (his account is on the free plan).

## CLAUDE'S WORKING CHOICES (record as working choices; list each as a question for Luke)
- FX method above (H.10 daily mean over the actual fiscal quarter).
- Sharadar used only as finding list and cross-check, never as evidence.
- Canonical series: no choice yet — recommend one in `K` after measuring coverage (Cowork's provisional lean: cash PP&E, because it is printed by every company and reproducible).

## DELIVERABLES AND REPORT
Files A–L and the two masters for the stage-1 companies under `data/rtt-103/`, a coverage matrix showing exactly which quarters are A_REPORTED / DERIVED_PRIMARY / NOT_FOUND, `J_QA_report.md` with PASS/FAIL per company, and `reports/RTT-103_data_report.md` with numbered questions for Luke (each with your recommendation and what happens if he does not answer). State clearly which results are file-format checks and which are financial QA.

## STATE
Update `state/STATE.json`, `state/HANDOVER.md`, `state/DECISIONS.md`. Push a branch and open a pull request against main; **do not merge** (DEC-057). Stop after opening it and give Luke a short plain-English summary: what was built, what passed, what is missing, and what he needs to decide.
