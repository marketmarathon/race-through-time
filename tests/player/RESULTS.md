# Player test results (RTT-002 full film, DEC-068; speed clips, DEC-071)

Written by `node tests/player/run_tests.js` (all cases). Frames are 1920x1080 (preview width), drawn headless in Playwright 1.56.1 Chromium, every race frame in order.
OCR: tesseract 5.3.4 on every value label (and stats label, where on) of the first frame of every race.

Overall: 20/20 PASS.

| Case | Result | Config | Rows | Races | Frames | Race length | Value labels checked | Winner lines checked | Highlight onsets (most in 1 s) | Numbers checked on fixed-pitch digits | Beats outside holds | Boundary frames | OCR read back (skipped: overlapping rows) | Board entries | Slowest entry (frames to clearly visible) | Colour-checked frames | Name size | Pacing (rank / visible / quiet) | Event labels checked (fading) | Event label: furthest right edge | Flags checked | Date lines checked (winner off the board) | Date line: closest item | Overlay boxes: closest item | Stats labels checked | Stats label: furthest right edge | Stats overlap: labels checked (row mid-overtake) | Stats label: closest item | Adapter output SHA-256 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| enter_leave | PASS | `config.json` | 5 | 27 | 591 | 19.20 s | 2688 | off | off | 5535 | 0.40-0.70 s | 54 | 85/85 (40) | 9 | 5 | 591 | 33px | 13 / 5 / 9 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `ea7d2b8cb412baba…` |
| long_names | PASS | `config.json` | 10 | 15 | 369 | 11.80 s | 885 | off | off | 2577 | 0.40-0.70 s | 30 | 28/28 (0) | 4 | 0 | 369 | 32px | 4 / 6 / 5 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `af96bed9a709e154…` |
| quiet_stretch | PASS | `config.json` | 10 | 57 | 918 | 30.10 s | 7935 | off | off | 12258 | 0.40-0.70 s | 114 | 525/525 (0) | 10 | 0 | 918 | 32px | 10 / 3 / 44 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `295097a2840bd36f…` |
| shared_drive | PASS | `config.json` | 10 | 5 | 240 | 7.50 s | 567 | off | off | 1774 | 0.70-0.70 s | 10 | 6/6 (6) | 3 | 0 | 240 | 32px | 5 / 0 / 0 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `ff6f31866ff42ed1…` |
| short_opening | PASS | `config.json` | 10 | 6 | 243 | 7.60 s | 531 | off | off | 1804 | 0.50-0.70 s | 12 | 12/12 (0) | 3 | 0 | 243 | 32px | 3 / 3 / 0 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `34b6817f696fdaf2…` |
| three_way_tie | PASS | `config.json` | 10 | 10 | 321 | 10.20 s | 987 | off | off | 2593 | 0.50-0.70 s | 20 | 14/14 (17) | 4 | 0 | 321 | 32px | 6 / 4 / 0 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `af4adc580593b42e…` |
| shared_drive_winner_highlight | PASS | `config.json` | 10 | 5 | 240 | 7.50 s | 567 | 210 | 4 (2) | 1984 | 0.70-0.70 s | 10 | 6/6 (6) | 3 | 0 | 240 | 32px | 5 / 0 / 0 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `ff6f31866ff42ed1…` |
| shared_drive_round4 | PASS | `config.json` | 20 | 5 | 240 | 7.50 s | 567 | off | 4 (2) | 1909 | 0.70-0.70 s | 10 | 6/6 (6) | 3 | 0 | 240 | 29px | 5 / 0 / 0 | 357 (18) | x 1783 | 357 | 210 (0) | 39 px | 9 px | off | n/a | n/a | n/a | `ff6f31866ff42ed1…` |
| shared_drive_round5 | PASS | `config.json` | 20 | 5 | 240 | 7.50 s | 567 | off | 4 (2) | 2101 | 0.70-0.70 s | 10 | 12/12 (12) | 3 | 0 | 240 | 29px | 5 / 0 / 0 | off | n/a | 357 | 210 (0) | 39 px | 12 px | 567 | x 1673 | 567 (175) | 9 px | `ff6f31866ff42ed1…` |
| rtt002_1984_1989 | PASS | `config.json` | 10 | 96 | 1461 | 48.20 s | 14698 | off | off | 22309 | 0.40-0.70 s | 192 | 564/564 (392) | 4 | 5 | 1461 | 32px | 14 / 16 / 66 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `c3fd47774f0db6f8…` |
| rtt002_2014_2021_A_top20 | PASS | `config_pilot_2014_2021_top20.json` | 20 | 160 | 2502 | 83.40 s | 50084 | off | 61 (3) | 112092 | 0.40-0.70 s | 320 | 3686/3686 (2710) | 2 | 1 | 2502 | 29px | 11 / 16 / 133 | off | n/a | 50084 | 2502 (588) | 39 px | 10 px | 50084 | x 1741 | 50082 (1486) | 7 px | `c3fd47774f0db6f8…` |
| rtt002_full_run | PASS | `config.json` | 10 | 1164 | 15747 | 524.40 s | 156008 | off | off | 239620 | 0.40-0.70 s | not saved | not run | 40 | 5 | 15747 | 32px | 136 / 140 / 888 | off | n/a | off | n/a | n/a | n/a | off | n/a | n/a | n/a | `c3fd47774f0db6f8…` |
| rtt002_film | PASS | `config_rtt002_film.json` | 20 | 1164 | 11852 | 395.07 s | 221161 | off | 475 (4) | 493173 | 0.27-0.47 s | not saved | not run | 60 | 5 | 11852 | 29px | 136 / 140 / 888 | off | n/a | 221161 | 11852 (3780) | 39 px | 10 px | 221161 | x 1741 | 221120 (19734) | 7 px | `c3fd47774f0db6f8…` |
| rtt002_speed_2014_2021_1x | PASS | `config_speed_2014_2021_1x.json` | 20 | 160 | 2502 | 83.40 s | 50084 | off | 61 (3) | 112092 | 0.40-0.70 s | not saved | not run | 2 | 1 | 2502 | 29px | 11 / 16 / 133 | off | n/a | 50084 | 2502 (588) | 39 px | 10 px | 50084 | x 1741 | 50082 (1486) | 7 px | `c3fd47774f0db6f8…` |
| rtt002_speed_2014_2021_1.25x | PASS | `config_speed_2014_2021_1.25x.json` | 20 | 160 | 2098 | 69.93 s | 42004 | off | 61 (3) | 93970 | 0.30-0.57 s | not saved | not run | 2 | 1 | 2098 | 29px | 11 / 16 / 133 | off | n/a | 42004 | 2098 (476) | 39 px | 10 px | 42004 | x 1741 | 42002 (1422) | 7 px | `c3fd47774f0db6f8…` |
| rtt002_speed_2014_2021_1.5x | PASS | `config_speed_2014_2021_1.5x.json` | 20 | 160 | 1828 | 60.93 s | 36604 | off | 61 (3) | 81859 | 0.27-0.47 s | not saved | not run | 2 | 1 | 1828 | 29px | 11 / 16 / 133 | off | n/a | 36604 | 1828 (392) | 39 px | 10 px | 36604 | x 1741 | 36602 (1363) | 7 px | `c3fd47774f0db6f8…` |

