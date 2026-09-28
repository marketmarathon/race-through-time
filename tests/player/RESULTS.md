# Player test results (IQ-05 round 2)

Written by `node tests/player/run_tests.js` (all cases). Frames are 1920x1080 (preview width), drawn headless in Playwright 1.56.1 Chromium, every race frame in order.
OCR: tesseract 5.3.4 on every value label of the first frame of every race.

Overall: 14/14 PASS.

| Case | Result | Config | Rows | Races | Frames | Race length | Value labels checked | Winner lines checked | Highlight onsets (most in 1 s) | Numbers checked on fixed-pitch digits | Beats outside holds | Boundary frames | OCR read back (skipped: overlapping rows) | Board entries | Slowest entry (frames to clearly visible) | Colour-checked frames | Name size | Pacing (rank / visible / quiet) | Adapter output SHA-256 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| enter_leave | PASS | `config.json` | 5 | 27 | 591 | 19.20 s | 2688 | off | off | 5535 | 0.40-0.70 s | 54 | 85/85 (40) | 9 | 5 | 591 | 33px | 13 / 5 / 9 | `bae1b8d036cb5835…` |
| long_names | PASS | `config.json` | 10 | 15 | 369 | 11.80 s | 885 | off | off | 2577 | 0.40-0.70 s | 30 | 28/28 (0) | 4 | 0 | 369 | 32px | 4 / 6 / 5 | `d2321b472d872afa…` |
| quiet_stretch | PASS | `config.json` | 10 | 57 | 918 | 30.10 s | 7935 | off | off | 12258 | 0.40-0.70 s | 114 | 525/525 (0) | 10 | 0 | 918 | 32px | 10 / 3 / 44 | `468a62380d522506…` |
| shared_drive | PASS | `config.json` | 10 | 5 | 240 | 7.50 s | 567 | off | off | 1774 | 0.70-0.70 s | 10 | 6/6 (6) | 3 | 0 | 240 | 32px | 5 / 0 / 0 | `5487a302f046954d…` |
| short_opening | PASS | `config.json` | 10 | 6 | 243 | 7.60 s | 531 | off | off | 1804 | 0.50-0.70 s | 12 | 12/12 (0) | 3 | 0 | 243 | 32px | 3 / 3 / 0 | `5220401ba091f4cd…` |
| three_way_tie | PASS | `config.json` | 10 | 10 | 321 | 10.20 s | 987 | off | off | 2593 | 0.50-0.70 s | 20 | 14/14 (17) | 4 | 0 | 321 | 32px | 6 / 4 / 0 | `88a3fa4b571976ee…` |
| shared_drive_winner_highlight | PASS | `config.json` | 10 | 5 | 240 | 7.50 s | 567 | 210 | 4 (2) | 1984 | 0.70-0.70 s | 10 | 6/6 (6) | 3 | 0 | 240 | 32px | 5 / 0 / 0 | `5487a302f046954d…` |
| rtt002_1984_1989 | PASS | `config.json` | 10 | 96 | 1461 | 48.20 s | 14698 | off | off | 22309 | 0.40-0.70 s | 192 | 564/564 (392) | 4 | 5 | 1461 | 32px | 14 / 16 / 66 | `ab11668e8a123f84…` |
| rtt002_2014_2021_A_top20 | PASS | `config_pilot_2014_2021_top20.json` | 20 | 160 | 2472 | 82.40 s | 49484 | off | 61 (3) | 63730 | 0.40-0.70 s | 320 | 1843/1843 (1355) | 2 | 1 | 2472 | 29px | 11 / 16 / 133 | `ab11668e8a123f84…` |
| rtt002_2014_2021_B_top10_winner | PASS | `config_pilot_2014_2021_top10_winner.json` | 10 | 160 | 2472 | 82.40 s | 24742 | 2472 | 52 (3) | 41460 | 0.40-0.70 s | 320 | 785/785 (814) | 1 | 5 | 2472 | 32px | 11 / 16 / 133 | `ab11668e8a123f84…` |
| rtt002_full_run | PASS | `config.json` | 10 | 1164 | 15747 | 524.40 s | 156008 | off | off | 239620 | 0.40-0.70 s | not saved | not run | 40 | 5 | 15747 | 32px | 136 / 140 / 888 | `ab11668e8a123f84…` |

