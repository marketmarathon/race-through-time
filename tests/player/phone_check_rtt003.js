/* RTT-003 phone check (IQ-10). For each board still in kits/rtt-003/stills.json (the design sheets are
 * not boards and are left out) the frame is drawn exactly as render_stills.js draws it, with placeholder
 * pictures, and every label's size is measured and converted to points on a phone showing the landscape
 * video 390 points wide (iPhone 12-16 class, as tests/player/phone_check.js).
 * Pass/fail, the thresholds of tests/player/phone_check.js unchanged (DEC-022 (3)):
 *   axis numbers >= console names; date line >= console names; footer >= 5.0 pt.
 * Added for RTT-003 with the same footer floor (5.0 pt), since none was set for them and none is invented
 * beyond it: maker key names and totals, the legend, the callout line and the "analyst estimate" label.
 * Pictures and the crown are reported (points on the phone), with no threshold.
 * Output: tests/player/PHONE_RTT003.md. Exit 1 on any failure.
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const KIT = path.join(ROOT, 'kits', 'rtt-002');
const rtt = require(path.join(KIT, 'rtt.js'));
const { placeholderPNG } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';
const PHONE_PT = 390, FLOOR = 5.0, k = PHONE_PT / 1920, pt = px => px * k;

(async () => {
  const dir = path.join(ROOT, 'tests', 'output', 'rtt003_phone', '_assets');
  fs.mkdirSync(path.join(dir, 'icons'), { recursive: true }); fs.mkdirSync(path.join(dir, 'logos'), { recursive: true });
  const stills = JSON.parse(fs.readFileSync(path.join(ROOT, 'kits', 'rtt-003', 'stills.json'), 'utf8')).stills.filter(s => !s.sheet);
  const out = ['# RTT-003 phone check (IQ-10)', '', `Each board still measured as drawn on the 1920 frame and converted to points on a phone showing the video ${PHONE_PT} points wide. Thresholds as tests/player/phone_check.js (axis and date at least the names; footer at least ${FLOOR} pt); the RTT-003 additions (maker key, legend, callout, analyst label) use the footer floor. Pictures and the crown: reported only.`, '',
               '| Still | Names | Values | Axis | Date | Footer | Key names / totals / estimate words | Legend | Callout / note | Analyst label | Picture box | Crown | Result |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|'];
  let ok = true;
  for (const s of stills) {
    const cfg = rtt.loadConfig('../rtt-003/' + s.config, s.overrides);
    const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
    for (const e of data.entrants) placeholderPNG(path.join(dir, 'icons', e.id + '.png'), 165, 100, [180, 180, 190]);
    for (const m of cfg.maker_order) fs.writeFileSync(path.join(dir, 'logos', m + '.svg'), '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="40"><rect width="120" height="40" fill="#555"/></svg>');
    placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
    process.env.RTT_LOCAL_ASSETS = dir;
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    delete process.env.RTT_LOCAL_ASSETS;
    const info = await pg.evaluate(() => ({ dates: TL.events.map(e => e.date), start: TL.startFrame, raceFrames: RACE_FRAMES }));
    const kq = info.dates.indexOf(s.at);
    const target = s.at === 'final' ? info.raceFrames - 1 : (kq + 1 < info.start.length ? info.start[kq + 1] : info.raceFrames) - 1;
    for (let f = 0; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
    const S = await pg.evaluate(() => ({ L: window.__LABELS, P: window.__PICS, CR: window.__CROWN }));
    await br.close();
    const size = kinds => { const v = S.L.filter(l => kinds.includes(l.kind) && l.alpha > 0.3).map(l => l.size); return v.length ? Math.min(...v) : null; };
    const z = { name: size(['name']), value: size(['value']), axis: size(['axis']), date: size(['time_line']), footer: size(['footer']),
                key: size(['key_name', 'key_total', 'key_est']), legend: size(['key_legend']), callout: size(['callout', 'callout_extra', 'note']), est: size(['est_label']) };
    const fails = [];
    if (!(pt(z.axis) >= pt(z.name))) fails.push('axis < names');
    if (!(pt(z.date) >= pt(z.name))) fails.push('date < names');
    for (const kk of ['footer', 'key', 'legend', 'callout', 'est']) if (z[kk] != null && pt(z[kk]) < FLOOR) fails.push(kk + ' < ' + FLOOR + ' pt');
    ok = ok && !fails.length;
    const f = v => v == null ? '—' : `${v}px = ${pt(v).toFixed(1)} pt`;
    const p = S.P[0];
    out.push(`| ${s.name} | ${f(z.name)} | ${f(z.value)} | ${f(z.axis)} | ${f(z.date)} | ${f(z.footer)} | ${f(z.key)} | ${f(z.legend)} | ${f(z.callout)} | ${f(z.est)} | ${p ? `${p.box.w} x ${p.box.h} px = ${pt(p.box.w).toFixed(1)} x ${pt(p.box.h).toFixed(1)} pt` : '—'} | ${S.CR ? `${S.CR.w.toFixed(0)} x ${S.CR.h.toFixed(0)} px = ${pt(S.CR.w).toFixed(1)} x ${pt(S.CR.h).toFixed(1)} pt` : '—'} | ${fails.length ? 'FAIL: ' + fails.join('; ') : 'PASS'} |`);
    console.log(`${fails.length ? 'FAIL' : 'PASS'} ${s.name}`);
  }
  out.push('', `Overall: ${ok ? 'PASS' : 'FAIL'}. For reference: RTT-002's approved film draws names and values at 29 px = 5.9 pt.`, '');
  fs.writeFileSync(path.join(__dirname, 'PHONE_RTT003.md'), out.join('\n'));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
