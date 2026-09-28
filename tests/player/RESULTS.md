# IQ-04 player test results

Written by `node tests/player/run_tests.js` (all cases). Frames are 1920x1080 (preview width), drawn headless in Playwright 1.56.1 Chromium, every race frame in order.
OCR: tesseract 5.3.4 on every value label of the first frame of every race.

| Case | Result | Races | Frames | Race length | Value labels checked | Boundary frames | OCR read back (skipped: overlapping rows) | Longest entry slide (frames) | Name size | Pacing (rank / visible / quiet) | Adapter output SHA-256 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| enter_leave | PASS | 27 | 591 | 19.20 s | 2671 | 54 | 87/87 (36) | 9 | 33px | 13 / 5 / 9 | `bae1b8d036cb5835…` |
| long_names | PASS | 15 | 369 | 11.80 s | 885 | 30 | 28/28 (0) | 0 | 32px | 4 / 6 / 5 | `d2321b472d872afa…` |
| quiet_stretch | PASS | 57 | 918 | 30.10 s | 7935 | 114 | 525/525 (0) | 0 | 32px | 10 / 3 / 44 | `468a62380d522506…` |
| shared_drive | PASS | 5 | 240 | 7.50 s | 567 | 10 | 6/6 (6) | 0 | 32px | 5 / 0 / 0 | `5487a302f046954d…` |
| short_opening | PASS | 6 | 243 | 7.60 s | 531 | 12 | 12/12 (0) | 0 | 32px | 3 / 3 / 0 | `5220401ba091f4cd…` |
| three_way_tie | PASS | 10 | 321 | 10.20 s | 987 | 20 | 14/14 (17) | 0 | 32px | 6 / 4 / 0 | `88a3fa4b571976ee…` |
| rtt002_1984_1989 | PASS | 96 | 1461 | 48.20 s | 14662 | 192 | 562/562 (387) | 22 | 32px | 14 / 16 / 66 | `ab11668e8a123f84…` |

**enter_leave**
- E6 enters the top 5 at race 13 and leaves after race 26

**quiet_stretch**
- quiet stretch paced at 0.8x; events take 26.10 s against 28.50 s unpaced

**shared_drive**
- shared drive at race 3: SA and SB both step on frame 72

The draw-call checks are the pass/fail gate. OCR is an independent read of the pixels: any mismatch is listed above, not hidden (0 in this run). Labels on rows that overlap mid-overtake are not OCR-read (count in brackets).
