#!/usr/bin/env python3
"""Race Through Time - find beat-aligned loop points in a music track (RTT-003 round 6; the method of DEC-074).

    python scripts/rtt_music_loop.py TRACK.mp3 FILM_SECONDS FINAL_HOLD_SEC [--from-beat N] [--to-beat N]

The track itself is never committed (it lives only in the private repo). Steps:
  1. beat tracking (librosa) and section boundaries (checkerboard novelty on beat-synchronous chroma + MFCC);
  2. candidate pairs A < B on the 16-beat grid between --from-beat and --to-beat, so both joins sit at the same
     point of a 4-bar phrase; only pairs that need ONE join and keep the music after the join inside that span
     (so the film ends before the track's outro) are kept;
  3. each pair is scored on the 8-beat crossfade window (4 beats each side, as scripts/rtt_mix_music.sh centres it):
     spectral match = mean cosine similarity of the log-mel frames around A and around B, aligned beat by beat
     (1.0 = identical), and level difference (dB RMS) between the two windows.
Prints the beat grid, the sections and the ten best pairs; nothing else.
"""
import argparse
import numpy as np
import librosa


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('track'); ap.add_argument('film_sec', type=float); ap.add_argument('hold_sec', type=float)
    ap.add_argument('--from-beat', type=int, default=0); ap.add_argument('--to-beat', type=int, default=10**6)
    a = ap.parse_args()
    y, sr = librosa.load(a.track, sr=22050, mono=True)
    hop = 512
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='frames', trim=False)
    bt = librosa.frames_to_time(beats, sr=sr, hop_length=hop)
    print(f"track {len(y) / sr:.3f} s; {float(np.atleast_1d(tempo)[0]):.2f} BPM; {len(bt)} beats; median beat {np.median(np.diff(bt)):.4f} s")
    C = librosa.util.sync(librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop), beats, aggregate=np.median)
    Mf = librosa.util.sync(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20, hop_length=hop)[1:], beats, aggregate=np.mean)
    F = np.vstack([C / (np.linalg.norm(C, axis=0) + 1e-9), Mf / (np.linalg.norm(Mf, axis=0) + 1e-9)])
    S = F.T @ F / 2
    k = 16; K = np.kron(np.array([[1, -1], [-1, 1]]), np.ones((k, k))); n = S.shape[0]
    nov = np.array([np.sum(S[i - k:i + k, i - k:i + k] * K) if k <= i < n - k else 0 for i in range(n)])
    sec = [i for i in range(1, n - 1) if nov[i] > nov[i - 1] and nov[i] >= nov[i + 1] and nov[i] > np.percentile(nov, 85)]
    print('section boundaries (beat: s): ' + ', '.join(f'{i}: {bt[i]:.1f}' for i in sec if i < len(bt)))
    L = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop, n_mels=64))
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    def window(i):                      # 8 beats around beat i, each beat resampled to 16 frames
        segs = []
        for j in range(i - 4, i + 4):
            f0, f1 = beats[j], beats[j + 1]
            idx = np.linspace(f0, f1, 16, endpoint=False).astype(int)
            segs.append(L[:, idx])
        return np.hstack(segs), rms[beats[i - 4]:beats[i + 4]]
    lo, hi = max(a.from_beat, 8), min(a.to_beat, len(bt) - 6)
    rows = []
    for ia in range(lo - lo % 16, hi, 16):
        if ia < lo: continue
        for ib in range(ia + 32, hi, 16):
            A, B = bt[ia], bt[ib]
            after = a.film_sec - B
            if after <= 0 or A + after > bt[hi]: continue
            wa, ra = window(ia); wb, rb = window(ib)
            za = (wa - wa.mean(0)) / (wa.std(0) + 1e-9); zb = (wb - wb.mean(0)) / (wb.std(0) + 1e-9)
            sim = float(np.mean(np.sum(za * zb, 0) / za.shape[0]))
            ddb = float(20 * np.log10((rb.mean() + 1e-9) / (ra.mean() + 1e-9)))
            rows.append((sim, ia, ib, A, B, bt[ib + 4] - bt[ib - 4], after, ddb))
    rows.sort(reverse=True)
    print(f"film {a.film_sec:.3f} s, final table {a.hold_sec} s (music fades out from {a.film_sec - a.hold_sec:.3f} s)")
    for sim, ia, ib, A, B, X, after, ddb in rows[:10]:
        print(f"match {sim:.3f} | level {ddb:+.1f} dB | A = beat {ia} {A:.3f} s | B = beat {ib} {B:.3f} s | {ib - ia} beats ({(ib - ia) // 4} bars) | "
              f"crossfade {X:.3f} s | join at {B:.2f} s in the film | then track {A:.1f}-{A + after:.1f} s")


if __name__ == '__main__':
    main()