Entry rule: a driver joining the visible board must be clearly visible (row opacity at least 0.8, name and value label drawn) within 8 frames of the first frame of that race, i.e. on frame +0 to +7. The column gives the slowest entry in the case (+N frames).
Colour rule on frames: on every frame drawn, no two bars on screen (opacity above 0) share a colour or are closer than CIEDE2000 18, and every driver is drawn in the same colour in every RTT-002 case with the same board size.
Winner highlight (where on): on the first frame of every race exactly the credited winners whose bars are on the board are lit, nothing else is ever lit, a highlight only rises from fully off on the first frame of a race that driver won (a repeat winner stays lit, so never flickers), highlights start on at most 3 different frames in any second (both bars of a shared drive light on the same frame and count as one flash, DEC-075; the column counts bars), and each fades out within highlight.sec.
Round 5 (where on): stats label = on every frame every bar with a value label carries "· <S> start(s) · <R>%" right after it, S from starts.csv and R = wins / starts recomputed here (one decimal, rounded half up), the win count bold and the stats regular, numbers changing only on the first frame of a race, ending inside the 64 px right margin; it overlaps no bar, flag, name, value or stats label of a row that is not mid-overtake (within 0.85 row; counted in brackets) and no title, subtitle, axis number, footer or date line (row labels measured as drawn, inside the board clip at y 150-1034, as bars are); OCR also reads every stats label back at race boundaries.
Round 4 (where on): date line = on every frame exactly one line "<D Month YYYY> · <GP>" for the race on screen, from races.csv, including races whose winner is off the board (frames of such races in brackets), overlapping nothing ("closest item" = the smallest gap on any frame to a bar, flag, name, value, event label, axis number, title, subtitle or footer); event labels now read "· <GP> · <D Month YYYY>" and must end inside the 64 px right margin (x 1856; "furthest right edge" = the largest on any frame); overlay boxes = also no axis grid line inside a box.
Round 3 (where on): flags = every flag drawn equals the driver's flag_code in the nationality file and sits on its row; event labels = on every frame each winner on the board shows "· <GP>" from races.csv right after its value, and the only other event labels are the previous race's, fading; time block = on every frame no overlap with any bar, flag, name, value, event label, axis number, title or footer ("closest item" = the smallest gap on any frame); overlay boxes = nothing enters the reserved logo and car boxes on any frame, placeholders drawn inside them, and the boxes stay out of the bottom 130 px.
Record holds (where on): the held races are exactly the BECOMES_JOINT / BECOMES_SOLE rows of data/rtt-002/record_progression.csv inside the window; on the last frame of each hold every row is within 0.1 row of its place; every other beat is within 0.8-1.4 x sec_per_event (to the nearest frame).

