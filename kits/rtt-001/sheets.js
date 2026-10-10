/* RTT-001 design sheets (IQ-13), drawn inside the player page after setup() with option C's config, so they use the
 * player's own font, colours and bar looks. Stills only: the palette (brief item 6) and the title wordings (item 10).
 * Loaded by render_stills.js with page.addScriptTag; nothing here runs in a video.
 */
(function () {
  'use strict';
  const MAT = {   // Machado, Oliveira & Fernandes 2009, severity 1.0, on linear sRGB (as kits/rtt-003/sheets.js)
    'red-blind': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    'green-blind': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    'blue-blind': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]
  };
  const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const delin = c => { c = Math.min(1, Math.max(0, c)); return Math.round(255 * (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055)); };
  const rgb = h => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
  const hex = a => '#' + a.map(v => v.toString(16).padStart(2, '0')).join('').toUpperCase();
  const sim = (h, m) => { const v = rgb(h).map(lin); return hex(m.map(r => delin(r[0] * v[0] + r[1] * v[1] + r[2] * v[2]))); };
  const lum = h => { const [r, g, b] = rgb(h).map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };

  /* every browser that ever reaches the top 10 of the drawn board, in order of first appearance */
  function onBoard() {
    const seen = [];
    for (const s of [TL.opening].concat(TL.states)) for (const id of s.order.slice(0, NROWS)) if (!seen.includes(id)) seen.push(id);
    return seen;
  }

  function sheetPalette() {
    baseTransform(); window.__LABELS = [];
    ctx.fillStyle = T.ground; ctx.fillRect(0, 0, 1920, 1080);
    ctx.fillStyle = T.ink; ctx.font = '700 44px ' + FONT; text('title', null, 'RTT-001 browser colours (proposal)', LEFT, 62, 'left');
    ctx.fillStyle = T.cap; ctx.font = '500 22px ' + FONT;
    text('sub', null, 'One colour per browser for the whole film, near its familiar colour. Each row: the bar as drawn, the estimated look (before 2009), and the colour as red-, green- and blue-blind viewers see it.', LEFT, 96, 'left');
    const ids = onBoard(), per = Math.ceil(ids.length / 2), rowH = 58;
    ids.forEach((id, i) => {
      const col = Math.floor(i / per), x = LEFT + col * 912, y = 128 + (i % per) * rowH, c = darkenForWhite(ENT[id].colour);
      drawStyledBar(x, y, 300, 44, c, 'official');
      ctx.fillStyle = '#F4F6FA'; ctx.font = '600 26px ' + FONT; text('bar', id, ENT[id].label, x + 12, y + 31, 'left');
      drawStyledBar(x + 312, y, 90, 44, c, 'estimated');
      Object.values(MAT).forEach((m, k) => { ctx.fillStyle = sim(c, m); rr(x + 414 + k * 58, y, 50, 44, 4); ctx.fill(); });
      ctx.fillStyle = T.cap; ctx.font = '500 20px ' + FONT;
      text('hex', id, c + ' · white ' + contrast(c, '#F4F6FA').toFixed(1) + ':1 · bg ' + contrast(c, T.ground).toFixed(1) + ':1', x + 594, y + 29, 'left');
    });
    /* closest pair of browsers that can be on screen together (top 10 this month or the three before, DEC-023) */
    const tops = [TL.opening].concat(TL.states).map(s => s.order.slice(0, NROWS));
    let mn = 1e9, mp = '';
    for (let k = 0; k < tops.length; k++) {
      const V = new Set(); for (let j = Math.max(0, k - 3); j <= k; j++) tops[j].forEach(x => V.add(x));
      const a = [...V];
      for (let i = 0; i < a.length; i++) for (let j = i + 1; j < a.length; j++) {
        const d = RTT_TIMELINE.deltaE(ENT[a[i]].colour, ENT[a[j]].colour); if (d < mn) { mn = d; mp = ENT[a[i]].label + ' / ' + ENT[a[j]].label; } }
    }
    ctx.fillStyle = T.cap; ctx.font = '500 22px ' + FONT;
    text('foot', null, 'Closest pair that can be on screen together: CIEDE2000 ' + mn.toFixed(1) + ' (' + mp + '); the house rule asks for at least 18. Browser names are always on the bars.', LEFT, 1040, 'left');
    window.__SHEET = { ids, min: mn, pair: mp };
  }

  const TITLES = [
    { t: 'Most-Used Web Browsers (share of web browsing)', note: 'Claude’s pick: says what is measured; “estimated” stays on the source line' },
    { t: 'Browser Wars: Share of Web Browsing', note: 'shorter, uses the series name' },
    { t: 'Most-Used Web Browsers (share of browsing, estimated before 2009)', note: 'the brief’s example: complete, but it runs into the date' }
  ];
  function sheetTitles() {
    baseTransform(); window.__LABELS = [];
    ctx.fillStyle = T.ground; ctx.fillRect(0, 0, 1920, 1080);
    const S = CFG.source_line, TLB = CFG.time_label;
    TITLES.forEach((o, i) => {
      const y0 = 40 + i * 340;
      ctx.fillStyle = T.panel; rr(24, y0 - 20, 1872, 300, 12); ctx.fill();
      ctx.fillStyle = T.ink; ctx.font = '700 50px ' + FONT;
      const tw = ctx.measureText(o.t).width; text('title', null, o.t, LEFT, y0 + 54, 'left');
      ctx.fillStyle = T.cap || T.muted; ctx.font = '500 ' + TLB.size + 'px ' + FONT;
      const dw = tabText('October 1998', TLB.x, y0 + 54, 'right', 'time_line', null);
      ctx.font = '500 ' + S.size + 'px ' + FONT;
      tabText('Source: University of Illinois EWS web server (hosts visiting one university server) · estimated', LEFT, y0 + 104, 'left', 'source_line', null);
      const fits = LEFT + tw + 40 <= TLB.x - dw;
      ctx.fillStyle = fits ? T.rule : '#F06A6A'; ctx.font = '600 26px ' + FONT;
      text('verdict', null, (i + 1) + '. ' + o.note + ' — ' + (fits ? 'fits beside the date' : 'too long: overlaps the date line'), LEFT, y0 + 190, 'left');
      ctx.fillStyle = T.cap; ctx.font = '500 22px ' + FONT;
      text('width', null, 'title ' + Math.round(tw) + ' px wide at 50 px; the date line starts at x ' + Math.round(TLB.x - dw), LEFT, y0 + 230, 'left');
    });
  }
  /* IQ-13b/13c (DEC-180, DEC-182): every browser that reaches the board with its logo exactly as drawn there (the tile
     at board size and at 1.5x; IE's 'e' cropped from its file, IE Mobile sharing it; our own neutral tile where no real
     logo exists), with the file's status. meta is logos.json, passed in by render_stills.js. */
  function sheetLogos(meta) {
    baseTransform(); window.__LABELS = [];
    ctx.fillStyle = T.ground; ctx.fillRect(0, 0, 1920, 1080);
    ctx.fillStyle = T.ink; ctx.font = '700 40px ' + FONT; text('title', null, 'RTT-001 browser logos (owner decisions; identification only)', LEFT, 56, 'left');
    ctx.fillStyle = T.cap; ctx.font = '500 20px ' + FONT;
    text('sub', null, 'Every browser that reaches the top 10, its logo as on the board (left) and larger (right). Free = public domain or a free licence; non-free = used only to identify the browser.', LEFT, 88, 'left');
    const by = {}; for (const L of meta.logos) by[L.browser_id] = L;
    const ids = onBoard(), per = 10, rowH = 94, G = geom(), box = G.PW, big = 82;
    ids.forEach((id, i) => {
      const col = Math.floor(i / per), x = LEFT + col * 610, y = 112 + (i % per) * rowH;
      const L = by[id] && by[id].same_as ? by[by[id].same_as] : by[id];
      const tile = (tx, ty, sz) => {
        const im = PICIMG[id], own = PIC.own && PIC.own[id];
        if (im) { ctx.fillStyle = '#F4F6FA'; rr(tx, ty, sz, sz, 8); ctx.fill();
          const cr = (PIC.crop && PIC.crop[id]) || { x: 0, y: 0, w: im.naturalWidth || 1, h: im.naturalHeight || 1 }, pad = 6 * sz / box, sc = Math.min((sz - 2 * pad) / cr.w, (sz - 2 * pad) / cr.h);
          if (Math.max(cr.w, cr.h) <= 64) ctx.imageSmoothingEnabled = false;
          ctx.drawImage(im, cr.x, cr.y, cr.w, cr.h, tx + (sz - cr.w * sc) / 2, ty + (sz - cr.h * sc) / 2, cr.w * sc, cr.h * sc); ctx.imageSmoothingEnabled = true; }
        else if (own) { ctx.fillStyle = darkenForWhite(ENT[id].colour); rr(tx, ty, sz, sz, 8); ctx.fill(); ctx.fillStyle = '#F4F6FA'; ctx.textAlign = 'center';
          let fs = Math.round(sz * 0.30); ctx.font = '700 ' + fs + 'px ' + FONT; while (fs > 10 && ctx.measureText(own.text).width > sz - 10) { fs--; ctx.font = '700 ' + fs + 'px ' + FONT; }
          ctx.fillText(own.text, tx + sz / 2, ty + sz * 0.50); ctx.font = '500 ' + Math.round(sz * 0.24) + 'px ' + FONT; ctx.fillText(String(own.year), tx + sz / 2, ty + sz * 0.82); ctx.textAlign = 'left'; }
        else { ctx.strokeStyle = '#F06A6A'; ctx.lineWidth = 2; rr(tx + 1, ty + 1, sz - 2, sz - 2, 8); ctx.stroke(); } };
      tile(x, y + (big - box) / 2, box); tile(x + box + 12, y, big);
      const tx = x + box + big + 24;
      const fit = t => { let u = String(t); while (u.length > 3 && ctx.measureText(u).width > x + 595 - tx) u = u.slice(0, -2); return u === String(t) ? u : u.trimEnd() + '\u2026'; };
      ctx.fillStyle = T.ink; ctx.font = '600 24px ' + FONT; text('name', id, ENT[id].label, tx, y + 28, 'left');
      ctx.fillStyle = T.cap; ctx.font = '500 17px ' + FONT;
      const own = meta.own_tiles && meta.own_tiles[id];
      const l1 = own ? 'Our own neutral tile: no logo found' : L ? (/non-free/.test(L.status || '') ? 'non-free: identification use only' : 'free \u00b7 ' + (L.licence || '')) : 'NO LOGO', l2 = own ? own.why : L ? (L.commons_title ? L.commons_title.replace('File:', '') : L.site) + (by[id] && by[id].same_as ? ' (as Internet Explorer)' : '') + (L.crop ? ' \u00b7 cropped' : '') : '';
      text('lic', id, fit(l1), tx, y + 52, 'left'); text('src', id, fit(l2), tx, y + 74, 'left');
    });
  }
  /* date/era round (DEC-215, DEC-216): the five era pictures - our own drawings, made from plain shapes in the player
     (drawDevice) - large and at their size in the film, with the proposed switch dates from era.eras. */
  function sheetDevices() {
    baseTransform(); window.__LABELS = [];
    ctx.fillStyle = T.ground; ctx.fillRect(0, 0, 1920, 1080);
    ctx.fillStyle = T.ink; ctx.font = '700 40px ' + FONT; text('title', null, 'RTT-001 era pictures (proposal): our own drawings, no photos, logos or brands', LEFT, 56, 'left');
    ctx.fillStyle = T.cap; ctx.font = '500 22px ' + FONT;
    text('sub', null, 'Each is drawn from plain shapes by the player. Top: large. Bottom: the size in the film (240 x 200 px on the 1920 frame). Each change crossfades over 2 s.', LEFT, 92, 'left');
    const names = { crt: 'CRT monitor + modem', tower: 'Desktop tower', laptop: 'Laptop', phone_early: 'Early touch phone', phone_modern: 'Modern phone' };
    const M = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const eras = ERA.eras, cw = (1920 - 2 * LEFT) / eras.length;
    eras.forEach((e, i) => {
      const x = LEFT + i * cw;
      ctx.fillStyle = T.panel; rr(x + 6, 120, cw - 12, 900, 12); ctx.fill();
      drawDevice(e.device, x + 16, 140, cw - 32, (cw - 32) * 200 / 240, 1, null);
      drawDevice(e.device, x + (cw - 240) / 2, 520, 240, 200, 1, null);
      ctx.fillStyle = T.ink; ctx.font = '700 28px ' + FONT; text('name', e.device, names[e.device] || e.device, x + 20, 790, 'left');
      ctx.fillStyle = T.cap; ctx.font = '600 26px ' + FONT;
      const until = i + 1 < eras.length ? eras[i + 1].from : null, mo = d => M[+d.slice(5, 7) - 1] + ' ' + d.slice(0, 4);
      text('from', e.device, 'from ' + mo(e.from), x + 20, 836, 'left');
      text('until', e.device, until ? 'to the end of ' + (+until.slice(0, 4) - 1) : 'to the end of the film', x + 20, 872, 'left');
    });
  }
  /* era photos (DEC-221): the contact sheet - every shortlisted photo (config_rtt001_photo_sheet.json loads them all), one
     row per era, three to a row, drawn exactly as in the film (tile, crop, background), with author, licence and Claude's
     recommended pick marked. */
  function sheetPhotos() {
    baseTransform(); window.__LABELS = [];
    ctx.fillStyle = T.ground; ctx.fillRect(0, 0, 1920, 1080);
    ctx.fillStyle = T.ink; ctx.font = '700 36px ' + FONT; text('title', null, 'RTT-001 era photos: the shortlist (Wikimedia Commons, commercial-use licences)', LEFT, 48, 'left');
    ctx.fillStyle = T.cap; ctx.font = '500 20px ' + FONT;
    text('sub', null, 'Each row is one era; each tile is drawn as in the film (300 x 225 px there). Gold outline = Claude\'s recommended pick (used in the stills). Under each: what it shows, photographer, licence.', LEFT, 78, 'left');
    const rows = ['crt', 'tower', 'laptop', 'phone_early', 'phone_modern'];
    const names = { crt: ['Mid-1990s', 'beige CRT desktop'], tower: ['2000s', 'desktop tower'], laptop: ['Mid-2000s', 'laptop'], phone_early: ['Around 2009', 'first touch phones'], phone_modern: ['2015 on', 'modern phone'] };
    const tw = 220, th = 165, rowH = 196, x0 = LEFT + 230, cw = 548, capw = cw - tw - 34;
    rows.forEach((dev, r) => {
      const y = 98 + r * rowH, list = ERA.eras.filter(e => e.device === dev);
      ctx.fillStyle = T.ink; ctx.font = '700 24px ' + FONT; text('era', dev, names[dev][0], LEFT, y + 40, 'left');
      ctx.fillStyle = T.cap; ctx.font = '500 20px ' + FONT; text('era2', dev, names[dev][1], LEFT, y + 70, 'left');
      list.forEach((e, i) => {
        const x = x0 + i * cw;
        drawEraPhoto(e, x, y, tw, th, 1);
        if (e.recommended) { ctx.save(); ctx.strokeStyle = '#F5C542'; ctx.lineWidth = 4; rr(x - 3, y - 3, tw + 6, th + 6, 14); ctx.stroke(); ctx.restore(); }
        ctx.fillStyle = T.ink; ctx.font = '600 19px ' + FONT;
        const fit = (s, w) => { let u = s; while (u.length > 3 && ctx.measureText(u).width > w) u = u.slice(0, -2); return u === s ? u : u.trimEnd() + '\u2026'; };
        text('label', dev, fit((e.recommended ? '\u2605 ' : '') + e.label, capw), x + tw + 12, y + 30, 'left');
        ctx.fillStyle = T.cap; ctx.font = '500 16px ' + FONT;
        const words = (e.credit || '').split(' · ');
        text('credit', dev, fit(words[0] || '', capw), x + tw + 12, y + 58, 'left');
        text('licence', dev, fit(words[1] || '', capw), x + tw + 12, y + 80, 'left');
      });
    });
  }
  window.RTT001_SHEETS = { sheet_palette: sheetPalette, sheet_titles: sheetTitles, sheet_logos: sheetLogos, sheet_devices: sheetDevices, sheet_photos: sheetPhotos };
})();
