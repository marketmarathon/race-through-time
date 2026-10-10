#!/usr/bin/env python3
"""RTT-102 (IQ-17): read the dated publications at their source from a GitHub-hosted runner.

The Claude Code cloud container's network policy blocks similarweb.com, digiday.com, the-decoder.com, linkedin.com and
the other publishers. Run by .github/workflows/rtt102_sources.yml. For each publication in
data/rtt-102/source/publications.csv (except Similarweb's website profiles, whose free search limit is not worked
around, the IPO PDF and the method pages) it checks robots.txt, fetches the page once and prints the HTTP status, the
page's SHA-256 and every sentence that holds a figure in millions or billions (at most about 40 words each), so each
figure and its wording can be checked from the run log. Nothing is saved or uploaded. Standard library only.
"""
import csv
import hashlib
import html
import re
import time
import urllib.parse
import urllib.request
import urllib.robotparser

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
SKIP = re.compile(r"^(S26_|S_METHOD_|Q26_IPO_PDF$)")
FIG = re.compile(r"\d[\d,.]*\s*(?:million|billion|bn|mn|[MBK])\b", re.I)
_robots = {}


def allowed(url):
    p = urllib.parse.urlsplit(url)
    base = f"{p.scheme}://{p.netloc}"
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            req = urllib.request.Request(base + "/robots.txt", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                rp.parse(r.read().decode("utf-8", errors="replace").splitlines())
        except Exception:
            rp = None  # no readable robots.txt: treat as allowed
        _robots[base] = rp
    rp = _robots[base]
    return True if rp is None else rp.can_fetch(UA, url)


def text_of(raw):
    t = raw.decode("utf-8", errors="replace")
    t = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def meta_dates(raw):
    t = raw.decode("utf-8", errors="replace")
    found = re.findall(r'"(datePublished|dateModified)"\s*:\s*"([^"]+)"', t)
    found += re.findall(r'(article:published_time|article:modified_time)"\s+content="([^"]+)"', t)
    return sorted(set(found))


def main():
    pubs = [p for p in csv.DictReader(open("data/rtt-102/source/publications.csv", encoding="utf-8")) if not SKIP.match(p["pub_id"])]
    ok = 0
    for p in pubs:
        url = p["url"]
        print(f"\n=== {p['pub_id']} {url}")
        try:
            if not allowed(url):
                print("SKIPPED: robots.txt disallows this URL")
                continue
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read()
                print(f"HTTP {r.status}, {len(raw)} bytes, sha256 {hashlib.sha256(raw).hexdigest()}")
        except Exception as e:  # report and continue: a blocked source is listed, not fatal
            print(f"FAILED: {type(e).__name__}: {e}")
            continue
        ok += 1
        for k, v in meta_dates(raw):
            print(f"  [{k}] {v}")
        seen = set()
        for s in re.split(r"(?<=[.!?])\s+", text_of(raw)):
            if FIG.search(s) and re.search(r"visit|traffic", s, re.I):
                words = s.split()
                s = " ".join(words[:40]) + (" …" if len(words) > 40 else "")
                if s not in seen:
                    seen.add(s)
                    print(f"  · {s}")
        if not seen:
            print("  (no sentence with a visits figure found)")
        time.sleep(2)
    print(f"\n{ok}/{len(pubs)} pages fetched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
