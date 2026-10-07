#!/usr/bin/env python3
"""RTT-101 (IQ-15): turn the private ChatGPT research files into lead evidence rows (UNVERIFIED leads only).

Reads the private folder (never committed, DEC-006) and writes data/rtt-101/source/leads_evidence.csv with only
public facts: date, player, clubs, the fee text as the cited source states it, the source's grade under our rules,
publisher, a quote under 25 words FROM THE CITED SOURCE, and its URL. ChatGPT's own notes are not copied.
Rows from part14b that repeat a section B row (same URL and fee) are matched, not added (brief section 3).
Usage: rtt101_extract_leads.py PRIVATE_DIR OUT_CSV"""
import csv, hashlib, os, re, sys

PRIV, OUT = sys.argv[1], sys.argv[2]
FILES = [("part09b_prompt2_biggest_transfers_B_1992-2000.csv", "B"),
         ("part10b_premier_league_biggest_transfers_B_2001-2008_2026-10-06.csv", "B"),
         ("part11_premier_league_biggest_transfers_B_2009-2016_2026-10-06.csv", "B"),
         ("part12b_premier_league_biggest_transfers_B_2017-2021_2026-10-06.csv", "B"),
         ("part13b_premier_league_biggest_transfers_B_2022-2026_2026-10-06.csv", "B"),
         ("part14b_premier_league_transfer_conflicts_C_2026-10-06.csv", "C"),
         ("part09c_prompt2_record_transfer_evidence_A_PARTIAL_v2_777rows.csv", "A")]
REPORTED = re.compile(r"\b(reported|believed|thought to be|understood|in the region of|around|about|some)\b", re.I)
UEFA = re.compile(r"uefa\.com", re.I)


def grade(row):
    g = (row.get("grade") or "").strip().upper()
    q = (row.get("exact_quote", "") + " " + row.get("fee_as_reported", ""))
    # brief section 7: UEFA.com news of another party's fee = B; "reported"/"thought to be" rows = reported (B)
    if g == "A" and (UEFA.search(row.get("source_url", "")) or REPORTED.search(q)):
        return "B", "graded A in the research file; treated as reported (B)"
    return g, ""


cols = ["lead_id", "lead_section", "lead_file_sha256_prefix", "lead_row", "transfer_ref", "date", "date_type", "player",
        "from_club", "to_club", "fee_as_reported", "currency", "guaranteed_part", "add_ons_part", "grade", "grade_note",
        "publisher", "quote", "quote_words", "url", "archive_url", "issue_type", "record_type"]
rows, seen_b = [], set()
for fn, sec in FILES:
    p = os.path.join(PRIV, fn)
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    for r in csv.DictReader(open(p, encoding="utf-8-sig")):
        url = (r.get("source_url") or "").strip()
        if "transfermarkt" in url.lower():
            continue  # DEC-236: nothing taken from Transfermarkt is stored
        key = (url, (r.get("fee_as_reported") or "").strip())
        if sec == "B":
            seen_b.add(key)
        elif sec == "C" and key in seen_b:
            continue  # repeat of a section B row: matched by source, not added
        g, gn = grade(r)
        q = (r.get("exact_quote") or "").strip()
        rid = r.get("evidence_id") or r.get("record_id")
        rows.append({"lead_id": f"L-{rid}", "lead_section": sec, "lead_file_sha256_prefix": sha, "lead_row": rid,
                     "transfer_ref": r.get("transfer_id") or r.get("related_B_transfer_id") or r.get("case_id") or "",
                     "date": r.get("date", ""), "date_type": r.get("date_type", ""), "player": r.get("player", ""),
                     "from_club": r.get("from_club", ""), "to_club": r.get("to_club", ""),
                     "fee_as_reported": r.get("fee_as_reported", "").strip(), "currency": r.get("currency", ""),
                     "guaranteed_part": r.get("guaranteed_part", ""), "add_ons_part": r.get("add_ons_part", ""),
                     "grade": g, "grade_note": gn, "publisher": r.get("publisher", ""), "quote": q,
                     "quote_words": len(q.split()), "url": url, "archive_url": r.get("archive_url", ""),
                     "issue_type": r.get("issue_type", ""), "record_type": r.get("record_type", "")})
rows.sort(key=lambda x: x["lead_id"])
w = csv.DictWriter(open(OUT, "w", newline="", encoding="utf-8"), fieldnames=cols)
w.writeheader(); w.writerows(rows)
print(len(rows), "lead rows;", sum(1 for r in rows if r["quote_words"] >= 25), "quotes of 25+ words")
