/* RTT-003 player tests (IQ-10, round 2). Every frame of each pilot clip and of the full-film config is drawn in
 * order (the rank glide is stateful) through the kit's own driver path (kits/rtt-002/rtt.js openPlayer)
 * at 1920 x 1080, and what was drawn (window.__LABELS, __BARS, __PICS, __LOGOS, __CROWN, __KEY, __CALLOUT,
 * __FINAL) is checked against data/rtt-003/*.csv, read HERE, independently of the adapter and of rtt_timeline.js:
 *
 *   1. date line: exactly one per frame, "<D Month YYYY>" of a quarter end, never going backwards
 *   2. no value before launch: every console on screen has a series.csv row for the quarter shown
 *   3. values COUNT (DEC-115): on every quarter-end frame each label = series.csv units in millions (one
 *      decimal, half up, computed with BigInt), "+" exactly where plus_flag is "yes"; while counting, the
 *      units stay between the two quarter ends, never go backwards, the label matches the counted units and
 *      carries "+" only if either end does; every bar that grows by 1 million or more in a quarter is seen
 *      strictly between the two figures (proof that it counts rather than jumps)
 *   4. order: exact (tie rule) at quarter ends; on every frame no row sits above one with more units
 *   5. estimated look: every bar's style = series.csv display_style; "· analyst estimate" exactly on those
 *   6. fade dates: full strength before the first quarter end on or after the fade date, fading after it
 *      (Atari 2600 from 31 Dec 1991)
 *   7. crown: on the counted leader on every frame; crown.csv's leader on every quarter-end frame
 *   8. callouts: exactly the crown changes inside the window plus the approved moments (Game Boy first past
 *      100 million, DS passes Game Boy), each from the frame its counted figures cross, for callout.sec;
 *      the on-hold Switch-passes-DS moment never shown
 *   9. pictures and logos: every row on screen has its picture and its maker's logo (consoles.csv maker_key)
 *      on its row, the logo between the picture and the bar; tall-picture overlap reported
 *  10. final-table line ("Switch is at least 3.4 million behind the PS2", gap from the data) and the PS2
 *      footnote only on the film's final table
 *  11. layout: nothing outside the frame; no bar, picture, logo, name, value or crown in the scoreboard or
 *      logo box; the callout, final line and footnote overlap no axis number, title or date line
 *  12. pacing: each quarter counts over 0.8-1.4 x its base (0.5 s to 1988, then 1.0 s, or the clip's base),
 *      a crown-change quarter then pauses record_hold.sec; final table final_board_sec
 *  13. scoreboard: totals = series_by_maker.csv at quarter ends, counted and in order between
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
                                          qend: TL.quarterEndFrame, count: TL.countFrames, mult: TL.mult, hold: TL.hold, geom: geom() }));
  const res = { name, config: configFile, frames: info.raceFrames, quarters: info.dates.length, opening: info.opening, last: info.dates[info.dates.length - 1],
                failures: [], counts: { quarter_end_values: 0, counting_values: 0, plus: 0, styles: { official: 0, estimated: 0, analyst_estimate: 0 }, est_labels: 0, faded_frames: 0, crown_frames: 0, callout_frames: 0, pics: 0, logos: 0, key_rows: 0, final_frames: 0 },
                crowns: [], callouts: [], fadeStarts: {}, closest: { key: 1e9, logo: 1e9, callout: 1e9 }, tallOverlap: 0 };
  const fail = m => { if (res.failures.length < 40) res.failures.push(m); };
  const pal = cfg.palette, mo = cfg.maker_order;
  const logo = (cfg.overlays || []).find(o => o.name === 'logo');
  const kOf = {}; info.dates.forEach((d, k) => kOf[d] = k);
  const prevQ = d => { const i = quarters.indexOf(d); return i > 0 ? quarters[i - 1] : null; };
  const isDataEnd = res.last === quarters[quarters.length - 1];
  const valNum = t => parseFloat(t.replace(/,/g, ''));
  // the moments the film must show: crown changes, plus the approved extras that are not on hold, inside the window
  const wantMoments = crown.filter(c => c.previous_leader && c.quarter_end > info.opening && c.quarter_end <= res.last).map(c => ({ q: c.quarter_end, type: 'crown', id: c.new_leader, other: c.previous_leader }));
  for (const m of cfg.moments || []) {
    if (m.on_hold) continue;
    let q = null;
    if (m.type === 'first_past') q = quarters.find(x => byQ[x][m.id] && BigInt(byQ[x][m.id].units) >= BigInt(m.units));
    if (m.type === 'passes') q = quarters.find(x => { const o = expectedOrder(x), p = prevQ(x) && expectedOrder(prevQ(x)); return o.indexOf(m.id) === m.rank - 1 && o.indexOf(m.other) === m.rank && p && p.indexOf(m.other) < p.indexOf(m.id); });
    if (q && q > info.opening && q <= res.last) wantMoments.push({ q, type: m.type, id: m.id, other: m.other });
  }
  let prevDate = null, firstFrameOf = {}, prevLab = {}, prevU = {}, prevRank0 = null;
  const between = new Set(), needBetween = [];
  const winDates = new Set(info.dates);
  for (let f = 0; f < info.raceFrames; f++) {
    const S = await pg.evaluate(t => { drawAt(t); return { L: window.__LABELS, B: window.__BARS, P: window.__PICS, LG: window.__LOGOS, CR: window.__CROWN, K: window.__KEY, CO: window.__CALLOUT, R: window.__RANK, FI: window.__FINAL }; }, f / cfg.fps);
    const dl = S.L.filter(l => l.kind === 'time_line');
    if (dl.length !== 1) { fail(`f${f}: ${dl.length} date lines`); continue; }
    const q = quarters.find(x => dateText(x) === dl[0].text);
    if (!q) { fail(`f${f}: date line "${dl[0].text}" is not a quarter end`); continue; }
    if (prevDate && q < prevDate) fail(`f${f}: date went backwards ${prevDate} -> ${q}`);
    if (q !== prevDate) { firstFrameOf[q] = f; if (prevDate && !winDates.has(q)) fail(`f${f}: quarter ${q} is not in the window`); }
    const k = kOf[q], atEnd = k == null || f >= info.qend[k];            // k undefined = the opening board (exact)
    const pq = k == null ? q : (k > 0 ? info.dates[k - 1] : info.opening);
    const vis = S.B.filter(b => b.alpha > 0);
    // 4. order: exact at the quarter end; while counting, the order of the counted figures
    if (atEnd) { const want = expectedOrder(q).slice(0, cfg.rows); if (want.join() !== S.R.join()) fail(`f${f} ${q}: order ${S.R.join(' ')} != ${want.join(' ')}`); }
    const uOf = {}; for (const b of S.B) uOf[b.id] = b.units;
    for (let i = 1; i < S.R.length; i++) if (uOf[S.R[i]] > uOf[S.R[i - 1]]) fail(`f${f}: ${S.R[i]} above ${S.R[i - 1]} with more units`);
    for (const b of vis) {
      const r = byQ[q][b.id];
      if (!r) { fail(`f${f} ${q}: ${b.id} on screen with no series row`); continue; }
      if (C[b.id].launch_date > q) fail(`f${f} ${q}: ${b.id} drawn before launch ${C[b.id].launch_date}`);
      if (b.style !== r.display_style) fail(`f${f} ${q}: ${b.id} style ${b.style} != ${r.display_style}`);
      res.counts.styles[b.style] = (res.counts.styles[b.style] || 0) + 1;
      // counted units stay between the two quarter ends and never go back (the data has one 10,000-unit dip, SNES early 1997)
      const lo = byQ[pq] && byQ[pq][b.id] ? BigInt(byQ[pq][b.id].units) : 0n, hi = BigInt(r.units);
      const u = BigInt(b.units), mn = lo < hi ? lo : hi, mx = lo < hi ? hi : lo;
      if (u < mn || u > mx) fail(`f${f} ${q}: ${b.id} counted ${b.units} outside ${mn}..${mx}`);
      if (atEnd && u !== hi) fail(`f${f} ${q}: ${b.id} ${b.units} at the quarter end, data ${r.units}`);
      if (!atEnd && u > mn && u < mx) between.add(q + ' ' + b.id);         // proof that it counts
      if (atEnd && f === info.qend[k] && hi - lo >= 1000000n) needBetween.push(q + ' ' + b.id);
      if (prevU[b.id] != null && firstFrameOf[q] !== f && hi >= lo && u < prevU[b.id]) fail(`f${f}: ${b.id} counted backwards`);
      prevU[b.id] = u;
      const wantCol = pal[mo.indexOf(C[b.id].maker_key)];
      if (b.colour.toLowerCase() !== wantCol.toLowerCase()) fail(`f${f}: ${b.id} colour ${b.colour} != ${wantCol}`);
      const fq = fadeQuarter[b.id];
      if (fq === null || q < fq) { if (Math.abs(b.fade - 1) > 1e-9) fail(`f${f} ${q}: ${b.id} faded before its fade quarter ${fq}`); }
      else {
        if (firstFrameOf[fq] !== f && !(b.fade < 1)) fail(`f${f} ${q}: ${b.id} not faded after the start of its fade quarter ${fq}`);
        res.counts.faded_frames++;
        if (!(b.id in res.fadeStarts)) res.fadeStarts[b.id] = q;
      }
      const mid = b.rect.y + b.rect.h / 2;
      const p = S.P.find(x => x.id === b.id);
      if (!p) fail(`f${f}: ${b.id} has no picture`); else {
        res.counts.pics++;
        if (Math.abs(p.box.y + p.box.h / 2 - mid) > 0.5) fail(`f${f}: ${b.id} picture not on its row`);
        if (p.drawn.x < p.box.x - 0.5 || p.drawn.x + p.drawn.w > p.box.x + p.box.w + 0.5 || p.drawn.y < p.box.y - 0.5 || p.drawn.y + p.drawn.h > p.box.y + p.box.h + 0.5) fail(`f${f}: ${b.id} picture outside its box`);
      }
      if (cfg.bar_logos && cfg.bar_logos.enabled) {
        const g = (S.LG || []).find(x => x.id === b.id);
        if (!g || g.maker !== C[b.id].maker_key || !g.drawn) fail(`f${f}: ${b.id} has no ${C[b.id].maker_key} logo`); else {
          res.counts.logos++;
          if (Math.abs(g.tile.y + g.tile.h / 2 - mid) > 0.5) fail(`f${f}: ${b.id} logo not on its row`);
          if (p && !(g.tile.x >= p.box.x + p.box.w - 0.5 && g.tile.x + g.tile.w <= b.rect.x + 0.5)) fail(`f${f}: ${b.id} logo not between its picture and its bar`);
          if (g.drawn.x < g.tile.x || g.drawn.x + g.drawn.w > g.tile.x + g.tile.w + 0.01 || g.drawn.y < g.tile.y || g.drawn.y + g.drawn.h > g.tile.y + g.tile.h + 0.01) fail(`f${f}: ${b.id} logo outside its tile`);
        }
      }
    }
    // tall pictures: how far a picture's drawn area reaches into a settled neighbour's (reported)
    const restY = Object.fromEntries(S.B.filter(b => Math.abs(b.y - Math.round(b.y)) < 0.02).map(b => [b.id, Math.round(b.y)]));
    const settled = S.P.filter(p => p.alpha > 0.99 && p.id in restY);
    for (let i = 0; i < settled.length; i++) for (let j = i + 1; j < settled.length; j++) {
      const A = settled[i].drawn, B = settled[j].drawn;
      if (overlap(A, B)) res.tallOverlap = Math.max(res.tallOverlap, Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y));
    }
    // 3. values: exact (with "+") at the quarter end; while counting, "+" if either end carries one; never backwards
    const finalOn = isDataEnd && k === info.dates.length - 1 && f >= info.qend[k] && !S.CO;
    for (const l of S.L.filter(l => l.kind === 'value')) {
      const r = byQ[q][l.id], pr = byQ[pq] && byQ[pq][l.id];
      const plusEnd = r.plus_flag === 'yes', plusPrev = pr ? pr.plus_flag === 'yes' : false;
      const mark = finalOn && cfg.final_footnote && cfg.final_footnote.enabled && cfg.final_footnote.id === l.id ? cfg.final_footnote.mark : '';
      if (atEnd) {
        res.counts.quarter_end_values++;
        const w = millions(r.units) + (plusEnd ? '+' : '') + mark;
        if (l.text !== w) fail(`f${f} ${q}: ${l.id} value "${l.text}" != "${w}" at the quarter end`);
      } else {
        res.counts.counting_values++;
        const b = S.B.find(x => x.id === l.id);
        const w = millions(String(b.units)) + ((plusEnd || plusPrev) ? '+' : '');
        if (l.text !== w) fail(`f${f} ${q}: ${l.id} counting label "${l.text}" != "${w}"`);
      }
      if (l.text.includes('+')) res.counts.plus++;
      if (prevLab[l.id] != null && firstFrameOf[q] !== f && valNum(l.text) < valNum(prevLab[l.id]) && !(pr && BigInt(pr.units) > BigInt(r.units))) fail(`f${f}: ${l.id} label went backwards ${prevLab[l.id]} -> ${l.text}`);
      prevLab[l.id] = l.text;
      if (!l.tab) fail(`f${f}: ${l.id} value not on fixed-pitch digits`);
      if (l.x + l.w > 1856 + 0.5) fail(`f${f}: ${l.id} value ends at x ${l.x + l.w} (limit 1856)`);
    }
    const est = new Set(S.L.filter(l => l.kind === 'est_label').map(l => l.id));
    res.counts.est_labels += est.size;
    for (const l of S.L.filter(l => l.kind === 'value')) {
      const want = byQ[q][l.id].display_style === 'analyst_estimate';
      if (want !== est.has(l.id)) fail(`f${f} ${q}: ${l.id} analyst label ${est.has(l.id)} but style ${byQ[q][l.id].display_style}`);
    }
    // 7. crown: on the counted leader every frame; crown.csv's leader at every quarter end
    if (!S.CR) fail(`f${f} ${q}: no crown`); else {
      res.counts.crown_frames++;
      if (S.CR.id !== S.R[0]) fail(`f${f}: crown on ${S.CR.id}, leader ${S.R[0]}`);
      if (atEnd && S.CR.id !== leaderAt(q).new_leader) fail(`f${f} ${q}: crown on ${S.CR.id}, crown.csv says ${leaderAt(q).new_leader}`);
      if (S.CR.x + S.CR.w > 1856.5) fail(`f${f}: crown ends at x ${S.CR.x + S.CR.w}`);
      if (!res.crowns.length || res.crowns[res.crowns.length - 1].id !== S.CR.id) res.crowns.push({ q, id: S.CR.id, f });
    }
    // callouts: each wanted moment from the frame its counted figures cross, for callout.sec; nothing else
    if (S.CO) {
      res.counts.callout_frames++;
      const m = wantMoments.find(x => x.q === info.dates[S.CO.k] && x.type === S.CO.type && x.id === S.CO.id);
      if (!m) fail(`f${f}: unexpected callout ${S.CO.type} ${S.CO.id}`);
      else {
        if (f - S.CO.frame >= Math.round(cfg.callout.sec * cfg.fps) || f < S.CO.frame) fail(`f${f}: callout outside its ${cfg.callout.sec} s`);
        if (f === S.CO.frame) {
          const b = S.B.find(x => x.id === m.id), o = m.other && S.B.find(x => x.id === m.other);
          if (m.type === 'crown' && S.R[0] !== m.id) fail(`f${f}: crown callout but ${m.id} not first`);
          if (m.type === 'crown' && prevRank0 === m.id) fail(`f${f}: crown callout ${m.id} was already first on the frame before`);
          if (m.type === 'first_past' && !(b && BigInt(b.units) >= BigInt(cfg.moments.find(x => x.id === m.id && x.type === 'first_past').units))) fail(`f${f}: first-past callout below the mark`);
          if (m.type === 'passes' && !(b && o && b.units > o.units)) fail(`f${f}: passes callout but ${m.id} not ahead of ${m.other}`);
          const cq = m.type === 'crown' ? crown.find(c => c.quarter_end === m.q) : null;
          const txt = S.L.filter(l => l.kind.startsWith('callout')).map(l => l.text).join('');
          if (cq && (cq.display_style !== 'official') !== txt.includes('estimated figures')) fail(`f${f}: callout "estimated figures" does not match crown.csv`);
          res.callouts.push({ q: m.q, id: m.id, type: m.type, f, text: txt });
        }
      }
    }
    // final-table line and footnote: only on the film's final table, with the gap from the data
    if (finalOn && (cfg.final_line || {}).enabled) {
      res.counts.final_frames++;
      const FL = cfg.final_line, a = BigInt(byQ[q][FL.id].units), bb = BigInt(byQ[q][FL.other].units), t = (bb - a) / 100000n;
      const want = `${FL.label} is ${byQ[q][FL.other].plus_flag === 'yes' ? 'at least ' : ''}${t / 10n}.${t % 10n} million behind the ${FL.other_label}`;
      const got = S.L.find(l => l.kind === 'final_line');
      if (!got || got.text !== want) fail(`f${f}: final line "${got && got.text}" != "${want}"`);
      const fn = S.L.find(l => l.kind === 'footnote');
      if (cfg.final_footnote && cfg.final_footnote.enabled && (!fn || fn.text !== cfg.final_footnote.mark + ' ' + cfg.final_footnote.text)) fail(`f${f}: footnote missing or wrong`);
    } else if (S.L.some(l => l.kind === 'final_line' || l.kind === 'footnote')) fail(`f${f}: final line or footnote outside the final table`);
    // 12. scoreboard: exact at quarter ends; totals counted in between
    if (S.K) {
      const mk = byMaker[q];
      const keys = S.K.rows.map(r => r.key);
      const totals = Object.fromEntries(S.K.rows.map(r => [r.key, r.total]));
      for (let i = 1; i < keys.length; i++) if (totals[keys[i]] > totals[keys[i - 1]]) fail(`f${f}: scoreboard out of order`);
      res.counts.key_rows += keys.length;
      for (const r of S.K.rows) {
        if (atEnd && String(r.total) !== mk[r.key]) fail(`f${f} ${q}: ${r.key} total ${r.total} != ${mk[r.key]}`);
        const ids = Object.keys(byQ[q]).filter(id => C[id].maker_key === r.key);
        const rank = { official: 0, estimated: 1, analyst_estimate: 2 };
        const st = ids.map(id => byQ[q][id].display_style).sort((a, b) => rank[b] - rank[a])[0];
        if (r.style !== st) fail(`f${f} ${q}: ${r.key} style ${r.style} != ${st}`);
        if (atEnd && r.plus !== ids.some(id => byQ[q][id].plus_flag === 'yes')) fail(`f${f} ${q}: ${r.key} plus wrong`);
        const tl = S.L.find(l => l.kind === 'key_total' && l.id === r.key);
        if (!tl || tl.text !== millions(String(r.total)) + (r.plus ? '+' : '')) fail(`f${f}: ${r.key} total label "${tl && tl.text}"`);
        const kn = S.L.find(l => l.kind === 'key_name' && l.id === r.key), ke = S.L.find(l => l.kind === 'key_est' && l.id === r.key);
        for (const x of [ke, tl]) if (x && kn && overlap(labelBox(kn), labelBox(x), 8)) fail(`f${f}: ${r.key} key name overlaps "${x.text}"`);
        if (!ke && st !== 'official') fail(`f${f}: ${r.key} total contains ${st} figures but is not marked`);
      }
    }
    // 10. layout
    const things = vis.map(b => ({ what: 'bar ' + b.id, r: b.rect })).concat(S.P.filter(p => p.alpha > 0).map(p => ({ what: 'picture ' + p.id, r: p.drawn })))
      .concat((S.LG || []).filter(g => g.alpha > 0).map(g => ({ what: 'logo tile ' + g.id, r: g.tile })))
      .concat(S.L.filter(l => ['name', 'value', 'est_label'].includes(l.kind) && l.alpha > 0).map(l => ({ what: l.kind + ' ' + l.id, r: labelBox(l) })));
    if (S.CR) things.push({ what: 'crown', r: S.CR });
    for (const l of S.L) { const bx = labelBox(l); if (bx.x < -0.5 || bx.x + bx.w > 1920.5 || bx.y < -0.5 || bx.y + bx.h > 1080.5) fail(`f${f}: ${l.kind} "${l.text}" outside the frame`); }
    const gapTo = (a, b) => Math.max(b.x - (a.x + a.w), a.x - (b.x + b.w), b.y - (a.y + a.h), a.y - (b.y + b.h));
    for (const t of things) {
      if (S.K) { if (overlap(t.r, S.K.box)) fail(`f${f}: ${t.what} enters the scoreboard`); else res.closest.key = Math.min(res.closest.key, gapTo(t.r, S.K.box)); }
      if (logo) { if (overlap(t.r, logo, cfg.overlay_gap)) fail(`f${f}: ${t.what} enters the logo box`); else res.closest.logo = Math.min(res.closest.logo, gapTo(t.r, logo)); }
    }
    const top = S.L.filter(l => ['callout', 'callout_extra', 'note', 'subtitle', 'final_line', 'footnote'].includes(l.kind) && l.alpha > 0.01);
    const others = S.L.filter(l => ['axis', 'title', 'time_line'].includes(l.kind));
    for (const a of top) for (const b of others.concat(top.filter(x => x !== a && x.kind !== a.kind && !(a.kind.startsWith('callout') && x.kind.startsWith('callout'))))) { const A = labelBox(a), B = labelBox(b);
      if (overlap(A, B)) fail(`f${f}: ${a.kind} overlaps ${b.kind} "${b.text}"`); else if (others.includes(b)) res.closest.callout = Math.min(res.closest.callout, gapTo(A, B)); }
    if (logo) for (const a of top) if (overlap(labelBox(a), logo)) fail(`f${f}: ${a.kind} enters the logo box`);
    prevDate = q; prevRank0 = S.R[0];
  }
  await br.close();
  // 11. pacing: count length per quarter, holds after the count on crown quarters, final table
  const P = cfg.pacing, base = d => { for (const s of P.segments || []) if (d <= s.to) return s.sec_per_event; return P.sec_per_event; };
  const shown = info.dates.filter(d => firstFrameOf[d] != null);
  if (shown.length !== info.dates.length) fail(`only ${shown.length} of ${info.dates.length} quarters shown`);
  const beats = [];
  for (let i = 0; i < info.dates.length; i++) {
    const d = info.dates[i], cnt = info.qend[i] - firstFrameOf[d] + 1;
    const lo = Math.round(base(d) * 0.8 * cfg.fps) - 1, hi = Math.round(base(d) * 1.4 * cfg.fps) + 1;
    if (cnt < lo || cnt > hi) fail(`${d}: counts over ${cnt} frames, outside ${lo}-${hi}`);
    if (i + 1 < info.dates.length) {
      const n = firstFrameOf[info.dates[i + 1]] - firstFrameOf[d], held = crown.some(c => c.quarter_end === d && c.previous_leader) && cfg.record_hold.enabled;
      if (n !== cnt + (held ? Math.round(cfg.record_hold.sec * cfg.fps) : 0) && Math.abs(n - cnt - (held ? Math.round(cfg.record_hold.sec * cfg.fps) : 0)) > 1) fail(`${d}: beat ${n} frames, count ${cnt}${held ? ' + hold' : ''}`);
    }
    beats.push({ d, n: cnt });
  }
  const lastF = firstFrameOf[info.dates[info.dates.length - 1]];
  if (info.raceFrames - lastF !== Math.round(P.final_board_sec * cfg.fps)) fail(`final table ${info.raceFrames - lastF} frames, want ${P.final_board_sec} s`);
  if (firstFrameOf[info.dates[0]] !== Math.round(P.lead_in_sec * cfg.fps)) fail(`first quarter after the opening lands at frame ${firstFrameOf[info.dates[0]]}`);
  const early = beats.filter(b => b.d <= '1988-12-31').map(b => b.n), late = beats.filter(b => b.d > '1988-12-31').map(b => b.n);
  res.beats = { early: early.length ? `${Math.min(...early)}-${Math.max(...early)} frames` : 'n/a', late: late.length ? `${Math.min(...late)}-${Math.max(...late)} frames` : 'n/a' };
  const want = wantMoments.map(m => m.q + ' ' + m.type + ' ' + m.id).sort().join(', '), got = res.callouts.map(m => m.q + ' ' + m.type + ' ' + m.id).sort().join(', ');
  if (want !== got) fail(`callouts [${got}] but the data and the approved moments give [${want}]`);
  if (res.callouts.some(c => c.id === 'nintendo_switch')) fail('the on-hold Switch passes DS moment was shown');
  const noCount = needBetween.filter(x => !between.has(x));
  if (noCount.length) fail(`${noCount.length} bars grew by 1 million or more in a quarter without counting through it, e.g. ${noCount.slice(0, 3).join('; ')}`);
  res.counted = needBetween.length;
  if (opts.atari && res.fadeStarts.atari_2600 !== '1991-12-31') fail(`Atari 2600 fades from ${res.fadeStarts.atari_2600}, want 1991-12-31`);
  if (isDataEnd && (cfg.final_line || {}).enabled && !res.counts.final_frames) fail('no final-table line on the final table');
  res.pass = res.failures.length === 0;
  return res;
}

function write(results) {
  const L = ['# RTT-003 player test results (IQ-10 round 2)', '',
    'Written by `node tests/player/run_tests_rtt003.js`. Every frame drawn in order at 1920 x 1080 in Playwright Chromium through `kits/rtt-002/rtt.js` (the same path as the render), with placeholder pictures and logos. Expected values read independently from `data/rtt-003/` (series.csv, consoles.csv, crown.csv, series_by_maker.csv). Round 2: the numbers count; on every quarter-end frame each value label must equal series.csv exactly (with "+" where plus_flag is yes); while counting, labels stay between the two quarter ends and never go backwards.', '',
    `Overall: ${results.filter(r => r.pass).length}/${results.length} PASS.`, '',
    '| Case | Result | Config | Quarters (opening → last) | Frames | Labels at quarter ends / while counting (with "+") / bars proven to count | Bar styles (official / estimated / analyst) | Analyst labels | Faded bar-frames | Pictures / logos checked | Crown leaders (frame) | Callouts (crossing frame) | Final-table frames | Fade starts | Counts (≤1988 / later) | Closest gap: scoreboard / logo / callout line | Tall-picture overlap |',
    '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|'];
  for (const r of results) L.push(`| ${r.name} | ${r.pass ? 'PASS' : 'FAIL'} | \`${r.config}\` | ${r.quarters} (${r.opening} → ${r.last}) | ${r.frames} (${(r.frames / 30).toFixed(1)} s) | ${r.counts.quarter_end_values} / ${r.counts.counting_values} (${r.counts.plus}) / ${r.counted} | ${r.counts.styles.official} / ${r.counts.styles.estimated} / ${r.counts.styles.analyst_estimate} | ${r.counts.est_labels} | ${r.counts.faded_frames} | ${r.counts.pics} / ${r.counts.logos} | ${r.crowns.map(c => c.id + ' f' + c.f).join(' → ')} | ${r.callouts.map(c => c.q + ' ' + c.id + ' f' + c.f).join('; ') || 'none'} | ${r.counts.final_frames} | ${Object.entries(r.fadeStarts).map(([k, v]) => k + ' ' + v).join('; ') || 'none'} | ${r.beats.early} / ${r.beats.late} | ${r.closest.key.toFixed(0)} / ${r.closest.logo.toFixed(0)} / ${r.closest.callout === 1e9 ? 'n/a' : r.closest.callout.toFixed(0)} px | ${r.tallOverlap.toFixed(1)} px |`);
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
    ['clip_A_1985_1992_1.5x', 'config_rtt003_clip_A_1985_1992_1.5x.json', { atari: true }],
    ['film_full_config', 'config_rtt003_film.json', { atari: true }]
  ].filter(c => process.argv.length <= 2 || process.argv.slice(2).includes(c[0]));
  const results = [];
  for (const [n, c, o] of cases) { const t0 = Date.now(); const r = await runCase(n, c, o); results.push(r);
    console.log(`${r.pass ? 'PASS' : 'FAIL'} ${n}: ${r.frames} frames in ${((Date.now() - t0) / 1000).toFixed(0)} s` + (r.pass ? '' : '\n  ' + r.failures.slice(0, 8).join('\n  '))); }
  if (process.argv.length <= 2) write(results);
  process.exit(results.every(r => r.pass) ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
