# CODE_SESSION_IQ-19: RTT-102 design round 1 (AI assistant websites race)

Task IQ-19, episode RTT-102: Similarweb's published estimates of monthly website visits to eight AI assistant websites, Dec 2022 to Aug 2026. Written by Cowork for Luke, 9 Oct 2026. This is the first design round: options side by side, no full film, no music.

## 0. Before you start
- Read `CLAUDE.md`, then `state/HANDOVER.md` and `state/STATE.json` on PR #21's branch, `reports/RTT-102_data_report.md` (sections 2 and 4), `reference/metric_contract_RTT-102.md` (display attributes), `reference/house_style.md` **as on PR #22's branch** (the latest version) and `reference/rights_ledger.md`.
- Save this brief word for word as `prompts/CODE_SESSION_IQ-19.md`.
- **DEC numbers:** continue RTT-102's block from **DEC-531** (IQ-17 used DEC-500 to DEC-530). Check `main` and every open pull request first; stay below DEC-600. RTT-103 (IQ-18) uses up to DEC-399; RTT-101 (IQ-15) DEC-400 to DEC-499.
- **Branch:** start from PR #21's branch `claude/nice-wozniak-f62eio` (head b04f33a) and merge in PR #22's branch `claude/magical-einstein-hguyvv` (it already contains PR #18), so that RTT-001's approved player work (big date top right, board sized to its bars, logo tiles, estimated look with frame-anchored stripes, "~" values) and RTT-103's story card are available. Do not push to either of those branches. The IQ-18 session is still working on #22: do not change RTT-103 files. In your pull request, give Luke the merge order: #18, then #22, then #21, then yours (yours contains #21's commits).

## 1. Owner decisions to record first (Owner DECs)
1. **9 Oct 2026 (Luke, Cowork chat), Similarweb trial:** figures seen inside Similarweb's paid platform (Luke's free trial, signed up 9 Oct) are not used for the video or the data. The race ends in Aug 2026 (as in DEC-530) unless Similarweb publishes September 2026 figures in public (its own newsletter, blog or reports); those would then be checked at source and added. Reason: Similarweb's terms s.6(iv) bar presenting or sharing data received through the Platform without consent, and DEC-244 (owner-accepted Similarweb risk; recorded on PR #19's branch `claude/nice-davinci-guln5e`, not yet on main) covers figures Similarweb published in public. Luke: "Yes I will go with your recommendation".
2. **9 Oct 2026 (Luke, Cowork chat):** start the RTT-102 design round now ("yes please").

## 2. Data
No data changes. The film runs Dec 2022 to **Aug 2026**. ChatGPT's verified Sep 2026 figure is not shown, because the other bars stop at August. Copilot (last figure Sep 2025) and Meta AI (last figure Dec 2025) stay on the board dimmed as "latest figure". Use `series_monthly.csv` as built.

## 3. House defaults to apply without asking (house_style sections 1 to 6)
- No intro or outro; the final table holds for 10 s.
- No running captions.
- Big date top right beside the RTT logo.
- The board is sized to the bars on it (only 2 or 3 bars before 2024).
- Values follow the bar.
- Continuous values count smoothly and land exactly on each published month.
- Each assistant keeps one colour (CIEDE2000 ≥ 18 apart; checked under colour blindness).
- Bars appear from their first published figure.
- Stills are taken on frames where a month's figures land.
- Phone check on every still.
- WCAG flash check on any clip with stripes.
- Footer credit to Similarweb; press credits in the description (report section 7).

No crown or record line is proposed, because ChatGPT leads every month. Say so if you think otherwise.

## 4. Round 1: options side by side
Use stills with phone copies. Use a clip only where motion is the question. Put one contact sheet per item.

**a. Title:** 2 or 3 options that name the measure, e.g. "Most-Visited AI Assistant Websites (2022–2026)" and "AI Chatbot Websites by Monthly Visits (2022–2026)". Show each with the fixed source line, whose wording should say Similarweb, estimates, website visits and worldwide.

