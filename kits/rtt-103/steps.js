/* RTT-103 design round 1 (IQ-18): the steps AFTER the race, drawn as option stills in the player page (like
 * kits/rtt-001/sheets.js). Nothing here is in a film yet (DEC-069): each function draws one option for Luke to choose.
 * Every figure comes from the race file's `steps` (scripts/rtt103_adapter.py, copied from data/rtt-103 unchanged); the
 * only change is display rounding, and Race Through Time estimates carry "~" (RTT-001's approved estimate look, DEC-185).
 * Uses the player's globals (ctx, T, FONT, LEFT, rr, text, tabText, ENT, PICIMG, OVL, darkenForWhite, mixGround,
 * mixWhite, drawStyledBar, drawCrown, money, CFG). Labels go to window.__LABELS as in the race (text / tabText).
 *
 *   window.RTT103_STEPS[name](race, opts)
 *     plans_A, plans_B            "2026 plans" step (DEC-338): range bars | plan beside the last 12 months' actual
 *     look_A (opts.year), look_B  look-ahead (DEC-326, DEC-327): estimate board for one year | combined line with bands
 *     peaks_A, peaks_B            forecasters disagree (DEC-328, owner decision DEC-344): three cards | one timeline
 *     icap_line, icap_bracket     iCapital's estimate (DEC-323) over the final race board (drawn first by render_stills)
 *     icap_card                   iCapital's estimate as a card on the 2026 plans step
 *     final_A, final_B            the final table (10 s hold, house style): June 2026 actuals | the 2030 look-ahead board
 */
