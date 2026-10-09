#!/usr/bin/env python3
"""RTT-101 Premier League net transfer spend: deterministic data build (IQ-15, phase 1).

Usage: python3 scripts/build_rtt101_dataset.py [DATA_DIR] [REPORT_PATH]
       (defaults: data/rtt-101 and reports/RTT-101_data_report.md)

Inputs (all committed, public):
  data/rtt-101/source/club_aliases.csv        club identity (one club_id per club; Wimbledon FC is not AFC Wimbledon/MK Dons)
  data/rtt-101/source/wiki_season_tables.csv  PL tables per season (Wikipedia pointers, grade C)
  data/rtt-101/source/wiki_window_rows.csv    per-window transfer lists 2002-2026 (pointers, grade C)
  data/rtt-101/source/wiki_club_season_rows.csv  1992-2002 club-season transfer tables (pointers, grade C), if present
  data/rtt-101/source/wiki_windows.csv        window dates as the lists' lead sentences state them (pointers)
  data/rtt-101/source/leads_evidence.csv      research leads (UNVERIFIED) extracted from the private files, public facts only
  data/rtt-101/source/runner_checks.csv       scripted source checks done on a GitHub runner (VERIFIED / not), if present
  data/rtt-101/source/fixed_dates.csv         dates the build cannot take from the pages above, each with its source
  data/rtt-101/cpi.csv, data/rtt-101/fx.csv   ONS D7BT; Bank of England rates (DEC-239)
Outputs: clubs.csv, pl_membership.csv, seasons.csv, transfers.csv, fee_evidence.csv, sources.csv, club_ledger.csv,
         club_season.csv, series_monthly.csv, moments.csv (if leads exist), conflicts.csv, tier1_list.csv, coverage.csv,
         window_totals.csv, CHECKS.md, manifest.json, and the report.
Rules: reference/metric_contract_RTT-101.md. Never averages, interpolates or forecasts; never uses Transfermarkt.
Everything in phase 1 is an UNVERIFIED preview unless a row says VERIFIED.
"""
import bisect, csv, datetime as dt, hashlib, json, os, random, re, sys, unicodedata, urllib.parse
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rtt101_lib as L  # noqa: E402

DATA = sys.argv[1] if len(sys.argv) > 1 else "data/rtt-101"
REPORT = sys.argv[2] if len(sys.argv) > 2 else "reports/RTT-101_data_report.md"
SRC = os.path.join(DATA, "source")
FREEZE = "2026-09-01"           # close of the summer 2026 window, 23:00 BST (DEC-237 (b), V-09)
START_MONTH_END = "1992-05-31"
GRADE_RANK = {"A": 0, "B": 1, "C": 2, "D": 3}
ERAS = [("1992-93", "2001-02", "1992-2002 (no window lists)"), ("2002-03", "2006-07", "2002-2007"),
        ("2007-08", "2011-12", "2007-2012"), ("2012-13", "2016-17", "2012-2017"), ("2017-18", "2021-22", "2017-2022"),
        ("2022-23", "2026-27", "2022-2026")]
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                       "september", "october", "november", "december"], 1)}


def rd(name, base=SRC):
    p = os.path.join(base, name)
    if not os.path.exists(p):
        return []
    return list(csv.DictReader(open(p, encoding="utf-8")))


def wr(name, rows, cols):
    p = os.path.join(DATA, name)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def season_label(w):  # "1992–93" -> "1992-93"; "1999–2000" -> "1999-00"
    a, b = w.replace("–", "-").split("-")
    return f"{a}-{b[-2:]}"


def iso_from_text(t):
    m = re.search(r"(\d{1,2}) ([A-Za-z]+) (\d{4})", t)
    if m and m.group(2).lower() in MONTHS:
        return f"{m.group(3)}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    return ""


def next_day(d):
    return (dt.date.fromisoformat(d) + dt.timedelta(days=1)).isoformat()


def month_end(d):
    y, m = int(d[:4]), int(d[5:7])
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - dt.timedelta(days=1)).isoformat()


def money(x):
    return f"{x:.2f}" if x is not None else ""


# ---------------------------------------------------------------- stage B: clubs, membership, seasons
aliases = rd("club_aliases.csv")
club_ids = [a["club_id"] for a in aliases]
season_rows = rd("wiki_season_tables.csv")
fixed = {r["key"]: r for r in rd("fixed_dates.csv")}

seasons = []
by_label = {}
for r in season_rows:
    lab = season_label(r["season"])
    if lab not in by_label:
        a = r["season_dates_infobox"]
        parts = re.split(r"\s+[–-]\s+", a)
        first = iso_from_text(parts[0] + (" " + parts[-1][-4:] if not re.search(r"\d{4}", parts[0]) else "")) if parts else ""
        last = iso_from_text(parts[-1]) if parts else ""
        by_label[lab] = {"season": lab, "first_matchday": first, "last_matchday": last, "dates_source": f"Wikipedia '{r['page']}' infobox (pointer, C)", "dates_revid": r["revid"]}
        seasons.append(by_label[lab])
seasons.sort(key=lambda s: s["season"])
prev_last = fixed.get("last_matchday_1991-92", {})
for i, s in enumerate(seasons):
    if i == 0:
        s["attribution_start"] = next_day(prev_last["date"]) if prev_last else ""
        s["attribution_start_basis"] = (f"day after the last 1991-92 First Division matchday ({prev_last.get('date', 'NOT FOUND')}; {prev_last.get('source', '')})")
    else:
        s["attribution_start"] = next_day(seasons[i - 1]["last_matchday"])
        s["attribution_start_basis"] = f"day after the last {seasons[i - 1]['season']} PL matchday"
    s["attribution_end"] = s["last_matchday"] if s["season"] != "2026-27" else FREEZE
    s["attribution_end_basis"] = "last PL matchday" if s["season"] != "2026-27" else "freeze: close of the summer 2026 window, 1 Sep 2026 23:00 BST (V-09)"
    s["window_system"] = ("no transfer windows: trading until 31 March (V-08)" if s["season"] < "2002-03"
                          else "summer and January windows (V-08)")
wins = {r["window"]: r for r in rd("wiki_windows.csv")}
for s in seasons:
    y = int(s["season"][:4])
    sw, jw = wins.get(f"summer {y}"), wins.get(f"winter {y}–{(y + 1) % 100:02d}")
    for key, w, lo, hi in (("summer", sw, f"{y}-04-01", f"{y}-10-31"), ("january", jw, f"{y}-08-01", f"{y + 1}-03-31")):
        ok = w and w["open_date"] and w["close_date"] and lo <= w["open_date"] < w["close_date"] <= hi and s["season"] >= "2002-03"
        s[f"{key}_window_open"] = w["open_date"] if ok else ""
        s[f"{key}_window_close"] = w["close_date"] if ok else ""
        s[f"{key}_window_source"] = (f"Wikipedia '{w['page']}' lead (pointer, C; UNVERIFIED)" if ok else
                                     ("not applicable" if s["season"] < "2002-03" else "NOT FOUND in the list's lead"))
    if s["season"] == "2026-27":
        s["summer_window_open"], s["summer_window_close"] = "2026-06-15", "2026-09-01 23:00 BST"
        s["summer_window_source"] = "premierleague.com/en/transfers/2026-27/summer (V-09, VERIFIED by Claude in Cowork 7 Oct 2026)"
        s["january_window_open"] = s["january_window_close"] = ""
        s["january_window_source"] = "after the freeze (not in this build)"
season_by_label = {s["season"]: s for s in seasons}
att_starts = [s["attribution_start"] for s in seasons]


def season_of(date):
    """Season whose attribution window contains date (None if before 1992-93 or after the freeze)."""
    if not date or date > FREEZE or not att_starts[0] or date < att_starts[0]:
        return None
    i = bisect.bisect_right(att_starts, date) - 1
    s = seasons[i]
    return s["season"] if date <= s["attribution_end"] else None


membership = []
in_pl = set()
for r in season_rows:
    lab = season_label(r["season"])
    in_pl.add((r["club_id"], lab))
    membership.append({"season": lab, "club_id": r["club_id"], "club_name_on_page": r["club_article"],
                       "final_position": r["position"], "relegated_per_table": r["relegated_flag"] or ("" if lab == "2026-27" else "no"),
                       "source": f"Wikipedia '{r['page']}' league table", "revid": r["revid"], "grade": "C",
                       "crosscheck": "matches research file part03b (see CHECKS.md)"})
membership.sort(key=lambda r: (r["season"], int(r["final_position"] or 99), r["club_id"]))
labels = sorted({m["season"] for m in membership})
for m in membership:  # relegated = in the PL this season and not the next (derived; 2026-27 not finished)
    nxt = labels[labels.index(m["season"]) + 1] if m["season"] != labels[-1] else None
    m["relegated"] = "" if nxt is None else ("no" if (m["club_id"], nxt) in in_pl else "yes")
seasons_of_club = defaultdict(list)
for c, lab in sorted(in_pl, key=lambda x: x[1]):
    seasons_of_club[c].append(lab)
clubs = []
for a in aliases:
    ss = seasons_of_club.get(a["club_id"], [])
    clubs.append({"club_id": a["club_id"], "display_name": a["display_name"], "other_names": a["other_names"],
                  "wikipedia_title": a["wikipedia_title"], "pl_seasons_to_2026_27": len(ss),
                  "first_pl_season": ss[0] if ss else "", "last_pl_season": ss[-1] if ss else "",
                  "colour_key": "", "logo_ref": ""})

# ---------------------------------------------------------------- reference: CPI and FX
cpi = {r["month"]: float(r["cpi_d7bt_2015_100"]) for r in rd("cpi.csv", DATA)}
cpi_base_month = max(m for m in cpi if m <= FREEZE[:7])
cpi_base = cpi[cpi_base_month]
fx_daily, fx_month = {}, {}
for r in rd("fx.csv", DATA):
    if r["kind"] == "daily spot":
        fx_daily[(r["currency"], r["date"])] = (float(r["units_per_gbp"]), r["series_code"], r["date"])
    else:
        fx_month[(r["currency"], r["date"][:7])] = (float(r["units_per_gbp"]), r["series_code"], r["date"])


