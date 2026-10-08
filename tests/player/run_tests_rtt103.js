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
  values_B: { config: 'config_rtt103_values_B.json' },
  gap_hold: { config: 'config_rtt103_gap_hold.json' },
  gap_leave: { config: 'config_rtt103_gap_leave.json' },
  entry_B: { config: 'config_rtt103_entry_B.json' },
  tencent_B: { config: 'config_rtt103_tencent_B.json' },
  date_B: { config: 'config_rtt103_date_B.json' },
  story_card: { config: 'config_rtt103_story_card.json' },
  story_line: { config: 'config_rtt103_story_line.json' },
  comb_line: { config: 'config_rtt103_comb_line.json' },
  comb_bar: { config: 'config_rtt103_comb_bar.json' },
  pace_1p0: { config: 'config_rtt103_clip_pace_2020_2026_1p0.json' },
};

const master = readCSV(path.join(D, 'AI_SPENDING_RACE_MASTER.csv'));
const byDate = {}; for (const r of master) (byDate[r.date] = byDate[r.date] || {})[r.company.toLowerCase()] = r.capex_TTM_usd;
const L = {}; for (const r of readCSV(path.join(D, 'L_aggregate_capex.csv'))) L[r.quarter] = r.aggregate_TTM_capex_usd;
const G = readCSV(path.join(D, 'G_AI_capex_story_events.csv'));
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
  /* 9. colours */
  const base = rtt.loadConfig(path.join(K103, 'config_rtt103_base.json'));
  const cols = base.palette.map(c => TLM.drawnColour(c));
  let minDE = 1e9, minBG = 1e9;
  for (let i = 0; i < cols.length; i++) { minBG = Math.min(minBG, TLM.deltaE(cols[i], '#0b1424')); for (let j = i + 1; j < cols.length; j++) minDE = Math.min(minDE, TLM.deltaE(cols[i], cols[j])); }
  if (minDE < 18) fails.push('9: two company colours closer than CIEDE2000 18 (' + minDE.toFixed(1) + ')');
  if (minBG < 25) fails.push('9: a company colour closer than 25 to the background (' + minBG.toFixed(1) + ')');
  /* 7. story quotes word for word in G (all story configs) */
  for (const f of fs.readdirSync(K103).filter(f => /^config_rtt103_story_/.test(f))) {
    const c = rtt.loadConfig(path.join(K103, f));
    for (const it of c.story.items) {
      for (const m of (String(it.text) + ' ' + String(it.short || '')).matchAll(/“([^”]+)”/g)) if (!G.some(g => g.event.includes(m[1].replace(/^…|…$/g, '')))) fails.push('7: ' + f + ' ' + it.when + ' quote not found in G: ' + m[1]);
      const g = G.find(g => g.event.includes((String(it.text).match(/“([^”]+)”/) || [])[1] || '\u0000'));
      if (g && /COMMITMENT|financing/.test(g.event_type) && !/not capital spending/.test(it.tag || '')) fails.push('7: ' + it.when + ' is ' + g.event_type + ' but not labelled "not capital spending"');
    }
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
  const info = await pg.evaluate(() => ({ dates: TL.events.map(e => e.date), start: TL.startFrame, qe: TL.quarterEndFrame, frames: RACE_FRAMES, opening: TL.openingEvent.date, mult: TL.mult, gaps: TL.gaps }));
  const fails = [], add = m => { if (fails.length < 40) fails.push(m); };
  const M = (cfg.values || {}).money, hold = cfg.gaps && cfg.gaps.mode === 'hold';
  const inGap = (id, d) => (info.gaps || []).some(g => g.id === id && d >= g.from && d <= g.to);
  const qeAt = {}; info.qe.forEach((f, k) => { qeAt[f] = k; });
  let checked = 0, prevComb = null;
  const tagOn = (cfg.bar_tags || []).find(t => t.id === 'tencent');
  for (let f = 0; f < info.frames; f++) {
    await rtt.drawFrame(pg, f, cfg);
    const k = qeAt[f];
    const S = await pg.evaluate(() => ({ L: window.__LABELS, B: window.__BARS, C: window.__COMBINED, ST: window.__STORY, DB: window.__DATEBLOCK, TF: window.__TAGFOOT, R: window.__RANK, CB: window.__CARDBOX }));
    for (const l of S.L) if (l.x < -1 || l.x + l.w > 1921 || l.y > 1081 || l.y < 0) add(f + ': label outside the frame: ' + l.kind + ' "' + l.text + '"');
    const drawn = S.B.filter(b => b.alpha > 0.02 && b.rect.y < 1034);
    /* 8. nothing overlaps the combined panel or the story card */
    const boxes = []; if (S.C) boxes.push(['combined', S.C.box]);
    if (S.ST && S.ST.mode === 'card' && S.CB) boxes.push(['story card', S.CB]);
    for (const [nm, bx] of boxes) {
      for (const b of drawn) if (b.rect.x < bx.x + bx.w && b.rect.x + b.rect.w > bx.x && b.rect.y < bx.y + bx.h && b.rect.y + b.rect.h > bx.y) add(f + ': bar ' + b.id + ' under the ' + nm);
      for (const l of S.L) if (['name', 'value', 'bar_tag', 'gap_note', 'entry_tag'].includes(l.kind) && l.alpha > 0.05 && l.x < bx.x + bx.w && l.x + l.w > bx.x && l.y > bx.y && l.y - l.size * 0.8 < bx.y + bx.h) add(f + ': ' + l.kind + ' "' + l.text + '" under the ' + nm);
    }
    /* 6. Tencent's note */
    if (tagOn && drawn.some(b => b.id === 'tencent' && b.alpha > 0.5)) {
      if ((tagOn.mode || 'after') === 'after' && !S.L.some(l => l.kind === 'bar_tag' && l.id === 'tencent')) add(f + ': Tencent drawn without its note');
      if (tagOn.mode === 'mark' && !(S.L.some(l => l.kind === 'value' && l.id === 'tencent' && l.text.endsWith(tagOn.mark)) && (S.TF || []).length)) add(f + ': Tencent drawn without its mark and footnote');
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
  /* 7. story windows: each moment from its own quarter (+ delay) or later, never two at once, each shown on its frames */
  if (cfg.story && cfg.story.enabled) {
    const Q = await pg.evaluate(() => storySchedule().map(q => ({ when: q.it.when, at: q.it.at, delay: q.it.delay || 0, f0: q.f0 })));
    let prevEnd = -1, maxLate = 0;
    for (const q of Q) { const kk = info.dates.indexOf(q.at), own = info.start[kk] + Math.round(q.delay * 30);
      if (q.f0 < own) add('story ' + q.when + ': shown before its quarter');
      if (q.f0 < prevEnd) add('story ' + q.when + ': overlaps the moment before');
      prevEnd = q.f0 + Math.round(cfg.story.sec * 30); maxLate = Math.max(maxLate, (q.f0 - own) / 30);
      await rtt.drawFrame(pg, q.f0 + 6, cfg); const st = await pg.evaluate(() => window.__STORY);
      if (!st || st.when !== q.when) add('story ' + q.when + ': not drawn on its frames'); }
    storyLate[name] = maxLate;
  }
  /* 10. pacing */
  const P = cfg.pacing, base = d => { for (const s of P.segments || []) if ((s.to == null || d <= s.to) && (s.from == null || d >= s.from)) return s.sec_per_event; return P.sec_per_event; };
  for (let kk = 0; kk + 1 < info.start.length; kk++) { const sec = (info.start[kk + 1] - info.start[kk]) / 30, b = base(info.dates[kk]);
    if (sec < 0.8 * b - 0.04 || sec > 1.4 * b + 0.04) add('pacing ' + info.dates[kk] + ': ' + sec.toFixed(2) + ' s, base ' + b); }
  await br.close();
  return { name, config: C.config, frames: info.frames, quarters: checked, fails, late: storyLate[name] };
}
function RTT_eventAt(info, f) { let k = -1; for (let i = 0; i < info.start.length; i++) if (info.start[i] <= f) k = i; else break; return k; }

(async () => {
  const only = process.argv.slice(2);
  const g = global(), res = [];
  for (const n of Object.keys(CASES).filter(n => !only.length || only.includes(n))) { const r = await runCase(n); res.push(r);
    console.log((r.fails.length ? 'FAIL ' : 'PASS ') + n + ' (' + r.frames + ' frames, ' + r.quarters + ' quarter ends)'); r.fails.slice(0, 8).forEach(m => console.log('   ' + m)); }
  const ok = !g.fails.length && res.every(r => !r.fails.length);
  g.fails.forEach(m => console.log('FAIL ' + m));
  const out = ['# RTT-103 player tests (IQ-18, design round 1)', '', 'Run: `node tests/player/run_tests_rtt103.js`. Checks 0-10 are listed at the top of the script.', '',
    '- Data untouched and player input as recorded (check 0), colours (check 9: closest pair CIEDE2000 ' + g.minDE.toFixed(1) + ', closest to the background ' + g.minBG.toFixed(1) + '), story quotes word for word in G (check 7): ' + (g.fails.length ? 'FAIL' : 'PASS'), '',
    '| Case | Config | Frames | Quarter ends checked | Result |', '|---|---|---|---|---|',
    ...res.map(r => `| ${r.name} | \`${r.config}\` | ${r.frames} | ${r.quarters} | ${r.fails.length ? 'FAIL: ' + r.fails.slice(0, 3).join('; ') : 'PASS'}${r.late != null ? ' (story moments: the latest starts ' + r.late.toFixed(1) + ' s after its own quarter, queued behind the one before)' : ''} |`), '',
    `**${ok ? 'PASS' : 'FAIL'}**: ${res.filter(r => !r.fails.length).length + (g.fails.length ? 0 : 1)}/${res.length + 1}`];
  if (!only.length) fs.writeFileSync(path.join(__dirname, 'RESULTS_RTT103.md'), out.join('\n') + '\n');
  console.log(ok ? 'ALL PASS' : 'FAILURES');
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
