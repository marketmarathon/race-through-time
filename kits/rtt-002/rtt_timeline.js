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
 */
(function (root) {
  'use strict';

  function rankOf(totals, reached) {
    const ids = Object.keys(totals).filter(id => totals[id] > 0);
    ids.sort((a, b) => (totals[b] - totals[a]) || (reached[a] - reached[b]));
    return ids;
  }

  function snapshot(totals, reached) {
    const order = rankOf(totals, reached);
    const tot = {};
    for (const id of order) tot[id] = totals[id];
    return { order, totals: tot };
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
    if (race.schema !== 'rtt-race/1') throw new Error('race file schema is ' + race.schema + ', expected rtt-race/1');
    const fps = cfg.fps, rows = cfg.rows, P = cfg.pacing;
    checkPacing(P);
    const from = (cfg.window && cfg.window.from) || '0000-00-00';
    const to   = (cfg.window && cfg.window.to)   || '9999-99-99';

    const totals = {}, reached = {};
    let opening = snapshot(totals, reached), openingEvent = null;
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
      const s = snapshot(totals, reached);
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

    return { events, states, opening, openingEvent, startFrame, raceFrames, mult, kind, fps, rows, colours, hold, records, highlight };
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
    const order = Object.keys(first).sort((a, b) => (first[a][0] - first[b][0]) || (first[a][1] - first[b][1]));
    const idx = {};
    for (const id of order) {
      let ci = 0;
      for (; ci < pal.length; ci++) {
        let ok = true;
        for (const m of adj[id] || []) if (m in idx && (idx[m] === ci || deltaE(pal[idx[m]], pal[ci]) < minDE)) { ok = false; break; }
        if (ok) break;
      }
      if (ci === pal.length) throw new Error('colour rule: the ' + pal.length + '-colour palette is not enough for ' + id + '; add a clearly distinct colour');
      idx[id] = ci;
    }
    for (const e of race.entrants) if (!(e.id in idx)) idx[e.id] = 0;
    const used = Math.max(...order.map(id => idx[id])) + 1;
    return { index: idx, used, sets, fadeRaces: W, minDeltaE: minDE, rows };
  }

  const api = { build, eventAt, rankOf, assignColours, coVisible, drawnColour, deltaE };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.RTT_TIMELINE = api;
})(typeof window !== 'undefined' ? window : this);