Entry rule: a driver joining the visible board must be clearly visible (row opacity at least 0.8, name and value label drawn) within 8 frames of the first frame of that race, i.e. on frame +0 to +7. The column gives the slowest entry in the case (+N frames).
Colour rule on frames: on every frame drawn, no two bars on screen (opacity above 0) share a colour or are closer than CIEDE2000 18, and every driver is drawn in the same colour in every RTT-002 case with the same board size.
Winner highlight (where on): on the first frame of every race exactly the credited winners whose bars are on the board are lit, nothing else is ever lit, a highlight only rises from fully off on the first frame of a race that driver won (a repeat winner stays lit, so never flickers), at most 3 onsets in any second, and each fades out within highlight.sec.
Record holds (where on): the held races are exactly the BECOMES_JOINT / BECOMES_SOLE rows of data/rtt-002/record_progression.csv inside the window; on the last frame of each hold every row is within 0.1 row of its place; every other beat is within 0.8-1.4 x sec_per_event (to the nearest frame).

**record_moments_full_dataset — PASS**
- 118 record events in record_progression.csv (12 BECOMES_SOLE, 12 BECOMES_JOINT, 94 EXTENDS_SOLE); the player's 118 match row for row

**colour_rule_full_dataset — PASS** (`config.json`, 10-row board; every race of the full RTT-002 dataset, boards computed from win_credits.csv alone)
- 1164 races; 40 drivers ever reach the top 10; at most 12 can be on screen together (top 10 after a race and the 3 before it, so rows still fading out count)
- 12 colours used of a 12-colour palette; every pair that can be on screen together differs, the closest being Mike Hawthorn / Jim Clark at CIEDE2000 18.5 (rule: at least 18)
- palette: closest pair of any two palette colours CIEDE2000 18.5; weakest white-name contrast on a bar 3.22:1
- 40 drivers drawn in the RTT-002 cases run with a 10-row board; each drawn in its assigned colour in every such case

| Colour (as drawn) | Drivers, in the order they first reach the top 10 |
|---|---|
| `#2e86de` | Giuseppe Farina, Jacky Ickx, Mario Andretti, Nelson Piquet, Lewis Hamilton |
| `#ee5f2f` | Juan Manuel Fangio, Max Verstappen |
| `#12a18e` | Johnnie Parsons, Jack Brabham, Michael Schumacher |
| `#bd19e6` | Lee Wallard, Tony Brooks, Niki Lauda |
| `#12a11b` | Luigi Fagioli, Maurice Trintignant, Phil Hill, John Surtees, Denny Hulme, James Hunt, Alain Prost |
| `#d01137` | José Froilán González, Bruce McLaren, Dan Gurney, Jochen Rindt, Emerson Fittipaldi, Nigel Mansell |
| `#ea3e8e` | Alberto Ascari, Ayrton Senna |
| `#4953df` | Piero Taruffi, Peter Collins, Jackie Stewart |
| `#97900c` | Troy Ruttman, Stirling Moss, Fernando Alonso |
| `#2d764a` | Bill Vukovich, Graham Hill, Damon Hill, Sebastian Vettel |
| `#96512c` | Mike Hawthorn |
| `#76642d` | Jim Clark |

**colour_rule_full_dataset_top20 — PASS** (`config_pilot_2014_2021_top20.json`, 20-row board; every race of the full RTT-002 dataset, boards computed from win_credits.csv alone)
- 1164 races; 59 drivers ever reach the top 20; at most 22 can be on screen together (top 20 after a race and the 3 before it, so rows still fading out count)
- 22 colours used of a 22-colour palette; every pair that can be on screen together differs, the closest being Peter Collins / Giuseppe Farina at CIEDE2000 18.2 (rule: at least 18)
- palette: closest pair of any two palette colours CIEDE2000 18.2; weakest white-name contrast on a bar 3.21:1
- 22 drivers drawn in the RTT-002 cases run with a 20-row board; each drawn in its assigned colour in every such case

