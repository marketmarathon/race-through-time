/* Player tests: the six stress fixtures (plus the shared drive again with the winner line and
 * highlight on), an RTT-002 slice (1984-1989), the two IQ-05 round-2 pilots (2014-2021: A top 20,
 * B top ten + winner line), the whole RTT-002 run, and full-dataset checks of the colour rule
 * (top ten and top 20) and of the record moments.
 *
 * For each case:
 *   1. scripts/rtt_adapter.py turns the CSVs into the player's input (as production does)
 *   2. the EXPECTED board after every race is computed here, independently, straight from
 *      win_credits.csv (career_wins_after, and credit order for ties) - not from the adapter's
 *      output and not from rtt_timeline.js
 *   3. the player is opened through the kit's own driver path (rtt.js openPlayer) at 1920
 *      preview width, and EVERY race frame is drawn in order (the rank glide is stateful)
 *   4. on every frame, the text the player drew is checked (draw-call log, window.__LABELS):
 *        - every value label is "<whole number> win(s)" and equals the expected count for that
 *          driver after the race the frame is showing
 *        - the race the frame shows (time label: season, Grand Prix, date) matches races.csv
 *        - the target order of the visible rows is the expected order (tie rule included)
 *        - axis labels are whole numbers; every label lies inside the 1920x1080 frame
 *        - races are shown in order, each for at least one frame, and a count never changes
 *          except on the first frame of a race
 *   5. at EVENT BOUNDARIES (the first and last frame of every race) the frame is saved as a PNG
 *      and, when tesseract is installed, every value label is cut out of the PNG and read back by
 *      OCR, so the pixels are checked as well as the draw calls
 *   6. fixture-specific expectations from fixture.json
 *
 * Added in IQ-05 (DEC-022):
 *   7. entry visibility: every driver who joins the visible top N must be CLEARLY VISIBLE (row
 *      opacity >= 0.8 with its name and value label drawn) within 8 frames of the first frame
 *      of that race
 *   8. colours, on every drawn frame: no two bars on screen (opacity > 0) share a colour or
 *      are closer than colour_rule.min_delta_e; each driver has one colour, the same in every
 *      case that draws RTT-002 (1984-89, both pilots, the full run)
 *   9. colours, on every race of the full RTT-002 dataset, from win_credits.csv alone: the
 *      drivers in the top N after that race and the fade_races races before it (so rows still
 *      fading out are included) all have different, clearly distinct colours
 *  10. milestones (pilots): Hamilton on 91 level with Schumacher at the 2020 Eifel GP, and
 *      past him at the 2020 Portuguese GP, read from the drawn labels
 *  11. pilots: no closing card, a hold of at least pacing.end_hold_sec on the final board
 *
 * Added in IQ-05 round 2 (DEC-027):
 *  12. winner line (when on): on every frame it reads "Won by <driver> · <n> win(s)" for every
 *      credited driver of the race shown, names and counts from drivers.csv / win_credits.csv
 *  13. winner highlight (when on): on the first frame of every race exactly the credited winners
 *      whose bars are in the top N are lit, and nothing else is ever lit; no flicker (a bar's
 *      highlight only ever rises at an onset, from fully off, on the first frame of a race that
 *      driver won; a repeat winner stays lit); at most 3 onsets in any 1 s; each fades out
 *      within highlight.sec
 *  14. record holds (when on): exactly the races that record_progression.csv marks BECOMES_JOINT
 *      or BECOMES_SOLE inside the window are held record_hold.sec, the rank glide has settled
 *      (every row within 0.1 row of its place) on the last frame of each hold, and every other
 *      race keeps a beat of 0.8-1.4 x sec_per_event
 *  15. every number (values, axis, season, date, winner line) is drawn on fixed-pitch digits
 *  16. opening without a title card (intro_sec 0): the first frame is the board with the title;
 *      pacing.final_board_sec: the final board is on screen exactly that long
 *  17. record_moments_full_dataset: the player's record events equal record_progression.csv on
 *      every row of the full dataset
 *
 * Added in IQ-05 round 3 (DEC-034 to DEC-044; variant B's case removed with its config):
 *  18. flags (when on): every flag drawn is the flag_code of that driver in the nationality file
 *      (read here, independently of rtt.js), sits on its row, and every row on screen whose driver
 *      has a flag code carries it; a driver without one (NOT FOUND) gets no flag
 *  19. event label (when on): on every frame of a race, each credited winner whose bar is on
 *      the board shows "· <Grand Prix, 'Grand Prix' written 'GP'>" from races.csv right after its
 *      value, at full strength; the only other event labels allowed are the previous race's
 *      winners, fading (never brightening) within event_label.fade_sec of the new race; nothing
 *      for a winner off the board
 *  20. time block (time_label.mode "block"): on every frame the season, Grand Prix and date (and
 *      winner line) overlap no bar, flag, name, value, event label, axis number, title or footer
 *  21. overlays: on every frame no text, bar or flag enters a reserved overlay box (logo, car);
 *      with placeholder pictures (plain rectangles written at test time, never committed) each
 *      is drawn inside its box; with the files absent nothing is drawn and the player still runs
 *  22. colour priority (top-20 pilot): Hamilton, Schumacher, Verstappen, Senna and Prost get
 *      bright colours (CIELAB L* and C* both at least 50 as drawn); the tiers of all drivers who
 *      ever reach the top ten are reported
 *
 * Changed in IQ-05 round 4 (DEC-045 to DEC-050; the round-3 fixture case now runs the round-4
 * features and is renamed shared_drive_round4):
 *  23. date line (time_label.mode "line"): on every frame exactly one line, reading
 *      "<D Month YYYY> · <Grand Prix, 'GP'>" for the race on screen from races.csv, including
 *      races whose winner is not on the board (counted and reported); it overlaps nothing (as 20)
 *  24. event label with date (event_label.date): the label reads "· <GP> · <D Month YYYY>" from
 *      races.csv, and every event label ends inside the 64 px right margin (x <= 1856); the
 *      furthest right edge on any frame is reported
 *  25. overlays: the axis grid lines are checked too, so nothing at all but the picture is drawn
 *      inside a reserved box
 *
 * Added in IQ-05 round 5 (DEC-053, DEC-054):
 *  26. stats label (stats_label.enabled): on every frame, every bar on screen that carries a value
 *      label carries exactly one stats label right after it, same row, same opacity, reading
 *      "· <S> start(s) · <R>%" where S is the driver's career starts after the race shown, read here
 *      from starts.csv, and R is wins / starts recomputed here from win_credits.csv and starts.csv
 *      (BigInt, one decimal, rounded half up); the win count (value label) is bold (700) and the
 *      stats label regular (500); the numbers change only on the first frame of a race; every stats
 *      label ends inside the 64 px right margin (furthest right edge reported)
 *  27. overlaps (row labels measured as drawn, inside the board's clip, y 150-1034): on every frame each stats label overlaps no bar, flag, name, value or stats label
 *      of any row that is not mid-overtake (another row within 0.85 row: those rows cross by design
 *      and are counted, not failed), and no title, subtitle, axis number, footer or date line; the
 *      overlay boxes (21, 25) and the frame edges are checked for it as for every label
 *  28. win_rate_rounding: the player's rateText against Python's decimal ROUND_HALF_UP on every
 *      pair 0 <= wins <= starts <= 500
 *
 * Usage: node tests/player/run_tests.js [case ...]     (needs `npm ci` in kits/rtt-002)
 * Output: tests/output/ (PNGs, gitignored) and tests/player/RESULTS.md
 */
