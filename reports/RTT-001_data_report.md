# RTT-001 Browser Wars — data report for Luke

Build `rtt001-build/1.0` (`scripts/build_rtt001_dataset.py`). Contract: `reference/metric_contract_RTT-001.md`. Data: `data/rtt-001/`.

## Summary for Luke

**What the race shows (January 1994 – September 2026, all devices).** Four leaders:

1. **Mosaic** leads from the start: 97.22% of GVU's January 1994 survey respondents named it as their main browser, and still 68% (all Mosaic versions together) in the October–November 1994 survey.
2. **Netscape** takes over somewhere between November 1994 and April 1996. There is **no figure in that gap**, so the month the straight line crosses (June 1995 in the data) is only where two lines meet and must not be shown as a date. By April 1996 Netscape has 83.3% of the hosts visiting the Illinois EWS server.
3. **Internet Explorer** first leads in **October 1998**, an observed month (EWS: Microsoft 49.1%, Netscape 48.3%). It peaks at about 96% in August 2002 (StatMarket 95.97% on 26 August 2002).
4. **Chrome** first leads in **May 2012**, also observed (StatCounter all platforms: Chrome 29.15%, IE 28.87%), and has led every month since. In September 2026 the board is Chrome 66.45%, Safari 18.2%, Edge 6.03%, Firefox 2.79%, Samsung Internet 2.31% and Opera 1.77%.

**How sure we are, part by part.**
- **2009 – 2026 (StatCounter): solid.** Every monthly value is the StatCounter export cell, checked by script. These are page views on StatCounter's member sites, not people.
- **1996 – 2000 (Illinois EWS): verified, but narrow.** Every month April 1996 – December 2000 was checked at its archived page. It is one university server's visiting hosts, not the whole web, which is why it is shown as an estimate.
- **2001 – April 2007 (StatMarket, then OneStat): verified snapshots.** 9 StatMarket and 64 OneStat figures, each read in the archived release, joined by straight lines.
- **May 2007 – December 2008 (W3Counter): verified monthly.**
- **1994 (GVU surveys): verified, weakest.** A self-selected online survey of early web users, mostly in North America.
- **The joins between sources are where the race is least reliable.** The sources measure different things, so the lines across the hand-overs show large moves that are really changes of measure: IE goes from 75.4% (EWS, December 2000) to 87.71% (StatMarket, February 2001), and from 85.81% (OneStat, January 2007) to 67.1% (W3Counter, May 2007). In June 2007 the two trackers were 19 points apart for the same browser (OneStat 85.81%, W3Counter 66.9%). This follows your decisions (DEC-152, DEC-153), but it is the main thing a sharp viewer could challenge.

**What Claude verified and how.** StatCounter and GVU were fetched by a GitHub runner, because this container's network blocks every source site. Eight EWS months came from the runner too. The web archive then blocked the runner with "too many requests", so Claude in Cowork checked the remaining 480 pre-2009 figures in your Chrome on 3 Oct 2026.
- Cowork's browser tool could not return page SHA-256 hashes, so those rows record the exact archive capture URL instead (`observations.csv` `url`; `page_sha256` empty).
- Rows checked by the runner do carry page hashes.
- The 384 cross-check figures (W3Schools, XiTi, Net Applications, TheCounter) remain UNVERIFIED. They are never on screen and only appear in the seam table.

## Checks

| Check | Result |
|---|---|
| values_within_0_100 | PASS |
| source_date_totals_at_most_100 | PASS |
| every_point_has_provenance | PASS |
| one_source_per_date | PASS |
| eras_do_not_overlap | PASS |
| statcounter_equals_raw_csv | PASS |
| no_unverified_or_not_found_used | PASS |
| nothing_before_first_or_after_last_source_date | PASS |
| month_grid_complete | PASS |
| arithmetic_rows_equal_their_parts | PASS |
| other_is_never_a_bar | PASS |

## Changes of first place

| Month | New leader | Share | Previous leader (share that month) | How the month's value is made | Source line |
|---|---|---|---|---|---|
| 1994-01 | Mosaic | 97.22% | — | observed | GVU WWW User Surveys (Georgia Tech) |
| 1995-06 | Netscape | 45.79% | Mosaic (44.55) | interpolated, on a hand-over stretch (no figure: the date is set only by the straight line) | Estimate between GVU survey (Nov 1994) and Illinois EWS server (Apr 1996) |
| 1998-10 | Internet Explorer | 49.1% | Netscape (48.3) | observed | University of Illinois EWS web server |
| 2012-05 | Chrome | 29.15% | Internet Explorer (28.87) | observed | StatCounter Global Stats |

## Top-ten boards

### January 1994

Source line: GVU WWW User Surveys (Georgia Tech) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Mosaic | 97.22% | observed |
| 2 | Lynx | 1.95% | observed |
| 3 | Samba | 0.30% | observed |
| 4 | Cello | 0.08% | observed |

### November 1994

Source line: Estimate between GVU survey (Nov 1994) and Illinois EWS server (Apr 1996) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Mosaic | 66.55% | interpolated |
| 2 | Netscape | 19.72% | interpolated |
| 3 | Lynx | 1.97% | interpolated |

### April 1996

Source line: University of Illinois EWS web server · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Netscape | 83.3% | observed |
| 2 | Mosaic | 12.9% | observed |
| 3 | Lynx | 0.8% | observed |

### October 1998

Source line: University of Illinois EWS web server · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 49.1% | observed |
| 2 | Netscape | 48.3% | observed |

### January 2001

Source line: Estimate between Illinois EWS server (Dec 2000) and StatMarket (Feb 2001) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 82.74% | interpolated |
| 2 | Netscape | 15.88% | interpolated |

### January 2004

Source line: OneStat.com · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 92.88% | interpolated |
| 2 | Netscape | 2.05% | interpolated |
| 3 | Mozilla Suite | 1.83% | interpolated |
| 4 | Safari | 0.50% | interpolated |

### January 2007

Source line: OneStat.com · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 85.81% | observed |
| 2 | Firefox | 11.69% | observed |
| 3 | Safari | 1.64% | observed |
| 4 | Opera | 0.58% | observed |
| 5 | Netscape | 0.13% | observed |

### December 2008

Source line: W3Counter · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 58.6% | observed |
| 2 | Firefox | 31.1% | observed |
| 3 | Safari | 2.9% | observed |
| 4 | Opera | 2.0% | observed |
| 5 | Mozilla Suite | 1.1% | observed |

### January 2009

Source line: StatCounter Global Stats

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 64.97% | observed |
| 2 | Firefox | 26.85% | observed |
| 3 | Opera | 3.07% | observed |
| 4 | Safari | 2.79% | observed |
| 5 | Chrome | 1.37% | observed |
| 6 | AOL | 0.27% | observed |
| 7 | Mozilla Suite | 0.15% | observed |
| 8 | Nokia | 0.12% | observed |
| 9 | Sony PS3 | 0.08% | observed |
| 10 | SeaMonkey | 0.04% | observed |

### May 2012

Source line: StatCounter Global Stats

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Chrome | 29.15% | observed |
| 2 | Internet Explorer | 28.87% | observed |
| 3 | Firefox | 22.98% | observed |
| 4 | Safari | 8.68% | observed |
| 5 | Opera | 3.81% | observed |
| 6 | Android Browser | 2.41% | observed |
| 7 | Nokia | 1.17% | observed |
| 8 | UC Browser | 0.86% | observed |
| 9 | BlackBerry | 0.57% | observed |
| 10 | NetFront | 0.4% | observed |

### January 2016

Source line: StatCounter Global Stats

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Chrome | 47.79% | observed |
| 2 | Safari | 12.9% | observed |
| 3 | Firefox | 8.97% | observed |
| 4 | Internet Explorer | 8.94% | observed |
| 5 | UC Browser | 7.31% | observed |
| 6 | Opera | 5.45% | observed |
| 7 | Android Browser | 4.83% | observed |
| 8 | Microsoft Edge | 1.05% | arithmetic |
| 9 | IE Mobile | 0.74% | observed |
| 10 | Yandex Browser | 0.32% | observed |

### January 2020

Source line: StatCounter Global Stats

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Chrome | 64.1% | observed |
| 2 | Safari | 17.21% | observed |
| 3 | Firefox | 4.7% | observed |
| 4 | Samsung Internet | 3.33% | observed |
| 5 | UC Browser | 2.61% | observed |
| 6 | Opera | 2.26% | observed |
| 7 | Microsoft Edge | 2.18% | arithmetic |
| 8 | Internet Explorer | 1.68% | observed |
| 9 | Android Browser | 0.54% | observed |
| 10 | Yandex Browser | 0.27% | observed |

### September 2026

Source line: StatCounter Global Stats

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Chrome | 66.45% | observed |
| 2 | Safari | 18.2% | observed |
| 3 | Microsoft Edge | 6.03% | arithmetic |
| 4 | Firefox | 2.79% | observed |
| 5 | Samsung Internet | 2.31% | observed |
| 6 | Opera | 1.77% | observed |
| 7 | UC Browser | 0.47% | observed |
| 8 | Brave | 0.45% | observed |
| 9 | Yandex Browser | 0.34% | observed |
| 10 | Android Browser | 0.24% | observed |

