/* RTT-101 player tests (IQ-21, design round 1). Run from the repo root: node tests/player/run_tests_rtt101.js
 *   0. data untouched: series_onscreen.csv, clubs.csv, pl_membership.csv, seasons.csv as data/rtt-101/manifest.json;
 *      race_rtt101.json as kits/rtt-101/dataset_hashes.txt; the race file's figures equal series_onscreen.csv (pence)
 *   1. landing frames (every config): on the frame where each month's count lands, every club's value is
 *      series_onscreen.csv exactly (rtt_timeline.js seriesFrame, the function the page draws from), for all 411 events
 *   2. ranks: the order on each landing frame is the series' own rank (ties: the club that reached the value first)
 *   3. eased motion: on every frame between two month ends each bar lies between those two figures (never beyond them)
 *   4. frozen bars (DEC-259): a club outside the PL keeps its bar at its last in-PL figure and its rank by value, and its
 *      status is "out" from the first frame of the month it leaves to the first frame of the month it returns
 *   5. the final table holds 5 s after the freeze figures land (DEC-569)
 *   6. drawn landing frames (a sample: every 12th month, every change of leader, the freeze): each value label on the
 *      board reads the series figure in the config's format (written out again here on BigInt pence), the crown sits on
 *      the leader, a frozen bar is dimmed and labelled as configured, nothing is drawn over the date block or the panel
 *   7. pacing: every beat within the house multipliers; config C's named rule gives 0.25 s to exactly its months
 * Placeholder crests and logo (tests/player/placeholders.js). Output: tests/player/RESULTS_RTT101.md. Exit 1 on failure.
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..', '..'), KIT = path.join(ROOT, 'kits', 'rtt-002'), K101 = path.join(ROOT, 'kits', 'rtt-101'), D = path.join(ROOT, 'data', 'rtt-101');
const rtt = require(path.join(KIT, 'rtt.js')), TLM = require(path.join(KIT, 'rtt_timeline.js'));
const { placeholderPNG, logoPlaceholders } = require('./placeholders.js');
const CHROME = process.env.PW_CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);   // the container's Chromium, else Playwright's own (runner)
const sha = f => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const CONFIGS = ['config_rtt101_base.json', 'config_rtt101_pace_B.json', 'config_rtt101_pace_C.json'];

function csv(f) { const t = fs.readFileSync(f, 'utf8').trim().split('\n'), H = t.shift().split(','); return t.map(l => { const v = l.split(','); return Object.fromEntries(H.map((h, i) => [h, v[i]])); }); }
const pence = s => { const [a, b = ''] = s.split('.'); const neg = a.startsWith('-'); const v = BigInt(a.replace('-', '')) * 100n + BigInt((b + '00').slice(0, 2)); return Number(neg ? -v : v); };

/* the value label, written out again on BigInt pence (as the player's netText) */
function netText(u, style, extra = 0) {
  if (u === 0) return '£0';
  const sg = u < 0 ? '−' : '', a = BigInt(Math.abs(u)), r = q => (a + q / 2n) / q, P = d => 10n ** BigInt(d);
  const dec = (n, d) => { if (!d) return Number(n).toLocaleString('en-GB'); const p = P(d); return Number(n / p).toLocaleString('en-GB') + '.' + String(n % p).padStart(d, '0'); };
  if (style === 'm1') { const d = 1 + extra; return sg + '£' + dec(r(100000000n / P(d)), d) + 'm'; }
  const dB = 2 + extra, b = r(100000000000n / P(dB));
  if (a >= 100000000000n || b >= P(dB)) return sg + '£' + dec(b, dB) + 'bn';
  const d1 = 1 + extra, t = r(100000000n / P(d1));
  if (a >= 10000000000n || t >= 100n * P(d1)) return sg + '£' + dec(r(100000000n / P(extra)), extra) + 'm';
  return sg + '£' + dec(t, d1) + 'm';
}