const fs = require('fs');
const path = require('path');
const { execFileSync, spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..', '..');
const KITDIR = path.join(ROOT, 'kits', 'rtt-002');
const rtt = require(path.join(KITDIR, 'rtt.js'));
const OUTDIR = path.join(ROOT, 'tests', 'output');
const FIX = path.join(ROOT, 'tests', 'fixtures');
const HAS_OCR = spawnSync('tesseract', ['--version']).status === 0;
const TIMELINE = require(path.join(KITDIR, 'rtt_timeline.js'));
const ENTRY_MAX_FRAMES = 8;          // DEC-022 (4): clearly visible within 8 frames (0.27 s at 30 fps)
const CLEAR_ALPHA = 0.8;             // "clearly visible": row opacity at least this, labels drawn
const COLOUR_OF = {};                // rows -> driver -> drawn colour, across every RTT-002 case with that board
const HOLD_SETTLE_ROWS = 0.1;        // "settled": every row within this many rows of its place
const MAX_ONSETS_PER_SEC = 3;        // blueprint section 10: no strobing
const TAB_KINDS = ['value', 'axis', 'time_season', 'time_date', 'time_line', 'winner', 'event', 'stats'];
const OVERTAKE_ROWS = 0.85;          // rows closer than this are mid-overtake (the player's name-pad rule)
const RIGHT_MARGIN = 1920 - 64;      // IQ-05d: every event label must end inside the 64 px right margin
const BRIGHT = 50;
const YT_CONTROLS_PX = 130;          // DEC-042: bottom strip YouTube's player controls may cover (estimate, 12% of 1080)                   // "bright" colour: CIELAB L* and C* both at least this, as drawn
const STARS = ['Lewis Hamilton', 'Michael Schumacher', 'Max Verstappen', 'Ayrton Senna', 'Alain Prost'];
const gpShort = gp => gp.replace(/Grand Prix/g, 'GP');       // DEC-034: "GP" throughout

const { placeholders: makePlaceholders } = require('./placeholders.js');
const placeholders = cfg => makePlaceholders(cfg, path.join(OUTDIR, '_placeholders'));
const rectOf = x => ({ l: x.x, r: x.x + x.w, t: x.y - (x.asc != null ? x.asc : x.size * 0.8), b: x.y + (x.desc != null ? x.desc : x.size * 0.25) });
const gap = (a, b) => { const dx = Math.max(0, a.l - b.r, b.l - a.r), dy = Math.max(0, a.t - b.b, b.t - a.b); return Math.hypot(dx, dy); };
const overlap = (a, b) => a.l < b.r && b.l < a.r && a.t < b.b && b.t < a.b;

/* ---- a small CSV reader (quoted fields allowed) ---- */
function readCSV(file) {
  const s = fs.readFileSync(file, 'utf8');
  const rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (q) { if (ch === '"') { if (s[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += ch; }
    else if (ch === '"') q = true;
    else if (ch === ',') { row.push(f); f = ''; }
    else if (ch === '\n') { row.push(f); rows.push(row); row = []; f = ''; }
    else if (ch !== '\r') f += ch;
  }
  if (f.length || row.length) { row.push(f); rows.push(row); }
  const head = rows.shift();
  return rows.filter(r => r.length === head.length).map(r => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}

/* ---- expected boards, from win_credits.csv alone ---- */
function expected(dir) {
  const races = readCSV(path.join(dir, 'races.csv'));
  const credits = readCSV(path.join(dir, 'win_credits.csv'));
  const names = Object.fromEntries(readCSV(path.join(dir, 'drivers.csv')).map(d => [d.driver_id, d.display_name]));
  const byRace = {};
  for (const c of credits) (byRace[c.race_index] = byRace[c.race_index] || []).push(c);
  /* (26) starts after each race, straight from starts.csv (career_starts_after) */
  const sFile = path.join(dir, 'starts.csv'), startsByRace = {};
  const hasStarts = fs.existsSync(sFile);
  if (hasStarts) for (const x of readCSV(sFile)) (startsByRace[x.race_index] = startsByRace[x.race_index] || []).push(x);
  const st = {};
  const tot = {}, reached = {}, after = {};
  for (const r of races) {
    for (const x of (startsByRace[r.race_index] || [])) st[x.driver_id] = +x.career_starts_after;
    for (const c of (byRace[r.race_index] || [])) {
      tot[c.driver_id] = +c.career_wins_after;                  // the data's own count
      reached[c.driver_id] = +c.credit_index;                   // when it reached that count
    }
    const order = Object.keys(tot).sort((a, b) => (tot[b] - tot[a]) || (reached[a] - reached[b]));
    const credits = (byRace[r.race_index] || []).slice().sort((a, b) => a.credit_index - b.credit_index)
      .map(c => ({ id: c.driver_id, n: +c.career_wins_after }));
    after[r.race_index] = { order, totals: { ...tot }, race: r, credits, starts: { ...st } };
  }
  return { races, after, names, hasStarts, startsFor: ri => after[ri] ? after[ri].starts : {} };
}

/* (26) win rate recomputed here: tenths of a percent = floor((2000 w + s) / (2 s)), in BigInt */
function rateOf(w, s) { const t = (2000n * BigInt(w) + BigInt(s)) / (2n * BigInt(s)); return `${t / 10n}.${t % 10n}`; }
function statsWant(w, s) { return `· ${s.toLocaleString('en-GB')} ${s === 1 ? 'start' : 'starts'} · ${rateOf(w, s)}%`; }

function winnerText(credits, names) {
  return 'Won by ' + credits.map(c => names[c.id] + ' · ' + c.n.toLocaleString('en-GB') + (c.n === 1 ? ' win' : ' wins')).join(' & ');
}

function dateText(iso, months) { const [y, m, d] = iso.split('-').map(Number); return d + ' ' + months[m - 1] + ' ' + y; }

function ocr(png) {
  // one thread: tesseract's own threading only slows it down on crops this small
  const r = spawnSync('tesseract', [png, 'stdout', '--psm', '7', '-l', 'eng'], { encoding: 'utf8', env: Object.assign({}, process.env, { OMP_THREAD_LIMIT: '1' }) });
  return (r.stdout || '').trim();
}

/* (9) The colour rule on every race of the full RTT-002 dataset, from win_credits.csv alone
   (the boards are computed here, not taken from rtt_timeline.js). The colours are the kit's
   assignment (rtt_timeline.js assignColours on the full race file); main() then checks that every
   colour actually DRAWN for a driver in any RTT-002 case is that same colour. */
function colourRuleFullDataset(dir, configFile, name) {
  const cfg = rtt.loadConfig(configFile);
  const data = JSON.parse(fs.readFileSync(path.join(KITDIR, cfg.race_file), 'utf8'));
  const E = expected(dir);
  const W = cfg.colour_rule.fade_races, minDE = cfg.colour_rule.min_delta_e;
  const assigned = TIMELINE.assignColours(data, cfg).index;
  const colour = id => TIMELINE.drawnColour(cfg.palette[assigned[id]]);
  const res = { name, config: configFile, rows: cfg.rows, events: E.races.length, failures: [], notes: [], max_together: 0, closest: Infinity };
  const fail = m => { if (res.failures.length < 40) res.failures.push(m); };
  const tops = E.races.map(r => E.after[r.race_index].order.slice(0, cfg.rows));
  const onBoard = new Set(tops.flat());
  E.races.forEach((r, k) => {
    const V = [...new Set(tops.slice(Math.max(0, k - W), k + 1).flat())];
    res.max_together = Math.max(res.max_together, V.length);
    for (const a of V) for (const b of V) if (a < b) {
      const d = TIMELINE.deltaE(colour(a), colour(b));
      if (d < res.closest) { res.closest = d; res.closest_pair = `${E.names[a]} / ${E.names[b]}`; }
      if (colour(a) === colour(b)) fail(`race ${r.race_index} (${r.season} ${r.grand_prix}): ${E.names[a]} and ${E.names[b]} share ${colour(a)}`);
      else if (d < minDE) fail(`race ${r.race_index}: ${E.names[a]} and ${E.names[b]} only ${d.toFixed(1)} apart`);
    }
  });
  res.drivers = onBoard.size;
  res.colours_used = new Set([...onBoard].map(colour)).size;
  res.palette = cfg.palette.length;
  res.pass = res.failures.length === 0;
  res.notes.push(`${res.events} races; ${res.drivers} drivers ever reach the top ${cfg.rows}; at most ${res.max_together} can be on screen together (top ${cfg.rows} after a race and the ${W} before it, so rows still fading out count)`);
  res.notes.push(`${res.colours_used} colours used of a ${res.palette}-colour palette; every pair that can be on screen together differs, the closest being ${res.closest_pair} at CIEDE2000 ${res.closest.toFixed(1)} (rule: at least ${minDE})`);
  let palMin = Infinity; cfg.palette.forEach((a, i) => cfg.palette.slice(0, i).forEach(b => { palMin = Math.min(palMin, TIMELINE.deltaE(a, b)); }));
  const lum = h => { const n = parseInt(TIMELINE.drawnColour(h).slice(1), 16), l = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
                     return 0.2126 * l((n >> 16) & 255) + 0.7152 * l((n >> 8) & 255) + 0.0722 * l(n & 255); };
  res.notes.push(`palette: closest pair of any two palette colours CIEDE2000 ${palMin.toFixed(1)}; weakest white-name contrast on a bar ${Math.min(...cfg.palette.map(h => 1.05 / (lum(h) + 0.05))).toFixed(2)}:1`);
  const byColour = {};
  for (const id of [...onBoard].sort((a, b) => E.races.findIndex(r => E.after[r.race_index].order.slice(0, cfg.rows).includes(a)) - E.races.findIndex(r => E.after[r.race_index].order.slice(0, cfg.rows).includes(b))))
    (byColour[colour(id)] = byColour[colour(id)] || []).push(E.names[id]);
  res.by_colour = byColour;
  res.colour_of = Object.fromEntries([...onBoard].map(id => [id, colour(id)]));
  /* (22) colour priority: tiers of the drivers who ever reach the top ten */
  if (cfg.colour_rule.priority) {
    const tier = h => { const [L, a, b] = TIMELINE.lab(h), C = Math.hypot(a, b); return L >= BRIGHT && C >= BRIGHT ? 'bright' : C >= BRIGHT ? 'vivid, darker' : 'muted'; };
    const top10 = new Set(E.races.flatMap(r => E.after[r.race_index].order.slice(0, cfg.colour_rule.priority.rows)));
    const count = {}; for (const id of top10) count[tier(colour(id))] = (count[tier(colour(id))] || 0) + 1;
    res.notes.push(`colour priority: ${top10.size} drivers ever reach the top ten; their colours: ${Object.entries(count).map(([k, v]) => `${v} ${k}`).join(', ')} (bright = CIELAB L* and C* both at least ${BRIGHT} as drawn)`);
    const idOf = nm => Object.keys(E.names).find(id => E.names[id] === nm);
    const stars = STARS.map(nm => { const h = colour(idOf(nm)), [L, a, b] = TIMELINE.lab(h); return { nm, h, L, C: Math.hypot(a, b), t: tier(h) }; });
    res.notes.push('named drivers: ' + stars.map(x => `${x.nm} \`${x.h}\` (L* ${x.L.toFixed(0)}, C* ${x.C.toFixed(0)}, ${x.t})`).join('; '));
    for (const x of stars) if (x.t !== 'bright') fail(`${x.nm} has a ${x.t} colour ${x.h}`);
    const brightOthers = [...onBoard].filter(id => !top10.has(id) && tier(colour(id)) === 'bright').map(id => E.names[id]);
    res.notes.push(`drivers who never reach the top ten but share a bright colour (only where nothing else fitted): ${brightOthers.join(', ') || 'none'}`);
    res.pass = res.failures.length === 0;
  }
  return res;
}

/* (17) The player derives record events from the counts (rtt_timeline.js); they must equal
   data/rtt-002/record_progression.csv row for row over the whole dataset. */
function recordProgression(dir) { return readCSV(path.join(dir, 'record_progression.csv')); }
function recordMomentsFullDataset(dir) {
  const cfg = rtt.loadConfig('config.json');
  const data = JSON.parse(fs.readFileSync(path.join(KITDIR, cfg.race_file), 'utf8'));
  const got = TIMELINE.build(data, cfg).records.map(r => [r.date, r.id, r.total, r.type].join('|'));
  const want = recordProgression(dir).map(r => [r.race_date, r.driver_id, r.career_wins, r.event].join('|'));
  const res = { name: 'record_moments_full_dataset', events: data.events.length, failures: [], notes: [] };
  for (let i = 0; i < Math.max(got.length, want.length); i++)
    if (got[i] !== want[i] && res.failures.length < 20) res.failures.push(`row ${i + 1}: player ${got[i]}, record_progression.csv ${want[i]}`);
  const n = t => want.filter(w => w.endsWith('|' + t)).length;
  res.notes.push(`${want.length} record events in record_progression.csv (${n('BECOMES_SOLE')} BECOMES_SOLE, ${n('BECOMES_JOINT')} BECOMES_JOINT, ${n('EXTENDS_SOLE')} EXTENDS_SOLE); the player's ${got.length} match row for row`);
  res.pass = res.failures.length === 0;
  return res;
}

/* (28) the player's win rate (rtt_timeline.js rateText, the function the page draws with) against
   Python's decimal ROUND_HALF_UP, a different implementation in a different language */
function winRateRounding() {
  const N = 500;
  const py = execFileSync('python3', ['-c', `
from decimal import Decimal, ROUND_HALF_UP
import sys
out = []
for w in range(0, ${N} + 1):
    for s in range(max(1, w), ${N} + 1):
        out.append(str((Decimal(100 * w) / Decimal(s)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)))
sys.stdout.write("\\n".join(out))`], { encoding: 'utf8', maxBuffer: 1 << 26 }).split('\n');
  const res = { name: 'win_rate_rounding', failures: [], notes: [] };
  let i = 0;
  for (let w = 0; w <= N; w++) for (let s = Math.max(1, w); s <= N; s++, i++) {
    const got = TIMELINE.rateText(w, s);
    if (got !== py[i] && res.failures.length < 20) res.failures.push(`${w}/${s}: player ${got}, decimal ROUND_HALF_UP ${py[i]}`);
    if (got !== rateOf(w, s) && res.failures.length < 20) res.failures.push(`${w}/${s}: player ${got}, test BigInt ${rateOf(w, s)}`);
  }
  const ex = [[1, 8], [1, 16], [3, 16], [1, 80], [91, 306], [1, 1], [1, 3]].map(([w, s]) => `${w}/${s} = ${TIMELINE.rateText(w, s)}%`).join(', ');
  res.notes.push(`${i} pairs (0 <= wins <= starts <= ${N}): player rateText = Python decimal ROUND_HALF_UP = test BigInt on every pair; examples ${ex}`);
  res.pass = res.failures.length === 0;
  return res;
}

async function runCase(c) {
  const out = path.join(OUTDIR, c.name);
  fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
  const json = path.join(out, 'race.json');
  const adapter = execFileSync('python3', [path.join(ROOT, 'scripts', 'rtt_adapter.py'), c.dir, json], { encoding: 'utf8' }).trim();
  const data = JSON.parse(fs.readFileSync(json, 'utf8'));
  const cfg = c.config ? rtt.loadConfig(c.config, c.overrides) : rtt.loadConfig('config.json', Object.assign({ window: c.window || { from: null, to: null } }, c.overrides || {}));
  const E = expected(c.dir);
  const inWindow = E.races.filter(r => (!cfg.window.from || r.race_date >= cfg.window.from) && (!cfg.window.to || r.race_date <= cfg.window.to));
  const before = E.races.filter(r => cfg.window.from && r.race_date < cfg.window.from).pop();

  const res = { name: c.name, adapter_sha256: adapter.split(/\s+/)[0], events: inWindow.length, frames: 0,
                boundary_frames: 0, labels_checked: 0, ocr_checked: 0, ocr_skipped_overlap: 0, ocr_mismatch: [], failures: [], notes: [],
                config: c.config || 'config.json', entries: 0, entry_frames_max: 0, colour_frames: 0,
                rows: cfg.rows, winner_lines: 0, onsets: 0, onsets_max_per_sec: 0, tab_labels: 0, holds: [],
                event_labels: 0, event_fading: 0, flags_checked: 0, block_clear: null, overlay_clear: null, overlays_drawn: {},
                date_lines: 0, date_lines_offboard: 0, offboard_races: 0, event_right: null, event_right_text: null,
                stats_labels: 0, ocr_stats: 0, stats_right: null, stats_right_text: null, stats_overlap_checked: 0, stats_overtake: 0, stats_clear: null };
  const fail = m => { if (res.failures.length < 40) res.failures.push(m); };

  if (cfg.overlays) process.env.RTT_LOCAL_ASSETS = placeholders(cfg);
  /* (18) the nationality file, read here independently of rtt.js */
  const FLAGON = !!(cfg.flags && cfg.flags.enabled), EVON = !!(cfg.event_label && cfg.event_label.enabled);
  const STON = !!(cfg.stats_label && cfg.stats_label.enabled);
  if (STON && !E.hasStarts) throw new Error(c.name + ': stats_label on but ' + c.dir + ' has no starts.csv');
  const natCode = {};
  if (FLAGON) for (const r of readCSV(path.resolve(KITDIR, cfg.flags.csv))) natCode[r.driver_id] = /^[a-z]{2}(-[a-z]+)?$/.test(r.flag_code) ? r.flag_code : null;
  const { br, pg } = await rtt.openPlayer({ cfg, data, raster: 1, chrome: process.env.PW_CHROME || '/opt/pw-browsers/chromium' });
  delete process.env.RTT_LOCAL_ASSETS;
  try {
    const info = await pg.evaluate(() => ({ raceFrames: RACE_FRAMES, start: TL.startFrame, kind: TL.kind, mult: TL.mult, hold: TL.hold, namePx: nameSize(), trunc: NAME_TRUNC }));
    const WL = !!(cfg.winner_line && cfg.winner_line.enabled), HLON = !!(cfg.highlight && cfg.highlight.enabled);
    const hlFrames = HLON ? Math.round((cfg.highlight.sec || 0.4) * cfg.fps) : 0;
    const prevHl = {}, onsetFrames = [];
    /* (13) who should be lit on race k: the credited winners in the top N after it */
    const litOn = k => { const e = E.after[inWindow[k].race_index]; return e.credits.map(x => x.id).filter(id => e.order.slice(0, cfg.rows).includes(id)); };
    const node = rtt.frameTotals(cfg, data);
    if (node.tl.raceFrames !== info.raceFrames) fail(`Node and page disagree on race frames (${node.tl.raceFrames} vs ${info.raceFrames})`);
    res.race_sec = info.raceFrames / cfg.fps; res.name_px = info.namePx; res.name_truncated = info.trunc;
    res.pacing = { rank_change: 0, visible_change: 0, quiet: 0 }; info.kind.forEach(k => res.pacing[k]++);
    const [lo, hi] = cfg.pacing.bounds;
    if (info.mult.some(m => m < lo - 1e-9 || m > hi + 1e-9)) fail('a pacing multiplier is outside ' + cfg.pacing.bounds);

    const bounds = new Set();
    info.start.forEach((s, k) => { bounds.add(s); bounds.add((k + 1 < info.start.length ? info.start[k + 1] : info.raceFrames) - 1); });

    const el = await pg.$('#c');
    let lastIdx = before ? before.race_index : null, seenRaces = [], prevVals = {}, lag = {};
    res.entry_lag_max = 0;
    const outroFrames = Math.round(cfg.fps * Math.min(0.5, cfg.outro_sec));
    /* entries: drivers in the top N after race k but not after the race before it */
    const prevTop = k => (k === 0 ? (before ? E.after[before.race_index].order : []) : E.after[inWindow[k - 1].race_index].order).slice(0, cfg.rows);
    const entering = {};             // driver -> {k, start frame} while waiting to be clearly visible
    const minDE = (cfg.colour_rule && cfg.colour_rule.min_delta_e) || 0;
    const fadeFrames = EVON ? Math.max(1, (cfg.event_label.fade_sec || 0.3) * cfg.fps) : 0;
    /* (24) the event label's text straight from races.csv: "<GP>" or, with event_label.date, "<GP> · <D Month YYYY>" */
    const evText = r => gpShort(r.grand_prix) + (EVON && cfg.event_label.date ? ' · ' + dateText(r.race_date, cfg.time_label.months) : '');
    res.offboard_races = inWindow.filter(r => { const e = E.after[r.race_index]; return !e.credits.some(x => e.order.slice(0, cfg.rows).includes(x.id)); }).length;
    let prevEv = {}, prevStats = {};
    const clipBarR = r => ({ l: r.x, r: r.x + r.w, t: Math.max(150, r.y), b: Math.min(1080 - 46, r.y + r.h) });
    /* the player clips everything on the board (bars and their labels) to y 150-1034, so a row
       sliding off the bottom is only drawn down to y 1034: measure a row's label as drawn */
    const clipRow = r => ({ l: r.l, r: r.r, t: Math.max(150, r.t), b: Math.min(1080 - 46, r.b) });
    for (let f = 0; f < info.raceFrames + outroFrames; f++) {
      const L = await pg.evaluate(t => { drawAt(t); return { labels: window.__LABELS, rank: window.__RANK, ev: window.__EVENT, bars: window.__BARS, flags: window.__FLAGS, overlays: window.__OVERLAYS || [], grid: window.__GRID || [] }; }, f / cfg.fps);
      res.frames++;
      const ri = L.ev.race_index == null ? null : String(L.ev.race_index);
      /* which race is showing, and does the time label say so */
      if (ri !== lastIdx) {
        if (f >= info.raceFrames) fail(`frame ${f}: race changed during the outro`);
        const want = lastIdx == null ? inWindow[0].race_index : String(+lastIdx + 1);
        if (String(ri) !== String(want)) fail(`frame ${f}: showed race ${ri} after ${lastIdx}, expected ${want}`);
        if (!info.start.includes(f)) fail(`frame ${f}: race changed off an event boundary`);
        seenRaces.push(String(ri)); lastIdx = ri;
      }
      const exp = ri != null ? E.after[ri] : { order: [], totals: {} };
      const k = L.ev.k;
      if (k >= 0 && info.start[k] === f)
        for (const id of exp.order.slice(0, cfg.rows)) if (!prevTop(k).includes(id)) { entering[id] = { k, s: f, race: ri }; res.entries++; }
      if (ri != null) {
        const r = exp.race;
        const tlL = L.labels.filter(x => x.kind.startsWith('time_'));
        const tl = Object.fromEntries(tlL.map(x => [x.kind, x.text]));
        if (cfg.time_label.mode === 'line') {
          /* (23) the date line: one line, the race on screen, whoever won it */
          const want = dateText(r.race_date, cfg.time_label.months) + ' · ' + gpShort(r.grand_prix);
          if (tlL.length !== 1 || tl.time_line !== want || !(tlL[0].alpha > 0.99)) fail(`frame ${f} (race ${ri}): date line "${tlL.map(x => x.text).join(' | ')}" != "${want}"`);
          else {
            res.date_lines++;
            if (!exp.credits.some(x => exp.order.slice(0, cfg.rows).includes(x.id))) res.date_lines_offboard++;
          }
        } else {
          if (tl.time_season !== r.season) fail(`frame ${f}: season label "${tl.time_season}" != ${r.season}`);
          if (tl.time_gp !== r.grand_prix) fail(`frame ${f}: Grand Prix label "${tl.time_gp}" != "${r.grand_prix}"`);
          if (tl.time_date !== dateText(r.race_date, cfg.time_label.months)) fail(`frame ${f}: date label "${tl.time_date}" != ${r.race_date}`);
        }
      }
      /* the visible order */
      const wantRank = exp.order.slice(0, cfg.rows);
      if (JSON.stringify(L.rank) !== JSON.stringify(wantRank)) fail(`frame ${f} (race ${ri}): order ${L.rank.join(',')} != expected ${wantRank.join(',')}`);
      /* every label */
      const vals = {};
      for (const x of L.labels) {
        if (x.alpha > 0 && (x.x < -0.5 || x.x + x.w > 1920.5)) fail(`frame ${f}: ${x.kind} "${x.text}" runs off the frame (x ${x.x.toFixed(1)}, w ${x.w.toFixed(1)})`);
        if (x.kind === 'axis' && !/^\d{1,3}(,\d{3})*$/.test(x.text)) fail(`frame ${f}: axis label "${x.text}" is not a whole number`);
        if (x.kind !== 'value') continue;
        res.labels_checked++;
        const m = /^(\d{1,3}(?:,\d{3})*) (wins|win)$/.exec(x.text);
        if (!m) { fail(`frame ${f}: value label "${x.text}" is not "<whole number> win(s)"`); continue; }
        const n = +m[1].replace(/,/g, '');
        if ((n === 1) !== (m[2] === 'win')) fail(`frame ${f}: "${x.text}" has the wrong unit form`);
        if (exp.totals[x.id] !== n) fail(`frame ${f} (race ${ri}): ${x.id} shows ${n}, data says ${exp.totals[x.id]}`);
        if (!exp.order.slice(0, cfg.rows + 3).includes(x.id)) fail(`frame ${f}: ${x.id} labelled but not in the top ${cfg.rows + 3}`);
        vals[x.id] = n;
      }
      /* a driver in the target top N must carry its label as soon as its bar is on screen. A bar
         climbing from below the board is still sliding in (C2-2's eased rank glide) and fully
         faded for a few frames; that delay is measured, not failed. */
      const bar = Object.fromEntries(L.bars.map(b => [b.id, b]));
      for (const id of wantRank) {
        if (id in vals) { delete lag[id]; continue; }
        if (bar[id] && bar[id].alpha > 0) fail(`frame ${f} (race ${ri}): ${id} is on screen in the top ${cfg.rows} but has no value label`);
        else { lag[id] = (lag[id] || 0) + 1; res.entry_lag_max = Math.max(res.entry_lag_max, lag[id]); }
      }
      for (const id in vals) if (id in prevVals && vals[id] !== prevVals[id] && !info.start.includes(f)) fail(`frame ${f}: ${id} changed ${prevVals[id]}->${vals[id]} between events`);
      /* (7) entry visibility */
      for (const [id, e] of Object.entries(entering)) {
        const clear = bar[id] && bar[id].alpha >= CLEAR_ALPHA && L.labels.some(x => x.kind === 'name' && x.id === id) && (id in vals);
        const late = f - e.s;
        if (clear) { res.entry_frames_max = Math.max(res.entry_frames_max, late); delete entering[id]; }
        else if (late >= ENTRY_MAX_FRAMES || !exp.order.slice(0, cfg.rows).includes(id)) {
          fail(`race ${e.race}: ${id} entered the top ${cfg.rows} on frame ${e.s} but was not clearly visible within ${ENTRY_MAX_FRAMES} frames`);
          delete entering[id];
        }
      }
      /* (12) winner line */
      const wl = L.labels.filter(x => x.kind === 'winner');
      if (!WL && wl.length) fail(`frame ${f}: winner line drawn although winner_line is off`);
      if (WL && ri != null) {
        const want = winnerText(exp.credits, E.names);
        if (wl.length !== 1 || wl[0].text !== want) fail(`frame ${f} (race ${ri}): winner line "${wl.map(x => x.text).join(' | ')}" != "${want}"`);
        else res.winner_lines++;
      }
      /* (15) fixed-pitch digits on every number */
      for (const x of L.labels) if (TAB_KINDS.includes(x.kind)) { res.tab_labels++; if (!x.tab) fail(`frame ${f}: ${x.kind} "${x.text}" not drawn on fixed-pitch digits`); }
      /* (13) winner highlight */
      const isStart = k >= 0 && info.start[k] === f;
      const lit = L.bars.filter(b => b.hl > 0);
      if (!HLON && lit.length) fail(`frame ${f}: a bar is highlighted although highlight is off`);
      if (HLON) {
        const want = k >= 0 ? litOn(k) : [];
        for (const b of lit) if (!want.includes(b.id)) fail(`frame ${f} (race ${ri}): ${b.id} lit but not a credited winner on the board`);
        if (isStart) for (const id of want) if (!(bar[id] && bar[id].hl >= 0.999)) fail(`frame ${f} (race ${ri}): winner ${id} not fully lit on the first frame of the race`);
        for (const b of L.bars) {
          const was = prevHl[b.id] || 0;
          if (b.hl > was + 1e-6) {
            if (!(isStart && want.includes(b.id) && was === 0)) fail(`frame ${f} (race ${ri}): ${b.id} highlight rose ${was.toFixed(2)} -> ${b.hl.toFixed(2)} outside an onset (flicker)`);
            else if (k > 0 && litOn(k - 1).includes(b.id)) fail(`frame ${f} (race ${ri}): ${b.id} won the previous race too but its highlight went out and re-lit (flicker)`);
            else { res.onsets++; onsetFrames.push(f); }
          }
          if (k >= 0 && f - info.start[k] >= hlFrames && b.hl > 0 && !(k + 1 < info.start.length && litOn(k + 1).includes(b.id)))
            fail(`frame ${f}: ${b.id} still lit ${f - info.start[k]} frames into the race (fade is ${hlFrames})`);
        }
        for (const id in prevHl) if (!(id in bar)) delete prevHl[id];
        for (const b of L.bars) prevHl[b.id] = b.hl;
        while (onsetFrames.length && onsetFrames[0] <= f - cfg.fps) onsetFrames.shift();
        res.onsets_max_per_sec = Math.max(res.onsets_max_per_sec, onsetFrames.length);
        if (onsetFrames.length > MAX_ONSETS_PER_SEC) fail(`frame ${f}: ${onsetFrames.length} highlight onsets in the last second (max ${MAX_ONSETS_PER_SEC})`);
      }
      /* (18) flags */
      if (!FLAGON && L.flags.length) fail(`frame ${f}: flag drawn although flags are off`);
      if (FLAGON) {
        const drawnFlag = {};
        for (const fl of L.flags) {
          drawnFlag[fl.id] = fl; res.flags_checked++;
          if (fl.code !== natCode[fl.id]) fail(`frame ${f}: ${fl.id} drawn with flag "${fl.code}", nationality file says "${natCode[fl.id]}"`);
          const b = bar[fl.id];
          if (!b || Math.abs((fl.y + fl.h / 2) - (b.rect.y + b.rect.h / 2)) > 0.5 || Math.abs(fl.alpha - b.alpha) > 1e-6) fail(`frame ${f}: ${fl.id}'s flag is not on its row`);
          if (fl.x + fl.w > b.rect.x) fail(`frame ${f}: ${fl.id}'s flag runs into its bar`);
        }
        for (const b of L.bars) if (b.alpha > 0 && natCode[b.id] && !drawnFlag[b.id]) fail(`frame ${f}: ${b.id} is on screen without its flag`);
      }
      /* (19) event labels */
      const evl = L.labels.filter(x => x.kind === 'event');
      if (!EVON && evl.length) fail(`frame ${f}: event label drawn although event_label is off`);
      if (EVON) {
        const since = k >= 0 ? f - info.start[k] : null, cur = k >= 0 ? litOn(k) : [], now = {};
        for (const x of evl) {
          const vl = L.labels.find(v => v.kind === 'value' && v.id === x.id);
          if (!vl || x.x < vl.x + vl.w || Math.abs(x.y - vl.y) > 0.5) fail(`frame ${f}: event label of ${x.id} is not right after its value`);
          if (x.x + x.w > RIGHT_MARGIN + 0.01) fail(`frame ${f}: event label of ${x.id} "${x.text}" ends at x ${(x.x + x.w).toFixed(1)}, past the 64 px right margin`);
          if (res.event_right == null || x.x + x.w > res.event_right) { res.event_right = x.x + x.w; res.event_right_text = `${x.text} (${x.id}, frame ${f})`; }
          if (cur.includes(x.id)) {
            const want = '· ' + evText(inWindow[k]);
            if (x.text !== want) fail(`frame ${f} (race ${ri}): ${x.id} event label "${x.text}" != "${want}"`);
            if (Math.abs(x.alpha - bar[x.id].alpha) > 1e-6) fail(`frame ${f}: ${x.id} event label not at full strength`);
            res.event_labels++;
          } else if (k > 0 && litOn(k - 1).includes(x.id) && since < fadeFrames) {
            const want = '· ' + evText(inWindow[k - 1]);
            if (x.text !== want) fail(`frame ${f}: fading label of ${x.id} "${x.text}" != "${want}"`);
            if (prevEv[x.id] != null && x.alpha > prevEv[x.id] + 1e-6) fail(`frame ${f}: fading label of ${x.id} brightened`);
            res.event_fading++;
          } else fail(`frame ${f} (race ${ri}): unexpected event label "${x.text}" on ${x.id}`);
          now[x.id] = x.alpha;
        }
        for (const id of cur) if (bar[id] && bar[id].alpha > 0 && !evl.some(x => x.id === id)) fail(`frame ${f} (race ${ri}): winner ${id} is on the board without its event label`);
        prevEv = now;
      }
      /* (26) stats labels: "· <S> start(s) · <R>%" on every bar that carries a value */
      const stl = L.labels.filter(x => x.kind === 'stats');
      if (!STON && stl.length) fail(`frame ${f}: stats label drawn although stats_label is off`);
      if (STON) {
        const nowS = {};
        const expS = ri != null ? exp.starts : E.startsFor(before ? before.race_index : null);
        for (const vl of L.labels.filter(x => x.kind === 'value')) {
          if (vl.weight !== 700) fail(`frame ${f}: value label of ${vl.id} "${vl.text}" is weight ${vl.weight}, not bold (700)`);
          const mine = stl.filter(x => x.id === vl.id);
          if (mine.length !== 1) { fail(`frame ${f} (race ${ri}): ${vl.id} has ${mine.length} stats labels`); continue; }
          const x = mine[0], w = exp.totals[vl.id], sN = expS[vl.id];
          res.stats_labels++;
          if (!(sN > 0)) { fail(`frame ${f} (race ${ri}): ${vl.id} has no starts in starts.csv (NOT FOUND) but is on the board`); continue; }
          const want = statsWant(w, sN);
          if (x.text !== want) fail(`frame ${f} (race ${ri}): ${vl.id} stats "${x.text}" != "${want}" (${w} wins, ${sN} starts in the CSVs)`);
          const m = /^· (\d{1,3}(?:,\d{3})*) (starts?) · (\d{1,3}\.\d)%$/.exec(x.text);
          if (!m) fail(`frame ${f}: stats label "${x.text}" is not "· <n> start(s) · <r>%"`);
          else if ((+m[1].replace(/,/g, '') === 1) !== (m[2] === 'start')) fail(`frame ${f}: "${x.text}" has the wrong unit form`);
          if (x.weight !== 500) fail(`frame ${f}: stats label of ${x.id} is weight ${x.weight}, expected 500`);
          if (x.x < vl.x + vl.w || Math.abs(x.y - vl.y) > 0.5) fail(`frame ${f}: stats label of ${x.id} is not right after its value`);
          if (Math.abs(x.alpha - vl.alpha) > 1e-6) fail(`frame ${f}: stats label of ${x.id} not at its row's opacity`);
          if (x.x + x.w > RIGHT_MARGIN + 0.01) fail(`frame ${f}: stats label of ${x.id} "${x.text}" ends at x ${(x.x + x.w).toFixed(1)}, past the 64 px right margin`);
          if (res.stats_right == null || x.x + x.w > res.stats_right) { res.stats_right = x.x + x.w; res.stats_right_text = `${vl.text} ${x.text} (${x.id}, frame ${f})`; }
          if (x.id in prevStats && prevStats[x.id] !== x.text && !info.start.includes(f)) fail(`frame ${f}: ${x.id} stats changed "${prevStats[x.id]}" -> "${x.text}" between races`);
          nowS[x.id] = x.text;
        }
        for (const x of stl) if (!L.labels.some(v => v.kind === 'value' && v.id === x.id)) fail(`frame ${f}: stats label on ${x.id} without a value label`);
        for (const id in prevStats) if (!(id in nowS)) delete prevStats[id];
        Object.assign(prevStats, nowS);
        /* (27) no overlap with other rows (unless mid-overtake) or with the fixed text */
        const rowItems = id => [...L.bars.filter(b => b.id === id && b.alpha > 0).map(b => clipBarR(b.rect)).filter(r => r.b > r.t),
                                ...L.flags.filter(x => x.id === id && x.alpha > 0).map(x => ({ l: x.x, r: x.x + x.w, t: x.y, b: x.y + x.h })),
                                ...L.labels.filter(x => x.id === id && x.alpha > 0 && ['name', 'value', 'stats'].includes(x.kind)).map(x => clipRow(rectOf(x))).filter(r => r.b > r.t)];
        const fixed = L.labels.filter(x => x.alpha > 0 && (['title', 'subtitle', 'axis', 'footer'].includes(x.kind) || x.kind.startsWith('time_'))).map(rectOf);
        for (const x of stl.filter(x => x.alpha > 0)) {
          const R = clipRow(rectOf(x)), me = bar[x.id];
          if (R.b <= R.t) continue;                  // wholly below the board's clip: nothing drawn
          let skipped = false;
          const against = [...fixed];
          for (const b of L.bars) {
            if (b.alpha <= 0) continue;
            if (b.id === x.id) { against.push(...rowItems(b.id).filter(o => !(o.l === R.l && o.t === R.t))); continue; }
            if (Math.abs(b.y - me.y) < OVERTAKE_ROWS) { skipped = true; continue; }
            against.push(...rowItems(b.id));
          }
          res.stats_overlap_checked++; if (skipped) res.stats_overtake++;
          for (const o of against) {
            if (overlap(R, o)) fail(`frame ${f} (race ${ri}): stats label of ${x.id} "${x.text}" overlaps something at x ${o.l.toFixed(0)}-${o.r.toFixed(0)}, y ${o.t.toFixed(0)}-${o.b.toFixed(0)}`);
            const g = gap(R, o); if (res.stats_clear == null || g < res.stats_clear) res.stats_clear = g;
          }
        }
      }
      /* (20) the time block overlaps nothing; (21) nothing enters an overlay box */
      const clipBar = clipBarR;
      const others = [...L.bars.filter(b => b.alpha > 0).map(b => clipBar(b.rect)).filter(r => r.b > r.t),
                      ...L.flags.filter(x => x.alpha > 0).map(x => ({ l: x.x, r: x.x + x.w, t: x.y, b: x.y + x.h })),
                      ...L.labels.filter(x => x.alpha > 0 && ['name', 'value', 'event', 'stats', 'axis', 'title', 'subtitle', 'footer'].includes(x.kind)).map(rectOf)];
      const blockR = L.labels.filter(x => x.alpha > 0 && (x.kind.startsWith('time_') || x.kind === 'winner')).map(rectOf);
      if (['block', 'line'].includes(cfg.time_label.mode)) for (const a of blockR) for (const o of others) {
        if (overlap(a, o)) fail(`frame ${f} (race ${ri}): the time block overlaps something at x ${o.l.toFixed(0)}-${o.r.toFixed(0)}, y ${o.t.toFixed(0)}-${o.b.toFixed(0)}`);
        const g = gap(a, o); if (res.block_clear == null || g < res.block_clear) res.block_clear = g;
      }
      for (const ov of L.overlays) {
        const B = { l: ov.box.x, r: ov.box.x + ov.box.w, t: ov.box.y, b: ov.box.y + ov.box.h };
        const grid = L.grid.map(x => ({ l: x.x, r: x.x + x.w, t: x.y, b: x.y + x.h }));
        for (const o of others.concat(blockR, grid)) {
          if (overlap(B, o)) fail(`frame ${f}: something enters the ${ov.name} box at x ${o.l.toFixed(0)}-${o.r.toFixed(0)}, y ${o.t.toFixed(0)}-${o.b.toFixed(0)}`);
          const g = gap(B, o); if (res.overlay_clear == null || g < res.overlay_clear) res.overlay_clear = g;
        }
        if (ov.drawn) {
          res.overlays_drawn[ov.name] = ov.drawn;
          if (ov.drawn.x < B.l - 0.01 || ov.drawn.x + ov.drawn.w > B.r + 0.01 || ov.drawn.y < B.t - 0.01 || ov.drawn.y + ov.drawn.h > B.b + 0.01) fail(`frame ${f}: ${ov.name} drawn outside its box`);
        } else if (cfg.overlays) fail(`frame ${f}: ${ov.name} placeholder not drawn`);
        if (B.b > 1080 - YT_CONTROLS_PX) fail(`${ov.name} box reaches into the bottom ${YT_CONTROLS_PX} px (YouTube controls)`);
      }
      /* (14) the rank glide has settled on the last frame of a held race */
      if (k >= 0 && info.hold[k] && k + 1 < info.start.length && f === info.start[k + 1] - 1) {
        let worst = 0;
        for (const b of L.bars) if (b.alpha > 0 && wantRank.includes(b.id)) worst = Math.max(worst, Math.abs(b.y - wantRank.indexOf(b.id)));
        res.holds.push({ k, race: ri, settle: worst });
        if (worst >= HOLD_SETTLE_ROWS) fail(`race ${ri}: held, but a row is still ${worst.toFixed(3)} rows from its place on the last frame of the hold`);
      }
      /* (8) colours on screen */
      const shown = L.bars.filter(b => b.alpha > 0);
      const CO = COLOUR_OF[cfg.rows] = COLOUR_OF[cfg.rows] || {};
      for (const b of shown) {
        if (c.rtt002) { if (!(b.id in CO)) CO[b.id] = { colour: b.colour, where: c.name };
                        else if (CO[b.id].colour !== b.colour) fail(`frame ${f}: ${b.id} is ${b.colour} here but ${CO[b.id].colour} in ${CO[b.id].where}`); }
        for (const o of shown) if (o.id < b.id) {
          if (o.colour === b.colour) fail(`frame ${f}: ${o.id} and ${b.id} are both on screen in ${b.colour}`);
          else if (TIMELINE.deltaE(o.colour, b.colour) < minDE) fail(`frame ${f}: ${o.id} ${o.colour} and ${b.id} ${b.colour} are on screen together and only ${TIMELINE.deltaE(o.colour, b.colour).toFixed(1)} apart`);
        }
      }
      res.colour_frames++;
      prevVals = vals;
      /* fixture-specific */
      if (c.expect.max_visible != null && Object.keys(vals).length > c.expect.max_visible) fail(`frame ${f}: more than ${c.expect.max_visible} bars`);

      /* event boundaries: keep the frame, and read the value labels back from its pixels */
      if (bounds.has(f) && !c.light) {
        res.boundary_frames++;
        const k = info.start.indexOf(f) >= 0 ? 'first' : 'last';
        const png = path.join(out, `f${String(f).padStart(5, '0')}_race${ri}_${k}.png`);
        await el.screenshot({ path: png });
        if (HAS_OCR && k === 'first') {
          const busy = id => L.bars.some(b => b.id !== id && b.alpha > 0 && Math.abs(b.y - bar[id].y) < 1);
          for (const x of L.labels.filter(x => x.kind === 'value' && x.alpha >= 0.99)) {
            if (busy(x.id)) { res.ocr_skipped_overlap++; continue; }
            const crop = path.join(out, '_crop.png');
            await pg.screenshot({ path: crop, clip: { x: Math.max(0, x.x - 6), y: x.y - x.size * 0.95, width: x.w + 12, height: x.size * 1.35 } });
            const got = ocr(crop).replace(/[^0-9a-z ]/gi, '').replace(/\s+/g, ' ').trim();
            res.ocr_checked++;
            if (got.replace(/ /g, '').toLowerCase() !== x.text.replace(/ /g, '').toLowerCase()) res.ocr_mismatch.push(`frame ${f} ${x.id}: drew "${x.text}", OCR read "${got}"`);
          }
          /* (26) the stats labels read back too: the two numbers and the words, ignoring the dots */
          const nums = t => (t.match(/\d+(?:\.\d)?%?|starts?/gi) || []).join(' ').toLowerCase();
          for (const x of L.labels.filter(x => x.kind === 'stats' && x.alpha >= 0.99)) {
            if (busy(x.id)) { res.ocr_skipped_overlap++; continue; }
            const crop = path.join(out, '_crop.png');
            await pg.screenshot({ path: crop, clip: { x: Math.max(0, x.x - 6), y: x.y - x.size * 0.95, width: x.w + 12, height: x.size * 1.35 } });
            const got = ocr(crop);
            res.ocr_checked++; res.ocr_stats++;
            if (nums(got) !== nums(x.text)) res.ocr_mismatch.push(`frame ${f} ${x.id}: drew "${x.text}", OCR read "${got}"`);
          }
          fs.rmSync(path.join(out, '_crop.png'), { force: true });
        }
      }
    }
    for (const [id, e] of Object.entries(entering)) fail(`race ${e.race}: ${id} entered but was never clearly visible`);
    if (cfg.time_label.mode === 'line') res.notes.push(`date line: ${res.date_lines} frames checked; ${res.offboard_races} of ${inWindow.length} races (${(100 * res.offboard_races / inWindow.length).toFixed(0)}%) were won by a driver not on the ${cfg.rows}-row board after the race, and their ${res.date_lines_offboard} frames still name the race`);
    if (res.stats_right != null) res.notes.push(`stats labels: ${res.stats_labels} checked (three numbers each against starts.csv and win_credits.csv); furthest right edge x ${res.stats_right.toFixed(1)} (limit ${RIGHT_MARGIN}), "${res.stats_right_text}"; overlap check on ${res.stats_overlap_checked} labels, ${res.stats_overtake} of them with a row mid-overtake (those rows skipped), closest item ${res.stats_clear == null ? 'n/a' : res.stats_clear.toFixed(1) + ' px'}`);
    if (res.event_right != null) res.notes.push(`furthest right edge of any event label: x ${res.event_right.toFixed(1)} (limit ${RIGHT_MARGIN}), "${res.event_right_text}"`);
    const wantRaces = inWindow.map(r => r.race_index);
    if (JSON.stringify(seenRaces) !== JSON.stringify(wantRaces)) fail(`races shown ${seenRaces.length} != races in window ${wantRaces.length}`);
    for (const [ri, want] of Object.entries((c.expect.after_race) || {}))
      if (JSON.stringify(E.after[ri].order) !== JSON.stringify(want)) fail(`fixture.json: after race ${ri} expected ${want}, data order ${E.after[ri].order}`);
    if (c.expect.same_frame_step) {
      const r = String(c.expect.same_frame_step), s = info.start[inWindow.findIndex(x => x.race_index === r)];
      const ids = E.races.find(x => x.race_index === r).winner_driver_ids.split(';');
      const a = await pg.evaluate(t => { drawAt(t); return window.__LABELS; }, (s - 1) / cfg.fps);
      const b = await pg.evaluate(t => { drawAt(t); return window.__LABELS; }, s / cfg.fps);
      for (const id of ids) {
        const va = a.find(x => x.kind === 'value' && x.id === id), vb = b.find(x => x.kind === 'value' && x.id === id);
        const na = va ? parseInt(va.text) : 0, nb = parseInt(vb.text);
        if (nb !== na + 1) fail(`shared drive: ${id} did not step by one on frame ${s} (${na} -> ${nb})`);
      }
      res.notes.push(`shared drive at race ${r}: ${ids.join(' and ')} both step on frame ${s}`);
    }
    if (c.expect.enters) {
      const inTop = Object.values(E.after).filter(a => wantRaces.includes(a.race.race_index)).map(a => a.order.slice(0, cfg.rows).includes(c.expect.enters));
      const entered = inTop.indexOf(true), left = inTop.lastIndexOf(true);
      if (entered < 0 || left === inTop.length - 1) fail(`${c.expect.enters} did not both enter and leave the top ${cfg.rows}`);
      else res.notes.push(`${c.expect.enters} enters the top ${cfg.rows} at race ${entered + 1} and leaves after race ${left + 1}`);
    }
    if (c.expect.quiet_from_race) {
      const ks = info.kind.slice(c.expect.quiet_from_race - 1, c.expect.quiet_to_race);
      if (ks.some(k => k !== 'quiet')) fail(`quiet stretch races ${c.expect.quiet_from_race}-${c.expect.quiet_to_race} not all paced quiet: ${ks.join(',')}`);
      const base = inWindow.length * cfg.pacing.sec_per_event;
      res.notes.push(`quiet stretch paced at ${cfg.pacing.mult.quiet}x; events take ${((info.raceFrames / cfg.fps) - cfg.pacing.lead_in_sec - cfg.pacing.end_hold_sec).toFixed(2)} s against ${base.toFixed(2)} s unpaced`);
    }
    /* (10) milestones, read from the drawn labels on the first frame of the race */
    for (const m of (c.expect.milestones || [])) {
      const k = inWindow.findIndex(r => r.season === m.season && r.grand_prix === m.grand_prix);
      if (k < 0) { fail(`milestone: ${m.season} ${m.grand_prix} is not in the passage`); continue; }
      const idOf = nm => Object.keys(E.names).find(id => E.names[id] === nm);
      const got = await pg.evaluate(t => { drawAt(t); return { labels: window.__LABELS, rank: window.__RANK }; }, info.start[k] / cfg.fps);
      const shows = nm => { const x = got.labels.find(l => l.kind === 'value' && l.id === idOf(nm)); return x ? parseInt(x.text.replace(/,/g, '')) : null; };
      const pos = nm => got.rank.indexOf(idOf(nm)) + 1;
      const said = m.show.map(([nm, n]) => `${nm} ${shows(nm)} (P${pos(nm)})`).join(', ');
      if (m.show.some(([nm, n]) => shows(nm) !== n)) fail(`milestone ${m.season} ${m.grand_prix}: expected ${m.show.map(x => x.join(' ')).join(', ')}, drawn ${said}`);
      if (m.order && m.order.some((nm, i) => i > 0 && pos(m.order[i - 1]) >= pos(nm))) fail(`milestone ${m.season} ${m.grand_prix}: order should be ${m.order.join(' ahead of ')}, drawn ${said}`);
      res.notes.push(`${m.season} ${m.grand_prix} (frame ${info.start[k]}): ${said} — ${m.note}`);
    }
    /* (11) no closing card; the final board holds for end_hold_sec */
    if (cfg.outro_sec === 0) {
      const last = info.raceFrames - 1;
      const out = await pg.evaluate(t => { drawAt(t); return window.__LABELS; }, last / cfg.fps);
      if (out.some(x => x.kind.startsWith('outro_'))) fail('closing card drawn although outro_sec is 0');
      const hold = (info.raceFrames - info.start[info.start.length - 1]) / cfg.fps;
      const total = rtt.frameTotals(cfg, data).total;
      if (cfg.pacing.final_board_sec == null) {
        if (hold < cfg.pacing.end_hold_sec) fail(`final board holds ${hold.toFixed(2)} s, less than ${cfg.pacing.end_hold_sec} s`);
        res.notes.push(`no closing card; final board on screen ${hold.toFixed(2)} s (last race slot + ${cfg.pacing.end_hold_sec} s hold)`);
      }
      res.notes.push(`FRAME_COUNT_ONLY total ${total} frames = ${(total / cfg.fps).toFixed(1)} s`);
      res.total_frames = total;
    }
    /* (16) the opening: the intro card draws the config title; without a card (intro_sec 0) the
       very first frame is the board, with the title and the opening totals on it */
    if (cfg.intro_sec > 0) {
      const intro = await pg.evaluate(t => { drawIntro(t); return window.__LABELS; }, 1.5);
      if (!intro.some(x => x.kind === 'intro_title' && x.text === cfg.title)) fail('intro card does not carry the config title');
    } else {
      if (rtt.frameTotals(cfg, data).intro !== 0) fail('intro_sec 0 but the driver plans intro frames');
      const first = await pg.evaluate(() => { drawAt(0); return window.__LABELS; });
      const vals = first.filter(x => x.kind === 'value' && x.alpha > 0).length;
      if (!first.some(x => x.kind === 'title' && x.text === cfg.title) || !vals) fail(`first frame is not the board with the title (title ${first.some(x => x.kind === 'title')}, ${vals} values)`);
      else res.notes.push(`opening: no title card; frame 0 is the board with the title "${cfg.title}" and ${vals} value labels (the totals before ${inWindow[0].season} ${inWindow[0].grand_prix}); first race lands at ${(info.start[0] / cfg.fps).toFixed(2)} s`);
    }
    if (cfg.pacing.final_board_sec != null) {
      const on = (info.raceFrames - info.start[info.start.length - 1]) / cfg.fps;
      if (Math.abs(on - cfg.pacing.final_board_sec) > 1e-9) fail(`final board on screen ${on} s, config says ${cfg.pacing.final_board_sec} s`);
      else res.notes.push(`final board on screen exactly ${on.toFixed(2)} s from the first frame of the last race, no closing card`);
    }
    /* (14) record holds: exactly the listed moments, and every other beat inside the bounds */
    const slot = k => ((k + 1 < info.start.length ? info.start[k + 1] : null) - info.start[k]);
    const heldRaces = inWindow.filter((r, k) => info.hold[k]).map(r => r.race_index);
    if (c.rtt002 && cfg.record_hold) {
      const types = cfg.record_hold.types || ['BECOMES_JOINT', 'BECOMES_SOLE'];
      const moments = recordProgression(c.dir).filter(r => inWindow.some(w => w.race_date === r.race_date));
      const want = cfg.record_hold.enabled ? [...new Set(moments.filter(r => types.includes(r.event)).map(r => inWindow.find(w => w.race_date === r.race_date).race_index))] : [];
      if (JSON.stringify(heldRaces) !== JSON.stringify(want)) fail(`held races ${heldRaces.join(',')} != record moments ${want.join(',')}`);
      for (const r of moments.filter(r => types.includes(r.event))) {
        const k = inWindow.findIndex(w => w.race_date === r.race_date), h = res.holds.find(x => x.k === k);
        res.notes.push(`record moment ${r.race_date} ${r.season} ${r.grand_prix}: ${r.driver_name} ${r.career_wins} wins, ${r.event} (record holders after: ${r.record_holders_after}) — ${info.hold[k] ? `held ${(slot(k) / cfg.fps).toFixed(2)} s, frames ${info.start[k]}-${info.start[k + 1] - 1}; rows settled to within ${h ? h.settle.toFixed(3) : '?'} row on its last frame` : 'NOT held'}`);
      }
      res.notes.push(`not held (EXTENDS_SOLE in the window): ${moments.filter(r => !types.includes(r.event)).length} races`);
    }
    const beatLo = cfg.pacing.bounds[0] * cfg.pacing.sec_per_event * cfg.fps, beatHi = cfg.pacing.bounds[1] * cfg.pacing.sec_per_event * cfg.fps;
    let slotMin = Infinity, slotMax = 0;
    for (let k = 0; k + 1 < info.start.length; k++) {
      if (info.hold[k]) { if (Math.abs(slot(k) - cfg.record_hold.sec * cfg.fps) > 1) fail(`race ${inWindow[k].race_index}: held ${slot(k)} frames, config says ${cfg.record_hold.sec} s`); continue; }
      slotMin = Math.min(slotMin, slot(k)); slotMax = Math.max(slotMax, slot(k));
      if (slot(k) < beatLo - 1 || slot(k) > beatHi + 1) fail(`race ${inWindow[k].race_index}: beat ${slot(k)} frames is outside ${cfg.pacing.bounds} x ${cfg.pacing.sec_per_event} s`);
    }
    res.slot_range = slotMin <= slotMax ? `${(slotMin / cfg.fps).toFixed(2)}-${(slotMax / cfg.fps).toFixed(2)} s` : 'n/a';
  } finally { await br.close(); }
  res.pass = res.failures.length === 0;
  return res;
}

async function main() {
  const only = process.argv.slice(2);
  const cases = [];
  for (const name of fs.readdirSync(FIX).filter(n => fs.statSync(path.join(FIX, n)).isDirectory()).sort()) {
    const fx = JSON.parse(fs.readFileSync(path.join(FIX, name, 'fixture.json'), 'utf8'));
    cases.push({ name, dir: path.join(FIX, name), overrides: fx.overrides, expect: fx.expect });
  }
  /* IQ-05b: the shared drive again with the winner line and the highlight on (both credited
     drivers named on the line and lit on the same frame) */
  const sd = JSON.parse(fs.readFileSync(path.join(FIX, 'shared_drive', 'fixture.json'), 'utf8'));
  cases.push({ name: 'shared_drive_winner_highlight', dir: path.join(FIX, 'shared_drive'),
               overrides: Object.assign({}, sd.overrides, { winner_line: { enabled: true }, highlight: { enabled: true, sec: 0.4, mix: 0.3, glow: 16 } }), expect: sd.expect });
  /* IQ-05c/d: the pilot's board features on the (fictional) shared drive with the pilot's 20-row
     geometry: flags from a fictional nationality file (one driver NOT FOUND), dated event labels on
     both credited drivers, the date line, and the overlay boxes. Round 4: the winner line is off
     here (it belongs under the big time block, which the date line replaces; the player refuses the
     two together); it stays covered by shared_drive_winner_highlight. */
  const pilot = rtt.loadConfig('config_pilot_2014_2021_top20.json');
  cases.push({ name: 'shared_drive_round4', dir: path.join(FIX, 'shared_drive'),
               overrides: Object.assign({}, sd.overrides, { rows: 20, board: pilot.board, namescale: pilot.namescale, barend: pilot.barend,
                 highlight: { enabled: true, sec: 0.4, mix: 0.3, glow: 16 }, overlay_gap: pilot.overlay_gap,
                 flags: Object.assign({}, pilot.flags, { enabled: true, csv: path.join(FIX, 'shared_drive', 'driver_nationality.csv') }),
                 event_label: Object.assign({}, pilot.event_label, { enabled: true }), time_label: Object.assign({}, pilot.time_label, { months: pilot.time_label.months }), overlays: pilot.overlays }),
               expect: sd.expect });
  /* IQ-05e: the round-5 pilot's board (stats label instead of the event label, round-3 bars) on
     the fictional shared drive, whose starts.csv has a driver skipping a race, a driver on 1 win
     from 1 start (100.0%) and starts before a first win */
  cases.push({ name: 'shared_drive_round5', dir: path.join(FIX, 'shared_drive'),
               overrides: Object.assign({}, sd.overrides, { rows: 20, board: pilot.board, namescale: pilot.namescale, barend: pilot.barend,
                 highlight: { enabled: true, sec: 0.4, mix: 0.3, glow: 16 }, overlay_gap: pilot.overlay_gap,
                 flags: Object.assign({}, pilot.flags, { enabled: true, csv: path.join(FIX, 'shared_drive', 'driver_nationality.csv') }),
                 event_label: pilot.event_label, stats_label: pilot.stats_label,
                 time_label: Object.assign({}, pilot.time_label, { months: pilot.time_label.months }), overlays: pilot.overlays }),
               expect: sd.expect });
  const RTT002 = path.join(ROOT, 'data', 'rtt-002');
  cases.push({ name: 'rtt002_1984_1989', dir: RTT002, rtt002: true,
               window: { from: '1984-01-01', to: '1989-12-31' }, overrides: {}, expect: {} });
  const milestones = [
    { season: '2020', grand_prix: 'Eifel Grand Prix', show: [['Lewis Hamilton', 91], ['Michael Schumacher', 91]], order: ['Michael Schumacher', 'Lewis Hamilton'],
      note: 'Hamilton equals Schumacher; Schumacher stays ahead on the tie rule (he reached 91 first)' },
    { season: '2020', grand_prix: 'Portuguese Grand Prix', show: [['Lewis Hamilton', 92], ['Michael Schumacher', 91]], order: ['Lewis Hamilton', 'Michael Schumacher'],
      note: 'Hamilton passes Schumacher' }];
  cases.push({ name: 'rtt002_2014_2021_A_top20', dir: RTT002, rtt002: true, config: 'config_pilot_2014_2021_top20.json', expect: { milestones } });
  /* the whole video, every frame, draw-call checks only (no PNGs or OCR: 16,000 frames) */
  cases.push({ name: 'rtt002_full_run', dir: RTT002, rtt002: true, light: true, overrides: {}, expect: {} });
  const run = only.length ? cases.filter(c => only.includes(c.name)) : cases;

  const results = [];
  if (!only.length || only.includes('colour_rule_full_dataset')) results.push(colourRuleFullDataset(RTT002, 'config.json', 'colour_rule_full_dataset'));
  if (!only.length || only.includes('colour_rule_full_dataset_top20')) results.push(colourRuleFullDataset(RTT002, 'config_pilot_2014_2021_top20.json', 'colour_rule_full_dataset_top20'));
  if (!only.length || only.includes('record_moments_full_dataset')) results.push(recordMomentsFullDataset(RTT002));
  if (!only.length || only.includes('win_rate_rounding')) results.push(winRateRounding());
  for (const c of run) {
    const t0 = Date.now();
    const r = await runCase(c);
    r.seconds = ((Date.now() - t0) / 1000).toFixed(1);
    results.push(r);
    console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}: ${r.events} events, ${r.frames} frames, ${r.labels_checked} value labels, ${r.winner_lines} winner lines, ${r.onsets} highlight onsets (max ${r.onsets_max_per_sec}/s), ${r.boundary_frames} boundary PNGs, OCR ${r.ocr_checked - r.ocr_mismatch.length}/${r.ocr_checked}, ${r.seconds} s`);
    for (const m of r.failures) console.log('   - ' + m);
    for (const m of r.ocr_mismatch.slice(0, 10)) console.log('   ocr: ' + m);
  }
  for (const full of results.filter(r => r.name.startsWith('colour_rule_full_dataset'))) {
    const drawn = COLOUR_OF[full.rows] || {};
    for (const [id, v] of Object.entries(drawn))
      if (full.colour_of[id] !== v.colour) { full.failures.push(`${id} drawn ${v.colour} in ${v.where} but assigned ${full.colour_of[id]}`); full.pass = false; }
    full.notes.push(`${Object.keys(drawn).length} drivers drawn in the RTT-002 cases run with a ${full.rows}-row board; each drawn in its assigned colour in every such case`);
    console.log(`${full.pass ? 'PASS' : 'FAIL'}  ${full.name}: ${full.events} races, ${full.drivers} drivers on the board, up to ${full.max_together} together, ${full.colours_used} colours, closest pair ${full.closest.toFixed(1)}`);
    for (const m of full.failures) console.log('   - ' + m);
  }
  for (const r of results.filter(r => r.name === 'record_moments_full_dataset' || r.name === 'win_rate_rounding')) {
    console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}: ${r.notes[0]}`);
    for (const m of r.failures) console.log('   - ' + m);
  }
  fs.mkdirSync(OUTDIR, { recursive: true });
  fs.writeFileSync(path.join(OUTDIR, 'results.json'), JSON.stringify(results, null, 1));
  if (!only.length) writeReport(results);
  process.exit(results.every(r => r.pass) ? 0 : 1);
}

function writeReport(results) {
  const pw = require(require.resolve('playwright/package.json', { paths: [KITDIR] })).version;
  const L = [];
  const cases = results.filter(r => r.frames != null), cols = results.filter(r => r.name.startsWith('colour_rule_full_dataset'));
  const rec = results.find(r => r.name === 'record_moments_full_dataset');
  L.push('# Player test results (IQ-05 round 5)', '');
  L.push('Written by `node tests/player/run_tests.js` (all cases). Frames are 1920x1080 (preview width), drawn headless in Playwright ' + pw + ' Chromium, every race frame in order.');
  L.push('OCR: ' + (HAS_OCR ? spawnSync('tesseract', ['--version'], { encoding: 'utf8' }).stdout.split('\n')[0] + ' on every value label (and stats label, where on) of the first frame of every race.' : 'NOT AVAILABLE (tesseract not installed); draw-call checks only.'), '');
  L.push(`Overall: ${results.filter(r => r.pass).length}/${results.length} PASS.`, '');
  L.push('| Case | Result | Config | Rows | Races | Frames | Race length | Value labels checked | Winner lines checked | Highlight onsets (most in 1 s) | Numbers checked on fixed-pitch digits | Beats outside holds | Boundary frames | OCR read back (skipped: overlapping rows) | Board entries | Slowest entry (frames to clearly visible) | Colour-checked frames | Name size | Pacing (rank / visible / quiet) | Event labels checked (fading) | Event label: furthest right edge | Flags checked | Date lines checked (winner off the board) | Date line: closest item | Overlay boxes: closest item | Stats labels checked | Stats label: furthest right edge | Stats overlap: labels checked (row mid-overtake) | Stats label: closest item | Adapter output SHA-256 |');
  L.push('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|');
  for (const r of cases)
    L.push(`| ${r.name} | ${r.pass ? 'PASS' : 'FAIL'} | \`${r.config}\` | ${r.rows} | ${r.events} | ${r.frames} | ${r.race_sec.toFixed(2)} s | ${r.labels_checked} | ${r.winner_lines || 'off'} | ${r.onsets ? `${r.onsets} (${r.onsets_max_per_sec})` : 'off'} | ${r.tab_labels} | ${r.slot_range} | ${r.boundary_frames || 'not saved'} | ${r.boundary_frames ? `${r.ocr_checked - r.ocr_mismatch.length}/${r.ocr_checked} (${r.ocr_skipped_overlap})` : 'not run'} | ${r.entries} | ${r.entry_frames_max} | ${r.colour_frames} | ${r.name_px}px${r.name_truncated ? ' (truncated)' : ''} | ${r.pacing.rank_change} / ${r.pacing.visible_change} / ${r.pacing.quiet} | ${r.event_labels ? `${r.event_labels} (${r.event_fading})` : 'off'} | ${r.event_right != null ? 'x ' + r.event_right.toFixed(0) : 'n/a'} | ${r.flags_checked || 'off'} | ${r.date_lines ? `${r.date_lines} (${r.date_lines_offboard})` : 'n/a'} | ${r.block_clear != null ? r.block_clear.toFixed(0) + ' px' : 'n/a'} | ${r.overlay_clear != null ? r.overlay_clear.toFixed(0) + ' px' : 'n/a'} | ${r.stats_labels || 'off'} | ${r.stats_right != null ? 'x ' + r.stats_right.toFixed(0) : 'n/a'} | ${r.stats_overlap_checked ? `${r.stats_overlap_checked} (${r.stats_overtake})` : 'n/a'} | ${r.stats_clear != null ? r.stats_clear.toFixed(0) + ' px' : 'n/a'} | \`${r.adapter_sha256.slice(0, 16)}…\` |`);
  L.push('');
  L.push(`Entry rule: a driver joining the visible board must be clearly visible (row opacity at least ${CLEAR_ALPHA}, name and value label drawn) within ${ENTRY_MAX_FRAMES} frames of the first frame of that race, i.e. on frame +0 to +${ENTRY_MAX_FRAMES - 1}. The column gives the slowest entry in the case (+N frames).`);
  L.push('Colour rule on frames: on every frame drawn, no two bars on screen (opacity above 0) share a colour or are closer than CIEDE2000 18, and every driver is drawn in the same colour in every RTT-002 case with the same board size.');
  L.push(`Winner highlight (where on): on the first frame of every race exactly the credited winners whose bars are on the board are lit, nothing else is ever lit, a highlight only rises from fully off on the first frame of a race that driver won (a repeat winner stays lit, so never flickers), at most ${MAX_ONSETS_PER_SEC} onsets in any second, and each fades out within highlight.sec.`);
  L.push('Round 5 (where on): stats label = on every frame every bar with a value label carries "· <S> start(s) · <R>%" right after it, S from starts.csv and R = wins / starts recomputed here (one decimal, rounded half up), the win count bold and the stats regular, numbers changing only on the first frame of a race, ending inside the 64 px right margin; it overlaps no bar, flag, name, value or stats label of a row that is not mid-overtake (within ' + OVERTAKE_ROWS + ' row; counted in brackets) and no title, subtitle, axis number, footer or date line (row labels measured as drawn, inside the board clip at y 150-1034, as bars are); OCR also reads every stats label back at race boundaries.');
  L.push('Round 4 (where on): date line = on every frame exactly one line "<D Month YYYY> · <GP>" for the race on screen, from races.csv, including races whose winner is off the board (frames of such races in brackets), overlapping nothing ("closest item" = the smallest gap on any frame to a bar, flag, name, value, event label, axis number, title, subtitle or footer); event labels now read "· <GP> · <D Month YYYY>" and must end inside the 64 px right margin (x ' + RIGHT_MARGIN + '; "furthest right edge" = the largest on any frame); overlay boxes = also no axis grid line inside a box.');
  L.push('Round 3 (where on): flags = every flag drawn equals the driver\'s flag_code in the nationality file and sits on its row; event labels = on every frame each winner on the board shows "· <GP>" from races.csv right after its value, and the only other event labels are the previous race\'s, fading; time block = on every frame no overlap with any bar, flag, name, value, event label, axis number, title or footer ("closest item" = the smallest gap on any frame); overlay boxes = nothing enters the reserved logo and car boxes on any frame, placeholders drawn inside them, and the boxes stay out of the bottom ' + YT_CONTROLS_PX + ' px.');
  L.push(`Record holds (where on): the held races are exactly the BECOMES_JOINT / BECOMES_SOLE rows of data/rtt-002/record_progression.csv inside the window; on the last frame of each hold every row is within ${HOLD_SETTLE_ROWS} row of its place; every other beat is within 0.8-1.4 x sec_per_event (to the nearest frame).`, '');
  for (const x of results.filter(r => r.name === 'win_rate_rounding')) {
    L.push(`**win_rate_rounding — ${x.pass ? 'PASS' : 'FAIL'}**`);
    for (const n of x.notes) L.push('- ' + n);
    for (const n of x.failures) L.push('- FAIL: ' + n);
    L.push('');
  }
  if (rec) {
    L.push(`**record_moments_full_dataset — ${rec.pass ? 'PASS' : 'FAIL'}**`);
    for (const n of rec.notes) L.push('- ' + n);
    for (const n of rec.failures) L.push('- FAIL: ' + n);
    L.push('');
  }
  for (const col of cols) {
    L.push(`**${col.name} — ${col.pass ? 'PASS' : 'FAIL'}** (\`${col.config}\`, ${col.rows}-row board; every race of the full RTT-002 dataset, boards computed from win_credits.csv alone)`);
    for (const n of col.notes) L.push('- ' + n);
    for (const n of col.failures) L.push('- FAIL: ' + n);
    L.push('', `| Colour (as drawn) | Drivers, in the order they first reach the top ${col.rows} |`, '|---|---|');
    for (const [c, names] of Object.entries(col.by_colour)) L.push(`| \`${c}\` | ${names.join(', ')} |`);
    L.push('');
  }
  for (const r of cases) {
    if (!r.notes.length && !r.failures.length && !r.ocr_mismatch.length) continue;
    L.push('**' + r.name + '**');
    for (const n of r.notes) L.push('- ' + n);
    for (const n of r.failures) L.push('- FAIL: ' + n);
    for (const n of r.ocr_mismatch) L.push('- OCR differs: ' + n);
    L.push('');
  }
  L.push('The draw-call checks are the pass/fail gate. OCR is an independent read of the pixels: any mismatch is listed above, not hidden (' + cases.reduce((n, r) => n + r.ocr_mismatch.length, 0) + ' in this run). Labels on rows that overlap mid-overtake are not OCR-read (count in brackets). The full run is checked on every frame by draw calls only (no PNGs, no OCR).');
  fs.writeFileSync(path.join(__dirname, 'RESULTS.md'), L.join('\n') + '\n');
}

main().catch(e => { console.error(e); process.exit(2); });
