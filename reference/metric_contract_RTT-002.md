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