def convert(amount, cur, date):
    """GBP value at the BoE daily spot for the date; monthly average if no daily (contract §5). None if no rate."""
    if cur == "GBP":
        return amount, None
    k = fx_daily.get((cur, date)) or fx_month.get((cur, date[:7]))
    if not k:
        return None, None
    rate, code, rdate = k
    return round(amount / rate, 2), {"fx_rate": rate, "fx_date": rdate, "fx_series": code}


# ---------------------------------------------------------------- stage C: transfer skeleton and evidence
def kind_of(fee_text):
    t = fee_text.lower()
    if re.search(r"end of loan|loan return|returned from loan|recalled", t):
        return "loan_return"
    if "loan" in t:
        return "loan"
    if re.search(r"swap|exchange|part[- ]exchange|in exchange", t):
        return "part_exchange"
    if re.search(r"\bfree\b|released|bosman|end of contract", t):
        return "free"
    if re.search(r"undisclosed|not disclosed|nominal", t):  # a nominal fee is a fee of unstated size, not a free transfer
        return "undisclosed"
    if re.search(r"tribunal|compensation", t):
        return "compensation"
    return "permanent"


def pname(s):
    s = L.norm(re.sub(r"\(.*?\)", "", s or ""))
    return s


def same_player(a, b):
    """Full name equal, or same surname and same first initial, or a one-word name equal to the other's first or last word."""
    pa, pb = pname(a), pname(b)
    if not pa or not pb:
        return False
    if pa == pb:
        return True
    ta, tb = pa.split(), pb.split()
    if len(ta) == 1 or len(tb) == 1:
        one, other = (ta, tb) if len(ta) == 1 else (tb, ta)
        return one[0] in (other[0], other[-1])
    if ta[-1] != tb[-1] or ta[0][0] != tb[0][0]:
        return False
    fa, fb = (NICK.get(x, x) for x in (ta[0].rstrip("."), tb[0].rstrip(".")))
    # an initial matches any first name with that letter; two written-out first names must agree in their first three letters or in their
    # consonants (Andy/Andrew, Franck/Frank, Alexei/Aleksey, Amdy/Amady yes; Dean/David no)
    skel = lambda x: re.sub(r"[aeiouy]", "", x)  # noqa: E731
    return len(fa) <= 1 or len(fb) <= 1 or fa[:3] == fb[:3] or skel(fa) == skel(fb)


NICK = {"mike": "michael", "mick": "michael", "bill": "william", "billy": "william", "bob": "robert", "bobby": "robert", "rob": "robert",
        "robbie": "robert", "jim": "james", "jimmy": "james", "tony": "anthony", "tom": "thomas", "tommy": "thomas", "joe": "joseph",
        "nick": "nicholas", "nicky": "nicholas", "ted": "edward", "eddie": "edward", "ed": "edward", "harry": "henry", "jack": "john",
        "johnny": "john", "sasha": "aleksandr", "pepe": "jose"}


transfers, evidence, sources = [], [], {}


def source_id(url, publisher, grade, kind):
    key = url or f"{kind}:{publisher}"
    sid = "S" + sha(key)[:10]
    if sid not in sources:
        sources[sid] = {"source_id": sid, "url": url, "publisher": publisher, "grade": grade, "kind": kind}
    return sid


wiki_rows = rd("wiki_window_rows.csv") + rd("wiki_club_season_rows.csv")
seen = {}
near = defaultdict(list)  # (player, from, to, loan) -> transfers, for the same deal listed on both clubs' pages
for r in wiki_rows:
    date = r["date"]
    k = kind_of(r["fee_text"])
    if k == "loan_return" or not date:
        continue
    basis = "Wikipedia list date (pointer)"
    if re.fullmatch(r"\d{4}-\d{2}", date):
        date, basis = month_end(date + "-01"), "month only on the Wikipedia page: month end (contract §2)"
    key = (pname(r["player"]), r["from_club_id"] or L.norm(r["from_name"]), r["to_club_id"] or L.norm(r["to_name"]), date, k == "loan")
    nk = key[:3] + (k == "loan",)
    hit = None
    if key not in seen:
        for t0 in near[nk]:
            if abs((dt.date.fromisoformat(t0["date"]) - dt.date.fromisoformat(date)).days) <= 60:
                hit = t0
                break
    if key in seen or hit:
        t = seen.get(key) or hit
    else:
        tid = "T" + sha("|".join(map(str, key)))[:10]
        t = {"transfer_id": tid, "player": r["player"], "player_article": r.get("player_article", ""), "from_club": r["from_club_id"] or r["from_name"],
             "to_club": r["to_club_id"] or r["to_name"], "from_club_id": r["from_club_id"], "to_club_id": r["to_club_id"],
             "type": k, "date": date, "date_basis": basis, "found_via": f"Wikipedia: {r['page']} (rev {r['revid']})",
             "parent_transfer_id": "", "_ev": []}
        seen[key] = t
        near[nk].append(t)
        transfers.append(t)
    wsid = source_id(f"https://en.wikipedia.org/w/index.php?oldid={r['revid']}", "Wikipedia: " + r["page"], "C", "wikipedia_pointer")
    p = L.parse_fee(r["fee_text"])
    t["_ev"].append({"origin": "wikipedia_list", "source_id": wsid, "grade": "C", "fee_text": r["fee_text"], "parsed": p,
                     "quote": r["fee_text"][:120], "url": f"https://en.wikipedia.org/w/index.php?oldid={r['revid']}",
                     "archive_url": "", "date": date, "cite_urls": r["cite_urls"], "cite_publishers": r["cite_publishers"],
                     "tm_only": r["citation_only_transfermarkt"] == "yes"})

# research leads (UNVERIFIED): match to the skeleton by player, PL club and date; otherwise a new row (found via research)
idx = defaultdict(list)
for t in transfers:
    for tok in set(pname(t["player"]).split(" ")):
        idx[tok].append(t)  # every word of the name, so "Juninho" finds "Juninho Paulista"
lead_rows = rd("leads_evidence.csv")


LEAD_DATES = {(L.norm(r["player"]), L.norm(r["from_club"]), L.norm(r["to_club"])): r for r in rd("lead_dates.csv")}


def lead_date(r):
    d = r["date"].strip()
    fix = LEAD_DATES.get((L.norm(r["player"]), L.norm(r["from_club"]), L.norm(r["to_club"])))
    if fix and not re.match(r"\d{4}-\d{2}", d):
        d0 = fix["date"]
        return (month_end(d0 + "-01") if len(d0) == 7 else d0), fix["date_basis"]
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return d, "research lead date (UNVERIFIED)"
    if re.fullmatch(r"\d{4}-\d{2}", d):
        return month_end(d + "-01"), "month only: month end (contract §2)"
    return "", "NOT FOUND"


group_new = {}
unmatched = []
by_tid = {t["transfer_id"]: t for t in transfers}
for r in lead_rows:
    if r["lead_section"] not in ("A", "B", "C", "G", "S"):
        continue
    d, basis = lead_date(r)
    best, far = None, None
    pool = []
    if r["lead_section"] == "S":
        # source rounds (DEC-275): the row names our deal, so it attaches to that transfer directly (no name or date matching)
        best, fid, toid = by_tid.get(r["transfer_ref"]), None, None
        if best is None:
            unmatched.append({"lead_id": r["lead_id"], "section": "S", "date": r["date"], "player": r["player"], "from_club": r["from_club"],
                              "to_club": r["to_club"], "fee_as_reported": r["fee_as_reported"], "grade": r["grade"], "url": r["url"],
                              "reason": f"deal's transfer {r['transfer_ref']} not in the build"})
            continue
    else:
        fid, toid = L.club_id(r["from_club"]), L.club_id(r["to_club"])
        if not (fid or toid):
            continue
        for tok in sorted(set(pname(r["player"]).split(" "))):  # sorted: the match must not depend on set order (build is deterministic)
            pool += [x for x in idx.get(tok, []) if x not in pool]
    pool.sort(key=lambda x: (x["date"], x["transfer_id"]))
    for t in pool:
        if not same_player(t["player"], r["player"]):
            continue
        if (fid and t["from_club_id"] != fid and toid and t["to_club_id"] != toid):
            continue
        if not ((fid and t["from_club_id"] == fid) or (toid and t["to_club_id"] == toid)):
            continue
        if t["type"] == "loan" and "loan" not in r["fee_as_reported"].lower():
            continue
        gap = abs((dt.date.fromisoformat(d) - dt.date.fromisoformat(t["date"])).days) if d and t["date"] else 0
        if gap <= 120:
            best = t
            break
        same_from = (t["from_club_id"] == fid) if fid else (L.norm(t["from_club"])[:6] == L.norm(r["from_club"])[:6] != "")
        same_to = (t["to_club_id"] == toid) if toid else (L.norm(t["to_club"])[:6] == L.norm(r["to_club"])[:6] != "")
        if gap <= 400 and (fid or toid) and same_from and same_to and far is None:
            far = t  # same player, same two clubs, within 400 days: the same deal reported at another stage
    note = ""
    if best is None and far is not None:
        best, note = far, "research lead dated more than 120 days from the transfer date (same player and clubs)"
    if best is None:
        early = bool(d) and (season_of(d) or "9999") < ("2007-08" if r["lead_section"] == "G" else "2002-03")
        if not early:
            unmatched.append({"lead_id": r["lead_id"], "section": r["lead_section"], "date": r["date"], "player": r["player"],
                              "from_club": r["from_club"], "to_club": r["to_club"], "fee_as_reported": r["fee_as_reported"],
                              "grade": r["grade"], "url": r["url"],
                              "reason": "no matching transfer in the finding list" + ("" if early else " (2002 or later: the Wikipedia lists are the finding list; review by hand)")})
            continue
        gk = r["transfer_ref"] if r["lead_section"] == "B" and r["transfer_ref"] else (pname(r["player"]), fid or L.norm(r["from_club"]), toid or L.norm(r["to_club"]), (d or "")[:4])
        if gk in group_new:
            best = group_new[gk]
            if d and (not best["date"] or (best["date_basis"].startswith("month") and basis.startswith("research"))):
                best["date"], best["date_basis"] = d, basis
        else:
            best = {"transfer_id": "T" + sha("lead|" + json.dumps(gk, ensure_ascii=False))[:10], "player": r["player"], "player_article": "",
                    "from_club": fid or r["from_club"], "to_club": toid or r["to_club"], "from_club_id": fid or "",
                    "to_club_id": toid or "", "type": {"part_exchange": "part_exchange", "loan": "loan"}.get(r.get("lead_type", ""), "permanent"),
                    "date": d, "date_basis": basis,
                    "found_via": ("ChatGPT gap list (DEC-264)" if r["lead_section"] == "G" else
                                  "research lead (private ChatGPT files; not in the Wikipedia lists)"), "parent_transfer_id": "", "_ev": []}
            group_new[gk] = best
            transfers.append(best)
            by_tid[best["transfer_id"]] = best  # a source-round row may name a transfer the gap list created earlier in this loop
            for tok in set(pname(r["player"]).split(" ")):
                idx[tok].append(best)
    if any(e["url"] == r["url"] and e["fee_text"] == r["fee_as_reported"] for e in best["_ev"]):
        continue  # the same source and figure already attached (research sections repeat each other)
    grade = r["grade"] if r["grade"] in GRADE_RANK else "D"
    sid = source_id(r["url"], r["publisher"], grade, "press_or_club")
    parsed = L.parse_fee(r["fee_as_reported"])
    gp = L.parse_fee(r.get("guaranteed_part", "")) if r.get("guaranteed_part", "").strip().upper() not in ("", "NOT FOUND") else None
    if (gp and gp["amount"] and gp["currency"] and "up_to" not in gp["qualifiers"]
            and (parsed["amount"] is None or gp["currency"] != parsed["currency"] or gp["amount"] >= 0.5 * parsed["amount"])):
        # a "guaranteed part" under half the headline is usually a first instalment, which is not the whole guaranteed fee
        parsed = dict(parsed, amount=gp["amount"], currency=gp["currency"], qualifiers=[q for q in parsed["qualifiers"] if q != "up_to"] + ["guaranteed_part"])
    best["_ev"].append({"origin": "research_lead", "source_id": sid, "grade": grade, "fee_text": r["fee_as_reported"],
                        "parsed": parsed, "quote": r["quote"], "url": r["url"],
                        "archive_url": r["archive_url"] if r["archive_url"].startswith("http") else "", "date": d,
                        "lead_id": r["lead_id"], "lead_section": r["lead_section"], "record_type": r["record_type"],
                        "issue_type": r["issue_type"], "grade_note": r["grade_note"], "note": note, "lead_published": r.get("published", "")})

