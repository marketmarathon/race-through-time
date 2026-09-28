/* RTT-002 nationality extraction (28 Sep 2026). Run in a browser tab on en.wikipedia.org
 * (Luke's Chrome), because Wikimedia rate-limits the cloud sandboxes (HTTP 429).
 * Output: data/rtt-002/source/wikipedia_wikidata_nationality.psv and wikidata_countries.psv
 * (verified by SHA-256 against hashes computed in the browser before use).
 *
 * 1. Wikitext of "List of Formula One Grand Prix winners" at revision 1376824402 (the revision
 *    already used as a cross-check in source/README.md): action=parse&oldid=1376824402&prop=wikitext.
 *    <ref> tags removed. Each driver row ("|-" separated) holds a flag cell ({{XXX}},
 *    {{flagicon|XXX}} or {{flagcountry|XXX|variant}}) before the {{sortname|First|Last|link|dab=...}}
 *    cell, then the wins cell. Link target = 3rd positional sortname argument, else "First Last",
 *    plus " (dab)" when dab= is set.
 * 2. Targets resolved with action=query&redirects=1&prop=pageprops&ppprop=wikibase_item
 *    (50 per request): canonical title, page ID (= drivers.csv driver_id "wp<pageid>"), Wikidata item.
 * 3. Wikidata wbgetentities (origin=*, 50 per request): lastrevid, P1532 (country for sport) and
 *    P27 (country of citizenship), deprecated statements ignored, preferred rank marked "*".
 *    Country items: English label and P298 (ISO 3166-1 alpha-3).
 */
async function extractNationality() {
  const REV = 1376824402;
  const p = await (await fetch(`/w/api.php?action=parse&oldid=${REV}&prop=wikitext&format=json&formatversion=2`)).json();
  const meta = { revid: p.parse.revid, retrieved: new Date().toISOString() };
  const wc = p.parse.wikitext.replace(/<ref[^>]*\/>/g, '').replace(/<ref[\s\S]*?<\/ref>/g, '');
  const nat = [];
  for (const r of wc.split(/\n\|-\s*\n/)) {
    const sm = r.match(/\{\{sortname\|([^}]*)\}\}/i);
    if (!sm) continue;
    const ps = sm[1].split('|');
    const pos = ps.filter(x => !x.includes('=')).map(s => s.trim());
    const named = Object.fromEntries(ps.filter(x => x.includes('=')).map(x => x.split('=').map(s => s.trim())));
    let target = (pos[2] && pos[2] !== '') ? pos[2] : (pos[0] + ' ' + pos[1]);
    if (named.dab) target = pos[0] + ' ' + pos[1] + ' (' + named.dab + ')';
    const lines = r.split('\n');
    const si = lines.findIndex(l => /\{\{sortname/i.test(l));
    let code = null, variant = null;
    for (let j = si - 1; j >= 0; j--) {
      let m = lines[j].match(/\{\{\s*flagcountry\|([A-Z]{3})(?:\|([^}|]*))?\}\}/i);
      if (m) { code = m[1]; variant = m[2] || ''; break; }
      m = lines[j].match(/\{\{\s*(?:flagicon\|)?([A-Z]{2,3})\s*(?:\|([^}]*))?\}\}/);
      if (m) { code = m[1]; variant = m[2] || ''; break; }
    }
    const wl = lines.slice(si + 1).map(l => l.replace(/"/g, '')).find(l => /^\|\s*align\s*=\s*center\s*\|\s*\d+\s*$/.test(l));
    nat.push({ target, code, variant, wins: wl ? wl.replace(/.*\|/, '').trim() : '' });
  }
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let i = 0; i < nat.length; i += 50) {
    const batch = nat.slice(i, i + 50);
    const j = await (await fetch('/w/api.php?action=query&format=json&formatversion=2&redirects=1&prop=pageprops&ppprop=wikibase_item&titles=' + encodeURIComponent(batch.map(x => x.target).join('|')))).json();
    const norm = {}; (j.query.normalized || []).forEach(n => norm[n.from] = n.to);
    const red = {}; (j.query.redirects || []).forEach(n => red[n.from] = n.to);
    const byTitle = {}; j.query.pages.forEach(pg => byTitle[pg.title] = pg);
    for (const x of batch) { let c = norm[x.target] || x.target; c = red[c] || c; const pg = byTitle[c]; Object.assign(x, { canonical: c, pageid: pg.pageid, qid: pg.pageprops.wikibase_item }); }
    await sleep(500);
  }
  const WD = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&origin=*';
  const ent = {};
  for (let i = 0; i < nat.length; i += 50) {
    Object.assign(ent, (await (await fetch(WD + '&props=claims|info&ids=' + nat.slice(i, i + 50).map(x => x.qid).join('|'))).json()).entities);
    await sleep(800);
  }
  const vals = (e, P) => (e.claims[P] || []).filter(c => c.rank !== 'deprecated' && c.mainsnak.datavalue);
  const cset = new Set();
  nat.forEach(x => {
    const e = ent[x.qid]; x.rev = e.lastrevid;
    x.p1532 = vals(e, 'P1532').map(c => c.mainsnak.datavalue.value.id + (c.rank === 'preferred' ? '*' : ''));
    x.p27 = vals(e, 'P27').map(c => c.mainsnak.datavalue.value.id);
    x.p1532.forEach(q => cset.add(q.replace('*', ''))); x.p27.forEach(q => cset.add(q));
  });
  const cq = [...cset], lab = {};
  for (let i = 0; i < cq.length; i += 50) {
    const j = await (await fetch(WD + '&props=labels|claims&languages=en&ids=' + cq.slice(i, i + 50).join('|'))).json();
    for (const [q, e] of Object.entries(j.entities)) lab[q] = [e.labels.en && e.labels.en.value, ((e.claims && e.claims.P298) || []).map(c => c.mainsnak.datavalue && c.mainsnak.datavalue.value)[0] || ''];
    await sleep(800);
  }
  const wdTime = new Date().toISOString();
  const f1 = [`#source|List of Formula One Grand Prix winners|revision ${meta.revid}|retrieved ${meta.retrieved}|wikidata retrieved ${wdTime}`,
    '#pageid|canonical_title|wp_flag_code|wp_flag_variant|wp_wins|wikidata_qid|wikidata_lastrevid|P1532|P27',
    ...nat.map(x => [x.pageid, x.canonical, x.code, x.variant, x.wins, x.qid, x.rev, x.p1532.join(';'), x.p27.join(';')].join('|'))].join('\n') + '\n';
  const f2 = ['#qid|label_en|iso3_P298', ...Object.entries(lab).sort().map(([q, v]) => [q, v[0] || '', v[1] || ''].join('|'))].join('\n') + '\n';
  return { f1, f2 };
}
