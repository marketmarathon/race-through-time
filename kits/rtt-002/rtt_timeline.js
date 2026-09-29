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

  const api = { build, eventAt, rankOf, assignColours, coVisible, drawnColour, deltaE, lab, gpShort, rateText };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.RTT_TIMELINE = api;
})(typeof window !== 'undefined' ? window : this);
