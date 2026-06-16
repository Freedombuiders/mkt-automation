# /// script
# requires-python = ">=3.10"
# dependencies = ["pydub", "audioop-lts"]
# ///
"""
Split MP3 into segments based on SRT timestamps for HeyGen avatar rotation.
Groups consecutive SRT segments into chunks and assigns avatars in round-robin.

Usage: uv run scripts/split_audio.py <mp3_path> <srt_path> --avatars "id1:desc,id2:desc,id3:desc" [--min-chunk-duration 8] [--max-chunk-duration 20]
Output: JSON manifest with chunks + split MP3 files in output directory.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def parse_srt(srt_path: str) -> list[dict]:
    """Parse SRT file into list of segments with start/end in seconds."""
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    segments = []
    blocks = re.split(r"\n\n+", content.strip())
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        time_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[1],
        )
        if not time_match:
            continue
        g = time_match.groups()
        start = int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000
        end = int(g[4]) * 3600 + int(g[5]) * 60 + int(g[6]) + int(g[7]) / 1000
        text = " ".join(lines[2:]).strip()
        segments.append({"start": round(start, 3), "end": round(end, 3), "text": text})
    return segments


def group_segments_into_chunks(
    segments: list[dict],
    min_duration: float = 8.0,
    max_duration: float = 20.0,
) -> list[dict]:
    """Group consecutive SRT segments into chunks within duration bounds."""
    chunks = []
    current_chunk = None

    for seg in segments:
        if current_chunk is None:
            current_chunk = {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
                "segments": [seg],
            }
            continue

        chunk_duration = seg["end"] - current_chunk["start"]

        if chunk_duration <= max_duration:
            current_chunk["end"] = seg["end"]
            current_chunk["text"] += " " + seg["text"]
            current_chunk["segments"].append(seg)
        else:
            # Current chunk is full, finalize it
            if current_chunk["end"] - current_chunk["start"] >= min_duration:
                chunks.append(current_chunk)
            else:
                # Too short, extend with this segment anyway
                current_chunk["end"] = seg["end"]
                current_chunk["text"] += " " + seg["text"]
                current_chunk["segments"].append(seg)
                chunks.append(current_chunk)
            current_chunk = {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
                "segments": [seg],
            }

    if current_chunk:
        # Merge last chunk if too short
        if chunks and (current_chunk["end"] - current_chunk["start"]) < min_duration:
            chunks[-1]["end"] = current_chunk["end"]
            chunks[-1]["text"] += " " + current_chunk["text"]
            chunks[-1]["segments"].extend(current_chunk["segments"])
        else:
            chunks.append(current_chunk)

    return chunks


def main():
    parser = argparse.ArgumentParser(description="Split MP3 by SRT for HeyGen avatar rotation")
    parser.add_argument("mp3_path", help="Path to source MP3")
    parser.add_argument("srt_path", help="Path to SRT file")
    parser.add_argument("--avatars", required=True, help='Avatar list: "id1:description,id2:description,id3:description"')
    parser.add_argument("--min-chunk-duration", type=float, default=8.0, help="Min chunk duration in seconds")
    parser.add_argument("--max-chunk-duration", type=float, default=20.0, help="Max chunk duration in seconds")
    parser.add_argument("--output-dir", help="Output directory (default: mp3_dir/chunks)")
    args = parser.parse_args()

    mp3_path = Path(args.mp3_path).resolve()
    srt_path = Path(args.srt_path).resolve()

    if not mp3_path.exists():
        print(f"Error: {mp3_path} not found", file=sys.stderr)
        sys.exit(1)
    if not srt_path.exists():
        print(f"Error: {srt_path} not found", file=sys.stderr)
        sys.exit(1)

    # Parse avatars
    avatars = []
    for item in args.avatars.split(","):
        parts = item.strip().split(":", 1)
        avatar_id = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else ""
        avatars.append({"id": avatar_id, "description": description})

    if not avatars:
        print("Error: at least one avatar required", file=sys.stderr)
        sys.exit(1)

    # Parse SRT
    segments = parse_srt(str(srt_path))
    if not segments:
        print("Error: no segments found in SRT", file=sys.stderr)
        sys.exit(1)

    # Group into chunks
    chunks = group_segments_into_chunks(segments, args.min_chunk_duration, args.max_chunk_duration)

    # Setup output
    output_dir = Path(args.output_dir) if args.output_dir else mp3_path.parent / "chunks"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Split audio
    from pydub import AudioSegment
    audio = AudioSegment.from_mp3(str(mp3_path))

    manifest = {"source_mp3": str(mp3_path), "avatars": avatars, "chunks": []}

    for i, chunk in enumerate(chunks):
        avatar = avatars[i % len(avatars)]
        chunk_filename = f"chunk_{i:03d}.mp3"
        chunk_path = output_dir / chunk_filename

        start_ms = int(chunk["start"] * 1000)
        end_ms = int(chunk["end"] * 1000)
        segment_audio = audio[start_ms:end_ms]
        segment_audio.export(str(chunk_path), format="mp3")

        duration = chunk["end"] - chunk["start"]
        manifest["chunks"].append({
            "index": i,
            "chunk_file": chunk_filename,
            "chunk_path": str(chunk_path),
            "start": chunk["start"],
            "end": chunk["end"],
            "duration": round(duration, 3),
            "text": chunk["text"],
            "avatar_id": avatar["id"],
            "avatar_description": avatar["description"],
            "heygen_video_id": None,  # filled after HeyGen submission
            "heygen_video_url": None,  # filled after HeyGen completion
            "local_video_path": None,  # filled after download
        })

    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"Split into {len(manifest['chunks'])} chunks:")
    for c in manifest["chunks"]:
        print(f"  [{c['index']:03d}] {c['duration']:.1f}s | avatar: {c['avatar_id']} ({c['avatar_description']}) | {c['text'][:60]}...")
    print(f"\nManifest: {manifest_path}")
    print(f"Chunks dir: {output_dir}")


if __name__ == "__main__":
    main()
