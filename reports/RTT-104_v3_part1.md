# RTT-104 V3 — Part 1: what caused each big change (IQ-24b, 16 Oct 2026)

**Status: STOPPED AT THE COST CHECK (brief step 2). Nothing was fetched from IPU Parline.** The change list is built from our own data; causes are not yet researched. Brief: `prompts/CODE_SESSION_IQ-24b.md`. Decisions DEC-660..DEC-665.

## 1. The change list (built)
- `data/rtt-104/v3_change_events.csv`, from `python3 scripts/rtt104_v3_changes.py data/rtt-104` — same figures and rules as `boards.csv` (4 m threshold, latest-year population, single-gap "latest figure"); ranked with the same sort as the approved boards (value high to low, then name). The script stops if its top 10 differs from `boards.csv`'s top board in any year (it does not).
- Ranks are full ranks among every country in the race that year, so a country moving from 42nd to 2nd shows both numbers.
- **44 countries** were ever in a top 20 (1997–2025). They have **1,210 year-to-year rows**, of which **611 are visible** (top 20 in either year) and **179 are big** (visible and ≥ 5.0 points or a move of 3+ places), across **41 countries**.
- Big for points (≥ 5.0): **51** (31 countries). Big for rank only: **128** — and **50 of those moved less than 1 point** (median 1.3 points). The 3-place rule mostly catches small shuffles inside a tight pack, not events.
- Rows where a figure starts: China and Laos join in 1998 at 15th and 16th (no 1997 figure); Afghanistan joins in 2005 at 20th. They have no change in points, so they are not "big".
- **DEC-625:** no country loses its parliament while in the top 20 (no visible row ends with a missing figure).
- 10 big changes involve a "latest figure" year (DEC-617), noted on their rows.

## 2. Cost check (brief step 2) — over the limit, so stopped
- Each big change needs its country's chamber election list plus the election page inside its window: **41 chamber pages + up to 179 election pages, about 220 pages** — well over the brief's ~80. Per the brief, nothing was fetched; this is pushed for Luke.
- Narrower alternatives (Claude proposal, DEC-665; Luke picks):
  - **A. Points rule only (≥ 5.0 points):** 51 changes, 31 countries → about 31 + 51 = **~82 pages**, at the limit. Most tags in any one year: 5 (2008). **Recommended.**
  - B. ≥ 7.5 points: 31 changes, 25 countries, ~56 pages. C. ≥ 10 points: 21 changes, 19 countries, ~40 pages.
  - D. As briefed (179 changes, ~220 pages): about three times the cost of A, and most of the extra rows are sub-point shuffles that an election tag would rarely explain.

## 3. How busy the screen would be (tags per year, from our data)
| Rule | Tags by to-year (1998 → 2025) | Most in one year |
|---|---|---|
| As briefed (179) | 6 5 10 3 4 12 6 7 4 3 6 8 1 7 8 4 10 4 4 11 2 14 6 7 3 8 7 9 | **14** (2019) |
| Points only (51) | 0 2 3 2 1 4 2 3 2 0 5 2 0 2 3 2 2 1 0 4 2 4 2 0 0 1 1 1 | **5** (2008) |

## 4. The largest big changes (all "not yet researched")
| Country | Years | Value (%) | Points | Rank |
|---|---|---|---|---|
| Bolivia | 2013→2014 | 25.4 → 53.1 | +27.7 | 42 → 2 |
| United Arab Emirates | 2018→2019 | 22.5 → 50.0 | +27.5 | 61 → 4 |
| Rwanda | 2002→2003 | 25.7 → 48.8 | +23.1 | 18 → 1 |
| Angola | 2007→2008 | 15.0 → 37.3 | +22.3 | 71 → 8 |
| Senegal | 2011→2012 | 22.7 → 42.7 | +20.0 | 42 → 4 |
| Nicaragua | 2010→2011 | 20.7 → 40.2 | +19.6 | 55 → 7 |
| Belarus | 2003→2004 | 10.3 → 29.4 | +19.1 | 65 → 16 |
| Nepal | 2007→2008 | 17.3 → 33.2 | +15.8 | 58 → 15 |
| Costa Rica | 2001→2002 | 19.3 → 35.1 | +15.8 | 28 → 5 |
| Bulgaria | 2000→2001 | 10.8 → 26.3 | +15.4 | 52 → 14 |

No cause is claimed for any of them: none has been looked up at its source yet.

## 5. Windows (proposed for the fetch, DEC-665; no case matched yet, so no borderline list yet)
DEC-621 found that a WDI year has no single date. Proposed rule: the change from year Y−1 to Y is matched to a general election of the lower or single house **held in calendar year Y** (most tested WDI years describe the position at the end of Y or 1 January Y+1). Exceptions: 1997 = 1 Jan 1997 and 1998 = 10 Aug 1998 (WDI's own note), so 1997→1998 runs 2 Jan 1997–10 Aug 1998 and 1998→1999 runs 11 Aug 1998–31 Dec 1999. **Borderline** = an election within about two months of a window edge (Nov–Feb), or a mid-year election that DEC-621 shows can lag into the next year's figure (Kuwait 2013): these are listed for Luke, never silently assigned.

## 6. Checks — `python3 tests/rtt104/check_v3_changes.py`
- Values equal `series.csv` (the WDI figures on this branch): 2,420/2,420 PASS.
- Election rows with a Parline URL and a dated excerpt: 0/0 (none yet) PASS.
- V2 film config, film workflow and music file byte-identical to c379631: PASS. RTT-104 data tests 23/23 PASS.

## 7. Questions for Luke
1. **Rights:** may V3 tags use IPU Parline election dates (same non-commercial IPU terms as DEC-608; owner-accepted risk as DEC-623, credited "IPU Parline")? Recommendation: yes, on the DEC-623 basis. Default if no answer: no Parline dates on screen; V3 not published.
2. **Part 2, or a narrower Part 1 first?** Recommendation: **not Part 2 yet** — first run the look-ups with the points-only rule (option A, ~82 pages, at most 5 tags a year), then decide on design once we know how many have a sourced cause. Default if no answer: nothing more is fetched.
