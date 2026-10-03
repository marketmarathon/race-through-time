# RTT-003 full film against the WCAG 2.x flash thresholds (round 6, DEC-149)

Measured 3 Oct 2026 by Claude Code with `tests/player/wcag_flash_rtt003.js` on `kits/rtt-003/config_rtt003_film.json` (`kit_version` rtt003_pilot5, the design Luke approved, DEC-146), at 1920 × 1080 with the real private pictures and logos. The 3840 × 2160 master is the same drawing at twice the pixels, so the areas scale exactly.

**Why a different method from RTT-002:** RTT-002's check (`reports/RTT-002_wcag_flash_check.md`, DEC-077) measured its winner highlight. RTT-003 has no highlight. Its moving parts are counting digits, bars and rows gliding, callouts fading in and out, the dimming of stopped bars and the crown moving. So this check follows **every pixel of every frame** of the film (9,247 frames).

## Thresholds used (WCAG 2.2, as known to Claude; w3.org was blocked from the container on 30 Sep 2026, the same definitions as RTT-002's report)
- **Transition:** a change in relative luminance of 0.1 or more from the pixel's last extreme, opposite to its previous transition, where the darker state is below 0.8. A **flash** is a pair of opposing transitions.
- **Red flash:** a transition in which either state is a saturated red, R / (R + G + B) ≥ 0.8.
- **Too often:** a pixel that makes 8 or more transitions within one second (more than three flashes).
- **Passes if either:** (1) no more than three general and no more than three red flashes in any one-second period; **or** (2) the combined area of concurrent flashes is no more than 25% of any 10° visual field. WCAG's estimate of a 10° field is 341 × 256 on a 1024 × 768 screen, a third of the screen each way. On the 1920 × 1080 frame that is **640 × 360 px, so 25% = 57,600 px**. As in RTT-002's report, scaling the estimate to the video frame is an assumption: it corresponds to watching full screen at a normal distance.

## Result
| Measure | Result | Threshold | Verdict |
|---|---|---|---|
| Frames with any pixel flashing more than three times a second | 8,895 of 9,247 | — | condition (1) alone is not met, so condition (2) decides |
| Largest area flashing too often, inside any 10° window | **8,579 px = 3.7% of the field** (frame 3225, 31 Dec 2001) | 25% (57,600 px) | **below** (about 6.7 times under) |
| Largest **red** area flashing too often, inside any 10° window | **622 px = 0.3%** (frame 7837) | 25% (57,600 px) | **below** |
| Largest such area in the whole frame | 10,633 px general, 622 px red (0.5% / 0.03% of 1920 × 1080) | — | — |
| Largest area making a single transition on the same frame, inside any 10° window | 50,509 px (frame 3603) | — | a single change, not a flash: for example a row moving one place, a callout appearing |
| Largest single luminance transition of a pixel | 1.0 (frame 364, the NES crown callout appearing) | 0.1 | a one-off change, not repeated |

**What flashes:** the worst frame, saved as a private diagnostic still and not committed, shows two sources:
- the fast-counting tenths digits on the values and in the scoreboard totals;
- a row that climbs past several others in one quarter (here the Game Boy Advance), whose picture, logo tile and name sweep through the neighbouring rows' pictures and names.

Both cover small areas.

**Conclusion:** some pixels change more than three times a second, but the area flashing too often stays at or under 3.7% of any 10° field (general) and 0.3% (red), far under the 25% in WCAG 2.x condition (2). The film is below the general-flash and red-flash thresholds. Unlike RTT-002, no exception is needed. This is a measurement against a published guideline, not a medical or legal assessment of photosensitive risk.