**win_rate_rounding — PASS**
- 125750 pairs (0 <= wins <= starts <= 500): player rateText = Python decimal ROUND_HALF_UP = test BigInt on every pair; examples 1/8 = 12.5%, 1/16 = 6.3%, 3/16 = 18.8%, 1/80 = 1.3%, 91/306 = 29.7%, 1/1 = 100.0%, 1/3 = 33.3%

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
- 22 colours used of a 22-colour palette; every pair that can be on screen together differs, the closest being Mike Hawthorn / Stirling Moss at CIEDE2000 18.2 (rule: at least 18)
- palette: closest pair of any two palette colours CIEDE2000 18.2; weakest white-name contrast on a bar 3.21:1
- colour priority: 40 drivers ever reach the top ten; their colours: 11 muted, 9 vivid, darker, 20 bright (bright = CIELAB L* and C* both at least 50 as drawn)
- named drivers: Lewis Hamilton `#2e86de` (L* 55, C* 52, bright); Michael Schumacher `#06a54e` (L* 59, C* 66, bright); Max Verstappen `#ff4f15` (L* 59, C* 92, bright); Ayrton Senna `#c97a00` (L* 58, C* 69, bright); Alain Prost `#ff4663` (L* 59, C* 75, bright)
- drivers who never reach the top ten but share a bright colour (only where nothing else fitted): Jacques Villeneuve
- 59 drivers drawn in the RTT-002 cases run with a 20-row board; each drawn in its assigned colour in every such case

