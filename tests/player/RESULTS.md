# Player test results (IQ-05)

Written by `node tests/player/run_tests.js` (all cases). Frames are 1920x1080 (preview width), drawn headless in Playwright 1.56.1 Chromium, every race frame in order.
OCR: tesseract 5.3.4 on every value label of the first frame of every race.

Overall: 11/11 PASS.

| Case | Result | Config | Races | Frames | Race length | Value labels checked | Boundary frames | OCR read back (skipped: overlapping rows) | Top-ten entries | Slowest entry (frames to clearly visible) | Colour-checked frames | Name size | Pacing (rank / visible / quiet) | Adapter output SHA-256 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| enter_leave | PASS | `config.json` | 27 | 591 | 19.20 s | 2688 | 54 | 85/85 (40) | 9 | 5 | 591 | 33px | 13 / 5 / 9 | `bae1b8d036cb5835…` |
| long_names | PASS | `config.json` | 15 | 369 | 11.80 s | 885 | 30 | 28/28 (0) | 4 | 0 | 369 | 32px | 4 / 6 / 5 | `d2321b472d872afa…` |
| quiet_stretch | PASS | `config.json` | 57 | 918 | 30.10 s | 7935 | 114 | 525/525 (0) | 10 | 0 | 918 | 32px | 10 / 3 / 44 | `468a62380d522506…` |
| shared_drive | PASS | `config.json` | 5 | 240 | 7.50 s | 567 | 10 | 6/6 (6) | 3 | 0 | 240 | 32px | 5 / 0 / 0 | `5487a302f046954d…` |
| short_opening | PASS | `config.json` | 6 | 243 | 7.60 s | 531 | 12 | 12/12 (0) | 3 | 0 | 243 | 32px | 3 / 3 / 0 | `5220401ba091f4cd…` |
| three_way_tie | PASS | `config.json` | 10 | 321 | 10.20 s | 987 | 20 | 14/14 (17) | 4 | 0 | 321 | 32px | 6 / 4 / 0 | `88a3fa4b571976ee…` |
| rtt002_1984_1989 | PASS | `config.json` | 96 | 1461 | 48.20 s | 14698 | 192 | 564/564 (392) | 4 | 5 | 1461 | 32px | 14 / 16 / 66 | `ab11668e8a123f84…` |
| rtt002_2014_2021_pilot | PASS | `config_pilot_2014_2021.json` | 160 | 2187 | 72.90 s | 21892 | 320 | 785/785 (814) | 1 | 5 | 2187 | 32px | 11 / 16 / 133 | `ab11668e8a123f84…` |
| rtt002_2014_2021_pilot_fast | PASS | `config_pilot_2014_2021_fast.json` | 160 | 1567 | 52.23 s | 15692 | 320 | 842/842 (757) | 1 | 5 | 1567 | 32px | 11 / 16 / 133 | `ab11668e8a123f84…` |
| rtt002_full_run | PASS | `config.json` | 1164 | 15747 | 524.40 s | 156008 | not saved | not run | 40 | 5 | 15747 | 32px | 136 / 140 / 888 | `ab11668e8a123f84…` |

Entry rule: a driver joining the visible top N must be clearly visible (row opacity at least 0.8, name and value label drawn) within 8 frames of the first frame of that race, i.e. on frame +0 to +7. The column gives the slowest entry in the case (+N frames).
Colour rule on frames: on every frame drawn, no two bars on screen (opacity above 0) share a colour or are closer than CIEDE2000 18, and every driver is drawn in the same colour in every RTT-002 case.

**colour_rule_full_dataset — PASS** (every race of the full RTT-002 dataset, boards computed from win_credits.csv alone)
- 1164 races; 40 drivers ever reach the top 10; at most 12 can be on screen together (top 10 after a race and the 3 before it, so rows still fading out count)
- 12 colours used of a 12-colour palette; every pair that can be on screen together differs, the closest being Mike Hawthorn / Jim Clark at CIEDE2000 18.5 (rule: at least 18)
- 40 drivers drawn in the RTT-002 cases run; each drawn in its assigned colour in every case

| Colour (as drawn) | Drivers, in the order they first reach the top ten |
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

**enter_leave**
- E6 enters the top 5 at race 13 and leaves after race 26

**quiet_stretch**
- quiet stretch paced at 0.8x; events take 26.10 s against 28.50 s unpaced

**shared_drive**
- shared drive at race 3: SA and SB both step on frame 72

**rtt002_2014_2021_pilot**
- 2020 Eifel Grand Prix (frame 1731): Lewis Hamilton 91 (P2), Michael Schumacher 91 (P1) — Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)
- 2020 Portuguese Grand Prix (frame 1743): Lewis Hamilton 92 (P1), Michael Schumacher 91 (P2) — Hamilton passes Schumacher
- no closing card; final board on screen 3.40 s (last race slot + 3 s hold); FRAME_COUNT_ONLY total 2277 frames = 75.9 s

**rtt002_2014_2021_pilot_fast**
- 2020 Eifel Grand Prix (frame 1221): Lewis Hamilton 91 (P2), Michael Schumacher 91 (P1) — Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)
- 2020 Portuguese Grand Prix (frame 1229): Lewis Hamilton 92 (P1), Michael Schumacher 91 (P2) — Hamilton passes Schumacher
- no closing card; final board on screen 3.27 s (last race slot + 3 s hold); FRAME_COUNT_ONLY total 1657 frames = 55.2 s

The draw-call checks are the pass/fail gate. OCR is an independent read of the pixels: any mismatch is listed above, not hidden (0 in this run). Labels on rows that overlap mid-overtake are not OCR-read (count in brackets). The full run is checked on every frame by draw calls only (no PNGs, no OCR).
