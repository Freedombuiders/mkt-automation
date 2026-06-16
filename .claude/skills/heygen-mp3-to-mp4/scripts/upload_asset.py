#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31"]
# ///
"""
Upload an audio file to HeyGen as an asset and return the asset_id.

The HeyGen MCP server (post-2026 reshape) no longer exposes an upload tool —
only `create_video_from_avatar` / `get_video` etc. To lip-sync from a local MP3
the API still requires either an `audioAssetId` (uploaded asset) or an `audioUrl`
(public HTTPS URL). This helper performs the asset upload via the documented
REST endpoint `POST https://upload.heygen.com/v1/asset` with `X-Api-Key` header.

Usage:
    uv run upload_asset.py <mp3_path> [--key-file PATH] [--quiet]

Outputs (stdout, one line):
    OK <asset_id>

Exit codes:
    0 — upload succeeded
    1 — file missing / api error / no api key

The API key is read from (in order):
    1. --key-file flag
    2. HEYGEN_API_KEY env var
    3. .env in current dir
    4. ~/Documents/GitHub/hoang-ai-marketing/.env (canonical fallback for the
       Hoang marketing setup — placeholder keys in claudeclaw-os/.env.local
       are intentionally left as `your_*` stubs)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import requests

ENDPOINT = "https://upload.heygen.com/v1/asset"
DEFAULT_KEY_FILES = [
    Path(".env.local"),
    Path(".env"),
    Path.home() / "Documents" / "GitHub" / "hoang-ai-marketing" / ".env",
]


def _read_key_from_env_file(path: Path) -> str | None:
    if not path.exists():
        return None
    for line in path.read_text().splitlines():
        m = re.match(r'^\s*HEYGEN_API_KEY\s*=\s*"?([^"\s#]+)"?\s*$', line)
        if not m:
            continue
        val = m.group(1).strip()
        # Skip placeholder stubs
        if val.startswith("your_") or "placeholder" in val.lower() or val == "":
            continue
        return val
    return None


def resolve_api_key(explicit: str | None) -> str | None:
    if explicit:
        return _read_key_from_env_file(Path(explicit)) or explicit
    if env := os.environ.get("HEYGEN_API_KEY", "").strip():
        if not env.startswith("your_") and "placeholder" not in env.lower():
            return env
    for p in DEFAULT_KEY_FILES:
        if val := _read_key_from_env_file(p):
            return val
    return None


def content_type_for(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".m4a": "audio/mp4",
        ".aac": "audio/aac",
        ".ogg": "audio/ogg",
    }.get(ext, "application/octet-stream")


def upload(mp3_path: Path, api_key: str, quiet: bool) -> str:
    if not mp3_path.exists():
        print(f"MISSING {mp3_path}", file=sys.stderr)
        sys.exit(1)
    ctype = content_type_for(mp3_path)
    if not quiet:
        print(f"[upload] POST {ENDPOINT} ({mp3_path.name}, {ctype})", file=sys.stderr)
    resp = requests.post(
        ENDPOINT,
        headers={"X-Api-Key": api_key, "Content-Type": ctype},
        data=mp3_path.read_bytes(),
        timeout=120,
    )
    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text[:500]}
    if resp.status_code >= 400 or body.get("code", 100) != 100:
        print(f"ERROR status={resp.status_code} body={body}", file=sys.stderr)
        sys.exit(1)
    asset_id = body.get("data", {}).get("id")
    if not asset_id:
        print(f"ERROR missing asset id in response: {body}", file=sys.stderr)
        sys.exit(1)
    return asset_id


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mp3_path", help="Path to the audio file to upload")
    ap.add_argument(
        "--key-file",
        help="Path to a .env-format file containing HEYGEN_API_KEY",
        default=None,
    )
    ap.add_argument("--quiet", "-q", action="store_true")
    args = ap.parse_args()

    api_key = resolve_api_key(args.key_file)
    if not api_key:
        print(
            "ERROR HEYGEN_API_KEY not found. Set env var, --key-file, or add a real "
            "key to .env.local / ~/Documents/GitHub/hoang-ai-marketing/.env "
            "(placeholder stubs starting with 'your_' are skipped).",
            file=sys.stderr,
        )
        sys.exit(1)

    mp3_path = Path(args.mp3_path).expanduser().resolve()
    asset_id = upload(mp3_path, api_key, args.quiet)
    print(f"OK {asset_id}")


if __name__ == "__main__":
    main()
