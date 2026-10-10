/* RTT-101 phone check (IQ-21, design round 1; adapted from phone_check_rtt102.js, which is not changed). For each still in
 * kits/rtt-101/stills.json (compositions left out) the frame is drawn exactly as kits/rtt-101/render_stills.js draws it,
 * and every label's size is measured and converted to points on a phone showing the landscape video 390 points wide:
 *   - names and values at least 5.9 pt (RTT-002's approved size, house style 6, DEC-108);
 *   - the axis numbers and the date at least the names... the axis at least 5.9 pt (it is smaller than the names here,
 *     as in RTT-102, and reported);
 *   - every other label (footer, the line under the title, status labels, story cards, the panel) at least 5.0 pt;
 *   - a still dated with a month (taken on the frame where that month's figures land) shows that month's figures exactly
 *     as data/rtt-101/series_onscreen.csv gives them, in the still's own format (with the near-tie option, the figure
 *     rounded to the decimals drawn), and the date block shows that month ("1 September" 2026 at the freeze).
 * The crest tile is reported (points on the phone), with no threshold. Placeholder crests (tests/player/placeholders.js).
 * Output: tests/player/PHONE_RTT101.md. Exit 1 on any failure.
 */
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..'), KIT = path.join(ROOT, 'kits', 'rtt-002'), K101 = path.join(ROOT, 'kits', 'rtt-101');
const rtt = require(path.join(KIT, 'rtt.js')), ST = require(path.join(K101, 'render_stills.js'));
const { placeholderPNG, logoPlaceholders } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);   // the container's Chromium, else Playwright's own (runner)
const PHONE_PT = 390, FLOOR = 5.0, NAMES = 5.9, k = PHONE_PT / 1920, pt = px => px * k;
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const pence = s => { const [a, b = ''] = s.split('.'); const neg = a.startsWith('-'); const v = BigInt(a.replace('-', '')) * 100n + BigInt((b + '00').slice(0, 2)); return neg ? -v : v; };
/* the drawn label back to pence bounds: "£1.71bn" -> [1.705bn, 1.715bn) */
function bounds(t) {
  const m = /^(−?)£([\d,]+)(?:\.(\d+))?(bn|m)?$/.exec(t); if (!m) return null;
  if (m[2] === '0' && !m[4]) return [0n, 0n, 0n];
  const d = (m[3] || '').length, unit = m[4] === 'bn' ? 100000000000n : 100000000n, q = unit / 10n ** BigInt(d);
  const v = (BigInt(m[2].replace(/,/g, '')) * 10n ** BigInt(d) + BigInt(m[3] || 0)) * q;
  return [v - q / 2n, v + q / 2n, m[1] ? -1n : 1n];
}

