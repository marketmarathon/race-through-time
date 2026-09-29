/* RTT-002 race starts extraction (29 Sep 2026). Run in a browser tab on en.wikipedia.org
 * (Luke's Chrome), because Wikimedia rate-limits the cloud sandboxes (HTTP 429).
 * Output: data/rtt-002/source/wikipedia_starts_extract.psv (saved by the browser, then verified by
 * SHA-256 against the hash computed here before use).
 *
 * 1. For each season, the World Drivers' Championship results table of the season article at the
 *    SAME revision used for the wins data (data/rtt-002/source/wikipedia_season_extract.psv):
 *    action=parse&oldid=<revision>&prop=text. The table is the largest wikitable whose header row
 *    has a "Driver" cell and a "Pts"/"Points" cell and no "Constructor" cell. Cells are laid out on
 *    a grid (rowspan/colspan expanded). Round columns are the header cells between Driver and Pts.
 *    For every driver row: the driver link (first link in the Driver cell outside the flag icon)
 *    and, per round, the cell text with <sup> elements (footnotes, sprint positions) removed.
 *    Nothing is classified here; the build script decides what counts as a start.
 * 2. "List of Formula One drivers" (current revision, recorded): driver link, race entries,
 *    race starts, race wins, from the table whose header has "Race entries" and "Race starts".
 * 3. Every driver link title resolved with action=query&redirects=1 to canonical title + page ID
 *    (drivers.csv driver_id = "wp<pageid>").
 */
async function extractStarts(REVS) {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const clean = el => { const c = el.cloneNode(true); c.querySelectorAll('sup, style, .reference').forEach(s => s.remove());
    return c.textContent.replace(/\s+/g, ' ').replace(/\|/g, '/').trim(); };
  const grid = tbl => { const G = []; [...tbl.rows].forEach((tr, r) => { G[r] = G[r] || []; let c = 0;
    for (const cell of tr.cells) { while (G[r][c]) c++; const rs = Math.max(1, +cell.rowSpan || 1), cs = Math.max(1, +cell.colSpan || 1);
      for (let i = 0; i < rs; i++) { G[r + i] = G[r + i] || []; for (let j = 0; j < cs; j++) G[r + i][c + j] = cell; } c += cs; } }); return G; };
  const linkOf = cell => { const a = [...cell.querySelectorAll('a[href^="/wiki/"]')].filter(a => !a.closest('.flagicon') && !a.closest('sup') && !/^\/wiki\/(File|Image):/.test(a.getAttribute('href')))[0];
    return a ? decodeURIComponent(a.getAttribute('href').slice(6).split('#')[0]).replace(/_/g, ' ') : null; };
  const out = [`#rtt002_starts_extract|script extract_starts.browser.js|created ${new Date().toISOString()}`];
  const titles = new Set(); const problems = [];
  for (const [season, rev] of REVS) {
    const j = await (await fetch(`/w/api.php?action=parse&oldid=${rev}&prop=text&format=json&formatversion=2`)).json();
    const retrieved = new Date().toISOString();
    const d = new DOMParser().parseFromString(j.parse.text, 'text/html');
    let best = null;
    for (const t of d.querySelectorAll('table.wikitable')) {
      const G = grid(t);
      const hr = G.findIndex(row => row && row.some(c => c && c.tagName === 'TH' && /^Driver$/i.test(clean(c))));
      if (hr < 0) continue;
      const H = G[hr].map(c => c ? clean(c) : '');
      if (H.some(h => /^Constructor/i.test(h))) continue;
      const di = H.findIndex(h => /^Driver$/i.test(h)); const pi = H.findIndex((h, i) => i > di && /^(Pts\.?|Points)$/i.test(h));
      if (di < 0 || pi < 0) continue;
      if (!best || t.rows.length > best.t.rows.length) best = { t, G, hr, H, di, pi };
    }
    if (!best) { problems.push(`${season}: no WDC table`); out.push(`#season|${season}|${j.parse.title}|${rev}|${retrieved}|NOT FOUND`); continue; }
    const { G, hr, H, di, pi } = best;
    // header cells between Driver and Pts; a colspan header repeats, so keep grid positions
    const cols = []; for (let c = di + 1; c < pi; c++) cols.push(c);
    out.push(`#season|${season}|${j.parse.title}|${rev}|${retrieved}|${cols.map(c => H[c]).join(';')}`);
    for (let r = hr + 1; r < G.length; r++) {
      const row = G[r]; if (!row || !row[di]) continue;
      if (row[di].tagName === 'TH' && /^Driver$/i.test(clean(row[di]))) continue;
      const lt = linkOf(row[di]); if (!lt) continue;
      titles.add(lt);
      out.push(['S', season, lt, ...cols.map(c => row[c] ? clean(row[c]) : '')].join('|'));
    }
    await sleep(250);
  }
  // List of Formula One drivers
  const L = await (await fetch('/w/api.php?action=parse&page=List_of_Formula_One_drivers&prop=text|revid&format=json&formatversion=2')).json();
  const ld = new DOMParser().parseFromString(L.parse.text, 'text/html');
  out.push(`#list_of_f1_drivers|${L.parse.title}|${L.parse.revid}|${new Date().toISOString()}`);
  for (const t of ld.querySelectorAll('table.wikitable')) {
    const G = grid(t); const H = (G[0] || []).map(c => c ? clean(c) : '');
    const ie = H.findIndex(h => /^Race entries/i.test(h)), is = H.findIndex(h => /^Race starts/i.test(h)), iw = H.findIndex(h => /^Race wins/i.test(h));
    if (ie < 0 || is < 0) continue;
    for (let r = 1; r < G.length; r++) { const row = G[r]; if (!row || !row[0]) continue; const lt = linkOf(row[0]); if (!lt) continue; titles.add(lt);
      out.push(['L', lt, clean(row[ie]), clean(row[is]), iw >= 0 ? clean(row[iw]) : ''].join('|')); }
  }
  // resolve every link title to canonical title + page ID
  out.push('#titles|link_title|canonical_title|pageid');
  const T = [...titles].sort();
  for (let i = 0; i < T.length; i += 50) {
    const b = T.slice(i, i + 50);
    const j = await (await fetch('/w/api.php?action=query&format=json&formatversion=2&redirects=1&titles=' + encodeURIComponent(b.join('|')))).json();
    const norm = {}; (j.query.normalized || []).forEach(n => norm[n.from] = n.to);
    const red = {}; (j.query.redirects || []).forEach(n => red[n.from] = n.to);
    const pg = {}; j.query.pages.forEach(p => pg[p.title] = p);
    for (const t of b) { let c = norm[t] || t; c = red[c] || c; const p = pg[c]; out.push(['T', t, c, p && !p.missing ? p.pageid : 'NOT FOUND'].join('|')); }
    await sleep(300);
  }
  return { text: out.join('\n') + '\n', problems };
}
