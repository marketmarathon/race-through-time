# Metric contract — RTT-001 Browser Wars · v1.0 (data build IQ-12) · 3 Oct 2026

Written before the data build (DEC-036). Owner decisions: DEC-144 (RTT-001 is next, the full browser wars, early years as estimates), DEC-152 to DEC-154 (Luke, 3 Oct 2026: one source per period, straight lines across the hand-overs, all devices). Claude's working choices: DEC-155 to DEC-159 (not yet confirmed by Luke; each is a question in `reports/RTT-001_data_report.md`).

**Public claim:** the share of web browsing by browser, worldwide, all devices, month by month from January 1994 to September 2026. Before January 2009 there is no single consistent measurement, so each period uses the best available historical source, and **everything before January 2009 is shown in the estimated look with the source named on screen** (DEC-153).
**Unit:** percentage share (0–100) of what the period's source counts (table below). Shown with one decimal place in the player unless Luke decides otherwise.
**Rank:** descending share at each month end. Ties (equal to the source's precision) keep the order of the previous month; if new, alphabetical.
**Timeline:** one value per browser per month end, 31 Jan 1994 to 30 Sep 2026 (393 month ends). A browser has no value outside its own source points (rule 4).

## Eras: one source per period (DEC-152)

| Era | Months | Source (on-screen source line) | What it counts | Geography | Dating of points |
|---|---|---|---|---|---|
| 1 | Jan 1994 – Nov 1994 | GVU WWW User Surveys, Georgia Tech (1st survey Jan 1994; 2nd survey 10 Oct – 16 Nov 1994) | **Survey respondents' primary browser** (self-selected web users answering an online questionnaire; mostly North American) | International sample | A survey period is dated at its last day (1st survey: 31 Jan 1994, month only; 2nd: 16 Nov 1994) |
| 2 | Apr 1996 – Dec 2000 | University of Illinois EWS web server, monthly reports | **Hosts at one university web server**: each host counted once per month, for the browser it used most recently | Visitors to one server (engineering student pages), many countries | Month end of the report month |
| 3 | 2001 – Apr 2007 | WebSideStory StatMarket (2001–2002), then OneStat.com (2002–2007) | **Visitors to sites using the tracker** (StatMarket: unique daily visitors on a given day; OneStat: visitors over a recent window, as each release states) | Worldwide, as stated by the tracker | A one-day snapshot at its day; a stated month at the month end; otherwise as recorded per observation |
| 4 | May 2007 – Dec 2008 | W3Counter | **Page views** on sites using W3Counter, as its monthly report states | Worldwide | Month end of the report month |
| 5 | Jan 2009 – Sep 2026 | StatCounter Global Stats, worldwide, all platforms (desktop + mobile + tablet + console) | **Page views** on sites using StatCounter | Worldwide | Month end |

The gaps between a source's last point and the next source's first point (for example 16 Nov 1994 to 30 Apr 1996) are **hand-over stretches**: straight lines, never a source of their own (DEC-153, DEC-156).

**These measures are not the same thing.** A survey answer, a university server's hosts, tracked-site visitors and page views can give very different numbers for the same month. The video shows them as one race only because Luke chose that (DEC-152, DEC-153), with the estimated look and the source named on screen for every month before January 2009. Cross-check sources are listed in the report, never on screen (DEC-156).

## Browser families (DEC-155, Claude working choice)
- **Mosaic** = every Mosaic variant the source reports (GVU's xmosaic + winmosaic + macmosaic; EWS "Mosaic", which until May 1996 also includes Microsoft's browser, then "Mosaic (other than MS)"). Following the source, recorded per observation.
- **Netscape** = Navigator, Communicator and Netscape 6–9.
- **Internet Explorer** = all IE versions (EWS "Microsoft"; StatCounter "IE"). **Edge** is separate from Internet Explorer; StatCounter's "Edge" and "Edge Legacy" are added together as one Edge bar (arithmetic). StatCounter's "IEMobile" stays a separate bar.
- **Firefox** is separate from the Mozilla Suite / SeaMonkey ("Mozilla").
- Android's stock browser, UC Browser, Samsung Internet, Opera and the rest **as StatCounter reports them**.
- **Arithmetic allowed:** adding the version buckets or platform labels of ONE browser inside ONE source at ONE date (recorded per observation as arithmetic, with the parts). **Never** adding different browsers, or figures from different sources.
- **"Other" / "unknown" is never a bar** (DEC-159).

## Method (deterministic: `scripts/build_rtt001_dataset.py`)
1. **Points.** The used observations in `data/rtt-001/observations.csv` (each VERIFIED at its source, with URL and a short quote or table cell) and every row of the StatCounter export are the points. Only VERIFIED figures are used; UNVERIFIED and NOT FOUND are listed, never used.
2. **One source per date.** Every point date belongs to exactly one era and one source. Cross-check sources are recorded with `used = no`.
3. **Hand-over rule (DEC-156).** Each era uses only its own source's dated points. The straight line runs from the last point of the outgoing source to the first point of the incoming one. The exact points are listed in the seam table of the report.
4. **Month-end values (DEC-153, DEC-157, DEC-158).** At a month end that is a point date: the point's value (`observed`, or `arithmetic` if the point is a sum of labels). Between two consecutive point dates at which the browser has a value: a straight line by calendar days (`interpolated`). **If the browser is not reported at a point date, it has no value in the stretches on either side of that date** (NOT FOUND; no bar). No value before a browser's first point or after its last. Nothing is held flat, nothing is carried across from another source, nothing is averaged.
5. **Values as published.** Percentages are read as text and converted exactly (decimal comma → point, ".8" → 0.8). A malformed published value (for example OneStat's "60.2.6") is NOT FOUND and never repaired. Interpolated values are rounded to two decimals (half up); observed values keep the source's own precision.
6. **StatCounter** values in `series.csv` equal the raw export cell exactly (checked).
7. **No forecasts, no intentions.** GVU's 1996–98 "browser expected to use in 12 months" figures are excluded.

## Provenance (per series point)
| Provenance | Meaning |
|---|---|
| observed | the month end is the date of a published figure for this browser |
| arithmetic | the month end is the date of a sum of one browser's own labels in one source (parts recorded) |
| interpolated | straight line between two points of this browser (within an era, or across a hand-over) |

Each point also records the two points it rests on (`left_point`, `right_point`), its era and source, and whether it lies on a hand-over stretch.

## Display attributes (DEC-036; built in a later player session only — DEC-069)

| Attribute | Source | File / column |
|---|---|---|
| Browser name (bar label) | maker's English name | `browsers.csv` `display_name` |
| Maker | maker | `browsers.csv` `maker` |
| Colour key (one per browser; the colours themselves are chosen in the player session) | — | `browsers.csv` `colour_key` (**empty for now**) |
| Logo reference | private media, never committed (DEC-006, DEC-060) | `browsers.csv` `logo_ref` (**empty for now**) |
| Value at each month end | method above | `series.csv` `share` |
| Estimated flag (estimated look) | every month end before 2009-01 (DEC-153) | `series.csv` `estimated` (yes/no) |
| Era and source label for the on-screen source line | era table above | `series.csv` `era`, `source_id`, `source_line` |
| Per-point provenance and the points it rests on | method above | `series.csv` `provenance`, `left_point`, `right_point`, `handover` |
| Leader at each month end, changes of first place | rank rule above | computed in the report (`reports/RTT-001_data_report.md`) |

## Claims this data cannot support
"Most people used X" before 2009 (the early sources are a survey sample, one university server and tracked sites, not the population); the exact month Netscape overtook Mosaic (it falls between November 1994 and April 1996, a stretch with no figure); exact pre-2009 positions (estimates); anything about 1993 (no usable figure); device splits (one all-devices race, DEC-154).
