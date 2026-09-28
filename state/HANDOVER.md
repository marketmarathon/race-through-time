# HANDOVER — 28 Sep 2026 (session 2, Cowork cloud session linked to Luke's laptop)

Previous handover (27 Sep, session 1, claude.ai chat) is in this file's git history.

## Done (evidence = commits in marketmarathon/race-through-time)
- **Repo bootstrapped on `main`** from `G:\My Drive\RTT_transfer\rtt_bootstrap` (byte-identical): README with DEC-006 public-repo rules `026bec2`, `state/` `5d6ac17`, `prompts/` `b681763`, `reference/` `b835861`. Four commits, not one: GitHub's web uploader cannot put several folders in one commit.
- **Independent check validated and frozen** (step 4): `F1_Fact_Check_2026-09-28.zip`, SHA-256 `0ac44247…cddd2`, kept private on the laptop. Sections A–G present, a source_url on every row, all internal-consistency checks pass, 22 NOT FOUND cells (Indy 500 separate F1/FIA career-total table and inclusion rule). Frozen in `state/RTT-002_independent_check_freeze.json` `d9df1ae`; validator `scripts/validate_independent_check.py` `8b5bb8c`.
- **RTT-002 dataset built** (IQ-03) on branch `rtt-002-data` @ `7696344` and **merged to `main`** on Luke's instruction (pull request #1, merge commit `7cde5df`): 1,164 races, 1,167 win credits, 116 drivers, freeze = 2026 Azerbaijan GP, 26 Sep 2026. Wikipedia (CC BY-SA 4.0) season pages 1950–2026 with page URL, revision ID and retrieval time on every row. Whole numbers only. 13/13 scripted checks pass, including career totals vs Wikipedia's separate "List of Formula One Grand Prix winners" page. Deterministic rebuild confirmed from the GitHub copy.
- **Comparison with the frozen check: 0 discrepancies** in A, B, E, F and G (`reports/RTT-002_discrepancy_report.md`).
- Every commit read back from GitHub and compared byte-for-byte with the local files.
- Laptop copy written to `Claude Workspace\race-through-time` (plain files, no git).

## How this session worked (capabilities found)
- Cowork cloud can run commands but **cannot push**: the GitHub proxy says race-through-time is not in the session's authorised repositories, and Cowork offers no way to attach one. Pushes went through **GitHub's web upload in Luke's Chrome** (authorised scope only).
- Luke added `*.wikipedia.org`, `*.wikimedia.org`, `*.wikidata.org` to claude.ai **Settings → Capabilities → Additional allowed domains**. This took effect in the running session, but Wikimedia rate-limits the shared cloud IP (HTTP 429), so the pages were read through the **MediaWiki API in Luke's Chrome**. Each transferred file was verified by SHA-256.
- Luke created a **Claude Code cloud environment "Race Through Time"** (Custom network: defaults + the three Wikimedia domains). `race-through-time` appears in Claude Code's repository list. Not used yet; intended for code work (IQ-04).

## Not done / not run
- No render, upload, publish or schedule.
- Contract checks not covered: an official F1/FIA top-20 career table was not consulted, and top-ten entries were not independently reconstructed (D-07).

## Decisions
- Resolved 28 Sep: merge done (DEC-014); follow the official F1 treatment, so the 11 Indy 500 wins count and shared drives credit each driver (DEC-012); "Carlos Sainz" = Carlos Sainz Jr. (DEC-013).
- Done 28 Sep: **D-07(b)** second blind check (top-ten entries, top ten at freeze) frozen in `state/RTT-002_independent_check2_freeze.json` and compared: 0 discrepancies (`reports/RTT-002_topten_check_report.md`, `data/rtt-002/topten_entries.csv`).
- Open: **D-07(a)** accept the top-20 totals as checked (Wikipedia list page + F1-archive reconstruction + StatsF1 agree; official totals seen for Hamilton, Schumacher, Prost only), or eyeball formula1.com for them.
- Open: **D-05** publication risk (before release only).

## Next safe actions
1. After merge: IQ-04 `player_rtt.html` (copy of C2-2; integer step-at-event display) in a Claude Code cloud session with environment "Race Through Time".
2. IQ-06 live feasibility for RTT-001, 003–012.

## Rules for the next session
Read `state/STATE.json`, this file, `state/DECISIONS.md` and `reference/metric_contract_RTT-002.md`. Never edit C2-2 files or anything in `marketmarathon/bars` for RTT. Follow DEC-006. The private check file never enters this repo. For bulk Wikipedia reads use Luke's Chrome; for repo writes from Cowork use the GitHub web upload and read every commit back.
