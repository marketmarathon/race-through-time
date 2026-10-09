#!/usr/bin/env python3
"""RTT-101 (IQ-15): turn the private ChatGPT research files into lead evidence rows (UNVERIFIED leads only).

Reads the private folder (never committed, DEC-006) and writes data/rtt-101/source/leads_evidence.csv with only
public facts: date, player, clubs, the fee text as the cited source states it, the source's grade under our rules,
publisher, a quote under 25 words FROM THE CITED SOURCE, and its URL. ChatGPT's own notes are not copied.
Rows from part14b that repeat a section B row (same URL and fee) are matched, not added (brief section 3).
Usage: rtt101_extract_leads.py PRIVATE_DIR OUT_CSV"""
import csv, hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PRIV, OUT = sys.argv[1], sys.argv[2]
FILES = [("part09b_prompt2_biggest_transfers_B_1992-2000.csv", "B"),
         ("part10b_premier_league_biggest_transfers_B_2001-2008_2026-10-06.csv", "B"),
         ("part11_premier_league_biggest_transfers_B_2009-2016_2026-10-06.csv", "B"),
         ("part12b_premier_league_biggest_transfers_B_2017-2021_2026-10-06.csv", "B"),
         ("part13b_premier_league_biggest_transfers_B_2022-2026_2026-10-06.csv", "B"),
         ("part14b_premier_league_transfer_conflicts_C_2026-10-06.csv", "C"),
         ("part09c_prompt2_record_transfer_evidence_A_PARTIAL_v2_777rows.csv", "A")]
# 1992-2007 gap lists (DEC-264): every CSV named part*_gaps_*.csv, as section "G" (leads only; fees checked at source)
import glob as _glob
_latest = {}
for f in sorted(_glob.glob(os.path.join(PRIV, "part*_gaps_*.csv"))):
    m = re.search(r"_gaps_([ABC])_", os.path.basename(f))  # sections A-C are transfer lists; D is conflicts/warnings (notes only)
    if m:
        _latest[m.group(1)] = f  # a later part replaces an earlier one (part19b replaces part18b)
FILES += [(os.path.basename(f), "G") for _, f in sorted(_latest.items())]
# source rounds (DEC-275): ChatGPT's press/club sources for named deals, section "S"; each row carries our deal_id, mapped to a
# transfer_id by data/rtt-101/source/source_round1_map.csv (built from the lists Cowork sent, player + date)
FILES += [(os.path.basename(f), "S") for f in sorted(_glob.glob(os.path.join(PRIV, "part2*_sources_round*_*.csv")))]
# source round 2 (IQ-15h): Claude helper research on the priority list, all rows combined in part23g (part22c and part23a-f are the same
# rows split by batch, so only part23g is read); deal IDs R0001-R0755 map through source_round2_map.csv
FILES += [(os.path.basename(f), "S") for f in sorted(_glob.glob(os.path.join(PRIV, "part23g_claude_round2_ALL_*.csv")))]
# source round 3 (IQ-15i): the undisclosed-fee sweep (part24a/e/f/g, U deal IDs via source_round3_map.csv) and the leader deals read by Cowork in
# Luke's Chrome (part24d) or by a helper (part24b), R deal IDs via source_round2_map.csv; part24c (round-up pages) is context only, not read
FILES += [(os.path.basename(f), "S") for f in sorted(_glob.glob(os.path.join(PRIV, "part24[abdefg]_*.csv")))]
# source round 4 (IQ-15k): the three leaders' undisclosed deals (part25a batch 1, part25c batch 2; U deal IDs via source_round3_map.csv)
# and the six January 2020 leader deals (part25d; deal_id = our transfer_id). part25b (Cowork's Chrome reads of the 12 round 3 pages
# the runner could not read) is recorded in source/round4_chrome_reads.csv instead: it gives no grade A/B figure
FILES += [(os.path.basename(f), "S") for f in sorted(_glob.glob(os.path.join(PRIV, "part25[acd]_*.csv")))]
# source round 5 (IQ-15l): the fees that decide the finish (part26a, deal_id = our transfer_id) and Cowork's reads of the cited pages in
# Luke's Chrome (part26b, keyed by transfer_id; its columns are mapped to the research columns below)
FILES += [(os.path.basename(f), "S") for f in sorted(_glob.glob(os.path.join(PRIV, "part26[ab]_*.csv")))]
_MAP = {"Tf8a5f7e6ee": "T6403be737e"}  # IQ-15k: Hector's club-season duplicate is dropped; his one Chelsea -> Fulham move (DEC-436)
for _name in ("source_round1_map.csv", "source_round2_map.csv", "source_round3_map.csv"):
    _mp = os.path.join(os.path.dirname(os.path.abspath(OUT)), _name)
    if os.path.exists(_mp):
        for _r in csv.DictReader(open(_mp, encoding="utf-8")):
            _MAP.setdefault(_r["deal_id"], _r["transfer_id"])  # a part-exchange pair maps to two transfers: the first carries the deal
