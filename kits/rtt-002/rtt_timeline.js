/* Race Through Time - the event timeline (IQ-04).
 *
 * One file, loaded by BOTH the Node driver (rtt.js, for FRAME_COUNT_ONLY and the frame plan)
 * and the player page (player_rtt.html), so the two can never disagree about when an event
 * lands. Nothing here draws.
 *
 * Input: the adapter's "rtt-race/1" file and the kit config. Output:
 *   states[k]    the board AFTER event k: every entrant with a count, ranked
 *   opening      the board before the first displayed event (events before the window)
 *   startFrame[k] the race frame at which event k's numbers appear (whole frames, so a test
 *                can land on the exact first frame of every event)
 *   raceFrames   the race length in frames; RACE_SEC = raceFrames / fps
 *
 * Rules, all from the brief (prompts/CODE_SESSION_IQ-04.md step 3):
 *   - a count changes only AT its event; there are no in-between values
 *   - ties: equal counts -> whoever reached that count first ranks higher, judged by the
 *     credit order (credit_index) in the data. There is no official rule (DEC-012).
 *   - pacing: each event lasts sec_per_event x a multiplier that must lie inside
 *     pacing.bounds (0.8-1.4 by the blueprint); quiet stretches take the low end.
 *
 * IQ-05 (DEC-022, DEC-023): colours. Every driver gets ONE palette colour for the whole
 * dataset, and no two drivers who can be on screen together get the same or a confusingly
 * similar colour. assignColours() below works on the WHOLE race file, never on the window, so
 * a passage and the full video give every driver the same colour.
 *
 * IQ-05 round 2 (DEC-027 to DEC-033): record events (BECOMES_JOINT / BECOMES_SOLE / EXTENDS_SOLE,
 * as in data/rtt-002/record_progression.csv) and optional holds on them (record_hold); pacing
 * judged on pacing.judge_rows; an exact final-board length (pacing.final_board_sec); and the
 * winner-highlight plan (who is lit on each race, and whether they stay lit into the next).
 * Without those keys every number is as before (config.json: 16,062 frames).
 *
 * IQ-05 round 5 (DEC-053): race starts. When the race file carries events[].starts (adapter 1.1,
 * from data/rtt-002/starts.csv), every state also holds starts[id], the driver's career starts
 * after that race, for every driver with a count. Like the wins, starts change only AT a race;
 * they never change the order, the pacing or the colours. rateText() is the win rate shown on
 * screen: wins / starts as a percentage with one decimal, rounded half up, in integer arithmetic.
 */