**b. How "estimates" is shown:**
- A: once for the whole film, in the title or source line, with solid bars and "~" values.
- B: every bar in the analyst-estimate look.

Cowork recommends A: one estimator and one measure, and the label never leaves the screen.

**c. Older estimates (before Similarweb's 28 Jul 2024 re-estimate) and the note at the revision (DEC-501, DEC-522):**
- A: frame-anchored stripes on each bar's older-estimate stretch, plus one dated line under the title at Aug 2024 (draft: "Similarweb re-estimated its figures in July 2024; earlier bars are its older estimates", shortened to fit a phone).
- B: the note only.

Show the Aug 2024 board, where Gemini's fall shows.

**d. Value labels:**
- "~" on every value (the contract's proposal, DEC-514) vs "~" only between published months.
- Rounding, e.g. "5.64bn", "950m", "84.1m".
- How "latest figure" reads on the dimmed Copilot and Meta AI bars.

**e. Motion:**
- Straight lines between published months (as decided) vs eased motion through the same published points. Eased motion must not overshoot and must keep exact values at published months, like RTT-001's draw-time smoothing (DEC-184).
- Make one clip of 2024 (Gemini, Perplexity and Claude across the data-version change; report section 4) rendered both ways.
- Say whether easing moves any place change listed in report section 2.

**f. Month-by-month vs quarter-by-quarter playback:** Luke wants to compare them ("it should be smooth").
- Render the same passage (Oct 2024 to Jun 2025: DeepSeek's surge and fall, Gemini retaking second) with a monthly clock and with a quarterly clock.
- Say what a quarterly clock loses (e.g. DeepSeek's Feb 2025 peak).
- Give 2 or 3 speeds, with the full film's running time for each. 45 months is short, so say what pace the story density supports (principle 12).

**g. Scale:** ChatGPT is about six times the next bar.
- Show the honest linear board at phone size for Feb 2025 and Aug 2026.
- Only if the race for second is hard to read: one alternative as a mock-up still (e.g. a clearly marked break in ChatGPT's bar), with your view on whether it claims more than the data shows (principle 21).

Cowork recommends linear unless it is unreadable.

**h. Names and logos:**
- The bar name is the name at that date (Bard until 7 Feb 2024, then Gemini; already in the contract).
- Logo per bar for identification (house_style section 7, approved for RTT-001 and RTT-103): Bard's logo of the time vs today's Gemini logo throughout.
- Every logo file and its status goes in the rights ledger, with files in the private repo only. Use a neutral tile where no usable file exists.

**i. Story moments:**
- At most 6 dated moments that the board cannot show, each with a reason. Candidates: Bard renamed Gemini (8 Feb 2024), chatgpt.com (May 2024), Similarweb's re-estimate (Jul 2024; this may be item c instead), DeepSeek's surge (Jan 2025), grok.com (Jan–Feb 2025).
- Only VERIFIED dates go on screen: V34 to V40 are verified. List any other moment for Cowork to check in Luke's Chrome.
- Show them as RTT-103's story card, or none. House style: where the board shows the change, leave it out.

**j. Final table (Aug 2026):** 10 s. Show it with and without a one-line summary (wording from verified figures only).

## 5. Checks and output
- Run the RTT-102 tests and the phone check on every still.
- Show that RTT-001, RTT-002, RTT-003 and RTT-103 approved output is unchanged (pixel-identical frames, as IQ-18 did).
- Render on a runner through RTT-102's own workflow, never another episode's.
- Save to a private pre-release in `race-through-time-private` with every file's SHA-256 in the release notes and `STATE.json`.
- Push your branch and open a pull request with code and written results only. Do not merge.
- Update HANDOVER and STATE.

## 6. Report
- Ask Luke numbered questions only on what is his: on-screen claims, title, rights, or choices the rules do not settle (DEC-417). Give each one your recommendation and what happens if he does not answer.
- Settle everything else yourself and list what you decided.
- Finish with a short plain-English summary for Luke: what was done (with links), what needs his decision, and the next step.
