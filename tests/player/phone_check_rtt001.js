/* RTT-001 phone check (IQ-13). For each board still in kits/rtt-001/stills.json (design sheets and compositions are
 * not boards and are left out) the frame is drawn exactly as render_stills.js draws it, and every label's size is
 * measured and converted to points on a phone showing the landscape video 390 points wide (as phone_check.js).
 * Pass/fail:
 *   - bar names and values at least 5.9 pt (RTT-002's approved size, house style 6, DEC-108);
 *   - axis numbers and the date line at least the names (DEC-022 (3), as phone_check.js);
 *   - footer, source line, "New source" marker, note line and callouts at least 5.0 pt (the footer floor of
 *     phone_check.js, as RTT-003 used for its callouts).
 * The empty picture box and the crown are reported (points on the phone), with no threshold.
 * Output: tests/player/PHONE_RTT001.md. Exit 1 on any failure.
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const KIT = path.join(ROOT, 'kits', 'rtt-002');
const rtt = require(path.join(KIT, 'rtt.js'));
const ST = require(path.join(ROOT, 'kits', 'rtt-001', 'render_stills.js'));
const { placeholderPNG } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';
const PHONE_PT = 390, FLOOR = 5.0, NAMES = 5.9, k = PHONE_PT / 1920, pt = px => px * k;

(async () => {
  const dir = path.join(ROOT, 'tests', 'output', 'rtt001_phone', '_assets'); fs.mkdirSync(dir, { recursive: true });
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  const stills = JSON.parse(fs.readFileSync(path.join(ROOT, 'kits', 'rtt-001', 'stills.json'), 'utf8')).stills.filter(s => s.config);
  const out = ['# RTT-001 phone check (IQ-13)', '', `Each board still measured as drawn on the 1920 frame and converted to points on a phone showing the video ${PHONE_PT} points wide. Names and values at least ${NAMES} pt (RTT-002's approved size); axis and date at least the names; footer, source line, marker, note and callouts at least ${FLOOR} pt. Picture box and crown: reported only.`, '',
               '| Still | Names | Values | Axis | Date | Footer | Source line | Marker | Note | Callout | Picture box | Crown | Result |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|'];
  let ok = true;
  for (const s of stills) {
    const cfg = ST.stillConfig(s);
    const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
    process.env.RTT_LOCAL_ASSETS = dir;
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    delete process.env.RTT_LOCAL_ASSETS;
    const target = await ST.targetFrame(pg, s);
    for (let f = 0; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
    const S = await pg.evaluate(() => ({ L: window.__LABELS, P: window.__PICS, CR: window.__CROWN }));
    await br.close();
    const size = kinds => { const v = S.L.filter(l => kinds.includes(l.kind) && l.alpha > 0.3).map(l => l.size); return v.length ? Math.min(...v) : null; };
    const z = { name: size(['name']), value: size(['value']), axis: size(['axis']), date: size(['time_line']), footer: size(['footer']),
                source: size(['source_line']), marker: size(['marker']), note: size(['note_line']), callout: size(['callout', 'callout_extra']) };
    const fails = [];
    for (const kk of ['name', 'value']) if (z[kk] == null || pt(z[kk]) < NAMES) fails.push(kk + ' < ' + NAMES + ' pt');
    if (!(z.axis >= z.name)) fails.push('axis < names');
    if (!(z.date >= z.name)) fails.push('date < names');
    for (const kk of ['footer', 'source', 'marker', 'note', 'callout']) if (z[kk] != null && pt(z[kk]) < FLOOR) fails.push(kk + ' < ' + FLOOR + ' pt');
    ok = ok && !fails.length;
    const f = v => v == null ? '—' : `${v}px = ${pt(v).toFixed(1)} pt`;
    const p = S.P[0];
    out.push(`| ${s.name} | ${f(z.name)} | ${f(z.value)} | ${f(z.axis)} | ${f(z.date)} | ${f(z.footer)} | ${f(z.source)} | ${f(z.marker)} | ${f(z.note)} | ${f(z.callout)} | ${p ? `${p.box.w} x ${p.box.h} px = ${pt(p.box.w).toFixed(1)} x ${pt(p.box.h).toFixed(1)} pt` : '—'} | ${S.CR ? `${S.CR.w.toFixed(0)} x ${S.CR.h.toFixed(0)} px = ${pt(S.CR.w).toFixed(1)} x ${pt(S.CR.h).toFixed(1)} pt` : '—'} | ${fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS'} |`);
    console.log(`${fails.length ? 'FAIL' : 'PASS'} ${s.name}`);
  }
  out.push('', `Overall: ${ok ? 'PASS' : 'FAIL'}. For reference: RTT-002's approved film draws names and values at 29 px = 5.9 pt; RTT-003's at 33 px = 6.7 pt.`, '');
  fs.writeFileSync(path.join(__dirname, 'PHONE_RTT001.md'), out.join('\n'));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
