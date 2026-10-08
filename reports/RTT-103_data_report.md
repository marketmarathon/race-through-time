# RTT-103 The AI Spending Race — data report (IQ-16 stage 1, 7 Oct 2026; IQ-16b to IQ-16e, stages 2–5, 8 Oct 2026)

**Newest first: stages 5, 4, 3 and 2, then the stage-1 report unchanged.**

## Stage 5 (IQ-16e, 8 Oct 2026): your decisions on the measure and a draft look-ahead

**In plain English.** Your decisions A to H are recorded as DEC-321 to DEC-328. The bars stay total capital spending.
- **AI statements:** the companies' own "most of our spending is for AI" statements are now dated story moments. I read all four word for word, Tencent's included, which Cowork couldn't reach.
- **iCapital:** its 70–75% AI-share estimate is stored as an estimate that is never applied to any figure.
- **The look-ahead:** built as a **draft** worked table, with every 2027–2030 figure labelled as our estimate and its growth source named. Nothing is chosen for the screen or rendered.

### What was done
- **The part07 files:** all seven, and the prompt, match the hashes in the private README (DEC-329). They confirm that no company reports AI-only capex, so an AI-only race would need invented figures (DEC-321).
- **Story moments added to G** (COMPANY STATEMENT):
  - Microsoft, 30 Jul 2024: "nearly all", cloud and AI combined.
  - Amazon, as reported by TechCrunch, 6 Feb 2025: "vast majority" of about $100bn.
  - Tencent, 18 Mar 2026: RMB22.4bn in Q4 2025 "primarily to support our AI efforts". This is a cash figure; our Tencent bars use additions.
  - Alphabet, 29 Apr 2026: "the overwhelming majority".
  - iCapital, 30 Apr 2026: 70–75%, stored as ESTIMATE (third party).
- **Peaks** (`AI_SPENDING_RACE_PEAK_VIEWS.csv`, DEC-328): the forecasters' peak views side by side. Only verified views may go on screen; BCG and Allianz's September view are marked "not allowed" until Cowork confirms them.
- **Draft look-ahead** (`AI_SPENDING_RACE_LOOKAHEAD_DRAFT.csv`, DEC-330): the worked table below. 2026 is each company's own figure. 2027–2030 are Race Through Time estimates: the 2026 base grown year by year by one named source, so only growth rates carry over. Nothing is averaged.
- **Checks:** financial QA 81/81; format checks **41/41** (5 new); tests **34/34** (4 new).

### Draft worked table (US$ bn; ranges where the company gave a range)
| Company | 2026 (base) | 2027 | 2028 | 2029 | 2030 (least reliable) | Growth source |
|---|---|---|---|---|---|---|
| Amazon | 220.0 | 275.4 | 298.5 | 313.4 | 315.9 | own FactSet growth |
| Microsoft | 175.0 | 231.4 | 248.8 | 265.7 | 346.2 | own FactSet growth |
| Alphabet | 195.0–205.0 | 294.2–309.3 | 332.2–349.3 | 343.1–360.7 | 359.5–378.0 | own FactSet growth |
| Meta | 130.0–145.0 | 178.5–199.1 | 194.4–216.9 | 195.1–217.6 | 224.5–250.4 | own FactSet growth |
| Oracle | 90.0–95.0 | 107.6–113.6 | 105.4–111.3 | 91.9–97.0 | 83.3–88.0 | own FactSet growth |
| Alibaba | 22.3 | 24.5 | 24.4 | 25.0 | 27.4 | Citi, then FactSet five |
| CoreWeave | 35.0–39.0 | 47.1–52.5 | 51.2–57.1 | 52.6–58.6 | 57.7–64.3 | FactSet five |
| Tencent | 17.0 | 22.9 | 24.9 | 25.5 | 28.0 | FactSet five |
| Baidu | 3.3 | 4.4 | 4.8 | 5.0 | 5.4 | FactSet five |
| **Combined capital spending** | 887.6–921.6 | 1186.0–1233.1 | 1284.6–1336.0 | 1317.3–1368.5 | 1447.9–1503.6 | sum of the bars |


- **2026 is not our estimate.** It shows company guidance: Amazon and Oracle as reported by Reuters; Oracle is its fiscal year to May 2027. For Alibaba, Tencent and Baidu, where there is no guidance, it shows the actual 12 months to June 2026.
- **Checks against what the companies said:**
  - Alphabet 2027 is up 50.9%, consistent with its "increase significantly".
  - Microsoft 2027 is up 32.2%, consistent with "grow" (its fiscal year to June 2027).