## Seam table (hand-overs between sources)

Each hand-over joins the outgoing source's last figure to the incoming source's first figure with a straight line (DEC-153, DEC-156). Cross-check figures are never on screen; they show how far apart the measures are.

### GVU WWW User Surveys (Georgia Tech) → University of Illinois EWS web server

Outgoing last point 1994-11-16; incoming first point 1996-04-30; 531 days of straight line.

| Browser | Outgoing value | Incoming value |
|---|---|---|
| Lynx | 2% | 0.8% |
| MacWeb | 3% | not reported |
| Mosaic | 68% | 12.9% |
| Netscape | 18% | 83.3% |

### University of Illinois EWS web server → WebSideStory StatMarket

Outgoing last point 2000-12-31; incoming first point 2001-02-21; 52 days of straight line.

| Browser | Outgoing value | Incoming value |
|---|---|---|
| Internet Explorer | 75.4% | 87.71% |
| Netscape | 21.6% | 12.01% |

Cross-checks within 45 days of either hand-over date, non-zero values (never on screen; all are in `observations.csv`):

| Source | Date | Browser (as published) | Value | Verified |
|---|---|---|---|---|
| THECOUNTER | 2000-11-30 | MSIE 4.x | 14 | UNVERIFIED |
| THECOUNTER | 2000-11-30 | MSIE 5.x | 68 | UNVERIFIED |
| THECOUNTER | 2000-11-30 | Netscape 4.x | 12 | UNVERIFIED |
| THECOUNTER | 2000-11-30 | Netscape comp. | 1 | UNVERIFIED |
| THECOUNTER | 2000-11-30 | Unknow | 1 | UNVERIFIED |
| THECOUNTER | 2001-01-31 | MSIE 4.x | 12 | UNVERIFIED |
| THECOUNTER | 2001-01-31 | MSIE 5.x | 72 | UNVERIFIED |
| THECOUNTER | 2001-01-31 | Netscape 4.x | 10 | UNVERIFIED |
| THECOUNTER | 2001-01-31 | Netscape comp. | 1 | UNVERIFIED |
| THECOUNTER | 2001-01-31 | Unknow | 1 | UNVERIFIED |
| THECOUNTER | 2001-02-28 | MSIE 4.x | 11 | UNVERIFIED |
| THECOUNTER | 2001-02-28 | MSIE 5.x | 75 | UNVERIFIED |
| THECOUNTER | 2001-02-28 | Netscape 4.x | 9 | UNVERIFIED |
| THECOUNTER | 2001-02-28 | Netscape comp. | 1 | UNVERIFIED |

### WebSideStory StatMarket → OneStat.com

Outgoing last point 2002-08-26; incoming first point 2002-09-30; 35 days of straight line.

| Browser | Outgoing value | Incoming value |
|---|---|---|
| Internet Explorer | 95.97% | 94.9% |
| Mozilla Suite | not reported | 0.9% |
| Netscape | 3.39% | 3.0% |

Cross-checks within 45 days of either hand-over date, non-zero values (never on screen; all are in `observations.csv`):

| Source | Date | Browser (as published) | Value | Verified |
|---|---|---|---|---|
| THECOUNTER | 2002-07-31 | MSIE 4.x | 2 | UNVERIFIED |
| THECOUNTER | 2002-07-31 | MSIE 5.x | 50 | UNVERIFIED |
| THECOUNTER | 2002-07-31 | MSIE 6.x | 39 | UNVERIFIED |
| THECOUNTER | 2002-07-31 | Netscape 4.x | 3 | UNVERIFIED |
| THECOUNTER | 2002-07-31 | Netscape comp. | 1 | UNVERIFIED |
| THECOUNTER | 2002-08-31 | MSIE 4.x | 2 | UNVERIFIED |
| THECOUNTER | 2002-08-31 | MSIE 5.x | 49 | UNVERIFIED |
| THECOUNTER | 2002-08-31 | MSIE 6.x | 41 | UNVERIFIED |
| THECOUNTER | 2002-08-31 | Netscape 4.x | 2 | UNVERIFIED |
| THECOUNTER | 2002-08-31 | Netscape comp. | 1 | UNVERIFIED |
| THECOUNTER | 2002-09-30 | MSIE 4.x | 2 | UNVERIFIED |
| THECOUNTER | 2002-09-30 | MSIE 5.x | 47 | UNVERIFIED |
| THECOUNTER | 2002-09-30 | MSIE 6.x | 43 | UNVERIFIED |
| THECOUNTER | 2002-09-30 | Netscape 4.x | 2 | UNVERIFIED |
| THECOUNTER | 2002-09-30 | Netscape comp. | 1 | UNVERIFIED |
| THECOUNTER | 2002-10-31 | MSIE 4.x | 2 | UNVERIFIED |
| THECOUNTER | 2002-10-31 | MSIE 5.x | 46 | UNVERIFIED |
| THECOUNTER | 2002-10-31 | MSIE 6.x | 45 | UNVERIFIED |
| THECOUNTER | 2002-10-31 | Netscape 4.x | 2 | UNVERIFIED |
| THECOUNTER | 2002-10-31 | Netscape 5.x | 1 | UNVERIFIED |
| THECOUNTER | 2002-10-31 | Netscape comp. | 1 | UNVERIFIED |
| W3SCHOOLS | 2002-07-31 | AOL | 3.5 | UNVERIFIED |
| W3SCHOOLS | 2002-07-31 | IE4 | 0.5 | UNVERIFIED |
| W3SCHOOLS | 2002-07-31 | IE5 | 40.1 | UNVERIFIED |
| W3SCHOOLS | 2002-07-31 | IE6 | 44.4 | UNVERIFIED |
| W3SCHOOLS | 2002-07-31 | N3 | 1.2 | UNVERIFIED |
| W3SCHOOLS | 2002-07-31 | N4 | 2.6 | UNVERIFIED |
| W3SCHOOLS | 2002-07-31 | N5 | 3.5 | UNVERIFIED |
| W3SCHOOLS | 2002-09-30 | AOL | 4.5 | UNVERIFIED |
| W3SCHOOLS | 2002-09-30 | IE5 | 34.4 | UNVERIFIED |
| W3SCHOOLS | 2002-09-30 | IE6 | 49.1 | UNVERIFIED |
| W3SCHOOLS | 2002-09-30 | N3 | 1.3 | UNVERIFIED |
| W3SCHOOLS | 2002-09-30 | N4 | 2.2 | UNVERIFIED |
| W3SCHOOLS | 2002-09-30 | N5 | 4.5 | UNVERIFIED |

### OneStat.com → W3Counter

Outgoing last point 2007-01-31; incoming first point 2007-05-31; 120 days of straight line.

| Browser | Outgoing value | Incoming value |
|---|---|---|
| AOL | not reported | 1.1% |
| Firefox | 11.69% | 24.8% |
| Internet Explorer | 85.81% | 67.1% |
| Netscape | 0.13% | not reported |
| Opera | 0.58% | 1.8% |
| Safari | 1.64% | 2.4% |

Cross-checks within 45 days of either hand-over date, non-zero values (never on screen; all are in `observations.csv`):

