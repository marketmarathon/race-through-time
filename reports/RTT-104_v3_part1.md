# RTT-104 V3 — Part 1: what caused each big change (IQ-24b, 16 Oct 2026)

**Status (17 Oct 2026, IQ-24c): causes matched — see section 8.** (IQ-24b stopped at the cost check below; Luke then had ChatGPT gather the dates, DEC-667, and our runner checked them.) Brief: `prompts/CODE_SESSION_IQ-24b.md`. Decisions DEC-660..DEC-665.

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

## 8. IQ-24c (17 Oct 2026): ChatGPT's dates checked by our runner, then matched
Brief `prompts/CODE_SESSION_IQ-24c.md`; decisions DEC-666..DEC-671.

**How.** Cowork's to-check list (490 rows, 44 countries, derived from ChatGPT; SHA-256 `a0c9949d91fa2905bc9d511d9cbad92d71e24b67a6b82ce8eeaf19c0b39ed991`) is **not committed** (DEC-006). Only its 345 distinct URLs went to the runner (`data/rtt-104/source/v3_fetch_urls.txt`). Run https://github.com/marketmarathon/race-through-time/actions/runs/39015680991 fetched them: **343 of 345 opened** (2 timed out), so the cost guard was not triggered. It kept short excerpts only: dated lines and lines naming the kind of event (`data/rtt-104/source/fetch_2026-10-17_run39015680991_v3dates/`).

`scripts/rtt104_v3_verify.py` then parsed the dates in those excerpts in code: English, Spanish, Portuguese, German and French month names, day lists and ranges, and ISO and dd/mm/yyyy dates.
- **VERIFIED** means a parsed date equals the claimed date (both ends of a range).
- For a non-election event, a word naming that kind of event must also stand in the same excerpt line.
- Wikipedia is not counted as a primary source.
- Result: **374 of 490 rows VERIFIED** (`data/rtt-104/v3_verified_events.csv`).

**Matching (`data/rtt-104/source/v3_causes.csv`, copied into `v3_change_events.csv`).** This uses the window rule of DEC-665: the change from year Y−1 to Y is matched to an event in calendar year Y, except that 1997→1998 runs 2 Jan 1997–10 Aug 1998 and 1998→1999 runs 11 Aug 1998–31 Dec 1999.
- An event that spans several days or rounds is placed by its first day; one that runs past the window's end is flagged.
- **Election** = a VERIFIED general election or partial renewal in the window.
- **Other** = a VERIFIED event of another kind. A dissolution followed within six months by a VERIFIED election is treated as the routine step before that election, not as a cause (DEC-669).
- **Borderline** = within 2 months of a window edge, or just outside it.

**Finding (DEC-670).** 4 of the 5 unexplained rule-(a) changes have a VERIFIED general election in November or December, just before their window: Turkmenistan Dec 2004 and Dec 1999, Austria Nov 2002, and Mozambique Dec 1999 under rule (b). For late-year elections, WDI's figure for that year often still shows the old parliament, as DEC-621 found. Moving such elections to the next year's change is a rule for Luke (question 3). It has not been applied.

### Rule (a): 5 points or more (working default, DEC-668) — 51 changes
- Explained by a VERIFIED election: **46 (90%)**; by another VERIFIED cause: **0 (0%)**; unexplained: **5 (10%)**.
- Borderline window (flagged on the row): 16.
- Tags per year (explained changes only; all a-rule changes in brackets), 1998 → 2025: 1998: 0 (0) · 1999: 2 (2) · 2000: 1 (3) · 2001: 2 (2) · 2002: 1 (1) · 2003: 3 (4) · 2004: 2 (2) · 2005: 2 (3) · 2006: 2 (2) · 2007: 0 (0) · 2008: 5 (5) · 2009: 2 (2) · 2010: 0 (0) · 2011: 1 (2) · 2012: 3 (3) · 2013: 2 (2) · 2014: 2 (2) · 2015: 1 (1) · 2016: 0 (0) · 2017: 4 (4) · 2018: 2 (2) · 2019: 4 (4) · 2020: 2 (2) · 2021: 0 (0) · 2022: 0 (0) · 2023: 1 (1) · 2024: 1 (1) · 2025: 1 (1)
- Most tags in one year: **5** (2008).

