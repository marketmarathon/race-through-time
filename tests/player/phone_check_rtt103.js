/* RTT-103 phone check (IQ-18, design round 1). For each still in kits/rtt-103/stills.json (board stills and the steps
 * drawn by steps.js; compositions are left out) the frame is drawn exactly as render_stills.js draws it, and every
 * label's size is measured and converted to points on a phone showing the landscape video 390 points wide (as
 * phone_check_rtt001.js). Pass/fail:
 *   - names and values at least 5.9 pt (RTT-002's approved size, house style 6, DEC-108);
 *   - on boards, the axis numbers and the date at least the names;
 *   - every other label (footer, notes, tags, story moments, the running total, step text) at least 5.0 pt.
 * The logo tile is reported (points on the phone), with no threshold. Placeholder logos (tests/placeholders.js).
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
const PHONE_PT = 390, FLOOR = 5.0, NAMES = 5.9, k = PHONE_PT / 1920, pt = px => px * k;

(async () => {
  const only = process.argv.slice(2);
  const dir = path.join(ROOT, 'tests', 'output', 'rtt103_phone', '_assets'); fs.mkdirSync(dir, { recursive: true });
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  const stills = JSON.parse(fs.readFileSync(path.join(K103, 'stills.json'), 'utf8')).stills.filter(s => !s.compose && (!only.length || only.includes(s.name)));
  const out = ['# RTT-103 phone check (IQ-18, design round 1)', '', `Each still measured as drawn on the 1920 frame and converted to points on a phone showing the video ${PHONE_PT} points wide. Names and values at least ${NAMES} pt; on boards the axis and the date at least the names; every other label at least ${FLOOR} pt. Logo tile: reported only.`, '',
               '| Still | Names | Values | Axis | Date | Smallest other label | Logo tile | Result |', '|---|---|---|---|---|---|---|---|'];
  let ok = true;
  for (const s of stills) {
    const cfg = ST.stillConfig(s.sheet ? Object.assign({ config: 'config_rtt103_base.json' }, s) : s);
    logoPlaceholders(cfg, dir);
    const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
    process.env.RTT_LOCAL_ASSETS = dir;
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    delete process.env.RTT_LOCAL_ASSETS;
    if (!s.sheet || s.at) { const target = await ST.targetFrame(pg, s); for (let f = 0; f <= target; f++) await rtt.drawFrame(pg, f, cfg); }
    if (s.sheet) { await pg.addScriptTag({ path: path.join(K103, 'steps.js') }); await pg.evaluate(([n, m, o]) => window.RTT103_STEPS[n](m, o || {}), [s.sheet, data, s.opts || null]); }
    const S = await pg.evaluate(() => ({ L: window.__LABELS, P: window.__PICS }));
    await br.close();
    const vis = S.L.filter(l => l.alpha > 0.3 && l.size);
    const size = kinds => { const v = vis.filter(l => kinds.includes(l.kind)).map(l => l.size); return v.length ? Math.min(...v) : null; };
    const z = { name: size(['name']), value: size(['value']), axis: size(['axis']), date: size(['time_line', 'date_month', 'date_year']) };
    const others = vis.filter(l => !['name', 'value', 'axis', 'time_line', 'date_month', 'date_year'].includes(l.kind));
    const small = others.length ? others.reduce((a, b) => (b.size < a.size ? b : a)) : null;
    const fails = [];
    for (const kk of ['name', 'value']) if (z[kk] != null && pt(z[kk]) < NAMES) fails.push(kk + ' < ' + NAMES + ' pt');
    if (!s.sheet && z.name != null) { if (!(z.axis >= z.name)) fails.push('axis < names'); if (z.date != null && !(z.date >= z.name)) fails.push('date < names'); }
    if (small && pt(small.size) < FLOOR) fails.push(small.kind + ' "' + small.text.slice(0, 30) + '" < ' + FLOOR + ' pt');
    ok = ok && !fails.length;
    const f = v => v == null ? '—' : `${v}px = ${pt(v).toFixed(1)} pt`;
    const p = (S.P || [])[0];
    out.push(`| ${s.name} | ${f(z.name)} | ${f(z.value)} | ${f(z.axis)} | ${f(z.date)} | ${small ? small.kind + ' ' + f(small.size) : '—'} | ${p ? `${p.box.w} x ${p.box.h} px = ${pt(p.box.w).toFixed(1)} x ${pt(p.box.h).toFixed(1)} pt` : '—'} | ${fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS'} |`);
    console.log(`${fails.length ? 'FAIL' : 'PASS'} ${s.name}${fails.length ? ': ' + fails.join('; ') : ''}`);
  }
  out.push('', `Overall: ${ok ? 'PASS' : 'FAIL'}. For reference: RTT-002's approved film draws names and values at 29 px = 5.9 pt; RTT-003's at 33 px = 6.7 pt.`, '');
  if (!only.length) fs.writeFileSync(path.join(__dirname, 'PHONE_RTT103.md'), out.join('\n'));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