| Source | Date | Browser (as published) | Value | Verified |
|---|---|---|---|---|
| ONESTAT | 2007-06-30 | Apple Safari | 1.79 | yes |
| ONESTAT | 2007-06-30 | Internet Explorer | 85.81 | yes |
| ONESTAT | 2007-06-30 | Mozilla Firefox | 12.72 | yes |
| ONESTAT | 2007-06-30 | Netscape | 0.11 | yes |
| ONESTAT | 2007-06-30 | Opera | 0.61 | yes |
| ONESTAT | 2007-06-30 | Explorer | 84.66 | yes |
| ONESTAT | 2007-06-30 | Firefox | 12.72 | yes |
| ONESTAT | 2007-06-30 | Netscape | 0.11 | yes |
| ONESTAT | 2007-06-30 | Opera | 0.61 | yes |
| ONESTAT | 2007-06-30 | Safari | 1.79 | yes |
| THECOUNTER | 2007-01-31 | FireFox | 11 | UNVERIFIED |
| THECOUNTER | 2007-01-31 | MSIE 5.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-01-31 | MSIE 6.x | 63 | UNVERIFIED |
| THECOUNTER | 2007-01-31 | MSIE 7.x | 20 | UNVERIFIED |
| THECOUNTER | 2007-01-31 | Opera x.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-01-31 | Safari | 3 | UNVERIFIED |
| THECOUNTER | 2007-01-31 | Unknown | 1 | UNVERIFIED |
| THECOUNTER | 2007-02-28 | FireFox | 11 | UNVERIFIED |
| THECOUNTER | 2007-02-28 | MSIE 5.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-02-28 | MSIE 6.x | 58 | UNVERIFIED |
| THECOUNTER | 2007-02-28 | MSIE 7.x | 24 | UNVERIFIED |
| THECOUNTER | 2007-02-28 | Opera x.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-02-28 | Safari | 3 | UNVERIFIED |
| THECOUNTER | 2007-02-28 | Unknown | 1 | UNVERIFIED |
| THECOUNTER | 2007-04-30 | FireFox | 12 | UNVERIFIED |
| THECOUNTER | 2007-04-30 | MSIE 5.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-04-30 | MSIE 6.x | 56 | UNVERIFIED |
| THECOUNTER | 2007-04-30 | MSIE 7.x | 14 | UNVERIFIED |
| THECOUNTER | 2007-04-30 | Netscape comp. | 12 | UNVERIFIED |
| THECOUNTER | 2007-04-30 | Opera x.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-04-30 | Safari | 3 | UNVERIFIED |
| THECOUNTER | 2007-04-30 | Unknown | 1 | UNVERIFIED |
| THECOUNTER | 2007-05-31 | FireFox | 12 | UNVERIFIED |
| THECOUNTER | 2007-05-31 | MSIE 5.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-05-31 | MSIE 6.x | 56 | UNVERIFIED |
| THECOUNTER | 2007-05-31 | MSIE 7.x | 15 | UNVERIFIED |
| THECOUNTER | 2007-05-31 | Netscape comp. | 11 | UNVERIFIED |
| THECOUNTER | 2007-05-31 | Opera x.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-05-31 | Safari | 3 | UNVERIFIED |
| THECOUNTER | 2007-05-31 | Unknown | 1 | UNVERIFIED |
| THECOUNTER | 2007-06-30 | FireFox | 12 | UNVERIFIED |
| THECOUNTER | 2007-06-30 | MSIE 5.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-06-30 | MSIE 6.x | 54 | UNVERIFIED |
| THECOUNTER | 2007-06-30 | MSIE 7.x | 16 | UNVERIFIED |
| THECOUNTER | 2007-06-30 | Netscape comp. | 11 | UNVERIFIED |
| THECOUNTER | 2007-06-30 | Opera x.x | 1 | UNVERIFIED |
| THECOUNTER | 2007-06-30 | Safari | 3 | UNVERIFIED |
| THECOUNTER | 2007-06-30 | Unknown | 1 | UNVERIFIED |
| W3SCHOOLS | 2007-01-31 | Firefox | 31.0 | UNVERIFIED |
| W3SCHOOLS | 2007-01-31 | IE5 | 3.0 | UNVERIFIED |
| W3SCHOOLS | 2007-01-31 | IE6 | 42.3 | UNVERIFIED |
| W3SCHOOLS | 2007-01-31 | IE7 | 13.3 | UNVERIFIED |
| W3SCHOOLS | 2007-01-31 | Mozilla | 1.5 | UNVERIFIED |
| W3SCHOOLS | 2007-01-31 | Opera | 1.5 | UNVERIFIED |
| W3SCHOOLS | 2007-01-31 | Safari | 1.7 | UNVERIFIED |
| W3SCHOOLS | 2007-05-31 | Firefox | 33.7 | UNVERIFIED |
| W3SCHOOLS | 2007-05-31 | IE5 | 1.6 | UNVERIFIED |
| W3SCHOOLS | 2007-05-31 | IE6 | 38.1 | UNVERIFIED |
| W3SCHOOLS | 2007-05-31 | IE7 | 19.2 | UNVERIFIED |
| W3SCHOOLS | 2007-05-31 | Mozilla | 1.3 | UNVERIFIED |
| W3SCHOOLS | 2007-05-31 | Opera | 1.7 | UNVERIFIED |
| W3SCHOOLS | 2007-05-31 | Safari | 1.5 | UNVERIFIED |

### W3Counter → StatCounter Global Stats

Outgoing last point 2008-12-31; incoming first point 2009-01-31; 31 days of straight line.

| Browser | Outgoing value | Incoming value |
|---|---|---|
| AOL | not reported | 0.27% |
| Android Browser | not reported | 0.01% |
| BlackBerry | not reported | 0.03% |
| Chrome | not reported | 1.37% |
| Firefox | 31.1% | 26.85% |
| IE Mobile | not reported | 0.01% |
| Internet Explorer | 58.6% | 64.97% |
| Mozilla Suite | 1.1% | 0.15% |
| NetFront | not reported | 0.01% |
| Nokia | not reported | 0.12% |
| Openwave | not reported | 0.02% |
| Opera | 2.0% | 3.07% |
| Safari | 2.9% | 2.79% |
| SeaMonkey | not reported | 0.04% |
| Sony PS3 | not reported | 0.08% |
| SonyEricsson | not reported | 0.02% |

Cross-checks within 45 days of either hand-over date, non-zero values (never on screen; all are in `observations.csv`):

| Source | Date | Browser (as published) | Value | Verified |
|---|---|---|---|---|
| THECOUNTER | 2008-11-30 | FireFox | 17 | UNVERIFIED |
| THECOUNTER | 2008-11-30 | MSIE 6.x | 35 | UNVERIFIED |
| THECOUNTER | 2008-11-30 | MSIE 7.x | 42 | UNVERIFIED |
| THECOUNTER | 2008-11-30 | Opera x.x | 1 | UNVERIFIED |
| THECOUNTER | 2008-11-30 | Safari | 4 | UNVERIFIED |
| THECOUNTER | 2008-11-30 | Unknown | 1 | UNVERIFIED |
| THECOUNTER | 2008-12-31 | FireFox | 17 | UNVERIFIED |
| THECOUNTER | 2008-12-31 | MSIE 6.x | 35 | UNVERIFIED |
| THECOUNTER | 2008-12-31 | MSIE 7.x | 42 | UNVERIFIED |
| THECOUNTER | 2008-12-31 | Opera x.x | 1 | UNVERIFIED |
| THECOUNTER | 2008-12-31 | Safari | 4 | UNVERIFIED |
| THECOUNTER | 2008-12-31 | Unknown | 1 | UNVERIFIED |
| THECOUNTER | 2009-02-28 | FireFox | 18 | UNVERIFIED |
| THECOUNTER | 2009-02-28 | MSIE 6.x | 34 | UNVERIFIED |
| THECOUNTER | 2009-02-28 | MSIE 7.x | 42 | UNVERIFIED |
| THECOUNTER | 2009-02-28 | Netscape comp. | 1 | UNVERIFIED |
| THECOUNTER | 2009-02-28 | Opera x.x | 1 | UNVERIFIED |
| THECOUNTER | 2009-02-28 | Safari | 4 | UNVERIFIED |
| THECOUNTER | 2009-02-28 | Unknown | 1 | UNVERIFIED |
| NETAPPLICATIONS | 2008-11-30 | Chrome | 0.83 | UNVERIFIED |
| NETAPPLICATIONS | 2008-11-30 | Firefox | 20.78 | UNVERIFIED |
| NETAPPLICATIONS | 2008-11-30 | Internet Explorer | 69.77 | UNVERIFIED |
| NETAPPLICATIONS | 2008-11-30 | Opera | 0.71 | UNVERIFIED |
| NETAPPLICATIONS | 2008-11-30 | Safari | 7.13 | UNVERIFIED |
| NETAPPLICATIONS | 2008-12-31 | Chrome | 1.04 | UNVERIFIED |
| NETAPPLICATIONS | 2008-12-31 | Firefox | 21.34 | UNVERIFIED |
| NETAPPLICATIONS | 2008-12-31 | Internet Explorer | 68.15 | UNVERIFIED |
| NETAPPLICATIONS | 2008-12-31 | Opera | 0.71 | UNVERIFIED |
| NETAPPLICATIONS | 2008-12-31 | Safari | 7.93 | UNVERIFIED |
| NETAPPLICATIONS | 2009-01-31 | Chrome | 1.12 | UNVERIFIED |
| NETAPPLICATIONS | 2009-01-31 | Firefox | 21.53 | UNVERIFIED |
| NETAPPLICATIONS | 2009-01-31 | Internet Explorer | 67.55 | UNVERIFIED |
| NETAPPLICATIONS | 2009-01-31 | Opera | 0.70 | UNVERIFIED |
| NETAPPLICATIONS | 2009-01-31 | Safari | 8.29 | UNVERIFIED |
| NETAPPLICATIONS | 2009-02-28 | Chrome | 1.15 | UNVERIFIED |
| NETAPPLICATIONS | 2009-02-28 | Firefox | 21.77 | UNVERIFIED |
| NETAPPLICATIONS | 2009-02-28 | Internet Explorer | 67.44 | UNVERIFIED |
| NETAPPLICATIONS | 2009-02-28 | Opera | 0.71 | UNVERIFIED |
| NETAPPLICATIONS | 2009-02-28 | Safari | 8.02 | UNVERIFIED |
| XITI | 2008-11-30 | Google Chrome | 0.9 | UNVERIFIED |
| XITI | 2008-11-30 | Internet Explorer | 67.2 | UNVERIFIED |
| XITI | 2008-11-30 | Mozilla | 26.4 | UNVERIFIED |
| XITI | 2008-11-30 | Netscape | 0.4 | UNVERIFIED |
| XITI | 2008-11-30 | Opera | 2.1 | UNVERIFIED |
| XITI | 2008-11-30 | Safari | 2.9 | UNVERIFIED |
| XITI | 2008-12-31 | Google Chrome | 1.1 | UNVERIFIED |
| XITI | 2008-12-31 | Internet Explorer | 66.2 | UNVERIFIED |
| XITI | 2008-12-31 | Mozilla | 27.0 | UNVERIFIED |
| XITI | 2008-12-31 | Netscape | 0.4 | UNVERIFIED |
| XITI | 2008-12-31 | Opera | 2.2 | UNVERIFIED |
| XITI | 2008-12-31 | Other browsers | 0.1 | UNVERIFIED |
| XITI | 2008-12-31 | Safari | 3.0 | UNVERIFIED |
| XITI | 2009-01-31 | Google Chrome | 1.2 | UNVERIFIED |
| XITI | 2009-01-31 | Internet Explorer | 66.0 | UNVERIFIED |
| XITI | 2009-01-31 | Mozilla | 27.2 | UNVERIFIED |
| XITI | 2009-01-31 | Netscape | 0.4 | UNVERIFIED |
| XITI | 2009-01-31 | Opera | 2.0 | UNVERIFIED |
| XITI | 2009-01-31 | Other browsers | 0.1 | UNVERIFIED |
| XITI | 2009-01-31 | Safari | 3.0 | UNVERIFIED |
| XITI | 2009-02-28 | Google Chrome | 1.3 | UNVERIFIED |
| XITI | 2009-02-28 | Internet Explorer | 65.6 | UNVERIFIED |
| XITI | 2009-02-28 | Mozilla | 27.4 | UNVERIFIED |
| XITI | 2009-02-28 | Netscape | 0.5 | UNVERIFIED |
| XITI | 2009-02-28 | Opera | 2.1 | UNVERIFIED |
| XITI | 2009-02-28 | Other browsers | 0.1 | UNVERIFIED |
| XITI | 2009-02-28 | Safari | 3.0 | UNVERIFIED |
| W3COUNTER | 2009-01-31 | Firefox | 31.1 | yes |
| W3COUNTER | 2009-01-31 | Internet Explorer | 58.4 | yes |
| W3COUNTER | 2009-01-31 | Mozilla | 1.1 | yes |
| W3COUNTER | 2009-01-31 | Opera | 2.0 | yes |
| W3COUNTER | 2009-01-31 | Safari | 2.7 | yes |
| W3SCHOOLS | 2008-11-30 | Chrome | 3.1 | UNVERIFIED |
| W3SCHOOLS | 2008-11-30 | Firefox | 44.2 | UNVERIFIED |
| W3SCHOOLS | 2008-11-30 | IE6 | 20.0 | UNVERIFIED |
| W3SCHOOLS | 2008-11-30 | IE7 | 26.6 | UNVERIFIED |
| W3SCHOOLS | 2008-11-30 | Opera | 2.3 | UNVERIFIED |
| W3SCHOOLS | 2008-11-30 | Safari | 2.7 | UNVERIFIED |
| W3SCHOOLS | 2008-12-31 | Chrome | 3.6 | UNVERIFIED |
| W3SCHOOLS | 2008-12-31 | Firefox | 44.4 | UNVERIFIED |
| W3SCHOOLS | 2008-12-31 | IE6 | 19.6 | UNVERIFIED |
| W3SCHOOLS | 2008-12-31 | IE7 | 26.1 | UNVERIFIED |
| W3SCHOOLS | 2008-12-31 | Opera | 2.4 | UNVERIFIED |
| W3SCHOOLS | 2008-12-31 | Safari | 2.7 | UNVERIFIED |
| W3SCHOOLS | 2009-01-31 | Chrome | 3.9 | UNVERIFIED |
| W3SCHOOLS | 2009-01-31 | Firefox | 45.5 | UNVERIFIED |
| W3SCHOOLS | 2009-01-31 | IE6 | 18.5 | UNVERIFIED |
| W3SCHOOLS | 2009-01-31 | IE7 | 25.7 | UNVERIFIED |
| W3SCHOOLS | 2009-01-31 | IE8 | 0.6 | UNVERIFIED |
| W3SCHOOLS | 2009-01-31 | Opera | 2.3 | UNVERIFIED |
| W3SCHOOLS | 2009-01-31 | Safari | 3.0 | UNVERIFIED |
| W3SCHOOLS | 2009-02-28 | Chrome | 4.0 | UNVERIFIED |
| W3SCHOOLS | 2009-02-28 | Firefox | 46.4 | UNVERIFIED |
| W3SCHOOLS | 2009-02-28 | IE6 | 17.4 | UNVERIFIED |
| W3SCHOOLS | 2009-02-28 | IE7 | 25.4 | UNVERIFIED |
| W3SCHOOLS | 2009-02-28 | IE8 | 0.8 | UNVERIFIED |
| W3SCHOOLS | 2009-02-28 | Opera | 2.2 | UNVERIFIED |
| W3SCHOOLS | 2009-02-28 | Safari | 3.0 | UNVERIFIED |