review = {r["check_id"]: r for r in rd("review_decisions.csv")}  # Claude's reading of each Tier 1 quote (phase 2)
art_cites = defaultdict(list)
for r in rd("player_article_citations.csv"):
    art_cites[r["transfer_id"]].append(r["url"])
# an "amount" rejection names the figure and, through its check ID ("...-3000GBP"), its currency: £30m rejected does not block €30m
# (IQ-15h: Curtis Jones's guaranteed €30m and Mayenda's €22m had been blocked by rejections of £30m and £22m totals)
_rej_cur = defaultdict(set)
for r in review.values():
    if r["decision"] == "reject" and r.get("scope") == "amount":
        _m = re.search(r"\d(GBP|EUR|USD)$", r["check_id"])
        _rej_cur[(r["transfer_id"], r.get("amount", ""))].add(_m.group(1) if _m else None)
amount_rejects = set(_rej_cur)


def amount_rejected(tid, amount, cur):
    curs = _rej_cur.get((tid, amount))
    return bool(curs) and (None in curs or cur in curs)
checks = defaultdict(list)
for c in rd("runner_checks.csv"):
    rv = review.get(c["check_id"])
    if not rv and amount_rejected(c["transfer_id"], c["amount"], c.get("currency") or "GBP"):
        rv = {"decision": "reject", "note": "the same figure was rejected for this deal on review"}
    if rv and rv["decision"] == "reject":
        c = dict(c, status="UNVERIFIED", result="REJECTED on review: " + rv["note"])
    elif rv:
        c = dict(c, reviewed=rv["decision"] + (": " + rv["note"] if rv["note"] else ""))
    checks[c["url"]].append(c)
SB_ROW = re.compile(r"(\d\d) (\w{3}), (\d\d)\s+(?:\d\d \w{3}, \d\d\s+)?$")
SB_MON = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def soccerbase_row_ok(c, tdate):
    """A Soccerbase career table lists every move; its figure counts only from the row whose joining date is this transfer's
    (within 62 days). A "Totals" line or another row's figure is not this deal's fee."""
    if "soccerbase.com" not in c["url"]:
        return True
    i = c["quote"].find(c["needle"])
    m = SB_ROW.search(c["quote"][:i]) if i >= 0 else None
    if not m or not tdate or m.group(2).lower() not in SB_MON:
        return False
    y = int(m.group(3))
    try:
        joined = dt.date(y + (1900 if y >= 50 else 2000), SB_MON[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        return False
    return abs((joined - dt.date.fromisoformat(tdate)).days) <= 62


# a figure the runner found at the cited source becomes its own evidence row (VERIFIED, graded by publisher). A check is
# attached only to a transfer that cites that page itself and whose player's surname is the one the runner looked for.
for t in transfers:
    own = {}
    for e in t["_ev"]:
        for u in ([e["url"]] if e["origin"] == "research_lead" else e.get("cite_urls", "").split()):
            own.setdefault(u, e)
    for u in art_cites.get(t["transfer_id"], []):
        own.setdefault(u, None)  # cited by the player's own Wikipedia article in a sentence about this move (pointer)
    sn = pname(t["player"]).split(" ")[-1] if t["player"] else ""
    amounts = {money(e["parsed"]["amount"]) for e in t["_ev"] if e["parsed"]["amount"] is not None}
    for u, e0 in list(own.items()):
        for c in checks.get(u, []):
            if c["status"] != "VERIFIED" or not sn or L.norm(c.get("near", "")) != sn or c["amount"] not in amounts:
                continue
            if amount_rejected(t["transfer_id"], c["amount"], c.get("currency") or "GBP"):
                continue  # Claude rejected this figure for this deal on review (whatever page states it)
            if not soccerbase_row_ok(c, t["date"]):
                continue  # another row of the player's Soccerbase table, or its career total
            if e0 and e0["origin"] == "research_lead" and e0["url"] == c["url"] and money(e0["parsed"]["amount"]) == c["amount"]:
                e0["checked"] = c
                continue
            if any(x.get("checked", {}).get("check_id") == c["check_id"] for x in t["_ev"]):
                continue
            sid = source_id(c["url"], urllib.parse.urlparse(c["url"]).netloc, c["grade_by_publisher"], "press_or_club")
            t["_ev"].append({"origin": "runner_check", "source_id": sid, "grade": c["grade_by_publisher"],
                             "fee_text": c["needle"], "parsed": {"amount": float(c["amount"]), "currency": c["currency"], "qualifiers": [], "kind": "fee"},
                             "quote": c["quote"], "url": c["url"], "archive_url": "", "date": t["date"], "checked": c,
                             "note": ("figure found at the source cited by the Wikipedia row" if e0 else
                                      "figure found at a source cited by the player's Wikipedia article") + " (GitHub runner)"})

# reported figures for undisclosed deals, found at a cited source and read by Claude (DEC-257); only "accept" rows are used
for r in rd("reported_fees.csv"):
    if r["decision"] != "accept":
        continue
    for t in transfers:
        if r.get("transfer_id") and t["transfer_id"] != r["transfer_id"]:
            continue  # the figure belongs to the deal it was found for, not to the same player's other moves on that page
        if pname(t["player"]).split(" ")[-1] != L.norm(r["near"]) or not (r["url"] in art_cites.get(t["transfer_id"], []) or any(
                r["url"] in ([e["url"]] if e["origin"] != "wikipedia_list" else e.get("cite_urls", "").split()) for e in t["_ev"])):
            continue
        sid = source_id(r["url"], urllib.parse.urlparse(r["url"]).netloc, r["grade_by_publisher"], "press_or_club")
        t["_ev"].append({"origin": "reported_search", "source_id": sid, "grade": r["grade_by_publisher"], "fee_text": r["money"],
                         "parsed": {"amount": float(r["amount"]), "currency": r["currency"],
                                    "qualifiers": ["guaranteed_part"] if r["candidate_id"].startswith("G-") else ["reported"], "kind": "fee"},
                         "quote": r["quote"], "url": r["url"], "archive_url": "", "date": t["date"],
                         "checked": {"check_id": r["candidate_id"], "quote": r["quote"], "retrieved": r["retrieved"], "reviewed": "accept: " + r["note"]},
                         "note": ("guaranteed fee stated on the same page as a total including add-ons, read at the source (DEC-237 (e))"
                                  if r["candidate_id"].startswith("G-") else "reported figure for an undisclosed fee, read at the source (DEC-257)")})

# publication date of each page (runner) or from the URL itself; used for "earliest contemporary report" (brief §7)
page_dates = {r["url"]: r["published"][:10] for r in rd("page_dates.csv")}
MON3 = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def pubdate(url):
    if url in page_dates and re.match(r"\d{4}-\d{2}-\d{2}", page_dates[url]):
        return page_dates[url]
    m = re.search(r"/(\d{4})/([a-z]{3})/(\d{1,2})/", url)
    if m and m.group(2) in MON3:
        return f"{m.group(1)}-{MON3[m.group(2)]:02d}-{int(m.group(3)):02d}"
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})/?$", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return ""


# a figure described as a total including add-ons is not the guaranteed fee (DEC-237 (e)) and not a rival version
TOTAL_RX = re.compile(r"(with|including|incl\.?|inclusive of|plus)\s+(all\s+)?(the\s+)?(add-ons|add ons|bonuses|extras)|in total|overall|total (fee|package|cost|deal)|package", re.I)


# deal structures (IQ-15d): combined fees, part-exchanges, conditional sums, loans and completion dates read at source and set out
# in data/rtt-101/source/deal_structure.csv (one row per transfer, with its source, quote and the rule applied). Dates first.
DS = rd("deal_structure.csv")
for r in DS:
    t = by_tid.get(r["transfer_id"])
    if t and r.get("date"):
        t["date"], t["date_basis"] = r["date"], r["date_basis"]

