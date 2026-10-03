ROUND 6 — MUSIC AND FULL FILM (Luke, 3 Oct 2026). Record decisions from the next free DEC number:
(a) Luke APPROVED the RTT-003 design exactly as rendered in round 5 (private pre-release rtt-003-pilot5-81534e5-run6) — "I love this… this is good". No further design changes.
(b) Music: "Powerup!" by Jeremy Blake, YouTube Studio Audio Library, licence "YouTube Audio Library licence" (no attribution required), Dance and Electronic / Bright, 4:46, added Nov 2018. Chosen by Luke; downloaded by Claude in Luke's Chrome from YouTube Studio on 3 Oct 2026.

THE FILE: in the PRIVATE repo, main branch, assets/rtt-003/music/ — stored as two base64 text parts plus README_powerup.txt (browser uploads are capped at 10 MB, and a raw binary split was corrupted in transfer, so base64 is used). Rebuild and verify before use:
  cat powerup_jeremy_blake.mp3.b64.part0 powerup_jeremy_blake.mp3.b64.part1 | tr -d '\r' | base64 -d > powerup_jeremy_blake.mp3
  SHA-256 must equal a855b541b2bd661a2077c6157ee3df11540a79d5c630a44d26f043ecdac7f7be (11,406,143 bytes). If it does not match, stop and tell Luke.
Commit the rebuilt MP3 next to the parts in the private repo (keep the parts and README; music never goes in the public repo; never make it available separately from videos). Add the track to reference/rights_ledger.md (title, artist, source, licence, date, SHA-256, private path).

MUSIC MIX: use the approved RTT-002 approach (DEC-073/DEC-074, scripts/rtt_mix_music.sh, kits/rtt-002/music_rtt002.json as the model) with a new kits/rtt-003 music config: the track is 4:46 and the film is about 5:08, so loop it with beat-aligned crossfades at a musically sensible point (report where the joins fall), fade out over the 10 s final table, mix to -16 LUFS integrated with true peak ≤ -1 dBTP. Do not change the RTT-002 music settings or files.

FULL FILM: render the full RTT-003 film with the approved round-5 design and data, with the music, the same way the RTT-002 final film was made (master 3840 × 2160 plus a 1920 × 1080 viewing copy), started by hand, to a PRIVATE pre-release in the private repo with the SHA-256 of both files. Run all RTT-003 and RTT-002 tests first and report them. Check the film for flashing against the WCAG 2.x thresholds as was done for RTT-002 (reports/RTT-002_wcag_flash_check.md) and report. Report length, loudness, true peak and the loop-join times.

Nothing is uploaded to YouTube or published. Luke approves the exact final render by its SHA-256 (principle 18). Update PR #13's description, state and handover. Do not merge. Finish with a short plain-English summary for Luke, including where to watch.
