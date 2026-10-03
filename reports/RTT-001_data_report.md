# RTT-001 Browser Wars — data report for Luke

Build `rtt001-build/1.0` (`scripts/build_rtt001_dataset.py`). Contract: `reference/metric_contract_RTT-001.md`. Data: `data/rtt-001/`.

## Summary
(draft)

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
| 1995-07 | Netscape | 47.72% | Mosaic (43.03) | interpolated, on a hand-over stretch (no figure: the date is set only by the straight line) | Estimate between GVU survey (Nov 1994) and Illinois EWS server (May 1996) |
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

Source line: Estimate between GVU survey (Nov 1994) and Illinois EWS server (May 1996) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Mosaic | 66.64% | interpolated |
| 2 | Netscape | 19.62% | interpolated |
| 3 | Lynx | 1.97% | interpolated |

### April 1996

Source line: Estimate between GVU survey (Nov 1994) and Illinois EWS server (May 1996) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Netscape | 79.41% | interpolated |
| 2 | Mosaic | 16.41% | interpolated |
| 3 | Lynx | 0.77% | interpolated |

### October 1998

Source line: University of Illinois EWS web server · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 49.1% | observed |
| 2 | Netscape | 48.3% | observed |

### January 2001

Source line: Estimate between Illinois EWS server (Jan 1999) and StatCounter (Jan 2009) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 56.28% | interpolated |

### January 2004

Source line: Estimate between Illinois EWS server (Jan 1999) and StatCounter (Jan 2009) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 59.53% | interpolated |

### January 2007

Source line: Estimate between Illinois EWS server (Jan 1999) and StatCounter (Jan 2009) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 62.79% | interpolated |

### December 2008

Source line: Estimate between Illinois EWS server (Jan 1999) and StatCounter (Jan 2009) · estimated look

| # | Browser | Share | Provenance |
|---|---|---|---|
| 1 | Internet Explorer | 64.88% | interpolated |

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

Outgoing last point 1994-11-16; incoming first point 1996-05-31; 562 days of straight line.

| Browser | Outgoing value | Incoming value |
|---|---|---|
| Lynx | 2% | 0.7% |
| MacWeb | 3% | not reported |
| Mosaic | 68% | 13.4% |
| Netscape | 18% | 83.0% |

### University of Illinois EWS web server → StatCounter Global Stats

Outgoing last point 1999-01-31; incoming first point 2009-01-31; 3653 days of straight line.

| Browser | Outgoing value | Incoming value |
|---|---|---|
| AOL | not reported | 0.27% |
| Android Browser | not reported | 0.01% |
| BlackBerry | not reported | 0.03% |
| Chrome | not reported | 1.37% |
| Firefox | not reported | 26.85% |
| IE Mobile | not reported | 0.01% |
| Internet Explorer | 54.1% | 64.97% |
| Mozilla Suite | not reported | 0.15% |
| NetFront | not reported | 0.01% |
| Netscape | 43.2% | not reported |
| Nokia | not reported | 0.12% |
| Openwave | not reported | 0.02% |
| Opera | not reported | 3.07% |
| Safari | not reported | 2.79% |
| SeaMonkey | not reported | 0.04% |
| Sony PS3 | not reported | 0.08% |
| SonyEricsson | not reported | 0.02% |

## Disagreements (recorded, never averaged)

| Figure | Source | Date | Value | Disagrees with | Note |
|---|---|---|---|---|---|

## UNVERIFIED and NOT FOUND items (listed, never used)

