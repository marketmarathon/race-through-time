/* IQ-04 player tests: the six stress fixtures and an RTT-002 slice (1984-1989).
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
  const r = spawnSync('tesseract', [png, 'stdout', '--psm', '7', '-l', 'eng'], { encoding: 'utf8' });
  return (r.stdout || '').trim();
}

async function runCase(c) {
  const out = path.join(OUTDIR, c.name);
  fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
  const json = path.join(out, 'race.json');
  const adapter = execFileSync('python3', [path.join(ROOT, 'scripts', 'rtt_adapter.py'), c.dir, json], { encoding: 'utf8' }).trim();
  const data = JSON.parse(fs.readFileSync(json, 'utf8'));
  const cfg = rtt.loadConfig('config.json', Object.assign({ window: c.window || { from: null, to: null } }, c.overrides || {}));
  const E = expected(c.dir);
  const inWindow = E.races.filter(r => (!cfg.window.from || r.race_date >= cfg.window.from) && (!cfg.window.to || r.race_date <= cfg.window.to));
  const before = E.races.filter(r => cfg.window.from && r.race_date < cfg.window.from).pop();

  const res = { name: c.name, adapter_sha256: adapter.split(/\s+/)[0], events: inWindow.length, frames: 0,
                boundary_frames: 0, labels_checked: 0, ocr_checked: 0, ocr_skipped_overlap: 0, ocr_mismatch: [], failures: [], notes: [] };
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
    const outroFrames = Math.round(cfg.fps * 0.5);
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
      prevVals = vals;
      /* fixture-specific */
      if (c.expect.max_visible != null && Object.keys(vals).length > c.expect.max_visible) fail(`frame ${f}: more than ${c.expect.max_visible} bars`);

      /* event boundaries: keep the frame, and read the value labels back from its pixels */
      if (bounds.has(f)) {
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
  cases.push({ name: 'rtt002_1984_1989', dir: path.join(ROOT, 'data', 'rtt-002'),
               window: { from: '1984-01-01', to: '1989-12-31' }, overrides: {}, expect: {} });
  const run = only.length ? cases.filter(c => only.includes(c.name)) : cases;

  const results = [];
  for (const c of run) {
    const t0 = Date.now();
    const r = await runCase(c);
    r.seconds = ((Date.now() - t0) / 1000).toFixed(1);
    results.push(r);
    console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}: ${r.events} events, ${r.frames} frames, ${r.labels_checked} value labels, ${r.boundary_frames} boundary PNGs, OCR ${r.ocr_checked - r.ocr_mismatch.length}/${r.ocr_checked}, ${r.seconds} s`);
    for (const m of r.failures) console.log('   - ' + m);
    for (const m of r.ocr_mismatch.slice(0, 10)) console.log('   ocr: ' + m);
  }
  fs.writeFileSync(path.join(OUTDIR, 'results.json'), JSON.stringify(results, null, 1));
  if (!only.length) writeReport(results);
  process.exit(results.every(r => r.pass) ? 0 : 1);
}

function writeReport(results) {
  const pw = require(require.resolve('playwright/package.json', { paths: [KITDIR] })).version;
  const L = [];
  L.push('# IQ-04 player test results', '');
  L.push('Written by `node tests/player/run_tests.js` (all cases). Frames are 1920x1080 (preview width), drawn headless in Playwright ' + pw + ' Chromium, every race frame in order.');
  L.push('OCR: ' + (HAS_OCR ? spawnSync('tesseract', ['--version'], { encoding: 'utf8' }).stdout.split('\n')[0] + ' on every value label of the first frame of every race.' : 'NOT AVAILABLE (tesseract not installed); draw-call checks only.'), '');
  L.push('| Case | Result | Races | Frames | Race length | Value labels checked | Boundary frames | OCR read back (skipped: overlapping rows) | Longest entry slide (frames) | Name size | Pacing (rank / visible / quiet) | Adapter output SHA-256 |');
  L.push('|---|---|---|---|---|---|---|---|---|---|---|---|');
  for (const r of results)
    L.push(`| ${r.name} | ${r.pass ? 'PASS' : 'FAIL'} | ${r.events} | ${r.frames} | ${r.race_sec.toFixed(2)} s | ${r.labels_checked} | ${r.boundary_frames} | ${r.ocr_checked - r.ocr_mismatch.length}/${r.ocr_checked} (${r.ocr_skipped_overlap}) | ${r.entry_lag_max} | ${r.name_px}px${r.name_truncated ? ' (truncated)' : ''} | ${r.pacing.rank_change} / ${r.pacing.visible_change} / ${r.pacing.quiet} | \`${r.adapter_sha256.slice(0, 16)}…\` |`);
  L.push('');
  for (const r of results) {
    if (!r.notes.length && !r.failures.length && !r.ocr_mismatch.length) continue;
    L.push('**' + r.name + '**');
    for (const n of r.notes) L.push('- ' + n);
    for (const n of r.failures) L.push('- FAIL: ' + n);
    for (const n of r.ocr_mismatch) L.push('- OCR differs: ' + n);
    L.push('');
  }
  L.push('The draw-call checks are the pass/fail gate. OCR is an independent read of the pixels: any mismatch is listed above, not hidden (' + results.reduce((n, r) => n + r.ocr_mismatch.length, 0) + ' in this run). Labels on rows that overlap mid-overtake are not OCR-read (count in brackets).');
  fs.writeFileSync(path.join(__dirname, 'RESULTS.md'), L.join('\n') + '\n');
}

main().catch(e => { console.error(e); process.exit(2); });