## Disagreements (recorded, never averaged)

| Figure | Source | Date | Value | Disagrees with | Note |
|---|---|---|---|---|---|
| STATMARKET-1999-02-08-internet_explorer | STATMARKET | 1999-02-08 | Internet Explorer 64.60 | EWS-1999-02-28-microsoft = 54.4 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-1999-02-08-netscape | STATMARKET | 1999-02-08 | Netscape 33.43 | EWS-1999-02-28-netscape = 43.0 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-1999-03-01-internet_explorer | STATMARKET | 1999-03-01 | Internet Explorer 66.9 | EWS-1999-03-31-microsoft = 54.7 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-1999-03-01-netscape | STATMARKET | 1999-03-01 | Netscape 31.21 | EWS-1999-03-31-netscape = 42.7 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-1999-04-06-internet_explorer | STATMARKET | 1999-04-06 | Internet Explorer 68.75 | EWS-1999-04-30-microsoft = 55.2 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-1999-04-06-netscape | STATMARKET | 1999-04-06 | Netscape 29.46 | EWS-1999-04-30-netscape = 42.4 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-1999-08-02-internet_explorer | STATMARKET | 1999-08-02 | Internet Explorer 75.31 | EWS-1999-08-31-microsoft = 61.8 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-1999-08-02-netscape | STATMARKET | 1999-08-02 | Netscape 24.68 | EWS-1999-08-31-netscape = 35.4 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-2000-06-18-internet_explorer | STATMARKET | 2000-06-18 | Internet Explorer 86.08 | EWS-2000-06-30-microsoft = 69.0 | outside this source's era: cross-check only (DEC-156) |
| STATMARKET-2000-06-18-netscape | STATMARKET | 2000-06-18 | Netscape 13.90 | EWS-2000-06-30-netscape = 28.4 | outside this source's era: cross-check only (DEC-156) |
| ONESTAT-2005-11-30-apple_safari | ONESTAT | 2005-11-30 | Apple Safari 1.75 | ONESTAT-2005-11-02 (same values, dated differently) | the same figures as OneStat's release of 2 Nov 2005 (used there); a later release labels them November 2005 |
| ONESTAT-2005-11-30-microsoft_ie | ONESTAT | 2005-11-30 | Microsoft IE 85.45 | ONESTAT-2005-11-02 (same values, dated differently) | the same figures as OneStat's release of 2 Nov 2005 (used there); a later release labels them November 2005 |
| ONESTAT-2005-11-30-mozilla_firefox | ONESTAT | 2005-11-30 | Mozilla Firefox 11.51 | ONESTAT-2005-11-02 (same values, dated differently) | the same figures as OneStat's release of 2 Nov 2005 (used there); a later release labels them November 2005 |
| ONESTAT-2005-11-30-netscape | ONESTAT | 2005-11-30 | Netscape 0.26 | ONESTAT-2005-11-02 (same values, dated differently) | the same figures as OneStat's release of 2 Nov 2005 (used there); a later release labels them November 2005 |
| ONESTAT-2005-11-30-opera | ONESTAT | 2005-11-30 | Opera 0.77 | ONESTAT-2005-11-02 (same values, dated differently) | the same figures as OneStat's release of 2 Nov 2005 (used there); a later release labels them November 2005 |
| ONESTAT-2007-06-30-apple_safari | ONESTAT | 2007-06-30 | Apple Safari 1.79 | W3COUNTER-2007-06-30-safari = 2.3 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2007-06-30-internet_explorer | ONESTAT | 2007-06-30 | Internet Explorer 85.81 | W3COUNTER-2007-06-30-internet_explorer = 66.9 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2007-06-30-mozilla_firefox | ONESTAT | 2007-06-30 | Mozilla Firefox 12.72 | W3COUNTER-2007-06-30-firefox = 25.1 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2007-06-30-opera | ONESTAT | 2007-06-30 | Opera 0.61 | W3COUNTER-2007-06-30-opera = 1.8 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2007-06-30-explorer | ONESTAT | 2007-06-30 | Explorer 84.66 | W3COUNTER-2007-06-30-internet_explorer = 66.9 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2007-06-30-firefox | ONESTAT | 2007-06-30 | Firefox 12.72 | W3COUNTER-2007-06-30-firefox = 25.1 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2007-06-30-opera_2 | ONESTAT | 2007-06-30 | Opera 0.61 | W3COUNTER-2007-06-30-opera = 1.8 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2007-06-30-safari | ONESTAT | 2007-06-30 | Safari 1.79 | W3COUNTER-2007-06-30-safari = 2.3 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2008-02-29-apple_safari | ONESTAT | 2008-02-29 | Apple Safari 2.18 | W3COUNTER-2008-02-29-safari = 2.8 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2008-02-29-internet_explorer | ONESTAT | 2008-02-29 | Internet Explorer 83.27 | W3COUNTER-2008-02-29-internet_explorer = 62.0 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2008-02-29-mozilla_firefox | ONESTAT | 2008-02-29 | Mozilla Firefox 13.76 | W3COUNTER-2008-02-29-firefox = 28.7 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2008-02-29-opera | ONESTAT | 2008-02-29 | Opera 0.55 | W3COUNTER-2008-02-29-opera = 2.0 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2003-07-28-mozilla | ONESTAT | 2003-07-28 | Mozilla 0.51 | ONESTAT-2003-07-28-mozilla_2 | two different values for this browser on this date in OneStat's releases: disagreement, neither used (never averaged) |
| ONESTAT-2003-07-28-mozilla_2 | ONESTAT | 2003-07-28 | Mozilla 1.6 | ONESTAT-2003-07-28-mozilla | two different values for this browser on this date in OneStat's releases: disagreement, neither used (never averaged) |
| ONESTAT-2003-02-03-microsoft_ie | ONESTAT | 2003-02-03 | Microsoft IE 15.41 | ONESTAT-2003-02-03-microsoft_all_versions / -netscape (same release) | second table in the 3 Feb 2003 release whose measure is not stated (IE 15.41 beside IE 95.2 in the same release cannot be a share of all browsers); listed, not used |
| ONESTAT-2003-02-03-mozilla | ONESTAT | 2003-02-03 | Mozilla 14.55 | ONESTAT-2003-02-03-microsoft_all_versions / -netscape (same release) | second table in the 3 Feb 2003 release whose measure is not stated (IE 15.41 beside IE 95.2 in the same release cannot be a share of all browsers); listed, not used |
| ONESTAT-2003-02-03-netscape_navigator | ONESTAT | 2003-02-03 | Netscape Navigator 15.29 | ONESTAT-2003-02-03-microsoft_all_versions / -netscape (same release) | second table in the 3 Feb 2003 release whose measure is not stated (IE 15.41 beside IE 95.2 in the same release cannot be a share of all browsers); listed, not used |
| ONESTAT-2008-11-24-apple_safari | ONESTAT | 2008-11-24 | Apple Safari 2.42 | W3COUNTER-2008-11-30-safari = 3.0 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2008-11-24-internet_explorer | ONESTAT | 2008-11-24 | Internet Explorer 81.36 | W3COUNTER-2008-11-30-internet_explorer = 59.0 | outside this source's era (DEC-152): cross-check only, never on screen |
| ONESTAT-2008-11-24-opera | ONESTAT | 2008-11-24 | Opera 0.55 | W3COUNTER-2008-11-30-opera = 2.0 | outside this source's era (DEC-152): cross-check only, never on screen |

