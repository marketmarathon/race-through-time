/* RTT-001 player tests (IQ-13, design pilot 1). Same method as run_tests_rtt003.js: every frame of each pilot clip and
 * of the four option configs (as built, A, B, C; the whole film, 1994-2026) is drawn in order through the kit's own
 * driver path (kits/rtt-002/rtt.js openPlayer) at 1920 x 1080, and what was drawn (window.__LABELS, __BARS, __RANK,
 * __PICS, __CROWN, __CALLOUT, __SOURCE, __MARKER, __NOTE) is checked against data/rtt-001/*.csv, read HERE,
 * independently of the adapter and of rtt_timeline.js:
 *
 *   0. the data is untouched (DEC-167): series.csv's SHA-256 equals the build manifest's
 *   1. date line: exactly one per frame, "<Month YYYY>" of a month end in series.csv, never going backwards
 *   2. no bar where series.csv has no value: on a month-end frame every drawn bar has a value that month and the
 *      board holds min(10, browsers with a value) bars; between month ends a bar has a value in the month counted
 *      towards or the one before (a browser that stops fades out, one that starts fades in)
 *   3. values at data points: as built, every drawn value on a month-end frame equals series.csv exactly. Smoothed
 *      (A, B, C): from January 2009 every value equals series.csv; before 2009 a value equals series.csv at every
 *      published figure (observed or arithmetic) outside a hand-over window; inside a window (recomputed here from
 *      handover_order.csv: 12 months centred on the hand-over, or the whole gap if longer, never past January 2009)
 *      it stays within the published figures and series values of that stretch (including both sources' boundary
 *      months); elsewhere it stays between the two
 *      published figures its series row rests on. Labels: one decimal (or two, values.decimals) rounded half up from
 *      the drawn hundredths; with values.approx every estimated value reads "~N%" (whole percent, half up) or "<1%"
 *   4. counting: between month ends a value stays between its two month-end values, and the label follows it
 *   5. order: on every frame no row above one with a larger value
 *   6. estimated look: every bar before January 2009 has the estimated style, every bar from 2009 the official one
 *   7. source line: on every frame exactly the month's source as series.csv names it (as built), or "changing from X
 *      to Y" inside a smoothed window, ending " · estimated" exactly before January 2009
 *   8. "New source" marker (option C): exactly from the first frame of each month whose source line first names a new
 *      source, for marker.sec; never with the marker off
 *   9. dated note (when notes_at is set): exactly for note_line.sec from the first frame of its month
 *  10. crown on the leader's bar on every frame (when on); callouts only at the leader changes whose month is a
 *      published figure for both browsers (leaders.csv: October 1998, May 2012) plus the configured extra moments
 *  11. logos (owner directions DEC-180, DEC-182): every drawn bar of a browser listed in pictures.files has its logo on a
 *      tile on its row, inside the tile and left of the bar; a browser in pictures.own has our own neutral tile; any
 *      other browser has none (name only)
 *  12. layout: no label outside the frame; the source line, marker, note and callout overlap no title, date line,
 *      axis number or the RTT logo box
 *  13. pacing: each month counts over 0.8-1.4 x its base (the config's sec_per_event, or a segment's), a dated leader
 *      change then holds record_hold.sec
 *  14. colours: one colour per browser on every frame; no two browsers on the board in the same month or the three
 *      before closer than CIEDE2000 18 (DEC-023)
 *  15. smoothing never moves a change of first place: the leaders on the month-end frames change exactly as in
 *      leaders.csv, except where a flagged stretch is smoothed on purpose (include_flagged), which is reported
 *  17. date block and era picture (date/era round, DEC-214/DEC-215, when configured): the date is read from the
 *      date block (month and year labels; check 1 applies to it); the date block and the era picture stay inside the
 *      frame above the footer, and no bar, name, value, logo tile, crown, source line or footer overlaps them
 *  16. board size (IQ-13 answers, DEC-188/DEC-202): one name size and one value size on every frame, and the bars'
 *      left edge never moves; every bar inside the slots is drawn whole inside the board, and no bar on the board stops
 *      being drawn for lack of room (a row gliding up into the last slot from below is cut by the board's edge, as
 *      always); with board.fit the slots stay
 *      within [min_slots, rows] and never below the bars on the board, are exactly rows while ten browsers are on it,
 *      and change smoothly (at most 0.2 slots and a change of speed of at most 0.012 slots from one frame to the
 *      next, so no jump and no sudden start or stop)
 * Placeholder RTT logo and browser logos (plain shapes, written at run time into tests/output/, never committed). Results:
 * tests/player/RESULTS_RTT001.md. Exit 1 on any failure.
 *
 *   node tests/player/run_tests_rtt001.js [case ...]
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..', '..');
const KIT = path.join(ROOT, 'kits', 'rtt-002');
const DATA = path.join(ROOT, 'data', 'rtt-001');
const rtt = require(path.join(KIT, 'rtt.js'));
const TLJS = require(path.join(KIT, 'rtt_timeline.js'));
const { placeholderPNG, logoPlaceholders } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';
const OUT = path.join(ROOT, 'tests', 'output', 'rtt001');
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const SC = '2009-01-31';

function readCSV(file) {
  const text = fs.readFileSync(file, 'utf8'), rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (q) { if (ch === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += ch; }
    else if (ch === '"') q = true; else if (ch === ',') { row.push(f); f = ''; }
    else if (ch === '\n') { row.push(f); rows.push(row); row = []; f = ''; } else if (ch !== '\r') f += ch;
  }
  if (f || row.length) { row.push(f); rows.push(row); }
  const head = rows.shift();
  return rows.filter(r => r.length === head.length).map(r => Object.fromEntries(r.map((v, i) => [head[i], v])));
}
const monthText = iso => MONTHS[+iso.slice(5, 7) - 1] + ' ' + iso.slice(0, 4);
const hund = s => { const [a, b = ''] = s.split('.'); return parseInt(a, 10) * 100 + parseInt((b + '00').slice(0, 2), 10); };   // exact
const day = iso => Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10)) / 864e5;
function pctText(u, est, V) {
  if (V.approx && est) { const w = Math.floor((u + 50) / 100); return w >= 1 ? '~' + w + '%' : '<1%'; }
  if (V.decimals === 2) return Math.floor(u / 100) + '.' + String(u % 100).padStart(2, '0') + '%';
  const t = Math.floor((u + 5) / 10); return Math.floor(t / 10) + '.' + (t % 10) + '%';
}
const overlap = (a, b, gap = 0) => a.x < b.x + b.w + gap && b.x < a.x + a.w + gap && a.y < b.y + b.h + gap && b.y < a.y + a.h + gap;
const labelBox = l => ({ x: l.x, y: l.y - (l.asc || l.size * 0.75), w: l.w, h: (l.asc || l.size * 0.75) + (l.desc || l.size * 0.25) });

/* ---- independent expectations from data/rtt-001 ---- */
const manifest = JSON.parse(fs.readFileSync(path.join(DATA, 'manifest.json'), 'utf8'));
const seriesHash = crypto.createHash('sha256').update(fs.readFileSync(path.join(DATA, 'series.csv'))).digest('hex');
const dataUntouched = manifest.sha256['series.csv'] === seriesHash;
const series = readCSV(path.join(DATA, 'series.csv'));
const obsVal = {}; for (const o of readCSV(path.join(DATA, 'observations.csv'))) if (o.used === 'yes') obsVal[o.obs_id] = o.value_text;
const byM = {}, monthSrc = {};
for (const r of series) {
  if (!r.share) continue;
  (byM[r.date] = byM[r.date] || {})[r.browser_id] = r;
  monthSrc[r.date] = { line: r.source_line, id: r.source_id };
}
const months = Object.keys(byM).sort();
const handovers = readCSV(path.join(DATA, 'handover_order.csv')).filter(r => r.kind === 'hand-over')
  .map(r => { const [from, to] = r.sources.split('>'); return { from, to, t_o: r.from, t_i: r.to, flagged: r.flag.startsWith('FLAG') }; });
