/* RTT-003 full film against the WCAG 2.x general-flash and red-flash thresholds (round 6, DEC-149).
 *
 * Usage: RTT_LOCAL_ASSETS=<private assets> node tests/player/wcag_flash_rtt003.js [config]
 *        (default ../rtt-003/config_rtt003_film.json; about 20 minutes)
 *
 * RTT-002's check (tests/player/wcag_flash.js, DEC-077) measured its winner highlight. RTT-003 has no highlight,
 * so this check measures the WHOLE picture: every frame of the film is drawn in order at 1920 x 1080 (as the
 * render draws it; the 3840 x 2160 master is the same drawing at twice the pixels, so areas scale exactly) and
 * every pixel's relative luminance (sRGB, WCAG formula) is followed from frame to frame:
 *   - a TRANSITION is a change of 0.1 or more in relative luminance from the pixel's last extreme, in the
 *     opposite direction to its previous transition, where the darker state is below 0.8 (WCAG 2.x "general
 *     flash": a flash is a pair of opposing transitions);
 *   - a RED transition is a transition in which either state is a saturated red, R / (R + G + B) >= 0.8;
 *   - a pixel FLASHES TOO OFTEN at a frame when it has made 8 or more transitions (more than three flashes) in
 *     the last 30 frames (one second at 30 fps); red counted separately;
 *   - WCAG 2.x passes content if there are no more than three flashes in any second OR the combined area of
 *     concurrent flashes is no more than 25% of any 10-degree visual field: WCAG's estimate of a 10-degree
 *     field is 341 x 256 at 1024 x 768, a third of the screen each way, i.e. 640 x 360 px on the 1920 x 1080
 *     frame, and 25% of it = 57,600 px. The largest number of too-often-flashing pixels inside any 640 x 360
 *     window (8 px steps) is reported for every frame; the film FAILS if it ever exceeds 57,600 (general or red).
 * Also reported (as RTT-002's report did): the largest area of pixels making a transition on the SAME frame
 * inside any 10-degree window, and the largest single luminance transition of any pixel.
 * Diagnostic: FLASH_DUMP=<frame> FLASH_DUMP_PNG=<file outside the repo> stops at that frame and saves it with the
 * too-often-flashing pixels in magenta (a private still: never commit it).
 * Prints JSON. Definitions taken from WCAG 2.2 as known to Claude (w3.org was blocked from the container on
 * 30 Sep 2026); a measurement against a published guideline, not a medical assessment.
 */
