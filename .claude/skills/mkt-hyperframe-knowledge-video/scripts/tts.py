#!/usr/bin/env python3
"""
ElevenLabs v3 TTS + Forced Alignment
─────────────────────────────────────
Takes a Markdown script (with optional ## beat headers), strips markdown,
calls ElevenLabs `text-to-speech/<voice>/with-timestamps`, saves the
MP3 + a word-level alignment JSON.

ENV:
  ELEVENLABS_API_KEY    required
  ELEVENLABS_VOICE_ID   optional, defaults to "pNInz6obpgDQGcFmaJgB" (Adam)
  ELEVENLABS_MODEL_ID   optional, defaults to "eleven_v3" (latest, with native alignment)

Usage:
  python tts.py \
    --script  workspace/content/2026-05-28/<slug>/script.md \
    --out-audio  workspace/content/2026-05-28/<slug>/audio/full.mp3 \
    --out-alignment  workspace/content/2026-05-28/<slug>/audio/alignment.json

Output alignment.json format:
  {
    "text": "Full plain text fed to TTS",
    "duration_ms": 87340,
    "characters": [
      {"char": "T", "start_ms": 0,    "end_ms": 35},
      {"char": "h", "start_ms": 35,   "end_ms": 70},
      ...
    ],
    "words": [
      {"word": "The",  "start_ms": 0,    "end_ms": 240},
      {"word": "biggest", "start_ms": 240,  "end_ms": 680},
      ...
    ]
  }

The `words` array is derived from `characters` by collapsing on whitespace
boundaries. Downstream consumers (caption builder, beat mapper) only need
the words array.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests


ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"
DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB"   # Adam — male, baritone, professional
DEFAULT_MODEL_ID = "eleven_v3"               # v3 with native timestamps
MAX_CHARS_PER_REQUEST = 4500                 # ElevenLabs hard limit is 5000; leave headroom


def strip_markdown(md_text: str) -> str:
    """Strip markdown formatting so TTS reads cleanly.

    Removes:
      - Heading markers (## Beat 1, # Title) — keeps the visible text on
        a new line so paragraph breaks survive
      - Bold/italic asterisks
      - Inline code backticks
      - Link syntax [text](url) → text
      - HTML comments
      - Em dashes replaced with commas (ElevenLabs is unpredictable on em)
    """
    text = md_text

    # Strip HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # Strip heading markers but keep the heading text as a sentence
    text = re.sub(r"^#{1,6}\s+(.*)$", r"\1.", text, flags=re.MULTILINE)

    # Bold + italic markers
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)

    # Inline code
    text = re.sub(r"`([^`]+)`", r"\1", text)

    # Links [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Em / en dashes → comma + space
    text = text.replace("—", ", ").replace("–", ", ")

    # Collapse multiple newlines into a single space (TTS handles paragraphs
    # better than abrupt newlines)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\n", " ", text)

    # Collapse multi-spaces
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def chars_to_words(chars: list[dict]) -> list[dict]:
    """Collapse character-level timestamps into word-level."""
    words: list[dict] = []
    current_word_chars: list[str] = []
    word_start_ms: float | None = None
    word_end_ms: float | None = None

    for c in chars:
        ch = c["char"]
        if ch.isspace():
            if current_word_chars:
                words.append({
                    "word": "".join(current_word_chars),
                    "start_ms": int(round(word_start_ms or 0)),
                    "end_ms":   int(round(word_end_ms or 0)),
                })
                current_word_chars = []
                word_start_ms = None
                word_end_ms = None
            continue
        if word_start_ms is None:
            word_start_ms = c["start_ms"]
        word_end_ms = c["end_ms"]
        current_word_chars.append(ch)

    if current_word_chars:
        words.append({
            "word": "".join(current_word_chars),
            "start_ms": int(round(word_start_ms or 0)),
            "end_ms":   int(round(word_end_ms or 0)),
        })
    return words


def split_into_chunks(text: str, max_chars: int = MAX_CHARS_PER_REQUEST) -> list[str]:
    """Split text into chunks under max_chars, breaking only at sentence boundaries.

    Walks the text, greedily packing sentences (split on '. ', '! ', '? ') into
    chunks. If a single sentence exceeds max_chars, falls back to splitting on
    ', ' boundaries within that sentence.
    """
    if len(text) <= max_chars:
        return [text]

    # First split into sentences. Keep the terminator with each sentence.
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: list[str] = []
    current = ""
    for s in sentences:
        if not s.strip():
            continue
        if len(s) > max_chars:
            # Sentence itself too long — split on comma boundaries.
            sub_parts = re.split(r"(?<=,)\s+", s)
            for sub in sub_parts:
                if len(current) + len(sub) + 1 > max_chars and current:
                    chunks.append(current.strip())
                    current = sub
                else:
                    current = f"{current} {sub}".strip()
            continue
        if len(current) + len(s) + 1 > max_chars and current:
            chunks.append(current.strip())
            current = s
        else:
            current = f"{current} {s}".strip()
    if current:
        chunks.append(current.strip())
    return chunks


def ffprobe_duration_ms(mp3_path: Path) -> int:
    """Return MP3 duration in ms via ffprobe."""
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path),
    ]).decode().strip()
    return int(round(float(out) * 1000))


def ffmpeg_concat_mp3(parts: list[Path], output: Path) -> None:
    """Concat MP3 files into output using ffmpeg concat demuxer (re-encoded for safety)."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in parts:
            f.write(f"file '{p.resolve()}'\n")
        list_path = Path(f.name)
    try:
        subprocess.check_call([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(list_path),
            "-c:a", "libmp3lame", "-b:a", "128k",
            str(output),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        list_path.unlink(missing_ok=True)


def call_elevenlabs_with_timestamps(text: str, voice_id: str, model_id: str, api_key: str) -> dict:
    """Call ElevenLabs `text-to-speech/<voice>/with-timestamps` endpoint.

    Returns:
      {
        "audio_base64": "...",
        "alignment": {
          "characters": [...],
          "character_start_times_seconds": [...],
          "character_end_times_seconds":   [...],
        },
        "normalized_alignment": {...}
      }
    """
    url = f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}/with-timestamps"
    headers = {
        "xi-api-key": api_key,
        "accept": "application/json",
        "content-type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
        "output_format": "mp3_44100_128",
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    if resp.status_code != 200:
        sys.stderr.write(f"[tts] ElevenLabs returned {resp.status_code}: {resp.text}\n")
        resp.raise_for_status()
    return resp.json()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--script",         required=True, help="Path to script.md")
    p.add_argument("--out-audio",      required=True, help="Path to write MP3")
    p.add_argument("--out-alignment",  required=True, help="Path to write alignment JSON")
    p.add_argument("--voice-id",       default=None)
    p.add_argument("--model-id",       default=None)
    args = p.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.stderr.write("[tts] ELEVENLABS_API_KEY env var is required\n")
        return 2

    voice_id = args.voice_id or os.environ.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID
    model_id = args.model_id or os.environ.get("ELEVENLABS_MODEL_ID") or DEFAULT_MODEL_ID

    script_path = Path(args.script)
    out_audio = Path(args.out_audio)
    out_alignment = Path(args.out_alignment)
    out_audio.parent.mkdir(parents=True, exist_ok=True)
    out_alignment.parent.mkdir(parents=True, exist_ok=True)

    if not script_path.exists():
        sys.stderr.write(f"[tts] script not found: {script_path}\n")
        return 2

    raw = script_path.read_text(encoding="utf-8")
    plain = strip_markdown(raw)
    if not plain:
        sys.stderr.write("[tts] script is empty after stripping markdown\n")
        return 2

    chunks = split_into_chunks(plain)
    sys.stderr.write(f"[tts] voice={voice_id} model={model_id} chars={len(plain)} chunks={len(chunks)}\n")

    all_characters: list[dict] = []
    chunk_mp3_paths: list[Path] = []
    tmpdir = Path(tempfile.mkdtemp(prefix="tts-chunks-"))

    try:
        # Network-bound — fan out HTTP calls in parallel. Order preserved via list index.
        max_workers = min(4, len(chunks))
        sys.stderr.write(f"[tts] fanning out {len(chunks)} chunks across {max_workers} workers\n")
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            responses = list(ex.map(
                lambda c: call_elevenlabs_with_timestamps(c, voice_id, model_id, api_key),
                chunks,
            ))

        # Sequential pass to write MP3s + accumulate offset_ms using REAL file durations.
        offset_ms = 0
        for i, (chunk, resp) in enumerate(zip(chunks, responses), start=1):
            chunk_mp3 = tmpdir / f"chunk-{i:02d}.mp3"
            chunk_mp3.write_bytes(base64.b64decode(resp["audio_base64"]))
            chunk_mp3_paths.append(chunk_mp3)

            al = resp.get("alignment") or resp.get("normalized_alignment") or {}
            chars_list = al.get("characters", [])
            starts = al.get("character_start_times_seconds", [])
            ends   = al.get("character_end_times_seconds", [])

            if not (len(chars_list) == len(starts) == len(ends)):
                sys.stderr.write(f"[tts] alignment arrays length mismatch in chunk {i}\n")
                return 3

            for j in range(len(chars_list)):
                all_characters.append({
                    "char": chars_list[j],
                    "start_ms": int(round(starts[j] * 1000)) + offset_ms,
                    "end_ms":   int(round(ends[j]   * 1000)) + offset_ms,
                })

            # Use actual file duration as offset for the next chunk so timestamps
            # match the concatenated audio, not just the last char's end time.
            chunk_dur_ms = ffprobe_duration_ms(chunk_mp3)
            offset_ms += chunk_dur_ms
            # Insert a synthetic space between chunks so word splitter sees a break.
            if i < len(chunks):
                all_characters.append({"char": " ", "start_ms": offset_ms, "end_ms": offset_ms})

        # Concat all chunks into final MP3.
        if len(chunk_mp3_paths) == 1:
            out_audio.write_bytes(chunk_mp3_paths[0].read_bytes())
        else:
            ffmpeg_concat_mp3(chunk_mp3_paths, out_audio)
        sys.stderr.write(f"[tts] wrote audio: {out_audio} ({out_audio.stat().st_size} bytes)\n")
    finally:
        for p in chunk_mp3_paths:
            p.unlink(missing_ok=True)
        try:
            tmpdir.rmdir()
        except OSError:
            pass

    characters = all_characters
    words = chars_to_words(characters)
    duration_ms = characters[-1]["end_ms"] if characters else 0

    payload = {
        "text": plain,
        "voice_id": voice_id,
        "model_id": model_id,
        "duration_ms": duration_ms,
        "characters": characters,
        "words": words,
    }
    out_alignment.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.stderr.write(f"[tts] wrote alignment: {out_alignment} (words={len(words)} duration={duration_ms}ms)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
