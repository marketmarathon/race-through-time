# RTT-104 Women in Parliament — times for YouTube (IQ-22c)

From the approved film config `config_rtt104_film.json` (2 s per year, 1.7 s move + 0.3 s hold; DEC-634..DEC-644): **2,271 frames at 30 fps = 1:15.7**. Worked out from the player's own plan (`planSummary()` in `player_rtt104.html`, deterministic); the film workflow checks that the rendered files have exactly these 2,271 frames. A year's label changes when its move starts; its figures land 1.7 s later. Values are `data/rtt-104/boards.csv`.

## Chapter-worthy moments
| Time (label changes / figures land) | Moment (as the board shows it) |
|---|---|
| 0:00.0 | 1997: Sweden leads (40.4%) |
| 0:03.5 – 0:05.3 | Pakistan leaves the bottom board: "No figure 1999–2001" |
| 0:13.3 / 0:15.0 | **2003: Rwanda takes first place (48.8%)** and leads to the end |
| 0:33.3 – 0:35.1 | Egypt leaves the bottom board: "No figure 2013–2015" |
| 0:35.1 / 0:36.8 | 2013: Rwanda 63.8%; Saudi Arabia leaves the 0% group (19.9%, not on a board) |
| 0:37.1 / 0:38.8 | **2014: Bolivia jumps onto the top board in second place (53.1%)** |
| 0:47.1 / 0:48.8 | **2019: the United Arab Emirates reach 50.0%** (4th) |
| 0:49.1 – 0:50.9 | **Haiti leaves the bottom board: "No sitting parliament: deputies' terms expired Jan 2020"** |
| 0:52.9 / 0:54.6 | **2021: Japan enters the bottom ten** (10th, 9.7%); 2022 10th (9.9%); 2023 8th (10.3%); out in 2024 |
| 0:58.9 – 1:00.7 | **Kuwait leaves the bottom board: "No sitting parliament: dissolved by the Emir, May 2024"** |
| 1:02.7 / 1:04.4 | **2025: the final table** (holds 1:04.4 – 1:09.7) |
| 1:09.7 – 1:15.7 | Closing card "Not included: no sitting parliament" |
| 1:10.7 – 1:15.7 | Music fades out (last 5 s, DEC-651) |

## Chapters (proposal; YouTube needs the first at 0:00, at least three, each at least 10 s long)
```
0:00 1997: Sweden leads
0:13 2003: Rwanda takes first place
0:37 2014: Bolivia jumps to 53.1%
0:47 2019–2024: the UAE at 50%, Japan in the bottom ten, Haiti and Kuwait leave
1:04 2025: the final table and who is not included
```
Haiti (0:49), Japan (0:53) and Kuwait (0:59) are too close to 0:47 and to each other for chapters of their own (10 s minimum), so they share one.

## Final table, 2025 (for the description)
**Highest:** 1 Rwanda 63.8% · 2 Cuba 55.7% · 3 Nicaragua 54.9% · 4 Bolivia 50.8% · 5 Mexico 50.2% · 6 United Arab Emirates 50.0% · 7 Costa Rica 49.1% · 8 Australia 46.0% · 9 New Zealand 45.5% · 10 Finland 45.5%
**Lowest above 0%:** 1 Papua New Guinea 2.7% · 2 Nigeria 4.2% · 3 Iran 4.9% · 4 Syria 4.9% · 5 Lebanon 6.3% · 6 Algeria 7.9% · 7 Sri Lanka 9.8% · 8 Liberia 11.0% · 9 Central African Republic 11.4% · 10 DR Congo 12.8%
**No women in parliament (0%):** Oman, Yemen
**World average (all countries):** 27.2%
New Zealand and Finland are both 45.5% to one decimal; full precision puts New Zealand ahead (`boards.csv`). Iran and Syria are both 4.9% to one decimal; full precision puts Iran lower.

## End screen (open question for Luke, DEC-648)
The last 6 s (1:09.7–1:15.7) are the closing card: its six lines fill the top two-thirds and reach about x 1400 of 1920, leaving the right third and the bottom band empty. Proposal: end screen over those 6 s, its elements in the empty areas so no line is covered.

## Description lines
See `kits/rtt-104/description_credits.md`.
