# CODE SESSION IQ-16c — RTT-103 stage 3: ChatGPT forecasts and OpenAI commitments (brief as received, 8 Oct 2026)

Saved word for word (CLAUDE.md, "Read first" 6).

---

ChatGPT's forecast and OpenAI results have arrived (Luke ran the prompt 8 Oct). They are in the private repo, research/rtt-103/ on main, all read back byte-identical:
- part05a_forecasts_part1_forward_capex.csv (60 rows; SHA-256 c126854cb5fb879a9926ef9dda05bc6c938e9adc35ca7d3a87970c8ddbc24952)
- part05b_forecasts_part2_openai_commitments.csv (38 rows; 3565530772aa71b2694a7f08fb893d1106b3e48ae6b25d8cc64bf43850330370)
- part05c_forecasts_part3_conflicts_and_warnings.csv (49 rows; 685a2ec030520d7fb623f5ffd5885e9f91e17856448c6a3b55d6d2c20efff8ca)
- RTT-103_chatgpt_forecasts_2026-2028_v1.md (the prompt; 4c6e563e4e2dedb257e0d9edd21bb02a78fc43873d6e240fb0bb2c5eec5e1913)
All rows are UNVERIFIED leads until checked at source.

Already checked at source by Cowork in Luke's Chrome on 8 Oct (record as Cowork checks):
- Microsoft FY26 Q4 call, 29 Jul 2026 (microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4): "Outside of this useful life impact, our calendar year 2026 CapEx investment expectations remain unchanged." / "However, the shift from finance to operating leases adjusts our expectation to approximately $175 billion." / "And we expect FY27 capital expenditures will grow year-over-year given demand signals across our portfolio." So roughly $190bn (Apr) to approximately $175bn (Jul) is an accounting change, not a cut; never show it as one.
- Meta Q2 2026 release, 29 Jul 2026 (investor.atmeta.com ... Meta-Reports-Second-Quarter-2026-Results): "We anticipate 2026 capital expenditures, including principal payments on finance leases, to be in the range of $130-145 billion, narrowed from our prior outlook of $125-145 billion."
- Amazon: Reuters, 30 Jul 2026 ("Amazon lifts investment plans after strong cloud sales; shares jump", reuters.com/business/retail-consumer/amazon-beats-estimates-quarterly-cloud-revenue-growth-2026-07-30/): "Amazon CEO Andy Jassy said demand remained so strong that the company still lacked enough computing capacity to serve customers despite raising its capital spending forecast by 10% to $220 billion." Grade B (press reporting the CEO; Amazon publishes call audio only). Latest Amazon 2026 figure = $220bn, replacing "about $200 billion".
- Oracle: Reuters, 10 Sep 2026 ("Oracle tops estimates as AI demand tempers cash-burn fears", reuters.com/technology/oracles-quarterly-revenue-beats-estimates-ai-boom-drives-cloud-demand-2026-09-10/): "Oracle said that most of the newly contracted revenue will not require large cash outlays for chips, helping it maintain its annual spending target of $90 billion to $95 billion." Grade B; fiscal 2027 ending May 2027 per the ChatGPT rows (check at source).
- CoreWeave: its Q2 2026 release (sec.gov exhibit coreweave2q26earningspress.htm) has no capex guidance; the $35–39bn 2026 range is only in the call transcript PDF on s205.q4cdn.com (see part05a). Please read the transcript PDFs on a runner.

Please now: (1) check every remaining part05a row that would appear in the forecast frame or the 2027 direction notes at its source on a runner (CoreWeave transcripts, Alibaba announcements, Tencent/Baidu, Alphabet June 2026 investor presentation); anything you can't reach, list for Cowork to read in Luke's Chrome. (2) Update F and the 2026E file: latest company figure per company, ranges kept, definitions as stated (Meta incl. finance-lease principal; Microsoft incl. finance leases, calendar 2026; Oracle fiscal year to May 2027; Amazon company-wide, not AWS or AI-only), previous guidance kept with superseded set. (3) 2027 and 2028: ChatGPT found NO company figure for either year, only directions (Alphabet "significantly increase" in 2027; Microsoft FY27 "will grow"; Meta declined to give a 2027 outlook; nothing for 2028). Record these as DIRECTION ONLY rows and do not create numeric 2027/2028 values; how (or whether) the video shows them is a question for Luke. (4) OpenAI (part05b): check the rows at source (openai.com, partner releases, SEC); verified ones become story moments in G labelled COMMITMENT, never capex, never a bar, never summed (part05c warns the Stargate totals overlap); rows marked NOT ELIGIBLE in part05c (unnamed sources, government figures) stay out. (5) Alibaba's 380bn-yuan multi-year plan is not annual guidance: never divide it into years.

Your questions A–C are with Luke; carry on with your recommended defaults meanwhile (A keep flagged; B design session; C US$29.3bn). Push to the PR #20 branch, do not merge, nothing rendered, and finish with a short plain-English summary for Luke.

---

## Update from Luke (Cowork chat, 8 Oct 2026), received mid-session, word for word

Update from Luke (Cowork chat, 8 Oct 2026); please record these as owner decisions (new DECs) and adjust the work you are doing now.

1. FORECAST SECTION EXTENDED (changes my earlier instruction that 2027/2028 are direction-only): Luke wants the video to end with a clearly labelled, speculative look ahead, ideally five years (to 2031), to show where AI capex is heading (the ramp-up and any expected peak and slow-down). Sources in order: the company's own forecasts first; where a company has given no figure, published analyst forecasts (named consensus provider, named bank or research firm). Luke's words: "We don't have to be too freaked out by it being accurate because of course how can it be accurate? We're just trying to make it as accurate as we possibly can." This is an owner exception to the standing rule "never use a forecast", for this closing section only: it must look visibly different from the historical race, every figure labelled with its forecaster and type (company / consensus / analyst), never presented as official, never averaged or blended between forecasters, and never extended beyond the years a source gives. The historical race (actuals to June 2026) is unchanged.
Cowork has given Luke a new ChatGPT prompt for this (private repo research/rtt-103/ will get it with the answers): company statements, consensus, named analysts and research firms for 2027–2031 per company, group totals, and peak/slow-down views. Please don't research analyst forecasts yourself; prepare F, the 2026E file (or a companion forecast file if the brief's schema can't hold it — tell me which) and the checks so they can hold years to 2031 with forecaster, forecaster_type, forecast_date and measure, and keep 2027 direction-only company rows as they are. The rule for choosing one figure per company per year will be proposed to Luke once we see the coverage.
2. Your question A (Alibaba before April 2016, 5–7% intangibles): keep the quarters as Alibaba reported them, with a flag and a note for the description. No percentage deduction (Luke offered "take about 6% off" as an alternative but said not to stress; Cowork recommends no estimated adjustment to historical bars, and Luke left it to us).
3. Question B: yes, decide in the design session with options side by side.
4. Question C: "more than US$29.3bn" (our exchange-rate method), Luke left it to us.

Carry on with the rest of my previous message (checks at source, OpenAI story moments, Alibaba plan never divided). Push to the PR #20 branch, do not merge, nothing rendered; short plain-English summary for Luke at the end.
