/*
 * RTT-002 source extraction: Formula One World Championship race winners from
 * English Wikipedia season pages (CC BY-SA 4.0).
 *
 * HOW IT WAS RUN (28 Sep 2026): pasted into the developer console of a tab on
 * https://en.wikipedia.org (Luke's Chrome, driven by Claude). The cloud sandbox
 * was rate-limited by Wikimedia (HTTP 429), so the same-origin API was called
 * from the browser instead. The output text was transferred to the build
 * machine and verified byte-for-byte by SHA-256 before use:
 *   data/rtt-002/source/wikipedia_season_extract.psv
 *   sha256 180fad720d91ad1b1bce5505de9d8f83e8a6c183625d535e2e25ec9d7f2559fa
 *
 * TO REPRODUCE EXACTLY: replace `action:'parse', page:title` with
 * `action:'parse', oldid:<revid>` using the revision IDs recorded in the
 * '#' header lines of the extract. Never scrape formula1.com; never use
 * Jolpica/Ergast (DEC-003, DEC-008).
 *
 * OUTPUT FORMAT (pipe-separated, UTF-8, '\n' line endings):
 *   #<season>|<page title>|<revision id>|<retrieved UTC>
 *   <season>|<round>|<date text>|<race article>|<winners>[|<gp override>|<cell text if different>|<calendar GP name if different>]
 *   winners = ';'-joined Wikipedia link targets; '~<text>' appended when the
 *   link text differs from the target with '_' -> ' '. Empty = no winner yet.
 */
