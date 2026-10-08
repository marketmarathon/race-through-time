DEC number clash (found by Cowork 8 Oct; fix agreed by Luke 8 Oct, Cowork chat). DEC-278, DEC-279 and DEC-280 on your branch (IQ-15d working choices and findings, 8 Oct 06:54 UTC) are also used on PR #20 (RTT-103, branch claude/gracious-meitner-aedj37) for Luke's owner decisions recorded on 7 Oct 23:23 UTC. PR #20 keeps them.

Please:
1. Renumber your three to DEC-400, DEC-401 and DEC-402, and update every reference to them (DECISIONS.md, STATE.json, HANDOVER.md, reports/RTT-101_data_report.md, the metric contract, data and source files, tests). Old commit messages stay as they are; note the renumbering in DECISIONS.md.
2. From now on use only your own block, DEC-403 to DEC-499 (Luke, 8 Oct). IQ-16 (RTT-103) uses up to DEC-399 and records the block rule as an owner DEC; IQ-17 (RTT-102, starting today) uses DEC-500 onwards. Note the block in your HANDOVER.
3. If practical, add a check that fails when a DEC number in your DECISIONS.md is used with different content on another open branch; if not, list it as a manual step in HANDOVER.

If you are part-way through a step (e.g. source round 1 list B), finish that step first. Rebuild, run the checks, push to the PR #19 branch, do not merge, and give Luke a short plain-English summary.
