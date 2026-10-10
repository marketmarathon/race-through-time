#!/usr/bin/env python3
"""RTT-104 Women in Parliament (IQ-20): fetch the sources the Claude Code cloud container cannot reach.

Run on a GitHub-hosted runner by .github/workflows/rtt104_sources.yml. The container's network policy blocks
api.worldbank.org, ourworldindata.org, ipu.org and data.ipu.org.

Open-licence data files (World Bank WDI API JSON, CC BY 4.0; Our World in Data grapher CSV, CC BY 4.0) are kept
byte for byte in data/rtt-104/source/raw/. Web pages (terms of use, IPU Parline country pages, metadata pages) are
NOT kept: only their SHA-256, size and the paragraphs that hold the searched words (short quotes for the record) go
to data/rtt-104/source/page_excerpts/. Every file's URL, UTC fetch time, HTTP status, bytes and SHA-256 go to
data/rtt-104/source/fetch_manifest.json. The log prints IDs, sizes, hashes and the excerpts (all public pages).

IQ-20 round 2 (FETCH_SET=parline): only the IPU Parline pages of the economies with no 2025 figure, read from the
round-1 WDI file (ROUND1 below), with a narrow filter that skips the site's country menu (round 1 caught only the menu).

IQ-20 round 3 (FETCH_SET=archive): IPU's archived monthly rankings (archive.ipu.org, static HTML, 1997-2018), to test
which date a WDI year's figure describes. Only the table rows naming the test countries are kept.

Usage: rtt104_fetch_sources.py <out_dir>      Standard library only (plus pdftotext for the one PDF).
"""
import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
WB = "https://api.worldbank.org/v2"

DATA = [  # (id, url, file name) - kept byte for byte
    ("WDI-PARL-ALL", f"{WB}/country/all/indicator/SG.GEN.PARL.ZS?format=json&per_page=20000&date=1997:2025&footnote=y",
     "wdi_SG.GEN.PARL.ZS_all_1997-2025.json"),
    ("WDI-PARL-WLD", f"{WB}/country/WLD/indicator/SG.GEN.PARL.ZS?format=json&per_page=200&date=1997:2025&footnote=y",
     "wdi_SG.GEN.PARL.ZS_WLD_1997-2025.json"),
    ("WDI-POP-ALL", f"{WB}/country/all/indicator/SP.POP.TOTL?format=json&per_page=20000&date=1997:2026",
     "wdi_SP.POP.TOTL_all_1997-2026.json"),
    ("WDI-COUNTRIES", f"{WB}/country?format=json&per_page=400", "wdi_country_list.json"),
    ("WDI-IND-PARL", f"{WB}/indicator/SG.GEN.PARL.ZS?format=json", "wdi_indicator_SG.GEN.PARL.ZS.json"),
    ("WDI-IND-POP", f"{WB}/indicator/SP.POP.TOTL?format=json", "wdi_indicator_SP.POP.TOTL.json"),
    ("WDI-META-PARL", f"{WB}/sources/2/series/SG.GEN.PARL.ZS/metadata?format=json", "wdi_metadata_SG.GEN.PARL.ZS.json"),
    ("WDI-META-POP", f"{WB}/sources/2/series/SP.POP.TOTL/metadata?format=json", "wdi_metadata_SP.POP.TOTL.json"),
    ("WDI-SOURCE", f"{WB}/sources/2?format=json", "wdi_source_2.json"),
    ("OWID-CSV", "https://ourworldindata.org/grapher/share-of-women-in-parliament-ipu.csv?v=1&csvType=full&useColumnShortNames=false",
     "owid_share-of-women-in-parliament-ipu.csv"),
    ("OWID-META", "https://ourworldindata.org/grapher/share-of-women-in-parliament-ipu.metadata.json?v=1&csvType=full&useColumnShortNames=false",
     "owid_share-of-women-in-parliament-ipu.metadata.json"),
]

