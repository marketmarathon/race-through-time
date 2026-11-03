/* Race Through Time thumbnail TEMPLATE v2 (IQ-27, owner decision 3 Nov 2026: one fixed thumbnail template for every
 * video; refines DEC-800/801; how: DEC-803 kept). A PROPOSAL for Luke (DEC-069): nothing here replaces a live thumbnail.
 *
 *   RTT_ASSETS_ROOT=<dir> node kits/thumbnails/template_v2.js OUT_DIR [rtt-001 ...]
 *
 * One layout, one type, one place for everything, on every video:
 *   - a plain white background (the house default, DEC-809);
 *   - left: the race board, at most 6 bars (variant A) or 5 bars (variant B), in a card of fixed size and place;
 *   - right: the subject in 2-4 huge words (Archivo 900, black), the years under them (Archivo 800, red), and ONE hero
 *     picture (a file already on the episode's private-file list and in reference/rights_ledger.md, or a flag from the
 *     flag-icons package for RTT-104); variant B makes the hero larger and the board smaller;
 *   - the RTT globe badge and name, small, top right, on every video; nothing bottom right (YouTube's length badge).
 *   - no taglines, no question marks.
 *
 * The board (DEC-803 kept): drawn by the episode's OWN approved film config and player, frame by frame to the frame
 * where the chosen period's figures land, redrawn 45 times so rows come to rest, then only cropped, never edited.
 * What differs from the film frame is layout only, set in kits/thumbnails/v2/rtt-###.json `variants.X.overrides`: the
 * number of rows (6 or 5), the bar end, the text size caps (board.name_cap / value_cap, player keys added in IQ-27,
 * unset = the approved 38 / 36) and side panels switched off. The check (render_thumbnails.js `check`, unchanged) then
 * compares every bar on the crop with the episode's own data file (figure, value label at its precision, order, one
 * scale), and a new top-N check proves the board shows exactly the N largest figures of that period in the data (ties
 * at the cut allowed). Any failure stops the render.
 *
 * Output per episode and variant: <kit>_v2<A|B>_1280x720.png and .jpg (JPG under 2 MB), _320x180_phone_feed.png,
 * _168x94_sidebar.png, <kit>_v2<A|B>_check.json; plus v2_side_by_side_<kit>.png (A and B together) and
 * v2_contact_sheet_A.png (the six A thumbnails as on the channel's Videos page, with each video's YouTube title).
 * OUT_DIR must be outside the repo; the workflow saves it only as a private pre-release (DEC-006, DEC-060).
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const rtt = require('../rtt-002/rtt.js');
const T = require('./render_thumbnails.js');
const W = 1280, H = 720;

/* the fixed template: every position in px on the 1280 x 720 thumbnail */
const LAYOUT = {
  A: { board: { x: 26, y: 78, w: 704, h: 600 }, col: { x: 756, r: 1256 }, hero: { w: 420, h: 200 }, words_max: 150 },
  B: { board: { x: 26, y: 140, w: 560, h: 480 }, col: { x: 612, r: 1256 }, hero: { w: 600, h: 250 }, words_max: 140 }
};
const INK = '#0B1424', RED = '#E0301E';

function v2configs(only) {
  const dir = path.join(__dirname, 'v2');
  return fs.readdirSync(dir).filter(f => /^rtt-\d{3}\.json$/.test(f)).map(f => f.replace('.json', ''))
    .filter(e => !only.length || only.includes(e))
    .map(e => {
      const V = JSON.parse(fs.readFileSync(path.join(dir, e + '.json'), 'utf8'));
      const B = JSON.parse(fs.readFileSync(path.join(__dirname, V.base), 'utf8'));
      return { e, V, B };
    });
}

