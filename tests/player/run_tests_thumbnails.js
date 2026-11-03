/* Tests for the thumbnail renderer's checks (IQ-23, kits/thumbnails/render_thumbnails.js). No browser needed.
 *   node tests/player/run_tests_thumbnails.js
 * 1. the board check catches a bar drawn too long (the ChatGPT image for RTT-103 drew one about 20% too long, DEC-801),
 *    a figure or label that differs from the data, and bars out of order; and passes a correct board;
 * 2. value labels are read at their own precision ("~5.9bn", "$128.3bn", "23.9%", "160.0m+");
 * 3. every config: the crop is inside the 1920 x 1080 frame, every picture is on the episode's private-file list (so it
 *    is a file already in the rights ledger, never a new one), and no image file sits in the public repo's kits/thumbnails.
 */
const fs = require('fs'), path = require('path');
const T = require('../../kits/thumbnails/render_thumbnails.js');
const ROOT = path.resolve(__dirname, '..', '..'), DIR = path.join(ROOT, 'kits', 'thumbnails');
let fails = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };

/* 1. the board check, on a made-up board against a made-up data file */
const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'rtt-thumb-test-'));
const rel = path.relative(ROOT, path.join(tmp, 'series.csv'));
fs.writeFileSync(path.join(tmp, 'series.csv'), 'date,id,v\n2020-01-31,a,100\n2020-01-31,b,80\n2020-01-31,c,40\n');
const C = { crop: { x: 0, y: 0, w: 1920, h: 1080 }, min_bars: 3,
            check: { file: rel, date_col: 'date', id_col: 'id', value_col: 'v', label_units: { m: 1e6 } } };
const board = (wB, vB, labB) => ({
  bars: [{ id: 'a', units: 100, alpha: 1, rect: { x: 100, y: 100, w: 1000, h: 40 } },
         { id: 'b', units: vB, alpha: 1, rect: { x: 100, y: 150, w: wB, h: 40 } },
         { id: 'c', units: 40, alpha: 1, rect: { x: 100, y: 200, w: 400, h: 40 } }],
  labels: [{ kind: 'value', id: 'a', text: '100' }, { kind: 'value', id: 'b', text: labB }, { kind: 'value', id: 'c', text: '40' }] });
ok(T.check(C, '2020-01-31', board(800, 80, '80')).errs.length === 0, 'a correct board passes');
const long = T.check(C, '2020-01-31', board(960, 80, '80')).errs;
ok(long.some(e => /off the common scale/.test(e)), 'a bar drawn 20% too long is caught (' + long[0] + ')');
ok(T.check(C, '2020-01-31', board(810, 81, '81')).errs.some(e => /bar figure 81 != data 80/.test(e)), 'a figure that differs from the data is caught');
ok(T.check(C, '2020-01-31', board(800, 80, '79')).errs.some(e => /not the data/.test(e)), 'a label that differs from the data is caught');
const swapped = board(800, 80, '80'); swapped.bars[1].rect.y = 50;
ok(T.check(C, '2020-01-31', swapped).errs.some(e => /^order/.test(e)), 'bars out of data order are caught');
fs.rmSync(tmp, { recursive: true });

/* 2. labels at their own precision */
const L = (t, u, want, half) => { const p = T.parseLabel(t, { label_units: u }); return p && Math.abs(p.shown - want) < 1e-6 * want && Math.abs(p.half - half) < 1e-6 * half; };
ok(L('~5.9bn', { m: 1e6, bn: 1e9 }, 5.9e9, 0.05e9), '"~5.9bn" = 5.9bn, to the nearest 0.1bn');
ok(L('$128.3bn', { m: 1e6, bn: 1e9 }, 128.3e9, 0.05e9), '"$128.3bn" = 128.3bn, to the nearest 0.1bn');
ok(L('23.9%', { '%': 1 }, 23.9, 0.05), '"23.9%" = 23.9, to the nearest 0.1');
ok(L('160.0m+ · retired', { m: 1e6 }, 160e6, 0.05e6), '"160.0m+ · retired" = 160.0m, to the nearest 0.1m');

