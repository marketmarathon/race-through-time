# RTT-002 independent check 3 (race starts): comparison report

Check: ChatGPT deep research, prompt `prompts/RTT-002_independent_check3_starts.md`, run by Luke on 29 Sep 2026. Its answer stays private on Luke's laptop (`Data/F1_Starts_Check_2026-09-29/`), transcribed by Claude in Cowork and hash-frozen before comparison (`state/RTT-002_independent_check3_freeze.json`). The check names the same freeze: Azerbaijan Grand Prix, 26 Sep 2026. Its main sources were StatsF1, GP Racing Stats and Formula 1 results pages, with Wikipedia used only where it said so.

Compared by Claude in Cowork against `data/rtt-002/starts.csv` and `career_starts.csv` as merged in pull request #7 (main @ ee0d4c2). Disagreements are listed, not resolved by guessing; the owner decisions that follow them are DEC-058 and DEC-059.

| Section | What was checked | Result |
|---|---|---|
| K | Career starts at the freeze, all 116 winners | 102 agree; the check has NOT FOUND for 7; 7 disagree (below). Career wins agree for all 116 |
| L | Which career start each 10+ win driver's first win came on (36 drivers) | 34 agree; 2 disagree (Brabham, Graham Hill) |
| M | 26 entered-but-not-started races for 8 drivers | 25 are non-starts in our data; 1 disagrees (Barrichello, 2002 Spanish GP) |
| N | Career starts at the end of 1989, 2006, 2016, 2021 (16 driver-seasons) | 16 of 16 agree |

## Disagreements

| Driver | Our data (Wikipedia season tables) | Check | Explanation found | On screen? | Outcome |
|---|---|---|---|---|---|
| Rubens Barrichello | 323 | 322 | Our 2002 season table shows "Ret" at the Spanish GP; the check (StatsF1 non-participation record, Formula 1) says he did not start (electrical failure before the start). Wikipedia's "List of Formula One drivers" (rev. 1377016608) and GP Racing Stats also give 322 | Never in the top 20 | Corrected to a non-start by a documented correction (DEC-058) |
| Jack Brabham | 126 (first win on start 17) | 123 (start 14) | 3 extra starts before his first win in our data. Likely cause (not confirmed race by race): Grands Prix in which Formula 2 cars ran alongside Formula 1; his 1957-58 starts include the 1957 and 1958 German GPs and the 1958 Moroccan GP, which had Formula 2 classes. Wikipedia's driver list also gives 126 | Yes, 1959-2021 | Kept: Wikipedia convention counts them (DEC-059) |
| Graham Hill | 176 (first win on start 33) | NOT FOUND in K (StatsF1 175, GP Racing Stats 175, Wikipedia 176); L gives start 32 | One extra early start in our data; likely the same convention question (not confirmed race by race); Wikipedia 176 | Yes, 1962-2026 | Kept (DEC-059) |
| Luigi Musso | 24 | 23 | 1953 Italian GP was a relief-only drive (our cell "7†"); the check excludes relief drives; Wikipedia counts them | Yes, 1956-1961 | Kept (DEC-059) |
| Pat Flaherty | 6 | 5 | 1954 Indianapolis 500 relief drive (our cell "Ret†") | Yes, 1956-1961 | Kept (DEC-059) |
| Johnny Herbert | 160 | 161 | StatsF1 figure; Wikipedia's driver list gives 160; no race identified | Never in the top 20 | Kept, listed |
| Pedro Rodríguez | 55 | 54 | Wikipedia's driver list gives 55; no race identified | Never in the top 20 | Kept, listed |
| François Cevert | 47 | 46 | Check notes Wikipedia 47 against StatsF1/GP Racing Stats 46; no race identified | Never in the top 20 | Kept, listed |

The check's NOT FOUND rows in K (Graham Hill, Jacky Ickx, Tony Brooks entries only, Keke Rosberg entries only, Bruce McLaren, Phil Hill, Maurice Trintignant starts, Jo Bonnier starts, Innes Ireland entries only, Jean-Pierre Beltoise) come from the same two conventions (Formula 2 runs in championship Grands Prix, relief drives) and from entry definitions; starts are not affected where the check gave a number.

## Conclusion

The starts data is confirmed by an independent route for every season-end point checked (16/16), for 34 of 36 first-win start numbers and for 102 of 109 career totals the check could settle. The one data error found (Barrichello, 2002 Spanish GP) is corrected. The remaining differences are a counting convention, which Luke decided to keep as Wikipedia's (relief drives and Formula 2 cars in championship Grands Prix count as starts), and three one-start conflicts between sources for drivers who never appear on screen.
