/* RTT-104 V3 design round (IQ-24d): render the stills in stills_v3.json with phone copies and sheets, and check them
 * and every frame of the V3 clips (clips_v3.txt).
 *
 * Usage: node kits/rtt-104/render_stills_v3.js <out_dir> [--check-only]
 *   Stills are private (DEC-006, DEC-060): <out_dir> must be outside the repo; with --check-only only the report is
 *   written. Phone copies and sheets as render_stills.js (390 pt wide at 3 device pixels per point).
 *
 * Checks (the run fails on any):
 *   VALUES  on a landing still, the bars in slot order are exactly the year's ranks 1-N with their one-decimal figure,
 *           read from data/rtt-104/v3_change_events.csv (new_rank, new_value_1dp; 1997 from old_rank, old_value_1dp),
 *           a file built separately from the player input (scripts/rtt104_v3_changes.py);
 *   TAGS    every tag drawn (stills and every clip frame) is a row of v3_change_events.csv with status VERIFIED, cause
 *           election or other, a source URL and a fetched excerpt, big under the config's rule (big_points = y for
 *           rule a, big = y for rule b), and its month and year are the row's first event date; it fits beside or on
 *           its bar; on a landing still every such row for a country on the board is drawn;
 *   PHONE   names, values and tags at least 5.9 pt on a phone (house style 6), other text at least 5.0 pt;
 *   OVERLAP no bar, name, value or tag inside the world panel or past the board's right edge (x 1856).
 * Results: tests/rtt104/STILLS_CHECK_V3.md (text only).
 */
const fs = require('fs');
const path = require('path');
const R = require('./render_rtt104.js');
const ROOT = path.resolve(__dirname, '..', '..');
const PHONE_PT = 390, DPR = 3, pt = px => px * PHONE_PT / 1920, BIG = 5.9, FLOOR = 5.0;
const MON = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ');

