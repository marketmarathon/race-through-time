/* Player tests: the six stress fixtures, an RTT-002 slice (1984-1989), the two IQ-05 pilots
 * (2014-2021, normal and fast pace) and a colour check over the whole RTT-002 run.
 *
 * For each case:
 *   1. scripts/rtt_adapter.py turns the CSVs into the player's input (as production does)
 *   2. the EXPECTED board after every race is computed here, independently, straight from
 *      win_credits.csv (career_wins_after, and credit order for ties) - not from the adapter's
 *      output and not from rtt_timeline.js
 *   3. the player is opened through the kit's own driver path (rtt.js openPlayer) at 1920
 *      preview width, and EVERY race frame is drawn in order (the rank glide is stateful)
 *   4. on every frame, the text the player drew is checked (draw-call log, window.__LABELS):
 *        - every value label is "<whole number> win(s)" and equals the expected count for that
 *          driver after the race the frame is showing
 *        - the race the frame shows (time label: season, Grand Prix, date) matches races.csv
 *        - the target order of the visible rows is the expected order (tie rule included)
 *        - axis labels are whole numbers; every label lies inside the 1920x1080 frame
 *        - races are shown in order, each for at least one frame, and a count never changes
 *          except on the first frame of a race
 *   5. at EVENT BOUNDARIES (the first and last frame of every race) the frame is saved as a PNG
 *      and, when tesseract is installed, every value label is cut out of the PNG and read back by
 *      OCR, so the pixels are checked as well as the draw calls
 *   6. fixture-specific expectations from fixture.json
 *
 * Added in IQ-05 (DEC-022):
 *   7. entry visibility: every driver who joins the visible top N must be CLEARLY VISIBLE (row
 *      opacity >= 0.8 with its name and value label drawn) within 8 frames of the first frame
 *      of that race
 *   8. colours, on every drawn frame: no two bars on screen (opacity > 0) share a colour or
 *      are closer than colour_rule.min_delta_e; each driver has one colour, the same in every
 *      case that draws RTT-002 (1984-89, both pilots, the full run)
 *   9. colours, on every race of the full RTT-002 dataset, from win_credits.csv alone: the
 *      drivers in the top N after that race and the fade_races races before it (so rows still
 *      fading out are included) all have different, clearly distinct colours
 *  10. milestones (pilots): Hamilton on 91 level with Schumacher at the 2020 Eifel GP, and
 *      past him at the 2020 Portuguese GP, read from the drawn labels
 *  11. pilots: no closing card, a hold of at least pacing.end_hold_sec on the final board
 *
 * Usage: node tests/player/run_tests.js [case ...]     (needs `npm ci` in kits/rtt-002)
 * Output: tests/output/ (PNGs, gitignored) and tests/player/RESULTS.md
 */