## UNVERIFIED and NOT FOUND items (listed, never used)

| Figure | Source | Date | Browser | Value | Status | Why |
|---|---|---|---|---|---|---|
| THECOUNTER-2000-11-30-msie_1_x | THECOUNTER | 2000-11-30 | MSIE 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-msie_2_x | THECOUNTER | 2000-11-30 | MSIE 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-msie_3_x | THECOUNTER | 2000-11-30 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-msie_4_x | THECOUNTER | 2000-11-30 | MSIE 4.x | 14 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-msie_5_x | THECOUNTER | 2000-11-30 | MSIE 5.x | 68 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-netscape_1_x | THECOUNTER | 2000-11-30 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-netscape_2_x | THECOUNTER | 2000-11-30 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-netscape_3_x | THECOUNTER | 2000-11-30 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-netscape_4_x | THECOUNTER | 2000-11-30 | Netscape 4.x | 12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-netscape_5_x | THECOUNTER | 2000-11-30 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-netscape_comp | THECOUNTER | 2000-11-30 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-opera_x_x | THECOUNTER | 2000-11-30 | Opera x.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2000-11-30-unknow | THECOUNTER | 2000-11-30 | Unknow | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-msie_1_x | THECOUNTER | 2001-01-31 | MSIE 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-msie_2_x | THECOUNTER | 2001-01-31 | MSIE 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-msie_3_x | THECOUNTER | 2001-01-31 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-msie_4_x | THECOUNTER | 2001-01-31 | MSIE 4.x | 12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-msie_5_x | THECOUNTER | 2001-01-31 | MSIE 5.x | 72 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-mozilla_5_x | THECOUNTER | 2001-01-31 | Mozilla 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-netscape_1_x | THECOUNTER | 2001-01-31 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-netscape_2_x | THECOUNTER | 2001-01-31 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-netscape_3_x | THECOUNTER | 2001-01-31 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-netscape_4_x | THECOUNTER | 2001-01-31 | Netscape 4.x | 10 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-netscape_comp | THECOUNTER | 2001-01-31 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-opera_x_x | THECOUNTER | 2001-01-31 | Opera x.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-01-31-unknow | THECOUNTER | 2001-01-31 | Unknow | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-msie_1_x | THECOUNTER | 2001-02-28 | MSIE 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-msie_2_x | THECOUNTER | 2001-02-28 | MSIE 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-msie_3_x | THECOUNTER | 2001-02-28 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-msie_4_x | THECOUNTER | 2001-02-28 | MSIE 4.x | 11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-msie_5_x | THECOUNTER | 2001-02-28 | MSIE 5.x | 75 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-mozilla_5_x | THECOUNTER | 2001-02-28 | Mozilla 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-netscape_1_x | THECOUNTER | 2001-02-28 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-netscape_2_x | THECOUNTER | 2001-02-28 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-netscape_3_x | THECOUNTER | 2001-02-28 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-netscape_4_x | THECOUNTER | 2001-02-28 | Netscape 4.x | 9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-netscape_comp | THECOUNTER | 2001-02-28 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-opera_x_x | THECOUNTER | 2001-02-28 | Opera x.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2001-02-28-unknow | THECOUNTER | 2001-02-28 | Unknow | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-msie_1_x | THECOUNTER | 2002-06-30 | MSIE 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-msie_2_x | THECOUNTER | 2002-06-30 | MSIE 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-msie_3_x | THECOUNTER | 2002-06-30 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-msie_4_x | THECOUNTER | 2002-06-30 | MSIE 4.x | 2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-msie_5_x | THECOUNTER | 2002-06-30 | MSIE 5.x | 52 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-msie_6_x | THECOUNTER | 2002-06-30 | MSIE 6.x | 37 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-netscape_1_x | THECOUNTER | 2002-06-30 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-netscape_2_x | THECOUNTER | 2002-06-30 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-netscape_3_x | THECOUNTER | 2002-06-30 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-netscape_4_x | THECOUNTER | 2002-06-30 | Netscape 4.x | 3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-netscape_5_x | THECOUNTER | 2002-06-30 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-netscape_6_x | THECOUNTER | 2002-06-30 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-netscape_comp | THECOUNTER | 2002-06-30 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-opera_x_x | THECOUNTER | 2002-06-30 | Opera x.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-06-30-unknown | THECOUNTER | 2002-06-30 | Unknown | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-msie_1_x | THECOUNTER | 2002-07-31 | MSIE 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-msie_2_x | THECOUNTER | 2002-07-31 | MSIE 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-msie_3_x | THECOUNTER | 2002-07-31 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-msie_4_x | THECOUNTER | 2002-07-31 | MSIE 4.x | 2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-msie_5_x | THECOUNTER | 2002-07-31 | MSIE 5.x | 50 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-msie_6_x | THECOUNTER | 2002-07-31 | MSIE 6.x | 39 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-netscape_1_x | THECOUNTER | 2002-07-31 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-netscape_2_x | THECOUNTER | 2002-07-31 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-netscape_3_x | THECOUNTER | 2002-07-31 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-netscape_4_x | THECOUNTER | 2002-07-31 | Netscape 4.x | 3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-netscape_5_x | THECOUNTER | 2002-07-31 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-netscape_6_x | THECOUNTER | 2002-07-31 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-netscape_comp | THECOUNTER | 2002-07-31 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-opera_x_x | THECOUNTER | 2002-07-31 | Opera x.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-07-31-unknown | THECOUNTER | 2002-07-31 | Unknown | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-msie_1_x | THECOUNTER | 2002-08-31 | MSIE 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-msie_2_x | THECOUNTER | 2002-08-31 | MSIE 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-msie_3_x | THECOUNTER | 2002-08-31 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-msie_4_x | THECOUNTER | 2002-08-31 | MSIE 4.x | 2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-msie_5_x | THECOUNTER | 2002-08-31 | MSIE 5.x | 49 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-msie_6_x | THECOUNTER | 2002-08-31 | MSIE 6.x | 41 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-netscape_1_x | THECOUNTER | 2002-08-31 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-netscape_2_x | THECOUNTER | 2002-08-31 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-netscape_3_x | THECOUNTER | 2002-08-31 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-netscape_4_x | THECOUNTER | 2002-08-31 | Netscape 4.x | 2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-netscape_5_x | THECOUNTER | 2002-08-31 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-netscape_6_x | THECOUNTER | 2002-08-31 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-netscape_comp | THECOUNTER | 2002-08-31 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-opera_x_x | THECOUNTER | 2002-08-31 | Opera x.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-08-31-unknown | THECOUNTER | 2002-08-31 | Unknown | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-msie_1_x | THECOUNTER | 2002-09-30 | MSIE 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-msie_2_x | THECOUNTER | 2002-09-30 | MSIE 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-msie_3_x | THECOUNTER | 2002-09-30 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-msie_4_x | THECOUNTER | 2002-09-30 | MSIE 4.x | 2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-msie_5_x | THECOUNTER | 2002-09-30 | MSIE 5.x | 47 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-msie_6_x | THECOUNTER | 2002-09-30 | MSIE 6.x | 43 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-netscape_1_x | THECOUNTER | 2002-09-30 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-netscape_2_x | THECOUNTER | 2002-09-30 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-netscape_3_x | THECOUNTER | 2002-09-30 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-netscape_4_x | THECOUNTER | 2002-09-30 | Netscape 4.x | 2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-netscape_5_x | THECOUNTER | 2002-09-30 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-netscape_6_x | THECOUNTER | 2002-09-30 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-netscape_comp | THECOUNTER | 2002-09-30 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-opera_x_x | THECOUNTER | 2002-09-30 | Opera x.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-09-30-unknown | THECOUNTER | 2002-09-30 | Unknown | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-msie_1_x | THECOUNTER | 2002-10-31 | MSIE 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-msie_2_x | THECOUNTER | 2002-10-31 | MSIE 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-msie_3_x | THECOUNTER | 2002-10-31 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-msie_4_x | THECOUNTER | 2002-10-31 | MSIE 4.x | 2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-msie_5_x | THECOUNTER | 2002-10-31 | MSIE 5.x | 46 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-msie_6_x | THECOUNTER | 2002-10-31 | MSIE 6.x | 45 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-netscape_1_x | THECOUNTER | 2002-10-31 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-netscape_2_x | THECOUNTER | 2002-10-31 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-netscape_3_x | THECOUNTER | 2002-10-31 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-netscape_4_x | THECOUNTER | 2002-10-31 | Netscape 4.x | 2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-netscape_5_x | THECOUNTER | 2002-10-31 | Netscape 5.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-netscape_6_x | THECOUNTER | 2002-10-31 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-netscape_comp | THECOUNTER | 2002-10-31 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-opera_x_x | THECOUNTER | 2002-10-31 | Opera x.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2002-10-31-unknown | THECOUNTER | 2002-10-31 | Unknown | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-firefox | THECOUNTER | 2007-01-31 | FireFox | 11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-konqueror | THECOUNTER | 2007-01-31 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-msie_3_x | THECOUNTER | 2007-01-31 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-msie_4_x | THECOUNTER | 2007-01-31 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-msie_5_x | THECOUNTER | 2007-01-31 | MSIE 5.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-msie_6_x | THECOUNTER | 2007-01-31 | MSIE 6.x | 63 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-msie_7_x | THECOUNTER | 2007-01-31 | MSIE 7.x | 20 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-netscape_1_x | THECOUNTER | 2007-01-31 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-netscape_2_x | THECOUNTER | 2007-01-31 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-netscape_3_x | THECOUNTER | 2007-01-31 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-netscape_4_x | THECOUNTER | 2007-01-31 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-netscape_5_x | THECOUNTER | 2007-01-31 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-netscape_6_x | THECOUNTER | 2007-01-31 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-netscape_7_x | THECOUNTER | 2007-01-31 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-netscape_comp | THECOUNTER | 2007-01-31 | Netscape comp. | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-opera_x_x | THECOUNTER | 2007-01-31 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-safari | THECOUNTER | 2007-01-31 | Safari | 3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-01-31-unknown | THECOUNTER | 2007-01-31 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-firefox | THECOUNTER | 2007-02-28 | FireFox | 11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-konqueror | THECOUNTER | 2007-02-28 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-msie_3_x | THECOUNTER | 2007-02-28 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-msie_4_x | THECOUNTER | 2007-02-28 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-msie_5_x | THECOUNTER | 2007-02-28 | MSIE 5.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-msie_6_x | THECOUNTER | 2007-02-28 | MSIE 6.x | 58 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-msie_7_x | THECOUNTER | 2007-02-28 | MSIE 7.x | 24 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-netscape_1_x | THECOUNTER | 2007-02-28 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-netscape_2_x | THECOUNTER | 2007-02-28 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-netscape_3_x | THECOUNTER | 2007-02-28 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-netscape_4_x | THECOUNTER | 2007-02-28 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-netscape_5_x | THECOUNTER | 2007-02-28 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-netscape_6_x | THECOUNTER | 2007-02-28 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-netscape_7_x | THECOUNTER | 2007-02-28 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-netscape_comp | THECOUNTER | 2007-02-28 | Netscape comp. | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-opera_x_x | THECOUNTER | 2007-02-28 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-safari | THECOUNTER | 2007-02-28 | Safari | 3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-02-28-unknown | THECOUNTER | 2007-02-28 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-firefox | THECOUNTER | 2007-03-31 | FireFox | 12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-konqueror | THECOUNTER | 2007-03-31 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-msie_3_x | THECOUNTER | 2007-03-31 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-msie_4_x | THECOUNTER | 2007-03-31 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-msie_5_x | THECOUNTER | 2007-03-31 | MSIE 5.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-msie_6_x | THECOUNTER | 2007-03-31 | MSIE 6.x | 58 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-msie_7_x | THECOUNTER | 2007-03-31 | MSIE 7.x | 25 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-netscape_1_x | THECOUNTER | 2007-03-31 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-netscape_2_x | THECOUNTER | 2007-03-31 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-netscape_3_x | THECOUNTER | 2007-03-31 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-netscape_4_x | THECOUNTER | 2007-03-31 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-netscape_5_x | THECOUNTER | 2007-03-31 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-netscape_6_x | THECOUNTER | 2007-03-31 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-netscape_7_x | THECOUNTER | 2007-03-31 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-netscape_comp | THECOUNTER | 2007-03-31 | Netscape comp. | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-opera_x_x | THECOUNTER | 2007-03-31 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-safari | THECOUNTER | 2007-03-31 | Safari | 3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-03-31-unknown | THECOUNTER | 2007-03-31 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-firefox | THECOUNTER | 2007-04-30 | FireFox | 12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-konqueror | THECOUNTER | 2007-04-30 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-msie_3_x | THECOUNTER | 2007-04-30 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-msie_4_x | THECOUNTER | 2007-04-30 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-msie_5_x | THECOUNTER | 2007-04-30 | MSIE 5.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-msie_6_x | THECOUNTER | 2007-04-30 | MSIE 6.x | 56 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-msie_7_x | THECOUNTER | 2007-04-30 | MSIE 7.x | 14 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-netscape_1_x | THECOUNTER | 2007-04-30 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-netscape_2_x | THECOUNTER | 2007-04-30 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-netscape_3_x | THECOUNTER | 2007-04-30 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-netscape_4_x | THECOUNTER | 2007-04-30 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-netscape_5_x | THECOUNTER | 2007-04-30 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-netscape_6_x | THECOUNTER | 2007-04-30 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-netscape_7_x | THECOUNTER | 2007-04-30 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-netscape_comp | THECOUNTER | 2007-04-30 | Netscape comp. | 12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-opera_x_x | THECOUNTER | 2007-04-30 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-safari | THECOUNTER | 2007-04-30 | Safari | 3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-04-30-unknown | THECOUNTER | 2007-04-30 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-firefox | THECOUNTER | 2007-05-31 | FireFox | 12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-konqueror | THECOUNTER | 2007-05-31 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-msie_3_x | THECOUNTER | 2007-05-31 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-msie_4_x | THECOUNTER | 2007-05-31 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-msie_5_x | THECOUNTER | 2007-05-31 | MSIE 5.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-msie_6_x | THECOUNTER | 2007-05-31 | MSIE 6.x | 56 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-msie_7_x | THECOUNTER | 2007-05-31 | MSIE 7.x | 15 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-netscape_1_x | THECOUNTER | 2007-05-31 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-netscape_2_x | THECOUNTER | 2007-05-31 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-netscape_3_x | THECOUNTER | 2007-05-31 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-netscape_4_x | THECOUNTER | 2007-05-31 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-netscape_5_x | THECOUNTER | 2007-05-31 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-netscape_6_x | THECOUNTER | 2007-05-31 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-netscape_7_x | THECOUNTER | 2007-05-31 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-netscape_comp | THECOUNTER | 2007-05-31 | Netscape comp. | 11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-opera_x_x | THECOUNTER | 2007-05-31 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-safari | THECOUNTER | 2007-05-31 | Safari | 3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-05-31-unknown | THECOUNTER | 2007-05-31 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-firefox | THECOUNTER | 2007-06-30 | FireFox | 12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-konqueror | THECOUNTER | 2007-06-30 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-msie_3_x | THECOUNTER | 2007-06-30 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-msie_4_x | THECOUNTER | 2007-06-30 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-msie_5_x | THECOUNTER | 2007-06-30 | MSIE 5.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-msie_6_x | THECOUNTER | 2007-06-30 | MSIE 6.x | 54 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-msie_7_x | THECOUNTER | 2007-06-30 | MSIE 7.x | 16 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-netscape_1_x | THECOUNTER | 2007-06-30 | Netscape 1.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-netscape_2_x | THECOUNTER | 2007-06-30 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-netscape_3_x | THECOUNTER | 2007-06-30 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-netscape_4_x | THECOUNTER | 2007-06-30 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-netscape_5_x | THECOUNTER | 2007-06-30 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-netscape_6_x | THECOUNTER | 2007-06-30 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-netscape_7_x | THECOUNTER | 2007-06-30 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-netscape_comp | THECOUNTER | 2007-06-30 | Netscape comp. | 11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-opera_x_x | THECOUNTER | 2007-06-30 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-safari | THECOUNTER | 2007-06-30 | Safari | 3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2007-06-30-unknown | THECOUNTER | 2007-06-30 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-firefox | THECOUNTER | 2008-11-30 | FireFox | 17 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-konqueror | THECOUNTER | 2008-11-30 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-msie_3_x | THECOUNTER | 2008-11-30 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-msie_4_x | THECOUNTER | 2008-11-30 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-msie_5_x | THECOUNTER | 2008-11-30 | MSIE 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-msie_6_x | THECOUNTER | 2008-11-30 | MSIE 6.x | 35 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-msie_7_x | THECOUNTER | 2008-11-30 | MSIE 7.x | 42 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-netscape_2_x | THECOUNTER | 2008-11-30 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-netscape_3_x | THECOUNTER | 2008-11-30 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-netscape_4_x | THECOUNTER | 2008-11-30 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-netscape_5_x | THECOUNTER | 2008-11-30 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-netscape_6_x | THECOUNTER | 2008-11-30 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-netscape_7_x | THECOUNTER | 2008-11-30 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-netscape_comp | THECOUNTER | 2008-11-30 | Netscape comp. | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-opera_x_x | THECOUNTER | 2008-11-30 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-safari | THECOUNTER | 2008-11-30 | Safari | 4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-11-30-unknown | THECOUNTER | 2008-11-30 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-firefox | THECOUNTER | 2008-12-31 | FireFox | 17 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-konqueror | THECOUNTER | 2008-12-31 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-msie_3_x | THECOUNTER | 2008-12-31 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-msie_4_x | THECOUNTER | 2008-12-31 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-msie_5_x | THECOUNTER | 2008-12-31 | MSIE 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-msie_6_x | THECOUNTER | 2008-12-31 | MSIE 6.x | 35 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-msie_7_x | THECOUNTER | 2008-12-31 | MSIE 7.x | 42 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-netscape_2_x | THECOUNTER | 2008-12-31 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-netscape_3_x | THECOUNTER | 2008-12-31 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-netscape_4_x | THECOUNTER | 2008-12-31 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-netscape_5_x | THECOUNTER | 2008-12-31 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-netscape_6_x | THECOUNTER | 2008-12-31 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-netscape_7_x | THECOUNTER | 2008-12-31 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-netscape_comp | THECOUNTER | 2008-12-31 | Netscape comp. | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-opera_x_x | THECOUNTER | 2008-12-31 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-safari | THECOUNTER | 2008-12-31 | Safari | 4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2008-12-31-unknown | THECOUNTER | 2008-12-31 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-firefox | THECOUNTER | 2009-02-28 | FireFox | 18 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-konqueror | THECOUNTER | 2009-02-28 | Konqueror | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-msie_3_x | THECOUNTER | 2009-02-28 | MSIE 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-msie_4_x | THECOUNTER | 2009-02-28 | MSIE 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-msie_5_x | THECOUNTER | 2009-02-28 | MSIE 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-msie_6_x | THECOUNTER | 2009-02-28 | MSIE 6.x | 34 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-msie_7_x | THECOUNTER | 2009-02-28 | MSIE 7.x | 42 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-netscape_2_x | THECOUNTER | 2009-02-28 | Netscape 2.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-netscape_3_x | THECOUNTER | 2009-02-28 | Netscape 3.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-netscape_4_x | THECOUNTER | 2009-02-28 | Netscape 4.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-netscape_5_x | THECOUNTER | 2009-02-28 | Netscape 5.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-netscape_6_x | THECOUNTER | 2009-02-28 | Netscape 6.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-netscape_7_x | THECOUNTER | 2009-02-28 | Netscape 7.x | 0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-netscape_comp | THECOUNTER | 2009-02-28 | Netscape comp. | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-opera_x_x | THECOUNTER | 2009-02-28 | Opera x.x | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-safari | THECOUNTER | 2009-02-28 | Safari | 4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| THECOUNTER-2009-02-28-unknown | THECOUNTER | 2009-02-28 | Unknown | 1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-11-30-chrome | NETAPPLICATIONS | 2008-11-30 | Chrome | 0.83 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-11-30-firefox | NETAPPLICATIONS | 2008-11-30 | Firefox | 20.78 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-11-30-internet_explorer | NETAPPLICATIONS | 2008-11-30 | Internet Explorer | 69.77 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-11-30-opera | NETAPPLICATIONS | 2008-11-30 | Opera | 0.71 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-11-30-safari | NETAPPLICATIONS | 2008-11-30 | Safari | 7.13 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-12-31-chrome | NETAPPLICATIONS | 2008-12-31 | Chrome | 1.04 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-12-31-firefox | NETAPPLICATIONS | 2008-12-31 | Firefox | 21.34 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-12-31-internet_explorer | NETAPPLICATIONS | 2008-12-31 | Internet Explorer | 68.15 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-12-31-opera | NETAPPLICATIONS | 2008-12-31 | Opera | 0.71 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2008-12-31-safari | NETAPPLICATIONS | 2008-12-31 | Safari | 7.93 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-01-31-chrome | NETAPPLICATIONS | 2009-01-31 | Chrome | 1.12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-01-31-firefox | NETAPPLICATIONS | 2009-01-31 | Firefox | 21.53 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-01-31-internet_explorer | NETAPPLICATIONS | 2009-01-31 | Internet Explorer | 67.55 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-01-31-opera | NETAPPLICATIONS | 2009-01-31 | Opera | 0.70 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-01-31-safari | NETAPPLICATIONS | 2009-01-31 | Safari | 8.29 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-02-28-chrome | NETAPPLICATIONS | 2009-02-28 | Chrome | 1.15 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-02-28-firefox | NETAPPLICATIONS | 2009-02-28 | Firefox | 21.77 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-02-28-internet_explorer | NETAPPLICATIONS | 2009-02-28 | Internet Explorer | 67.44 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-02-28-opera | NETAPPLICATIONS | 2009-02-28 | Opera | 0.71 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| NETAPPLICATIONS-2009-02-28-safari | NETAPPLICATIONS | 2009-02-28 | Safari | 8.02 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-11-30-google_chrome | XITI | 2008-11-30 | Google Chrome | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-11-30-internet_explorer | XITI | 2008-11-30 | Internet Explorer | 67.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-11-30-mozilla | XITI | 2008-11-30 | Mozilla | 26.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-11-30-netscape | XITI | 2008-11-30 | Netscape | 0.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-11-30-opera | XITI | 2008-11-30 | Opera | 2.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-11-30-other_browsers | XITI | 2008-11-30 | Other browsers | 0.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-11-30-safari | XITI | 2008-11-30 | Safari | 2.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-12-31-google_chrome | XITI | 2008-12-31 | Google Chrome | 1.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-12-31-internet_explorer | XITI | 2008-12-31 | Internet Explorer | 66.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-12-31-mozilla | XITI | 2008-12-31 | Mozilla | 27.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-12-31-netscape | XITI | 2008-12-31 | Netscape | 0.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-12-31-opera | XITI | 2008-12-31 | Opera | 2.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-12-31-other_browsers | XITI | 2008-12-31 | Other browsers | 0.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2008-12-31-safari | XITI | 2008-12-31 | Safari | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-01-31-google_chrome | XITI | 2009-01-31 | Google Chrome | 1.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-01-31-internet_explorer | XITI | 2009-01-31 | Internet Explorer | 66.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-01-31-mozilla | XITI | 2009-01-31 | Mozilla | 27.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-01-31-netscape | XITI | 2009-01-31 | Netscape | 0.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-01-31-opera | XITI | 2009-01-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-01-31-other_browsers | XITI | 2009-01-31 | Other browsers | 0.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-01-31-safari | XITI | 2009-01-31 | Safari | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-02-28-google_chrome | XITI | 2009-02-28 | Google Chrome | 1.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-02-28-internet_explorer | XITI | 2009-02-28 | Internet Explorer | 65.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-02-28-mozilla | XITI | 2009-02-28 | Mozilla | 27.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-02-28-netscape | XITI | 2009-02-28 | Netscape | 0.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-02-28-opera | XITI | 2009-02-28 | Opera | 2.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-02-28-other_browsers | XITI | 2009-02-28 | Other browsers | 0.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| XITI-2009-02-28-safari | XITI | 2009-02-28 | Safari | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-07-31-aol | W3SCHOOLS | 2002-07-31 | AOL | 3.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-07-31-ie4 | W3SCHOOLS | 2002-07-31 | IE4 | 0.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-07-31-ie5 | W3SCHOOLS | 2002-07-31 | IE5 | 40.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-07-31-ie6 | W3SCHOOLS | 2002-07-31 | IE6 | 44.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-07-31-n3 | W3SCHOOLS | 2002-07-31 | N3 | 1.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-07-31-n4 | W3SCHOOLS | 2002-07-31 | N4 | 2.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-07-31-n5 | W3SCHOOLS | 2002-07-31 | N5 | 3.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-09-30-aol | W3SCHOOLS | 2002-09-30 | AOL | 4.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-09-30-ie4 | W3SCHOOLS | 2002-09-30 | IE4 | NOT FOUND | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-09-30-ie5 | W3SCHOOLS | 2002-09-30 | IE5 | 34.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-09-30-ie6 | W3SCHOOLS | 2002-09-30 | IE6 | 49.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-09-30-n3 | W3SCHOOLS | 2002-09-30 | N3 | 1.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-09-30-n4 | W3SCHOOLS | 2002-09-30 | N4 | 2.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2002-09-30-n5 | W3SCHOOLS | 2002-09-30 | N5 | 4.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-01-31-firefox | W3SCHOOLS | 2007-01-31 | Firefox | 31.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-01-31-ie5 | W3SCHOOLS | 2007-01-31 | IE5 | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-01-31-ie6 | W3SCHOOLS | 2007-01-31 | IE6 | 42.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-01-31-ie7 | W3SCHOOLS | 2007-01-31 | IE7 | 13.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-01-31-mozilla | W3SCHOOLS | 2007-01-31 | Mozilla | 1.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-01-31-opera | W3SCHOOLS | 2007-01-31 | Opera | 1.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-01-31-safari | W3SCHOOLS | 2007-01-31 | Safari | 1.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-03-31-firefox | W3SCHOOLS | 2007-03-31 | Firefox | 31.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-03-31-ie5 | W3SCHOOLS | 2007-03-31 | IE5 | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-03-31-ie6 | W3SCHOOLS | 2007-03-31 | IE6 | 38.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-03-31-ie7 | W3SCHOOLS | 2007-03-31 | IE7 | 18.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-03-31-mozilla | W3SCHOOLS | 2007-03-31 | Mozilla | 1.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-03-31-opera | W3SCHOOLS | 2007-03-31 | Opera | 1.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-03-31-safari | W3SCHOOLS | 2007-03-31 | Safari | 1.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-05-31-firefox | W3SCHOOLS | 2007-05-31 | Firefox | 33.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-05-31-ie5 | W3SCHOOLS | 2007-05-31 | IE5 | 1.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-05-31-ie6 | W3SCHOOLS | 2007-05-31 | IE6 | 38.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-05-31-ie7 | W3SCHOOLS | 2007-05-31 | IE7 | 19.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-05-31-mozilla | W3SCHOOLS | 2007-05-31 | Mozilla | 1.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-05-31-opera | W3SCHOOLS | 2007-05-31 | Opera | 1.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2007-05-31-safari | W3SCHOOLS | 2007-05-31 | Safari | 1.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-11-30-chrome | W3SCHOOLS | 2008-11-30 | Chrome | 3.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-11-30-firefox | W3SCHOOLS | 2008-11-30 | Firefox | 44.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-11-30-ie5 | W3SCHOOLS | 2008-11-30 | IE5 | NOT FOUND | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-11-30-ie6 | W3SCHOOLS | 2008-11-30 | IE6 | 20.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-11-30-ie7 | W3SCHOOLS | 2008-11-30 | IE7 | 26.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-11-30-opera | W3SCHOOLS | 2008-11-30 | Opera | 2.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-11-30-safari | W3SCHOOLS | 2008-11-30 | Safari | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-12-31-chrome | W3SCHOOLS | 2008-12-31 | Chrome | 3.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-12-31-firefox | W3SCHOOLS | 2008-12-31 | Firefox | 44.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-12-31-ie5 | W3SCHOOLS | 2008-12-31 | IE5 | NOT FOUND | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-12-31-ie6 | W3SCHOOLS | 2008-12-31 | IE6 | 19.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-12-31-ie7 | W3SCHOOLS | 2008-12-31 | IE7 | 26.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-12-31-opera | W3SCHOOLS | 2008-12-31 | Opera | 2.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2008-12-31-safari | W3SCHOOLS | 2008-12-31 | Safari | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-01-31-chrome | W3SCHOOLS | 2009-01-31 | Chrome | 3.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-01-31-firefox | W3SCHOOLS | 2009-01-31 | Firefox | 45.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-01-31-ie6 | W3SCHOOLS | 2009-01-31 | IE6 | 18.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-01-31-ie7 | W3SCHOOLS | 2009-01-31 | IE7 | 25.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-01-31-ie8 | W3SCHOOLS | 2009-01-31 | IE8 | 0.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-01-31-opera | W3SCHOOLS | 2009-01-31 | Opera | 2.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-01-31-safari | W3SCHOOLS | 2009-01-31 | Safari | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-02-28-chrome | W3SCHOOLS | 2009-02-28 | Chrome | 4.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-02-28-firefox | W3SCHOOLS | 2009-02-28 | Firefox | 46.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-02-28-ie6 | W3SCHOOLS | 2009-02-28 | IE6 | 17.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-02-28-ie7 | W3SCHOOLS | 2009-02-28 | IE7 | 25.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-02-28-ie8 | W3SCHOOLS | 2009-02-28 | IE8 | 0.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-02-28-opera | W3SCHOOLS | 2009-02-28 | Opera | 2.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| W3SCHOOLS-2009-02-28-safari | W3SCHOOLS | 2009-02-28 | Safari | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |

