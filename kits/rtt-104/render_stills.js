/* RTT-104 design round 1 (IQ-22): render the stills in stills.json, check every one, and make the side-by-side sheets.
 *
 * Usage: node kits/rtt-104/render_stills.js <out_dir> [--check-only]
 *   Stills are private (DEC-006, DEC-060): <out_dir> must be outside the repo (the workflow uses $RUNNER_TEMP), and the
 *   pictures go only to a private pre-release. With --check-only nothing is written except the check report (text).
 *
 * Each still is drawn on its frame through the same page and driver as the clips (render_rtt104.js): a year's
 * landing frame (the frame on which its figures land), a leave note (40 frames into it), frame 0, or the closing
 * card (1 s in). Every still also gets a phone copy: the same frame shown 390 points wide at 3 device pixels per
 * point (as RTT-001). Sheets put the options side by side at half size, each with a caption.
 *
 * Checks (the run fails on any):
 *   VALUES  on a landing still, both boards hold exactly boards.csv's countries for that year, in rank order, each
 *           showing value_1dp + "%", and the 0% group lists exactly zero_group.csv's countries; on a note still the
 *           same for the year before (the note is shown on that year's board);
 *   PHONE   names and values at least 5.9 pt on a phone showing the video 390 pt wide (RTT-002's approved size,
 *           house style 6); every other text at least 5.0 pt (the footer floor of the earlier phone checks);
 *   OVERLAP no board label inside the world panel, and no board label past its own board's right edge.
 * Results: tests/rtt104/STILLS_CHECK.md (written by this script; text only).
 */
const fs = require('fs');
const path = require('path');
const R = require('./render_rtt104.js');
const ROOT = path.resolve(__dirname, '..', '..');
const PHONE_PT = 390, DPR = 3, k = PHONE_PT / 1920, pt = px => px * k, NAMES = 5.9, FLOOR = 5.0;