- **Alternative to compare:** one group uplift (FactSet's five-company growth) applied to every US company.

| Company | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|
| Amazon | 296.3 | 322.1 | 330.5 | 362.7 |
| Microsoft | 235.7 | 256.2 | 262.9 | 288.5 |
| Alphabet | 262.6–276.1 | 285.5–300.1 | 293.0–308.0 | 321.5–338.0 |
| Meta | 175.1–195.3 | 190.3–212.3 | 195.3–217.8 | 214.3–239.1 |
| Oracle | 121.2–128.0 | 131.8–139.1 | 135.2–142.7 | 148.4–156.6 |
| Combined capital spending | 1195.3–1241.2 | 1299.4–1349.2 | 1333.5–1384.5 | 1463.3–1519.4 |


  The main difference is Oracle: FactSet sees it peaking in 2027 and falling, while a group uplift makes it rise to 2030.

### Sources I would use, and why
- **US five: each company's own FactSet growth** (consensus as of 31 Aug 2026).
  - It is the only verified multi-year forecast for each company, from one provider, for 2027–2030.
  - Only its growth rates carry over, so the companies' own 2026 figures stay and there is no false jump. Microsoft starts from its 175, not FactSet's 157.7.
- **Alibaba: Citi** (23 Sep 2026) for as far as it reaches, then FactSet's five-company growth.
- **Tencent, Baidu and CoreWeave: FactSet's five-company growth.**
  - It is a consensus of many analysts, covers every year 2027–2030, and is verified.
  - Dell'Oro's July release gives only an end point ("more than $3 trillion by 2030"). A yearly rate from it would mix two forecast vintages, so I didn't use it.
- **Not used:** AI-only forecasts (Allianz's AI capex peak), BCG (unverified), single-bank figures (unverified).

### Questions for Luke (Claude's recommendation; what happens if unanswered)
1. **US five: each company's own FactSet growth, or one group uplift for all?**
   - *Recommendation:* own growth. It keeps FactSet's view that Oracle peaks in 2027 and that the companies grow at different speeds.
   - *If unanswered:* own growth.
2. **Alibaba's starting point.** Your method (actual 12 months to June 2026, $22.3bn, plus Citi's growth) gives $24–27bn a year. Citi's own levels are far higher: about $37.8bn (2026 frame), $41.5bn and $41.4bn. Continued with FactSet's five-company growth, that path reaches about $42.4bn (2029) and $46.6bn (2030).
   - *Recommendation:* use Citi's levels for 2026–2028. Alibaba's spending is ramping fast (CEO: will "overshoot" its RMB380bn plan), so the 12-month actual understates it. Label them "Citi estimate".
   - *If unanswered:* your method as built, with Citi's levels in the notes.
3. **Tencent, Baidu and CoreWeave: FactSet's five-company growth, or something else?**
   - Dell'Oro's "nearly 60 percent" yearly growth for AI-specialised clouds (neoclouds such as CoreWeave; period not stated) would take CoreWeave to about $229–256bn by 2030, against $58–64bn as built.
   - *Recommendation:* FactSet's five-company growth for all three, with Dell'Oro's rate mentioned in narration at most.
   - *If unanswered:* as built.
4. **Oracle's 2027.** Its base is its fiscal year to May 2027 ($90–95bn). Growing that by FactSet's calendar growth gives $108–114bn for 2027, while FactSet's own Oracle 2027 is $92.1bn, so the method probably overstates Oracle in 2027–2028.
   - *Recommendation:* keep one rule for everyone and flag Oracle's 2027 in the notes.
   - *If unanswered:* as built.
5. **The 2026 frame mixes periods:** full-year guidance for the US companies and CoreWeave; actual 12 months to June 2026 for Alibaba, Tencent and Baidu.
   - *Recommendation:* accept it and label each bar's period.
   - *If unanswered:* as built.
6. **Microsoft 2030** ($346bn) rests on FactSet's weakest cell (+30% in one year).
   - *Recommendation:* keep it, inside the "least reliable year" marking you asked for.
   - *If unanswered:* kept and marked.
7. **2031:** no authoritative growth projection covering 2031 has been verified. BCG's chart is waiting on Cowork; Bain's 2031 figure is one worldwide AI-infrastructure level, a different measure.
   - *Recommendation:* stop at 2030. Revisit only if Cowork confirms BCG, and even then BCG's group change would have to be applied to every company.
   - *If unanswered:* stop at 2030.
8. **The look-ahead's starting point.** The race ends at June 2026 (12-month total $625.5bn); the 2026 frame totals $888–922bn, because it shows full-year plans.
   - *Recommendation:* show the 2026 frame as its own step, labelled "2026 plans", so the jump is explained.
   - *If unanswered:* a design-session question.

### Next
1. Your answers to 1–8.
2. Cowork's checklist results (BCG and FactSet's definition first).
3. I finalise the look-ahead and mark what goes on screen.
4. The design session for the story moments, the iCapital estimate, the running total, the look-ahead's look and the peak views.


