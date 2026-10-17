# IQ-25 — RTT-104 V3 thumbnail with the house thumbnail renderer

v1, 17 Oct 2026 (Cowork). Continue in this session on the same branch and pull request #24 (next DEC after DEC-707; check). Luke is not technical: finish with a short plain-English summary. Keep it lean.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-25.md`.

## Task
Make the V3 thumbnail with the house renderer (`kits/thumbnails/`, IQ-23, DEC-800 to DEC-810; house default "A with short words", DEC-809).
- Add `kits/thumbnails/rtt-104.json` pointing at the approved V3 film config (DEC-704; master 54e96cd5…ebffe5).
- **Frame:** the 2019 landing frame, where the UAE reaches 50% with its "Election · Oct 2019" tag. Never 2025: the renderer refuses the final period, and showing it would spoil the ending.
- **Crop:** the whole board, with every bar and label intact. Switch off the side panels by override only if the crop would cut through them; the renderer's identical-board check must pass.
- **Data check:** `data/rtt-104/series.csv`, with values as on screen to 1 decimal place.
- **Words:** two options with the house layout:
  - A: "WOMEN IN / PARLIAMENT", years "1997–2025";
  - B: "TOP 20 / WOMEN MPs", years "1997–2025".

  Recommend one. Both must be readable at 320 × 180.
- **Picture row:** flags of 4–6 countries visible in the chosen frame, only if the renderer can use the film's flag-icons files under their recorded licence (MIT, already in the rights ledger) without a new visual feature. If it needs a renderer change, leave the row out and say so. Don't change the renderer just for this.
- **Background:** the house default.

Render on the runner (thumbnails workflow, episode `rtt-104` only). Put the PNG, the JPG, the 320 × 180 and 168 × 94 copies and the check file in a PRIVATE pre-release, with a SHA-256 for each. Other episodes' thumbnails, the V2 and V3 film files and all film workflows must not change.

Update `state/`, push to pull request #24, and do not merge. Nothing is uploaded to YouTube.

## Questions for Luke (numbered; give your recommendation and the default for each)
1. Option A or B.

Finish with the plain-English summary.
