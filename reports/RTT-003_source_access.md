# RTT-003 source access test — 1 Oct 2026

Run by Claude Code (cloud session, environment "Race Through Time") before the RTT-003 data build (IQ-09), 1 Oct 2026, 17:45–17:50 UTC. One `curl` request per host to `https://<host>/` through the environment's proxy (browser-like user agent), then the redirect followed once. Where curl failed, one retry through the WebFetch tool, which uses a different network route. A "BLOCKED" verdict means figures whose only source is on that host are marked **UNVERIFIED (source blocked)** in `data/rtt-003/observations.csv` and listed for Luke to check in his Chrome.

| Host | curl (first request) | After redirect / retry | WebFetch | Verdict |
|---|---|---|---|---|
| nintendo.co.jp | 301 | 200 (www.nintendo.com/jp/) | – | OPEN (IR pages and the historical-data spreadsheet download) |
| nintendo.com | 301 | 200 (/us/) | – | OPEN |
| sonyinteractive.com | 301 | 200 (/en/) | – | OPEN (business data page and press-release PDFs) |
| sony.com | 301 | 403 "Access Denied" (www.sony.com, Akamai) | "unable to fetch" | BLOCKED |
| sony.net | 301 → www.sony.co.jp | proxy refuses CONNECT (403) | EGRESS_BLOCKED (www.sony.co.jp) | BLOCKED |
| playstation.com | 301 | 200 (/en-us/) | – | OPEN |
| sec.gov | 403 (requires a declared contact in the user agent) | not retried with contact details (no personal data is sent) | 200 (home page) | OPEN via WebFetch only |
| microsoft.com | 301 | 200 | – | OPEN |
| news.microsoft.com | 301 | 200 (/source/) | – | OPEN |
| news.xbox.com | 302 | 200 (/en-us/) | – | OPEN |
| blogs.microsoft.com | 200 | – | – | OPEN |
| segasammy.co.jp | proxy CONNECT 502 | – | 200 | OPEN via WebFetch only |
| sega.jp | 301 | 403 (Cloudflare challenge) | 403 | BLOCKED |
| segaretro.org | 200 | – | – | OPEN |
| archive.org | 200 | – | – | OPEN (item pages, downloads, metadata API) |
| web.archive.org | connection reset after 8 s | reset again; `http://` 403 | "unable to fetch" | BLOCKED (Wayback Machine unreachable) |
| segaxtreme.net | 200 | – | – | OPEN |
| files.virtual-boy.com | 403 | 403 | 403 | BLOCKED |
| atarimania.com | TLS connect failed | – | 200 | OPEN via WebFetch only |
| ataricompendium.com | 200 | – | – | OPEN |
| ampereanalysis.com | 200 | – | – | OPEN |
| gamedeveloper.com | 301 | 200 | – | OPEN |
| videogameschronicle.com | 301 | 200 | – | OPEN |
| gamespot.com | 301 | 403 (Cloudflare challenge) | 403 | BLOCKED |
| law.justia.com | 403 | 403 | 403 | BLOCKED |
| archive.computerhistory.org | 404 (site root) | 404 | 404 | NOT CHECKED BY HOST TEST (root has no page; individual document URLs tested during verification) |
| cgwmuseum.org | 200 | – | – | OPEN |

## Consequences for the build
- **Old Sony Computer Entertainment data pages** (`scei.co.jp/corporate/data/bizdata*_e.html`: PlayStation, PS2, PSP and PS3 cumulative production shipments by quarter) exist only in the Wayback Machine, which is blocked. Their figures are kept only where needed for the curve and marked UNVERIFIED (source blocked).
- **Sony IR documents on sony.com / sony.net** (20-F filings mirrored there, earnings supplements, the 2019 Corporate Report) are blocked. Sony's current business-data page on sonyinteractive.com is open and gives the PS4 and PS5 quarterly sell-in tables and the lifetime totals.
- **Nintendo Online Magazine** (the Game Boy series 1989–1997) is removed from nintendo.co.jp (404) and only in the Wayback Machine: UNVERIFIED (source blocked); used only as a cross-check.
- **Sega's history pages on sega.jp** (Master System "about 19 million", Game Gear "10 million") are blocked.
- **The Famitsu page of 20 May 1997 on files.virtual-boy.com** (cumulative shipments at 31 Mar 1996) is blocked.

The per-figure outcome is in the `verified` column of `data/rtt-003/observations.csv`; the list for Luke is in `reports/RTT-003_data_report.md` ("UNVERIFIED items").