## Stage 4 (IQ-16d, 8 Oct 2026): the look-ahead to 2031, checked at source

**In plain English.** I checked ChatGPT's look-ahead figures at their sources.
- **FactSet:** the table Cowork found is exactly as ChatGPT gave it, including Microsoft's surprising 2030 figure.
- **Visible Alpha:** a second consensus source measures the same lines as our bars, but only reaches 2027.
- **Where coverage runs out:** after 2030 nothing exists per company, and outside the US five almost nothing could be checked.
- **Status:** 82 verified rows are loaded with their forecaster, type, date and measure. Nothing is chosen for the screen and nothing is rendered.

### What was confirmed at source
- **FactSet consensus (Morgan Stanley PDF, 17 Sep 2026, Exhibit 13).**
  - **How it was read:** morganstanley.com refuses our computers, so I read an Internet Archive copy of the official PDF (DEC-318).
  - **Cells:** all 47 Capex cells match, for both the 31 Aug 2025 and the 31 Aug 2026 tables.
  - **Units:** "Calendar Yrs; $BB". The note says "Data calendarized; Estimates are FactSet consensus."
  - **Microsoft 2030 (312.0):** printed exactly like that. The year-on-year change cell is N/A, because the 2025 table had no Microsoft 2030 figure, and Microsoft's 2030 sales estimate jumps 25% in the same table. The source itself says these estimates "become less reliable further into the forecast horizon".
  - **What "Capex" means:** not stated. The PDF never defines it, never mentions leases and doesn't say how it calendarises.
  - **A clue, not proof:** FactSet's Microsoft 2026 figure (157.7) is close to Visible Alpha's cash figure (153.7), not Microsoft's own ~175 that includes leases. That suggests a cash basis.
- **Visible Alpha consensus (S&P charts, 22 Jul 2026, read by eye).**
  - **Lines used:** the same cash-flow lines our race uses.
  - **History versus our figures:**
    - Alphabet and Meta: equal to our numbers exactly.
    - Amazon: gross purchases, about 3% above our net figure.
    - Microsoft: its "calendar" years are the average of two fiscal years (DEC-317).
  - **Coverage:** Amazon, Alphabet, Microsoft and Meta, 2026–2027 (Meta to 2028). No Oracle.
- **Citi on Alibaba (Sina, 23 Sep 2026):** 258bn, 283bn and 282bn yuan for its fiscal years 2027–2029. Citi assumes the spending is shared with partners.
- **Group views confirmed:**
  - **Morgan Stanley Research:** "five largest U.S. technology companies", about $800bn (2026), about $1.2tn (2027) and $1.4tn (2028). The page doesn't name the five, so the SpaceX claim is unchecked.
  - **Bain:** $780bn in 2026 for the five; $1.5tn in 2031 for all AI infrastructure worldwide.
  - **Dell'Oro:** more than $3tn of data-centre capex worldwide by 2030.
  - **Allianz (March):** over $600bn in 2026; growth slowing to about 5% by 2028.
  - **DBS:** 2027 growth could slow.
- **Could not be checked (Cowork checklist, 37 items):**
  - BCG's chart (blocked, and it needs reading by eye);
  - Allianz's September peak view;
  - Fitch and S&P Ratings on CoreWeave;
  - Citi's table for Tencent and Baidu;
  - Goldman on Tencent;
  - McKinsey;
  - the single-bank figures in MarketWatch, Barron's, Investing.com and IBD.

### Coverage (verified only)
| Company | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---|---|---|---|---|
| Amazon, Microsoft, Alphabet, Meta, Oracle | FactSet (+ Visible Alpha, not Oracle) | FactSet (Meta also Visible Alpha) | FactSet | FactSet | none |
| Alibaba | Citi (FY to Mar 2028) | Citi (FY to Mar 2029) | none | none | none |
| Tencent, Baidu, CoreWeave | none verified | none | none | none | none |
| Groups | Morgan Stanley Research, Visible Alpha, DBS (direction) | Morgan Stanley Research | (BCG unverified) | Dell'Oro (worldwide) | Bain (worldwide AI infrastructure); BCG unverified |

