# RTT-104 V3 — YouTube times (IQ-24g, 17 Oct 2026): "Women in Parliament: The Top 20 (1997–2025)"

For the film rendered from `kits/rtt-104/config_rtt104_v3_film.json` (private pre-release in DEC-703). **Not approved yet:** these times hold only for that exact render; Luke approves the master by its SHA-256 (DEC-078). V2's `youtube_times.md` is unchanged and still describes the approved V2 film.

**Running time: 2:54.5** (5,235 frames at 30 fps): 1.5 s on 1997, 28 years at 6 s each, then the 5 s final table (2025 lands at 2:49.5). No closing card (DEC-701).

## Chapters (proposal for Luke; YouTube needs the first at 0:00, at least three, each at least 10 s; the shortest here is the last, 11 s)
```
0:00 1997: Sweden leads
0:31 2003: Rwanda takes first place
1:37 2014: Bolivia jumps to second (53.1%)
2:07 2019: the UAE jumps to 50%
2:43 2025: the final top 20
```
Each chapter starts as the bars begin moving into that year; the year lands 6 s later (2003 at 0:37.5, 2014 at 1:43.5, 2019 at 2:13.5, 2025 at 2:49.5). Checked against the film's own timeline and `race_rtt104_v3.json`: 2003 Rwanda 1st (48.8%); 2014 Bolivia 2nd (53.1%); 2019 UAE 4th (50.0%, tag "Election · Oct 2019").

## End screen
The last 5 s, **2:49.5–2:54.5**, over the final table (as V2, DEC-648/DEC-659).

## Final table, 2025 (lands 2:49.5; values re-read from `kits/rtt-104/race_rtt104_v3.json`, built from `data/rtt-104/series.csv`; ranks 1–10 = `boards.csv`)
1 Rwanda 63.8% · 2 Cuba 55.7% · 3 Nicaragua 54.9% · 4 Bolivia 50.8% · 5 Mexico 50.2% · 6 United Arab Emirates 50.0% · 7 Costa Rica 49.1% · 8 Australia 46.0% · 9 New Zealand 45.5% · 10 Finland 45.5% · 11 Ecuador 45.0% · 12 Sweden 45.0% · 13 South Africa 44.9% · 14 Spain 44.3% · 15 Denmark 43.6% · 16 Netherlands 43.3% · 17 Ethiopia 41.9% · 18 Peru 41.5% · 19 Belgium 41.3% · 20 Argentina 41.2%

World average (all countries): 27.2% (`data/rtt-104/world.csv`).

## Description lines (additions to V2's `description_credits.md`)
- Data: Inter-Parliamentary Union (IPU), via World Bank World Development Indicators (CC BY 4.0) — as V2.
- Election dates: IPU Parline (data.ipu.org) (DEC-666).
- Continents: UN M49 regions (UN Statistics Division) (DEC-687; optional, the legend already names it).
- Music: "No.10 A New Beginning" by Esther Abrami (YouTube Audio Library) — as V2, looped once (DEC-699).
