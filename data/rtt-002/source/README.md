# RTT-002 source extraction (Wikipedia, CC BY-SA 4.0)

Retrieved 28 Sep 2026, 09:16–09:18 UTC, from en.wikipedia.org through the MediaWiki API, in Luke's Chrome (the cloud sandbox was rate-limited by Wikimedia with HTTP 429). Extraction code: `scripts/extract_wikipedia_f1_seasons.browser.js`. Each file was transferred to the build machine and verified by SHA-256 against a hash computed in the browser before use.

| File | SHA-256 | Content |
|---|---|---|
| `wikipedia_season_extract.psv` | `180fad720d91ad1b1bce5505de9d8f83e8a6c183625d535e2e25ec9d7f2559fa` | 77 season pages: `#season|title|revision|retrieved` header, then one line per round: `season|round|date|race article|winners[...]` |
| `wikipedia_driver_ids.psv` | `a160dabd7f86f44edb1e7a8615639821c0b115a1eab166e2e2c0034d461fe15c` | Winner link target → canonical title → page ID (Wikipedia redirects resolved) |
| `wikipedia_list_of_gp_winners.psv` | `383d8691af3cda78626c6814fca90f62cc16841d6b829ecf21007c7df0fed11a` | "List of Formula One Grand Prix winners" rev. 1376824402: canonical title, wins, first win, last win. Used only as a cross-check |

Rounds with an empty winners field are 2026 races not yet run at retrieval time (rounds 16–23; the source lists round 16, the Bahrain Grand Prix, for 4 Oct 2026).

To reproduce exactly, parse each season page at the recorded revision (`action=parse&oldid=<revision>`).
