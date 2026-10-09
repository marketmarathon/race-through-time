/* RTT-102 player tests (IQ-19, design round 1). Same method as run_tests_rtt103.js: every frame of each case is drawn in
 * order through the kit's own driver path (kits/rtt-002/rtt.js openPlayer) at 1920 x 1080, and what was drawn
 * (window.__LABELS, __BARS, __RANK, __STATUS, __DATEBLOCK, __STORY, __CARDBOX, __NOTE, __FINAL) is checked against
 * data/rtt-102/*.csv, read HERE, independently of the adapter and of rtt_timeline.js:
 *
 *   0. the data is untouched: series_monthly.csv and identities.csv have the SHA-256 in data/rtt-102/manifest.json, and
 *      the player input has the SHA-256 in kits/rtt-102/dataset_hashes.txt
 *   1. values: on every month's landing frame each drawn value equals series_monthly.csv's visits for that month (a held
 *      bar: its last published figure), formatted here ("~5.6bn": billions to 1 or 2 decimals, whole millions from
 *      100m, else one decimal; half up on the whole visits; "~" as the option says). Eased motion: on a published month
 *      the exact figure; on every frame each bar stays within the two published figures either side (no overshoot)
 *   2. bars: on a landing frame the board holds exactly the assistants with a series row that month, plus the ones
 *      after their last published month (held at that figure, "· latest figure, <Mon YYYY>" or "· latest figure",
 *      ranked below every live bar); never a bar before its first published month; nothing after August 2026 (the
 *      race ends there, DEC-530/DEC-531: ChatGPT's September 2026 figure is never drawn)
 *   3. order: on every landing frame no live bar sits above a live bar with more visits
 *   4. date: the date block reads the month's name and year on its landing frame
 *   5. names: each bar's name is series_monthly.csv's bar_label for that month ("Bard" to January 2024)
 *   6. looks: Similarweb's older estimates (older_estimate = yes) are drawn striped exactly where the option asks for it;
 *      every other bar solid (or every bar in the analyst look, option b B); the revision note on screen in August 2024
 *   7. story cards: each card's quoted words (between “ and ”, split at "…") appear word for word in Cowork's checks
 *      (data/rtt-102/source/verification.csv exact_wording_seen) and its date is that check's date; one card at a time;
 *      a card never covers a name, value or tag; how late each card appears after its own month starts (seconds)
 *   8. layout: no label outside the frame; title, source line and note line clear of the date block and logo box
 *   9. colours: no two assistants closer than CIEDE2000 18 as drawn (DEC-023); colour-blind (protan, deutan) minimum
 *      reported
 *  10. pacing: each month (or quarter) counts over 0.8-1.4 x its base (to the whole frame)
 *  11. eased vs straight lines: the month-end order of every place (1st to 8th) compared month by month (report only)
 * Results: tests/player/RESULTS_RTT102.md. Exit 1 on any failure.
 *
 *   node tests/player/run_tests_rtt102.js [case ...]
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..', '..');
const KIT = path.join(ROOT, 'kits', 'rtt-002');
const K102 = path.join(ROOT, 'kits', 'rtt-102');
const rtt = require(path.join(KIT, 'rtt.js'));
const TLM = require(path.join(KIT, 'rtt_timeline.js'));
const { placeholders, logoPlaceholders } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const D = path.join(ROOT, 'data', 'rtt-102');

function readCSV(file) {
  const t = fs.readFileSync(file, 'utf8').replace(/^﻿/, ''), rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < t.length; i++) { const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true; else if (c === ',') { row.push(f); f = ''; } else if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; } else if (c !== '\r') f += c; }
  if (f || row.length) { row.push(f); rows.push(row); }
  const h = rows.shift(); return rows.filter(r => r.length > 1).map(r => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}
const sha = f => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const MSHORT = MONTHS.map(m => m.slice(0, 3));
/* the value label, independently of the player: BigInt, half up */
function visitsText(visits, V, pub) {
  const u = BigInt(visits), D2 = V.bn_decimals === 2 ? 2 : 1, P = 10n ** BigInt(D2);
  const bn = (u + 500000000n / P) / (1000000000n / P), m = (u + 500000n) / 1000000n, t = (u + 50000n) / 100000n;
  let s;
  if (u >= 1000000000n || m >= 1000n) s = (bn / P) + '.' + String(bn % P).padStart(D2, '0') + 'bn';
  else if (u >= 100000000n || t >= 1000n) s = m + 'm';
  else s = (t / 10n) + '.' + (t % 10n) + 'm';
  if (!pub && V.between === 'sig2') {                 // IQ-19b (Cowork fix (b)): two significant figures, half up
    let p = 1n; while (u >= p * 100n) p *= 10n;        // u in [10p, 100p) (or below 100)
    let r = (u + p / 2n) / p; if (r >= 100n) { p *= 10n; r = (u + p / 2n) / p; }
    const v = r * p;
    if (v >= 1000000000n) s = v >= 10000000000n ? String(v / 1000000000n) + 'bn' : (Number(v / 100000000n) / 10).toFixed(1) + 'bn';
    else s = v >= 10000000n ? String(v / 1000000n) + 'm' : v >= 1000000n ? (Number(v / 100000n) / 10).toFixed(1) + 'm' : (Number(v / 10000n) / 100).toFixed(2) + 'm';
  }
  return (V.approx === 'all' || (V.approx === 'between' && !pub) ? '~' : '') + s;
}

