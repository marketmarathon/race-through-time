IQ-19h: bring pull request #23 up to date with main (10 Oct 2026)

Save this message word for word as prompts/CODE_SESSION_IQ-19h.md. Same branch, same pull request #23. Do not merge anything into main.

1. Why
- Luke has merged PR #18 and PR #22 into main (merge commit 7705838).
- Cowork ran a trial merge. PR #23 now conflicts with main in three files only: state/DECISIONS.md, state/HANDOVER.md and state/STATE.json.
- PR #23 already contains PR #21's branch (b04f33a). Once #23 is up to date, Luke can merge #23 on its own, and #21 should then show as merged.
- The RTT-102 video is uploaded as Private on YouTube. Its description points to data/rtt-102 on GitHub, so it waits for this merge before going public.

2. What to do
- Merge origin/main into claude/relaxed-clarke-9e0sqq.
- In the three state files, keep both sides:
  - every DEC from main and from this branch, in number order, none dropped or renumbered;
  - HANDOVER and STATE covering RTT-103 as on main and RTT-102 as on this branch.
- Check that no DEC number appears twice.
- Before pushing, check the workflow triggers. If the push would start any render or film workflow, stop and say so instead of pushing. Do not touch rtt102_film.yml.
- Run the RTT-102 tests and the pixel comparison for the approved films (RTT-001, 002, 003, 103). No render.
- Push, then confirm that GitHub shows PR #23 with no conflicts.
- Check whether the private repo's branch claude/relaxed-clarke-9e0sqq (the RTT-102 logos) still needs merging there, and whether it can be merged as it is.
- No new owner decision. Record a Claude DEC only if you have to make a choice.

3. Report
- A one-line confirmation with the commit.
- Then tell Luke in plain English:
  - which pull requests to merge now, in which repo and in what order;
  - whether #21 needs anything after #23 is merged.
