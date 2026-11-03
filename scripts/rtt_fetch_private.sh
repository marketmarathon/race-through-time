#!/usr/bin/env bash
# IQ-27: fetch an episode's private files (pictures, logos, Luke's badge and, with --music, the film's track) from the
# PRIVATE repo into ROOT/<kit>/ (the layout kits/thumbnails/README.md describes), and check every SHA-256.
#   GH_TOKEN=<secret> scripts/rtt_fetch_private.sh ROOT rtt-002 [rtt-003 ...] [--music]
# The file list is the episode's thumbnail config's `assets_list` (kits/thumbnails/rtt-###.json, private branch
# `private_ref`, then main); the music is the kit's music_rtt###.json (`private_path`, `sha256`). The token is only
# read by gh from GH_TOKEN and never printed. Stops on any mismatch. Used by thumbnails_v2.yml, rtt003_numfmt.yml and
# shorts_pilot.yml; the film workflows keep their own fetch steps unchanged.
set -euo pipefail
PRIVATE_REPO=${PRIVATE_REPO:-marketmarathon/race-through-time-private}
ROOT=$1; shift
MUSIC=no; EPS=()
for a in "$@"; do if [ "$a" = "--music" ]; then MUSIC=yes; else EPS+=("$a"); fi; done
[ -n "${GH_TOKEN:-}" ] || { echo "::error::GH_TOKEN (the secret RTT_PRIVATE_TOKEN) is not available"; exit 1; }
mkdir -p "$ROOT"; CHECK=$(mktemp)
get() {  # private path, ref, destination: the branch first, then main
  gh api -H 'Accept: application/vnd.github.raw' "repos/$PRIVATE_REPO/contents/$1?ref=$2" > "$3" 2>/dev/null \
    || gh api -H 'Accept: application/vnd.github.raw' "repos/$PRIVATE_REPO/contents/$1?ref=main" > "$3"
}
for e in "${EPS[@]}"; do
  c="kits/thumbnails/$e.json"
  REF=$(node -e "console.log(require('./$c').private_ref)"); LIST=$(node -e "console.log(require('./$c').assets_list)"); KIT=$(node -e "console.log(require('./$c').kit)")
  while read -r sum p; do
    case "$sum" in ''|'#'*) continue;; esac
    case "$p" in assets/rtt-[0-9][0-9][0-9]/*) rel=${p#assets/rtt-[0-9][0-9][0-9]/};; *) echo "::error::unexpected path $p"; exit 1;; esac
    dst="$ROOT/$KIT/$rel"; mkdir -p "$(dirname "$dst")"
    get "$p" "$REF" "$dst"
    printf '%s  %s\n' "$sum" "$dst" >> "$CHECK"
  done < "$LIST"
  if [ "$MUSIC" = yes ]; then
    m=$(ls kits/$KIT/music_rtt[0-9][0-9][0-9].json | head -1)
    mp=$(node -e "console.log(require('./$m').private_path)"); ms=$(node -e "console.log(require('./$m').sha256)")
    case "$mp" in assets/$KIT/*) ;; *) echo "::error::unexpected music path $mp"; exit 1;; esac
    dst="$ROOT/$KIT/${mp#assets/$KIT/}"; mkdir -p "$(dirname "$dst")"
    get "$mp" "$REF" "$dst"
    printf '%s  %s\n' "$ms" "$dst" >> "$CHECK"
  fi
done
sha256sum -c --quiet "$CHECK"
echo "$(wc -l < "$CHECK") private file(s) fetched into the runner's temporary folder, every SHA-256 checked"
rm -f "$CHECK"
