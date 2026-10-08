/* RTT-103 player tests (IQ-18, design round 1). Same method as run_tests_rtt001.js: every frame of each case is drawn in
 * order through the kit's own driver path (kits/rtt-002/rtt.js openPlayer) at 1920 x 1080, and what was drawn
 * (window.__LABELS, __BARS, __COMBINED, __STORY, __SLOTS, __DATEBLOCK) is checked against data/rtt-103/*.csv, read HERE,
 * independently of the adapter and of rtt_timeline.js:
 *
 *   0. the data is untouched: every data file the adapter reads has the SHA-256 in data/rtt-103/manifest.json, and the
 *      player input has the SHA-256 in kits/rtt-103/dataset_hashes.txt
 *   1. values: on every quarter-end frame each drawn value label equals the master's capex_TTM_usd for that quarter,
 *      formatted here ("$169.0bn": one decimal, half up on the whole dollars; option B whole billions from $10bn)
 *   2. no bar without a figure: on a quarter-end frame the board holds exactly the companies with a master row that
 *      quarter (late entrants from their first point, DEC-295; Alibaba absent for its seven gap points), except a bar
 *      held in the "hold" option, which is dimmed and carries no number; between quarter ends a bar has a figure in
 *      the quarter counted towards or the one before
 *   3. order: on every quarter-end frame the board's order (window.__RANK) puts no company above one with a larger figure
 *   4. combined: on every quarter-end frame "Combined capital spending" equals L_aggregate_capex.csv to the dollar and
 *      its label is that figure formatted as in 1; between quarter ends it stays between its two quarter-end values
 *   5. date: the date block reads "12 months to <Month>" (or "Q<n>") and the quarter's year on its quarter-end frame
 *   6. Tencent's note (DEC-292): on every frame Tencent's bar is drawn, its "measured differently" tag (option A) or its
 *      mark and footnote (option B) is drawn too
 *   7. story moments: each configured moment's quoted words (between “ and ”) appear word for word in
 *      G_AI_capex_story_events.csv; a moment shows only within its window; COMMITMENT and financing moments say
 *      "not capital spending"
 *   8. layout: no label outside the frame; nothing drawn overlaps the "Combined capital spending" panel or the story
 *      card (bars, names, values, tags); title and date block do not overlap
 *   9. colours: no two companies closer than CIEDE2000 18 (DEC-023); every colour at least 25 from the background
 *  10. pacing: each quarter counts over 0.8-1.4 x its base
 *  11. (IQ-18b) the total panel's text stays inside the panel; a story card's text is at least the names' size (DEC-357)
 *  12. (IQ-18b) the steps after the race: no card over a value, label or panel; the line and final-table figures as the
 *      look-ahead file and L give them (display rounding only); the cards quote G word for word (check 7); (IQ-18c) the
 *      explanation's points all drawn inside the frame
 *  13. (IQ-18c, DEC-371) the race carrying on after June 2026: on each forward board's landing frame every bar's value
 *      is the look-ahead file's range for that year (display rounding as rtt_steps.js bn(); Microsoft "~" in 2026,
 *      ByteDance "more than" from the race file's press report, 2026 board only); exactly those companies are on the
 *      board, ordered by the top of their range; Race Through Time estimates striped ("estimated"), Citi's in the
 *      analyst look, plans and actuals solid; Oracle's "probably high" exactly where the file's notes say so, Citi's
 *      note on Citi rows; the total is the file's combined range and never includes ByteDance; the date block reads the
 *      board's label and year; the source line under the title is on screen; every footer and source line stays
 *      inside the margins and the date block never meets the title (all frames)
 * Results: tests/player/RESULTS_RTT103.md. Exit 1 on any failure.
 *
 *   node tests/player/run_tests_rtt103.js [case ...]
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..', '..');
const KIT = path.join(ROOT, 'kits', 'rtt-002');
const K103 = path.join(ROOT, 'kits', 'rtt-103');
const rtt = require(path.join(KIT, 'rtt.js'));
const TLM = require(path.join(KIT, 'rtt_timeline.js'));
const { placeholderPNG, logoPlaceholders } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const D = path.join(ROOT, 'data', 'rtt-103');

function readCSV(file) {
  const t = fs.readFileSync(file, 'utf8').replace(/^﻿/, ''), rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < t.length; i++) { const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true; else if (c === ',') { row.push(f); f = ''; } else if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; } else if (c !== '\r') f += c; }
  if (f || row.length) { row.push(f); rows.push(row); }
  const h = rows.shift(); return rows.filter(r => r.length > 1).map(r => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}
const sha = f => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
/* "$169.0bn" from whole dollars, independently of the player: tenths of a billion, half up, in BigInt */
function moneyText(dollars, M) {
  const u = BigInt(dollars), pre = (M && M.prefix) || '$', suf = (M && M.suffix) || 'bn';
  if (M && M.decimals === 0 && (M.whole_from == null || u >= BigInt(M.whole_from) * 1000000000n)) { const b = (u + 500000000n) / 1000000000n; return pre + Number(b).toLocaleString('en-GB') + suf; }
  const t = (u + 50000000n) / 100000000n; return pre + Number(t / 10n).toLocaleString('en-GB') + '.' + (t % 10n) + suf;
}
const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];

