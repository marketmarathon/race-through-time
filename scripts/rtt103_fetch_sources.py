#!/usr/bin/env python3
"""RTT-103 (IQ-16): fetch the source documents the Claude Code cloud container cannot reach.

Run on a GitHub-hosted runner by .github/workflows/rtt103_sources.yml. The URL lists are the private research
catalogues in race-through-time-private/research/rtt-103/ (ChatGPT's Section A files, DEC-006: they never enter this
public repo), plus the two FX sources. Every URL whose host is not www.sec.gov is downloaded once; for each file the
manifest records the URL, the catalogue source_ids that cite it, HTTP status, bytes, SHA-256 and content type.
PDFs are converted to layout text with pdftotext and only the text is kept (the PDF's own SHA-256 is recorded);
HTML and CSV are kept as downloaded. Output goes to the private repo only. The log prints IDs, sizes and hashes only.

IQ-16d: with FETCH_SET=part06 the URL lists are ChatGPT's look-ahead files (part06a-d) plus any URLs (chart images, PDFs
linked from fetched pages) listed in the private fetch_extra_part06.csv (source_id,url); PDFs and images are also kept
as downloaded (private repo only), so tables and charts can be read cell by cell or by eye.
IQ-16c: with FETCH_SET=part05 the URL lists are instead ChatGPT's forecast and OpenAI files (part05a-c, private); each URL
is identified as P05A-<row>, P05B-<row> or P05C-<row> (row number in the private file), and the FX sources are skipped.

Usage: rtt103_fetch_sources.py <private_repo_dir> <out_dir>
Standard library only (plus the pdftotext command).
"""
import csv
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
INPUTS = ["part01_sectionA_source_catalogue.csv", "part02b_china_prompt_tencent_Section_A_file.txt",
          "part03b_china_prompt_baidu_Section_A_file.txt", "part04b_china_prompt_alibaba_Section_A_file.txt"]
EXTRA = [  # FX (brief: Federal Reserve H.10, FRED DEXCHUS as distributor) - not in the catalogues by these exact URLs
    ("FX-FRED-DEXCHUS", "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXCHUS"),
    ("FX-H10-HIST-CHINA", "https://www.federalreserve.gov/releases/h10/hist/dat00_ch.htm"),
    ("FX-FRED-DEXCHUS-PAGE", "https://fred.stlouisfed.org/series/DEXCHUS"),
]
PART05 = [("P05A", "part05a_forecasts_part1_forward_capex.csv"), ("P05B", "part05b_forecasts_part2_openai_commitments.csv"),
          ("P05C", "part05c_forecasts_part3_conflicts_and_warnings.csv")]
PART06 = [("P06A", "part06a_to2031_part1_company_forecasts.csv"), ("P06B", "part06b_to2031_part2_group_forecasts.csv"),
          ("P06C", "part06c_to2031_part3_peak_and_slowdown.csv"), ("P06D", "part06d_to2031_part4_coverage_and_warnings.csv")]
SKIP_HOSTS = {"www.sec.gov"}  # fetched directly from the container


def part05_urls(src, files=PART05, cols=("source_url", "related_source_url")):
    """(source_id, url) for every URL in the given columns of ChatGPT's part05 (IQ-16c) or part06 (IQ-16d) files."""
    for prefix, name in files:
        rows = csv.DictReader(io.StringIO(open(os.path.join(src, name), encoding="utf-8-sig").read()))
        for n, row in enumerate(rows, 1):
            for col in cols:
                for u in re.findall(r"https?://[^\s;\"()]+", row.get(col) or ""):
                    yield f"{prefix}-{n:03d}", u.rstrip(".,")


def part06_urls(src, extra_only=False):
    if not extra_only:
        yield from part05_urls(src, PART06, ("source_url", "notes"))
    extra = os.path.join(src, "fetch_extra_part06.csv")
    if os.path.exists(extra):
        for row in csv.DictReader(open(extra, encoding="utf-8")):
            yield row["source_id"], row["url"]


def catalogue_rows(path):
    """Yield dict rows from a plain CSV or from the ```csv blocks of a ChatGPT Section A text file."""
    raw = open(path, encoding="utf-8-sig").read()
    if path.endswith(".csv"):
        blocks = [raw]
    else:
        blocks = re.findall(r"```csv\n(.*?)```", raw, flags=re.S)
    for b in blocks:
        rd = csv.DictReader(io.StringIO(b))
        if not rd.fieldnames or "url" not in rd.fieldnames or "source_id" not in rd.fieldnames:
            continue
        for row in rd:
            yield row


def safe_name(sid):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", sid)


def fetch(url, tries=2):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,text/html,image/*;q=0.9,*/*;q=0.8",
                                                       "Accept-Language": "en-GB,en;q=0.9,zh;q=0.6"})
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read()
                if body[:2] == b"\x1f\x8b":  # gzip-encoded body (Internet Archive copies, IQ-16d)
                    body = gzip.decompress(body)
                return r.status, r.headers.get("Content-Type", ""), body
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (403, 404, 410):
                break
        except Exception as e:  # report, retry, continue: a blocked source is listed, not fatal
            last = f"{type(e).__name__}: {e}"
        time.sleep(3)
    return None, last, None


