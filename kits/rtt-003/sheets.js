/* RTT-003 design sheets (IQ-10), drawn inside the player page (after setup() with the film config) so
 * they use the player's own font, colours, bar styles and the same private pictures and logos.
 * Stills only, for Luke to judge working choices (b) maker colours and (e) pictures at icon size.
 * Loaded by render_stills.js with page.addScriptTag; nothing here runs in a video.
 */
(function () {
  'use strict';
  const MAT = {   // Machado, Oliveira & Fernandes 2009, severity 1.0, on linear sRGB
    'red-blind (protan)': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    'green-blind (deutan)': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    'blue-blind (tritan)': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]
  };
  const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const delin = c => { c = Math.min(1, Math.max(0, c)); return Math.round(255 * (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055)); };
  const rgb = h => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
  const hex = a => '#' + a.map(v => v.toString(16).padStart(2, '0')).join('').toUpperCase();
  const sim = (h, m) => { const v = rgb(h).map(lin); return hex(m.map(r => delin(r[0] * v[0] + r[1] * v[1] + r[2] * v[2]))); };
  const lum = h => { const [r, g, b] = rgb(h).map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  /* CIEDE2000 on the colours exactly as given (the player's deltaE first darkens light colours for
     white text, which would distort the simulated colours) */
  function lab(h) {
    const [r, g, b] = rgb(h).map(lin);
    const X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, Y = 0.2126 * r + 0.7152 * g + 0.0722 * b, Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883;
    const f = t => t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116;
    return [116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))];
  }
  function de00(h1, h2) {
    const [L1, a1, b1] = lab(h1), [L2, a2, b2] = lab(h2), rad = Math.PI / 180, deg = 180 / Math.PI, p7 = x => Math.pow(x, 7);
    const Cb = (Math.hypot(a1, b1) + Math.hypot(a2, b2)) / 2, G = 0.5 * (1 - Math.sqrt(p7(Cb) / (p7(Cb) + p7(25))));
    const a1p = (1 + G) * a1, a2p = (1 + G) * a2, C1p = Math.hypot(a1p, b1), C2p = Math.hypot(a2p, b2);
    const h1p = (Math.atan2(b1, a1p) * deg + 360) % 360, h2p = (Math.atan2(b2, a2p) * deg + 360) % 360;
    const dL = L2 - L1, dC = C2p - C1p; let dh = 0;
    if (C1p * C2p !== 0) { dh = h2p - h1p; if (dh > 180) dh -= 360; else if (dh < -180) dh += 360; }
    const dH = 2 * Math.sqrt(C1p * C2p) * Math.sin(dh / 2 * rad), Lb = (L1 + L2) / 2, Cbp = (C1p + C2p) / 2;
    let hb = h1p + h2p; if (C1p * C2p !== 0) hb = Math.abs(h1p - h2p) <= 180 ? hb / 2 : (hb < 360 ? (hb + 360) / 2 : (hb - 360) / 2);
    const T2 = 1 - 0.17 * Math.cos((hb - 30) * rad) + 0.24 * Math.cos(2 * hb * rad) + 0.32 * Math.cos((3 * hb + 6) * rad) - 0.20 * Math.cos((4 * hb - 63) * rad);
    const dth = 30 * Math.exp(-Math.pow((hb - 275) / 25, 2)), RC = 2 * Math.sqrt(p7(Cbp) / (p7(Cbp) + p7(25)));
    const SL = 1 + 0.015 * Math.pow(Lb - 50, 2) / Math.sqrt(20 + Math.pow(Lb - 50, 2)), SC = 1 + 0.045 * Cbp, SH = 1 + 0.015 * Cbp * T2, RT = -Math.sin(2 * dth * rad) * RC;
    return Math.sqrt(Math.pow(dL / SL, 2) + Math.pow(dC / SC, 2) + Math.pow(dH / SH, 2) + RT * (dC / SC) * (dH / SH));
  }

  function sheetColours() {
    baseTransform(); window.__LABELS = [];
    ctx.fillStyle = T.ground; ctx.fillRect(0, 0, 1920, 1080);
    ctx.fillStyle = T.ink; ctx.font = '700 50px ' + FONT; text('title', null, 'RTT-003 maker colours (proposal)', LEFT, 74, 'left');
    ctx.fillStyle = T.cap; ctx.font = '500 26px ' + FONT;
    text('sub', null, 'One colour per maker on the RTT-002 background; white names on every bar; the three looks the bars use', LEFT, 116, 'left');
    const cols = [{ x: 440, t: 'official' }, { x: 790, t: 'estimated' }, { x: 1140, t: 'analyst estimate' }];
    ctx.font = '600 24px ' + FONT; ctx.fillStyle = T.muted;
    for (const c of cols) text('head', null, c.t, c.x, 178, 'left');
    text('head', null, 'as colour-blind viewers see it', 1490, 150, 'left');
    ctx.font = '500 20px ' + FONT; ctx.fillStyle = T.cap;
    Object.keys(MAT).forEach((n, k) => text('sim', n, n.split(' ')[0], 1490 + k * 128, 182, 'left'));
    const names = Object.keys(MAT);
    MAKERS.forEach((m, i) => {
      const y = 205 + i * 132, col = darkenForWhite(CFG.palette[i]);
      ctx.fillStyle = '#F4F6FA'; rr(LEFT, y + 6, 150, 50, 8); ctx.fill();
      const im = LOGOIMG[m];
      if (im && im.naturalWidth) { const s = Math.min(134 / im.naturalWidth, 40 / im.naturalHeight);
        ctx.drawImage(im, LEFT + (150 - im.naturalWidth * s) / 2, y + 6 + (50 - im.naturalHeight * s) / 2, im.naturalWidth * s, im.naturalHeight * s); }
      ctx.fillStyle = T.ink; ctx.font = '600 34px ' + FONT; text('maker', m, MAKERNAME[m], LEFT + 168, y + 44, 'left');
      ctx.fillStyle = T.cap; ctx.font = '500 22px ' + FONT;
      text('hex', m, col + ' · white text ' + contrast(col, '#F4F6FA').toFixed(1) + ':1 · on background ' + contrast(col, T.ground).toFixed(1) + ':1', LEFT, y + 92, 'left');
      for (const [j, c] of cols.entries()) {
        drawStyledBar(c.x, y, 320, 62, col, ['official', 'estimated', 'analyst_estimate'][j]);
        ctx.fillStyle = '#F4F6FA'; ctx.font = '600 34px ' + FONT; text('bar', m, MAKERNAME[m], c.x + 16, y + 43, 'left');
      }
      names.forEach((n, k) => {
        const sc = sim(col, MAT[n]);
        ctx.fillStyle = sc; rr(1490 + k * 128, y, 112, 62, 4); ctx.fill();
      });
    });
    ctx.fillStyle = T.cap; ctx.font = '500 24px ' + FONT;
    const d = CFG.palette.map(darkenForWhite);
    let mins = { normal: 1e9 }; for (const n of names) mins[n] = 1e9;
    for (let a = 0; a < d.length; a++) for (let b = a + 1; b < d.length; b++) {
      mins.normal = Math.min(mins.normal, de00(d[a], d[b]));
      for (const n of names) mins[n] = Math.min(mins[n], de00(sim(d[a], MAT[n]), sim(d[b], MAT[n])));
    }
    text('foot', null, 'Closest pair of makers (CIEDE2000; RTT-002 asked 18 between drivers, on normal vision): normal vision ' + mins.normal.toFixed(1) + ' · ' +
      names.map(n => n.split(' ')[0] + ' ' + mins[n].toFixed(1)).join(' · '), LEFT, 900, 'left');
    text('foot', null, 'Simulation: Machado et al. 2009, full severity. Logos identify the maker only. Each bar also carries its console picture and name.', LEFT, 940, 'left');
    window.__SHEET = { mins };
  }

  const NOTE = {
    wii_u: 'plain black box; Wii U GamePad picture would read better',
    nintendo_switch: 'docked: the console is hidden; the red/blue Joy-Cons carry it',
    xbox_360: 'portrait: drawn narrow', playstation_5: 'portrait: drawn narrow',
    xbox_series: 'portrait and dark: a black tower', game_boy: 'portrait: drawn narrow',
    nintendo_switch_2: 'mostly black screen at this size', playstation_4: 'dark; the controller carries it',
    xbox_one: 'dark; the controller carries it', playstation_3: 'dark, glossy'
  };
  function sheetIcons() {
    baseTransform(); window.__LABELS = [];
    ctx.fillStyle = T.ground; ctx.fillRect(0, 0, 1920, 1080);
    ctx.fillStyle = T.ink; ctx.font = '700 44px ' + FONT; text('title', null, 'RTT-003 console pictures at their size on the board', LEFT, 64, 'left');
    const G = geom(), PW = G.PW, PH = G.PH;
    ctx.fillStyle = T.cap; ctx.font = '500 22px ' + FONT;
    text('sub', null, 'Box ' + PW + ' x ' + PH + ' px on the 1920 frame (12 rows). Grey notes = may read poorly (working choice e); no picture has been swapped.', LEFT, 100, 'left');
    const ids = TL.entrants.map(e => e.id);
    ids.forEach((id, i) => {
      const cx = LEFT + (i % 4) * 452, cy = 128 + Math.floor(i / 4) * 132;
      const im = PICIMG[id];
      ctx.save(); ctx.strokeStyle = 'rgba(244,246,250,0.18)'; ctx.setLineDash([4, 4]); ctx.strokeRect(cx + 0.5, cy + 0.5, PW - 1, PH - 1); ctx.restore();
      if (im && im.naturalWidth) { const s = Math.min(PW / im.naturalWidth, PH / im.naturalHeight);
        ctx.drawImage(im, cx + (PW - im.naturalWidth * s) / 2, cy + (PH - im.naturalHeight * s) / 2, im.naturalWidth * s, im.naturalHeight * s); }
      const tx = cx + PW + 16;
      ctx.fillStyle = T.ink; ctx.font = '600 26px ' + FONT; text('name', id, ENT[id].label, tx, cy + 26, 'left');
      if (NOTE[id]) { ctx.fillStyle = T.muted; ctx.font = '500 20px ' + FONT;
        const words = NOTE[id].split(' '); let line = '', ly = cy + 54;
        for (const w of words) { if (line && ctx.measureText(line + w).width > 300) { text('note', id, line.trim(), tx, ly, 'left'); line = ''; ly += 23; } line += w + ' '; }
        text('note', id, line.trim(), tx, ly, 'left'); }
    });
  }
  window.RTT003_SHEETS = { sheet_colours: sheetColours, sheet_icons: sheetIcons };
})();
