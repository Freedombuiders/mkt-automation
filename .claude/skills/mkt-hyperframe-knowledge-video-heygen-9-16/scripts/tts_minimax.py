#!/usr/bin/env python3
"""
MiniMax T2A v2 TTS + Whisper word alignment
────────────────────────────────────────────
Drop-in alternative to tts.py (ElevenLabs). Same inputs, same outputs:
takes a Markdown script, writes audio/full.mp3 + audio/alignment.json
in the exact format map_beats.py and the caption builder consume.

MiniMax does NOT return word timestamps, so alignment is recovered by
running local OpenAI Whisper (word_timestamps=True) on the generated MP3.
Whisper transcribes what was SPOKEN, so the `words` array may differ
slightly from the script text — pick beat anchors that are plain words
(no digits, no abbreviations) and map_beats.py will match fine.

ENV:
  MINIMAX_API_KEY     required
  MINIMAX_GROUP_ID    required
  MINIMAX_VOICE_ID    required (system voice or cloned voice id)
  MINIMAX_MODEL       optional, defaults to "speech-02-hd"
  MINIMAX_API_BASE    optional, defaults to "https://api.minimax.io"
                      (China accounts: https://api.minimaxi.com)

Deps: requests, ffmpeg/ffprobe on PATH, and `pip install -U openai-whisper`
for the alignment step.

Usage (mirror of tts.py):
  python tts_minimax.py \
    --script  <OUT>/script.md \
    --out-audio  <OUT>/audio/full.mp3 \
    --out-alignment  <OUT>/audio/alignment.json \
    [--lang vi] [--whisper-model small]

Output alignment.json format (same consumer contract as tts.py — the
`characters` array is empty because downstream only reads `words`):
  {
    "text": "...", "duration_ms": 87340,
    "characters": [],
    "words": [{"word": "The", "start_ms": 0, "end_ms": 240}, ...]
  }
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests


DEFAULT_MODEL = "speech-02-hd"        # chậm hơn turbo nhưng tiếng Việt tốt hơn
DEFAULT_API_BASE = "https://api.minimax.io"
MAX_CHARS_PER_REQUEST = 4500          # MiniMax limit ~10k; giữ chunk nhỏ cho ổn định


def strip_markdown(md_text: str) -> str:
    """Strip markdown formatting so TTS reads cleanly (same rules as tts.py)."""
    text = md_text
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"^#{1,6}\s+(.*)$", r"\1.", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("—", ", ").replace("–", ", ")
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def split_into_chunks(text: str, max_chars: int = MAX_CHARS_PER_REQUEST) -> list[str]:
    """Split text into chunks under max_chars at sentence boundaries (same as tts.py)."""
    if len(text) <= max_chars:
        return [text]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: list[str] = []
    current = ""
    for s in sentences:
        if not s.strip():
            continue
        if len(s) > max_chars:
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
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path),
    ]).decode().strip()
    return int(round(float(out) * 1000))


def ffmpeg_concat_mp3(parts: list[Path], output: Path) -> None:
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


def call_minimax_t2a(text: str, voice_id: str, model: str,
                     api_key: str, group_id: str, base: str) -> bytes:
    """Call MiniMax t2a_v2 (non-streaming). Audio comes back as a HEX string in JSON."""
    url = f"{base.rstrip('/')}/v1/t2a_v2?GroupId={group_id}"
    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": voice_id, "speed": 1.0, "vol": 1.0, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    }
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload, timeout=300,
    )
    if resp.status_code != 200:
        sys.stderr.write(f"[tts-minimax] HTTP {resp.status_code}: {resp.text[:500]}\n")
        resp.raise_for_status()
    body = resp.json()
    base_resp = body.get("base_resp") or {}
    if base_resp.get("status_code") not in (0, None):
        raise RuntimeError(
            f"MiniMax error {base_resp.get('status_code')}: {base_resp.get('status_msg')}"
        )
    audio_hex = (body.get("data") or {}).get("audio")
    if not audio_hex:
        raise RuntimeError(f"No audio in MiniMax response: {json.dumps(body)[:500]}")
    return bytes.fromhex(audio_hex)


def whisper_word_alignment(mp3_path: Path, lang: str, whisper_model: str) -> list[dict]:
    """Transcribe the MP3 with local Whisper and return tts.py-style words array."""
    try:
        import whisper  # type: ignore
    except ImportError:
        sys.stderr.write(
            "[tts-minimax] openai-whisper is required for alignment:\n"
            "    pip install -U openai-whisper\n"
            "(or use the ElevenLabs provider — scripts/tts.py — which has native timestamps)\n"
        )
        raise SystemExit(2)

    sys.stderr.write(f"[tts-minimax] whisper model={whisper_model} lang={lang} — transcribing for alignment...\n")
    model = whisper.load_model(whisper_model)
    result = model.transcribe(str(mp3_path), language=lang, word_timestamps=True, verbose=False)

    words: list[dict] = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            token = (w.get("word") or "").strip()
            if not token:
                continue
            words.append({
                "word": token,
                "start_ms": int(round(float(w["start"]) * 1000)),
                "end_ms": int(round(float(w["end"]) * 1000)),
            })
    return words


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--script",        required=True, help="Path to script.md")
    p.add_argument("--out-audio",     required=True, help="Path to write MP3")
    p.add_argument("--out-alignment", required=True, help="Path to write alignment JSON")
    p.add_argument("--voice-id",      default=None)
    p.add_argument("--model-id",      default=None)
    p.add_argument("--lang",          default="vi", help="Whisper language hint (default vi)")
    p.add_argument("--whisper-model", default="small", help="Whisper model for alignment")
    args = p.parse_args()

    api_key = os.environ.get("MINIMAX_API_KEY")
    group_id = os.environ.get("MINIMAX_GROUP_ID")
    if not api_key or not group_id:
        sys.stderr.write("[tts-minimax] MINIMAX_API_KEY and MINIMAX_GROUP_ID env vars are required\n")
        return 2

    voice_id = args.voice_id or os.environ.get("MINIMAX_VOICE_ID")
    if not voice_id:
        sys.stderr.write("[tts-minimax] MINIMAX_VOICE_ID env var (or --voice-id) is required\n")
        return 2

    model = args.model_id or os.environ.get("MINIMAX_MODEL") or DEFAULT_MODEL
    base = os.environ.get("MINIMAX_API_BASE") or DEFAULT_API_BASE

    script_path = Path(args.script)
    out_audio = Path(args.out_audio)
    out_alignment = Path(args.out_alignment)
    out_audio.parent.mkdir(parents=True, exist_ok=True)
    out_alignment.parent.mkdir(parents=True, exist_ok=True)

    if not script_path.exists():
        sys.stderr.write(f"[tts-minimax] script not found: {script_path}\n")
        return 2

    plain = strip_markdown(script_path.read_text(encoding="utf-8"))
    if not plain:
        sys.stderr.write("[tts-minimax] script is empty after stripping markdown\n")
        return 2

    chunks = split_into_chunks(plain)
    sys.stderr.write(
        f"[tts-minimax] voice={voice_id} model={model} chars={len(plain)} chunks={len(chunks)}\n"
    )

    tmpdir = Path(tempfile.mkdtemp(prefix="tts-minimax-"))
    chunk_paths: list[Path] = []
    try:
        max_workers = min(4, len(chunks))
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            audio_parts = list(ex.map(
                lambda c: call_minimax_t2a(c, voice_id, model, api_key, group_id, base),
                chunks,
            ))
        for i, audio in enumerate(audio_parts, start=1):
            cp = tmpdir / f"chunk-{i:02d}.mp3"
            cp.write_bytes(audio)
            chunk_paths.append(cp)

        if len(chunk_paths) == 1:
            out_audio.write_bytes(chunk_paths[0].read_bytes())
        else:
            ffmpeg_concat_mp3(chunk_paths, out_audio)
        sys.stderr.write(f"[tts-minimax] wrote audio: {out_audio} ({out_audio.stat().st_size} bytes)\n")
    finally:
        for cp in chunk_paths:
            cp.unlink(missing_ok=True)
        try:
            tmpdir.rmdir()
        except OSError:
            pass

    duration_ms = ffprobe_duration_ms(out_audio)
    words = whisper_word_alignment(out_audio, args.lang, args.whisper_model)

    payload = {
        "text": plain,
        "voice_id": voice_id,
        "model_id": model,
        "provider": "minimax",
        "duration_ms": duration_ms,
        "characters": [],   # downstream (map_beats.py, captions) only reads `words`
        "words": words,
    }
    out_alignment.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.stderr.write(
        f"[tts-minimax] wrote alignment: {out_alignment} (words={len(words)} duration={duration_ms}ms)\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
