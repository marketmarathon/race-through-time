/* RTT-103 phone check (IQ-18, design round 1). For each still in kits/rtt-103/stills.json (board stills and the steps
 * drawn by steps.js; compositions are left out) the frame is drawn exactly as render_stills.js draws it, and every
 * label's size is measured and converted to points on a phone showing the landscape video 390 points wide (as
 * phone_check_rtt001.js). Pass/fail:
 *   - names and values at least 5.9 pt (RTT-002's approved size, house style 6, DEC-108);
 *   - on boards, the axis numbers and the date at least the names;
 *   - every other label (footer, notes, tags, story moments, the running total, step text) at least 5.0 pt.
 * The logo tile is reported (points on the phone), with no threshold. Placeholder logos (tests/placeholders.js).
 * IQ-18b (Cowork fix (h)): every still dated with a quarter (`at`) must show that quarter's figures exactly as the master
 * gives them (the still is taken on the frame where they land, never mid-move), and its date block that quarter.
 * IQ-18c: a still of a forward board (2026 plans, 2027-2030 estimates) shows that year's figures as the look-ahead file
 * gives them.
 * Output: tests/player/PHONE_RTT103.md. Exit 1 on any failure.
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const KIT = path.join(ROOT, 'kits', 'rtt-002');
const K103 = path.join(ROOT, 'kits', 'rtt-103');
const rtt = require(path.join(KIT, 'rtt.js'));
const ST = require(path.join(K103, 'render_stills.js'));
const { placeholderPNG, logoPlaceholders } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';
/* display rounding of the forward boards, as kits/rtt-002/rtt_steps.js bn() documents it (written out again here) */
function RTT_STEPS_bn(lo, hi, mode) {
  const big = mode === 'est' && Math.max(lo, hi) >= 1000, f = v => { const t = Math.round(v * 10);
    if (big) return (Math.floor((t + 50) / 100) / 100).toFixed(2);
    if (mode === 'whole' || (mode === 'est' && v >= 10)) return String(Math.floor((t + 5) / 10));
    if (mode === 'est' || mode === 'actual') return (t / 10).toFixed(1);
    return t % 10 ? (t / 10).toFixed(1) : String(t / 10); };
  const a = f(lo), b = f(hi); return (mode === 'est' ? '~' : '') + '$' + (a === b ? a : a + '–' + b) + (big ? 'tn' : 'bn');
}
const PHONE_PT = 390, FLOOR = 5.0, NAMES = 5.9, k = PHONE_PT / 1920, pt = px => px * k;