async function drawn(cfgFile, tl, series, fails, notes) {
  const dir = path.join(ROOT, 'tests', 'output', 'rtt101_tests'); fs.mkdirSync(dir, { recursive: true });
  placeholderPNG(path.join(dir, 'rtt_logo.png'), 885, 885, [212, 175, 55]);
  const prev = process.cwd(); process.chdir(KIT);
  const cfg = rtt.loadConfig('../rtt-101/' + cfgFile); process.chdir(prev);
  cfg.local_assets = dir; logoPlaceholders(cfg, dir);
  const data = JSON.parse(fs.readFileSync(path.join(K101, 'race_rtt101.json'), 'utf8'));
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
  const lead = []; let pl = null;
  tl.states.forEach((s, k) => { if (s.order[0] !== pl) lead.push(k); pl = s.order[0]; });
  const ks = [...new Set([...tl.events.map((e, k) => k).filter(k => k % 12 === 0), ...lead, tl.events.length - 1])].sort((a, b) => a - b);
  const style = (cfg.values && cfg.values.net && cfg.values.net.style) || 'compact', outTxt = cfg.status && cfg.status.out;
  let checked = 0;
  for (const k of ks) {
    const f = tl.quarterEndFrame[k];
    for (let i = 0; i < 40; i++) await rtt.drawFrame(pg, f, cfg);       // rows at rest
    const r = await pg.evaluate(() => ({ L: window.__LABELS, B: window.__BARS, C: window.__CROWN, R: window.__RANK, DB: window.__DATEBLOCK, P: window.__COMBINED, S: window.__STATUS }));
    const date = tl.events[k].date, row = series[date], board = r.R.slice(0, cfg.rows);
    const want = Object.keys(row).sort((a, b) => row[a].rank - row[b].rank).slice(0, cfg.rows);
    if (board.join() !== want.join()) fails.push(`${cfgFile} ${date}: board ${board.join(',')} vs series ${want.join(',')}`);
    for (const id of board) {
      const v = r.L.find(l => l.kind === 'value' && l.id === id);
      if (!v) { fails.push(`${cfgFile} ${date}: no value label for ${id}`); continue; }
      if (cfg.values.net.ties !== 'extra' && v.text !== netText(row[id].v, style)) fails.push(`${cfgFile} ${date} ${id}: label ${v.text}, series ${netText(row[id].v, style)}`);
      const b = r.B.find(x => x.id === id);
      if (b.units !== row[id].v) fails.push(`${cfgFile} ${date} ${id}: bar ${b.units} pence, series ${row[id].v}`);
      if (row[id].out) {
        if (b.status !== 'out') fails.push(`${cfgFile} ${date} ${id}: out of the PL but status ${b.status}`);
        const tag = r.L.find(l => l.kind === 'status_tag' && l.id === id);
        if (outTxt && (!tag || tag.text !== '· ' + outTxt.replace('{year}', row[id].rel))) fails.push(`${cfgFile} ${date} ${id}: status label ${tag && tag.text}`);
        if (!outTxt && tag) fails.push(`${cfgFile} ${date} ${id}: dimmed-only option shows ${tag.text}`);
      } else if (b.status === 'out') fails.push(`${cfgFile} ${date} ${id}: in the PL but drawn out`);
      checked++;
    }
    if (cfg.crown && cfg.crown.enabled && (!r.C || r.C.id !== want[0])) fails.push(`${cfgFile} ${date}: crown on ${r.C && r.C.id}, leader ${want[0]}`);
    const boxes = [r.DB && r.DB.box, r.P && r.P.box].filter(Boolean);
    for (const L of r.L) { if (!L.size || ['date_month', 'date_year', 'date_year_old', 'comb_label', 'comb_value', 'comb_count', 'comb_axis', 'comb_drop', 'comb_note'].includes(L.kind)) continue;
      const y0 = L.y - L.size * 0.8, y1 = L.y + L.size * 0.25;
      for (const bx of boxes) if (L.x < bx.x + bx.w && L.x + L.w > bx.x && y0 < bx.y + bx.h && y1 > bx.y) fails.push(`${cfgFile} ${date}: ${L.kind} "${L.text}" overlaps a box at ${Math.round(bx.x)},${Math.round(bx.y)}`);
      if (L.x + L.w > 1920 - 16) fails.push(`${cfgFile} ${date}: ${L.kind} "${L.text}" runs off the frame`); }
  }
  await br.close();
  notes.push(`${cfgFile}: ${ks.length} landing frames drawn, ${checked} value labels checked`);
}