| Colour (as drawn) | Drivers, in the order they first reach the top 20 |
|---|---|
| `#97511a` | Giuseppe Farina, Nelson Piquet |
| `#367400` | Juan Manuel Fangio |
| `#06a54e` | Johnnie Parsons, Jacky Ickx, Michael Schumacher |
| `#ff4663` | Lee Wallard, Jochen Rindt, Alain Prost |
| `#909600` | Luigi Fagioli, Denny Hulme, Jacques Villeneuve, Fernando Alonso |
| `#c4025c` | José Froilán González, Niki Lauda |
| `#1e6c84` | Alberto Ascari, Nico Rosberg |
| `#cc031b` | Piero Taruffi, Jackie Stewart |
| `#464af9` | Troy Ruttman, John Surtees, Nigel Mansell |
| `#7a8580` | Bill Vukovich, Alan Jones, Kimi Räikkönen |
| `#2e86de` | Mike Hawthorn, James Hunt, Lewis Hamilton |
| `#ff4f15` | Maurice Trintignant, Emerson Fittipaldi, Max Verstappen |
| `#009ca2` | Bob Sweikert, Dan Gurney, René Arnoux, Gerhard Berger, Damon Hill |
| `#7d77b3` | Stirling Moss |
| `#a230aa` | Luigi Musso, Jim Clark |
| `#007260` | Pat Flaherty, Graham Hill |
| `#7a6f41` | Peter Collins, Clay Regazzoni, Jody Scheckter, Mika Häkkinen |
| `#9e7c6d` | Sam Hanks, Phil Hill, Carlos Reutemann, Jenson Button |
| `#c97a00` | Tony Brooks, Ayrton Senna |
| `#6a616a` | Jimmy Bryan, Wolfgang von Trips, Ronnie Peterson, David Coulthard |
| `#ac6f8c` | Jack Brabham |
| `#fb07f1` | Bruce McLaren, Mario Andretti, Sebastian Vettel |

**enter_leave**
- E6 enters the top 5 at race 13 and leaves after race 26

**quiet_stretch**
- quiet stretch paced at 0.8x; events take 26.10 s against 28.50 s unpaced

**shared_drive**
- shared drive at race 3: SA and SB both step on frame 72

**shared_drive_winner_highlight**
- shared drive at race 3: SA and SB both step on frame 72

**shared_drive_round4**
- date line: 210 frames checked; 0 of 5 races (0%) were won by a driver not on the 20-row board after the race, and their 0 frames still name the race
- furthest right edge of any event label: x 1782.9 (limit 1856), "· Test GP 4 · 18 May 2003 (SA, frame 104)"
- shared drive at race 3: SA and SB both step on frame 72

**shared_drive_round5**
- date line: 210 frames checked; 0 of 5 races (0%) were won by a driver not on the 20-row board after the race, and their 0 frames still name the race
- stats labels: 567 checked (three numbers each against starts.csv and win_credits.csv); furthest right edge x 1672.5 (limit 1856), "2 wins · 3 starts · 66.7% (SB, frame 72)"; overlap check on 567 labels, 175 of them with a row mid-overtake (those rows skipped), closest item 8.6 px
- shared drive at race 3: SA and SB both step on frame 72