const leaders = readCSV(path.join(DATA, 'leaders.csv'));
const datedLeaders = leaders.filter(l => l.previous_leader && ['observed', 'arithmetic'].includes(l.provenance) && l.handover === 'no');
function windowsFor(S) {
  if (!S || S.mode !== 'eased') return [];
  const half0 = (S.handover_months || 12) * 365.25 / 24, sc = day(SC);
  return handovers.filter(h => !h.flagged || S.include_flagged).map(h => {
    const to = day(h.t_o), ti = day(h.t_i), c = (to + ti) / 2, half = Math.max(half0, (ti - to) / 2);
    let a = c - half, b = c + half; if (b > sc) { a -= b - sc; b = sc; }
    return Object.assign({ a, b, months: months.filter(m => day(m) >= a && day(m) <= b && m < SC) }, h);
  });
}

async function runCase(name, configFile, overrides) {
  let cfg = rtt.loadConfig('../rtt-001/' + configFile);
  if (overrides) cfg = require(path.join(ROOT, 'kits', 'rtt-001', 'render_stills.js')).merge(cfg, overrides);
  const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
  const dir = path.join(OUT, '_assets'); fs.mkdirSync(dir, { recursive: true });
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  const withLogo = new Set(logoPlaceholders(cfg, dir)), own = new Set(Object.keys((cfg.pictures && cfg.pictures.own) || {}));
  process.env.RTT_LOCAL_ASSETS = dir;
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
  delete process.env.RTT_LOCAL_ASSETS;
  const info = await pg.evaluate(() => ({ start: TL.startFrame, raceFrames: RACE_FRAMES, dates: TL.events.map(e => e.date), opening: TL.openingEvent.date,
                                          qend: TL.quarterEndFrame, hold: TL.hold }));
  const V = Object.assign({ decimals: 1, approx: false }, cfg.values || {});
  const S = cfg.smoothing || {}, SMOOTH = S.mode === 'eased', W = windowsFor(S);
  const inWin = m => W.find(w => w.months.includes(m));
  const SL = cfg.source_line, MK = cfg.marker && cfg.marker.enabled ? Object.assign({ sec: 3.0 }, cfg.marker) : null;
  const NL = Object.assign({ sec: 3.0 }, cfg.note_line || {}), notes = cfg.notes_at || [];
  const res = { name, config: configFile, frames: info.raceFrames, months: info.dates.length, opening: info.opening, last: info.dates[info.dates.length - 1],
                failures: [], counts: { exact: 0, window: 0, between: 0, approx: 0, counting: 0, enter_leave: 0, est: 0, off: 0, markers: 0, notes: 0, crown: 0, callout: 0, pics: 0, nameOnly: 0, own: 0 },
                maxOff: 0, maxOffAt: '', callouts: [], leaderChanges: [], lastLeader: null, markerMonths: [], minDE: 1e9, minPair: '',
                slots: { min: 1e9, max: 0, step: 0, accel: 0 }, sizes: { name: new Set(), value: new Set(), x0: new Set() } };
  const fail = m => { if (res.failures.length < 40) res.failures.push(m); };
  if (!dataUntouched) fail('series.csv differs from the build manifest (the data must not change, DEC-167)');
  const logo = (cfg.overlays || []).find(o => o.name === 'logo');
  const kOf = {}; info.dates.forEach((d, k) => { kOf[d] = k; });
  const prevMonth = m => { const i = months.indexOf(m); return i > 0 ? months[i - 1] : null; };
  /* the expected source line and its sources, month by month */
  const nm = id => SL.names[id] || id, sh = id => (SL.short || {})[id] || nm(id);
  const srcOf = m => { const w = SMOOTH && m < SC && inWin(m); if (w) return [w.from, w.to]; return monthSrc[m].id.split('>'); };
  const lineOf = m => { const w = SMOOTH && m < SC && inWin(m), s = monthSrc[m];
    const t = w ? SL.changing.replace('{from}', sh(w.from)).replace('{to}', sh(w.to)) : s.id.includes('>') ? s.line.charAt(0).toLowerCase() + s.line.slice(1) : nm(s.id) + (SL.measure[s.id] ? ' (' + SL.measure[s.id] + ')' : '');
    return SL.prefix + t + (m < SC ? SL.estimated : ''); };
  const markerMonths = new Set(info.dates.filter((m, k) => { const was = srcOf(k > 0 ? info.dates[k - 1] : info.opening); return srcOf(m).some(x => !was.includes(x)); }));
  const mOfLeader = l => months.find(m => m.startsWith(l.month));
  const wantCallouts = cfg.callout && cfg.callout.enabled ? datedLeaders.filter(l => mOfLeader(l) > info.opening && mOfLeader(l) <= res.last).map(l => mOfLeader(l) + ' ' + l.leader) : [];
  const drawnAt = {};                    // [month][id] = drawn hundredths on the month-end frame
  let prevDate = null; const firstFrameOf = {}; const coTops = [];
  const FIT = cfg.board && cfg.board.fit && cfg.board.fit.enabled ? Object.assign({ min_slots: 5 }, cfg.board.fit) : null, slotsAt = [];
  const BOTTOM = 1080 - 46; const drawnBefore = new Set();
  for (let f = 0; f < info.raceFrames; f++) {
    const X = await pg.evaluate(t => { drawAt(t); return { L: window.__LABELS, B: window.__BARS, R: window.__RANK, P: window.__PICS, CR: window.__CROWN, CO: window.__CALLOUT, SO: window.__SOURCE, MA: window.__MARKER, NO: window.__NOTE, SL: window.__SLOTS, ER: window.__ERA, DB: window.__DATEBLOCK }; }, f / cfg.fps);
    const DBK = cfg.date_block && cfg.date_block.enabled;
    // (option B draws the date on both devices while they crossfade: the more visible one is read; both name the same month)
    const top1 = arr => arr.length ? arr.reduce((m, l) => (l.alpha > m.alpha ? l : m)) : null;
    const dl = DBK ? (() => { const mo = X.L.filter(l => l.kind === 'date_month'), yr = X.L.filter(l => l.kind === 'date_year');
      if (new Set(mo.map(l => l.text)).size > 1 || new Set(yr.map(l => l.text)).size > 1) return [{ text: 'two different dates' }];
      return mo.length && yr.length ? [{ text: top1(mo).text + ' ' + top1(yr).text }] : []; })() : X.L.filter(l => l.kind === 'time_line');
    // 17. date block and era picture: inside the frame above the footer, overlapping nothing on the board
    if (DBK || (cfg.era && cfg.era.enabled)) {
      const boxes = X.DB && X.DB.box ? [X.DB.box] : [];      // the date block's own area (the rolling year is clipped to it)
      if (X.ER) boxes.push(X.ER.box);
      const foot = X.L.find(l => l.kind === 'footer'), footTop = foot ? labelBox(foot).y : 1080;
      for (const b of boxes) { if (b.x < 0 || b.x + b.w > 1920 || b.y < 0 || b.y + b.h > footTop) fail(`f${f}: date/era box ${JSON.stringify(b)} outside the frame or into the footer`);
        for (const r of X.B.filter(r => r.alpha > 0.01)) if (overlap(b, r.rect)) fail(`f${f}: ${r.id}'s bar overlaps the date/era area`);
        for (const l of X.L.filter(l => ['name', 'value', 'source_line', 'marker', 'note_line', 'axis', 'title'].includes(l.kind) && l.alpha > 0.01)) if (overlap(b, labelBox(l))) fail(`f${f}: ${l.kind} "${l.text}" overlaps the date/era area`);
        for (const pc of X.P.filter(pc => pc.alpha > 0.01)) if (overlap(b, pc.box)) fail(`f${f}: ${pc.id}'s logo tile overlaps the date/era area`);
        if (X.CR && overlap(b, X.CR)) fail(`f${f}: the crown overlaps the date/era area`); }
      res.counts.dateEra = (res.counts.dateEra || 0) + 1;
    }
    if (dl.length !== 1) { fail(`f${f}: ${dl.length} date lines`); continue; }
    const q = months.find(m => monthText(m) === dl[0].text);
    if (!q) { fail(`f${f}: date line "${dl[0].text}" is not a month of the data`); continue; }
    if (prevDate && q < prevDate) fail(`f${f}: date went backwards ${prevDate} -> ${q}`);
    if (q !== prevDate) firstFrameOf[q] = f;
    const k = kOf[q], atEnd = k == null || f >= info.qend[k];
    const pq = k == null ? q : (k > 0 ? info.dates[k - 1] : info.opening);
    const vis = X.B.filter(b => b.alpha > 0 && b.y <= 9.5);
    const lab = {}; for (const l of X.L.filter(l => l.kind === 'value')) lab[l.id] = l;
    // 2. bars only where the data has a value
    for (const b of vis) {
      if (atEnd && !byM[q][b.id]) fail(`f${f} ${q}: ${b.id} drawn on the month end with no series.csv value`);
      if (!atEnd && !byM[q][b.id] && !(byM[pq] || {})[b.id]) fail(`f${f} ${q}: ${b.id} drawn with no value in ${pq} or ${q}`);
      if (b.enter_leave) res.counts.enter_leave++;
    }
    if (atEnd && f === info.qend[k]) {
      if (X.R.length !== Math.min(cfg.rows, Object.keys(byM[q]).length)) fail(`f${f} ${q}: ${X.R.length} bars on the board, data has ${Object.keys(byM[q]).length}`);
      for (const id of X.R) if (!byM[q][id]) fail(`f${f} ${q}: ${id} on the board with no series.csv value`); }
    // 3-4. values
    for (const b of vis) {
      const r = byM[q][b.id] || (byM[pq] || {})[b.id], est = q < SC || (pq < SC && !byM[q][b.id]);
      const l = lab[b.id];
      if (!l) { fail(`f${f}: ${b.id} has no value label`); continue; }
      if (!Number.isInteger(b.units)) fail(`f${f}: ${b.id} drawn value ${b.units} is not whole hundredths`);
      if (l.text !== pctText(b.units, b.style === 'estimated', V)) fail(`f${f} ${q}: ${b.id} label "${l.text}" for drawn ${b.units}`);
      if (V.approx && b.style === 'estimated') res.counts.approx++;
      // 6. estimated look
      if ((b.style === 'estimated') !== est) fail(`f${f} ${q}: ${b.id} style ${b.style} in ${q}`);
      if (atEnd && byM[q][b.id]) {
        const want = hund(r.share), w = SMOOTH && q < SC && inWin(q);
        (drawnAt[q] = drawnAt[q] || {})[b.id] = b.units;
        if (!SMOOTH || q >= SC || (!w && ['observed', 'arithmetic'].includes(r.provenance))) {
          if (b.units !== want) fail(`f${f} ${q}: ${b.id} drawn ${b.units}, series.csv ${want} (must be exact here)`);
          if (V.approx && q < SC ? l.text !== pctText(want, true, V) : l.text !== pctText(want, false, V)) fail(`f${f} ${q}: ${b.id} label "${l.text}" != series.csv ${r.share}`);
          res.counts.exact++;
        } else {
          let lo, hi;
          if (w) { const vs = [];
            for (const m of w.months.concat(months.filter(m => m.slice(0, 7) === w.t_i.slice(0, 7) || m.slice(0, 7) === w.t_o.slice(0, 7)))) { const rr = byM[m][b.id]; if (!rr) continue; vs.push(hund(rr.share)); for (const p of [rr.left_point, rr.right_point]) if (obsVal[p]) vs.push(hund(obsVal[p].replace(',', '.'))); }
            lo = Math.min(...vs); hi = Math.max(...vs); res.counts.window++; }
          else { const a = hund(obsVal[r.left_point].replace(',', '.')), z = hund(obsVal[r.right_point].replace(',', '.')); lo = Math.min(a, z); hi = Math.max(a, z); res.counts.between++; }
          if (b.units < lo - 1 || b.units > hi + 1) fail(`f${f} ${q}: ${b.id} drawn ${b.units} outside ${lo}..${hi}${w ? ' (window ' + w.from + '>' + w.to + ')' : ''}`);
          const off = Math.abs(b.units - want); if (off > res.maxOff) { res.maxOff = off; res.maxOffAt = `${b.id} ${q}: drawn ${b.units / 100}, series.csv ${r.share}`; }
          if (off) res.counts.off++;
        }
      } else if (!atEnd && byM[q][b.id] && (byM[pq] || {})[b.id] && drawnAt[pq] && drawnAt[pq][b.id] != null && !b.enter_leave) {
        res.counts.counting++;            // counting: between the previous month end as drawn and this month's value
        const a = drawnAt[pq][b.id], z = SMOOTH ? null : hund(byM[q][b.id].share);
        if (z != null && (b.units < Math.min(a, z) || b.units > Math.max(a, z))) fail(`f${f} ${q}: ${b.id} counted ${b.units} outside ${a}..${z}`);
      }
    }
    // 5. order
    const uOf = {}; for (const b of X.B) uOf[b.id] = b.units;
    for (let i = 1; i < X.R.length; i++) if (uOf[X.R[i]] > uOf[X.R[i - 1]]) fail(`f${f}: ${X.R[i]} above ${X.R[i - 1]} with a larger value`);
    // 7. source line
    const want = lineOf(q);
    if (!X.SO || X.SO.text !== want) fail(`f${f} ${q}: source line "${X.SO && X.SO.text}" != "${want}"`);
    // 8. marker
    const mOn = MK && [...markerMonths].some(m => firstFrameOf[m] != null && f >= firstFrameOf[m] && f < firstFrameOf[m] + Math.round(MK.sec * cfg.fps));
    if (!!X.MA !== !!mOn && !(X.MA && X.MA.alpha === 0)) fail(`f${f} ${q}: marker ${X.MA ? 'shown' : 'not shown'}, expected ${mOn ? 'shown' : 'not'}`);
    if (X.MA) { res.counts.markers++; if (!res.markerMonths.includes(X.MA.date)) res.markerMonths.push(X.MA.date); }
    // 9. note
    const nOn = notes.some(n => firstFrameOf[n.date] != null && f >= firstFrameOf[n.date] && f < firstFrameOf[n.date] + Math.round(NL.sec * cfg.fps));
    if (!!X.NO !== nOn && !(X.NO && X.NO.alpha === 0)) fail(`f${f} ${q}: note ${X.NO ? 'shown' : 'not shown'}`);
    if (X.NO) res.counts.notes++;
    // 10. crown and callouts
    if (cfg.crown && cfg.crown.enabled) { if (!X.CR || X.CR.id !== X.R[0]) fail(`f${f}: crown on ${X.CR && X.CR.id}, leader ${X.R[0]}`); else res.counts.crown++; }
    else if (X.CR) fail(`f${f}: crown drawn with the crown off`);
    if (X.CO) { res.counts.callout++; const c = info.dates[X.CO.k] + ' ' + X.CO.id; if (!res.callouts.includes(c)) res.callouts.push(c); }
    // 11. pictures
    for (const b of vis) { const p = X.P.find(p => p.id === b.id);
      if (withLogo.has(b.id)) {
        if (!p || !p.tile || !p.drawn) { fail(`f${f}: ${b.id} has no logo`); continue; }
        res.counts.pics++;
        const d = p.drawn, bx = p.box;
        if (d.x < bx.x - 0.5 || d.y < bx.y - 0.5 || d.x + d.w > bx.x + bx.w + 0.5 || d.y + d.h > bx.y + bx.h + 0.5) fail(`f${f}: ${b.id} logo outside its tile`);
        if (Math.abs((bx.y + bx.h / 2) - (b.rect.y + b.rect.h / 2)) > 1) fail(`f${f}: ${b.id} logo off its row`);
        if (bx.x + bx.w > b.rect.x) fail(`f${f}: ${b.id} logo overlaps its bar`);
      } else if (own.has(b.id)) {                 // IQ-13c: our own neutral tile where no real logo exists
        if (!p || !p.own) fail(`f${f}: ${b.id} has no own tile`); else res.counts.own++;
      } else if (p) fail(`f${f}: ${b.id} has a picture but no logo file is listed for it`);
      else { res.counts.nameOnly++; if (own.size) fail(`f${f}: ${b.id} is on the board with no logo or tile (DEC-182: every browser on the board has one)`); } }
    // 12. layout
    for (const l of X.L) if (l.alpha > 0.01 && l.kind !== 'name' && (l.x < 0 || l.x + l.w > 1920)) fail(`f${f}: ${l.kind} "${l.text}" outside the frame`);
    const topL = X.L.filter(l => ['source_line', 'marker', 'note_line', 'callout', 'callout_extra'].includes(l.kind) && l.alpha > 0.01);
    const others = X.L.filter(l => ['axis', 'title', 'time_line'].includes(l.kind));
    for (const a of topL) { for (const b of others) if (overlap(labelBox(a), labelBox(b))) fail(`f${f}: ${a.kind} overlaps ${b.kind} "${b.text}"`);
      if (logo && overlap(labelBox(a), logo, cfg.overlay_gap || 0)) fail(`f${f}: ${a.kind} enters the logo box`); }
    if (X.MA) { const mb = X.MA.box; for (const b of others.concat(topL.filter(l => l.kind !== 'marker'))) if (overlap(mb, labelBox(b))) fail(`f${f}: marker overlaps ${b.kind}`);
      if (logo && overlap(mb, logo, cfg.overlay_gap || 0)) fail(`f${f}: marker enters the logo box`); }
    // 16. board size
    for (const l of X.L) { if (l.kind === 'name') res.sizes.name.add(l.size); if (l.kind === 'value') res.sizes.value.add(l.size); }
    for (const b of vis) res.sizes.x0.add(Math.round(b.rect.x * 100) / 100);
    const sl = X.SL;
    for (const id of X.R) { const b = X.B.find(b => b.id === id);   // (a row gliding up into the last slot from below is cut by the board's edge, as always)
      if (!b) { if (drawnBefore.has(id)) fail(`f${f} ${q}: ${id} was on the board and is no longer drawn (no room)`); continue; }
      if (b.alpha > 0 && b.y <= sl - 1 + 1e-6 && b.rect.y + b.rect.h > BOTTOM + 0.5) fail(`f${f} ${q}: ${id} in slot ${b.y.toFixed(2)} of ${sl.toFixed(2)} drawn below the board (${(b.rect.y + b.rect.h).toFixed(1)} > ${BOTTOM})`); }
    drawnBefore.clear(); for (const b of X.B) if (X.R.includes(b.id)) drawnBefore.add(b.id); slotsAt.push(sl); res.slots.min = Math.min(res.slots.min, sl); res.slots.max = Math.max(res.slots.max, sl);
    if (FIT) {
      if (sl < FIT.min_slots - 1e-9 || sl > cfg.rows + 1e-9) fail(`f${f}: ${sl.toFixed(3)} slots outside ${FIT.min_slots}..${cfg.rows}`);
      if (sl < X.R.length - 1e-9) fail(`f${f} ${q}: ${sl.toFixed(3)} slots for ${X.R.length} bars`);
    } else if (sl !== cfg.rows) fail(`f${f}: ${sl} slots with board.fit off`);
    // 14. colours (collected on month-end frames)
    if (atEnd && k != null && f === info.qend[k]) { if (X.R[0] !== res.lastLeader) { res.leaderChanges.push(q.slice(0, 7) + ' ' + X.R[0]); res.lastLeader = X.R[0]; } }
    if (f === 0) { res.lastLeader = X.R[0]; }
    if (atEnd && k != null && f === info.qend[k]) coTops.push(X.R.map(id => [id, X.B.find(b => b.id === id).colour]));
    prevDate = q;
  }
  await br.close();
  // 16. the slots change smoothly, and are exactly rows wherever ten browsers have been on the board for a whole window
  for (let f = 1; f < slotsAt.length; f++) { const d = Math.abs(slotsAt[f] - slotsAt[f - 1]); res.slots.step = Math.max(res.slots.step, d);
    if (f > 1) res.slots.accel = Math.max(res.slots.accel, Math.abs(slotsAt[f] - 2 * slotsAt[f - 1] + slotsAt[f - 2])); }
  if (res.slots.step > 0.2) fail(`slots change by up to ${res.slots.step.toFixed(3)} per frame (> 0.2)`);
  if (res.slots.accel > 0.012) fail(`slots change speed by up to ${res.slots.accel.toFixed(4)} per frame (> 0.012)`);
  if (FIT && info.dates.some(d => d >= '2009-12-31') && Math.abs(slotsAt[slotsAt.length - 1] - cfg.rows) > 1e-9) fail(`slots ${slotsAt[slotsAt.length - 1]} at the end, want ${cfg.rows}`);
  if (res.sizes.name.size > 1) fail(`name sizes ${[...res.sizes.name].join(', ')} (one size for the whole video)`);
  if (res.sizes.value.size > 1) fail(`value sizes ${[...res.sizes.value].join(', ')}`);
  if (res.sizes.x0.size > 1) fail(`bars start at x ${[...res.sizes.x0].join(', ')} (the left edge must not move)`);
  for (let i = 0; i < coTops.length; i++) {
    const V2 = new Map(); for (let j = Math.max(0, i - 3); j <= i; j++) for (const [id, c] of coTops[j]) { if (V2.has(id) && V2.get(id) !== c) fail(`${id} changes colour`); V2.set(id, c); }
    const a = [...V2]; for (let x = 0; x < a.length; x++) for (let y = x + 1; y < a.length; y++) { const d = TLJS.deltaE(a[x][1], a[y][1]); if (d < res.minDE) { res.minDE = d; res.minPair = a[x][0] + ' / ' + a[y][0]; } }
  }
  if (res.minDE < 18) fail(`colours: ${res.minPair} CIEDE2000 ${res.minDE.toFixed(1)} < 18`);
  // 10. callouts: exactly the dated leader changes (plus configured extra moments) inside the window
  if ((cfg.moments || []).length) { const miss = wantCallouts.filter(c => !res.callouts.includes(c)); if (miss.length) fail(`callouts missing: ${miss.join(', ')}`); }
  else if (res.callouts.slice().sort().join() !== wantCallouts.slice().sort().join()) fail(`callouts [${res.callouts.join(', ')}], expected [${wantCallouts.join(', ')}]`);
  if (!(cfg.callout && cfg.callout.enabled) && res.callouts.length) fail('callouts drawn with callouts off');
  // 8. marker months
  if (MK) { const want = [...markerMonths].filter(m => firstFrameOf[m] != null).sort().join(); if (res.markerMonths.slice().sort().join() !== want) fail(`marker months [${res.markerMonths.join(', ')}], expected [${want}]`); }
  // 15. smoothing never moves a change of first place, except on a flagged stretch smoothed on purpose (DEC-167, DEC-168)
  if (!S.include_flagged) { const want = leaders.filter(l => l.previous_leader && l.month > info.opening.slice(0, 7) && l.month <= res.last.slice(0, 7)).map(l => l.month + ' ' + l.leader).join(', ');
    if (res.leaderChanges.join(', ') !== want) fail(`changes of first place [${res.leaderChanges.join(', ')}], leaders.csv [${want}]`); }
  // 13. pacing
  const P = cfg.pacing, base = d => { for (const s of P.segments || []) if ((s.to == null || d <= s.to) && (s.from == null || d >= s.from)) return s.sec_per_event; return P.sec_per_event; };
  for (let i = 0; i < info.dates.length; i++) {
    const d = info.dates[i], cnt = info.qend[i] - firstFrameOf[d] + 1;
    if (firstFrameOf[d] == null) { fail(`${d} never shown`); continue; }
    const lo = Math.round(base(d) * 0.8 * cfg.fps) - 1, hi = Math.round(base(d) * 1.4 * cfg.fps) + 1;
    if (cnt < lo || cnt > hi) fail(`${d}: counts over ${cnt} frames, outside ${lo}-${hi}`);
    if (i + 1 < info.dates.length) { const n = firstFrameOf[info.dates[i + 1]] - firstFrameOf[d], held = cfg.record_hold && cfg.record_hold.enabled && datedLeaders.some(l => d.startsWith(l.month));
      const wantN = cnt + (held ? Math.round(cfg.record_hold.sec * cfg.fps) : 0); if (Math.abs(n - wantN) > 1) fail(`${d}: beat ${n} frames, want ${wantN}`); }
  }
  res.pass = res.failures.length === 0;
  return res;
}