def main():
    priv, out = sys.argv[1], sys.argv[2]
    src = os.path.join(priv, "research", "rtt-103")
    os.makedirs(os.path.join(out, "docs"), exist_ok=True)
    urls = {}  # url -> list of source_ids
    fset = os.environ.get("FETCH_SET", "")
    part05 = fset in ("part05", "part06")
    part05 = part05 or fset == "part06x"
    keep_raw = fset in ("part06", "part06x")  # part06x: only the URLs in fetch_extra_part06.csv (retries, archive copies)
    for sid, u in (part05_urls(src) if fset == "part05" else part06_urls(src, fset == "part06x") if keep_raw else []):
        if urllib.parse.urlparse(u).hostname not in SKIP_HOSTS:
            urls.setdefault(u, []).append(sid)
    for name in ([] if part05 else INPUTS):
        for row in catalogue_rows(os.path.join(src, name)):
            for u in re.findall(r"https?://[^\s;\"]+", row.get("url", "")):
                if urllib.parse.urlparse(u).hostname in SKIP_HOSTS:
                    continue
                urls.setdefault(u, []).append(row["source_id"])
    for sid, u in ([] if part05 else EXTRA):
        urls.setdefault(u, []).append(sid)
    print(f"{len(urls)} URLs to fetch")
    manifest, last_host_time, host_fails, used_names = [], {}, {}, set()
    deadline = time.time() + 60 * float(os.environ.get("BUDGET_MINUTES", "70"))
    for n, (u, sids) in enumerate(sorted(urls.items(), key=lambda kv: kv[1][0])):
        host = urllib.parse.urlparse(u).hostname
        rec = {"url": u, "source_ids": sids, "host": host}
        if time.time() > deadline:
            manifest.append(dict(rec, ok=False, error="not attempted: time budget reached"))
            continue
        if host_fails.get(host, 0) >= 4:  # four failures in a row: the host refuses this runner; list the rest
            manifest.append(dict(rec, ok=False, error="not attempted: host failed 4 times in a row"))
            continue
        wait = 1.5 - (time.time() - last_host_time.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        status, ctype, body = fetch(u)
        last_host_time[host] = time.time()
        rec["fetched_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if body is None:
            host_fails[host] = host_fails.get(host, 0) + 1
            rec.update({"ok": False, "error": ctype})
            print(f"[{n + 1}] {sids[0]} FAILED {ctype}")
            manifest.append(rec)
            continue
        host_fails[host] = 0
        sha = hashlib.sha256(body).hexdigest()
        base = safe_name(sids[0])
        while base in used_names:  # two URLs cited by the same first row must not overwrite each other (IQ-16d)
            base += "_b"
        used_names.add(base)
        is_pdf = body[:5] == b"%PDF-" or "pdf" in ctype.lower()
        img = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "image/gif": ".gif", "image/svg+xml": ".svg"}.get(ctype.split(";")[0].strip().lower())
        rec.update({"ok": True, "http_status": status, "content_type": ctype, "bytes": len(body), "sha256": sha,
                    "is_pdf": is_pdf})
        if keep_raw and (is_pdf or img):
            raw = os.path.join(out, "docs", base + (".pdf" if is_pdf else img))
            open(raw, "wb").write(body)
            rec["raw_file"] = f"docs/{base}{'.pdf' if is_pdf else img}"
        if img:
            rec["kept_file"], rec["kept_sha256"] = rec["raw_file"], sha
        elif is_pdf:
            tmp = os.path.join(out, "tmp.pdf")
            open(tmp, "wb").write(body)
            txt = os.path.join(out, "docs", base + ".pdf.txt")
            r = subprocess.run(["pdftotext", "-layout", tmp, txt], capture_output=True)
            os.remove(tmp)
            rec["kept_file"] = f"docs/{base}.pdf.txt" if r.returncode == 0 else None
            if r.returncode == 0:
                rec["kept_sha256"] = hashlib.sha256(open(txt, "rb").read()).hexdigest()
            else:
                rec["pdftotext_error"] = r.stderr.decode(errors="replace")[:200]
        else:
            ext = ".csv" if ("csv" in ctype.lower() or u.endswith(".csv")) else ".html"
            path = os.path.join(out, "docs", base + ext)
            open(path, "wb").write(body)
            rec["kept_file"] = f"docs/{base}{ext}"
            rec["kept_sha256"] = sha
        print(f"[{n + 1}] {sids[0]} HTTP {status} {len(body)} bytes sha256 {sha[:16]} pdf={is_pdf}")
        manifest.append(rec)
    json.dump({"made_by": "scripts/rtt103_fetch_sources.py", "run": os.environ.get("RUN_URL", ""),
               "documents": manifest}, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    ok = sum(1 for m in manifest if m["ok"])
    print(f"{ok}/{len(manifest)} fetched")
    for h in sorted({m["host"] for m in manifest}):
        hm = [m for m in manifest if m["host"] == h]
        print(f"  {h}: {sum(m['ok'] for m in hm)}/{len(hm)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