const CASES = {
  base: { config: 'config_rtt103_base.json' },
  film: { config: 'config_rtt103_film.json' },
  clip_2025_end: { config: 'config_rtt103_clip_2025_end.json' },
};

const master = readCSV(path.join(D, 'AI_SPENDING_RACE_MASTER.csv'));
const byDate = {}; for (const r of master) (byDate[r.date] = byDate[r.date] || {})[r.company.toLowerCase()] = r.capex_TTM_usd;
const L = {}; for (const r of readCSV(path.join(D, 'L_aggregate_capex.csv'))) L[r.quarter] = r.aggregate_TTM_capex_usd;
const G = readCSV(path.join(D, 'G_AI_capex_story_events.csv'));
const LOOK = readCSV(path.join(D, 'AI_SPENDING_RACE_LOOKAHEAD.csv'));
const FORECAST = readCSV(path.join(D, 'AI_SPENDING_RACE_FORECAST.csv'));
const storyLate = {};
const qOf = d => d.slice(0, 4) + '-Q' + Math.ceil(+d.slice(5, 7) / 3);

function global() {
  const fails = [];
  const man = JSON.parse(fs.readFileSync(path.join(D, 'manifest.json'), 'utf8'));
  const files = JSON.stringify(man);
  for (const f of ['AI_SPENDING_RACE_MASTER.csv', 'L_aggregate_capex.csv', 'AI_SPENDING_RACE_LOOKAHEAD.csv', 'AI_SPENDING_RACE_FORECAST.csv', 'AI_SPENDING_RACE_PEAK_VIEWS.csv', 'G_AI_capex_story_events.csv']) {
    const h = sha(path.join(D, f)); if (!files.includes(h)) fails.push('0: ' + f + ' SHA-256 ' + h.slice(0, 12) + ' not in data/rtt-103/manifest.json');
  }
  const want = fs.readFileSync(path.join(K103, 'dataset_hashes.txt'), 'utf8').split('\n').find(l => l.endsWith('race_rtt103.json'));
  if (!want || want.split(' ')[0] !== sha(path.join(K103, 'race_rtt103.json'))) fails.push('0: race_rtt103.json differs from dataset_hashes.txt');
  for (const l of fs.readFileSync(path.join(K103, 'dataset_hashes.txt'), 'utf8').split('\n').filter(l => / input /.test(l))) {
    const [h, , p] = l.split(' '); if (sha(path.join(ROOT, p)) !== h) fails.push('0: ' + p + ' changed since the adapter ran');
  }
  /* render settings: every clip config carries the encoder settings rtt.js passes to ffmpeg (run 1 of rtt103_pilot.yml
     failed without them, IQ-18) */
  for (const c of fs.readFileSync(path.join(K103, 'clips.txt'), 'utf8').split('\n').filter(Boolean)) {
    const cf = rtt.loadConfig(path.join(K103, c)); if (cf.crf == null || !cf.preset) fails.push('0: ' + c + ' has no crf/preset for ffmpeg');
  }
  /* 9. colours */
  const base = rtt.loadConfig(path.join(K103, 'config_rtt103_base.json'));
  const cols = base.palette.map(c => TLM.drawnColour(c));
  let minDE = 1e9, minBG = 1e9;
  for (let i = 0; i < cols.length; i++) { minBG = Math.min(minBG, TLM.deltaE(cols[i], '#0b1424')); for (let j = i + 1; j < cols.length; j++) minDE = Math.min(minDE, TLM.deltaE(cols[i], cols[j])); }
  if (minDE < 18) fails.push('9: two company colours closer than CIEDE2000 18 (' + minDE.toFixed(1) + ')');
  if (minBG < 25) fails.push('9: a company colour closer than 25 to the background (' + minBG.toFixed(1) + ')');
  /* 7. quotes word for word in G (IQ-18b, DEC-357: trimmed with "…"): every quoted fragment of a story card or a step card
     appears in ONE row of G; COMMITMENT and financing rows say "not capital spending", the ESTIMATE row "estimate" */
  const film = rtt.loadConfig(path.join(K103, 'config_rtt103_film.json'));
  const cards = film.story.items.filter(it => !it.plain).concat((film.steps.plans || {}).cards || []);
  for (const it of cards) {
    const q = (String(it.text).match(/“([^”]+)”/) || [])[1];
    if (!q) { fails.push('7: ' + it.when + ' has no quote'); continue; }
    const frags = q.split('…').map(x => x.trim()).filter(x => x.split(' ').length >= 2);
    const g = G.find(g => frags.every(fr => g.event.includes(fr)));
    if (!g) { fails.push('7: ' + it.when + ' quote not word for word in one row of G: ' + q); continue; }
    if (/COMMITMENT|financing/.test(g.event_type) && !/not capital spending/.test(it.tag || '')) fails.push('7: ' + it.when + ' is ' + g.event_type + ' but not labelled "not capital spending"');
    if (/ESTIMATE/.test(g.event_type) && !/estimate/i.test((it.tag || '') + it.who)) fails.push('7: ' + it.when + ' is an estimate but not labelled so');
    const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], gd = (+g.date.slice(8, 10)) + ' ' + MON[+g.date.slice(5, 7) - 1] + ' ' + g.date.slice(0, 4);
    if (it.when !== gd) fails.push('7: card dated ' + it.when + ', G row dated ' + g.date);
  }
  return { fails, minDE, minBG };
}