(function (root) {
  'use strict';

  function rankOf(totals, reached) {
    const ids = Object.keys(totals).filter(id => totals[id] > 0);
    ids.sort((a, b) => (totals[b] - totals[a]) || (reached[a] - reached[b]));
    return ids;
  }

  function snapshot(totals, reached, starts) {
    const order = rankOf(totals, reached);
    const tot = {};
    for (const id of order) tot[id] = totals[id];
    const snap = { order, totals: tot };
    if (starts) { snap.starts = {}; for (const id of order) snap.starts[id] = starts[id] || 0; }
    return snap;
  }

  /* IQ-05e (DEC-053): win rate = wins / starts, percent, one decimal, rounded half up. In tenths
     of a percent that is floor((1000 w / s) + 1/2) = floor((2000 w + s) / (2 s)), done on
     integers so no binary rounding can creep in: 1/8 -> "12.5", 1/16 -> "6.3", 91/306 -> "29.7". */
  function rateText(w, s) {
    if (!(Number.isInteger(w) && Number.isInteger(s) && s > 0 && w >= 0 && w <= s)) throw new Error('win rate of ' + w + ' wins from ' + s + ' starts');
    const a = 2000 * w + s, b = 2 * s, t = (a - a % b) / b;
    return Math.floor(t / 10) + '.' + (t % 10);
  }

  function sameList(a, b) {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
    return true;
  }

  function checkPacing(p) {
    const lo = p.bounds[0], hi = p.bounds[1];
    if (!(lo >= 0.8 - 1e-9 && hi <= 1.4 + 1e-9 && lo <= hi))
      throw new Error('pacing.bounds must lie within 0.8-1.4 (blueprint); got ' + p.bounds);
    for (const k of ['rank_change', 'visible_change', 'quiet']) {
      const m = p.mult[k];
      if (!(m >= lo - 1e-9 && m <= hi + 1e-9))
        throw new Error('pacing.mult.' + k + ' = ' + m + ' is outside pacing.bounds ' + p.bounds);
    }
  }

  function build(race, cfg) {
    if (race.schema === 'rtt-series/1') return buildSeries(race, cfg);     // IQ-10 (RTT-003); RTT-002 never gets here
    if (race.schema !== 'rtt-race/1') throw new Error('race file schema is ' + race.schema + ', expected rtt-race/1');
    const fps = cfg.fps, rows = cfg.rows, P = cfg.pacing;
    checkPacing(P);
    const from = (cfg.window && cfg.window.from) || '0000-00-00';
    const to   = (cfg.window && cfg.window.to)   || '9999-99-99';

    const totals = {}, reached = {};
    /* IQ-05e: starts ride along when the race file has them (all events or none) */
    const HAS_STARTS = race.events.length > 0 && race.events.every(ev => Array.isArray(ev.starts));
    if (!HAS_STARTS && race.events.some(ev => Array.isArray(ev.starts))) throw new Error('some events carry starts and some do not');
    const starts = HAS_STARTS ? {} : null;
    let opening = snapshot(totals, reached, starts), openingEvent = null;
    const events = [], states = [], recordOf = [];
    let record = 0, holders = new Set();
    for (const ev of race.events) {
      if (ev.date > to) break;
      /* IQ-05b: the all-time record, credit by credit, with the same three outcomes as
         data/rtt-002/record_progression.csv (scripts/build_rtt002_dataset.py): passing the record
         is BECOMES_SOLE (EXTENDS_SOLE if the driver already held it alone), reaching it is
         BECOMES_JOINT. The player tests check this against the CSV on every race. */
      const rec = [];
      for (const c of ev.credits) {
        const now = (totals[c.id] || 0) + 1;
        if (now !== c.total) throw new Error('event ' + ev.race_index + ': ' + c.id + ' total ' + c.total + ' but counted ' + now);
        totals[c.id] = now;
        reached[c.id] = c.credit_index;          // when this driver reached this total
        if (now > record) { rec.push({ id: c.id, total: now, type: holders.size === 1 && holders.has(c.id) ? 'EXTENDS_SOLE' : 'BECOMES_SOLE' }); record = now; holders = new Set([c.id]); }
        else if (now === record) { holders.add(c.id); rec.push({ id: c.id, total: now, type: 'BECOMES_JOINT' }); }
      }
      if (HAS_STARTS) for (const st of ev.starts) {
        const n = (starts[st.id] || 0) + 1;
        if (n !== st.total) throw new Error('event ' + ev.race_index + ': ' + st.id + ' starts ' + st.total + ' but counted ' + n);
        starts[st.id] = n;
      }
      if (HAS_STARTS) for (const c of ev.credits) if (!ev.starts.some(st => st.id === c.id)) throw new Error('event ' + ev.race_index + ': winner ' + c.id + ' has no start');
      const s = snapshot(totals, reached, starts);
      if (ev.date < from) { opening = s; openingEvent = ev; continue; }
      events.push(ev); states.push(s); recordOf.push(rec);
    }
    if (!events.length) throw new Error('no events inside the window ' + from + ' .. ' + to);

    /* Pacing. An event that reorders or changes who is on the visible board gets the long
       beat; one that only moves a visible bar gets the normal beat; one nobody can see, or
       the (settled_run_after+1)th visible-but-unchanged event in a row, gets the short beat.
       That is what "quiet stretches compress" means here.
       IQ-05b: pacing.judge_rows (default: rows) is the board the beat is judged on. The two
       round-2 pilots both judge on the top ten, so the top-20 board and the top-ten board run on
       identical timestamps and can be compared frame for frame (blueprint section 9). */
    const JR = P.judge_rows || rows;
    const mult = [], kind = [];
    let prev = opening, settled = 0;
    for (let k = 0; k < events.length; k++) {
      const a = prev.order.slice(0, JR), b = states[k].order.slice(0, JR);
      const credited = events[k].credits.map(c => c.id);
      let kd;
      if (!sameList(a, b)) { kd = 'rank_change'; settled = 0; }
      else if (credited.some(id => b.includes(id))) { settled++; kd = settled > P.settled_run_after ? 'quiet' : 'visible_change'; }
      else { settled++; kd = 'quiet'; }
      kind.push(kd); mult.push(P.mult[kd]);
      prev = states[k];
    }

    /* IQ-05b record moments (a switchable test, record_hold.enabled): a race on which a driver
       reaches (BECOMES_JOINT) or takes (BECOMES_SOLE) the all-time record is held for
       record_hold.sec instead of its normal beat, so the rank glide settles before the next
       race lands. EXTENDS_SOLE is not held. Every other beat keeps the 0.8-1.4x bounds. */
    const RH = cfg.record_hold || {};
    const holdTypes = RH.types || ['BECOMES_JOINT', 'BECOMES_SOLE'];
    const hold = events.map((ev, k) => !!RH.enabled && recordOf[k].some(r => holdTypes.includes(r.type)));
    const records = [];
    events.forEach((ev, k) => recordOf[k].forEach(r => records.push(Object.assign({ k, race_index: ev.race_index, date: ev.date, season: ev.season, grand_prix: ev.grand_prix, held: hold[k] }, r))));

    const startFrame = [];
    let sec = P.lead_in_sec;
    for (let k = 0; k < events.length; k++) {
      startFrame.push(Math.round(sec * fps));
      if (k < events.length - 1) sec += hold[k] ? RH.sec : P.sec_per_event * mult[k];
    }
    /* The final board: pacing.final_board_sec (IQ-05b) puts it on screen for exactly that long
       from the first frame of the last race. Without it, the last race keeps its beat and
       end_hold_sec is added (IQ-04/IQ-05 behaviour, unchanged for config.json). */
    const lastK = events.length - 1;
    const raceFrames = P.final_board_sec != null
      ? startFrame[lastK] + Math.round(P.final_board_sec * fps)
      : Math.round((sec + (hold[lastK] ? RH.sec : P.sec_per_event * mult[lastK]) + P.end_hold_sec) * fps);
    for (let k = 1; k < startFrame.length; k++)
      if (startFrame[k] <= startFrame[k - 1]) throw new Error('two events share a frame; raise sec_per_event');

    /* IQ-05b winner highlight plan: on each race, the credited winners whose bars are on the
       board (top `rows` after the race). streak = the same driver also wins the next race on
       the board, so the player keeps the highlight lit through the streak instead of fading and
       re-lighting it (no flicker). */
    const winners = events.map((ev, k) => ev.credits.map(c => c.id).filter(id => states[k].order.slice(0, rows).includes(id)));
    const highlight = winners.map((ids, k) => ids.map(id => ({ id, streak: k + 1 < winners.length && winners[k + 1].includes(id) })));

    /* The colour rule assumes a driver who drops off the board has faded within
       colour_rule.fade_races races. A row leaving the last slot fades out in about
       ln(4) x glide.rank_sec (23 frames at 0.55 s); refuse a pace so fast that fade_races of the
       shortest race slot cannot cover it (the player tests check every frame as well). */
    const colours = assignColours(race, cfg);
    let minSlot = Infinity;
    for (let k = 1; k < startFrame.length; k++) minSlot = Math.min(minSlot, startFrame[k] - startFrame[k - 1]);
    const fadeFrames = Math.ceil(Math.log(4) * cfg.glide.rank_sec * fps);
    if (startFrame.length > 1 && colours.fadeRaces * minSlot < fadeFrames)
      throw new Error('pace too fast for the colour rule: ' + colours.fadeRaces + ' races x ' + minSlot + ' frames < ' + fadeFrames + '-frame fade');

    return { events, states, opening, openingEvent, startFrame, raceFrames, mult, kind, fps, rows, colours, hold, records, highlight, hasStarts: HAS_STARTS };
  }

  /* ---- IQ-10 (RTT-003): a quarter-end series ("rtt-series/1", scripts/rtt003_adapter.py) ----
   * Same output shape as build(), so the player and the driver use one path. Differences:
   *   - an event is a quarter end; a state holds every console on sale with its units (an integer
   *     straight from data/rtt-003/series.csv), its display style and its "+" flag, and the maker
   *     totals. Values change only AT a quarter end; nothing in between is computed here.
   *   - rank: most units first; equal units -> the console that reached that value first, then the
   *     earlier launch (reference/metric_contract_RTT-003.md, Rank).
   *   - opening: the last quarter end before window.from; if there is none (the race starts with the
   *     data), the FIRST quarter end is the opening board, shown at full length from frame 0.
   *   - pacing: RTT-002's rule (sec_per_event x 1.4 / 1.0 / 0.8, judged on judge_rows; a console
   *     "moved" when its units changed), with optional pacing.segments [{to, sec_per_event}]: a
   *     quarter end on or before `to` uses that base instead (DEC-097: quickly through 1985-88).
   *   - holds: record_hold with type "CROWN" holds every change of first place (the race-start row
   *     of the crown list is not a change) for record_hold.sec.
   *   - colours: one per MAKER (cfg.maker_order -> cfg.palette), not per console; no colour rule.
   *   - fade: the window event from which each retired console fades (first quarter end on or after
   *     its fade_date); -1 = already faded on the opening board; null = not inside the window.
   */
  /* ---- IQ-13 (RTT-001): a monthly SHARE series (race.kind "share", scripts/rtt001_adapter.py) ----
   * Values are whole HUNDREDTHS of a percent, copied from data/rtt-001/series.csv. Nothing here changes the data
   * (DEC-167): shareRace() returns a copy of the race whose month-end values are what the player DRAWS under
   * cfg.smoothing, plus the hand-over windows it used, the source line of each month and the changes of first place
   * of the drawn values. With smoothing off (or mode "none") every value is series.csv exactly.
   *
   * smoothing {mode: "none" | "eased", handover_months: 12, include_flagged: false}:
   *   - within one source, the line through that source's published figures (race.knots) is a monotone cubic
   *     (Fritsch-Carlson) instead of straight lines: it passes through every published figure, never goes beyond the
   *     two figures either side of it, and comes to rest (zero slope) at a source's first and last figure;
   *   - at each hand-over, for a browser reported on both sides, the bar blends gradually from the outgoing source's
   *     line O to the incoming source's line I over a window of handover_months months centred on the hand-over (the
   *     whole gap when the gap is longer), never reaching into StatCounter's months (from race.sc_start; that window
   *     ends on StatCounter's first month instead): (1 - w) O(t) + w I(t), with O held at its last figure after it
   *     and I at its first figure before it, and w an eased 0..1 ramp (smoothstep) over the window. A blend of two
   *     published lines never goes outside the figures the two sources gave in that stretch;
   *   - hand-overs flagged in the order check (DEC-168) are left as built unless include_flagged is true;
   *   - from race.sc_start (StatCounter) and outside every window nothing is smoothed: values are series.csv exactly
   *     at every month end that is a published figure, and on every StatCounter month;
   *   - a bar is drawn in exactly the months series.csv has a value for it (never added, never removed).
   * Rank: share, then the previous month's order, then the browser's name (reference/metric_contract_RTT-001.md). */
  const dayNum = iso => Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10)) / 864e5;
  function pchip(xs, ys) {
    const n = xs.length;
    if (n === 1) return () => ys[0];
    const h = [], d = [], m = new Array(n).fill(0);
    for (let i = 0; i < n - 1; i++) { h.push(xs[i + 1] - xs[i]); d.push((ys[i + 1] - ys[i]) / h[i]); }
    for (let i = 1; i < n - 1; i++) if (d[i - 1] * d[i] > 0) { const w1 = 2 * h[i] + h[i - 1], w2 = h[i] + 2 * h[i - 1]; m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i]); }
    return x => {
      if (x <= xs[0]) return ys[0];
      if (x >= xs[n - 1]) return ys[n - 1];
      let i = 0; while (x > xs[i + 1]) i++;
      const t = (x - xs[i]) / h[i], t2 = t * t, t3 = t2 * t;
      return (2 * t3 - 3 * t2 + 1) * ys[i] + (t3 - 2 * t2 + t) * h[i] * m[i] + (-2 * t3 + 3 * t2) * ys[i + 1] + (t3 - t2) * h[i] * m[i + 1];
    };
  }
  function linear(xs, ys) {
    return x => { if (x <= xs[0]) return ys[0]; if (x >= xs[xs.length - 1]) return ys[ys.length - 1];
      let i = 0; while (x > xs[i + 1]) i++; return ys[i] + (ys[i + 1] - ys[i]) * (x - xs[i]) / (xs[i + 1] - xs[i]); };
  }
  const smoothstep = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u);
  function shareOrder(values, prevOrder, label) {
    const pos = {}; prevOrder.forEach((id, i) => { pos[id] = i; });
    return Object.keys(values).sort((a, b) => (values[b] - values[a]) || ((a in pos ? pos[a] : 1e9) - (b in pos ? pos[b] : 1e9)) || (label[a] < label[b] ? -1 : label[a] > label[b] ? 1 : 0));
  }
  /* IQ-19 (RTT-102): a monthly VISITS series (race.kind "visits", scripts/rtt102_adapter.py). Values are whole visits
     from data/rtt-102/series_monthly.csv (a published month the figure used, a month between two published months the
     build's straight line); nothing here changes the data. Options, all at draw time:
       cfg.clock "month" (default) | "quarter": the clock ticks every month, or only at quarter ends (March, June,
         September, December) plus the race's last month; a quarterly clock counts on a straight line from one quarter
         end to the next, so a month between them (e.g. DeepSeek's February 2025 peak) is never shown;
       cfg.smoothing.mode "none" (straight lines, as built: DEC-501 (4)) | "eased": each bar moves on a monotone cubic
         (Fritsch-Carlson, pchip) through its published figures that the clock shows, by month index - it passes through
         every one of them exactly, never goes beyond the two figures either side of it (no overshoot) and comes to rest
         at a bar's first and last figure (RTT-001's draw-time smoothing, DEC-184); evaluated frame by frame (shareFrame);
       cfg.status.sink (default true with cfg.status): a bar after its last published month (held at that figure,
         status "latest_figure") ranks below every bar with a figure for the month - a held figure is never compared
         with a later month's.
     Rank otherwise: visits, then the previous month's order, then the name (the metric contract). */
  function visitsRace(race, cfg) {
    const Q = cfg.clock === 'quarter', last = race.events[race.events.length - 1].date;
    const evs = race.events.filter(ev => !Q || [3, 6, 9, 12].includes(+ev.date.slice(5, 7)) || ev.date === last)
      .map(ev => Object.assign({}, ev, { values: Object.assign({}, ev.values), series_values: ev.values }));
    const S = Object.assign({ mode: 'none' }, cfg.smoothing || {}), label = {};
    for (const e of race.entrants) label[e.id] = e.label;
    const idx = {}; race.events.forEach((ev, i) => { idx[ev.date] = i; });
    const ease = {};
    if (S.mode === 'eased') {
      const shown = new Set(evs.map(ev => ev.date));
      for (const [id, ks] of Object.entries(race.knots || {})) {
        const kk = ks.filter(k => shown.has(k.date));
        if (kk.length) ease[id] = pchip(kk.map(k => idx[k.date]), kk.map(k => k.v));
      }
      for (const ev of evs) for (const id of Object.keys(ev.values))
        if (ev.prov[id] !== 'h' && ease[id]) ev.values[id] = Math.round(ease[id](idx[ev.date]));
    }
    const SINK = !!(cfg.status && cfg.status.enabled && cfg.status.sink !== false);
    const live = (ev, id) => !SINK || (ev.status || {})[id] !== 'latest_figure';
    let prevOrder = [];
    for (const ev of evs) {
      const o = shareOrder(ev.values, prevOrder, label);
      ev.order = o.filter(id => live(ev, id)).concat(o.filter(id => !live(ev, id)));
      prevOrder = ev.order;
    }
    return Object.assign({}, race, { events: evs, crown: [], windows: [], smoothing: S, ease, monthIndex: idx, sink: SINK });
  }

  function shareRace(race, cfg) {
    if (race.kind === 'visits') return visitsRace(race, cfg);    // IQ-19 (RTT-102)
    const S = Object.assign({ mode: 'none', handover_months: 12, include_flagged: false }, cfg.smoothing || {});
    const SC = race.sc_start ? dayNum(race.sc_start) : Infinity, label = {};   // IQ-18: a money race has no source hand-overs
    for (const e of race.entrants) label[e.id] = e.label;
    const evs = race.events.map(ev => Object.assign({}, ev, { values: Object.assign({}, ev.values), series_values: ev.values }));
    const windows = [];
    if (S.mode === 'eased') {
      /* segments: per browser and source, the function through that source's points */
      const seg = {};
      for (const [id, ks] of Object.entries(race.knots || {})) {
        for (const k of ks) { const s = (seg[id] = seg[id] || {})[k.src] = seg[id][k.src] || { xs: [], ys: [] }; s.xs.push(dayNum(k.date)); s.ys.push(k.v); }
        for (const s of Object.values(seg[id])) s.f = pchip(s.xs, s.ys);
      }
      for (const ev of evs) if (dayNum(ev.date) >= SC) for (const [id, v] of Object.entries(ev.values)) {
        const s = ((seg[id] = seg[id] || {}).STATCOUNTER = seg[id].STATCOUNTER || { xs: [], ys: [] }); s.xs.push(dayNum(ev.date)); s.ys.push(v / 100);
      }
      for (const id in seg) if (seg[id].STATCOUNTER) seg[id].STATCOUNTER.f = linear(seg[id].STATCOUNTER.xs, seg[id].STATCOUNTER.ys);
      const half0 = S.handover_months * 365.25 / 24;
      for (const h of race.handovers || []) {
        if (h.flagged && !S.include_flagged) continue;
        const to = dayNum(h.t_o), ti = dayNum(h.t_i), c = (to + ti) / 2, half = Math.max(half0, (ti - to) / 2);
        let a = c - half, b = c + half;
        if (b > SC) { a -= b - SC; b = SC; }
        const joined = Object.keys(seg).filter(id => seg[id][h.from] && seg[id][h.to] && seg[id][h.from].xs[seg[id][h.from].xs.length - 1] === to && seg[id][h.to].xs[0] === ti);
        windows.push({ from: h.from, to: h.to, t_o: h.t_o, t_i: h.t_i, a, b, flagged: h.flagged, joined,
                       D: Object.fromEntries(joined.map(id => [id, seg[id][h.to].ys[0] - seg[id][h.from].ys[seg[id][h.from].ys.length - 1]])) });
      }
      for (const ev of evs) {
        const t = dayNum(ev.date);
        if (t >= SC) continue;
        const W = windows.find(w => t >= w.a && t <= w.b);
        if (W) ev.smooth = { from: W.from, to: W.to };
        for (const id of Object.keys(ev.values)) {
          let v = null;
          if (W && W.joined.includes(id)) {
            const O = seg[id][W.from], I = seg[id][W.to], w = smoothstep((t - W.a) / (W.b - W.a));
            v = (1 - w) * O.f(t) + w * I.f(t);           // pchip / linear hold their end values outside their points
          } else {
            const s = Object.values(seg[id] || {}).find(s => t >= s.xs[0] && t <= s.xs[s.xs.length - 1]);
            if (s) v = s.f(t);                         // inside one source's points: the eased line
          }                                            // otherwise (a hand-over left as built): series.csv
          if (v != null) ev.values[id] = Math.round(Math.min(100, Math.max(0, v)) * 100);
        }
      }
    }
    /* changes of first place of the DRAWN values; dated = both browsers' figures that month are published (observed or
       arithmetic) and the month is not inside a smoothed window - only those get a callout and a hold (DEC-165 (7)) */
    const crown = [];
    let prev = null, prevOrder = [];
    for (const ev of evs) {
      const order = shareOrder(ev.values, prevOrder, label);
      ev.order = order;
      if (order[0] !== prev) {
        const dated = prev != null && !ev.smooth && 'oa'.includes(ev.prov[order[0]]) && 'oa'.includes(ev.prov[prev] || 'i');
        crown.push({ date: ev.date, id: order[0], previous: dated ? prev : null, was: prev, style: ev.style[order[0]], dated });
      }
      prev = order[0]; prevOrder = order;
    }
    return Object.assign({}, race, { events: evs, crown, windows, smoothing: S });
  }

  /* IQ-18 (RTT-103): a MONEY series (race.kind "money", scripts/rtt103_adapter.py) is drawn as the share kind is
     (bars that start or stop fade in and out, board.fit), with whole US dollars instead of hundredths of a percent and
     no smoothing. cfg.gaps {mode: "leave" | "hold"}: "leave" (the data as it is) - a company with no figure leaves the
     board and comes back; "hold" (an option for Luke) - during a gap listed in race.gaps the bar stays on the board at
     the length of its last figure, marked held (the player dims it and shows no number). A held length is never a
     figure: it is excluded from the combined total (race events' `combined`, the data's sum of the bars). */
  function holdGaps(race, cfg) {
    if (race.kind !== 'money' || !cfg.gaps || cfg.gaps.mode !== 'hold') return race;
    const evs = race.events.map(ev => Object.assign({}, ev, { values: Object.assign({}, ev.values), style: Object.assign({}, ev.style),
                                                             prov: Object.assign({}, ev.prov), held: [] }));
    for (const g of race.gaps || []) for (const ev of evs) if (ev.date >= g.from && ev.date <= g.to) {
      if (g.id in ev.values) throw new Error('gap ' + g.id + ' ' + ev.date + ': the data has a figure');
      ev.values[g.id] = g.last_value; ev.style[g.id] = 'official'; ev.prov[g.id] = 'o'; ev.held.push(g.id);
    }
    return Object.assign({}, race, { events: evs });
  }

  /* IQ-18c (RTT-103, Luke's direction DEC-371): after June 2026 the race carries straight on, on the same board, through
     the 2026 plans and the 2027-2030 estimates. cfg.forward {enabled, count_sec, boards:[{year, kind "plans"|"estimate",
     sec, count_sec?, month, source_line, footer, comb_note, notes{id: text}, prefix{id: text}}], extra{id: {label,
     colour}}}. One event per board is appended after the data's last quarter, built from race.steps.lookahead (the
     look-ahead file, copied by scripts/rtt103_adapter.py unchanged; whole dollars from its tenths of a billion): the
     bar's length is the top of its range (`values`, so the order is by the top of the range) and `lo` the bottom;
     style "official" (a company plan or a 12-month actual), "estimated" (a Race Through Time estimate, striped) or
     "analyst_estimate" (Citi); an extra row (ByteDance, a press report on the 2026 board only) has style "press" and
     is never in `combined`. Each board holds for `sec`, counting from the board before over count_sec. Off (and
     nothing appended) unless configured. */
  function forwardBoards(race, cfg) {
    const F = cfg.forward;
    if (race.kind !== 'money' || !F || !F.enabled) return race;
    const LA = (race.steps || {}).lookahead || [], label = {};
    for (const e of race.entrants) label[e.id] = e.label;
    for (const [id, x] of Object.entries(F.extra || {})) label[id] = x.label;
    const D = s => { const t = String(s).trim(); if (!/^\d+(\.\d)?$/.test(t)) throw new Error('forward: not a figure in tenths of a billion: ' + s);
      const [a, b] = t.split('.'); return (Number(a) * 10 + Number(b || 0)) * 100000000; };
    const evs = race.events.slice();
    let prevOrder = evs[evs.length - 1].order || [];
    for (const B of F.boards) {
      const y = String(B.year), rows = LA.filter(r => r.frame_year === y && r.row_type !== 'COMBINED'), C = LA.find(r => r.frame_year === y && r.row_type === 'COMBINED');
      if (!rows.length || !C) throw new Error('forward: no look-ahead rows for ' + y);
      const values = {}, lo = {}, style = {}, mode = {}, prov = {};
      for (const r of rows) { const id = r.company.toLowerCase();
        if (!(id in label)) throw new Error('forward: ' + r.company + ' is not in the race');
        values[id] = D(r.estimate_high_usd_bn); lo[id] = D(r.estimate_low_usd_bn); prov[id] = 'o';
        const citi = r.row_type === 'CITI_ESTIMATE' || r.label === 'Citi estimate';
        style[id] = citi ? 'analyst_estimate' : B.kind === 'estimate' ? 'estimated' : 'official';
        mode[id] = B.kind === 'estimate' ? (citi ? 'actual' : 'est') : (r.label === 'actual' ? 'actual' : 'plan'); }
      let sum = 0, sumLo = 0; for (const id of Object.keys(values)) { sum += values[id]; sumLo += lo[id]; }
      if (Math.abs(sum - D(C.estimate_high_usd_bn)) > 1e8 * rows.length || Math.abs(sumLo - D(C.estimate_low_usd_bn)) > 1e8 * rows.length)
        throw new Error('forward ' + y + ': the bars do not add up to the combined row');
      for (const [id, x] of Object.entries(F.extra || {})) if ((x.years || []).includes(B.year)) {
        const src = (race.steps || {})[x.source]; if (!src) throw new Error('forward: no ' + x.source + ' in the race file');
        values[id] = lo[id] = D(src[x.field]); style[id] = 'press'; mode[id] = 'actual'; prov[id] = 'o'; }
      const order = shareOrder(values, prevOrder, label); prevOrder = order;
      evs.push({ date: y + '-12-31', quarter: y + '-F', values, lo, style, prov, plus: [], order,
                 combined: D(C.estimate_high_usd_bn), combined_lo: D(C.estimate_low_usd_bn),
                 beat_sec: B.sec, count_sec: B.count_sec != null ? B.count_sec : (F.count_sec || 1.5),
                 fwd: Object.assign({ mode, extra: Object.keys(F.extra || {}).filter(id => id in values) }, B) });
    }
    return Object.assign({}, race, { events: evs });
  }

  function buildSeries(race, cfg) {
    const SHARE = race.kind === 'share' || race.kind === 'money' || race.kind === 'visits', MONEY = race.kind === 'money', VISITS = race.kind === 'visits';
    if (MONEY) race = holdGaps(race, cfg);
    if (SHARE) race = shareRace(race, cfg);
    if (MONEY) race = forwardBoards(race, cfg);                  // IQ-18c: off unless cfg.forward
    const fps = cfg.fps, rows = cfg.rows, P = cfg.pacing;
    checkPacing(P);
    const from = (cfg.window && cfg.window.from) || '0000-00-00';
    const to   = (cfg.window && cfg.window.to)   || '9999-99-99';
    const launch = {}, maker = {};
    for (const e of race.entrants) { launch[e.id] = e.launch_date; maker[e.id] = e.maker; }
    const reached = {}, lastVal = {};
    const all = [];
    race.events.forEach((ev, i) => {
      if (i > 0 && !(ev.date > race.events[i - 1].date)) throw new Error('quarter ends out of order at ' + ev.date);
      for (const [id, u] of Object.entries(ev.values)) {
        if (!Number.isInteger(u) || u < 0) throw new Error(ev.date + ' ' + id + ': units must be a whole number');
        if (lastVal[id] !== u) { lastVal[id] = u; reached[id] = ev.date; }
      }
      const r = Object.assign({}, reached);
      const order = SHARE ? ev.order : Object.keys(ev.values).sort((a, b) => (ev.values[b] - ev.values[a]) || (r[a] < r[b] ? -1 : r[a] > r[b] ? 1 : 0) || (launch[a] < launch[b] ? -1 : launch[a] > launch[b] ? 1 : 0));
      const plus = {}; for (const id of ev.plus) plus[id] = true;
      const mplus = {}; for (const m of ev.maker_plus || []) mplus[m] = true;
      const held = {}; for (const id of ev.held || []) held[id] = true;            // IQ-18: hold option only
      if (VISITS) { let c = 0; for (const [id, v] of Object.entries(ev.values)) if ((ev.status || {})[id] !== 'latest_figure') c += v; ev.combined = c; }   // IQ-19b: the sum of the bars with a figure that month (held bars left out)
      const fx = ev.fwd ? { lo: Object.assign({}, ev.lo), fwd: true } : VISITS ? { labels: Object.assign({}, ev.labels), prov: Object.assign({}, ev.prov) } : {};   // IQ-18c; IQ-19: the name at that date, published / line / held
      all.push({ ev, st: { order, totals: Object.assign({}, ev.values), style: Object.assign({}, ev.style), plus, status: Object.assign({}, ev.status || {}), held, ...fx,
                           maker_totals: Object.assign({}, ev.maker_totals), maker_style: Object.assign({}, ev.maker_style), maker_plus: mplus } });
    });
    let first = all.findIndex(x => x.ev.date >= from);
    if (first < 0) throw new Error('no quarter ends inside the window ' + from + ' .. ' + to);
    const openIdx = first > 0 ? first - 1 : 0;
    if (first === 0) first = 1;
    const opening = all[openIdx].st, openingEvent = Object.assign({ season: all[openIdx].ev.date.slice(0, 4) }, all[openIdx].ev);
    const win = all.slice(first).filter(x => x.ev.date <= to);
    if (!win.length) throw new Error('no quarter ends inside the window ' + from + ' .. ' + to);
    const events = win.map(x => Object.assign({ season: x.ev.date.slice(0, 4), credits: [] }, x.ev));
    const states = win.map(x => x.st);

    const JR = P.judge_rows || rows, mult = [], kind = [];
    /* round 3 (live_only): the beat is judged on the live board - consoles up to their retirement quarter */
    const LIVE_ON = !!(cfg.live_only && cfg.live_only.enabled), retQ = {};
    if (LIVE_ON) for (const e of race.entrants) if (e.fade_date) { const f = all.find(x => x.ev.date >= e.fade_date); if (f) retQ[e.id] = f.ev.date; }
    const vis = (st, date) => (LIVE_ON ? st.order.filter(id => !retQ[id] || date <= retQ[id]) : st.order).slice(0, JR);
    let prev = opening, prevDate = openingEvent.date, settled = 0;
    for (let k = 0; k < events.length; k++) {
      const a = vis(prev, prevDate), b = vis(states[k], events[k].date); prevDate = events[k].date;
      const moved = b.filter(id => states[k].totals[id] !== prev.totals[id]);
      let kd;
      if (!sameList(a, b)) { kd = 'rank_change'; settled = 0; }
      else if (moved.length) { settled++; kd = settled > P.settled_run_after ? 'quiet' : 'visible_change'; }
      else { settled++; kd = 'quiet'; }
      kind.push(kd); mult.push(P.mult[kd]); prev = states[k];
    }
    const RH = cfg.record_hold || {};
    const crownAt = {};
    for (const c of race.crown || []) if (c.previous) crownAt[c.date] = c;
    const records = [], hold = [];
    events.forEach((ev, k) => {
      const c = crownAt[ev.date];
      hold.push(!!RH.enabled && (RH.types || []).includes('CROWN') && !!c);
      if (c) records.push({ k, date: ev.date, id: c.id, previous: c.previous, style: c.style, type: 'CROWN', held: hold[k] });
    });
    /* IQ-13: a segment may also name the month it starts from ({from, sec_per_event}: a faster fixed pace from a named month) */
    const base = ev => { for (const s of P.segments || []) if ((s.to == null || ev.date <= s.to) && (s.from == null || ev.date >= s.from)) return s.sec_per_event; return P.sec_per_event; };
    /* With counting (cfg.count, round 2), a held quarter counts at its normal beat and THEN holds for
       record_hold.sec, so the pause follows the overtake; without counting (round 1) the hold replaces
       the beat, as RTT-002's record pauses do. */
    const CNT = !!(cfg.count && cfg.count.enabled);
    const beatSec = k => events[k].beat_sec != null ? events[k].beat_sec : CNT ? base(events[k]) * mult[k] + (hold[k] ? RH.sec : 0) : (hold[k] ? RH.sec : base(events[k]) * mult[k]);
    const startFrame = [];
    let sec = P.lead_in_sec;
    for (let k = 0; k < events.length; k++) {
      startFrame.push(Math.round(sec * fps));
      if (k < events.length - 1) sec += beatSec(k);
    }
    const lastK = events.length - 1;
    const raceFrames = events[lastK].beat_sec != null ? startFrame[lastK] + Math.round(events[lastK].beat_sec * fps)   // IQ-18c/18e: the last forward board's own length
      : P.final_board_sec != null
      ? startFrame[lastK] + Math.round(P.final_board_sec * fps)
      : Math.round((sec + beatSec(lastK) + P.end_hold_sec) * fps);
    for (let k = 1; k < startFrame.length; k++)
      if (startFrame[k] <= startFrame[k - 1]) throw new Error('two events share a frame; raise sec_per_event');

    const MO = cfg.maker_order || [];
    const index = {};
    for (const e of race.entrants) {
      const i = MO.indexOf(e.maker);
      if (i < 0 || i >= (cfg.palette || []).length) throw new Error('no maker colour for ' + e.maker + ' (maker_order / palette)');
      index[e.id] = i;
    }
    const fade = {};
    for (const e of race.entrants) {
      if (!e.fade_date) { fade[e.id] = null; continue; }
      if (e.fade_date <= openingEvent.date) { fade[e.id] = -1; continue; }
      const k = events.findIndex(ev => ev.date >= e.fade_date);
      fade[e.id] = k < 0 ? null : k;
    }
    /* IQ-10 round 2 (DEC-115): counting. Quarter k counts from quarter k-1's figures to its own over
       countFrames[k] frames (its whole beat; a held quarter and the last quarter: one normal beat, then the
       board holds),
       reaching the exact series.csv value on the LAST frame of that count (the quarter-end frame). */
    const countFrames = events.map((ev, k) => ev.count_sec != null ? Math.min(Math.round(ev.count_sec * fps), k < lastK ? startFrame[k + 1] - startFrame[k] : Infinity)   // IQ-18c
                                         : k < lastK && !hold[k] ? startFrame[k + 1] - startFrame[k] : Math.max(1, Math.round(base(ev) * mult[k] * fps)));
    const tl = { series: true, events, states, opening, openingEvent, startFrame, raceFrames, mult, kind, fps, rows,
                 colours: { index, used: MO.length, sets: [], fadeRaces: 0, minDeltaE: 0, rows }, hold, records,
                 highlight: events.map(() => []), hasStarts: false, fade, makers: race.makers, entrants: race.entrants,
                 countFrames, launch };
    tl.quarterEndFrame = events.map((ev, k) => startFrame[k] + countFrames[k] - 1);
    /* Moments (callouts): every change of first place (crown.csv) plus the configured extra moments
       (cfg.moments: {type: "first_past", id, units} or {type: "passes", id, other, rank}). Each is checked
       against the data here (a claim the data does not support stops the build) and placed on the exact
       frame where the counted figures cross. */
    const moments = [];
    const crossing = (k, test) => { for (let s = 0; s < countFrames[k]; s++) { if (test(seriesFrame(tl, k, s))) return startFrame[k] + s; } return null; };
    for (const r of records) {
      const f = crossing(r.k, F => F.order[0] === r.id);
      if (f == null) throw new Error('crown change ' + r.date + ': the counted figures never put ' + r.id + ' first');
      moments.push({ type: 'crown', k: r.k, date: r.date, id: r.id, other: r.previous, style: r.style, frame: f });
    }
    const styleOf = (k, ids) => ids.map(id => states[k].style[id]).sort((a, b) => ({ official: 0, estimated: 1, analyst_estimate: 2 }[b] - { official: 0, estimated: 1, analyst_estimate: 2 }[a]))[0];
    for (const m of cfg.moments || []) {
      if (m.on_hold) continue;                                   // approved but not shown yet
      if (m.type === 'first_past') {
        const k = states.findIndex(s => (s.totals[m.id] || 0) >= m.units);
        if (k < 0) continue;                                     // not inside this window
        const before = k > 0 ? states[k - 1] : opening;
        if ((before.totals[m.id] || 0) >= m.units) continue;     // crossed before the window
        const firstEver = all.findIndex(x => Object.values(x.st.totals).some(u => u >= m.units));
        if (all[firstEver].ev.date !== events[k].date || !(all[firstEver].st.totals[m.id] >= m.units)) throw new Error('moment: ' + m.id + ' is not the first console past ' + m.units);
        const f = crossing(k, F => F.u[m.id] >= m.units);
        moments.push({ type: m.type, k, date: events[k].date, id: m.id, units: m.units, style: styleOf(k, [m.id]), frame: f });
      } else if (m.type === 'passes') {
        const k = states.findIndex((s, i) => { const b = i > 0 ? states[i - 1] : opening;
          return s.order.indexOf(m.id) === m.rank - 1 && s.order.indexOf(m.other) === m.rank && b.order.indexOf(m.other) >= 0 && b.order.indexOf(m.other) < (b.order.indexOf(m.id) < 0 ? 1e9 : b.order.indexOf(m.id)); });
        if (k < 0) continue;
        const f = crossing(k, F => F.order.indexOf(m.id) === m.rank - 1 && F.order.indexOf(m.other) === m.rank);
        if (f == null) throw new Error('moment: ' + m.id + ' never passes ' + m.other + ' in the counted figures');
        moments.push({ type: m.type, k, date: events[k].date, id: m.id, other: m.other, rank: m.rank, style: styleOf(k, [m.id, m.other]), frame: f });
      } else throw new Error('unknown moment type ' + m.type);
    }
    moments.sort((a, b) => a.frame - b.frame);
    tl.moments = moments;
    /* The final-table line (cfg.final_line {id, other}): "<id> is at least <gap> million behind the <other>",
       gap = other - id rounded DOWN to 0.1 million, "at least" only when the other's figure is a lower bound. */
    const FL = cfg.final_line;
    tl.isDataEnd = events[lastK].date === race.events[race.events.length - 1].date;   // the final table of the film
    if (VISITS && FL && FL.enabled && tl.isDataEnd) tl.finalLine = { text: FL.text };   // IQ-19: one line of fixed wording, from verified figures (the config says which)
    else if (FL && FL.enabled && tl.isDataEnd) {
      const s = states[lastK], a = s.totals[FL.id], b = s.totals[FL.other];
      if (!(b > a)) throw new Error('final line: ' + FL.other + ' is not ahead of ' + FL.id);
      const t = Math.floor((b - a) / 100000);
      tl.finalLine = { text: (FL.label || FL.id) + ' is ' + (s.plus[FL.other] ? 'at least ' : '') + Math.floor(t / 10) + '.' + (t % 10) + ' million behind the ' + (FL.other_label || FL.other), gap: b - a, atLeast: !!s.plus[FL.other] };
    }
    tl.finalFrom = tl.quarterEndFrame[lastK];
    /* IQ-10 round 3 (DEC-125): live consoles only. A console races while it is still adding shipments:
       up to and including the first quarter end on or after its fade_date (data/rtt-003/consoles.csv).
       During that last quarter its row carries "· retires"; right after the quarter's count it fades over
       exit_fade_sec and leaves the board. exit[id] = {k, start (tag from), fadeFrom, end, units} (k -1 = at
       the opening board);
       'gone' = retired before the window; absent = races to the end of the window. With the window
       reaching the end of the data, the film closes on the ALL-TIME top table (retired consoles included):
       a transition of final_transition_sec after the last count, then final_hold_sec. */
    const LO = cfg.live_only;
    if (LO && LO.enabled) {
      tl.liveOnly = true;
      const fps_ = fps, fadeF = Math.round((LO.exit_fade_sec || 0.5) * fps_);
      tl.exitFade = fadeF;
      tl.exit = {};
      for (const e of race.entrants) {
        if (!e.fade_date) continue;
        const fq = all.find(x => x.ev.date >= e.fade_date);
        if (!fq) continue;
        if (fq.ev.date < openingEvent.date) { tl.exit[e.id] = 'gone'; continue; }
        const k = fq.ev.date === openingEvent.date ? -1 : events.findIndex(ev => ev.date === fq.ev.date);
        if (k === -1 && fq.ev.date !== openingEvent.date) continue;    // retires after the window
        const start = k >= 0 ? startFrame[k] : 0, fadeFrom = (k >= 0 ? tl.quarterEndFrame[k] : startFrame[0] - 1) + 1;
        tl.exit[e.id] = { k, date: fq.ev.date, start, fadeFrom, end: fadeFrom + fadeF, units: fq.st.totals[e.id], plus: !!fq.st.plus[e.id] };
      }
      if (tl.isDataEnd) {
        tl.finalTable = true;
        tl.finalTransition = Math.round((LO.final_transition_sec || 1.0) * fps_);
        tl.raceFrames = tl.quarterEndFrame[lastK] + 1 + tl.finalTransition + Math.round((LO.final_hold_sec != null ? LO.final_hold_sec : 10) * fps_);
        tl.finalLineFrom = tl.quarterEndFrame[lastK] + 1 + tl.finalTransition;
      }
    }
    /* IQ-10 round 4 (DEC-131, DEC-132): every console stays on the all-time board; a bar that is not live
       carries its status from the data (series.csv `status`: "latest_figure" or "retired"). The status of
       quarter k applies from that quarter's quarter-end frame (the frame on which its count lands on the
       exact figure) until the next quarter-end frame; before the first one, the opening board's status.
       status[id] = [{frame, kind}] (frame -Infinity = the opening board); dimFrom = the frame the bar
       stopped being live (the dim and the label fade in over status.sec from there). */
    const ST = cfg.status;
    if (ST && ST.enabled) {
      tl.statusOn = true;
      tl.statusFade = Math.max(1, Math.round((ST.sec != null ? ST.sec : 0.6) * fps));
      tl.status = {};
      for (const e of race.entrants) {
        const list = [{ frame: -Infinity, kind: opening.status[e.id] || 'live' }];
        events.forEach((ev, k) => { const kd = states[k].status[e.id] || 'live';
          if (kd !== list[list.length - 1].kind) list.push({ frame: VISITS ? startFrame[k] : tl.quarterEndFrame[k], kind: kd }); });   // IQ-19b: a visits bar dims while it sinks below the live bars (the month's count), so its landing frame shows it dimmed
        tl.status[e.id] = list;
      }
    }
    /* IQ-13 (RTT-001, share): the hand-over windows used, the "new source" markers and the dated notes */
    if (SHARE) {
      tl.share = true; tl.windows = race.windows; tl.smoothing = race.smoothing; tl.scStart = race.sc_start;
      if (MONEY && events.some(ev => ev.fwd)) { tl.forward = true; tl.lastActual = events.findIndex(ev => ev.fwd) - 1; }   // IQ-18c: the index of June 2026 (-1: before the window)
      if (MONEY) { tl.allCombined = all.filter(x => !x.ev.fwd).map(x => ({ date: x.ev.date, c: x.ev.combined })); tl.money = true; tl.gaps = race.gaps || []; tl.story = race.story || []; tl.steps = race.steps || {}; tl.notesData = race.notes || {}; }
      if (VISITS) { tl.visits = true; tl.ease = race.ease; tl.monthIndex = race.monthIndex; tl.sink = race.sink; tl.clock = cfg.clock || 'month'; tl.story = [];   // IQ-19
        tl.allCombined = all.map(x => ({ date: x.ev.date, c: x.ev.combined })); }                                                                   // IQ-19b: the panel's line
      tl.crownAll = race.crown;
      const srcs = ev => ev.smooth ? [ev.smooth.from, ev.smooth.to] : String(ev.source_id || '').split('>').filter(Boolean);
      tl.markers = [];
      events.forEach((ev, k) => { const was = srcs(k > 0 ? events[k - 1] : openingEvent), now = srcs(ev);
        const fresh = now.filter(s => !was.includes(s));
        if (fresh.length && was.length) tl.markers.push({ k, date: ev.date, frame: startFrame[k], sources: fresh }); });
      tl.notes = [];
      for (const n of cfg.notes_at || []) { const k = events.findIndex(ev => ev.date === n.date); if (k >= 0) tl.notes.push(Object.assign({ k, date: n.date, frame: startFrame[k], text: n.text },
        n.to ? { end: tl.quarterEndFrame[events.findIndex(ev => ev.date === n.to)] } : {})); }   // IQ-19b: notes_at[].to - on screen until the landing frame of month `to`
    }
    /* IQ-18b (RTT-103, money): the steps after the race (cfg.steps.sequence [{name, sec, ...}], drawn by rtt_steps.js),
       scheduled from the race's last frame; only when the window reaches the end of the data. tl.raceEnd = the first
       frame after the race; tl.stepPlan[i] = {name, ..., first, frames}; tl.raceFrames then covers the steps too. */
    if (MONEY && cfg.steps && cfg.steps.enabled && tl.isDataEnd) {
      tl.raceEnd = tl.raceFrames; tl.stepPlan = [];
      let f = tl.raceFrames;
      for (const st of cfg.steps.sequence) { const n = Math.round(st.sec * fps); tl.stepPlan.push(Object.assign({}, st, { first: f, frames: n })); f += n; }
      tl.raceFrames = f;
    }
    return tl;
  }

  /* IQ-13 (RTT-001, share): the counted board on frame `since` of month k. Like seriesFrame, plus bars that enter
     and leave: a browser with no value at month k-1 appears at month k's value, fading in over the count; one with
     no value at month k keeps month k-1's value and fades out, gone on the month-end frame (no bar where the data
     has no value). alpha[id] is that fade (1 for every other bar). */
  function shareFrame(tl, k, since) {
    if (k < 0) { const o = tl.opening, alpha = {}; o.order.forEach(id => { alpha[id] = 1; });
      return { g: 1, u: Object.assign({}, o.totals), order: o.order.slice(), plus: {}, mu: {}, mplus: {}, alpha }; }
    const cur = tl.states[k], prev = k > 0 ? tl.states[k - 1] : tl.opening, n = tl.countFrames[k];
    const g = n <= 1 ? 1 : Math.min(1, Math.max(0, since) / (n - 1));
    const u = {}, alpha = {}, idx = {};
    cur.order.forEach((id, i) => { idx[id] = i; const b = cur.totals[id];
      if (id in prev.totals) { const a = prev.totals[id]; u[id] = g >= 1 ? b : Math.round(a + (b - a) * g); alpha[id] = 1; }
      else { u[id] = b; alpha[id] = g; } });
    if (g < 1) prev.order.forEach((id, i) => { if (!(id in cur.totals)) { u[id] = prev.totals[id]; alpha[id] = 1 - g; idx[id] = 1e6 + i; } });
    if (tl.visits) {                       // IQ-19 (RTT-102): eased motion frame by frame; held bars below the live ones
      const MI = tl.monthIndex, d0 = k > 0 ? tl.events[k - 1].date : tl.openingEvent.date, x = MI[d0] + (MI[tl.events[k].date] - MI[d0]) * g;
      if (g < 1 && tl.ease) for (const id of Object.keys(u)) if (tl.ease[id] && id in prev.totals && id in cur.totals && cur.prov[id] !== 'h') u[id] = Math.round(tl.ease[id](x));
      const held = id => tl.sink && (cur.status[id] === 'latest_figure' || (!(id in cur.totals) && prev.status[id] === 'latest_figure'));
      const order = Object.keys(u).sort((a, b) => (held(a) - held(b)) || (u[b] - u[a]) || (idx[a] - idx[b]));
      return { g, u, order, plus: {}, mu: {}, mplus: {}, alpha };
    }
    const order = Object.keys(u).sort((x, y) => (u[y] - u[x]) || (idx[x] - idx[y]));
    if (!cur.lo && !prev.lo) return { g, u, order, plus: {}, mu: {}, mplus: {}, alpha };
    /* IQ-18c: a forward board's ranges - the bottom of each range counted like the top (from the previous board's
       bottom, or from the June 2026 figure) */
    const lo = {}, L0 = id => prev.lo && id in prev.lo ? prev.lo[id] : prev.totals[id];
    for (const id of Object.keys(u)) {
      if (!(id in cur.totals)) lo[id] = L0(id);
      else if (!(id in prev.totals)) lo[id] = cur.lo ? cur.lo[id] : cur.totals[id];
      else { const a = L0(id), b = cur.lo ? cur.lo[id] : cur.totals[id]; lo[id] = g >= 1 ? b : Math.round(a + (b - a) * g); } }
    return { g, u, order, plus: {}, mu: {}, mplus: {}, alpha, lo };
  }

  /* IQ-10 round 4: a bar's status at frame f: {kind, dimFrom} (dimFrom: frame it stopped being live,
     -Infinity = before the window, null = live). */
  function statusAt(tl, id, f) {
    const list = tl.status && tl.status[id];
    if (!list) return { kind: 'live', dimFrom: null };
    let i = 0; while (i + 1 < list.length && list[i + 1].frame <= f) i++;
    if (list[i].kind === 'live') return { kind: 'live', dimFrom: null };
    let j = i; while (j > 0 && list[j - 1].kind !== 'live') j--;
    return { kind: list[i].kind, dimFrom: list[j].frame };
  }

  /* IQ-10 round 3: is console id on the live board at frame f? (launched, and not past the end of its exit) */
  function isLive(tl, id, f) {
    const x = tl.exit && tl.exit[id];
    if (x === 'gone') return false;
    return !x || f < x.end;
  }

  /* IQ-10 round 2: the counted board on frame `since` of quarter k (k = -1: the opening board). Units are
     whole numbers on a straight line from quarter k-1 to quarter k, exact on the quarter-end frame (g = 1).
     Order: most counted units first; equal counts keep quarter k's order (its tie rule). "+": on the
     quarter-end frame exactly the data's flag; while counting, "+" if either end is a lower bound. */
  function seriesFrame(tl, k, since) {
    if (tl.share) return shareFrame(tl, k, since);
    if (k < 0) { const o = tl.opening; return { g: 1, u: Object.assign({}, o.totals), order: o.order.slice(), plus: Object.assign({}, o.plus), mu: Object.assign({}, o.maker_totals), mplus: Object.assign({}, o.maker_plus) }; }
    const cur = tl.states[k], prev = k > 0 ? tl.states[k - 1] : tl.opening, n = tl.countFrames[k];
    const g = n <= 1 ? 1 : Math.min(1, Math.max(0, since) / (n - 1));
    const u = {}, plus = {}, mu = {}, mplus = {}, idx = {};
    cur.order.forEach((id, i) => { idx[id] = i; const a = prev.totals[id] || 0, b = cur.totals[id];
      u[id] = g >= 1 ? b : Math.round(a + (b - a) * g);
      plus[id] = g >= 1 ? !!cur.plus[id] : !!(cur.plus[id] || prev.plus[id]); });
    const order = cur.order.slice().sort((x, y) => (u[y] - u[x]) || (idx[x] - idx[y]));
    for (const m of Object.keys(cur.maker_totals)) { const a = prev.maker_totals[m] || 0, b = cur.maker_totals[m];
      mu[m] = g >= 1 ? b : Math.round(a + (b - a) * g);
      mplus[m] = g >= 1 ? !!cur.maker_plus[m] : !!(cur.maker_plus[m] || prev.maker_plus[m]); }
    return { g, u, order, plus, mu, mplus };
  }

  /* Which event is showing at race frame f: the last event whose start frame is <= f, or -1
     during the lead-in (the opening board). */
  function eventAt(tl, f) {
    let lo = 0, hi = tl.startFrame.length - 1, k = -1;
    while (lo <= hi) {
      const m = (lo + hi) >> 1;
      if (tl.startFrame[m] <= f) { k = m; lo = m + 1; } else hi = m - 1;
    }
    return k;
  }

  /* ---- colours (IQ-05) ---- */

  /* Every label on a bar is white; a palette colour too light for white type is darkened,
     keeping its hue (C2-2's darkenForWhite, moved here so the colour rule is judged on the
     colour actually drawn). */
  const _ink = {};
  function drawnColour(hex) {
    if (_ink[hex]) return _ink[hex];
    const n = parseInt(hex.replace('#', ''), 16);
    let r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    const L = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    if (L > 0.52) { const k = 0.46 / L; r = Math.round(r * k); g = Math.round(g * k); b = Math.round(b * k); }
    return _ink[hex] = '#' + [r, g, b].map(v => v.toString(16).padStart(2, '0')).join('');
  }
  /* CIE L*a*b* (D65) of a colour as drawn, and the CIEDE2000 difference between two drawn
     colours (Sharma, Wu & Dalal 2005). About 1 is the smallest difference people notice side by
     side; colour_rule.min_delta_e (18) asks for colours that read as different colours. CIEDE2000
     is used rather than the plain Lab distance because the plain distance overrates differences
     between blues, purples and pinks. */
  function lab(hex) {
    const n = parseInt(drawnColour(hex).slice(1), 16);
    const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    const r = lin((n >> 16) & 255), g = lin((n >> 8) & 255), b = lin(n & 255);
    const X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, Y = 0.2126 * r + 0.7152 * g + 0.0722 * b,
          Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883;
    const f = t => t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116;
    return [116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))];
  }
  function deltaE(h1, h2) {
    const [L1, a1, b1] = lab(h1), [L2, a2, b2] = lab(h2);
    const rad = Math.PI / 180, deg = 180 / Math.PI, p7 = x => Math.pow(x, 7);
    const Cb = (Math.hypot(a1, b1) + Math.hypot(a2, b2)) / 2;
    const G = 0.5 * (1 - Math.sqrt(p7(Cb) / (p7(Cb) + p7(25))));
    const a1p = (1 + G) * a1, a2p = (1 + G) * a2;
    const C1p = Math.hypot(a1p, b1), C2p = Math.hypot(a2p, b2);
    const h1p = (Math.atan2(b1, a1p) * deg + 360) % 360, h2p = (Math.atan2(b2, a2p) * deg + 360) % 360;
    const dL = L2 - L1, dC = C2p - C1p;
    let dh = 0;
    if (C1p * C2p !== 0) { dh = h2p - h1p; if (dh > 180) dh -= 360; else if (dh < -180) dh += 360; }
    const dH = 2 * Math.sqrt(C1p * C2p) * Math.sin(dh / 2 * rad);
    const Lb = (L1 + L2) / 2, Cbp = (C1p + C2p) / 2;
    let hb = h1p + h2p;
    if (C1p * C2p !== 0) hb = Math.abs(h1p - h2p) <= 180 ? hb / 2 : (hb < 360 ? (hb + 360) / 2 : (hb - 360) / 2);
    const T = 1 - 0.17 * Math.cos((hb - 30) * rad) + 0.24 * Math.cos(2 * hb * rad) + 0.32 * Math.cos((3 * hb + 6) * rad) - 0.20 * Math.cos((4 * hb - 63) * rad);
    const dth = 30 * Math.exp(-Math.pow((hb - 275) / 25, 2));
    const RC = 2 * Math.sqrt(p7(Cbp) / (p7(Cbp) + p7(25)));
    const SL = 1 + 0.015 * Math.pow(Lb - 50, 2) / Math.sqrt(20 + Math.pow(Lb - 50, 2));
    const SC = 1 + 0.045 * Cbp, SH = 1 + 0.015 * Cbp * T, RT = -Math.sin(2 * dth * rad) * RC;
    return Math.sqrt(Math.pow(dL / SL, 2) + Math.pow(dC / SC, 2) + Math.pow(dH / SH, 2) + RT * (dC / SC) * (dH / SH));
  }

  /* Who can be on screen together, over the whole race file. A driver is on the board while in
     the top N, and a driver who has just dropped out is still fading for a moment, so the set
     that can be seen during event k is the top N after events k-W .. k, W = colour_rule.fade_races.
     The same pairs are returned for every config that shares rows and fade_races, whatever
     its window or pace. */
  function coVisible(race, rows, W) {
    const totals = {}, reached = {}, tops = [], first = {};
    race.events.forEach((ev, k) => {
      for (const c of ev.credits) { totals[c.id] = (totals[c.id] || 0) + 1; reached[c.id] = c.credit_index; }
      const top = rankOf(totals, reached).slice(0, rows);
      top.forEach((id, i) => { if (!(id in first)) first[id] = [k, i]; });
      tops.push(top);
    });
    const adj = {}, sets = [];
    for (let k = 0; k < tops.length; k++) {
      const V = new Set();
      for (let j = Math.max(0, k - W); j <= k; j++) tops[j].forEach(id => V.add(id));
      const ids = [...V];
      sets.push(ids);
      for (const a of ids) { adj[a] = adj[a] || new Set(); for (const b of ids) if (a !== b) adj[a].add(b); }
    }
    return { adj, sets, first };
  }

  /* One colour per driver: drivers in the order they first reach the top N (ties at the same
     race by rank), each takes the first palette colour that is at least min_delta_e away from
     the colour of every driver it can share the screen with. Deterministic: same file, same
     config -> same colours. A driver who never reaches the top N is never drawn and takes the
     first colour. If the palette runs out, it refuses rather than repeat a colour. */
  function assignColours(race, cfg) {
    const pal = cfg.palette, R = cfg.colour_rule || {};
    const W = R.fade_races != null ? R.fade_races : 3, minDE = R.min_delta_e != null ? R.min_delta_e : 0;
    const rows = cfg.rows;
    const { adj, sets, first } = coVisible(race, rows, W);
    let order = Object.keys(first).sort((a, b) => (first[a][0] - first[b][0]) || (first[a][1] - first[b][1]));
    /* IQ-05c (DEC-034 step 5), colour_rule.priority {rows, bright}: the drivers who ever reach the
       top priority.rows (10) choose first, most career wins at the end of the race file first (ties:
       who reached the top priority.rows first), and the palette's first priority.bright colours
       (the bright, light ones) are kept for them: every other driver tries the rest of the palette
       first and takes a bright colour only if nothing else fits. The DEC-023 rule itself (no two
       drivers on screen together closer than min_delta_e) is unchanged. */
    const P = R.priority, top = new Set();
    let bright = 0;
    if (P) {
      const fin = {}, reached = {}, firstTop = {};
      race.events.forEach((ev, k) => {
        for (const c of ev.credits) { fin[c.id] = c.total; reached[c.id] = c.credit_index; }
        rankOf(fin, reached).slice(0, P.rows).forEach((id, i) => { top.add(id); if (!(id in firstTop)) firstTop[id] = [k, i]; });
      });
      const pos = id => order.indexOf(id);
      const tops = order.filter(id => top.has(id)).sort((a, b) => (fin[b] - fin[a]) || (firstTop[a][0] - firstTop[b][0]) || (firstTop[a][1] - firstTop[b][1]));
      order = tops.concat(order.filter(id => !top.has(id)).sort((a, b) => pos(a) - pos(b)));
      bright = P.bright || 0;
    }
    const idx = {};
    const tryOrderOf = id => {
      const t = [];
      if (P && !top.has(id)) { for (let i = bright; i < pal.length; i++) t.push(i); for (let i = 0; i < bright; i++) t.push(i); }
      else for (let i = 0; i < pal.length; i++) t.push(i);
      return t;
    };
    if (!P) {
      /* IQ-05 greedy, unchanged: each driver takes the first colour that fits */
      for (const id of order) {
        let pick = -1;
        for (const ci of tryOrderOf(id)) {
          let ok = true;
          for (const m of adj[id] || []) if (m in idx && (idx[m] === ci || deltaE(pal[idx[m]], pal[ci]) < minDE)) { ok = false; break; }
          if (ok) { pick = ci; break; }
        }
        if (pick < 0) throw new Error('colour rule: the ' + pal.length + '-colour palette is not enough for ' + id + '; add a clearly distinct colour');
        idx[id] = pick;
      }
    } else {
      /* IQ-05c: with a priority order the plain greedy can paint itself into a corner (the 22
         top-20 colours are packed tightly), so this is a depth-first search in the same order:
         each driver tries its colours in preference order, and when a later driver has none left
         the search goes back to the most recent choice first. Earlier (higher-priority) drivers
         therefore keep their first choice unless nothing else works. Forward check: no choice is
         kept that leaves an uncoloured neighbour with no colour. Deterministic. */
      const n = pal.length, fits = [];
      for (let i = 0; i < n; i++) { fits.push([]); for (let j = 0; j < n; j++) fits[i].push(i !== j && deltaE(pal[i], pal[j]) >= minDE); }
      const nb = order.map(id => [...(adj[id] || [])].map(m => order.indexOf(m)).filter(j => j >= 0));
      const col = new Array(order.length).fill(-1), prefs = order.map(tryOrderOf);
      const allowed = (v, ci) => nb[v].every(j => col[j] < 0 || fits[ci][col[j]]);
      let steps = 0;
      const dfs = v => {
        if (v === order.length) return true;
        if (++steps > 2e6) throw new Error('colour rule: search gave up after 2,000,000 steps');
        for (const ci of prefs[v]) {
          if (!allowed(v, ci)) continue;
          col[v] = ci;
          if (nb[v].every(j => col[j] >= 0 || j < v || prefs[j].some(cj => allowed(j, cj))) && dfs(v + 1)) return true;
          col[v] = -1;
        }
        return false;
      };
      if (!dfs(0)) throw new Error('colour rule: the ' + pal.length + '-colour palette cannot colour every driver; add a clearly distinct colour');
      order.forEach((id, v) => { idx[id] = col[v]; });
    }
    for (const e of race.entrants) if (!(e.id in idx)) idx[e.id] = 0;
    const used = new Set(order.map(id => idx[id])).size;
    return { index: idx, used, sets, fadeRaces: W, minDeltaE: minDE, rows, priorityTop: [...top], bright };
  }

  /* IQ-05c event label: the Grand Prix as drawn next to a winner's value ("Portuguese GP").
     "Grand Prix" -> "GP" wherever it appears; a race without those words (the Indianapolis 500)
     keeps its name. Everything else is races.csv's grand_prix exactly. */
  function gpShort(name) { return String(name).replace(/Grand Prix/g, 'GP'); }

  const api = { build, buildSeries, shareRace, pchip, seriesFrame, isLive, statusAt, eventAt, rankOf, assignColours, coVisible, drawnColour, deltaE, lab, gpShort, rateText };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.RTT_TIMELINE = api;
})(typeof window !== 'undefined' ? window : this);