### On the draft rule (FactSet 8/31/26, 2027–2030, US five; a group total to 2031 from one forecaster)
- **The draft fits the coverage:** FactSet is the only consistent series for the US five, and it reaches 2030.
- **Use FactSet for the 2026 bars too, and show company guidance only as a label.** Otherwise the bases mix: Microsoft would jump from ~175 (company figure, including leases) to 208.5 (FactSet, apparently cash). On FactSet's own basis it goes 157.7 to 208.5.
- **The basis is not proven.** FactSet doesn't define "Capex" or say how it calendarises. Visible Alpha does match our lines, but only to 2027. Cowork could try to find FactSet's definition.
- **Microsoft 2030 is the weakest cell.** Consider ending the per-company bars at 2029, or flag 2030 on screen.
- **A BCG closing total would contradict the bars before it.** If Cowork confirms BCG's chart, its 2027 total (884) is far below what the FactSet five add up to (1,066; I added them only to compare). Its peak in 2029 also conflicts with FactSet still rising in 2030 and Allianz saying 2028. The honest "peak" story is that forecasters disagree.
- **CoreWeave would leave the race at the look-ahead.** It has no verified forecast, and nor do Tencent or Baidu. Alibaba has Citi only.

### Checks
- **Financial QA:** 81/81 PASS.
- **File-format checks:** **36/36 PASS**. New: every look-ahead figure is printed in its own quote in the source's units; fiscal years sit in the right frame; there is one current figure per forecaster, company and year.
- **Tests:** **30/30 PASS**. New: all 25 FactSet cells; the old vintage is superseded; no unverified forecaster appears.
- **Quotes:** each look-ahead quote was re-found in its source by script.

### Next
1. Luke picks the rule.
2. Cowork works through the checklists.
3. I set `selected_for_screen` to match the rule.
4. The design session.


## Stage 3 (IQ-16c, 8 Oct 2026): company forecasts, the look-ahead and OpenAI

**In plain English.** ChatGPT's forecast and OpenAI lists were checked against the original pages wherever we could reach them. The 2026 frame now has the latest company figures for six companies, plus ByteDance greyed. The data files can now hold your look-ahead to 2031, with every figure's forecaster named; they are ready for ChatGPT's analyst results. OpenAI now has 15 checked story moments, all labelled COMMITMENT. Nothing is rendered or published. The historical race is unchanged.

### Your decisions recorded
- **DEC-306:** a look-ahead to 2031, using analyst forecasts where a company gives no figure. This is an exception for the closing section only.
- **DEC-307:** Alibaba's figures before April 2016 are kept as reported, flagged, with a note for the description. Draft wording is in `K_recommended_dataset.md`.
- **DEC-308:** absent bars and late entrants will be decided in the design session.
- **DEC-309:** ByteDance is shown as "more than US$29.3bn".
- **DEC-310:** Cowork's checks.

### The 2026 frame (each company's latest figure)
| Company | 2026 figure | What it is |
|---|---|---|
| Alphabet | US$195–205bn | company guidance (22 Jul call) |
| Amazon | US$220bn | as reported by Reuters from the CEO (30 Jul); Amazon publishes no written transcript |
| Microsoft | about US$175bn | calendar 2026, including finance leases. Lower than April's US$190bn only because of a lease-accounting change; **never shown as a cut** |
| Meta | US$130–145bn | including finance-lease payments |
| Oracle | US$90–95bn | its fiscal year June 2026 – May 2027, as reported by Reuters (10 Sep). Oracle's own releases print no figure |
| CoreWeave | US$35–39bn | from its 11 Aug call transcript; its release has no capex figure |
| ByteDance (greyed) | more than US$29.3bn | press report, unnamed sources |

- **Not in the frame:**
  - **Alibaba:** it gives only a multi-year plan (at least RMB380bn over three years from February 2025, since said to be "overshot"). It is never divided into years.
  - **Tencent:** its press quotes could not be checked; its own announcements give no outlook.
  - **Baidu:** gives no outlook.
- **Oracle's measure (DEC-312):** Oracle now also reports a "net cash outlay" figure, which deducts customer prepayments: US$47.7bn against US$55.7bn of capex last year. The report does not say which measure its US$90–95bn uses.
- **Oracle's placement:** its fiscal year runs June 2026 to May 2027, so it sits in the 2026 frame (DEC-314). It is labelled as its own fiscal year.

### 2027 and later
- **Company statements so far:**
  - Alphabet: "increase significantly" in 2027.
  - Microsoft: its fiscal 2027 (to June 2027) "will grow".
  - Meta: said it is not giving a 2027 outlook.
  - Nothing for 2028–2031.
- **How these rows are held:** as stated, with no figures.
- **The data files** (DEC-314):
  - `F` keeps the brief's columns.
  - A companion input, `source/forecast_lookahead_2027_2031.csv`, holds the look-ahead: one row per forecaster, company and year, with its quote. It is empty until ChatGPT's results are checked.
  - The forecast file gains these columns: forecaster, forecaster type (company, consensus, analyst, research firm), forecast date, measure, scope (company or group) and "selected for screen".