TERMS_WORDS = r"commercial|licen[cs]e|copyright|reus|re-us|attribut|permission|third.part|creative commons|CC BY|terms|redistribut|sell|sale|dataset|data set|proprietary|acknowledg"
PAGES = [  # (id, url, regex of words whose paragraphs are kept) - excerpts only
    ("WB-TERMS-DATASETS", "https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets", TERMS_WORDS),
    ("WB-PUBLIC-LICENSES", "https://datacatalog.worldbank.org/public-licenses", TERMS_WORDS),
    ("WB-INDICATOR-PAGE", "https://data.worldbank.org/indicator/SG.GEN.PARL.ZS", TERMS_WORDS + r"|as of|January|IPU|Inter-Parliamentary"),
    ("IPU-TERMS", "https://www.ipu.org/terms-use", TERMS_WORDS),
    ("IPU-PARLINE-ABOUT", "https://data.ipu.org/about", TERMS_WORDS + r"|open|free"),
    ("IPU-PARLINE-HOME", "https://data.ipu.org/", TERMS_WORDS),
    ("IPU-WOMEN-RANKING", "https://data.ipu.org/women-ranking?month=1&year=2025", r"as of|January|situation|ranking|data|note|vacan|occupied|seats|commercial|licen"),
    ("IPU-WOMEN-AVERAGES", "https://data.ipu.org/women-averages", r"as of|January|situation|average|note|seats"),
    ("OWID-FAQ-LICENCE", "https://ourworldindata.org/faqs", TERMS_WORDS),
    ("UN-SDG-META-551A", "https://unstats.un.org/sdgs/metadata/files/Metadata-05-05-01a.pdf",
     r"1 January|as of|as at|reference|periodicity|lower|single|chamber|vacan|occupied|appointed|elected|data availability|release|calendar"),
]
PARLINE_NARROW = (r"dissol|suspen|coup|militar|seiz|takeover|transition|interim|no longer|not function|expired|lapse|"
                  r"vacan|ceased|postpon|Taliban|junta|prorog|status|state of emergency|decree|last election|next election|"
                  r"renewal|term of|mandate")
ROUND1 = "data/rtt-104/source/fetch_2026-10-10_run38029495926/raw"
MENU = re.compile(r"^[A-Z][^|\d.;:]{1,50} - [A-Z][^\s|]*(?: [^\s|]+){0,5}$")  # "Country - Chamber name" menu entries
PARLINE_WORDS = (r"dissol|suspend|suspension|coup|transition|military|no parliament|not functioning|no longer|"
                 r"elections? (?:held|postponed|scheduled|due)|interim|status|last election|mandate|expired|vacan|"
                 r"National Assembly|Parliament|Jirga|Majlis|Hluttaw|Congress|Chamber|House")


def fetch(url, tries=3):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-GB,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read(), r.geturl()
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (403, 404, 410):
                break
        except Exception as e:  # listed, not fatal
            last = f"{type(e).__name__}: {e}"
        time.sleep(4)
    return None, last, None, url


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def to_text(body, ctype, url):
    if body[:4] == b"%PDF":
        p = subprocess.run(["pdftotext", "-layout", "-", "-"], input=body, capture_output=True)
        return p.stdout.decode("utf-8", "replace")
    t = body.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", t)
    t = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|td|th|dd|dt|section|article)>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in t.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def excerpts(text, words, limit=60):
    """Lines holding the words, each with the line before and after (no more than `limit` blocks, 700 chars each)."""
    lines = text.splitlines()
    rx = re.compile(words, re.I)
    out, used = [], set()
    for i, ln in enumerate(lines):
        if rx.search(ln) and i not in used:
            block = [lines[j] for j in range(max(0, i - 1), min(len(lines), i + 2)) if j not in used]
            used.update(range(max(0, i - 1), min(len(lines), i + 2)))
            out.append(" | ".join(block)[:700])
            if len(out) >= limit:
                break
    return out


