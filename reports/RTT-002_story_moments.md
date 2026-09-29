# RTT-002 story moments (full film)

Written by `scripts/rtt002_story.py` from the audited files in `data/rtt-002/` (none changed); the same rows are in `data/rtt-002/story_moments.csv`, which the player reads for its captions. Every moment is re-derived from `win_credits.csv` alone and the build stops on any disagreement. The tests (`tests/player/run_tests.js`, case `rtt002_film`) check every caption as drawn against these files.

Rules: every change of all-time leader; a record equalled on the way to taking the lead; the first driver to 50 and to 100 wins; the day each driver of today's top ten entered the all-time top ten; the first race and the data freeze. Nothing else is captioned.

| # | Kind | Date | Grand Prix | Caption | Source |
|---|---|---|---|---|---|
| 1 | FIRST_RACE | 13 May 1950 | 1950 British Grand Prix | The first World Championship Grand Prix / Won by Giuseppe Farina | races.csv race_index 1; record_progression.csv row 1 |
| 2 | EQUALS | 18 June 1950 | 1950 Belgian Grand Prix | Record equalled / Juan Manuel Fangio · 2 wins / level with Giuseppe Farina | record_progression.csv row 6 (BECOMES_JOINT) |
| 3 | LEADER | 2 July 1950 | 1950 French Grand Prix | New all-time leader / Juan Manuel Fangio · 3 wins / passes Giuseppe Farina (2 wins) | record_progression.csv row 7 (BECOMES_SOLE) |
| 4 | EQUALS | 3 August 1952 | 1952 German Grand Prix | Record equalled / Alberto Ascari · 6 wins / level with Juan Manuel Fangio | record_progression.csv row 13 (BECOMES_JOINT) |
| 5 | LEADER | 17 August 1952 | 1952 Dutch Grand Prix | New all-time leader / Alberto Ascari · 7 wins / passes Juan Manuel Fangio (6 wins) | record_progression.csv row 14 (BECOMES_SOLE) |
| 6 | EQUALS | 5 September 1954 | 1954 Italian Grand Prix | Record equalled / Juan Manuel Fangio · 13 wins / level with Alberto Ascari | record_progression.csv row 21 (BECOMES_JOINT) |
| 7 | LEADER | 16 January 1955 | 1955 Argentine Grand Prix | New all-time leader / Juan Manuel Fangio · 14 wins / passes Alberto Ascari (13 wins) | record_progression.csv row 22 (BECOMES_SOLE) |
| 8 | TOPTEN | 9 June 1963 | 1963 Belgian Grand Prix | Into the all-time top ten / Jim Clark · 4 wins | topten_entries.csv row 21 |
| 9 | EQUALS | 22 October 1967 | 1967 Mexican Grand Prix | Record equalled / Jim Clark · 24 wins / level with Juan Manuel Fangio | record_progression.csv row 33 (BECOMES_JOINT) |
| 10 | LEADER | 1 January 1968 | 1968 South African Grand Prix | New all-time leader / Jim Clark · 25 wins / passes Juan Manuel Fangio (24 wins) | record_progression.csv row 34 (BECOMES_SOLE) |
| 11 | TOPTEN | 6 October 1968 | 1968 United States Grand Prix | Into the all-time top ten / Jackie Stewart · 5 wins | topten_entries.csv row 24 |
| 12 | EQUALS | 3 June 1973 | 1973 Monaco Grand Prix | Record equalled / Jackie Stewart · 25 wins / level with Jim Clark | record_progression.csv row 35 (BECOMES_JOINT) |
| 13 | LEADER | 29 July 1973 | 1973 Dutch Grand Prix | New all-time leader / Jackie Stewart · 26 wins / passes Jim Clark (25 wins) | record_progression.csv row 36 (BECOMES_SOLE) |
| 14 | TOPTEN | 5 August 1984 | 1984 German Grand Prix | Into the all-time top ten / Alain Prost · 13 wins | topten_entries.csv row 32 |
| 15 | EQUALS | 17 May 1987 | 1987 Belgian Grand Prix | Record equalled / Alain Prost · 27 wins / level with Jackie Stewart | record_progression.csv row 38 (BECOMES_JOINT) |
| 16 | LEADER | 20 September 1987 | 1987 Portuguese Grand Prix | New all-time leader / Alain Prost · 28 wins / passes Jackie Stewart (27 wins) | record_progression.csv row 39 (BECOMES_SOLE) |
| 17 | TOPTEN | 23 April 1989 | 1989 San Marino Grand Prix | Into the all-time top ten / Ayrton Senna · 15 wins | topten_entries.csv row 34 |
| 18 | TOPTEN | 13 August 1989 | 1989 Hungarian Grand Prix | Into the all-time top ten / Nigel Mansell · 15 wins | topten_entries.csv row 35 |
| 19 | MILESTONE | 11 July 1993 | 1993 British Grand Prix | First driver to 50 wins / Alain Prost | record_progression.csv row 61 (EXTENDS_SOLE, career_wins 50) |
| 20 | TOPTEN | 30 July 1995 | 1995 German Grand Prix | Into the all-time top ten / Michael Schumacher · 15 wins | topten_entries.csv row 36 |
| 21 | EQUALS | 19 August 2001 | 2001 Hungarian Grand Prix | Record equalled / Michael Schumacher · 51 wins / level with Alain Prost | record_progression.csv row 63 (BECOMES_JOINT) |
| 22 | LEADER | 2 September 2001 | 2001 Belgian Grand Prix | New all-time leader / Michael Schumacher · 52 wins / passes Alain Prost (51 wins) | record_progression.csv row 64 (BECOMES_SOLE) |
| 23 | TOPTEN | 25 July 2010 | 2010 German Grand Prix | Into the all-time top ten / Fernando Alonso · 23 wins | topten_entries.csv row 38 |
| 24 | TOPTEN | 7 October 2012 | 2012 Japanese Grand Prix | Into the all-time top ten / Sebastian Vettel · 24 wins | topten_entries.csv row 39 |
| 25 | TOPTEN | 20 April 2014 | 2014 Chinese Grand Prix | Into the all-time top ten / Lewis Hamilton · 25 wins | topten_entries.csv row 40 |
| 26 | EQUALS | 11 October 2020 | 2020 Eifel Grand Prix | Record equalled / Lewis Hamilton · 91 wins / level with Michael Schumacher | record_progression.csv row 104 (BECOMES_JOINT) |
| 27 | LEADER | 25 October 2020 | 2020 Portuguese Grand Prix | New all-time leader / Lewis Hamilton · 92 wins / passes Michael Schumacher (91 wins) | record_progression.csv row 105 (BECOMES_SOLE) |
| 28 | MILESTONE | 26 September 2021 | 2021 Russian Grand Prix | First driver to 100 wins / Lewis Hamilton | record_progression.csv row 113 (EXTENDS_SOLE, career_wins 100) |
| 29 | TOPTEN | 19 June 2022 | 2022 Canadian Grand Prix | Into the all-time top ten / Max Verstappen · 26 wins | topten_entries.csv row 41 |
| 30 | FREEZE | 26 September 2026 | 2026 Azerbaijan Grand Prix | Standings at the data freeze / 2026 Azerbaijan GP · 26 September 2026 | races.csv race_index 1164 (last row); data/rtt-002/README.md freeze |