Largest unexplained changes, rule (a):

| Country | Years | Value (%) | Points | Rank | Borderline note |
|---|---|---|---|---|---|
| Turkmenistan | 2004→2005 | 26.0 → 16.0 | -10.0 | 20 → 51 | 2004-12-19 general election just outside the window (VERIFIED) |
| Rwanda | 1999→2000 | 17.1 → 25.7 | +8.6 | 29 → 16 | — |
| Turkmenistan | 1999→2000 | 18.0 → 26.0 | +8.0 | 26 → 14 | 1999-12-12 general election just outside the window (VERIFIED) |
| Austria | 2002→2003 | 26.8 → 33.9 | +7.1 | 15 → 10 | 2002-11-24 general election just outside the window (VERIFIED) |
| Tanzania | 2010→2011 | 30.7 → 36.0 | +5.3 | 22 → 16 | — |

### Rule (b): 5 points or more, or 3+ places (the earlier rule) — 179 changes
- Explained by a VERIFIED election: **99 (55%)**; by another VERIFIED cause: **2 (1%)**; unexplained: **78 (44%)**.
- Borderline window (flagged on the row): 39.
- Tags per year (explained changes only; all b-rule changes in brackets), 1998 → 2025: 1998: 3 (6) · 1999: 3 (5) · 2000: 1 (10) · 2001: 2 (3) · 2002: 3 (4) · 2003: 3 (12) · 2004: 3 (6) · 2005: 4 (7) · 2006: 3 (4) · 2007: 1 (3) · 2008: 6 (6) · 2009: 6 (8) · 2010: 1 (1) · 2011: 4 (7) · 2012: 6 (8) · 2013: 3 (4) · 2014: 4 (10) · 2015: 3 (4) · 2016: 2 (4) · 2017: 8 (11) · 2018: 2 (2) · 2019: 8 (14) · 2020: 2 (6) · 2021: 4 (7) · 2022: 2 (3) · 2023: 5 (8) · 2024: 3 (7) · 2025: 6 (9)
- Most tags in one year: **8** (2017, 2019).

Largest unexplained changes, rule (b):

| Country | Years | Value (%) | Points | Rank | Borderline note |
|---|---|---|---|---|---|
| Turkmenistan | 2004→2005 | 26.0 → 16.0 | -10.0 | 20 → 51 | 2004-12-19 general election just outside the window (VERIFIED) |
| Rwanda | 1999→2000 | 17.1 → 25.7 | +8.6 | 29 → 16 | — |
| Turkmenistan | 1999→2000 | 18.0 → 26.0 | +8.0 | 26 → 14 | 1999-12-12 general election just outside the window (VERIFIED) |
| Austria | 2002→2003 | 26.8 → 33.9 | +7.1 | 15 → 10 | 2002-11-24 general election just outside the window (VERIFIED) |
| Tanzania | 2010→2011 | 30.7 → 36.0 | +5.3 | 22 → 16 | — |
| Mozambique | 1999→2000 | 25.2 → 30.0 | +4.8 | 13 → 8 | 1999-12-03 general election just outside the window (VERIFIED) |
| Argentina | 2001→2002 | 26.5 → 30.7 | +4.3 | 13 → 8 | — |
| South Africa | 1997→1998 | 25.0 → 28.8 | +3.8 | 12 → 7 | — |
| Spain | 2013→2014 | 36.0 → 39.7 | +3.7 | 18 → 10 | — |
| Spain | 1998→1999 | 24.7 → 21.6 | -3.2 | 14 → 18 | — |

### Visible changes overall (611)
- election 175, other 5, unexplained 431.

### Rows of the to-check list that failed verification (116 of 490; 374 VERIFIED)

