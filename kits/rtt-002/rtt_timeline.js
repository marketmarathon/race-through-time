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
    const events = [], states = [];
    for (const ev of race.events) {
      if (ev.date > to) break;
      for (const c of ev.credits) {
        const now = (totals[c.id] || 0) + 1;
        if (now !== c.total) throw new Error('event ' + ev.race_index + ': ' + c.id + ' total ' + c.total + ' but counted ' + now);
        totals[c.id] = now;
        reached[c.id] = c.credit_index;          // when this driver reached this total
      }
      const s = snapshot(totals, reached);
      if (ev.date < from) { opening = s; openingEvent = ev; continue; }
      events.push(ev); states.push(s);
    }
    if (!events.length) throw new Error('no events inside the window ' + from + ' .. ' + to);

    /* Pacing. An event that reorders or changes who is on the visible board gets the long
       beat; one that only moves a visible bar gets the normal beat; one nobody can see, or
       the (settled_run_after+1)th visible-but-unchanged event in a row, gets the short beat.
       That is what "quiet stretches compress" means here. */
    const mult = [], kind = [];
    let prev = opening, settled = 0;
    for (let k = 0; k < events.length; k++) {
      const a = prev.order.slice(0, rows), b = states[k].order.slice(0, rows);
      const credited = events[k].credits.map(c => c.id);
      let kd;
      if (!sameList(a, b)) { kd = 'rank_change'; settled = 0; }
      else if (credited.some(id => b.includes(id))) { settled++; kd = settled > P.settled_run_after ? 'quiet' : 'visible_change'; }
      else { settled++; kd = 'quiet'; }
      kind.push(kd); mult.push(P.mult[kd]);
      prev = states[k];
    }

    const startFrame = [];
    let sec = P.lead_in_sec;
    for (let k = 0; k < events.length; k++) {
      startFrame.push(Math.round(sec * fps));
      sec += P.sec_per_event * mult[k];
    }
    sec += P.end_hold_sec;
    const raceFrames = Math.round(sec * fps);
    for (let k = 1; k < startFrame.length; k++)
      if (startFrame[k] <= startFrame[k - 1]) throw new Error('two events share a frame; raise sec_per_event');

    return { events, states, opening, openingEvent, startFrame, raceFrames, mult, kind, fps, rows };
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

  const api = { build, eventAt, rankOf };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.RTT_TIMELINE = api;
})(typeof window !== 'undefined' ? window : this);
