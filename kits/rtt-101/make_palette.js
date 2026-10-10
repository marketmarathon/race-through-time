/* RTT-101 colours (IQ-21, design round 1, item e). Two options for Luke, both one colour per club for the whole film:
 *   kit       each club's own kit colour family (kit_colours.json: the main colour, plus a second colour), with the shade
 *             moved inside that family (lightness and chroma, hue within ±12°) where two clubs that share the board would
 *             otherwise be closer than CIEDE2000 18; a pair still closer gets the second club's second colour as an
 *             edge along its bar (player key bar_edge);
 *   distinct  a palette of clearly different colours (the RTT-002 family), each club taking the first colour at least
 *             CIEDE2000 18 from every club it shares the board with (DEC-023), the leaders first.
 * "Shares the board" = in the top N+1 (the fading row) that month, or in the top N the month before (a bar leaving), over the whole race.
 * Every difference is judged on the colour as drawn (rtt_timeline.js drawnColour: white type on every bar) and, for the
 * colour-blind check, after a protanopia and a deuteranopia simulation (Machado, Oliveira & Fernandes 2009, severity 1,
 * as tests/player/run_tests_rtt102.js).
 *
 *   node kits/rtt-101/make_palette.js [N=12]     -> kits/rtt-101/palettes.json and tests/player/COLOURS_RTT101.md
 */
const fs = require('fs'), path = require('path');
const T = require('../rtt-002/rtt_timeline.js');
const K = __dirname, ROOT = path.resolve(K, '..', '..');
const race = JSON.parse(fs.readFileSync(path.join(K, 'race_rtt101.json'), 'utf8'));
const KIT = JSON.parse(fs.readFileSync(path.join(K, 'kit_colours.json'), 'utf8')).clubs;
const MIN = 18, CB_MIN = +(process.env.CB_MIN || 0);
const MAT = { protan: [[0.152286,1.052583,-0.204868],[0.114503,0.786281,0.099216],[-0.003882,-0.048116,1.051998]],
              deutan: [[0.367322,0.860646,-0.227968],[0.280085,0.672501,0.047413],[-0.011820,0.042940,0.968881]] };
const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
const gam = c => { c = Math.min(1, Math.max(0, c)); return Math.round(255 * (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055)); };
const hex = v => '#' + v.map(x => Math.max(0, Math.min(255, Math.round(x))).toString(16).padStart(2, '0')).join('').toUpperCase();
const rgb = h => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const sim = (h, M) => { const v = rgb(T.drawnColour(h)).map(lin); return hex(M.map(r => gam(r[0] * v[0] + r[1] * v[1] + r[2] * v[2]))); };
const dE = (a, b) => T.deltaE(a, b);
const dCB = (a, b) => Math.min(...Object.values(MAT).map(M => T.deltaE(sim(a, M), sim(b, M))));

/* Lab <-> sRGB for the shade search */
function toLab(h) { const [r, g, b] = rgb(h).map(lin);
  const X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, Y = 0.2126 * r + 0.7152 * g + 0.0722 * b, Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883;
  const f = t => t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116; return [116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))]; }
function fromLab([L, a, b]) { const fy = (L + 16) / 116, fx = fy + a / 500, fz = fy - b / 200, inv = t => t ** 3 > 0.008856 ? t ** 3 : (t - 16 / 116) / 7.787;
  const X = inv(fx) * 0.95047, Y = inv(fy), Z = inv(fz) * 1.08883;
  const r = 3.2406 * X - 1.5372 * Y - 0.4986 * Z, g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z, bb = 0.0557 * X - 0.2040 * Y + 1.0570 * Z;
  if ([r, g, bb].some(c => c < -0.002 || c > 1.002)) return null; return hex([r, g, bb].map(gam)); }