**date shown, but no word naming the event beside it: 71** (dissolved or suspended 67, quota or seat law 3, appointed seats 1)
- Australia, dissolved or suspended, claimed 2016-05-09 — https://data.ipu.org/parliament/AU/AU-LC01/election/AU-LC01-E20160702/
- Australia, dissolved or suspended, claimed 2019-04-11 — https://data.ipu.org/parliament/AU/AU-LC01/election/AU-LC01-E20190518/
- Australia, dissolved or suspended, claimed 2022-04-11 — https://data.ipu.org/parliament/AU/AU-LC01/election/AU-LC01-E20220521/
- Australia, dissolved or suspended, claimed 2025-03-28 — https://data.ipu.org/parliament/AU/AU-LC01/election/AU-LC01-E20250503/
- Austria, dissolved or suspended, claimed 2017-11-09 — https://data.ipu.org/parliament/AT/AT-LC01/election/AT-LC01-E20171015/
- Austria, dissolved or suspended, claimed 2019-10-23 — https://data.ipu.org/parliament/AT/AT-LC01/election/AT-LC01-E20190929/
- Austria, dissolved or suspended, claimed 2024-10-24 — https://data.ipu.org/parliament/AT/AT-LC01/election/AT-LC01-E20240929/
- Belgium, dissolved or suspended, claimed 2014-04-28 — https://data.ipu.org/parliament/BE/BE-LC01/election/BE-LC01-E20140525/
- Belgium, dissolved or suspended, claimed 2019-05-23 — https://data.ipu.org/parliament/BE/BE-LC01/election/BE-LC01-E20190526/
- Bulgaria, dissolved or suspended, claimed 2017-01-27 — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20170326/
- Bulgaria, dissolved or suspended, claimed 2021-03-26 — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20210404/
- Bulgaria, dissolved or suspended, claimed 2021-05-11 — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20210711/
- Bulgaria, dissolved or suspended, claimed 2021-09-15 — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20211114/
- Bulgaria, dissolved or suspended, claimed 2022-08-02 — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20221002/
- Bulgaria, dissolved or suspended, claimed 2023-02-02 — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20230402/
- Bulgaria, dissolved or suspended, claimed 2024-06-19 — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20240609/
- Canada, dissolved or suspended, claimed 2015-08-02 — https://data.ipu.org/parliament/CA/CA-LC01/election/CA-LC01-E20151019/
- Canada, dissolved or suspended, claimed 2019-09-11 — https://data.ipu.org/parliament/CA/CA-LC01/election/CA-LC01-E20191021/
- Canada, dissolved or suspended, claimed 2021-08-15 — https://data.ipu.org/parliament/CA/CA-LC01/election/CA-LC01-E20210920/
- Canada, dissolved or suspended, claimed 2025-03-23 — https://data.ipu.org/parliament/CA/CA-LC01/election/CA-LC01-E20250428/
- Costa Rica, dissolved or suspended, claimed 2022-04-30 — https://data.ipu.org/parliament/CR/CR-LC01/election/CR-LC01-E20220206/
- Denmark, dissolved or suspended, claimed 2015-06-18 — https://data.ipu.org/parliament/DK/DK-LC01/election/DK-LC01-E20150618/
- Denmark, dissolved or suspended, claimed 2019-06-05 — https://data.ipu.org/parliament/DK/DK-LC01/election/DK-LC01-E20190605/
- Ecuador, appointed seats, claimed 2008-10-29 — https://data.ipu.org/election-summary/HTML/2095_08.htm
- Ecuador, dissolved or suspended, claimed 2017-05-14 — https://data.ipu.org/parliament/EC/EC-LC01/election/EC-LC01-E20170219/
- Ecuador, dissolved or suspended, claimed 2023-05-17 — https://data.ipu.org/parliament/EC/EC-LC01/election/EC-LC01-E20230820/
- Ethiopia, dissolved or suspended, claimed 2021-07-07 — https://data.ipu.org/parliament/ET/ET-LC01/election/ET-LC01-E20210621/
- Finland, dissolved or suspended, claimed 2015-04-22 — https://data.ipu.org/parliament/FI/FI-LC01/election/FI-LC01-E20150419/
- Finland, dissolved or suspended, claimed 2019-04-17 — https://data.ipu.org/parliament/FI/FI-LC01/election/FI-LC01-E20190414/
- Finland, dissolved or suspended, claimed 2023-03-29 — https://data.ipu.org/parliament/FI/FI-LC01/election/FI-LC01-E20230402/
- France, dissolved or suspended, claimed 2017-06-20 — https://data.ipu.org/parliament/FR/FR-LC01/election/FR-LC01-E20170611/
- France, dissolved or suspended, claimed 2024-06-09 — https://data.ipu.org/parliament/FR/FR-LC01/election/FR-LC01-E20240630/
- Germany, dissolved or suspended, claimed 2017-10-24 — https://data.ipu.org/parliament/DE/DE-LC01/election/DE-LC01-E20170924/
- Germany, dissolved or suspended, claimed 2021-10-26 — https://data.ipu.org/parliament/DE/DE-LC01/election/DE-LC01-E20210926/
- Germany, dissolved or suspended, claimed 2024-12-27 — https://data.ipu.org/parliament/DE/DE-LC01/election/DE-LC01-E20250223/
- Mexico, dissolved or suspended, claimed 2018-08-31 — https://data.ipu.org/parliament/MX/MX-LC01/election/MX-LC01-E20180701/
- Mozambique, dissolved or suspended, claimed 2025-01-12 — https://data.ipu.org/parliament/MZ/MZ-LC01/election/MZ-LC01-E20241009/
- Nepal, dissolved or suspended, claimed 2007-01-15 — https://data.ipu.org/election-summary/HTML/2386_07.htm
- Nepal, dissolved or suspended, claimed 2025-09-12 — https://data.ipu.org/parliament/NP/NP-LC01/election/NP-LC01-E20260305/
- Netherlands, dissolved or suspended, claimed 2017-03-23 — https://data.ipu.org/parliament/NL/NL-LC01/election/NL-LC01-E20170315/
- Netherlands, dissolved or suspended, claimed 2021-03-25 — https://data.ipu.org/parliament/NL/NL-LC01/election/NL-LC01-E20210317/
- New Zealand, dissolved or suspended, claimed 2017-08-22 — https://data.ipu.org/parliament/NZ/NZ-LC01/election/NZ-LC01-E20170923/
- New Zealand, dissolved or suspended, claimed 2020-09-06 — https://data.ipu.org/parliament/NZ/NZ-LC01/election/NZ-LC01-E20201017/
- Nicaragua, dissolved or suspended, claimed 2016-12-15 — https://data.ipu.org/parliament/NI/NI-LC01/election/NI-LC01-E20161106/
- Nicaragua, dissolved or suspended, claimed 2021-12-15 — https://data.ipu.org/parliament/NI/NI-LC01/election/NI-LC01-E20211107/
- Peru, dissolved or suspended, claimed 2019-09-30 — https://data.ipu.org/parliament/PE/PE-LC01/election/PE-LC01-E20200126/
- Portugal, dissolved or suspended, claimed 2015-10-22 — https://data.ipu.org/parliament/PT/PT-LC01/election/PT-LC01-E20151004/
- Portugal, quota or seat law, claimed 2019-03-29 — https://files.dre.pt/1s/2019/03/06300/0176701769.pdf
- Portugal, dissolved or suspended, claimed 2019-10-24 — https://data.ipu.org/parliament/PT/PT-LC01/election/PT-LC01-E20191006/
- Portugal, dissolved or suspended, claimed 2021-11-04 — https://data.ipu.org/parliament/PT/PT-LC01/election/PT-LC01-E20220130/
- Portugal, dissolved or suspended, claimed 2024-01-15 — https://data.ipu.org/parliament/PT/PT-LC01/election/PT-LC01-E20240310/
- Portugal, dissolved or suspended, claimed 2025-03-19 — https://data.ipu.org/parliament/PT/PT-LC01/election/PT-LC01-E20250518/
- Rwanda, dissolved or suspended, claimed 2018-08-09 — https://data.ipu.org/parliament/RW/RW-LC01/election/RW-LC01-E20180903/
- Rwanda, dissolved or suspended, claimed 2024-06-14 — https://data.ipu.org/parliament/RW/RW-LC01/election/RW-LC01-E20240715/
- Senegal, dissolved or suspended, claimed 2024-09-12 — https://data.ipu.org/parliament/SN/SN-LC01/election/SN-LC01-E20241117/
- Serbia, dissolved or suspended, claimed 2016-03-04 — https://data.ipu.org/parliament/RS/RS-LC01/election/RS-LC01-E20160424/
- Serbia, dissolved or suspended, claimed 2023-11-01 — https://data.ipu.org/parliament/RS/RS-LC01/election/RS-LC01-E20231217/
- Spain, dissolved or suspended, claimed 2016-05-03 — https://data.ipu.org/parliament/ES/ES-LC01/election/ES-LC01-E20160626/
- Spain, dissolved or suspended, claimed 2019-03-05 — https://data.ipu.org/parliament/ES/ES-LC01/election/ES-LC01-E20190428/
- Spain, quota or seat law, claimed 2024-08-02 — https://www.boe.es/buscar/act.php?id=BOE-A-2024-15936
- Sweden, dissolved or suspended, claimed 2014-09-29 — https://data.ipu.org/parliament/SE/SE-LC01/election/SE-LC01-E20140914/
- Switzerland, dissolved or suspended, claimed 2015-11-30 — https://data.ipu.org/parliament/CH/CH-LC01/election/CH-LC01-E20151018/
- Tanzania, dissolved or suspended, claimed 2015-08-20 — https://data.ipu.org/parliament/TZ/TZ-LC01/election/TZ-LC01-E20151025/
- Tanzania, dissolved or suspended, claimed 2020-06-16 — https://data.ipu.org/parliament/TZ/TZ-LC01/election/TZ-LC01-E20201028/
- Turkmenistan, quota or seat law, claimed 2008-09-26 — https://data.ipu.org/election-summary/HTML/2325_08.htm
- Uganda, dissolved or suspended, claimed 2016-05-11 — https://data.ipu.org/parliament/UG/UG-LC01/election/UG-LC01-E20160218/
- Uganda, dissolved or suspended, claimed 2021-05-11 — https://data.ipu.org/parliament/UG/UG-LC01/election/UG-LC01-E20210114/
- United Kingdom, dissolved or suspended, claimed 2017-05-03 — https://data.ipu.org/parliament/GB/GB-LC01/election/GB-LC01-E20170608/
- United Kingdom, dissolved or suspended, claimed 2019-11-06 — https://data.ipu.org/parliament/GB/GB-LC01/election/GB-LC01-E20191212/
- United Kingdom, dissolved or suspended, claimed 2024-05-30 — https://data.ipu.org/parliament/GB/GB-LC01/election/GB-LC01-E20240704/
- Vietnam, dissolved or suspended, claimed 2016-07-19 — https://data.ipu.org/parliament/VN/VN-LC01/election/VN-LC01-E20160522/

