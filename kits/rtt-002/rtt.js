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

  await pg.evaluate(o => window.setup(o), { data, cfg, raster });
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

module.exports = { loadConfig, frameTotals, openPlayer, drawFrame, KIT };
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
