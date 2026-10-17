# IQ-24g — RTT-104 V3: build and render the full film

v1, 17 Oct 2026 (Cowork). Continue in this session on the same branch and pull request #24 (next DEC after DEC-696; check). Luke is not technical: finish with a short plain-English summary.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-24g.md`.

## Owner decisions to record (Luke, Cowork, 17 Oct 2026 12:48 BST)
1. **Colours:** palette C.
2. **Pace:** 6 s per year. Luke: 12 s "is just too slow … the dynamics just don't seem to work".
3. **Music:** yes, loop "No.10 A New Beginning" with a smooth crossfade, as for RTT-003.

## Build the full V3 film
- **Own files:** V3 gets its own configs and its own render workflow. The approved V2 configs and workflow stay byte-identical to c379631.
- **Approved V3 choices:**
  - 20 rows, fixed 0–70% scale, palette C with the "Continent (UN M49)" key;
  - filled amber tags for changes of 5 points or more, VERIFIED rows only, held 4 s;
  - late-year elections untagged;
  - 6 s per year with smooth motion (DEC-654/655);
  - world-average panel, title and measure line as in round 3;
  - credit line "Data: IPU via World Bank WDI (CC BY 4.0) · Election dates: IPU Parline".
- **Ending:** the 5 s final table (DEC-569).
- **Closing card:** keep V2's "Not included: no sitting parliament" card only if it still makes sense for a top-20 film. If it doesn't, leave it out and say why. This is a question for Luke, not a new feature.
- **Music:** loop the track with a crossfade at a musically sensible point, and fade out at the end. It must not be audible on its own anywhere in the release.
- **Master:** 3840×2160, as V2.

## Checks
- Every landing frame equals `boards.csv`, and every tag maps to a VERIFIED row with a fetched excerpt.
- The whole film passes the WCAG flash check.
- Phone readability is checked on sample frames (1997, 2008, 2019, 2025).
- The audio loop point is checked for clicks or jumps.
- The V2 files are unchanged.

## Release
- PRIVATE pre-release in `race-through-time-private`, containing:
  - the 4K master;
  - a 1080p viewing copy;
  - 4 phone-size stills;
  - the SHA-256 of every file.
- Give the running time and the YouTube chapter times for V3, so the description can be updated.

Update `state/`, push to pull request #24, and do not merge. Nothing is published. V3 stays private until Luke approves the exact master by its SHA-256.

## Questions for Luke (numbered; give your recommendation and the default for each)
- The closing card, if relevant.
- Anything you had to judge yourself while building.

Finish with the plain-English summary.