**no date in the to-check list: 23** (other 13, appointed seats 6, partial renewal 2, dissolved or suspended 1, quota or seat law 1)
- Afghanistan, dissolved or suspended, claimed NOT FOUND — https://data.ipu.org/parliament/AF/AF-LC01/election/AF-LC01-E20181020/
- Argentina, other, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2011_05.htm
- Austria, other, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2017_08.htm
- Belgium, other, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2029_07.htm
- Bulgaria, other, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2045_05.htm
- Bulgaria, other, claimed NOT FOUND — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20241027/
- Bulgaria, other, claimed NOT FOUND — https://data.ipu.org/parliament/BG/BG-LC01/election/BG-LC01-E20241027/
- Denmark, other, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2087_07.htm
- Ecuador, partial renewal, claimed NOT FOUND — https://data.ipu.org/parliament/EC/EC-LC01/election/EC-LC01-E20230820/
- Nepal, appointed seats, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2386_13.htm
- Nepal, appointed seats, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2386_08.htm
- New Zealand, other, claimed NOT FOUND — https://data.ipu.org/parliament/NZ/NZ-LC01/election/NZ-LC01-E20231014/
- Peru, other, claimed NOT FOUND — https://data.ipu.org/parliament/PE/PE-LC01/election/PE-LC01-E20160410/
- Portugal, other, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2257_09.htm
- Serbia, other, claimed NOT FOUND — https://data.ipu.org/parliament/RS/RS-LC01/election/RS-LC01-E20220403/
- Switzerland, other, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2305_07.htm
- Tanzania, partial renewal, claimed NOT FOUND — https://data.ipu.org/parliament/TZ/TZ-LC01/election/TZ-LC01-E20201028/
- Tanzania, appointed seats, claimed NOT FOUND — https://data.ipu.org/parliament/TZ/TZ-LC01/election/TZ-LC01-E20251029/
- Tanzania, appointed seats, claimed NOT FOUND — https://data.ipu.org/parliament/TZ/TZ-LC01/election/TZ-LC01-E20201028/
- Uganda, appointed seats, claimed NOT FOUND — https://data.ipu.org/parliament/UG/UG-LC01/election/UG-LC01-E20210114/
- Uganda, appointed seats, claimed NOT FOUND — https://data.ipu.org/election-summary/HTML/2329_11.htm
- United Arab Emirates, quota or seat law, claimed NOT FOUND — https://data.ipu.org/parliament/AE/AE-LC01/election/AE-LC01-E20191005/
- Vietnam, other, claimed NOT FOUND — https://data.ipu.org/parliament/VN/VN-LC01/election/VN-LC01-E20160522/

