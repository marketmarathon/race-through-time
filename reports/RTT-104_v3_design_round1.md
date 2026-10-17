# RTT-104 V3 — design round 1: the top-20 board and election tags (IQ-24d, 17 Oct 2026)

Brief `prompts/CODE_SESSION_IQ-24d.md`. Owner DEC-672 (go ahead), DEC-673 (see both tag rules), DEC-674 (late-year question, answer pending); Claude DEC-675..DEC-679. Nothing here is approved; no film was rendered. **The approved V2 film is unchanged** (its page, configs, input, music, workflow and the shared driver byte-identical to c379631, `python3 tests/rtt104/check_v3_changes.py`).

**Watch:** the private pre-release named in DEC-679 (stills, phone copies, three sheets, two clips; every SHA-256 in its notes).

## What was built
- `kits/rtt-104/player_rtt104_v3.html`: runs the approved V2 page's own code unchanged and replaces only the board (DEC-675). One full-width board of 20, bars 33 px thick (V2: 20 px), flag left of the bar, name and value on the bar, big year, world-average panel bottom right, title "Women in Parliament: The Top 20 (1997–2025)", measure line as V2, credit "Race Through Time · Data: IPU via World Bank WDI (CC BY 4.0) · Election dates: IPU Parline". Smooth motion at 3 s per year as V2.
- Tags: "Election · Oct 2019", in amber, beside the bar after its value; in for the last 2 s of the move into the year and on the landing, out over 0.3 s. Only from VERIFIED rows of `data/rtt-104/v3_change_events.csv` with a fetched excerpt; unexplained changes get none. Input `kits/rtt-104/race_rtt104_v3.json` (`python3 scripts/rtt104_v3_tags.py`): 101 tags under rule (b), 46 of them under rule (a).
- Configs `kits/rtt-104/config_rtt104_v3_*.json` (base = the recommended set; each option changes one key); stills `stills_v3.json`; clips `clips_v3.txt`; workflow `.github/workflows/rtt104_v3_pilot.yml`.

## Checks (all PASS; `tests/rtt104/STILLS_CHECK_V3.md`)
- **Values:** every still's 20 (or 15) bars = the year's ranks and one-decimal figures in `v3_change_events.csv`; also all 29 year landings of the whole race, under both scales (local full scan).
- **Tags:** every tag on every still and every frame of both clips is a VERIFIED row with a source URL and fetched excerpt, big under the rule shown, with the row's month and year; on a landing every such row is drawn. Whole race scanned too: all 46 (a) and 101 (b) tags appear and fit, under both scales. `check_v3_changes.py`: 180/180 cause rows have a runner-fetched excerpt showing the date.
- **Phone:** names, values and tags 30 px = **6.1 pt** at 390 pt wide (≥ 5.9: PASS); top 15: 6.9 pt (DEC-676).
- **Overlap:** no bar or text inside the world panel or past the edge, every frame.
- **WCAG flash:** both clips, on the runner (results in the release notes and DEC-679).
- Data tests 23/23.

## What the clips show (2016 → 2020, 3 s per year)
- Rule (a): **12 tags** — 2017 Angola, France, Germany, New Zealand; 2018 Costa Rica, Mexico; 2019 Belarus, Finland, Switzerland, UAE; 2020 Bolivia, New Zealand.
- Rule (b): **20 tags** — the 12 above plus 2017 Argentina, Ecuador, Netherlands, Senegal; 2019 Argentina, Belgium, Mozambique, Spain ("Elections · Apr & Nov 2019"). 2019 has 8 at once.
- In motion, a bar jumping many places (UAE 61st → 4th in 2019) crosses others and its tag briefly overlaps theirs; it settles by the landing.

## Late-year elections (proposal, DEC-677)
The one documented case: WDI's 1998 figure is "as of August 10, 1998". **Australia's election of 3 Oct 1998** shows up in the 1999 figure (15.5% → 22.4%, 30th → 16th); the still `v3_late_election_PROPOSAL_1999` tags that jump "Election · Oct 1998". No November–December election has a documented reference date before it, and in 2007, 2012 and 2017 the figure already includes late elections (Denmark Nov 2007, Nicaragua Nov 2011), so moving every Nov–Dec election to the next year would put some tags on the wrong jump.

## Questions for Luke
1. **Board size: 20 or 15?** Recommend **20** (readable on a phone at 6.1 pt; it is what V3 was asked for). Default if no answer: 20. Sheet `sheet_v3_rows`.
2. **Tag look?** Recommend **look 1, the filled amber tag** (reads at a glance, also on a bar). Default: look 1. Sheet `sheet_v3_tag_look`.
3. **Tag rule (a) or (b), after watching both clips?** Recommend **(a)**: 9 in 10 of its tags have a VERIFIED election, at most 5 a year; (b) adds many small moves and can tag a bar whose own figure did not change (DEC-678). Default: (a).
4. **Scale?** Recommend **fixed 0–70%**: the bars grow over the years, which is the story; following the leader makes 1997 look like 2025. Default: fixed. Sheet `sheet_v3_scale`.
5. **Late-year elections?** Recommend **leave those jumps untagged** unless the figure's date is documented (only 1998 is); tag the Australia 1998 kind as shown. Default: untagged.

## Proposals beyond the brief
- If (b) is chosen: no tag where the country's own figure did not change (5 tags, none in the clips; DEC-678).
