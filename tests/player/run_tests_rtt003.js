/* RTT-003 player tests (IQ-10). Every frame of each pilot clip and of the full-film config is drawn in
 * order (the rank glide is stateful) through the kit's own driver path (kits/rtt-002/rtt.js openPlayer)
 * at 1920 x 1080, and what was drawn (window.__LABELS, __BARS, __PICS, __CROWN, __KEY, __CALLOUT) is
 * checked against data/rtt-003/*.csv, read HERE, independently of the adapter and of rtt_timeline.js:
 *
 *   1. date line: exactly one per frame, "<D Month YYYY>" of a quarter end, never going backwards; the
 *      quarter shown is taken from it for every other check
 *   2. no value before launch: every console on screen has a series.csv row at the quarter shown and
 *      was launched on or before it (consoles.csv launch_date)
 *   3. values: every value label = series.csv units at the quarter shown, in millions with one decimal
 *      (rounded half up on the whole units, computed here with BigInt), "+" exactly where plus_flag is
 *      "yes", nothing in between quarter ends (a label changes only on the first frame of a quarter)
 *   4. order: the visible rows' target order = series.csv sorted by units, ties by who reached the value
 *      first, then the earlier launch (metric contract, Rank)
 *   5. estimated look: every bar's style = series.csv display_style at the quarter shown; the
 *      "· analyst estimate" label is drawn exactly on the analyst_estimate bars (DEC-084)
 *   6. fade dates: a console's bar is at full strength before the first quarter end on or after its
 *      consoles.csv fade_date, fades from that quarter end and is fully faded within fade.sec (+1 frame);
 *      Atari 2600 from 31 Dec 1991 (DEC-093)
 *   7. crown: on every frame the crown is on the leader per crown.csv (the latest change on or before
 *      the quarter shown); callouts appear exactly at the crown.csv changes inside the window, name the
 *      new and previous leader, and say "estimated figures" where crown.csv display_style is not official
 *   8. colours: every bar is its maker's colour (one colour per maker)
 *   9. pictures: every console row on screen has its picture, inside the picture column on its row
 *  10. layout: every label inside the frame (value labels and the crown inside the 64 px right margin);
 *      no bar, picture, name, value or label enters the maker key panel, the logo box or the callout line
 *  11. pacing: quarter ends up to 31 Dec 1988 at 0.5 s x 0.8-1.4, later 1.0 s x 0.8-1.4, crown changes
 *      held record_hold.sec, final table final_board_sec
 *  12. scoreboard (where on): each maker's total = series_by_maker.csv, ranked, "+" and the estimate
 *      marking as the adapter documents (any console of that maker with a "+"; least certain style)
 * Placeholder pictures and logos (plain shapes written at run time into tests/output/, never committed)
 * stand in for the private files. Results: tests/player/RESULTS_RTT003.md. Exit 1 on any failure.
 *
 *   node tests/player/run_tests_rtt003.js [case ...]
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const KIT = path.join(ROOT, 'kits', 'rtt-002');
const DATA = path.join(ROOT, 'data', 'rtt-003');
const rtt = require(path.join(KIT, 'rtt.js'));
const { placeholderPNG } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';
const OUT = path.join(ROOT, 'tests', 'output', 'rtt003');
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

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
const dateText = iso => { const [y, m, d] = iso.split('-').map(Number); return d + ' ' + MONTHS[m - 1] + ' ' + y; };
function millions(units) { const u = BigInt(units), t = (u + 50000n) / 100000n; return (t / 10n).toLocaleString('en-GB') + '.' + (t % 10n) + 'm'; }
const overlap = (a, b, gap = 0) => a.x < b.x + b.w + gap && b.x < a.x + a.w + gap && a.y < b.y + b.h + gap && b.y < a.y + a.h + gap;
const labelBox = l => ({ x: l.x, y: l.y - (l.asc || l.size * 0.75), w: l.w, h: (l.asc || l.size * 0.75) + (l.desc || l.size * 0.25) });

/* independent expectations from data/rtt-003 */
const consoles = readCSV(path.join(DATA, 'consoles.csv')).filter(r => r.in_scope === 'yes');
const C = Object.fromEntries(consoles.map(r => [r.console_id, r]));
const series = readCSV(path.join(DATA, 'series.csv'));
const byQ = {};
for (const r of series) (byQ[r.quarter_end] = byQ[r.quarter_end] || {})[r.console_id] = r;
const quarters = Object.keys(byQ).sort();
const reachedAt = {};       // [quarter][id] = first quarter end at which the console had this exact value
{ const last = {}, since = {};
  for (const q of quarters) { reachedAt[q] = {}; for (const [id, r] of Object.entries(byQ[q])) { if (last[id] !== r.units) { last[id] = r.units; since[id] = q; } reachedAt[q][id] = since[id]; } } }
