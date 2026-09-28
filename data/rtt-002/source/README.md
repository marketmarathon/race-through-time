# RTT-002 source extraction (Wikipedia, CC BY-SA 4.0)

Retrieved 28 Sep 2026, 09:16–09:18 UTC, from en.wikipedia.org through the MediaWiki API, in Luke's Chrome (the cloud sandbox was rate-limited by Wikimedia with HTTP 429). Extraction code: `scripts/extract_wikipedia_f1_seasons.browser.js`. Each file was transferred to the build machine and verified by SHA-256 against a hash computed in the browser before use.

| File | SHA-256 | Content |
|---|---|---|
| `wikipedia_season_extract.psv` | `180fad720d91ad1b1bce5505de9d8f83e8a6c183625d535e2e25ec9d7f2559fa` | 77 season pages: `#season|title|revision|retrieved` header, then one line per round: `season|round|date|race article|winners[...]` |
| `wikipedia_driver_ids.psv` | `a160dabd7f86f44edb1e7a8615639821c0b115a1eab166e2e2c0034d461fe15c` | Winner link target → canonical title → page ID (Wikipedia redirects resolved) |
| `wikipedia_list_of_gp_winners.psv` | `383d8691af3cda78626c6814fca90f62cc16841d6b829ecf21007c7df0fed11a` | "List of Formula One Grand Prix winners" rev. 1376824402: canonical title, wins, first win, last win. Used only as a cross-check |

Rounds with an empty winners field are 2026 races not yet run at retrieval time (rounds 16–23; the source lists round 16, the Bahrain Grand Prix, for 4 Oct 2026).

To reproduce exactly, parse each season page at the recorded revision (`action=parse&oldid=<revision>`).

## Nationality (added 28 Sep 2026, IQ-05 round 3; DEC-035, DEC-036)

Retrieved 28 Sep 2026 in Luke's Chrome by Claude in Cowork through the MediaWiki and Wikidata APIs (Claude Code's cloud environment got HTTP 429 from Wikimedia on every request and did not work around it). Extraction code: `scripts/extract_nationality.browser.js` (its header explains the method). Delivered to the Claude Code session as a package (SHA-256 `7237669ea68f779ada9853f6c18bcf2fd4a0e532b08e8ff1dca132f5a000054b`, not committed); each file verified by SHA-256 before use. Built into `../driver_nationality.csv` by `scripts/rtt002_nationality.py`; comparison in `reports/RTT-002_nationality_comparison.md`.

| File | SHA-256 | Retrieved (UTC) | Content |
|---|---|---|---|
| `wikipedia_wikidata_nationality.psv` | `e041cff55f059f1ece3e91afd84a52a551754eb96546f52dbe448027775e9fb8` | Wikipedia 2026-09-28T18:10:25Z; Wikidata 2026-09-28T18:12:55Z | "List of Formula One Grand Prix winners" rev. 1376824402 (the same revision as above): per driver row the flag code and variant, wins, then the driver's Wikidata item, its last revision ID, P1532 (country for sport; `*` = preferred) and P27 (country of citizenship). `pageid|canonical_title|wp_flag_code|wp_flag_variant|wp_wins|wikidata_qid|wikidata_lastrevid|P1532|P27` |
| `wikidata_countries.psv` | `083a9cd05d6e18edb62f06bed7905980a6b9aede57699f93a4a09ce8ab43bd5c` | 2026-09-28 (with the Wikidata read above) | The countries named by those P1532 / P27 values: English label and P298 (ISO 3166-1 alpha-3). `qid|label_en|iso3_P298` |

Wikidata content is CC0; Wikipedia content CC BY-SA 4.0.