const fs = require('fs');
const path = require('path');
const KIT = path.resolve(__dirname, '..', '..', 'kits', 'rtt-002');
const rtt = require(path.join(KIT, 'rtt.js'));
(async () => {
  const cfg = rtt.loadConfig(process.argv[2] || '../rtt-003/config_rtt003_film.json');
  const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file)));
  if (!process.env.RTT_LOCAL_ASSETS) console.error('note: RTT_LOCAL_ASSETS not set - pictures and logos missing (use the real private files)');
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: process.env.PW_CHROME || '/opt/pw-browsers/chromium' });
  const DUMP = process.env.FLASH_DUMP != null ? +process.env.FLASH_DUMP : null;   // diagnostic: stop at this frame and save it
  const frames = DUMP != null ? DUMP + 1 : await pg.evaluate(() => RACE_FRAMES);
  if (DUMP != null) await pg.evaluate(f => { window.__DUMP = f; }, DUMP);
  await pg.evaluate(() => {
    const W = 1920, H = 1080, N = W * H, K = 8;       // keep the last 8 transition frames per pixel
    const lin = new Float64Array(256);
    for (let i = 0; i < 256; i++) { const c = i / 255; lin[i] = c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
    const S = window.__FL = { W, H, N, K, lin, ext: new Float32Array(N), dir: new Int8Array(N), red: new Uint8Array(N),
      tg: new Int32Array(N * K).fill(-1e9), tr: new Int32Array(N * K).fill(-1e9), ig: new Uint8Array(N), ir: new Uint8Array(N),
      first: true, maxStep: 0, maxStepAt: -1 };
    const winMax = (mask) => {                         // largest count of set pixels in any 640 x 360 window, 8 px steps
      const I = new Int32Array((W + 1) * (H + 1));
      for (let y = 0; y < H; y++) { let rs = 0; for (let x = 0; x < W; x++) { rs += mask[y * W + x]; I[(y + 1) * (W + 1) + x + 1] = I[y * (W + 1) + x + 1] + rs; } }
      let best = 0, bx = 0, by = 0;
      for (let y = 0; y + 360 <= H; y += 8) for (let x = 0; x + 640 <= W; x += 8) {
        const v = I[(y + 360) * (W + 1) + x + 640] - I[y * (W + 1) + x + 640] - I[(y + 360) * (W + 1) + x] + I[y * (W + 1) + x];
        if (v > best) { best = v; bx = x; by = y; } }
      return { best, x: bx, y: by };
    };
    window.__flash = (f) => {
      drawAt(f / FPS);
      const d = ctx.getImageData(0, 0, W, H).data, L = S.lin;
      const now = new Uint8Array(N), fastG = new Uint8Array(N), fastR = new Uint8Array(N);
      let nNow = 0, nFastG = 0, nFastR = 0;
      for (let p = 0; p < N; p++) {
        const r = d[p * 4], g = d[p * 4 + 1], b = d[p * 4 + 2];
        const l = 0.2126 * L[r] + 0.7152 * L[g] + 0.0722 * L[b], s = r + g + b, isRed = s > 0 && r / s >= 0.8 ? 1 : 0;
        if (S.first) { S.ext[p] = l; S.red[p] = isRed; continue; }
        const e = S.ext[p], dl = l - e;
        if (S.dir[p] >= 0 && l > e && S.dir[p] === 1) { S.ext[p] = l; S.red[p] = isRed; }        // still rising: new peak
        else if (S.dir[p] <= 0 && l < e && S.dir[p] === -1) { S.ext[p] = l; S.red[p] = isRed; }  // still falling: new trough
        else if (Math.abs(dl) >= 0.1 && Math.min(l, e) < 0.8) {                                  // a transition
          const k = S.ig[p]; S.tg[p * S.K + k] = f; S.ig[p] = (k + 1) % S.K; now[p] = 1; nNow++;
          if (isRed || S.red[p]) { const kr = S.ir[p]; S.tr[p * S.K + kr] = f; S.ir[p] = (kr + 1) % S.K; }
          S.dir[p] = dl > 0 ? 1 : -1; S.ext[p] = l; S.red[p] = isRed;
          if (Math.abs(dl) > S.maxStep) { S.maxStep = Math.abs(dl); S.maxStepAt = f; }
        }
        // 8 transitions within the last 30 frames = the oldest of the 8 kept is at most 29 frames old
        if (S.tg[p * S.K + S.ig[p]] > -1e8 && f - S.tg[p * S.K + S.ig[p]] < 30) { fastG[p] = 1; nFastG++; }
        if (S.tr[p * S.K + S.ir[p]] > -1e8 && f - S.tr[p * S.K + S.ir[p]] < 30) { fastR[p] = 1; nFastR++; }
      }
      S.first = false;
      const out = { f, nNow, nFastG, nFastR };
      if (nNow > 57600 / 4) out.nowWin = winMax(now).best;          // only worth a window scan when it could matter
      else out.nowWin = nNow;                                        // upper bound
      out.fastGWin = nFastG > 0 ? winMax(fastG) : { best: 0 };
      out.fastRWin = nFastR > 0 ? winMax(fastR) : { best: 0 };
      if (window.__DUMP === f) {                       // diagnostic: the frame, with too-often-flashing pixels in magenta
        const c2 = document.createElement('canvas'); c2.width = W; c2.height = H; const x2 = c2.getContext('2d');
        const im = x2.createImageData(W, H);
        for (let p = 0; p < N; p++) { const q = p * 4, m = fastG[p] || fastR[p];
          im.data[q] = m ? 255 : d[q] * 0.5; im.data[q + 1] = m ? 0 : d[q + 1] * 0.5; im.data[q + 2] = m ? 255 : d[q + 2] * 0.5; im.data[q + 3] = 255; }
        x2.putImageData(im, 0, 0); out.dump = c2.toDataURL('image/png');
      }
      return out;
    };
  });
  const LIMIT = 57600;
  const res = { config: cfg.kit_version, frames, limit_px_10deg: LIMIT, worst: { now: { best: 0 }, fastG: { best: 0 }, fastR: { best: 0 } },
                framesWithFastG: 0, framesWithFastR: 0, maxFastGTotal: 0, maxFastRTotal: 0, pass: true };
  for (let f = 0; f < frames; f++) {
    const o = await pg.evaluate(fr => window.__flash(fr), f);
    if (o.nowWin > res.worst.now.best) res.worst.now = { best: o.nowWin, f };
    if (o.fastGWin.best > res.worst.fastG.best) res.worst.fastG = { ...o.fastGWin, f };
    if (o.fastRWin.best > res.worst.fastR.best) res.worst.fastR = { ...o.fastRWin, f };
    if (o.nFastG) res.framesWithFastG++; if (o.nFastR) res.framesWithFastR++;
    res.maxFastGTotal = Math.max(res.maxFastGTotal, o.nFastG); res.maxFastRTotal = Math.max(res.maxFastRTotal, o.nFastR);
    if (o.dump) fs.writeFileSync(process.env.FLASH_DUMP_PNG || 'flash_dump.png', Buffer.from(o.dump.split(',')[1], 'base64'));
    if (f % 1000 === 0) console.error(`frame ${f}/${frames}`);
  }
  const st = await pg.evaluate(() => ({ maxStep: window.__FL.maxStep, maxStepAt: window.__FL.maxStepAt }));
  res.maxLuminanceStep = st;
  res.pass = res.worst.fastG.best <= LIMIT && res.worst.fastR.best <= LIMIT;
  await br.close();
  console.log(JSON.stringify(res, null, 1));
  process.exit(res.pass ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
