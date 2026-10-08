/* Race Through Time - the steps AFTER a money race (RTT-103, IQ-18b round 2; Luke's answers DEC-353..DEC-365).
 * Loaded by player_rtt.html; used only when a money race's config has `steps.enabled` (rtt_timeline.js buildSeries
 * schedules them after the race), so nothing here runs for RTT-001, RTT-002 or RTT-003.
 *
 * Each step is drawn on the player's canvas with the player's globals (ctx, T, FONT, LEFT, rr, text, tabText, ENT,
 * PICIMG, OVL, money, drawStyledBar, mixGround, mixWhite, darkenForWhite, wrapLines, nameSize, CFG, TL) as a pure
 * function of (step, seconds into the step), so any frame can be drawn on its own:
 *   plans   the 2026 plans step (DEC-338, DEC-360): range bars, each bar's period on its own line after its value
 *           (Cowork fix (e)); Microsoft "~$175bn" (its "approximately", fix (c)); Alibaba's Citi bar in the
 *           analyst-estimate look (fix (b)); ByteDance greyed (DEC-296); Tencent's 2026 note (DEC-343, DEC-356); the
 *           combined range in whole billions; Alphabet's share-sale card, then iCapital's card (DEC-358, DEC-361)
 *   look    one look-ahead board per year 2027-2030 (DEC-360): Race Through Time estimates, "~", dashed half-strength
 *           bars on a lighter hatched ground; bars, order and the total move from the previous board over move_sec
 *   line    the combined line 2010-2030 with the estimate band, the closing view of the look-ahead (DEC-360)
 *   peaks   forecasters disagree, one timeline (DEC-328, DEC-344, DEC-360); the rows appear one by one
 *   final   the race's last board with its one-line summary, held (DEC-363); drawn by the player
 * Every figure comes from the race file's `steps` (scripts/rtt103_adapter.py, copied from data/rtt-103 unchanged);
 * only display rounding is applied here. Labels go to window.__LABELS as in the race; window.__STEP describes the frame.
 */