| Colour (as drawn) | Drivers, in the order they first reach the top 20 |
|---|---|
| `#2e86de` | Giuseppe Farina, Nelson Piquet |
| `#fb07f1` | Juan Manuel Fangio |
| `#ff4f15` | Johnnie Parsons, Jacky Ickx, Michael Schumacher |
| `#464af9` | Lee Wallard, Denny Hulme, Gerhard Berger, Damon Hill |
| `#ff4663` | Luigi Fagioli, Jackie Stewart |
| `#06a54e` | José Froilán González, Ronnie Peterson, Mika Häkkinen |
| `#c97a00` | Alberto Ascari, Nico Rosberg |
| `#909600` | Piero Taruffi, Jochen Rindt, Alain Prost |
| `#cc031b` | Troy Ruttman, Dan Gurney, Alan Jones, Kimi Räikkönen |
| `#a230aa` | Bill Vukovich, Niki Lauda |
| `#c4025c` | Mike Hawthorn, James Hunt, David Coulthard, Jenson Button |
| `#367400` | Maurice Trintignant, Emerson Fittipaldi, Max Verstappen |
| `#009ca2` | Bob Sweikert, John Surtees, René Arnoux, Ayrton Senna |
| `#97511a` | Stirling Moss |
| `#007260` | Luigi Musso, Jim Clark |
| `#ac6f8c` | Pat Flaherty, Graham Hill |
| `#7d77b3` | Peter Collins, Clay Regazzoni, Jody Scheckter, Jacques Villeneuve, Fernando Alonso |
| `#1e6c84` | Sam Hanks, Phil Hill, Carlos Reutemann, Lewis Hamilton |
| `#7a6f41` | Tony Brooks, Nigel Mansell |
| `#9e7c6d` | Jimmy Bryan, Bruce McLaren, Mario Andretti, Sebastian Vettel |
| `#7a8580` | Jack Brabham |
| `#6a616a` | Wolfgang von Trips |

**enter_leave**
- E6 enters the top 5 at race 13 and leaves after race 26

**quiet_stretch**
- quiet stretch paced at 0.8x; events take 26.10 s against 28.50 s unpaced

**shared_drive**
- shared drive at race 3: SA and SB both step on frame 72

**shared_drive_winner_highlight**
- shared drive at race 3: SA and SB both step on frame 72

**rtt002_2014_2021_A_top20**
- 2020 Eifel Grand Prix (frame 1761): Lewis Hamilton 91 (P2), Michael Schumacher 91 (P1) — Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)
- 2020 Portuguese Grand Prix (frame 1806): Lewis Hamilton 92 (P1), Michael Schumacher 91 (P2) — Hamilton passes Schumacher
- FRAME_COUNT_ONLY total 2472 frames = 82.4 s
- opening: no title card; frame 0 is the board with the title "Most Formula 1 Grand Prix Wins" and 20 value labels (the totals before 2014 Australian Grand Prix); first race lands at 2.00 s
- final board on screen exactly 10.00 s from the first frame of the last race, no closing card
- record moment 2020-10-11 2020 Eifel Grand Prix: Lewis Hamilton 91 wins, BECOMES_JOINT (record holders after: Lewis Hamilton; Michael Schumacher) — held 1.50 s, frames 1761-1805; rows settled to within 0.000 row on its last frame
- record moment 2020-10-25 2020 Portuguese Grand Prix: Lewis Hamilton 92 wins, BECOMES_SOLE (record holders after: Lewis Hamilton) — held 1.50 s, frames 1806-1850; rows settled to within 0.065 row on its last frame
- not held (EXTENDS_SOLE in the window): 11 races

**rtt002_2014_2021_B_top10_winner**
- 2020 Eifel Grand Prix (frame 1761): Lewis Hamilton 91 (P2), Michael Schumacher 91 (P1) — Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)
- 2020 Portuguese Grand Prix (frame 1806): Lewis Hamilton 92 (P1), Michael Schumacher 91 (P2) — Hamilton passes Schumacher
- FRAME_COUNT_ONLY total 2472 frames = 82.4 s
- opening: no title card; frame 0 is the board with the title "Most Formula 1 Grand Prix Wins" and 11 value labels (the totals before 2014 Australian Grand Prix); first race lands at 2.00 s
- final board on screen exactly 10.00 s from the first frame of the last race, no closing card
- record moment 2020-10-11 2020 Eifel Grand Prix: Lewis Hamilton 91 wins, BECOMES_JOINT (record holders after: Lewis Hamilton; Michael Schumacher) — held 1.50 s, frames 1761-1805; rows settled to within 0.000 row on its last frame
- record moment 2020-10-25 2020 Portuguese Grand Prix: Lewis Hamilton 92 wins, BECOMES_SOLE (record holders after: Lewis Hamilton) — held 1.50 s, frames 1806-1850; rows settled to within 0.065 row on its last frame
- not held (EXTENDS_SOLE in the window): 11 races

The draw-call checks are the pass/fail gate. OCR is an independent read of the pixels: any mismatch is listed above, not hidden (0 in this run). Labels on rows that overlap mid-overtake are not OCR-read (count in brackets). The full run is checked on every frame by draw calls only (no PNGs, no OCR).
