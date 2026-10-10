# RTT-104 Women in Parliament — times for YouTube (IQ-22b)

From the approved film config `config_rtt104_film.json` (2 s per year, 1.7 s move + 0.3 s hold; DEC-634..DEC-644): **2,271 frames at 30 fps = 1:15.7**. Worked out from the player's own plan (`planSummary()` in `player_rtt104.html`), not measured on a render: check against the rendered file before use. A year's label changes when its move starts; its figures land 1.7 s later.

## Key times
| Moment | Time |
|---|---|
| 1997 on screen (opening) | 0:00.0 |
| Leave note: Pakistan "No figure 1999–2001" | 0:03.5 – 0:05.3 |
| 2003: Rwanda takes first place (label changes / figures land) | 0:13.3 / 0:15.0 |
| Leave note: Egypt "No figure 2013–2015" | 0:33.3 – 0:35.1 |
| 2013: Rwanda 63.8%, Saudi Arabia leaves the 0% group (19.9%) | 0:35.1 / 0:36.8 |
| 2019: United Arab Emirates 50.0% | 0:47.1 / 0:48.8 |
| Leave note: Haiti "No sitting parliament: deputies' terms expired Jan 2020" | 0:49.1 – 0:50.9 |
| Leave note: Kuwait "No sitting parliament: dissolved by the Emir, May 2024" | 0:58.9 – 1:00.7 |
| 2025 figures land (final table begins) | 1:04.4 |
| Final table holds | 1:04.4 – 1:09.7 (5.3 s) |
| Closing card "Not included: no sitting parliament" | 1:09.7 – 1:15.7 (6 s) |
| Music fade-out (over the closing card, `music_rtt104.json` fade_sec 6) | 1:09.7 – 1:15.7 |

## Chapters (proposal for Luke; YouTube needs the first at 0:00, at least three, each at least 10 s)
```
0:00 1997: Sweden leads
0:13 2003: Rwanda takes first place
0:35 2013: Rwanda passes 60%
0:47 2019: the UAE reaches 50%
1:04 2025: the final table and who is not included
```
Each line states only what the board shows at that time (`data/rtt-104/boards.csv`, `events.csv`).

## End screen (question for Luke)
YouTube's end screen uses the last 5–20 s. Here the last 6 s are the closing card. The card's six lines run from the top to about two-thirds down (y ≤ about 760 of 1080) and reach about x 1400 at the longest (Myanmar's line); the right third above the footer and the bottom band are empty. Proposal: end screen for the last 6 s (1:09.7–1:15.7), its elements placed in the right third and the bottom band so that no line of the card is covered (Luke places them in Studio and checks).

## Description lines (approved wording, DEC-624, DEC-623)
- "Annual figures as published by the World Bank (World Development Indicators), from the IPU's monthly ranking of women in national parliaments."
- "Share of seats held by women in the lower or single house of each national parliament. Countries of 4 million people or more."
- "Data: Inter-Parliamentary Union (IPU), via World Bank World Development Indicators (CC BY 4.0). Population: World Bank WDI (CC BY 4.0). Flags: flag-icons (MIT)."
- Music credit: to be added when Luke chooses the track.
