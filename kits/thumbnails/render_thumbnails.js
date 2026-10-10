/* Race Through Time thumbnails (IQ-23, owner DEC-800 to DEC-802): a real board from the approved film on the left,
 * 2-4 big words and the years on the right, a row of recognisable logos or pictures, a bright background.
 * One config per episode (kits/thumbnails/rtt-###.json); a later episode needs only a new config.
 *
 *   RTT_ASSETS_ROOT=<dir> node kits/thumbnails/render_thumbnails.js OUT_DIR [rtt-001 ...]
 *
 * RTT_ASSETS_ROOT holds one folder per episode (rtt-001/, rtt-002/, ...) laid out as that episode's film workflow lays
 * out RTT_LOCAL_ASSETS (rtt_logo.png, logos/, icons/, photos/). Everything drawn comes from there or from the kit's npm
 * packages (flags, Archivo); nothing is fetched here. Thumbnails are private (DEC-006, DEC-060): OUT_DIR must be outside
 * the repo, and the workflow saves it only as a private pre-release.
 *
 * For each episode:
 *  1. the board: the approved film config is drawn frame by frame (raster 2, 3840 x 2160) up to the frame where the
 *     chosen period's figures land (series films: TL.quarterEndFrame; event films: the last frame of the race's beat),
 *     then that frame is redrawn `settle` times so rows caught mid-glide come to rest (as kits/rtt-001/render_stills.js);
 *     the frame is never edited, only cropped (`crop`, in 1920 x 1080 coordinates);
 *  2. the check: every bar on the crop is read from the player (window.__BARS, window.__LABELS) and compared with the
 *     episode's data file (`check`): the bar's figure equals the data, its value label equals the data at the label's
 *     own precision, the bars are in data order and every bar's length is in proportion to its figure (one scale);
 *     any failure stops the render (exit 2);
 *  3. each option (`options`: background "white", "bright" or "dark") is laid out in HTML at 1280 x 720 and saved as
 *     PNG and JPG (JPG must be under 2 MB), plus 320 x 180 (phone feed) and 168 x 94 (sidebar) copies of the PNG;
 *  4. <episode>_check.json records the frame, the period, every bar's figure, label and data value.
 * Prints each file's SHA-256.
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const rtt = require('../rtt-002/rtt.js');
const ROOT = path.resolve(__dirname, '..', '..');
const CHROME = process.env.PW_CHROME || (fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined);
const W = 1280, H = 720, SIZES = [[320, 180, 'phone_feed'], [168, 94, 'sidebar']], JPG_MAX = 2 * 1024 * 1024;
const RASTER = 2;
function merge(base, over) {
  const out = Object.assign({}, base);
  for (const [k, v] of Object.entries(over || {}))
    out[k] = v && typeof v === 'object' && !Array.isArray(v) && base[k] && typeof base[k] === 'object' && !Array.isArray(base[k]) ? merge(base[k], v) : v;
  return out;
}

/* ---------- data files ---------- */
function csv(file) {
  const rows = [], txt = fs.readFileSync(file, 'utf8').replace(/\r/g, '');
  let row = [], cell = '', q = false;
  for (let i = 0; i < txt.length; i++) {
    const ch = txt[i];
    if (q) { if (ch === '"' && txt[i + 1] === '"') { cell += '"'; i++; } else if (ch === '"') q = false; else cell += ch; }
    else if (ch === '"') q = true;
    else if (ch === ',') { row.push(cell); cell = ''; }
    else if (ch === '\n') { row.push(cell); rows.push(row); row = []; cell = ''; }
    else cell += ch;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const head = rows.shift();
  return rows.filter(r => r.length === head.length).map(r => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}

/* the data value of every entity at the period, from the episode's own data file (not the player input) */
function dataAt(C, date, bars) {
  const K = C.check, out = {};
  if (K.type === 'f1_wins') {                    // RTT-002: wins after the race (cumulative_wins_wide.csv), starts (starts.csv)
    const wide = csv(path.join(ROOT, K.wins_file)).find(r => r.race_date === date);
    if (!wide) throw new Error('no race on ' + date + ' in ' + K.wins_file);
    const names = Object.fromEntries(csv(path.join(ROOT, K.drivers_file)).map(r => [r.driver_id, r[K.name_col || 'display_name']]));
    for (const b of bars) if (!(names[b.id] in wide)) throw new Error('no column for ' + b.id + ' (' + names[b.id] + ') in ' + K.wins_file);
    const starts = {};
    for (const r of csv(path.join(ROOT, K.starts_file))) if (+r.race_index <= +wide.race_index) starts[r.driver_id] = +r.career_starts_after;
    for (const b of bars) out[b.id] = { value: +wide[names[b.id]], starts: starts[b.id], name: names[b.id], race: wide.grand_prix + ' ' + wide.season };
    return out;
  }
  const want = K.period === 'month' ? date.slice(0, 7) : date;
  for (const r of csv(path.join(ROOT, K.file))) {
    if (r[K.date_col] !== want) continue;
    const id = K.id_lower ? r[K.id_col].toLowerCase() : r[K.id_col];
    out[id] = { value: +r[K.value_col] };
  }
  return out;
}

/* a value label as a number in the data file's unit, with the half-step of its last digit */
function parseLabel(txt, K) {
  const m = /([~<]?)\$?([0-9][0-9,]*(?:\.[0-9]+)?)\s*(bn|m|k|%)?/.exec(txt);
  if (!m) return null;
  const digits = m[2].replace(/,/g, ''), dec = (digits.split('.')[1] || '').length, mult = (K.label_units || {})[m[3] || ''] || 1;
  return { approx: m[1], shown: +digits * mult, half: 0.5 * Math.pow(10, -dec) * mult, text: m[0] };
}

/* the check: bars on the crop against the data file */
function check(C, date, st) {
  const K = C.check, crop = C.crop, errs = [];
  const inCrop = b => b.rect.y + b.rect.h > crop.y && b.rect.y < crop.y + crop.h && b.alpha > 0.05;
  const bars = st.bars.filter(inCrop).sort((a, b) => a.rect.y - b.rect.y);
  const data = dataAt(C, date, bars);
  const rows = [];
  for (const b of bars) {
    const d = data[b.id], lab0 = st.labels.find(l => l.kind === 'value' && l.id === b.id),
          stats = st.labels.find(l => l.kind === 'stats' && l.id === b.id);           // RTT-002: " · 306 starts · 29.7%"
    const lab = lab0 && stats ? { text: (lab0.text + ' ' + stats.text).replace(/\s+/g, ' ').trim() } : lab0;
    const row = { id: b.id, rank: rows.length + 1, figure: b.units, label: lab ? lab.text : null, data: d ? d.value : null, width_px: +b.rect.w.toFixed(2) };
    if (!d || !Number.isFinite(d.value)) { errs.push(b.id + ': no data value at ' + date); rows.push(row); continue; }
    const want = d.value * (K.units_per_value || 1);
    if (Math.abs(b.units - want) > 1e-6 * Math.max(1, Math.abs(want))) errs.push(`${b.id}: bar figure ${b.units} != data ${want}`);
    if (!lab) errs.push(b.id + ': no value label drawn');
    else if (K.type === 'f1_wins') {
      const m = /^(\d+) wins? · (\d+) starts? · ([0-9.]+)%$/.exec(lab.text);
      row.starts = d.starts;
      if (!m) errs.push(`${b.id}: label "${lab.text}" not in the form "W wins · S starts · P%"`);
      else {
        if (+m[1] !== d.value) errs.push(`${b.id}: label wins ${m[1]} != data ${d.value}`);
        if (+m[2] !== d.starts) errs.push(`${b.id}: label starts ${m[2]} != data ${d.starts}`);
        if (Math.abs(+m[3] - 100 * d.value / d.starts) > 0.05 + 1e-9) errs.push(`${b.id}: label rate ${m[3]}% != ${(100 * d.value / d.starts).toFixed(2)}%`);
      }
    } else {
      const p = parseLabel(lab.text, K);
      if (!p) errs.push(`${b.id}: label "${lab.text}" has no number`);
      else if (Math.abs(p.shown - d.value) > p.half * (1 + 1e-9)) errs.push(`${b.id}: label "${lab.text}" (${p.shown}) is not the data ${d.value} at the label's precision`);
    }
    rows.push(row);
  }
  for (let i = 1; i < rows.length; i++) if (rows[i].data > rows[i - 1].data) errs.push(`order: ${rows[i].id} (${rows[i].data}) is below ${rows[i - 1].id} (${rows[i - 1].data})`);
  /* one scale: every bar's length / its figure is the same (to within one pixel of the longest bar) */
  const scale = bars.map(b => b.rect.w / b.units), top = Math.max(...bars.map(b => b.rect.w)), k0 = bars[0].rect.w / bars[0].units;
  bars.forEach((b, i) => { const off = Math.abs(b.rect.w - k0 * b.units); rows[i].length_error_px = +off.toFixed(3); if (off > 1) errs.push(`${b.id}: bar is ${off.toFixed(1)} px off the common scale`); });
  if (bars.length < (C.min_bars || 1)) errs.push(`only ${bars.length} bars on the crop (want at least ${C.min_bars})`);
  return { rows, errs, longest_px: top, scale_spread: Math.max(...scale) / Math.min(...scale) - 1 };
}

/* ---------- the board frame ---------- */
/* draw `cfg` frame by frame to the landing frame of period C.at; returns the open player and what it drew */
async function drawTo(C, cfg, data) {
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: RASTER, chrome: CHROME });
  const info = await pg.evaluate(() => ({ dates: TL.events.map(e => e.date), start: TL.startFrame, qe: TL.quarterEndFrame || null,
                                          raceFrames: RACE_FRAMES }));
  const k = info.dates.indexOf(C.at);
  if (k < 0) { await br.close(); throw new Error(C.kit + ': no period ' + C.at + ' in ' + C.film_config); }
  if (k === info.dates.length - 1) { await br.close(); throw new Error(C.kit + ': ' + C.at + ' is the final table (not allowed: it spoils the ending)'); }
  const target = info.qe ? info.qe[k] : (info.start[k + 1] - 1);
  for (let f = 0; f <= target; f++) await rtt.drawFrame(pg, f, cfg);
  for (let i = 0; i < (C.settle != null ? C.settle : 45); i++) await rtt.drawFrame(pg, target, cfg);
  const st = await pg.evaluate(() => ({ bars: window.__BARS, labels: window.__LABELS, logos: window.__LOGOS, pics: window.__PICS,
                                         flags: window.__FLAGS, date: window.__DATEBLOCK || null }));
  return { br, pg, target, k, st, total: info.raceFrames };
}
/* what makes up the board: every bar (figure, place, length, colour) and every name, value and stats label and picture on it */
const boardOf = st => JSON.stringify({
  bars: st.bars.map(b => [b.id, b.units, b.rect, b.colour, b.alpha, b.style]),
  labels: st.labels.filter(l => ['value', 'stats', 'name'].includes(l.kind)).map(l => [l.kind, l.id, l.text, l.x, l.y, l.size]),
  pics: st.pics.map(p => [p.id, p.box, p.drawn]), logos: st.logos.map(p => [p.id, p.tile, p.drawn]), flags: st.flags.map(f => [f.id, f.code, f.x, f.y]) });

