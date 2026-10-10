/* Shared-player regression check (IQ-18). Draws the same frames of other episodes' configs with two copies of the
 * player - a reference checkout (e.g. a git worktree of the commit before a change) and this checkout - and compares
 * the PNGs byte for byte. Use it whenever kits/rtt-002/player_rtt.html, rtt_timeline.js or rtt.js changes: the approved
 * episodes must draw exactly as before (CLAUDE.md "Building and rendering").
 *
 *   node tests/player/compare_frames.js <reference repo root> [frames per config]
 *
 * Configs: RTT-002's film and pilot, RTT-003's film, RTT-001's approved film configs, RTT-103's film (IQ-19), RTT-102's approved film (IQ-21). Each config's frames are spread
 * evenly over the whole film (default 8, plus the first and last). Private pictures are absent on both sides (each
 * player reports them "not found" and draws its fallback), so the comparison covers every drawn element the same way.
 * Prints one line per config and exits 1 on any difference.
 */
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..', '..');
const REF = path.resolve(process.argv[2] || '');
const N = +(process.argv[3] || 8);
const CHROME = process.env.PW_CHROME || '/opt/pw-browsers/chromium';
const CONFIGS = ['../rtt-002/config_rtt002_film.json', '../rtt-002/config_pilot_2014_2021_top20.json', '../rtt-003/config_rtt003_film.json',
                 '../rtt-001/config_rtt001_approved_fit.json', '../rtt-001/config_rtt001_photos.json', '../rtt-103/config_rtt103_film.json',
                 '../rtt-102/config_rtt102_film.json'];   // IQ-21: RTT-102's approved film too

async function frames(root, cfgFile, picks) {
  const kit = path.join(root, 'kits', 'rtt-002');
  const rtt = require(path.join(kit, 'rtt.js'));
  const prev = process.cwd(); process.chdir(kit);
  try {
    const cfg = rtt.loadConfig(cfgFile);
    const data = JSON.parse(fs.readFileSync(path.resolve(kit, cfg.race_file), 'utf8'));
    const { total } = rtt.frameTotals(cfg, data);
    const want = picks || [...new Set([0, ...Array.from({ length: N }, (_, i) => Math.round((i + 1) * (total - 1) / (N + 1))), total - 1])];
    const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: CHROME });
    const out = {}; let f = 0;
    for (const t of want) { for (; f <= t; f++) await rtt.drawFrame(pg, f, cfg);
      out[t] = crypto.createHash('sha256').update(await (await pg.$('#c')).screenshot()).digest('hex'); }
    await br.close();
    return { want, out, total };
  } finally { process.chdir(prev); for (const k of Object.keys(require.cache)) if (k.startsWith(kit)) delete require.cache[k]; }
}

(async () => {
  if (!fs.existsSync(path.join(REF, 'kits', 'rtt-002', 'player_rtt.html'))) { console.error('usage: node tests/player/compare_frames.js <reference repo root>'); process.exit(2); }
  let ok = true, n = 0;
  for (const c of CONFIGS) {
    const a = await frames(REF, c), b = await frames(ROOT, c, a.want);
    const diff = a.want.filter(t => a.out[t] !== b.out[t]); n += a.want.length;
    ok = ok && !diff.length && a.total === b.total;
    console.log(`${diff.length || a.total !== b.total ? 'DIFF' : 'SAME'} ${c}: ${a.want.length} frames of ${a.total}${a.total !== b.total ? ' (frame count ' + a.total + ' -> ' + b.total + ')' : ''}${diff.length ? ' differ at ' + diff.join(',') : ' pixel-identical'}`);
  }
  console.log(ok ? `ALL SAME (${n} frames)` : 'DIFFERENCES');
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
