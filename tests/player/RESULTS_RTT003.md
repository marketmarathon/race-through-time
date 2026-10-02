# RTT-003 player test results (IQ-10 round 2)

Written by `node tests/player/run_tests_rtt003.js`. Every frame drawn in order at 1920 x 1080 in Playwright Chromium through `kits/rtt-002/rtt.js` (the same path as the render), with placeholder pictures and logos. Expected values read independently from `data/rtt-003/` (series.csv, consoles.csv, crown.csv, series_by_maker.csv). Round 2: the numbers count; on every quarter-end frame each value label must equal series.csv exactly (with "+" where plus_flag is yes); while counting, labels stay between the two quarter ends and never go backwards.

Overall: 5/5 PASS.

| Case | Result | Config | Quarters (opening → last) | Frames | Labels at quarter ends / while counting (with "+") / bars proven to count | Bar styles (official / estimated / analyst) | Analyst labels | Faded bar-frames | Pictures / logos checked | Crown leaders (frame) | Callouts (crossing frame) | Final-table frames | Fade starts | Counts (≤1988 / later) | Closest gap: scoreboard / logo / callout line | Tall-picture overlap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clip_A_1985_1992 | PASS | `config_rtt003_clip_A_1985_1992.json` | 31 (1985-03-31 → 1992-12-31) | 939 (31.3 s) | 921 / 3825 (1268) / 51 | 0 / 4746 / 0 | 0 | 234 | 4746 / 4746 | atari_2600 f0 → nes f260 | 1988-12-31 nes f260 | 0 | atari_2600 1991-12-31 | 12-21 frames / 24-42 frames | 279 / 167 / 6 px | 0.0 px |
| clip_B_1996_1999 | PASS | `config_rtt003_clip_B_1996_1999.json` | 16 (1995-12-31 → 1999-12-31) | 744 (24.8 s) | 1964 / 5620 (1578) / 51 | 3438 / 4146 / 0 | 0 | 3192 | 7584 / 7584 | nes f0 → game_boy f343 | 1997-12-31 game_boy f343 | 0 | atari_2600 1995-12-31; master_system 1995-12-31; mega_drive 1996-03-31; game_gear 1996-03-31; saturn 1998-03-31 | n/a / 30-42 frames | 175 / 188 / 22 px | 0.0 px |
| clip_C_2005_2009 | PASS | `config_rtt003_clip_C_2005_2009.json` | 20 (2004-12-31 → 2009-12-31) | 996 (33.2 s) | 2822 / 12231 (2026) / 92 | 11159 / 3894 / 0 | 0 | 9232 | 15053 / 15053 | game_boy f0 → playstation_2 f454 | 2007-06-30 playstation_2 f454; 2009-12-31 nintendo_ds f926 | 0 | game_boy 2004-12-31; nes 2004-12-31; snes 2004-12-31; nintendo_64 2004-12-31; mega_drive 2004-12-31; atari_2600 2004-12-31; game_gear 2004-12-31; saturn 2004-12-31; dreamcast 2004-12-31; master_system 2004-12-31; playstation 2005-03-31; xbox 2006-06-30; gamecube 2008-03-31; game_boy_advance 2009-12-31 | n/a / 30-42 frames | 171 / 148 / 22 px | 0.0 px |
| clip_A_1985_1992_1.5x | PASS | `config_rtt003_clip_A_1985_1992_1.5x.json` | 31 (1985-03-31 → 1992-12-31) | 1304 (43.5 s) | 816 / 5811 (1802) / 51 | 0 / 6627 / 0 | 0 | 306 | 6627 / 6627 | atari_2600 f0 → nes f359 | 1988-12-31 nes f359 | 0 | atari_2600 1991-12-31 | 18-32 frames / 36-64 frames | 279 / 167 / 6 px | 0.0 px |
| film_full_config | PASS | `config_rtt003_film.json` | 165 (1985-03-31 → 2026-06-30) | 6309 (210.3 s) | 7888 / 71685 (16920) / 480 | 56531 / 21371 / 1671 | 1671 | 50264 | 79573 / 79573 | atari_2600 f0 → nes f260 → game_boy f1546 → playstation_2 f3097 | 1988-12-31 nes f260; 1997-12-31 game_boy f1546; 2000-09-30 game_boy f1974; 2007-06-30 playstation_2 f3097; 2009-12-31 nintendo_ds f3569 | 271 | atari_2600 1991-12-31; master_system 1993-03-31; mega_drive 1996-03-31; game_gear 1996-03-31; saturn 1998-03-31; snes 2001-03-31; dreamcast 2001-03-31; nintendo_64 2002-03-31; game_boy 2003-03-31; nes 2003-03-31; playstation 2005-03-31; xbox 2006-06-30; gamecube 2008-03-31; game_boy_advance 2009-12-31; playstation_2 2012-03-31; psp 2012-03-31; nintendo_ds 2014-03-31; wii 2016-03-31; xbox_360 2016-06-30; playstation_3 2017-03-31; nintendo_3ds 2021-03-31; xbox_one 2021-09-30; playstation_4 2022-03-31 | 12-21 frames / 24-42 frames | 120 / 135 / 6 px | 0.0 px |

Callout texts:
- clip_A_1985_1992, 1988-12-31: "NES becomes the best-selling console ever · passes Atari 2600 · estimated figures"
- clip_B_1996_1999, 1997-12-31: "Game Boy becomes the best-selling console ever · passes NES"
- clip_C_2005_2009, 2007-06-30: "PlayStation 2 becomes the best-selling console ever · passes Game Boy · estimated figures"
- clip_C_2005_2009, 2009-12-31: "Nintendo DS passes Game Boy for second place"
- clip_A_1985_1992_1.5x, 1988-12-31: "NES becomes the best-selling console ever · passes Atari 2600 · estimated figures"
- film_full_config, 1988-12-31: "NES becomes the best-selling console ever · passes Atari 2600 · estimated figures"
- film_full_config, 1997-12-31: "Game Boy becomes the best-selling console ever · passes NES"
- film_full_config, 2000-09-30: "Game Boy is the first console past 100 million"
- film_full_config, 2007-06-30: "PlayStation 2 becomes the best-selling console ever · passes Game Boy · estimated figures"
- film_full_config, 2009-12-31: "Nintendo DS passes Game Boy for second place"