**rtt002_2014_2021_A_top20**
- date line: 2502 frames checked; 49 of 160 races (31%) were won by a driver not on the 20-row board after the race, and their 588 frames still name the race
- stats labels: 50084 checked (three numbers each against starts.csv and win_credits.csv); furthest right edge x 1740.5 (limit 1856), "100 wins · 281 starts · 35.6% (wp675561, frame 2118)"; overlap check on 50082 labels, 1486 of them with a row mid-overtake (those rows skipped), closest item 7.0 px
- 2020 Eifel Grand Prix (frame 1761): Lewis Hamilton 91 (P2), Michael Schumacher 91 (P1) — Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)
- 2020 Portuguese Grand Prix (frame 1821): Lewis Hamilton 92 (P1), Michael Schumacher 91 (P2) — Hamilton passes Schumacher
- FRAME_COUNT_ONLY total 2502 frames = 83.4 s
- opening: no title card; frame 0 is the board with the title "Most Formula 1 Grand Prix Wins" and 20 value labels (the totals before 2014 Australian Grand Prix); first race lands at 2.00 s
- final board on screen exactly 10.00 s from the first frame of the last race, no closing card
- record moment 2020-10-11 2020 Eifel Grand Prix: Lewis Hamilton 91 wins, BECOMES_JOINT (record holders after: Lewis Hamilton; Michael Schumacher) — held 2.00 s, frames 1761-1820; rows settled to within 0.000 row on its last frame
- record moment 2020-10-25 2020 Portuguese Grand Prix: Lewis Hamilton 92 wins, BECOMES_SOLE (record holders after: Lewis Hamilton) — held 2.00 s, frames 1821-1880; rows settled to within 0.026 row on its last frame
- not held (EXTENDS_SOLE in the window): 11 races

