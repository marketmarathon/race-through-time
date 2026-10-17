/* RTT-104 V3 whole-film check (IQ-24g), run before the film render.
 *
 * Usage: node tests/rtt104/film_check_v3.js <config in kits/rtt-104> [stills_out_dir]
 *
 * Every frame of the film (closing card, if any, excluded):
 *   TAGS    every tag drawn is a VERIFIED row of data/rtt-104/v3_change_events.csv with a source URL and a fetched
 *           excerpt, big under the film's rule, with the row's month and year, fitting beside or on its bar; on a
 *           landing frame every such row for a country on the board is drawn (kits/rtt-104/render_stills_v3.js);
 *   LAYOUT  no bar, name, value or tag inside the world panel or legend or past the board edge.
 * Every landing frame (each year's figures, 1997-2025):
 *   VALUES  ranks 1-20 and their one-decimal figures = v3_change_events.csv, and ranks 1-10 = data/rtt-104/boards.csv
 *           (board "top") exactly.
 * Landing frames of 1997, 2008, 2019 and 2025:
 *   PHONE   names, values and tags at least 5.9 pt at 390 pt wide, other text at least 5.0 pt; with stills_out_dir
 *           (outside the repo: the stills are private) each is saved at 1920 x 1080 and as a phone copy (390 pt at 3x).
 * Writes tests/rtt104/FILM_CHECK_V3.md (text only); exits 1 on any failure.
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const R = require(path.join(ROOT, 'kits', 'rtt-104', 'render_rtt104.js'));
const C = require(path.join(ROOT, 'kits', 'rtt-104', 'render_stills_v3.js'));
const PHONE_YEARS = [1997, 2008, 2019, 2025], pt = px => px * 390 / 1920;

function boardsTop(year) {
  const lines = fs.readFileSync(path.join(ROOT, 'data', 'rtt-104', 'boards.csv'), 'utf8').split(/\r?\n/).filter(Boolean);
  const h = lines.shift().split(','), ix = k => h.indexOf(k);
  return lines.map(l => l.split(',')).filter(r => +r[ix('year')] === year && r[ix('board')] === 'top')
    .sort((a, b) => a[ix('rank')] - b[ix('rank')]).map(r => r[ix('iso3')] + ' ' + r[ix('value_1dp')] + '%');
}

async function main() {
  const cfgFile = process.argv[2], out = process.argv[3];
  if (!cfgFile) throw new Error('usage: film_check_v3.js <config> [stills_out_dir]');
  if (out && path.resolve(out).startsWith(ROOT + path.sep)) throw new Error('stills are private: write them outside the repository');
  const cfg = R.config(cfgFile), { br, pg } = await R.open(cfg);
  const plan = await pg.evaluate(() => ({ total: RACE_FRAMES, card: PLAN.card ? PLAN.card.from : null, landing: PLAN.landing }));
  const end = plan.card != null ? plan.card : plan.total;
  const atLand = Object.fromEntries(Object.entries(plan.landing).map(([y, f]) => [f, +y]));
  const fails = new Set(), seen = new Set(), rows = [];
  let vals = 0, top10 = 0;
  for (let f = 0; f < end; f++) {
    await R.frame(pg, f);
    const st = await C.grab(pg), ly = atLand[f];
    for (const x of [...C.checkTags(st, cfg, ly && ly !== 1997 ? ly : null), ...C.checkLayout(st)]) fails.add(`frame ${f}: ${x}`);
    st.labels.filter(l => l.kind === 'tag' && l.alpha > 0.05).forEach(l => seen.add(l.id + ' ' + l.year));
    if (ly) {
      const got = st.bars.slice().sort((a, b) => a.slot - b.slot).map(b => b.id + ' ' + b.value);
      if (got.join('|') === C.wantBoard(ly, cfg.v3.rows).join('|')) vals++; else fails.add(`values ${ly}`);
      if (got.slice(0, 10).join('|') === boardsTop(ly).join('|')) top10++; else fails.add(`boards.csv top 10 ${ly}`);
      if (PHONE_YEARS.includes(ly)) {
        const p = C.checkPhone(st); p.fails.forEach(x => fails.add(`phone ${ly}: ${x}`));
        const f1 = k => p.min[k] ? pt(p.min[k]).toFixed(1) : '—';
        const other = Object.entries(p.min).filter(([k]) => !['name', 'value', 'tag'].includes(k)).reduce((m, [, x]) => Math.min(m, x), 1e9);
        rows.push(`| ${ly} | ${f} (${(f / 30).toFixed(1)} s) | ${f1('name')} / ${f1('value')} / ${f1('tag')} / ${pt(other).toFixed(1)} pt | ${p.fails.length ? 'FAIL' : 'PASS'} |`);
        if (out) {
          fs.mkdirSync(out, { recursive: true });
          const file = path.join(out, `rtt104_v3_${ly}_1920x1080.png`);
          await (await pg.$('#c')).screenshot({ path: file });
        }
      }
    }
  }
  await br.close();
  if (out) {   // phone copies, as render_stills_v3.js
    const { chromium } = require(require.resolve('playwright', { paths: [path.join(ROOT, 'kits', 'rtt-002')] }));
    const b2 = await chromium.launch({ executablePath: process.env.PW_CHROME || '/opt/pw-browsers/chromium' });
    const ph = await b2.newPage({ viewport: { width: 390, height: Math.round(390 * 9 / 16) }, deviceScaleFactor: 3 });
    for (const y of PHONE_YEARS) {
      const f = path.join(out, `rtt104_v3_${y}_1920x1080.png`);
      await ph.setContent(`<body style="margin:0;background:#000"><img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:390px;display:block"></body>`);
      await ph.waitForLoadState('load'); await ph.screenshot({ path: path.join(out, `rtt104_v3_${y}_phone_390pt.png`) });
      fs.unlinkSync(f);   // the release carries the phone copies only
    }
    await b2.close();
  }
  const n = Object.keys(plan.landing).length, ok = !fails.size;
  const report = ['# RTT-104 V3 whole-film check (IQ-24g)', '',
    `Written by \`tests/rtt104/film_check_v3.js ${cfgFile}\`. Every frame 0–${end - 1} (${(end / 30).toFixed(1)} s): tags and layout; every landing frame: values.`, '',
    `- Landing frames: ranks 1–20 = \`v3_change_events.csv\` ${vals}/${n}; ranks 1–10 = \`boards.csv\` ${top10}/${n}.`,
    `- Tags shown: ${seen.size} (each a VERIFIED row with a fetched excerpt, rule ${cfg.v3.tag.rule}).`,
    `- Tag and layout checks, every frame: ${[...fails].filter(x => x.startsWith('frame')).length ? 'FAIL' : 'PASS'}.`, '',
    '| Phone still | Frame | Smallest name / value / tag / other | Result |', '|---|---|---|---|', ...rows, '',
    ok ? 'Overall: PASS.' : 'Overall: FAIL: ' + [...fails].slice(0, 20).join('; '), ''];
  fs.writeFileSync(path.join(ROOT, 'tests', 'rtt104', 'FILM_CHECK_V3.md'), report.join('\n'));
  console.log(report.slice(4, 7).join('\n')); console.log(ok ? 'film check PASS' : 'film check FAIL');
  process.exit(ok ? 0 : 1);
}
main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