async function runCase(name) {
  const C = CASES[name], cfg = rtt.loadConfig(path.join(K103, C.config));
  const dir = path.join(ROOT, 'tests', 'output', 'rtt103', '_assets'); fs.mkdirSync(dir, { recursive: true });
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  logoPlaceholders(cfg, dir);
  const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
  process.env.RTT_LOCAL_ASSETS = dir;
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
  delete process.env.RTT_LOCAL_ASSETS;
  const info = await pg.evaluate(() => ({ dates: TL.events.map(e => e.date), start: TL.startFrame, qe: TL.quarterEndFrame, frames: RACE_FRAMES, opening: TL.openingEvent.date, mult: TL.mult, gaps: TL.gaps, fwd: TL.events.map(e => !!e.fwd) }));
  const boards = {}; for (const b of (cfg.forward && cfg.forward.enabled ? cfg.forward.boards : [])) boards[b.year + '-12-31'] = b;
  let fwdChecked = 0;
  const fails = [], add = m => { if (fails.length < 40) fails.push(m); };
  const M = (cfg.values || {}).money, hold = cfg.gaps && cfg.gaps.mode === 'hold';
  const inGap = (id, d) => (info.gaps || []).some(g => g.id === id && d >= g.from && d <= g.to);
  const qeAt = {}; info.qe.forEach((f, k) => { qeAt[f] = k; });
  let checked = 0, prevComb = null;
  const tagOn = (cfg.bar_tags || []).find(t => t.id === 'tencent');
  const steps = await pg.evaluate(() => TL.stepPlan ? { end: TL.raceEnd, plan: TL.stepPlan } : null);
  if (steps) steps.cfg = cfg.steps;
  const stepSeen = {};
  for (let f = 0; f < info.frames; f++) {
    await rtt.drawFrame(pg, f, cfg);
    const k = qeAt[f];
    const S = await pg.evaluate(() => ({ L: window.__LABELS, B: window.__BARS, C: window.__COMBINED, ST: window.__STORY, DB: window.__DATEBLOCK, TF: window.__TAGFOOT, R: window.__RANK, CB: window.__CARDBOX, STEP: window.__STEP, CARDS: window.__CARDS, PANELS: window.__PANELS }));
    for (const l of S.L) if (l.x < -1 || l.x + l.w > 1921 || l.y > 1081 || l.y < 0) add(f + ': label outside the frame: ' + l.kind + ' "' + l.text + '"');
    /* 13. footers and source lines inside the margins; the date block clear of the title */
    for (const l of S.L) if (['footer', 'source_line'].includes(l.kind) && l.alpha > 0.05 && l.x + l.w > 1920 - 64 + 1) add(f + ': ' + l.kind + ' past the right margin: "' + l.text.slice(0, 40) + '"');
    const tl_ = S.L.find(l => l.kind === 'title'), dm_ = S.L.find(l => l.kind === 'date_month');
    if (tl_ && dm_ && overlap(lbox(tl_), lbox(dm_))) add(f + ': the date block "' + dm_.text + '" meets the title');
    if (steps && f >= steps.end) { stepChecks(f, S, steps, stepSeen, add); continue; }
    /* 11. the panel's own text stays inside it (Cowork fix (g)); a story card's text is at least the names' size (DEC-357) */
    if (S.C) for (const l of S.L) if (/^comb_/.test(l.kind) && l.kind !== 'comb_axis' && l.alpha > 0.05 && (l.x < S.C.box.x || l.x + l.w > S.C.box.x + S.C.box.w + 1)) add(f + ': ' + l.kind + ' "' + l.text + '" outside the total panel');
    if (S.CB) for (const l of S.L) if (/^story_/.test(l.kind) && l.alpha > 0.05 && (l.x < S.CB.x || l.x + l.w > S.CB.x + S.CB.w + 1)) add(f + ': ' + l.kind + ' "' + l.text + '" outside its card');
    if (S.CB) { const nm = S.L.filter(l => l.kind === 'name' && l.alpha > 0.5).map(l => l.size), st = S.L.filter(l => /^story_(text|who)$/.test(l.kind)).map(l => l.size);
      if (nm.length && st.length && Math.min(...st) < Math.min(...nm)) add(f + ': story card text ' + Math.min(...st) + ' px, smaller than the names ' + Math.min(...nm) + ' px'); }
    const drawn = S.B.filter(b => b.alpha > 0.02 && b.rect.y < 1034);
    /* 8. nothing overlaps the combined panel or the story card */
    const boxes = []; if (S.C) boxes.push(['combined', S.C.box]);
    if (S.ST && S.ST.mode === 'card' && S.CB) boxes.push(['story card', S.CB]);
    for (const [nm, bx] of boxes) {
      for (const b of drawn) if (b.rect.x < bx.x + bx.w && b.rect.x + b.rect.w > bx.x && b.rect.y < bx.y + bx.h && b.rect.y + b.rect.h > bx.y) add(f + ': bar ' + b.id + ' under the ' + nm);
      for (const l of S.L) if (['name', 'value', 'bar_tag', 'gap_note', 'entry_tag', 'fwd_note'].includes(l.kind) && l.alpha > 0.05 && l.x < bx.x + bx.w && l.x + l.w > bx.x && l.y > bx.y && l.y - l.size * 0.8 < bx.y + bx.h) add(f + ': ' + l.kind + ' "' + l.text + '" under the ' + nm);
    }
    /* 6. Tencent's note */
    if (tagOn && drawn.some(b => b.id === 'tencent' && b.alpha > 0.5)) {
      if ((tagOn.mode || 'after') === 'after' && !S.L.some(l => l.kind === 'bar_tag' && l.id === 'tencent')) add(f + ': Tencent drawn without its note');
      if (tagOn.mode === 'mark' && !(S.L.some(l => l.kind === 'value' && l.id === 'tencent' && l.text.endsWith(tagOn.mark)) && (S.TF || []).length)) add(f + ': Tencent drawn without its mark and footnote');
    }
    const kk0 = RTT_eventAt(info, f);
    if (kk0 >= 0 && info.fwd[kk0]) {   // 13. a forward board (IQ-18c)
      const d = info.dates[kk0], B = boards[d], dp = info.dates[kk0 - 1];
      if (k == null) { const ok = new Set(fwdIds(d).concat(info.fwd[kk0 - 1] ? fwdIds(dp) : Object.keys(byDate[dp] || {})));
        for (const b of drawn) if (!ok.has(b.id)) add(f + ': bar ' + b.id + ' drawn with no figure in ' + dp + ' or ' + d);
        continue; }
      fwdChecked++; fwdCheck(d, B, S, drawn, add); continue;
    }
    if (k == null) {          // between quarter ends: every bar has a figure now or at the quarter before (or is held)
      const kk = RTT_eventAt(info, f), d = kk >= 0 ? info.dates[kk] : info.opening, dp = kk > 0 ? info.dates[kk - 1] : info.opening;
      for (const b of drawn) if (!(b.id in (byDate[d] || {})) && !(b.id in (byDate[dp] || {})) && !(hold && (inGap(b.id, d) || inGap(b.id, dp)))) add(f + ': bar ' + b.id + ' drawn with no figure in ' + dp + ' or ' + d);
      if (S.C && prevComb) { const v = S.C.value; if (v < Math.min(prevComb.a, prevComb.b) - 1 || v > Math.max(prevComb.a, prevComb.b) + 1) add(f + ': combined ' + v + ' outside its two quarter ends'); }
      continue;
    }
    checked++;
    const d = info.dates[k], fig = byDate[d], q = qOf(d);
    /* 2. exactly the companies with a figure (plus held bars) */
    const want = Object.keys(fig).sort(), got = drawn.filter(b => b.alpha > 0.5 && !(b.held >= 0.5)).map(b => b.id).sort();
    if (want.join() !== got.join()) add(d + ': board ' + got.join(',') + ' but the master has ' + want.join(','));
    for (const b of drawn) if (b.held >= 0.5 && !(hold && inGap(b.id, d))) add(d + ': ' + b.id + ' held outside a gap');
    /* 1. values */
    for (const id of want) { const l = S.L.find(l => l.kind === 'value' && l.id === id), t = moneyText(fig[id], M);
      if (!l || l.text.replace(/\*$/, '') !== t) add(d + ' ' + id + ': value "' + (l && l.text) + '", master ' + t); }
    for (const l of S.L) if (l.kind === 'value' && !(l.id in fig)) add(d + ': a number drawn for ' + l.id + ', which has no figure');
    /* 3. order (the board's target order; rows then glide into it over glide.rank_sec) */
    const rows = S.R.filter(id => id in fig);
    for (let i = 1; i < rows.length; i++) if (BigInt(fig[rows[i]]) > BigInt(fig[rows[i - 1]])) add(d + ': ' + rows[i] + ' below ' + rows[i - 1] + ' with a larger figure');
    /* 4. combined */
    if (S.C) { if (String(S.C.value) !== L[q] || !S.C.exact) add(d + ': combined ' + S.C.value + ', L_aggregate_capex.csv ' + L[q]);
      const lab = S.L.find(l => l.kind === 'comb_value'); if (!lab || lab.text !== moneyText(L[q], M)) add(d + ': combined label "' + (lab && lab.text) + '", want ' + moneyText(L[q], M));
      prevComb = { a: +L[q], b: k + 1 < info.dates.length ? +L[qOf(info.dates[k + 1])] : +L[q] }; }
    /* 5. date */
    if (cfg.date_block && cfg.date_block.enabled !== false) {
      const ml = S.L.find(l => l.kind === 'date_month'), yl = S.L.find(l => l.kind === 'date_year');
      const wantM = cfg.date_block.label === 'quarter' ? 'Q' + Math.ceil(+d.slice(5, 7) / 3) : '12 months to ' + (cfg.date_block.months_short || MONTHS)[+d.slice(5, 7) - 1];
      if (!ml || ml.text !== wantM || !yl || yl.text !== d.slice(0, 4)) add(d + ': date "' + (ml && ml.text) + ' ' + (yl && yl.text) + '"');
    }
  }
  /* 7. story windows: each moment from its own quarter (+ delay) or later, never two on one lane at once, shown whole
     before the race ends; lateness = seconds after its own quarter's first frame (DEC-358: reported) */
  if (cfg.story && cfg.story.enabled) {
    const Q = await pg.evaluate(() => storySchedule().map(q => ({ when: q.it.when, at: q.it.at, plain: !!q.it.plain, delay: q.it.delay || 0, sec: q.it.sec, f0: q.f0 })));
    const prevEnd = {}, late = [];
    for (const q of Q) { const kk = info.dates.indexOf(q.at), own = info.start[kk] + Math.round(q.delay * 30), lane = q.plain ? 'plain' : 'card';
      if (q.f0 < own) add('story ' + (q.when || q.at) + ': shown before its quarter');
      if (q.f0 < (prevEnd[lane] || -1)) add('story ' + (q.when || q.at) + ': overlaps the moment before');
      prevEnd[lane] = q.f0 + Math.round((q.sec != null ? q.sec : cfg.story.sec) * 30);
      if (steps && prevEnd[lane] > steps.end) add('story ' + (q.when || q.at) + ': still showing when the race ends');
      if (!q.plain) late.push(q.when + ' ' + ((q.f0 - own) / 30).toFixed(1) + ' s');
      await rtt.drawFrame(pg, q.f0 + 6, cfg); const st = await pg.evaluate(() => window.__STORY);
      if (!st || (q.plain ? !(st.plain && st.plain.at === q.at) : st.when !== q.when)) add('story ' + (q.when || q.at) + ': not drawn on its frames'); }
    storyLate[name] = late.join('; ');
  }
  /* 10. pacing */
  const P = cfg.pacing, base = d => { for (const s of P.segments || []) if ((s.to == null || d <= s.to) && (s.from == null || d >= s.from)) return s.sec_per_event; return P.sec_per_event; };
  for (let kk = 0; kk + 1 < info.start.length; kk++) { if (info.fwd[kk]) continue; const sec = (info.start[kk + 1] - info.start[kk]) / 30, b = base(info.dates[kk]);
    if (sec < 0.8 * b - 0.04 || sec > 1.4 * b + 0.04) add('pacing ' + info.dates[kk] + ': ' + sec.toFixed(2) + ' s, base ' + b); }
  await br.close();
  if (steps) for (const p of steps.plan) if (['explain', 'line', 'final'].includes(p.name) && !stepSeen[p.name]) add('step ' + p.name + ': never checked');
  if (Object.keys(boards).length && fwdChecked !== info.fwd.filter(Boolean).length) add('forward boards: ' + fwdChecked + ' landing frames checked of ' + info.fwd.filter(Boolean).length);
  return { name, config: C.config, frames: info.frames, quarters: checked, fwd: fwdChecked, fails, late: storyLate[name], steps: steps ? steps.plan.length : 0 };
}
/* 12. the steps after the race (IQ-18b): no card over a value, label or panel; the panel's text inside it; the figures as
   the look-ahead file gives them (display rounding as rtt_steps.js documents it); the final line from L */