(async () => {
  const fails = [], notes = [];
  // 0. data untouched
  const man = JSON.parse(fs.readFileSync(path.join(D, 'manifest.json'), 'utf8')).files;
  for (const f of ['series_onscreen.csv', 'clubs.csv', 'pl_membership.csv', 'seasons.csv']) if (man[f] !== sha(path.join(D, f))) fails.push(f + ' differs from manifest.json');
  const hl = fs.readFileSync(path.join(K101, 'dataset_hashes.txt'), 'utf8').split('\n').find(l => !l.startsWith('#') && / output /.test(l)).split(' ')[0];
  if (hl !== sha(path.join(K101, 'race_rtt101.json'))) fails.push('race_rtt101.json differs from dataset_hashes.txt');
  const series = {};
  for (const r of csv(path.join(D, 'series_onscreen.csv'))) if (r.rank && r.month_end >= '1992-07-31') (series[r.month_end] = series[r.month_end] || {})[r.club_id] = { v: pence(r.cum_net_gbp), rank: +r.rank, out: r.in_pl === 'no' };
  const data = JSON.parse(fs.readFileSync(path.join(K101, 'race_rtt101.json'), 'utf8'));
  for (const ev of data.events) { const s = series[ev.date];
    if (!s || Object.keys(s).length !== Object.keys(ev.values).length) { fails.push(ev.date + ': race file and series differ in clubs'); continue; }
    for (const [id, v] of Object.entries(ev.values)) { if (s[id].v !== v) fails.push(`${ev.date} ${id}: race ${v}, series ${s[id].v}`); if (s[id].out) s[id].rel = ev.rel[id]; } }
  const res = [];
  for (const c of CONFIGS) {
    const prev = process.cwd(); process.chdir(KIT); const cfg = rtt.loadConfig('../rtt-101/' + c); process.chdir(prev);
    const tl = TLM.build(data, cfg), n0 = fails.length;
    // 1-2. landing frames: values and ranks, every event (the opening board = July 1992)
    const land = [{ date: tl.openingEvent.date, F: TLM.seriesFrame(tl, -1, 0) }].concat(tl.events.map((e, k) => ({ date: e.date, F: TLM.seriesFrame(tl, k, tl.countFrames[k] - 1) })));
    for (const { date, F } of land) { const s = series[date];
      for (const id of Object.keys(s)) if (F.u[id] !== s[id].v) { fails.push(`${c} ${date} ${id}: landed ${F.u[id]}, series ${s[id].v}`); break; }
      const want = Object.keys(s).sort((a, b) => s[a].rank - s[b].rank);
      if (F.order.join() !== want.join()) fails.push(`${c} ${date}: landed order differs from the series rank`); }
    // 3. eased motion stays between the two month ends
    let between = 0;
    tl.events.forEach((e, k) => { const a = k ? tl.states[k - 1].totals : tl.opening.totals, b = tl.states[k].totals;
      for (let f = 0; f < tl.countFrames[k]; f++) { const F = TLM.seriesFrame(tl, k, f);
        for (const id of Object.keys(b)) if (id in a) { const lo = Math.min(a[id], b[id]), hi = Math.max(a[id], b[id]); between++;
          if (F.u[id] < lo || F.u[id] > hi) { fails.push(`${c} ${e.date} frame ${f} ${id}: ${F.u[id]} outside ${lo}..${hi}`); break; } } } });
    // 4. frozen bars
    const lastIn = {};
    for (const { date } of land) for (const [id, s] of Object.entries(series[date])) {
      if (!s.out) lastIn[id] = s.v; else if (lastIn[id] != null && s.v !== lastIn[id]) fails.push(`${c} ${date} ${id}: out of the PL but its figure moved (${lastIn[id]} -> ${s.v})`); }
    tl.events.forEach((e, k) => { for (const [id, s] of Object.entries(series[e.date])) { const st = TLM.statusAt(tl, id, tl.startFrame[k]).kind;
      if ((st === 'out') !== s.out) fails.push(`${c} ${e.date} ${id}: status ${st} at the month's first frame, in_pl ${s.out ? 'no' : 'yes'}`); } });
    // 5. the 5 s ending
    const after = tl.raceFrames - tl.quarterEndFrame[tl.events.length - 1] - 1;
    if (tl.isDataEnd && !(cfg.steps && cfg.steps.enabled) && after !== Math.round(cfg.pacing.final_after_landing_sec * 30)) fails.push(`${c}: ${after} frames after the freeze lands, want ${cfg.pacing.final_after_landing_sec * 30}`);
    // 7. pacing
    const R = cfg.pacing.month_rules || [];
    tl.events.forEach((e, k) => { if (k === tl.events.length - 1) return; const n = tl.startFrame[k + 1] - tl.startFrame[k];
      const rule = R.find(s => (s.to == null || e.date <= s.to) && (s.from == null || e.date >= s.from) && s.months.includes(+e.date.slice(5, 7)) && !e.freeze);
      const base = rule ? rule.sec_per_event : cfg.pacing.sec_per_event, m = n / 30 / base;
      if (m < 0.8 - 0.05 || m > 1.4 + 0.05) fails.push(`${c} ${e.date}: beat ${n} frames = ${m.toFixed(2)} x base`); });
    res.push({ c, frames: tl.raceFrames, sec: (tl.raceFrames / 30).toFixed(1), between, fails: fails.length - n0 });
  }
  // 6. drawn landing frames, base config and the label options
  await drawn('config_rtt101_base.json', TLM.build(data, (() => { const p = process.cwd(); process.chdir(KIT); const x = rtt.loadConfig('../rtt-101/config_rtt101_base.json'); process.chdir(p); return x; })()), series, fails, notes);
  const ok = !fails.length;
  const md = ['# RTT-101 player tests (IQ-21, design round 1)', '', `Run: node tests/player/run_tests_rtt101.js · ${ok ? 'ALL PASS' : 'FAILURES'}`, '',
    '0. Data untouched: ' + (fails.some(f => /manifest|dataset_hashes|race file/.test(f)) ? 'FAIL' : 'PASS (series_onscreen.csv, clubs.csv, pl_membership.csv, seasons.csv as data/rtt-101/manifest.json; race_rtt101.json as dataset_hashes.txt; every race figure = series_onscreen.csv in pence)'),
    '', '| Config | Frames | Film length | 1-5, 7: landing values, ranks, eased frames checked, frozen bars, ending, pacing |', '|---|---|---|---|',
    ...res.map(r => `| ${r.c} | ${r.frames} | ${r.sec} s | ${r.fails ? 'FAIL (' + r.fails + ')' : 'PASS'}: 412 landing boards (July 1992 to the freeze), ${r.between.toLocaleString('en-GB')} eased bar-frames between month ends |`),
    '', '6. Drawn landing frames: ' + (fails.some(f => f.startsWith('config_rtt101_base.json ')) ? 'FAIL' : 'PASS') + ' - ' + notes.join('; '), '',
    ...(fails.length ? ['Failures (first 40):', ...fails.slice(0, 40).map(f => '- ' + f), ''] : [])];
  fs.writeFileSync(path.join(__dirname, 'RESULTS_RTT101.md'), md.join('\n') + '\n');
  console.log(md.join('\n'));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