**date differs (page shows another date that year): 14** (quota or seat law 3, dissolved or suspended 3, newly formed 3, partial renewal 2, appointed seats 2, other 1)
- Argentina, quota or seat law, claimed 2017-11-22; page shows 2017-12-06 — https://data.ipu.org/parliament/AR/AR-LC01/
- Argentina, quota or seat law, claimed 2017-12-14; page shows 2017-12-06 — https://data.ipu.org/parliament/AR/AR-LC01/
- Argentina, quota or seat law, claimed 2017-12-15; page shows 2017-12-06 — https://data.ipu.org/parliament/AR/AR-LC01/
- Canada, dissolved or suspended, claimed 2005-11-29; page shows 2005-11-28 — https://data.ipu.org/election-summary/HTML/2055_06.htm
- Ecuador, dissolved or suspended, claimed 2007-11-29; page shows 2007-01-15; 2007-09-30 — https://data.ipu.org/election-summary/HTML/2095_09.htm
- Ecuador, newly formed, claimed 2007-11-29; page shows 2007-01-15; 2007-09-30 — https://data.ipu.org/election-summary/HTML/2095_09.htm
- Ecuador, newly formed, claimed 2008-10-25; page shows 2008-10-29 — https://data.ipu.org/election-summary/HTML/2095_08.htm
- Germany, other, claimed 2005-11-16; page shows 2005-07-21; 2005-09-01; 2005-09-18; 2005-10-18; 2005-11-09 — https://data.ipu.org/election-summary/HTML/2121_05.htm
- Portugal, partial renewal, claimed 2022-03-12 to 2022-03-13; page shows 2022-01-30; 2022-02-11; 2022-02-15; 2022-02-25; 2022-03-28; 2022-03-29 — https://data.ipu.org/parliament/PT/PT-LC01/election/PT-LC01-E20220130/
- Uganda, newly formed, claimed 1996-07-07; page shows 1996-06-27 — https://data.ipu.org/election-summary/HTML/2329_96.htm
- Uganda, partial renewal, claimed 2001-06-22; page shows 2001-06-01; 2001-06-26; 2001-07-03; 2001-07-04 — https://data.ipu.org/election-summary/HTML/2329_01.htm
- United Arab Emirates, dissolved or suspended, claimed 2011-02-08; page shows 2011-09-01; 2011-09-24; 2011-10-06; 2011-11-16 — https://data.ipu.org/election-summary/HTML/2333_11.htm
- United Arab Emirates, appointed seats, claimed 2011-11-15; page shows 2011-09-01; 2011-09-24; 2011-10-06; 2011-11-16 — https://data.ipu.org/election-summary/HTML/2333_11.htm
- United Arab Emirates, appointed seats, claimed 2019-11-11; page shows 2019-10-05; 2019-10-23; 2019-11-12; 2019-11-14 — https://data.ipu.org/parliament/AE/AE-LC01/election/AE-LC01-E20191005/