## Questions for Luke (each with Claude's recommendation)

1. **Browser families (DEC-155).** Mosaic versions added together; Netscape 1–9 as one; Edge separate from IE; Firefox separate from the Mozilla Suite. Two further calls:
   - StatCounter's "Edge" and "Edge Legacy" are added together as one Edge bar. Because of this, September 2026 shows Edge at 6.03%, not StatCounter's headline 6.02%.
   - StatCounter's "IE Mobile" stays a separate bar.

   *Recommendation: accept both.*
2. **Hand-over rule (DEC-156).** Each source uses only its own figures. A straight line joins the last figure of one source to the first of the next. Cross-check sources are never shown. *Recommendation: accept.*
3. **Browsers a source does not report (DEC-157, refined in DEC-162).**
   - A line is drawn only between two figures of the same browser from the same source, or across a hand-over when both sides report it.
   - A single release that leaves a browser out does not break that source's line. Example: OneStat's 2004 releases omit Netscape.
   - Consequences:
     - MacWeb (3% on 16 Nov 1994) never appears at a month end.
     - Lynx and Mosaic stop in June 1997, when EWS stops listing them.
     - Netscape stops in January 2007.
     - Chrome first appears in January 2009, because W3Counter's tables do not list it.
     - Opera first appears in November 2004. StatMarket's single Opera figure (0.33% on 25 Oct 2001) has no neighbouring Opera figure to join, and OneStat gave Opera only by version until November 2004.

   *Recommendation: accept.*
