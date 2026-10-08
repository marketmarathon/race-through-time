# Metric contract — RTT-102 AI assistant websites race · v1.1 (IQ-17b, Luke's answers and Cowork's checks) · 8 Oct 2026

v1.1 changes: the conflict rule gains Luke's step 4 (DEC-517) and Claude's proposed step 5 (DEC-524); agreement is tested between every pair; the IPO report and Similarweb's September 2026 newsletter are read; owner answers DEC-515 to DEC-522.

Written before any design work (DEC-036). Owner decisions: DEC-243 and DEC-244 (pull request #19: the episode; Similarweb used without permission, credited, stopped if Similarweb objects), DEC-245 (no contacting anyone about data), **DEC-500 to DEC-504** and **DEC-515 to DEC-522** (Luke, 7–8 Oct 2026). Claude's working choices, proposals and findings: DEC-505 to DEC-514 and DEC-523 to DEC-527, each open to Luke. Brief: `prompts/CODE_SESSION_IQ-17.md`; start message `prompts/CODE_SESSION_IQ-17_start.md`.

**Public claim:** the most-visited AI assistant websites, month by month from December 2022 to September 2026, by **Similarweb's published estimates of monthly website visits, worldwide** (desktop and mobile web). One supplier, one measure (DEC-500). **Not market share, not users, not app use.** Bars show visits, not shares (DEC-501).
**Unit:** visits in the month (a count), as Similarweb or the press quoting it printed it.
**Rank:** descending visits among the bars that have a value that month. Ties keep the previous month's order; if new, alphabetical.
**Timeline:** one value per bar per month, Dec 2022 – Sep 2026 (46 months). A bar starts at its first published month and stops at its last (no extrapolation).

## Sources (DEC-500)
- **Similarweb's own publications** (`S`): blog posts, LinkedIn posts and newsletters by Similarweb or its named staff, the 2025 table "Winners and Losers in the Gen AI Market" (21 Jan 2026), its newsletter "The Summer the AI Market Swapped Roles" (17 Sep 2026), its free website profiles, and its IPO report (17 Sep 2026: Exhibit 3 monthly rows for claude.ai, and an August 2026 snapshot with each site's peak month for six sites).
- **Reputable press quoting Similarweb** (`P`): Digiday, The Decoder, The Economic Times, Reuters, DataReportal, Rest of World.
- Every publication, with date, author, URL and data version: `data/rtt-102/source/publications.csv`.
- **Not used:** Sensor Tower (users; route not chosen), Semrush and every other panel, OECD.AI, Ofcom, referral trackers, rank lists, a16z mixes. Company user figures (research part05 D) are context only, never a bar value.
- **Data versions:** Similarweb launched a new data version on 28 Jul 2024 with "a full 5-year historical rerun" (V32). A figure published before that day is `older`, on or after it `current` (DEC-501). Older figures are shown as "Similarweb's older estimates" with a short note at the revision (a design option first, DEC-069).

## Bars and addresses (`data/rtt-102/identities.csv`)
| Bar | Address(es) counted | Label |
|---|---|---|
| ChatGPT | chat.openai.com to Apr 2024; chatgpt.com from May 2024 (Similarweb joins the two; switch day NOT FOUND) | ChatGPT |
| Gemini | bard.google.com to 7 Feb 2024; gemini.google.com from 8 Feb 2024 (V34) | "Bard" until 7 Feb 2024, "Gemini" from 8 Feb 2024 |
| Claude | claude.ai from 11 Jul 2023 (V36) | Claude |
| Copilot | copilot.microsoft.com from 15 Nov 2023 (V35); Bing chat redirected into it from about late 2024, so growth then is partly Bing's | Copilot |
| Perplexity | perplexity.ai | Perplexity |
| DeepSeek | deepseek.com, whose Similarweb total includes chat.deepseek.com (V41; DEC-502 (3)). **Never** deepseek.com + chat.deepseek.com | DeepSeek |
| Grok | grok.com from January 2025 | Grok |
| Meta AI | meta.ai from 18 Apr 2024 (V37) | Meta AI |

**Not counted:** Bing Chat inside bing.com and Grok inside x.com (no Similarweb figure isolates them); Le Chat (left out, DEC-501). In a monthly table the label and address are those in force at the end of the month (DEC-511): February 2024 reads "Gemini".