const CASES = {
  // round 1's cases (IQ-19, results in git history) are retired: its base config keeps round 1's note timing, which Cowork's fix (a) replaced
  film: { config: 'config_rtt102_film.json' },                                   // round 2 (IQ-19b, IQ-19c): the main version
  film_linear: { config: 'config_rtt102_film.json', over: { smoothing: { mode: 'none' } } },   // the panel = series_monthly.csv sums on every landing frame
};
for (const c of fs.readFileSync(path.join(K102, 'clips.txt'), 'utf8').split('\n').filter(Boolean)) CASES[c.replace(/^config_rtt102_|\.json$/g, '')] = { config: c };

const series = readCSV(path.join(D, 'series_monthly.csv'));
const byMonth = {}; for (const r of series) (byMonth[r.month] = byMonth[r.month] || {})[r.assistant_id] = r;
const lastPub = {}, firstMonth = {}, knots = {};
for (const r of series) { if (r.month > '2026-08') continue; firstMonth[r.assistant_id] = firstMonth[r.assistant_id] || r.month;
  if (r.provenance === 'published') { lastPub[r.assistant_id] = r.month; (knots[r.assistant_id] = knots[r.assistant_id] || []).push(r); } }
const verif = readCSV(path.join(D, 'source', 'verification.csv'));

function merge(base, over) {
  const out = Object.assign({}, base);
  for (const [k, v] of Object.entries(over || {}))
    out[k] = v && typeof v === 'object' && !Array.isArray(v) && base[k] && typeof base[k] === 'object' && !Array.isArray(base[k]) ? merge(base[k], v) : v;
  return out;
}
const overlap = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
const lbox = L => ({ x: L.x, y: L.y - L.asc, w: L.w, h: L.asc + L.desc });

