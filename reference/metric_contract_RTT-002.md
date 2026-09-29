# Metric contract — RTT-002 F1 Grand Prix Wins · DRAFT v0.2 (not signed off) · 27 Sep 2026

**Public claim:** Most Formula 1 World Championship Grand Prix wins by driver, 1950 → last completed Grand Prix before data freeze.
**Unit:** wins (integer). **Rank:** descending cumulative wins.
**Universe:** every driver classified first in a World Championship Grand Prix. Full candidate universe kept, not just today's top ten.
**Excluded:** Sprint races; non-championship F1 races; pole positions, podiums, titles.
**Event time:** race date. The count changes only on a race date. Bars may glide to new positions; the displayed number never shows fractions.
**Timeline:** race-by-race, compressed through quiet stretches (adaptive pacing within 0.8–1.4×, per blueprint).
**2026:** partial season; cutoff = last completed Grand Prix at freeze, stated on screen and in the description.

## Defaults proposed (you can override)
| Question | Proposed default | Reason |
|---|---|---|
| Indianapolis 500, 1950–60 (championship rounds) | Follow the official F1 results classification; state the treatment in the description | Source precedence, not personal judgement |
| Shared drives credited as wins | Credit each driver the official record credits | Same |
| Ties in rank | Driver who reached the total first ranks higher | Stable, explainable, no invented data |
| Identity | One row per driver; name as officially recorded | Drivers do not merge |

## Sources
1. **Production:** Wikipedia list of Formula One Grand Prix winners and season pages — CC BY-SA 4.0; attribution in the description; our derived dataset published under CC BY-SA 4.0.
2. **Independent check:** ChatGPT deep research, run by Luke, blind (prompt: prompts/RTT-002_independent_check.md). Seeded sample seasons: 1959, 1965, 1980, 1990, 2001, 2012, 2013, 2021 (Python `random.Random(20260927).sample(range(1950, 2026), 8)`).
3. **Official site (formula1.com):** eyeball individual decisive results only. Its guidelines assert copyright and database rights over results data and forbid substantial or commercial reuse or scraping.
4. **Excluded:** Jolpica/Ergast (CC BY-NC-SA 4.0) unless written commercial permission is obtained.
5. **Presentation:** no F1 logos or team marks; "F1"/"Formula 1" used descriptively in titles only.
6. **Open before release:** D-05 (publication risk).

## Checks before DATA_AUDIT passes
- Wins per season = championship races held (shared-drive adjustments explicit).
- Final table matches official career-win totals for the top 20.
- Every change of all-time leader and every top-ten entry reconstructed independently from source 2.
- Seeded random sample ≥ 10% of remaining race winners.
- No row created by interpolation; missing = NOT FOUND, never zero.

## Claims this data cannot support
"Greatest driver", "most dominant", win rate (unless computed and labelled), anything about Sprints, poles or titles.

## Display attributes (added 28 Sep 2026, IQ-05 round 3; DEC-036; starts and win rate added 29 Sep 2026, DEC-053)
Every attribute the video displays, with its source. **Process lesson (DEC-036, Luke):** nationality should have been captured from the outset. It was added late, on 28 Sep 2026, after DATA_AUDIT had passed, when Luke asked for a flag next to each driver's name (DEC-034). Future metric contracts list every displayed attribute and its source before the data build (DEC-036).

