# Race Through Time

Code, configuration, metric contracts and open-licence datasets for the Race Through Time YouTube channel (@racethroughtime).

## Public-repo rules (DECISIONS.md, DEC-006, 27 Sep 2026)

This repository is **public**. Anything committed here is publicly redistributed.

**Commit only:** code, configs, metric contracts, and open-licence datasets with their attribution.

**Never commit:**
- licensed data (for example Official Charts, CTBUH, Jolpica/Ergast);
- music, or logos/images without redistribution rights;
- credentials, tokens or secrets of any kind;
- unreleased masters (draft or finished renders).

**Also:**
- Renders are saved only as **private pre-releases** in `marketmarathon/race-through-time-private`, with a SHA-256 for every file (DEC-060, DEC-061). Nothing is uploaded to YouTube or published from this repo; Luke approves the exact file by its SHA-256 (DEC-078) and, for now, uploads it by hand (DEC-080).
- Workflows in this repo upload **no workflow artifacts** and use no cache (DEC-061).
- The full rules for every Claude Code session are in [`CLAUDE.md`](CLAUDE.md).
- Licensed audio is pulled at render time from private storage, as Market Marathon already does.
- Private research inputs (for example independent-check files) stay outside this repo; only their SHA-256 hash and validation results are recorded here.

## Layout

- `state/` — the canonical record: STATE.json, DECISIONS.md, HANDOVER.md.
- `reference/` — environment audit, capability matrix, reconciliation, feasibility notes, metric contracts.
- `prompts/` — session and independent-check prompts.

Market Marathon lives separately in `marketmarathon/bars` and is not changed from here.