async function runCase(name, C) {
  const prev = process.cwd(); process.chdir(KIT);
  const cfg = merge(rtt.loadConfig('../rtt-102/' + C.config), C.over);
  const out = path.join(ROOT, 'tests', 'output', 'rtt102_' + name); placeholders(cfg, out); logoPlaceholders(cfg, out);
  process.env.RTT_LOCAL_ASSETS = out;
  const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
  const V = Object.assign({ approx: 'all', bn_decimals: 1, older: 'stripes', look: 'solid' }, (cfg.values || {}).visits || {});
  const { tl, total } = rtt.frameTotals(cfg, data);
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
  process.chdir(prev);
  const fails = [], notes = [], landing = {}; tl.quarterEndFrame.forEach((f, k) => { landing[f] = k; });
  const fail = m => { if (fails.length < 40) fails.push(m); };
  const EASED = (cfg.smoothing || {}).mode === 'eased';
  const lateness = {}, cardsSeen = {}, panelRows = [];
  let maxBelow = 0;
  for (let f = 0; f < total; f++) {
    const S = await pg.evaluate(fr => { drawAt(fr / 30); return { L: window.__LABELS, B: window.__BARS, R: window.__RANK, ST: window.__STATUS, DB: window.__DATEBLOCK,
      SY: window.__STORY, CB: window.__CARDBOX, N: window.__NOTE, F: window.__FINAL, O: window.__OVERLAYS, C: window.__COMBINED }; }, f);
    const k = TLM.eventAt(tl, f), ev = k >= 0 ? tl.events[k] : tl.openingEvent, month = ev.date.slice(0, 7);
    if (month > '2026-08') fail(`frame ${f}: a month after August 2026 (${month})`);
    const labels = S.L, byKind = kd => labels.filter(L => L.kind === kd);
    // 8. layout
    for (const L of labels) if (L.w > 0 && (L.x < -0.5 || L.x + L.w > 1920.5)) fail(`frame ${f}: ${L.kind} "${L.text}" outside the frame`);
    const title = byKind('title')[0], db = S.DB && S.DB.box, logo = (S.O || [])[0];
    for (const L of labels.filter(L => ['title', 'source_line', 'note_line', 'final_line'].includes(L.kind))) {
      if (db && overlap(lbox(L), db)) fail(`frame ${f}: ${L.kind} meets the date block`);
      if (logo && overlap(lbox(L), logo.box)) fail(`frame ${f}: ${L.kind} meets the logo box`); }
    if (!title) fail(`frame ${f}: no title`);
    // eased: no overshoot on any frame
    if (EASED && k >= 0) for (const b of S.B) {
      const ks = knots[b.id]; if (!ks || b.status === 'latest_figure') continue;
      const m = month, prevM = (k > 0 ? tl.events[k - 1] : tl.openingEvent).date.slice(0, 7);
      const lo = ks.filter(r => r.month <= prevM).pop(), hi = ks.find(r => r.month >= m);
      if (lo && hi) { const a = Math.min(+lo.visits, +hi.visits), c = Math.max(+lo.visits, +hi.visits);
        if (b.units < a - 1 || b.units > c + 1) fail(`frame ${f} ${b.id}: ${b.units} outside its published figures ${a}..${c}`); }
    }
    // 6 (IQ-19b, Cowork fix (a)): stripes on a bar's older-estimate stretch, kept while it counts to its first current
    // figure and gone when that lands; the note only while some bar is striped
    const kPrevM = (k > 0 ? tl.events[k - 1] : tl.openingEvent).date.slice(0, 7), counting = k >= 0 && f < tl.quarterEndFrame[k];
    const olderOf = (id, m) => { const r = (byMonth[m] || {})[id]; if (r) return r.older_estimate === 'yes'; const lp = lastPub[id]; return lp && lp < m ? byMonth[lp][id].older_estimate === 'yes' : null; };
    if (k >= 0 && V.look !== 'analyst') for (const b of S.B) { if (!(b.alpha > 0.01)) continue;
      const now = olderOf(b.id, month), was = olderOf(b.id, kPrevM);
      const want = V.older === 'stripes' && (now === true || (counting && was === true)) ? 'estimated' : 'official';
      if (b.style !== want) fail(`frame ${f} (${month}${counting ? ', counting' : ''}) ${b.id}: drawn ${b.style}, want ${want}`); }
    if (S.N && S.N.alpha > 0.01 && /striped/.test(S.N.text) && !S.B.some(b => b.style === 'estimated' && b.alpha > 0.01)) fail(`frame ${f}: the note is on screen with no striped bar`);
    // (IQ-19b, Cowork fix (b)): every value on every frame - a published figure only on its landing frame (or held)
    if (V.between === 'sig2') for (const b of S.B) { const v = labels.find(L => L.kind === 'value' && L.id === b.id); if (!v) continue;
      const r = (byMonth[month] || {})[b.id], held = b.status === 'latest_figure' || (!r && lastPub[b.id] && lastPub[b.id] < month);
      const pubF = held || (!counting && r && r.provenance === 'published');
      const w = visitsText(b.units, V, pubF); if (v.text !== w) fail(`frame ${f} (${month}) ${b.id}: value "${v.text}", want "${w}" (${pubF ? 'published' : 'not a published figure'})`); }
    // the combined panel (IQ-19b item 3c): never covers a name, value or tag; its text formatted as the bars'
    if (cfg.combined && cfg.combined.enabled) { if (!S.C) fail(`frame ${f}: no combined panel`);
      else { for (const L of labels.filter(L => ['name', 'value', 'status_tag'].includes(L.kind))) if (overlap(lbox(L), S.C.box)) fail(`frame ${f}: the panel covers ${L.kind} "${L.text}"`); } }
    // 7. story cards
    if (S.SY && S.SY.at) { const it = cfg.story.items.find(x => x.at === S.SY.at);
      cardsSeen[it.at] = true; if (lateness[it.at] == null) lateness[it.at] = (f - tl.startFrame[tl.events.findIndex(e => e.date === it.at)]) / 30;
      if (S.CB) for (const L of labels.filter(L => ['name', 'value', 'status_tag', 'est_label'].includes(L.kind))) if (overlap(lbox(L), S.CB)) fail(`frame ${f}: the ${it.when} card covers ${L.kind} "${L.text}"`); }
    if (!(f in landing)) continue;
    // ---- a landing frame ----
    const row = byMonth[month] || {};
    const want = Object.keys(firstMonth).filter(id => firstMonth[id] <= month);
    const drawn = S.B.filter(b => b.alpha > 0.01).map(b => b.id).sort();
    if (JSON.stringify(drawn) !== JSON.stringify(want.slice().sort())) fail(`${month}: board ${drawn} but the data has ${want.sort()}`);
    const live = S.R.filter(id => row[id]), held = S.R.filter(id => !row[id]);
    if (JSON.stringify(S.R) !== JSON.stringify(live.concat(held))) fail(`${month}: a held bar ranks above a live one (${S.R})`);
    for (const id of want) {
      const held_ = !row[id], r = held_ ? byMonth[lastPub[id]][id] : row[id], b = S.B.find(x => x.id === id);
      if (held_ && !(month > lastPub[id])) fail(`${month} ${id}: no series row but not after its last published month`);
      const pub = held_ || r.provenance === 'published';
      if (!EASED || pub) { const v = labels.find(L => L.kind === 'value' && L.id === id), w = visitsText(r.visits, V, pub);
        if (!v || v.text !== w) fail(`${month} ${id}: value "${v && v.text}" but the data gives "${w}"`);
        if (b.units !== +r.visits) fail(`${month} ${id}: bar units ${b.units} but the data ${r.visits}`); }
      const nm = labels.find(L => L.kind === 'name' && L.id === id);
      if (!nm || nm.text !== r.bar_label) fail(`${month} ${id}: name "${nm && nm.text}" but the data "${r.bar_label}"`);
      const st = held_ ? labels.find(L => L.kind === 'status_tag' && L.id === id) : null;
      if (held_) { const [y, mo] = lastPub[id].split('-'), tx = '· ' + cfg.status.latest_figure.replace('{month}', MSHORT[+mo - 1] + ' ' + y);
        if (!st || st.text !== tx) fail(`${month} ${id}: held but its tag is "${st && st.text}" (want "${tx}")`); }
      const wantSt = V.look === 'analyst' ? 'analyst_estimate' : V.older === 'stripes' && r.older_estimate === 'yes' ? 'estimated' : 'official';
      if (b.style !== wantSt) fail(`${month} ${id}: drawn ${b.style}, want ${wantSt}`);
    }
    // 3. order
    for (let i = 0; i < live.length; i++) for (let j = i + 1; j < live.length; j++) {
      const a = S.B.find(x => x.id === live[i]).units, c = S.B.find(x => x.id === live[j]).units;
      if (c > a) fail(`${month}: ${live[j]} (${c}) below ${live[i]} (${a})`); }
    // the combined panel on a landing frame: the sum of the bars with a figure that month (held bars left out) = the drawn
    // bars' sum; with straight lines (or where every one is published) = series_monthly.csv's sum; the bottom line
    if (cfg.combined && cfg.combined.enabled && S.C) {
      const liveIds = want.filter(id => row[id]), drawnSum = liveIds.reduce((a, id) => a + S.B.find(x => x.id === id).units, 0);
      const dataSum = liveIds.reduce((a, id) => a + +row[id].visits, 0), allPub = liveIds.every(id => row[id].provenance === 'published');
      if (S.C.value !== drawnSum) fail(`${month}: panel ${S.C.value} but the bars add up to ${drawnSum}`);
      if ((!EASED || allPub) && S.C.value !== dataSum) fail(`${month}: panel ${S.C.value} but series_monthly.csv adds up to ${dataSum}`);
      if (S.C.text !== visitsText(S.C.value, V, allPub)) fail(`${month}: panel text "${S.C.text}", want "${visitsText(S.C.value, V, allPub)}"`);
      const out = want.filter(id => !row[id]);
      const wantNote = out.length === 1 ? cfg.combined.drop_one.replace('{id}', out[0] === 'meta_ai' ? 'Meta AI' : 'Copilot').replace('{month}', MSHORT[+lastPub[out[0]].slice(5) - 1] + ' ' + lastPub[out[0]].slice(0, 4))
        : out.length > 1 ? cfg.combined.drop_many.replace('{ids}', S.R.filter(id => out.includes(id)).map(id => id === 'meta_ai' ? 'Meta AI' : 'Copilot').join(', ')) : null;
      if ((S.C.note || null) !== wantNote) fail(`${month}: panel line "${S.C.note}", want "${wantNote}"`);
      if (!out.length && S.C.companies !== liveIds.length) fail(`${month}: panel counts ${S.C.companies} sites, want ${liveIds.length}`);
      panelRows.push(month + ' ' + S.C.text + (S.C.note ? ' (' + S.C.note + ')' : '')); }
    // 4. date
    const [y, mo] = month.split('-').map(Number);
    if (!S.DB || S.DB.year !== y || S.DB.month !== MONTHS[mo - 1]) fail(`${month}: date block ${S.DB && S.DB.month} ${S.DB && S.DB.year}`);
    // 6. the note
    if (month === '2024-08' && (cfg.notes_at || []).length && !(S.N && S.N.text === cfg.notes_at[0].text)) fail('August 2024: the revision note is not on screen');
    if (month === '2026-08' && cfg.final_line && cfg.final_line.enabled && f === tl.quarterEndFrame[tl.events.length - 1] && !(S.F && S.F.line === cfg.final_line.text)) fail('the final line is not on the final table');
  }
  // 7. story cards: wording and dates against Cowork's checks
  if (cfg.story && cfg.story.enabled) for (const it of cfg.story.items.filter(x => !x.plain)) {
    const m = /“(.*)”/.exec(it.text); const parts = m ? m[1].split('…').map(s => s.trim()).filter(Boolean) : [];
    const v = verif.find(r => parts.length && parts.every(p => r.exact_wording_seen.includes(p.replace(/\.$/, ''))));
    if (!v) fail(`card ${it.when}: "${it.text}" not found word for word in verification.csv`);
    else { const dd = new Date(v.month + 'T00:00:00Z'), w = dd.getUTCDate() + ' ' + MSHORT[dd.getUTCMonth()] + ' ' + dd.getUTCFullYear();
      if (w !== it.when) fail(`card: date ${it.when} but ${v.check_id} gives ${w}`); else notes.push(`card ${it.when} = ${v.check_id} (${v.status})`); }
    if (!cardsSeen[it.at] && tl.events.some(e => e.date === it.at)) fail(`card ${it.when} never shown`);
  }
  if (panelRows.length) notes.push('panel on landing frames: ' + panelRows.filter((_, i) => i % 6 === 0 || i === panelRows.length - 1).join('; '));
  for (const [at, s] of Object.entries(lateness)) notes.push(`card dated ${at.slice(0, 7)} first on screen ${s.toFixed(1)} s after its month starts`);
  // 10. pacing
  const base = cfg.pacing.sec_per_event;
  for (let i = 0; i + 1 < tl.startFrame.length; i++) { const n = tl.startFrame[i + 1] - tl.startFrame[i];   // whole frames: one frame of rounding allowed
    if (n < 0.8 * base * 30 - 1 || n > 1.4 * base * 30 + 1) fail(`pacing: event ${i} lasts ${(n / 30 / base).toFixed(2)} x base`); }
  await br.close();
  return { name, config: C.config, frames: total, fails, notes };
}

