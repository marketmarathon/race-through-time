# CODE_SESSION_IQ-27: channel format changes (length, thumbnail template, Shorts, number format)

Written 3 Nov 2026 by Cowork. Repo: marketmarathon/race-through-time (public) and marketmarathon/race-through-time-private. Environment: Race Through Time. Save this brief as `prompts/CODE_SESSION_IQ-27.md`.

**DEC block: DEC-900 to DEC-949.** Highest DEC seen across all branches on 3 Nov: DEC-810 (main and PR #24/#27 branches), with DEC-574–577 on `claude/busy-wright-16ylyl`. Check again before writing; if anything in DEC-900–949 is already used, take the next free block of 50 and say so. Base your branch on `main`. Merge nothing.

## Why
Studio, last 28 days (read by Cowork 3 Nov): 2.7k thumbnail impressions across the six public videos, 4.4% click-through, average view duration 2:01, 1 subscriber. RTT-104 (Women in Parliament) got 38 impressions and 3 views in 17 days. YouTube is barely showing the films. Successful channels in the niche (e.g. Origin to Now: 2.1k subscribers, 75 videos in about 3 months, one recent film at 119k views) publish far more often, run 9–14 minutes, pick mass-appeal subjects and use one identical thumbnail layout on every video. Luke has decided to change the format.

## 1. Record first (owner DECs, Luke 3 Nov 2026, Cowork chat; his reply was "One, yes. Two, okay, we'll go for A on two. Yeah, I agree with three, yes. Yeah, okay, let's do four")
1. **Fast lane:** alongside the deep-research episodes, run quick episodes on mass-appeal subjects where one trusted, commercially usable source covers the whole race, so a film takes a day or two. Evidence rules are unchanged (VERIFIED only on screen).
2. **Length:** aim for about 8–12 minutes where the data genuinely supports it: longer periods, finer time steps, more contenders on the board, slower pacing through real drama. Never pad with holds, repeats or filler. This replaces house_style §1 "No fixed length … do not stretch a film to reach a length" (DEC-076's choice for RTT-002) and amends project principle 12 to "length follows the data, aiming for 8–12 minutes where the data supports it".
3. **One fixed thumbnail template for every video:** huge 2–4 word subject, the years, one hero image, the race bars, the same layout and type every time; no taglines. Refines DEC-800/801. Cowork's reading (not Luke's words): ChatGPT restyles (Awaiting recording 61, 17 Oct) are used only if they keep the template exactly; otherwise the house render is used, so the channel page looks consistent.
4. **Shorts:** 2–3 vertical Shorts cut from each film, each pointing to the full video.

Update `reference/house_style.md` (§1 length, the thumbnails section, a new Shorts section) in the same pull request.

## 2. Thumbnail template v2 (render only, for review)
Use the existing `kits/thumbnails/render_thumbnails.js`. Keep everything in DEC-803 (board from a landing frame, never edited, every bar checked against the data).
- Make **one template** for all six public videos: RTT-002 F1, RTT-003 consoles, RTT-001 browsers, RTT-103 AI spending, RTT-102 chatbots, RTT-104 Women in Parliament (needs a config; use its approved film and data).
- Template: bright plain background; board on the left (about 55%), at most 6 bars so every name reads at 168 × 94; on the right the subject in 2–4 huge words, the years underneath, and one hero image (a logo or picture already in `reference/rights_ledger.md` and the private repo, nothing new fetched without listing it as a question); small RTT logo in one fixed corner; no taglines, no question marks, no "you won't believe".
- Suggested words (change if they don't fit): F1 WINS 1950–2026; BEST-SELLING CONSOLES 1985–2026; BROWSER WARS 1994–2026; AI SPENDING RACE 2010–2030; CHATGPT VS RIVALS 2022–2026; WOMEN IN PARLIAMENT 1997–2025.
- Render two variants side by side (A: board left/words right as above; B: same with the hero image larger and the board reduced to 5 bars), each at 1280 × 720, 320 × 180 and 168 × 94, plus one contact sheet showing all six A thumbnails together as they would look on the channel page.
- Private pre-release with SHA-256 for every file. Do not change any live thumbnail; Luke chooses, then Cowork sets them in Studio.

## 3. Number format test (Luke asked; show, do not decide)
Luke noticed that popular races show full numbers with every digit rolling (e.g. 155,370,000) instead of compact labels ("155.4m"), so the board looks busy even in calm stretches. Render one 30-second clip of RTT-003 (consoles, a calm stretch plus one overtake) twice, side by side: A as approved (compact), B full numbers rolling. Rules for B:
- Full numbers only where the source publishes the figure to that precision (e.g. Nintendo's own totals); estimates keep "~" and compact form (principle 21). Say which bars in the clip would stay compact.
- Every landing frame still equals the data exactly; in between, the digits roll as the bar moves.
- Check names and values at phone size (5.9 pt floor); report whether B's longer labels push anything below it.
List as one question for Luke: which to use as the house default.

## 4. Shorts pilot
From two approved films, RTT-002 (F1) and RTT-003 (consoles), make two Shorts each:
- 1080 × 1920, 30–50 s, built from the film's own data and player (re-laid out for vertical, not a crop of the 16:9 frame), starting on the most dramatic stretch (a leader change or record).
- First 2 s: a large hook line (e.g. "WHO HAS THE MOST F1 WINS?"); last frame: the subject and "Full race on the channel". Board at most 8 bars; phone check.
- Music: the film's own approved Audio Library track, same mix rules (a Short on YouTube is fine; tracks are never shared off YouTube).
- Private pre-release with SHA-256s. Luke uploads; the related-video link to the full film is set in Studio by hand.

## 5. Length check for the episodes in progress
For RTT-101 (PL net transfer spend, PR #19/#25, design round 1 at about 3:00) report what running time the new rule would give, and how (pace, board size), without rendering. No change to any approved or published film.

## 6. Finish
Run the existing tests; approved films must stay pixel-identical. Push a branch, open a pull request, merge nothing. Update `state/HANDOVER.md` and `STATE.json`.

## Standing rules
Never touch marketmarathon/bars or any Market Marathon files. Public repo: code, configs, data and written results only; pictures, logos, music, stills, clips and renders only in the private repo. Never print RTT_PRIVATE_TOKEN or upload workflow artifacts from the public repo. No new visual feature is approved until Luke sees it (DEC-069): everything above is a proposal for review. Never invent or average figures. Do not install software or change credentials or settings without asking. Nothing is published or uploaded to YouTube.

## Report back
A short plain-English summary for Luke (what was made, where to look, what it costs in running time), then numbered questions with your recommendation and what happens if he does not answer: (1) thumbnail A or B, (2) number format A or B, (3) Shorts approved as a pattern.
