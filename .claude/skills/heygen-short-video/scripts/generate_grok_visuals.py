#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
Generate Grok visual videos via 79ai (gommo.net) API.

Usage:
  python generate_grok_visuals.py <production-plan.json> <output-dir> [--ratio 16:9] [--resolution 720p] [--duration 6] [--max-wait 300]

Reads visual segments from production-plan.json, generates videos via 79ai API,
polls for completion, downloads MP4s to output-dir as 1.mp4, 2.mp4, etc.

Environment variables (from .env):
  GOMMO_ACCESS_TOKEN  - 79ai API access token
  GOMMO_DOMAIN        - 79ai domain (default: 79ai.net)
"""

import argparse
import json
import os
import sys
import time
import requests
from pathlib import Path
from urllib.parse import quote

# Load .env from project root
project_root = Path(__file__).resolve().parents[4]  # .claude/skills/heygen-short-video/scripts -> root
env_path = project_root / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

API_BASE = "https://api.gommo.net/ai"
CREATE_URL = f"{API_BASE}/create-video"
STATUS_URL = f"{API_BASE}/video"


def create_video(prompt: str, access_token: str, domain: str,
                 ratio: str = "16:9", resolution: str = "720p",
                 duration: str = "6", mode: str = "fast") -> dict:
    """Submit a video generation request to 79ai API."""
    data = {
        "access_token": access_token,
        "domain": domain,
        "model": "grok_video_heavy",
        "privacy": "PRIVATE",
        "prompt": prompt,
        "translate_to_en": "true",
        "ratio": ratio,
        "resolution": resolution,
        "duration": str(duration),
        "mode": mode,
    }
    resp = requests.post(CREATE_URL, data=data, timeout=30)
    resp.raise_for_status()
    result = resp.json()
    if not result.get("success"):
        raise RuntimeError(f"79ai create-video failed: {result.get('message', 'Unknown error')}")
    return result


def get_video_status(video_id: str, access_token: str, domain: str) -> dict:
    """Poll video generation status by id_base."""
    data = {
        "access_token": access_token,
        "domain": domain,
        "videoId": video_id,
    }
    resp = requests.post(STATUS_URL, data=data, timeout=30)
    resp.raise_for_status()
    return resp.json()


def wait_for_video(video_id: str, access_token: str, domain: str,
                   max_wait: int = 300, poll_interval: int = 10) -> dict:
    """Poll until video is ready or timeout."""
    elapsed = 0
    while elapsed < max_wait:
        result = get_video_status(video_id, access_token, domain)
        video_info = result.get("videoInfo", {})
        status = video_info.get("status", "")

        if status == "MEDIA_GENERATION_STATUS_SUCCESSFUL":
            return video_info
        elif "FAILED" in status or "ERROR" in status:
            raise RuntimeError(f"Video generation failed: {status} - {video_info.get('message', '')}")

        print(f"  Status: {status} (elapsed: {elapsed}s)", flush=True)
        time.sleep(poll_interval)
        elapsed += poll_interval

    raise TimeoutError(f"Video {video_id} not ready after {max_wait}s")


def download_video(url: str, output_path: Path) -> None:
    """Download video file from URL."""
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def main():
    parser = argparse.ArgumentParser(description="Generate Grok visual videos via 79ai API")
    parser.add_argument("production_plan", help="Path to production-plan.json")
    parser.add_argument("output_dir", help="Output directory for MP4 files (e.g., grok_visuals/)")
    parser.add_argument("--ratio", default="16:9", help="Video ratio (default: 16:9)")
    parser.add_argument("--resolution", default="720p", help="Resolution (default: 720p)")
    parser.add_argument("--duration", default="6", help="Duration in seconds (default: 6)")
    parser.add_argument("--max-wait", type=int, default=300, help="Max wait per video in seconds (default: 300)")
    parser.add_argument("--mode", default="fast", help="Generation mode (default: fast)")
    args = parser.parse_args()

    access_token = os.environ.get("GOMMO_ACCESS_TOKEN")
    domain = os.environ.get("GOMMO_DOMAIN", "79ai.net")

    if not access_token:
        print("ERROR: GOMMO_ACCESS_TOKEN not set in environment or .env", file=sys.stderr)
        sys.exit(1)

    # Read production plan
    plan_path = Path(args.production_plan)
    with open(plan_path) as f:
        plan = json.load(f)

    segments = plan.get("segments", [])
    visual_segments = [s for s in segments if s.get("type") == "visual"]

    if not visual_segments:
        print("No visual segments found in production plan. Nothing to generate.")
        sys.exit(0)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(visual_segments)} visual segments to generate")
    print(f"Output: {output_dir}")
    print()

    # Phase 1: Submit all video generation requests
    jobs = []  # [(visual_index, id_base, prompt)]
    for i, seg in enumerate(visual_segments, 1):
        prompt = seg.get("grokPrompt", "")
        if not prompt:
            print(f"WARNING: Segment {seg.get('id', '?')} has no grokPrompt, skipping")
            continue

        print(f"[{i}/{len(visual_segments)}] Submitting: {prompt[:80]}...")
        try:
            result = create_video(
                prompt=prompt,
                access_token=access_token,
                domain=domain,
                ratio=args.ratio,
                resolution=args.resolution,
                duration=args.duration,
                mode=args.mode,
            )
            video_id = result.get("id_base", "")
            credits_used = result.get("videoInfo", {}).get("credit_fee", 0)
            credits_remaining = result.get("balancesInfo", {}).get("credits_ai", 0)
            print(f"  Submitted! id_base={video_id} (credits: -{credits_used}, remaining: {credits_remaining})")
            jobs.append((i, video_id, prompt))
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    if not jobs:
        print("No jobs submitted. Exiting.")
        sys.exit(1)

    print(f"\nAll {len(jobs)} jobs submitted. Polling for completion...\n")

    # Phase 2: Poll all jobs and download
    results = []
    for idx, video_id, prompt in jobs:
        output_path = output_dir / f"{idx}.mp4"
        print(f"[{idx}/{len(visual_segments)}] Waiting for {video_id}...")

        try:
            video_info = wait_for_video(video_id, access_token, domain, max_wait=args.max_wait)
            download_url = video_info.get("download_url", "")
            if not download_url:
                print(f"  ERROR: No download_url in response", file=sys.stderr)
                continue

            print(f"  Downloading: {download_url}")
            download_video(download_url, output_path)
            print(f"  Saved: {output_path}")

            results.append({
                "index": idx,
                "id_base": video_id,
                "prompt": prompt,
                "download_url": download_url,
                "output_path": str(output_path),
                "status": "success",
            })
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            results.append({
                "index": idx,
                "id_base": video_id,
                "prompt": prompt,
                "output_path": str(output_path),
                "status": f"failed: {e}",
            })

    # Write manifest
    manifest_path = output_dir / "grok_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump({"videos": results, "total": len(results)}, f, indent=2, ensure_ascii=False)
    print(f"\nManifest saved: {manifest_path}")

    # Summary
    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"\nDone! {success_count}/{len(jobs)} videos generated successfully.")

    if success_count < len(jobs):
        sys.exit(1)


if __name__ == "__main__":
    main()
