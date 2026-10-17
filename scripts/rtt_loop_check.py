#!/usr/bin/env python3
"""Race Through Time - check a mixed film's music at its loop joins for clicks and level jumps (IQ-24g).

    python3 scripts/rtt_loop_check.py VIDEO JOIN_SEC[,JOIN_SEC...] XFADE_SEC

The audio is decoded with ffmpeg (48 kHz, mono mix, 32-bit float) and never written anywhere. For each join the
window checked is the crossfade (join +/- XFADE/2) plus 0.25 s each side. Two measures, each compared with the rest of
the music (the whole film minus every join window and minus the final fade):
  click  = the largest 5 ms RMS of the sample-to-sample difference (a click is a burst of high-frequency energy);
           PASS if the window's largest is no more than the 99.9th percentile of the rest;
  jump   = the largest step in loudness between neighbouring 100 ms windows (dB RMS);
           PASS if the window's largest is no more than the 99th percentile of the rest.
Prints the numbers only and exits 1 on any FAIL.
"""
import subprocess
import sys
import numpy as np

SR = 48000


def main():
    video, joins, xf = sys.argv[1], [float(j) for j in sys.argv[2].split(',') if j], float(sys.argv[3])
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', video, '-map', '0:a:0', '-ac', '1', '-ar', str(SR),
                          '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    dur = len(x) / SR
    d = np.abs(np.diff(x, prepend=x[0]))
    n5, n100 = int(0.005 * SR), int(0.1 * SR)
    hf = np.sqrt(np.mean(d[: len(d) // n5 * n5].reshape(-1, n5) ** 2, axis=1))          # 5 ms windows
    rms = np.sqrt(np.mean(x[: len(x) // n100 * n100].reshape(-1, n100) ** 2, axis=1))     # 100 ms windows
    lvl = 20 * np.log10(rms + 1e-6)
    step = np.abs(np.diff(lvl))
    t5, t100 = np.arange(len(hf)) * 0.005, np.arange(len(step)) * 0.1 + 0.1
    pad = xf / 2 + 0.25
    in_join5 = np.zeros(len(hf), bool); in_join100 = np.zeros(len(step), bool)
    for j in joins:
        in_join5 |= (t5 >= j - pad) & (t5 <= j + pad); in_join100 |= (t100 >= j - pad) & (t100 <= j + pad)
    fade = 6.0                                                                             # leave out the final fade
    rest5 = ~in_join5 & (t5 > 1.0) & (t5 < dur - fade); rest100 = ~in_join100 & (t100 > 1.0) & (t100 < dur - fade)
    ref_click, ref_jump = np.percentile(hf[rest5], 99.9), np.percentile(step[rest100], 99)
    ok = True
    print(f"audio {dur:.3f} s; reference (rest of the music): click 99.9th percentile {ref_click:.5f}, "
          f"loudness step 99th percentile {ref_jump:.2f} dB per 100 ms")
    for j in joins:
        w5 = (t5 >= j - pad) & (t5 <= j + pad); w100 = (t100 >= j - pad) & (t100 <= j + pad)
        c, s = hf[w5].max(), step[w100].max()
        lv_before = lvl[(np.arange(len(lvl)) * 0.1 >= j - pad - 1) & (np.arange(len(lvl)) * 0.1 < j - pad)].mean()
        lv_after = lvl[(np.arange(len(lvl)) * 0.1 > j + pad) & (np.arange(len(lvl)) * 0.1 <= j + pad + 1)].mean()
        pc, ps = c <= ref_click, s <= ref_jump
        ok &= pc and ps
        print(f"join at {j:.3f} s (crossfade {xf:.3f} s): click {c:.5f} ({'PASS' if pc else 'FAIL'}), "
              f"largest loudness step {s:.2f} dB ({'PASS' if ps else 'FAIL'}); level 1 s before {lv_before:.1f} dB, "
              f"1 s after {lv_after:.1f} dB")
    print('loop check:', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