**date not found on the page: 3** (quota or seat law 2, dissolved or suspended 1)
- Ecuador, dissolved or suspended, claimed 2008-10-20 — https://data.ipu.org/election-summary/HTML/2095_09.htm
- Portugal, quota or seat law, claimed 2006-08-21 — https://files.dre.pt/1s/2019/03/06300/0176701769.pdf
- Spain, quota or seat law, claimed 2007-03-22 — https://www.boe.es/buscar/act.php?id=BOE-A-2024-15936

**page did not open (URLError: <urlopen error timed out>): 2** (general election 2)
- Afghanistan, general election, claimed 2005-09-18 — https://archive.ipu.org/parline-e/reports/arc/2381_05.htm
- Afghanistan, general election, claimed 2010-09-18 — https://archive.ipu.org/parline-e/reports/arc/2381_10.htm

**date shown, but on Wikipedia (not a primary source): 2** (general election 1, partial renewal 1)
- Afghanistan, general election, claimed 2018-10-20 to 2018-10-27 — https://en.wikipedia.org/wiki/2018_Afghan_parliamentary_election
- Argentina, partial renewal, claimed 2003-04-27 to 2003-11-23 — https://es.wikipedia.org/wiki/Elecciones_legislativas_de_Argentina_de_2003

**date partly found (one end of the claimed range): 1** (general election 1)
- Germany, general election, claimed 2005-09-18 to 2005-10-02; page shows 2005-07-21; 2005-09-01; 2005-09-18; 2005-10-18; 2005-11-09 — https://data.ipu.org/election-summary/HTML/2121_05.htm