## Method (deterministic: `scripts/build_rtt102_dataset.py`)
1. **Points** (`data/rtt-102/points.csv`): one row per assistant per month per printed version in each publication, with the figure as printed, its qualifier ("about", "nearly", "more than", "preliminary"), source type, publication date, data version, URL, the wording seen at source and the check that saw it. Never invented, calculated or rounded.
2. **Verified only:** a figure is VERIFIED only when Cowork saw it at its source in Luke's Chrome (`source/verification.csv`, V01–V42, including all 84 cells of the 2025 table) or a GitHub runner read it in the page's text (`source/runner_checks.csv`, round R1). UNVERIFIED figures are listed for Cowork, never used.
3. **What counts** (DEC-506): monthly visits only. Not forecasts or projections, daily averages, unique visitors, shares or partial months. "Last month" in Digiday's 1 Dec 2023 article is read as November 2023. Lower bounds ("more than 1 billion") count, flagged `bound = lower`.
4. **Addresses** (DEC-507): a press figure that names only the product counts for the bar's one address at that month; for DeepSeek, which has two Similarweb addresses, a press figure without an address does not count. Similarweb's own "DeepSeek" means deepseek.com.
5. **Conflicts** (DEC-502 (2), DEC-508, DEC-517, DEC-523, DEC-524): never averaged. Among VERIFIED, eligible figures for the same bar and month: (1) current data version over older; (2) Similarweb's own publication over press; (3) final over preliminary; (4) the later publication over the earlier; (5) *Claude's proposal, applied until Luke decides:* within one publication, its labelled month-by-month chart or table over its prose. Figures that are the same number printed at different precision (rounded or cut, e.g. 2.6 billion and 2.595B) agree, tested between every pair; the most reliable, then most precise, then latest version is used. Anything still unresolved is a **leftover**: no figure is used (the straight line runs across) until Luke decides. Every case is in `conflicts.csv`. Nothing is derived from percentage changes, shares or quarter-to-date sums (e.g. July 2026 for ChatGPT and Gemini is a straight line).
6. **Set-asides** (DEC-509, DEC-520, DEC-525, `source/exclusions.csv`): figures contradicted by their own publication, unit slips, probable mislabelled months (including the IPO blog's "203 million" for February 2026, which is January's figure) and a press report whose data version is uncertain.
7. **Series** (`series_monthly.csv`, DEC-511): published months show the used figure exactly; months between two published months are a straight line by month (whole visits, half up), flagged `interpolated` with both end points. No value before a bar's first or after its last published month. Flags per row: `data_version` (older, current, or older->current on a line across the change), `older_estimate`, `preliminary`, `rests_on_preliminary`, `bound`.
8. **Places** (`place_changes.csv`): every change of first, second and third place, with whether both bars are published that month.
9. **Checks** (`CHECKS.md`; `python3 tests/rtt102/run_tests_rtt102.py`): every on-screen value VERIFIED with URL and wording; no averaging; no point before a site's start; one address per bar per month; DeepSeek never summed; no forecast; data version on every row; no extrapolation; leftovers unused; two clean rebuilds identical.

## Display attributes (DEC-036; built only in a later, approved design session — DEC-069)
| Attribute | Source | File / column |
|---|---|---|
| Bar value | method above | `series_monthly.csv` `visits` |
| Bar label (name at that date) | identities; Bard → Gemini 8 Feb 2024 (V34); Copilot from 15 Nov 2023 (V35) | `series_monthly.csv` `bar_label`; `identities.csv` |
| Value label: "~" + rounded | from `visits`; lower bounds "+" (house style 3; Luke, DEC-519: "more than 1 billion" shows as "1bn+"; no bar uses a lower bound at present) | `series_monthly.csv` `value_label_proposed` (**proposal**, DEC-514: "~5.9bn", "~614m", "~84.1m", "1.0bn+") |
| Date label | the month | `series_monthly.csv` `month` |
| Source line | fixed | "Estimates: Similarweb — website visits, worldwide" (brief; wording for the design session) |
| Older-estimate marking and the note at the revision | `data_version` / `older_estimate` (published before 28 Jul 2024, V32) | `series_monthly.csv` `older_estimate`, `data_version` (look and note wording: design option, DEC-501) |
| Preliminary marking (if Luke wants one) | qualifier "preliminary" | `series_monthly.csv` `preliminary`, `rests_on_preliminary` |
| "Latest figure" where a bar's figures end early | last published month (never "retired", DEC-132) | report §1 table; `series_monthly.csv` (last row of each bar) |
| Changes of first, second, third place | ranks above | `place_changes.csv` |
| Credits: Similarweb on screen and in the description (DEC-244); press articles whose figures are used, in the description | used points with source type P | report §7; `points.csv` (`used`, `source_type`, `publisher`, `url`) |
| Colours, logos, pictures, callouts | not in this phase | — |

## Claims this data cannot support
Market share or "most-used AI" (visits to websites only; app use is not counted); user numbers; anything about Bing Chat inside bing.com or Grok inside x.com; exact months of overtakes that fall on straight lines (report §2 says which); Gemini's 2024 fall as real (it crosses Similarweb's re-estimate); any month after a bar's last published figure.