**rtt002_film**
- date line: 11852 frames checked; 436 of 1164 races (37%) were won by a driver not on the 20-row board after the race, and their 3780 frames still name the race
- stats labels: 221161 checked (three numbers each against starts.csv and win_credits.csv); furthest right edge x 1740.5 (limit 1856), "100 wins · 281 starts · 35.6% (wp675561, frame 10574)"; overlap check on 221120 labels, 19734 of them with a row mid-overtake (those rows skipped), closest item 7.0 px
- highlights: 21 one-second windows with 4 highlight starts (more than the usual 3), exactly the 21 Luke accepted (DEC-077); measured below the WCAG 2.x general- and red-flash area thresholds (worst 11.4% of a 10-degree field; reports/RTT-002_wcag_flash_check.md)
- leader changes: the drawn leader changed 8 times, each on the first frame of the race record_progression.csv gives (the win_credits.csv recount agrees), and on no other frame: 1950-07-02 Juan Manuel Fangio; 1952-08-17 Alberto Ascari; 1955-01-16 Juan Manuel Fangio; 1968-01-01 Jim Clark; 1973-07-29 Jackie Stewart; 1987-09-20 Alain Prost; 2001-09-02 Michael Schumacher; 2020-10-25 Lewis Hamilton
- final table (last frame): 1. Lewis Hamilton 106, 2. Michael Schumacher 91, 3. Max Verstappen 71, 4. Sebastian Vettel 53, 5. Alain Prost 51, 6. Ayrton Senna 41, 7. Fernando Alonso 32, 8. Nigel Mansell 31, 9. Jackie Stewart 27, 10. Jim Clark 25, 11. Niki Lauda 25, 12. Juan Manuel Fangio 24, 13. Nelson Piquet 23, 14. Nico Rosberg 23, 15. Damon Hill 22, 16. Kimi Räikkönen 21, 17. Mika Häkkinen 20, 18. Stirling Moss 16, 19. Jenson Button 15, 20. Graham Hill 14; equal to career_totals.csv ranks 1-20 and topten_at_freeze.csv; on screen 10.0 s
- FRAME_COUNT_ONLY total 11852 frames = 395.1 s
- opening: no title card; frame 0 is the board with the title "Most Formula 1 Grand Prix Wins" and 1 value labels (the board opens empty, so 1950 British Grand Prix lands on frame 0); first race lands at 0.00 s
- final board on screen exactly 10.00 s from the first frame of the last race, no closing card
- record moment 1950-05-13 1950 British Grand Prix: Giuseppe Farina 1 wins, BECOMES_SOLE (record holders after: Giuseppe Farina) — held 2.00 s, frames 0-59; rows settled to within 0.000 row on its last frame
- record moment 1950-05-21 1950 Monaco Grand Prix: Juan Manuel Fangio 1 wins, BECOMES_JOINT (record holders after: Giuseppe Farina; Juan Manuel Fangio) — held 2.00 s, frames 60-119; rows settled to within 0.000 row on its last frame
- record moment 1950-05-30 1950 Indianapolis 500: Johnnie Parsons 1 wins, BECOMES_JOINT (record holders after: Giuseppe Farina; Johnnie Parsons; Juan Manuel Fangio) — held 2.00 s, frames 120-179; rows settled to within 0.000 row on its last frame
- record moment 1950-06-04 1950 Swiss Grand Prix: Giuseppe Farina 2 wins, BECOMES_SOLE (record holders after: Giuseppe Farina) — held 2.00 s, frames 180-239; rows settled to within 0.000 row on its last frame
- record moment 1950-06-18 1950 Belgian Grand Prix: Juan Manuel Fangio 2 wins, BECOMES_JOINT (record holders after: Giuseppe Farina; Juan Manuel Fangio) — held 2.00 s, frames 240-299; rows settled to within 0.000 row on its last frame
- record moment 1950-07-02 1950 French Grand Prix: Juan Manuel Fangio 3 wins, BECOMES_SOLE (record holders after: Juan Manuel Fangio) — held 2.00 s, frames 300-359; rows settled to within 0.026 row on its last frame
- record moment 1950-09-03 1950 Italian Grand Prix: Giuseppe Farina 3 wins, BECOMES_JOINT (record holders after: Giuseppe Farina; Juan Manuel Fangio) — held 2.00 s, frames 360-419; rows settled to within 0.001 row on its last frame
- record moment 1951-05-27 1951 Swiss Grand Prix: Juan Manuel Fangio 4 wins, BECOMES_SOLE (record holders after: Juan Manuel Fangio) — held 2.00 s, frames 420-479; rows settled to within 0.000 row on its last frame
- record moment 1951-06-17 1951 Belgian Grand Prix: Giuseppe Farina 4 wins, BECOMES_JOINT (record holders after: Giuseppe Farina; Juan Manuel Fangio) — held 2.00 s, frames 494-553; rows settled to within 0.000 row on its last frame
- record moment 1951-07-01 1951 French Grand Prix: Juan Manuel Fangio 5 wins, BECOMES_SOLE (record holders after: Juan Manuel Fangio) — held 2.00 s, frames 554-613; rows settled to within 0.000 row on its last frame
- record moment 1952-08-03 1952 German Grand Prix: Alberto Ascari 6 wins, BECOMES_JOINT (record holders after: Alberto Ascari; Juan Manuel Fangio) — held 2.00 s, frames 728-787; rows settled to within 0.012 row on its last frame
- record moment 1952-08-17 1952 Dutch Grand Prix: Alberto Ascari 7 wins, BECOMES_SOLE (record holders after: Alberto Ascari) — held 2.00 s, frames 788-847; rows settled to within 0.027 row on its last frame
- record moment 1954-09-05 1954 Italian Grand Prix: Juan Manuel Fangio 13 wins, BECOMES_JOINT (record holders after: Alberto Ascari; Juan Manuel Fangio) — held 2.00 s, frames 1018-1077; rows settled to within 0.010 row on its last frame
- record moment 1955-01-16 1955 Argentine Grand Prix: Juan Manuel Fangio 14 wins, BECOMES_SOLE (record holders after: Juan Manuel Fangio) — held 2.00 s, frames 1092-1151; rows settled to within 0.056 row on its last frame
- record moment 1967-10-22 1967 Mexican Grand Prix: Jim Clark 24 wins, BECOMES_JOINT (record holders after: Jim Clark; Juan Manuel Fangio) — held 2.00 s, frames 2352-2411; rows settled to within 0.006 row on its last frame
- record moment 1968-01-01 1968 South African Grand Prix: Jim Clark 25 wins, BECOMES_SOLE (record holders after: Jim Clark) — held 2.00 s, frames 2412-2471; rows settled to within 0.026 row on its last frame
- record moment 1973-06-03 1973 Monaco Grand Prix: Jackie Stewart 25 wins, BECOMES_JOINT (record holders after: Jackie Stewart; Jim Clark) — held 2.00 s, frames 3072-3131; rows settled to within 0.026 row on its last frame
- record moment 1973-07-29 1973 Dutch Grand Prix: Jackie Stewart 26 wins, BECOMES_SOLE (record holders after: Jackie Stewart) — held 2.00 s, frames 3162-3221; rows settled to within 0.026 row on its last frame
- record moment 1987-05-17 1987 Belgian Grand Prix: Alain Prost 27 wins, BECOMES_JOINT (record holders after: Alain Prost; Jackie Stewart) — held 2.00 s, frames 5014-5073; rows settled to within 0.017 row on its last frame
- record moment 1987-09-20 1987 Portuguese Grand Prix: Alain Prost 28 wins, BECOMES_SOLE (record holders after: Alain Prost) — held 2.00 s, frames 5138-5197; rows settled to within 0.032 row on its last frame
- record moment 2001-08-19 2001 Hungarian Grand Prix: Michael Schumacher 51 wins, BECOMES_JOINT (record holders after: Alain Prost; Michael Schumacher) — held 2.00 s, frames 7200-7259; rows settled to within 0.000 row on its last frame
- record moment 2001-09-02 2001 Belgian Grand Prix: Michael Schumacher 52 wins, BECOMES_SOLE (record holders after: Michael Schumacher) — held 2.00 s, frames 7260-7319; rows settled to within 0.026 row on its last frame
- record moment 2020-10-11 2020 Eifel Grand Prix: Lewis Hamilton 91 wins, BECOMES_JOINT (record holders after: Lewis Hamilton; Michael Schumacher) — held 2.00 s, frames 10296-10355; rows settled to within 0.000 row on its last frame
- record moment 2020-10-25 2020 Portuguese Grand Prix: Lewis Hamilton 92 wins, BECOMES_SOLE (record holders after: Lewis Hamilton) — held 2.00 s, frames 10356-10415; rows settled to within 0.026 row on its last frame
- not held (EXTENDS_SOLE in the window): 94 races

