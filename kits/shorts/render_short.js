/* Race Through Time Shorts pilot (IQ-27; owner decision 3 Nov 2026: 2-3 vertical Shorts cut from each film, each
 * pointing to the full video). A PROPOSAL for Luke (DEC-069): nothing here is approved or uploaded.
 *
 *   RTT_ASSETS_ROOT=<dir> node kits/shorts/render_short.js OUT_DIR [short id ...]      (ids from kits/shorts/shorts.json)
 *
 * A Short is 1080 x 1920, 30 fps, 30-50 s, built from the film's OWN data and player, re-laid out for vertical (not a
 * crop of the 16:9 film frame): the episode's approved film config plus a Short config (kits/rtt-###/config_*_short_N.json:
 * window, 8 rows, a narrow board, no title/footer/logo/side panels in the player) is drawn frame by frame at raster 2;
 * the left 972 x 1080 of that frame (the narrow board laid out for it) is scaled to 1080 x 1200 and placed in the
 * vertical frame. Around it, the Short's own bands (one HTML layout, Archivo, the thumbnail template's words and red years):
 *   - 0-2 s: the hook line, large ("WHO HAS THE MOST F1 WINS?");
 *   - from 2 s: the subject in big words, the years, and the measure line;
 *   - the last 3 s (so the last frame has it): "Full race on the channel" under the board;
 *   - always: the RTT badge and name top left; the data credit small under the board.
 * Music: the film's own approved Audio Library track (private repo, SHA-256 checked by the workflow), played from a
 * strong beat (`music.start`), faded out over the last 3 s and mixed by scripts/rtt_mix_music.sh (the films' own mix:
 * -16 LUFS integrated, true peak at most -1 dBTP).
 * Checks (any failure stops): the duration is 30-50 s; on the last landing frame every bar's figure equals the episode's
 * data file; names and values are at least 5.9 pt on a phone showing the Short 390 pt wide (DEC-108's floor).
 * Output: <id>.mp4 (with music), <id>_still_last.png (the last frame), <id>_still_hook.png (frame 15), <id>_check.json.
 * OUT_DIR must be outside the repo; the workflow saves it only as a private pre-release (DEC-006, DEC-060).
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const { spawn, execFileSync } = require('child_process');
const rtt = require('../rtt-002/rtt.js');
const T = require('../thumbnails/render_thumbnails.js');
const ROOT = path.resolve(__dirname, '..', '..');
const VW = 1080, VH = 1920, REGION_W = 972, BOARD_Y = 250, BOARD_H = 1200, RASTER = 2, HOOK_SEC = 2, END_SEC = 3, PHONE_PT = 390, FLOOR = 5.9;
const SCALE = BOARD_H / 1080;              // player units -> Short pixels (1.111)
const INK = '#F4F6FA', RED = '#FF4B3A', NAVY = '#0b1424';

function bands(S, assets, fontDir) {
  const fonts = [500, 700, 800, 900].map(w => `@font-face{font-family:Archivo;font-weight:${w};src:url("file://${fontDir}/archivo-latin-${w}-normal.woff2") format("woff2")}`).join('');
  const mark = T.dataUrl(path.join(assets, 'rtt_logo.png'));
  const css = `${fonts} html,body{margin:0;width:${VW}px;height:${VH}px;overflow:hidden;background:transparent;font-family:Archivo;color:${INK}}
    .top{position:absolute;left:40px;right:40px;top:100px;height:${BOARD_Y - 96 - 8}px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
    .w{font-weight:900;line-height:.95;white-space:nowrap}
    .y{font-weight:800;color:${RED};font-size:0.46em;margin-left:18px;white-space:nowrap}
    .m{font-weight:500;font-size:27px;color:#AEB7C6;margin-top:6px}
    .hook{font-weight:900;line-height:1.0;font-size:84px;text-shadow:0 4px 18px rgba(0,0,0,.5)}
    .badge{position:absolute;left:36px;top:30px;display:flex;align-items:center;gap:12px;font-weight:800;font-size:26px;letter-spacing:.06em}
    .badge img{width:52px;height:52px}
    .credit{position:absolute;left:40px;right:40px;top:${BOARD_Y + BOARD_H + 8}px;font-weight:500;font-size:22px;line-height:1.3;color:#8C96A8}
    .end{position:absolute;left:0;right:0;top:${BOARD_Y + BOARD_H + 70}px;display:flex;justify-content:center}
    .end div{background:${RED};color:#fff;font-weight:900;font-size:50px;padding:14px 34px;border-radius:18px;box-shadow:0 6px 24px rgba(0,0,0,.45)}`;
  const fit = `<script>window.done=(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));
    /* each [data-fit] element shrinks (whole px) until it is no wider than its data-fit and no taller than its band */
    for(const e of document.querySelectorAll('[data-fit]')){let f=parseFloat(getComputedStyle(e).fontSize);const max=+e.dataset.fit, band=e.closest('.top');
      const tooBig=()=>e.scrollWidth>max||e.getBoundingClientRect().width>max||(band&&band.scrollHeight>band.clientHeight+1);
      while(tooBig()&&f>24){f-=1;e.style.fontSize=f+'px';}}
    return true;})();</script>`;
  const doc = body => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${body}${fit}</body></html>`;
  const words = S.words.join(' ');
  return {
    base: doc(`<div class="badge"><img src="${mark}">RACE THROUGH TIME</div><div class="credit">${T.esc(S.credit)}</div>`),
    title: doc(`<div class="top"><div data-fit="1000" style="display:inline-flex;align-items:baseline;justify-content:center;font-size:96px;white-space:nowrap"><span class="w">${T.esc(words)}</span><span class="y">${T.esc(S.years)}</span></div><div class="m">${T.esc(S.measure)}</div></div>`),
    hook: doc(`<div class="top"><div class="hook" data-fit="1000">${S.hook.map(T.esc).join('<br>')}</div></div>`),
    end: doc(`<div class="end"><div>${T.esc(S.end_line || 'Full race on the channel')}</div></div>`)
  };
}