/* 9. colours and 11. eased vs linear orders (no drawing) */
function colours(cfg) {
  const pal = cfg.palette, ids = cfg.maker_order, res = [];
  let mn = 99, mp = '';
  for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) { const d = TLM.deltaE(pal[i], pal[j]); if (d < mn) { mn = d; mp = ids[i] + '/' + ids[j]; } }
  const MAT = { protan: [[0.152286,1.052583,-0.204868],[0.114503,0.786281,0.099216],[-0.003882,-0.048116,1.051998]], deutan: [[0.367322,0.860646,-0.227968],[0.280085,0.672501,0.047413],[-0.011820,0.042940,0.968881]] };
  const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }, de = c => { c = Math.min(1, Math.max(0, c)); return Math.round(255 * (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055)); };
  const sim = (h, M) => { const n = parseInt(TLM.drawnColour(h).slice(1), 16), v = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map(lin); return '#' + M.map(r => de(r[0] * v[0] + r[1] * v[1] + r[2] * v[2]).toString(16).padStart(2, '0')).join(''); };
  let cb = 99, cbp = '';
  for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) for (const M of Object.values(MAT)) { const d = TLM.deltaE(sim(pal[i], M), sim(pal[j], M)); if (d < cb) { cb = d; cbp = ids[i] + '/' + ids[j]; } }
  return { mn, mp, cb, cbp, ok: mn >= 18 };
}
function orders(cfg, data) {
  const lin = TLM.buildSeries(data, merge(cfg, { smoothing: { mode: 'none' } })), eas = TLM.buildSeries(data, merge(cfg, { smoothing: { mode: 'eased' } }));
  const diffs = [];
  lin.states.forEach((s, k) => { if (s.order.join() !== eas.states[k].order.join()) diffs.push(lin.events[k].date.slice(0, 7) + ': ' + s.order.join(' > ') + '  vs eased  ' + eas.states[k].order.join(' > ')); });
  return diffs;
}

