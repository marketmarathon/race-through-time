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
import bisect, csv, datetime as dt, hashlib, json, os, random, re, sys, urllib.parse
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
    if re.search(r"\bfree\b|released|nominal|bosman|end of contract", t):
        return "free"
    if re.search(r"undisclosed|not disclosed", t):
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
    return ta[-1] == tb[-1] and ta[0][0] == tb[0][0]


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
    idx[pname(t["player"]).split(" ")[-1] if t["player"] else ""].append(t)
lead_rows = rd("leads_evidence.csv")


def lead_date(r):
    d = r["date"].strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return d, "research lead date (UNVERIFIED)"
    if re.fullmatch(r"\d{4}-\d{2}", d):
        return month_end(d + "-01"), "month only: month end (contract §2)"
    return "", "NOT FOUND"


group_new = {}
unmatched = []
for r in lead_rows:
    if r["lead_section"] not in ("A", "B", "C"):
        continue
    d, basis = lead_date(r)
    fid, toid = L.club_id(r["from_club"]), L.club_id(r["to_club"])
    if not (fid or toid):
        continue
    last = pname(r["player"]).split(" ")[-1] if r["player"] else ""
    best, far = None, None
    for t in idx.get(last, []):
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
        if gap <= 400 and fid and toid and t["from_club_id"] == fid and t["to_club_id"] == toid and far is None:
            far = t  # same player, same two clubs, within 400 days: the same deal reported at another stage
    note = ""
    if best is None and far is not None:
        best, note = far, "research lead dated more than 120 days from the transfer date (same player and clubs)"
    if best is None:
        early = bool(d) and (season_of(d) or "9999") < "2002-03"
        if r["lead_section"] not in ("B", "C") or not early:
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
                    "to_club_id": toid or "", "type": "permanent", "date": d, "date_basis": basis,
                    "found_via": "research lead (private ChatGPT files; not in the Wikipedia lists)", "parent_transfer_id": "", "_ev": []}
            group_new[gk] = best
            transfers.append(best)
            idx[last].append(best)
    if any(e["url"] == r["url"] and e["fee_text"] == r["fee_as_reported"] for e in best["_ev"]):
        continue  # the same source and figure already attached (research sections repeat each other)
    grade = r["grade"] if r["grade"] in GRADE_RANK else "D"
    sid = source_id(r["url"], r["publisher"], grade, "press_or_club")
    parsed = L.parse_fee(r["fee_as_reported"])
    gp = L.parse_fee(r.get("guaranteed_part", "")) if r.get("guaranteed_part", "").strip().upper() not in ("", "NOT FOUND") else None
    if gp and gp["amount"] and gp["currency"] and "up_to" not in gp["qualifiers"]:
        parsed = dict(parsed, amount=gp["amount"], currency=gp["currency"], qualifiers=[q for q in parsed["qualifiers"] if q != "up_to"] + ["guaranteed_part"])
    best["_ev"].append({"origin": "research_lead", "source_id": sid, "grade": grade, "fee_text": r["fee_as_reported"],
                        "parsed": parsed, "quote": r["quote"], "url": r["url"],
                        "archive_url": r["archive_url"] if r["archive_url"].startswith("http") else "", "date": d,
                        "lead_id": r["lead_id"], "lead_section": r["lead_section"], "record_type": r["record_type"],
                        "issue_type": r["issue_type"], "grade_note": r["grade_note"], "note": note})

review = {r["check_id"]: r for r in rd("review_decisions.csv")}  # Claude's reading of each Tier 1 quote (phase 2)
checks = defaultdict(list)
for c in rd("runner_checks.csv"):
    rv = review.get(c["check_id"])
    if rv and rv["decision"] == "reject":
        c = dict(c, status="UNVERIFIED", result="REJECTED on review: " + rv["note"])
    elif rv:
        c = dict(c, reviewed=rv["decision"] + (": " + rv["note"] if rv["note"] else ""))
    checks[c["url"]].append(c)
# a figure the runner found at the cited source becomes its own evidence row (VERIFIED, graded by publisher). A check is
# attached only to a transfer that cites that page itself and whose player's surname is the one the runner looked for.
for t in transfers:
    own = {}
    for e in t["_ev"]:
        for u in ([e["url"]] if e["origin"] == "research_lead" else e.get("cite_urls", "").split()):
            own.setdefault(u, e)
    sn = pname(t["player"]).split(" ")[-1] if t["player"] else ""
    amounts = {money(e["parsed"]["amount"]) for e in t["_ev"] if e["parsed"]["amount"] is not None}
    for u, e0 in list(own.items()):
        for c in checks.get(u, []):
            if c["status"] != "VERIFIED" or not sn or L.norm(c.get("near", "")) != sn or c["amount"] not in amounts:
                continue
            if e0["origin"] == "research_lead" and e0["url"] == c["url"] and money(e0["parsed"]["amount"]) == c["amount"]:
                e0["checked"] = c
                continue
            if any(x.get("checked", {}).get("check_id") == c["check_id"] for x in t["_ev"]):
                continue
            sid = source_id(c["url"], urllib.parse.urlparse(c["url"]).netloc, c["grade_by_publisher"], "press_or_club")
            t["_ev"].append({"origin": "runner_check", "source_id": sid, "grade": c["grade_by_publisher"],
                             "fee_text": c["needle"], "parsed": {"amount": float(c["amount"]), "currency": c["currency"], "qualifiers": [], "kind": "fee"},
                             "quote": c["quote"], "url": c["url"], "archive_url": "", "date": t["date"], "checked": c,
                             "note": "figure found at the source cited by the Wikipedia row (scripted check, GitHub runner)"})

