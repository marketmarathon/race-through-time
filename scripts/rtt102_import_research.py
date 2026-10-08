#!/usr/bin/env python3
"""RTT-102 (IQ-17): turn the private research inputs into the public source tables.

    python3 scripts/rtt102_import_research.py <private research/rtt-102 folder> data/rtt-102/source

Reads only the private files listed in their own 00_README.md and refuses to run if any file's SHA-256 differs
from that table (or the IQ-17 brief differs from the hash in the start prompt). Writes public facts only
(DEC-006): publication titles, dates and URLs; each figure as printed; the short wording quoted by the research
or seen at source; Cowork's check results. No private file is copied. Standard library only; deterministic.

Outputs (in the out folder):
  publications.csv          dossier section A (59 publications), plus the data version each falls in
  observations_research.csv dossier section B (110 visits rows) with the 28 S25_TABLE quarter-end rows replaced by
                            all 84 cells of Cowork's copy of the 2025 table
  verification.csv          Cowork's checks at source, V01-V42 and V43-V101, as recorded
  inputs_sha256.csv         the private inputs and their SHA-256 (checked)
"""
import csv
import hashlib
import io
import os
import re
import sys

BRIEF = ("CODE_SESSION_IQ-17_RTT-102_data.md", "28bf52abc316ba4ecf891341345fde4db62fb129b3ff3533f0df677d58a2e569")
# Files whose hash is given in a brief rather than in the README's table (IQ-17b: Cowork's checks V43-V101)
BRIEF_HASHED = [("cowork_similarweb_verification_2026-10-08_IQ17.csv", "eda8fdd8157c6429ba42aca4b667fbd08cf43b9b534927ec9678e2f38d45d3ed")]
DATA_VERSION_DATE = "2024-07-28"  # Similarweb's new data version launched (V32)
TABLE_SITES = {"chatgpt.com": "chatgpt", "gemini.google.com": "gemini", "deepseek.com": "deepseek", "grok.com": "grok",
               "perplexity.ai": "perplexity", "claude.ai": "claude", "meta.ai": "meta_ai"}
ASSISTANT_IDS = {"ChatGPT": "chatgpt", "Bard/Gemini": "gemini", "Claude": "claude", "Copilot": "copilot",
                 "Perplexity": "perplexity", "DeepSeek": "deepseek", "Grok": "grok", "Meta AI": "meta_ai",
                 "Le Chat": "le_chat"}


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_hashes(src):
    readme = open(os.path.join(src, "00_README.md"), encoding="utf-8").read()
    rows = re.findall(r"^\| ([^|]+?) \|.*\| ([0-9a-f]{64}) \|$", readme, re.M)
    if len(rows) != 11:
        sys.exit(f"expected 11 hashed files in 00_README.md, found {len(rows)}")
    out = []
    for name, want in rows + [BRIEF] + BRIEF_HASHED:
        got = sha256(os.path.join(src, name))
        if got != want:
            sys.exit(f"SHA-256 mismatch for {name}: {got} != {want}")
        out.append((name, os.path.getsize(os.path.join(src, name)), got, "matches 00_README.md" if (name, want) in rows else "matches the hash in the IQ-17 / IQ-17b brief"))
    for name in sorted(os.listdir(src)):  # the three prompts carry no hash in the README: record theirs
        if name.startswith("RTT-102_chatgpt_") or name == "00_README.md":
            out.append((name, os.path.getsize(os.path.join(src, name)), sha256(os.path.join(src, name)), "recorded here (no hash in 00_README.md)"))
    return out


def csv_blocks(text):
    return [b.strip() for b in re.findall(r"```csv\n(.*?)```", text, re.S)]


def data_version(pub_date):
    if not re.match(r"\d{4}-\d{2}-\d{2}$", pub_date):
        return "current"  # undated Similarweb website profiles show September 2026
    return "older" if pub_date < DATA_VERSION_DATE else "current"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    hashes = check_hashes(src)
    dossier = open(os.path.join(src, "part04b_prompt3_quarterly_dossier.txt"), encoding="utf-8").read()
    sec_a = dossier.split("## A. Publication list")[1].split("## B. Visits figures")[0]
    sec_b = dossier.split("## B. Visits figures")[1].split("## C. Coverage grid")[0]

    pubs = list(csv.DictReader(io.StringIO(csv_blocks(sec_a)[0])))
    assert len(pubs) == 59, len(pubs)
    with open(os.path.join(out, "publications.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["pub_id", "title", "publisher", "author", "publication_date", "source_type", "data_version", "url"])
        for p in pubs:
            w.writerow([p["pub_id"], p["title"], p["publisher"], p["author"], p["publication_date"], p["source_type"],
                        data_version(p["publication_date"]), p["source_url"]])
    pub_date = {p["pub_id"]: p["publication_date"] for p in pubs}

    b_rows = []
    for block in csv_blocks(sec_b):
        b_rows += list(csv.DictReader(io.StringIO(block)))
    assert len(b_rows) == 110, len(b_rows)
    table = list(csv.DictReader(open(os.path.join(src, "cowork_similarweb_genai_table_2025_monthly.csv"), encoding="utf-8")))
    assert len(table) == 12

    cols = ["obs_id", "origin", "pub_id", "source_type", "publication_date", "month", "relative_label", "assistant_id",
            "site_as_recorded", "visits_as_published", "qualifier", "quote_as_recorded", "url"]
    rows = []
    n = 0
    for r in b_rows:
        if r["pub_id"] == "S25_TABLE":
            continue  # replaced below by all 84 cells read at source by Cowork (V01)
        n += 1
        rows.append([f"B{n:03d}", "dossier B", r["pub_id"], r["source_type"], r["publication_date"], r["month"],
                     r["relative_label"], ASSISTANT_IDS[r["assistant"]], r["site_domain"], r["visits_as_published"],
                     r["qualifier"], r["exact_quote"], r["source_url"]])
    url_table = next(p["source_url"] for p in pubs if p["pub_id"] == "S25_TABLE")
    for t in table:
        for site, aid in TABLE_SITES.items():
            rows.append([f"T{t['month']}-{aid}", "2025 table (Cowork V01)", "S25_TABLE", "S", pub_date["S25_TABLE"],
                         t["month"], "", aid, site, t[site], "", "table cell", url_table])
    with open(os.path.join(out, "observations_research.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        w.writerows(rows)

    ver = list(csv.reader(open(os.path.join(src, "cowork_similarweb_verification_2026-10-07.csv"), encoding="utf-8")))
    assert ver[0][0] == "check_id" and len(ver) == 43, len(ver)
    ver2 = list(csv.reader(open(os.path.join(src, BRIEF_HASHED[0][0]), encoding="utf-8")))
    assert ver2[0] == ver[0] and len(ver2) == 60, len(ver2)
    ver += ver2[1:]  # V01-V42 (7-8 Oct) then V43-V101 (IQ-17b)
    with open(os.path.join(out, "verification.csv"), "w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(ver)

    with open(os.path.join(out, "inputs_sha256.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["private_file", "bytes", "sha256", "check"])
        for h in sorted(set(hashes)):
            w.writerow(h)
    print(f"publications {len(pubs)}, observations {len(rows)} (dossier B {n} + table 84), checks {len(ver) - 1}")


if __name__ == "__main__":
    main()
