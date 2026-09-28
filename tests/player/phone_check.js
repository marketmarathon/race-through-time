/* IQ-04 step 7: the phone check.
 *
 * Two 1920x1080 stills from the full RTT-002 run (a crowded mid-history board and the final
 * board), then each shown as a phone shows a landscape video held upright: the full frame
 * 390 points wide (iPhone 12-16 class) at 3 device pixels per point, plus a crop of the bottom
 * left (footer, the smallest label) at that same scale. Also measures every label's size on
 * the frame and at phone scale.
 *
 * Usage: node tests/player/phone_check.js      Output: tests/output/phone/ (gitignored)
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const KITDIR = path.join(ROOT, 'kits', 'rtt-002');
const rtt = require(path.join(KITDIR, 'rtt.js'));
const OUT = path.join(ROOT, 'tests', 'output', 'phone');
const PHONE_PT = 390, DPR = 3;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const cfg = rtt.loadConfig('config.json');
  const data = JSON.parse(fs.readFileSync(path.join(KITDIR, cfg.race_file), 'utf8'));
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: process.env.PW_CHROME || '/opt/pw-browsers/chromium' });
  const info = await pg.evaluate(() => ({ start: TL.startFrame, races: TL.events.map(e => e.race_index), raceFrames: RACE_FRAMES }));
  // still A: the last frame of the 1988 Australian Grand Prix slot (race index 468 in data/rtt-002, last race of 1988);
  // still B: the final board, one second before the closing card
  const kA = info.races.indexOf(468);
  const targets = [
    { name: 'still_A_1988', frame: info.start[kA + 1] - 1 },
    { name: 'still_B_final', frame: info.raceFrames - cfg.fps }
  ];
  const el = await pg.$('#c');
  const report = [];
  let f = 0;
  for (const t of targets) {
    for (; f <= t.frame; f++) await pg.evaluate(tt => drawAt(tt), f / cfg.fps);   // glide is stateful
    const png = path.join(OUT, t.name + '_1920.png');
    await el.screenshot({ path: png });
    const labels = await pg.evaluate(() => window.__LABELS);
    const sizes = {};
    for (const l of labels) if (l.alpha > 0.5) sizes[l.kind] = Math.min(sizes[l.kind] || 1e9, l.size);
    report.push({ still: t.name, frame: t.frame, sizes });
  }
  await br.close();

  // the phone view: the 1920 still displayed PHONE_PT points wide
  const { chromium } = require(require.resolve('playwright', { paths: [KITDIR] }));
  const b2 = await chromium.launch({ executablePath: process.env.PW_CHROME || '/opt/pw-browsers/chromium', args: ['--disable-background-networking', '--disable-component-update'] });
  const ph = await b2.newPage({ viewport: { width: PHONE_PT, height: Math.round(PHONE_PT * 9 / 16) }, deviceScaleFactor: DPR });
  for (const t of targets) {
    const src = 'data:image/png;base64,' + fs.readFileSync(path.join(OUT, t.name + '_1920.png')).toString('base64');
    await ph.setContent(`<body style="margin:0;background:#000"><img src="${src}" style="width:${PHONE_PT}px;display:block"></body>`);
    await ph.waitForLoadState('load');
    await ph.screenshot({ path: path.join(OUT, t.name + '_phone_full.png') });
    // bottom-left quarter at phone scale: footer, lower bars and their values
    await ph.screenshot({ path: path.join(OUT, t.name + '_phone_crop_bottomleft.png'),
                          clip: { x: 0, y: PHONE_PT * 9 / 16 / 2, width: PHONE_PT / 2, height: PHONE_PT * 9 / 16 / 2 } });
  }
  await b2.close();

  const k = PHONE_PT / 1920;
  const lines = ['still,frame,label,px_on_1920_frame,points_on_phone_' + PHONE_PT + 'pt_wide'];
  for (const r of report) for (const [kind, px] of Object.entries(r.sizes).sort((a, b) => a[1] - b[1]))
    lines.push([r.still, r.frame, kind, px, (px * k).toFixed(1)].join(','));
  fs.writeFileSync(path.join(OUT, 'label_sizes.csv'), lines.join('\n') + '\n');
  console.log(lines.join('\n'));
})().catch(e => { console.error(e); process.exit(2); });