/* the N bars of the board (top N rows, settled) and the box around them and everything drawn for them */
function boardBox(st, n, pad) {
  const bars = st.bars.filter(b => b.alpha > 0.05).sort((a, b) => a.rect.y - b.rect.y).slice(0, n);
  const ids = new Set(bars.map(b => b.id));
  const boxes = bars.map(b => b.rect);
  for (const l of st.labels) if (ids.has(l.id) && l.alpha > 0.05 && l.w > 0) {
    const asc = l.asc != null ? l.asc : (l.size || 30) * 0.8, desc = l.desc != null ? l.desc : (l.size || 30) * 0.2;
    boxes.push({ x: l.x, y: l.kind === 'flag' ? l.y : l.y - asc, w: l.w, h: l.kind === 'flag' ? (l.h || 0) : asc + desc });
  }
  for (const p of st.pics || []) if (ids.has(p.id)) boxes.push(p.box);
  for (const p of st.logos || []) if (ids.has(p.id) && p.tile) boxes.push(p.tile);
  for (const f of st.flags || []) if (ids.has(f.id) && f.w) boxes.push({ x: f.x, y: f.y, w: f.w, h: f.h });
  if (st.crown && ids.has(st.crown.id) && st.crown.alpha > 0.05) boxes.push({ x: st.crown.x, y: st.crown.y, w: st.crown.w, h: st.crown.h });
  const x0 = Math.min(...boxes.map(b => b.x)) - pad, y0 = Math.min(...boxes.map(b => b.y)) - Math.min(pad, 6);   // little room above the first row: the axis numbers sit just above it
  const x1 = Math.max(...boxes.map(b => b.x + b.w)) + pad, y1 = Math.max(...boxes.map(b => b.y + b.h)) + pad;
  return { bars, ids, x0, y0, x1, y1 };
}
/* widen or heighten the box to the card's aspect, inside the 1920 x 1080 frame (the film's own ground fills it) */
function toAspect(b, aspect, nextRowY) {
  let x = Math.max(0, b.x0), y = Math.max(0, b.y0), w = Math.min(1920, b.x1) - x, h = Math.min(1080, b.y1) - y;
  if (w / h > aspect) { const nh = Math.min(1080, w / aspect); y = Math.min(Math.max(0, y - (nh - h) / 2), 1080 - nh); h = nh; if (h * aspect > w) { const nw = h * aspect; x = Math.max(0, Math.min(x, 1920 - nw)); w = nw; } }   // the extra room split above and below the rows
  else { const nw = h * aspect; x = Math.max(0, x - (nw - w) * 0.15); w = nw; if (x + w > 1920) { x = 1920 - w; } }
  return { x: +x.toFixed(1), y: +y.toFixed(1), w: +w.toFixed(1), h: +h.toFixed(1) };
}

/* top-N: the bars on the card are the N largest figures of the period in the data (ties at the cut allowed) */
function topN(C, date, ids, n) {
  const all = T.dataAt(C, date, [...ids].map(id => ({ id })));
  const K = C.check;
  let vals;
  if (K.type === 'f1_wins') vals = null;
  else {
    const want = K.period === 'month' ? date.slice(0, 7) : date, v = {};
    for (const r of T.csv(path.join(T.ROOT, K.file))) if (r[K.date_col] === want) v[K.id_lower ? r[K.id_col].toLowerCase() : r[K.id_col]] = +r[K.value_col];
    vals = v;
  }
  if (!vals) {               // RTT-002: every driver's wins after the race, from the wide file
    const wide = T.csv(path.join(T.ROOT, K.wins_file)).find(r => r.race_date === date);
    const byName = Object.fromEntries(T.csv(path.join(T.ROOT, K.drivers_file)).map(r => [r[K.name_col || 'display_name'], r.driver_id]));
    vals = {};
    for (const [col, x] of Object.entries(wide)) if (byName[col]) vals[byName[col]] = +x;
  }
  const on = [...ids].map(id => vals[id]).filter(Number.isFinite), off = Object.entries(vals).filter(([id, x]) => !ids.has(id) && Number.isFinite(x)).map(([, x]) => x);
  const errs = [];
  if (on.length !== n) errs.push(`top-${n}: ${on.length} of the card's bars have a data value`);
  if (off.length && Math.min(...on) < Math.max(...off)) errs.push(`top-${n}: a bar off the card (${Math.max(...off)}) is larger than one on it (${Math.min(...on)})`);
  return { errs, cut: off.length ? Math.max(...off) : null, smallest_on: Math.min(...on), all };
}

function heroHtml(V, assets, L) {
  const h = V.hero;
  let src;
  if (h.flag) {
    if (!/^[a-z]{2}$/.test(h.flag)) throw new Error('hero.flag must be an ISO alpha-2 code');
    src = T.dataUrl(path.join(path.dirname(require.resolve('flag-icons/package.json', { paths: [rtt.KIT] })), 'flags', '4x3', h.flag + '.svg'));
  } else src = T.dataUrl(path.join(assets, h.file));
  const k = h.scale || 1, frame = h.flag ? 'box-shadow:0 0 0 2px #D9DEE7,0 6px 18px rgba(11,20,36,.25);border-radius:10px' : '';
  return `<div class="hero"><img src="${src}" style="max-width:${Math.round(L.hero.w * k)}px;max-height:${Math.round(L.hero.h * k)}px;${frame}"></div>`;
}

