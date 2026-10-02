#!/usr/bin/env python3
"""RTT-003 round 4: check figures at sources the Claude Code cloud container cannot reach (network policy).

Run on a GitHub-hosted runner by .github/workflows/rtt003_sources.yml. For each page it prints the HTTP status,
the page's SHA-256 and, for each search term, a short excerpt (about 30 words) around the first matches, so the
figure and its wording can be checked from the run log. Nothing is saved or uploaded. Standard library only.
"""
import hashlib
import html
import re
import sys
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
VG = ["Xbox Series X|S -", "Xbox Series X|S", "Worldwide hardware estimates", "week ending", " - ", "Estimates for"]
PAGES = [
    ("VGC-2024-10-05", "https://www.vgchartz.com/article/462852/ps5-best-seller-xs-tops-30m-lt-worldwide-hardware-estimates-for-september-2024/", VG),
    ("VGC-2025-01-04", "https://www.vgchartz.com/article/463776/global-hardware-december-2024/", VG),
    ("VGC-2025-04-05", "https://www.vgchartz.com/article/464519/ps5-sells-over-11m-and-tops-75m-lifetime-worldwide-hardware-estimates-for-march-2025/", VG),
    ("VGC-2025-07-05", "https://www.vgchartz.com/article/465283/switch-2-sets-record-with-over-5m-sold-in-1st-month-worldwide-hardware-estimates-for-june-2025/", VG),
    ("VGC-2025-10-04", "https://www.vgchartz.com/article/466071/ps5-outsells-switch-2-ps5-tops-80m-worldwide-hardware-estimates-for-september-2025/", VG),
    ("VGC-2026-01-03", "https://www.vgchartz.com/article/466834/global-hardware-december-2025/", VG),
    ("VGC-2026-04-04", "https://www.vgchartz.com/article/467615/switch-2-best-seller-ps5-tops-91m-lt-worldwide-hardware-estimates-for-march-2026/", VG),
    ("VGC-2026-07-04", "https://www.vgchartz.com/article/468546/switch-2-best-seller-xs-tops-35m-lt-worldwide-hardware-estimates-for-june-2026/", VG),
    ("VGC-PLATFORM-TOTALS", "https://www.vgchartz.com/charts/platform_totals/Hardware.php/", ["Xbox 360", "X360", "total shipments", "85.7", "85,7"]),
    ("GWR-2600", "https://www.guinnessworldrecords.com/world-records/109745-best-selling-second-generation-videogame-console", ["27.64", "discontinuation", "1 January 1992"]),
    ("ATARI-HISTORY", "https://atari.com/pages/history", ["30 million", "2600"]),
    ("SEGA-COL02", "https://www.sega.jp/history/hard/column/column_02.html", ["万台", "1,900", "1900"]),
    ("SEGA-COL04", "https://www.sega.jp/history/hard/column/column_04.html", ["万台", "最終的"]),
    ("TELECOMPAPER-1996", "https://www.telecompaper.com/news/sega-trims-hardware-range--79620", ["Master System", "Game Gear", "discontinu", "Trims"]),
    ("SHMUPLATIONS-SEGA", "https://shmuplations.com/segahistory/", ["14 million", "Game Gear"]),
    ("INSIDE-2019", "https://www.inside-games.jp/article/2019/04/30/122048_2.html", ["メガドライブ", "3,075", "3075", "白書"]),
    ("MIRAI-MD05", "https://www.mirai-idea.jp/post/megadrive05", ["3000万", "3,000万", "万台"]),
]


def text_of(raw):
    t = raw.decode("utf-8", errors="replace")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def main():
    ok = 0
    for pid, url, terms in PAGES:
        print(f"\n=== {pid} {url}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9,ja;q=0.8"})
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read()
                print(f"HTTP {r.status}, {len(raw)} bytes, sha256 {hashlib.sha256(raw).hexdigest()}")
        except Exception as e:  # report and continue: a blocked source is listed, not fatal
            print(f"FAILED: {type(e).__name__}: {e}")
            continue
        ok += 1
        t = text_of(raw)
        for term in terms:
            hits = [m.start() for m in re.finditer(re.escape(term), t)][:4]
            for h in hits:
                print(f"  [{term}] …{t[max(0, h - 110):h + 140]}…")
            if not hits:
                print(f"  [{term}] not found")
    print(f"\n{ok}/{len(PAGES)} pages fetched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
