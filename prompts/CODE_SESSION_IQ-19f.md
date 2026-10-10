IQ-19f: music chosen, render the full film (9 Oct 2026)

Save this message word for word as prompts/CODE_SESSION_IQ-19f.md. Record the two owner decisions below from DEC-568, and your own choices as Claude DECs after them (RTT-102 block, below DEC-600). Same branch and pull request #23. Do not merge.

1. Owner decisions
(a) Music: "Glitcher" by Dyalla, from YouTube Studio's Audio Library (Race Through Time channel). Luke chose it on 9 Oct 2026 from Cowork's shortlist of five (Glitcher, Fun Vibe, The Theme, Intergalactic, Time of your life). Luke: "let's go with Glitcher - and ok to download".
- Licence: YouTube Audio Library licence. The library says: "You can use this audio track in any of your videos, including videos that you monetise. No attribution is required."
- Library details: Dance and Electronic / Bright, 3:54, added Jun 2025.
- File: private repo main, assets/rtt-102/music/glitcher_dyalla.mp3 (commit b4adada). 9,367,547 bytes; SHA-256 e848dfe29dd5374ad6b5d86c8c09a4d55b6fe5472b136184aba9ba71311225a3; MP3 320 kbps, 44.1 kHz, stereo, 234.16 s.
- README: assets/rtt-102/music/README_glitcher.txt, SHA-256 1de6789e054f34f482bf0c2a46cb1b88d0d11084b582d2d50c3f155b9fa77f1c.
- Cowork read both files back from GitHub: they match. Check both hashes again before use.
(b) The 5-second ending becomes the house default for later films. Cowork asked whether 5 s should be the ending for future films too; Luke answered: "Yeah, I think cut it to five seconds."
- Update reference/house_style.md section 1: the final table holds 5 s, YouTube's minimum end-screen window, instead of DEC-070's 10 s.
- Approved films (RTT-001, RTT-002, RTT-003, RTT-103) stay exactly as approved.

2. Full film
- Add kits/rtt-102/music_rtt102.json (path, SHA-256, length) and a new .github/workflows/rtt102_film.yml modelled on rtt103_film.yml.
- Fetch the music from the private repo main and hash-check it.
- The track (234 s) is longer than the film (about 78 s), so no loop is needed. Start where the track gets going: if its opening is near-silent or a long build-up, pick a start on a strong beat. Settle this yourself under DEC-417, record the offset and say why.
- Fade the music out over the final 5 s. Mix to −16 LUFS integrated, true peak ≤ −1 dBTP, measured after encoding.
- Run the whole-film WCAG flash check with the real logos before the render.
- Render a 3840 × 2160 master and a 1920 × 1080 viewing copy. Put them in a private pre-release with every SHA-256, size and running time.
- Rights ledger: add the track. Credit it in the description only (DEC-230); no credit is required.
- Write kits/rtt-102/youtube_times.md from the frame plan, for the packaging:
  - chapter-worthy moments with times (e.g. DeepSeek reaches second, Gemini retakes second, Claude reaches third, the Copilot and Meta AI drop-out lines);
  - the final table's on-screen values;
  - the combined-visits panel's first and last values.
- No other change to the look. Luke approves the exact master by its SHA-256 (DEC-078).

3. Report
- Ask Luke only to watch the film and approve it by its SHA-256.
- End with a short plain-English summary for Luke.