function bnT(lo, hi, mode) {
  const big = mode === 'est' && Math.max(lo, hi) >= 1000, f = v => { const t = Math.round(v * 10);
    if (big) return (Math.floor((t + 50) / 100) / 100).toFixed(2);
    if (mode === 'whole' || (mode === 'est' && v >= 10)) return String(Math.floor((t + 5) / 10));
    if (mode === 'est' || mode === 'actual') return (t / 10).toFixed(1);
    return t % 10 ? (t / 10).toFixed(1) : String(t / 10); };
  const a = f(lo), b = f(hi); return (mode === 'est' ? '~' : '') + '$' + (a === b ? a : a + '–' + b) + (big ? 'tn' : 'bn');
}
const overlap = (a, b) => a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
const lbox = l => ({ x: l.x, y: l.y - l.size * 0.8, w: l.w, h: l.size });
function stepChecks(f, S, steps, seen, add) {
  const st = S.STEP || {}, plan = steps.plan[st.index], u = st.u;
  for (const c of S.CARDS || []) { for (const l of S.L) if (['value', 'period', 'name', 'tag', 'axis', 'comb_value', 'comb_label', 'comb_note'].includes(l.kind) && overlap(c, lbox(l))) add(f + ': card ' + c.when + ' over ' + l.kind + ' "' + l.text + '"');
    for (const p of S.PANELS || []) if (overlap(c, p)) add(f + ': card ' + c.when + ' over the total panel');
    for (const l of S.L) if (/^card_/.test(l.kind) && l.x >= c.x && l.x < c.x + c.w && l.x + l.w > c.x + c.w + 1) add(f + ': ' + l.kind + ' "' + l.text + '" outside its card'); }
  for (const p of S.PANELS || []) for (const l of S.L) if (/^comb_/.test(l.kind) && l.x >= p.x - 1 && l.x < p.x + p.w && l.x + l.w > p.x + p.w + 1) add(f + ': ' + l.kind + ' "' + l.text + '" outside its panel');
  if (!plan || st.dip > 0.01) return;
  const vals = {}; for (const l of S.L) if (l.kind === 'value' && l.id) vals[l.id] = l.text;
  if (plan.name === 'explain' && u > 3.0 && !seen.explain) { seen.explain = 1; const want = (steps.cfg.explain || {}).items || [];
    const leads = S.L.filter(l => l.kind === 'explain_lead' && l.alpha > 0.9).map(l => l.text);
    if (leads.join('|') !== want.map(i => i.lead).join('|')) add('explain: points drawn ' + leads.join(', '));
    if (!(S.STEP.bottom < 1080 - 80)) add('explain: the points run into the footer (' + S.STEP.bottom + ')'); }
  if (plan.name === 'line' && u > 1.5 && !seen.line) { seen.line = 1; if (!S.L.some(l => l.kind === 'value' && l.text === '$903–937bn')) add('line: the 2026 plans label is not "$903–937bn"'); }
  if (plan.name === 'final' && !seen.final) { seen.final = 1; const fl = S.L.find(l => l.kind === 'final_line');
    const want = 'Combined: ' + moneyText(L['2026-Q2']) + ' in the 12 months to June 2026, up from ' + moneyText(L['2025-Q2']) + ' a year earlier';
    if (!fl || fl.text !== want) add('final line: "' + (fl && fl.text) + '", want "' + want + '"');
    if ((S.CARDS || []).length || (S.ST && S.ST.at)) add('final table: a story card is showing'); }
}
/* 13. the forward boards (IQ-18c), read from the look-ahead file here, independently of rtt_timeline.js */
const BD = FORECAST.find(r => r.company === 'ByteDance' && r.forecast_year === '2026');
function fwdRows(d) { return LOOK.filter(r => r.frame_year === d.slice(0, 4) && r.row_type !== 'COMBINED'); }
function fwdIds(d) { return fwdRows(d).map(r => r.company.toLowerCase()).concat(d.slice(0, 4) === '2026' ? ['bytedance'] : []); }
function fwdCheck(d, B, S, drawn, add) {
  const y = d.slice(0, 4), est = B.kind === 'estimate', rows = fwdRows(d), vals = {}, notes = {};
  for (const l of S.L) if (l.kind === 'value' && l.id) vals[l.id] = l.text;
  for (const l of S.L) if (l.kind === 'fwd_note' && l.id) notes[l.id] = l.text;
  const want = fwdIds(d).sort(), got = drawn.filter(b => b.alpha > 0.5).map(b => b.id).sort();
  if (want.join() !== got.join()) add(y + ': board ' + got.join(',') + ', the look-ahead file has ' + want.join(','));
  for (const r of rows) { const id = r.company.toLowerCase(), citi = r.row_type === 'CITI_ESTIMATE' || r.label === 'Citi estimate';
    const mode = est ? (citi ? 'actual' : 'est') : (r.label === 'actual' ? 'actual' : 'plan');
    const w = (!est && id === 'microsoft' ? '~' : '') + bnT(+r.estimate_low_usd_bn, +r.estimate_high_usd_bn, mode);
    if (vals[id] !== w) add(y + ' ' + id + ': value "' + vals[id] + '", want "' + w + '"');
    const bar = drawn.find(b => b.id === id), st = citi ? 'analyst_estimate' : est ? 'estimated' : 'official';
    if (!bar || bar.style !== st) add(y + ' ' + id + ': drawn as ' + (bar && bar.style) + ', want ' + st);
    const ph = /Probably high/i.test(r.notes || '');
    if (ph !== /probably high/.test(notes[id] || '')) add(y + ' ' + id + ': "probably high" ' + (ph ? 'missing' : 'where the file does not say so'));
    if (citi && !/Citi estimate/.test(notes[id] || '')) add(y + ' ' + id + ': Citi row without "Citi estimate"'); }
  if (y === '2026') { const wb = 'more than ' + bnT(+BD.forecast_amount_usd_bn, +BD.forecast_amount_usd_bn, 'actual');
    if (vals.bytedance !== wb) add('2026 ByteDance: "' + vals.bytedance + '", want "' + wb + '"');
    const b = drawn.find(b => b.id === 'bytedance'); if (!b || b.style !== 'press' || !/press report/.test(notes.bytedance || '')) add('2026 ByteDance not greyed and marked "press report"'); }
  const order = S.R.filter(id => id !== 'bytedance'), top = id => +(rows.find(r => r.company.toLowerCase() === id) || {}).estimate_high_usd_bn;
  for (let i = 1; i < order.length; i++) if (top(order[i]) > top(order[i - 1])) add(y + ': ' + order[i] + ' below ' + order[i - 1] + ' with a higher top of range');
  const C = LOOK.find(r => r.frame_year === y && r.row_type === 'COMBINED'), cv = S.L.find(l => l.kind === 'comb_value');
  const wc = bnT(+C.estimate_low_usd_bn, +C.estimate_high_usd_bn, est ? 'est' : 'whole');
  if (!cv || cv.text !== wc) add(y + ': combined "' + (cv && cv.text) + '", want "' + wc + '"');
  const sum = rows.reduce((a, r) => a + Math.round(+r.estimate_high_usd_bn * 10), 0) * 1e8;
  if (!S.C || Math.abs(S.C.value - sum) > 1e8 * rows.length || Math.abs(S.C.value - Math.round(+C.estimate_high_usd_bn * 10) * 1e8) > 1) add(y + ': the total is not the file\'s combined row (or includes ByteDance)');
  const ml = S.L.find(l => l.kind === 'date_month'), yl = S.L.find(l => l.kind === 'date_year');
  if (!ml || ml.text !== B.month || !yl || yl.text !== y) add(y + ': date block "' + (ml && ml.text) + ' ' + (yl && yl.text) + '"');
  if (!S.L.some(l => l.kind === 'source_line' && l.alpha > 0.9)) add(y + ': no source line under the title');
  if (est && !/estimates/.test((S.L.find(l => l.kind === 'source_line') || {}).text || '')) add(y + ': the source line does not say these are estimates');
  if (y === '2030' && !S.L.some(l => /least reliable/.test(l.text))) add('2030: "least reliable" not on screen');
}
function RTT_eventAt(info, f) { let k = -1; for (let i = 0; i < info.start.length; i++) if (info.start[i] <= f) k = i; else break; return k; }

