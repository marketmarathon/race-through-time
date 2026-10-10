# RTT kit — RTT-101 "Premier League net transfer spend" (cumulative net spend on reported transfer fees, July 1992 – 1 Sep 2026) · design round 1 (IQ-21)

**IQ-21 (10 Oct 2026): the first design round - options side by side for Luke, no full film, no music** (brief `prompts/CODE_SESSION_IQ-21.md`; decisions DEC-700 onwards in `state/DECISIONS.md`). **The data is not changed:** `data/rtt-101/` as built by the IQ-15 sessions (pull request #19, merged in at IQ-15n). On screen only `series_onscreen.csv` (VERIFIED fees only, DEC-448), never the all-fees preview `series_monthly.csv`. **Preview figures:** the Tier 1 checks may still change them; the release notes say so, the frames do not.

This kit has **no player of its own**: it is drawn by the RTT-002 player (`kits/rtt-002/player_rtt.html`, `rtt_timeline.js`, `rtt.js`) with RTT-001's, RTT-102's and RTT-103's approved additions (big date top right, board sized to its bars, logo tiles, crown, eased motion through every data month, running-total panel with its line, the 5 s ending), brought in by merging pull request #23's branch. IQ-21 adds a **net** race kind (DEC-702): every RTT-101 feature is switched on by the race file's `kind: "net"` or by a config key, and is off for every other episode: frames of RTT-001, RTT-002, RTT-003, RTT-102 and RTT-103 configs are pixel-identical before and after (`tests/player/compare_frames.js`).

| File | What it is |
|---|---|
| `race_rtt101.json` | Player input ("rtt-series/1", kind "net"), written by `scripts/rtt101_adapter.py` from `data/rtt-101/series_onscreen.csv`, `clubs.csv`, `pl_membership.csv` and `seasons.csv` (their SHA-256 checked against `data/rtt-101/manifest.json` first): 411 events (every month end from July 1992 to August 2026, plus the freeze, 1 Sep 2026); each club's cumulative net in whole pence from its first PL season, the series' own rank, "out" while the club is outside the PL (with the year its last PL season ended), its average per PL season in 2026 £ and seasons played, and the sum of every club's figure (the panel) |
| `dataset_hashes.txt` | SHA-256 of the adapter's inputs and output (the render and the tests check them) |
| `config_rtt101_base.json` | Claude's recommendation for every item (none approved yet, DEC-069): house defaults (sections 1-6), title A with "undisclosed fees not included" in the line under it, 12 bars, compact values ("£1.74bn", "£683m", "£45.3m"), frozen bars dimmed with "· relegated 2009", crown on the leader, today's crest on a light tile, the distinct palette, one pace (0.5 s a month), eased through every month end, the all-clubs panel with its line, the final table held 5 s after the freeze lands |
| `config_rtt101_pace_{A,B,C}.json`, `config_rtt101_clip_pace{A,B,C}_2003_2004.json` | Item f: one pace 0.5 s a month / the house multipliers / 0.25 s for the months with no open transfer window (from 2002-03: March, April, October, November, December; before: April), and the June 2003 - September 2004 clips |
| `config_rtt101_colours_kit.json`, `kit_colours.json`, `palettes.json`, `make_palette.js` | Item e: kit colours (Claude's approximate hex values of each club's colours; shades moved at most CIEDE2000 8, a second-colour edge where a pair is still close) vs the distinct 18-colour palette; `tests/player/COLOURS_RTT101.md` lists every failing pair |
| `crests.json`, `assets_sha256.txt` | The crests (identification only, owner DEC-700): each file's page, licence or non-free status and SHA-256; `dated`: older crests for the "crest in use at each date" demonstration. The files live only in the private repo (`assets/rtt-101/crests/`), fetched by `.github/workflows/rtt101_assets.yml` with `scripts/rtt101_fetch_crests.py` |
| `config_rtt101_crests_dated.json`, `config_rtt101_crests_notile.json` | Item e: the crest in use at the date where a dated file was found; crests without the light tile |
| `config_rtt101_panel_avg.json`, `config_rtt101_closing_avg.json` | Items g B and h A: the leader's average per PL season (2026 £) in the panel; one closing view after the final table |
| `config_rtt101_story_card.json`, `config_rtt101_story_line.json` | Item i: five candidate moments as RTT-103's card or as one line under the title (layout only: every candidate is still UNVERIFIED) |
| `config_rtt101_final_note.json`, `config_rtt101_footer_undisclosed.json` | Items j and a: the "updated after the January 2027 window" line on the final table; "undisclosed fees not included" in the footer instead |
| `config_rtt101_clip_relegation_2009_2010.json` | Item d: Newcastle relegated in May 2009 and back in May 2010 (motion) |
| `stills.json`, `render_stills.js`, `clips.txt` | 57 stills (each also at phone size), 13 contact sheets, 4 clips |
| `description_credits.md` | The footer as drawn and the draft description lines |

## Run

```
cd kits/rtt-002 && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
python3 scripts/rtt101_adapter.py data/rtt-101 kits/rtt-101/race_rtt101.json --hash-file kits/rtt-101/dataset_hashes.txt   # from the repo root
RTT_CONFIG=../rtt-101/config_rtt101_pace_A.json FRAME_COUNT_ONLY=1 node rtt.js        # the whole film at pace A
node kits/rtt-101/make_palette.js 12                                                  # palettes.json, COLOURS_RTT101.md
RTT_LOCAL_ASSETS=<folder with rtt_logo.png and crests/> node kits/rtt-101/render_stills.js OUT_DIR   # stills and sheets (outside the repo)
node tests/player/run_tests_rtt101.js ; node tests/player/phone_check_rtt101.js      # from the repo root
node tests/player/compare_frames.js <a checkout of the commit before a player change>
```

Render: `.github/workflows/rtt101_pilot.yml` (its own workflow; a push that changes it on the IQ-21 branch): runs the tests and the phone check, fetches Luke's logo and the crests from the private repo, checks every SHA-256, runs the WCAG flash check on every clip, renders the clips at 1920 × 1080 with no audio and the stills, and saves everything only as one pre-release in `marketmarathon/race-through-time-private`. No workflow artifact, no cache.

## Not in this kit

No crest files, stills or renders (DEC-006, DEC-060): they live only in the private repo. No music (not chosen yet).
