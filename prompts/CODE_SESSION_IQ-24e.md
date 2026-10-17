# IQ-24e — RTT-104 V3: Luke's answers, continent colours and a slower pace (one more clip round, then the film)

v1, 17 Oct 2026 (Cowork). Continue in this session on the same branch and pull request #24 (next DEC after DEC-679; check). Luke is not technical: finish with a short plain-English summary. Keep it lean.

First, save this exact prompt as `prompts/CODE_SESSION_IQ-24e.md`.

## Owner decisions to record (Luke, Cowork, 17 Oct 2026 10:36 BST)
1. **Board:** 20 rows.
2. **Tag look:** the filled amber tag.
3. **Tag rule:** (a), changes of 5 points or more only.
4. **Scale:** fixed 0–70%. Luke took Claude's recommendation.
5. **Late-year elections:** untagged for now. Luke took Claude's recommendation.
6. **NEW: colour the bars by continent.** Luke: "them all being blue is quite boring."
7. **NEW: slower.** Luke: the clip "moves way too quickly … it needs to move slower, so that we can … follow the movement."

## Round: one still sheet and two clips (no full film yet)
Items 6 and 7 are a new visual feature and a pace change (DEC-069), so show them before the film.

a. **Continent colours.**
   - Use the UN M49 regions: Africa, Americas, Asia, Europe, Oceania. Record the source, and its licence basis, in the rights ledger.
   - Choose 5 colours that are easy to tell apart, readable with the dark text on the bar, safe for colour-blind viewers, and clearly different from the amber election tag.
   - Add a small legend in a corner that is already empty (not over the world-average panel).
   - Show one still sheet: 2019 with the tags, plus its phone copy.
   - If a country's continent is ambiguous (e.g. Türkiye), use its M49 region, then list it for Luke.
b. **Pace.** Two clips of the same 2016–2020 stretch with rule (a), continent colours and tags:
   - one at **4.5 s per year**;
   - one at **6 s per year**.

   Tags stay on screen proportionally longer, at least 2.5 s. Keep the smooth motion (DEC-654/655). Give the estimated running time of the full film at each pace.

   Run a WCAG flash check on both clips.

## Checks
- Values equal the data.
- Tags map to VERIFIED rows.
- The phone check still passes with the colours.
- V2 is byte-identical to c379631.

Put the files in a PRIVATE pre-release, with a SHA-256 for each. Update `state/`, push to pull request #24, and do not merge.

## Questions for Luke (numbered; give your recommendation and the default for each)
1. Continent colours as shown: yes, or change any?
2. Pace: 4.5 s or 6 s per year, or somewhere between?

When he answers, the next step is the full V3 film with its own configs and workflow, ending with the music, the 5 s final table and the credits as in V2.

Finish with the plain-English summary.
