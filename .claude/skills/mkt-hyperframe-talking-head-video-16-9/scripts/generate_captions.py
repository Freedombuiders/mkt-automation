#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["jinja2>=3.1"]
# ///
"""Generate `compositions/captions.html` for the 16:9 video pipeline.

Captions are rendered from a constant Jinja template
(`assets/templates/captions.html.j2`) — only the data array changes per video.

Source order for the caption track (first match wins):

  1. workspace/captions.json     — orchestrator-curated, preferred for VN.
                                    Format: [{"text": "...", "start": s, "end": s}, ...]
                                    Use this when you want clean script-derived text
                                    instead of raw Whisper output.

  2. workspace/voiceover_segments.json — raw Whisper output, fallback.
                                          Each segment becomes one caption block.
                                          Vietnamese accuracy is rough at the `base` model
                                          (numbers + brand names get mangled). Acceptable
                                          for first-pass; replace with a curated
                                          captions.json before the final render.

Usage:

    uv run generate_captions.py --workspace workspace/content/YYYY-MM-DD/<slug>/

Output:
    workspace/.../compositions/captions.html  (constant template + injected data)

The mounted composition is then auto-detected by `generate_root_index.py`,
which adds the `.captions-mount` overlay to `index.html` at z-index 28
(above slide, below avatar frame).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_ROOT / "assets" / "templates"
TEMPLATE_NAME = "captions.html.j2"


def load_captions(workspace: Path) -> list[dict]:
    """Return the caption track. Prefer curated `captions.json`; fall back to Whisper segments."""
    curated = workspace / "captions.json"
    if curated.exists():
        data = json.loads(curated.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            raise ValueError(f"{curated} is empty or not a list")
        return data

    segments = workspace / "voiceover_segments.json"
    if segments.exists():
        raw = json.loads(segments.read_text(encoding="utf-8"))
        # Whisper segments: [{id, start, end, text, words}, ...]
        return [
            {
                "text": s["text"].strip(),
                "start": float(s["start"]),
                "end": float(s["end"]),
            }
            for s in raw
            if s.get("text", "").strip()
        ]

    raise FileNotFoundError(
        f"Neither captions.json nor voiceover_segments.json found in {workspace}"
    )


def render(workspace: Path) -> Path:
    captions = load_captions(workspace)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,  # JSON injection — no HTML escaping
        keep_trailing_newline=True,
    )
    tpl = env.get_template(TEMPLATE_NAME)
    html = tpl.render(
        captions_json=json.dumps(captions, ensure_ascii=False, indent=None)
    )

    out = workspace / "compositions" / "captions.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    total = max((c["end"] for c in captions), default=0.0)
    src_label = "captions.json" if (workspace / "captions.json").exists() else "voiceover_segments.json"
    print(f"[captions] wrote {out} — {len(captions)} chunks · {total:.2f}s coverage · source: {src_label}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace", "-w", required=True, help="Workspace folder")
    args = ap.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.is_dir():
        print(f"ERROR workspace not a directory: {workspace}", file=sys.stderr)
        sys.exit(1)

    try:
        render(workspace)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
