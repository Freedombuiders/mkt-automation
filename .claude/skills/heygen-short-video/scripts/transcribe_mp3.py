# /// script
# requires-python = ">=3.10"
# dependencies = ["openai-whisper", "pydub"]
# ///
"""
Transcribe MP3 to SRT using OpenAI Whisper (local).
Usage: uv run scripts/transcribe_mp3.py <mp3_path> [--language vi] [--model base]
Output: SRT file next to the MP3 + segments JSON for splitting.
"""
import argparse
import json
import sys
from pathlib import Path


def format_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    parser = argparse.ArgumentParser(description="Transcribe MP3 to SRT using Whisper")
    parser.add_argument("mp3_path", help="Path to MP3 file")
    parser.add_argument("--language", default="vi", help="Language code (default: vi)")
    parser.add_argument("--model", default="base", help="Whisper model: tiny/base/small/medium/large (default: base)")
    parser.add_argument("--output-dir", help="Output directory (default: same as MP3)")
    args = parser.parse_args()

    mp3_path = Path(args.mp3_path).resolve()
    if not mp3_path.exists():
        print(f"Error: {mp3_path} not found", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else mp3_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = mp3_path.stem

    print(f"Loading Whisper model '{args.model}'...")
    import whisper
    model = whisper.load_model(args.model)

    print(f"Transcribing {mp3_path.name} (language={args.language})...")
    result = model.transcribe(str(mp3_path), language=args.language, verbose=False, word_timestamps=True)

    # Write SRT
    srt_path = output_dir / f"{stem}.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"], 1):
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(seg['start'])} --> {format_srt_time(seg['end'])}\n")
            f.write(f"{seg['text'].strip()}\n\n")
    print(f"SRT saved: {srt_path}")

    # Write segments JSON (for splitting) — includes word-level timestamps
    segments = []
    for seg in result["segments"]:
        seg_data = {
            "id": seg["id"],
            "start": round(seg["start"], 3),
            "end": round(seg["end"], 3),
            "text": seg["text"].strip(),
        }
        if "words" in seg:
            seg_data["words"] = [
                {
                    "word": w["word"].strip(),
                    "start": round(w["start"], 3),
                    "end": round(w["end"], 3),
                }
                for w in seg["words"]
                if w["word"].strip()
            ]
        segments.append(seg_data)

    segments_path = output_dir / f"{stem}_segments.json"
    with open(segments_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)
    print(f"Segments JSON saved: {segments_path}")

    # Print summary
    total_duration = result["segments"][-1]["end"] if result["segments"] else 0
    print(f"\nSummary: {len(segments)} segments, {total_duration:.1f}s total")


if __name__ == "__main__":
    main()