(async () => {
  const only = process.argv.slice(2);
  const res = [];
  // 0. the data is untouched
  const man = JSON.parse(fs.readFileSync(path.join(D, 'manifest.json'), 'utf8')).files;
  const zero = [];
  for (const f of ['series_monthly.csv', 'identities.csv']) if (man[f] !== sha(path.join(D, f))) zero.push(f + ' differs from manifest.json');
  const hl = fs.readFileSync(path.join(K102, 'dataset_hashes.txt'), 'utf8').split('\n').filter(l => !l.startsWith('#') && / output /.test(l))[0].split(' ')[0];
  if (hl !== sha(path.join(K102, 'race_rtt102.json'))) zero.push('race_rtt102.json differs from dataset_hashes.txt');
  const prev = process.cwd(); process.chdir(KIT);
  const baseCfg = rtt.loadConfig('../rtt-102/config_rtt102_base.json'), data = JSON.parse(fs.readFileSync(path.join(K102, 'race_rtt102.json'), 'utf8'));
  process.chdir(prev);
  const col = colours(baseCfg), ord = orders(baseCfg, data);
  for (const [name, C] of Object.entries(CASES)) if (!only.length || only.includes(name)) { const r = await runCase(name, C); res.push(r); console.log(`${r.fails.length ? 'FAIL' : 'PASS'} ${name} (${r.frames} frames)${r.fails.length ? '\n  ' + r.fails.join('\n  ') : ''}`); }
  const ok = !zero.length && col.ok && res.every(r => !r.fails.length);
  const md = ['# RTT-102 player tests (IQ-19, design round 1)', '', `Run: node tests/player/run_tests_rtt102.js · ${ok ? 'ALL PASS' : 'FAILURES'}`, '',
    `0. Data untouched: ${zero.length ? 'FAIL ' + zero.join('; ') : 'PASS (series_monthly.csv and identities.csv as data/rtt-102/manifest.json; race_rtt102.json as dataset_hashes.txt)'}`,
    `9. Colours: closest pair as drawn CIEDE2000 ${col.mn.toFixed(1)} (${col.mp}) ${col.ok ? 'PASS' : 'FAIL'} (>= 18); colour-blind (protan/deutan simulation) closest ${col.cb.toFixed(1)} (${col.cbp}), reported`,
    `11. Eased vs straight lines, month-end order of all places: ${ord.length ? ord.length + ' month(s) differ:' : 'no month differs (every place change of report section 2 and every lower place stays in its month)'}`, ...ord.map(d => '   - ' + d), '',
    '| Case | Config | Frames | Result |', '|---|---|---|---|', ...res.map(r => `| ${r.name} | ${r.config} | ${r.frames} | ${r.fails.length ? 'FAIL: ' + r.fails.slice(0, 5).join('; ') : 'PASS'} |`), '',
    'Notes:', ...[...new Set(res.flatMap(r => r.notes.map(n => r.name + ': ' + n)))].map(n => '- ' + n), ''];
  if (!only.length) fs.writeFileSync(path.join(__dirname, 'RESULTS_RTT102.md'), md.join('\n'));
  console.log(md.slice(0, 8).join('\n'));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