const fs = require('fs');
const path = require('path');
const { execFileSync, spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..', '..');
const KITDIR = path.join(ROOT, 'kits', 'rtt-002');
const rtt = require(path.join(KITDIR, 'rtt.js'));
const OUTDIR = path.join(ROOT, 'tests', 'output');
const FIX = path.join(ROOT, 'tests', 'fixtures');
const HAS_OCR = spawnSync('tesseract', ['--version']).status === 0;
const TIMELINE = require(path.join(KITDIR, 'rtt_timeline.js'));
const ENTRY_MAX_FRAMES = 8;          // DEC-022 (4): clearly visible within 8 frames (0.27 s at 30 fps)
const CLEAR_ALPHA = 0.8;             // "clearly visible": row opacity at least this, labels drawn
const COLOUR_OF = {};                // driver -> drawn colour, across every RTT-002 case

/* ---- a small CSV reader (quoted fields allowed) ---- */
function readCSV(file) {
  const s = fs.readFileSync(file, 'utf8');
  const rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (q) { if (ch === '"') { if (s[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += ch; }
    else if (ch === '"') q = true;
    else if (ch === ',') { row.push(f); f = ''; }
    else if (ch === '\n') { row.push(f); rows.push(row); row = []; f = ''; }
    else if (ch !== '\r') f += ch;
  }
  if (f.length || row.length) { row.push(f); rows.push(row); }
  const head = rows.shift();
  return rows.filter(r => r.length === head.length).map(r => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}

/* ---- expected boards, from win_credits.csv alone ---- */
function expected(dir) {
  const races = readCSV(path.join(dir, 'races.csv'));
  const credits = readCSV(path.join(dir, 'win_credits.csv'));
  const names = Object.fromEntries(readCSV(path.join(dir, 'drivers.csv')).map(d => [d.driver_id, d.display_name]));
  const byRace = {};
  for (const c of credits) (byRace[c.race_index] = byRace[c.race_index] || []).push(c);
  const tot = {}, reached = {}, after = {};
  for (const r of races) {
    for (const c of (byRace[r.race_index] || [])) {
      tot[c.driver_id] = +c.career_wins_after;                  // the data's own count
      reached[c.driver_id] = +c.credit_index;                   // when it reached that count
    }
    const order = Object.keys(tot).sort((a, b) => (tot[b] - tot[a]) || (reached[a] - reached[b]));
    after[r.race_index] = { order, totals: { ...tot }, race: r };
  }
  return { races, after, names };
}

function dateText(iso, months) { const [y, m, d] = iso.split('-').map(Number); return d + ' ' + months[m - 1] + ' ' + y; }

function ocr(png) {
  // one thread: tesseract's own threading only slows it down on crops this small
  const r = spawnSync('tesseract', [png, 'stdout', '--psm', '7', '-l', 'eng'], { encoding: 'utf8', env: Object.assign({}, process.env, { OMP_THREAD_LIMIT: '1' }) });
  return (r.stdout || '').trim();
}

/* (9) The colour rule on every race of the full RTT-002 dataset, from win_credits.csv alone
   (the boards are computed here, not taken from rtt_timeline.js). The colours are the kit's
   assignment (rtt_timeline.js assignColours on the full race file); main() then checks that every
   colour actually DRAWN for a driver in any RTT-002 case is that same colour. */
function colourRuleFullDataset(dir) {
  const cfg = rtt.loadConfig('config.json');
  const data = JSON.parse(fs.readFileSync(path.join(KITDIR, cfg.race_file), 'utf8'));
  const E = expected(dir);
  const W = cfg.colour_rule.fade_races, minDE = cfg.colour_rule.min_delta_e;
  const assigned = TIMELINE.assignColours(data, cfg).index;
  const colour = id => TIMELINE.drawnColour(cfg.palette[assigned[id]]);
  const res = { name: 'colour_rule_full_dataset', events: E.races.length, failures: [], notes: [], max_together: 0, closest: Infinity };
  const fail = m => { if (res.failures.length < 40) res.failures.push(m); };
  const tops = E.races.map(r => E.after[r.race_index].order.slice(0, cfg.rows));
  const onBoard = new Set(tops.flat());
  E.races.forEach((r, k) => {
    const V = [...new Set(tops.slice(Math.max(0, k - W), k + 1).flat())];
    res.max_together = Math.max(res.max_together, V.length);
    for (const a of V) for (const b of V) if (a < b) {
      const d = TIMELINE.deltaE(colour(a), colour(b));
      if (d < res.closest) { res.closest = d; res.closest_pair = `${E.names[a]} / ${E.names[b]}`; }
      if (colour(a) === colour(b)) fail(`race ${r.race_index} (${r.season} ${r.grand_prix}): ${E.names[a]} and ${E.names[b]} share ${colour(a)}`);
      else if (d < minDE) fail(`race ${r.race_index}: ${E.names[a]} and ${E.names[b]} only ${d.toFixed(1)} apart`);
    }
  });
  res.drivers = onBoard.size;
  res.colours_used = new Set([...onBoard].map(colour)).size;
  res.palette = cfg.palette.length;
  res.pass = res.failures.length === 0;
  res.notes.push(`${res.events} races; ${res.drivers} drivers ever reach the top ${cfg.rows}; at most ${res.max_together} can be on screen together (top ${cfg.rows} after a race and the ${W} before it, so rows still fading out count)`);
  res.notes.push(`${res.colours_used} colours used of a ${res.palette}-colour palette; every pair that can be on screen together differs, the closest being ${res.closest_pair} at CIEDE2000 ${res.closest.toFixed(1)} (rule: at least ${minDE})`);
  const byColour = {};
  for (const id of [...onBoard].sort((a, b) => E.races.findIndex(r => E.after[r.race_index].order.slice(0, cfg.rows).includes(a)) - E.races.findIndex(r => E.after[r.race_index].order.slice(0, cfg.rows).includes(b))))
    (byColour[colour(id)] = byColour[colour(id)] || []).push(E.names[id]);
  res.by_colour = byColour;
  res.colour_of = Object.fromEntries([...onBoard].map(id => [id, colour(id)]));
  return res;
}

async function runCase(c) {
  const out = path.join(OUTDIR, c.name);
  fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
  const json = path.join(out, 'race.json');
  const adapter = execFileSync('python3', [path.join(ROOT, 'scripts', 'rtt_adapter.py'), c.dir, json], { encoding: 'utf8' }).trim();
  const data = JSON.parse(fs.readFileSync(json, 'utf8'));
  const cfg = c.config ? rtt.loadConfig(c.config, c.overrides) : rtt.loadConfig('config.json', Object.assign({ window: c.window || { from: null, to: null } }, c.overrides || {}));
  const E = expected(c.dir);
  const inWindow = E.races.filter(r => (!cfg.window.from || r.race_date >= cfg.window.from) && (!cfg.window.to || r.race_date <= cfg.window.to));
  const before = E.races.filter(r => cfg.window.from && r.race_date < cfg.window.from).pop();

  const res = { name: c.name, adapter_sha256: adapter.split(/\s+/)[0], events: inWindow.length, frames: 0,
                boundary_frames: 0, labels_checked: 0, ocr_checked: 0, ocr_skipped_overlap: 0, ocr_mismatch: [], failures: [], notes: [],
                config: c.config || 'config.json', entries: 0, entry_frames_max: 0, colour_frames: 0 };
  const fail = m => { if (res.failures.length < 40) res.failures.push(m); };

  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: process.env.PW_CHROME || '/opt/pw-browsers/chromium' });
  try {
    const info = await pg.evaluate(() => ({ raceFrames: RACE_FRAMES, start: TL.startFrame, kind: TL.kind, mult: TL.mult, namePx: nameSize(), trunc: NAME_TRUNC }));
    const node = rtt.frameTotals(cfg, data);
    if (node.tl.raceFrames !== info.raceFrames) fail(`Node and page disagree on race frames (${node.tl.raceFrames} vs ${info.raceFrames})`);
    res.race_sec = info.raceFrames / cfg.fps; res.name_px = info.namePx; res.name_truncated = info.trunc;
    res.pacing = { rank_change: 0, visible_change: 0, quiet: 0 }; info.kind.forEach(k => res.pacing[k]++);
    const [lo, hi] = cfg.pacing.bounds;
    if (info.mult.some(m => m < lo - 1e-9 || m > hi + 1e-9)) fail('a pacing multiplier is outside ' + cfg.pacing.bounds);

    const bounds = new Set();
    info.start.forEach((s, k) => { bounds.add(s); bounds.add((k + 1 < info.start.length ? info.start[k + 1] : info.raceFrames) - 1); });

    const el = await pg.$('#c');
    let lastIdx = before ? before.race_index : null, seenRaces = [], prevVals = {}, lag = {};
    res.entry_lag_max = 0;
    const outroFrames = Math.round(cfg.fps * Math.min(0.5, cfg.outro_sec));
    /* entries: drivers in the top N after race k but not after the race before it */
    const prevTop = k => (k === 0 ? (before ? E.after[before.race_index].order : []) : E.after[inWindow[k - 1].race_index].order).slice(0, cfg.rows);
    const entering = {};             // driver -> {k, start frame} while waiting to be clearly visible
    const minDE = (cfg.colour_rule && cfg.colour_rule.min_delta_e) || 0;
    for (let f = 0; f < info.raceFrames + outroFrames; f++) {
      const L = await pg.evaluate(t => { drawAt(t); return { labels: window.__LABELS, rank: window.__RANK, ev: window.__EVENT, bars: window.__BARS }; }, f / cfg.fps);
      res.frames++;
      const ri = L.ev.race_index == null ? null : String(L.ev.race_index);
      /* which race is showing, and does the time label say so */
      if (ri !== lastIdx) {
        if (f >= info.raceFrames) fail(`frame ${f}: race changed during the outro`);
        const want = lastIdx == null ? inWindow[0].race_index : String(+lastIdx + 1);
        if (String(ri) !== String(want)) fail(`frame ${f}: showed race ${ri} after ${lastIdx}, expected ${want}`);
        if (!info.start.includes(f)) fail(`frame ${f}: race changed off an event boundary`);
        seenRaces.push(String(ri)); lastIdx = ri;
      }
      const exp = ri != null ? E.after[ri] : { order: [], totals: {} };
      const k = L.ev.k;
      if (k >= 0 && info.start[k] === f)
        for (const id of exp.order.slice(0, cfg.rows)) if (!prevTop(k).includes(id)) { entering[id] = { k, s: f, race: ri }; res.entries++; }
      if (ri != null) {
        const r = exp.race;
        const tl = Object.fromEntries(L.labels.filter(x => x.kind.startsWith('time_')).map(x => [x.kind, x.text]));
        if (tl.time_season !== r.season) fail(`frame ${f}: season label "${tl.time_season}" != ${r.season}`);
        if (tl.time_gp !== r.grand_prix) fail(`frame ${f}: Grand Prix label "${tl.time_gp}" != "${r.grand_prix}"`);
        if (tl.time_date !== dateText(r.race_date, cfg.time_label.months)) fail(`frame ${f}: date label "${tl.time_date}" != ${r.race_date}`);
      }
      /* the visible order */
      const wantRank = exp.order.slice(0, cfg.rows);
      if (JSON.stringify(L.rank) !== JSON.stringify(wantRank)) fail(`frame ${f} (race ${ri}): order ${L.rank.join(',')} != expected ${wantRank.join(',')}`);
      /* every label */
      const vals = {};
      for (const x of L.labels) {
        if (x.alpha > 0 && (x.x < -0.5 || x.x + x.w > 1920.5)) fail(`frame ${f}: ${x.kind} "${x.text}" runs off the frame (x ${x.x.toFixed(1)}, w ${x.w.toFixed(1)})`);
        if (x.kind === 'axis' && !/^\d{1,3}(,\d{3})*$/.test(x.text)) fail(`frame ${f}: axis label "${x.text}" is not a whole number`);
        if (x.kind !== 'value') continue;
        res.labels_checked++;
        const m = /^(\d{1,3}(?:,\d{3})*) (wins|win)$/.exec(x.text);
        if (!m) { fail(`frame ${f}: value label "${x.text}" is not "<whole number> win(s)"`); continue; }
        const n = +m[1].replace(/,/g, '');
        if ((n === 1) !== (m[2] === 'win')) fail(`frame ${f}: "${x.text}" has the wrong unit form`);
        if (exp.totals[x.id] !== n) fail(`frame ${f} (race ${ri}): ${x.id} shows ${n}, data says ${exp.totals[x.id]}`);
        if (!exp.order.slice(0, cfg.rows + 3).includes(x.id)) fail(`frame ${f}: ${x.id} labelled but not in the top ${cfg.rows + 3}`);
        vals[x.id] = n;
      }
      /* a driver in the target top N must carry its label as soon as its bar is on screen. A bar
         climbing from below the board is still sliding in (C2-2's eased rank glide) and fully
         faded for a few frames; that delay is measured, not failed. */
      const bar = Object.fromEntries(L.bars.map(b => [b.id, b]));
      for (const id of wantRank) {
        if (id in vals) { delete lag[id]; continue; }
        if (bar[id] && bar[id].alpha > 0) fail(`frame ${f} (race ${ri}): ${id} is on screen in the top ${cfg.rows} but has no value label`);
        else { lag[id] = (lag[id] || 0) + 1; res.entry_lag_max = Math.max(res.entry_lag_max, lag[id]); }
      }
      for (const id in vals) if (id in prevVals && vals[id] !== prevVals[id] && !info.start.includes(f)) fail(`frame ${f}: ${id} changed ${prevVals[id]}->${vals[id]} between events`);
      /* (7) entry visibility */
      for (const [id, e] of Object.entries(entering)) {
        const clear = bar[id] && bar[id].alpha >= CLEAR_ALPHA && L.labels.some(x => x.kind === 'name' && x.id === id) && (id in vals);
        const late = f - e.s;
        if (clear) { res.entry_frames_max = Math.max(res.entry_frames_max, late); delete entering[id]; }
        else if (late >= ENTRY_MAX_FRAMES || !exp.order.slice(0, cfg.rows).includes(id)) {
          fail(`race ${e.race}: ${id} entered the top ${cfg.rows} on frame ${e.s} but was not clearly visible within ${ENTRY_MAX_FRAMES} frames`);
          delete entering[id];
        }
      }
      /* (8) colours on screen */
      const shown = L.bars.filter(b => b.alpha > 0);
      for (const b of shown) {
        if (c.rtt002) { if (!(b.id in COLOUR_OF)) COLOUR_OF[b.id] = { colour: b.colour, where: c.name };
                        else if (COLOUR_OF[b.id].colour !== b.colour) fail(`frame ${f}: ${b.id} is ${b.colour} here but ${COLOUR_OF[b.id].colour} in ${COLOUR_OF[b.id].where}`); }
        for (const o of shown) if (o.id < b.id) {
          if (o.colour === b.colour) fail(`frame ${f}: ${o.id} and ${b.id} are both on screen in ${b.colour}`);
          else if (TIMELINE.deltaE(o.colour, b.colour) < minDE) fail(`frame ${f}: ${o.id} ${o.colour} and ${b.id} ${b.colour} are on screen together and only ${TIMELINE.deltaE(o.colour, b.colour).toFixed(1)} apart`);
        }
      }
      res.colour_frames++;
      prevVals = vals;
      /* fixture-specific */
      if (c.expect.max_visible != null && Object.keys(vals).length > c.expect.max_visible) fail(`frame ${f}: more than ${c.expect.max_visible} bars`);

      /* event boundaries: keep the frame, and read the value labels back from its pixels */
      if (bounds.has(f) && !c.light) {
        res.boundary_frames++;
        const k = info.start.indexOf(f) >= 0 ? 'first' : 'last';
        const png = path.join(out, `f${String(f).padStart(5, '0')}_race${ri}_${k}.png`);
        await el.screenshot({ path: png });
        if (HAS_OCR && k === 'first') {
          const busy = id => L.bars.some(b => b.id !== id && b.alpha > 0 && Math.abs(b.y - bar[id].y) < 1);
          for (const x of L.labels.filter(x => x.kind === 'value' && x.alpha >= 0.99)) {
            if (busy(x.id)) { res.ocr_skipped_overlap++; continue; }
            const crop = path.join(out, '_crop.png');
            await pg.screenshot({ path: crop, clip: { x: Math.max(0, x.x - 6), y: x.y - x.size * 0.95, width: x.w + 12, height: x.size * 1.35 } });
            const got = ocr(crop).replace(/[^0-9a-z ]/gi, '').replace(/\s+/g, ' ').trim();
            res.ocr_checked++;
            if (got.replace(/ /g, '').toLowerCase() !== x.text.replace(/ /g, '').toLowerCase()) res.ocr_mismatch.push(`frame ${f} ${x.id}: drew "${x.text}", OCR read "${got}"`);
          }
          fs.rmSync(path.join(out, '_crop.png'), { force: true });
        }
      }
    }
    for (const [id, e] of Object.entries(entering)) fail(`race ${e.race}: ${id} entered but was never clearly visible`);
    const wantRaces = inWindow.map(r => r.race_index);
    if (JSON.stringify(seenRaces) !== JSON.stringify(wantRaces)) fail(`races shown ${seenRaces.length} != races in window ${wantRaces.length}`);
    for (const [ri, want] of Object.entries((c.expect.after_race) || {}))
      if (JSON.stringify(E.after[ri].order) !== JSON.stringify(want)) fail(`fixture.json: after race ${ri} expected ${want}, data order ${E.after[ri].order}`);
    if (c.expect.same_frame_step) {
      const r = String(c.expect.same_frame_step), s = info.start[inWindow.findIndex(x => x.race_index === r)];
      const ids = E.races.find(x => x.race_index === r).winner_driver_ids.split(';');
      const a = await pg.evaluate(t => { drawAt(t); return window.__LABELS; }, (s - 1) / cfg.fps);
      const b = await pg.evaluate(t => { drawAt(t); return window.__LABELS; }, s / cfg.fps);
      for (const id of ids) {
        const va = a.find(x => x.kind === 'value' && x.id === id), vb = b.find(x => x.kind === 'value' && x.id === id);
        const na = va ? parseInt(va.text) : 0, nb = parseInt(vb.text);
        if (nb !== na + 1) fail(`shared drive: ${id} did not step by one on frame ${s} (${na} -> ${nb})`);
      }
      res.notes.push(`shared drive at race ${r}: ${ids.join(' and ')} both step on frame ${s}`);
    }
    if (c.expect.enters) {
      const inTop = Object.values(E.after).filter(a => wantRaces.includes(a.race.race_index)).map(a => a.order.slice(0, cfg.rows).includes(c.expect.enters));
      const entered = inTop.indexOf(true), left = inTop.lastIndexOf(true);
      if (entered < 0 || left === inTop.length - 1) fail(`${c.expect.enters} did not both enter and leave the top ${cfg.rows}`);
      else res.notes.push(`${c.expect.enters} enters the top ${cfg.rows} at race ${entered + 1} and leaves after race ${left + 1}`);
    }
    if (c.expect.quiet_from_race) {
      const ks = info.kind.slice(c.expect.quiet_from_race - 1, c.expect.quiet_to_race);
      if (ks.some(k => k !== 'quiet')) fail(`quiet stretch races ${c.expect.quiet_from_race}-${c.expect.quiet_to_race} not all paced quiet: ${ks.join(',')}`);
      const base = inWindow.length * cfg.pacing.sec_per_event;
      res.notes.push(`quiet stretch paced at ${cfg.pacing.mult.quiet}x; events take ${((info.raceFrames / cfg.fps) - cfg.pacing.lead_in_sec - cfg.pacing.end_hold_sec).toFixed(2)} s against ${base.toFixed(2)} s unpaced`);
    }
    /* (10) milestones, read from the drawn labels on the first frame of the race */
    for (const m of (c.expect.milestones || [])) {
      const k = inWindow.findIndex(r => r.season === m.season && r.grand_prix === m.grand_prix);
      if (k < 0) { fail(`milestone: ${m.season} ${m.grand_prix} is not in the passage`); continue; }
      const idOf = nm => Object.keys(E.names).find(id => E.names[id] === nm);
      const got = await pg.evaluate(t => { drawAt(t); return { labels: window.__LABELS, rank: window.__RANK }; }, info.start[k] / cfg.fps);
      const shows = nm => { const x = got.labels.find(l => l.kind === 'value' && l.id === idOf(nm)); return x ? parseInt(x.text.replace(/,/g, '')) : null; };
      const pos = nm => got.rank.indexOf(idOf(nm)) + 1;
      const said = m.show.map(([nm, n]) => `${nm} ${shows(nm)} (P${pos(nm)})`).join(', ');
      if (m.show.some(([nm, n]) => shows(nm) !== n)) fail(`milestone ${m.season} ${m.grand_prix}: expected ${m.show.map(x => x.join(' ')).join(', ')}, drawn ${said}`);
      if (m.order && m.order.some((nm, i) => i > 0 && pos(m.order[i - 1]) >= pos(nm))) fail(`milestone ${m.season} ${m.grand_prix}: order should be ${m.order.join(' ahead of ')}, drawn ${said}`);
      res.notes.push(`${m.season} ${m.grand_prix} (frame ${info.start[k]}): ${said} — ${m.note}`);
    }
    /* (11) no closing card; the final board holds for end_hold_sec */
    if (cfg.outro_sec === 0) {
      const last = info.raceFrames - 1;
      const out = await pg.evaluate(t => { drawAt(t); return window.__LABELS; }, last / cfg.fps);
      if (out.some(x => x.kind.startsWith('outro_'))) fail('closing card drawn although outro_sec is 0');
      const hold = (info.raceFrames - info.start[info.start.length - 1]) / cfg.fps;
      if (hold < cfg.pacing.end_hold_sec) fail(`final board holds ${hold.toFixed(2)} s, less than ${cfg.pacing.end_hold_sec} s`);
      const total = rtt.frameTotals(cfg, data).total;
      res.notes.push(`no closing card; final board on screen ${hold.toFixed(2)} s (last race slot + ${cfg.pacing.end_hold_sec} s hold); FRAME_COUNT_ONLY total ${total} frames = ${(total / cfg.fps).toFixed(1)} s`);
    }
    /* the intro card draws the config title */
    const intro = await pg.evaluate(t => { drawIntro(t); return window.__LABELS; }, 1.5);
    if (!intro.some(x => x.kind === 'intro_title' && x.text === cfg.title)) fail('intro card does not carry the config title');
  } finally { await br.close(); }
  res.pass = res.failures.length === 0;
  return res;
}

async function main() {
  const only = process.argv.slice(2);
  const cases = [];
  for (const name of fs.readdirSync(FIX).filter(n => fs.statSync(path.join(FIX, n)).isDirectory()).sort()) {
    const fx = JSON.parse(fs.readFileSync(path.join(FIX, name, 'fixture.json'), 'utf8'));
    cases.push({ name, dir: path.join(FIX, name), overrides: fx.overrides, expect: fx.expect });
  }
  const RTT002 = path.join(ROOT, 'data', 'rtt-002');
  cases.push({ name: 'rtt002_1984_1989', dir: RTT002, rtt002: true,
               window: { from: '1984-01-01', to: '1989-12-31' }, overrides: {}, expect: {} });
  const milestones = [
    { season: '2020', grand_prix: 'Eifel Grand Prix', show: [['Lewis Hamilton', 91], ['Michael Schumacher', 91]], order: ['Michael Schumacher', 'Lewis Hamilton'],
      note: 'Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)' },
    { season: '2020', grand_prix: 'Portuguese Grand Prix', show: [['Lewis Hamilton', 92], ['Michael Schumacher', 91]], order: ['Lewis Hamilton', 'Michael Schumacher'],
      note: 'Hamilton passes Schumacher' }];
  cases.push({ name: 'rtt002_2014_2021_pilot', dir: RTT002, rtt002: true, config: 'config_pilot_2014_2021.json', expect: { milestones } });
  cases.push({ name: 'rtt002_2014_2021_pilot_fast', dir: RTT002, rtt002: true, config: 'config_pilot_2014_2021_fast.json', expect: { milestones } });
  /* the whole video, every frame, draw-call checks only (no PNGs or OCR: 16,000 frames) */
  cases.push({ name: 'rtt002_full_run', dir: RTT002, rtt002: true, light: true, overrides: {}, expect: {} });
  const run = only.length ? cases.filter(c => only.includes(c.name)) : cases;

  const results = [];
  if (!only.length || only.includes('colour_rule_full_dataset')) results.push(colourRuleFullDataset(path.join(ROOT, 'data', 'rtt-002')));
  for (const c of run) {
    const t0 = Date.now();
    const r = await runCase(c);
    r.seconds = ((Date.now() - t0) / 1000).toFixed(1);
    results.push(r);
    console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}: ${r.events} events, ${r.frames} frames, ${r.labels_checked} value labels, ${r.boundary_frames} boundary PNGs, OCR ${r.ocr_checked - r.ocr_mismatch.length}/${r.ocr_checked}, ${r.seconds} s`);
    for (const m of r.failures) console.log('   - ' + m);
    for (const m of r.ocr_mismatch.slice(0, 10)) console.log('   ocr: ' + m);
  }
  const full = results.find(r => r.name === 'colour_rule_full_dataset');
  if (full) for (const [id, v] of Object.entries(COLOUR_OF))
    if (full.colour_of[id] !== v.colour) { full.failures.push(`${id} drawn ${v.colour} in ${v.where} but assigned ${full.colour_of[id]}`); full.pass = false; }
  if (full) full.notes.push(`${Object.keys(COLOUR_OF).length} drivers drawn in the RTT-002 cases run; each drawn in its assigned colour in every case`);
  if (results[0] && results[0].name === 'colour_rule_full_dataset') {
    const r = results[0];
    console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}: ${r.events} races, ${r.drivers} drivers on the board, up to ${r.max_together} together, ${r.colours_used} colours, closest pair ${r.closest.toFixed(1)}`);
    for (const m of r.failures) console.log('   - ' + m);
  }
  fs.mkdirSync(OUTDIR, { recursive: true });
  fs.writeFileSync(path.join(OUTDIR, 'results.json'), JSON.stringify(results, null, 1));
  if (!only.length) writeReport(results);
  process.exit(results.every(r => r.pass) ? 0 : 1);
}

