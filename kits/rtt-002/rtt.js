/* Race Through Time - the RTT renderer entry point (IQ-04).
 *
 * COPIED from Market Marathon's formatc.js (Format C2-2 kit MarketMarathon_RaceKit_RF_US_C2_v3,
 * marketmarathon/bars @ 2a10877). It honours the SAME environment contract, so the C2-2
 * shard-and-join workflow shape can drive it unchanged:
 *
 *   FRAME_COUNT_ONLY=1   print "FRAMES <n>" and exit, for the plan job
 *   SEG_START, SEG_END   render frames [START, END) only
 *   SEG_OUT              write that slice to this mp4
 *   RASTER_W             3840 for a master, 1920 for a preview
 *   NOMUX=1              video only (this driver never muxes audio; accepted for the contract)
 *   REF_PNG_DIR          write each frame as a lossless PNG into this directory INSTEAD of
 *                        encoding a video, and skip ffmpeg entirely
 *
 * Additive, RTT only:
 *   RTT_CONFIG           config file to use (default config.json), so a quieter variant is a
 *                        second config, not a second player
 *   PW_CHROME            Chromium executable (as in formatc.js)
 *
 * What differs from formatc.js and why:
 *   - no photographs, logo, flag, sub-sector icons or short summaries are loaded (RTT has none;
 *     brief step 3c)
 *   - the race length is derived from the EVENT timeline (rtt_timeline.js), not from
 *     periods x seconds_per_year. FRAME_COUNT_ONLY computes it in Node from the same file the
 *     page uses, so the plan job and the renderer cannot disagree; the page's figure is still
 *     checked against it, as formatc.js checks race_sec.
 *   - IQ-05c: with "flags" {enabled: true, csv: <file>} the driver reads the nationality file
 *     (data/rtt-002/driver_nationality.csv: driver_id, flag_code) and hands the page each needed
 *     flag as an SVG from the npm package flag-icons (MIT, reference/rights_ledger.md). No flag
 *     file is copied into the repo. A code with no flag-icons file refuses to render; a driver
 *     whose flag_code is NOT FOUND / NOT AVAILABLE simply gets no flag (the name is always drawn).
 *   - Archivo is loaded from the npm package @fontsource/archivo (SIL OFL 1.1) instead of the
 *     TTFs in the Market Marathon kit, so no font file is copied into this public repo. The
 *     same measure-against-a-missing-family check refuses to render substituted type.
 */
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const TIMELINE = require('./rtt_timeline.js');

const KIT = __dirname;

/* A config may name a base config in "extends" (IQ-05): the pilot configs are config.json plus
   a window, a pace and no closing card. Objects merge key by key (so "pacing":
   {"sec_per_event": 0.35} changes only that key); arrays and plain values replace. */
function merge(base, over) {
  const out = Object.assign({}, base);
  for (const [k, v] of Object.entries(over))
    out[k] = v && typeof v === 'object' && !Array.isArray(v) && base[k] && typeof base[k] === 'object' && !Array.isArray(base[k]) ? merge(base[k], v) : v;
  return out;
}
function readConfig(file, seen = []) {
  const full = path.resolve(KIT, file);
  if (seen.includes(full)) throw new Error('config "extends" loops: ' + seen.concat(full).join(' -> '));
  const cfg = JSON.parse(fs.readFileSync(full, 'utf8'));
  if (!cfg.extends) return cfg;
  const base = readConfig(path.resolve(path.dirname(full), cfg.extends), seen.concat(full));
  const own = Object.assign({}, cfg); delete own.extends;
  return merge(base, own);
}
function loadConfig(file, overrides) {
  return Object.assign(readConfig(file || 'config.json'), overrides || {});
}

function frameTotals(cfg, data) {
  const tl = TIMELINE.build(data, cfg);
  const intro = Math.round(cfg.intro_sec * cfg.fps), outro = Math.round(cfg.outro_sec * cfg.fps);
  return { tl, intro, outro, total: intro + tl.raceFrames + outro };
}

