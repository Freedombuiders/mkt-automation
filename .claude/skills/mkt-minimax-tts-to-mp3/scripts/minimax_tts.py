#!/usr/bin/env python3
"""MiniMax T2A v2 -> MP3.

Usage:
    python3 minimax_tts.py --text-file script.txt --out voiceover.mp3
    python3 minimax_tts.py --text "Xin chào" --out hello.mp3 --voice-id female-shaonv

Reads MINIMAX_API_KEY, MINIMAX_GROUP_ID, MINIMAX_VOICE_ID, MINIMAX_API_BASE,
MINIMAX_MODEL from .env in the current directory (or real env vars, which win).
The non-streaming T2A v2 endpoint returns audio as a HEX string inside JSON —
this script decodes it to raw MP3 bytes.
"""

import argparse
import json
import os
import sys
import urllib.request


def load_env_file(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip("'\"")
            if key and val and key not in os.environ:
                os.environ[key] = val


def main():
    p = argparse.ArgumentParser()
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text")
    src.add_argument("--text-file")
    p.add_argument("--out", required=True)
    p.add_argument("--voice-id", default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--speed", type=float, default=1.0)
    args = p.parse_args()

    load_env_file()
    api_key = os.environ.get("MINIMAX_API_KEY")
    group_id = os.environ.get("MINIMAX_GROUP_ID")
    if not api_key:
        sys.exit("Missing MINIMAX_API_KEY (set it in .env)")

    voice_id = args.voice_id or os.environ.get("MINIMAX_VOICE_ID")
    if not voice_id:
        sys.exit("Missing voice id: pass --voice-id or set MINIMAX_VOICE_ID in .env")

    model = args.model or os.environ.get("MINIMAX_MODEL", "speech-02-hd")
    base = os.environ.get("MINIMAX_API_BASE", "https://api.minimax.io").rstrip("/")

    text = args.text if args.text else open(args.text_file, encoding="utf-8").read()
    text = text.strip()
    if not text:
        sys.exit("Empty text")
    if len(text) > 10000:
        sys.exit(f"Text too long ({len(text)} chars, limit ~10000). Split it first.")

    body = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": args.speed,
            "vol": 1.0,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }

    url = f"{base}/v1/t2a_v2"
    if group_id:
        url += f"?GroupId={group_id}"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    base_resp = payload.get("base_resp") or {}
    if base_resp.get("status_code") not in (0, None):
        sys.exit(f"MiniMax error {base_resp.get('status_code')}: {base_resp.get('status_msg')}")

    audio_hex = (payload.get("data") or {}).get("audio")
    if not audio_hex:
        sys.exit(f"No audio in response: {json.dumps(payload)[:500]}")

    audio = bytes.fromhex(audio_hex)
    with open(args.out, "wb") as f:
        f.write(audio)

    extra = payload.get("extra_info") or {}
    print(json.dumps({
        "out": os.path.abspath(args.out),
        "bytes": len(audio),
        "duration_ms": extra.get("audio_length"),
        "usage_characters": extra.get("usage_characters"),
        "voice_id": voice_id,
        "model": model,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
