# RTT-104 Women in Parliament — times for YouTube (V2, IQ-22d)

**V2 film** (`config_rtt104_film_v2.json`: the approved look with smooth motion at 3 s per year, DEC-653..DEC-655): **3,111 frames at 30 fps = 1:43.7**. Rendered master and its SHA-256: see the private pre-release named in `state/HANDOVER.md` (the workflow checks the rendered files have exactly these 3,111 frames). Times come from the player's own plan (`planSummary()` in `player_rtt104.html`, deterministic). In V2 the bars glide through each year without stopping; a year's figures **land** at the time shown (the board then equals `data/rtt-104/boards.csv` exactly), and its year label rolls in during the 0.5 s before. V1's times (2 s per year, 1:15.7) are in git history.

## Chapter-worthy moments
| Time | Moment (as the board shows it) |
|---|---|
| 0:00.0 | 1997: Sweden leads (40.4%) |
| 0:04.5 – 0:06.3 | Pakistan's note on the bottom board: "No figure 1999–2001" (the board pauses 1.8 s), then it leaves |
| 0:18.3 → 0:21.3 | **Rwanda glides from below the top board to first place; 2003 lands at 0:21.3 (48.8%)**; it leads to the end |
| 0:48.3 – 0:50.1 | Egypt's note: "No figure 2013–2015" (pause 1.8 s), then it leaves |
| 0:53.1 | 2013 lands: Rwanda 63.8%; Saudi Arabia leaves the 0% group (19.9%, not on a board) |
| 0:53.1 → 0:56.1 | **Bolivia glides onto the top board; 2014 lands at 0:56.1 in second place (53.1%)** |
| 1:08.1 → 1:11.1 | **The UAE rises to 50.0%; 2019 lands at 1:11.1** (4th) |
| 1:11.1 – 1:12.9 | **Haiti's note: "No sitting parliament: deputies' terms expired Jan 2020"** (pause 1.8 s), then it greys and shrinks away |
| 1:15.9 → 1:18.9 | **Japan glides into the bottom ten; 2021 lands at 1:18.9** (10th, 9.7%); 2022 10th (9.9%); 2023 8th (10.3%, lands 1:24.9); out in 2024 |
| 1:24.9 – 1:26.7 | **Kuwait's note: "No sitting parliament: dissolved by the Emir, May 2024"** (pause 1.8 s), then it leaves |
| 1:32.7 | **2025 lands: the final table** (holds 1:32.7 – 1:37.7) |
| 1:37.7 – 1:43.7 | Closing card "Not included: no sitting parliament" |
| 1:38.7 – 1:43.7 | Music fades out (last 5 s, DEC-651); the music starts 0.705 s into the track |

## Chapters (proposal; YouTube needs the first at 0:00, at least three, each at least 10 s long)
```
0:00 1997: Sweden leads
0:18 2003: Rwanda takes first place
0:53 2014: Bolivia jumps to 53.1%
1:08 2019–2024: the UAE at 50%, Japan in the bottom ten, Haiti and Kuwait leave
1:32 2025: the final table and who is not included
```

## Final table, 2025 (for the description; unchanged from V1)
**Highest:** 1 Rwanda 63.8% · 2 Cuba 55.7% · 3 Nicaragua 54.9% · 4 Bolivia 50.8% · 5 Mexico 50.2% · 6 United Arab Emirates 50.0% · 7 Costa Rica 49.1% · 8 Australia 46.0% · 9 New Zealand 45.5% · 10 Finland 45.5%
**Lowest above 0%:** 1 Papua New Guinea 2.7% · 2 Nigeria 4.2% · 3 Iran 4.9% · 4 Syria 4.9% · 5 Lebanon 6.3% · 6 Algeria 7.9% · 7 Sri Lanka 9.8% · 8 Liberia 11.0% · 9 Central African Republic 11.4% · 10 DR Congo 12.8%
**No women in parliament (0%):** Oman, Yemen
**World average (all countries):** 27.2%
New Zealand and Finland are both 45.5% to one decimal; full precision puts New Zealand ahead. Iran and Syria are both 4.9% to one decimal; full precision puts Iran lower.

## End screen (open question for Luke, DEC-648)
The last 6 s (1:37.7–1:43.7) are the closing card: its six lines fill the top two-thirds and reach about x 1400 of 1920. Proposal: end screen over those 6 s, its elements in the empty right third and bottom band so no line is covered.

## Description lines
See `kits/rtt-104/description_credits.md`.