def parline_round(out):
    exc = os.path.join(out, "page_excerpts")
    os.makedirs(exc, exist_ok=True)
    manifest = {"fetched_by": "GitHub runner, .github/workflows/rtt104_sources.yml (FETCH_SET=parline)",
                "run_url": os.environ.get("RUN_URL", ""), "files": [], "pages": []}
    parl = json.load(open(os.path.join(ROUND1, "wdi_SG.GEN.PARL.ZS_all_1997-2025.json")))[1]
    ctry = json.load(open(os.path.join(ROUND1, "wdi_country_list.json")))[1]
    iso2 = {c["id"]: c["iso2Code"] for c in ctry if c["region"]["id"] != "NA"}
    has = {}
    for r in parl:
        c = r["countryiso3code"]
        if c in iso2 and r["value"] is not None:
            has.setdefault(c, set()).add(r["date"])
    missing = sorted(c for c, ys in has.items() if "2025" not in ys)
    if os.environ.get("PARLINE_ISO3"):  # IQ-22 round 4: named economies only (board exits with a gap)
        missing = os.environ["PARLINE_ISO3"].split()
    print("economies with figures but no 2025 figure:", ", ".join(missing))
    for c in missing:
        i2 = iso2[c]
        for sid, url in ((f"IPU-PARLINE2-{c}", f"https://data.ipu.org/parliament/{i2}/"),
                         (f"IPU-PARLINE2-{c}-LC", f"https://data.ipu.org/parliament/{i2}/{i2}-LC01/"),
                         (f"IPU-PARLINE2-{c}-LC-ELECTIONS", f"https://data.ipu.org/parliament/{i2}/{i2}-LC01/elections/"),
                         (f"IPU-OLD-{c}", f"https://www.ipu.org/parlement/{i2}")):
            status, ctype, body, final = fetch(url)
            rec = {"id": sid, "url": url, "fetched_utc": now(), "status": status}
            if body is None:
                rec["error"] = ctype
                print(f"{sid}: FAILED {ctype}")
                manifest["pages"].append(rec)
                continue
            text = to_text(body, ctype, url)
            lines = [ln for ln in text.splitlines() if not MENU.match(ln)]
            ex = excerpts("\n".join(lines), PARLINE_NARROW, limit=25)
            rec.update({"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "content_type": ctype,
                        "final_url": final, "text_chars": len(text), "excerpt_file": f"page_excerpts/{sid}.txt",
                        "excerpts": len(ex)})
            with open(os.path.join(exc, f"{sid}.txt"), "w", encoding="utf-8") as f:
                f.write(f"# {sid}\n# url: {url}\n# final url: {final}\n# fetched (UTC): {rec['fetched_utc']}\n"
                        f"# HTTP {status}; {len(body)} bytes; SHA-256 {rec['sha256']}\n"
                        "# Short excerpts only (lines holding the searched words, with the line before and after).\n\n")
                for e in ex:
                    f.write(e + "\n\n")
            print(f"{sid}: {status} {len(body)} bytes sha256 {rec['sha256']} excerpts {len(ex)}")
            manifest["pages"].append(rec)
            time.sleep(1)
    json.dump(manifest, open(os.path.join(out, "fetch_manifest.json"), "w"), indent=1, sort_keys=True)


ARCHIVE_DATES = ["010197", "100898", "250198", "010103", "010104", "310103", "310104", "010107", "010108", "310107",
                 "310108", "010118", "010119", "010218", "010219", "010113", "010213", "010214"]
ARCHIVE_COUNTRIES = r"Rwanda|Mexico|United Arab Emirates|Sweden|Saudi Arabia|Japan|Nepal|Kuwait|Guinea-Bissau|Bangladesh|Haiti|Sudan"


def archive_round(out):
    exc = os.path.join(out, "page_excerpts")
    os.makedirs(exc, exist_ok=True)
    manifest = {"fetched_by": "GitHub runner, .github/workflows/rtt104_sources.yml (FETCH_SET=archive)",
                "run_url": os.environ.get("RUN_URL", ""), "files": [], "pages": []}
    rx = re.compile(os.environ.get("ARCHIVE_COUNTRIES") or ARCHIVE_COUNTRIES)
    dates = os.environ.get("ARCHIVE_DATES", "").split() or ARCHIVE_DATES
    urls = [(f"IPU-ARCHIVE-{d}", f"http://archive.ipu.org/wmn-e/arc/classif{d}.htm") for d in dates]
    urls.append(("IPU-ARCHIVE-INDEX", "http://archive.ipu.org/wmn-e/classif-arc.htm"))
    for sid, url in urls:
        status, ctype, body, final = fetch(url)
        rec = {"id": sid, "url": url, "fetched_utc": now(), "status": status}
        if body is None:
            rec["error"] = ctype
            print(f"{sid}: FAILED {ctype}")
            manifest["pages"].append(rec)
            continue
        t = body.decode("utf-8", "replace") if b"charset=utf-8" in body[:2000].lower() else body.decode("latin-1")
        title = re.findall(r"(?is)<title>(.*?)</title>", t)
        heads = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()
                 for h in re.findall(r"(?is)<(?:h1|h2|h3|b|strong)[^>]*>(.*?)</(?:h1|h2|h3|b|strong)>", t)][:12]
        rows = []
        for tr in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", t):
            cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
                     for c in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", tr)]
            line = " | ".join(cells)
            if rx.search(line) or (sid.endswith("INDEX") and re.search(r"\d{4}", line)):
                rows.append(line[:400])
        if os.environ.get("ARCHIVE_NOTES"):  # IQ-22: footnotes and other text naming the countries, outside the table
            body_text = to_text(re.sub(r"(?is)<table.*?</table>", " ", t).encode("utf-8"), "", url)
            rows += ["NOTE: " + ln[:400] for ln in body_text.splitlines() if rx.search(ln)][:40]
        rec.update({"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "content_type": ctype,
                    "final_url": final, "excerpt_file": f"page_excerpts/{sid}.txt", "excerpts": len(rows)})
        with open(os.path.join(exc, f"{sid}.txt"), "w", encoding="utf-8") as f:
            f.write(f"# {sid}\n# url: {url}\n# final url: {final}\n# fetched (UTC): {rec['fetched_utc']}\n"
                    f"# HTTP {status}; {len(body)} bytes; SHA-256 {rec['sha256']}\n# title: {title[:1]}\n"
                    f"# headings: {heads}\n# Table rows naming the test countries only.\n\n")
            for r in rows[:80]:
                f.write(r + "\n")
        print(f"{sid}: {status} {len(body)} bytes rows {len(rows)}")
        manifest["pages"].append(rec)
        time.sleep(1)
    json.dump(manifest, open(os.path.join(out, "fetch_manifest.json"), "w"), indent=1, sort_keys=True)


