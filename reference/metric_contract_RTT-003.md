# Metric contract — RTT-003 Best-Selling Consoles 1985–2026 · v1.0 (data build IQ-09) · 1 Oct 2026

Written before the data build (DEC-036). Owner decisions: DEC-081 to DEC-085 (Luke, 30 Sep 2026). Claude's working choices: DEC-086 to DEC-090 (questions for Luke, listed in `reports/RTT-003_data_report.md`).

**Public claim:** the best-selling video game consoles of all time, race from 31 March 1985 to 30 June 2026, measured in **units shipped** (manufacturers' sell-in to retailers and distributors). The title must say "units shipped" (DEC-081).
**Unit:** consoles (hardware units), cumulative since launch, worldwide. Shown in millions.
**Rank:** descending cumulative units at each quarter end. Ties (equal values to the unit) rank the console that reached the value first higher; if both reached it on the same date, the earlier launch ranks higher.
**Timeline:** one value per console per calendar quarter end, 31 Mar 1985 to 30 Jun 2026 (166 quarter ends). Nothing before launch.

## Universe (DEC-083)
- Dedicated home, handheld and hybrid video game consoles with roughly **8 million or more lifetime units**, on the evidence found.
- **Manufacturer's own model grouping.** One row per family as the manufacturer reports it: Game Boy includes Game Boy Pocket, Light and Color; Nintendo DS includes DS Lite, DSi and DSi XL; Nintendo 3DS includes 3DS XL, 2DS and the New models; Nintendo Switch includes Switch Lite and the OLED Model; Nintendo Switch 2 is separate; PlayStation includes PS one; PSP includes PSP go and E-1000; Xbox Series X and Series S are one family; Xbox One includes One S and One X; Famicom and NES are one; Super Famicom and SNES are one; Sega Mark III and Master System are one; Mega Drive and Genesis are one.
- **Excluded:** Game & Watch; VTech V.Smile and V.Motion; add-ons (Famicom Disk System, Mega-CD/Sega CD, 32X, Nintendo 64DD, PC Engine CD-ROM²); mini and classic re-releases (NES/SNES Classic Edition, Mega Drive Mini, PlayStation Classic and similar); PCs, home computers and PC handhelds (e.g. Steam Deck).
- Consoles below the threshold or with no figure reaching it are listed in `data/rtt-003/consoles.csv` with `in_scope = no` and the reason, so the check "all excluded consoles absent from the series" can run.

## Metric and basis
- **Preferred basis:** units shipped / sold in, worldwide, as the manufacturer reports it.
- Nintendo: "consolidated hardware sales units" (shipments), fiscal years ending 31 March, rounded by Nintendo to 10,000 units.
- Sony: older figures are "cumulative production shipments" (Sony Computer Entertainment, to 2007); current figures are "sell-in". **A change of basis is never shown as a fall in sales:** when a later figure on a new basis is lower than an earlier figure on the old basis, the bar holds the higher value and the later figure is recorded as consistent ("more than X") or as a disagreement.
- Microsoft: units shipped (fiscal years ending 30 June) until it stopped publishing console units; afterwards **analyst estimates** (DEC-084), which may be sell-through or installed base; their basis is recorded per point and the bars carry the analyst-estimate label.
- Sega and Atari: manufacturer statements as worded ("sold", "shipped"); basis recorded as stated.
- **Forecasts are never used as figures.** A forecast is any figure made before the date it refers to.

## Evidence grades (per observation)
| Grade | Meaning |
|---|---|
| A | Manufacturer, worldwide figure (including arithmetic on manufacturer worldwide figures, e.g. a lifetime total minus later fiscal years) |
| B | Manufacturer regional figure, or the sum of same-date regional figures from the manufacturer; also a manufacturer figure whose geography is not stated |
| C | Press or trade magazine quoting the company (including sums of same-date regional figures printed by the magazine) |
| D | Analyst or other estimate (including case-study tables and unattributed press figures) |

## Method (deterministic: `scripts/build_rtt003_dataset.py`)
1. **Anchors.** For each console, the dated observations marked `used = yes` in `data/rtt-003/observations.csv` are its anchors. Each console also gets a zero anchor on its launch date (first market).
2. **One figure per date.** Where two sources disagree for the same date, the higher grade is used and the other is recorded (`used = no`, reason "disagreement") and listed for Luke. Never averaged.
3. **Quarter-end values.** At a quarter end that is an anchor date, the anchor value. Between anchors: straight line by calendar days between the neighbouring anchors (launch = 0). After the last anchor: **held** flat at the last anchor value. Before launch: no row.
4. **Nintendo March year ends** (`source/nintendo_fy_hardware.csv`, transcribed from Nintendo's "Consolidated Sales Transition by Region", as of 31 Mar 2026): the total at 31 March of year Y = Nintendo's life-to-date total minus the sum of all later fiscal-year figures. Nintendo prints amounts under 10,000 units as markers (+0.1 / −0.1 in the 10,000-unit column); these count as zero, and each fiscal-year figure is rounded to 10,000 units, so a rebuilt total can be off by up to 5,000 units per later fiscal year. These rebuilt totals are compared with the independent older figures (Nintendo Online Magazine Game Boy series, Famitsu 1993–1997 tables, Nintendo's 1996 and 1997 company reports).
5. **Sony PS4 and PS5** quarter ends are the running sums of Sony's quarterly sell-in table (0.1 million precision), checked against Sony's headlines ("more than 117 million", "more than 95 million").
6. **Lower bounds.** A figure worded "more than", "over" or "at least", or a sum that leaves out known regions, carries the lower-bound flag; the bar label shows "+" at that anchor and while held at it.
7. **Missing = NOT FOUND,** never zero and never invented. A lifetime figure with no date is recorded but not placed on the timeline.

## Provenance (per series point)
| Provenance | Meaning |
|---|---|
| official | the quarter end is the date of a grade A or B anchor |
| arithmetic | the value is computed from grade A or B figures (Nintendo March rebuild, Sony quarterly sums, a manufacturer's regional sum) at that quarter end |
| estimate | the quarter end is the date of a grade C or D anchor |
| interpolated | straight line between two anchors |
| held | after the console's last anchor, held flat |

Each point also records the anchors it rests on (`left_anchor`, `right_anchor`) and the lowest grade among them (`grade`).

## Display attributes (DEC-036; design approved in principle by DEC-085, built in a later player session only — DEC-069)
Every attribute the later player needs, and where it lives:

| Attribute | Source | File / column |
|---|---|---|
| Console name (bar label) | manufacturer's English name | `consoles.csv` `display_name` |
| Other names (regional names, family members) | manufacturer pages | `consoles.csv` `other_names`, `models_included` |
| Maker | manufacturer | `consoles.csv` `maker` |
| Maker colour key (one colour per maker; the colours themselves are chosen in the player session) | — | `consoles.csv` `maker_key` (atari, nintendo, sega, sony, microsoft) |
| Maker logo in a key | private media, never committed (DEC-006, DEC-060) | `consoles.csv` `maker_key` joins to a private asset later |
| Type (home / handheld / hybrid) | manufacturer | `consoles.csv` `type` |
| Launch date (first market) and region | manufacturer where reachable | `consoles.csv` `launch_date`, `launch_region`, `launch_source` |
| Fade date (retired consoles fade) and its basis | DEC-086 rule | `consoles.csv` `fade_date`, `fade_basis` |
| Value at each quarter end | method above | `series.csv` `units` |
| Lower-bound "+" flag | method step 6 | `series.csv` `plus_flag` |
| Per-point provenance and anchors | method above | `series.csv` `provenance`, `left_anchor`, `right_anchor` |
| Grade | lowest grade the point rests on | `series.csv` `grade` |
| Estimated look (DEC-082: 1985–1993 bridged stretches; DEC-084: analyst estimates) | DEC-090 rule | `series.csv` `display_style` (official / estimated / analyst_estimate) |
| Console picture | private media, chosen later | `consoles.csv` `picture_ref` (**empty for now**) |
| "Best-selling console ever" crown | first place at each quarter end | `crown.csv` |
| Company scoreboard (pilot test) | sum of a maker's consoles at each quarter end | computed by the player from `series.csv` + `maker_key`; per-maker totals in `series_by_maker.csv` |
| Rare callouts at big moments | crown changes and top-ten overtakes | `crown.csv`, `overtakes.csv` (each with the grade and display style it rests on) |

## Claims this data cannot support
"Most popular console" (units shipped is not players or play time), sell-through or installed base claims, revenue, anything about the PS Vita (Sony never disclosed its sales), exact Xbox One or Xbox Series X|S sales (analyst estimates only), exact 1985–1993 positions (bridged estimates).