### Checks (`python3 tests/rtt104/check_v3_changes.py`)
- Values equal the WDI figures (`series.csv`): 2,420/2,420 PASS.
- Every "election" or "other" row has a URL our runner fetched and an excerpt from that fetch showing its date: 180/180 PASS.
- V2 film config, film workflow and music file byte-identical to c379631: PASS.
- RTT-104 data tests: 23/23 PASS.

### Questions for Luke (IQ-24c)
1. **Go on to Part 2, the design round (top-20 board, tags, scale, pace)?** *Recommendation: yes.* Under rule (a), 46 of 51 big changes (90%) have a checked election behind them, and the busiest year has 5 tags. *Default if no answer: no design work starts.*
2. **Which tag rule, (a) 5 points or more, or (b) 5 points or more or 3+ places?** *Recommendation: (a).* It gives 90% explained against 55%, at most 5 tags a year against 8, and fewer bare "unexplained" moves. *Default: (a), the working default (DEC-668).*
3. *(Proposal, DEC-671.)* **Should a November or December election count towards the following year's change?** That is what WDI's figures suggest. It would give those 3 rule-(a) changes a cause, but it would also move others that are matched now (for example Nicaragua's November 2011 election). The net effect has not been worked out. *Recommendation: decide in Part 2, with each case shown. Default: keep the calendar-year rule and flag those cases.*