(function (root) {
  const W = 1920, H = 1080, TEAL = '#2FD0C8', GOLD = '#E8B44A';
  const num = s => parseFloat(s);
  const ease = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u);
  const lerp = (a, b, f) => a + (b - a) * f;
  const tw = (kind, id, str, x, y, align) => { text(kind, id, str, x, y, align); const w = ctx.measureText(str).width; ctx.textAlign = 'left'; return w; };
  /* Display rounding only (the data has one decimal):
     'plan'   company plans as the companies give them: "$195–205bn", "$37.8bn" (".0" dropped)
     'actual' as the race: "$17.0bn"
     'whole'  whole billions, half up: "$903–937bn" (sums of plans given in whole billions, Cowork fix (c))
     'est'    Race Through Time estimates with "~": whole billions from $10bn, one decimal below; "~$1.47–1.52tn" from
              $1,000bn */
  function bn(lo, hi, mode) {
    const big = mode === 'est' && Math.max(lo, hi) >= 1000;
    const f = v => { const t = Math.round(v * 10);
      if (big) return (Math.floor((t + 50) / 100) / 100).toFixed(2);
      if (mode === 'whole' || (mode === 'est' && v >= 10)) return String(Math.floor((t + 5) / 10));
      if (mode === 'est' || mode === 'actual') return (t / 10).toFixed(1);
      return t % 10 ? (t / 10).toFixed(1) : String(t / 10); };
    const a = f(lo), b = f(hi);
    return (mode === 'est' ? '~' : '') + '$' + (a === b ? a : a + '–' + b) + (big ? 'tn' : 'bn');
  }
  function ground(col) { baseTransform(); window.__LABELS = []; ctx.globalAlpha = 1; ctx.fillStyle = col || T.ground; ctx.fillRect(0, 0, W, H); ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left'; }
  function logoBox() { for (const b of OVL) if (b.img) { const s = Math.min(b.w / b.img.naturalWidth, b.h / b.img.naturalHeight); ctx.drawImage(b.img, b.x + (b.w - b.img.naturalWidth * s) / 2, b.y + (b.h - b.img.naturalHeight * s) / 2, b.img.naturalWidth * s, b.img.naturalHeight * s); } }
  function pill(str, x, y, col) {
    ctx.font = '700 28px ' + FONT; const w = ctx.measureText(str).width + 32;
    ctx.fillStyle = col || TEAL; rr(x, y - 30, w, 42, 21); ctx.fill();
    ctx.fillStyle = T.ground; text('step_pill', null, str, x + 16, y, 'left'); ctx.textAlign = 'left'; return w;
  }
  function header(p, title, sub, col) {
    pill(p, LEFT, 52, col);
    ctx.fillStyle = T.ink; ctx.font = '700 46px ' + FONT; tw('title', null, title, LEFT, 118, 'left');
    if (sub) { ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT; tabText(sub, LEFT, 162, 'left', 'subtitle', null); }
    logoBox();
  }
  /* the footer: one line, or two when it does not fit (both in the bottom strip, house style 3) */
  function footer(t) {
    ctx.fillStyle = T.foot; ctx.font = '400 26px ' + FONT;
    if (ctx.measureText(t).width <= W - 2 * LEFT) { tw('footer', null, t, LEFT, H - 20, 'left'); return; }
    const parts = t.split(' · '); let a = '', i = 0;
    while (i < parts.length && ctx.measureText(a ? a + ' · ' + parts[i] : parts[i]).width <= W - 2 * LEFT) { a = a ? a + ' · ' + parts[i] : parts[i]; i++; }
    tw('footer', null, a, LEFT, H - 52, 'left'); tw('footer', null, parts.slice(i).join(' · '), LEFT, H - 20, 'left');
  }
  /* the company's tile, as on the race board (logo, or our own neutral tile) */
  function tile(id, x, y, w, h, alpha) {
    ctx.save(); ctx.globalAlpha = alpha == null ? 1 : alpha;
    const im = PICIMG[id], own = CFG.pictures && CFG.pictures.own && CFG.pictures.own[id];
    if (im && im.naturalWidth) {
      ctx.fillStyle = '#F4F6FA'; rr(x, y, w, h, 8); ctx.fill();
      const pad = 8, sc = Math.min((w - 2 * pad) / im.naturalWidth, (h - 2 * pad) / im.naturalHeight);
      ctx.drawImage(im, x + (w - im.naturalWidth * sc) / 2, y + (h - im.naturalHeight * sc) / 2, im.naturalWidth * sc, im.naturalHeight * sc);
    } else {
      const t = own ? own.text : (ENT[id] ? ENT[id].label : id === 'bytedance' ? 'ByteDance' : id); let fs = Math.round(h * 0.62);
      ctx.font = '700 ' + fs + 'px ' + FONT; while (fs > 12 && ctx.measureText(t).width > w - 20) { fs--; ctx.font = '700 ' + fs + 'px ' + FONT; }
      ctx.fillStyle = id === 'bytedance' ? '#3A4458' : (ENT[id] ? darkenForWhite(ENT[id].colour) : '#5A6375'); rr(x, y, w, h, 8); ctx.fill();
      ctx.fillStyle = id === 'bytedance' ? T.cap : '#F4F6FA'; ctx.textAlign = 'center'; ctx.fillText(t, x + w / 2, y + h / 2 + fs * 0.36); ctx.textAlign = 'left';
    }
    ctx.restore();
  }
  const colourOf = id => ENT[id] ? darkenForWhite(ENT[id].colour) : '#6E7480';
  /* a range bar: solid (or the analyst-estimate look) to the low end, half strength with a dashed outline to the high end */
  function rangeBar(x, y, w0, w1, h, col, est) {
    if (est) drawStyledBar(x, y, Math.max(3, w0), h, col, 'analyst_estimate'); else { ctx.fillStyle = col; rr(x, y, Math.max(3, w0), h, 2); ctx.fill(); }
    if (w1 > w0 + 2) {
      ctx.fillStyle = mixGround(col, est ? 0.72 : 0.55); ctx.fillRect(x + w0, y, w1 - w0, h);
      ctx.save(); ctx.strokeStyle = mixWhite(col, 0.35); ctx.lineWidth = 2.5; ctx.setLineDash([8, 6]);
      ctx.strokeRect(x + w0 + 1.25, y + 1.25, w1 - w0 - 2.5, h - 2.5); ctx.restore();
      ctx.fillStyle = mixWhite(col, 0.4); ctx.fillRect(x + w1 - 3, y - 6, 3, h + 12);
    }
  }
  function axis(x0, w, max, top, bottom, step) {
    ctx.font = '400 38px ' + FONT;
    for (let v = 0; v <= max * 1.001; v += step) { const x = x0 + w * v / max;
      ctx.fillStyle = T.axis; tabText(v ? '$' + v + 'bn' : '0', x, top - 8, 'center', 'axis', null);
      ctx.fillStyle = T.grid; ctx.fillRect(Math.round(x), top + 4, 1, bottom - top - 4); }
  }
  function panel(x, y, w, h, label, value, sub) {
    ctx.fillStyle = T.panel; rr(x, y, w, h, 12); ctx.fill();
    ctx.fillStyle = T.cap; ctx.font = '600 28px ' + FONT; tw('comb_label', null, label, x + 20, y + 44, 'left');
    ctx.fillStyle = T.ink; ctx.font = '800 60px ' + FONT; tabText(value, x + 20, y + 116, 'left', 'comb_value', null);
    if (sub) { ctx.fillStyle = T.cap; ctx.font = '500 26px ' + FONT; tw('comb_note', null, sub, x + 20, y + h - 20, 'left'); }
    window.__PANELS = (window.__PANELS || []).concat([{ x, y, w, h }]);
  }
  /* a card (story moment or estimate): date line, title, body lines, tag line; returns its box */
  function card(c, x, y, w, size, alpha) {
    const pad = 22; ctx.save(); ctx.globalAlpha = alpha;
    ctx.font = '700 ' + size + 'px ' + FONT; const who = wrapLines(c.who, w - 2 * pad);
    ctx.font = '500 ' + size + 'px ' + FONT; const body = wrapLines(c.text, w - 2 * pad);
    ctx.font = '500 ' + size + 'px ' + FONT; const sub = c.sub ? wrapLines(c.sub, w - 2 * pad) : [];
    ctx.font = '700 26px ' + FONT; const tags = c.tag ? wrapLines(c.tag.toUpperCase(), w - 2 * pad) : [];
    const lh = size + 8, h = pad * 2 + 30 + (who.length + body.length + sub.length) * lh + tags.length * 36 + (tags.length ? 6 : 0);
    ctx.fillStyle = T.panel; rr(x, y, w, h, 12); ctx.fill(); ctx.fillStyle = c.colour || TEAL; rr(x, y, 6, h, 3); ctx.fill();
    let yy = y + pad + 24;
    ctx.fillStyle = T.cap; ctx.font = '600 28px ' + FONT; tabText(c.when, x + pad, yy, 'left', 'card_when', null);
    ctx.fillStyle = T.ink; ctx.font = '700 ' + size + 'px ' + FONT; for (const l of who) { yy += lh; tw('card_who', null, l, x + pad, yy, 'left'); }
    ctx.font = '500 ' + size + 'px ' + FONT; for (const l of body) { yy += lh; tabText(l, x + pad, yy, 'left', 'card_text', null); }
    ctx.fillStyle = T.cap; for (const l of sub) { yy += lh; tabText(l, x + pad, yy, 'left', 'card_sub', null); }
    ctx.fillStyle = c.tagColour || T.cap; ctx.font = '700 26px ' + FONT; tags.forEach((l, i) => { yy += i ? 34 : 40; tw('card_tag', null, l, x + pad, yy, 'left'); });
    ctx.restore();
    const box = { x, y, w, h }; window.__CARDS = (window.__CARDS || []).concat([Object.assign({ when: c.when }, box)]); return box;
  }
  const fadeWin = (u, a, b, fi, fo) => u < a || u > b ? 0 : Math.min(1, (u - a) / fi, (b - u) / fo);
  const look = () => TL.steps.lookahead;
  const rowsFor = year => look().filter(r => r.frame_year === String(year) && r.row_type !== 'COMBINED');
  const combinedFor = year => look().find(r => r.frame_year === String(year) && r.row_type === 'COMBINED');
  const cid = r => r.company.toLowerCase();
  const SC = () => CFG.steps;

  /* ---- the 2026 plans step ---- */
  const PLAN_LABEL = {   // each bar's period, short (DEC-335; Cowork fix (e)); the long source detail is in the footer
    amazon: '2026 plan, as reported by Reuters', alphabet: '2026 plan', microsoft: '2026 plan, incl. finance leases',
    meta: '2026 plan, incl. finance-lease principal', oracle: 'year to May 2027, as reported by Reuters',
    coreweave: '2026 plan', alibaba: 'Citi estimate, year to Mar 2027', tencent: '12 months to Jun 2026',
    baidu: '12 months to Jun 2026 · no outlook given', bytedance: 'AI infrastructure · press report, unnamed sources' };
  const APPROX = { microsoft: true };   // the company's own words are "approximately $175 billion" (DEC-310; fix (c))
  function plans(u) {
    const S = SC().plans || {};
    ground(); header('2026 PLANS', 'What each company plans to spend in 2026', 'Each bar shows its own period · ranges as the companies give them');
    const rs = rowsFor(2026).slice().sort((a, b) => num(b.estimate_high_usd_bn) - num(a.estimate_high_usd_bn));
    const bd = TL.steps.bytedance_2026, BD = { company: 'ByteDance', estimate_low_usd_bn: bd.forecast_amount_usd_bn, estimate_high_usd_bn: bd.forecast_amount_usd_bn, grey: true };
    const list = rs.slice(); list.splice(list.findIndex(r => num(r.estimate_high_usd_bn) < num(BD.estimate_low_usd_bn)), 0, BD);
    const top = 232, bottom = 1000, rh = (bottom - top) / list.length, bh = Math.round(rh * 0.52), x0 = LEFT + 214, max = 240, bw = S.bar_w || 520;
    axis(x0, bw, max, top, bottom, 100);
    const vs = S.value_size || 34, ls = S.label_size || 30;
    list.forEach((r, i) => {
      const id = r.grey ? 'bytedance' : cid(r), col = r.grey ? '#5A6375' : colourOf(id), y = top + i * rh + (rh - bh) / 2;
      const lo = num(r.estimate_low_usd_bn), hi = num(r.estimate_high_usd_bn), citi = r.label === 'Citi estimate';
      tile(id, LEFT, y - 6, 196, bh + 12);
      if (r.grey) { ctx.save(); ctx.globalAlpha = 0.6; ctx.fillStyle = '#5A6375'; rr(x0, y, bw * lo / max, bh, 2); ctx.fill();
        ctx.strokeStyle = '#8492A6'; ctx.setLineDash([8, 6]); ctx.lineWidth = 2; rr(x0 + 1, y + 1, bw * lo / max - 2, bh - 2, 2); ctx.stroke(); ctx.restore(); }
      else rangeBar(x0, y, bw * lo / max, bw * hi / max, bh, col, citi);
      let x = x0 + bw * hi / max + 20, mid = y + bh / 2 + vs * 0.35;
      ctx.fillStyle = r.grey ? T.cap : T.ink; ctx.font = '700 ' + vs + 'px ' + FONT;
      const val = (r.grey ? 'more than ' : '') + (APPROX[id] ? '~' : '') + bn(lo, hi, r.label === 'actual' ? 'actual' : 'plan');
      x += tabText(val, x, mid, 'left', 'value', id) + 12;
      let lab = PLAN_LABEL[id] || r.period_label;
      if (id === 'tencent' && S.tencent_note) lab += ' · ' + S.tencent_note;
      ctx.fillStyle = T.cap; ctx.font = '500 ' + ls + 'px ' + FONT; tabText('· ' + lab, x, mid, 'left', 'period', id);
    });
    const C = combinedFor(2026), P = S.panel || { x: 1490, y: 770, w: 390, h: 180 };
    panel(P.x, P.y, P.w, P.h, 'Combined capital spending', bn(num(C.estimate_low_usd_bn), num(C.estimate_high_usd_bn), 'whole'), 'nine bars · not ByteDance');
    /* the cards (DEC-358: the share sale first; DEC-361: then iCapital), one at a time on the right */
    const K = S.card || { x: 1490, y: 236, w: 390, size: 32 };
    for (const c of S.cards || []) { const a = fadeWin(u, c.from, c.to, 0.3, 0.4); if (a > 0) card(c, K.x, K.y, K.w, K.size, a); }
    footer(S.footer || '');
    window.__STEP = { name: 'plans', rows: list.map(r => r.company) };
  }

  /* ---- a look-ahead board for one year, moving from the previous board ---- */
  function lookBoard(year, from, u) {
    const S = SC().look || {}, g = from == null ? 1 : ease(u / (S.move_sec || 1.2));
    ground('#101B30');
    ctx.save(); ctx.strokeStyle = 'rgba(47,208,200,0.10)'; ctx.lineWidth = 2;   // fine diagonal hatching over the whole frame
    for (let c = -H; c < W; c += 46) { ctx.beginPath(); ctx.moveTo(c, H); ctx.lineTo(c + H, 0); ctx.stroke(); } ctx.restore();
    header('LOOK-AHEAD · OUR ESTIMATES', 'Where the spending could go', 'Race Through Time estimates, not company forecasts · growth: FactSet consensus', GOLD);
    ctx.fillStyle = T.ink; ctx.font = '800 112px ' + FONT; tabText(String(year), 1680, 160, 'right', 'date_year', null);
    ctx.fillStyle = GOLD; ctx.font = '700 36px ' + FONT; tw('date_month', null, String(year) === '2030' ? 'estimate · least reliable year' : 'estimate', 1680, 60, 'right');
    const now = rowsFor(year), prev = from == null ? null : (from === 2026 ? rowsFor(2026) : rowsFor(from));
    const vals = r => [num(r.estimate_low_usd_bn), num(r.estimate_high_usd_bn)];
    const P = {}; if (prev) for (const r of prev) P[cid(r)] = vals(r);
    const order = rs => rs.slice().sort((a, b) => num(b.estimate_high_usd_bn) - num(a.estimate_high_usd_bn)).map(cid);
    const oNow = order(now), oPrev = prev ? order(prev) : oNow;
    const top = 232, bottom = 1000, rh = (bottom - top) / now.length, bh = rh * 0.62, x0 = LEFT + 214, max = 400, bw = 1000;
    axis(x0, bw, max, top, bottom, 100);
    for (const r of now) {
      const id = cid(r), [lo1, hi1] = vals(r), [lo0, hi0] = P[id] || [lo1, hi1], lo = lerp(lo0, lo1, g), hi = lerp(hi0, hi1, g);
      const yi = lerp(oPrev.indexOf(id) < 0 ? oNow.indexOf(id) : oPrev.indexOf(id), oNow.indexOf(id), g), y = top + yi * rh + (rh - bh) / 2;
      tile(id, LEFT, y - 2, 196, bh + 4, 0.9);
      rangeBar(x0, y, bw * lo / max, bw * hi / max, bh, colourOf(id), true);
      ctx.font = '600 38px ' + FONT; const nm = ENT[id].label, inside = ctx.measureText(nm).width + 40 < bw * lo / max;
      let x = x0 + bw * hi / max + 18;
      if (inside) { ctx.fillStyle = '#F4F6FA'; tw('name', id, nm, x0 + 18, y + bh / 2 + 13, 'left'); }
      else { ctx.fillStyle = T.ink; x += tw('name', id, nm, x, y + bh / 2 + 13, 'left') + 16; }
      const citi = r.row_type === 'CITI_ESTIMATE';
      ctx.fillStyle = T.ink; ctx.font = '700 38px ' + FONT; x += tabText(bn(lo, hi, citi ? 'actual' : 'est'), x, y + bh / 2 + 13, 'left', 'value', id) + 14;
      const tag = citi ? '· Citi estimate, year to Mar ' + (+year + 1) : (/Probably high/.test(r.notes) ? '· probably high' : '');
      if (tag) { ctx.fillStyle = T.cap; ctx.font = '500 32px ' + FONT; tabText(tag, x, y + bh / 2 + 13, 'left', 'tag', id); }
    }
    const C = combinedFor(year), C0 = from == null ? C : combinedFor(from);
    const clo = lerp(num(C0.estimate_low_usd_bn), num(C.estimate_low_usd_bn), g), chi = lerp(num(C0.estimate_high_usd_bn), num(C.estimate_high_usd_bn), g);
    panel(1380, 700, 500, 190, 'Combined capital spending', bn(clo, chi, 'est'), 'sum of the nine bars · ' + year);
    footer(S.footer || '');
    window.__STEP = { name: 'look', year, from, landed: g >= 1, rows: oNow };
  }

  /* ---- the combined line 2010-2030, the closing view of the look-ahead ---- */
  function line(u) {
    const S = SC().line || {};
    ground();
    header('LOOK-AHEAD · OUR ESTIMATES', 'Combined capital spending, 2010–2030', 'Each point is a 12-month total at the middle of its period · band: 2026 plans, then our estimates', GOLD);
    const x0 = 230, x1 = 1830, y0 = 250, y1 = 950, t0 = 2010, t1 = 2031, max = 1600;
    const X = t => x0 + (x1 - x0) * (t - t0) / (t1 - t0), Y = v => y1 - (y1 - y0) * v / max;
    const mid = d => +d.slice(0, 4) + (+d.slice(5, 7)) / 12 - 0.5;           // the middle of the 12 months to date d
    ctx.fillStyle = 'rgba(232,180,74,0.07)'; ctx.fillRect(X(2027), y0 - 10, X(2031) - X(2027), y1 - y0 + 10);
    ctx.fillStyle = 'rgba(232,180,74,0.09)'; ctx.fillRect(X(2030), y0 - 10, X(2031) - X(2030), y1 - y0 + 10);
    ctx.font = '400 38px ' + FONT;
    for (let v = 0; v <= max; v += 400) { ctx.fillStyle = T.axis; tabText(v ? (v >= 1000 ? '$' + (v / 1000) + 'tn' : '$' + v + 'bn') : '0', x0 - 16, Y(v) + 12, 'right', 'axis', null); ctx.fillStyle = T.grid; ctx.fillRect(x0, Math.round(Y(v)), x1 - x0, 1); }
    for (let t = 2010; t <= 2030; t += 5) { ctx.fillStyle = T.axis; tabText(String(t), X(t + 0.5), y1 + 46, 'center', 'axis', null); }
    const A = TL.allCombined;
    ctx.strokeStyle = TEAL; ctx.lineWidth = 5; ctx.lineJoin = 'round'; ctx.beginPath();
    A.forEach((e, i) => { const x = X(mid(e.date)), y = Y(e.c / 1e9); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke();
    const yrs = [2026, 2027, 2028, 2029, 2030].map(y => ({ y, t: y + 0.5, lo: num(combinedFor(y).estimate_low_usd_bn), hi: num(combinedFor(y).estimate_high_usd_bn) }));
    const lastE = A[A.length - 1], lx = X(mid(lastE.date)), ly = Y(lastE.c / 1e9), a = ease(u / (S.band_sec || 1.0));
    ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = 'rgba(232,180,74,0.55)'; ctx.beginPath(); ctx.moveTo(lx, ly);
    yrs.forEach(p => ctx.lineTo(X(p.t), Y(p.hi))); yrs.slice().reverse().forEach(p => ctx.lineTo(X(p.t), Y(p.lo))); ctx.closePath(); ctx.fill();
    yrs.forEach(p => { ctx.fillStyle = GOLD; ctx.beginPath(); ctx.arc(X(p.t), Y((p.lo + p.hi) / 2), 5, 0, Math.PI * 2); ctx.fill(); });
    const p26 = yrs[0], p30 = yrs[4];
    ctx.fillStyle = T.ink; ctx.font = '700 34px ' + FONT; tabText(bn(p26.lo, p26.hi, 'whole'), X(p26.t) - 24, Y(p26.hi) - 20, 'right', 'value', null);
    ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT; tw('value_sub', null, '2026 plans', X(p26.t) - 24, Y(p26.hi) - 60, 'right');
    ctx.fillStyle = T.ink; ctx.font = '700 34px ' + FONT; tabText(bn(p30.lo, p30.hi, 'est'), X(p30.t) - 18, Y(p30.hi) - 22, 'right', 'value', null);
    ctx.fillStyle = GOLD; ctx.font = '600 30px ' + FONT; tw('band', null, '2030: least reliable year', X(2031), y0 - 24, 'right');
    tw('band', null, 'our estimates', X(2027) + 12, y1 - 24, 'left');
    ctx.restore();
    ctx.fillStyle = T.ink; ctx.font = '700 34px ' + FONT; tabText(money(lastE.c), lx + 10, ly + 48, 'left', 'value', null);
    ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT; tw('value_sub', null, '12 months to June 2026', lx + 10, ly + 86, 'left');
    footer(S.footer || '');
    window.__STEP = { name: 'line' };
  }

  /* ---- forecasters disagree on the peak: one timeline; rows appear one by one ---- */
  function peaks(u) {
    const S = SC().peaks || {};
    ground();
    header('WHEN DOES IT PEAK?', 'Forecasters disagree on when the spending peaks', 'Each row is a different forecaster and a different measure · none is added to the race');
    const x0 = 680, x1 = 1820, t0 = 2026, t1 = 2031, X = t => x0 + (x1 - x0) * (t - t0) / (t1 - t0), y0 = 300;
    for (let t = 2026; t <= 2030; t++) { ctx.fillStyle = T.axis; ctx.font = '600 38px ' + FONT; tabText(String(t), X(t + 0.5), y0 - 30, 'center', 'axis', null); ctx.fillStyle = T.grid; ctx.fillRect(Math.round(X(t)), y0, 1, 640); }
    ctx.fillStyle = T.grid; ctx.fillRect(Math.round(X(2031)), y0, 1, 640);
    const rows = [
      { who: 'BCG', sub: 'US big five together', peak: 2029, col: '#7FA7FF', txt: 'peak' },
      { who: 'AI capex (Allianz)', sub: 'AI spending only', peak: 2028, col: GOLD, txt: 'peak · about $1trn (AI only)' },
      { who: 'FactSet consensus', sub: 'company by company', peak: null, col: TEAL, txt: '4 of 5 still rising in 2030 (Oracle: 2027)' } ];
    rows.forEach((r, i) => {
      const a = ease((u - 0.3 - i * (S.row_gap_sec || 1.2)) / 0.5); if (a <= 0) return;
      ctx.save(); ctx.globalAlpha = a;
      const y = y0 + 110 + i * 200;
      ctx.fillStyle = T.ink; ctx.font = '800 40px ' + FONT; tw('row_who', null, r.who, LEFT, y, 'left');
      ctx.fillStyle = T.cap; ctx.font = '500 32px ' + FONT; tw('row_sub', null, r.sub, LEFT, y + 44, 'left');
      ctx.strokeStyle = mixGround(r.col, 0.4); ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(X(2026.1), y - 10);
      if (r.peak) { ctx.lineTo(X(r.peak + 0.5), y - 10); ctx.stroke(); ctx.fillStyle = r.col; ctx.beginPath(); ctx.arc(X(r.peak + 0.5), y - 10, 20, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = T.ink; ctx.font = '700 36px ' + FONT; tw('row_peak', null, r.txt, X(r.peak + 0.5) + 32, y + 2, 'left'); }
      else { ctx.lineTo(X(2031) - 10, y - 10); ctx.stroke(); ctx.fillStyle = r.col; ctx.beginPath(); ctx.moveTo(X(2031) + 14, y - 10); ctx.lineTo(X(2031) - 18, y - 32); ctx.lineTo(X(2031) - 18, y + 12); ctx.closePath(); ctx.fill();
        ctx.fillStyle = T.ink; ctx.font = '700 36px ' + FONT; tw('row_peak', null, r.txt, X(2028.6), y - 34, 'center'); }
      ctx.restore();
    });
    footer(S.footer || '');
    window.__STEP = { name: 'peaks' };
  }

  root.RTT_STEPS = { plans, lookBoard, line, peaks, bn, card };
})(typeof window !== 'undefined' ? window : this);
