# CODE_SESSION_IQ-21: RTT-101 design round 1 (Premier League net transfer spend)

Task IQ-21, episode RTT-101: cumulative net spend on reported transfer fees by every Premier League club, month by month, July 1992 to the close of the summer 2026 window (1 Sep 2026). Written by Cowork for Luke, 10 Oct 2026. This is the first design round: options side by side, no full film, no music.

## 0. Before you start
- Read these first:
  - `CLAUDE.md`;
  - `state/HANDOVER.md` and `state/STATE.json` on PR #19's branch `claude/nice-davinci-guln5e`;
  - `reports/RTT-101_data_report.md` sections 18 and 19;
  - `data/rtt-101/DESIGN_INPUTS.md`;
  - `reference/metric_contract_RTT-101.md` (section 8, display attributes);
  - `reference/house_style.md` **as on PR #23's branch** (the latest version);
  - `reference/rights_ledger.md`.
- Save this brief word for word as `prompts/CODE_SESSION_IQ-21.md`.
- **DEC numbers:** your block is **DEC-700 to DEC-799**. Check `main` and every open pull request and branch first, and confirm 700+ is free. Other blocks: RTT-101 data (IQ-15) DEC-400–499; RTT-102 up to DEC-573; RTT-104 (IQ-20) DEC-600–699.
- **Branch:**
  - Start from PR #19's branch at its latest commit (IQ-15m wrap-up aa6bf3c or later; IQ-15n is running and will push round 6 results). Merge in PR #23's branch `claude/relaxed-clarke-9e0sqq`, which already contains PRs #18, #21 and #22. This gives you the latest player work: big date top right, board sized to its bars, logo tiles, eased motion through every data month, running-total panel with its line, and the 5 s ending.
  - Resolve state-file conflicts by keeping both sides. Do not push to either branch.
  - **The IQ-15 session may still push data to PR #19** while Cowork checks the remaining Tier 1 fees. Merge #19 again before each render. Never change RTT-101 data files or the build yourself; report any data problem instead.
  - In your pull request, give Luke the merge order: #18, #22, #21, #23, #19, then yours.

## 1. Owner decisions to record first (Owner DECs)
1. **10 Oct 2026 (Luke, Cowork chat): club crests beside the bars.** Each club's crest appears on a tile beside its bar, purely to identify the club, the same way as the browser logos in RTT-001 (house_style section 7: non-free logo files accepted by Luke for identification; each file's source and status in the rights ledger; files in the private repo only; crop only where Luke allows, never redrawn; our own neutral tile where no real crest exists). Cowork had flagged a small risk of a takedown request from a club, and said it was not legal advice. Luke answered "yes" to Cowork's question.

Luke's other 10 Oct decisions are recorded by the IQ-15 session: DEC-445 (keep building from our own deal-by-deal data) and DEC-450 (round 6 checks). Check they are there.

