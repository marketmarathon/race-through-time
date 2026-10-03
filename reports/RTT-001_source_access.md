# RTT-001 Browser Wars — source access test (IQ-12, 3 Oct 2026)

One request to each source site, first from this Claude Code cloud container, then from a GitHub-hosted runner (`.github/workflows/rtt001_sources.yml`, `scripts/rtt001_check_sources.py`; no secret, no artifact, no cache — the same pattern as `rtt003_sources.yml`, DEC-136).

| Site | From the container (12:07 UTC) | From a GitHub runner (runs 1–2, 12:12 and 13:00 UTC) |
|---|---|---|
| gs.statcounter.com | blocked (proxy 403 to CONNECT) | HTTP 200 |
| web.archive.org | blocked (connection reset by the proxy) | HTTP 200 for the home page, then **HTTP 429 "too many requests" and refused connections** for most archived pages (see below) |
| sites.cc.gatech.edu (GVU) | blocked (proxy 403) | HTTP 200 (the GVU survey pages are still live) |
| www.justice.gov | blocked (proxy 403) | HTTP 200 |
| w3counter.com | blocked (proxy 403) | HTTP 200 |
| onestat.com | blocked (proxy 403) | **timed out** (twice); the site appears to be gone |

Claude Code's own web-fetch tool also refused web.archive.org ("unable to fetch").

## What the runner could and could not fetch

- **Run 1** (run https://github.com/marketmarathon/race-through-time/actions/runs/37122102266, one job, about 140 pages at 2 s spacing): StatCounter export, every GVU page, 7 EWS monthly pages, then the web archive started answering HTTP 429 and refusing connections; the job hit its 45-minute limit.
- **Run 2** (https://github.com/marketmarathon/race-through-time/actions/runs/37124724022, 13 parallel jobs, about ten archive pages each at 12 s spacing with 60/120/180 s back-off): non-archive pages all fetched (StatCounter again, same SHA-256; StatCounter FAQ; W3Counter live; Ars Technica; justice.gov); the web archive answered HTTP 429 to almost every request, about one archived page per job got through in 40 minutes.
- **Run 3** (one slow job, one archive request every 150 s, hand-over pages first): see `state/HANDOVER.md` and `data/rtt-001/README.md` for its result.

**Rule followed:** a figure whose archived page could not be fetched is **UNVERIFIED (source blocked)**, is not used, and is listed for Claude in Cowork to check in Luke's Chrome (CLAUDE.md evidence rules).

## Pages fetched and hashed (raw response, SHA-256)

| Page | SHA-256 | Used for |
|---|---|---|
| StatCounter export, worldwide, all platforms, monthly 2009-01 to 2026-09 | `f595b08621cdd8029e0071597780ab00ac72e45c67bad7b926c4fe2ce925dc7e` (37,466 bytes, identical in runs 1 and 2) | era 5 (committed as `data/rtt-001/source/statcounter_browser_ww_all_monthly_200901-202609.csv`) |
| StatCounter FAQ https://gs.statcounter.com/faq | `11e4393b2b188bc6d1704e28fc8a2c10e6ac9eaf177c02fa2f29b964f8fa59eb` | licence and measure (page views) |
| GVU 1st survey paper https://sites.cc.gatech.edu/gvu/user_surveys/survey-01-1994/survey-paper.html | `5f4066b8d438678e4e592aa2b7161085aecf67be86c2b16b6b37e8f75a9b92c5` | January 1994 browser table |
| GVU 2nd survey index https://sites.cc.gatech.edu/gvu/user_surveys/survey-09-1994/ | `b6d577405c500231cfba6bba83bef60a553fe6d50dbbda3a13b3fa9b44333c94` | survey dates 10 Oct – 16 Nov 1994 |
| GVU 2nd survey copyright page …/survey-09-1994/copyright.html | `62c8001866decd2954d299d5111df06fbfa88650f11ef5fffa0c13f69ffa0b00` | terms |
| GVU 3rd survey (Apr 1995) graph index …/survey-04-1995/graphs/ | `109c27683a4c5b2609a01b23abe6a5ff58a211fd6ba131756f78d26fded36970` | shows no browser-type chart (only frequency, hours and use of browser) |
| GVU 4th survey (Oct 1995) graph index …/survey-10-1995/graphs/ | `9f97b5013a1af492153ceda5787390b3a58788ba3f1b7b605b4b2b5fdecc6888` | likewise no browser-type chart |
| EWS monthly reports May 1996, Jul 1996, Dec 1996, May 1997, Jul 1997, Dec 1997, Nov 1998, Jan 1999 (web.archive.org raw captures) | listed per figure in `data/rtt-001/observations.csv` (`page_sha256`) | era 2 |
| W3Counter live page for December 2008 https://www.w3counter.com/globalstats.php?year=2008&month=12 | `a4e0c0d8c448c9e2ff838b145df8264a0187fa120e06a22cb21119a0e9c4281d` | finding: today's page relabels old Internet Explorer versions as "Edge 6" and "Edge 7"; the 2010 archived copies are the contemporary record |
| justice.gov, Declaration of David Sibley | `92a00b49cc4ec1b9e3ecd0bab12b02a1987787e010081c710167cc103dcd6c3d` | the Zona table did not come through as text; not used |