NO_DEC404 = os.environ.get("RTT101_NO_DEC404") == "1"  # only for listing what DEC-404 changes (report section 12)
# a completion report: "completed", "joined", "signed" (strong) or "capture", "clinched", "the £Xm signing" (weaker: such headlines can
# come before the formal completion); a strong report beats a weaker one, and either beats a bid, an agreed or an expected figure
COMPLETED_RX = re.compile(r"(?<!to )(?<!will )(?<!would )(?<!could )(?<!may )(?<!might )\b(signed|signs|completed|completes|completion|joined|joins|"
                          r"has moved|moved to|moved from|unveiled|finally left|rubber-stamped|registered|finalised)\b", re.I)
WEAK_DONE_RX = re.compile(r"(?<!to )(?<!will )(?<!would )(?<!could )(?<!may )(?<!might )\b(sealed|secured?|snapped up|landed|lands|clinched|"
                          r"arrived|bought|capture|recruit|debut)\b", re.I)
# "the new £1.3m signing", "Boro's pounds 3.5m signing from Benfica": a signing already made ("proposed £3.4m signing" is not)
SIGNING_RX = re.compile(r"(?:\bnew\s+(?:(?:£|pounds\s?)[\d.,]+\s*(?:m|mn|million|k)?\s+)?|(?<!proposed )(?<!planned )(?<!potential )(?<!prospective )(?<!would-be )(?:£|\bpounds\s?)[\d.,]+\s*(?:m|mn|million|k)?\s+)signing\b(?!\s+(?:target|bid|attempt))", re.I)
# "since his £1.3m move from Columbus Crew": a move already made (IQ-15i, Friedel); "a possible £5m move" is not
MOVE_RX = re.compile(r"\b(?:his|her)\s+(?:£|pounds\s?)[\d.,]+\s*(?:m|mn|million|k)?\s+(?:move|switch|transfer)\b", re.I)
PRECONTRACT_RX = re.compile(r"\b(bid|bids|offer|offered|agreed|agree|agreement|expected|expects|likely|poised|set to|close to|talks|negotiat\w*|"
                            r"proposed|will cost|would cost|hoping|hopes|target|tipped|about to|on the verge|prospective|rumou?r\w*|"
                            r"is to|are to|will pay|will receive|set for|in line)\b", re.I)


# wording that the deal was still to be done, even where a completion word appears ("the £3m capture of Domi is apparently imminent")
STILL_PRE_RX = re.compile(r"\b(imminent|on the verge|about to (?:complete|sign|join)|close to (?:completing|signing|joining)|poised to|"
                          r"set to (?:complete|sign|join)|yet to (?:complete|sign|agree|be completed|be finalised)|awaiting|subject to|pending|proposed)\b", re.I)


def completion_kind(e, surname=""):
    """'completed' if the report says this player's deal was done; 'pre' if it reports a bid, an agreed fee or an expected figure;
    else ''. A completion word counts only within 120 characters of the player's surname when the text names him (a list sentence
    can describe a neighbouring deal)."""
    txt = f"{e.get('fee_text') or ''} {e.get('quote') or ''} {(e.get('checked') or {}).get('quote') or ''}"  # with the page's own sentence
    low = "".join((unicodedata.normalize("NFKD", c) or " ")[0] for c in txt.lower())  # same length as txt, accents dropped
    spots = [m.start() for m in re.finditer(re.escape(surname), low)] if surname else []
    def near(m):
        return not spots or any(abs(m.start() - p) <= 120 for p in spots)
    if STILL_PRE_RX.search(txt):
        return "pre"
    if any(near(m) for m in COMPLETED_RX.finditer(txt)):
        return "completed"
    if any(near(m) for rx in (WEAK_DONE_RX, SIGNING_RX, MOVE_RX) for m in rx.finditer(txt)):
        return "completed_weak"
    if PRECONTRACT_RX.search(txt):
        return "pre"
    return ""


# canonical fee per transfer
for t in transfers:
    t["season_attributed"] = season_of(t["date"]) or ""
    cands = []
    wiki_undisclosed = any(e["origin"] == "wikipedia_list" and kind_of(e["fee_text"]) == "undisclosed" for e in t["_ev"])
    # DEC-408 (a): a club, league or quality-press (A/B) report that names the player and calls the fee undisclosed or nominal
    # has the same effect as a Wikipedia "undisclosed" row: only an A/B figure can then be the fee (DEC-237 (g))
    sn0 = pname(t["player"]).split(" ")[-1] if t["player"] else ""
    press_undisclosed = any(e["origin"] != "wikipedia_list" and e["grade"] in ("A", "B") and e["parsed"]["kind"] == "undisclosed"
                            and sn0 and sn0 in L.norm(e.get("quote") or "") for e in t["_ev"])
    wiki_undisclosed = wiki_undisclosed or press_undisclosed
    for i, e in enumerate(t["_ev"]):
        e["evidence_id"] = f"{t['transfer_id']}-E{i + 1:02d}"
        p = e["parsed"]
        e["amount"], e["currency"] = p["amount"], p["currency"]
        e["qualifiers"] = ";".join(p["qualifiers"])
        e["gbp"], e["fx"] = (None, None)
        if p["amount"] is not None and e.get("tm_only"):
            e["amount"] = e["gbp"] = None
            e["note"] = "fee NOT FOUND: the list's only citation is Transfermarkt (DEC-236, DEC-250 (c)); not stored"
            e["fee_text"] = "(not stored: Transfermarkt citation)"
            e["quote"] = ""
        elif p["amount"] is not None:
            e["gbp"], e["fx"] = convert(p["amount"], p["currency"], t["date"] or e["date"] or "")
        ck = e.get("checked")
        # DEC-274 (Luke): a figure is confirmed at source by a club or league (A), the quality press (B) or a Soccerbase row (C, labelled as a
        # database source); a figure seen only on a weaker source (any other C, or D) is not enough
        strong = e["grade"] in ("A", "B") or (e["grade"] == "C" and "soccerbase.com" in (e.get("url") or ""))
        e["status"] = "VERIFIED" if ck and strong else "UNVERIFIED"
        if ck and not strong:
            e["note"] = ((e.get("note") or "") + "; " if e.get("note") else "") + \
                f"seen at its source, but a grade {e['grade']} source other than Soccerbase does not confirm a fee (DEC-274)"
        if ck:
            # keep a research lead's own sentence from that page when it names the player (the runner's snippet can open on a
            # neighbouring deal in a list); otherwise the runner's snippet is the quote
            sn_ = pname(t["player"]).split(" ")[-1] if t["player"] else ""
            if not (e["origin"] == "research_lead" and sn_ and sn_ in L.norm(e.get("quote") or "")):
                e["quote"] = ck["quote"]
            e["retrieved"] = ck["retrieved"]
        e["total_incl_addons"] = bool(TOTAL_RX.search(e["fee_text"] or "")) and "guaranteed_part" not in p["qualifiers"]
        if re.search(r"sell-on|sell on", e["fee_text"] or "", re.I):
            e["total_incl_addons"] = True  # a sell-on payment to a former club is not this deal's fee (DEC-238 handles it)
        e["figure_rejected"] = (e["gbp"] is not None and amount_rejected(t["transfer_id"], money(e["gbp"]), "GBP")) or (
            e["amount"] is not None and amount_rejected(t["transfer_id"], money(e["amount"]), e["currency"] or "GBP"))
        usable = (e["gbp"] is not None and "up_to" not in p["qualifiers"] and "combined" not in p["qualifiers"]
                  and not e["total_incl_addons"] and not e["figure_rejected"]
                  and not (wiki_undisclosed and e["grade"] in ("C", "D")))  # undisclosed: only an A/B reported figure (DEC-237 (g))
        if usable:
            e["published"] = pubdate(e["url"]) or e.get("lead_published", "")
            cands.append((0 if e["status"] == "VERIFIED" else 1, GRADE_RANK.get(e["grade"], 3), 0 if e["currency"] == "GBP" else 1,
                          e["published"] or "9999", i, e))
    kinds = [kind_of(e["fee_text"]) for e in t["_ev"] if e["origin"] == "wikipedia_list"]
    if cands:
        cands.sort(key=lambda x: x[:5])
        # DEC-404 (Luke, 8 Oct): among the best figures (same confirmation status and grade), a report that the deal was completed
        # beats earlier reports of bids, agreed fees or expected figures; the earliest report is used only when none says completed
        # (a figure within 2% of the one already chosen, or 5% when one of the two is converted from another currency, is the same fee
        # reported twice: no change)
        top = [c for c in cands if c[:2] == cands[0][:2]]
        kinds_ = [completion_kind(c[5], sn0) for c in top]
        pick = None
        if kinds_[0] != "completed":
            pick = next((c for c, k in zip(top, kinds_) if k == "completed"), None)
            if pick is None and kinds_[0] != "completed_weak":
                pick = next((c for c, k in zip(top, kinds_) if k == "completed_weak"), None)
        if (pick is not None and not NO_DEC404
                and abs(pick[5]["gbp"] - top[0][5]["gbp"]) > (0.02 if pick[5]["currency"] == top[0][5]["currency"] else 0.05) * max(top[0][5]["gbp"], 1)):
            cands.remove(pick)
            cands.insert(0, pick)
            pick[5]["dec404"] = True
        e = cands[0][5]
        t["canonical"] = e
        t["fee_gbp"] = e["gbp"]
        t["original_amount"], t["currency"] = e["amount"], e["currency"]
        t["fx_rate"] = e["fx"]["fx_rate"] if e["fx"] else ""
        t["fx_date"] = e["fx"]["fx_date"] if e["fx"] else ""
        t["fx_series"] = e["fx"]["fx_series"] if e["fx"] else ""
        rep = ("reported" in e["parsed"]["qualifiers"] or "undisclosed" in e["fee_text"].lower() or bool(e.get("grade_note"))
               or (e["origin"] == "reported_search" and "guaranteed_part" not in e["parsed"]["qualifiers"]))
        t["fee_status"] = ("free" if e["gbp"] == 0 else "reported" if rep else "stated")
        if e["gbp"] == 0 and t["type"] not in ("loan",):
            t["type"] = "free"
        t["grade"] = e["grade"]
        t["canonical_source_id"] = e["source_id"]
        t["status"] = e["status"]
        if t["type"] in ("undisclosed", "free") and e["gbp"] > 0:
            t["type"] = "permanent"
    else:
        t["canonical"] = None
        t["fee_gbp"] = 0.0
        t["original_amount"] = t["currency"] = t["fx_rate"] = t["fx_date"] = t["fx_series"] = ""
        if any(e.get("tm_only") for e in t["_ev"]):
            t["fee_status"] = "NOT FOUND (only citation is Transfermarkt); counted £0"
        elif any(e.get("figure_rejected") for e in t["_ev"]) and not any(e["gbp"] for e in t["_ev"] if not e.get("figure_rejected")
                                                                           and e["origin"] != "wikipedia_list"):
            t["fee_status"] = "only a maximum, a total with add-ons or a combined fee found: counted £0 (DEC-276)"
        elif press_undisclosed:
            t["fee_status"] = "undisclosed, no figure: counted £0"
            if t["type"] in ("free", "permanent"):
                t["type"] = "undisclosed"
        elif t["type"] == "free" or "free" in kinds:
            t["fee_status"] = "free"
        elif t["type"] == "loan":
            t["fee_status"] = "loan, no fee stated"
        elif t["type"] == "undisclosed" or "undisclosed" in kinds:
            t["fee_status"] = "undisclosed, no figure: counted £0"
        else:
            t["fee_status"] = "NOT FOUND: counted £0"
        t["grade"] = min((e["grade"] for e in t["_ev"]), key=lambda g: GRADE_RANK.get(g, 3)) if t["_ev"] else ""
        t["canonical_source_id"] = ""
        t["status"] = "UNVERIFIED"
    amts = sorted({round(e["gbp"]) for e in t["_ev"] if e["gbp"] is not None})
    t["fee_versions_gbp"] = ";".join(str(a) for a in amts)

