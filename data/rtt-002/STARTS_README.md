# RTT-002 — race starts and win rate (added 29 Sep 2026, IQ-05 round 5; DEC-053)

Luke's decision (DEC-053): the text after every bar shows wins, starts and win rate, "91 wins · 306 starts · 29.7%". He chose **starts** (races actually started), not entries. Definition, source and rounding are in `reference/metric_contract_RTT-002.md`, "Display attributes" (written before the build, DEC-036).

These are **new files** (starts_corrections.csv added 29 Sep 2026, DEC-058). The audited dataset files (`races.csv`, `win_credits.csv`, `drivers.csv`, `career_totals.csv` and the rest, and `README.md`, `source/README.md`, `manifest.json`) were only read, not changed. Licence: CC BY-SA 4.0, derived from Wikipedia, as `ATTRIBUTION.md`; the starts come from the same season-page revisions listed there, plus the cross-check page below.

| File | What it is |
|---|---|
| `starts.csv` | 14,479 rows (after the DEC-058 correction): one per driver (the 116 of `drivers.csv`) per championship race started, in race order; the source cell(s) and the driver's career starts after that race; season page, revision, permanent link, retrieval time |
| `career_starts.csv` | Per driver at the freeze (2026 Azerbaijan GP): wins, starts, win rate, first start, and the "Race entries" / "Race starts" of "List of Formula One drivers" with AGREE / DISAGREE |
| `STARTS_CHECKS.md`, `starts_checks.json` | 13 scripted checks (all pass), the corrections applied, disagreements with the List page (none since DEC-058), round columns per season |
| `starts_corrections.csv` | Documented corrections applied after classification (DEC-058): one row, Barrichello 2002 Spanish GP = not a start, with reason and evidence |
| `starts_manifest.json` | SHA-256 of the source, the extraction code, the four dataset files read, the corrections file and every output |
| `source/wikipedia_starts_extract.psv` | The raw extraction (below) |

## Source

`source/wikipedia_starts_extract.psv`, SHA-256 `b26c0ed439d09b247462343c176c48964951291ec7058d8f476ef65ecdac9b64`, extracted 29 Sep 2026 04:49–04:52 UTC in Luke's Chrome by Claude in Cowork with `scripts/extract_starts.browser.js` (SHA-256 `ac8edfdb347fbf84a683ab570cbf14889797573afbf2127fac545034371d5845`; its header explains the method), because Wikimedia answers the cloud sandboxes with HTTP 429. Verified by SHA-256 before use.

- `#season` / `S` lines: each season's World Drivers' Championship results table, at the **same revision** as the wins data (checked for all 77 seasons against `races.csv`): round headers, then per driver row the driver link and one cell per round (footnote `<sup>` removed, nothing classified).
- `#list_of_f1_drivers` / `L` lines: "List of Formula One drivers", revision **1377016608** (https://en.wikipedia.org/w/index.php?oldid=1377016608): race entries, race starts, race wins. Cross-check only.
- `T` lines: every link title resolved to its canonical title and page ID (`driver_id` = "wp" + page ID).

## Results

- Every season's round columns, after dropping the empty-header separator column (1967, 1968, 1969, 1970, 1972, 1975, 1976, 1979), equal `races.csv` (2026: 23 listed, 15 run).
- Every one of the 1,167 win credits has a start at that race (0 exceptions).
- Career starts at the freeze equal the List page for **116 of 116** drivers. (Build 1.0 had 115: Rubens Barrichello 323 from the season tables against 322 in the List page. Independent check 3 found the cause, the 2002 Spanish GP, where the table shows "Ret" but he did not take the start; Luke corrected it, DEC-058, by `starts_corrections.csv`. He now has 322.)
- Michael Schumacher: 91 wins · 306 starts · 29.7% (Luke's example).

## Independent check 3 and the counting convention (29 Sep 2026)

Independent check 3 (ChatGPT deep research, run by Luke; frozen in `state/RTT-002_independent_check3_freeze.json`; report `reports/RTT-002_starts_check3_report.md`) agrees with this data for all 16 season-end points checked, 34 of 36 first-win start numbers and 102 of 109 career totals it could settle. The one data error it found (Barrichello, above) is corrected. The rest are a counting convention.

**Convention (DEC-059, Luke):** starts follow Wikipedia's convention: relief drives (a driver who took over another car without taking the start himself) and Formula 2 cars that ran in the same championship Grand Prix count as starts. Some statistics sources exclude them (hence the check's lower figures for Jack Brabham, Graham Hill, Luigi Musso and Pat Flaherty). Three one-start conflicts between sources for drivers who never appear on screen (Johnny Herbert, Pedro Rodríguez, François Cevert) are kept at Wikipedia's figure and listed in the report.

**Methodology note for the video description:** "Starts and win rates follow Wikipedia's Formula One driver statistics; relief drives and Formula 2 entries in championship Grands Prix count as starts."

## How to rebuild

```
python scripts/rtt002_starts.py data/rtt-002
```
Standard library only; the same inputs always give byte-identical outputs (hashes in `starts_manifest.json`). The build stops on any failed check or any cell value the rules do not name.
