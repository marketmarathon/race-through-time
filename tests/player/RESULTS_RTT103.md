# RTT-103 player tests (IQ-18, design round 1)

Run: `node tests/player/run_tests_rtt103.js`. Checks 0-10 are listed at the top of the script.

- Data untouched and player input as recorded (check 0), colours (check 9: closest pair CIEDE2000 19.4, closest to the background 32.6), story quotes word for word in G (check 7): PASS

| Case | Config | Frames | Quarter ends checked | Result |
|---|---|---|---|---|
| base | `config_rtt103_base.json` | 3861 | 65 | PASS |
| values_B | `config_rtt103_values_B.json` | 3861 | 65 | PASS |
| gap_hold | `config_rtt103_gap_hold.json` | 3879 | 65 | PASS |
| gap_leave | `config_rtt103_gap_leave.json` | 3861 | 65 | PASS (story moments: the latest starts 0.0 s after its own quarter, queued behind the one before) |
| entry_B | `config_rtt103_entry_B.json` | 3861 | 65 | PASS |
| tencent_B | `config_rtt103_tencent_B.json` | 3861 | 65 | PASS |
| date_B | `config_rtt103_date_B.json` | 3861 | 65 | PASS |
| story_card | `config_rtt103_story_card.json` | 3861 | 65 | PASS (story moments: the latest starts 6.5 s after its own quarter, queued behind the one before) |
| story_line | `config_rtt103_story_line.json` | 3861 | 65 | PASS (story moments: the latest starts 6.5 s after its own quarter, queued behind the one before) |
| comb_line | `config_rtt103_comb_line.json` | 3861 | 65 | PASS |
| comb_bar | `config_rtt103_comb_bar.json` | 3861 | 65 | PASS |
| pace_1p0 | `config_rtt103_clip_pace_2020_2026_1p0.json` | 1050 | 26 | PASS |

**PASS**: 13/13