function expectedOrder(q) {
  return Object.keys(byQ[q]).sort((a, b) => {
    const ua = BigInt(byQ[q][a].units), ub = BigInt(byQ[q][b].units);
    if (ua !== ub) return ua > ub ? -1 : 1;
    const ra = reachedAt[q][a], rb = reachedAt[q][b]; if (ra !== rb) return ra < rb ? -1 : 1;
    return C[a].launch_date < C[b].launch_date ? -1 : C[a].launch_date > C[b].launch_date ? 1 : 0;
  });
}
const crown = readCSV(path.join(DATA, 'crown.csv'));
const leaderAt = q => crown.filter(c => c.quarter_end <= q).slice(-1)[0];
const byMaker = {};
for (const r of readCSV(path.join(DATA, 'series_by_maker.csv'))) (byMaker[r.quarter_end] = byMaker[r.quarter_end] || {})[r.maker_key] = r.units;
const fadeQuarter = {};
for (const c of consoles) fadeQuarter[c.console_id] = c.fade_date ? quarters.find(q => q >= c.fade_date) || null : null;

function placeholderAssets(cfg) {
  const dir = path.join(OUT, '_assets');
  fs.mkdirSync(path.join(dir, 'icons'), { recursive: true }); fs.mkdirSync(path.join(dir, 'logos'), { recursive: true });
  for (const c of consoles) placeholderPNG(path.join(dir, 'icons', c.console_id + '.png'), 165, 100, [180, 180, 190]);
  for (const m of cfg.maker_order) fs.writeFileSync(path.join(dir, 'logos', m + '.svg'), `<svg xmlns="http://www.w3.org/2000/svg" width="120" height="40"><rect width="120" height="40" fill="#555"/></svg>`);
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  return dir;
}

