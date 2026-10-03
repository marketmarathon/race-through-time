# RTT-001 — Browser Wars (share of web browsing by browser, January 1994 – September 2026, all devices)

Status: **DATA BUILD (IQ-12), 3 Oct 2026 — pull request open, not merged** (DEC-057). Nothing rendered; no player or visual change (DEC-069).
Contract: `reference/metric_contract_RTT-001.md` v1.0. Owner decisions DEC-144, DEC-152 to DEC-154; Claude's working choices DEC-155 to DEC-159 (open questions for Luke); findings DEC-160 onward.
Report for Luke: `reports/RTT-001_data_report.md`. Source access test: `reports/RTT-001_source_access.md`.

**Race:** month ends from 31 Jan 1994 to 30 Sep 2026 (393 month ends). **One source per period** (DEC-152): GVU surveys 1994 → Illinois EWS server 1996–2000 → StatMarket, then OneStat 2001 – Apr 2007 → W3Counter May 2007 – Dec 2008 → StatCounter from Jan 2009. Straight lines between dated figures, including across each hand-over (DEC-153). Everything before January 2009 is estimated (`series.csv` `estimated = yes`).

## Files

| File | What it is |
|---|---|
| `browsers.csv` | One row per browser family: display name, maker, the StatCounter labels it covers, the family rule, `colour_key` and `logo_ref` (both **empty** until the player session), first and last point, best rank |
| `observations.csv` | Every figure used or considered: date and how it was dated, the label as published, browser family, value as published (text), measure, geography, source, URL, page SHA-256, a short quote or table cell (under 25 words), `verified` (yes / UNVERIFIED), who verified it, `used` (yes / no) and why, the parts of an arithmetic row, the hand-over it is a cross-check for |
| `series.csv` | One row per browser per month end: `share`, `provenance` (observed / arithmetic / interpolated / not_found), `estimated`, `era`, `source_id`, `source_line` (the on-screen source line), `handover`, and the two points it rests on |
| `leaders.csv` | Every change of first place, with what it rests on |
| `CHECKS.md`, `checks.json` | Scripted checks |
| `manifest.json` | SHA-256 of every input and output |
| `source/statcounter_browser_ww_all_monthly_200901-202609.csv` | StatCounter's raw export, byte for byte (CC BY-SA 3.0; URL, date and hash in `statcounter.source.txt`) |
| `source/browsers_curated.csv` | Hand-made browser list (input) |
| `source/observations_curated.csv` | Pre-2009 figures (input): verified ones transcribed from the `rtt001-sources` runner logs or from Claude in Cowork's checks; research leads listed as UNVERIFIED with numbers and labels only |
| `source/report_notes.md` | Hand-written parts of the report (summary, questions for Luke) |

## How to rebuild

```
python scripts/build_rtt001_dataset.py data/rtt-001 reports/RTT-001_data_report.md
```
Standard library only; the same `source/` files always give byte-identical outputs (hashes in `manifest.json`).

## Rules in one paragraph
A bar uses a dated, VERIFIED figure where one exists; between two dated figures of the same browser it follows a straight line by calendar days, also across a change of source. A browser the source does not report at a date has no value on either side of it (no bar); nothing is held flat, carried across from another source, averaged or invented. UNVERIFIED and NOT FOUND figures are listed, never used. StatCounter values equal the raw export. "Other" is never a bar.

## Rights
StatCounter data is CC BY-SA 3.0: credit "StatCounter Global Stats" with a link. GVU's terms ask for acknowledgement of Georgia Tech Research Corporation and include a restriction listed for Luke (`reference/rights_ledger.md`). No images, logos or research-assistant text are committed (DEC-006); the private research leads (`race-through-time-private/research/rtt-001-chatgpt/`) are used only to find sources, and only their numbers and labels appear here, marked UNVERIFIED until seen at source.