function shades(h) {          // the kit colour first, then its family by closeness
  const [L, a, b] = toLab(h), C = Math.hypot(a, b), H = Math.atan2(b, a), out = [h];
  for (const dL of [0, -8, 8, -16, 16, -24, 24]) for (const kC of [1, 0.8, 1.15, 0.6]) for (const dH of [0, -6, 6, -12, 12]) {
    if (!dL && kC === 1 && !dH) continue;
    const c = C < 8 ? C : C * kC, hh = H + dH * Math.PI / 180, x = fromLab([Math.min(92, Math.max(22, L + dL)), c * Math.cos(hh), c * Math.sin(hh)]);
    if (x && !out.includes(x)) out.push(x); }
  return out;
}

const N = +(process.argv[2] || 12);
function coVisible(n) {
  const ev = race.events, adj = {}, firstTop = {};
  ev.forEach((e, k) => { const S = new Set(e.order.slice(0, n + 1)); if (k) ev[k - 1].order.slice(0, n).forEach(id => S.add(id));
    e.order.slice(0, n).forEach((id, i) => { if (!(id in firstTop)) firstTop[id] = k * 100 + i; });
    for (const a of S) { adj[a] = adj[a] || new Set(); for (const b of S) if (a !== b) adj[a].add(b); } });
  return { adj, firstTop };
}
function importance(n) {      // the leaders first: best rank ever, then months in the top n
  const best = {}, months = {};
  race.events.forEach(e => e.order.slice(0, n + 1).forEach((id, i) => { best[id] = Math.min(best[id] ?? 99, i); months[id] = (months[id] || 0) + 1; }));
  return Object.keys(best).sort((a, b) => best[a] - best[b] || months[b] - months[a] || (a < b ? -1 : 1));
}
/* the distinct palette: colours that carry white names as they are (not darkened by drawnColour) and stand out from the
   navy ground (L* >= 33, chroma >= 20), chosen farthest-first in CIEDE2000 from an sRGB grid (deterministic) */
function distinctPool(n) {
  const pool = [];
  for (let r = 0; r <= 255; r += 15) for (let g = 0; g <= 255; g += 15) for (let b = 0; b <= 255; b += 15) {
    const h = hex([r, g, b]); if (T.drawnColour(h).toUpperCase() !== h) continue;
    const [L, a, bb] = toLab(h), C = Math.hypot(a, bb); if (L < 33 || C < 20) continue; pool.push(h); }
  /* the distance used: CIEDE2000 as drawn, and the colour-blind distance scaled up by MIN / CB_MIN, so a palette colour is
     at least MIN from every other as drawn AND at least CB_MIN under both simulations */
  const sc = CB_MIN ? (a, b) => Math.min(dE(a, b), dCB(a, b) * MIN / CB_MIN) : dE;
  const out = ['#E6194B'.toUpperCase()];
  const dmin = pool.map(c => sc(c, out[0]));
  while (out.length < n) { let bi = 0; for (let i = 1; i < pool.length; i++) if (dmin[i] > dmin[bi]) bi = i;
    if (dmin[bi] < MIN) break;
    out.push(pool[bi]); for (let i = 0; i < pool.length; i++) dmin[i] = Math.min(dmin[i], sc(pool[i], pool[bi])); }
  return out;
}
const DISTINCT = distinctPool(40);
/* depth-first colouring (as rtt_timeline.js assignColours with a priority): clubs in importance order, each trying its
   candidates in preference order; a club with no candidate left sends the search back to the most recent choice */
function search(order, adj, candsOf) {
  const col = {}, steps = { n: 0 };
  const ok = (id, c) => [...(adj[id] || [])].every(m => !(m in col) || dE(c, col[m]) >= MIN);
  const dfs = v => { if (v === order.length) return true; if (++steps.n > 300000) return false;
    const id = order[v];
    for (const c of candsOf(id)) { if (!ok(id, c)) continue; col[id] = c; if (dfs(v + 1)) return true; delete col[id]; }
    return false; };
  return dfs(0) ? col : null;
}