async function board(C, out) {
  process.env.RTT_LOCAL_ASSETS = path.join(path.resolve(process.env.RTT_ASSETS_ROOT || ''), C.kit);
  const film = rtt.loadConfig('../' + C.kit + '/' + C.film_config);
  /* `overrides` may only switch off things beside the board that the crop would otherwise cut through (RTT-001's era
     photo, RTT-002's car, the maker key, story cards, running-total panels); merged key by key, as
     kits/rtt-001/render_stills.js does. The approved film config is drawn too, and the board (frame number, every bar,
     label and picture) must be identical, or the render stops. */
  const cfg = merge(film, C.overrides);
  const data = JSON.parse(fs.readFileSync(path.resolve(rtt.KIT, cfg.race_file), 'utf8'));
  let same = null;
  if (C.overrides) {
    const R = await drawTo(C, film, data); await R.br.close();
    same = R;
  }
  const D = await drawTo(C, cfg, data);
  try {
    if (same && (same.target !== D.target || boardOf(same.st) !== boardOf(D.st)))
      throw new Error(C.kit + ': the overrides change the board (frame ' + same.target + ' vs ' + D.target + ')');
    const missing = [...D.st.logos.filter(p => !p.drawn), ...D.st.pics.filter(p => p.placeholder || (p.drawn == null && !p.own))];
    const file = path.join(out, C.kit + '_board_3840x2160.png');
    await (await D.pg.$('#c')).screenshot({ path: file });
    return { file, frame: D.target, k: D.k, st: D.st, total: D.total, missing, cfg, overrides_checked: !!same };
  } finally { await D.br.close(); }
}