function page(V, variant, boardPng, crop, assets, fontDir) {
  const L = LAYOUT[variant], bw = L.board.w, bh = L.board.h;
  const fonts = [800, 900].map(w => `@font-face{font-family:Archivo;font-weight:${w};src:url("file://${fontDir}/archivo-latin-${w}-normal.woff2") format("woff2")}`).join('');
  const words = V.words.map(w => `<div class="w">${T.esc(w)}</div>`).join('');
  const mark = T.dataUrl(path.join(assets, 'rtt_logo.png'));
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fonts}
  html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:#FFFFFF;font-family:Archivo}
  .board{position:absolute;left:${L.board.x}px;top:${L.board.y}px;width:${bw}px;height:${bh}px;overflow:hidden;border-radius:16px;box-shadow:0 8px 26px rgba(11,20,36,.30);background:#0b1424}
  .board img{position:absolute;left:${-crop.x * bw / crop.w}px;top:${-crop.y * bh / crop.h}px;width:${1920 * bw / crop.w}px;height:${1080 * bh / crop.h}px}
  .col{position:absolute;left:${L.col.x}px;width:${L.col.r - L.col.x}px;top:0;text-align:center;color:${INK}}
  .w{font-weight:900;line-height:.92;letter-spacing:-.01em;white-space:nowrap;font-size:${L.words_max}px}
  .y{font-weight:800;color:${RED};font-size:62px;margin-top:12px;letter-spacing:.01em}
  .hero{margin-top:22px;display:flex;justify-content:center;align-items:center}
  .hero img{display:block}
  .mark{position:absolute;right:20px;top:16px;display:flex;align-items:center;gap:8px;color:${INK};font-weight:800;font-size:19px;letter-spacing:.06em}
  .mark img{width:38px;height:38px}
  </style></head><body>
  <div class="board"><img src="file://${boardPng}"></div>
  <div class="col">${words}<div class="y">${T.esc(V.years)}</div>${heroHtml(V, assets, L)}</div>
  <div class="mark"><img src="${mark}">RACE THROUGH TIME</div>
  <script>
  window.layoutDone = (async () => {
    await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode()));
    const col = document.querySelector('.col'), cw = col.clientWidth;
    /* the same size for every word of a subject: the largest (up to ${L.words_max} px) at which its longest word fits */
    const ws = [...document.querySelectorAll('.w')]; let f = ${L.words_max};
    const fits = () => ws.every(w => { w.style.display = 'inline-block'; const ok = w.offsetWidth <= cw; w.style.display = 'block'; return ok; });
    while (!fits() && f > 30) { f -= 1; ws.forEach(w => w.style.fontSize = f + 'px'); }
    /* the column centred top to bottom (below the badge row) */
    const r = col.getBoundingClientRect(); col.style.top = Math.round(56 + (${H} - 56 - r.height) / 2) + 'px';
    const hero = document.querySelector('.hero img').getBoundingClientRect(), c2 = col.getBoundingClientRect();
    return { word_px: f, col_top: c2.top, col_bottom: c2.bottom, hero: [hero.left, hero.top, hero.right, hero.bottom] };
  })();
  </script></body></html>`;
}

async function main() {
  const out = path.resolve(process.argv[2] || '');
  if (!process.argv[2] || out.startsWith(T.ROOT + path.sep)) { console.error('usage: node kits/thumbnails/template_v2.js OUT_DIR (outside the repo) [rtt-### ...]'); process.exit(2); }
  if (!process.env.RTT_ASSETS_ROOT) { console.error('RTT_ASSETS_ROOT is not set'); process.exit(2); }
  fs.mkdirSync(out, { recursive: true });
  const fontDir = path.join(path.dirname(require.resolve('@fontsource/archivo/package.json', { paths: [rtt.KIT] })), 'files');
  const { chromium } = require(require.resolve('playwright', { paths: [rtt.KIT] }));
  const files = [], made = [];
  let failed = false;
  for (const { e, V, B } of v2configs(process.argv.slice(3))) {
    const assets = path.join(path.resolve(process.env.RTT_ASSETS_ROOT), B.kit);
    process.env.RTT_LOCAL_ASSETS = assets;
    if (V.hero.file && !fs.existsSync(path.join(assets, V.hero.file))) throw new Error(e + ': hero ' + V.hero.file + ' not found');
    const film = rtt.loadConfig('../' + B.kit + '/' + B.film_config);
    const at = process.env.THUMB_AT_TEST || V.at || B.at;     // THUMB_AT_TEST: layout trials only, never a deliverable
    const data = JSON.parse(fs.readFileSync(path.resolve(rtt.KIT, film.race_file), 'utf8'));
    for (const variant of Object.keys(V.variants)) {
      const X = V.variants[variant], L = LAYOUT[variant], stem = `${B.kit}_v2${variant}`;
      const cfg = T.merge(T.merge(film, V.overrides || {}), X.overrides || {});
      const D = await T.drawTo({ kit: B.kit, film_config: B.film_config, at, settle: V.settle }, cfg, data);
      let rec;
      try {
        D.st.crown = await D.pg.evaluate(() => window.__CROWN || null);      // the leader's crown, so the crop keeps it whole
        const bx = boardBox(D.st, X.bars, V.pad != null ? V.pad : 14);
        const crop = toAspect(bx, L.board.w / L.board.h);
        const C2 = Object.assign({}, B, { crop: { x: crop.x, y: Math.max(crop.y, bx.y0), w: crop.w, h: bx.y1 - Math.max(crop.y, bx.y0) }, min_bars: X.bars });
        const res = T.check(C2, at, D.st);
        const tn = topN(B, at, bx.ids, X.bars);
        const onCrop = res.rows.length;
        const errs = res.errs.concat(tn.errs);
        if (onCrop !== X.bars) errs.push(`${onCrop} bars on the card, want ${X.bars}`);
        const missing = [...(D.st.logos || []).filter(p => !p.drawn && bx.ids.has(p.id)), ...(D.st.pics || []).filter(p => bx.ids.has(p.id) && (p.placeholder || (p.drawn == null && !p.own)))];
        if (missing.length) errs.push('pictures not found: ' + missing.map(p => p.id).join(', '));
        rec = { episode: B.episode, template: 'v2', variant, film_config: 'kits/' + B.kit + '/' + B.film_config, layout_overrides: Object.assign({}, V.overrides || {}, X.overrides || {}),
                period: at, frame: D.target, film_frames: D.total, crop, bars: res.rows,
                text_px: (() => { const k = L.board.w / crop.w, nm = Math.min(...D.st.labels.filter(l => l.kind === 'name' && bx.ids.has(l.id)).map(l => l.size || 1e9)); return { name_on_frame: nm, name_at_1280: +(nm * k).toFixed(1), name_at_320: +(nm * k / 4).toFixed(1), name_at_168: +(nm * k * 168 / 1280).toFixed(1) }; })(), top_n: { n: X.bars, smallest_on_card: tn.smallest_on, largest_off_card: tn.cut }, errors: errs };
        fs.writeFileSync(path.join(out, stem + '_check.json'), JSON.stringify(rec, null, 1)); files.push(path.join(out, stem + '_check.json'));
        console.log(`${B.episode} ${variant}: ${at}, frame ${D.target} of ${D.total}; ${onCrop} bars on the card; ` + (errs.length ? 'CHECK FAILED:\n  ' + errs.join('\n  ') : `every bar = the data file (figure, label, order, one scale); the top ${X.bars} of the period`));
        if (errs.length) { failed = true; continue; }
        const boardPng = path.join(out, `_${stem}_board.png`);
        await (await D.pg.$('#c')).screenshot({ path: boardPng });
        rec.boardPng = boardPng;
      } finally { await D.br.close(); }
      const br = await chromium.launch({ executablePath: T.CHROME });
      try {
        const pg = await br.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
        const html = path.join(out, '_' + stem + '.html');
        fs.writeFileSync(html, page(V, variant, rec.boardPng, rec.crop, assets, fontDir));
        await pg.goto('file://' + html);
        const lay = await pg.evaluate(() => window.layoutDone);
        if (!(await pg.evaluate(() => document.fonts.check('900 100px Archivo')))) throw new Error('Archivo 900 did not load');
        if (lay.col_top < 52 || lay.col_bottom > H - 10) throw new Error(stem + ': the words and hero do not fit top to bottom (' + Math.round(lay.col_top) + '-' + Math.round(lay.col_bottom) + ')');
        if (lay.hero[2] > W - 150 && lay.hero[3] > H - 70) throw new Error(stem + ': the hero reaches the bottom-right corner (YouTube shows the length there)');
        fs.unlinkSync(html);
        const png = path.join(out, stem + '_1280x720.png'), jpg = path.join(out, stem + '_1280x720.jpg');
        await pg.screenshot({ path: png }); await pg.screenshot({ path: jpg, type: 'jpeg', quality: 92 });
        if (fs.statSync(jpg).size >= T.JPG_MAX) throw new Error(jpg + ' is not under 2 MB');
        files.push(png, jpg);
        for (const [w, h, tag] of T.SIZES) {
          await pg.setViewportSize({ width: w, height: h });
          await pg.setContent(`<body style="margin:0"><img src="${T.dataUrl(png)}" style="width:${w}px;height:${h}px;display:block"></body>`);
          await pg.evaluate(() => document.images[0].decode());
          const f = path.join(out, `${stem}_${w}x${h}_${tag}.png`); await pg.screenshot({ path: f }); files.push(f);
        }
        made.push({ e, variant, png, title: V.yt_title, word_px: lay.word_px });
        rec.word_px = lay.word_px; delete rec.boardPng;
        fs.writeFileSync(path.join(out, stem + '_check.json'), JSON.stringify(rec, null, 1));
      } finally { await br.close(); }
      if (!process.env.THUMB_KEEP_BOARD) fs.unlinkSync(path.join(out, `_${stem}_board.png`));
    }
  }
  /* review sheets: A and B side by side per episode; the six A thumbnails as on the channel's Videos page */
  const br = await chromium.launch({ executablePath: T.CHROME });
  try {
    const pg = await br.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
    const byE = {};
    for (const m of made) (byE[m.e] = byE[m.e] || {})[m.variant] = m;
    for (const [e, v] of Object.entries(byE)) if (v.A && v.B) {
      await pg.setViewportSize({ width: 2 * 1280 + 3 * 40, height: 720 + 2 * 40 + 50 });
      await pg.setContent(`<body style="margin:0;background:#E9ECF1;font:700 30px sans-serif;color:#0B1424">
        <div style="display:flex;gap:40px;padding:20px 40px 40px">${['A', 'B'].map(k => `<div><div style="height:50px">${k}${k === 'A' ? ' · 6 bars' : ' · 5 bars, larger picture'}</div><img src="${T.dataUrl(v[k].png)}" style="width:1280px;height:720px;display:block"></div>`).join('')}</div></body>`);
      await pg.evaluate(() => Promise.all([...document.images].map(i => i.decode())));
      const f = path.join(out, `v2_side_by_side_${e}.png`); await pg.screenshot({ path: f, fullPage: true }); files.push(f);
    }
    const A = made.filter(m => m.variant === 'A');
    if (A.length > 1) {
      /* YouTube's channel Videos grid on a desktop: about 4 across at ~310 px wide (we use 3 across at 360 px so two rows hold six) */
      await pg.setViewportSize({ width: 1180, height: 760 });
      await pg.setContent(`<body style="margin:0;background:#FFFFFF;font-family:Roboto,Arial,sans-serif;color:#0F0F0F">
        <div style="padding:24px 28px 8px;font:500 16px Roboto,Arial,sans-serif;color:#606060">Race Through Time · Videos (mock-up of the channel page, A thumbnails)</div>
        <div style="display:grid;grid-template-columns:repeat(3,360px);gap:28px 16px;padding:12px 28px">
        ${A.map(m => `<div><img src="${T.dataUrl(m.png)}" style="width:360px;height:202px;border-radius:12px;display:block">
          <div style="font-weight:500;font-size:15px;line-height:21px;margin-top:10px">${T.esc(m.title || m.e)}</div></div>`).join('')}</div></body>`);
      await pg.evaluate(() => Promise.all([...document.images].map(i => i.decode())));
      const f = path.join(out, 'v2_contact_sheet_A.png'); await pg.screenshot({ path: f, fullPage: true }); files.push(f);
    }
  } finally { await br.close(); }
  for (const f of files) console.log(crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex') + '  ' + path.basename(f));
  if (failed) { console.error('::error::a thumbnail check failed (see above); nothing was drawn for that board'); process.exit(2); }
}
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
module.exports = { LAYOUT, boardBox, toAspect, topN };
