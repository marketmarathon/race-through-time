# RTT-104 whole-film WCAG flash check — V2 (IQ-22d)

`node tests/player/wcag_flash_rtt003.js ../rtt-104/config_rtt104_film_v2.json` (the RTT-003 whole-picture check, unchanged; every frame of the V2 film drawn at 1920 x 1080). Run in the Claude Code container on 10 Oct 2026 without Luke's logo (a static box); the film workflow runs it again on the runner before the render. V1's result: `WCAG_FLASH_FILM.md`.

- Frames: 3,111 (the whole V2 film, 1:43.7)
- **Result: PASS**
- Largest area of too-often-flashing pixels in any 640 x 360 window (10-degree field): **29,881 px** of 57,600 allowed, at frame 623 (20.8 s), window at x 0, y 528 (V1: 51,183 px)
- Red flashes: largest area 826 px (frame 2663)
- Frames with any too-often-flashing pixel: 2,549 of 3,111; largest number on one frame 33,720 px (whole frame)
- Largest area changing on one frame in any window: 60,200 px at frame 2936 (the closing card fading in: one transition, not a flash)

A measurement against the published guideline, not a medical assessment.