/* 3. the configs */
const imgs = fs.readdirSync(DIR).filter(f => /\.(png|jpe?g|gif|webp|svg)$/i.test(f));
ok(imgs.length === 0, 'no image file in kits/thumbnails (DEC-006, DEC-060)' + (imgs.length ? ': ' + imgs.join(', ') : ''));
for (const f of fs.readdirSync(DIR).filter(f => /^rtt-\d{3}\.json$/.test(f))) {
  const c = JSON.parse(fs.readFileSync(path.join(DIR, f), 'utf8'));
  ok(c.crop.x >= 0 && c.crop.y >= 0 && c.crop.x + c.crop.w <= 1920 && c.crop.y + c.crop.h <= 1080, f + ': crop inside the frame');
  const listed = new Set(fs.readFileSync(path.join(ROOT, c.assets_list), 'utf8').split('\n').filter(l => l && !l.startsWith('#'))
    .map(l => l.trim().split(/\s+/)[1].replace(/^assets\/rtt-\d{3}\//, '')));
  const pics = ['rtt_logo.png', ...(c.rows || []).flatMap(r => r.items.map(i => i.file))];
  const off = pics.filter(p => !listed.has(p));
  ok(!off.length, f + ': every picture (' + pics.length + ') is a listed private file' + (off.length ? '; not listed: ' + off.join(', ') : ''));
  ok(fs.existsSync(path.join(ROOT, 'kits', c.kit, c.film_config)), f + ': film config kits/' + c.kit + '/' + c.film_config + ' exists');
}
/* 4. template v2 (IQ-27): the configs, the crop helpers and the top-N check */
{
  const V2 = require(path.join(ROOT, 'kits', 'thumbnails', 'template_v2.js'));
  const vdir = path.join(DIR, 'v2');
  const vimgs = fs.readdirSync(vdir).filter(f => /\.(png|jpe?g|gif|webp|svg)$/i.test(f));
  ok(vimgs.length === 0, 'no image file in kits/thumbnails/v2');
  const v2 = fs.readdirSync(vdir).filter(f => /^rtt-\d{3}\.json$/.test(f));
  ok(v2.length === 6, 'template v2 has a config for all six public videos (' + v2.join(', ') + ')');
  for (const f of v2) {
    const V = JSON.parse(fs.readFileSync(path.join(vdir, f), 'utf8')), c = JSON.parse(fs.readFileSync(path.join(DIR, V.base), 'utf8'));
    ok(V.words.length >= 1 && V.words.length <= 2 && V.words.join(' ').split(/\s+/).length >= 2 && V.words.join(' ').split(/\s+/).length <= 4, 'v2/' + f + ': 2-4 words (' + V.words.join(' ') + ')');
    ok(!/[?!]/.test(V.words.join(' ')), 'v2/' + f + ': no question or exclamation mark (no taglines)');
    ok(/^\d{4}–\d{4}$/.test(V.years), 'v2/' + f + ': years as "YYYY–YYYY"');
    ok(V.variants.A.bars <= 6 && V.variants.B.bars === 5, 'v2/' + f + ': A at most 6 bars, B 5 bars');
    if (V.hero.file) {
      const listed = new Set(fs.readFileSync(path.join(ROOT, c.assets_list), 'utf8').split('\n').filter(l => l && !l.startsWith('#'))
        .map(l => l.trim().split(/\s+/)[1].replace(/^assets\/rtt-\d{3}\//, '')));
      ok(listed.has(V.hero.file), 'v2/' + f + ': hero ' + V.hero.file + ' is a listed private file');
    } else ok(/^[a-z]{2}$/.test(V.hero.flag) && fs.existsSync(path.join(ROOT, 'kits', 'rtt-002', 'node_modules', 'flag-icons', 'flags', '4x3', V.hero.flag + '.svg')),
              'v2/' + f + ': hero flag ' + V.hero.flag + ' from flag-icons (MIT, rights ledger)');
    const allowed = ['rows', 'barend', 'board_top', 'title', 'subtitle', 'footer', 'measure', 'time_label', 'date_block', 'source_line', 'board', 'pictures', 'bar_logos',
                     'maker_key', 'overlays', 'combined', 'story', 'v3'];
    const keys = [...Object.keys(V.overrides || {}), ...Object.values(V.variants).flatMap(x => Object.keys(x.overrides || {}))];
    const bad = keys.filter(k => !allowed.includes(k));
    ok(!bad.length, 'v2/' + f + ': overrides change layout only (' + (bad.length ? 'not allowed: ' + bad.join(', ') : 'rows, margins, text caps, side panels') + ')');
  }
  const crop = V2.toAspect({ x0: 50, y0: 40, x1: 1250, y1: 1000 }, 704 / 600);
  ok(crop.x >= 0 && crop.y >= 0 && crop.x + crop.w <= 1920.01 && crop.y + crop.h <= 1080.01 && Math.abs(crop.w / crop.h - 704 / 600) < 1e-3, 'toAspect keeps the card aspect inside the frame');
}
console.log(fails ? fails + ' FAILED' : 'all thumbnail tests PASS');
process.exit(fails ? 1 : 0);