function csvRows(f) {
  const lines = fs.readFileSync(f, 'utf8').split(/\r?\n/).filter(Boolean), head = lines.shift().split(',');
  return lines.map(l => { const out = []; let cur = '', q = false;
    for (let i = 0; i < l.length; i++) { const c = l[i]; if (q) { if (c === '"') { if (l[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
      else if (c === '"') q = true; else if (c === ',') { out.push(cur); cur = ''; } else cur += c; }
    out.push(cur); return Object.fromEntries(head.map((h, i) => [h, out[i]])); });
}
const CH = csvRows(path.join(ROOT, 'data', 'rtt-104', 'v3_change_events.csv'));
const ROW = Object.fromEntries(CH.map(r => [r.iso3 + '|' + r.to_year, r]));

function wantBoard(year, n) {
  const rows = year === 1997 ? CH.filter(r => +r.from_year === 1997 && r.old_rank && +r.old_rank <= n).map(r => [+r.old_rank, r.iso3 + ' ' + r.old_value_1dp + '%'])
    : CH.filter(r => +r.to_year === year && r.new_rank && +r.new_rank <= n).map(r => [+r.new_rank, r.iso3 + ' ' + r.new_value_1dp + '%']);
  return rows.sort((a, b) => a[0] - b[0]).map(x => x[1]);
}
function checkTags(st, cfg, landingYear) {
  const fails = [], rule = cfg.v3.tag.rule;
  for (const l of st.labels.filter(l => l.kind === 'tag' && l.alpha > 0.05)) {
    const r = ROW[l.id + '|' + l.year], where = `${l.id} ${l.year} "${l.text}"`;
    if (!r) { fails.push(`tag ${where}: no row`); continue; }
    if (r.status !== 'VERIFIED' || !['election', 'other'].includes(r.cause) || !r.excerpt.trim() || !r.source_url.trim()) fails.push(`tag ${where}: row not VERIFIED with an excerpt`);
    if ((rule === 'a' ? r.big_points : r.big) !== 'y') fails.push(`tag ${where}: not big under rule ${rule}`);
    const d = r.election_date.trim().slice(0, 10);
    if (!l.text.endsWith(d.slice(0, 4)) || !l.text.includes(MON[+d.slice(5, 7) - 1])) fails.push(`tag ${where}: date is not ${d}`);
    if (!l.fits) fails.push(`tag ${where}: does not fit`);
    if (pt(l.size) < BIG - 1e-9) fails.push(`tag ${where}: ${pt(l.size).toFixed(1)} pt`);
  }
  if (landingYear) {
    const n = cfg.v3.rows, on = new Set(st.bars.map(b => b.id)), drawn = new Set(st.labels.filter(l => l.kind === 'tag' && l.alpha > 0.99).map(l => l.id));
    for (const r of CH) if (+r.to_year === landingYear && on.has(r.iso3) && (rule === 'a' ? r.big_points : r.big) === 'y' && ['election', 'other'].includes(r.cause) && !drawn.has(r.iso3))
      fails.push(`tag ${r.iso3} ${landingYear}: VERIFIED row not drawn`);
  }
  return fails;
}
function checkLayout(st) {
  const fails = [], p = st.panel, inP = (x, y, w, h) => x < p.x + p.w && x + w > p.x && y < p.y + p.h && y + h > p.y;
  for (const b of st.bars) { if (inP(b.rect.x, b.rect.y, b.rect.w, b.rect.h)) fails.push(`bar ${b.id} inside the world panel`);
    if (b.rect.x + b.rect.w > 1856) fails.push(`bar ${b.id} past the edge`); }
  for (const l of st.labels) if (['name', 'value', 'tag'].includes(l.kind) && l.alpha > 0.05) {
    const box = l.box || { x: l.x, y: l.y - l.size * 0.8, w: l.w, h: l.size };
    if (inP(box.x, box.y, box.w, box.h)) fails.push(`${l.kind} ${l.id} "${l.text}" inside the world panel`);
    if (box.x + box.w > 1857) fails.push(`${l.kind} ${l.id} "${l.text}" past the edge`);
  }
  return fails;
}
function checkPhone(st) {
  const fails = [], min = {};
  for (const l of st.labels) if (l.size && l.alpha > 0.3) min[l.kind] = Math.min(min[l.kind] || 1e9, l.size);
  for (const k of Object.keys(min)) { const need = ['name', 'value', 'tag', 'card_name', 'card_line'].includes(k) ? BIG : FLOOR;
    if (pt(min[k]) < need - 1e-9) fails.push(`${k} ${min[k]}px = ${pt(min[k]).toFixed(1)} pt < ${need}`); }
  return { fails, min };
}
const grab = pg => pg.evaluate(() => ({ labels: window.__LABELS, bars: window.__BARS, panel: G.panel, state: window.__STATE }));

async function main() {
  const out = process.argv[2], checkOnly = process.argv.includes('--check-only');
  if (!out) throw new Error('usage: render_stills_v3.js <out_dir> [--check-only]');
  if (!checkOnly && path.resolve(out).startsWith(ROOT + path.sep)) throw new Error('stills are private: write them outside the repository');
  fs.mkdirSync(out, { recursive: true });
  const spec = JSON.parse(fs.readFileSync(path.join(__dirname, 'stills_v3.json'), 'utf8'));
  const report = ['# RTT-104 V3 design round — still and clip checks (IQ-24d)', '',
    'Written by `kits/rtt-104/render_stills_v3.js`. VALUES: bars = ranks 1–N of `data/rtt-104/v3_change_events.csv` with their one-decimal figures. TAGS: every tag drawn is a VERIFIED row of `v3_change_events.csv` with a source URL and a fetched excerpt, big under the rule shown, with the row\'s month and year, fitting its bar; on a landing still every such row is drawn. PHONE: names, values and tags at least 5.9 pt at 390 pt wide, other text at least 5.0 pt. OVERLAP: nothing inside the world panel or past the board edge.', '',
    '| Still | Config | Frame | Values | Tags | Phone (smallest name / value / tag / other) | Overlap | Result |', '|---|---|---|---|---|---|---|---|'];
  const files = {}; let ok = true;
  for (const s of spec.stills) {
    const cfg = R.config(s.config), { br, pg } = await R.open(cfg);
    const f = await pg.evaluate(a => landingFrame(a), s.at);
    for (let i = 0; i < 3; i++) await R.frame(pg, f);
    const st = await grab(pg);
    if (!checkOnly) { const file = path.join(out, s.name + '_1920x1080.png'); await (await pg.$('#c')).screenshot({ path: file }); files[s.name] = file; }
    await br.close();
    const n = st.state && cfg.v3 ? R.config(s.config).v3.rows : 20;
    const got = st.bars.slice().sort((a, b) => a.slot - b.slot).map(b => b.id + ' ' + b.value), want = wantBoard(s.at, n);
    const v = got.join('|') === want.join('|') ? [] : [`values ${s.at}: want ${want.join(', ')} got ${got.join(', ')}`];
    const t = checkTags(st, cfg, s.at), p = checkPhone(st), o = checkLayout(st), res = [...v, ...t, ...p.fails, ...o];
    if (res.length) ok = false;
    const other = Object.entries(p.min).filter(([k]) => !['name', 'value', 'tag'].includes(k)).reduce((m, [, x]) => Math.min(m, x), 1e9);
    const f1 = x => x ? pt(x).toFixed(1) : '—';
    const nt = st.labels.filter(l => l.kind === 'tag' && l.alpha > 0.99).length;
    report.push(`| ${s.name} | ${s.config} | ${f} | ${v.length ? 'FAIL' : 'PASS'} (${n} bars) | ${t.length ? 'FAIL' : 'PASS'} (${nt}) | ${f1(p.min.name)} / ${f1(p.min.value)} / ${f1(p.min.tag)} / ${f1(other < 1e9 ? other : 0)} pt | ${o.length ? 'FAIL' : 'PASS'} | ${res.length ? 'FAIL: ' + res.join('; ') : 'PASS'} |`);
    console.log(`${res.length ? 'FAIL' : 'PASS'} ${s.name}${res.length ? ': ' + res.join('; ') : ''}`);
  }
  /* every frame of every V3 clip: tags and layout; landing frames also values */
  report.push('', '| Clip | Frames | Tags shown (country-year) | Landing values | Tag and layout checks, every frame |', '|---|---|---|---|---|');
  for (const c of fs.readFileSync(path.join(__dirname, 'clips_v3.txt'), 'utf8').split(/\s+/).filter(Boolean)) {
    const cfg = R.config(c), { br, pg } = await R.open(cfg);
    const total = await pg.evaluate(() => RACE_FRAMES), lands = await pg.evaluate(() => PLAN.landing);
    const atLand = Object.fromEntries(Object.entries(lands).map(([y, f]) => [f, +y])), first = Math.min(...Object.keys(lands).map(Number));
    const fails = new Set(), seen = new Set(); let vals = 0;
    for (let f = 0; f < total; f++) {
      await R.frame(pg, f); const st = await grab(pg), ly = atLand[f];
      for (const x of [...checkTags(st, cfg, ly === first ? null : ly), ...checkLayout(st)]) fails.add(x);   // no change lands on the first year shown
      st.labels.filter(l => l.kind === 'tag' && l.alpha > 0.05).forEach(l => seen.add(l.id + ' ' + l.year));
      if (ly) { const got = st.bars.slice().sort((a, b) => a.slot - b.slot).map(b => b.id + ' ' + b.value).join('|');
        if (got === wantBoard(ly, cfg.v3.rows).join('|')) vals++; else fails.add(`values ${ly}`); }
    }
    await br.close();
    if (fails.size) ok = false;
    report.push(`| ${c} | ${total} | ${seen.size}: ${[...seen].sort((a, b) => a.slice(4).localeCompare(b.slice(4)) || a.localeCompare(b)).join(', ')} | ${vals}/${Object.keys(lands).length} PASS | ${fails.size ? 'FAIL: ' + [...fails].join('; ') : 'PASS'} |`);
    console.log(`${fails.size ? 'FAIL' : 'PASS'} ${c}: ${total} frames, ${seen.size} tags${fails.size ? ': ' + [...fails].join('; ') : ''}`);
  }
  report.push('', `Overall: ${ok ? 'PASS' : 'FAIL'}.`, '');
  fs.writeFileSync(path.join(ROOT, 'tests', 'rtt104', 'STILLS_CHECK_V3.md'), report.join('\n'));
  if (checkOnly) process.exit(ok ? 0 : 1);

  /* phone copies and sheets (as render_stills.js) */
  const { chromium } = require(require.resolve('playwright', { paths: [path.join(ROOT, 'kits', 'rtt-002')] }));
  const b2 = await chromium.launch({ executablePath: process.env.PW_CHROME || '/opt/pw-browsers/chromium' });
  const ph = await b2.newPage({ viewport: { width: PHONE_PT, height: Math.round(PHONE_PT * 9 / 16) }, deviceScaleFactor: DPR });
  for (const f of Object.values(files)) {
    await ph.setContent(`<body style="margin:0;background:#000"><img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:${PHONE_PT}px;display:block"></body>`);
    await ph.waitForLoadState('load'); await ph.screenshot({ path: f.replace('_1920x1080.png', '_phone_390pt.png') });
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
    await cp.screenshot({ path: path.join(out, C.name + '.png'), fullPage: true }); fs.unlinkSync(html);
  }
  await b2.close();
  console.log(`${Object.keys(files).length} stills, ${Object.keys(files).length} phone copies, ${spec.compose.length} sheets in ${out}`);
  process.exit(ok ? 0 : 1);
}
module.exports = { checkTags, checkLayout, checkPhone, wantBoard, grab };
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