- **Labels:** analyst figures will be labelled, for example, "2028 ANALYST FORECAST (bank name)" and "not official", in their own style.
- **New checks block:**
  - any average or blend of forecasters;
  - any figure that is not printed in its own quote;
  - any year outside 2026–2031;
  - any analyst figure labelled as guidance.

### OpenAI (story moments only)
- **15 moments, checked from partner releases and SEC filings:**
  - Microsoft (2023 investment; the US$250bn Azure purchase, Oct 2025);
  - Oracle (2024);
  - CoreWeave (up to US$11.9bn, US$4.0bn and US$6.5bn; "approximately $22.4 billion" in total);
  - AMD (6 GW);
  - NVIDIA (at least 10 GW);
  - Cerebras (750 MW);
  - Tata (100 MW, option to 1 GW);
  - Amazon (US$100bn added to a US$38bn AWS deal; a US$50bn investment);
  - SB Energy and NVIDIA (an 8 GW site in Ohio leased to OpenAI; NVIDIA guarantees capped at US$105bn);
  - Firmus (Malaysia).
- **How they are labelled:** all COMMITMENT; never capex, never a bar and never added up, because the totals overlap.
- **Still to check:** openai.com refuses our computers, so 22 rows, including the Stargate announcements, are on a checklist for Cowork in the private repo. The 3 rows ChatGPT marked not eligible stay out.

### Checks
- **Financial QA:** 81/81 PASS.
- **File-format checks:** 33/33 PASS (9 new).
- **Tests:** 27/27 PASS, including a byte-identical rebuild.
- **Quotes:** every quote written into F and G was re-found word for word in its source document by script (35 of 35).
- **ChatGPT's files:** the hashes and row counts of all four matched your message.

### Questions for Luke (stage 3; Claude's recommendation)
- **D. How should press-reported company figures (Amazon US$220bn, Oracle US$90–95bn) be labelled on screen?**
  - *Recommendation:* show them like the other company figures, with a small "as reported by Reuters" note.
  - *If unanswered:* that note.
- **E. Should Oracle sit in the 2026 frame, given that its fiscal year runs June 2026 to May 2027?**
  - *Recommendation:* yes, labelled "fiscal year to May 2027".
  - *If unanswered:* as recommended.
- **F. Look-ahead selection rule:** this will be proposed once ChatGPT's coverage is checked (DEC-306). No question yet.

### Next
1. Cowork works through the 28 checks on the private checklist.
2. ChatGPT's look-ahead results arrive and are checked at source.
3. Claude proposes the one-figure-per-company-per-year rule.
4. Design session.


## Stage 2 (IQ-16b, 8 Oct 2026): Luke's answers applied

**In plain English.** All ten answers are recorded (DEC-291 to DEC-301) and applied. The race now has nine companies, with CoreWeave joining at the end of 2024. Alibaba's gap is smaller and its 2017–2018 figures are now rebuilt from Alibaba's own numbers. The forecast frames hold only the companies' own guidance, plus ByteDance greyed as a press report. Nothing is rendered or published.

### What each answer led to
| # | Your answer | What was done |
|---|---|---|
| 1 | Option C; the title names total capital spending (DEC-291) | K marked APPROVED; title rule added to the metric contract and `reference/house_style.md` (example: "Big Tech's Capital Spending, 2010–2026"). |
| 2 | Tencent kept with a note (DEC-292) | Every Tencent row in the master carries the note "measured differently - additions, including some intangible assets". Exact on-screen wording is a design question. |
| 3 | Amazon net (DEC-293) | No change needed. |
| 4 | Alibaba: its own re-presented figures (DEC-294) | Found and used (see below, DEC-303). |
| 5 | CoreWeave as a late entrant (DEC-295) | Added from its first published quarter (Q1 2024); first bar at **2024 Q4**, once four quarters exist. Eligibility table says ADDED. |
| 6 | ByteDance only in the 2026 frame, greyed, after reading the SCMP article (DEC-296) | The article was read at source (9 May 2026): "more than 200 billion yuan (US$30 billion), according to two people familiar with the matter". In the 2026 frame only, greyed, as "more than US$29.3bn" (converted at the 2026 average H.10 rate to date). Never in the historical race. |
| 7 | 2026 frame with ranges; roll forward to 2027–2028 with companies' own forecasts (DEC-297) | New `AI_SPENDING_RACE_FORECAST.csv` (DEC-304); `AI_SPENDING_RACE_2026E.csv` is its 2026 part. Ranges always carry both ends. 2027 holds only Alphabet ("increase significantly") and Microsoft (year to June 2027, "grow year-over-year"); 2028 is empty until company statements are checked. No analyst forecasts. |
| 8 | H.10, everything in US$ (DEC-298) | Confirmed; no change. |
| 9 | Catalogue private (DEC-299) | Confirmed; no change. |
| 10 | Cowork's checks (DEC-300) | Alphabet 2026 guidance now **$195–205bn** (22 Jul 2026 call); $175–185bn and $180–190bn kept as superseded. Amazon stays "about $200 billion". |
| — | OpenAI never a bar or capex (DEC-301) | A new format check fails the build if OpenAI or ByteDance ever appears as a bar. |

