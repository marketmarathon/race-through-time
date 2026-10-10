# RTT-103 player tests (IQ-18 round 1, IQ-18b round 2, IQ-18c round 3)

Run: `node tests/player/run_tests_rtt103.js`. Checks 0-12 are listed at the top of the script.

- Data untouched and player input as recorded (check 0), colours (check 9: closest pair CIEDE2000 19.4, closest to the background 32.6), story and step cards quoted word for word from G (check 7): PASS

| Case | Config | Frames | Quarter ends checked | Result |
|---|---|---|---|---|
| base | `config_rtt103_base.json` | 3861 | 65 | PASS |
| film | `config_rtt103_film.json` | 5940 | 65 + 5 forward boards | PASS (story cards start after their own quarter by: 23 Jan 2023 0.0 s; 30 Jul 2024 0.0 s; 21 Jan 2025 0.0 s; 23 Sep 2025 0.2 s; 29 Apr 2026 0.0 s; 2 Jun 2026 2.3 s; 30 Apr 2026 6.1 s) · 4 steps after the race checked |
| clip_2025_end | `config_rtt103_clip_2025_end.json` | 2700 | 6 + 5 forward boards | PASS (story cards start after their own quarter by: 21 Jan 2025 0.0 s; 23 Sep 2025 0.2 s; 29 Apr 2026 0.0 s; 2 Jun 2026 2.3 s; 30 Apr 2026 6.1 s) · 4 steps after the race checked |

**PASS**: 4/4
