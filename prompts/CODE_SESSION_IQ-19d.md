IQ-19d: Cowork's review of round 2 and two changes (9 Oct 2026)

Save this message word for word as prompts/CODE_SESSION_IQ-19d.md. Record Luke's answers as Owner DECs from DEC-562, and your own choices as Claude DECs after them (RTT-102 block, below DEC-600). Same branch and pull request #23. Do not merge.

Cowork reviewed rtt-102-round2-1a8e17e-run2 in Luke's Chrome (both sheets; the Aug 2024, Oct 2025 and Aug 2026 stills; one phone copy). Right as built: title and the line under it; fix (a) (the note shows only while stripes do, and Sep 2024 lands with neither); fix (b); the drop-out lines; held bars. The panel's sums match series_monthly.csv (Feb 2025 5.127bn, Oct 2025 8.346bn, Jan 2026 8.312bn, Aug 2026 9.867bn).

1. Eased motion through every month of the data. Luke: yes ("yes, to both. Looking really good").
- Today the monotone cubic runs through the published figures only. So on the landing frames of in-between months, the board shows values that are not in series_monthly.csv. Some sit up to about 22% away from its straight-line values.
- Cowork's PCHIP check reproduces the stills exactly. Examples:
  - Claude Feb 2024: ~31m vs 39.3m.
  - Perplexity Feb 2023: ~7.3m vs 9.4m.
  - Copilot Feb 2025: ~89m vs 80.4m. The fixes sheet's own caption says "~80m".
  - Gemini Aug 2024: ~260m vs 278.3m.
- In all, 32 of the 83 in-between months differ by more than 5%.
- Change: keep the monotone cubic (no overshoot), but use every month in series_monthly.csv, published and interpolated, as its knots. Every landing frame then equals the data file, and the motion stays smooth.
- Then:
  - extend "values = series_monthly.csv on every landing frame" to the eased film and the clip, and the panel test to every landing frame;
  - report whether any month-end order still differs from the straight-line film (DEC-539's Dec 2024 Copilot/Claude swap should go);
  - keep DEC-557's two-significant-figure rule.
- Drawing only; no figure changes.

2. A taller line in the combined panel. Luke: yes (same reply).
- The line is about 20 px tall, so its roughly 37-fold rise (0.27bn in Dec 2022 to 9.9bn in Aug 2026) looks almost flat, especially on a phone.
- Make the line about three times taller (around 60–70 px). Grow the panel upwards into the empty space above it, without covering a bar or value label on any frame.
- Keep the number, label, axis years, arrival dots and bottom line as they are.
- Put this behind an RTT-102 config key, so RTT-103's approved panel stays pixel-identical.

3. Output
- Re-render with phone copies: Feb 2024 (new), Aug 2024, Feb 2025, Oct 2025 and Aug 2026, plus the clip from Oct 2024 to the end.
- Put them in a new private pre-release with every SHA-256.
- Run the RTT-102 tests, the phone check, the WCAG flash check on the clip, and the pixel comparison for RTT-001/002/003/103.
- Give the running time if it changes.
- No music and no full film yet.

4. Report
- Questions for Luke only on anything new.
- End with a short plain-English summary for Luke.
