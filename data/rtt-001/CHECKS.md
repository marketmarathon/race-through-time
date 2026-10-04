# RTT-001 scripted checks

Build `rtt001-build/1.1`. All checks PASS: **True**. A check marked REVIEW found something that is reported in full below, not hidden or fixed.

| Check | Result | Detail |
|---|---|---|
| values_within_0_100 | PASS | 6015 values; outside: 0 |
| source_date_totals_at_most_100 | PASS | 312 source dates; max total 99.97; breaches beyond the source's rounding: 0 |
| every_point_has_provenance | PASS | 6015 values checked; missing: 0 |
| one_source_per_date | PASS | 312 source dates; dates with two sources: {} |
| eras_do_not_overlap | PASS | GVU 1994-01-31..1994-11-16; EWS 1996-04-30..2000-12-31; STATMARKET 2001-02-21..2002-08-26; ONESTAT 2002-09-30..2007-01-31; W3COUNTER 2007-05-31..2008-12-31; STATCOUNTER 2009-01-31..2026-09-30; overlaps: []; points outside their era window: [] |
| statcounter_equals_raw_csv | PASS | 5420 StatCounter values compared with the raw export (213 months, 42 columns); mismatches: [] |
| no_unverified_or_not_found_used | PASS | 5743 used figures; used but not VERIFIED: [] |
| nothing_before_first_or_after_last_source_date | PASS | 45 browsers with points; values outside their first..last point: []; points without a browser row: [] |
| month_grid_complete | PASS | 393 month ends 1994-01-31..2026-09-30 x 45 browsers = 17685 rows |
| arithmetic_rows_equal_their_parts | PASS | 136 arithmetic rows; problems: [] |
| other_is_never_a_bar | PASS | 'Other'/'unknown' rows in series: 0 |

## Source dates whose shown browsers total more than 100 (beyond the source's own rounding)

- none

## Era spans (first and last point of each source)

- GVU: 1994-01-31 to 1994-11-16
- EWS: 1996-04-30 to 2000-12-31
- STATMARKET: 2001-02-21 to 2002-08-26
- ONESTAT: 2002-09-30 to 2007-01-31
- W3COUNTER: 2007-05-31 to 2008-12-31
- STATCOUNTER: 2009-01-31 to 2026-09-30