# deal structures: the fee set by the row's rule replaces the canonical figure (no split is invented: a combined fee sits on one
# transfer of the pair, the partner counts £0; a part-exchange counts cash only unless a source values the player, DEC-237 (d))
for r in DS:
    t = by_tid.get(r["transfer_id"])
    if not t or r["fee_amount"] == "":
        continue  # a date-only row (completion date from a grade B report): the fee follows the normal rule
    amt, cur = float(r["fee_amount"] or 0), (r["currency"] or "GBP")
    gbp, fx = convert(amt, cur, t["date"]) if amt else (0.0, None)
    grade = r["grade"]
    strong = grade in ("A", "B") or (grade == "C" and "soccerbase.com" in r["url"])
    conf = [c for c in checks.get(r["url"], []) if c["status"] == "VERIFIED" and c["amount"] in r["confirm_amounts"].split(";")]
    sid = source_id(r["url"], r["publisher"] or urllib.parse.urlparse(r["url"]).netloc, grade, "press_or_club") if r["url"] else ""
    e = {"origin": "deal_structure", "source_id": sid, "grade": grade, "fee_text": r["fee_text"],
         "parsed": {"amount": amt, "currency": cur, "qualifiers": ["deal_structure"], "kind": "fee"}, "amount": amt, "currency": cur,
         "qualifiers": "deal_structure", "gbp": gbp, "fx": fx, "quote": r["quote"], "url": r["url"], "archive_url": "", "date": t["date"],
         "status": "VERIFIED" if (conf and strong) else "UNVERIFIED", "note": f"{r['rule']}: {r['note']}", "published": r["published"],
         "evidence_id": f"{t['transfer_id']}-E{len(t['_ev']) + 1:02d}", "total_incl_addons": False, "figure_rejected": False}
    if conf and strong:
        e["checked"] = {"check_id": conf[0]["check_id"], "quote": r["quote"], "retrieved": conf[0]["retrieved"], "reviewed": "accept: " + r["rule"]}
        e["retrieved"] = conf[0]["retrieved"]
    t["_ev"].append(e)
    t["canonical"], t["fee_gbp"] = e, gbp
    t["original_amount"], t["currency"] = (amt if amt else ""), (cur if amt else "")
    t["fx_rate"] = fx["fx_rate"] if fx else ""
    t["fx_date"] = fx["fx_date"] if fx else ""
    t["fx_series"] = fx["fx_series"] if fx else ""
    t["fee_status"] = r["fee_status"]
    t["type"] = r["type"] or t["type"]
    t["grade"], t["canonical_source_id"], t["status"] = grade, sid, e["status"]
    t["fee_versions_gbp"] = ";".join(str(a) for a in sorted({round(x["gbp"]) for x in t["_ev"] if x["gbp"] is not None}))

transfers = [t for t in transfers if t["season_attributed"] and (
    (t["from_club_id"], t["season_attributed"]) in in_pl or (t["to_club_id"], t["season_attributed"]) in in_pl)]
transfers.sort(key=lambda t: (t["date"], t["transfer_id"]))

# ---------------------------------------------------------------- stage D: ledger, series
ledger = []
for t in transfers:
    s = t["season_attributed"]
    for side, cid, other, sign in (("buyer", t["to_club_id"], t["from_club"], 1), ("seller", t["from_club_id"], t["to_club"], -1)):
        if not cid:
            continue
        counted = (cid, s) in in_pl
        amt = (t["fee_gbp"] or 0.0) * sign
        real = round(amt * cpi_base / cpi[t["date"][:7]], 2) if t["date"][:7] in cpi else None
        ledger.append({"club_id": cid, "date": t["date"], "season": s, "transfer_id": t["transfer_id"], "side": side,
                       "player": t["player"], "counterparty": other, "type": t["type"], "net_gbp": money(amt),
                       "net_real_gbp2026": money(real), "counted": "yes" if counted else "no",
                       "reason": "" if counted else "club not in the PL that season (frozen)",
                       "fee_status": t["fee_status"], "grade": t["grade"], "status": t["status"],
                       "notes": (f"converted from {t['currency']} {t['original_amount']:.0f} at {t['fx_rate']} ({t['fx_series']}, {t['fx_date']})"
                                 if t["fx_rate"] else "")})
ledger.sort(key=lambda r: (r["date"], r["club_id"], r["transfer_id"], r["side"]))

month_ends = []
d = dt.date.fromisoformat(START_MONTH_END)
while d.isoformat() <= "2026-08-31":
    month_ends.append(d.isoformat())
    d = dt.date.fromisoformat(month_end((d + dt.timedelta(days=1)).isoformat()))
month_ends.append(FREEZE)

counted_by_club = defaultdict(list)
for r in ledger:
    if r["counted"] == "yes":
        counted_by_club[r["club_id"]].append(r)
series, series_index = [], {}
for c in club_ids:
    rows = counted_by_club.get(c, [])
    j, cum, real, last_change = 0, 0.0, 0.0, ""
    for me in month_ends:
        while j < len(rows) and rows[j]["date"] <= me:
            v = float(rows[j]["net_gbp"])
            if v != 0:
                last_change = rows[j]["date"]
            cum += v
            real += float(rows[j]["net_real_gbp2026"] or 0)
            j += 1
        played = [s for s in seasons_of_club.get(c, []) if season_by_label[s]["attribution_start"] <= me]
        cur = season_of(me)
        rec = {"month_end": me, "club_id": c, "cum_net_gbp": round(cum, 2), "in_pl": "yes" if (c, cur) in in_pl else "no",
               "pl_seasons_played": len(played), "cum_real_net_gbp2026": round(real, 2),
               "avg_real_net_per_season_gbp2026": round(real / len(played), 2) if played else None,
               "_reached": last_change or "0000"}
        series.append(rec)
by_month = defaultdict(list)
for r in series:
    if r["pl_seasons_played"] > 0:
        by_month[r["month_end"]].append(r)
