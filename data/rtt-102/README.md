# RTT-102 AI assistant websites race: data (phase 1, IQ-17)

Similarweb's published estimates of monthly website visits, worldwide, to eight AI assistant websites, Dec 2022 – Sep 2026. Contract: `reference/metric_contract_RTT-102.md`. Report: `reports/RTT-102_data_report.md`. Decisions DEC-500 to DEC-514 (`state/DECISIONS.md`). **Data only: nothing designed or rendered (DEC-069).**

Rebuild (deterministic): `python3 scripts/build_rtt102_dataset.py data/rtt-102 reports/RTT-102_data_report.md`. Tests: `python3 tests/rtt102/run_tests_rtt102.py`.

| File | What it holds |
|---|---|
| `identities.csv` | Each bar's name and web address with the dates they apply, and the sites not counted |
| `points.csv` | Every figure found: one row per bar, month and printed version, with source, data version, URL, wording seen at source, check, status, eligibility and whether it is used |
| `conflicts.csv` | Every bar-month with disagreeing versions: what Luke's rule settles, what is pending verification, what is left over for Luke |
| `series_monthly.csv` | The race: one row per bar per month, published or on a straight line, with label, address, flags and a proposed value label |
| `place_changes.csv` | Changes of first, second and third place |
| `turns.csv` | Points where a long straight line turns sharply (for the design session) |
| `CHECKS.md`, `checks.json` | The build's checks |
| `manifest.json` | SHA-256 of every file here |
| `source/` | The public source tables (below) |

`source/`:
- `publications.csv`: the 59 publications (research dossier section A), with data version (`older` before 28 Jul 2024).
- `observations_research.csv`: the dossier's 110 visits rows, with its 28 quarter-end rows of the 2025 table replaced by all 84 cells (written by `scripts/rtt102_import_research.py` from the private research, which is never committed: DEC-006).
- `observations_manual.csv`: figures added by hand from Cowork's checks (V-file), the dossier's revision cases (D, E, F) and the runner round R1, each with its origin.
- `verification.csv`: Cowork's checks at source, V01–V42, as recorded. `verification_map.csv`: which check confirms which figure, with the wording seen. `runner_checks.csv`: runner round R1, page by page (status, page SHA-256, dates).
- `exclusions.csv`: figures set aside, with the reason (DEC-509).
- `inputs_sha256.csv`: the private inputs and their SHA-256, all matching the private `00_README.md`.