### Alibaba: stage 1 got the dates wrong, now corrected (DEC-303)
- Alibaba's capex included licensed copyrights (from the Youku deal) from **April 2016**, not January 2017 as stage 1 said.
- Alibaba's FY2019 annual report (20-F) re-presents FY2017 and FY2018 on its later, narrower scope. Its quarterly releases from Sep 2018 to Jun 2019 re-present each earlier quarter the same way. From these, the five quarters Jun 2017 to Jun 2018 are rebuilt exactly; they add up to Alibaba's own FY2018 total (RMB19,628m).
- The four quarters Apr 2016–Mar 2017 cannot be split, so they stay out. **Alibaba now has no bar for seven TTM points (2016 Q2 to 2017 Q4)**, instead of stage 1’s eight (2017 Q1 to 2018 Q4). Stage 1 wrongly showed bars for 2016 Q2–Q4; the four 2018 points now have bars.
- Before April 2016, Alibaba's figure also includes small intangible purchases (5.2% in FY2015, 6.6% in FY2016). These quarters are kept and flagged (DEC-302; question A below).

### Alphabet's equity raise (DEC-305)
- Alphabet's 8-K of 4 Jun 2026 was read at source. It describes an equity raise "to fund investments in its world-class AI compute infrastructure", priced on 2 Jun 2026 at **$84.75bn** in total (this includes a $40bn at-the-market programme sold over time).
- It is added to the story moments (G) as financing, not capex.

### At the end of June 2026 (12 months to the latest quarter)
| Rank | Company | US$ bn |
|---|---|---|
| 1 | Amazon | 169.0 |
| 2 | Alphabet | 132.4 |
| 3 | Microsoft | 115.9 |
| 4 | Meta | 89.3 |
| 5 | Oracle | 55.7 |
| 6 | Alibaba | 22.3 |
| 7 | CoreWeave | 20.6 |
| 8 | Tencent | 17.0 |
| 9 | Baidu | 3.3 |

- **Race total:** US$625.5bn, up 80.0% on a year earlier. CoreWeave pushes Tencent and Baidu down one place each; the order of the top six is unchanged.
- **Turning points:**
  - The leader and first-past-the-mark moments are unchanged from stage 1.
  - The total passed US$100bn at the end of 2020, US$250bn at the end of 2024 (US$264.3bn, with CoreWeave's first bar) and US$500bn in Q1 2026 (US$526.7bn).

### Checks
- **Financial QA:** PASS for all nine companies, 81 of 81 checks.
- **File-format checks:** PASS, 24 of 24. The four new checks are:
  - every cited source is listed in A;
  - OpenAI and ByteDance never appear as bars;
  - the forecast frames hold company guidance only, plus the greyed ByteDance row;
  - every range has both a low and a high.
- **Tests:** 19 of 19 pass (`python tests/rtt103/run_tests_rtt103.py`), including a byte-identical rebuild.
- **Master:** 496 bars.
- **Cross-checks** (for information): unchanged. The same two intra-year restatements are listed in I. Private vendor data agrees for all five CoreWeave quarters.

### Questions for Luke (stage 2)
- **A. Alibaba before April 2016** (DEC-302): its figure includes 5–7% intangible purchases, which cannot be split by quarter. Should these quarters be kept, flagged?
  - *Recommendation:* keep them with the data flag. The effect is small, and leaving them out would remove Alibaba from 2014 to 2016.
  - *If unanswered:* kept, flagged.
- **B. How absent bars look** (Alibaba 2016 Q2–2017 Q4) and how a late entrant arrives (CoreWeave at 2024 Q4): this is a design question (DEC-069).
  - *Recommendation:* decide it in the design session, with options side by side.
  - *If unanswered:* nothing is built.
- **C. ByteDance's figure in the frame:** show "more than US$29.3bn" (converted by us) or SCMP's own "US$30 billion"?
  - *Recommendation:* US$29.3bn. It uses the same exchange-rate method as every other figure (DEC-298), and the note quotes the yuan figure.
  - *If unanswered:* US$29.3bn.

### Still to do
- **ChatGPT's results** (2026–2028 company forecasts, OpenAI commitments): awaited. When they arrive, each will be checked at source before any row is filled. 2028 is empty until then.
- **The design session:** logos, colours, notes, absent bars, frames. Nothing is built without your approval.

---

# Stage 1 report (IQ-16, 7 Oct 2026)

**For Luke, in plain English.** The data for the AI Spending Race is built for all eight companies, from 2010 to the end of June 2026, and every figure in the race was read in the company's own filing. Nothing has been rendered or published. Below: what was built, what passed, what is missing, and ten questions (each with Claude's recommendation).

