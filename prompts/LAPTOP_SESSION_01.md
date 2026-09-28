# Laptop session 01 kickoff (28 Sep 2026)
Paste into a new Claude session on the laptop that can work in the Claude Workspace folder.

---
You are continuing the Race Through Time (RTT) setup. Work only inside my Claude Workspace folder (confirm its real path; it should be C:\Users\luke\Desktop\Claude Workspace). Never touch the marketmarathon/bars repo or any Market Marathon files.

1. Find the Race Through Time folder and the rtt_bootstrap folder in it. Read HANDOVER.md, STATE.json, DECISIONS.md and metric_contract_RTT-002.md. They are the current record of decisions.

2. Capability check. Report before going further: can you run commands (for example git --version), and can you push to https://github.com/marketmarathon/race-through-time? Do not install software, change credentials or change any settings without asking me. If pushing is not possible, stop and explain in plain English what is missing.

3. Clone marketmarathon/race-through-time (public, currently empty) into Claude Workspace\race-through-time. Make the first commit on main with state/ (STATE.json, DECISIONS.md, HANDOVER.md), reference/ (environment_audit.md, capability_matrix.md, reconciliation.md, feasibility_first12.md, metric_contract_RTT-002.md), prompts/, and a short README stating the public-repo rules in DECISIONS.md DEC-006. Push it and confirm the commit is visible on GitHub.

4. Find the ChatGPT deep-research output for RTT-002 in the Race Through Time Data folder. Do not put it in the public repo. Validate it: sections A to G present; every row has a source_url; list every NOT FOUND item; check internal consistency (each season's wins in B add up to its rounds, allowing for shared drives; B totalled per driver matches F; the G seasons match B). Record the file's SHA-256 hash and the validation results in state/ so the check is frozen.

5. If steps 2 to 4 pass, build the RTT-002 dataset (IQ-03) on a new branch rtt-002-data, not main. Follow metric_contract_RTT-002.md v0.2: race-by-race winners from 1950 to the last completed Grand Prix, sourced from Wikipedia (CC BY-SA 4.0), recording page URL, revision ID and retrieval time for every row; never scrape formula1.com and never use Jolpica data. Build the cumulative wins table with whole numbers only. Run scripted checks, then compare against the frozen ChatGPT check (B, E, F and G). Write a discrepancy report. Do not resolve disagreements by averaging or guessing; list them for me. Commit the dataset with an attribution file, push the branch, and read it back from GitHub.

6. Stop and report in plain English: what ran, what passed, what failed, the discrepancy list, and any decision you need from me. Update HANDOVER.md and STATE.json before stopping. Do not render, upload or publish anything.
---