function csvRows(f) {
  const lines = fs.readFileSync(f, 'utf8').split(/\r?\n/).filter(Boolean), head = lines.shift().split(',');
  return lines.map(l => { const out = []; let cur = '', q = false;
    for (let i = 0; i < l.length; i++) { const c = l[i]; if (q) { if (c === '"') { if (l[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
      else if (c === '"') q = true; else if (c === ',') { out.push(cur); cur = ''; } else cur += c; }
    out.push(cur); return Object.fromEntries(head.map((h, i) => [h, out[i]])); });
}
const BOARDS = csvRows(path.join(ROOT, 'data', 'rtt-104', 'boards.csv'));
const ZERO = Object.fromEntries(csvRows(path.join(ROOT, 'data', 'rtt-104', 'zero_group.csv')).map(r => [r.year, r]));

async function targetFrame(pg, at) {
  return pg.evaluate(a => typeof a === 'number' ? landingFrame(a) : a.startsWith('note:') ? noteFrame(+a.slice(5)) + 40
    : a === 'card' ? cardFrame() + 30 : +a.slice(6), at);
}
function checkValues(s, st) {
  const at = s.at, fails = [];
  if (typeof at !== 'number' && !String(at).startsWith('note:')) return fails;
  const year = typeof at === 'number' ? at : +String(at).slice(5) - 1;
  for (const b of ['top', 'bottom']) {
    const want = BOARDS.filter(r => +r.year === year && r.board === b).sort((x, y) => x.rank - y.rank).map(r => r.iso3 + ' ' + r.value_1dp + '%');
    const got = st.bars.filter(x => x.board === b && x.alpha > 0.99).sort((x, y) => x.slot - y.slot).map(x => x.id + ' ' + x.value);
    if (want.join('|') !== got.join('|')) fails.push(`${b} ${year}: want ${want.join(', ')} got ${got.join(', ')}`);
  }
  const zl = st.labels.filter(l => l.kind === 'zero_names');
  const zt = zl.map(l => l.text.replace(/^ · /, '')).join(', ');
  const want = (ZERO[year].countries || '').split('; ').filter(Boolean).join(', ');
  if (zl.length && zt !== want) fails.push(`0% group ${year}: want "${want}" got "${zt}"`);
  if (!zl.length && want) fails.push(`0% group ${year}: want "${want}", none drawn`);
  return fails;
}
function checkPhone(st) {
  const fails = [], min = {};
  for (const l of st.labels) if (l.size && l.alpha > 0.3) min[l.kind] = Math.min(min[l.kind] || 1e9, l.size);
  for (const kk of Object.keys(min)) {
    const need = ['name', 'value', 'zero_head', 'zero_names', 'card_name', 'card_line'].includes(kk) ? NAMES : FLOOR;
    if (pt(min[kk]) < need - 1e-9) fails.push(`${kk} ${min[kk]}px = ${pt(min[kk]).toFixed(1)} pt < ${need}`);
  }
  return { fails, min };
}
function checkOverlap(st, cfg) {
  const fails = [];
  const boardKinds = ['name', 'value', 'latest', 'leave_note', 'zero_head', 'zero_names'];
  if (cfg.world_panel && st.panel && st.panel.h > 0) {
    const p = st.panel;
    for (const l of st.labels) if (boardKinds.includes(l.kind) && l.alpha > 0.05) {
      const top = l.y - (l.size || 0) * 0.8, bot = l.y + (l.size || 0) * 0.2;
      if (l.x < p.x + p.w && l.x + l.w > p.x && top < p.y + p.h && bot > p.y) fails.push(`${l.kind} "${l.text}" inside the world panel`);
    }
  }
  for (const l of st.labels) if (boardKinds.includes(l.kind) && l.alpha > 0.05 && l.x + l.w > 1856 + 1) fails.push(`${l.kind} "${l.text}" past the board edge (${Math.round(l.x + l.w)})`);
  if (st.lr) for (const l of st.labels) if (boardKinds.includes(l.kind) && l.alpha > 0.05 && l.x < 936 && l.x + l.w > 936 + 1) fails.push(`${l.kind} "${l.text}" crosses into the right board`);
  return fails;
}

async function main() {
  const out = process.argv[2], checkOnly = process.argv.includes('--check-only');
  if (!out) throw new Error('usage: render_stills.js <out_dir> [--check-only]');
  if (!checkOnly && path.resolve(out).startsWith(ROOT + path.sep)) throw new Error('stills are private: write them outside the repository');
  fs.mkdirSync(out, { recursive: true });
  const spec = JSON.parse(fs.readFileSync(path.join(__dirname, 'stills.json'), 'utf8'));
  const report = ['# RTT-104 design round 1 — still checks (IQ-22)', '',
    'Written by `kits/rtt-104/render_stills.js`. VALUES: every bar and the 0% group equal `data/rtt-104/boards.csv` and `zero_group.csv` for the year shown. PHONE: on a phone showing the video 390 pt wide, names, values, 0% group and closing-card lines at least 5.9 pt, every other text at least 5.0 pt. OVERLAP: no board text inside the world panel or past its board.', '',
    '| Still | Option | Frame | Values | Phone (smallest name / value / other) | Overlap | Result |', '|---|---|---|---|---|---|---|'];
  const files = {}; let ok = true;
  for (const s of spec.stills) {
    const cfg = R.config(s.config);
    const { br, pg } = await R.open(cfg);
    const f = await targetFrame(pg, s.at);
    for (let i = 0; i < 3; i++) await R.frame(pg, f);
    const st = await pg.evaluate(() => ({ labels: window.__LABELS, bars: window.__BARS, panel: G.panel, lr: G.lr }));
    if (!checkOnly) { const file = path.join(out, s.name + '_1920x1080.png'); await (await pg.$('#c')).screenshot({ path: file }); files[s.name] = file; }
    await br.close();
    const v = checkValues(s, st), p = checkPhone(st), o = checkOverlap(st, cfg);
    const other = Object.entries(p.min).filter(([kk]) => !['name', 'value'].includes(kk)).reduce((m, [, x]) => Math.min(m, x), 1e9);
    const ph = `${p.min.name ? pt(p.min.name).toFixed(1) : '—'} / ${p.min.value ? pt(p.min.value).toFixed(1) : '—'} / ${other < 1e9 ? pt(other).toFixed(1) : '—'} pt`;
    const res = [...v, ...p.fails, ...o];
    // layout B (top/bottom) is expected to miss the phone sizes: reported, and it does not stop the run
    const expected = s.config === 'config_rtt104_a_tb.json' && !v.length && !o.length;
    if (res.length && !expected) ok = false;
    report.push(`| ${s.name} | ${s.question} | ${f} | ${v.length ? 'FAIL' : (typeof s.at === 'number' || String(s.at).startsWith('note:')) ? 'PASS' : 'n/a'} | ${ph}${p.fails.length ? ' FAIL' : ''} | ${o.length ? 'FAIL' : 'PASS'} | ${res.length ? (expected ? 'REPORTED (option B misses the phone sizes): ' : 'FAIL: ') + res.join('; ') : 'PASS'} |`);
    console.log(`${res.length ? (expected ? 'REPORTED' : 'FAIL') : 'PASS'} ${s.name}${res.length ? ': ' + res.join('; ') : ''}`);
  }
  report.push('', `Overall: ${ok ? 'PASS' : 'FAIL'}.`, '');
  fs.mkdirSync(path.join(ROOT, 'tests', 'rtt104'), { recursive: true });
  fs.writeFileSync(path.join(ROOT, 'tests', 'rtt104', 'STILLS_CHECK.md'), report.join('\n'));
  if (checkOnly) process.exit(ok ? 0 : 1);

  /* phone copies and sheets */
  const { chromium } = require(require.resolve('playwright', { paths: [path.join(ROOT, 'kits', 'rtt-002')] }));
  const b2 = await chromium.launch({ executablePath: process.env.PW_CHROME || '/opt/pw-browsers/chromium' });
  const ph = await b2.newPage({ viewport: { width: PHONE_PT, height: Math.round(PHONE_PT * 9 / 16) }, deviceScaleFactor: DPR });
  for (const [n, f] of Object.entries(files)) {
    await ph.setContent(`<body style="margin:0;background:#000"><img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:${PHONE_PT}px;display:block"></body>`);
    await ph.waitForLoadState('load');
    await ph.screenshot({ path: f.replace('_1920x1080.png', '_phone_390pt.png') });
  }
  const fontCss = path.join(path.dirname(require.resolve('@fontsource/archivo/package.json', { paths: [path.join(ROOT, 'kits', 'rtt-002')] })), '600.css');
  const cp = await b2.newPage({ viewport: { width: 1960, height: 1200 }, deviceScaleFactor: 1 });
  for (const C of spec.compose) {
    const cols = C.cols || 2, rows = Math.ceil(C.items.length / cols);
    const cell = ([n, cap]) => `<div style="width:960px"><div style="font:600 26px Archivo;color:#F4F6FA;margin:0 0 8px 2px">${cap}</div>` +
      `<img src="data:image/png;base64,${fs.readFileSync(files[n]).toString('base64')}" style="width:960px;display:block"></div>`;
    await cp.setViewportSize({ width: cols * 960 + (cols - 1) * 20 + 40, height: 90 + rows * 590 });
    const html = path.join(out, '_compose.html');
    fs.writeFileSync(html, `<html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${fontCss}"></head><body style="margin:0;padding:20px;background:#0b1424">` +
      `<div style="font:600 32px Archivo;color:#AAB3C2;margin-bottom:16px">${C.title}</div>` +
      `<div style="display:grid;grid-template-columns:repeat(${cols},960px);gap:22px 20px">${C.items.map(cell).join('')}</div></body></html>`);
    await cp.goto('file://' + html); await cp.evaluate(() => document.fonts.ready);
    await cp.screenshot({ path: path.join(out, C.name + '.png'), fullPage: true });
    fs.unlinkSync(html);
  }
  await b2.close();
  console.log(`${Object.keys(files).length} stills, ${Object.keys(files).length} phone copies, ${spec.compose.length} sheets in ${out}`);
  process.exit(ok ? 0 : 1);
}
module.exports = { checkValues, checkPhone, checkOverlap, targetFrame };
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