function assign(kind, n) {
  const { adj } = coVisible(n), order = importance(n), edge = {};
  let pick = {};
  if (kind === 'distinct') {        /* first an exact search: DSATUR with backtracking (the club with the most differently
                                       coloured neighbours next, ties: most neighbours, then importance); greedy DSATUR if it gives up */
    const ids = order, nb = Object.fromEntries(ids.map(id => [id, [...(adj[id] || [])].filter(m => ids.includes(m))])), col = {};
    let steps = 0;
    const dfs = () => {
      if (++steps > 3e6) return null;
      let best = null, bs = -1, bd = -1;
      for (const id of ids) if (!(id in col)) { const sat = new Set(nb[id].filter(m => m in col).map(m => col[m])).size, d = nb[id].length;
        if (sat > bs || (sat === bs && d > bd)) { best = id; bs = sat; bd = d; } }
      if (best == null) return true;
      const used = new Set(nb[best].filter(m => m in col).map(m => col[m]));
      for (const c of DISTINCT) if (!used.has(c)) { col[best] = c; const r = dfs(); if (r) return r; if (r === null) return null; delete col[best]; }
      return false;
    };
    const r = dfs();
    if (r) { pick = col; console.error('distinct: exact search coloured every club (' + n + ' bars, ' + steps + ' steps)'); }
    else console.error('distinct: exact search ' + (r === null ? 'gave up' : 'proved ' + DISTINCT.length + ' colours too few'));
  }
  if (kind === 'distinct' && !Object.keys(pick).length) {      /* DSATUR: the club with the most differently coloured neighbours next (ties: importance);
                                     it takes the first palette colour none of its neighbours has. Every palette colour is at
                                     least MIN from every other, so a proper colouring clears the rule for every pair. */
    const rank = Object.fromEntries(order.map((id, i) => [id, i]));
    while (Object.keys(pick).length < order.length) {
      let best = null, bs = -1;
      for (const id of order) if (!(id in pick)) { const sat = new Set([...(adj[id] || [])].filter(m => m in pick).map(m => pick[m])).size;
        if (sat > bs || (sat === bs && rank[id] < rank[best])) { bs = sat; best = id; } }
      const used = new Set([...(adj[best] || [])].filter(m => m in pick).map(m => pick[m]));
      const c = DISTINCT.find(x => !used.has(x));
      if (!c) { const nbC = [...(adj[best] || [])].filter(m => m in pick).map(m => pick[m]), far = x => Math.min(99, ...nbC.map(y => dE(x, y)));
        console.error('distinct palette of ' + DISTINCT.length + ' colours is not enough for ' + best + ' on a board of ' + n + ': it takes the colour farthest from its neighbours');
        pick[best] = DISTINCT.slice().sort((x, y) => far(y) - far(x))[0]; continue; }
      pick[best] = c;
    }
  }
  if (!Object.keys(pick).length) for (const id of order) {
    const nb = [...(adj[id] || [])].filter(m => m in pick);
    const cands = kind === 'kit' ? shades(KIT[id].main) : DISTINCT;
    let best = null, bestScore = -1;
    for (const [i, c] of cands.entries()) {
      const m = nb.length ? Math.min(...nb.map(o => dE(c, pick[o]))) : 99;
      if (kind === 'distinct') { if (m >= MIN) { best = c; break; } if (m > bestScore) { bestScore = m; best = c; } continue; }
      if (m >= MIN) { best = c; break; }        // the closest shade to the kit colour that clears the rule
      if (m > bestScore + 0.5) { bestScore = m; best = c; }
    }
    pick[id] = best;
  }
  for (const e of race.entrants) if (!(e.id in pick)) pick[e.id] = kind === 'kit' ? KIT[e.id].main : DISTINCT[0];
  /* pairs still under the rule; the kit option gives the less important club of each its second colour as an edge */
  const fails = [];
  for (const a of order) for (const b of order) if (a < b && adj[a] && adj[a].has(b)) {
    const d = dE(pick[a], pick[b]), cb = dCB(pick[a], pick[b]);
    if (d < MIN) { fails.push({ a, b, d, cb }); if (kind === 'kit') { const lo = order.indexOf(a) > order.indexOf(b) ? a : b; if (KIT[lo].second) edge[lo] = KIT[lo].second; } }
  }
  let cbMin = 99, cbPair = '';
  for (const a of order) for (const b of order) if (a < b && adj[a] && adj[a].has(b)) { const c = dCB(pick[a], pick[b]); if (c < cbMin) { cbMin = c; cbPair = a + '/' + b; } }
  return { pick, edge, fails, cbMin, cbPair, order };
}

