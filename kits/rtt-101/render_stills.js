/* RTT-101 stills (IQ-21, design round 1; adapted from kits/rtt-102/render_stills.js, which is not changed). Draw a config
 * up to a chosen month and save the 1920 x 1080 frame, plus the same frame as a phone shows a landscape video held
 * upright (390 points wide at 3 device pixels per point). Stills are private (DEC-006, DEC-060): write them only outside
 * the repo (the render workflow saves them to the private pre-release).
 *
 *   RTT_LOCAL_ASSETS=<private assets> node kits/rtt-101/render_stills.js OUT_DIR [still-name ...]
 *
 * stills.json entries:
 *   {name, config, at: "YYYY-MM-DD" | "final", overrides?, settle?, warm?, cvd?}   a board still on the frame where that
 *       month's figures land (never mid-move, house style 6). The race is wound up from `warm` frames before the target
 *       (default 120: the rank glide settles in about ten time constants of 0.55 s) and the target frame is then redrawn
 *       `settle` times (default 150: the 0.55 s glide closes all but 0.01% of a gap), as a paused video would come to rest; values, colours and text are the target frame's.
 *       cvd "protan" | "deutan": the frame as a person with protanopia or deuteranopia would see it (Machado, Oliveira &
 *       Fernandes 2009, severity 1, in linear RGB; the colour-blind check of item e).
 *       after_sec: that many seconds after the month's first frame (motion stills only); card: the story card dated `at`,
 *       after_sec into its own time.
 *   {name, config, step, step_sec}           a step after the race (the closing view), step_sec seconds into step `step`
 *   {name, compose: {title, cols, phone?, items: [{still, caption}]}}   earlier stills side by side with captions;
 *       phone true puts the phone-size copies side by side instead (item b, board size at phone size)
 * Board stills get a phone-size copy; compositions do not (each of their parts has one). Prints each file's SHA-256.
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const rtt = require('../rtt-002/rtt.js');
const CHROME = process.env.PW_CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const PHONE_PT = 390, DPR = 3;
const CVD = { protan: [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
              deutan: [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]] };

function merge(base, over) {
  const out = Object.assign({}, base);
  for (const [k, v] of Object.entries(over || {}))
    out[k] = v && typeof v === 'object' && !Array.isArray(v) && base[k] && typeof base[k] === 'object' && !Array.isArray(base[k]) ? merge(base[k], v) : v;
  return out;
}
function stillConfig(s) { return merge(rtt.loadConfig('../rtt-101/' + s.config), s.overrides); }

async function targetFrame(pg, s) {
  const info = await pg.evaluate(() => ({ dates: TL.events.map(e => e.date), start: TL.startFrame, qe: TL.quarterEndFrame, raceFrames: RACE_FRAMES, opening: TL.openingEvent.date, steps: TL.stepPlan || null }));
  if (s.step != null) { const st = info.steps[s.step]; return st.first + Math.round((s.step_sec || 0) * 30); }
  if (s.at === 'final') return (info.steps ? info.steps[0].first : info.raceFrames) - 1;
  if (s.at === info.opening && !info.dates.includes(s.at)) return info.start[0] - 1;   // the opening board (July 1992)
  const k = info.dates.indexOf(s.at);
  if (k < 0) throw new Error(s.name + ': no month end ' + s.at + ' in ' + s.config);
  if (s.card) {
    const f0 = await pg.evaluate(d => { const q = storySchedule().find(x => x.it.at === d && !x.it.plain); return q ? q.f0 : null; }, s.at);
    if (f0 == null) throw new Error(s.name + ': no story card dated ' + s.at);
    return f0 + Math.round((s.after_sec || 0) * 30);
  }
  if (s.after_sec != null) return info.start[k] + Math.round(s.after_sec * 30);
  return info.qe[k];
}

async function main() {
  const out = path.resolve(process.argv[2]); const only = process.argv.slice(3);
  fs.mkdirSync(out, { recursive: true });
  const all = JSON.parse(fs.readFileSync(path.join(__dirname, 'stills.json'), 'utf8')).stills;
  const list = all.filter(s => !only.length || only.includes(s.name) || (s.compose && s.compose.items.some(i => only.includes(i.still))));
  const { chromium } = require(require.resolve('playwright', { paths: [rtt.KIT] }));
  const res = [], full = {};
  for (const s of list.filter(s => !s.compose)) {
    const cfg = stillConfig(s);
    const data = JSON.parse(fs.readFileSync(path.resolve(rtt.KIT, cfg.race_file), 'utf8'));
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    const target = await targetFrame(pg, s);
    const raceEnd = await pg.evaluate(() => TL.raceEnd || null);
    const from = s.step != null ? target : Math.max(0, target - (s.warm != null ? s.warm : 120));
    for (let f = from; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
    if (!raceEnd || target < raceEnd) for (let i = 0; i < (s.settle != null ? s.settle : 150); i++) await rtt.drawFrame(pg, target, cfg);
    if (s.cvd) await pg.evaluate(M => {           // the colour-blind view of the drawn frame (linear RGB)
      const c = document.getElementById('c'), x = c.getContext('2d'), im = x.getImageData(0, 0, c.width, c.height), d = im.data;
      const L = new Float32Array(256); for (let i = 0; i < 256; i++) { const v = i / 255; L[i] = v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
      const g = v => { v = Math.min(1, Math.max(0, v)); return Math.round(255 * (v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055)); };
      for (let i = 0; i < d.length; i += 4) { const r = L[d[i]], gg = L[d[i + 1]], b = L[d[i + 2]];
        d[i] = g(M[0][0] * r + M[0][1] * gg + M[0][2] * b); d[i + 1] = g(M[1][0] * r + M[1][1] * gg + M[1][2] * b); d[i + 2] = g(M[2][0] * r + M[2][1] * gg + M[2][2] * b); }
      x.putImageData(im, 0, 0); }, CVD[s.cvd]);
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
  const cp = await b2.newPage({ viewport: { width: 1940, height: 1200 }, deviceScaleFactor: 1 });
  const fontCss = path.join(path.dirname(require.resolve('@fontsource/archivo/package.json', { paths: [rtt.KIT] })), '600.css');
  for (const s of list.filter(s => s.compose)) {
    const C = s.compose, cols = C.cols || 2, rowsN = Math.ceil(C.items.length / cols), W = C.phone ? 585 : 960, H = Math.round(W * 9 / 16);
    const cell = it => {
      const f = (C.phone ? path.join(out, it.still + '_phone_390pt.png') : (full[it.still] || path.join(out, it.still + '_1920x1080.png')));
      if (!fs.existsSync(f)) throw new Error(s.name + ': part ' + it.still + ' was not rendered');
      return `<div style="width:${W}px"><div style="font:600 ${C.phone ? 22 : 26}px Archivo;color:#F4F6FA;margin:0 0 8px 2px">${it.caption}</div>` +
             `<img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:${W}px;display:block"></div>`;
    };
    await cp.setViewportSize({ width: cols * W + (cols - 1) * 20 + 40, height: 90 + rowsN * (H + 60) });
    const html = path.join(out, '_compose.html');
    fs.writeFileSync(html, `<html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${fontCss}"></head><body style="margin:0;padding:20px;background:#0b1424">` +
      `<div style="font:600 30px Archivo;color:#AAB3C2;margin-bottom:16px;max-width:${cols * W}px">${C.title}</div>` +
      `<div style="display:grid;grid-template-columns:repeat(${cols},${W}px);gap:22px 20px">${C.items.map(cell).join('')}</div></body></html>`);
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