## What was built
- **The race:** trailing-12-month capital expenditure in US dollars for Amazon, Microsoft, Alphabet (Google), Meta (Facebook), Oracle, Alibaba, Tencent and Baidu, quarter by quarter from 2010 Q1 to **2026 Q2**, the last quarter every company has reported. 488 bars in `data/rtt-103/AI_SPENDING_RACE_MASTER.csv`.
- **Where the numbers come from:**
  - US companies: 339 quarterly and annual SEC reports (2009–2026). Each number was taken from the cash-flow statement *as printed* (2,133 printed values matched; values not printed in the statement were never used).
  - Baidu: its quarterly results on sec.gov (2009–2026).
  - Alibaba: its quarterly results from Alibaba's investor site and sec.gov (2013–2026).
  - Tencent: its HKEXnews announcements (2011–2026).
  - Exchange rate: the Federal Reserve's daily rates (H.10), averaged over each company quarter.
- **Every brief file:** A to L and both master files, with the brief's exact columns, in `data/rtt-103/` (see its README).
- **Also built:** the CoreWeave eligibility table, 2026 guidance (F) and the 2026 end frame, 20 sourced AI/cloud statements (G), and 13 turning points calculated from the data.

### At the end of June 2026 (12 months to the latest quarter)
| Rank | Company | US$ bn | Basis |
|---|---|---|---|
| 1 | Amazon | 169.0 | cash, net of proceeds and incentives |
| 2 | Alphabet | 132.4 | cash purchases of property and equipment |
| 3 | Microsoft | 115.9 | cash additions to property and equipment |
| 4 | Meta | 89.3 | cash purchases of property and equipment |
| 5 | Oracle | 55.7 | cash capital expenditures (year to 31 May 2026) |
| 6 | Alibaba | 22.3 | cash capex (RMB, converted quarter by quarter) |
| 7 | Tencent | 17.0 | additions incl. some intangible assets (RMB) |
| 8 | Baidu | 3.3 | cash purchases of fixed assets (RMB) |
Race total: US$604.9bn, up 78.5% on a year earlier. CoreWeave, not in the race, would rank 7th (US$20.6bn).

### Turning points (from `narrative_checkpoints.csv`)
- Microsoft led in early 2010.
- Alphabet led from the end of 2010.
- Amazon led briefly in late 2012, then again from Q3 2020 onwards.
- Alphabet was first above US$25bn (end of 2018); Amazon was first above US$50bn (Q3 2021), above US$100bn (Q2 2025) and above US$150bn (Q2 2026).
- The eight-company total passed US$100bn in 2020, US$250bn in 2024 and US$500bn in Q1 2026.

