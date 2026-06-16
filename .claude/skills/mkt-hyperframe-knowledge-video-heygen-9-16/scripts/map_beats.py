#!/usr/bin/env python3
"""Map narrative beats to time ranges from audio/alignment.json.

Deterministic beat segmentation: each beat is anchored by the first few words
of its narration. We find where that word sequence starts in the alignment,
take its start_ms as the beat start; the next beat's start is this beat's end
(last beat ends at duration_ms).

Usage:
  python map_beats.py --project <OUT_DIR>

Reads:
  <OUT>/audio/alignment.json   (from tts.py)
  <OUT>/beats-spec.json        (orchestrator-authored, see schema below)
Writes:
  <OUT>/beats.json

beats-spec.json schema (orchestrator writes this from the script):
  [
    {"id": "scene-01-hook", "slug": "hook", "pattern": "hero",
     "anchor": ["y", "combinator"]},
    {"id": "scene-02-problem", "slug": "problem", "pattern": "stat-problem",
     "anchor": ["agency", "kiểu", "cũ"]},
    ...
  ]
  - anchor = lowercased words (diacritics kept) that uniquely start the beat.
  - First beat always starts at 0 regardless of its anchor's timestamp.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path


def norm(w: str) -> str:
    return re.sub(r"[^\w]", "", w, flags=re.UNICODE).lower()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="Project OUT dir")
    args = ap.parse_args()
    out = Path(args.project)

    align = json.loads((out / "audio" / "alignment.json").read_text(encoding="utf-8"))
    spec = json.loads((out / "beats-spec.json").read_text(encoding="utf-8"))
    words = align["words"]
    duration_ms = align["duration_ms"]
    nwords = [norm(w["word"]) for w in words]

    def find_seq(seq, start_from=0):
        L = len(seq)
        for i in range(start_from, len(nwords) - L + 1):
            if nwords[i:i + L] == seq:
                return i
        return -1

    starts = []
    cursor = 0
    for b in spec:
        anchor = [norm(w) for w in b["anchor"]]
        idx = find_seq(anchor, cursor)
        if idx < 0:
            sys.stderr.write(f"!! anchor not found for {b['id']}: {b['anchor']}\n")
            return 1
        starts.append((idx, words[idx]["start_ms"]))
        cursor = idx + 1

    beats = []
    for n, b in enumerate(spec):
        start_ms = 0 if n == 0 else starts[n][1]
        end_ms = duration_ms if n == len(spec) - 1 else starts[n + 1][1]
        ai = starts[n][0]
        ctx = " ".join(w["word"] for w in words[ai:ai + 10])
        beats.append({
            "index": n + 1,
            "id": b["id"],
            "slug": b["slug"],
            "pattern": b["pattern"],
            "start_ms": start_ms,
            "end_ms": end_ms,
            "duration_ms": end_ms - start_ms,
            "duration_s": round((end_ms - start_ms) / 1000, 3),
            "start_s": round(start_ms / 1000, 3),
            "pip": b.get("pip"),
            "anchor_context": ctx,
        })

    (out / "beats.json").write_text(
        json.dumps({"total_ms": duration_ms, "beats": beats}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    print(f"total duration: {duration_ms/1000:.3f}s  ({len(beats)} beats)\n")
    for b in beats:
        print(f"{b['index']}. {b['id']:24s} {b['start_s']:7.3f}s  dur={b['duration_s']:6.3f}s  | {b['anchor_context']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