/* ---------- layout ---------- */
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
function dataUrl(f) {
  const ext = path.extname(f).slice(1).toLowerCase();
  const type = { svg: 'image/svg+xml', png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif', webp: 'image/webp' }[ext];
  if (!type) throw new Error('unknown picture type ' + f);
  return `data:${type};base64,${fs.readFileSync(f).toString('base64')}`;
}

const THEMES = {
  white:  { bg: '#FFFFFF', ink: '#0B1424', years: '#E0301E', tile: '#FFFFFF', tileEdge: '#D9DEE7', shadow: '0 6px 22px rgba(11,20,36,.28)', mark: '#0B1424' },
  bright: { bg: '#FFD21F', ink: '#0B1424', years: '#C8102E', tile: '#FFFFFF', tileEdge: 'rgba(11,20,36,.18)', shadow: '0 6px 22px rgba(11,20,36,.35)', mark: '#0B1424' },
  dark:   { bg: '#0b1424', ink: '#0B1424', years: '#C8102E', tile: '#FFFFFF', tileEdge: 'rgba(11,20,36,.18)', panel: '#FFD21F', shadow: 'none', mark: '#F4F6FA' }
};

function html(C, opt, boardPng, assets, fontDir, filmCfg) {
  const T = Object.assign({}, THEMES[opt.background], opt.colours || {});
  const L = Object.assign({ board_w: 790, board_x: 18, words_x: 826, words_right: 18, words_top: 100 }, C.layout || {}, opt.layout || {});
  const cr = C.crop, dark = opt.background === 'dark', words = opt.words || C.words, sizes = opt.word_sizes || C.word_sizes || [];
  const wordsHtml = words.map((w, i) => `<div class="w" style="font-size:${sizes[i] || 120}px">${esc(w)}</div>`).join('');
  /* pictures: each the film's own file, drawn whole (never redrawn or recoloured), or with the crop the film itself
     uses for it (pictures.crop, e.g. RTT-001's IE6 'e' without its wordmark, DEC-199); on a light tile, or plain for a
     cut-out photo. rows: [{top, tile_w, tile_h, gap, plain, items: [{file, crop_id}]}] */
  const filmCrop = id => id && filmCfg.pictures && filmCfg.pictures.crop && filmCfg.pictures.crop[id];
  const rowsHtml = (C.rows || []).map(R => {
    const tw = R.tile_w || 100, th = R.tile_h || tw, pad = R.plain ? 0 : (R.pad != null ? R.pad : 12);
    const items = R.items.map(it => { const cp = filmCrop(it.crop_id);
      return `<div class="t${R.plain ? ' plain' : ''}" style="width:${tw}px;height:${th}px"><img src="${dataUrl(path.join(assets, it.file))}" alt="" ` +
             `style="max-width:${tw - 2 * pad}px;max-height:${th - 2 * pad}px" data-box="${tw - 2 * pad},${th - 2 * pad}"${cp ? ` data-crop='${JSON.stringify(cp)}'` : ''}></div>`; }).join('');
    return `<div class="row" style="top:${R.top}px;gap:${R.gap != null ? R.gap : 14}px">${items}</div>`;
  }).join('');
  const markImg = dataUrl(path.join(assets, 'rtt_logo.png'));
  const fonts = [700, 800, 900].map(w => `@font-face{font-family:Archivo;font-weight:${w};src:url("file://${fontDir}/archivo-latin-${w}-normal.woff2") format("woff2")}`).join('');
  /* the board: the film frame cropped (never edited), on the left. White/bright: a card on the background. Dark: no
     card - the film's own navy ground runs the full width - and the words sit on a bright panel on the right. */
  const bw = L.board_w, bh = Math.round(bw * cr.h / cr.w);
  const bx = L.board_x, by = L.board_y != null ? L.board_y : Math.round((H - bh) / 2);
  const panel = dark ? `<div class="panel" style="left:${L.words_x - 14}px"></div>` : '';
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fonts}
  html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:${T.bg};font-family:Archivo}
  .board{position:absolute;left:${bx}px;top:${by}px;width:${bw}px;height:${bh}px;overflow:hidden;border-radius:${dark ? 0 : 14}px;box-shadow:${T.shadow};background:#0b1424}
  .board img{position:absolute;left:${-cr.x * bw / cr.w}px;top:${-cr.y * bh / cr.h}px;width:${1920 * bw / cr.w}px;height:${1080 * bh / cr.h}px}
  .panel{position:absolute;top:0;right:0;bottom:0;background:${T.panel};box-shadow:-10px 0 30px rgba(0,0,0,.35)}
  .words{position:absolute;left:${L.words_x}px;right:${L.words_right}px;top:${L.words_top}px;color:${T.ink};text-align:center}
  .w{font-weight:900;line-height:.93;letter-spacing:-.01em;white-space:nowrap}
  .y{font-weight:800;color:${T.years};font-size:${C.years_size || 66}px;margin-top:14px;letter-spacing:.01em}
  .row{position:absolute;left:${L.words_x}px;right:${L.words_right}px;display:flex;justify-content:center;flex-wrap:wrap}
  .t{background:${T.tile};border-radius:18px;box-shadow:0 0 0 2px ${T.tileEdge}, 0 4px 14px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center;overflow:hidden}
  .t.plain{background:none;box-shadow:none;border-radius:0;overflow:visible}
  .mark{position:absolute;${L.mark_pos || 'right:20px;top:14px'};display:flex;align-items:center;gap:8px;color:${dark ? T.ink : T.mark};font-weight:800;font-size:19px;letter-spacing:.06em}
  .mark img{width:38px;height:38px}
  </style></head><body>
  <div class="board"><img src="file://${boardPng}"></div>${panel}
  <div class="words">${wordsHtml}<div class="y">${esc(C.years)}</div></div>
  ${rowsHtml}
  <div class="mark"><img src="${markImg}">RACE THROUGH TIME</div>
  <script>
  window.layoutDone = (async () => {
    await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode()));
    /* each word as large as asked, shrunk only as far as needed to fit the column */
    const col = document.querySelector('.words').clientWidth;
    for (const w of document.querySelectorAll('.w')) { let f = parseFloat(w.style.fontSize);
      w.style.display = 'inline-block'; while (w.offsetWidth > col && f > 20) { f -= 1; w.style.fontSize = f + 'px'; } w.style.display = 'block'; }
    /* the film's crop of a picture: only that region of the file, scaled to the tile */
    for (const im of document.querySelectorAll('img[data-crop]')) { const c = JSON.parse(im.dataset.crop), [bw, bh] = im.dataset.box.split(',').map(Number);
      const k = Math.min(bw / c.w, bh / c.h), d = document.createElement('div');
      d.style.cssText = 'position:relative;overflow:hidden;width:' + c.w * k + 'px;height:' + c.h * k + 'px';
      im.style.cssText = 'position:absolute;max-width:none;max-height:none;left:' + (-c.x * k) + 'px;top:' + (-c.y * k) + 'px;width:' + im.naturalWidth * k + 'px;height:' + im.naturalHeight * k + 'px';
      im.replaceWith(d); d.appendChild(im); }
    /* small pictures (e.g. 64 px GIF icons) fill their box rather than staying at their natural size */
    for (const im of document.querySelectorAll('.t > img')) { const [bw, bh] = im.dataset.box.split(',').map(Number);
      const k = Math.min(bw / im.naturalWidth, bh / im.naturalHeight); im.style.width = im.naturalWidth * k + 'px'; im.style.height = im.naturalHeight * k + 'px'; }
    /* the words and pictures as one block, centred top to bottom (rows' "top" sets only the spacing) */
    const blk = [document.querySelector('.words'), ...document.querySelectorAll('.row')];
    const t0 = Math.min(...blk.map(e => e.getBoundingClientRect().top)), t1 = Math.max(...blk.map(e => e.getBoundingClientRect().bottom));
    const dy = Math.round((${H} + ${L.centre_offset != null ? L.centre_offset : 20} - (t1 - t0)) / 2 - t0);
    for (const e of blk) e.style.top = (parseFloat(getComputedStyle(e).top) + dy) + 'px';
    const words = document.querySelector('.words').getBoundingClientRect(), rows = [...document.querySelectorAll('.row')].map(r => r.getBoundingClientRect());
    return { words_bottom: words.bottom, rows: rows.map(r => [r.top, r.bottom]) };
  })();
  </script>
  </body></html>`;
}

async function main() {
  const out = path.resolve(process.argv[2] || '');
  if (!process.argv[2] || out.startsWith(ROOT + path.sep)) { console.error('usage: node kits/thumbnails/render_thumbnails.js OUT_DIR (outside the repo) [rtt-### ...]'); process.exit(2); }
  if (!process.env.RTT_ASSETS_ROOT) { console.error('RTT_ASSETS_ROOT is not set'); process.exit(2); }
  fs.mkdirSync(out, { recursive: true });
  const only = process.argv.slice(3);
  const configs = fs.readdirSync(__dirname).filter(f => /^rtt-\d{3}\.json$/.test(f)).map(f => f.replace('.json', ''))
    .filter(e => !only.length || only.includes(e));
  const fontDir = path.join(path.dirname(require.resolve('@fontsource/archivo/package.json', { paths: [rtt.KIT] })), 'files');
  const { chromium } = require(require.resolve('playwright', { paths: [rtt.KIT] }));
  const files = [];
  let failed = false;
  for (const e of configs) {
    const C = JSON.parse(fs.readFileSync(path.join(__dirname, e + '.json'), 'utf8'));
    const assets = path.join(path.resolve(process.env.RTT_ASSETS_ROOT), C.kit);
    for (const R of C.rows || []) for (const r of R.items) if (!fs.existsSync(path.join(assets, r.file))) throw new Error(e + ': picture ' + r.file + ' not found');
    const B = await board(C, out);
    const res = check(C, C.at, B.st);
    const rec = { episode: C.episode, film_config: 'kits/' + C.kit + '/' + C.film_config, period: C.at, frame: B.frame, film_frames: B.total,
                  crop: C.crop, overrides: C.overrides || null, board_same_as_film_config: B.overrides_checked ? true : 'no overrides', bars: res.rows, errors: res.errs, pictures_not_found: B.missing.map(p => p.id) };
    fs.writeFileSync(path.join(out, e + '_check.json'), JSON.stringify(rec, null, 1));
    files.push(path.join(out, e + '_check.json'));
    console.log(`${C.episode}: ${C.at}, frame ${B.frame} of ${B.total}; ${res.rows.length} bars on the crop; ` +
                (res.errs.length ? 'CHECK FAILED:\n  ' + res.errs.join('\n  ') : 'every bar = the data file (figure, label, order, one scale)'));
    if (res.errs.length || B.missing.length) { if (B.missing.length) console.log('  pictures not found: ' + B.missing.map(p => p.id).join(', ')); failed = true; continue; }
    const br = await chromium.launch({ executablePath: CHROME });
    try {
      const pg = await br.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
      for (const opt of C.options) {
        const stem = `${C.kit}_thumb_${opt.name}`;
        const page = path.join(out, '_' + stem + '.html');
        fs.writeFileSync(page, html(C, opt, B.file, assets, fontDir, B.cfg));
        await pg.goto('file://' + page);
        const lay = await pg.evaluate(() => window.layoutDone);
        if (lay.rows.length && lay.rows[0][0] < lay.words_bottom + 8) throw new Error(stem + ': the pictures overlap the words (words end at ' + Math.round(lay.words_bottom) + ' px)');
        if (lay.rows.some(r => r[1] > H - 8)) throw new Error(stem + ': a row of pictures runs off the bottom');
        if (!(await pg.evaluate(() => document.fonts.check('900 100px Archivo')))) throw new Error('Archivo 900 did not load');
        fs.unlinkSync(page);
        const png = path.join(out, stem + '_1280x720.png'), jpg = path.join(out, stem + '_1280x720.jpg');
        await pg.screenshot({ path: png });
        await pg.screenshot({ path: jpg, type: 'jpeg', quality: 92 });
        if (fs.statSync(jpg).size >= JPG_MAX) throw new Error(jpg + ' is not under 2 MB');
        files.push(png, jpg);
        const sp = await br.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
        for (const [w, h, tag] of SIZES) {
          await sp.setViewportSize({ width: w, height: h });
          await sp.setContent(`<body style="margin:0"><img src="${dataUrl(png)}" style="width:${w}px;height:${h}px;display:block"></body>`);
          await sp.evaluate(() => document.images[0].decode());
          const f = path.join(out, `${stem}_${w}x${h}_${tag}.png`);
          await sp.screenshot({ path: f }); files.push(f);
        }
        await sp.close();
      }
    } finally { await br.close(); }
    if (!process.env.THUMB_KEEP_BOARD) fs.unlinkSync(B.file);       // the full film frame is not a deliverable
  }
  for (const f of files) console.log(crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex') + '  ' + path.basename(f));
  if (failed) { console.error('::error::a thumbnail check failed (see above); nothing was drawn for that episode'); process.exit(2); }
}
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
module.exports = { csv, parseLabel, check, dataAt };