# canonical fee per transfer
for t in transfers:
    t["season_attributed"] = season_of(t["date"]) or ""
    cands = []
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
        e["status"] = "VERIFIED" if ck else "UNVERIFIED"
        if ck:
            e["quote"], e["retrieved"] = ck["quote"], ck["retrieved"]
        usable = e["gbp"] is not None and "up_to" not in p["qualifiers"]
        if usable:
            cands.append((0 if e["status"] == "VERIFIED" else 1, GRADE_RANK.get(e["grade"], 3), 0 if e["currency"] == "GBP" else 1,
                          e["date"] or "9999", i, e))
    kinds = [kind_of(e["fee_text"]) for e in t["_ev"] if e["origin"] == "wikipedia_list"]
    if cands:
        cands.sort(key=lambda x: x[:5])
        e = cands[0][5]
        t["canonical"] = e
        t["fee_gbp"] = e["gbp"]
        t["original_amount"], t["currency"] = e["amount"], e["currency"]
        t["fx_rate"] = e["fx"]["fx_rate"] if e["fx"] else ""
        t["fx_date"] = e["fx"]["fx_date"] if e["fx"] else ""
        t["fx_series"] = e["fx"]["fx_series"] if e["fx"] else ""
        rep = "reported" in e["parsed"]["qualifiers"] or "undisclosed" in e["fee_text"].lower() or bool(e.get("grade_note"))
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
tier3 = sorted(t["transfer_id"] for t in transfers if t["tier"] == "3")
sample3 = set(rng.sample(tier3, max(1, round(len(tier3) * 0.05)))) if tier3 else set()
for t in transfers:
    t["tier3_sample"] = "yes" if t["transfer_id"] in sample3 else ""

conflicts = []
for t in transfers:
    vs = [e for e in t["_ev"] if e["gbp"] is not None and "up_to" not in e["parsed"]["qualifiers"]]
    if len({round(e["gbp"]) for e in vs}) < 2:
        continue
    lo, hi = min(e["gbp"] for e in vs), max(e["gbp"] for e in vs)
    same_grade = defaultdict(set)
    for e in vs:
        same_grade[e["grade"]].add(round(e["gbp"]))
    flag = any(len(v) > 1 and (max(v) - min(v)) > 1e6 and (max(v) - min(v)) > 0.1 * min(v) for v in same_grade.values())
    conflicts.append({"transfer_id": t["transfer_id"], "player": t["player"], "from_club": t["from_club"], "to_club": t["to_club"],
                      "date": t["date"], "canonical_gbp": money(t["fee_gbp"]), "canonical_grade": t["grade"],
                      "min_gbp": money(lo), "max_gbp": money(hi), "spread_gbp": money(hi - lo), "versions": len(vs),
                      "tier": t["tier"], "same_grade_gap_over_10pct_and_1m": "yes" if flag else "",
                      "for_luke": "yes" if (flag and t["tier"] == "1") else "",
                      "versions_detail": " | ".join(f"{e['grade']} {e['fee_text'][:60]} ({e['url'][:80]})" for e in vs)})
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
                        "review": (e.get("checked") or {}).get("reviewed", ""), "check_id": (e.get("checked") or {}).get("check_id", "")})
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
         "grade", "tier", "tier_reason", "tier3_sample", "status", "found_via", "parent_transfer_id"]
with open(os.path.join(DATA, "transfers.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow([c.replace("_out", "") for c in TCOLS])
    for t in transfers:
        w.writerow([t.get(c, "") for c in TCOLS])
wr("fee_evidence.csv", ev_rows, ["evidence_id", "transfer_id", "source_id", "origin", "fee_text", "amount", "currency", "qualifiers", "gbp", "grade", "quote",
                                 "quote_words", "url", "archive_url", "cited_urls", "cited_publishers", "retrieved", "status", "canonical", "note", "check_id", "review"])
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
                                "versions", "tier", "same_grade_gap_over_10pct_and_1m", "for_luke", "versions_detail"])
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
v04 = {"XUMADMS": "2.8564", "XUMAFFS": "9.7433", "XUMAILS": "2152.4916", "XUMASPS": "181.055", "XUMANGS": "3.217", "XUMAPES": "247.3737", "XUMAUSS": "1.8127"}
got = {r["series_code"]: r["units_per_gbp"] for r in rd("fx.csv", DATA) if r["date"] == "1992-01-31" and r["series_code"] in v04}
check("Bank of England Jan 1992 monthly averages equal Cowork's V-04 reading", all(abs(float(got.get(k, "nan")) - float(v)) < 1e-9 for k, v in v04.items()),
      f"{len(got)} of 7 series compared")
ecb = {r["month"]: r["gbp_per_eur"] for r in rd("fx_ecb_crosscheck.csv", DATA)}
check("ECB GBP/EUR 1999-01 equals Cowork's V-06 reading (0.7029125)", ecb.get("1999-01") == "0.7029125", f"{len(ecb)} months")
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
