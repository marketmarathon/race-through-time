# CODE SESSION IQ-15 — RTT-101 Premier League net transfer spend: DATA BUILD, phase 1

Written by Claude in Cowork, 7 Oct 2026, for a Claude Code cloud session on `marketmarathon/race-through-time` (environment "Race Through Time").

## 1. Task and scope

Build the first version of the RTT-101 dataset: **cumulative nominal net spend on reported transfer fees by every Premier League club, month by month, 1992 to the close of the summer 2026 window**, with the reference tables it needs (membership, calendar, CPI, exchange rates) and a coverage report.

- **Data only.** No player, renderer, workflow-for-render or visual changes; nothing rendered (DEC-069).
- **Phase 1 of 2.** Phase 1 = owner decisions recorded, metric contract, reference tables, transfer skeleton, fee evidence from cited sources, scripted checks, Tier 1 list, coverage report, first (UNVERIFIED) series. Phase 2 (a later brief) = Tier 1 verification at source in batches, then the final build.
- **This is a big job and the Code usage allowance was close to its weekly limit (resets Fri 9 Oct 10:00 UK).** Work in the stages of section 9 and **commit and push after every stage**, so nothing is lost if the session stops. If you are running low, finish the current stage, push, open the pull request and report what is left.
- Luke is not technical: **finish with a short plain-English summary for him** (what was done, with links; what needs his decision, as numbered questions with your recommendation; the next step).

**First, save this exact brief as `prompts/CODE_SESSION_IQ-15.md`.** (It is also in the private repo at `research/rtt-101-chatgpt/CODE_SESSION_IQ-15_RTT-101_data.md`.)

## 2. Read first
- `CLAUDE.md` (repo rules: they all apply), `state/HANDOVER.md`, `state/STATE.json`.
- From `state/DECISIONS.md` only what you need: DEC-003, DEC-006, DEC-036, DEC-057, DEC-060, DEC-069, DEC-132, and search for "RTT-101" (nothing yet as of 7 Oct).
- `reference/metric_contract_RTT-001.md` and `scripts/build_rtt001_dataset.py` as the model for a contract and a deterministic build; `reference/rights_ledger.md`.
- **Check main AND every open pull request and branch before choosing DEC numbers.** Highest seen by Cowork on 7 Oct: **DEC-234** (branch `claude/compassionate-cray-tlnnkm`). IQ-14 is the analytics dashboard (private repo), so this task is **IQ-15**.

