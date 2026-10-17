# IQ-24c — RTT-104 V3 Part 1, continued: check the election dates and match them to the changes

v1, 17 Oct 2026 (Cowork). Continue in this session on the same branch and pull request #24 (next DEC after DEC-665; check). Luke is not technical: finish with a short plain-English summary. Keep it lean: Luke is saving allowance.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-24c.md`.

## Owner decisions to record
- **Owner DEC** (Luke, Cowork, 16 Oct 2026 16:42 BST): **yes to IPU Parline election dates for the V3 tags.** Credit "IPU Parline", on the same owner-accepted-risk basis as DEC-623. Add it to the rights ledger.
- **Owner DEC** (Luke, Cowork, 16 Oct 2026 16:44 BST): **the date gathering goes to ChatGPT deep research, not Claude**, to save allowance. Luke ran the Cowork prompt `RTT-104_chatgpt_parline_elections_v1`.
- **Claude DEC**: Cowork recommended that "big" means changes of 5 points or more. Luke did not answer that question, so treat it as the working default, not an owner decision. Report both rules below so he can choose at the design stage.

## The attached file: a to-check list, not evidence
`rtt104_v3_candidate_events.csv` (attached; 490 rows, 44 countries, 1996–2025) is derived by Cowork from ChatGPT's answer. It lists:
- general elections, partial renewals, and dissolutions or suspensions;
- quota or seat laws, appointed seats, newly formed parliaments, and other events.

By-elections were left out on purpose. 480 rows have an IPU Parline URL.

Every row is UNVERIFIED for us, whatever ChatGPT's own status column says.
- **Do not commit this file or its quotes to the public repo.** ChatGPT material stays on Luke's laptop (DEC-006).
- What goes in the repo is only what our runner retrieves itself: the URL plus an excerpt taken from the fetched page.

## Steps
1. **Verify with a script, not by reading.** On a GitHub runner, as in IQ-20, a script fetches each claimed URL and checks that the claimed date appears on the page.
   - Parse the dates in code. Do not have the model read pages one by one.
   - Keep only short excerpts, and keep raw pages out of the public repo.
   - A row becomes **VERIFIED** only if the fetched page shows the date. Otherwise it is **UNVERIFIED**, with the reason (page did not open, date not found, or date differs).
   - Where the page shows a different date, record both and flag it. Never pick one.
   - **Cost guard:** if Parline blocks the runner or most fetches fail, stop and report. Do not fall back to reading pages by hand.
2. **Match.** For every visible change in `data/rtt-104/v3_change_events.csv` (611), apply the DEC-621 window rules from the brief:
   - **election**: only a VERIFIED general election or partial renewal of that chamber inside the window;
   - **other**: only a VERIFIED sourced event of another kind;
   - **unexplained**: everything else.

   Flag borderline windows.
3. **Report.** Append to `reports/RTT-104_v3_part1.md`, for two rules:
   - (a) changes of 5 points or more;
   - (b) the earlier rule: 5 points or more, or a move of 3 or more places.

   For each rule give:
   - how many changes are explained by an election, by another cause, or not at all;
   - tags per year, and the most in any one year;
   - the 10 largest unexplained changes;
   - the rows that failed verification, grouped by reason.

No player, stills, clip or render in this session.

## Checks
- Every "election" or "other" row in the CSV has a URL and an excerpt that our runner fetched.
- Values still equal the WDI figures.
- V2 config and workflow are byte-identical to c379631.

Update `state/`, push to pull request #24, and do not merge.

## Questions for Luke (numbered; give your recommendation and the default for each)
1. Go on to Part 2, the design round (top-20 board, tags, scale, pace)?
2. Which tag rule: (a) or (b)?

Finish with the plain-English summary.