(async () => {
  const only = process.argv.slice(2);
  const dir = path.join(ROOT, 'tests', 'output', 'rtt101_phone', '_assets'); fs.mkdirSync(dir, { recursive: true });
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  const stills = JSON.parse(fs.readFileSync(path.join(K101, 'stills.json'), 'utf8')).stills.filter(s => !s.compose && (!only.length || only.includes(s.name)));
  const t = fs.readFileSync(path.join(ROOT, 'data', 'rtt-101', 'series_onscreen.csv'), 'utf8').trim().split('\n'), H = t.shift().split(',');
  const by = {};
  for (const l of t) { const v = l.split(','), r = Object.fromEntries(H.map((h, i) => [h, v[i]])); if (r.rank) (by[r.month_end] = by[r.month_end] || {})[r.club_id] = pence(r.cum_net_gbp); }
  const out = ['# RTT-101 phone check (IQ-21, design round 1)', '', `Each still measured as drawn on the 1920 frame and converted to points on a phone showing the video ${PHONE_PT} points wide. Names and values at least ${NAMES} pt; the axis at least ${NAMES} pt; every other label at least ${FLOOR} pt. Crest tile: reported only. A still dated with a month shows that month's figures (series_onscreen.csv) and that month in the date block. Placeholder crests.`, '',
               '| Still | Names | Values | Axis | Date | Smallest other label | Crest tile | Figures of the dated month | Result |', '|---|---|---|---|---|---|---|---|---|'];
  let ok = true;
  for (const s of stills) {
    const cfg = ST.stillConfig(s);
    logoPlaceholders(cfg, dir);
    const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
    process.env.RTT_LOCAL_ASSETS = dir;
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    delete process.env.RTT_LOCAL_ASSETS;
    const target = await ST.targetFrame(pg, s);
    const from = s.step != null ? target : Math.max(0, target - (s.warm != null ? s.warm : 120));
    for (let f = from; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
    if (s.step == null) for (let i = 0; i < 150; i++) await rtt.drawFrame(pg, target, cfg);
    const S = await pg.evaluate(() => ({ L: window.__LABELS, P: window.__PICS, R: window.__RANK, dates: TL.events.map(e => e.date), open: TL.openingEvent.date }));
    await br.close();
    const vis = S.L.filter(l => l.alpha > 0.3 && l.size);
    const size = kinds => { const v = vis.filter(l => kinds.includes(l.kind)).map(l => l.size); return v.length ? Math.min(...v) : null; };
    const z = { name: size(['name']), value: size(['value']), axis: size(['axis']), date: size(['date_month', 'date_year']) };
    const others = vis.filter(l => !['name', 'value', 'axis', 'date_month', 'date_year', 'date_year_old'].includes(l.kind));
    const small = others.length ? others.reduce((a, b) => (b.size < a.size ? b : a)) : null;
    const fails = []; let figs = '—';
    const at = s.step != null || s.after_sec != null || s.card ? null : s.at === 'final' ? '2026-09-01' : s.at;
    if (at) { const row = by[at] || {}, bad = []; let n = 0;
      for (const l of vis.filter(l => l.kind === 'value')) { const b = bounds(l.text), v = row[l.id];
        if (v == null) { bad.push(l.id + ' drawn with no figure'); continue; }
        if (!b) { bad.push(l.id + ' unreadable ' + l.text); continue; } n++;
        const av = v < 0n ? -v : v;
        if (b[2] === 0n ? v !== 0n : ((v < 0n) !== (b[2] < 0n) || av < b[0] || av >= b[1])) bad.push(`${l.id} ${l.text} (data ${v} pence)`); }
      const ml = vis.find(l => l.kind === 'date_month'), yl = vis.find(l => l.kind === 'date_year');
      const wantM = at === '2026-09-01' ? '1 September' : MONTHS[+at.slice(5, 7) - 1];
      if (!ml || ml.text !== wantM || !yl || yl.text !== at.slice(0, 4)) bad.push('date ' + (ml && ml.text) + ' ' + (yl && yl.text));
      figs = bad.length ? 'FAIL: ' + bad.slice(0, 4).join('; ') : n + ' figures = series_onscreen.csv ' + at;
      if (bad.length) fails.push('figures not those of ' + at); }
    else figs = s.step != null ? 'closing view (figures: avg_real_net_per_season_gbp2026 at the freeze)' : 'story-card still (inside a count)';
    for (const kk of ['name', 'value', 'axis']) if (z[kk] != null && pt(z[kk]) < NAMES) fails.push(kk + ' < ' + NAMES + ' pt');
    if (z.name != null && z.date != null && !(z.date >= z.name)) fails.push('date < names');
    if (small && pt(small.size) < FLOOR) fails.push(small.kind + ' "' + small.text.slice(0, 30) + '" < ' + FLOOR + ' pt');
    ok = ok && !fails.length;
    const f = v => v == null ? '—' : `${v}px = ${pt(v).toFixed(1)} pt`;
    const p = (S.P || [])[0];
    out.push(`| ${s.name} | ${f(z.name)} | ${f(z.value)} | ${f(z.axis)} | ${f(z.date)} | ${small ? small.kind + ' ' + f(small.size) : '—'} | ${p ? `${Math.round(p.box.w)} x ${Math.round(p.box.h)} px = ${pt(p.box.w).toFixed(1)} x ${pt(p.box.h).toFixed(1)} pt` : '—'} | ${figs} | ${fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS'} |`);
    console.log(`${fails.length ? 'FAIL' : 'PASS'} ${s.name}${fails.length ? ': ' + fails.join('; ') : ''}`);
  }
  out.push('', `Overall: ${ok ? 'PASS' : 'FAIL'}. For reference: RTT-002's approved film draws names and values at 29 px = 5.9 pt; RTT-003's at 33 px = 6.7 pt.`, '');
  if (!only.length) fs.writeFileSync(path.join(__dirname, 'PHONE_RTT101.md'), out.join('\n'));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
