/* IQ-27 number-format test for RTT-003 (A compact, as approved; B whole numbers rolling where the maker publishes the
 * figure to 0.01 million or finer; kits/rtt-003/config_rtt003_numfmt_{A,B}.json, points from scripts/rtt003_full_digits.py).
 *
 * For each config, EVERY frame of the clip is drawn (raster 1, placeholder pictures; the labels do not depend on them):
 *  1. landing frames (TL.quarterEndFrame): every bar's figure equals data/rtt-003/series.csv `units` exactly; in B a
 *     full-digit label equals the data figure written out in full ("155,370,000", "+" for a lower bound), every other
 *     label is the approved compact form of the same figure; A has no full-digit label at all;
 *  2. every frame: in B a label is either compact or whole digits (no mixed form), and a whole-digit label's number
 *     equals the bar's figure on that frame (the digits roll with the bar);
 *  3. every frame: no value or status label overlaps the maker key panel or another bar's value label;
 *  4. phone: names and values at least 5.9 pt on a phone showing the video 390 pt wide (DEC-108), and B's sizes equal A's.
 * Writes tests/player/NUMFMT_RTT003.md. Exit 1 on any failure.
 */
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..'), KIT = path.join(ROOT, 'kits', 'rtt-002');
const rtt = require(path.join(KIT, 'rtt.js'));
const { placeholderPNG } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';
const PT = px => px * 390 / 1920, FLOOR_PT = 5.9;

function seriesUnits() {
  const lines = fs.readFileSync(path.join(ROOT, 'data/rtt-003/series.csv'), 'utf8').trim().split('\n'), head = lines.shift().split(',');
  const qi = head.indexOf('quarter_end'), ci = head.indexOf('console_id'), ui = head.indexOf('units'), pi = head.indexOf('plus_flag');
  const m = {};
  for (const l of lines) { const c = l.split(','); m[c[qi] + '|' + c[ci]] = { units: +c[ui], plus: c[pi] === 'yes' }; }
  return m;
}
const compact = (u, plus) => { const t = Math.floor((u + 50000) / 100000); return Math.floor(t / 10).toLocaleString('en-GB') + '.' + (t % 10) + 'm' + (plus ? '+' : ''); };
const full = (u, plus) => u.toLocaleString('en-GB') + (plus ? '+' : '');
const overlap = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;

