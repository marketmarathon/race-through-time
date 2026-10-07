#!/usr/bin/env python3
"""Decode an rtt101-sources job log (as saved from the GitHub API) into files: OUTDIR/<name> and OUTDIR/index.tsv.
Usage: rtt101_decode_log.py LOGFILE OUTDIR"""
import base64, gzip, hashlib, json, os, sys

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
raw = open(src, encoding="utf-8").read()
try:
    raw = json.loads(raw)["logs_content"]
except Exception:
    pass
idx = open(os.path.join(out, "index.tsv"), "a", encoding="utf-8")
checks = open(os.path.join(out, "checks.jsonl"), "a", encoding="utf-8")
for line in raw.splitlines():
    if " RTT101CHECKS " in line:
        for rec in json.loads(line.split(" RTT101CHECKS ", 1)[1]):
            checks.write(json.dumps(rec, ensure_ascii=False) + "\n")
        continue
    hit = False
    for tag, fn in ((" RTT101WIKIFEES ", "wikifees.jsonl"), (" RTT101PROBE ", "probe.jsonl")):
        if tag in line:
            with open(os.path.join(out, fn), "a", encoding="utf-8") as fh:
                for rec in json.loads(line.split(tag, 1)[1]):
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            hit = True
    if hit:
        continue
    if " RTT101B64 " not in line:
        continue
    name, st, err, sha, b64 = line.split(" RTT101B64 ", 1)[1].split(" ", 4)
    body = gzip.decompress(base64.b64decode(b64)) if b64 != "-" else b""
    assert hashlib.sha256(body).hexdigest() == sha, name
    fn = name.replace("/", "_").replace(":", "__")
    open(os.path.join(out, fn), "wb").write(body)
    idx.write(f"{name}\t{st}\t{err}\t{sha}\t{len(body)}\n")
    print(name, st, err, len(body))
