# RTT-003 — Best-Selling Consoles 1985–2026 (units shipped)

Status: **DATA BUILD (IQ-09), 1 Oct 2026; owner answers applied 2 Oct 2026 — pull request #12, not merged** (DEC-069). **Round-4 data update (IQ-10, DEC-134, 2 Oct 2026):** Xbox Series X|S (VGChartz to Jun 2026), Xbox 360 (85.73m at 20 Apr 2016), Atari 2600 (27.64m at 1 Jan 1992), Master System (Famitsu No. 259), Sega end dates; build 1.1 adds each bar's `status` (live / latest_figure / retired, DEC-131/DEC-132/DEC-135). **Round 5 (DEC-139, DEC-140, 3 Oct 2026):** Nintendo's quarterly Switch figures (Jun 2024 to Dec 2025), Famitsu No. 259's Mega Drive and Game Gear for Mar 1993, documented end-of-production reports as evidence; build 1.2 applies rule 2 (retired = manufacturer's final total or documented end; latest figure only with neither).
Contract: `reference/metric_contract_RTT-003.md` v1.0. Owner decisions DEC-081 to DEC-085; Claude's working choices DEC-086 to DEC-092, confirmed by Luke on 2 Oct 2026 (DEC-093 to DEC-102).
Report for Luke: `reports/RTT-003_data_report.md`. Source access test: `reports/RTT-003_source_access.md`.

**Race:** quarter ends from 31 Mar 1985 to 30 Jun 2026 (166 quarter ends). **Metric:** cumulative worldwide hardware units shipped (sell-in), by console family as the manufacturer groups it.

## Files

| File | What it is |
|---|---|
| `consoles.csv` | One row per console considered (in scope and excluded, with the reason). Display attributes: name, other names, models included, maker, maker colour key, type, launch date and region, fade date and basis, `picture_ref` (empty until the player session), end value, best rank; `latest_figure_from`, `retired_from`, `status_basis` (build 1.1) |
| `observations.csv` | Every figure used or considered: date, units, qualifier, lower-bound flag, basis, geography, grade (A–D), analyst flag, forecast flag, arithmetic flag and derivation, source title, publisher, URL, a short verbatim quote from the source (under 25 words), `verified` (yes / no / UNVERIFIED = source blocked), `used` (yes / no) and why, the figure it disagrees with |
| `series.csv` | One row per console per quarter end from launch (or 31 Mar 1985): units, millions, provenance (official / arithmetic / estimate / interpolated / held), lowest grade it rests on, display style (official / estimated / analyst_estimate), "+" flag, unverified flag, the two anchors it rests on, and `status` (live / latest_figure / retired; build 1.1) |
| `series_by_maker.csv` | Per-maker totals per quarter end (input for the company scoreboard Luke wants tested in the pilot) |
| `crown.csv` | Every change of first place, with what it rests on |
| `overtakes.csv` | Every overtake inside the top ten, with what it rests on |
| `CHECKS.md`, `checks.json` | Scripted checks |
| `manifest.json` | SHA-256 of every input and output |
| `source/consoles_curated.csv` | Hand-curated console list (input) |
| `source/observations_curated.csv` | Hand-checked figures (input); every row checked against its source on 1 Oct 2026 or marked UNVERIFIED |
| `source/nintendo_fy_hardware.csv` | Nintendo's fiscal-year hardware units, transcribed from Nintendo's spreadsheet by `scripts/rtt003_extract_nintendo.py` (the spreadsheet itself is not committed; its SHA-256 is in `nintendo_fy_hardware.source.txt`) |
| `source/sony_business_data.csv` | Sony's lifetime totals and PS4/PS5 quarterly sell-in, transcribed from Sony's business-data page by `scripts/rtt003_extract_sony.py` |
| `source/report_notes.md` | Hand-written parts of the report (summary, questions for Luke) |

## How to rebuild

```
python scripts/build_rtt003_dataset.py data/rtt-003 reports/RTT-003_data_report.md
```
Standard library only; the same `source/` files always give byte-identical outputs (hashes in `manifest.json`). Re-transcribing the Nintendo spreadsheet needs `openpyxl` (`scripts/rtt003_extract_nintendo.py <xlsx> data/rtt-003/source`).

## Rules in one paragraph
A bar uses a dated figure where one exists; between dated figures it follows a straight line (each console is 0 on its launch date); after its last figure it is held flat. Nothing before launch. Missing figures are NOT FOUND, never zero, never invented. Disagreeing sources are never averaged: the higher grade is used, the other recorded and listed. Forecasts are never used. A change of basis (e.g. Sony production shipments to sell-in) is never shown as a fall in sales. Grades: A manufacturer worldwide; B manufacturer regional, sum of same-date manufacturer regions, or manufacturer figure with unstated geography; C press or magazine quoting the company; D analyst or other estimate.

## Rights
Figures are facts taken from manufacturers' published data and the press; quotes are short excerpts for verification only. No images, logos, scans or research-assistant text are committed (DEC-006). The private research ledger used as leads (`race-through-time-private/research/rtt-003-chatgpt/`) is referenced by row number only (`ledger_rows`).