async function runCase(name, configFile, opts = {}) {
  const cfg = rtt.loadConfig('../rtt-003/' + configFile);
  const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
  process.env.RTT_LOCAL_ASSETS = placeholderAssets(cfg);
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
  delete process.env.RTT_LOCAL_ASSETS;
  const info = await pg.evaluate(() => ({ start: TL.startFrame, raceFrames: RACE_FRAMES, dates: TL.events.map(e => e.date), opening: TL.openingEvent.date,
                                          holdK: TL.hold.map((h, k) => h ? k : -1).filter(k => k >= 0), mult: TL.mult, geom: geom() }));
  const res = { name, config: configFile, frames: info.raceFrames, quarters: info.dates.length, opening: info.opening, last: info.dates[info.dates.length - 1],
                failures: [], counts: { values: 0, plus: 0, styles: { official: 0, estimated: 0, analyst_estimate: 0 }, est_labels: 0, faded_frames: 0, crown_frames: 0, callout_frames: 0, pics: 0, key_rows: 0 },
                crowns: [], callouts: [], fadeStarts: {}, closest: { key: 1e9, logo: 1e9, callout: 1e9 } };
  const fail = m => { if (res.failures.length < 40) res.failures.push(m); };
  const pal = cfg.palette, mo = cfg.maker_order, drawn = h => h;   // colours are checked as drawn (drawnColour leaves these unchanged)
  const logo = (cfg.overlays || []).find(o => o.name === 'logo');
  let prevDate = null, prevVals = {}, firstFrameOf = {}, fadeSeen = {};
  const winDates = new Set(info.dates);
  for (let f = 0; f < info.raceFrames; f++) {
    const S = await pg.evaluate(t => { drawAt(t); return { L: window.__LABELS, B: window.__BARS, P: window.__PICS, CR: window.__CROWN, K: window.__KEY, CO: window.__CALLOUT, R: window.__RANK }; }, f / cfg.fps);
    const dl = S.L.filter(l => l.kind === 'time_line');
    if (dl.length !== 1) { fail(`f${f}: ${dl.length} date lines`); continue; }
    const q = quarters.find(x => dateText(x) === dl[0].text);
    if (!q) { fail(`f${f}: date line "${dl[0].text}" is not a quarter end`); continue; }
    if (prevDate && q < prevDate) fail(`f${f}: date went backwards ${prevDate} -> ${q}`);
    if (q !== prevDate) { firstFrameOf[q] = f; if (prevDate && !winDates.has(q)) fail(`f${f}: quarter ${q} is not in the window`); }
    const isFirst = firstFrameOf[q] === f;
    // 4. order
    const want = expectedOrder(q).slice(0, cfg.rows), got = S.R;
    if (want.join() !== got.join()) fail(`f${f} ${q}: order ${got.join(' ')} != ${want.join(' ')}`);
    const vis = S.B.filter(b => b.alpha > 0);
    for (const b of vis) {
      const r = byQ[q][b.id];
      // 2. nothing before launch
      if (!r) { fail(`f${f} ${q}: ${b.id} on screen with no series row`); continue; }
      if (C[b.id].launch_date > q) fail(`f${f} ${q}: ${b.id} drawn before launch ${C[b.id].launch_date}`);
      // 5. style
      if (b.style !== r.display_style) fail(`f${f} ${q}: ${b.id} style ${b.style} != ${r.display_style}`);
      res.counts.styles[b.style] = (res.counts.styles[b.style] || 0) + 1;
      // 8. colour
      const wantCol = pal[mo.indexOf(C[b.id].maker_key)];
      if (b.colour.toLowerCase() !== drawn(wantCol).toLowerCase()) fail(`f${f}: ${b.id} colour ${b.colour} != ${wantCol} (${C[b.id].maker_key})`);
      // 6. fade
      const fq = fadeQuarter[b.id];
      if (fq === null || q < fq) { if (Math.abs(b.fade - 1) > 1e-9) fail(`f${f} ${q}: ${b.id} faded (${b.fade}) before its fade quarter ${fq}`); }
      else {
        const onset = firstFrameOf[fq] === f;            // the fade starts on this frame (still 1 here)
        if (!onset && !(b.fade < 1)) fail(`f${f} ${q}: ${b.id} not faded after the start of its fade quarter ${fq}`);
        res.counts.faded_frames++;
        if (!(b.id in res.fadeStarts)) res.fadeStarts[b.id] = q;
        const startF = firstFrameOf[fq] != null ? firstFrameOf[fq] : -1e9;
        if (f - startF > Math.ceil(cfg.fade.sec * cfg.fps) + 1 && Math.abs(b.fade - cfg.fade.alpha) > 1e-6) fail(`f${f} ${q}: ${b.id} still fading (${b.fade}) more than fade.sec after ${fq}`);
      }
      // 9. picture
      const p = S.P.find(x => x.id === b.id);
      if (!p) fail(`f${f}: ${b.id} has no picture`); else {
        res.counts.pics++;
        const mid = b.rect.y + b.rect.h / 2;
        if (Math.abs(p.box.y + p.box.h / 2 - mid) > 0.5) fail(`f${f}: ${b.id} picture not on its row`);
        if (p.drawn.x < p.box.x - 0.5 || p.drawn.x + p.drawn.w > p.box.x + p.box.w + 0.5 || p.drawn.y < p.box.y - 0.5 || p.drawn.y + p.drawn.h > p.box.y + p.box.h + 0.5) fail(`f${f}: ${b.id} picture outside its box`);
      }
    }
    // 3. values and "+"
    for (const l of S.L.filter(l => l.kind === 'value')) {
      const r = byQ[q][l.id];
      if (!r) { fail(`f${f}: value for ${l.id} with no series row at ${q}`); continue; }
      const w = millions(r.units) + (r.plus_flag === 'yes' ? '+' : '') + (cfg.bar_notes && cfg.bar_notes.some(n => n.id === l.id) ? '*' : '');
      res.counts.values++; if (r.plus_flag === 'yes') res.counts.plus++;
      if (l.text !== w) fail(`f${f} ${q}: ${l.id} value "${l.text}" != "${w}"`);
      if (!l.tab) fail(`f${f}: ${l.id} value not on fixed-pitch digits`);
      if (!isFirst && prevVals[l.id] != null && prevVals[l.id] !== l.text && l.alpha > 0) fail(`f${f}: ${l.id} value changed inside a quarter`);
      prevVals[l.id] = l.text;
      if (l.x + l.w > 1856 + 0.5) fail(`f${f}: ${l.id} value ends at x ${l.x + l.w} (limit 1856)`);
    }
    // 5b. analyst label exactly on analyst bars
    const est = new Set(S.L.filter(l => l.kind === 'est_label').map(l => l.id));
    res.counts.est_labels += est.size;
    for (const l of S.L.filter(l => l.kind === 'value')) {
      const want = byQ[q][l.id] && byQ[q][l.id].display_style === 'analyst_estimate';
      if (want !== est.has(l.id)) fail(`f${f} ${q}: ${l.id} analyst label ${est.has(l.id)} but style ${byQ[q][l.id] && byQ[q][l.id].display_style}`);
    }
    // 7. crown
    const lead = leaderAt(q);
    if (!S.CR) fail(`f${f} ${q}: no crown`); else {
      res.counts.crown_frames++;
      if (S.CR.id !== lead.new_leader) fail(`f${f} ${q}: crown on ${S.CR.id}, crown.csv says ${lead.new_leader}`);
      if (S.CR.x + S.CR.w > 1856.5) fail(`f${f}: crown ends at x ${S.CR.x + S.CR.w}`);
      if (!res.crowns.length || res.crowns[res.crowns.length - 1].id !== S.CR.id) res.crowns.push({ q, id: S.CR.id });
    }
    if (S.CO) {
      res.counts.callout_frames++;
      // the latest crown change on or before the quarter shown, which must have started < callout.sec ago
      const c = crown.filter(x => x.previous_leader && x.quarter_end <= q && firstFrameOf[x.quarter_end] != null).slice(-1)[0];
      if (!c || f - firstFrameOf[c.quarter_end] >= Math.round(cfg.callout.sec * cfg.fps)) fail(`f${f} ${q}: callout more than callout.sec after a crown change`);
      else {
        if (S.CO.id !== c.new_leader || S.CO.previous !== c.previous_leader) fail(`f${f}: callout ${S.CO.id}/${S.CO.previous} != ${c.new_leader}/${c.previous_leader}`);
        const ex = S.L.find(l => l.kind === 'callout_extra');
        if (ex && (c.display_style !== 'official') !== ex.text.includes('estimated figures')) fail(`f${f}: callout "estimated figures" does not match crown.csv style ${c.display_style}`);
        if (!res.callouts.some(x => x.q === c.quarter_end)) res.callouts.push({ q: c.quarter_end, id: c.new_leader, text: S.L.filter(l => l.kind.startsWith('callout')).map(l => l.text).join('') });
      }
    }
    if (isFirst && crown.some(x => x.previous_leader && x.quarter_end === q) && !S.CO) fail(`f${f} ${q}: no callout on the crown change`);
    // 12. scoreboard
    if (S.K) {
      const sb = cfg.maker_key.scoreboard, mk = byMaker[q];
      const keys = S.K.rows.map(r => r.key), want = mo.filter(m => mk[m] != null);
      const wantOrder = sb ? want.slice().sort((a, b) => (BigInt(mk[b]) > BigInt(mk[a]) ? 1 : BigInt(mk[b]) < BigInt(mk[a]) ? -1 : mo.indexOf(a) - mo.indexOf(b))) : want;
      if (keys.join() !== wantOrder.join()) fail(`f${f} ${q}: key rows ${keys.join()} != ${wantOrder.join()}`);
      res.counts.key_rows += keys.length;
      if (sb) for (const r of S.K.rows) {
        const ids = Object.keys(byQ[q]).filter(id => C[id].maker_key === r.key);
        const rank = { official: 0, estimated: 1, analyst_estimate: 2 };
        const st = ids.map(id => byQ[q][id].display_style).sort((a, b) => rank[b] - rank[a])[0];
        const plus = ids.some(id => byQ[q][id].plus_flag === 'yes');
        if (String(r.total) !== mk[r.key]) fail(`f${f} ${q}: ${r.key} total ${r.total} != ${mk[r.key]}`);
        if (r.style !== st || r.plus !== plus) fail(`f${f} ${q}: ${r.key} style/plus ${r.style}/${r.plus} != ${st}/${plus}`);
        const tl = S.L.find(l => l.kind === 'key_total' && l.id === r.key);
        if (!tl || tl.text !== millions(mk[r.key]) + (plus ? '+' : '')) fail(`f${f}: ${r.key} total label "${tl && tl.text}"`);
      }
    }
    // 10. layout
    const things = vis.map(b => ({ what: 'bar ' + b.id, r: b.rect })).concat(S.P.filter(p => p.alpha > 0).map(p => ({ what: 'picture ' + p.id, r: p.drawn })))
      .concat(S.L.filter(l => ['name', 'value', 'est_label'].includes(l.kind) && l.alpha > 0).map(l => ({ what: l.kind + ' ' + l.id, r: labelBox(l) })));
    if (S.CR) things.push({ what: 'crown', r: S.CR });
    for (const l of S.L) { const bx = labelBox(l); if (bx.x < -0.5 || bx.x + bx.w > 1920.5 || bx.y < -0.5 || bx.y + bx.h > 1080.5) fail(`f${f}: ${l.kind} "${l.text}" outside the frame`); }
    const gapTo = (a, b) => Math.max(b.x - (a.x + a.w), a.x - (b.x + b.w), b.y - (a.y + a.h), a.y - (b.y + b.h));
    for (const t of things) {
      if (S.K) { if (overlap(t.r, S.K.box)) fail(`f${f}: ${t.what} enters the maker key`); else res.closest.key = Math.min(res.closest.key, gapTo(t.r, S.K.box)); }
      if (logo) { if (overlap(t.r, logo, cfg.overlay_gap)) fail(`f${f}: ${t.what} enters the logo box`); else res.closest.logo = Math.min(res.closest.logo, gapTo(t.r, logo)); }
    }
    const top = S.L.filter(l => ['callout', 'callout_extra', 'note', 'subtitle'].includes(l.kind) && l.alpha > 0.01);
    const others = S.L.filter(l => ['axis', 'title', 'time_line'].includes(l.kind));
    for (const a of top) for (const b of others) { const A = labelBox(a), B = labelBox(b);
      if (overlap(A, B)) fail(`f${f}: ${a.kind} overlaps ${b.kind} "${b.text}"`); else res.closest.callout = Math.min(res.closest.callout, gapTo(A, B)); }
    if (logo) for (const a of top) if (overlap(labelBox(a), logo)) fail(`f${f}: ${a.kind} enters the logo box`);
    prevDate = q;
  }
  await br.close();
  // 11. pacing, from the frames each quarter was on screen
  const sec = cfg.pacing, base = d => { for (const s of sec.segments || []) if (d <= s.to) return s.sec_per_event; return sec.sec_per_event; };
  const shown = info.dates.filter(d => firstFrameOf[d] != null);
  if (shown.length !== info.dates.length) fail(`only ${shown.length} of ${info.dates.length} quarters shown`);
  const beats = [];
  for (let i = 0; i + 1 < info.dates.length; i++) {
    const d = info.dates[i], n = firstFrameOf[info.dates[i + 1]] - firstFrameOf[d], held = crown.some(c => c.quarter_end === d && c.previous_leader) && cfg.record_hold.enabled;
    if (held) { if (n !== Math.round(cfg.record_hold.sec * cfg.fps)) fail(`${d}: crown change held ${n} frames`); continue; }
    const lo = Math.round(base(d) * 0.8 * cfg.fps) - 1, hi = Math.round(base(d) * 1.4 * cfg.fps) + 1;
    if (n < lo || n > hi) fail(`${d}: beat ${n} frames outside ${lo}-${hi}`);
    beats.push({ d, n });
  }
  const lastF = firstFrameOf[info.dates[info.dates.length - 1]];
  if (info.raceFrames - lastF !== Math.round(sec.final_board_sec * cfg.fps)) fail(`final table ${info.raceFrames - lastF} frames, want ${sec.final_board_sec} s`);
  if (info.dates[0] && firstFrameOf[info.dates[0]] !== Math.round(sec.lead_in_sec * cfg.fps)) fail(`first quarter after the opening lands at frame ${firstFrameOf[info.dates[0]]}`);
  const early = beats.filter(b => b.d <= '1988-12-31').map(b => b.n), late = beats.filter(b => b.d > '1988-12-31').map(b => b.n);
  res.beats = { early: early.length ? `${Math.min(...early)}-${Math.max(...early)} frames` : 'n/a', late: late.length ? `${Math.min(...late)}-${Math.max(...late)} frames` : 'n/a' };
  // 6b. the crown changes inside the window all appeared as callouts; Atari's fade date
  const want = crown.filter(c => c.previous_leader && c.quarter_end > info.opening && c.quarter_end <= res.last).map(c => c.quarter_end);
  if (want.join() !== res.callouts.map(c => c.q).join()) fail(`callouts at ${res.callouts.map(c => c.q).join()} but crown.csv changes at ${want.join()}`);
  if (opts.atari && res.fadeStarts.atari_2600 !== '1991-12-31') fail(`Atari 2600 fades from ${res.fadeStarts.atari_2600}, want 1991-12-31`);
  res.pass = res.failures.length === 0;
  return res;
}

