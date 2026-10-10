# RTT-103 — chapter times and on-screen values for the YouTube description (IQ-18g)

Film: the APPROVED master `rtt103_film_265e6fd_3840x2160.mp4` (DEC-383), 5,940 frames at 30 fps = 198.000 s (3:18), from commit `265e6fd`. Every time below comes from that commit's frame plan (`kits/rtt-103/config_rtt103_film.json`, `rtt_timeline.js` with no code change since): the film time of the first frame on which the item appears, **rounded down to the second** (frame ÷ 30). The leader changes and the values were read from the player itself, drawing every frame of the race in order (9 Oct 2026; placeholder logos only, which change no text or timing).

## Chapters
| Time | What first appears | Frame |
|---|---|---|
| 0:00 | First quarter: 12 months to March 2010 (the opening board) | 0 |
| 0:00 | 2010 | 0 |
| 0:07 | 2011 | 213 |
| 0:13 | 2012 | 411 |
| 0:20 | 2013 | 627 |
| 0:28 | 2014 | 843 |
| 0:36 | 2015 | 1095 |
| 0:44 | 2016 | 1329 |
| 0:51 | 2017 | 1545 |
| 0:58 | 2018 | 1761 |
| 1:06 | 2019 | 1995 |
| 1:13 | 2020 | 2211 |
| 1:21 | 2021 | 2445 |
| 1:26 | 2022 | 2607 |
| 1:34 | 2023 | 2832 |
| 1:42 | 2024 | 3066 |
| 1:50 | 2025 | 3300 |
| 1:56 | 2026 (12 months to March 2026; June 2026 is the last real quarter, at 1:58, frame 3561) | 3498 |
| 2:00 | 2026 plans board ("company plans 2026") | 3606 |
| 2:11 | 2027 (estimates) | 3930 |
| 2:17 | 2028 | 4110 |
| 2:23 | 2029 | 4290 |
| 2:29 | 2030 ("least reliable year"; held from 2:35 to 2:38) | 4470 |
| 2:38 | Explanation page ("About the estimates") | 4740 |
| 2:54 | Combined line, 2010–2030 | 5220 |
| 3:00 | Peak timeline ("When does it peak?") | 5400 |
| 3:08 | Final June 2026 table (to the end, 3:18) | 5640 |

## Changes of leader (the crown), as drawn
Each is the first frame on which the new leader is first on the board; the values are the two on-screen labels on that frame (still counting towards the quarter's figures), and the date block's quarter.
| Time | Change | On screen at that moment | Date block | Frame |
|---|---|---|---|---|
| 0:00 | Microsoft leads at the start | Microsoft $2.1bn | 12 months to Mar 2010 | 0 |
| 0:05 | Alphabet (Google) passes Microsoft | Alphabet $2.1bn, Microsoft $2.1bn | 12 months to Dec 2010 | 162 |
| 0:20 | Amazon passes Alphabet | Amazon $3.3bn, Alphabet $3.2bn | 12 months to Dec 2012 | 604 |
| 0:23 | Alphabet passes Amazon again | Alphabet $4.1bn, Amazon $4.1bn | 12 months to Jun 2013 | 692 |
| 1:19 | Amazon passes Alphabet | Amazon $23.4bn, Alphabet $23.3bn | 12 months to Sep 2020 | 2376 |
| 2:12 | Alphabet passes Amazon (on our estimates, ranked by the top of its range) | Alphabet ~$226–237bn, Amazon ~$237bn | estimate 2027 | 3985 |

Amazon leads the real race from 1:19 to its end (June 2026) and on the 2026 plans board; Alphabet leads every estimate year, 2027–2030.

## Final June 2026 table (3:08 to the end), exactly as displayed
Title line: "Combined: $625.5bn in the 12 months to June 2026, up from $347.4bn a year earlier"; date block "12 months to Jun 2026".
1. Amazon $169.0bn (crown)
2. Alphabet (Google) $132.4bn
3. Microsoft $115.9bn
4. Meta (Facebook) $89.3bn
5. Oracle $55.7bn
6. Alibaba $22.3bn
7. CoreWeave $20.6bn
8. Tencent $17.0bn · includes some intangibles
9. Baidu $3.3bn

Combined capital spending panel: $625.5bn, "sum of 9 companies".

## 2030 board (2:35–2:38, landed and held), exactly as displayed
Date block "estimate 2030"; line under the title "Race Through Time estimates · growth: FactSet consensus · 2030: least reliable year".
1. Alphabet (Google) ~$360–378bn (crown)
2. Microsoft ~$346bn
3. Amazon ~$316bn
4. Meta (Facebook) ~$225–250bn
5. Oracle ~$83–88bn
6. CoreWeave ~$58–64bn
7. Alibaba ~$47bn
8. Tencent ~$28bn · includes some intangibles
9. Baidu ~$5.4bn

Combined capital spending panel: ~$1.47–1.52tn, "sum of the 9 bars". All 2030 bars are striped (Race Through Time estimates).