async function renderOne(S, out, chromium, fontDir) {
  const assets = path.join(path.resolve(process.env.RTT_ASSETS_ROOT), S.kit);
  process.env.RTT_LOCAL_ASSETS = assets;
  const cfg = rtt.loadConfig('../' + S.kit + '/' + S.config);
  const data = JSON.parse(fs.readFileSync(path.resolve(rtt.KIT, cfg.race_file), 'utf8'));
  const tmp = fs.mkdtempSync(path.join(out, '_' + S.id + '_'));
  /* the bands, each a transparent 1080 x 1920 PNG */
  const br0 = await chromium.launch({ executablePath: T.CHROME });
  const B = bands(S, assets, fontDir), png = {};
  try {
    const pg = await br0.newPage({ viewport: { width: VW, height: VH } });
    for (const [k, h] of Object.entries(B)) {
      const f = path.join(tmp, k + '.html'); fs.writeFileSync(f, h); await pg.goto('file://' + f); await pg.evaluate(() => window.done);
      png[k] = path.join(tmp, k + '.png'); await pg.screenshot({ path: png[k], omitBackground: true });
    }
  } finally { await br0.close(); }

  /* the board frames */
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: RASTER, chrome: T.CHROME });
  const info = await pg.evaluate(() => ({ n: RACE_FRAMES, dates: TL.events.map(e => e.date), qe: TL.quarterEndFrame || null, start: TL.startFrame }));
  const frames = info.n + 1, D = frames / cfg.fps;
  if (D < 30 || D > 50) { await br.close(); throw new Error(`${S.id}: ${D.toFixed(2)} s, not 30-50 s`); }
  const lastK = info.dates.length - 1, lastLanding = info.qe ? info.qe[lastK] : info.start[lastK];
  await pg.evaluate(([rw, bw, bh, r]) => { const c2 = document.createElement('canvas'); c2.width = bw; c2.height = bh; window.__SHORT = { c2, x: c2.getContext('2d'), rw, r }; }, [REGION_W, VW, BOARD_H, RASTER]);
  const silent = path.join(tmp, 'video.mp4');
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'mjpeg', '-framerate', String(cfg.fps), '-i', 'pipe:0',
    '-loop', '1', '-i', png.base, '-loop', '1', '-i', png.title, '-loop', '1', '-i', png.hook, '-loop', '1', '-i', png.end,
    '-filter_complex', `color=c=${NAVY}:s=${VW}x${VH}:r=${cfg.fps}[bg];[bg][0:v]overlay=0:${BOARD_Y}:shortest=1[a];[a][1:v]overlay=0:0[b];` +
      `[b][3:v]overlay=0:0:enable='lt(t,${HOOK_SEC})'[c];[c][2:v]overlay=0:0:enable='gte(t,${HOOK_SEC})'[d];[d][4:v]overlay=0:0:enable='gte(t,${(D - END_SEC).toFixed(3)})',format=yuv420p[v]`,
    '-map', '[v]', '-frames:v', String(frames), '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-r', String(cfg.fps),
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart', silent], { stdio: ['pipe', 'inherit', 'inherit'] });
  const write = buf => new Promise((res, rej) => ff.stdin.write(buf, e => e ? rej(e) : res()));
  let minName = 1e9, minValue = 1e9, landing = null;
  for (let f = 0; f < frames; f++) {
    await rtt.drawFrame(pg, f, cfg);
    const r = await pg.evaluate(() => { const S = window.__SHORT, c = document.getElementById('c');
      S.x.imageSmoothingEnabled = true; S.x.imageSmoothingQuality = 'high';
      S.x.drawImage(c, 0, 0, S.rw * S.r, 1080 * S.r, 0, 0, S.c2.width, S.c2.height);
      const L = window.__LABELS.filter(l => l.alpha > 0.05 && l.x < S.rw);
      return { jpg: S.c2.toDataURL('image/jpeg', 0.96),
               name: Math.min(...L.filter(l => l.kind === 'name').map(l => l.size), 1e9), value: Math.min(...L.filter(l => l.kind === 'value').map(l => l.size), 1e9),
               over: L.filter(l => ['name', 'value', 'record'].includes(l.kind) && l.x + l.w > S.rw).map(l => l.text) }; });
    minName = Math.min(minName, r.name); minValue = Math.min(minValue, r.value);
    if (r.over.length) { ff.stdin.end(); await br.close(); throw new Error(`${S.id} frame ${f}: label runs past the board's right edge: ${r.over.join(', ')}`); }
    if (f === lastLanding) landing = await pg.evaluate(() => ({ bars: window.__BARS.filter(b => b.alpha > 0.05).map(b => ({ id: b.id, units: b.units, x: b.rect.x })) }));
    await write(Buffer.from(r.jpg.split(',')[1], 'base64'));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await br.close();

  /* checks: figures on the last landing frame; phone sizes */
  const errs = [];
  const base = JSON.parse(fs.readFileSync(path.join(ROOT, 'kits', 'thumbnails', S.kit + '.json'), 'utf8'));
  const dv = T.dataAt(base, info.dates[lastK], landing.bars);
  for (const b of landing.bars) { const d = dv[b.id]; if (!d) errs.push(`${b.id}: no data at ${info.dates[lastK]}`); else if (b.units !== d.value * (base.check.units_per_value || 1)) errs.push(`${b.id}: ${b.units} != data ${d.value}`); }
  const pt = px => px * RASTER * (VW / (REGION_W * RASTER)) * PHONE_PT / VW;
  if (pt(minName) < FLOOR || pt(minValue) < FLOOR) errs.push(`names ${pt(minName).toFixed(2)} pt / values ${pt(minValue).toFixed(2)} pt below ${FLOOR} pt`);

  /* music: the film's track from a strong beat, faded over the last END_SEC, mixed as the films are */
  const music = path.join(assets, S.music.file), trimmed = path.join(tmp, 'music.wav'), mp4 = path.join(out, S.id + '.mp4');
  execFileSync('ffmpeg', ['-nostdin', '-hide_banner', '-loglevel', 'error', '-y', '-ss', String(S.music.start), '-i', music, '-t', String(D + 1), '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s24le', trimmed]);
  const mixLog = execFileSync('bash', [path.join(ROOT, 'scripts', 'rtt_mix_music.sh'), silent, trimmed, mp4, String(END_SEC)], { encoding: 'utf8' });
  const stills = {};
  for (const [tag, t] of [['hook', 0.5], ['last', D - 1 / cfg.fps]]) {
    const f = path.join(out, `${S.id}_still_${tag}.png`); stills[tag] = f;
    execFileSync('ffmpeg', ['-nostdin', '-hide_banner', '-loglevel', 'error', '-y', '-ss', t.toFixed(3), '-i', silent, '-frames:v', '1', f]);
  }
  fs.rmSync(tmp, { recursive: true, force: true });
  const rec = { id: S.id, episode: S.episode, config: 'kits/' + S.kit + '/' + S.config, window: cfg.window, frames, seconds: +D.toFixed(3), size: `${VW}x${VH}`,
                last_period: info.dates[lastK], last_landing_frame: lastLanding, bars_checked: landing.bars.length,
                phone_pt: { names: +pt(minName).toFixed(2), values: +pt(minValue).toFixed(2), floor: FLOOR }, music: { title: S.music.title, from_sec: S.music.start, mix: mixLog.trim().split('\n').slice(-1)[0] }, errors: errs };
  fs.writeFileSync(path.join(out, S.id + '_check.json'), JSON.stringify(rec, null, 1));
  console.log(`${S.id}: ${D.toFixed(2)} s, ${frames} frames; last period ${rec.last_period}: ${landing.bars.length} bars = the data file; names ${rec.phone_pt.names} pt, values ${rec.phone_pt.values} pt on a 390 pt phone; ${rec.music.mix}` + (errs.length ? '\n  CHECK FAILED: ' + errs.join('; ') : ''));
  return { files: [mp4, stills.hook, stills.last, path.join(out, S.id + '_check.json')], ok: !errs.length };
}

async function main() {
  const out = path.resolve(process.argv[2] || '');
  if (!process.argv[2] || out.startsWith(ROOT + path.sep)) { console.error('usage: node kits/shorts/render_short.js OUT_DIR (outside the repo) [id ...]'); process.exit(2); }
  if (!process.env.RTT_ASSETS_ROOT) { console.error('RTT_ASSETS_ROOT is not set'); process.exit(2); }
  fs.mkdirSync(out, { recursive: true });
  const only = process.argv.slice(3), all = JSON.parse(fs.readFileSync(path.join(__dirname, 'shorts.json'), 'utf8')).shorts.filter(s => !only.length || only.includes(s.id));
  const fontDir = path.join(path.dirname(require.resolve('@fontsource/archivo/package.json', { paths: [rtt.KIT] })), 'files');
  const { chromium } = require(require.resolve('playwright', { paths: [rtt.KIT] }));
  const files = []; let ok = true;
  for (const S of all) { const r = await renderOne(S, out, chromium, fontDir); files.push(...r.files); ok = ok && r.ok; }
  for (const f of files) console.log(crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex') + '  ' + path.basename(f));
  if (!ok) { console.error('::error::a Short check failed'); process.exit(2); }
}
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
module.exports = { bands };