4. **Dates (DEC-158).**
   - GVU's first survey (announced 17 January 1994, "posted on the Web for a month") is dated 31 January 1994.
   - OneStat releases are dated on their release day.
   - Monthly reports are dated at the month end.

   *Recommendation: accept.*
5. **"Other" is never a bar (DEC-159).** *Recommendation: accept.*
6. **EWS "Mosaic" includes Internet Explorer until May 1996.**
   - Following the source, the Mosaic bar falls from 13.4% (May 1996) to 3.4% (June 1996).
   - Internet Explorer then appears from nowhere at 11.0%.

   *Recommendation: keep the source as published and, in the player session, propose a short on-screen note (a new feature, so your approval first, DEC-069).*
7. **Netscape overtaking Mosaic.** It happens on the 1994–96 hand-over line (June 1995 in the data), which has no figure. *Recommendation: no dated callout; if a callout is wanted, word it "between late 1994 and spring 1996 (estimate)".*
8. **The big moves at the hand-overs.** IE +12 points across 2000–01 and −19 points across 2007, as the measure changes. *Recommendation: accept, as you decided (DEC-153), and name the source on screen at each era as planned. Optional extra: a short "new source" marker at each hand-over (a new feature, DEC-069).*
9. **GVU's terms.** GVU's copyright notice says the recipient "may not derive income for the Georgia Tech Research Corporation information itself" and must acknowledge GTRC (`reference/rights_ledger.md`). *Recommendation: credit GVU / Georgia Tech on screen and in the description. Decide whether you are comfortable that a monetised video does not "derive income for the information itself". This is not legal advice, and Isle of Man law has not been checked.*
10. **Terms for EWS, StatMarket, OneStat and W3Counter: NOT FOUND.** *Recommendation: we use only a few published percentages as facts, with the source named; accept, or ask Cowork to look for terms pages.*
11. **Disagreements.**
    - StatMarket's 1999–2000 figures are 10–17 points higher for IE than EWS in the same months.
    - OneStat's 3 February 2003 release has a second table with an unstated measure. It is not used.
    - OneStat's 28 July 2003 release prints two Mozilla values (0.51 and 1.6). Neither is used.

    *Recommendation: as handled (never averaged); listed below.*
12. **GVU April 1995 (Netscape 54%) stays UNVERIFIED.** It exists only in a secondary source, and GVU's own April 1995 survey pages have no browser chart. *Recommendation: leave it out.*
