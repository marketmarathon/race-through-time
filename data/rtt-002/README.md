# RTT-002 — F1 World Championship Grand Prix wins, 1950 → 2026 Azerbaijan GP

Status: **DATA_BUILD complete, merged to `main`** (pull request #1). DATA_AUDIT still open: second independent check on top-ten entries in progress (D-07). Not greenlit for render.
Contract: `reference/metric_contract_RTT-002.md` v0.2. Rules confirmed by Luke 28 Sep 2026 (DEC-012): follow the official Formula 1 treatment.
Licence: CC BY-SA 4.0, derived from Wikipedia — see `ATTRIBUTION.md`.

**Data freeze:** last completed Grand Prix before 28 Sep 2026 = **2026 Azerbaijan Grand Prix, 26 Sep 2026** (15 of 23 rounds of 2026 completed).

## Files

| File | What it is |
|---|---|
| `races.csv` | 1,164 completed championship races. Date, Grand Prix, winner(s), and for every row the Wikipedia page, revision ID, permanent link and retrieval time |
| `win_credits.csv` | 1,167 win credits in race order (three shared drives credit two drivers each), with each driver's running total |
| `cumulative_wins_wide.csv` | Race-by-race cumulative wins, one column per driver (116), whole numbers only. Column order = `drivers.csv` order |
| `career_totals.csv` | Wins per driver at the freeze, ranked; ties ranked by who reached the total first |
| `record_progression.csv` | 118 events: every time a driver became sole holder, equalled, or extended the all-time wins record |
| `drivers.csv` | Stable driver IDs (`wp<Wikipedia page ID>`), Wikipedia title, display name |
| `CHECKS.md`, `checks.json` | Scripted checks (all pass) |
| `manifest.json` | Input and output SHA-256 hashes, every source revision |
| `source/` | The raw extraction from Wikipedia, exactly as retrieved (see `source/README.md`) |

## How to rebuild

```
python scripts/build_rtt002_dataset.py data/rtt-002
```
Standard library only; the same `source/` files always give byte-identical outputs (hashes in `manifest.json`).

## Rules (DEC-012: follow the official Formula 1 treatment)

- **Indianapolis 500, 1950–1960:** included (11 races). They counted towards the World Championship, and formula1.com treats these wins as World Championship Grand Prix wins. State this in the video description.
- **Shared drives:** each credited driver gets one full win (1951 French GP Fangio + Fagioli; 1956 Argentine GP Musso + Fangio; 1957 British GP Brooks + Moss). The season's race count is unchanged.
- **Ties in rank (display rule, no official rule exists):** the driver who reached the total first ranks higher.
- **Identity:** one row per driver, keyed by Wikipedia page ID; redirect variants merged (Pedro Rodriguez → Pedro Rodríguez; Jim Rathmann (race car driver) → Jim Rathmann).

## What this data cannot support

"Greatest driver", "most dominant", win rates (unless computed and labelled), anything about Sprints, poles or titles.