**rtt002_speed_2014_2021_1x**
- date line: 2502 frames checked; 49 of 160 races (31%) were won by a driver not on the 20-row board after the race, and their 588 frames still name the race
- stats labels: 50084 checked (three numbers each against starts.csv and win_credits.csv); furthest right edge x 1740.5 (limit 1856), "100 wins · 281 starts · 35.6% (wp675561, frame 2118)"; overlap check on 50082 labels, 1486 of them with a row mid-overtake (those rows skipped), closest item 7.0 px
- 2020 Eifel Grand Prix (frame 1761): Lewis Hamilton 91 (P2), Michael Schumacher 91 (P1) — Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)
- 2020 Portuguese Grand Prix (frame 1821): Lewis Hamilton 92 (P1), Michael Schumacher 91 (P2) — Hamilton passes Schumacher
- FRAME_COUNT_ONLY total 2502 frames = 83.4 s
- opening: no title card; frame 0 is the board with the title "Most Formula 1 Grand Prix Wins" and 20 value labels (the totals before 2014 Australian Grand Prix); first race lands at 2.00 s
- final board on screen exactly 10.00 s from the first frame of the last race, no closing card
- record moment 2020-10-11 2020 Eifel Grand Prix: Lewis Hamilton 91 wins, BECOMES_JOINT (record holders after: Lewis Hamilton; Michael Schumacher) — held 2.00 s, frames 1761-1820; rows settled to within 0.000 row on its last frame
- record moment 2020-10-25 2020 Portuguese Grand Prix: Lewis Hamilton 92 wins, BECOMES_SOLE (record holders after: Lewis Hamilton) — held 2.00 s, frames 1821-1880; rows settled to within 0.026 row on its last frame
- not held (EXTENDS_SOLE in the window): 11 races

