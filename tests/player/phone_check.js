/* Phone check (IQ-04 step 7; thresholds added in IQ-05, DEC-022; round-2 pilots IQ-05b).
 *
 * 1920x1080 stills: from the full RTT-002 run a crowded mid-history board (1988) and the final
 * board, and from EACH round-2 pilot (A: top 20, B: top ten + winner line) the 2020 Portuguese
 * Grand Prix and the final board. Each is then shown
 * as a phone shows a landscape video held upright: the full frame 390 points wide
 * (iPhone 12-16 class) at 3 device pixels per point, plus a crop of the bottom left (footer) at
 * that same scale. Every label's size is measured on the frame and at phone scale.
 *
 * Pass/fail (DEC-022 (3)), on every still:
 *   - axis numbers  >= driver names (points at phone scale)
 *   - date          >= driver names
 *   - footer        >= 5.0 pt
 *   - winner line   >= driver names (variant B only; the same rule as the date it sits under)
 * The thresholds are unchanged from IQ-05. Because they are relative to the driver names, a board
 * with smaller names passes them more easily, so the names' own size is also printed against
 * round 1's top-ten names (32 px = 6.5 pt) for information; that line is not a pass/fail gate.
 * Exit code 1 if any check fails.
 *
 * Usage: node tests/player/phone_check.js      Output: tests/output/phone/ (gitignored)
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const KITDIR = path.join(ROOT, 'kits', 'rtt-002');
const rtt = require(path.join(KITDIR, 'rtt.js'));
const OUT = path.join(ROOT, 'tests', 'output', 'phone');
const PHONE_PT = 390, DPR = 3, FOOTER_MIN_PT = 5.0;
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';

/* Draw every frame up to each target (the rank glide is stateful) and keep the stills. */
async function stills(configFile, pick) {
  const cfg = rtt.loadConfig(configFile);
  const data = JSON.parse(fs.readFileSync(path.join(KITDIR, cfg.race_file), 'utf8'));
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
  const info = await pg.evaluate(() => ({ start: TL.startFrame, races: TL.events.map(e => e.race_index), raceFrames: RACE_FRAMES }));
  const targets = pick(info, cfg);
  const el = await pg.$('#c');
  const report = [];
  let f = 0;
  for (const t of targets) {
    for (; f <= t.frame; f++) await pg.evaluate(tt => drawAt(tt), f / cfg.fps);
    await el.screenshot({ path: path.join(OUT, t.name + '_1920.png') });
    const labels = await pg.evaluate(() => window.__LABELS);
    const sizes = {};
    for (const l of labels) if (l.alpha > 0.5) sizes[l.kind] = Math.min(sizes[l.kind] || 1e9, l.size);
    report.push({ still: t.name, config: configFile, frame: t.frame, sizes });
  }
  await br.close();
  return report;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const report = [];
  // A: last frame of the 1988 Australian Grand Prix slot (race index 468, last race of 1988);
  // B: the final board, one second before the closing card
  report.push(...await stills('config.json', (info, cfg) => {
    const kA = info.races.indexOf(468);
    return [{ name: 'still_A_1988', frame: info.start[kA + 1] - 1 }, { name: 'still_B_final', frame: info.raceFrames - cfg.fps }];
  }));
  // C, D: each round-2 pilot, last frame of the 2020 Portuguese Grand Prix slot (race index 1030,
  // Hamilton past Schumacher, end of the record hold) and one second before the end of the final board
  for (const [file, tag] of [['config_pilot_2014_2021_top20.json', 'A_top20'], ['config_pilot_2014_2021_top10_winner.json', 'B_top10_winner']])
    report.push(...await stills(file, (info, cfg) => {
      const k = info.races.indexOf(1030);
      return [{ name: `still_C_${tag}_2020_portugal`, frame: info.start[k + 1] - 1 }, { name: `still_D_${tag}_final`, frame: info.raceFrames - cfg.fps }];
    }));

  // the phone view: the 1920 still displayed PHONE_PT points wide
  const { chromium } = require(require.resolve('playwright', { paths: [KITDIR] }));
  const b2 = await chromium.launch({ executablePath: CHROME, args: ['--disable-background-networking', '--disable-component-update'] });
  const ph = await b2.newPage({ viewport: { width: PHONE_PT, height: Math.round(PHONE_PT * 9 / 16) }, deviceScaleFactor: DPR });
  for (const t of report) {
    const src = 'data:image/png;base64,' + fs.readFileSync(path.join(OUT, t.still + '_1920.png')).toString('base64');
    await ph.setContent(`<body style="margin:0;background:#000"><img src="${src}" style="width:${PHONE_PT}px;display:block"></body>`);
    await ph.waitForLoadState('load');
    await ph.screenshot({ path: path.join(OUT, t.still + '_phone_full.png') });
    // bottom-left quarter at phone scale: footer, lower bars and their values
    await ph.screenshot({ path: path.join(OUT, t.still + '_phone_crop_bottomleft.png'),
                          clip: { x: 0, y: PHONE_PT * 9 / 16 / 2, width: PHONE_PT / 2, height: PHONE_PT * 9 / 16 / 2 } });
  }
  await b2.close();

  const k = PHONE_PT / 1920, pt = px => px * k;
  const lines = ['still,frame,label,px_on_1920_frame,points_on_phone_' + PHONE_PT + 'pt_wide'];
  for (const r of report) for (const [kind, px] of Object.entries(r.sizes).sort((a, b) => a[1] - b[1]))
    lines.push([r.still, r.frame, kind, px, pt(px).toFixed(1)].join(','));
  fs.writeFileSync(path.join(OUT, 'label_sizes.csv'), lines.join('\n') + '\n');
  console.log(lines.join('\n'), '\n');

  let ok = true;
  const check = (still, what, got, min) => {
    const pass = got != null && got + 1e-9 >= min;
    ok = ok && pass;
    console.log(`${pass ? 'PASS' : 'FAIL'}  ${still}: ${what} ${got == null ? 'NOT DRAWN' : got.toFixed(2) + ' pt'} (needs >= ${min.toFixed(2)} pt)`);
  };
  for (const r of report) {
    const s = r.sizes, name = pt(s.name);
    check(r.still, 'axis numbers', s.axis && pt(s.axis), name);
    check(r.still, 'date', s.time_date && pt(s.time_date), name);
    check(r.still, 'footer', s.footer && pt(s.footer), FOOTER_MIN_PT);
    if (r.config.includes('winner')) check(r.still, 'winner line', s.winner && pt(s.winner), name);
  }
  console.log('\nFor information (not a gate): driver names and value labels at phone scale, against round 1\'s top-ten names (32 px = ' + pt(32).toFixed(2) + ' pt)');
  for (const r of report) console.log(`  ${r.still} (${r.config}): names ${r.sizes.name}px = ${pt(r.sizes.name).toFixed(2)} pt, values ${r.sizes.value}px = ${pt(r.sizes.value).toFixed(2)} pt${r.sizes.winner ? `, winner line ${r.sizes.winner}px = ${pt(r.sizes.winner).toFixed(2)} pt` : ''}`);
  console.log(ok ? '\nPHONE CHECK PASS' : '\nPHONE CHECK FAIL');
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