const out = { note: 'Generated by kits/rtt-101/make_palette.js from race_rtt101.json and kit_colours.json; one colour per club for the whole film (house style 4). maker_order is the clubs.csv order.', board: N, options: {} };
let pmin = 99; for (let i = 0; i < DISTINCT.length; i++) for (let j = i + 1; j < DISTINCT.length; j++) pmin = Math.min(pmin, dE(DISTINCT[i], DISTINCT[j]));
const md = ['# RTT-101 colours (IQ-21, design round 1, item e)', '', `Distinct palette: ${DISTINCT.length} colours, closest pair CIEDE2000 ${pmin.toFixed(1)}.`, '', `Board of ${N} (co-visible = in the top ${N + 1} that month, or the top ${N} the month before). Rule: CIEDE2000 >= ${MIN} as drawn (DEC-023). Colour-blind: protanopia and deuteranopia simulation (Machado et al. 2009), reported.`, ''];
const ids = race.entrants.map(e => e.id);
for (const kind of ['kit_raw', 'kit', 'distinct']) {
  let r;
  if (kind === 'kit_raw') { const { adj } = coVisible(N), order = importance(N), pick = Object.fromEntries(ids.map(id => [id, KIT[id].main])), fails = [];
    for (const a of order) for (const b of order) if (a < b && adj[a] && adj[a].has(b)) { const d = dE(pick[a], pick[b]); if (d < MIN) fails.push({ a, b, d, cb: dCB(pick[a], pick[b]) }); }
    r = { pick, edge: {}, fails, order }; }
  else r = assign(kind, N);
  out.options[kind] = { palette: ids.map(id => r.pick[id]), bar_edge: r.edge, fails: r.fails.map(f => [f.a, f.b, +f.d.toFixed(1), +f.cb.toFixed(1)]) };
  md.push(`## ${kind === 'kit_raw' ? 'Kit colours as they are' : kind === 'kit' ? 'Kit colours, closest pairs adjusted (second-colour edge where still close)' : 'Distinct palette'}`, '',
          `${r.fails.length} pair(s) that share the board are closer than CIEDE2000 ${MIN}${r.cbMin != null && r.cbMin < 99 ? `; colour-blind closest ${r.cbMin.toFixed(1)} (${r.cbPair})` : ''}.`, '');
  if (r.fails.length) { md.push('| Pair | CIEDE2000 as drawn | colour-blind (worse of protan/deutan) |', '|---|---|---|');
    for (const f of r.fails.sort((x, y) => x.d - y.d)) md.push(`| ${f.a} / ${f.b} | ${f.d.toFixed(1)} | ${f.cb.toFixed(1)} |`); md.push(''); }
  if (Object.keys(r.edge || {}).length) md.push('Second-colour edges: ' + Object.entries(r.edge).map(([k, v]) => `${k} ${v}`).join(', '), '');
}
out.maker_order = ids;
fs.writeFileSync(path.join(K, 'palettes.json'), JSON.stringify(out, null, 1) + '\n');
fs.writeFileSync(path.join(ROOT, 'tests', 'player', 'COLOURS_RTT101.md'), md.join('\n') + '\n');
console.log(md.join('\n'));