| Figure | Source | Date | Browser | Value | Status | Why |
|---|---|---|---|---|---|---|
| EWS-1996-04-30-lynx | EWS | 1996-04-30 | Lynx | .8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-04-30-mosaic | EWS | 1996-04-30 | Mosaic | 12.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-04-30-netscape | EWS | 1996-04-30 | Netscape | 83.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-04-30-other | EWS | 1996-04-30 | other | 3.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-06-30-lynx | EWS | 1996-06-30 | Lynx | .7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-06-30-microsoft | EWS | 1996-06-30 | Microsoft | 11.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-06-30-mosaic_other_than_ms | EWS | 1996-06-30 | Mosaic(other than MS) | 3.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-06-30-netscape | EWS | 1996-06-30 | Netscape | 82.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-06-30-other | EWS | 1996-06-30 | other | 2.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-08-31-lynx | EWS | 1996-08-31 | Lynx | .7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-08-31-microsoft | EWS | 1996-08-31 | Microsoft | 14.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-08-31-mosaic_other_than_ms | EWS | 1996-08-31 | Mosaic (other than MS) | 2.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-08-31-netscape | EWS | 1996-08-31 | Netscape | 79.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-08-31-other | EWS | 1996-08-31 | other | 2.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-09-30-lynx | EWS | 1996-09-30 | Lynx | .6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-09-30-microsoft | EWS | 1996-09-30 | Microsoft | 16.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-09-30-mosaic_other_than_ms | EWS | 1996-09-30 | Mosaic (other than MS) | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-09-30-netscape | EWS | 1996-09-30 | Netscape | 79.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-09-30-other | EWS | 1996-09-30 | other | 2.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-10-31-lynx | EWS | 1996-10-31 | Lynx | .5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-10-31-microsoft | EWS | 1996-10-31 | Microsoft | 17.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-10-31-mosaic_other_than_ms | EWS | 1996-10-31 | Mosaic (other than MS) | 1.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-10-31-netscape | EWS | 1996-10-31 | Netscape | 78.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-10-31-other | EWS | 1996-10-31 | other | 2.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-11-30-lynx | EWS | 1996-11-30 | Lynx | .5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-11-30-microsoft | EWS | 1996-11-30 | Microsoft | 19.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-11-30-mosaic_other_than_ms | EWS | 1996-11-30 | Mosaic (other than MS) | 1.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-11-30-netscape | EWS | 1996-11-30 | Netscape | 77.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1996-11-30-other | EWS | 1996-11-30 | other | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-01-31-lynx | EWS | 1997-01-31 | Lynx | .5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-01-31-microsoft | EWS | 1997-01-31 | Microsoft | 21.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-01-31-mosaic_other_than_ms | EWS | 1997-01-31 | Mosaic (other than MS) | .7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-01-31-netscape | EWS | 1997-01-31 | Netscape | 75.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-01-31-other | EWS | 1997-01-31 | other | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-02-28-lynx | EWS | 1997-02-28 | Lynx | .4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-02-28-microsoft | EWS | 1997-02-28 | Microsoft | 22.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-02-28-mosaic_other_than_ms | EWS | 1997-02-28 | Mosaic (other than MS) | .6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-02-28-netscape | EWS | 1997-02-28 | Netscape | 74.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-02-28-other | EWS | 1997-02-28 | other | 1.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-03-31-lynx | EWS | 1997-03-31 | Lynx | .4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-03-31-microsoft | EWS | 1997-03-31 | Microsoft | 24.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-03-31-mosaic_other_than_ms | EWS | 1997-03-31 | Mosaic (other than MS) | .5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-03-31-netscape | EWS | 1997-03-31 | Netscape | 73.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-03-31-other | EWS | 1997-03-31 | other | 1.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-04-30-lynx | EWS | 1997-04-30 | Lynx | .3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-04-30-microsoft | EWS | 1997-04-30 | Microsoft | 24.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-04-30-mosaic_other_than_ms | EWS | 1997-04-30 | Mosaic (other than MS) | .4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-04-30-netscape | EWS | 1997-04-30 | Netscape | 72.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-04-30-other | EWS | 1997-04-30 | other | 1.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-06-30-lynx | EWS | 1997-06-30 | Lynx | .3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-06-30-microsoft | EWS | 1997-06-30 | Microsoft | 30.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-06-30-mosaic_other_than_ms | EWS | 1997-06-30 | Mosaic (other than MS) | .3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-06-30-netscape | EWS | 1997-06-30 | Netscape | 66.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-06-30-other | EWS | 1997-06-30 | other | 2.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-08-31-microsoft | EWS | 1997-08-31 | Microsoft | 33.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-08-31-netscape | EWS | 1997-08-31 | Netscape | 63.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-08-31-other | EWS | 1997-08-31 | other | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-09-30-microsoft | EWS | 1997-09-30 | Microsoft | 32.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-09-30-netscape | EWS | 1997-09-30 | Netscape | 65.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-09-30-other | EWS | 1997-09-30 | other | 2.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-10-31-microsoft | EWS | 1997-10-31 | Microsoft | 33.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-10-31-netscape | EWS | 1997-10-31 | Netscape | 65.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-10-31-other | EWS | 1997-10-31 | other | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-11-30-microsoft | EWS | 1997-11-30 | Microsoft | 35.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-11-30-netscape | EWS | 1997-11-30 | Netscape | 61.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1997-11-30-other | EWS | 1997-11-30 | other | 2.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-01-31-microsoft | EWS | 1998-01-31 | Microsoft | 39.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-01-31-netscape | EWS | 1998-01-31 | Netscape | 58.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-01-31-other | EWS | 1998-01-31 | other | 2.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-02-28-microsoft | EWS | 1998-02-28 | Microsoft | 38.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-02-28-netscape | EWS | 1998-02-28 | Netscape | 59.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-02-28-other | EWS | 1998-02-28 | other | 2.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-03-31-microsoft | EWS | 1998-03-31 | Microsoft | 41.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-03-31-netscape | EWS | 1998-03-31 | Netscape | 55.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-03-31-other | EWS | 1998-03-31 | other | 3.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-04-30-microsoft | EWS | 1998-04-30 | Microsoft | 41.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-04-30-netscape | EWS | 1998-04-30 | Netscape | 55.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-04-30-other | EWS | 1998-04-30 | other | 3.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-05-31-microsoft | EWS | 1998-05-31 | Microsoft | 42.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-05-31-netscape | EWS | 1998-05-31 | Netscape | 53.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-05-31-other | EWS | 1998-05-31 | other | 3.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-06-30-microsoft | EWS | 1998-06-30 | Microsoft | 45.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-06-30-netscape | EWS | 1998-06-30 | Netscape | 51.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-06-30-other | EWS | 1998-06-30 | other | 3.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-07-31-microsoft | EWS | 1998-07-31 | Microsoft | 47.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-07-31-netscape | EWS | 1998-07-31 | Netscape | 49.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-07-31-other | EWS | 1998-07-31 | other | 3.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-08-31-microsoft | EWS | 1998-08-31 | Microsoft | 48.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-08-31-netscape | EWS | 1998-08-31 | Netscape | 48.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-08-31-other | EWS | 1998-08-31 | other | 3.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-12-31-microsoft | EWS | 1998-12-31 | Microsoft | 51.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-12-31-netscape | EWS | 1998-12-31 | Netscape | 45.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1998-12-31-other | EWS | 1998-12-31 | other | 2.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-02-28-microsoft | EWS | 1999-02-28 | Microsoft | 54.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-02-28-netscape | EWS | 1999-02-28 | Netscape | 43.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-02-28-other | EWS | 1999-02-28 | other | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-03-31-microsoft | EWS | 1999-03-31 | Microsoft | 54.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-03-31-netscape | EWS | 1999-03-31 | Netscape | 42.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-03-31-other | EWS | 1999-03-31 | other | 2.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-04-30-microsoft | EWS | 1999-04-30 | Microsoft | 55.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-04-30-netscape | EWS | 1999-04-30 | Netscape | 42.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-04-30-other | EWS | 1999-04-30 | other | 2.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-05-31-microsoft | EWS | 1999-05-31 | Microsoft | 57.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-05-31-netscape | EWS | 1999-05-31 | Netscape | 40.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-05-31-other | EWS | 1999-05-31 | other | 2.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-06-30-microsoft | EWS | 1999-06-30 | Microsoft | 59.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-06-30-netscape | EWS | 1999-06-30 | Netscape | 38.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-06-30-other | EWS | 1999-06-30 | other | 2.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-07-31-microsoft | EWS | 1999-07-31 | Microsoft | 61.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-07-31-netscape | EWS | 1999-07-31 | Netscape | 36.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-07-31-other | EWS | 1999-07-31 | other | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-08-31-microsoft | EWS | 1999-08-31 | Microsoft | 61.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-08-31-netscape | EWS | 1999-08-31 | Netscape | 35.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-08-31-other | EWS | 1999-08-31 | other | 2.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-09-30-microsoft | EWS | 1999-09-30 | Microsoft | 61.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-09-30-netscape | EWS | 1999-09-30 | Netscape | 35.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-09-30-other | EWS | 1999-09-30 | other | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-10-31-microsoft | EWS | 1999-10-31 | Microsoft | 62.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-10-31-netscape | EWS | 1999-10-31 | Netscape | 35.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-10-31-other | EWS | 1999-10-31 | other | 2.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-11-30-microsoft | EWS | 1999-11-30 | Microsoft | 62.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-11-30-netscape | EWS | 1999-11-30 | Netscape | 34.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-11-30-other | EWS | 1999-11-30 | other | 2.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-12-31-microsoft | EWS | 1999-12-31 | Microsoft | 65.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-12-31-netscape | EWS | 1999-12-31 | Netscape | 32.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-1999-12-31-other | EWS | 1999-12-31 | other | 2.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-01-31-microsoft | EWS | 2000-01-31 | Microsoft | 66.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-01-31-netscape | EWS | 2000-01-31 | Netscape | 31.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-01-31-other | EWS | 2000-01-31 | other | 2.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-02-29-microsoft | EWS | 2000-02-29 | Microsoft | 66.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-02-29-netscape | EWS | 2000-02-29 | Netscape | 31.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-02-29-other | EWS | 2000-02-29 | other | 2.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-03-31-microsoft | EWS | 2000-03-31 | Microsoft | 67.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-03-31-netscape | EWS | 2000-03-31 | Netscape | 30.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-03-31-other | EWS | 2000-03-31 | other | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-04-30-microsoft | EWS | 2000-04-30 | Microsoft | 67.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-04-30-netscape | EWS | 2000-04-30 | Netscape | 29.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-04-30-other | EWS | 2000-04-30 | other | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-05-31-microsoft | EWS | 2000-05-31 | Microsoft | 68.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-05-31-netscape | EWS | 2000-05-31 | Netscape | 28.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-05-31-other | EWS | 2000-05-31 | other | 2.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-06-30-microsoft | EWS | 2000-06-30 | Microsoft | 69.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-06-30-netscape | EWS | 2000-06-30 | Netscape | 28.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-06-30-other | EWS | 2000-06-30 | other | 2.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-07-31-microsoft | EWS | 2000-07-31 | Microsoft | 71.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-07-31-netscape | EWS | 2000-07-31 | Netscape | 25.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-07-31-other | EWS | 2000-07-31 | other | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-08-31-microsoft | EWS | 2000-08-31 | Microsoft | 71.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-08-31-netscape | EWS | 2000-08-31 | Netscape | 25.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-08-31-other | EWS | 2000-08-31 | other | 3.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-09-30-microsoft | EWS | 2000-09-30 | Microsoft | 72.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-09-30-netscape | EWS | 2000-09-30 | Netscape | 24.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-09-30-other | EWS | 2000-09-30 | other | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-10-31-microsoft | EWS | 2000-10-31 | Microsoft | 72.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-10-31-netscape | EWS | 2000-10-31 | Netscape | 24.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-10-31-other | EWS | 2000-10-31 | other | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-11-30-microsoft | EWS | 2000-11-30 | Microsoft | 74.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-11-30-netscape | EWS | 2000-11-30 | Netscape | 22.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-11-30-other | EWS | 2000-11-30 | other | 3.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-12-31-microsoft | EWS | 2000-12-31 | Microsoft | 75.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-12-31-netscape | EWS | 2000-12-31 | Netscape | 21.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| EWS-2000-12-31-other | EWS | 2000-12-31 | other | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-1999-02-08-internet_explorer | STATMARKET | 1999-02-08 | Internet Explorer | 64.60 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-02-08-netscape | STATMARKET | 1999-02-08 | Netscape | 33.43 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-03-01-internet_explorer | STATMARKET | 1999-03-01 | Internet Explorer | 66.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-03-01-netscape | STATMARKET | 1999-03-01 | Netscape | 31.21 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-03-01-webtv | STATMARKET | 1999-03-01 | WebTV | 1.81 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-04-06-internet_explorer | STATMARKET | 1999-04-06 | Internet Explorer | 68.75 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-04-06-netscape | STATMARKET | 1999-04-06 | Netscape | 29.46 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-internet_explorer | STATMARKET | 1999-08-02 | Internet Explorer | 75.31 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-msie_3_x | STATMARKET | 1999-08-02 | MSIE 3.x | 3.60 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-msie_4_x | STATMARKET | 1999-08-02 | MSIE 4.x | 44.73 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-msie_5_x | STATMARKET | 1999-08-02 | MSIE 5.x | 24.86 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-netscape | STATMARKET | 1999-08-02 | Netscape | 24.68 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-netscape_3_x | STATMARKET | 1999-08-02 | Netscape 3.x | 2.32 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-netscape_4_x | STATMARKET | 1999-08-02 | Netscape 4.x | 22.03 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-other | STATMARKET | 1999-08-02 | Other | 1.02 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-1999-08-02-webtv | STATMARKET | 1999-08-02 | WebTV | 1.44 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-2000-06-18-internet_explorer | STATMARKET | 2000-06-18 | Internet Explorer | 86.08 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-2000-06-18-netscape | STATMARKET | 2000-06-18 | Netscape | 13.90 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome; cross-check only, never on screen (DEC-156) |
| STATMARKET-2001-02-21-internet_explorer | STATMARKET | 2001-02-21 | Internet Explorer | 87.71 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-02-21-netscape | STATMARKET | 2001-02-21 | Netscape | 12.01 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-02-21-other | STATMARKET | 2001-02-21 | other | 0.27 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-04-25-aol | STATMARKET | 2001-04-25 | AOL | 6.41 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-04-25-internet_explorer | STATMARKET | 2001-04-25 | Internet Explorer | 86.61 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-04-25-netscape | STATMARKET | 2001-04-25 | Netscape | 13.10 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-04-25-other | STATMARKET | 2001-04-25 | Other | 0.29 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-10-25-internet_explorer | STATMARKET | 2001-10-25 | Internet Explorer | 89 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-10-25-internet_explorer_2 | STATMARKET | 2001-10-25 | Internet Explorer | 89.03 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-10-25-netscape | STATMARKET | 2001-10-25 | Netscape | 10.47 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-10-25-netscape_2 | STATMARKET | 2001-10-25 | Netscape | 10.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2001-10-25-opera | STATMARKET | 2001-10-25 | Opera | .33 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2002-08-26-internet_explorer | STATMARKET | 2002-08-26 | Internet Explorer | 95.97 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2002-08-26-internet_explorer_2 | STATMARKET | 2002-08-26 | Internet Explorer | 96 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2002-08-26-netscape | STATMARKET | 2002-08-26 | Netscape | 3.39 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2002-08-26-netscape_2 | STATMARKET | 2002-08-26 | Netscape | 3.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| STATMARKET-2002-08-26-other | STATMARKET | 2002-08-26 | Other | 0.64 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-21-microsoft_browser_all_versions | ONESTAT | 2002-06-21 | Microsoft browser (all versions) | 95.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-21-mozilla_1_0 | ONESTAT | 2002-06-21 | Mozilla 1.0 | 0.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-21-netscape | ONESTAT | 2002-06-21 | Netscape | 3.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-21-netscape_7_0 | ONESTAT | 2002-06-21 | Netscape 7.0 | 0.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-21-opera | ONESTAT | 2002-06-21 | Opera | 0.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-microsoft_all_versions | ONESTAT | 2003-02-03 | Microsoft (all versions) | 95,2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-netscape | ONESTAT | 2003-02-03 | Netscape | 2.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-netscape_7 | ONESTAT | 2003-02-03 | Netscape 7 | 0.64 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-opera_7 | ONESTAT | 2003-02-03 | Opera 7 | 0.03 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-safari | ONESTAT | 2003-02-03 | Safari | 0.11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-30-apple_safari | ONESTAT | 2005-11-30 | Apple Safari | 1.75 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-30-microsoft_ie | ONESTAT | 2005-11-30 | Microsoft IE | 85.45 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-30-mozilla_firefox | ONESTAT | 2005-11-30 | Mozilla Firefox | 11.51 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-30-netscape | ONESTAT | 2005-11-30 | Netscape | 0.26 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-30-opera | ONESTAT | 2005-11-30 | Opera | 0.77 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-apple_safari | ONESTAT | 2006-01-31 | Apple Safari | 1.88 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-internet_explorer | ONESTAT | 2006-01-31 | Internet Explorer | 85.82 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-mozilla_firefox | ONESTAT | 2006-01-31 | Mozilla Firefox | 11.23 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-netscape | ONESTAT | 2006-01-31 | Netscape | 0.16 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-opera | ONESTAT | 2006-01-31 | Opera | 0.77 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-apple_safari_2 | ONESTAT | 2006-01-31 | Apple Safari | 1.88 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-microsoft_ie | ONESTAT | 2006-01-31 | Microsoft IE | 85.82 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-mozilla_firefox_2 | ONESTAT | 2006-01-31 | Mozilla Firefox | 11.23 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-netscape_2 | ONESTAT | 2006-01-31 | Netscape | 0.16 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-01-31-opera_2 | ONESTAT | 2006-01-31 | Opera | 0.77 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-05-31-apple_safari | ONESTAT | 2006-05-31 | Apple Safari | 2.02 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-05-31-internet_explorer | ONESTAT | 2006-05-31 | Internet Explorer | 85.17 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-05-31-mozilla_firefox | ONESTAT | 2006-05-31 | Mozilla Firefox | 11.79 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-05-31-netscape | ONESTAT | 2006-05-31 | Netscape | 0.15 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-05-31-opera | ONESTAT | 2006-05-31 | Opera | 0.79 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-07-31-apple_safari | ONESTAT | 2006-07-31 | Apple Safari | 1.84 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-07-31-microsoft_ie | ONESTAT | 2006-07-31 | Microsoft IE | 83.05 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-07-31-mozilla_firefox | ONESTAT | 2006-07-31 | Mozilla Firefox | 12.93 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-07-31-netscape | ONESTAT | 2006-07-31 | Netscape | 0.16 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-07-31-opera | ONESTAT | 2006-07-31 | Opera | 1.00 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-10-31-apple_safari | ONESTAT | 2006-10-31 | Apple Safari | 1.61 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-10-31-microsoft_ie | ONESTAT | 2006-10-31 | Microsoft IE | 85.85 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-10-31-mozilla_firefox | ONESTAT | 2006-10-31 | Mozilla Firefox | 11.49 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-10-31-netscape | ONESTAT | 2006-10-31 | Netscape | 0.12 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-10-31-opera | ONESTAT | 2006-10-31 | Opera | 0.69 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-explorer | ONESTAT | 2007-01-31 | Explorer | 85.81 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-firefox | ONESTAT | 2007-01-31 | Firefox | 11.69 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-netscape | ONESTAT | 2007-01-31 | Netscape | 0.13 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-opera | ONESTAT | 2007-01-31 | Opera | 0.58 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-safari | ONESTAT | 2007-01-31 | Safari | 1.64 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-apple_safari | ONESTAT | 2007-01-31 | Apple Safari | 1.64 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-microsoft_ie | ONESTAT | 2007-01-31 | Microsoft IE | 85.81 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-mozilla_firefox | ONESTAT | 2007-01-31 | Mozilla Firefox | 11.69 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-netscape_2 | ONESTAT | 2007-01-31 | Netscape | 0.13 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-01-31-opera_2 | ONESTAT | 2007-01-31 | Opera | 0.58 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-apple_safari | ONESTAT | 2007-06-30 | Apple Safari | 1.79 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-internet_explorer | ONESTAT | 2007-06-30 | Internet Explorer | 85.81 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-mozilla_firefox | ONESTAT | 2007-06-30 | Mozilla Firefox | 12.72 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-netscape | ONESTAT | 2007-06-30 | Netscape | 0.11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-opera | ONESTAT | 2007-06-30 | Opera | 0.61 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-explorer | ONESTAT | 2007-06-30 | Explorer | 84.66 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-firefox | ONESTAT | 2007-06-30 | Firefox | 12.72 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-netscape_2 | ONESTAT | 2007-06-30 | Netscape | 0.11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-opera_2 | ONESTAT | 2007-06-30 | Opera | 0.61 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2007-06-30-safari | ONESTAT | 2007-06-30 | Safari | 1.79 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-02-29-apple_safari | ONESTAT | 2008-02-29 | Apple Safari | 2.18 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-02-29-internet_explorer | ONESTAT | 2008-02-29 | Internet Explorer | 83.27 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-02-29-internet_explorer_6 | ONESTAT | 2008-02-29 | Internet Explorer 6 | 53.95 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-02-29-internet_explorer_7 | ONESTAT | 2008-02-29 | Internet Explorer 7 | 29.06 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-02-29-mozilla_firefox | ONESTAT | 2008-02-29 | Mozilla Firefox | 13.76 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-02-29-netscape | ONESTAT | 2008-02-29 | Netscape | 0.14 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-02-29-opera | ONESTAT | 2008-02-29 | Opera | 0.55 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2009-03-31-apple_safari | ONESTAT | 2009-03-31 | Apple Safari | 2.65 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2009-03-31-google_chrome | ONESTAT | 2009-03-31 | Google Chrome | 0.86 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2009-03-31-internet_explorer | ONESTAT | 2009-03-31 | Internet Explorer | 79.79 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2009-03-31-mozilla_firefox | ONESTAT | 2009-03-31 | Mozilla Firefox | 15.59 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2009-03-31-netscape | ONESTAT | 2009-03-31 | Netscape | 0.31 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2009-03-31-opera | ONESTAT | 2009-03-31 | Opera | 0.54 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-04-27-apple_safari | ONESTAT | 2005-04-27 | Apple Safari | 1.26 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-04-27-microsoft_ie | ONESTAT | 2005-04-27 | Microsoft IE | 86.63 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-04-27-mozilla_firefox | ONESTAT | 2005-04-27 | Mozilla Firefox | 8.69 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-04-27-netscape | ONESTAT | 2005-04-27 | Netscape | 1.08 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-04-27-opera | ONESTAT | 2005-04-27 | Opera | 1.03 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-microsoft_ie | ONESTAT | 2003-07-28 | Microsoft IE | 95.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-microsoft_ie_4_0 | ONESTAT | 2003-07-28 | Microsoft IE 4.0 | 0.51 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-microsoft_ie_5_0 | ONESTAT | 2003-07-28 | Microsoft IE 5.0 | 0.51 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-microsoft_ie_5_5 | ONESTAT | 2003-07-28 | Microsoft IE 5.5 | 1.49 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-microsoft_ie_6_0 | ONESTAT | 2003-07-28 | Microsoft IE 6.0 | 97.34 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-mozilla | ONESTAT | 2003-07-28 | Mozilla | 0.51 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-mozilla_2 | ONESTAT | 2003-07-28 | Mozilla | 1.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-netscape_navigator | ONESTAT | 2003-07-28 | Netscape Navigator | 2.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-netscape_navigator_4 | ONESTAT | 2003-07-28 | Netscape Navigator 4 | 0.51 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-07-28-opera_6_0 | ONESTAT | 2003-07-28 | Opera 6.0 | 0.51 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-01-19-microsoft_ie_4_0 | ONESTAT | 2004-01-19 | Microsoft IE 4.0 | 0.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-01-19-microsoft_ie_5_0 | ONESTAT | 2004-01-19 | Microsoft IE 5.0 | 11.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-01-19-microsoft_ie_5_5 | ONESTAT | 2004-01-19 | Microsoft IE 5.5 | 13.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-01-19-microsoft_ie_6_0 | ONESTAT | 2004-01-19 | Microsoft IE 6.0 | 68.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-01-19-mozilla | ONESTAT | 2004-01-19 | Mozilla | 1.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-01-19-opera_7_0 | ONESTAT | 2004-01-19 | Opera 7.0 | 0.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-01-19-safari | ONESTAT | 2004-01-19 | Safari | 0.48 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-04-29-microsoft_ie_4_0 | ONESTAT | 2002-04-29 | Microsoft IE 4.0 | 1.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-04-29-microsoft_ie_5_0 | ONESTAT | 2002-04-29 | Microsoft IE 5.0 | 25.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-04-29-microsoft_ie_5_5 | ONESTAT | 2002-04-29 | Microsoft IE 5.5 | 25.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-04-29-microsoft_ie_6_0 | ONESTAT | 2002-04-29 | Microsoft IE 6.0 | 44.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-04-29-netscape_navigator_3_0 | ONESTAT | 2002-04-29 | Netscape Navigator 3.0 | 0.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-04-29-netscape_navigator_4_0 | ONESTAT | 2002-04-29 | Netscape Navigator 4.0 | 1.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-04-29-opera_6_0 | ONESTAT | 2002-04-29 | Opera 6.0 | 0.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-02-28-apple_safari | ONESTAT | 2005-02-28 | Apple Safari | 1.21 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-02-28-microsoft_ie | ONESTAT | 2005-02-28 | Microsoft IE | 87.28 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-02-28-mozilla_firefox | ONESTAT | 2005-02-28 | Mozilla Firefox | 8.45 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-02-28-netscape | ONESTAT | 2005-02-28 | Netscape | 1.11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-02-28-opera | ONESTAT | 2005-02-28 | Opera | 1.09 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-microsoft_ie_5_0 | ONESTAT | 2004-11-22 | Microsoft IE 5.0 | 4.18 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-microsoft_ie_5_5 | ONESTAT | 2004-11-22 | Microsoft IE 5.5 | 3.66 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-microsoft_ie_6_0 | ONESTAT | 2004-11-22 | Microsoft IE 6.0 | 80.95 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-microsoft_internet_explorer | ONESTAT | 2004-11-22 | Microsoft Internet Explorer | 88,90 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-mozilla_1_x | ONESTAT | 2004-11-22 | Mozilla 1.x | 2.77 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-mozilla_firefox | ONESTAT | 2004-11-22 | Mozilla Firefox | 4.58 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-mozilla_firefox_0_1 | ONESTAT | 2004-11-22 | Mozilla Firefox 0.1 | 2.79 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-mozilla_firefox_1_0 | ONESTAT | 2004-11-22 | Mozilla Firefox 1.0 | 1.79 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-opera | ONESTAT | 2004-11-22 | Opera | 1.33 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-opera_7_x | ONESTAT | 2004-11-22 | Opera 7.x | 1.29 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-11-22-safari | ONESTAT | 2004-11-22 | Safari | 0.91 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-11-06-apple_safari | ONESTAT | 2006-11-06 | Apple Safari | 1.61 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-11-06-microsoft_ie | ONESTAT | 2006-11-06 | Microsoft IE | 85.24 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-11-06-mozilla_firefox | ONESTAT | 2006-11-06 | Mozilla Firefox | 12.15 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-11-06-netscape | ONESTAT | 2006-11-06 | Netscape | 0.11 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2006-11-06-opera | ONESTAT | 2006-11-06 | Opera | 0.69 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-microsoft_ie | ONESTAT | 2002-09-30 | Microsoft IE | 94.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-microsoft_ie_4_0 | ONESTAT | 2002-09-30 | Microsoft IE 4.0 | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-microsoft_ie_5_0 | ONESTAT | 2002-09-30 | Microsoft IE 5.0 | 19.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-microsoft_ie_5_5 | ONESTAT | 2002-09-30 | Microsoft IE 5.5 | 20.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-microsoft_ie_6_0 | ONESTAT | 2002-09-30 | Microsoft IE 6.0 | 52.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-mozilla | ONESTAT | 2002-09-30 | Mozilla | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-mozilla_1 | ONESTAT | 2002-09-30 | Mozilla 1 | 0.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-netscape_navigator | ONESTAT | 2002-09-30 | Netscape Navigator | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-netscape_navigator_4_0 | ONESTAT | 2002-09-30 | Netscape Navigator 4.0 | 1.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-09-30-opera_6_0 | ONESTAT | 2002-09-30 | Opera 6.0 | 0.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-microsoft_ie | ONESTAT | 2003-02-03 | Microsoft IE | 15.41 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-microsoft_ie_4_0 | ONESTAT | 2003-02-03 | Microsoft IE 4.0 | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-microsoft_ie_5_0 | ONESTAT | 2003-02-03 | Microsoft IE 5.0 | 16.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-microsoft_ie_5_5 | ONESTAT | 2003-02-03 | Microsoft IE 5.5 | 16.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-microsoft_ie_6_0 | ONESTAT | 2003-02-03 | Microsoft IE 6.0 | 60.26 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-mozilla | ONESTAT | 2003-02-03 | Mozilla | 14.55 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-mozilla_1 | ONESTAT | 2003-02-03 | Mozilla 1 | 1.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-netscape_navigator | ONESTAT | 2003-02-03 | Netscape Navigator | 15.29 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-netscape_navigator_4_0 | ONESTAT | 2003-02-03 | Netscape Navigator 4.0 | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2003-02-03-opera_6_0 | ONESTAT | 2003-02-03 | Opera 6.0 | 0.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-microsoft_ie | ONESTAT | 2002-12-16 | Microsoft IE | 95.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-microsoft_ie_4_0 | ONESTAT | 2002-12-16 | Microsoft IE 4.0 | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-microsoft_ie_5_0 | ONESTAT | 2002-12-16 | Microsoft IE 5.0 | 16.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-microsoft_ie_5_5 | ONESTAT | 2002-12-16 | Microsoft IE 5.5 | 18.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-microsoft_ie_6_0 | ONESTAT | 2002-12-16 | Microsoft IE 6.0 | 57.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-mozilla | ONESTAT | 2002-12-16 | Mozilla | 1.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-mozilla_1 | ONESTAT | 2002-12-16 | Mozilla 1 | 1.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-netscape_navigator | ONESTAT | 2002-12-16 | Netscape Navigator | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-netscape_navigator_4_0 | ONESTAT | 2002-12-16 | Netscape Navigator 4.0 | 1.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-12-16-opera_6_0 | ONESTAT | 2002-12-16 | Opera 6.0 | 0.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-11-24-apple_safari | ONESTAT | 2008-11-24 | Apple Safari | 2.42 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-11-24-google_chrome | ONESTAT | 2008-11-24 | Google Chrome | 0.54 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-11-24-internet_explorer | ONESTAT | 2008-11-24 | Internet Explorer | 81.36 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-11-24-mozilla_firefox | ONESTAT | 2008-11-24 | Mozilla / Firefox | 14.67 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-11-24-netscape | ONESTAT | 2008-11-24 | Netscape | 0.32 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2008-11-24-opera | ONESTAT | 2008-11-24 | Opera | 0.55 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-05-28-microsoft_ie_4_0 | ONESTAT | 2004-05-28 | Microsoft IE 4.0 | 0.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-05-28-microsoft_ie_5_0 | ONESTAT | 2004-05-28 | Microsoft IE 5.0 | 10.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-05-28-microsoft_ie_5_5 | ONESTAT | 2004-05-28 | Microsoft IE 5.5 | 12.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-05-28-microsoft_ie_6_0 | ONESTAT | 2004-05-28 | Microsoft IE 6.0 | 69.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-05-28-mozilla | ONESTAT | 2004-05-28 | Mozilla | 2.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-05-28-opera_7_0 | ONESTAT | 2004-05-28 | Opera 7.0 | 1.02 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2004-05-28-safari | ONESTAT | 2004-05-28 | Safari | 0.71 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-24-microsoft_ie_4_0 | ONESTAT | 2002-06-24 | Microsoft IE 4.0 | 1.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-24-microsoft_ie_5_0 | ONESTAT | 2002-06-24 | Microsoft IE 5.0 | 23.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-24-microsoft_ie_5_5 | ONESTAT | 2002-06-24 | Microsoft IE 5.5 | 23.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-24-microsoft_ie_6_0 | ONESTAT | 2002-06-24 | Microsoft IE 6.0 | 46.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-24-netscape_navigator_3_0 | ONESTAT | 2002-06-24 | Netscape Navigator 3.0 | 0.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-24-netscape_navigator_4_0 | ONESTAT | 2002-06-24 | Netscape Navigator 4.0 | 1.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2002-06-24-opera_6_0 | ONESTAT | 2002-06-24 | Opera 6.0 | 0.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-02-apple_safari | ONESTAT | 2005-11-02 | Apple Safari | 1.75 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-02-microsoft_ie | ONESTAT | 2005-11-02 | Microsoft IE | 85.45 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-02-mozilla_firefox | ONESTAT | 2005-11-02 | Mozilla Firefox | 11.51 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-02-netscape | ONESTAT | 2005-11-02 | Netscape | 0.26 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| ONESTAT-2005-11-02-opera | ONESTAT | 2005-11-02 | Opera | 0.77 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
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
| W3COUNTER-2007-05-31-aol | W3COUNTER | 2007-05-31 | AOL | 1.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-05-31-firefox | W3COUNTER | 2007-05-31 | Firefox | 24.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-05-31-internet_explorer | W3COUNTER | 2007-05-31 | Internet Explorer | 67.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-05-31-opera | W3COUNTER | 2007-05-31 | Opera | 1.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-05-31-safari | W3COUNTER | 2007-05-31 | Safari | 2.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-06-30-aol | W3COUNTER | 2007-06-30 | AOL | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-06-30-firefox | W3COUNTER | 2007-06-30 | Firefox | 25.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-06-30-internet_explorer | W3COUNTER | 2007-06-30 | Internet Explorer | 66.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-06-30-opera | W3COUNTER | 2007-06-30 | Opera | 1.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-06-30-safari | W3COUNTER | 2007-06-30 | Safari | 2.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-07-31-aol | W3COUNTER | 2007-07-31 | AOL | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-07-31-firefox | W3COUNTER | 2007-07-31 | Firefox | 25.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-07-31-internet_explorer | W3COUNTER | 2007-07-31 | Internet Explorer | 66.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-07-31-opera | W3COUNTER | 2007-07-31 | Opera | 1.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-07-31-safari | W3COUNTER | 2007-07-31 | Safari | 2.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-08-31-aol | W3COUNTER | 2007-08-31 | AOL | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-08-31-firefox | W3COUNTER | 2007-08-31 | Firefox | 25.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-08-31-internet_explorer | W3COUNTER | 2007-08-31 | Internet Explorer | 66.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-08-31-opera | W3COUNTER | 2007-08-31 | Opera | 1.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-08-31-safari | W3COUNTER | 2007-08-31 | Safari | 2.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-09-30-aol | W3COUNTER | 2007-09-30 | AOL | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-09-30-firefox | W3COUNTER | 2007-09-30 | Firefox | 25.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-09-30-internet_explorer | W3COUNTER | 2007-09-30 | Internet Explorer | 66.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-09-30-opera | W3COUNTER | 2007-09-30 | Opera | 1.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-09-30-safari | W3COUNTER | 2007-09-30 | Safari | 2.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-10-31-aol | W3COUNTER | 2007-10-31 | AOL | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-10-31-firefox | W3COUNTER | 2007-10-31 | Firefox | 26.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-10-31-internet_explorer | W3COUNTER | 2007-10-31 | Internet Explorer | 65.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-10-31-opera | W3COUNTER | 2007-10-31 | Opera | 1.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-10-31-safari | W3COUNTER | 2007-10-31 | Safari | 2.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-11-30-aol | W3COUNTER | 2007-11-30 | AOL | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-11-30-firefox | W3COUNTER | 2007-11-30 | Firefox | 27.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-11-30-internet_explorer | W3COUNTER | 2007-11-30 | Internet Explorer | 63.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-11-30-opera | W3COUNTER | 2007-11-30 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-11-30-safari | W3COUNTER | 2007-11-30 | Safari | 2.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-12-31-aol | W3COUNTER | 2007-12-31 | AOL | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-12-31-firefox | W3COUNTER | 2007-12-31 | Firefox | 28.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-12-31-internet_explorer | W3COUNTER | 2007-12-31 | Internet Explorer | 62.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-12-31-opera | W3COUNTER | 2007-12-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2007-12-31-safari | W3COUNTER | 2007-12-31 | Safari | 2.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-01-31-aol | W3COUNTER | 2008-01-31 | AOL | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-01-31-firefox | W3COUNTER | 2008-01-31 | Firefox | 28.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-01-31-internet_explorer | W3COUNTER | 2008-01-31 | Internet Explorer | 62.2 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-01-31-opera | W3COUNTER | 2008-01-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-01-31-safari | W3COUNTER | 2008-01-31 | Safari | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-02-29-firefox | W3COUNTER | 2008-02-29 | Firefox | 28.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-02-29-internet_explorer | W3COUNTER | 2008-02-29 | Internet Explorer | 62.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-02-29-mozilla | W3COUNTER | 2008-02-29 | Mozilla | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-02-29-opera | W3COUNTER | 2008-02-29 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-02-29-safari | W3COUNTER | 2008-02-29 | Safari | 2.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-03-31-firefox | W3COUNTER | 2008-03-31 | Firefox | 28.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-03-31-internet_explorer | W3COUNTER | 2008-03-31 | Internet Explorer | 62.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-03-31-mozilla | W3COUNTER | 2008-03-31 | Mozilla | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-03-31-opera | W3COUNTER | 2008-03-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-03-31-safari | W3COUNTER | 2008-03-31 | Safari | 2.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-04-30-firefox | W3COUNTER | 2008-04-30 | Firefox | 28.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-04-30-internet_explorer | W3COUNTER | 2008-04-30 | Internet Explorer | 62.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-04-30-mozilla | W3COUNTER | 2008-04-30 | Mozilla | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-04-30-opera | W3COUNTER | 2008-04-30 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-04-30-safari | W3COUNTER | 2008-04-30 | Safari | 2.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-05-31-firefox | W3COUNTER | 2008-05-31 | Firefox | 28.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-05-31-internet_explorer | W3COUNTER | 2008-05-31 | Internet Explorer | 61.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-05-31-mozilla | W3COUNTER | 2008-05-31 | Mozilla | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-05-31-opera | W3COUNTER | 2008-05-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-05-31-safari | W3COUNTER | 2008-05-31 | Safari | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-06-30-firefox | W3COUNTER | 2008-06-30 | Firefox | 29.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-06-30-internet_explorer | W3COUNTER | 2008-06-30 | Internet Explorer | 61.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-06-30-mozilla | W3COUNTER | 2008-06-30 | Mozilla | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-06-30-opera | W3COUNTER | 2008-06-30 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-06-30-safari | W3COUNTER | 2008-06-30 | Safari | 2.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-07-31-firefox | W3COUNTER | 2008-07-31 | Firefox | 29.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-07-31-internet_explorer | W3COUNTER | 2008-07-31 | Internet Explorer | 60.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-07-31-mozilla | W3COUNTER | 2008-07-31 | Mozilla | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-07-31-opera | W3COUNTER | 2008-07-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-07-31-safari | W3COUNTER | 2008-07-31 | Safari | 2.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-08-31-firefox | W3COUNTER | 2008-08-31 | Firefox | 31.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-08-31-internet_explorer | W3COUNTER | 2008-08-31 | Internet Explorer | 58.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-08-31-mozilla | W3COUNTER | 2008-08-31 | Mozilla | 0.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-08-31-opera | W3COUNTER | 2008-08-31 | Opera | 2.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-08-31-safari | W3COUNTER | 2008-08-31 | Safari | 2.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-09-30-firefox | W3COUNTER | 2008-09-30 | Firefox | 32.5 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-09-30-internet_explorer | W3COUNTER | 2008-09-30 | Internet Explorer | 57.3 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-09-30-mozilla | W3COUNTER | 2008-09-30 | Mozilla | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-09-30-opera | W3COUNTER | 2008-09-30 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-09-30-safari | W3COUNTER | 2008-09-30 | Safari | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-10-31-firefox | W3COUNTER | 2008-10-31 | Firefox | 30.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-10-31-internet_explorer | W3COUNTER | 2008-10-31 | Internet Explorer | 59.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-10-31-mozilla | W3COUNTER | 2008-10-31 | Mozilla | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-10-31-opera | W3COUNTER | 2008-10-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-10-31-safari | W3COUNTER | 2008-10-31 | Safari | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-11-30-firefox | W3COUNTER | 2008-11-30 | Firefox | 30.8 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-11-30-internet_explorer | W3COUNTER | 2008-11-30 | Internet Explorer | 59.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-11-30-mozilla | W3COUNTER | 2008-11-30 | Mozilla | 1.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-11-30-opera | W3COUNTER | 2008-11-30 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-11-30-safari | W3COUNTER | 2008-11-30 | Safari | 3.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-12-31-firefox | W3COUNTER | 2008-12-31 | Firefox | 31.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-12-31-internet_explorer | W3COUNTER | 2008-12-31 | Internet Explorer | 58.6 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-12-31-mozilla | W3COUNTER | 2008-12-31 | Mozilla | 1.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-12-31-opera | W3COUNTER | 2008-12-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2008-12-31-safari | W3COUNTER | 2008-12-31 | Safari | 2.9 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2009-01-31-firefox | W3COUNTER | 2009-01-31 | Firefox | 31.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2009-01-31-internet_explorer | W3COUNTER | 2009-01-31 | Internet Explorer | 58.4 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2009-01-31-mozilla | W3COUNTER | 2009-01-31 | Mozilla | 1.1 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2009-01-31-opera | W3COUNTER | 2009-01-31 | Opera | 2.0 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
| W3COUNTER-2009-01-31-safari | W3COUNTER | 2009-01-31 | Safari | 2.7 | UNVERIFIED | UNVERIFIED: the web archive refused the GitHub runner (HTTP 429), not yet seen at source; listed for Cowork to check in Luke's Chrome |
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

## Questions for Luke
(draft)
