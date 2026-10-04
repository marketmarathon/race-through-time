/* RTT-001 stills (IQ-13, design pilot 1). Same method as kits/rtt-003/render_stills.js: draw a config frame by frame
 * up to a chosen month and save the 1920 x 1080 frame, plus the same frame as a phone shows a landscape video held
 * upright (390 points wide at 3 device pixels per point). Stills are private (DEC-006, DEC-060): write them only
 * outside the repo (the render workflow saves them to the private pre-release).
 *
 *   RTT_LOCAL_ASSETS=<private assets> node kits/rtt-001/render_stills.js OUT_DIR [still-name ...]
 *
 * stills.json entries:
 *   {name, config, at: "YYYY-MM-DD" (the last frame of that month's beat) | "final", overrides?, settle?}   a board still
 *       (the target frame is redrawn `settle` times, default 45, so rows caught mid-glide come to rest); after_sec
 *       instead takes the frame that many seconds after the month's first frame (a note or marker on screen), after_moment_sec
 *       that many seconds after the frame a callout's figures cross
 *       (overrides are merged into the config key by key, as "extends" does)
 *   {name, sheet}                                   a design sheet drawn in the player page (sheets.js)
 *   {name, compose: {title, cols, items: [{still, caption}]}}   earlier stills side by side with captions, so
 *       options can be compared in one picture (house style: options side by side in the same round)
 * Board stills and sheets also get a phone-size version; compositions do not (each of their parts has one).
 * Prints each file's SHA-256.
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const rtt = require('../rtt-002/rtt.js');
const CHROME = process.env.PW_CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const PHONE_PT = 390, DPR = 3;

function merge(base, over) {
  const out = Object.assign({}, base);
  for (const [k, v] of Object.entries(over || {}))
    out[k] = v && typeof v === 'object' && !Array.isArray(v) && base[k] && typeof base[k] === 'object' && !Array.isArray(base[k]) ? merge(base[k], v) : v;
  return out;
}
function stillConfig(s) { return merge(rtt.loadConfig('../rtt-001/' + s.config), s.overrides); }

/* the frame a still shows: the last frame of month `at`'s beat, or the film's last frame */
async function targetFrame(pg, s) {
  const info = await pg.evaluate(() => ({ dates: TL.events.map(e => e.date), start: TL.startFrame, raceFrames: RACE_FRAMES, opening: TL.openingEvent.date }));
  if (s.at === 'final') return info.raceFrames - 1;
  if (s.at === info.opening && !info.dates.includes(s.at)) return info.start[0] - 1;   // the opening board (e.g. January 1994)
  const k = info.dates.indexOf(s.at);
  if (k < 0) throw new Error(s.name + ': no month end ' + s.at + ' in ' + s.config);
  if (s.after_moment_sec != null) {               // a callout: that many seconds after the frame its figures cross
    const m = await pg.evaluate(d => (TL.moments || []).find(x => x.date === d), s.at);
    if (!m) throw new Error(s.name + ': no callout moment in ' + s.at);
    return m.frame + Math.round(s.after_moment_sec * 30);
  }
  if (s.after_sec != null) return info.start[k] + Math.round(s.after_sec * 30);     // a moment inside the month's beat
  return (k + 1 < info.start.length ? info.start[k + 1] : info.raceFrames) - 1;
}

async function main() {
  const out = path.resolve(process.argv[2]); const only = process.argv.slice(3);
  fs.mkdirSync(out, { recursive: true });
  const all = JSON.parse(fs.readFileSync(path.join(__dirname, 'stills.json'), 'utf8')).stills;
  const list = all.filter(s => !only.length || only.includes(s.name));
  const { chromium } = require(require.resolve('playwright', { paths: [rtt.KIT] }));
  const res = [], full = {};
  for (const s of list.filter(s => !s.compose)) {
    const cfg = stillConfig(s.sheet ? Object.assign({ config: 'config_rtt001_opt_C.json' }, s) : s);
    const data = JSON.parse(fs.readFileSync(path.resolve(rtt.KIT, cfg.race_file), 'utf8'));
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    if (s.sheet) {
      await pg.addScriptTag({ path: path.join(__dirname, 'sheets.js') });
      const meta = JSON.parse(fs.readFileSync(path.join(__dirname, 'logos.json'), 'utf8'));
      await pg.evaluate(([n, m]) => window.RTT001_SHEETS[n](m), [s.sheet, meta]);
    } else {
      const target = await targetFrame(pg, s);
      for (let f = 0; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
      /* the rows glide (0.55 s) and a monthly beat is shorter than that, so a still taken on a frame can catch two
         rows mid-overtake. Redrawing the same frame lets the glide settle, as a paused video would after a moment;
         values, colours and text are those of the target frame. */
      for (let i = 0; i < (s.settle != null ? s.settle : 45); i++) await rtt.drawFrame(pg, target, cfg);
    }
    const file = path.join(out, s.name + '_1920x1080.png');
    await (await pg.$('#c')).screenshot({ path: file });
    await br.close(); res.push(file); full[s.name] = file;
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
  /* compositions: each part at half size (960 x 540) with a caption, on the RTT background */
  const cp = await b2.newPage({ viewport: { width: 1940, height: 1200 }, deviceScaleFactor: 1 });
  const fontCss = path.join(path.dirname(require.resolve('@fontsource/archivo/package.json', { paths: [rtt.KIT] })), '600.css');
  for (const s of list.filter(s => s.compose)) {
    const C = s.compose, cols = C.cols || 2, rowsN = Math.ceil(C.items.length / cols);
    const cell = it => {
      const f = full[it.still] || path.join(out, it.still + '_1920x1080.png');
      if (!fs.existsSync(f)) throw new Error(s.name + ': part ' + it.still + ' was not rendered');
      return `<div style="width:960px"><div style="font:600 26px Archivo;color:#F4F6FA;margin:0 0 8px 2px">${it.caption}</div>` +
             `<img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:960px;display:block"></div>`;
    };
    await cp.setViewportSize({ width: cols * 960 + (cols - 1) * 20 + 40, height: 90 + rowsN * 590 });
    const html = path.join(out, '_compose.html');      // a file page, so the local Archivo stylesheet loads
    fs.writeFileSync(html, `<html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${fontCss}"></head><body style="margin:0;padding:20px;background:#0b1424">` +
      `<div style="font:600 32px Archivo;color:#AAB3C2;margin-bottom:16px">${C.title}</div>` +
      `<div style="display:grid;grid-template-columns:repeat(${cols},960px);gap:22px 20px">${C.items.map(cell).join('')}</div></body></html>`);
    await cp.goto('file://' + html);
    await cp.evaluate(async () => { await document.fonts.load('600 32px Archivo'); await document.fonts.ready; });
    if (!(await cp.evaluate(() => document.fonts.check('600 32px Archivo')))) throw new Error('Archivo did not load for ' + s.name);
    fs.unlinkSync(html);
    await cp.waitForTimeout(200);
    const file = path.join(out, s.name + '_sheet.png');
    await cp.screenshot({ path: file, fullPage: true }); res.push(file);
  }
  await b2.close();
  for (const f of res) console.log(crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex') + '  ' + path.basename(f));
}
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
module.exports = { merge, stillConfig, targetFrame };