REPORTED = re.compile(r"\b(reported|believed|thought to be|understood|in the region of|around|about|some)\b", re.I)
UEFA = re.compile(r"uefa\.com", re.I)


# round 2 (IQ-15h): aggregator, scores, blog and fan sites are pointers (C) whatever grade the research file gives; a contemporary agency
# copy or regional paper stays B (the helpers' notes name the agency); a post resting only on social media is C
AGGREGATOR = re.compile(r"(flashscore|sportskeeda|90min\.com|getfootballnews|football-espana|worldsoccertalk|soccernews\.com|sportsmole|newswav|"
                        r"hitc\.com|footballtransfers|vavel|fichajes|thehardtackle|sixonefivesoccer|lastwordonsports|planetfootball|fotmob|"
                        r"sofascore|soccerway|bleacherreport|foot01|maxifoot|sporting-heroes|africasoccer|soccernet\.ng|kahawatungu|"
                        r"football365|myfootball\.com\.au|sportsnews\.com\.au)", re.I)


# round 4 (IQ-15k, DEC-420 (a)): the sites batch 1's helpers graded B are aggregators too, unless the helper's note says the page itself is syndicated agency copy
# Sporting Life is not in this list: the build has always graded it B (15 fees in use rest on it); Luke decides (DEC-438, question 1)
AGGREGATOR4 = re.compile(r"(goal\.com|90min|fourfourtwo|thescore\.com|football-espana|teamtalk)", re.I)
SI90 = re.compile(r"(^|//|\.)si\.com/", re.I)  # Sports Illustrated's own reporting stays as graded; its pages carrying 90min copy are C
AGENCY = re.compile(r"syndicated copy of (?:PA|Reuters|AFP|AP|the Press Association|Associated Press)\b")  # the page itself is agency copy


# round 5 (IQ-15l): agency copy on a foreign site keeps the agency's grade B only where the page credits the agency (the helper's or
# Cowork's note says so: "page credits Reuters", "text credited to AFP", "dateline LONDON (AP)", "'— Reuters' at the end")
FOREIGN = re.compile(r"(omanobserver|thejakartapost|tsn\.ca|supersport|malaymail|morungexpress|ahram\.org|gulfnews|iol\.co\.za|channelstv|"
                     r"aljazeera|mg\.co\.za|tribune\.com\.pk|the-star\.co\.ke)", re.I)
CREDITED = re.compile(r"(syndicated copy of|(?:Reuters|AFP|AP|Sapa-AP) copy|credit|dateline|footer shows|ends '|— ?Reuters|- AFP|\(AP\)|"
                      r"byline[^.;]*(?:Reuters|Agence France|AFP))", re.I)
UNCREDITED = re.compile(r"no agency credit|NOT confirmed", re.I)


