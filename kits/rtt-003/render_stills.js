/* RTT-003 stills (IQ-10): draw a config up to a chosen moment and save the 1920 x 1080 frame, plus the
 * same frame as a phone shows a landscape video held upright (390 points wide at 3 device pixels per
 * point, as tests/player/phone_check.js). Stills are private (DEC-006, DEC-060): write them only
 * outside the repo (the render workflow saves them to the private pre-release).
 *
 *   RTT_LOCAL_ASSETS=<private assets> node kits/rtt-003/render_stills.js OUT_DIR [still-name ...]
 *
 * Every frame from 0 to the target is drawn in order (the rank glide is stateful). A still is named in
 * stills.json: {name, config, at: "YYYY-MM-DD" (the last frame of that quarter end's beat) | "final"
 * (the last frame of the final table)}. Prints each file's SHA-256.
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const rtt = require('../rtt-002/rtt.js');
const CHROME = process.env.PW_CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const PHONE_PT = 390, DPR = 3;

async function main() {
  const out = path.resolve(process.argv[2]); const only = process.argv.slice(3);
  fs.mkdirSync(out, { recursive: true });
  const list = JSON.parse(fs.readFileSync(path.join(__dirname, 'stills.json'), 'utf8')).stills.filter(s => !only.length || only.includes(s.name));
  const { chromium } = require(require.resolve('playwright', { paths: [rtt.KIT] }));
  const res = [];
  for (const s of list) {
    if (s.sheet) {                                  // a design sheet, drawn in the player page (sheets.js)
      const cfg = rtt.loadConfig('../rtt-003/config_rtt003_film.json');
      const data = JSON.parse(fs.readFileSync(path.resolve(rtt.KIT, cfg.race_file), 'utf8'));
      const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
      await pg.addScriptTag({ path: path.join(__dirname, 'sheets.js') });
      await pg.evaluate(n => window.RTT003_SHEETS[n](), s.sheet);
      const file = path.join(out, s.name + '_1920x1080.png');
      await (await pg.$('#c')).screenshot({ path: file });
      await br.close(); res.push(file); continue;
    }
    const cfg = rtt.loadConfig('../rtt-003/' + s.config, s.overrides);
    const data = JSON.parse(fs.readFileSync(path.resolve(rtt.KIT, cfg.race_file), 'utf8'));
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    const info = await pg.evaluate(() => ({ dates: TL.events.map(e => e.date), start: TL.startFrame, raceFrames: RACE_FRAMES }));
    let target;
    if (s.at === 'final') target = info.raceFrames - 1;
    else { const k = info.dates.indexOf(s.at); if (k < 0) throw new Error(s.name + ': no quarter end ' + s.at + ' in ' + s.config);
           target = (k + 1 < info.start.length ? info.start[k + 1] : info.raceFrames) - 1; }
    for (let f = 0; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
    const file = path.join(out, s.name + '_1920x1080.png');
    await (await pg.$('#c')).screenshot({ path: file });
    await br.close();
    res.push(file);
  }
  const b2 = await chromium.launch({ executablePath: CHROME });
  const ph = await b2.newPage({ viewport: { width: PHONE_PT, height: Math.round(PHONE_PT * 9 / 16) }, deviceScaleFactor: DPR });
  for (const f of res.slice()) {
    const src = 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
    await ph.setContent(`<body style="margin:0;background:#000"><img src="${src}" style="width:${PHONE_PT}px;display:block"></body>`);
    await ph.waitForLoadState('load');
    const pf = f.replace('_1920x1080.png', '_phone_390pt.png');
    await ph.screenshot({ path: pf }); res.push(pf);
  }
  await b2.close();
  for (const f of res) console.log(crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex') + '  ' + path.basename(f));
}
main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
