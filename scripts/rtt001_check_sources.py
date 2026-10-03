#!/usr/bin/env python3
"""RTT-001 Browser Wars (IQ-12): fetch the sources the Claude Code cloud container cannot reach (its network policy
blocks gs.statcounter.com, web.archive.org, sites.cc.gatech.edu, www.justice.gov, w3counter.com and onestat.com).

Run on a GitHub-hosted runner by .github/workflows/rtt001_sources.yml, the same way as rtt003_sources.yml (DEC-136):
no secret, no artifact, no cache. Nothing is saved or uploaded; everything needed for checking goes to the run log:
  - ACCESS: one request to each source site (HTTP status only), for reports/RTT-001_source_access.md;
  - for each page: HTTP status, byte count, SHA-256 of the raw response, the <title>, and the page's text lines that
    contain a digit (table rows and figure sentences), cut to 240 characters, plus lines naming terms of use;
  - the StatCounter worldwide all-platform monthly CSV, line by line (CC BY-SA 3.0 data), with its SHA-256, so the
    exact file can be rebuilt and checked against that hash.
Wayback pages are requested in raw "id_" form so the hash is of the archived original. Standard library only.
"""
import hashlib
import html
import re
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
WB = "https://web.archive.org/web/"
EWS = "http://www.ews.uiuc.edu/bstats/months/"
GVU = "https://sites.cc.gatech.edu/gvu/user_surveys/"
WSS = "http://www.websidestory.com/company/news-events/press-releases/view-release.html?"
ONE = "http://www.onestat.com/html/"

STATCOUNTER_CSV = ("https://gs.statcounter.com/chart.php?statType_hidden=browser&region_hidden=ww&granularity=monthly"
                   "&fromInt=200901&toInt=202609&fromMonthYear=2009-01&toMonthYear=2026-09"
                   "&device_hidden=desktop%2Bmobile%2Btablet%2Bconsole&csv=1")

ACCESS = ["https://gs.statcounter.com/", "https://web.archive.org/", "https://sites.cc.gatech.edu/gvu/user_surveys/",
          "https://www.justice.gov/", "https://www.w3counter.com/", "https://www.onestat.com/"]

# EWS monthly host reports, April 1996 to April 2001 (archive capture timestamps as found in the research leads)
EWS_CAPTURES = {
    "9604": "20010507151202", "9605": "20010507151131", "9606": "20010507151448", "9607": "20010507152042",
    "9608": "20010624182616", "9609": "20010507152419", "9610": "20010507145607", "9611": "20010507150001",
    "9612": "20010507150349", "9701": "20010507150416", "9702": "20010507151137", "9703": "20010507151500",
    "9704": "20010507151601", "9705": "20010507151610", "9706": "20010507170623", "9707": "20010507152516",
    "9708": "20010507145718", "9709": "20010507150240", "9710": "20010507150536", "9711": "20010507150634",
    "9712": "20010507151412", "9801": "20010507151453", "9802": "20020328154600", "9803": "20010507151807",
    "9804": "20010624183723", "9805": "20010507152708", "9806": "20010507150103", "9807": "20010507150051",
    "9808": "20010507150251", "9809": "20010507150642", "9810": "20010507151253", "9811": "20010507151405",
    "9812": "20020328154223", "9901": "20010507151656", "9902": "20020623054045", "9903": "20010507152056",
    "9904": "20010507145703", "9905": "20010507145924", "9906": "20010507150416", "9907": "20010507150825",
    "9908": "20010507151155", "9909": "20010507150934", "9910": "20010507151506", "9911": "20010507151804",
    "9912": "20010507153200", "0001": "20010507084225", "0002": "20010507084420", "0003": "20010507085400",
    "0004": "20010507150630", "0005": "20010507150334", "0006": "20010624184754", "0007": "20010507151236",
    "0008": "20010507151210", "0009": "20020328155200", "0010": "20010507151854", "0011": "20020328153712",
    "0012": "20010507152406", "0101": "20010507145900", "0102": "20010507150215", "0103": "20010507150557",
    "0104": "20010507150631",
}

PAGES = []
# GVU WWW User Surveys (live site first; the archive copy is fetched only if the live page fails)
for pid, path, ts in [
    ("GVU-1-PAPER", "survey-01-1994/survey-paper.html", "20250811125244"),
    ("GVU-1-INDEX", "survey-01-1994/", "2025"),
    ("GVU-2-INDEX", "survey-09-1994/", "2025"),
    ("GVU-2-BROWSER", "survey-09-1994/graphs/Browser.html", "20250815044505"),
    ("GVU-2-PAPER", "survey-09-1994/html-paper/survey_2_paper.html", "20250713204020"),
    ("GVU-2-COPYRIGHT", "survey-09-1994/copyright.html", "2025"),
    ("GVU-3-INDEX", "survey-04-1995/", "2025"),
    ("GVU-3-GRAPHS", "survey-04-1995/graphs/", "2025"),
    ("GVU-3-PAPER", "survey-04-1995/html-paper/survey_3_paper.html", "2025"),
    ("GVU-4-INDEX", "survey-10-1995/", "2025"),
    ("GVU-4-GRAPHS", "survey-10-1995/graphs/", "2025"),
]:
    PAGES.append((pid, GVU + path, WB + ts + "id_/" + GVU + path))