| Attribute shown | Source | File | Added |
|---|---|---|---|
| Driver name | Wikipedia season pages (display name = page title without disambiguation) | `data/rtt-002/drivers.csv` | data build, 28 Sep 2026 |
| Win count after each race | Wikipedia season pages | `data/rtt-002/win_credits.csv` | data build |
| Season, Grand Prix, date (time block; "GP" short form in the event label) | Wikipedia season pages | `data/rtt-002/races.csv` | data build |
| Nationality (flag) | Primary: the flag in each driver's row of Wikipedia's "List of Formula One Grand Prix winners", revision 1376824402 (the revision already used as a cross-check), codes mapped to ISO 3166-1 alpha-3. Cross-check: Wikidata P1532 (country for sport), else P27 (citizenship). Disagreements listed for Luke, never resolved by guessing; the Wikipedia value is used. Flag drawn = today's design of that country's flag (DEC-035), from flag-icons (MIT) | `data/rtt-002/driver_nationality.csv`; `reports/RTT-002_nationality_comparison.md` | **late: 28 Sep 2026** (after DATA_AUDIT) |
| Race starts after each race (label "306 starts") | Primary: each season's World Drivers' Championship results table on Wikipedia, at the SAME revision as the wins data (the 77 season-page revisions in `races.csv`), extracted in Luke's Chrome by `scripts/extract_starts.browser.js` into `data/rtt-002/source/wikipedia_starts_extract.psv` (SHA-256 `b26c0ed4…ecdac9b64`). Cross-check: "Race starts" column of Wikipedia's "List of Formula One drivers" (revision recorded in the source file; 1377016608). Disagreements listed for Luke, never resolved by guessing; the season-table value is used | `data/rtt-002/starts.csv`, `career_starts.csv`, `STARTS_CHECKS.md` (built by `scripts/rtt002_starts.py`); corrections `starts_corrections.csv` (DEC-058); independent check 3 `reports/RTT-002_starts_check3_report.md` | **29 Sep 2026** (DEC-053; listed here before the build, DEC-036; convention DEC-059) |
| Win rate after each race (label "29.7%") | Computed: wins after the race (`win_credits.csv`) ÷ starts after the race (`starts.csv`) | computed by the player from the adapter output; checked on every frame against the CSVs | **29 Sep 2026** (DEC-053) |

**Starts (DEC-053, Luke, 29 Sep 2026).** Luke chose race STARTS (races actually started), not entries (Wikipedia: Michael Schumacher 308 entries, 306 starts). A driver has a start at a championship race when that season's Drivers' Championship table cell for that round shows a classified position (a number), Ret, NC or DSQ, including any part of a shared or swapped-car cell such as "2†/ Ret"; DNS, DNQ, DNPQ, WD, EX, DNA, DNP or an empty cell is not a start. Before classifying: drop the "Race: …; Sprint: …" annotation (the race result is the first token; a Sprint start is never a start), strip brackets and the marks † ‡ * ^ ~, split the cell on "/" and classify the first token of each part; any other value stops the build. Columns with an empty header are dropped (the 1967–1979 tables have one separator column); round columns map to `races.csv` by order; for 2026 only the 15 completed rounds count. The Indianapolis 500 of 1950–1960 counts (DEC-012). One start per driver per race, even with several cars. Rows match drivers through Wikipedia page IDs (`driver_id` = "wp" + page ID); the "Formula Two" separator rows are not drivers. A missing value is NOT FOUND, never zero.

**Counting convention (DEC-059, Luke, 29 Sep 2026).** Starts follow Wikipedia's convention: a relief drive (a driver who took over another car without taking the start himself) and a Formula 2 car that ran in the same championship Grand Prix both count as starts, because the season tables show a result for them. Independent check 3 (`reports/RTT-002_starts_check3_report.md`) showed that some statistics sources (e.g. StatsF1) exclude these, which explains its differences for Jack Brabham, Graham Hill, Luigi Musso and Pat Flaherty. **Methodology note for the video description:** "Starts and win rates follow Wikipedia's Formula One driver statistics; relief drives and Formula 2 entries in championship Grands Prix count as starts."

**Documented corrections (DEC-058, Luke, 29 Sep 2026).** Where the season table is shown to be wrong, the start is corrected in `data/rtt-002/starts_corrections.csv`, applied by the build after classification and reported in its checks; the source extract is never edited. One correction: Rubens Barrichello, 2002 Spanish Grand Prix (race_index 685) is NOT a start (table "Ret"; he did not take the start; Wikipedia's "List of Formula One drivers" rev. 1377016608, independent check 3 section M and GP Racing Stats all give 322). Career starts then equal the List page for all 116 drivers.

**Win rate (DEC-053).** Win rate = wins ÷ starts at that moment (both counted after the race shown), as a percentage with one decimal, **rounded half up** (e.g. 1/8 = 12.5%, 1/16 = 6.25% → 6.3%, 91/306 = 29.738…% → 29.7%). Computed with exact decimal/integer arithmetic, never binary floating point; always one decimal ("100.0%", "6.0%"). Shown only on bars, so wins ≥ 1 and starts ≥ 1. Label: "<wins> wins · <starts> starts · <rate>%" ("1 win", "1 start"). The numbers step only at races; nothing in between is shown. This is the labelled, computed win rate the "Claims this data cannot support" line allows; it describes the record, it does not claim "most dominant".

Nationality means the country the driver raced under (racing-licence nationality), following the official Formula 1 treatment (DEC-012). The nationality file and the starts files are new files; the audited dataset files were not changed.
