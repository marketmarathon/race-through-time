# Rights ledger — Race Through Time

Every third-party or owner asset the RTT player draws or ships, with its licence as read from the licence file itself. Started 28 Sep 2026 (IQ-05 round 3, `prompts/CODE_SESSION_IQ-05c.md`); updated 28 Sep 2026 (IQ-05 round 4, `prompts/CODE_SESSION_IQ-05d.md`: full logo, real car photo). Public-repo rule (DEC-006): code, configs, data files and written results only; no renders, stills, logos, pictures or other media are committed. Updated 29 Sep 2026 (DEC-060, DEC-061): the private asset store. Update this file whenever an asset is added or its source changes.

## Drawn in the video

| Asset | Where it comes from | Version | Licence (read from) | Obligations | Committed? |
|---|---|---|---|---|---|
| Archivo typeface (400, 500, 600, 700) | npm `@fontsource/archivo`, installed by `npm ci` in `kits/rtt-002/` | 5.3.0 | SIL Open Font License 1.1 (`node_modules/@fontsource/archivo/LICENSE`, "Copyright 2020 The Archivo Project Authors"; package.json `"license": "OFL-1.1"`) | Use in videos is allowed; the font files may not be sold on their own; the licence must go with any redistribution of the font files (we do not redistribute them) | No (node_modules is git-ignored) |
| National flags (today's design of each flag, DEC-035) | npm `flag-icons`, `flags/4x3/<iso alpha-2>.svg`, installed by `npm ci` in `kits/rtt-002/` | 7.5.0 | MIT (`node_modules/flag-icons/LICENSE`, "Copyright (c) 2013 Panayiotis Lipiridis"; package.json `"license": "MIT"`) | Keep the copyright and permission notice with copies of the software; images drawn into a video frame carry no further obligation under MIT. National flags themselves are public symbols; no flag is altered | No — no flag file is committed |
| Race data (winners, dates, Grands Prix) | English Wikipedia, via `data/rtt-002/` | revisions listed in `data/rtt-002/ATTRIBUTION.md` | CC BY-SA 4.0 | Attribution in the video (footer) and description; derived dataset shared alike (it is) | Yes (data files) |
| Driver nationality | English Wikipedia "List of Formula One Grand Prix winners" rev. 1376824402 (primary), Wikidata (cross-check), via `data/rtt-002/driver_nationality.csv` | retrieved 28 Sep 2026 (`data/rtt-002/source/README.md`) | Wikipedia CC BY-SA 4.0; Wikidata CC0 1.0 | As for the race data | Yes (data files) |
| RTT logo as a round badge: a complete globe with "RACE THROUGH TIME" inside it, nothing coloured outside the circle (885 × 885 px, 1 : 1, transparent outside the circle; made by Claude in Cowork from Luke's logo, DEC-051) — replaces the square emblem of round 3 and the wide banner logo of DEC-045 (1) | Luke; stored in the private repo `marketmarathon/race-through-time-private` at `assets/rtt-002/rtt_logo.png`, SHA-256 `e3db4611…0eeca` (see "Where the private assets live"); fetched at render time into `kits/rtt-002/local_assets/` (git-ignored) or the render runner's temporary folder | — | Owner's own brand asset (DEC-035, DEC-045, DEC-051) | Private brand asset: never committed or published outside the videos | **No** (DEC-006) |
| Car photo: Lewis Hamilton's Ferrari SF-26 (#44), 2026 Chinese Grand Prix, qualifying (DEC-045 (4); replaces the generic unbranded car of DEC-035 (3)) | Wikimedia Commons, *File:2026 Chinese GP - Ferrari - Lewis Hamilton - Qualifying.jpg*, https://commons.wikimedia.org/wiki/File:2026_Chinese_GP_-_Ferrari_-_Lewis_Hamilton_-_Qualifying.jpg — see "Car photo" below. Modified copy stored in the private repo `marketmarathon/race-through-time-private` at `assets/rtt-002/rtt_car.png`, SHA-256 `4be74e67…aa5bb`; fetched at render time into `kits/rtt-002/local_assets/` (git-ignored) or the render runner's temporary folder | original uploaded 18 Mar 2026, SHA-1 `cc6c19a2ba42a45c774b44c70c84beb86eb57721` | **CC BY 4.0** (Commons file page metadata, read through the Commons API on 28 Sep 2026: LicenseShortName "CC BY 4.0", AttributionRequired true, author Liauzh, "Own work") | Credit the author, name the licence (with a link where practical), link the source, say that it was changed. On screen: the footer credit below; the video description should carry the same credit with the source and licence links. CC BY 4.0 gives no trademark rights: the car shows team and sponsor marks, see the D-05 note | **No** (DEC-006) |

## Where the private assets live (DEC-060, recorded 29 Sep 2026)

| File | Stored in | SHA-256 | Size | Used by |
|---|---|---|---|---|
| RTT logo, round badge | `marketmarathon/race-through-time-private` (**private**), `assets/rtt-002/rtt_logo.png` | `e3db46119b52648c84eae5f6acd682bd7be855819818856e695592b20572eeca` | 885 × 885 PNG | logo box of the pilot |
| Car photo, background removed (modified from Liauzh's CC BY 4.0 original, see below) | same repo, `assets/rtt-002/rtt_car.png` | `4be74e673c601a93d0c08511d474638ca51e04cce5d4f2af46198696e81aa5bb` | 3435 × 936 PNG | car box of the pilot |
| Rendered pilot and full-film videos (review renders, not for publication) | same repo, **Releases** (tags `rtt-002-pilot5-…`, `rtt-002-film-…`), written by `.github/workflows/render_pilot.yml` (DEC-061) | in each release's notes | 3840 × 2160 master + 1920 × 1080 viewing copy | Luke's review |

Access: Actions secret `RTT_PRIVATE_TOKEN` in this repo (fine-grained token, `race-through-time-private` only, Contents read and write, expires 28 Sep 2027 — renew before then) and the Claude GitHub App. The render workflow checks both hashes before drawing and leaves nothing on the public side: no workflow artifact, no cache, no committed file (DEC-061). Hashes read back by Claude Code on 29 Sep 2026: both match.

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
| Committed? | No. Photo, modified copy and any render using it stay out of this repo (DEC-006); the modified copy and the renders live in the private repo (DEC-060) |

## Tools used to make the video (not drawn, not shipped)

| Tool | Version | Licence |
|---|---|---|
| Playwright (drives headless Chromium to draw frames) | 1.56.1 | Apache-2.0 (package.json) |
| Tesseract OCR (tests only) | 5.3.4 | Apache-2.0 (Ubuntu package) |
| FFmpeg with libx264 (encodes the video; installed on the render runner from Ubuntu 24.04 packages) | Ubuntu 24.04 package | GPL (Ubuntu package); used as a tool, not shipped |

## Not used

Market Marathon's Archivo TTFs (no licence file in that kit, DEC-016), any formula1.com material (DEC-008), Jolpica/Ergast data (non-commercial, DEC-003), team or sponsor logos as separate graphics (the car photo shows them on the car, see above), music (none chosen or licensed yet: the pilot and the full film are video only, with no audio track; the render workflow checks this, DEC-063).