PAGES.append(("BERGHEL-PCAI", WB + "20210227013423id_/http://berghel.net/col-edit/cybernautica/jan-feb96/pcai961.php", None))
for ym, ts in EWS_CAPTURES.items():
    PAGES.append(("EWS-" + ym, WB + ts + "id_/" + EWS + ym + "-month.html", None))
# WebSideStory StatMarket press releases (1999 ones are cross-checks for the EWS era)
for rid, ts in [("1120&year=2001", "20070211144452"), ("1198&year=1999", "20070211145820"),
                ("1195&year=1999", "20070211145751"), ("1183&year=1999", "20070211145548"),
                ("1107&year=2001", "20070211144235"), ("1088&year=2001", "20070211143914"),
                ("1044&year=2002", "20070211143254")]:
    PAGES.append(("WSS-" + rid.split("&")[0], WB + ts + "id_/" + WSS + "id=" + rid, None))
# OneStat press releases, 2002 to 2007 (2021 captures, plus the contemporaneous 2003 captures of two releases)
for name, ts in [("aboutus_pressbox4.html", "20210224155400"), ("aboutus_pressbox7.html", "20210411002141"),
                 ("aboutus_pressbox11.html", "20210225142055"), ("aboutus_pressbox15.html", "20210225175726"),
                 ("aboutus_pressbox18.html", "20210225143407"), ("aboutus_pressbox18.html", "20031231224859"),
                 ("aboutus_pressbox23.html", "20210211161917"), ("aboutus_pressbox23.html", "20031203003253"),
                 ("aboutus_pressbox26.html", "20210212004757"), ("aboutus_pressbox30.html", "20210227122607"),
                 ("aboutus_pressbox34.html", "20210225005934"), ("aboutus_pressbox36.html", "20210224232208"),
                 ("aboutus_pressbox37.html", "20210126095725"),
                 ("aboutus_pressbox40_browser_market_firefox_growing.html", "20210414092524"),
                 ("aboutus_pressbox41_mozilla_firefox_usage_share.html", "20210225024139"),
                 ("aboutus_pressbox42_microsoft_internet_explorer_has_slightly_increased.html", "20210225010059"),
                 ("aboutus_pressbox44-mozilla-firefox-has-slightly-increased.html", "20210427170257"),
                 ("aboutus_pressbox48-microsoft-internet-explorer-usage.html", "20210304200542"),
                 ("aboutus_pressbox49-microsoft-internet-explorer-7-usage.html", "20210225130755"),
                 ("aboutus_pressbox50-microsoft-internet-explorer-7-usage.html", "20210227065641"),
                 ("aboutus_pressbox53-firefox-mozilla-browser-market-share.html", "20210226040826"),
                 ("aboutus_pressbox57-firefox-mozilla-ie-browser-market-share.html", "20210224142758")]:
    num = re.search(r"pressbox(\d+)", name).group(1)
    PAGES.append((f"ONESTAT-{num}-{ts[:4]}", WB + ts + "id_/" + ONE + name, None))
# W3Counter monthly global stats, May 2007 to January 2009 (archived report pages)
W3C_TS = {(2007, 5): "20101203165436", (2007, 6): "20101203165401", (2007, 7): "20101203165259",
          (2007, 8): "20101203165120", (2007, 9): "20101203165010", (2007, 10): "20101203170332",
          (2007, 11): "20101203170119", (2007, 12): "20101203170425", (2008, 1): "20101203170042",
          (2008, 2): "20101203170005", (2008, 3): "20101203165932", (2008, 4): "20101203165813",
          (2008, 5): "20101203165848", (2008, 6): "20101203165657", (2008, 7): "20101203165737",
          (2008, 8): "20101203165503", (2008, 9): "20101203165544", (2008, 10): "20101203164437",
          (2008, 11): "20101203164515", (2008, 12): "20101203164558", (2009, 1): "20101203163411"}
for (y, m), ts in W3C_TS.items():
    PAGES.append((f"W3C-{y}-{m:02d}", WB + ts + f"id_/http://w3counter.com/globalstats.php?year={y}&month={m}", None))
