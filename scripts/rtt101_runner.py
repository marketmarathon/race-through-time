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
import base64, gzip, hashlib, html, json, re, sys, time, urllib.parse, urllib.request

UA = "Mozilla/5.0 (compatible; RTT-research/1.0; +https://github.com/marketmarathon/race-through-time)"
WUA = "RTT-research/1.0 (https://github.com/marketmarathon/race-through-time; data build IQ-15)"
JOB = "data/rtt-101/runner_job.json"


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
    for it in job.get("check", []):
        st, body, err = get(it["url"])
        t = text_of(body) if body else ""
        found = []
        for n in it.get("needles", []):
            i = t.find(n)
            if i >= 0:
                found.append((n, t[max(0, i - 100): i + len(n) + 60]))
        rec = {"id": it["id"], "status": st, "err": err, "sha256": hashlib.sha256(body).hexdigest() if body else "",
               "bytes": len(body), "found": [f[0] for f in found], "excerpt": found[0][1] if found else ""}
        print("RTT101CHECK " + json.dumps(rec, ensure_ascii=False))
        sys.stdout.flush()
        time.sleep(job.get("delay", 1.5))


if __name__ == "__main__":
    main()
