#!/usr/bin/env bash
# Race Through Time - add a music track to a rendered (silent) video (DEC-072).
#
#   scripts/rtt_mix_music.sh VIDEO_IN MUSIC_IN VIDEO_OUT FINAL_HOLD_SEC [LOOP_START LOOP_END XFADE_SEC]
#
# - with loop points (DEC-074): the track plays from its start; each time it reaches LOOP_END it
#   crossfades back to LOOP_START with an equal-power (quarter-sine) crossfade of XFADE_SEC centred on
#   the two points (so beats placed at both points coincide), as often as the video needs; without loop
#   points the track is simply repeated end to start; either way it is cut to the video's exact length;
# - it fades out over the last FINAL_HOLD_SEC seconds (the final table, under YouTube's end screen);
# - it is loudness-normalised in two passes (ffmpeg loudnorm, linear) to about -16 LUFS integrated with
#   true peak aimed at -1.5 dBTP, then encoded AAC 320 kb/s 48 kHz stereo; the video stream is copied
#   untouched;
# - the result is measured again (ebur128, true peak) and the script FAILS unless the integrated
#   loudness is within 1 LU of -16 LUFS and the true peak is at most -1.0 dBTP.
# Needs ffmpeg, ffprobe and python3. Prints only numbers, never the file's contents.
set -euo pipefail
IN=$1; MUSIC=$2; OUT=$3; HOLD=$4; LA=${5:-}; LB=${6:-}; XF=${7:-}
TARGET_I=-16; TARGET_TP=-1.5; LIMIT_TP=-1.0; TOL=1.0
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

D=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$IN")
FS=$(python3 -c "print(max(0.0, $D - $HOLD))")
echo "video ${D} s; music fades out from ${FS} s over ${HOLD} s"

# 1. loop (crossfaded at the loop points if given), cut to length, fade out (48 kHz stereo PCM)
ffmpeg -nostdin -hide_banner -loglevel error -y -i "$MUSIC" -ar 48000 -ac 2 -c:a pcm_s24le "$T/src.wav"
if [ -n "$LB" ]; then
  GRAPH=$(python3 - "$D" "$LA" "$LB" "$XF" <<'PY'
import math, sys
D, A, B, X = (float(v) for v in sys.argv[1:])
assert 0 < X < B - A and A - X / 2 >= 0, "bad loop points"
h = X / 2
# length after the first part is B + h; every further copy adds (B - A)
k = max(0, math.ceil((D - (B + h)) / (B - A))) + 1
n = k + 1
# every piece reads its own input of the same file (asplit + atrim loses audio on long graphs)
parts = [f"[0:a]atrim=0:{B + h:.6f},asetpts=PTS-STARTPTS[p0]"]
for i in range(1, n):
    parts.append(f"[{i}:a]atrim={A - h:.6f}:{B + h:.6f},asetpts=PTS-STARTPTS[p{i}]")
prev = "p0"
for i in range(1, n):
    parts.append(f"[{prev}][p{i}]acrossfade=d={X:.6f}:c1=qsin:c2=qsin[x{i}]")
    prev = f"x{i}"
print(n); print(";".join(parts) + f";[{prev}]anull[loop]")
joins = [B + j * (B - A) for j in range(k) if B + j * (B - A) < D]
sys.stderr.write(f"loop: {len(joins)} crossfaded join(s) in the video" + (f" at {', '.join(f'{t:.2f} s' for t in joins)}" if joins else "") + "\n")
PY
)
  N=$(echo "$GRAPH" | head -1); GRAPH=$(echo "$GRAPH" | tail -1)
  INPUTS=(); for _ in $(seq "$N"); do INPUTS+=(-i "$T/src.wav"); done
  ffmpeg -nostdin -hide_banner -loglevel error -y "${INPUTS[@]}" -filter_complex "$GRAPH" -map '[loop]' -c:a pcm_s24le "$T/loop.wav"
  LD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$T/loop.wav")
  python3 -c "import sys; sys.exit(0 if $LD >= $D - 0.01 else 'looped track is only $LD s for a $D s video')"
else
  ffmpeg -nostdin -hide_banner -loglevel error -y -stream_loop -1 -i "$T/src.wav" -c:a pcm_s24le -t "$D" "$T/loop.wav"
fi
ffmpeg -nostdin -hide_banner -loglevel error -y -i "$T/loop.wav" -t "$D" \
  -af "afade=t=out:st=${FS}:d=${HOLD}" -ar 48000 -ac 2 -c:a pcm_s24le "$T/a.wav"

# 2. loudnorm pass 1: measure
ffmpeg -nostdin -hide_banner -nostats -y -i "$T/a.wav" \
  -af "loudnorm=I=${TARGET_I}:TP=${TARGET_TP}:LRA=11:print_format=json" -f null - 2> "$T/p1.txt"
read -r MI MTP MLRA MTH OFF < <(python3 - "$T/p1.txt" <<'PY'
import json, re, sys
t = open(sys.argv[1]).read()
j = json.loads(t[t.rindex('{'):t.rindex('}') + 1])
print(j['input_i'], j['input_tp'], j['input_lra'], j['input_thresh'], j['target_offset'])
PY
)
echo "track as given: ${MI} LUFS integrated, true peak ${MTP} dBTP"

# 3. loudnorm pass 2: apply (linear)
ffmpeg -nostdin -hide_banner -loglevel error -y -i "$T/a.wav" \
  -af "loudnorm=I=${TARGET_I}:TP=${TARGET_TP}:LRA=11:measured_I=${MI}:measured_TP=${MTP}:measured_LRA=${MLRA}:measured_thresh=${MTH}:offset=${OFF}:linear=true" \
  -ar 48000 -c:a pcm_s24le "$T/n.wav"

# 4. mux: video copied, audio AAC
ffmpeg -nostdin -hide_banner -loglevel error -y -i "$IN" -i "$T/n.wav" -map 0:v:0 -map 1:a:0 -c:v copy \
  -c:a aac -b:a 320k -ar 48000 -ac 2 -t "$D" -movflags +faststart "$OUT"

# 5. measure the result and enforce the limits
ffmpeg -nostdin -hide_banner -nostats -i "$OUT" -map 0:a:0 -af ebur128=peak=true -f null - 2> "$T/m.txt"
python3 - "$T/m.txt" "$TARGET_I" "$TOL" "$LIMIT_TP" <<'PY'
import re, sys
t = open(sys.argv[1]).read()
s = t[t.rindex('Summary:'):]
i = float(re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1))
tp = float(re.search(r'True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS', s).group(1))
target, tol, limit = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
print(f"mixed: {i} LUFS integrated (target {target} +/- {tol}), true peak {tp} dBTP (limit {limit})")
if abs(i - target) > tol or tp > limit:
    sys.exit("::error::music loudness out of range")
PY