**rtt002_speed_2014_2021_1.25x**
- date line: 2098 frames checked; 49 of 160 races (31%) were won by a driver not on the 20-row board after the race, and their 476 frames still name the race
- stats labels: 42004 checked (three numbers each against starts.csv and win_credits.csv); furthest right edge x 1740.5 (limit 1856), "100 wins · 281 starts · 35.6% (wp675561, frame 1730)"; overlap check on 42002 labels, 1422 of them with a row mid-overtake (those rows skipped), closest item 7.0 px
- 2020 Eifel Grand Prix (frame 1421): Lewis Hamilton 91 (P2), Michael Schumacher 91 (P1) — Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)
- 2020 Portuguese Grand Prix (frame 1481): Lewis Hamilton 92 (P1), Michael Schumacher 91 (P2) — Hamilton passes Schumacher
- FRAME_COUNT_ONLY total 2098 frames = 69.9 s
- opening: no title card; frame 0 is the board with the title "Most Formula 1 Grand Prix Wins" and 20 value labels (the totals before 2014 Australian Grand Prix); first race lands at 2.00 s
- final board on screen exactly 10.00 s from the first frame of the last race, no closing card
- record moment 2020-10-11 2020 Eifel Grand Prix: Lewis Hamilton 91 wins, BECOMES_JOINT (record holders after: Lewis Hamilton; Michael Schumacher) — held 2.00 s, frames 1421-1480; rows settled to within 0.000 row on its last frame
- record moment 2020-10-25 2020 Portuguese Grand Prix: Lewis Hamilton 92 wins, BECOMES_SOLE (record holders after: Lewis Hamilton) — held 2.00 s, frames 1481-1540; rows settled to within 0.026 row on its last frame
- not held (EXTENDS_SOLE in the window): 11 races

**rtt002_speed_2014_2021_1.5x**
- date line: 1828 frames checked; 49 of 160 races (31%) were won by a driver not on the 20-row board after the race, and their 392 frames still name the race
- stats labels: 36604 checked (three numbers each against starts.csv and win_credits.csv); furthest right edge x 1740.5 (limit 1856), "100 wins · 281 starts · 35.6% (wp675561, frame 1472)"; overlap check on 36602 labels, 1363 of them with a row mid-overtake (those rows skipped), closest item 7.0 px
- 2020 Eifel Grand Prix (frame 1194): Lewis Hamilton 91 (P2), Michael Schumacher 91 (P1) — Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)
- 2020 Portuguese Grand Prix (frame 1254): Lewis Hamilton 92 (P1), Michael Schumacher 91 (P2) — Hamilton passes Schumacher
- FRAME_COUNT_ONLY total 1828 frames = 60.9 s
- opening: no title card; frame 0 is the board with the title "Most Formula 1 Grand Prix Wins" and 20 value labels (the totals before 2014 Australian Grand Prix); first race lands at 2.00 s
- final board on screen exactly 10.00 s from the first frame of the last race, no closing card
- record moment 2020-10-11 2020 Eifel Grand Prix: Lewis Hamilton 91 wins, BECOMES_JOINT (record holders after: Lewis Hamilton; Michael Schumacher) — held 2.00 s, frames 1194-1253; rows settled to within 0.000 row on its last frame
- record moment 2020-10-25 2020 Portuguese Grand Prix: Lewis Hamilton 92 wins, BECOMES_SOLE (record holders after: Lewis Hamilton) — held 2.00 s, frames 1254-1313; rows settled to within 0.026 row on its last frame
- not held (EXTENDS_SOLE in the window): 11 races

The draw-call checks are the pass/fail gate. OCR is an independent read of the pixels: any mismatch is listed above, not hidden (0 in this run). Labels on rows that overlap mid-overtake are not OCR-read (count in brackets). The full run is checked on every frame by draw calls only (no PNGs, no OCR).
