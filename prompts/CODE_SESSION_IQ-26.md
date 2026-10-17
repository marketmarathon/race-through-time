# IQ-26 — RTT-102 thumbnail in Luke's words: "CAN ANYONE CATCH CHATGPT?"

v1, 17 Oct 2026 (Cowork). New session from `main` (repos race-through-time and race-through-time-private). RTT-102's DEC block: next free is DEC-574 (check across main and open pull requests). Luke is not technical: finish with a short plain-English summary. Keep it lean.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-26.md`.

## Background
- RTT-102 `87ccrXy8Vys` has been public since 10 Oct 2026. Its live thumbnail is `rtt-102_thumb_A_short_1280x720.jpg` (DEC-809/810): "CHATGPT / VS RIVALS", the September 2025 board, a white background and eight logos. Studio, 10–16 Oct: 561 thumbnail impressions at 0.9% click-through.
- Luke, 17 Oct 2026 (Cowork chat): "I'd like to change the thumbnail title to read 'CAN ANYONE CATCH CHATGPT?'". He wants it in the house style ("with the bar chart race in the background"), not as a ChatGPT image. Record this as an owner DEC (from DEC-574).

## Task
Change only the words in `kits/thumbnails/rtt-102.json`. Keep everything else as it is live:
- period 2025-09 (DEC-804);
- the crop, the overrides and the data check;
- the two logo rows;
- the white background;
- the years "2022–2026".

**Words:** exactly "CAN ANYONE CATCH CHATGPT?", with the question mark and nothing added. Render two line splits side by side:
- A: "CAN ANYONE / CATCH CHATGPT?";
- B: "CAN ANYONE / CATCH / CHATGPT?". Use a different three-line split only if it reads clearly bigger.

Set the word sizes in the config so each line is as large as fits. If the words and both logo rows don't fit (the renderer stops on overlap), use one row of the four leading logos (ChatGPT, Gemini, Claude, DeepSeek) for that option, and say so. Recommend one option, judged on the 320 × 180 and 168 × 94 copies. Name them e.g. `D_luke_2line` and `D_luke_3line`. Once Luke picks, the config keeps only the live option (as DEC-809 and DEC-711).

**No renderer change and no new visual feature.**

**Render** on the runner (thumbnails workflow, episode `rtt-102` only). Pull request #24 (branch `claude/nifty-brown-hrl2yi`, not merged) already adds `tag_prefix` and `note` inputs to `thumbnails.yml`, so don't make a different edit to that file. Either:
- dispatch main's workflow as it is and record the true purpose in the DEC and `state/` (the release title will still say "round 1"); or
- copy pull request #24's exact change, so the two branches merge cleanly.

Your choice; say which.

**Output:** a PRIVATE pre-release with the PNG, the JPG (under 2 MB), the 320 × 180 and 168 × 94 copies and `rtt-102_check.json`, each with its SHA-256. The check file's bars must equal round 1's (`rtt-thumbs-r1-68750d6-run1`): it is the same board.

**Leave alone:** other episodes' thumbnails, the film files and every film workflow. Nothing goes to YouTube; Cowork sets the chosen JPG in Studio after Luke picks.

Update `state/`, push a branch and open a pull request. Do not merge.

## Questions for Luke (numbered; give your recommendation and the default)
1. A or B.

Finish with the plain-English summary.
