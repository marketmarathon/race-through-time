/* RTT-102 phone check (IQ-19, design round 1; adapted from phone_check_rtt103.js, which is not changed). For each still in
 * kits/rtt-102/stills.json (compositions are left out) the frame is drawn exactly as render_stills.js draws it, and every
 * label's size is measured and converted to points on a phone showing the landscape video 390 points wide. Pass/fail:
 *   - names and values at least 5.9 pt (RTT-002's approved size, house style 6, DEC-108);
 *   - the axis numbers and the date at least the names;
 *   - every other label (footer, source line, note, tags, story cards, the final line) at least 5.0 pt;
 *   - a still dated with a month (`at`, taken on the frame where that month's figures land) shows that month's figures
 *     exactly as data/rtt-102/series_monthly.csv gives them (a bar after its last published month: that figure), with
 *     the value label's rounding written out again here, and the date block shows that month. Stills taken mid-move
 *     (after_sec) and story-card stills are reported, not checked against the month (their figures are still counting);
 *     eased-motion stills are checked on published months only.
 * IQ-19b: a number that is not a published figure is checked at two significant figures (values.visits.between "sig2");
 *   the combined panel's text is measured with the other labels.
 * The logo tile is reported (points on the phone), with no threshold. Placeholder logos (tests/player/placeholders.js).
 * Output: tests/player/PHONE_RTT102.md. Exit 1 on any failure.
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const KIT = path.join(ROOT, 'kits', 'rtt-002');
const K102 = path.join(ROOT, 'kits', 'rtt-102');
const rtt = require(path.join(KIT, 'rtt.js'));
const ST = require(path.join(K102, 'render_stills.js'));
const { placeholderPNG, logoPlaceholders } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';
const PHONE_PT = 390, FLOOR = 5.0, NAMES = 5.9, k = PHONE_PT / 1920, pt = px => px * k;
const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
function visitsText(visits, V, pub) {
  const u = BigInt(visits), D2 = V.bn_decimals === 2 ? 2 : 1, P = 10n ** BigInt(D2);
  const bn = (u + 500000000n / P) / (1000000000n / P), m = (u + 500000n) / 1000000n, t = (u + 50000n) / 100000n;
  let s;
  if (u >= 1000000000n || m >= 1000n) s = (bn / P) + '.' + String(bn % P).padStart(D2, '0') + 'bn';
  else if (u >= 100000000n || t >= 1000n) s = m + 'm';
  else s = (t / 10n) + '.' + (t % 10n) + 'm';
  if (!pub && V.between === 'sig2') {                 // IQ-19b: two significant figures (as run_tests_rtt102.js)
    let p = 1n; while (u >= p * 100n) p *= 10n;
    let r = (u + p / 2n) / p; if (r >= 100n) { p *= 10n; r = (u + p / 2n) / p; }
    const v = r * p;
    if (v >= 1000000000n) s = v >= 10000000000n ? String(v / 1000000000n) + 'bn' : (Number(v / 100000000n) / 10).toFixed(1) + 'bn';
    else s = v >= 10000000n ? String(v / 1000000n) + 'm' : v >= 1000000n ? (Number(v / 100000n) / 10).toFixed(1) + 'm' : (Number(v / 10000n) / 100).toFixed(2) + 'm';
  }
  return (V.approx === 'all' || (V.approx === 'between' && !pub) ? '~' : '') + s;
}

(async () => {
  const only = process.argv.slice(2);
  const dir = path.join(ROOT, 'tests', 'output', 'rtt102_phone', '_assets'); fs.mkdirSync(dir, { recursive: true });
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  const stills = JSON.parse(fs.readFileSync(path.join(K102, 'stills.json'), 'utf8')).stills.filter(s => !s.compose && (!only.length || only.includes(s.name)));
  const t = fs.readFileSync(path.join(ROOT, 'data', 'rtt-102', 'series_monthly.csv'), 'utf8').trim().split('\n'), H = t.shift().split(',');
  const byMonth = {}, lastPub = {};
  for (const l of t) { const v = l.split(','), r = Object.fromEntries(H.map((h, i) => [h, v[i]])); if (r.month > '2026-08') continue;
    (byMonth[r.month] = byMonth[r.month] || {})[r.assistant_id] = r; if (r.provenance === 'published') lastPub[r.assistant_id] = r.month; }
  const out = ['# RTT-102 phone check (IQ-19, design round 1)', '', `Each still measured as drawn on the 1920 frame and converted to points on a phone showing the video ${PHONE_PT} points wide. Names and values at least ${NAMES} pt; the axis and the date at least the names; every other label at least ${FLOOR} pt. Logo tile: reported only. A still dated with a month shows that month's figures (series_monthly.csv) and that month in the date block.`, '',
               '| Still | Names | Values | Axis | Date | Smallest other label | Logo tile | Figures of the dated month | Result |', '|---|---|---|---|---|---|---|---|---|'];
  let ok = true;
  for (const s of stills) {
    const cfg = ST.stillConfig(s);
    logoPlaceholders(cfg, dir);
    const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
    process.env.RTT_LOCAL_ASSETS = dir;
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    delete process.env.RTT_LOCAL_ASSETS;
    const target = await ST.targetFrame(pg, s); for (let f = 0; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
    const S = await pg.evaluate(() => ({ L: window.__LABELS, P: window.__PICS, B: window.__BARS }));
    await br.close();
    const vis = S.L.filter(l => l.alpha > 0.3 && l.size);
    const size = kinds => { const v = vis.filter(l => kinds.includes(l.kind)).map(l => l.size); return v.length ? Math.min(...v) : null; };
    const z = { name: size(['name']), value: size(['value']), axis: size(['axis']), date: size(['date_month', 'date_year']) };
    const others = vis.filter(l => !['name', 'value', 'axis', 'date_month', 'date_year'].includes(l.kind));
    const small = others.length ? others.reduce((a, b) => (b.size < a.size ? b : a)) : null;
    const fails = []; let figs = '—';
    const V = Object.assign({ approx: 'all', bn_decimals: 1 }, (cfg.values || {}).visits || {}), EASED = (cfg.smoothing || {}).mode === 'eased' && cfg.smoothing.knots !== 'all';   // IQ-19d: knots on every month = the data on every landing frame
    const at = s.after_sec != null || s.card ? null : s.at === 'final' ? '2026-08' : s.at.slice(0, 7);
    if (at) { const row = byMonth[at] || {}, bad = []; let n = 0;
      for (const id of Object.keys(lastPub)) { const held = !row[id] && lastPub[id] < at && Object.keys(byMonth).some(m => m <= at && byMonth[m][id]);
        if (!row[id] && !held) { if (vis.some(l => l.kind === 'value' && l.id === id)) bad.push(id + ' drawn with no figure'); continue; }
        const r = held ? byMonth[lastPub[id]][id] : row[id], pub = held || r.provenance === 'published';
        if (EASED && !pub) continue;
        const w = visitsText(r.visits, V, pub), l = vis.find(l => l.kind === 'value' && l.id === id); n++;
        if (!l || l.text !== w) bad.push(id + ' ' + (l ? l.text : 'missing') + ' (data ' + w + ')'); }
      const ml = vis.find(l => l.kind === 'date_month'), yl = vis.find(l => l.kind === 'date_year');
      if (!ml || ml.text !== MONTHS[+at.slice(5, 7) - 1] || !yl || yl.text !== at.slice(0, 4)) bad.push('date ' + (ml && ml.text) + ' ' + (yl && yl.text));
      figs = bad.length ? 'FAIL: ' + bad.join('; ') : n + ' figures = series_monthly.csv ' + at;
      if (bad.length) fails.push('figures not those of ' + at); }
    else figs = 'mid-move or card still (not a landing frame)';
    for (const kk of ['name', 'value']) if (z[kk] != null && pt(z[kk]) < NAMES) fails.push(kk + ' < ' + NAMES + ' pt');
    if (z.name != null) { if (!(z.axis >= z.name)) fails.push('axis < names'); if (z.date != null && !(z.date >= z.name)) fails.push('date < names'); }
    if (small && pt(small.size) < FLOOR) fails.push(small.kind + ' "' + small.text.slice(0, 30) + '" < ' + FLOOR + ' pt');
    ok = ok && !fails.length;
    const f = v => v == null ? '—' : `${v}px = ${pt(v).toFixed(1)} pt`;
    const p = (S.P || [])[0];
    out.push(`| ${s.name} | ${f(z.name)} | ${f(z.value)} | ${f(z.axis)} | ${f(z.date)} | ${small ? small.kind + ' ' + f(small.size) : '—'} | ${p ? `${Math.round(p.box.w)} x ${Math.round(p.box.h)} px = ${pt(p.box.w).toFixed(1)} x ${pt(p.box.h).toFixed(1)} pt` : '—'} | ${figs} | ${fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS'} |`);
    console.log(`${fails.length ? 'FAIL' : 'PASS'} ${s.name}${fails.length ? ': ' + fails.join('; ') : ''}`);
  }
  out.push('', `Overall: ${ok ? 'PASS' : 'FAIL'}. For reference: RTT-002's approved film draws names and values at 29 px = 5.9 pt; RTT-003's at 33 px = 6.7 pt.`, '');
  if (!only.length) fs.writeFileSync(path.join(__dirname, 'PHONE_RTT102.md'), out.join('\n'));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