## What passed
**Financial QA** (the brief's section 25; `J_QA_report.md`): **PASS for all eight companies**, 71 of 71 checks. The checks were:
- the quarters add up to each printed year;
- every TTM recalculated;
- quarter lengths and calendar placement;
- signs, units and wrong lines (free cash flow, depreciation, acquisitions);
- no zero or negative quarters;
- exchange-rate range and direction;
- every input read at its source.

**File-format checks:** PASS, 20 of 20. These cover exact columns, allowed H values, one row per key, sort order and the 2026E labels. The tests (`tests/rtt103/run_tests_rtt103.py`) pass 13 of 13; they include a rebuild that matches the committed files byte for byte.

**Independent cross-checks** (for information; every difference is listed in file I):
- **Agree:**
  - Amazon's own printed 12-month figures, all 50.
  - Meta's release figures, 55 of 56.
  - Alphabet's quarterly figures printed in its reports, 9 of 10.
  - The licensed vendor data, which stays private: Amazon 69/69, Microsoft 69/69 and Oracle 67/69 quarters equal.
- **Differ:** two quarters, where a company restated an earlier figure during the year: Alphabet Q3 2016 by 1.1% and Meta Q4 2018 by 1.6%.
- **The vendor's differences** (Meta, Alphabet 2009–2015, Alibaba) are explained in file I. In every case the filing value stands.

## What is missing or weak (all in `I_conflicts_and_warnings.csv`)
- **Alibaba 2017–2018:** for five quarters (Jan 2017 to Mar 2018) Alibaba reported capex together with intangible assets. These are not mixed in, so Alibaba has no bar for the TTM points 2017 Q1 to 2019 Q1.
- **Tencent's measure is different:** it is *additions* (an accounting measure, not cash) and includes some intangible assets. Tencent prints its cash figure only half-yearly.
- **Microsoft's own "capex including finance leases"** is quoted only on its earnings calls. The race uses its cash figure, like the other US companies.
- **Amazon:** its cash figure is net of incentives for the whole period, because Amazon printed gross purchases only from 2017. The difference is about 2% now and 13% in 2017.
- **Missing quarters:**
  - Not public: Tencent before 2011, Alibaba before mid-2013 and Meta before 2012.
  - So the race starts with 5 companies in 2010; Meta joins in 2012, Tencent in 2011 Q4 and Alibaba in 2014 Q1.
- **2026 guidance not yet checked at source:**
  - Alphabet's reported raise to $180–190bn. TrendForce reports it; Alphabet's own site refused the download.
  - Amazon's and Alphabet's later updates on their calls.
  - Any 2026 guidance from Oracle, Tencent, Alibaba and Baidu.
  - Reuters items, which refused access.

## Questions for Luke (Claude's recommendation; what happens if unanswered)
1. **Which series powers the race?**
   - *Recommendation:* option C, "cash spent on property and equipment as each company reports it" (see `K_recommended_dataset.md`). Series A cannot be used because Microsoft has no published figure, and series B would leave Amazon out until 2017.
   - *If unanswered:* stage 2 continues on C as a working assumption; nothing is rendered.
2. **Tencent:** keep it in the race with an on-screen note ("additions, including some intangible assets"), or leave it out?
   - *Recommendation:* keep it with the note (it is one of the nine companies the industry tracks, and its definition is printed in every announcement).
   - *If unanswered:* it stays in the data, flagged, and the design session asks again.
3. **Amazon's net figure:** OK to show Amazon net of incentives for the whole race (its own capex measure; about 2% below gross today)?
   - *Recommendation:* yes.
   - *If unanswered:* as recommended.
4. **Alibaba's 2017–2019 gap:**
   - *Recommendation:* stage 2 looks for Alibaba's own re-presented figures (its FY2019 annual report) to close the gap. Until then its bar is absent for those points. How to show an absence is a design question for you (DEC-069).
   - *If unanswered:* the gap stays.
5. **CoreWeave** (US$20.6bn in the year to June 2026, but quarterly figures only from 2024):
   - *Recommendation:* keep it out of the race and mention it in narration.
   - *If unanswered:* out.
6. **ByteDance in the 2026 end frame** (a press report from unnamed sources: "more than 200 billion yuan"):
   - *Recommendation:* leave it out of the on-screen frame, or show it only as "press report".
   - *If unanswered:* out of the frame, kept in F.
7. **The 2026 end frame at all?** Company guidance uses different definitions: Meta adds lease payments, Microsoft adds finance leases and uses a calendar year.
   - *Recommendation:* show it as a separate, clearly labelled "2026 guidance" frame with ranges, never midpoints alone.
   - *If unanswered:* no 2026 frame.
8. **Exchange rate method** (working choice DEC-281: Federal Reserve daily rates averaged over each quarter):
   - *Recommendation:* confirm.
   - *If unanswered:* stays.
9. **Public source list** (DEC-285): the brief asks for ChatGPT's catalogue rows to be appended to file A unchanged. Your rule DEC-006 keeps research inputs private. Claude kept the full catalogue private and listed only the sources it opened in the public file A.
   - *Recommendation:* confirm.
   - *If unanswered:* stays private.
10. **Unchecked 2026 guidance:**
    - *Recommendation:* ask Cowork to open Alphabet's Q1/Q2 2026 call pages and Amazon's latest call in your Chrome and record the figures. Alphabet's site refuses GitHub runners.
    - *If unanswered:* 2026E uses the last verified figures (Alphabet $175–185bn, Amazon about $200bn).

## Working choices and findings recorded
- **Working choices:** DEC-281 (exchange rates), DEC-282 (Sharadar as cross-check only), DEC-284 (quarters as first reported; rounded first prints) and DEC-285 (public source list).
- **Proposal:** DEC-283 (option C).
- **Findings:** DEC-286 (definitions by company) and DEC-287 (source access).
- **Also recorded:** DEC-288 (latest common quarter), DEC-289 (Sharadar's definition) and DEC-290 (tests).

## COMPLETED / STILL TO DO
- **COMPLETED:** sections A to L, both master files, the CoreWeave eligibility table and the narrative checkpoints, for all eight companies.
- **STILL TO DO** (stage 2, after Luke's answers):
  - close Alibaba's 2017–2018 gap if a re-presented source exists;
  - the 2026 guidance checks in question 10;
  - Microsoft's call-quoted capex history (only if wanted);
  - the design session (logos, colours, labels) — nothing is built without Luke's approval.
