#!/usr/bin/env python3
"""RTT-101 (IQ-15): fetch sources the Claude Code container cannot reach, on a GitHub runner.

Public repo (DEC-006, DEC-061): no secrets, no artifacts, no cache. Output goes to the job log only:
each fetched body is printed as ONE line "RTT101B64 <name> <status> <sha256> <base64(gzip(body))>", so the log
stays short and is decoded by scripts/rtt101_decode_log.py in the container.
The job is described by data/rtt-101/runner_job.json:
  "fetch": [{"name": ..., "url": ...}]        plain HTTP GET
  "wiki":  ["Title", ...]                      MediaWiki API parse (wikitext + revision id), 1 request/s
  "check": [{"id", "url", "needles": [...]}]   fetch a cited source; report which figures appear, with an excerpt
Never fetches Transfermarkt (DEC-236).
"""
import base64, gzip, hashlib, html, json, re, sys, time, unicodedata, urllib.parse, urllib.request

UA = "Mozilla/5.0 (compatible; RTT-research/1.0; +https://github.com/marketmarathon/race-through-time)"
WUA = "RTT-research/1.0 (https://github.com/marketmarathon/race-through-time; data build IQ-15)"
JOB = sys.argv[1] if len(sys.argv) > 1 else "data/rtt-101/runner_job.json"


def get(url, ua=UA, timeout=45):
    if "transfermarkt" in url.lower():
        return None, b"", "SKIPPED_TRANSFERMARKT"
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "en-GB,en;q=0.8"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read(), ""
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(15 * (attempt + 1)); continue
            return e.code, b"", f"HTTP{e.code}"
        except Exception as e:  # network errors are reported, never guessed
            return None, b"", type(e).__name__
    return None, b"", "RETRIES"


def emit(name, st, body, err=""):
    b64 = base64.b64encode(gzip.compress(body, 9)).decode()
    print(f"RTT101B64 {name.replace(' ', '_')} {st} {err or '-'} {hashlib.sha256(body).hexdigest()} {b64 or '-'}")
    sys.stdout.flush()


def fold(s):
    """lower case, accents and apostrophes removed (for the club-name check)"""
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c)).replace("'", "").replace("\u2019", "")


