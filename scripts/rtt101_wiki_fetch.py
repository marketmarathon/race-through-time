#!/usr/bin/env python3
"""RTT-101 (IQ-15): fetch Wikipedia pages (wikitext + revision id) via the MediaWiki API, politely.
Usage: rtt101_wiki_fetch.py OUTDIR "Title 1" "Title 2" ...   (cache: skips titles already saved)
Wikipedia is CC BY-SA 4.0; pages are pointers (grade C) only (DEC-247)."""
import json, os, sys, time, urllib.parse, urllib.request

UA = "RTT-research/1.0 (https://github.com/marketmarathon/race-through-time; data build IQ-15)"
API = "https://en.wikipedia.org/w/api.php"


def fetch(title):
    q = urllib.parse.urlencode({"action": "parse", "page": title, "prop": "wikitext|revid|displaytitle",
                                "redirects": 1, "format": "json", "formatversion": 2})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA}), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 * (attempt + 1)); continue
            raise
    raise RuntimeError("429 repeatedly")


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for t in sys.argv[2:]:
        fn = os.path.join(out, t.replace("/", "_") + ".json")
        if os.path.exists(fn):
            continue
        d = fetch(t)
        json.dump(d, open(fn, "w", encoding="utf-8"), ensure_ascii=False)
        p = d.get("parse", {})
        print(t, "->", p.get("title"), p.get("revid"), d.get("error", {}).get("code", ""))
        time.sleep(1.0)


if __name__ == "__main__":
    main()