for me, rows in by_month.items():
    rows.sort(key=lambda r: (-r["cum_net_gbp"], r["_reached"], r["club_id"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

# ---------------------------------------------------------------- tiers, conflicts, coverage
order_cache = {}
for me, rows in by_month.items():
    order_cache[me] = [(r["club_id"], r["cum_net_gbp"], r["_reached"]) for r in rows]


def top12_changes(club_deltas, from_date):
    """True if shifting the clubs' values by deltas from from_date changes the leader, or who is in the top 12,
    at any month end (DEC-256)."""
    for me in month_ends:
        if me < from_date or me not in order_cache:
            continue
        base = order_cache[me]
        if not any(c in club_deltas for c, _, _ in base):
            continue
        top = {c for c, _, _ in base[:12]}
        mod = [(c, v - club_deltas.get(c, 0.0), rch) for c, v, rch in base]
        mod.sort(key=lambda x: (-x[1], x[2], x[0]))
        if mod[0][0] != base[0][0] or {c for c, _, _ in mod[:12]} != top:
            return True
    return False


record_tids = {t["transfer_id"] for t in transfers for e in t["_ev"] if "record" in (e.get("record_type") or "").lower()}
disputed_tids = {t["transfer_id"] for t in transfers for e in t["_ev"] if e.get("lead_section") == "C"}
rng = random.Random(101)
for t in transfers:
    reasons = []
    f = t["fee_gbp"] or 0.0
    if f >= 20e6:
        reasons.append("fee >= £20m")
    if t["transfer_id"] in record_tids:
        reasons.append("club or British record (research lead)")
    if t["transfer_id"] in disputed_tids:
        reasons.append("disputed fee (research section C)")
    if f > 0 and not reasons:
        deltas = {}
        s = t["season_attributed"]
        if t["to_club_id"] and (t["to_club_id"], s) in in_pl:
            deltas[t["to_club_id"]] = f
        if t["from_club_id"] and (t["from_club_id"], s) in in_pl:
            deltas[t["from_club_id"]] = deltas.get(t["from_club_id"], 0) - f
        if deltas and top12_changes(deltas, t["date"]):
            reasons.append("removal changes the leader or the top 12")
    vers = [float(v) for v in t["fee_versions_gbp"].split(";") if v]
    if f > 0 and len(vers) > 1 and not reasons:
        for alt in (min(vers), max(vers)):
            dlt = {}
            s = t["season_attributed"]
            if t["to_club_id"] and (t["to_club_id"], s) in in_pl:
                dlt[t["to_club_id"]] = f - alt
            if t["from_club_id"] and (t["from_club_id"], s) in in_pl:
                dlt[t["from_club_id"]] = dlt.get(t["from_club_id"], 0) - (f - alt)
            if dlt and abs(f - alt) > 0 and top12_changes(dlt, t["date"]):
                reasons.append("alternative fee version changes the leader or the top 12"); break
    if reasons:
        t["tier"], t["tier_reason"] = "1", "; ".join(reasons)
    elif f >= 2e6:
        t["tier"], t["tier_reason"] = "2", "£2m to under £20m"
    elif f > 0:
        t["tier"], t["tier_reason"] = "3", "under £2m"
    else:
        t["tier"], t["tier_reason"] = "", "no fee counted"
# order test for the round 2 deals not researched (IQ-15h, DEC-419 (a)): does removing the fee, or using another version of it, change
# the leader or who is in the top 12 at any month end? Written to source/round2_order_test.csv; those deals go to a later round
_r2map = os.path.join(SRC, "source_round2_map.csv")
if os.path.exists(_r2map):
    _researched = set()
    for _l in rd("leads_evidence.csv"):
        _m = re.match(r"part2(?:2b|3g|4b|4d)-(R\d{4})-", _l["lead_row"])
        if _m:
            _researched.add(_m.group(1))
    _tby = {t["transfer_id"]: t for t in transfers}

    def _first_change(club_deltas, from_date):
        for me in month_ends:
            if me < from_date or me not in order_cache:
                continue
            base = order_cache[me]
            if not any(c in club_deltas for c, _, _ in base):
                continue
            mod = sorted(((c, v - club_deltas.get(c, 0.0), rch) for c, v, rch in base), key=lambda x: (-x[1], x[2], x[0]))
            if mod[0][0] != base[0][0]:
                return me, "leader"
            if {c for c, _, _ in mod[:12]} != {c for c, _, _ in base[:12]}:
                return me, "top 12"
        return "", ""

    def _deltas(t, amount):
        d, s_ = {}, t["season_attributed"]
        if t["to_club_id"] and (t["to_club_id"], s_) in in_pl:
            d[t["to_club_id"]] = amount
        if t["from_club_id"] and (t["from_club_id"], s_) in in_pl:
            d[t["from_club_id"]] = d.get(t["from_club_id"], 0) - amount
        return d

    _out = []
    for _r in csv.DictReader(open(_r2map, encoding="utf-8")):
        t = _tby.get(_r["transfer_id"])
        if _r["deal_id"] in _researched or not t:
            continue
        f = t["fee_gbp"] or 0.0
        res = ("", "")
        how = ""
        if f > 0:
            res = _first_change(_deltas(t, f), t["date"])
            how = "fee removed" if res[0] else ""
            if not res[0]:
                for alt in sorted({float(v) for v in t["fee_versions_gbp"].split(";") if v} - {f}):
                    res = _first_change(_deltas(t, f - alt), t["date"])
                    if res[0]:
                        how = "another version of the fee"
                        break
        _out.append({"deal_id": _r["deal_id"], "transfer_id": t["transfer_id"], "player": t["player"], "date": t["date"],
                     "season": t["season_attributed"], "fee_gbp": f"{f:.2f}", "could_change": "yes" if res[0] else "no",
                     "first_month_end": res[0], "what_changes": res[1], "test": how})
    with open(os.path.join(os.path.dirname(_r2map), "round2_order_test.csv"), "w", newline="", encoding="utf-8") as _fh:
        _w = csv.DictWriter(_fh, fieldnames=list(_out[0].keys()) if _out else ["deal_id"], lineterminator="\n")
        _w.writeheader(); _w.writerows(_out)
tier3 = sorted(t["transfer_id"] for t in transfers if t["tier"] == "3")
sample3 = set(rng.sample(tier3, max(1, round(len(tier3) * 0.05)))) if tier3 else set()
for t in transfers:
    t["tier3_sample"] = "yes" if t["transfer_id"] in sample3 else ""

conflicts = []
for t in transfers:
    vs = [e for e in t["_ev"] if e["gbp"] is not None and "up_to" not in e["parsed"]["qualifiers"] and "combined" not in e["parsed"]["qualifiers"]
          and not e.get("total_incl_addons") and not e.get("figure_rejected")]
    if len({round(e["gbp"]) for e in vs}) < 2:
        continue
    lo, hi = min(e["gbp"] for e in vs), max(e["gbp"] for e in vs)
    same_grade = defaultdict(set)
    for e in vs:
        same_grade[e["grade"]].add(round(e["gbp"]))
    flag = any(len(v) > 1 and (max(v) - min(v)) > 1e6 and (max(v) - min(v)) > 0.1 * min(v) for v in same_grade.values())
    # settled at source (DEC-261): the fee used is VERIFIED and no differing figure of the same grade is VERIFIED
    can = t["canonical"]
    # totals that a source itself explains: guaranteed fee + add-ons, or a stated "rising to" maximum (any currency, in GBP)
    explained = set()
    for e in t["_ev"]:
        txt = (e["fee_text"] or "") + " " + (e.get("quote") or "")
        if not re.search(r"add-on|add ons|bonus|variable|rise|rising|performance|incentive|instalment|up to|potential|could reach|"
                         r"appearance|further|initial|guaranteed|up front|upfront|clause|player-plus-cash|plus", txt, re.I):
            continue
        nums = []
        for mm in re.finditer(r"(£|€|\$)\s?(\d+(?:\.\d+)?)\s?(m|million|bn)", txt.replace(",", "")):
            v = float(mm.group(2)) * (1e9 if mm.group(3) == "bn" else 1e6)
            g, _ = convert(v, {"£": "GBP", "€": "EUR", "$": "USD"}[mm.group(1)], t["date"] or "")
            if g:
                nums.append(g)
        explained.update(nums)
        if len(nums) >= 2:
            explained.add(nums[0] + nums[1])
    def is_explained(v):
        return any(abs(v - x) <= max(0.03 * x, 2e5) for x in explained)
    rival_verified = [e for e in vs if e["status"] == "VERIFIED" and can is not None and e["grade"] == can["grade"]
                      and abs(e["gbp"] - can["gbp"]) > max(1e6, 0.1 * can["gbp"]) and not is_explained(e["gbp"])]
    settled = (can is not None and can["status"] == "VERIFIED" and not rival_verified)
    # DEC-277 (Luke): a disagreement is settled by the contract's rule — best grade first, then the earliest report (a contemporary GBP
    # figure from an A/B source preferred, §5). Say which step decided it.
    if can is None or can["status"] != "VERIFIED":
        rule = "no figure confirmed at source yet: the fee stays UNVERIFIED (not on screen) until one is"
    else:
        others = [e for e in vs if e is not can and e["status"] == "VERIFIED" and round(e["gbp"]) != round(can["gbp"])]
        if not others:
            rule = "the only figure confirmed at source"
        elif all(GRADE_RANK.get(e["grade"], 3) > GRADE_RANK.get(can["grade"], 3) for e in others):
            rule = f"best grade ({can['grade']})"
        elif can["currency"] == "GBP" and any(e["currency"] != "GBP" and e["grade"] == can["grade"] for e in others) and all(
                e["currency"] != "GBP" for e in others if e["grade"] == can["grade"] and (e.get("published") or "9999") < (can.get("published") or "9999")):
            rule = "same grade; the contemporary sterling figure is preferred (contract §5)"
        elif can.get("dec404"):
            rule = f"same grade; the report that the deal was completed beats earlier bids, agreed or expected figures (DEC-404; {can.get('published') or 'date not stated'})"
        else:
            rule = f"same grade; earliest report ({can.get('published') or 'date not stated: list order'})"
    rule_text = f"£{t['fee_gbp'] / 1e6:.1f}m ({can['grade'] if can else ''}, {urllib.parse.urlparse(can['url']).netloc if can and can.get('url') else 'no source'}): {rule}"
    conflicts.append({"transfer_id": t["transfer_id"], "player": t["player"], "from_club": t["from_club"], "to_club": t["to_club"],
                      "date": t["date"], "canonical_gbp": money(t["fee_gbp"]), "canonical_grade": t["grade"],
                      "min_gbp": money(lo), "max_gbp": money(hi), "spread_gbp": money(hi - lo), "versions": len(vs),
                      "tier": t["tier"], "same_grade_gap_over_10pct_and_1m": "yes" if flag else "",
                      "settled_at_source": ("yes: the fee used is confirmed at source; differing figures were not" if settled else
                                            ("no: two same-grade sources confirm different figures" if rival_verified else
                                             "no: the fee used is not yet confirmed at source")),
                      "for_luke": "yes" if (flag and t["tier"] == "1" and not settled) else "",
                      "rule_result": rule_text if (flag and t["tier"] == "1" and not settled) else "",
                      "versions_detail": " | ".join(f"{e['grade']} {e['status'][0]} {e['fee_text'][:60]} ({e['url'][:80]})" for e in vs)})
conflicts.sort(key=lambda c: (-float(c["spread_gbp"]), c["transfer_id"]))


def era_of(season):
    for a, b, name in ERAS:
        if a <= season <= b:
            return name
    return ""


cov = defaultdict(lambda: Counter())
for t in transfers:
    for cid in (t["to_club_id"], t["from_club_id"]):
        if cid and (cid, t["season_attributed"]) in in_pl:
            c = cov[(cid, era_of(t["season_attributed"]))]
            c["transfers_found"] += 1
            if t["fee_gbp"]:
                c["fee_bearing"] += 1
            if t["fee_status"].startswith("undisclosed"):
                c["undisclosed_no_figure"] += 1
            if t["fee_status"].startswith("NOT FOUND"):
                c["fee_not_found"] += 1
            if t["fee_gbp"] and t["status"] != "VERIFIED":
                c["fee_unverified"] += 1
            if t["fee_gbp"] and t["status"] == "VERIFIED":
                c["fee_verified"] += 1
            if t["fee_gbp"] and t["grade"] in ("A", "B"):
                c["fee_grade_A_or_B"] += 1
coverage = []
for (cid, era), c in sorted(cov.items()):
    seasons_in = [s for s in seasons_of_club[cid] if era_of(s) == era]
    coverage.append({"club_id": cid, "era": era, "pl_seasons_in_era": len(seasons_in), **{k: c.get(k, 0) for k in (
        "transfers_found", "fee_bearing", "fee_grade_A_or_B", "fee_verified", "fee_unverified", "undisclosed_no_figure", "fee_not_found")}})

# league-wide window totals (cross-check with published totals only; never forced to match)
wt = defaultdict(lambda: {"gross_spend_gbp": 0.0, "pl_income_from_non_pl_gbp": 0.0, "transfers": 0})
for t in transfers:
    if not t["fee_gbp"]:
        continue
    m = int(t["date"][5:7])
    y = int(t["date"][:4])
    win = f"summer {y}" if 4 <= m <= 10 else (f"January {y}" if m <= 3 else f"January {y + 1}")
    s = t["season_attributed"]
    buyer_pl = t["to_club_id"] and (t["to_club_id"], s) in in_pl
    seller_pl = t["from_club_id"] and (t["from_club_id"], s) in in_pl
    if buyer_pl:
        wt[win]["gross_spend_gbp"] += t["fee_gbp"]
        wt[win]["transfers"] += 1
    if seller_pl and not buyer_pl:
        wt[win]["pl_income_from_non_pl_gbp"] += t["fee_gbp"]
    if buyer_pl and not seller_pl:
        wt[win].setdefault("pl_spend_with_non_pl_gbp", 0.0)
        wt[win]["pl_spend_with_non_pl_gbp"] += t["fee_gbp"]
window_totals = []
for k in sorted(wt, key=lambda w: (w.split()[1], 0 if w.startswith("January") else 1)):
    v = wt[k]
    net = v.get("pl_spend_with_non_pl_gbp", 0.0) - v["pl_income_from_non_pl_gbp"]
    window_totals.append({"window": k, "gross_spend_gbp": money(v["gross_spend_gbp"]), "net_spend_gbp": money(net),
                          "fee_transfers": v["transfers"]})

# deals with a PL side per window, against the two windows of the same type either side (IQ-15j: January 2020 had been cut short by a
# shortened Wikipedia list revision); a window under half the median of its neighbours is flagged and the check below fails
# windows the deal-count check knows are short, with the reason (DEC-431). Each one's club-season pages list the missing deals
# (source/club_page_rows_unused.csv); they are not in the build because no brief has approved that window's change yet.
KNOWN_SPARSE = {
    "January 1993": "1992-93 club-season pages: 19 more rows readable with the newer table reading, not used",
    "January 1994": "1993-94 club-season pages: 15 more rows readable with the newer table reading, not used",
    "January 2004": "the winter 2003-04 list page misses most deals; 2003-04 club-season pages list 52 more, not used",
    "January 2005": "the winter 2004-05 list page misses most deals; 2004-05 club-season pages list 36 more, not used",
}
wdeals = Counter()
for t in transfers:
    s = t["season_attributed"]
    if (t["to_club_id"] and (t["to_club_id"], s) in in_pl) or (t["from_club_id"] and (t["from_club_id"], s) in in_pl):
        m, y = int(t["date"][5:7]), int(t["date"][:4])
        wdeals[f"summer {y}" if 4 <= m <= 10 else (f"January {y}" if m <= 3 else f"January {y + 1}")] += 1
window_counts = []
for k in sorted(wdeals, key=lambda w: (w.split()[1], 0 if w.startswith("January") else 1)):
    kind, y = k.split()[0], int(k.split()[1])
    nb = [wdeals[f"{kind} {y + d}"] for d in (-2, -1, 1, 2) if f"{kind} {y + d}" in wdeals]
    med = sorted(nb)[len(nb) // 2] if len(nb) % 2 else (sorted(nb)[len(nb) // 2 - 1] + sorted(nb)[len(nb) // 2]) / 2 if nb else 0
    window_counts.append({"window": k, "deals_with_pl_side": wdeals[k], "neighbour_median": med,
                          "flag": "far below its neighbours" if nb and wdeals[k] < 0.5 * med else ""})

# ---------------------------------------------------------------- write files
ev_rows = []
for t in transfers:
    for e in t["_ev"]:
        ev_rows.append({"evidence_id": e["evidence_id"], "transfer_id": t["transfer_id"], "source_id": e["source_id"],
                        "origin": e["origin"], "fee_text": e["fee_text"], "amount": money(e["amount"]) if e["amount"] is not None else "",
                        "currency": e["currency"] or "", "qualifiers": e["qualifiers"], "gbp": money(e["gbp"]),
                        "grade": e["grade"], "quote": e["quote"], "quote_words": len(e["quote"].split()), "url": e["url"],
                        "archive_url": e["archive_url"], "cited_urls": e.get("cite_urls", ""),
                        "cited_publishers": e.get("cite_publishers", ""), "retrieved": e.get("retrieved", ""),
                        "status": e["status"], "canonical": "yes" if t["canonical"] is e else "",
                        "note": e.get("note", "") or e.get("grade_note", ""),
                        "review": (e.get("checked") or {}).get("reviewed", ""), "check_id": (e.get("checked") or {}).get("check_id", ""),
                        "published": e.get("published", "") or pubdate(e["url"])})
used_sources = {e["source_id"] for e in ev_rows}
src_rows = sorted((s for s in sources.values() if s["source_id"] in used_sources), key=lambda s: s["source_id"])
for t in transfers:
    t["fee_gbp_out"] = money(t["fee_gbp"])
    t["original_amount_out"] = f"{t['original_amount']:.2f}" if isinstance(t["original_amount"], float) else ""

wr("clubs.csv", clubs, ["club_id", "display_name", "other_names", "wikipedia_title", "pl_seasons_to_2026_27", "first_pl_season", "last_pl_season", "colour_key", "logo_ref"])
wr("pl_membership.csv", membership, ["season", "club_id", "club_name_on_page", "final_position", "relegated", "source", "revid", "grade", "crosscheck"])
wr("seasons.csv", seasons, ["season", "first_matchday", "last_matchday", "dates_source", "dates_revid", "attribution_start", "attribution_start_basis",
                            "attribution_end", "attribution_end_basis", "window_system", "summer_window_open", "summer_window_close", "summer_window_source",
                            "january_window_open", "january_window_close", "january_window_source"])
TCOLS = ["transfer_id", "player", "player_article", "from_club", "to_club", "type", "date", "date_basis", "season_attributed", "fee_status",
         "original_amount_out", "currency", "fx_rate", "fx_date", "fx_series", "fee_gbp_out", "fee_versions_gbp", "canonical_source_id",
         "grade", "tier", "tier_reason", "tier3_sample", "status", "verified_by", "found_via", "parent_transfer_id"]
VBY = {"A": "club or league statement (A)", "B": "press report (B)", "C": "database source: Soccerbase (C)"}
for t in transfers:
    t["verified_by"] = VBY.get(t["grade"], "") if t["status"] == "VERIFIED" else ""
with open(os.path.join(DATA, "transfers.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow([c.replace("_out", "") for c in TCOLS])
    for t in transfers:
        w.writerow([t.get(c, "") for c in TCOLS])
wr("fee_evidence.csv", ev_rows, ["evidence_id", "transfer_id", "source_id", "origin", "fee_text", "amount", "currency", "qualifiers", "gbp", "grade", "quote",
                                 "quote_words", "url", "archive_url", "cited_urls", "cited_publishers", "retrieved", "status", "canonical", "note", "check_id", "review", "published"])
wr("sources.csv", src_rows, ["source_id", "url", "publisher", "grade", "kind"])
wr("club_ledger.csv", ledger, ["club_id", "date", "season", "transfer_id", "side", "player", "counterparty", "type", "net_gbp", "net_real_gbp2026",
                               "counted", "reason", "fee_status", "grade", "status", "notes"])
cs = defaultdict(lambda: Counter())
for r in ledger:
    if r["counted"] != "yes":
        continue
    c = cs[(r["club_id"], r["season"])]
    v = float(r["net_gbp"])
    c["spend"] += v if v > 0 else 0
    c["income"] += -v if v < 0 else 0
    c["net"] += v
    c["real"] += float(r["net_real_gbp2026"] or 0)
    c["n"] += 1
    if r["fee_status"].startswith("undisclosed"):
        c["und"] += 1
club_season = [{"club_id": c, "season": s, "spend_gbp": money(v["spend"]), "income_gbp": money(v["income"]), "net_gbp": money(v["net"]),
                "net_real_gbp2026": money(v["real"]), "transfers": v["n"], "undisclosed_no_figure": v["und"]}
               for (c, s) in sorted(in_pl, key=lambda x: (x[1], x[0])) for v in [cs[(c, s)]]]
wr("club_season.csv", club_season, ["club_id", "season", "spend_gbp", "income_gbp", "net_gbp", "net_real_gbp2026", "transfers", "undisclosed_no_figure"])
for r in series:
    r["avg_real_net_per_season_gbp2026"] = money(r["avg_real_net_per_season_gbp2026"])
    r["cum_net_gbp"] = money(r["cum_net_gbp"])
    r["cum_real_net_gbp2026"] = money(r["cum_real_net_gbp2026"])
wr("series_monthly.csv", series, ["month_end", "club_id", "cum_net_gbp", "rank", "in_pl", "pl_seasons_played", "cum_real_net_gbp2026",
                                  "avg_real_net_per_season_gbp2026"])
wr("conflicts.csv", conflicts, ["transfer_id", "player", "from_club", "to_club", "date", "canonical_gbp", "canonical_grade", "min_gbp", "max_gbp", "spread_gbp",
                                "versions", "tier", "same_grade_gap_over_10pct_and_1m", "settled_at_source", "for_luke", "rule_result", "versions_detail"])
PRIORITY = ["chelsea", "manchester_united", "manchester_city", "arsenal", "liverpool", "newcastle_united", "blackburn_rovers", "everton"]  # DEC-263


def prio(t):
    ids = [PRIORITY.index(c) for c in (t["to_club_id"], t["from_club_id"]) if c in PRIORITY]
    return min(ids) if ids else len(PRIORITY)


tier1 = sorted((t for t in transfers if t["tier"] == "1"), key=lambda t: (prio(t), -(t["fee_gbp"] or 0), t["transfer_id"]))
for i, t in enumerate(tier1):
    t["batch"] = f"T1-{i // 50 + 1:02d}"
    ce = t["canonical"] or {}
    t["canonical_url"] = ce.get("url", "")
    t["canonical_quote"] = ce.get("quote", "")
    t["review"] = (ce.get("checked") or {}).get("reviewed", "")
wr("tier1_list.csv", tier1, ["batch", "transfer_id", "player", "from_club", "to_club", "date", "season_attributed", "fee_gbp_out", "fee_status", "grade",
                             "status", "tier_reason", "fee_versions_gbp", "canonical_source_id", "canonical_url", "canonical_quote", "review"])
_p = os.path.join(DATA, "tier1_list.csv")
_s = open(_p, encoding="utf-8").read().replace("fee_gbp_out", "fee_gbp", 1)
open(_p, "w", encoding="utf-8").write(_s)
wr("coverage.csv", coverage, ["club_id", "era", "pl_seasons_in_era", "transfers_found", "fee_bearing", "fee_grade_A_or_B", "fee_verified", "fee_unverified",
                              "undisclosed_no_figure", "fee_not_found"])
wr("unmatched_leads.csv", sorted(unmatched, key=lambda u: (u["date"], u["lead_id"])), ["lead_id", "section", "date", "player", "from_club", "to_club",
                                                                                     "fee_as_reported", "grade", "url", "reason"])
wr("window_totals.csv", window_totals, ["window", "gross_spend_gbp", "net_spend_gbp", "fee_transfers"])
wr("source/window_deal_counts.csv", window_counts, ["window", "deals_with_pl_side", "neighbour_median", "flag"])
mom = rd("moments_leads.csv")
if mom:
    wr("moments.csv", mom, list(mom[0].keys()))

# ---------------------------------------------------------------- checks
res = []


def check(name, ok, detail=""):
    res.append((name, "PASS" if ok else "FAIL", detail))


cnt = Counter(m["season"] for m in membership)
check("22 clubs per season 1992-95, 20 after (706 club-seasons)", all(cnt[s] == (22 if s < "1995-96" else 20) for s in cnt) and sum(cnt.values()) == 706,
      f"{sum(cnt.values())} club-seasons in {len(cnt)} seasons")
check("every season has an attribution window", all(s["attribution_start"] and s["attribution_end"] and s["attribution_start"] <= s["attribution_end"] for s in seasons),
      f"{seasons[0]['attribution_start']} to {seasons[-1]['attribution_end']}")
check("51 clubs, each with at least one PL season", len(clubs) == 51 and all(c["pl_seasons_to_2026_27"] for c in clubs), f"{len(clubs)} clubs")
bad = [r for r in ledger if r["counted"] == "yes" and (r["club_id"], r["season"]) not in in_pl]
check("no transfer counted outside its club's PL seasons", not bad, f"{sum(1 for r in ledger if r['counted'] == 'no')} ledger rows frozen (club not in the PL)")
pl_spend = sum(float(r["net_gbp"]) for r in ledger if r["counted"] == "yes" and float(r["net_gbp"]) > 0)
pl_income = -sum(float(r["net_gbp"]) for r in ledger if r["counted"] == "yes" and float(r["net_gbp"]) < 0)
ext = 0.0
for t in transfers:
    s = t["season_attributed"]
    b = bool(t["to_club_id"]) and (t["to_club_id"], s) in in_pl
    sl = bool(t["from_club_id"]) and (t["from_club_id"], s) in in_pl
    ext += (t["fee_gbp"] or 0) * ((1 if b else 0) - (1 if sl else 0))
check("PL-to-PL deals net to zero (spend - income of PL clubs = net spend with non-PL clubs)", abs((pl_spend - pl_income) - ext) < 1,
      f"spend £{pl_spend:,.0f} − income £{pl_income:,.0f} = £{pl_spend - pl_income:,.0f}; net with non-PL clubs £{ext:,.0f}")
nofee = [t for t in transfers if t["fee_gbp"] and not (t["canonical_source_id"] and t["canonical_source_id"] in used_sources)]
check("no fee without a source row", not nofee, f"{sum(1 for t in transfers if t['fee_gbp'])} fee-bearing transfers")
tm = []
for fn in os.listdir(DATA):
    if fn.endswith(".csv"):
        for line in open(os.path.join(DATA, fn), encoding="utf-8"):
            if re.search(r"https?://[^ ,\"]*transfermarkt", line, re.I):
                tm.append(fn)
check("no Transfermarkt figure or URL anywhere", not tm, ", ".join(sorted(set(tm))) or "none found")
long_q = [e for e in ev_rows if e["quote_words"] >= 25]
check("quotes under 25 words", not long_q, f"{len(ev_rows)} evidence rows")
noconv = [t for t in transfers if t["currency"] and t["currency"] != "GBP" and t["fee_gbp"] and not t["fx_rate"]]
check("every conversion has a rate row", not noconv, f"{sum(1 for t in transfers if t['fx_rate'])} conversions")
ser_ok = True
last = {}
for r in series:
    if r["month_end"] == FREEZE:
        last[r["club_id"]] = float(r["cum_net_gbp"])
for c in club_ids:
    tot = sum(float(r["net_gbp"]) for r in counted_by_club.get(c, []) if r["date"] <= FREEZE)
    if abs(tot - last.get(c, 0.0)) > 0.5:
        ser_ok = False
check("month-end series consistent with the ledger", ser_ok, f"{len(month_ends)} month ends × {len(club_ids)} clubs")
_lowwin = [f"{w['window']} ({w['deals_with_pl_side']} deals; neighbours' median {w['neighbour_median']:g})" for w in window_counts
           if w["flag"] and w["window"] not in KNOWN_SPARSE]
_known = [w["window"] for w in window_counts if w["flag"] and w["window"] in KNOWN_SPARSE]
_stale = sorted(set(KNOWN_SPARSE) - set(_known))
check("no window has under half the PL deals of the same-type windows either side (bar documented gaps)", not _lowwin and not _stale,
      "; ".join(_lowwin + [f"{w} documented but no longer flagged: remove it from KNOWN_SPARSE" for w in _stale])
      or f"{len(window_counts)} windows compared; documented gaps (DEC-431): {', '.join(_known) or 'none'}")
_undated = [r for r in rd("wiki_window_rows.csv") if not r["date"]]
check("every list-page row has a date (IQ-15j: undated rows are dropped from the build)", not _undated,
      f"{len(_undated)} undated rows" if _undated else f"{len(rd('wiki_window_rows.csv'))} rows")
v04 = {"XUMADMS": "2.8564", "XUMAFFS": "9.7433", "XUMAILS": "2152.4916", "XUMASPS": "181.055", "XUMANGS": "3.217", "XUMAPES": "247.3737", "XUMAUSS": "1.8127"}
got = {r["series_code"]: r["units_per_gbp"] for r in rd("fx.csv", DATA) if r["date"] == "1992-01-31" and r["series_code"] in v04}
check("Bank of England Jan 1992 monthly averages equal Cowork's V-04 reading", all(abs(float(got.get(k, "nan")) - float(v)) < 1e-9 for k, v in v04.items()),
      f"{len(got)} of 7 series compared")
ecb = {r["month"]: r["gbp_per_eur"] for r in rd("fx_ecb_crosscheck.csv", DATA)}
check("ECB GBP/EUR 1999-01 equals Cowork's V-06 reading (0.7029125)", ecb.get("1999-01") == "0.7029125", f"{len(ecb)} months")
# lesson of IQ-15b (two over-broad rejections): an "amount" rejection must not silently remove a research lead whose own quote names the player
# with that figure, unless the review note says it was weighed against that lead
blocked = []
for t in transfers:
    sn = pname(t["player"]).split(" ")[-1] if t["player"] else ""
    for e in t["_ev"]:
        if e["origin"] == "research_lead" and e.get("figure_rejected") and sn and sn in L.norm(e.get("quote") or ""):
            notes = [r["note"] for r in review.values() if r.get("scope") == "amount" and r["transfer_id"] == t["transfer_id"]]
            if not any("research lead" in n for n in notes):
                blocked.append(f"{t['player']} {e['fee_text']}")
check("no amount rejection silently removes a research lead that quotes the player with that figure", not blocked,
      "; ".join(blocked[:10]) or "all such rejections were weighed against the lead")
check("CPI base month recorded", True, f"D7BT {cpi_base_month} = {cpi_base} (September 2026 not yet published at build time)")

with open(os.path.join(DATA, "CHECKS.md"), "w", encoding="utf-8") as f:
    f.write("# RTT-101 data checks (generated by `scripts/build_rtt101_dataset.py`; do not edit by hand)\n\n")
    f.write("Phase 1 preview: every fee is UNVERIFIED unless `status` says VERIFIED. Not for screen.\n\n| Check | Result | Detail |\n|---|---|---|\n")
    for n, r, dtl in res:
        f.write(f"| {n} | **{r}** | {dtl} |\n")
    extra = os.path.join(SRC, "private_crosschecks.md")
    if os.path.exists(extra):
        f.write("\n" + open(extra, encoding="utf-8").read())

manifest = {"build": "IQ-15 phase 1", "freeze": FREEZE, "cpi_base_month": cpi_base_month, "files": {}}
for fn in sorted(os.listdir(DATA)):
    p = os.path.join(DATA, fn)
    if os.path.isfile(p) and fn not in ("manifest.json", "runner_job.json") and fn.endswith((".csv", ".md")):
        manifest["files"][fn] = hashlib.sha256(open(p, "rb").read()).hexdigest()
json.dump(manifest, open(os.path.join(DATA, "manifest.json"), "w"), indent=1, sort_keys=True)

# ---------------------------------------------------------------- report data for the report writer
json.dump({"checks": res, "n_transfers": len(transfers), "n_fee": sum(1 for t in transfers if t["fee_gbp"]),
           "n_tier": Counter(t["tier"] for t in transfers), "n_status": Counter(t["status"] for t in transfers if t["fee_gbp"]),
           "n_conflicts": len(conflicts), "n_conflicts_for_luke": sum(1 for c in conflicts if c["for_luke"]),
           "cpi_base_month": cpi_base_month},
          open(os.path.join(SRC, "build_summary.json"), "w"), indent=1, sort_keys=True, default=str)
print("\n".join(f"{r}  {n}  ({d})" for n, r, d in res))
print(len(transfers), "transfers;", sum(1 for t in transfers if t["fee_gbp"]), "with a fee;", dict(Counter(t["tier"] for t in transfers)))
