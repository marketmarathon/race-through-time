# RTT-002 story moments (`story_moments.csv`)

Added 29 Sep 2026 for the full film (DEC-063). A new, derived file: built by `scripts/rtt002_story.py` from files already in this folder (`races.csv`, `win_credits.csv`, `drivers.csv`, `record_progression.csv`, `topten_entries.csv`, `topten_at_freeze.csv`), none of which was changed. The player reads it for the film's captions and pacing holds (`kits/rtt-002/config_rtt002_film.json`, key `story`).

One row per moment: `moment, kind, race_index, race_date, season, grand_prix, driver_id, driver_name, career_wins, caption_1, caption_2, caption_3, source`. Kinds: FIRST_RACE, LEADER (every change of all-time leader), EQUALS (a record equalled on the way to the lead), MILESTONE (first driver to 50 and to 100 wins), TOPTEN (the day each driver of today's top ten entered the all-time top ten), FREEZE (the last race in the data). Rules and the full list with sources: `reports/RTT-002_story_moments.md`.

Every row is re-derived from `win_credits.csv` by the script (it stops on any disagreement) and rebuilt independently in JavaScript by the player tests (`tests/player/run_tests.js`, case `rtt002_film`), which also check every caption as drawn. Licence: as the rest of this folder (derived from Wikipedia, CC BY-SA 4.0; `ATTRIBUTION.md`).
