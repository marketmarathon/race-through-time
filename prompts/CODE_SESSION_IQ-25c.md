# IQ-25c — RTT-104 V3 thumbnail on the 1997 board (Luke's words)

v1, 17 Oct 2026 (Cowork). Same branch and pull request #24 (next DEC after DEC-712; check). Save this exact prompt as `prompts/CODE_SESSION_IQ-25c.md`.

## Owner decision to record (Luke, Cowork, 17 Oct 2026 23:23 BST)
Luke wants the thumbnail board to show **1997, not 2019**. The words stay "NOT WHO YOU THINK!" (DEC-711). This is for the ChatGPT restyle route in Cowork's `RTT_thumbnail_restyle_template.md`.

## Task
- In `kits/thumbnails/rtt-104.json`, render the 1997 landing frame of the approved V3 film (DEC-704). It is the first period, not the last, so the no-spoiler rule is met.
- Keep everything else as `C_luke`: the whole board, the white house background, the years "1997–2025", no flag row, and the same data check against `data/rtt-104/series.csv`.
- **Line split:** render two splits and pick the one whose words read biggest at 320 × 180:
  - "NOT WHO / YOU THINK!"
  - "NOT / WHO YOU / THINK!"

  Keep only the winner as the live option, and say which won and why.
- Render `rtt-104` only on the runner. Put the PNG, the JPG, the 320 × 180 and 168 × 94 copies and `rtt-104_check.json` in a PRIVATE pre-release, with a SHA-256 for each.

No film, other thumbnail or workflow changes. Update `state/` and push. Do not merge. Nothing goes to YouTube.

Finish with a two-line plain-English summary, giving the release tag and the PNG's file name and SHA-256.
