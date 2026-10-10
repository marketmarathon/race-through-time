/* Race Through Time - the steps AFTER a money race (RTT-103, IQ-18b round 2; Luke's answers DEC-353..DEC-365).
 * Loaded by player_rtt.html; used only when a money race's config has `steps.enabled` (rtt_timeline.js buildSeries
 * schedules them after the race), so nothing here runs for RTT-001, RTT-002 or RTT-003.
 *
 * Each step is drawn on the player's canvas with the player's globals (ctx, T, FONT, LEFT, rr, text, tabText, ENT,
 * PICIMG, OVL, money, drawStyledBar, mixGround, mixWhite, darkenForWhite, wrapLines, nameSize, CFG, TL) as a pure
 * function of (step, seconds into the step), so any frame can be drawn on its own:
 *   explain IQ-18c (DEC-371): after the race has carried on through the 2026 plans and the 2027-2030 estimates (drawn
 *           by the player as race boards, cfg.forward), one short page saying what those figures are and how they
 *           were made; the 2026 plans step and the look-ahead boards of round 2 are gone (Luke: "just jumping to that
 *           other thing is just not what you would expect in a bar chart race")
 *   line    the combined line 2010-2030 with the estimate band, the closing view of the look-ahead (DEC-360)
 *   peaks   forecasters disagree, one timeline (DEC-328, DEC-344, DEC-360); the rows appear one by one
 *   final   the June 2026 board with its one-line summary, held (DEC-363); drawn by the player
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
  const look = () => TL.steps.lookahead;
  const combinedFor = year => look().find(r => r.frame_year === String(year) && r.row_type === 'COMBINED');
  const SC = () => CFG.steps;

  /* ---- IQ-18c (DEC-371): the explanation after 2030, before the combined line. Luke: "you can have the explanation at
     the end". One short page: a bold lead and a few plain lines per point (cfg.steps.explain.items [{lead, text}]),
     each point fading in row_gap_sec after the one before; the full sources in the footer. ---- */
  function explain(u) {
    const S = SC().explain || {}, items = S.items || [], LW = S.lead_w || 330, size = S.size || 36, lead = S.lead_size || 38, lh = size + 12;
    ground();
    header(S.pill || 'ABOUT THE ESTIMATES', S.title || '', S.sub || '', GOLD);
    let y = S.top || 268;
    items.forEach((it, i) => {
      ctx.font = '500 ' + size + 'px ' + FONT; const lines = wrapLines(it.text, W - 2 * LEFT - LW);
      const a = ease((u - 0.2 - i * (S.row_gap_sec != null ? S.row_gap_sec : 0.5)) / 0.4);
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = it.colour || GOLD; ctx.font = '700 ' + lead + 'px ' + FONT; tw('explain_lead', null, it.lead, LEFT, y + size, 'left');
      ctx.fillStyle = T.ink; ctx.font = '500 ' + size + 'px ' + FONT;
      lines.forEach((l, j) => tabText(l, LEFT + LW, y + size + j * lh, 'left', 'explain_text', null));
      ctx.restore();
      y += lines.length * lh + (S.item_gap || 30);
    });
    footer(S.footer || '');
    window.__STEP = { name: 'explain', bottom: y };
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

  root.RTT_STEPS = { explain, line, peaks, bn };
})(typeof window !== 'undefined' ? window : this);
