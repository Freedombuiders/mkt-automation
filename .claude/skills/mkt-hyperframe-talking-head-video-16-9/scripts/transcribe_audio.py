#!/usr/bin/env python3
"""Transcribe voiceover.mp3 → transcript.json (word-level Vietnamese).

Strategy:
1. If `mkt-ai-video-extract-srt-segment` skill is available locally, prefer it
   (provides SRT + segments JSON in one shot).
2. Otherwise fall back to `whisper` CLI directly with --word_timestamps True.

Output:
    <workspace>/transcript.json   — list of {text, start, end} word-level entries

Usage:
    python3 transcribe_audio.py --workspace <folder>
    python3 transcribe_audio.py                       # workspace = CWD
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run_whisper_cli(mp3_path: Path, out_dir: Path) -> Path:
    """Invoke local `whisper` CLI to produce a JSON with word_timestamps.
    Returns path to written word-level transcript.json.
    """
    cmd = [
        'whisper', str(mp3_path),
        '--model', 'medium',
        '--language', 'vi',
        '--word_timestamps', 'True',
        '--output_format', 'json',
        '--output_dir', str(out_dir),
        '--verbose', 'False',
    ]
    print(f'[transcribe] {" ".join(cmd)}', file=sys.stderr)
    subprocess.check_call(cmd)

    # Whisper writes <stem>.json next to out_dir.
    stem = mp3_path.stem
    raw = out_dir / f'{stem}.json'
    if not raw.exists():
        raise FileNotFoundError(f'Whisper output not found: {raw}')

    # Normalize to a flat word-level array.
    with raw.open() as f:
        data = json.load(f)

    words = []
    for seg in data.get('segments', []):
        for w in seg.get('words', []) or []:
            text = (w.get('word') or '').strip()
            if not text:
                continue
            words.append({
                'text': text,
                'start': float(w.get('start', 0.0)),
                'end': float(w.get('end', 0.0)),
            })

    out = out_dir / 'transcript.json'
    with out.open('w') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', '-w', default='.', help='Workspace folder containing voiceover.mp3')
    ap.add_argument('--mp3', default=None, help='Override MP3 path (default: <workspace>/voiceover.mp3)')
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    mp3 = Path(args.mp3) if args.mp3 else workspace / 'voiceover.mp3'

    if not mp3.exists():
        print(f'[transcribe] ERROR: {mp3} not found', file=sys.stderr)
        sys.exit(1)

    out = run_whisper_cli(mp3, workspace)
    print(f'[transcribe] wrote {out}')

    with out.open() as f:
        words = json.load(f)
    if words:
        print(f'[transcribe] {len(words)} words, last end {words[-1]["end"]:.2f}s')


if __name__ == '__main__':
    main()