(async () => {
  const only = process.argv.slice(2);
  const dir = path.join(ROOT, 'tests', 'output', 'rtt103_phone', '_assets'); fs.mkdirSync(dir, { recursive: true });
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  const stills = JSON.parse(fs.readFileSync(path.join(K103, 'stills.json'), 'utf8')).stills.filter(s => !s.compose && (!only.length || only.includes(s.name)));
  const D = path.join(ROOT, 'data', 'rtt-103'), MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const rowsM = fs.readFileSync(path.join(D, 'AI_SPENDING_RACE_MASTER.csv'), 'utf8').trim().split('\n'), H = rowsM.shift().split(',');
  const byDate = {}; for (const l of rowsM) { const v = l.split(','); const r = Object.fromEntries(H.map((h, i) => [h, v[i]])); (byDate[r.date] = byDate[r.date] || {})[r.company.toLowerCase()] = r.capex_TTM_usd; }
  const LOOK = (() => { const t = fs.readFileSync(path.join(D, 'AI_SPENDING_RACE_LOOKAHEAD.csv'), 'utf8').trim().split('\n'), h = t.shift().split(',');
    return t.map(l => { const v = l.match(/("([^"]|"")*"|[^,]*)(,|$)/g).map(x => x.replace(/,$/, '').replace(/^"|"$/g, '').replace(/""/g, '"')); return Object.fromEntries(h.map((k, i) => [k, v[i]])); }); })();
  const moneyText = d => { const t = (BigInt(d) + 50000000n) / 100000000n; return '$' + Number(t / 10n).toLocaleString('en-GB') + '.' + (t % 10n) + 'bn'; };
  const out = ['# RTT-103 phone check (IQ-18 round 1, IQ-18b round 2, IQ-18c round 3)', '', `Each still measured as drawn on the 1920 frame and converted to points on a phone showing the video ${PHONE_PT} points wide. Names and values at least ${NAMES} pt; on boards the axis and the date at least the names; every other label at least ${FLOOR} pt. Logo tile: reported only.`, '',
               '| Still | Names | Values | Axis | Date | Smallest other label | Logo tile | Figures of the dated quarter | Result |', '|---|---|---|---|---|---|---|---|---|'];
  let ok = true;
  for (const s of stills) {
    const cfg = ST.stillConfig(s);
    logoPlaceholders(cfg, dir);
    const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
    process.env.RTT_LOCAL_ASSETS = dir;
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    delete process.env.RTT_LOCAL_ASSETS;
    const target = await ST.targetFrame(pg, s); for (let f = 0; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
    const S = await pg.evaluate(() => ({ L: window.__LABELS, P: window.__PICS }));
    await br.close();
    const vis = S.L.filter(l => l.alpha > 0.3 && l.size);
    const size = kinds => { const v = vis.filter(l => kinds.includes(l.kind)).map(l => l.size); return v.length ? Math.min(...v) : null; };
    const z = { name: size(['name']), value: size(['value']), axis: size(['axis']), date: size(['time_line', 'date_month', 'date_year']) };
    const others = vis.filter(l => !['name', 'value', 'axis', 'time_line', 'date_month', 'date_year'].includes(l.kind));
    const small = others.length ? others.reduce((a, b) => (b.size < a.size ? b : a)) : null;
    const fails = []; let figs = '—';
    const atD = s.at === 'final' ? Object.keys(byDate).sort().pop() : s.at;   // the final table is the last quarter's board
    if (atD && !byDate[atD]) {   // IQ-18c: a forward board - its figures as the look-ahead file gives them (rounding as rtt_steps.js bn())
      const y = atD.slice(0, 4), est = y !== '2026', bad = [];
      for (const r of LOOK.filter(r => r.frame_year === y && r.row_type !== 'COMBINED')) { const id = r.company.toLowerCase(), citi = r.row_type === 'CITI_ESTIMATE' || r.label === 'Citi estimate';
        const w = (!est && id === 'microsoft' ? '~' : '') + RTT_STEPS_bn(+r.estimate_low_usd_bn, +r.estimate_high_usd_bn, est ? (citi ? 'actual' : 'est') : (r.label === 'actual' ? 'actual' : 'plan'));
        const l = vis.find(l => l.kind === 'value' && l.id === id); if (!l || l.text !== w) bad.push(id + ' ' + (l ? l.text : 'missing') + ' (file ' + w + ')'); }
      const yl = vis.find(l => l.kind === 'date_year'); if (!yl || yl.text !== y) bad.push('date ' + (yl && yl.text));
      figs = bad.length ? 'FAIL: ' + bad.join('; ') : 'look-ahead ' + y + ' = file'; if (bad.length) fails.push('figures not those of ' + y);
    } else if (atD) { const fig = byDate[atD], bad = [];   // Cowork fix (h)
      for (const [id, d] of Object.entries(fig)) { const l = vis.find(l => l.kind === 'value' && l.id === id); if (!l || l.text !== moneyText(d)) bad.push(id + ' ' + (l ? l.text : 'missing') + ' (master ' + moneyText(d) + ')'); }
      for (const l of vis) if (l.kind === 'value' && !(l.id in fig)) bad.push(l.id + ' drawn with no figure');
      const ml = vis.find(l => l.kind === 'date_month'), yl = vis.find(l => l.kind === 'date_year');
      if (!ml || ml.text !== '12 months to ' + MON[+atD.slice(5, 7) - 1] || !yl || yl.text !== atD.slice(0, 4)) bad.push('date ' + (ml && ml.text) + ' ' + (yl && yl.text));
      figs = bad.length ? 'FAIL: ' + bad.join('; ') : Object.keys(fig).length + ' figures = master ' + atD;
      if (bad.length) fails.push('figures not those of ' + atD); }
    for (const kk of ['name', 'value']) if (z[kk] != null && pt(z[kk]) < NAMES) fails.push(kk + ' < ' + NAMES + ' pt');
    if (s.step == null && z.name != null) { if (!(z.axis >= z.name)) fails.push('axis < names'); if (z.date != null && !(z.date >= z.name)) fails.push('date < names'); }
    if (small && pt(small.size) < FLOOR) fails.push(small.kind + ' "' + small.text.slice(0, 30) + '" < ' + FLOOR + ' pt');
    ok = ok && !fails.length;
    const f = v => v == null ? '—' : `${v}px = ${pt(v).toFixed(1)} pt`;
    const p = (S.P || [])[0];
    out.push(`| ${s.name} | ${f(z.name)} | ${f(z.value)} | ${f(z.axis)} | ${f(z.date)} | ${small ? small.kind + ' ' + f(small.size) : '—'} | ${p ? `${p.box.w} x ${p.box.h} px = ${pt(p.box.w).toFixed(1)} x ${pt(p.box.h).toFixed(1)} pt` : '—'} | ${figs} | ${fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS'} |`);
    console.log(`${fails.length ? 'FAIL' : 'PASS'} ${s.name}${fails.length ? ': ' + fails.join('; ') : ''}`);
  }
  out.push('', `Overall: ${ok ? 'PASS' : 'FAIL'}. For reference: RTT-002's approved film draws names and values at 29 px = 5.9 pt; RTT-003's at 33 px = 6.7 pt.`, '');
  if (!only.length) fs.writeFileSync(path.join(__dirname, 'PHONE_RTT103.md'), out.join('\n'));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