def main():
    out = sys.argv[1]
    if os.environ.get("FETCH_SET") == "round4":  # IQ-22: Parline pages and archived rankings for named countries
        sub = os.path.join(out, "parline")
        parline_round(sub)
        archive_round(os.path.join(out, "archive"))
        return
    if os.environ.get("FETCH_SET") == "archive":
        return archive_round(out)
    if os.environ.get("FETCH_SET") == "parline":
        return parline_round(out)
    raw = os.path.join(out, "raw")
    exc = os.path.join(out, "page_excerpts")
    os.makedirs(raw, exist_ok=True)
    os.makedirs(exc, exist_ok=True)
    manifest = {"fetched_by": "GitHub runner, .github/workflows/rtt104_sources.yml", "run_url": os.environ.get("RUN_URL", ""),
                "files": [], "pages": []}

    for sid, url, name in DATA:
        status, ctype, body, final = fetch(url)
        rec = {"id": sid, "url": url, "fetched_utc": now(), "status": status}
        if body is None:
            rec["error"] = ctype
            print(f"{sid}: FAILED {ctype}")
        else:
            open(os.path.join(raw, name), "wb").write(body)
            rec.update({"file": f"raw/{name}", "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                        "content_type": ctype, "final_url": final})
            print(f"{sid}: {status} {len(body)} bytes sha256 {rec['sha256']}")
        manifest["files"].append(rec)

    # IPU Parline pages for every WDI economy with no 2025 figure (closing-card candidates and the rest), by ISO2
    pages = list(PAGES)
    try:
        parl = json.load(open(os.path.join(raw, "wdi_SG.GEN.PARL.ZS_all_1997-2025.json")))[1]
        ctry = json.load(open(os.path.join(raw, "wdi_country_list.json")))[1]
        iso2 = {c["id"]: c["iso2Code"] for c in ctry if c["region"]["id"] != "NA"}
        has = {}
        for r in parl:
            iso3 = r["countryiso3code"] or r["country"]["id"]
            if iso3 in iso2:
                has.setdefault(iso3, set())
                if r["value"] is not None:
                    has[iso3].add(r["date"])
        missing = sorted(c for c, ys in has.items() if "2025" not in ys and ys)
        print("economies with figures but no 2025 figure:", ", ".join(missing))
        for c in missing:
            pages.append((f"IPU-PARLINE-{c}", f"https://data.ipu.org/parliament/{iso2[c]}/", PARLINE_WORDS))
            pages.append((f"IPU-PARLINE-{c}-LC", f"https://data.ipu.org/parliament/{iso2[c]}/{iso2[c]}-LC01/", PARLINE_WORDS))
    except Exception as e:
        print(f"closing-card page list not built: {type(e).__name__}: {e}")

    for sid, url, words in pages:
        status, ctype, body, final = fetch(url)
        rec = {"id": sid, "url": url, "fetched_utc": now(), "status": status}
        if body is None:
            rec["error"] = ctype
            print(f"{sid}: FAILED {ctype}")
        else:
            text = to_text(body, ctype, url)
            ex = excerpts(text, words)
            rec.update({"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "content_type": ctype,
                        "final_url": final, "text_chars": len(text), "excerpt_file": f"page_excerpts/{sid}.txt",
                        "excerpts": len(ex)})
            with open(os.path.join(exc, f"{sid}.txt"), "w", encoding="utf-8") as f:
                f.write(f"# {sid}\n# url: {url}\n# final url: {final}\n# fetched (UTC): {rec['fetched_utc']}\n"
                        f"# HTTP {status}; {len(body)} bytes; SHA-256 {rec['sha256']}\n"
                        "# Short excerpts only (lines holding the searched words, with the line before and after).\n\n")
                for e in ex:
                    f.write(e + "\n\n")
            print(f"{sid}: {status} {len(body)} bytes sha256 {rec['sha256']} excerpts {len(ex)}")
        manifest["pages"].append(rec)
        time.sleep(1)

    json.dump(manifest, open(os.path.join(out, "fetch_manifest.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
