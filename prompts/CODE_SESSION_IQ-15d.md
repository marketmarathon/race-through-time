IQ-15, source round 1, list A results (1992–93 to 1996–97) are ready. This is the ChatGPT research round Luke approved on 7 Oct (his "yes to all four": one more research round on tier1_needs_press_source.csv, starting with 1992–2002).

WHERE (private repo marketmarathon/race-through-time-private, main, folder research/rtt-101-chatgpt/; all 10 files read back byte-identical by SHA-256 after upload):
- RTT-101_chatgpt_sources_round1_1992-2002_v1.md = the prompt Luke ran.
- RTT-101_source_round1_A_1992-93_to_1996-97.csv (211 deals, A0001–A0211) and RTT-101_source_round1_B_1997-98_to_2001-02.csv (342 deals, B-ids) = the lists sent to ChatGPT. They were built by Cowork from data/rtt-101/tier1_needs_press_source.csv at commit 25fb6b7, with our fee figures removed. Map deal_id back to transfer_id on player + date (approx_date = the date in that file).
- part20b, part20d, part20f = ChatGPT's answers for list A (295 rows, 16 columns: deal_id, player, from_club, to_club, fee_as_reported, currency, guaranteed_part, add_ons_part, transfer_date_reported, publisher, publication_date, grade, exact_quote, source_url, archive_url, notes). part20a/c/e = its covering notes. 00_README.md = Cowork's notes on every file (section "Source round 1").

WHAT COWORK FOUND (internal checks plus a spot check, not a substitute for your Tier 1 check):
- All 211 deals covered; only A0038 Tommy Wright is NOT FOUND. 180 deals have a grade B source (almost all The Independent's online archive), 30 only grade C, and every quote names the player.
- In Luke's Chrome, 33 cited Independent pages were opened and all were genuine (each contains the player and fee as quoted; 24 quotes were matched word for word). The Independent's datePublished is the US-time evening before the print edition, so ChatGPT's publication_date is often one day later. Both refer to the same edition.
- In 48 deals a grade B figure differs from the fee we use. Plain examples: Toal and Beardsmore were free transfers (ours £320,000 and £210,000); Brazil £85,000 (ours £185,000); Donaghy £150,000 (ours £100,800); Klinsmann £2m (ours £2.3m); Ingesson £2m (ours £800,000); Dicks a £100,000 down-payment plus £50,000 per 25 games, completed 20 Oct 1994 (ours £1m, dated May); Hartson £5m (ours £3.3m, a later report); Des Hamilton £2.5m (ours £1.5m); Flitcroft £3.2m (ours £3.5m); Joachim £1.5m (ours £1.89m).
- Deal-structure cases, which need the rules and not a straight swap of figure:
  - Combined fees: Charles + Tommy Johnson £2.9m for the pair (our build shows £1.45m each, an equal split no source states: please remove any split that is not sourced); McKee + Whitworth £530,000; Kovačević + Stefanović £4m/£4.5m (Kovačević alone £2.5m in another B report).
  - Part-exchanges and cash adjustments: Beauchamp ↔ Whitbread (£350,000 cash, Whitbread valued £750,000); Whittingham ↔ Ian Taylor (£250,000 or £300,000 cash); Carr ↔ Parker (deal valued £550,000); Anderton + Paul Walsh; Whittingham + Mark Blake (£875,000 cash, £1.2m total also reported); Short £2.7m deal = £2.4m + Gary Rowett; Gillespie the £1m "makeweight" in the Cole deal; Burrows ↔ Cottee (retrospective "est" values only).
  - Tribunals and conditional sums: Dozzell £1.75m rising to £1.9m; Sellars tribunal value £950,000 with £720,000 paid after a sell-on; Pearson £500,000 + £250,000 on appearances; Swailes £150,000 rising to £225,000.
  - Loan, not a transfer: Lamptey (£200,000 paid; the £1m rows are an expected price).
  - Retrospective "pounds 250" rows (Mathie, Thompson) come from a Keegan table whose footnote says to add three noughts (£250,000).

PLEASE:
1. Check each list A row at source on a GitHub runner, as in phase 2: read the page and confirm the quote, player, clubs and fee. Then apply the existing rules: DEC-265 source-reading rules; the highest grade wins, then the earliest report (Luke, 7 Oct); add-ons only when reported as triggered; a stated player valuation counts on both sides, otherwise cash only; the guaranteed fee where only a maximum or "rising to" total exists; Soccerbase counts as grade C (DEC-274–277).
2. Record found_via as "ChatGPT source round 1 (DEC-264 route)", with the publisher and URL as the canonical source. Never average conflicting figures; same-grade conflicts go through the agreed rule, and any that remain go into the report for Luke.
3. Fix the deal-structure cases above (no unsourced splits), and correct dates where a grade B source dates the completion (e.g. Dicks).
4. Rebuild, run all checks, and report in reports/RTT-101_data_report.md: how many list A fees are now VERIFIED, how many changed and by how much, how the 1992–97 window totals move against published figures, and whether any leader or top-12 position changes. Commit to the branch and push; do not merge.
5. List B (1997–2002, 342 deals) is running in ChatGPT now and will follow the same way as part21….

When done, please give Luke a short plain-English summary (what changed, what it means for the race, anything that needs his decision), with your recommendation on each question.