function write(results) {
  const L = ['# RTT-001 player test results (IQ-13 design pilot 1; IQ-13 answers: the approved choices and the board-size option)', '',
    'Written by `node tests/player/run_tests_rtt001.js`. Every frame drawn in order at 1920 x 1080 in Playwright Chromium through `kits/rtt-002/rtt.js` (the same path as the render). Expected values read independently from `data/rtt-001/` (series.csv, observations.csv, handover_order.csv, leaders.csv, manifest.json). The checks are listed at the top of the test file.', '',
    `Data untouched: series.csv SHA-256 ${seriesHash} ${dataUntouched ? '= the build manifest' : '**differs from the build manifest**'}.`, '',
    `Overall: ${results.filter(r => r.pass).length}/${results.length} PASS.`, '',
    '| Case | Result | Config | Months (opening → last) | Frames | Month-end values exact / in a hand-over window / between their two figures | Counting values checked | "~" labels | Smoothed values that differ from series.csv (largest difference) | Enter/leave bar-frames | Source markers (months) | Note frames | Crown frames | Callouts | Logos / own tiles / name-only bar-frames | Closest colours (CIEDE2000) | Changes of first place (month-end frames) | Board slots min–max (largest change / change of speed per frame) |',
    '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|'];
  for (const r of results) L.push(`| ${r.name} | ${r.pass ? 'PASS' : 'FAIL'} | \`${r.config}\` | ${r.months} (${r.opening} → ${r.last}) | ${r.frames} (${(r.frames / 30).toFixed(1)} s) | ${r.counts.exact} / ${r.counts.window} / ${r.counts.between} | ${r.counts.counting} | ${r.counts.approx} | ${r.counts.off}${r.maxOff ? ' (' + (r.maxOff / 100).toFixed(2) + ' points: ' + r.maxOffAt + ')' : ''} | ${r.counts.enter_leave} | ${r.counts.markers} (${r.markerMonths.join(', ') || 'none'}) | ${r.counts.notes} | ${r.counts.crown} | ${r.callouts.join('; ') || 'none'} | ${r.counts.pics} / ${r.counts.own} / ${r.counts.nameOnly} | ${r.minDE === 1e9 ? 'n/a' : r.minDE.toFixed(1) + ' (' + r.minPair + ')'} | ${r.leaderChanges.join(', ') || 'none'} | ${r.slots.min === r.slots.max ? r.slots.min : r.slots.min.toFixed(2) + '–' + r.slots.max.toFixed(2) + ' (' + r.slots.step.toFixed(3) + ' / ' + r.slots.accel.toFixed(4) + ')'} |`);
  for (const r of results) if (!r.pass) { L.push('', `**${r.name} failures** (first 40):`); for (const f of r.failures) L.push('- ' + f); }
  L.push('');
  fs.writeFileSync(path.join(__dirname, 'RESULTS_RTT001.md'), L.join('\n'));
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const clips = fs.readFileSync(path.join(ROOT, 'kits', 'rtt-001', 'clips.txt'), 'utf8').split('\n').filter(Boolean);
  const cases = clips.map(c => [c.replace(/^config_rtt001_clip_|\.json$/g, ''), c])
    .concat([['film_as_built', 'config_rtt001_film.json'], ['film_option_A', 'config_rtt001_opt_A.json'], ['film_option_B', 'config_rtt001_opt_B.json'],
             ['film_option_C', 'config_rtt001_opt_C.json'],
             ['film_option_C_note_crown_callouts', 'config_rtt001_opt_C.json', { notes_at: [{ date: '1996-06-30', text: 'Note: until May 1996 this source counted Internet Explorer inside “Mosaic”' }], crown: { enabled: true }, callout: { enabled: true }, record_hold: { enabled: true } }],
             ['film_approved_fixed_slots', 'config_rtt001_approved.json'], ['film_approved_board_fit', 'config_rtt001_approved_fit.json'],
             ['film_era_A', 'config_rtt001_era_A.json'], ['film_era_B', 'config_rtt001_era_B.json']])
    .filter(c => process.argv.length <= 2 || process.argv.slice(2).includes(c[0]));
  const results = [];
  for (const [n, c, o] of cases) { const t0 = Date.now(); const r = await runCase(n, c, o); results.push(r);
    console.log(`${r.pass ? 'PASS' : 'FAIL'} ${n}: ${r.frames} frames in ${((Date.now() - t0) / 1000).toFixed(0)} s` + (r.pass ? '' : '\n  ' + r.failures.slice(0, 8).join('\n  '))); }
  if (process.argv.length <= 2) write(results);
  process.exit(results.every(r => r.pass) ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