PAGES.append(("W3C-LIVE-2008-12", "https://www.w3counter.com/globalstats.php?year=2008&month=12", None))
# Cross-checks at the hand-over months (never on screen)
for pid, url in [
    ("TC-2000-12", WB + "2001id_/http://www.thecounter.com/stats/2000/December/browser.php"),
    ("TC-2001-01", WB + "20020806171422id_/http://www.thecounter.com/stats/2001/January/browser.php"),
    ("TC-2002-08", WB + "20030406091546id_/http://www.thecounter.com/stats/2002/August/browser.php"),
    ("TC-2002-09", WB + "20021213194028id_/http://www.thecounter.com/stats/2002/September/browser.php"),
    ("TC-2007-04", WB + "20080220193221id_/http://www.thecounter.com/stats/2007/April/browser.php"),
    ("TC-2007-05", WB + "20080220193248id_/http://www.thecounter.com/stats/2007/May/browser.php"),
    ("TC-2008-12", WB + "20090826070444id_/http://www.thecounter.com/stats/2008/December/browser.php"),
    ("W3SCHOOLS", WB + "20100114153201id_/http://www.w3schools.com/browsers/browsers_stats.asp"),
    ("ARS-NETAPP-2008-12", "https://arstechnica.com/information-technology/2009/01/december-2008-firefox-safari-and-chrome-grab-more-users/"),
    ("ADTECH-2009-01", WB + "20090817190734id_/http://www.adtech.info/news/pr-04-01-2009_en.htm"),
    ("XITI-23-2009-04", WB + "20090520083409id_/http://www.atinternet-institute.com/en-us/browsers-barometer/browser-barometer-april-2009/index-1-2-3-169.html"),
    ("SIBLEY-ZONA", "https://www.justice.gov/atr/declaration-david-sibley"),
]:
    PAGES.append((pid, url, None))
# Terms of use pages
for pid, url in [("SC-FAQ", "https://gs.statcounter.com/faq"),
                 ("W3C-HOME", "https://www.w3counter.com/globalstats.php"),
                 ("ONESTAT-HOME", "https://www.onestat.com/"),
                 ("EWS-INDEX", WB + "2001id_/http://www.ews.uiuc.edu/bstats/")]:
    PAGES.append((pid, url, None))

TERMS = re.compile(r"(?i)(licen[cs]e|copyright|terms of use|permission|creative commons|attribution|may be reproduced|reprint)")
SIBLEY = re.compile(r"(?i)(zona|navigator|internet explorer|%)")


def get(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read(), r.geturl()
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (403, 404, 410):
                break
        except Exception as e:  # report and continue: a blocked source is listed, not fatal
            last = f"{type(e).__name__}: {e}"
        time.sleep(5 * (i + 1))
    return None, last, url


def lines_of(raw):
    t = raw.decode("utf-8", errors="replace")
    if "�" in t:
        t = raw.decode("latin-1")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?i)</t[dh]\s*>", " | ", t)
    t = re.sub(r"(?i)<(br|/?p|/?tr|/?li|/?h\d|/?div|/?table|/?pre|/?ul|/?ol|/?dt|/?dd)\b[^>]*>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return [re.sub(r"[ \t\r\f\v]+", " ", ln).strip() for ln in t.split("\n")]


def report(pid, url, fallback):
    print(f"\n=== {pid} {url}")
    status, raw, final = get(url)
    if status is None and fallback:
        print(f"FAILED: {raw}; trying archive copy {fallback}")
        status, raw, final = get(fallback)
    if status is None:
        print(f"FAILED: {raw}")
        return False
    print(f"HTTP {status}, {len(raw)} bytes, sha256 {hashlib.sha256(raw).hexdigest()}, final {final}")
    m = re.search(rb"(?is)<title[^>]*>(.*?)</title>", raw)
    if m:
        print("TITLE| " + re.sub(r"\s+", " ", html.unescape(m.group(1).decode("latin-1"))).strip()[:200])
    cap = 400 if pid.startswith(("EWS-", "SIBLEY")) else 200
    n = 0
    for ln in lines_of(raw):
        if not ln:
            continue
        if TERMS.search(ln):
            print("K| " + ln[:240])
        if re.search(r"\d", ln) and n < cap:
            if pid.startswith("SIBLEY") and not SIBLEY.search(ln):
                continue
            print("L| " + ln[:240])
            n += 1
    return True


def statcounter():
    print(f"\n=== STATCOUNTER-CSV {STATCOUNTER_CSV}")
    status, raw, final = get(STATCOUNTER_CSV)
    if status is None:
        print(f"FAILED: {raw}")
        return
    print(f"HTTP {status}, {len(raw)} bytes, sha256 {hashlib.sha256(raw).hexdigest()}, final {final}")
    crlf, lf, end, bom = raw.count(b"\r\n"), raw.count(b"\n"), raw.endswith(b"\n"), raw.startswith(b"\xef\xbb\xbf")
    print(f"CRLF {crlf}, LF {lf}, ends_with_newline {end}, bom {bom}, non_ascii {sum(1 for b in raw if b > 127)}")
    for ln in raw.decode("utf-8", errors="replace").replace("\r\n", "\n").split("\n"):
        print("CSV| " + ln)


def main():
    print("RETRIEVED_UTC " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    for url in ACCESS:
        status, raw, _ = get(url, tries=1)
        print(f"ACCESS| {url} | {('HTTP ' + str(status)) if status else raw}")
    statcounter()
    ok = 0
    for pid, url, fallback in PAGES:
        ok += report(pid, url, fallback)
        time.sleep(2)
    print(f"\n{ok}/{len(PAGES)} pages fetched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
