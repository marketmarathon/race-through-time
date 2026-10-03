#!/usr/bin/env python3
"""RTT-003 rounds 4-5: check figures and statements at sources the Claude Code cloud container cannot reach (network policy).

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
PAGES = [   # round 5 (3 Oct 2026): documented end-of-production reports (round 4's list is in git history)
    ("KOTAKU-WIIU", "https://kotaku.com/wii-u-production-has-officially-ended-for-japan-1791813878", ["production has ended globally", "Wii U production", "datePublished"]),
    ("GAMESPOT-PS1", "https://www.gamespot.com/articles/sony-stops-making-original-ps/1100-6146549/", ["PSone", "PS one", "production", "datePublished"]),
    ("GUARDIAN-PS2", "https://www.theguardian.com/technology/2013/jan/04/playstation-2-manufacture-ends-years", ["all PS2 production has ended worldwide", "production", "datePublished"]),
    ("GAMESPOT-PSP", "https://www.gamespot.com/articles/after-10-years-sony-discontinues-psp-what-s-your-favorite-memory/1100-6420050/", ["discontinu", "end of", "datePublished"]),
    ("KOTAKU-PS3", "https://kotaku.com/sony-killed-off-the-ps3-in-japan-update-1793363510", ["production of PS3 itself has already terminated", "terminated", "datePublished"]),
    ("GAMESPOT-XBOX", "https://www.gamespot.com/articles/microsoft-pulls-plug-on-original-xbox-support/1100-6205466/", ["ceased", "production", "manufactur", "datePublished"]),
    ("EURONEWS-XBOXONE", "https://www.euronews.com/next/2022/01/13/microsoft-xbox", ["stopped production for all Xbox One consoles", "end of 2020"]),
    ("GAMEWATCH-DC", "https://game.watch.impress.co.jp/docs/20010131/sega2.htm", ["生産", "3月31日", "ドリームキャスト"]),
    ("GAMESPOT-FAMICOM", "https://www.gamespot.com/articles/nintendo-to-end-famicom-and-super-famicom-production/1100-6029220/", ["Famicom", "September", "production", "datePublished"]),
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