(function () {
  const S = {};
  const W = 1920, H = 1080, TEAL = '#2FD0C8', GOLD = '#F5C542';
  const num = s => parseFloat(s);
  const tw = (kind, id, str, x, y, align) => { text(kind, id, str, x, y, align); const w = ctx.measureText(str).width; ctx.textAlign = 'left'; return w; };
  /* Display rounding only (figures as printed in the data, one decimal):
     mode 'plan'   company plans as the companies give them: "$195–205bn", "$37.8bn" (".0" dropped)
     mode 'actual' as the race: "$17.0bn"
     mode 'est'    Race Through Time estimates, with "~": whole billions from $10bn, one decimal below, "~$1.47–1.52tn"
                   from $1,000bn (half up from the printed figure) */
  function bn(lo, hi, mode) {
    const big = Math.max(lo, hi) >= 1000;
    const f = v => { const t = Math.round(v * 10);
      if (big) return (Math.floor((t + 50) / 100) / 100).toFixed(2);
      if (mode === 'est') return v >= 10 ? String(Math.floor((t + 5) / 10)) : (t / 10).toFixed(1);
      if (mode === 'actual') return (t / 10).toFixed(1);
      return t % 10 ? (t / 10).toFixed(1) : String(t / 10); };
    const a = f(lo), b = f(hi);
    return (mode === 'est' ? '~' : '') + '$' + (a === b ? a : a + '–' + b) + (big ? 'tn' : 'bn');
  }
  function ground() { baseTransform(); window.__LABELS = []; ctx.globalAlpha = 1; ctx.fillStyle = T.ground; ctx.fillRect(0, 0, W, H); ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left'; }
  function logoBox() { for (const b of OVL) if (b.img) { const s = Math.min(b.w / b.img.naturalWidth, b.h / b.img.naturalHeight); ctx.drawImage(b.img, b.x + (b.w - b.img.naturalWidth * s) / 2, b.y + (b.h - b.img.naturalHeight * s) / 2, b.img.naturalWidth * s, b.img.naturalHeight * s); } }
  function pill(str, x, y, col) {
    ctx.font = '700 28px ' + FONT; const w = ctx.measureText(str).width + 32;
    ctx.fillStyle = col || TEAL; rr(x, y - 30, w, 42, 21); ctx.fill();
    ctx.fillStyle = T.ground; text('step_pill', null, str, x + 16, y, 'left'); return w;
  }
  function header(p, title, sub, col) {
    const pw = pill(p, LEFT, 52, col);
    ctx.fillStyle = T.ink; ctx.font = '700 46px ' + FONT; text('title', null, title, LEFT, 118, 'left');
    if (sub) { ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT; tabText(sub, LEFT, 162, 'left', 'subtitle', null); }
    logoBox(); return pw;
  }
  function footer(t) { ctx.fillStyle = T.foot; ctx.font = '400 26px ' + FONT; text('footer', null, t, LEFT, H - 20, 'left'); }
  /* the company's tile, as on the race board (logo, or our own neutral tile), at the race's tile proportions */
  function tile(id, x, y, w, h, alpha) {
    ctx.save(); ctx.globalAlpha = alpha == null ? 1 : alpha;
    const im = PICIMG[id], own = CFG.pictures && CFG.pictures.own && CFG.pictures.own[id];
    if (im && im.naturalWidth) {
      ctx.fillStyle = '#F4F6FA'; rr(x, y, w, h, 8); ctx.fill();
      const pad = 8, sc = Math.min((w - 2 * pad) / im.naturalWidth, (h - 2 * pad) / im.naturalHeight);
      ctx.drawImage(im, x + (w - im.naturalWidth * sc) / 2, y + (h - im.naturalHeight * sc) / 2, im.naturalWidth * sc, im.naturalHeight * sc);
    } else {
      ctx.fillStyle = ENT[id] ? darkenForWhite(ENT[id].colour) : '#5A6375'; rr(x, y, w, h, 8); ctx.fill();
      const t = own ? own.text : (ENT[id] ? ENT[id].label : id); let fs = Math.round(h * 0.62);
      ctx.font = '700 ' + fs + 'px ' + FONT; while (fs > 12 && ctx.measureText(t).width > w - 20) { fs--; ctx.font = '700 ' + fs + 'px ' + FONT; }
      ctx.fillStyle = '#F4F6FA'; ctx.textAlign = 'center'; ctx.fillText(t, x + w / 2, y + h / 2 + fs * 0.36); ctx.textAlign = 'left';
    }
    ctx.restore();
  }
  function colourOf(id) { return ENT[id] ? darkenForWhite(ENT[id].colour) : '#6E7480'; }
  /* a range bar: solid to the low end, the colour at half strength with a dashed outline from low to high, an end cap */
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
    ctx.font = '400 30px ' + FONT;
    for (let v = 0; v <= max * 1.001; v += step) { const x = x0 + w * v / max;
      ctx.fillStyle = T.axis; tabText(v ? '$' + v + 'bn' : '0', x, top - 8, 'center', 'axis', null);
      ctx.fillStyle = T.grid; ctx.fillRect(Math.round(x), top + 4, 1, bottom - top - 4); }
  }
  const look = race => race.steps.lookahead;
  const rowsFor = (race, year) => look(race).filter(r => r.frame_year === String(year) && r.row_type !== 'COMBINED');
  const combinedFor = (race, year) => look(race).find(r => r.frame_year === String(year) && r.row_type === 'COMBINED');
  const cid = r => r.company.toLowerCase();
  const TENCENT_2026 = 'aims to boost capital spending in 2026 (Reuters, 18 Mar 2026; no amount given)';

  /* ---- g. the "2026 plans" step (DEC-338, DEC-335, DEC-311, DEC-296; owner decision DEC-343 for Tencent) ---- */
  function plans(race, mode, opts) {
    ground();
    header('2026 PLANS', 'What each company plans to spend in 2026', 'Each bar shows its own period · ranges as the companies give them');
    const rs = rowsFor(race, 2026).slice().sort((a, b) => num(b.estimate_high_usd_bn) - num(a.estimate_high_usd_bn));
    const bd = race.steps.bytedance_2026, BD = { company: 'ByteDance', display_name: 'ByteDance', estimate_low_usd_bn: bd.forecast_amount_usd_bn, estimate_high_usd_bn: bd.forecast_amount_usd_bn, grey: true };
    const list = rs.slice(); list.splice(list.findIndex(r => num(r.estimate_high_usd_bn) < num(BD.estimate_low_usd_bn)), 0, BD);
    const last = race.events[race.events.length - 1].values;              // the last race figure (12 months to June 2026)
    const top = 228, bottom = 1000, rh = (bottom - top) / list.length, bh = rh * 0.42, x0 = LEFT + 214, max = 240, bw = 1010;
    axis(x0, bw, max, top, bottom, 50);
    const notes = [];
    list.forEach((r, i) => {
      const y = top + i * rh + 8, id = r.grey ? 'bytedance' : cid(r), col = r.grey ? '#5A6375' : colourOf(id);
      const lo = num(r.estimate_low_usd_bn), hi = num(r.estimate_high_usd_bn);
      if (r.grey) { ctx.save(); ctx.globalAlpha = 0.85; ctx.fillStyle = '#3A4458'; rr(LEFT, y, 196, bh + 10, 8); ctx.fill(); ctx.fillStyle = T.cap; ctx.font = '700 30px ' + FONT; ctx.textAlign = 'center'; ctx.fillText('ByteDance', LEFT + 98, y + bh * 0.5 + 15); ctx.textAlign = 'left'; ctx.restore(); }
      else tile(id, LEFT, y, 196, bh + 10);
      const by = y + 5;
      if (mode === 'B' && !r.grey && last[id] != null) {                // the last 12 months' actual, as a thin outline behind
        const wa = bw * last[id] / 1e9 / max; ctx.save(); ctx.strokeStyle = 'rgba(244,246,250,0.55)'; ctx.lineWidth = 2; ctx.setLineDash([4, 5]);
        ctx.strokeRect(x0 + 1, by - 6, wa, bh + 12); ctx.restore();
      }
      if (r.grey) { ctx.save(); ctx.globalAlpha = 0.6; ctx.fillStyle = '#5A6375'; rr(x0, by, bw * lo / max, bh, 2); ctx.fill();
        ctx.strokeStyle = '#8492A6'; ctx.setLineDash([8, 6]); ctx.lineWidth = 2; rr(x0 + 1, by + 1, bw * lo / max - 2, bh - 2, 2); ctx.stroke(); ctx.restore(); }
      else rangeBar(x0, by, bw * lo / max, bw * hi / max, bh, col, false);
      let x = x0 + bw * hi / max + 20;
      ctx.fillStyle = r.grey ? T.cap : T.ink; ctx.font = '700 34px ' + FONT;
      x += tabText((r.grey ? 'more than ' : '') + bn(lo, hi, r.label === 'actual' ? 'actual' : 'plan'), x, by + bh * 0.5 + 12, 'left', 'value', id) + 16;
      let sub = r.grey ? 'press report from unnamed sources (SCMP, 9 May 2026) · AI infrastructure' : r.period_label;
      if (!r.grey && r.label === 'Citi estimate') sub = 'Citi estimate, fiscal year to March 2027';
      if (!r.grey && r.row_type === 'BASE' && r.label === 'actual') sub = 'actual, 12 months to June 2026' + (id === 'baidu' ? ' · no outlook given' : '');
      if (id === 'tencent') { if (mode === 'A') sub += ' · ' + TENCENT_2026; else { sub += ' *'; notes.push('* Tencent ' + TENCENT_2026); } }
      if (mode === 'B' && !r.grey && last[id] != null && r.label !== 'actual') sub += ' · last 12 months ' + money(last[id]);
      ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT; tabText(sub, x0, by + bh + 36, 'left', 'period', id);
    });
    const C = combinedFor(race, 2026);
    if (mode === 'B') { ctx.save(); ctx.strokeStyle = 'rgba(244,246,250,0.55)'; ctx.lineWidth = 2; ctx.setLineDash([4, 5]); ctx.strokeRect(1380, 1010, 34, 22); ctx.restore();
      ctx.fillStyle = T.cap; ctx.font = '500 26px ' + FONT; text('legend', null, '= last 12 months (June 2026)', 1424, 1030, 'left'); }
    panel(1380, 640, 500, 190, 'Combined capital spending', bn(num(C.estimate_low_usd_bn), num(C.estimate_high_usd_bn), 'actual'), 'nine bars · ByteDance not included');
    notes.forEach((n, i) => { ctx.fillStyle = T.cap; ctx.font = '500 28px ' + FONT; text('note', null, n, 1880, 600 - i * 34, 'right'); });
    footer('Company plans: results calls and releases · Amazon, Oracle as reported by Reuters · Alibaba: Citi estimate · ByteDance: SCMP');
    window.__STEP = { name: 'plans_' + mode, rows: list.map(r => r.company) };
  }
  function panel(x, y, w, h, label, value, sub) {
    ctx.fillStyle = T.panel; rr(x, y, w, h, 12); ctx.fill();
    ctx.fillStyle = T.cap; ctx.font = '600 28px ' + FONT; text('comb_label', null, label, x + 20, y + 44, 'left');
    ctx.fillStyle = T.ink; ctx.font = '800 60px ' + FONT; tabText(value, x + 20, y + 116, 'left', 'comb_value', null);
    if (sub) { ctx.fillStyle = T.cap; ctx.font = '500 26px ' + FONT; text('comb_note', null, sub, x + 20, y + h - 20, 'left'); }
  }
  S.plans_A = (race, o) => plans(race, 'A', o);
  S.plans_B = (race, o) => plans(race, 'B', o);

  /* ---- h. look-ahead A: an estimate board for one year (dashed half-strength bars, "~", a different ground tint) ---- */
  S.look_A = (race, o) => {
    const year = String(o.year || 2028);
    ground(); ctx.fillStyle = '#101B30'; ctx.fillRect(0, 0, W, H);           // a lighter, bluer ground than the race
    ctx.save(); ctx.strokeStyle = 'rgba(47,208,200,0.10)'; ctx.lineWidth = 2;   // fine diagonal hatching over the whole frame
    for (let c = -H; c < W; c += 46) { ctx.beginPath(); ctx.moveTo(c, H); ctx.lineTo(c + H, 0); ctx.stroke(); } ctx.restore();
    header('LOOK-AHEAD · OUR ESTIMATES', 'Where the spending could go', 'Race Through Time estimates, not company forecasts · growth: FactSet consensus', '#E8B44A');
    ctx.fillStyle = T.ink; ctx.font = '800 112px ' + FONT; tabText(year, 1680, 160, 'right', 'date_year', null);
    ctx.fillStyle = '#E8B44A'; ctx.font = '700 36px ' + FONT; text('date_month', null, year === '2030' ? 'estimate · least reliable year' : 'estimate', 1680, 60, 'right');
    const rs = rowsFor(race, year).slice().sort((a, b) => num(b.estimate_high_usd_bn) - num(a.estimate_high_usd_bn));
    const top = 232, bottom = 1000, rh = (bottom - top) / rs.length, bh = rh * 0.62, x0 = LEFT + 214, max = 400, bw = 1000;
    axis(x0, bw, max, top, bottom, 100);
    rs.forEach((r, i) => {
      const id = cid(r), y = top + i * rh + (rh - bh) / 2, lo = num(r.estimate_low_usd_bn), hi = num(r.estimate_high_usd_bn);
      tile(id, LEFT, y - 2, 196, bh + 4, 0.9);
      rangeBar(x0, y, bw * lo / max, bw * hi / max, bh, colourOf(id), true);
      ctx.font = '600 34px ' + FONT; const nm = ENT[id].label, inside = ctx.measureText(nm).width + 40 < bw * lo / max;
      let x = x0 + bw * hi / max + 18;
      if (inside) { ctx.fillStyle = '#F4F6FA'; tw('name', id, nm, x0 + 18, y + bh / 2 + 12, 'left'); }
      else { ctx.fillStyle = T.ink; x += tw('name', id, nm, x, y + bh / 2 + 12, 'left') + 16; }
      ctx.fillStyle = T.ink; ctx.font = '700 34px ' + FONT; x += tabText(bn(lo, hi, r.row_type !== 'CITI_ESTIMATE' ? 'est' : 'actual'), x, y + bh / 2 + 12, 'left', 'value', id) + 14;
      ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT;
      const tag = r.row_type === 'CITI_ESTIMATE' ? '· Citi estimate, fiscal year to March ' + (+year + 1) : /Oracle/.test(r.company) && /Probably high/.test(r.notes) ? '· probably high' : '';
      if (tag) tabText(tag, x, y + bh / 2 + 12, 'left', 'tag', id);
    });
    const C = combinedFor(race, year);
    panel(1380, 700, 500, 190, 'Combined capital spending', bn(num(C.estimate_low_usd_bn), num(C.estimate_high_usd_bn), 'est'), 'sum of the nine bars · ' + year);
    footer('Growth: FactSet consensus (via Morgan Stanley, 31 Aug 2026) · Alibaba: Citi to March 2029 · Race Through Time estimates, not official');
    window.__STEP = { name: 'look_A', year, rows: rs.map(r => r.company) };
  };

  /* ---- h. look-ahead B: the combined total as a line, history solid, our estimates as a widening band ---- */
  S.look_B = (race, o) => {
    ground();
    header('LOOK-AHEAD · OUR ESTIMATES', 'Combined capital spending, 2010–2030', 'Each point is a 12-month total at the middle of its period · band: 2026 plans, then our estimates', '#E8B44A');
    const x0 = 210, x1 = 1830, y0 = 250, y1 = 960, t0 = 2010, t1 = 2031, max = 1600;
    const X = t => x0 + (x1 - x0) * (t - t0) / (t1 - t0), Y = v => y1 - (y1 - y0) * v / max;
    const mid = d => +d.slice(0, 4) + (+d.slice(5, 7)) / 12 - 0.5;           // the middle of the 12 months to date d
    ctx.fillStyle = 'rgba(232,180,74,0.07)'; ctx.fillRect(X(2027), y0 - 10, X(2031) - X(2027), y1 - y0 + 10);
    ctx.fillStyle = 'rgba(232,180,74,0.09)'; ctx.fillRect(X(2030), y0 - 10, X(2031) - X(2030), y1 - y0 + 10);
    ctx.font = '400 30px ' + FONT;
    for (let v = 0; v <= max; v += 400) { ctx.fillStyle = T.axis; tabText(v ? (v >= 1000 ? '$' + (v / 1000) + 'tn' : '$' + v + 'bn') : '0', x0 - 16, Y(v) + 10, 'right', 'axis', null); ctx.fillStyle = T.grid; ctx.fillRect(x0, Math.round(Y(v)), x1 - x0, 1); }
    for (let t = 2010; t <= 2030; t += 5) { ctx.fillStyle = T.axis; tabText(String(t), X(t + 0.5), y1 + 44, 'center', 'axis', null); }
    ctx.strokeStyle = TEAL; ctx.lineWidth = 5; ctx.lineJoin = 'round'; ctx.beginPath();
    race.events.forEach((e, i) => { const x = X(mid(e.date)), y = Y(e.combined / 1e9); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke();
    const yrs = [2026, 2027, 2028, 2029, 2030].map(y => ({ y, t: y + 0.5, lo: num(combinedFor(race, y).estimate_low_usd_bn), hi: num(combinedFor(race, y).estimate_high_usd_bn) }));
    const lastE = race.events[race.events.length - 1], lx = X(mid(lastE.date)), ly = Y(lastE.combined / 1e9);
    ctx.fillStyle = 'rgba(232,180,74,0.55)'; ctx.beginPath(); ctx.moveTo(lx, ly);
    yrs.forEach(p => ctx.lineTo(X(p.t), Y(p.hi))); yrs.slice().reverse().forEach(p => ctx.lineTo(X(p.t), Y(p.lo))); ctx.closePath(); ctx.fill();
    yrs.forEach(p => { ctx.fillStyle = '#E8B44A'; ctx.beginPath(); ctx.arc(X(p.t), Y((p.lo + p.hi) / 2), 5, 0, Math.PI * 2); ctx.fill(); });
    ctx.fillStyle = T.ink; ctx.font = '700 32px ' + FONT;
    tabText(money(lastE.combined), lx + 10, ly + 46, 'left', 'value', null);
    ctx.fillStyle = T.cap; ctx.font = '500 28px ' + FONT; text('value_sub', null, '12 months to June 2026', lx + 10, ly + 82, 'left');
    const p26 = yrs[0], p30 = yrs[4];
    ctx.fillStyle = T.ink; ctx.font = '700 32px ' + FONT; tabText(bn(p26.lo, p26.hi, 'actual'), X(p26.t) - 24, Y(p26.hi) - 20, 'right', 'value', null);
    ctx.fillStyle = T.cap; ctx.font = '500 28px ' + FONT; text('value_sub', null, '2026 plans', X(p26.t) - 24, Y(p26.hi) - 58, 'right');
    ctx.fillStyle = T.ink; ctx.font = '700 32px ' + FONT; tabText(bn(p30.lo, p30.hi, 'est'), X(p30.t) - 18, Y(p30.hi) - 22, 'right', 'value', null);
    ctx.fillStyle = '#E8B44A'; ctx.font = '600 28px ' + FONT; tw('band', null, '2030: least reliable year', X(2031), y0 - 22, 'right');
    tw('band', null, 'our estimates', X(2027) + 12, y1 - 24, 'left');
    footer('Actual: company filings · 2026: company plans (Amazon, Oracle as reported by Reuters; Alibaba: Citi) · 2027–2030: Race Through Time estimates');
    window.__STEP = { name: 'look_B' };
  };

  /* ---- i. forecasters disagree on the peak (DEC-328; Allianz labelled "AI capex (Allianz)", owner decision DEC-344) ---- */
  function peakData(race) {
    const P = race.steps.peaks, f = s => P.find(p => p.forecaster.startsWith(s));
    return { bcg: f('BCG'), fs: f('FactSet'), al: P.find(p => p.forecaster === 'Allianz Research (28 Sep 2026)'), bars: race.steps.bcg_group };
  }
  S.peaks_A = race => {
    ground(); const D = peakData(race);
    header('WHEN DOES IT PEAK?', 'Forecasters disagree on when the spending peaks', 'Three views, three different measures · none is added to the race');
    const cards = [
      { who: 'BCG', when: '12 Jun 2026', what: "Microsoft, Alphabet, Amazon, Meta and Oracle together (BCG's chart)", peak: 'Peak: 2029', body: 'Highest in 2029, then a little lower in 2030', chart: true, col: '#7FA7FF' },
      { who: 'FactSet consensus', when: '31 Aug 2026', what: 'Company by company (Amazon, Microsoft, Alphabet, Meta, Oracle)', peak: 'No peak by 2030', body: 'Amazon, Microsoft, Alphabet and Meta still rising in 2030; Oracle highest in 2027', col: TEAL },
      { who: 'AI capex (Allianz)', when: '28 Sep 2026', what: 'AI spending only (companies not listed) · not added to Combined capital spending', peak: 'Peak: 2028', body: '“…peak at USD1trn in 2028”', col: '#E8B44A' } ];
    const cw = 572, gap = 24, y = 220, h = 760;
    cards.forEach((c, i) => {
      const x = LEFT + i * (cw + gap);
      ctx.fillStyle = T.panel; rr(x, y, cw, h, 14); ctx.fill(); ctx.fillStyle = c.col; rr(x, y, cw, 10, 5); ctx.fill();
      ctx.fillStyle = T.ink; ctx.font = '800 44px ' + FONT; text('card_who', null, c.who, x + 28, y + 76, 'left');
      ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT; text('card_when', null, c.when, x + 28, y + 118, 'left');
      ctx.font = '500 30px ' + FONT; let yy = y + 170; for (const l of wrapLines(c.what, cw - 56)) { text('card_what', null, l, x + 28, yy, 'left'); yy += 38; }
      ctx.fillStyle = c.col; ctx.font = '800 54px ' + FONT; text('card_peak', null, c.peak, x + 28, yy + 50, 'left'); yy += 100;
      ctx.fillStyle = T.ink; ctx.font = '500 32px ' + FONT; for (const l of wrapLines(c.body, cw - 56)) { text('card_body', null, l, x + 28, yy, 'left'); yy += 42; }
      if (c.chart) {                                                      // BCG's group bars 2026-2030 as read from its chart
        const bx = x + 40, bw = cw - 80, base = y + h - 70, mh = 200, n = D.bars.length, mx = 1000;
        D.bars.forEach((b, j) => { const v = num(b.value_usd_bn), bh = mh * v / mx, w = bw / n - 18, xx = bx + j * bw / n;
          ctx.fillStyle = b.year === '2029' ? c.col : mixGround(c.col, 0.55); rr(xx, base - bh, w, bh, 3); ctx.fill();
          ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT; tabText(b.year, xx + w / 2, base + 38, 'center', 'axis', null); });
      }
    });
    footer('BCG (12 Jun 2026, chart read by eye) · FactSet consensus via Morgan Stanley (31 Aug 2026) · Allianz Research (28 Sep 2026)');
    window.__STEP = { name: 'peaks_A' };
  };
  S.peaks_B = race => {
    ground(); const D = peakData(race);
    header('WHEN DOES IT PEAK?', 'Forecasters disagree on when the spending peaks', 'Each row is a different forecaster and a different measure · none is added to the race');
    const x0 = 640, x1 = 1820, t0 = 2026, t1 = 2031, X = t => x0 + (x1 - x0) * (t - t0) / (t1 - t0), y0 = 300;
    for (let t = 2026; t <= 2030; t++) { ctx.fillStyle = T.axis; ctx.font = '600 34px ' + FONT; tabText(String(t), X(t + 0.5), y0 - 30, 'center', 'axis', null); ctx.fillStyle = T.grid; ctx.fillRect(Math.round(X(t)), y0, 1, 640); }
    ctx.fillStyle = T.grid; ctx.fillRect(Math.round(X(2031)), y0, 1, 640);
    const rows = [
      { who: 'BCG', sub: 'US big five together', peak: 2029, col: '#7FA7FF', txt: 'peak' },
      { who: 'AI capex (Allianz)', sub: 'AI spending only', peak: 2028, col: '#E8B44A', txt: 'peak · about $1trn (AI only)' },
      { who: 'FactSet consensus', sub: 'company by company', peak: null, col: TEAL, txt: '4 of 5 still rising in 2030 (Oracle: 2027)' } ];
    rows.forEach((r, i) => {
      const y = y0 + 110 + i * 200;
      ctx.fillStyle = T.ink; ctx.font = '800 40px ' + FONT; text('row_who', null, r.who, LEFT, y, 'left');
      ctx.fillStyle = T.cap; ctx.font = '500 30px ' + FONT; text('row_sub', null, r.sub, LEFT, y + 42, 'left');
      ctx.strokeStyle = mixGround(r.col, 0.4); ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(X(2026.1), y - 10);
      if (r.peak) { ctx.lineTo(X(r.peak + 0.5), y - 10); ctx.stroke(); ctx.fillStyle = r.col; ctx.beginPath(); ctx.arc(X(r.peak + 0.5), y - 10, 20, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = T.ink; ctx.font = '700 34px ' + FONT; text('row_peak', null, r.txt, X(r.peak + 0.5) + 32, y + 2, 'left'); }
      else { ctx.lineTo(X(2031) - 10, y - 10); ctx.stroke(); ctx.fillStyle = r.col; ctx.beginPath(); ctx.moveTo(X(2031) + 14, y - 10); ctx.lineTo(X(2031) - 18, y - 32); ctx.lineTo(X(2031) - 18, y + 12); ctx.closePath(); ctx.fill();
        ctx.fillStyle = T.ink; ctx.font = '700 34px ' + FONT; text('row_peak', null, r.txt, X(2028.6), y - 34, 'center'); }
    });
    footer('BCG (12 Jun 2026, chart read by eye) · FactSet consensus via Morgan Stanley (31 Aug 2026) · Allianz Research (28 Sep 2026)');
    window.__STEP = { name: 'peaks_B' };
  };

  /* ---- j. iCapital's estimate, once near the end (DEC-323), labelled as an estimate ---- */
  const ICAP_Q = '“an estimated 70–75% of that spend now tied directly to AI infrastructure”';
  const ICAP_WHO = 'iCapital estimate, 30 Apr 2026 · Amazon, Microsoft, Alphabet and Meta';
  S.icap_line = () => {                                    // over the final race board: one line under the title
    ctx.fillStyle = T.ground; ctx.fillRect(LEFT - 4, 92, 1300, 42);
    ctx.fillStyle = '#E8B44A'; ctx.font = '700 28px ' + FONT; const w = tw('icap', null, 'iCapital estimate: ', LEFT, 124, 'left');
    ctx.fillStyle = T.ink; ctx.font = '500 28px ' + FONT; tw('icap', null, '70–75% of the big four’s spending “now tied directly to AI infrastructure”', LEFT + w, 124, 'left');
    window.__STEP = { name: 'icap_line' };
  };
  S.icap_bracket = () => {                                 // over the final race board: a bracket beside the four US bars
    const B = (window.__BARS || []).filter(b => ['amazon', 'alphabet', 'microsoft', 'meta'].includes(b.id));
    const ya = Math.min(...B.map(b => b.rect.y)), yb = Math.max(...B.map(b => b.rect.y + b.rect.h)), x = 1660;
    ctx.strokeStyle = '#E8B44A'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x - 18, ya); ctx.lineTo(x, ya); ctx.lineTo(x, yb); ctx.lineTo(x - 18, yb); ctx.stroke();
    ctx.fillStyle = '#E8B44A'; ctx.font = '800 54px ' + FONT; text('icap', null, '70–75%', x + 22, (ya + yb) / 2 - 20, 'left');
    ctx.font = '600 30px ' + FONT; text('icap', null, 'for AI', x + 22, (ya + yb) / 2 + 20, 'left');
    ctx.fillStyle = T.cap; ctx.font = '500 26px ' + FONT; text('icap', null, 'iCapital', x + 22, (ya + yb) / 2 + 58, 'left'); text('icap', null, 'estimate', x + 22, (ya + yb) / 2 + 90, 'left');
    window.__STEP = { name: 'icap_bracket', span: [ya, yb] };
  };
  S.icap_card = race => {                                  // a card on the 2026 plans step
    plans(race, 'A');
    const x = 1380, y = 262, w = 500, h = 330;
    ctx.fillStyle = T.panel; rr(x, y, w, h, 12); ctx.fill(); ctx.fillStyle = '#E8B44A'; rr(x, y, 6, h, 3); ctx.fill();
    ctx.fillStyle = '#E8B44A'; ctx.font = '700 26px ' + FONT; text('icap', null, 'ESTIMATE · ICAPITAL, 30 APR 2026', x + 26, y + 46, 'left');
    ctx.fillStyle = T.ink; ctx.font = '500 30px ' + FONT; let yy = y + 92;
    for (const l of wrapLines(ICAP_Q, w - 52)) { text('icap', null, l, x + 26, yy, 'left'); yy += 40; }
    ctx.fillStyle = T.cap; ctx.font = '500 26px ' + FONT; for (const l of wrapLines('about Amazon, Microsoft, Alphabet and Meta; never applied to the bars', w - 52)) { yy += 6; text('icap', null, l, x + 26, yy + 30, 'left'); yy += 30; }
    window.__STEP = { name: 'icap_card' };
  };

  /* ---- l. the final table (10 s hold): B = the 2030 look-ahead board instead of the actuals ---- */
  S.final_A = race => {                                    // over the final race board: the one-line summary and notes
    ctx.fillStyle = T.ground; ctx.fillRect(LEFT - 4, 92, 1300, 46);
    const e = race.events[race.events.length - 1], y4 = race.events[race.events.length - 5];
    ctx.fillStyle = T.ink; ctx.font = '600 30px ' + FONT;
    tabText('Combined: ' + money(e.combined) + ' in the 12 months to June 2026, up from ' + money(y4.combined) + ' a year earlier', LEFT, 124, 'left', 'final_line', null);
    window.__STEP = { name: 'final_A' };
  };
  S.final_B = (race) => S.look_A(race, { year: 2030 });
  window.RTT103_STEPS = S;
})();