## 2. Data
- Use the on-screen series `series_onscreen.csv` (VERIFIED fees only, DEC-448; report section 19), never the preview `series_monthly.csv`. Section 19's question 1 (whether small unconfirmed fees stay off screen) is still with Luke; it changes no leader.
- Figures may still change after Cowork's Tier 1 checks, so this round is about the look. Mark every still and clip "preview figures" in the release notes, not on the frame.
- Start at July 1992 (DEC-260). End at the freeze, 1 Sep 2026.
- Relegated clubs keep a frozen bar and their rank (DEC-259).
- Never round, smooth or ease a value so that a month-end shows a figure that is not in the data. Eased motion must pass through every month end of the series (RTT-102's DEC-562 approach).

## 3. House defaults to apply without asking (house_style sections 1 to 6)
- No intro or outro. The final table holds for 5 s after the last figures land (DEC-569).
- No running captions.
- Big date top right, beside the RTT logo.
- The board is sized to the bars on it.
- Values follow the bar and count smoothly, landing exactly on each month end.
- Each club keeps one colour, with the CIEDE2000 ≥ 18 rule on screen together, checked under colour blindness.
- Stills are taken on landing frames only, with a phone copy of each and the phone check.
- WCAG flash check on every clip.
- Credits in the footer and the description.
- Crown on the leader's bar (approved feature; propose it, as the lead changes hands many times).

## 4. Round 1: options side by side
Use stills with phone copies. Use a clip only where motion is the question. Make one contact sheet per item. Representative boards: Jul 1992, Jun 2003, Aug 2008, Aug 2015, Jul 2016, Sep 2022 and the freeze, plus any close call listed in DESIGN_INPUTS.

**a. Title and the line under it.**
- Give 2 or 3 options. Each must name the measure or put it in the line under the title (house_style section 1). Examples:
  - A: "Premier League Net Transfer Spend (1992–2026)".
  - B: "The Premier League's Biggest Spenders (1992–2026)", with "Net spend on reported transfer fees, since 1992" under it.
- "Undisclosed fees not included" (DEC-429) must be on screen for the whole film. Show it as part of the fixed line under the title vs in the footer. Cowork recommends the line under the title, as with RTT-102's "estimates".

**b. Board size.**
- Compare 10, 12 and 15 bars at phone size on the Jun 2003, Aug 2015 and freeze boards.
- The order test so far assumed 12 (DEC-256). Say which size the story and phone readability support, and how many clubs ever reach the board at each size.

**c. Value labels.**
- Units and rounding, e.g. "£1.67bn", "£612m", "£4.2m".
- What a near-tie looks like when two values round the same (e.g. Mar–Jun 2003, if still within £0.1m). Option: one more decimal for the clubs concerned only while they round equal vs leave the order to speak. This is an on-screen claim, so it is Luke's question (principle 21).
- If DESIGN_INPUTS lists a negative bar on the board, show how it is drawn (from the zero line, value "−£12m"). Otherwise one line saying none occurs.

**d. Clubs outside the Premier League (DEC-259).**
- A relegated club's frozen bar: dimmed, plus a short label, e.g. "· relegated 2001" or "· not in the PL", vs dimmed only. Show its return to the league.
- A newly promoted club enters at its first PL season and simply fades in (house_style section 5, late entrants).
- Wording must be exact. Wimbledon FC (PL 1992–2000) is a different club from AFC Wimbledon and MK Dons (contract section 7).

**e. Club identity and colours.**
- Name on the bar (`clubs.csv` `display_name`).
- Colours: many clubs share red or blue kits. Compare kit colours (recognisable, with the closest pairs adjusted or given a second-colour edge) against a distinct palette, on the busiest board, with the colour-blind check. Say which pairs fail the CIEDE2000 rule.
- **Crest tile beside each bar** (owner decision 1):
  - Fetch the crests on a runner into the private repo, as RTT-001 and RTT-103 did with logos. Use Wikimedia Commons first, then English Wikipedia's non-free files. Record each file's source, licence or non-free status, and SHA-256 in the rights ledger.
  - Use Wimbledon FC's own crest, never AFC Wimbledon's or MK Dons'.
  - Show side by side: today's crest throughout vs the crest in use at each date (several clubs changed crests after 1992, e.g. Man City, Arsenal, Spurs, Leeds, West Ham). RTT-103 used today's logos; RTT-102 used Bard's own logo while it was called Bard. Cowork leans to today's crest throughout, because it is simpler and easier to recognise on a phone. Say how many clubs would need an older crest.
  - Check the crests at phone size; small detailed crests may need the tile enlarged.
  - Use a neutral tile only where no usable file exists, and list those clubs.

**f. Pacing.** Transfer money arrives in bursts:
- summer and January windows from 2002–03;
- before that, trading until 31 March.

Render one passage (Jun 2003 to Sep 2004, Chelsea's first Abramovich windows) in three versions:
- A: one pace, 0.5 s per month.
- B: the house multipliers (×1.4 when the visible order changes, ×1.0 when a bar grows, ×0.8 when nothing visible changes).
- C: a faster fixed pace for quiet months.

Give the full film's running time for each (about 410 months). A smooth speed curve is not approved (house_style section 2); C must be one named rule, with clean boundaries. Say what pace the story density supports (principle 12).

**g. Bottom-right panel** (Luke prefers a picture or one small statistic to story cards; house_style section 1):
- A: a running total with its line, e.g. "All Premier League clubs: net spend". Say in the round what it adds up, and that it equals PL clubs' net spend with clubs outside the PL that season.
- B: the leader's average net spend per PL season in 2026 £, the secondary statistic (contract §6).
- C: nothing.

**h. The secondary statistic** (Luke's owner brief: CPI-adjusted average net spend per PL season played). Options for where it appears:
- A: one closing view after the final table, ranked, labelled "(2026 £)" and "average per Premier League season".
- B: panel only (item g B).
- C: description only.

Cowork leans A.

**i. Story moments.** Luke is not keen on cards; propose them only where nothing else can carry a moment the board cannot show.
- Choose at most 5 from `moments.csv`, each with a reason. Candidates:
  - Bosman ruling (15 Dec 1995);
  - transfer windows from 2002–03;
  - Abramovich buys Chelsea (Jul 2003);
  - Glazer control of Man Utd (May 2005);
  - ADUG buys Man City (Sep 2008);
  - Newcastle takeover (Oct 2021);
  - Chelsea sale (May 2022).
- Show them as RTT-103's story card vs one line under the title for about 3 s vs none.
- Only VERIFIED moments go on screen. List every candidate that is still UNVERIFIED, with its URL, for Cowork to read in Luke's Chrome.
- **The Man City Premier League case stays off the board in this round.** It is a topical hook only, in neutral wording (Luke's brief), for the description and packaging. Never put any figure from it next to City's bar.

**j. Final table at the freeze.**
- Hold 5 s.
- Show it with and without the note that the figures will be updated after the January 2027 window (DEC-237 (b)): a final-table line vs description only.
- No summary line unless it says something the board cannot show (DEC-550).

**k. Footer credits.**
- Wording from the contract: "Reported transfer fees from club statements and press reports; CPI: ONS; exchange rates: Bank of England". Add the ECB where euro rates come from it.
- Fit it to the bottom strip at phone size.

## 5. Checks and output
- Add RTT-101 player tests (values at every landing frame equal the on-screen series; ranks; frozen bars) and the phone check on every still.
- Show that the approved output of RTT-001, RTT-002, RTT-003, RTT-102 and RTT-103 is unchanged (pixel-identical frames).
- Render on a runner through RTT-101's own workflow, never another episode's.
- Save to a private pre-release in `race-through-time-private`, with every file's SHA-256 in the release notes and `STATE.json`. Logo or crest files go in the private repo only.
- Push your branch and open a pull request with code and written results only. Do not merge. Update HANDOVER and STATE.

## 6. Report
- Ask Luke numbered questions only on what is his: on-screen claims, title, rights, or choices the rules do not settle (DEC-417). Give each your recommendation and what happens if he does not answer.
- Settle everything else yourself and list what you decided.
- Finish with a short plain-English summary for Luke: what was done (with links), what needs his decision, and the next step.