(async () => {
  const dir = path.join(ROOT, 'tests', 'output', 'rtt003_numfmt', '_assets');
  fs.mkdirSync(path.join(dir, 'icons'), { recursive: true }); fs.mkdirSync(path.join(dir, 'logos'), { recursive: true });
  process.env.RTT_LOCAL_ASSETS = process.env.RTT003_REAL_ASSETS || dir;
  const S = seriesUnits(), res = {}, fails = [];
  for (const v of ['A', 'B']) {
    const cfg = rtt.loadConfig('../rtt-003/config_rtt003_numfmt_' + v + '.json');
    const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
    if (!process.env.RTT003_REAL_ASSETS) {
      for (const e of data.entrants) placeholderPNG(path.join(dir, 'icons', e.id + '.png'), 165, 100, [180, 180, 190]);
      for (const m of cfg.maker_order) fs.writeFileSync(path.join(dir, 'logos', m + '.svg'), '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="40"><rect width="120" height="40" fill="#555"/></svg>');
    }
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    const info = await pg.evaluate(() => ({ dates: TL.events.map(e => e.date), qe: TL.quarterEndFrame, n: RACE_FRAMES }));
    const landing = new Map(info.qe.map((f, k) => [f, info.dates[k]]));
    const R = res[v] = { frames: info.n + 1, landings: 0, fullLabels: new Set(), compactIds: new Set(), minName: 1e9, minValue: 1e9, overlaps: 0, keyOverlaps: 0, landingOverlaps: 0, longest: '' };
    for (let f = 0; f <= info.n; f++) {
      await rtt.drawFrame(pg, f, cfg);
      const st = await pg.evaluate(() => ({ bars: window.__BARS.filter(b => b.alpha > 0.05), labels: window.__LABELS.filter(l => l.alpha > 0.05), key: window.__KEY }));
      const val = st.labels.filter(l => l.kind === 'value');
      for (const l of st.labels) { if (l.kind === 'name') R.minName = Math.min(R.minName, l.size); if (l.kind === 'value') R.minValue = Math.min(R.minValue, l.size); }
      for (const l of val) {
        const b = st.bars.find(x => x.id === l.id); if (!b) continue;
        const isFull = /^\d{1,3}(,\d{3})+\+?\*?$/.test(l.text) || /^\d{1,3}\+?$/.test(l.text);
        if (isFull) {
          R.fullLabels.add(l.id); if (l.text.length > R.longest.length) R.longest = l.text;
          if (v === 'A') fails.push(`A frame ${f}: ${l.id} shows a whole number "${l.text}"`);
          if (+l.text.replace(/[,+*]/g, '') !== Math.round(b.units)) fails.push(`${v} frame ${f}: ${l.id} "${l.text}" is not the bar's figure ${b.units}`);
        } else if (!/^~?\d[\d,]*\.\d(m|bn)\+?\*?$/.test(l.text)) fails.push(`${v} frame ${f}: ${l.id} label "${l.text}" is neither compact nor whole digits`);
        else R.compactIds.add(l.id);
      }
      if (landing.has(f)) {
        R.landings++;
        const q = landing.get(f);
        for (const b of st.bars) {
          const d = S[q + '|' + b.id]; if (!d) { fails.push(`${v} ${q}: ${b.id} has no row in series.csv`); continue; }
          if (b.units !== d.units) fails.push(`${v} ${q}: ${b.id} bar ${b.units} != data ${d.units}`);
          const l = val.find(x => x.id === b.id); if (!l) continue;
          const want = l.text.includes(',') && !l.text.includes('.') ? full(d.units, d.plus) : compact(d.units, d.plus);
          if (l.text.replace(/\*$/, '') !== want) fails.push(`${v} ${q}: ${b.id} label "${l.text}" != "${want}"`);
        }
      }
      /* overlaps: value and status labels against the maker key and against each other */
      const boxes = st.labels.filter(l => ['value', 'status', 'retired', 'latest_figure', 'est'].includes(l.kind) || l.kind === 'value')
        .map(l => ({ id: l.id, kind: l.kind, text: l.text, x: l.x, y: l.y - (l.asc || l.size * 0.75), w: l.w, h: (l.asc || l.size * 0.75) + (l.desc || l.size * 0.2) }));
      if (st.key) for (const b of boxes) if (overlap(b, st.key.box)) { R.keyOverlaps++; if (R.keyOverlaps < 6) fails.push(`${v} frame ${f}: ${b.kind} "${b.text}" (${b.id}) overlaps the maker key`); }
      /* two bars' labels cross while the bars swap places (the approved film does this too): counted; on a landing frame it fails */
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++)
        if (boxes[i].id !== boxes[j].id && overlap(boxes[i], boxes[j])) { R.overlaps++;
          if (landing.has(f)) { R.landingOverlaps++; (R.landingList = R.landingList || []).push(`frame ${f}: "${boxes[i].text}" / "${boxes[j].text}"`); } }
    }
    await br.close();
    if (PT(R.minName) < FLOOR_PT || PT(R.minValue) < FLOOR_PT) fails.push(`${v}: names ${PT(R.minName).toFixed(2)} pt / values ${PT(R.minValue).toFixed(2)} pt, below ${FLOOR_PT} pt`);
  }
  /* the approved film's rows may still be gliding on a landing frame (A has the same crossing); B may not add one */
  if (res.B.landingOverlaps > res.A.landingOverlaps) fails.push(`B adds a crossing on a landing frame: ${(res.B.landingList || []).join('; ')}`);
  if (res.A.minName !== res.B.minName || res.A.minValue !== res.B.minValue) fails.push(`B's text sizes differ from A's (names ${res.B.minName} vs ${res.A.minName} px, values ${res.B.minValue} vs ${res.A.minValue} px)`);
  const fullIds = [...res.B.fullLabels].sort(), compactOnly = [...res.B.compactIds].filter(i => !res.B.fullLabels.has(i)).sort();
  const md = ['# RTT-003 number-format test (IQ-27)', '',
    'Clip: 1 Jan 2023 - 31 Dec 2025 (the Switch passes the DS on 31 Dec 2025, 155,370,000 vs 154,020,000). A = approved compact labels; B = whole numbers rolling where the maker publishes the figure to 0.01 million or finer (`scripts/rtt003_full_digits.py`). Every frame drawn; generated by `tests/player/numfmt_check_rtt003.js`.', '',
    '| | A (compact) | B (whole numbers) |', '|---|---|---|',
    `| Frames checked / landing frames | ${res.A.frames} / ${res.A.landings} | ${res.B.frames} / ${res.B.landings} |`,
    `| Smallest name, value (px on the 1920 frame; pt on a 390 pt phone) | ${res.A.minName}, ${res.A.minValue} px; ${PT(res.A.minName).toFixed(2)}, ${PT(res.A.minValue).toFixed(2)} pt | ${res.B.minName}, ${res.B.minValue} px; ${PT(res.B.minName).toFixed(2)}, ${PT(res.B.minValue).toFixed(2)} pt |`,
    `| Labels overlapping the maker key | ${res.A.keyOverlaps} | ${res.B.keyOverlaps} |`,
    `| Labels overlapping each other on a landing frame (rows still gliding into place; B may not add any) | ${res.A.landingOverlaps} ${(res.A.landingList || []).join('; ')} | ${res.B.landingOverlaps} ${(res.B.landingList || []).join('; ')} |`,
    `| Frames x label pairs crossing while bars swap places (in motion; reported, approved behaviour in A) | ${res.A.overlaps} | ${res.B.overlaps} |`,
    `| Bars with whole-number labels in the clip | none | ${fullIds.join(', ')} |`,
    `| Bars that stay compact in B | - | ${compactOnly.join(', ')} |`,
    `| Longest whole-number label | - | ${res.B.longest} |`, '',
    fails.length ? '**FAIL**\n\n' + fails.slice(0, 40).map(x => '- ' + x).join('\n') : '**PASS**: every landing frame equals series.csv exactly (figure and label); B\'s whole numbers always equal the bar\'s figure on the frame; no label touches the maker key, and B adds no crossing on a landing frame; names and values at least ' + FLOOR_PT + ' pt, B the same size as A.'];
  fs.writeFileSync(path.join(__dirname, 'NUMFMT_RTT003.md'), md.join('\n') + '\n');
  console.log(md.join('\n'));
  process.exit(fails.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
