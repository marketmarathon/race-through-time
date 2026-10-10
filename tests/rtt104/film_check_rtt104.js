/* RTT-104 whole-film check (IQ-22b), run before the film render (.github/workflows/rtt104_film.yml) and by hand:
 *   node tests/rtt104/film_check_rtt104.js [config, default config_rtt104_film.json]
 * Draws the film config's landing frame of EVERY year (the frame on which that year's figures land), every leave-note
 * frame (40 frames in) and the closing card, and checks each with kits/rtt-104/render_stills.js's own checks:
 *   VALUES  both boards = data/rtt-104/boards.csv for the year (countries, order, value_1dp + "%"), 0% group = zero_group.csv;
 *   PHONE   names, values, 0% group and closing-card lines at least 5.9 pt at 390 pt wide; other text at least 5.0 pt;
 *   OVERLAP no board text inside the world panel or past its board.
 * Also: the closing card lists exactly closing_card.csv's on-card countries with their card wording, in order.
 * Writes tests/rtt104/FILM_CHECK.md (text only). Exit 1 on any failure.
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const R = require(path.join(ROOT, 'kits', 'rtt-104', 'render_rtt104.js'));
const S = require(path.join(ROOT, 'kits', 'rtt-104', 'render_stills.js'));

(async () => {
  const cfgName = process.argv[2] || 'config_rtt104_film.json';
  const cfg = R.config(cfgName);
  const { br, pg } = await R.open(cfg);
  const plan = await pg.evaluate(() => planSummary());
  const shots = plan.years.map(y => ({ name: 'year ' + y, at: y }))
    .concat(Object.keys(plan.notes).map(y => ({ name: 'leave note before ' + y, at: 'note:' + y })))
    .concat([{ name: 'closing card', at: 'card' }]);
  const out = ['# RTT-104 whole-film check (IQ-22b)', '', `Config \`kits/rtt-104/${cfgName}\`: ${plan.total} frames = ${(plan.total / 30).toFixed(1)} s. Every year's landing frame, every leave note and the closing card, checked with \`kits/rtt-104/render_stills.js\`'s checks (values against \`data/rtt-104/boards.csv\` and \`zero_group.csv\`; phone sizes; overlaps).`, '',
    '| Frame | Shot | Values | Phone | Overlap |', '|---|---|---|---|---|'];
  let ok = true;
  for (const s of shots) {
    const f = await S.targetFrame(pg, s.at);
    for (let i = 0; i < 2; i++) await R.frame(pg, f);
    const st = await pg.evaluate(() => ({ labels: window.__LABELS, bars: window.__BARS, panel: G.panel, lr: G.lr }));
    const v = S.checkValues(s, st), p = S.checkPhone(st), o = S.checkOverlap(st, cfg);
    if (s.at === 'card') {
      const rows = fs.readFileSync(path.join(ROOT, 'data', 'rtt-104', 'closing_card.csv'), 'utf8').split(/\r?\n/).filter(Boolean);
      const want = await pg.evaluate(() => D.closing_card.map(c => c.label + ' — ' + c.line));
      const names = st.labels.filter(l => l.kind === 'card_name').map(l => l.text), lines = st.labels.filter(l => l.kind === 'card_line').map(l => l.text);
      const got = names.map((n, i) => n + ' ' + lines[i]);
      if (got.join('|') !== want.join('|')) v.push('closing card lines differ from closing_card.csv');
      if (names.length !== rows.filter(r => /,yes,/.test(r)).length) v.push('closing card count differs from closing_card.csv');
    }
    const bad = v.length || p.fails.length || o.length; if (bad) ok = false;
    out.push(`| ${f} | ${s.name} | ${v.length ? 'FAIL: ' + v.join('; ') : 'PASS'} | ${p.fails.length ? 'FAIL: ' + p.fails.join('; ') : 'PASS'} | ${o.length ? 'FAIL: ' + o.join('; ') : 'PASS'} |`);
  }
  await br.close();
  out.push('', `Overall: ${ok ? 'PASS' : 'FAIL'} (${shots.length} shots).`, '');
  fs.writeFileSync(path.join(__dirname, 'FILM_CHECK.md'), out.join('\n'));
  console.log(`RTT-104 film check: ${ok ? 'PASS' : 'FAIL'} (${shots.length} shots)`);
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
