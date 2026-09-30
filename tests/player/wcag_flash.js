/* Measure the winner highlight against the WCAG 2.x general-flash and red-flash thresholds (DEC-077).
 *
 * Usage: node tests/player/wcag_flash.js [config]   (default config_rtt002_film.json; about 10 minutes)
 *
 * Every frame of the race is drawn in order (the rank glide is stateful). On every frame on which a
 * winner highlight is lit, the same frame is drawn a second time with the highlight switched off (the
 * rows restored to the same positions first), and the two images are compared pixel by pixel:
 *   - general flash pixel: relative luminance (sRGB, WCAG formula) differs by 0.1 or more and the darker
 *     of the two is below 0.8 (WCAG 2.x "general flash");
 *   - red flash pixel: the pixel changes and either state is a saturated red, R / (R + G + B) >= 0.8
 *     (WCAG 2.2 "red flash", conservative: any change involving a saturated red counts);
 * and the largest number of such pixels inside any 640 x 360 window is found (WCAG's estimate of a 10-degree
 * visual field is a 341 x 256 rectangle at 1024 x 768, i.e. a third of the screen each way; 640 x 360 on the
 * 1920 x 1080 frame). WCAG 2.x passes content if there are no more than three flashes in any second OR the
 * combined area of concurrent flashes is no more than 25% of any 10-degree field; highlights of bars that are
 * lit at the same moment (a new winner plus earlier ones still fading) are measured together.
 * Prints JSON. Definitions taken from WCAG 2.2 as known to Claude; w3.org was not reachable from the container.
 */
const fs = require('fs');
const KIT = '/home/user/race-through-time/kits/rtt-002';
const rtt = require(KIT + '/rtt.js');
(async () => {
  const cfg = rtt.loadConfig(process.argv[2] || 'config_rtt002_film.json');
  const data = JSON.parse(fs.readFileSync(KIT + '/race_rtt002.json'));
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: '/opt/pw-browsers/chromium' });
  await pg.evaluate(() => {
    const lin = new Float64Array(256);
    for (let i = 0; i < 256; i++) { const c = i / 255; lin[i] = c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
    window.__LIN = lin;
    window.__measure = (t, WW, WH) => {
      const ids = Object.keys(ENT), pre = ids.map(id => ENT[id]._y);
      drawAt(t);
      const lit = window.__BARS.filter(b => b.hl > 0 && b.alpha > 0);
      if (!lit.length) return null;
      const post = ids.map(id => ENT[id]._y);
      const A = ctx.getImageData(0, 0, 1920, 1080).data;
      ids.forEach((id, i) => { ENT[id]._y = pre[i]; });
      const hl = HL; HL = null; drawAt(t); HL = hl;
      const B = ctx.getImageData(0, 0, 1920, 1080).data;
      ids.forEach((id, i) => { ENT[id]._y = post[i]; });
      drawAt(t);                                     // leave the canvas and state exactly as a normal frame
      ids.forEach((id, i) => { ENT[id]._y = post[i]; });
      const W = 1920, H = 1080, L = window.__LIN;
      const g = new Int32Array((W + 1) * (H + 1)), r = new Int32Array((W + 1) * (H + 1));
      let maxdL = 0, nG = 0, nR = 0, nChanged = 0;
      for (let y = 0; y < H; y++) {
        let rg = 0, rr = 0;
        for (let x = 0; x < W; x++) {
          const p = (y * W + x) * 4;
          const ra = A[p], ga = A[p + 1], ba = A[p + 2], rb = B[p], gb = B[p + 1], bb = B[p + 2];
          let fg = 0, fr = 0;
          if (ra !== rb || ga !== gb || ba !== bb) {
            nChanged++;
            const la = 0.2126 * L[ra] + 0.7152 * L[ga] + 0.0722 * L[ba];
            const lb = 0.2126 * L[rb] + 0.7152 * L[gb] + 0.0722 * L[bb];
            const d = Math.abs(la - lb); if (d > maxdL) maxdL = d;
            if (d >= 0.1 && Math.min(la, lb) < 0.8) { fg = 1; nG++; }
            const sa = ra + ga + ba, sb = rb + gb + bb;
            if ((sa > 0 && ra / sa >= 0.8) || (sb > 0 && rb / sb >= 0.8)) { fr = 1; nR++; }
          }
          rg += fg; rr += fr;
          const i = (y + 1) * (W + 1) + x + 1;
          g[i] = g[i - W - 1] + rg; r[i] = r[i - W - 1] + rr;
        }
      }
      const box = (S, x, y) => S[(y + WH) * (W + 1) + x + WW] - S[y * (W + 1) + x + WW] - S[(y + WH) * (W + 1) + x] + S[y * (W + 1) + x];
      let bg = 0, bgAt = null, brd = 0;
      for (let y = 0; y + WH <= H; y += 2) for (let x = 0; x + WW <= W; x += 2) {
        const a = box(g, x, y); if (a > bg) { bg = a; bgAt = [x, y]; }
        const b = box(r, x, y); if (b > brd) brd = b;
      }
      return { lit: lit.map(b => b.id + ':' + b.hl.toFixed(2) + ':' + b.colour), maxdL, nG, nR, nChanged, winG: bg, winR: brd, at: bgAt };
    };
  });
  const tl = rtt.frameTotals(cfg, data).tl, WW = 640, WH = 360, area = WW * WH;
  let worst = { winG: -1 }, worstR = { winR: -1 }, worstL = { maxdL: -1 }, measured = 0;
  const colours = {};
  for (let f = 0; f < tl.raceFrames; f++) {
    const m = await pg.evaluate(([t, WW, WH]) => window.__measure(t, WW, WH), [f / cfg.fps, WW, WH]);
    if (!m) continue;
    measured++; m.f = f;
    for (const s of m.lit) { const c = s.split(':')[2]; colours[c] = true; }
    if (m.winG > worst.winG) worst = m;
    if (m.winR > worstR.winR) worstR = m;
    if (m.maxdL > worstL.maxdL) worstL = m;
  }
  await br.close();
  const pct = n => (100 * n / area).toFixed(2) + '% of a 640x360 (10-degree) window';
  const out = { config: cfg.kit_version, frames_with_highlight: measured, window_px: [WW, WH],
    general: { worst_window_px: worst.winG, worst_window: pct(worst.winG), frame: worst.f, lit: worst.lit, whole_frame_px: worst.nG },
    red: { worst_window_px: worstR.winR, worst_window: pct(worstR.winR), frame: worstR.f, lit: worstR.lit },
    max_luminance_change: { value: +worstL.maxdL.toFixed(4), frame: worstL.f, lit: worstL.lit },
    bar_colours_lit: Object.keys(colours).sort() };
  console.log(JSON.stringify(out, null, 1));
})().catch(e => { console.error(e); process.exit(2); });