function writeReport(results) {
  const pw = require(require.resolve('playwright/package.json', { paths: [KITDIR] })).version;
  const L = [];
  const cases = results.filter(r => r.frames != null), col = results.find(r => r.name === 'colour_rule_full_dataset');
  L.push('# Player test results (IQ-05)', '');
  L.push('Written by `node tests/player/run_tests.js` (all cases). Frames are 1920x1080 (preview width), drawn headless in Playwright ' + pw + ' Chromium, every race frame in order.');
  L.push('OCR: ' + (HAS_OCR ? spawnSync('tesseract', ['--version'], { encoding: 'utf8' }).stdout.split('\n')[0] + ' on every value label of the first frame of every race.' : 'NOT AVAILABLE (tesseract not installed); draw-call checks only.'), '');
  L.push(`Overall: ${results.filter(r => r.pass).length}/${results.length} PASS.`, '');
  L.push('| Case | Result | Config | Races | Frames | Race length | Value labels checked | Boundary frames | OCR read back (skipped: overlapping rows) | Top-ten entries | Slowest entry (frames to clearly visible) | Colour-checked frames | Name size | Pacing (rank / visible / quiet) | Adapter output SHA-256 |');
  L.push('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|');
  for (const r of cases)
    L.push(`| ${r.name} | ${r.pass ? 'PASS' : 'FAIL'} | \`${r.config}\` | ${r.events} | ${r.frames} | ${r.race_sec.toFixed(2)} s | ${r.labels_checked} | ${r.boundary_frames || 'not saved'} | ${r.boundary_frames ? `${r.ocr_checked - r.ocr_mismatch.length}/${r.ocr_checked} (${r.ocr_skipped_overlap})` : 'not run'} | ${r.entries} | ${r.entry_frames_max} | ${r.colour_frames} | ${r.name_px}px${r.name_truncated ? ' (truncated)' : ''} | ${r.pacing.rank_change} / ${r.pacing.visible_change} / ${r.pacing.quiet} | \`${r.adapter_sha256.slice(0, 16)}…\` |`);
  L.push('');
  L.push(`Entry rule: a driver joining the visible top N must be clearly visible (row opacity at least ${CLEAR_ALPHA}, name and value label drawn) within ${ENTRY_MAX_FRAMES} frames of the first frame of that race, i.e. on frame +0 to +${ENTRY_MAX_FRAMES - 1}. The column gives the slowest entry in the case (+N frames).`);
  L.push('Colour rule on frames: on every frame drawn, no two bars on screen (opacity above 0) share a colour or are closer than CIEDE2000 ' + (col ? col.notes[1].match(/at least (\d+)/)[1] : '18') + ', and every driver is drawn in the same colour in every RTT-002 case.', '');
  if (col) {
    L.push(`**colour_rule_full_dataset — ${col.pass ? 'PASS' : 'FAIL'}** (every race of the full RTT-002 dataset, boards computed from win_credits.csv alone)`);
    for (const n of col.notes) L.push('- ' + n);
    for (const n of col.failures) L.push('- FAIL: ' + n);
    L.push('', '| Colour (as drawn) | Drivers, in the order they first reach the top ten |', '|---|---|');
    for (const [c, names] of Object.entries(col.by_colour)) L.push(`| \`${c}\` | ${names.join(', ')} |`);
    L.push('');
  }
  for (const r of cases) {
    if (!r.notes.length && !r.failures.length && !r.ocr_mismatch.length) continue;
    L.push('**' + r.name + '**');
    for (const n of r.notes) L.push('- ' + n);
    for (const n of r.failures) L.push('- FAIL: ' + n);
    for (const n of r.ocr_mismatch) L.push('- OCR differs: ' + n);
    L.push('');
  }
  L.push('The draw-call checks are the pass/fail gate. OCR is an independent read of the pixels: any mismatch is listed above, not hidden (' + cases.reduce((n, r) => n + r.ocr_mismatch.length, 0) + ' in this run). Labels on rows that overlap mid-overtake are not OCR-read (count in brackets). The full run is checked on every frame by draw calls only (no PNGs, no OCR).');
  fs.writeFileSync(path.join(__dirname, 'RESULTS.md'), L.join('\n') + '\n');
}

main().catch(e => { console.error(e); process.exit(2); });
