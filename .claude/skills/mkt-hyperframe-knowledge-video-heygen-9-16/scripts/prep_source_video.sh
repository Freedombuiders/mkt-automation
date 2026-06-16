#!/usr/bin/env bash
# Source-video helpers for the HeyGen SPLIT/PIP pipeline.
#
#   placeholder <project_dir>
#       Make a dark 720x1280 placeholder source.mp4 (real audio from audio/full.mp3)
#       so you can lint/inspect/draft-render the FULL composition WHILE HeyGen renders
#       in the background. Swap with the real avatar later via `reencode`.
#
#   reencode <raw_heygen.mp4> <out_source.mp4>
#       Re-encode the HeyGen MP4 with DENSE keyframes (1s GOP @ 30fps). HeyGen
#       output is 25fps with ~8s keyframe spacing, which makes the hyperframes
#       renderer warn "sparse keyframes -> seek failures / frame freezing".
#       This fixes it. ALWAYS run this on the downloaded HeyGen mp4 before render.
set -euo pipefail

cmd="${1:-}"
case "$cmd" in
  placeholder)
    OUT="${2:?usage: prep_source_video.sh placeholder <project_dir>}"
    DUR="$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$OUT/audio/full.mp3")"
    ffmpeg -y -f lavfi -i "color=c=0x141a28:s=720x1280:d=$DUR" -i "$OUT/audio/full.mp3" \
      -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -shortest "$OUT/source.mp4"
    echo "placeholder source.mp4 written ($DUR s)"
    ;;
  reencode)
    RAW="${2:?usage: prep_source_video.sh reencode <raw.mp4> <out.mp4>}"
    DST="${3:?usage: prep_source_video.sh reencode <raw.mp4> <out.mp4>}"
    ffmpeg -y -i "$RAW" \
      -c:v libx264 -r 30 -g 30 -keyint_min 30 -pix_fmt yuv420p -movflags +faststart \
      -c:a aac -b:a 160k "$DST"
    echo "re-encoded -> $DST"
    ffprobe -v error -select_streams v -show_entries stream=width,height,avg_frame_rate -of csv=p=0 "$DST"
    ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$DST"
    ;;
  *)
    echo "usage:"
    echo "  prep_source_video.sh placeholder <project_dir>"
    echo "  prep_source_video.sh reencode <raw_heygen.mp4> <out_source.mp4>"
    exit 1
    ;;
esac
