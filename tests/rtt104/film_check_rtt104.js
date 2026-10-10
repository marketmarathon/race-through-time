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
  /* IQ-22d (V2, smooth motion): every frame of every move: each bar's value label lies between its two years' published
     figures (one-decimal rounding allowed) and is never below 0; the year label is one of the move's two years. */
  const between = await pg.evaluate(() => !!CURVES);
  if (between) {
    const moves = await pg.evaluate(() => PLAN.steps.filter(s => s.kind === 'move').map(s => ({ a: s.a, b: s.b, from: s.from, to: s.to })));
    let checked = 0, bad = [];
    for (const m of moves) for (let f = m.from + 1; f < m.to; f++) {
      const r = await pg.evaluate(([ff, a, b]) => {
        drawAt(ff / 30);
        const val = (y, k, id) => { const R = D.frames[PLAN.idx[y]].ranks[k].find(x => x.id === id); return R ? +R.v : null; };
        const errs = [];
        for (const x of window.__BARS) {
          if (x.alpha < 0.05) continue;
          const t = parseFloat(x.value), va = val(a, x.board, x.id), vb = val(b, x.board, x.id);
          const lo = Math.min(...[va, vb].filter(v => v != null)), hi = Math.max(...[va, vb].filter(v => v != null));
          if (!(t >= 0) || t < Math.round(lo * 10) / 10 - 0.05 - 1e-9 || t > Math.round(hi * 10) / 10 + 0.05 + 1e-9) errs.push(`${x.board} ${x.id} ${x.value} outside ${lo}-${hi}`);
        }
        const yl = window.__LABELS.filter(l => l.kind === 'year').map(l => +l.text);
        if (yl.some(y => y !== a && y !== b)) errs.push('year label ' + yl.join(','));
        return { n: window.__BARS.length, errs };
      }, [f, m.a, m.b]);
      checked++; if (r.errs.length) bad.push(`frame ${f}: ${r.errs.join('; ')}`);
    }
    if (bad.length) ok = false;
    out.push('', `Between landings (smooth motion): ${checked} frames checked; every value label between its two years' published figures and not below 0, the year label one of the two years: ${bad.length ? 'FAIL' : 'PASS'}${bad.length ? ' — ' + bad.slice(0, 10).join(' | ') : ''}.`);
  }
  await br.close();
  out.push('', `Overall: ${ok ? 'PASS' : 'FAIL'} (${shots.length} shots).`, '');
  fs.writeFileSync(path.join(__dirname, 'FILM_CHECK.md'), out.join('\n'));
  console.log(`RTT-104 film check: ${ok ? 'PASS' : 'FAIL'} (${shots.length} shots)`);
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
