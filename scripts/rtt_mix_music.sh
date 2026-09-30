#!/usr/bin/env bash
# Race Through Time - add a music track to a rendered (silent) video (DEC-072).
#
#   scripts/rtt_mix_music.sh VIDEO_IN MUSIC_IN VIDEO_OUT FINAL_HOLD_SEC
#
# - the track is looped if it is shorter than the video and cut to the video's exact length;
# - it fades out over the last FINAL_HOLD_SEC seconds (the final table, under YouTube's end screen);
# - it is loudness-normalised in two passes (ffmpeg loudnorm, linear) to about -16 LUFS integrated with
#   true peak aimed at -1.5 dBTP, then encoded AAC 320 kb/s 48 kHz stereo; the video stream is copied
#   untouched;
# - the result is measured again (ebur128, true peak) and the script FAILS unless the integrated
#   loudness is within 1 LU of -16 LUFS and the true peak is at most -1.0 dBTP.
# Needs ffmpeg, ffprobe and python3. Prints only numbers, never the file's contents.
set -euo pipefail
IN=$1; MUSIC=$2; OUT=$3; HOLD=$4
TARGET_I=-16; TARGET_TP=-1.5; LIMIT_TP=-1.0; TOL=1.0
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

D=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$IN")
FS=$(python3 -c "print(max(0.0, $D - $HOLD))")
echo "video ${D} s; music fades out from ${FS} s over ${HOLD} s"

# 1. loop, cut to length, fade out (48 kHz stereo PCM)
ffmpeg -nostdin -hide_banner -loglevel error -y -stream_loop -1 -i "$MUSIC" -t "$D" \
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
