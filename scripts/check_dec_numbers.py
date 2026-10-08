#!/usr/bin/env python3
"""Fail if a DEC number in this branch's state/DECISIONS.md is used with different content on another open pull request's branch
(lesson of 8 Oct 2026: DEC-278 to DEC-280 were used on two branches at once). Needs network: lists open pull requests with the gh CLI
(REST), fetches their branches and compares each DEC entry's title (the bold text after the number).
Usage: python3 scripts/check_dec_numbers.py"""
import json, re, subprocess, sys

REPO = "marketmarathon/race-through-time"
ENTRY = re.compile(r"^- \*\*DEC-(\d+)\b(.*?)\*\*", re.M)


def entries(text):
    out = {}
    for m in ENTRY.finditer(text):
        title = re.sub(r"\s+", " ", m.group(2)).strip(" ·")
        # the label after the date and author is the stable part; compare its first 80 characters, ignoring status words added later
        title = re.sub(r"SUPERSEDED[^·]*·\s*", "", title)
        out.setdefault(int(m.group(1)), title[-80:])
    return out


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


mine = entries(open("state/DECISIONS.md", encoding="utf-8").read())
me = git("rev-parse", "--abbrev-ref", "HEAD").strip()
prs = json.loads(subprocess.run(["gh", "api", f"repos/{REPO}/pulls?state=open&per_page=100"], capture_output=True, text=True, check=True).stdout)
bad = []
for pr in prs:
    ref = pr["head"]["ref"]
    if ref == me:
        continue
    subprocess.run(["git", "fetch", "-q", "origin", ref], check=True)
    try:
        theirs = entries(git("show", f"origin/{ref}:state/DECISIONS.md"))
    except subprocess.CalledProcessError:
        continue
    for n, t in sorted(mine.items()):
        if n in theirs and theirs[n] != t:
            bad.append(f"DEC-{n}: here '{t[:60]}…' vs PR #{pr['number']} ({ref}) '{theirs[n][:60]}…'")
print("\n".join(bad) if bad else f"PASS: no DEC number here is used with different content on the {len(prs) - 1} other open pull requests")
sys.exit(1 if bad else 0)