(async () => {
  const only = process.argv.slice(2);
  const g = global(), res = [];
  for (const n of Object.keys(CASES).filter(n => !only.length || only.includes(n))) { const r = await runCase(n); res.push(r);
    console.log((r.fails.length ? 'FAIL ' : 'PASS ') + n + ' (' + r.frames + ' frames, ' + r.quarters + ' quarter ends)'); r.fails.slice(0, 8).forEach(m => console.log('   ' + m)); }
  const ok = !g.fails.length && res.every(r => !r.fails.length);
  g.fails.forEach(m => console.log('FAIL ' + m));
  const out = ['# RTT-103 player tests (IQ-18 round 1, IQ-18b round 2, IQ-18c round 3)', '', 'Run: `node tests/player/run_tests_rtt103.js`. Checks 0-12 are listed at the top of the script.', '',
    '- Data untouched and player input as recorded (check 0), colours (check 9: closest pair CIEDE2000 ' + g.minDE.toFixed(1) + ', closest to the background ' + g.minBG.toFixed(1) + '), story and step cards quoted word for word from G (check 7): ' + (g.fails.length ? 'FAIL' : 'PASS'), '',
    '| Case | Config | Frames | Quarter ends checked | Result |', '|---|---|---|---|---|',
    ...res.map(r => `| ${r.name} | \`${r.config}\` | ${r.frames} | ${r.quarters}${r.fwd ? ' + ' + r.fwd + ' forward boards' : ''} | ${r.fails.length ? 'FAIL: ' + r.fails.slice(0, 3).join('; ') : 'PASS'}${r.late != null ? ' (story cards start after their own quarter by: ' + r.late + ')' : ''}${r.steps ? ' · ' + r.steps + ' steps after the race checked' : ''} |`), '',
    `**${ok ? 'PASS' : 'FAIL'}**: ${res.filter(r => !r.fails.length).length + (g.fails.length ? 0 : 1)}/${res.length + 1}`];
  if (!only.length) fs.writeFileSync(path.join(__dirname, 'RESULTS_RTT103.md'), out.join('\n') + '\n');
  console.log(ok ? 'ALL PASS' : 'FAILURES');
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