def text_of(body):
    t = body.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def main():
    job = json.load(open(JOB, encoding="utf-8"))
    for f in job.get("fetch", []):
        st, body, err = get(f["url"])
        emit(f["name"], st, body, err)
        time.sleep(job.get("delay", 2))
    for t in job.get("wiki", []):
        q = urllib.parse.urlencode({"action": "parse", "page": t, "prop": "wikitext|revid", "redirects": 1,
                                    "format": "json", "formatversion": 2, "maxlag": 5})
        st, body, err = get(f"https://en.wikipedia.org/w/api.php?{q}", ua=WUA)
        emit("wiki:" + t, st, body, err)
        time.sleep(1.0)
    # "wiki_fees": player articles -> only sentences that mention a fee, with their citations (keeps the log small)
    out = []
    for t in job.get("wiki_fees", []):
        q = urllib.parse.urlencode({"action": "parse", "page": t, "prop": "wikitext|revid", "redirects": 1,
                                    "format": "json", "formatversion": 2, "maxlag": 5})
        st, body, err = get(f"https://en.wikipedia.org/w/api.php?{q}", ua=WUA)
        rec = {"title": t, "status": st, "err": err, "revid": None, "sentences": []}
        try:
            j = json.loads(body)
            rec["revid"] = j["parse"]["revid"]
            w = j["parse"]["wikitext"]
            named = {}
            for m in re.finditer(r"<ref\s+name\s*=\s*\"?([^\">/]+?)\"?\s*>(.*?)</ref>", w, re.S):
                u = re.search(r"url\s*=\s*([^|}\s]+)", m.group(2))
                named[m.group(1).strip()] = u.group(1) if u else ""
            for para in re.split(r"\n\s*\n|\n(?=[*=])", w):
                if not re.search(r"£|€|\$|undisclosed|fee|million|transfer", para, re.I):
                    continue
                for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z\[])", para):
                    if not re.search(r"£|€|undisclosed|fee\b|million", sent, re.I):
                        continue
                    urls = []
                    for m in re.finditer(r"<ref(?:\s+name\s*=\s*\"?([^\">/]+?)\"?)?\s*(/>|>(.*?)</ref>)", sent, re.S):
                        if m.group(3):
                            u = re.search(r"url\s*=\s*([^|}\s]+)", m.group(3))
                            urls.append(u.group(1) if u else "")
                        elif m.group(1):
                            urls.append(named.get(m.group(1).strip(), ""))
                    txt = re.sub(r"<ref.*?(</ref>|/>)", "", sent, flags=re.S)
                    txt = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", txt)
                    txt = re.sub(r"\{\{[^{}]*\}\}", "", txt).replace("'", "")
                    txt = re.sub(r"\s+", " ", txt).strip()[:400]
                    urls = [u for u in urls if u and "transfermarkt" not in u.lower()]
                    if txt:
                        rec["sentences"].append({"text": txt, "urls": urls})
        except Exception as e:  # report, never guess
            rec["err"] = rec["err"] or type(e).__name__
        out.append(rec)
        if len(out) == 10:
            print("RTT101WIKIFEES " + json.dumps(out, ensure_ascii=False)); sys.stdout.flush(); out = []
        time.sleep(1.0)
    if out:
        print("RTT101WIKIFEES " + json.dumps(out, ensure_ascii=False))
    # "probe": every money figure within 350 characters of the surname, plus the page's publication date
    MONEY = re.compile(r"(?:£|€|\$|pounds?\s|euros?\s)\s?\d[\d,.]*\s?(?:m\b|mn\b|million|bn|billion|k\b)?|\d[\d,.]*\s?(?:million|m)\s(?:pounds|euros)", re.I)
    out = []
    for it in job.get("probe", []):
        st, body, err = get(it["url"])
        raw = body.decode("utf-8", "replace") if body else ""
        pub = ""
        m = re.search(r"(?:article:published_time|datePublished|dcterms.created|og:published_time)\"?\s*(?:content=|:)\s*\"([^\"]{8,40})\"", raw)
        if m:
            pub = m.group(1)
        t = text_of(body) if body else ""
        # accents folded without changing positions (Zúñiga = Zuniga); apostrophes dropped only for the club check (Queen's = Queens)
        low = "".join((unicodedata.normalize("NFKD", c) or " ")[0] for c in t.lower())
        near = "".join((unicodedata.normalize("NFKD", c) or " ")[0] for c in (it.get("near") or "").lower())
        snips, seen = [], set()
        if near:
            for mm in MONEY.finditer(t):
                win = low[max(0, mm.start() - 350): mm.end() + 350]
                if near in win:
                    snips.append({"money": mm.group(0).strip(), "excerpt": t[max(0, mm.start() - 120): mm.end() + 80]})
                    seen.add(mm.start())
                if len(snips) >= 6:
                    break
            if job.get("anchored"):
                # long lists: also every figure within 350 characters after (or 120 before) each mention of the name, up to 16 in all
                for nm in list(re.finditer(re.escape(near), low))[:8]:
                    for mm in MONEY.finditer(t, max(0, nm.start() - 120), min(len(t), nm.end() + 350)):
                        if mm.start() not in seen and len(snips) < 16:
                            seen.add(mm.start())
                            snips.append({"money": mm.group(0).strip(), "excerpt": t[max(0, mm.start() - 120): mm.end() + 80]})
        out.append({"id": it["id"], "status": st, "err": err, "sha256": hashlib.sha256(body).hexdigest() if body else "",
                    "published": pub, "surname_on_page": bool(near and near in low),
                    "undisclosed_on_page": bool(near and "undisclosed" in low), "snips": snips,
                    "also_found": [any(fold(v) in fold(t) for v in grp) for grp in it.get("also", [])]})
        if len(out) == 20:
            print("RTT101PROBE " + json.dumps(out, ensure_ascii=False)); sys.stdout.flush(); out = []
        time.sleep(job.get("delay", 1.0))
    if out:
        print("RTT101PROBE " + json.dumps(out, ensure_ascii=False))
    batch = []
    for it in job.get("check", []):
        st, body, err = get(it["url"])
        t = text_of(body) if body else ""
        near = (it.get("near") or "").lower()
        hit = None
        for n in it.get("needles", []):
            for mm in re.finditer(re.escape(n), t):
                i = mm.start()
                win = t[max(0, i - 400): i + len(n) + 400].lower()
                if not near or near in win:
                    hit = (n, t[max(0, i - 110): i + len(n) + 70])
                    break
            if hit:
                break
        batch.append({"id": it["id"], "status": st, "err": err, "sha256": hashlib.sha256(body).hexdigest() if body else "",
                      "bytes": len(body), "needle": hit[0] if hit else "", "excerpt": hit[1] if hit else "",
                      "surname_on_page": bool(near and near in t.lower())})
        if len(batch) == 20:
            print("RTT101CHECKS " + json.dumps(batch, ensure_ascii=False)); sys.stdout.flush(); batch = []
        time.sleep(job.get("delay", 1.5))
    if batch:
        print("RTT101CHECKS " + json.dumps(batch, ensure_ascii=False))

if __name__ == "__main__":
    main()