def grade(row):
    g = (row.get("grade") or "").strip().upper()
    if row.get("_round5") and g == "B" and "eredivisie.com" in row.get("source_url", "") and "Ajax" in row.get("notes", "") and "statement" in row.get("notes", ""):
        return "A", "the club's own statement (Ajax), reproduced word for word by the league with its credit: grade A (contract §3, IQ-15l)"
    if row.get("_round5") and g in ("A", "B") and FOREIGN.search(row.get("source_url", "")) and (
            not CREDITED.search(row.get("notes", "")) or UNCREDITED.search(row.get("notes", ""))):
        return "C", "agency copy on a foreign site without an agency credit on the page: a pointer (C) (IQ-15l)"
    if row.get("_round2") and g in ("A", "B") and AGGREGATOR.search(row.get("source_url", "")):
        return "C", "aggregator, scores, blog or fan site: a pointer (C), whatever the research file says"
    agg4 = AGGREGATOR4.search(row.get("source_url", "")) or (SI90.search(row.get("source_url", "")) and re.search(r"90 ?min", row.get("notes", ""), re.I))
    if row.get("_round4") and g in ("A", "B") and agg4 and not AGENCY.search(row.get("notes", "")):
        return "C", "aggregator site with no agency named: a pointer (C), whatever the research file says (DEC-420 (a), IQ-15k)"
    q = (row.get("exact_quote", "") + " " + row.get("fee_as_reported", ""))
    # brief section 7: UEFA.com news of another party's fee = B; "reported"/"thought to be" rows = reported (B)
    if g == "A" and (UEFA.search(row.get("source_url", "")) or REPORTED.search(q)):
        return "B", "graded A in the research file; treated as reported (B)"
    return g, ""


cols = ["lead_id", "lead_section", "lead_file_sha256_prefix", "lead_row", "transfer_ref", "date", "date_type", "player",
        "from_club", "to_club", "fee_as_reported", "currency", "guaranteed_part", "add_ons_part", "grade", "grade_note",
        "publisher", "quote", "quote_words", "url", "archive_url", "issue_type", "record_type", "published", "lead_type"]
