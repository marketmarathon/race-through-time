# Pack v2.0 vs the working system — reconciliation
Status labels: AGREES · CONFLICT · GAP. "Recommendation" = Claude's proposal, not a decision.

1. **Renderer** — AGREES. Pack says keep the 4K canvas pipeline; C2-2 is exactly that. GAP for RTT: integer counts that step on event dates, non-currency units, no flags. Recommendation: copy the C2-2 player to `player_rtt.html` with an RTT config inside an RTT kit. C2-2 files are not edited, so Market Marathon's pixel baseline cannot move.
2. **Repo layout** — CONFLICT (mild). Pack sketches episodes/, state/, reports/; the repo is a flat root of zipped kits plus one workflow per kit. Recommendation: do not restructure Market Marathon. Where RTT lives is decision D-02.
3. **Public repo vs licensed data** — CONFLICT. Pack requires a rights ledger; anything committed here is publicly redistributed. Recommendation: RTT kits in a public repo may contain only data whose licence allows redistribution; everything else goes to private storage. Part of D-02.
4. **Release approval** — AGREES. Pack forbids an agent-editable approval flag. Your existing practice (private upload, you publish by hand in Studio) already meets that. Recommendation: for launch, RTT uses the same gate — you schedule each approved video yourself in Studio. Automate only later, behind a protected GitHub environment with a separate identity.
5. **Uploader** — GAP. `yt_upload.py` accepts `--privacy public` and does not read back the channel. Recommendation: an RTT uploader copy that cannot set public and refuses to upload unless the authorised channel ID matches RTT's. Prevents a Market Marathon token uploading RTT films to the wrong channel.
6. **Research method** — CONFLICT. Your standing Market Marathon rule: Claude writes a ChatGPT deep-research prompt, you run it, Claude parses. The pack has Claude build datasets from primary sources with independent checks. Decision D-03.
7. **Starter files** — GAP. STATE.json, HANDOVER.md, skills and task prompts from the pack are not in the project. Fresh STATE/DECISIONS/HANDOVER were created; if the pack's templates are added later, merge into these rather than keep two.
8. **Identity / merger rules** — AGREES. Market Marathon lineage decisions stay as they are; each RTT contract sets its own identity policy.
9. **Cadence** — AGREES. No Market Marathon schedule found in the repo; nothing changed. RTT cadence remains a template until launch gates pass.
10. **Reporting** — AGREES. Pack schedules are inactive; none activated.
11. **Source register** — AGREES with the pack's caution. "Page retrieved" ≠ usable dataset: the first live licence check (Jolpica, for RTT-002) found a non-commercial licence.
