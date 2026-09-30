# RTT-002 final film: winner highlight against the WCAG 2.x flash thresholds (DEC-077)

Measured 30 Sep 2026 by Claude Code with `tests/player/wcag_flash.js` on `kits/rtt-002/config_rtt002_film.json` (1.5×, `kit_version` rtt002_film3), at 1920 × 1080 (the 3840 × 2160 master is the same drawing at twice the pixels, so the fractions are the same).

**Why:** at 1.5× the "no strobing" test (DEC-030: at most 3 highlight starts in any second) finds 21 one-second windows with 4 starts. Luke accepted them (DEC-077) on condition that the highlight is measured against WCAG first.

## Thresholds used (WCAG 2.2, as known to Claude; w3.org was blocked from the container on 30 Sep 2026, so the text was not re-read that day)
- **General flash:** a pair of opposing changes in relative luminance of 0.1 or more, where the darker state is below 0.8.
- **Red flash:** a pair of opposing transitions involving a saturated red (R / (R + G + B) ≥ 0.8).
- **Passes if either:** (1) no more than three general and no more than three red flashes in any one-second period; **or** (2) the combined area of concurrent flashes is no more than 25% of any 10° visual field at typical viewing distance. WCAG's pixel estimate of a 10° field is 341 × 256 on a 1024 × 768 screen, a third of the screen each way; on the 1920 × 1080 frame that is **640 × 360 px, so 25% = 57,600 px**. Scaling the estimate proportionally to the video frame is an assumption: it corresponds to watching full screen at a normal distance.

## Method
Every frame of the film was drawn in order. On each of the **7,144 frames with a highlight lit**, the frame was drawn again with the highlight switched off (rows restored to the same positions) and the two images compared pixel by pixel. Bars lit at the same moment (a new winner plus earlier ones still fading) are measured together. The largest count of qualifying pixels in any 640 × 360 window (scanned in 2 px steps) is reported.

## Result
| Measure | Result | Threshold | Verdict |
|---|---|---|---|
| Largest luminance change of a highlighted pixel | **0.275** (frame 5358, Nigel Mansell, `#464AF9`) | 0.1 | exceeds: highlights are luminance transitions |
| Saturated red involved | yes (`#CC031B`, Jackie Stewart) | — | red transitions occur |
| Largest concurrent **general-flash** area in any 10° window | **26,242 px = 11.4%** (frame 7138, Michael Schumacher, `#06A54E`) | 25% (57,600 px) | **below** |
| Largest concurrent **red-flash** area in any 10° window | **24,318 px = 10.6%** (frame 2918, Jackie Stewart, `#CC031B`) | 25% (57,600 px) | **below** |
| Largest general-flash area in the whole frame | 42,706 px = 2.1% of 1920 × 1080 | — | — |

**Conclusion:** the highlight's luminance change is large enough to be a flash transition, but its area stays under 25% of any 10° field (worst case 11.4%, about 2.2 times under). Under WCAG 2.x condition (2) it is below the general-flash and red-flash thresholds even in the 21 seconds with four highlight starts, so those do not count as failing flashes under WCAG. This is a measurement against a published guideline, not a medical or legal assessment of photosensitive risk.

## What changed in the tests
`tests/player/run_tests.js`: the RTT-002 film case (`rtt002_film`) carries an owner-accepted exception (DEC-077). Up to **4** highlight starts in a second are allowed there, and the case fails unless the number of such windows is exactly **21**, so any change to the film shows up. Every other case keeps the limit of 3.