async function rttExtract() {
  const API = '/w/api.php';
  const j = async (params) => {
    const u = API + '?' + new URLSearchParams({ ...params, format: 'json', formatversion: 2 });
    for (let k = 0; k < 4; k++) {
      const r = await fetch(u);
      if (r.ok) return r.json();
      await new Promise((s) => setTimeout(s, 3000 * (k + 1)));
    }
    throw new Error('fail ' + u);
  };

  // 1. Resolve the season page title for every year (two naming schemes exist).
  const cands = [];
  for (let y = 1950; y <= 2026; y++) cands.push(`${y} Formula One World Championship`, `${y} Formula One season`);
  const titles = {};
  for (let i = 0; i < cands.length; i += 50) {
    const d = await j({ action: 'query', titles: cands.slice(i, i + 50).join('|'), redirects: 1 });
    const norm = Object.fromEntries((d.query.normalized || []).map((x) => [x.from, x.to]));
    const redir = Object.fromEntries((d.query.redirects || []).map((x) => [x.from, x.to]));
    const exist = new Set(d.query.pages.filter((p) => !p.missing).map((p) => p.title));
    for (const c of cands.slice(i, i + 50)) {
      let t = norm[c] || c; t = redir[t] || t;
      if (exist.has(t)) (titles[c.slice(0, 4)] ||= new Set()).add(t);
    }
  }

  // 2. Fetch each page (rendered HTML + revision id) and record retrieval time.
  const pages = {};
  for (const [y, set] of Object.entries(titles)) {
    const [title] = [...set];
    const retrieved = new Date().toISOString().replace(/\.\d+Z$/, 'Z');
    const d = await j({ action: 'parse', page: title, prop: 'text|revid', redirects: 1 });
    pages[y] = { title: d.parse.title, revid: d.parse.revid, retrieved_utc: retrieved, html: d.parse.text };
    await new Promise((s) => setTimeout(s, 300));
  }

  // 3. Parse the calendar table (Round | Grand Prix | Circuit | [Race] date) and
  //    the results table (Round | Grand Prix|Race | ... | Winning driver | ... | Report).
  const extract = (y) => {
    const page = pages[y];
    const doc = new DOMParser().parseFromString(page.html, 'text/html');
    doc.querySelectorAll('style, sup.reference, .mw-ref, .sortkey, .reference').forEach((e) => e.remove());
    const txt = (e) => (e ? e.textContent.replace(/\s+/g, ' ').trim() : '');
    const grid = (t) => {  // expand rowspan/colspan
      const rows = [...t.querySelectorAll(':scope > tbody > tr, :scope > thead > tr, :scope > tr')];
      const g = [];
      rows.forEach((tr, ri) => {
        g[ri] ||= []; let ci = 0;
        for (const cell of tr.children) {
          while (g[ri][ci]) ci++;
          const rs = +(cell.getAttribute('rowspan') || 1), cs = +(cell.getAttribute('colspan') || 1);
          for (let r = 0; r < rs; r++) for (let c = 0; c < cs; c++) (g[ri + r] ||= [])[ci + c] = cell;
          ci += cs;
        }
      });
      return g;
    };
    const links = (c) => (c ? [...c.querySelectorAll('a[href^="/wiki/"]')]
      .filter((a) => !a.closest('.flagicon') && !a.querySelector('img') && !/^\/wiki\/(File|Help|Template):/.test(a.getAttribute('href')))
      .map((a) => [decodeURIComponent(a.getAttribute('href').slice(6)), txt(a)]) : []);
    let cal = null, res = null;
    for (const t of doc.querySelectorAll('table')) {
      const g = grid(t); if (!g.length) continue;
      const h = g[0].map(txt);
      const iR = h.findIndex((x) => /^Round$/i.test(x)), iG = h.findIndex((x) => /^(Grand Prix|Race$)/.test(x));
      if (iR < 0 || iG < 0) continue;
      const iW = h.findIndex((x) => /^Winning driver/.test(x)), iD = h.findIndex((x) => /^(Race )?[Dd]ate$/.test(x)), iRep = h.findIndex((x) => /^Report$/.test(x));
      const data = g.slice(1).filter((r) => r[iR] && /^\d+$/.test(txt(r[iR])));
      if (iW >= 0 && !res) { res = {}; for (const r of data) { const rep = links(r[iRep]); res[+txt(r[iR])] = [txt(r[iG]), rep.length ? rep[0][0] : '', links(r[iW]), txt(r[iW])]; } }
      else if (iD >= 0 && !cal) { cal = {}; for (const r of data) cal[+txt(r[iR])] = [txt(r[iD]), txt(r[iG])]; }
    }
    const rounds = [...new Set([...Object.keys(cal || {}), ...Object.keys(res || {})].map(Number))].sort((a, b) => a - b);
    const races = rounds.map((n) => {
      const c = (cal || {})[n] || ['', ''], r = (res || {})[n] || ['', '', [], ''];
      return [n, c[0], r[0] || c[1], r[1], r[2], r[3] !== r[2].map((x) => x[1]).join(' ') ? r[3] : null, c[1]];
    });
    return { y: +y, t: page.title, rev: page.revid, at: page.retrieved_utc, races };
  };

  // 4. Serialise.
  const sp = (s) => s.replace(/_/g, ' ');
  const lines = [];
  for (const x of Object.keys(pages).sort().map(extract)) {
    lines.push(`#${x.y}|${x.t}|${x.rev}|${x.at}`);
    for (const [n, date, gp, href, drv, cellDiff, calGp] of x.races) {
      const dv = drv.map((d) => (sp(d[0]) === d[1] ? d[0] : d[0] + '~' + d[1])).join(';');
      const gpDefault = href ? sp(href.replace(/^\d{4}_/, '')) : '';
      const f = [x.y, n, date, href, dv, gp === gpDefault ? '' : gp, cellDiff === null ? '' : cellDiff, calGp === gp ? '' : calGp];
      while (f.length > 5 && f[f.length - 1] === '') f.pop();
      lines.push(f.join('|'));
    }
  }
  return lines.join('\n') + '\n';
}

/*
 * Companion extracts (same session, same method):
 *  - wikipedia_driver_ids.psv: every winner link target resolved through
 *    Wikipedia redirects (action=query&redirects=1) -> canonical title|pageid.
 *    Lines: <link target>|<canonical title>|<pageid>.
 *  - wikipedia_list_of_gp_winners.psv: "List of Formula One Grand Prix winners"
 *    (revision 1376824402), table "Rank | Country | Driver | Wins | Seasons
 *    active | First win | Last win". Lines: <canonical title>|<wins>|<first win>|<last win>.
 */
