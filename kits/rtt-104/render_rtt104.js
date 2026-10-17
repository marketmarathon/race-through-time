/* Race Through Time - RTT-104 renderer entry point (IQ-22, design round 1).
 *
 * The same environment contract as kits/rtt-002/rtt.js (FRAME_COUNT_ONLY, SEG_START, SEG_END, SEG_OUT, RASTER_W,
 * REF_PNG_DIR, RTT_CONFIG, PW_CHROME, RTT_LOCAL_ASSETS), and it opens the page through the shared driver's
 * openPlayer(): Archivo from @fontsource (proven, never substituted), flags from flag-icons (MIT), Luke's logo from
 * the private assets. Only the page differs: kits/rtt-104/player_rtt104.html (the split race). Nothing in
 * kits/rtt-002 is changed. Run from anywhere: node kits/rtt-104/render_rtt104.js (RTT_CONFIG relative to kits/rtt-104).
 */
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const rtt = require('../rtt-002/rtt.js');
const HERE = __dirname;

function config(file) {       // rtt.loadConfig resolves against kits/rtt-002, so name the file from there
  return rtt.loadConfig(path.relative(rtt.KIT, path.resolve(HERE, file || 'config_rtt104_base.json')));
}
async function open(cfg, raster = 1) {
  const data = JSON.parse(fs.readFileSync(path.resolve(rtt.KIT, cfg.race_file), 'utf8'));
  const o = await rtt.openPlayer({ cfg, data, raster, chrome: process.env.PW_CHROME || '/opt/pw-browsers/chromium' });
  return Object.assign(o, { data });
}
async function frame(pg, f) { return pg.evaluate(ff => window.drawAt(ff / 30), f); }

async function main() {
  const cfg = config(process.env.RTT_CONFIG);
  const R = +(process.env.RASTER_W || 1920) / 1920;
  if (!Number.isInteger(R) || R < 1) { console.error('RASTER_W must be a whole multiple of 1920'); process.exit(2); }
  const { br, pg } = await open(cfg, R);
  const TOTAL = await pg.evaluate(() => RACE_FRAMES);
  if (process.env.FRAME_COUNT_ONLY) { console.log('FRAMES ' + TOTAL); await br.close(); return; }
  const A = process.env.SEG_START ? +process.env.SEG_START : 0, B = process.env.SEG_END ? +process.env.SEG_END : TOTAL;
  const REFDIR = process.env.REF_PNG_DIR;
  if (REFDIR) {
    fs.mkdirSync(REFDIR, { recursive: true });
    const el = await pg.$('#c');
    for (let f = A; f < B; f++) { await frame(pg, f); await el.screenshot({ path: path.join(REFDIR, 'f' + String(f).padStart(5, '0') + '.png') }); }
    await br.close(); console.log(`wrote ${B - A} PNG(s) to ${REFDIR}`); return;
  }
  const OUT = process.env.SEG_OUT || 'rtt104.mp4';
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'mjpeg', '-framerate', '30', '-i', 'pipe:0',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', String(cfg.crf), '-preset', cfg.preset,
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-r', '30', '-movflags', '+faststart', OUT],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const write = buf => new Promise((res, rej) => ff.stdin.write(buf, e => e ? rej(e) : res()));
  for (let f = A; f < B; f++) {
    const u = await pg.evaluate(ff2 => { window.drawAt(ff2 / 30); return document.getElementById('c').toDataURL('image/jpeg', 0.97); }, f);
    await write(Buffer.from(u.split(',')[1], 'base64'));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await br.close();
  console.log(`wrote ${OUT}: frames ${A} to ${B - 1} of ${TOTAL} at ${1920 * R}x${1080 * R}`);
}
module.exports = { config, open, frame, HERE };
if (require.main === module) main().catch(e => { console.error('::error::' + e.message); process.exit(2); });
