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
  window.RTT001_SHEETS = { sheet_palette: sheetPalette, sheet_titles: sheetTitles };
})();