rows, seen_b, _seq = [], set(), {}
for fn, sec in FILES:
    p = os.path.join(PRIV, fn)
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    _r26a = {}
    if fn.startswith("part26b"):  # grade each Chrome read like the research row citing the same page, else by its publisher
        for _x in csv.DictReader(open(os.path.join(PRIV, next(f for f, _ in FILES if f.startswith("part26a"))), encoding="utf-8-sig")):
            _r26a.setdefault(_x["source_url"].strip(), (_x.get("grade (A/B/C)") or _x.get("grade"), _x.get("notes", "")))
    for r in csv.DictReader(open(p, encoding="utf-8-sig")):
        if fn.startswith("part26b"):
            import rtt101_lib as _L
            _u = (r.get("url") or "").strip()
            if _u and not _u.startswith("http"):
                _u = "https://n" + _u if _u.startswith("ews.bbc.co.uk") else "https://" + _u
            _g, _hn = _r26a.get(_u) or ({"A": "A", "B": "B"}.get(_L.grade_of(_u), "C"), "")
            if _g == "C" and FOREIGN.search(_u) and CREDITED.search(r.get("note", "")):
                _g = "B"  # Cowork's note says the page credits the agency
            r = {"deal_id": r["transfer_id"], "player": r["player"], "from_club": "", "to_club": "", "fee_as_reported": r["fee_as_read"],
                 "currency": "", "guaranteed_part": "", "add_ons_part": "", "transfer_date_reported": "", "publisher": r["publisher"],
                 "publication_date": r["publication_date"], "grade": _g, "exact_quote": r["exact_quote"], "source_url": _u,
                 "archive_url": "", "notes": r["note"] + " (" + r["read_id"] + ", read by Cowork in Luke's Chrome " + r["read_on"] + ")"
                 + (" | helper's note on the same page: " + _hn if _hn else "")}
            if r["fee_as_reported"].strip().upper().startswith("NOT READ"):
                continue
        if sec == "G":
            r = dict(r, date=r.get("transfer_date", ""), date_type=r.get("date_basis", ""), evidence_id=r.get("row_id"))
            if "soccerbase" in (r.get("source_url") or "").lower() or (r.get("publisher") or "").lower().startswith("soccerbase"):
                r["grade"] = "C"  # specialist database: a pointer (brief section 7)
        if sec == "S":
            if not r.get("grade") and r.get("grade (A/B/C)"):
                r = dict(r, grade=r["grade (A/B/C)"])  # list B files label the column "grade (A/B/C)"
            if (r.get("fee_as_reported") or "").strip().upper() in ("", "NOT FOUND"):
                continue  # deal not found: nothing to check
            _n = _seq.setdefault(r["deal_id"], 0) + 1
            _seq[r["deal_id"]] = _n
            _tid = _MAP.get(r["deal_id"], "") or (r["deal_id"] if re.fullmatch(r"T[0-9a-f]{10}", r["deal_id"]) else "")
            r = dict(r, evidence_id=f"{r['deal_id']}-{_n:02d}", transfer_id=_tid, date=r.get("transfer_date_reported", ""))
            if "soccerbase" in (r.get("source_url") or "").lower() or (r.get("publisher") or "").lower().startswith("soccerbase"):
                r["grade"] = "C"
            if fn.startswith(("part22", "part23", "part24", "part25")):
                r["_round2"] = True
            if fn.startswith(("part25", "part26")):
                r["_round4"] = True
            if fn.startswith("part26"):
                r["_round5"] = True
        url = (r.get("source_url") or "").strip()
        url = re.sub(r"^https?://acc-english\.ajax\.nl", "https://english.ajax.nl", url)  # a copy of the same Ajax page (Cowork, IQ-15h)
        if "transfermarkt" in url.lower() or "wikipedia.org" in url.lower():
            continue  # DEC-236: nothing taken from Transfermarkt is stored; Wikipedia is never the source of a fee
        key = (url, (r.get("fee_as_reported") or "").strip())
        if sec == "B":
            seen_b.add(key)
        elif sec == "C" and key in seen_b:
            continue  # repeat of a section B row: matched by source, not added
        g, gn = grade(r)
        q = (r.get("exact_quote") or "").strip()
        if len(q.split()) >= 25:
            # quotes stay under 25 words (contract): keep the 22 words around the first figure, marking the cuts
            ws = q.split()
            k = next((n for n, w_ in enumerate(ws) if re.search(r"[£€$]|\d", w_)), 0)
            a = max(0, min(k - 10, len(ws) - 22))
            q = ("[…] " if a > 0 else "") + " ".join(ws[a:a + 22]) + (" […]" if a + 22 < len(ws) else "")
        rid = r.get("evidence_id") or r.get("record_id")
        if sec in ("G", "S"):
            rid = fn.split("_")[0] + "-" + rid  # e.g. part18b-A0001 (gap-list rows reuse letters used elsewhere)
        rows.append({"lead_id": f"L-{rid}", "lead_section": sec, "lead_file_sha256_prefix": sha, "lead_row": rid,
                     "transfer_ref": r.get("transfer_id") or r.get("related_B_transfer_id") or r.get("case_id") or "",
                     "date": r.get("date", ""), "date_type": r.get("date_type", ""), "player": r.get("player", ""),
                     "from_club": r.get("from_club", ""), "to_club": r.get("to_club", ""),
                     "fee_as_reported": r.get("fee_as_reported", "").strip(), "currency": r.get("currency", ""),
                     "guaranteed_part": r.get("guaranteed_part", ""), "add_ons_part": r.get("add_ons_part", ""),
                     "grade": g, "grade_note": gn, "publisher": r.get("publisher", ""), "quote": q,
                     "quote_words": len(q.split()), "url": url, "archive_url": r.get("archive_url", ""),
                     "issue_type": r.get("issue_type", ""), "record_type": r.get("record_type", ""),
                     "published": (r.get("publication_date") or "") if re.match(r"\d{4}-\d{2}-\d{2}", r.get("publication_date") or "") else "",
                     "lead_type": r.get("type", "")})
rows.sort(key=lambda x: x["lead_id"])
w = csv.DictWriter(open(OUT, "w", newline="", encoding="utf-8"), fieldnames=cols)
w.writeheader(); w.writerows(rows)
print(len(rows), "lead rows;", sum(1 for r in rows if r["quote_words"] >= 25), "quotes of 25+ words")

