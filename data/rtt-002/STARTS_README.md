# RTT-002 — race starts and win rate (added 29 Sep 2026, IQ-05 round 5; DEC-053)

Luke's decision (DEC-053): the text after every bar shows wins, starts and win rate, "91 wins · 306 starts · 29.7%". He chose **starts** (races actually started), not entries. Definition, source and rounding are in `reference/metric_contract_RTT-002.md`, "Display attributes" (written before the build, DEC-036).

These are **new files**. The audited dataset files (`races.csv`, `win_credits.csv`, `drivers.csv`, `career_totals.csv` and the rest, and `README.md`, `source/README.md`, `manifest.json`) were only read, not changed. Licence: CC BY-SA 4.0, derived from Wikipedia, as `ATTRIBUTION.md`; the starts come from the same season-page revisions listed there, plus the cross-check page below.

| File | What it is |
|---|---|
| `starts.csv` | 14,480 rows: one per driver (the 116 of `drivers.csv`) per championship race started, in race order; the source cell(s) and the driver's career starts after that race; season page, revision, permanent link, retrieval time |
| `career_starts.csv` | Per driver at the freeze (2026 Azerbaijan GP): wins, starts, win rate, first start, and the "Race entries" / "Race starts" of "List of Formula One drivers" with AGREE / DISAGREE |
| `STARTS_CHECKS.md`, `starts_checks.json` | 12 scripted checks (all pass), the disagreement with the evidence, round columns per season |
| `starts_manifest.json` | SHA-256 of the source, the extraction code, the four dataset files read and every output |
| `source/wikipedia_starts_extract.psv` | The raw extraction (below) |

## Source

`source/wikipedia_starts_extract.psv`, SHA-256 `b26c0ed439d09b247462343c176c48964951291ec7058d8f476ef65ecdac9b64`, extracted 29 Sep 2026 04:49–04:52 UTC in Luke's Chrome by Claude in Cowork with `scripts/extract_starts.browser.js` (SHA-256 `ac8edfdb347fbf84a683ab570cbf14889797573afbf2127fac545034371d5845`; its header explains the method), because Wikimedia answers the cloud sandboxes with HTTP 429. Verified by SHA-256 before use.

- `#season` / `S` lines: each season's World Drivers' Championship results table, at the **same revision** as the wins data (checked for all 77 seasons against `races.csv`): round headers, then per driver row the driver link and one cell per round (footnote `<sup>` removed, nothing classified).
- `#list_of_f1_drivers` / `L` lines: "List of Formula One drivers", revision **1377016608** (https://en.wikipedia.org/w/index.php?oldid=1377016608): race entries, race starts, race wins. Cross-check only.
- `T` lines: every link title resolved to its canonical title and page ID (`driver_id` = "wp" + page ID).

## Results

- Every season's round columns, after dropping the empty-header separator column (1967, 1968, 1969, 1970, 1972, 1975, 1976, 1979), equal `races.csv` (2026: 23 listed, 15 run).
- Every one of the 1,167 win credits has a start at that race (0 exceptions).
- Career starts at the freeze equal the List page for **115 of 116** drivers. **One disagreement, for Luke, not resolved:** Rubens Barrichello, **323** from the season tables against **322** in the List page. The 94 candidate races (counted starts whose cell shows Ret, NC or DSQ) are listed in `STARTS_CHECKS.md`; the task names the 2002 Spanish GP ("Ret" in the 2002 table) as an example. The season-table value, 323, is used.
- Michael Schumacher: 91 wins · 306 starts · 29.7% (Luke's example).

## How to rebuild

```
python scripts/rtt002_starts.py data/rtt-002
```
Standard library only; the same inputs always give byte-identical outputs (hashes in `starts_manifest.json`). The build stops on any failed check or any cell value the rules do not name.
