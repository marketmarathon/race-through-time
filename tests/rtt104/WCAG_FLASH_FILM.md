# RTT-104 whole-film WCAG flash check (IQ-22b)

`node tests/player/wcag_flash_rtt003.js ../rtt-104/config_rtt104_film.json` (the RTT-003 whole-picture check, unchanged; every frame of the film drawn at 1920 x 1080; definitions in that file's header). Run in the Claude Code container on 10 Oct 2026 without Luke's logo (the logo box is static, so it cannot flash); the film workflow runs it again on the runner before the render.

- Frames: 2271 (the whole film, 1:15.7)
- **Result: PASS**
- Largest area of too-often-flashing pixels (8 or more transitions in 30 frames) in any 640 x 360 window (10-degree field): **51,183 px** of 57,600 allowed, at frame 443 (14.8 s, Rwanda's 2002 to 2003 move), window at x 0, y 528
- Red flashes: largest area 399 px (frame 1855)
- Frames with any too-often-flashing pixel: 1,681 of 2,271; largest number on one frame: 67,216 px (whole frame)
- Largest area changing on a single frame in any window: 60,092 px at frame 2096 (the closing card fading in: one transition, not a flash)
- Largest single luminance step of any pixel: 1.00

A measurement against the published guideline, not a medical assessment.