# ---- dated moments (part15b, grades A/B only) -> data/rtt-101/source/moments_leads.csv (UNVERIFIED leads)
MOM = os.path.join(os.path.dirname(OUT), "moments_leads.csv")
mrows, done = [], set()
fn = "part15b_premier_league_dated_moments_D_2026-10-06.csv"
msha = hashlib.sha256(open(os.path.join(PRIV, fn), "rb").read()).hexdigest()[:16]
for r in csv.DictReader(open(os.path.join(PRIV, fn), encoding="utf-8-sig")):
    if r["grade"] not in ("A", "B") or r["event_id"] in done or "transfermarkt" in r["source_url"].lower():
        continue
    done.add(r["event_id"])
    est = r["event_category"] == "RECORD_WINDOW"
    mrows.append({"moment_id": "M-" + r["event_id"], "date": r["date"], "category": r["event_category"].lower(), "clubs": r["clubs"],
                  "event": r["event"], "grade": r["grade"], "publisher": r["publisher"], "quote": r["exact_quote"],
                  "quote_words": len(r["exact_quote"].split()), "url": r["source_url"], "status": "UNVERIFIED",
                  "use_note": ("league-wide total from an analyst or the press: label as an estimate, never official, never split across clubs"
                               if est else ""), "lead_file_sha256_prefix": msha})
mrows.append({"moment_id": "M-PL-2026-09-29", "date": "2026-09-29", "category": "regulatory", "clubs": "Manchester City",
              "event": "Premier League statement on the independent Commission's decision in the Manchester City case; sanction to be decided at a further hearing",
              "grade": "A", "publisher": "Premier League", "quote": "the issue of sanction will be addressed separately in a further hearing with the independent Commission",
              "quote_words": 16, "url": "https://www.premierleague.com/en/news/4727779/premier-league-statement-manchester-city-fc/",
              "status": "VERIFIED (Claude in Cowork, web fetch, 7 Oct 2026; re-read word for word in Luke's Chrome before any on-screen use)",
              "use_note": "topical hook only, neutral wording; the case concerns financial rules, not transfer spending: never place it so it implies spending was wrongdoing; say the club has appealed (1 Oct 2026, UNVERIFIED)",
              "lead_file_sha256_prefix": ""})
mrows.sort(key=lambda r: (r["date"], r["moment_id"]))
with open(MOM, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(mrows[0])); w.writeheader(); w.writerows(mrows)
print(len(mrows), "moments")

# ---- league-wide window totals (part17b, grades A/B) -> data/rtt-101/source/window_totals_leads.csv (cross-check only)
WT = os.path.join(os.path.dirname(OUT), "window_totals_leads.csv")
fn = "part17b_premier_league_season_totals_F_2026-10-07.csv"
wsha = hashlib.sha256(open(os.path.join(PRIV, fn), "rb").read()).hexdigest()[:16]
wrows = []
for r in csv.DictReader(open(os.path.join(PRIV, fn), encoding="utf-8-sig")):
    m = re.match(r"F-(\d{4})-(JAN|SUM)$", r["window_id"])
    if not m or r["grade"] not in ("A", "B"):
        continue
    import rtt101_lib as L
    g, n = L.parse_fee(r["gross_spend_as_reported"]), L.parse_fee(r["net_spend_as_reported"])
    wrows.append({"window": ("January " if m.group(2) == "JAN" else "summer ") + m.group(1), "grade": r["grade"], "publisher": r["publisher"],
                  "gross_as_reported": r["gross_spend_as_reported"], "gross_gbp": g["amount"] if g["currency"] == "GBP" else "",
                  "net_as_reported": r["net_spend_as_reported"],
                  "net_gbp": ((-n["amount"] if (re.match(r"\s*[−-]", r["net_spend_as_reported"]) or re.search(r"profit|receipts", r["net_spend_as_reported"], re.I)) else n["amount"]) if n["currency"] == "GBP" else ""),
                  "method": r["method"][:160], "url": r["source_url"], "status": "UNVERIFIED (research lead)", "lead_file_sha256_prefix": wsha})
with open(WT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(wrows[0])); w.writeheader(); w.writerows(wrows)
print(len(wrows), "window-total lead rows")