## 3. Inputs (private: never commit them to the public repo, DEC-006)
All in the private repo `marketmarathon/race-through-time-private`, folder `research/rtt-101-chatgpt/` (uploaded by Cowork 7 Oct 2026; byte-identical to Luke's laptop folder `Data\RTT-101_ChatGPT_answers\`). **`00_README.md` there lists every file with its SHA-256 and Claude's check notes: read it first and check the hashes.** Everything from ChatGPT is UNVERIFIED research, a list of leads, never evidence.

Most useful:
- `part09c_prompt2_record_transfer_evidence_A_PARTIAL_v2_777rows.csv` — record-fee evidence, 777 rows (replaces part08b).
- `part09b…`, `part10b…`, `part11_…`, `part12b…`, `part13b…` — big transfers by era, 1992–2026 (alternative versions share a `transfer_id`; not a complete or ranked list).
- `part14b_premier_league_transfer_conflicts_C_2026-10-06.csv` — disputed fees, 46 cases (122 of its 159 rows repeat section B: match by source, do not add).
- `part15b…` dated moments; `part16b…` Man City case timeline; `part17b…` league-wide window totals (cross-check only); `part17c…` consolidated conflicts and warnings (1,910 rows).
- `part03b…` membership (its source is CC BY-NC: **cross-check only**; its `relegated` flag is wrong for Oldham 1992–93 and Ipswich 1993–94), `part04b…` calendar, `part05b…` CPI/FX sources.
- `RTT-101_cowork_chrome_verification_2026-10-07.csv` — checks done by Cowork (section 6).
- Plan: `claude/RTT-101_project_plan_v1.md` (Cowork project; its rules are restated below).

The CSVs from 2009 on start with a UTF-8 byte-order mark.

## 4. Hard rules
Everything in `CLAUDE.md`, in particular: never touch `marketmarathon/bars`; nothing published or uploaded to YouTube; never invent, average, interpolate or forecast; never pick between disagreeing sources by averaging — keep every version and list the disagreement; only VERIFIED figures go on screen; no non-commercial data; do not install software system-wide or change credentials, settings or permissions; do not merge (DEC-057).

Episode-specific:
- **Transfermarkt (route A, owner decision below):** use it only to find which transfers happened. Its legal notice forbids reproduction "even in part" without its consent (VERIFIED, V-01), so **store nothing taken from Transfermarkt** (no lists, fees, dates, exports or cached pages) in either repo, and never use a Transfermarkt fee. Each transfer row rests on its own press or club source; where Transfermarkt pointed us to it, say so truthfully in `found_via`. If Transfermarkt blocks the container or runner, do not work around it: list what is missing for Cowork.
- Wikipedia lists and club-season pages are **pointers** (grade C): follow each row's citation and take the fee from the cited source.
- Web access: Wikimedia and some publishers rate-limit this container. Use a GitHub runner workflow for bulk fetching, the way `.github/workflows/rtt003_sources.yml` and `rtt001_assets.yml` do (no secrets, no artifacts, no cache, DEC-061), with polite rate limits. Anything you cannot reach is UNVERIFIED and listed, never guessed.

## 5. OWNER DECISIONS to record as new DEC entries
Label each "Owner (Luke, Cowork chat, <date>)".

RTT-101:
1. **4 Oct 2026:** new episode RTT-101, "Premier League Clubs: Cumulative Net Transfer Spend, 1992–2026". Neutral historical race; the Manchester City financial case is the topical hook only, neutral wording, never implying spending was wrongdoing. Main bars = cumulative **nominal** net spend in GBP (fees paid − fees received), may fall; every PL club in the data; monthly from actual transfer dates, no interpolation; **PL activity only** (frozen while relegated, resumes on return). Secondary statistic per club: average CPI-adjusted net spend per PL season played. Include permanent fees, explicit loan fees, purchase fees after loans, transfer/registration compensation, add-ons once known to be payable, sell-on payments (rule 6 below). Exclude wages, agents' fees, signing bonuses, levies, market values. Free = £0. Undisclosed fees never invented. Conflicting fees preserved. The data must also support "PL net spend by season" and "which PL clubs spend most per season".
2. **4 Oct 2026, route A:** Transfermarkt is used openly as the finding list (which transfers happened, club and season); each fee and date is taken from a named press or club source, and the record states both ("found via Transfermarkt; fee from <source>"). No bulk copying; provenance always recorded truthfully.
3. **5 Oct 2026, plan answers:** (a) episode number RTT-101; (b) the race runs to the close of the summer 2026 window (1 Sep 2026, 11pm BST) and 2026–27 counts as a season, with an on-screen/description note that figures will be updated (January 2027 window still to come); (c) season attribution switches the day after the previous season's last PL match; (d) part-exchange: a stated player valuation is counted on both sides, otherwise cash only; (e) add-ons only when a club or grade B source reports them as triggered/payable, otherwise the guaranteed fee; "up to £X" is never the fee; (f) **tiered verification** approved — Tier 1 at source by hand, Tier 2 scripted citation check, Tier 3 random sample with a published error rate — and the title says "reported transfer fees"; (g) undisclosed fees: a grade B reported figure is used and flagged "reported", otherwise £0 plus a per-club undisclosed-count report.
4. **7 Oct 2026, sell-on payments:** when a selling club owes part of a fee to a former club, deduct it from the seller's receipt **only when a club or grade B source states the amount**; otherwise count the headline fee. If the receiving former club is in the PL at that date, it counts as that club's income on the date reported.
5. **7 Oct 2026, exchange rates:** use Bank of England exchange rates freely for conversions. Luke's words: "this exchange rate thing is ridiculous … you can get this data anywhere. Let's just use it and not stress about it." Owner-accepted risk on the Bank's "selected exchange rate data" licence exclusion (V-02, V-03); record it in `reference/rights_ledger.md` as "owner-accepted risk; credited". The ECB rate (free with credit, V-05/V-06) may be used as a cross-check.
6. **7 Oct 2026, pre-1999 foreign-currency fees** (few cases): convert at the Bank of England rate for the transfer date or month and show only the GBP result, with a note of the rate used. A contemporary GBP figure from a grade A/B source is always preferred to a conversion.

Other episodes and channel (record now so the backlog clears; no work on them):
7. **4 Oct 2026, analytics dashboard:** lives at stats.marketmarathon.com on Cloudflare Pages with Google sign-in (luke@marketmarathon.com only, 30 days); DNS stays at GoDaddy with one CNAME `stats`.
8. **5 Oct 2026:** the dashboard also covers Market Marathon (buttons "Race Through Time | Market Marathon"; MM Shorts and long videos in separate tables, Shorts with shares); the Google sign-in app stays Internal. Built and merged as private PR #5.
9. **6 Oct 2026:** "AI Assistant Market Share, 2023–2026" is the next race after RTT-101, month by month. Not Luke's decisions (defaults he did not object to): number RTT-102, start Jan 2023, general-purpose assistants only.
10. **6 Oct 2026, RTT-102 data rights:** use Similarweb's figures without asking permission; credit Similarweb on screen and in the description; stop the video if Similarweb objects. Luke: "Let's not stress about getting Similarweb's permission. We will credit them, and if they have an issue with it, they can contact us, and we'll stop the video." Owner-accepted risk (rights ledger: no licence).
11. **7 Oct 2026, all episodes:** do not email or contact anybody about data (providers or companies, for data or permission); find routes that need no contact. Luke: "I don't want to be emailing anybody about data."
12. **7 Oct 2026:** new episode "The AI Spending Race — How Big Tech Started Spending Hundreds of Billions" (trailing-12-month capex, nominal US$, about 2010 to the latest common complete quarter; two series kept; ByteDance only with robust quarterly evidence; CoreWeave candidate only; no estimated or divided quarters; guidance kept separate and labelled). Not Luke's decisions: number RTT-103 and its queue position.

## 6. Verified in Cowork (Luke's Chrome, 7 Oct 2026) — re-check only if your own access works
| ID | Fact | Source | Quote |
|---|---|---|---|
| V-01 | Transfermarkt: reuse needs written consent | https://www.transfermarkt.co.uk/intern/impressum | "duplication on data media of any kind, even in part, is only permitted with prior written consent from Transfermarkt" |
| V-02 | Bank of England: OGL except selected FX | https://www.bankofengland.co.uk/legal | "selected exchange rate data and series are excluded from this licence" |
| V-03 | BoE spot rates may contain LSEG content | https://www.bankofengland.co.uk/statistics/details/further-details-about-spot-exchange-rates-data | "Republication or redistribution of LSEG content … is prohibited without the prior written consent of LSEG." |
| V-04 | BoE monthly averages exist from 1992 for DEM, FRF, ITL, ESP, NLG, PTE, USD (XUMADMS, XUMAFFS, XUMAILS, XUMASPS, XUMANGS, XUMAPES, XUMAUSS); XUMAERS (EUR) from 1999 | BoE database CSV | Jan 1992 row: "2.8564, 9.7433, 2152.4916, 181.055, 3.217, 247.3737, , 1.8127" |
| V-05 | ECB: free reuse, ECB cited | https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html | "users of this website may make free use of the information obtained directly from it" |
| V-06 | ECB GBP/EUR monthly reference rate Jan 1999–Sep 2026 | https://data-api.ecb.europa.eu/service/data/EXR/M.GBP.EUR.SP00.A?format=csvdata | 1999-01 = 0.7029125 |
| V-07 | ONS CPI D7BT, 2015=100, Jan 1988–Aug 2026, OGL v3; next release 21 Oct 2026; 1988–96 modelled | https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23 | "All content is available under the Open Government Licence v3.0" |
| V-08 | Windows from 2002/03; before that trading until 31 March | https://www.premierleague.com/en/news/60258 | "The present system was introduced for the 2002/03 season." |
| V-09 | Summer 2026 window 15 Jun–1 Sep 2026, 11pm BST | https://www.premierleague.com/en/transfers/2026-27/summer | "Window has closed Monday 15 June - Tuesday 1 September at 11pm BST" |
| V-10 | Wikipedia window lists: 49, summer 2002–summer 2026, none earlier | https://en.wikipedia.org/wiki/Category:English_football_transfer_lists | "List of English football transfers summer 2002" |
| V-11 | 51 PL clubs to 2026–27 (Wikipedia only) | https://en.wikipedia.org/wiki/List_of_Premier_League_clubs | "Over that span, 51 teams have played in the Premier League" |

Also (WebFetch only, to be re-read in Chrome before any on-screen use): Premier League statement 29 Sep 2026, https://www.premierleague.com/en/news/4727779/premier-league-statement-manchester-city-fc/ — "found Manchester City FC guilty of all charges related to serious breaches of the Premier League's financial rules over a nine-season period"; sanction "addressed separately in a further hearing". City appealed 1 Oct 2026 (per ChatGPT section E, UNVERIFIED). For `moments.csv` only, neutral wording.

## 7. Rules for the build (from the plan, as answered)
- **Season attribution:** season N runs from the day after the last PL matchday of N−1 to the last PL matchday of N (1992–93 starts the day after the last 1991–92 First Division matchday; 2015–16 ends 17 May 2016, the replayed match). A transfer counts for a club only if that club plays in the PL in season N. 2026–27 runs to the freeze (1 Sep 2026, 23:00 BST).
- **Dating:** completion/registration date, else official announcement, else first grade A/B report; record `date_basis`. Month-only dates go to that month-end, never spread.
- **Fees:** guaranteed fee; add-ons only as decision 3(e), dated when payable; loan fee at the loan date; option/obligation to buy as a separate row when exercised; compensation and tribunal fees at the decision date; sell-on as decision 4; part-exchange as decision 3(d); free £0; undisclosed as 3(g). PL-to-PL deals count at both ends; deals with non-PL or foreign clubs count only for the PL club.
- **Grades:** A = club's or league's own statement; B = high-quality contemporary press (BBC, Sky, Guardian, Times, Telegraph, Independent, PA, Reuters…); UEFA.com news reports of another party's fee = **B, not A** (finding of 6 Oct; also flagged in part17c G-1674 and 14 UEFA rows); C = specialist databases and Wikipedia (pointers); D = secondary/reconstructed. Rows ChatGPT graded A although the source says "reported"/"thought to be" are treated as reported (B).
- **Canonical fee when sources disagree:** highest grade; within a grade, the earliest contemporary report. Never average. Same-grade disagreements over 10% and £1m on Tier 1 transfers go to Luke as a list.
- **Currency:** contemporary GBP from A/B preferred; otherwise convert at the BoE daily spot for the transfer date (monthly average if no daily); store original amount, currency, rate, rate date, series code. Never convert a modern reconstructed euro figure at today's rate.
- **CPI (secondary statistic only):** each fee × CPI(base) ÷ CPI(month of transfer); base = latest D7BT month at the freeze (Aug 2026, unless Sep 2026 is published by the time you build: record which). Label "(2026 £)". Main bars never adjusted.
- **PL seasons played:** seasons whose attribution window has begun while the club is in the PL; average shown once a club has at least one season.
- **Ranking:** by cumulative nominal net at each month-end; ties: earlier arrival at the value ranks higher; bars frozen outside the PL.
- **Identity:** Wimbledon FC ≠ AFC Wimbledon / MK Dons (see part03a); one `club_id` per club, other names in `clubs.csv`.

## 8. CLAUDE'S WORKING CHOICES (record as working choices; list each as a question for Luke, never as his decision)
- W1 **Finding list:** (a) Wikipedia per-window lists 2002–2026 (V-10) for every PL club's ins and outs; (b) 1992–2002: Wikipedia club-season pages and contemporary press indexes (BBC archive pages, Guardian/Independent archives) for each PL club-season, plus the leads in the private ChatGPT files; (c) Transfermarkt consulted, not stored, to spot omissions (route A). Report coverage by era.
- W2 **Tier 1** = every fee of £20m or more nominal; every club or British record; every disputed fee (part14b, part17c); every transfer whose removal or alternative version changes the top-12 order in any month (computed). Tier 2 = £2m to under £20m (scripted check that the cited source states the figure). Tier 3 = under £2m (5% random sample, error rate published).
- W3 **Board size** for later design: dataset keeps all 51 clubs; the board size is a design question (DEC-069), not decided here.
- W4 Anything else you need to choose: record it here and ask.

## 9. Stages, deliverables and checks
Commit and push after each stage on one branch; open the pull request after stage C at the latest, then keep pushing to it.

**A. Records and contract.** DEC entries for section 5; `reference/metric_contract_RTT-101.md` listing every attribute the video will display and its source (DEC-036): club name, cumulative net (nominal), real average per PL season, PL seasons played, in/out of PL, month, source line, notes for estimates/"reported" fees, moments; rights ledger rows (Wikipedia CC BY-SA 4.0 pointers; ONS OGL v3; BoE owner-accepted risk; ECB credit; Transfermarkt not used as data).

**B. Reference tables** in `data/rtt-101/`: `clubs.csv`, `pl_membership.csv` (706 club-seasons expected; built from commercially usable sources, part03b only as a cross-check), `seasons.csv` (last PL matchday per season, attribution windows, window dates), `cpi.csv` (ONS D7BT), `fx.csv` (BoE series used, with codes), each with source columns. Checks: 22 clubs 1992–95, 20 after; membership matches part03b except the two known flag errors; every season has an attribution window.

**C. Transfer skeleton and evidence:** `transfers.csv` (one row per transfer event: transfer_id, player, from_club, to_club, type, date, date_basis, season_attributed, fee_status, original_amount, currency, fx_rate, fx_date, fee_gbp, canonical_source_id, grade, tier, status, found_via, parent_transfer_id), `fee_evidence.csv` (one row per transfer × source: amount, currency, grade, quote under 25 words, url, archive_url, retrieved), `sources.csv`. Scripted Tier 2 check results. Match the ChatGPT files' leads into this structure by source; mark each figure VERIFIED (seen by your script or runner at its source, with quote) or UNVERIFIED.

**D. Derived series and reports (UNVERIFIED preview, not for screen):** `club_ledger.csv`, `club_season.csv`, `series_monthly.csv`, `moments.csv`, `conflicts.csv`, `tier1_list.csv` (for the phase 2 verification batches), `coverage.csv` (per club and era: transfers found, fee-bearing, undisclosed with no figure, UNVERIFIED), and `reports/RTT-101_data_report.md` with: leaders over time, top-12 at key dates, the biggest open conflicts, the comparison with the league-wide window totals in part17b (gross and net per window — expect gaps; explain them, never force a match), and numbered questions for Luke with your recommendations.

**Checks** (`data/rtt-101/CHECKS.md`, deterministic build script `scripts/build_rtt101_dataset.py`, tests): no transfer outside its club's PL seasons counted; PL-to-PL deals net to zero across the league (spend − income by PL clubs = net spend with non-PL clubs); no fee without a source row; no Transfermarkt figure anywhere; quotes under 25 words; every conversion has a rate row; month-end series consistent with the ledger; totals reproduce from a clean run.

## 10. STATE and finish
- Update `state/STATE.json`, `state/HANDOVER.md` (status, open items for Luke, rules for the next RTT-101 session) and `state/DECISIONS.md`.
- Push the branch and open a pull request against `main`. **Do not merge** (DEC-057). The PR description lists what was built, check results, coverage by era, blocked sources, and numbered questions for Luke.
- Stop, then give Luke the short plain-English summary: what was done (links), what needs his decision, and the next step (phase 2 verification).
