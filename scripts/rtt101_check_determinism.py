#!/usr/bin/env python3
"""RTT-101: the build must give byte-identical outputs whatever Python's hash seed (lesson of IQ-15b: lead matching once depended on
set order). Runs the build with two seeds and compares every output file. Usage: python3 scripts/rtt101_check_determinism.py"""
import glob, hashlib, os, subprocess, sys


def run(seed):
    subprocess.run([sys.executable, "scripts/build_rtt101_dataset.py"], check=True, capture_output=True, env=dict(os.environ, PYTHONHASHSEED=str(seed)))
    return {p: hashlib.sha256(open(p, "rb").read()).hexdigest() for p in sorted(glob.glob("data/rtt-101/*.csv")) + ["data/rtt-101/CHECKS.md"]}


a, b = run(1), run(11)
diff = [p for p in a if a[p] != b.get(p)]
print("PASS: identical outputs with hash seeds 1 and 11" if not diff else "FAIL: outputs differ: " + ", ".join(diff))
sys.exit(1 if diff else 0)
