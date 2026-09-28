# Rights ledger — Race Through Time

Every third-party or owner asset the RTT player draws or ships, with its licence as read from the licence file itself. Started 28 Sep 2026 (IQ-05 round 3, `prompts/CODE_SESSION_IQ-05c.md`). Public-repo rule (DEC-006): code, configs, data files and written results only; no renders, stills, logos, pictures or other media are committed. Update this file whenever an asset is added or its source changes.

## Drawn in the video

| Asset | Where it comes from | Version | Licence (read from) | Obligations | Committed? |
|---|---|---|---|---|---|
| Archivo typeface (400, 500, 600, 700) | npm `@fontsource/archivo`, installed by `npm ci` in `kits/rtt-002/` | 5.3.0 | SIL Open Font License 1.1 (`node_modules/@fontsource/archivo/LICENSE`, "Copyright 2020 The Archivo Project Authors"; package.json `"license": "OFL-1.1"`) | Use in videos is allowed; the font files may not be sold on their own; the licence must go with any redistribution of the font files (we do not redistribute them) | No (node_modules is git-ignored) |
| National flags (today's design of each flag, DEC-035) | npm `flag-icons`, `flags/4x3/<iso alpha-2>.svg`, installed by `npm ci` in `kits/rtt-002/` | 7.5.0 | MIT (`node_modules/flag-icons/LICENSE`, "Copyright (c) 2013 Panayiotis Lipiridis"; package.json `"license": "MIT"`) | Keep the copyright and permission notice with copies of the software; images drawn into a video frame carry no further obligation under MIT. National flags themselves are public symbols; no flag is altered | No — no flag file is committed |
| Race data (winners, dates, Grands Prix) | English Wikipedia, via `data/rtt-002/` | revisions listed in `data/rtt-002/ATTRIBUTION.md` | CC BY-SA 4.0 | Attribution in the video (footer) and description; derived dataset shared alike (it is) | Yes (data files) |
| Driver nationality | English Wikipedia "List of Formula One Grand Prix winners" rev. 1376824402 (primary), Wikidata (cross-check), via `data/rtt-002/driver_nationality.csv` | retrieved 28 Sep 2026 (`data/rtt-002/source/README.md`) | Wikipedia CC BY-SA 4.0; Wikidata CC0 1.0 | As for the race data | Yes (data files) |
| RTT emblem (Luke's logo: gold globe and compass, square, 1254 × 1254 px) | Luke; supplied at render time into `kits/rtt-002/local_assets/rtt_logo.png` (git-ignored) | — | Owner's own brand asset (DEC-035) | Private brand asset: never committed or published outside the videos | **No** (DEC-006) |
| Car picture (generic modern Formula One-style car, unbranded: no team liveries, sponsor logos or F1 marks) | Supplied by Claude in Cowork at render time into `kits/rtt-002/local_assets/rtt_car.png` (git-ignored) | — | **NOT FOUND — to be recorded when the file is supplied** (who made it, under what licence or terms, and that it carries no third-party marks). Not yet cleared | Must be cleared before any render that uses it is published | **No** (DEC-006) |

## Tools used to make the video (not drawn, not shipped)

| Tool | Version | Licence |
|---|---|---|
| Playwright (drives headless Chromium to draw frames) | 1.56.1 | Apache-2.0 (package.json) |
| Tesseract OCR (tests only) | 5.3.4 | Apache-2.0 (Ubuntu package) |

## Not used

Market Marathon's Archivo TTFs (no licence file in that kit, DEC-016), any formula1.com material (DEC-008), Jolpica/Ergast data (non-commercial, DEC-003), team or sponsor logos, music (none chosen yet).
