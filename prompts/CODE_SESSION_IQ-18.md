IQ-18 — RTT-103 "The AI Spending Race": design pilot, round 1 (brief written in Cowork, 8 Oct 2026)

TASK. First design round for RTT-103. Build the episode's kit on the existing player and show Luke every open design question as options side by side, mostly as stills (each also at phone size), with one short clip only where motion is the question. The data is final on main (PR #20 merged by Luke on 8 Oct 2026, merge commit 9742721): do not change any figure. No full film, no music (Luke picks the track later), nothing published. Luke is not technical: finish with a short plain-English summary for him.

FIRST, save this brief word for word as prompts/CODE_SESSION_IQ-18.md.

READ FIRST. The repo's CLAUDE.md (its rules apply in full); state/HANDOVER.md (RTT-103 stage 6) and state/STATE.json; reference/metric_contract_RTT-103.md; data/rtt-103/README.md; reference/house_style.md (section 5 now carries RTT-103's rules: DEC-291, 292, 295–297, 306, 311, 313, 314, 321–328); reference/rights_ledger.md. Check open pull requests and branches first. RTT-001's approved design (film approved, DEC-233; choices DEC-184–203) sits on the unmerged branch claude/compassionate-cray-tlnnkm (PR #18), including its house_style additions (board sized to the entries on it, logo tiles, big date top right, "~" estimates with a source line, era photo box, no callouts for visible changes). Read them there and reuse that player work rather than rebuilding it; say in your PR how you brought it in.

DECISION NUMBERS. RTT-103 uses the block DEC-331–DEC-399; the next free number should be DEC-342 (check main and every open PR). Never use DEC-400–499 (RTT-101) or DEC-500 onwards (RTT-102).

OWNER DECISIONS to record first (Luke, Cowork chat, 8 Oct 2026; his answers to IQ-16f's three questions):
1. CoreWeave 2027: keep the one rule (FactSet five-company growth) even though both rating agencies expect a dip (Fitch about $41bn to $37bn; S&P about $31bn to $25bn); the expected dip goes in the notes or narration, not on the bar.
2. Tencent's verified statement that it "aims to boost capital expenditure in 2026" (Investing.com/Reuters, 18 Mar 2026) appears as a short labelled note beside Tencent's bar, with no number.
3. Allianz's AI capex peak ("peak at USD1trn in 2028", 28 Sep 2026) appears in the "forecasters disagree" step, labelled "AI capex (Allianz)", beside BCG and FactSet, and is never added to "Combined capital spending".
Also record as a fact: Luke merged PR #20 on 8 Oct 2026.

ROUND 1: show each item as labelled options (A/B/C) side by side. Stills unless the question is motion.
a. Board and bars: all companies on the board (up to nine); value label style (e.g. "$169.0bn"); the date line (e.g. "12 months to Jun 2026" versus "Q2 2026"); two or three title options that name the measure (DEC-321).
b. Company identity: a logo per bar versus the name only. Logos are for identification only; every file needs a recorded basis in the rights ledger (as for RTT-001) and lives only in the private repo. Show both.
c. Late entrants and gaps: Meta (2012), Alibaba (2014) and CoreWeave (2024 Q4) joining from their first valid point (DEC-295); Alibaba's seven-point gap (mid-2016 to end-2017): options such as the bar held dimmed with a short "figures not comparable" note versus the bar leaving and returning.
d. Tencent: placement of its "measured differently" note (DEC-292) and of owner decision 2's 2026 note.
e. Story moments: the companies' own "most of our capex is for AI" statements (DEC-322), the OpenAI COMMITMENT moments (never added together) and the Alphabet share sale. Show how a dated moment appears without breaking house style's "callouts are rare" rule (for example one line under the title for about 3 s, a small lower card, or a marker on the date line), and propose a shortlist of at most eight moments that earn a place, each with a reason. Luke chooses.
f. Luke's bottom-right running total, "Combined capital spending", across the whole film (DEC-324): two or three options (a counting number, a small line chart that grows, a small single bar), each at phone size, and how it behaves when a company joins or has a gap.
g. The "2026 plans" step after the race: each bar labelled with its period, ranges shown as ranges, ByteDance greyed as a press report, "as reported by Reuters" labels (DEC-311). Two options.
h. The look-ahead 2027–2030 (Race Through Time estimates, growth source named, Oracle 2027–28 flagged as probably high, 2030 marked least reliable; DEC-326, DEC-327): two or three looks that are clearly different from the historical race.
i. "Forecasters disagree on the peak" (DEC-328): BCG (peak 2029, US five), FactSet (still rising in 2030) and Allianz (AI capex, 2028): two layouts; never one closing figure.
j. iCapital's "an estimated 70–75%" (DEC-323), once near the end, labelled as an estimate: placement options.
k. Pace: one clip of the same passage (suggest 2020–2026, where Amazon takes the lead) at two or three speeds per quarter, and your estimate of the total running time for each.
l. Draft footer credits and the final table (10 s hold, house style).

OUTPUTS. A private pre-release in marketmarathon/race-through-time-private with side-by-side contact sheets (c01, c02 …), stills plus their phone-size versions, and the pace clip(s), with a SHA-256 for every file. The public pull request holds the kit, configs and tests only. Run the existing test suites before rendering, and show that RTT-002's approved output is unchanged if you touch shared player code.

QUESTIONS. Numbered questions for Luke in the PR and in your summary, each with your recommendation and what happens if he does not answer, so he can reply "1 A, 2 yes". Anything beyond the items above goes in as a proposal, not built (DEC-069).

STATE. Record the DECs, update state/STATE.json and state/HANDOVER.md, push a branch and open a pull request. Do not merge (DEC-057). Stop and give Luke the short plain-English summary.
