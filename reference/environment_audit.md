# RTT environment audit (P00_BOOTSTRAP)
27 Sep 2026 · claude.ai chat, Project "Race Through Time" · model Claude Opus 5.5 · all work read-only

## 1. What this session could reach
| Item | Result | Test |
|---|---|---|
| Pack: 00_START_HERE.md, Master Blueprint, Playbook, Slate workbook | VERIFIED | read in full; workbook parsed (10 sheets, 100 briefs, all "Research brief — not greenlit") |
| Pack: CLAUDE_KICKOFF_PROMPT.txt, Claude_Starter/ (STATE.json, HANDOVER.md, instructions, skill templates, task prompts incl. P00_BOOTSTRAP), Data/ (JSON/CSV, SOURCE_REGISTER.md) | NOT FOUND | not in /mnt/project; no uploads. Workbook carries the same briefs and source rows, so research is not blocked |
| GitHub `marketmarathon/bars` | VERIFIED public, read-only | `git ls-remote` + clone of main @ 2a10877 (22 Sep 2026) |
| GitHub write / push | NOT AVAILABLE here | no GitHub connector or credentials in this session |
| Laptop `Claude Workspace` | NOT AVAILABLE here | no desktop link in this chat |
| Connectors present (Drive, Gmail, Supabase, Cloudflare, Dynadot, Instant Domain Search, Claude in Chrome) | present, not exercised | not needed for P0 |
| Sandbox | ephemeral Linux, Node 22, Python; no Chromium; allowlist covers github.com, raw.githubusercontent, npm, PyPI only; GitHub REST API rate-limited on shared IP | commands run |

## 2. Repository map (main @ 2a10877)
- 122 commits; branches `main`, `fr-quarterly`; tags `video-3`, `video-4`. Clone ≈ 647 MB.
- Flat root: 36 kit zips (`MarketMarathon_RaceKit_*`), shared root assets (logo PNGs, fonts, `Emotional.mp3`, `config.json`, `uk_race.json`), `racekit_full.js`, `yt_upload.py`, `fetch_panels.sh` (Cloudinary), `make_review_assets.sh`; image folders story_images (60), rf_year_photos (29), uk_c2_year_photos (30), us_c2_year_photos (29).
- README is stale (describes a single-job 1920×1080 UK render).
- No CLAUDE.md, no test suite, no `.claude/skills` in the repo.
- Two renderer generations:
  - `racekit_full.js` — Node + resvg (older Market Cap line).
  - Format C/C2 — `formatc.js` drives `player_formatc2.html` in Playwright Chromium. Env contract: FRAME_COUNT_ONLY, SEG_START/SEG_END/SEG_OUT, RASTER_W (3840 master / 1920 preview), NOMUX, REF_PNG_DIR (lossless reference frames for pixel diffs). `race_sec` derived from data.
- Protected baseline C2-2: kits RF_US_C2_v3, RF_UK_C2_v1, RF_FR_C2_v1 (22 Sep). Layout is config tokens (picmode wedge, picw 1080, barend 1150, namescale 0.88, yearsize 112, valw 260; 30 fps; 20 s/year; crf 4).
- Provenance: each kit's `dataset_hashes.txt` records content hash, frozen dataset ID and notes — reusable for RTT manifests.
- Market-cap-specific code in the C2-2 player: value labels hard-wired to `bn`/`tn` with one decimal (`toFixed(1)`); values interpolated between periods (`lerp`); country flags drawn; sub-sector icons; merger lineage rows.

## 3. Workflows
- 23 workflows, all `workflow_dispatch` (manual). No `schedule` triggers: nothing recurring is active in GitHub.
- Split renders: plan → matrix shards (default 18) → join; 300-min shard timeout; 240 s stall watchdog; music beds pulled from a separate release via `AUDIO_REPO_TOKEN`.
- Every workflow checked calls `yt_upload.py ... --privacy private`. The script itself accepts private / unlisted / public, so "private only" is a workflow convention, not an enforced boundary.
- Secrets referenced by name only: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN, AUDIO_REPO_TOKEN. The refresh token authorises one Google account's channel(s); RTT needs its own.
- No GitHub environment or required-reviewer gate.
- 18-shard default is consistent with the reported ~40-min render; not benchmarked here.

## 4. Security
- Credential pattern scan (GitHub tokens, Google API keys, OAuth client secrets / refresh tokens, Cloudinary URLs, `sk-` keys) over the working tree, the contents of all 36 kit zips and full git history: no matches. A pattern scan is not proof of absence.
- The repo is public. It contains kit datasets (provenance names companiesmarketcap), logos, generated images and a music file (`Emotional.mp3`, added 30 Jul 2026). Whether each licence permits public redistribution: NOT CHECKED. For RTT this matters directly: licensed data (Official Charts, CTBUH, Jolpica) must not be committed to a public repo.

## 5. Carried from earlier sessions, not re-verified today
- Laptop is Windows on ARM. On 11 Sep git was not installed and a linked cloud session could not run commands; commits landed 21–22 Sep, so a push route now exists — method NOT CHECKED.
- Shorts uploader `RaceKit\publish_pipeline\mm_upload.py` (local, no publish flag). Public publishing is done by hand in YouTube Studio.
- Market Marathon channel ID is known. A Race Through Time YouTube channel: NOT FOUND.