function write(results) {
  const L = ['# RTT-003 player test results (IQ-10)', '',
    'Written by `node tests/player/run_tests_rtt003.js`. Every frame drawn in order at 1920 x 1080 in Playwright Chromium through `kits/rtt-002/rtt.js` (the same path as the render), with placeholder pictures and logos. Expected values read independently from `data/rtt-003/` (series.csv, consoles.csv, crown.csv, series_by_maker.csv).', '',
    `Overall: ${results.filter(r => r.pass).length}/${results.length} PASS.`, '',
    '| Case | Result | Config | Quarters (opening → last) | Frames | Value labels checked (with "+") | Bar styles checked (official / estimated / analyst) | Analyst labels | Faded bar-frames | Crown frames / leaders | Callouts | Fade starts seen | Beats (≤1988 / later) | Closest gap: key / logo / callout line |',
    '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|'];
  for (const r of results) L.push(`| ${r.name} | ${r.pass ? 'PASS' : 'FAIL'} | \`${r.config}\` | ${r.quarters} (${r.opening} → ${r.last}) | ${r.frames} (${(r.frames / 30).toFixed(1)} s) | ${r.counts.values} (${r.counts.plus}) | ${r.counts.styles.official} / ${r.counts.styles.estimated} / ${r.counts.styles.analyst_estimate} | ${r.counts.est_labels} | ${r.counts.faded_frames} | ${r.counts.crown_frames} / ${r.crowns.map(c => c.id + ' ' + c.q).join(' → ')} | ${r.callouts.map(c => c.q + ' ' + c.id).join('; ') || 'none'} | ${Object.entries(r.fadeStarts).map(([k, v]) => k + ' ' + v).join('; ') || 'none'} | ${r.beats.early} / ${r.beats.late} | ${r.closest.key.toFixed(0)} / ${r.closest.logo.toFixed(0)} / ${r.closest.callout === 1e9 ? 'n/a' : r.closest.callout.toFixed(0)} px |`);
  L.push('', 'Callout texts:');
  for (const r of results) for (const c of r.callouts) L.push(`- ${r.name}, ${c.q}: "${c.text}"`);
  for (const r of results) if (!r.pass) { L.push('', `**${r.name} failures** (first 40):`); for (const f of r.failures) L.push('- ' + f); }
  L.push('');
  fs.writeFileSync(path.join(__dirname, 'RESULTS_RTT003.md'), L.join('\n'));
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const cases = [
    ['clip_A_1985_1992', 'config_rtt003_clip_A_1985_1992.json', { atari: true }],
    ['clip_B_1996_1999', 'config_rtt003_clip_B_1996_1999.json'],
    ['clip_C_2005_2009', 'config_rtt003_clip_C_2005_2009.json'],
    ['clip_C_2005_2009_scoreboard', 'config_rtt003_clip_C_2005_2009_scoreboard.json'],
    ['film_full_config', 'config_rtt003_film.json', { atari: true }],
    ['still_ps2_note', 'config_rtt003_still_ps2_note.json', { atari: true }],
    ['still_2015_top20', 'config_rtt003_still_2015_top20.json', { atari: true }]
  ].filter(c => process.argv.length <= 2 || process.argv.slice(2).includes(c[0]));
  const results = [];
  for (const [n, c, o] of cases) { const t0 = Date.now(); const r = await runCase(n, c, o); results.push(r);
    console.log(`${r.pass ? 'PASS' : 'FAIL'} ${n}: ${r.frames} frames in ${((Date.now() - t0) / 1000).toFixed(0)} s` + (r.pass ? '' : '\n  ' + r.failures.slice(0, 8).join('\n  '))); }
  if (process.argv.length <= 2) write(results);
  process.exit(results.every(r => r.pass) ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
