# Rights ledger — Race Through Time

Every third-party or owner asset the RTT player draws or ships, with its licence as read from the licence file itself. Started 28 Sep 2026 (IQ-05 round 3, `prompts/CODE_SESSION_IQ-05c.md`); updated 28 Sep 2026 (IQ-05 round 4, `prompts/CODE_SESSION_IQ-05d.md`: full logo, real car photo). Public-repo rule (DEC-006): code, configs, data files and written results only; no renders, stills, logos, pictures or other media are committed. Update this file whenever an asset is added or its source changes.

## Drawn in the video

| Asset | Where it comes from | Version | Licence (read from) | Obligations | Committed? |
|---|---|---|---|---|---|
| Archivo typeface (400, 500, 600, 700) | npm `@fontsource/archivo`, installed by `npm ci` in `kits/rtt-002/` | 5.3.0 | SIL Open Font License 1.1 (`node_modules/@fontsource/archivo/LICENSE`, "Copyright 2020 The Archivo Project Authors"; package.json `"license": "OFL-1.1"`) | Use in videos is allowed; the font files may not be sold on their own; the licence must go with any redistribution of the font files (we do not redistribute them) | No (node_modules is git-ignored) |
| National flags (today's design of each flag, DEC-035) | npm `flag-icons`, `flags/4x3/<iso alpha-2>.svg`, installed by `npm ci` in `kits/rtt-002/` | 7.5.0 | MIT (`node_modules/flag-icons/LICENSE`, "Copyright (c) 2013 Panayiotis Lipiridis"; package.json `"license": "MIT"`) | Keep the copyright and permission notice with copies of the software; images drawn into a video frame carry no further obligation under MIT. National flags themselves are public symbols; no flag is altered | No — no flag file is committed |
| Race data (winners, dates, Grands Prix) | English Wikipedia, via `data/rtt-002/` | revisions listed in `data/rtt-002/ATTRIBUTION.md` | CC BY-SA 4.0 | Attribution in the video (footer) and description; derived dataset shared alike (it is) | Yes (data files) |
| Driver nationality | English Wikipedia "List of Formula One Grand Prix winners" rev. 1376824402 (primary), Wikidata (cross-check), via `data/rtt-002/driver_nationality.csv` | retrieved 28 Sep 2026 (`data/rtt-002/source/README.md`) | Wikipedia CC BY-SA 4.0; Wikidata CC0 1.0 | As for the race data | Yes (data files) |
| RTT logo, full version with the "RACE THROUGH TIME" wordmark (Luke's banner logo: gold wordmark over a globe, 1983 × 793 px, 2.5 : 1, edges faded to transparent by Claude in Cowork) — replaces the square emblem of round 3 (DEC-045 (1)) | Luke; supplied at render time into `kits/rtt-002/local_assets/rtt_logo.png` (git-ignored) | — | Owner's own brand asset (DEC-035, DEC-045) | Private brand asset: never committed or published outside the videos | **No** (DEC-006) |
| Car photo: Lewis Hamilton's Ferrari SF-26 (#44), 2026 Chinese Grand Prix, qualifying (DEC-045 (4); replaces the generic unbranded car of DEC-035 (3)) | Wikimedia Commons, *File:2026 Chinese GP - Ferrari - Lewis Hamilton - Qualifying.jpg*, https://commons.wikimedia.org/wiki/File:2026_Chinese_GP_-_Ferrari_-_Lewis_Hamilton_-_Qualifying.jpg — see "Car photo" below. Modified copy supplied at render time into `kits/rtt-002/local_assets/rtt_car.png` (git-ignored) | original uploaded 18 Mar 2026, SHA-1 `cc6c19a2ba42a45c774b44c70c84beb86eb57721` | **CC BY 4.0** (Commons file page metadata, read through the Commons API on 28 Sep 2026: LicenseShortName "CC BY 4.0", AttributionRequired true, author Liauzh, "Own work") | Credit the author, name the licence (with a link where practical), link the source, say that it was changed. On screen: the footer credit below; the video description should carry the same credit with the source and licence links. CC BY 4.0 gives no trademark rights: the car shows team and sponsor marks, see the D-05 note | **No** (DEC-006) |

## Car photo (DEC-045 (4), recorded 28 Sep 2026)

| Field | Value |
|---|---|
| Title | 2026 Chinese GP - Ferrari - Lewis Hamilton - Qualifying (Commons file name `2026 Chinese GP - Ferrari - Lewis Hamilton - Qualifying.jpg`) |
| Subject | Lewis Hamilton's Ferrari SF-26, car number 44, qualifying for the 2026 Chinese Grand Prix (taken 14 Mar 2026 15:33 according to the file page) |
| Author | Liauzh (Wikimedia Commons user; the file page says "Own work") |
| Licence | Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0 |
| Source URL | https://commons.wikimedia.org/wiki/File:2026_Chinese_GP_-_Ferrari_-_Lewis_Hamilton_-_Qualifying.jpg (page ID 186405409) |
| Original file | 3858 × 2170 px JPEG, 1,049,874 bytes, uploaded 18 Mar 2026 by Liauzh; SHA-1 `cc6c19a2ba42a45c774b44c70c84beb86eb57721` |
| Checked | 28 Sep 2026 by Claude Code, one request to the Commons API (`prop=imageinfo`): SHA-1, author, licence and attribution requirement all as above, matching what Luke / Claude in Cowork supplied |
| Changes made | Background removed and cropped by Claude in Cowork; the result is a transparent PNG, 3435 × 936 px (about 3.67 : 1), car facing left. The modified file was not seen in this session (it is supplied at render time and never committed); its size is as supplied by Cowork |
| Attribution text (on-screen footer of the pilot) | "Car photo: Liauzh, CC BY 4.0, via Wikimedia Commons (background removed)" |
| Attribution text (video description, suggested) | Car photo: "2026 Chinese GP - Ferrari - Lewis Hamilton - Qualifying" by Liauzh, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0), via Wikimedia Commons (https://commons.wikimedia.org/wiki/File:2026_Chinese_GP_-_Ferrari_-_Lewis_Hamilton_-_Qualifying.jpg); background removed and cropped |
| Trademarks | The car carries team and sponsor trademarks (Ferrari, HP, Shell and others). The copyright licence does not cover them. Luke chose the real car knowingly (DEC-045 (4)); this is listed for review in the D-05 pre-release publication check (`state/DECISIONS.md`) before any public release |
| Committed? | No. Photo, modified copy and any render using it stay out of the repo (DEC-006) |

## Tools used to make the video (not drawn, not shipped)

| Tool | Version | Licence |
|---|---|---|
| Playwright (drives headless Chromium to draw frames) | 1.56.1 | Apache-2.0 (package.json) |
| Tesseract OCR (tests only) | 5.3.4 | Apache-2.0 (Ubuntu package) |

## Not used

Market Marathon's Archivo TTFs (no licence file in that kit, DEC-016), any formula1.com material (DEC-008), Jolpica/Ergast data (non-commercial, DEC-003), team or sponsor logos as separate graphics (the car photo shows them on the car, see above), music (none chosen yet).