/* IQ-05c: the nationality file -> {byId: {driver_id: code}, svg: {code: data URL}}. */
function readCsvRows(file) {
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/).filter(Boolean);
  const split = l => { const out = []; let f = '', q = false;
    for (let i = 0; i < l.length; i++) { const ch = l[i];
      if (q) { if (ch === '"') { if (l[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += ch; }
      else if (ch === '"') q = true; else if (ch === ',') { out.push(f); f = ''; } else f += ch; }
    out.push(f); return out; };
  const head = split(lines.shift());
  return lines.map(l => Object.fromEntries(split(l).map((v, i) => [head[i], v])));
}
function loadFlags(cfg) {
  const F = cfg.flags;
  if (!F || !F.enabled) return null;
  const file = path.resolve(KIT, F.csv);
  if (!fs.existsSync(file)) throw new Error('flags.enabled but ' + F.csv + ' does not exist (switch flags off until the nationality data is built)');
  const dir = path.join(path.dirname(require.resolve('flag-icons/package.json', { paths: [KIT] })), 'flags', '4x3');
  const byId = {}, svg = {};
  for (const r of readCsvRows(file)) {
    const code = r.flag_code;
    if (!/^[a-z]{2}(-[a-z]+)?$/.test(code || '')) continue;          // NOT FOUND / NOT AVAILABLE: no flag
    const f = path.join(dir, code + '.svg');
    if (!fs.existsSync(f)) throw new Error('flag-icons has no flag "' + code + '" (driver ' + r.driver_id + ')');
    byId[r.driver_id] = code;
    if (!svg[code]) svg[code] = 'data:image/svg+xml;base64,' + fs.readFileSync(f).toString('base64');
  }
  return { byId, svg };
}

/* IQ-05c overlays (DEC-035): Luke's logo and a generic car picture are private media and never
   committed (DEC-006). Each overlay names a file in the git-ignored local_assets/ folder (or
   cfg.local_assets / RTT_LOCAL_ASSETS); a missing file is reported and skipped, the render goes on. */
function loadOverlays(cfg) {
  const dir = path.resolve(KIT, process.env.RTT_LOCAL_ASSETS || cfg.local_assets || 'local_assets');
  const out = {};
  for (const b of cfg.overlays || []) {
    const f = path.join(dir, b.file);
    if (!fs.existsSync(f)) { console.log('overlay "' + b.name + '": ' + f + ' not found - box kept empty'); continue; }
    const ext = path.extname(f).slice(1).toLowerCase(), mime = ext === 'svg' ? 'image/svg+xml' : ext === 'jpg' ? 'image/jpeg' : 'image/' + ext;
    out[b.name] = 'data:' + mime + ';base64,' + fs.readFileSync(f).toString('base64');
  }
  return out;
}

/* IQ-10 (RTT-003): the console pictures and maker logos are private media (DEC-006, DEC-060), never
   committed. With "pictures" {enabled, dir} each console's icon is read from <assets>/<dir>/<id>.png and,
   with "maker_key" {enabled, logo_dir}, each maker's logo from <assets>/<logo_dir>/<key>.svg (assets =
   RTT_LOCAL_ASSETS or cfg.local_assets). A missing file is reported ("not found - none drawn") and the
   render goes on; the render workflow treats that message as a failure. Nothing happens for RTT-002. */
function dataUrl(f) {
  const ext = path.extname(f).slice(1).toLowerCase(), mime = ext === 'svg' ? 'image/svg+xml' : ext === 'jpg' ? 'image/jpeg' : 'image/' + ext;
  return 'data:' + mime + ';base64,' + fs.readFileSync(f).toString('base64');
}
function loadPictures(cfg, data) {
  const P = cfg.pictures;
  if (!P || !P.enabled) return null;
  const dir = path.join(path.resolve(KIT, process.env.RTT_LOCAL_ASSETS || cfg.local_assets || 'local_assets'), P.dir || 'icons');
  const out = {};
  for (const e of data.entrants) {
    const f = path.join(dir, e.id + '.png');
    if (!fs.existsSync(f)) { console.log('picture "' + e.id + '": ' + f + ' not found - none drawn'); continue; }
    out[e.id] = dataUrl(f);
  }
  return out;
}
function loadLogos(cfg) {
  const K = cfg.maker_key || {}, BL = cfg.bar_logos || {};
  if (!(K.enabled && K.logos) && !BL.enabled) return {};   // IQ-10 round 2: also for the logos on the bars
  const dir = path.join(path.resolve(KIT, process.env.RTT_LOCAL_ASSETS || cfg.local_assets || 'local_assets'), K.logo_dir || BL.dir || 'logos');
  const out = {};
  for (const m of cfg.maker_order || []) {
    const f = path.join(dir, m + '.svg');
    if (!fs.existsSync(f)) { console.log('logo "' + m + '": ' + f + ' not found - none drawn'); continue; }
    out[m] = dataUrl(f);
  }
  return out;
}

/* Open Chromium on the player, fonts loaded and proven, setup() done. Used by the CLI below
   and by the tests (tests/player/run_tests.js), so both draw through exactly the same path. */
async function openPlayer({ cfg, data, raster = 1, chrome }) {
  const { chromium } = require(require.resolve('playwright', { paths: [KIT] }));
  const br = await chromium.launch({ executablePath: chrome || process.env.PW_CHROME || undefined,
                                     args: ['--disable-lcd-text', '--allow-file-access-from-files', '--disable-background-networking', '--disable-component-update'] });
  const pg = await br.newPage({ viewport: { width: 1920 * raster, height: 1080 * raster } });
  pg.on('console', m => { if (m.type() === 'error') console.error('[player] ' + m.text()); else if (process.env.RTT_VERBOSE) console.log('[player] ' + m.text()); });
  pg.on('pageerror', e => console.error('[player] ' + e.message));
  await pg.goto('file://' + path.resolve(KIT, cfg.renderer_file || 'player_rtt.html'));

  const fam = (cfg.fonts && cfg.fonts.family) || 'Archivo';
  const pkg = path.dirname(require.resolve('@fontsource/archivo/package.json', { paths: [KIT] }));
  for (const w of ['400', '500', '600', '700'])
    await pg.addStyleTag({ url: 'file://' + path.join(pkg, w + '.css') });
  /* Chromium substitutes SILENTLY if a face is missing. document.fonts.check() is no use (it
     answers true for anything it has never heard of), so, as formatc.js does, measure a string
     in Archivo against a family that cannot exist. Accented names are in the sample, so the
     latin-ext faces are proven too. */
  const fontOK = await pg.evaluate(async fam => {
    const S = 'Kimi Räikkönen Pérez Rodríguez François Häkkinen 1234567890';
    await Promise.all(['400', '500', '600', '700'].map(w => document.fonts.load(w + ' 64px "' + fam + '"', S)));
    await document.fonts.ready;
    const c = document.createElement('canvas').getContext('2d');
    c.font = '700 64px "NoSuchFamily12345"'; const fallback = c.measureText(S).width;
    c.font = '700 64px "' + fam + '"';       const got = c.measureText(S).width;
    return Math.abs(got - fallback) > 0.5;
  }, fam);
  if (!fontOK) { await br.close(); throw new Error(fam + ' did not resolve - refusing to render substituted type'); }

  await pg.evaluate(o => window.setup(o), { data, cfg, raster, flags: loadFlags(cfg), overlays: loadOverlays(cfg),
                                          pictures: loadPictures(cfg, data), logos: loadLogos(cfg) });
  await pg.evaluate(() => window.__imagesReady);
  return { br, pg };
}

async function drawFrame(pg, f, cfg) {
  return pg.evaluate(([tt, intro]) => { tt < intro ? drawIntro(tt) : drawAt(tt - intro); }, [f / cfg.fps, cfg.intro_sec]);
}

async function main() {
  const cfg = loadConfig(process.env.RTT_CONFIG);
  const data = JSON.parse(fs.readFileSync(path.resolve(KIT, cfg.race_file), 'utf8'));
  const { tl, total: TOTAL } = frameTotals(cfg, data);
  const FPS = cfg.fps;

  if (process.env.FRAME_COUNT_ONLY) { console.log('FRAMES ' + TOTAL); process.exit(0); }

  const RW  = +(process.env.RASTER_W || 1920);
  const R   = RW / 1920;
  const A   = process.env.SEG_START ? +process.env.SEG_START : 0;
  const B   = process.env.SEG_END   ? +process.env.SEG_END   : TOTAL;
  const OUT = process.env.SEG_OUT   || cfg.out;
  if (!Number.isInteger(R) || R < 1) { console.error('RASTER_W must be a whole multiple of 1920'); process.exit(2); }

  const { br, pg } = await openPlayer({ cfg, data, raster: R });
  const raceFrames = await pg.evaluate(() => RACE_FRAMES);
  if (raceFrames !== tl.raceFrames) { console.error(`::error::Node timeline says ${tl.raceFrames} race frames, the page ${raceFrames}`); process.exit(2); }
  if (cfg.race_sec != null && Math.abs(cfg.race_sec - raceFrames / FPS) > 0.001) {
    console.error(`::error::config says race_sec ${cfg.race_sec} but the data gives ${raceFrames / FPS}`); process.exit(2);
  }
  await pg.waitForTimeout(300);

  /* The rank glide is stateful, so a shard that starts mid-race is wound up to its own first
     frame first (formatc.js: 140 frames, ten time constants at the 0.55 s glide). */
  const WARM = 140;
  for (let f = Math.max(0, A - WARM); f < A; f++) await drawFrame(pg, f, cfg);

  const REFDIR = process.env.REF_PNG_DIR;
  if (REFDIR) {
    fs.mkdirSync(REFDIR, { recursive: true });
    const el = await pg.$('#c');
    for (let f = A; f < B; f++) {
      await drawFrame(pg, f, cfg);
      await el.screenshot({ path: path.join(REFDIR, 'f' + String(f).padStart(5, '0') + '.png'), type: 'png' });
    }
    await br.close();
    console.log(`wrote ${B - A} reference PNG(s) to ${REFDIR} at ${1920 * R}x${1080 * R}`);
    return;
  }

  const args = ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'mjpeg', '-framerate', String(FPS), '-i', 'pipe:0',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', String(cfg.crf), '-preset', cfg.preset,
                '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                '-r', String(FPS), '-movflags', '+faststart', OUT];
  const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
  ff.on('error', e => { console.error('ffmpeg failed to start:', e.message); process.exit(2); });
  const write = buf => new Promise((res, rej) => ff.stdin.write(buf, e => e ? rej(e) : res()));

  const t0 = Date.now();
  for (let f = A; f < B; f++) {
    const u = await pg.evaluate(([tt, intro]) => {
      tt < intro ? drawIntro(tt) : drawAt(tt - intro);
      return document.getElementById('c').toDataURL('image/jpeg', 0.97);
    }, [f / FPS, cfg.intro_sec]);
    await write(Buffer.from(u.split(',')[1], 'base64'));
    if ((f - A) % 250 === 0) {
      const done = f - A + 1, el = (Date.now() - t0) / 1000;
      console.log(`frame ${f}/${B}  ${(done / el).toFixed(1)} fps  rss ${(process.memoryUsage().rss / 1e6).toFixed(0)} MB`);
    }
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await br.close();
  console.log(`wrote ${OUT}: frames ${A} to ${B - 1} of ${TOTAL} at ${1920 * R}x${1080 * R}`);
}

module.exports = { loadConfig, frameTotals, openPlayer, drawFrame, loadFlags, loadOverlays, loadPictures, loadLogos, KIT };
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
