#!/usr/bin/env python3
"""Blotato multi-platform publisher CLI.

Subcommands:
  accounts                       List connected accounts + Facebook/LinkedIn pages
  upload <file-or-url>           Upload media to Blotato, print public URL
  publish --platform ... --media ... --text ...   Publish a post
  status <postSubmissionId>      Check (or --wait for) a post's status

Auth: BLOTATO_API_KEY env var, or BLOTATO_API_KEY= line in the project root .env
(walked up from this script's location).

stdlib only — no pip installs needed.
"""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://backend.blotato.com/v2"


def find_api_key() -> str:
    key = os.environ.get("BLOTATO_API_KEY", "").strip()
    if key:
        return key
    # Walk up from this script looking for a .env with BLOTATO_API_KEY
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(10):
        env_path = os.path.join(d, ".env")
        if os.path.isfile(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("BLOTATO_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if key:
                            return key
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    sys.exit("ERROR: BLOTATO_API_KEY not found in env or any parent .env")


def api(method: str, path: str, body=None, raw_data=None, headers=None, timeout=120):
    url = path if path.startswith("http") else BASE + path
    hdrs = {"blotato-api-key": find_api_key()}
    if headers:
        hdrs.update(headers)
    data = raw_data
    if body is not None:
        data = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", "replace")
            return json.loads(text) if text.strip() else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit(f"ERROR: HTTP {e.code} {method} {url}\n{detail}")


def cmd_accounts(_args):
    accounts = api("GET", "/users/me/accounts").get("items", [])
    out = []
    for acc in accounts:
        entry = dict(acc)
        if acc.get("platform") in ("facebook", "linkedin"):
            subs = api("GET", f"/users/me/accounts/{acc['id']}/subaccounts").get("items", [])
            entry["pages"] = subs
        out.append(entry)
    print(json.dumps(out, indent=2, ensure_ascii=False))


def upload_media(path_or_url: str) -> str:
    if path_or_url.startswith("http"):
        res = api("POST", "/media", body={"url": path_or_url})
        return res["url"]
    path = os.path.abspath(path_or_url)
    if not os.path.isfile(path):
        sys.exit(f"ERROR: file not found: {path}")
    filename = os.path.basename(path)
    res = api("POST", "/media/uploads", body={"filename": filename})
    presigned, public = res["presignedUrl"], res["publicUrl"]
    ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(presigned, data=data, method="PUT",
                                 headers={"Content-Type": ctype})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: presigned PUT failed HTTP {e.code}\n{e.read().decode('utf-8', 'replace')}")
    return public


def cmd_upload(args):
    print(upload_media(args.file))


def build_target(args) -> dict:
    p = args.platform
    if p == "facebook":
        if not args.page_id:
            sys.exit("ERROR: facebook requires --page-id (run `accounts` to list pages)")
        target = {"targetType": "facebook", "pageId": args.page_id}
        if args.fb_media_type:
            target["mediaType"] = args.fb_media_type
        return target
    if p == "tiktok":
        target = {
            "targetType": "tiktok",
            "privacyLevel": args.tiktok_privacy,
            "disabledComments": False,
            "disabledDuet": False,
            "disabledStitch": False,
            "isBrandedContent": False,
            "isYourBrand": False,
            "isAiGenerated": not args.no_ai_label,
        }
        if args.title:
            target["title"] = args.title[:90]
        return target
    if p == "instagram":
        return {"targetType": "instagram"}
    if p == "youtube":
        if not args.title:
            sys.exit("ERROR: youtube requires --title (the video title, max 100 chars)")
        return {
            "targetType": "youtube",
            "title": args.title[:100],
            "privacyStatus": getattr(args, "youtube_privacy", None) or "public",
            "shouldNotifySubscribers": True,
            "isMadeForKids": bool(getattr(args, "made_for_kids", False)),
        }
    # generic fallback: platforms whose target needs only targetType
    return {"targetType": p}


def cmd_publish(args):
    media_urls = []
    for m in args.media or []:
        # already-hosted blotato media URL (docs say .com, API returns .io)
        if "database.blotato." in m:
            media_urls.append(m)
        else:
            media_urls.append(upload_media(m))
    body = {
        "post": {
            "accountId": str(args.account_id),
            "target": build_target(args),
            "content": {
                "text": args.text or "",
                "platform": args.platform,
                "mediaUrls": media_urls,
            },
        }
    }
    if args.scheduled_time:
        body["scheduledTime"] = args.scheduled_time
    res = api("POST", "/posts", body=body)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    sub_id = res.get("postSubmissionId") or (res.get("post") or {}).get("postSubmissionId")
    if args.wait and sub_id:
        wait_for(sub_id, args.wait)


def wait_for(sub_id: str, timeout_s: int):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        res = api("GET", f"/posts/{sub_id}")
        status = res.get("status")
        if status in ("published", "failed"):
            print(json.dumps(res, indent=2, ensure_ascii=False))
            sys.exit(0 if status == "published" else 2)
        time.sleep(10)
    sys.exit(f"TIMEOUT: post {sub_id} still in-progress after {timeout_s}s")


def cmd_status(args):
    if args.wait:
        wait_for(args.id, args.wait)
    print(json.dumps(api("GET", f"/posts/{args.id}"), indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("accounts")

    up = sub.add_parser("upload")
    up.add_argument("file", help="local file path or http(s) URL")

    pb = sub.add_parser("publish")
    pb.add_argument("--platform", required=True,
                    choices=["facebook", "tiktok", "instagram", "youtube", "threads",
                             "twitter", "linkedin", "pinterest", "bluesky"])
    pb.add_argument("--account-id", required=True)
    pb.add_argument("--text", default="")
    pb.add_argument("--media", action="append",
                    help="local file, external URL, or blotato publicUrl; repeatable")
    pb.add_argument("--page-id", help="facebook page id (subaccount id)")
    pb.add_argument("--fb-media-type", choices=["reel", "story"],
                    help="facebook only; omit for normal feed post")
    pb.add_argument("--title", help="tiktok title (max 90) / youtube title (max 100)")
    pb.add_argument("--youtube-privacy", default="public",
                    choices=["public", "unlisted", "private"],
                    help="youtube only; default public")
    pb.add_argument("--made-for-kids", action="store_true",
                    help="youtube only; mark video as made for kids (default: NOT for kids)")
    pb.add_argument("--tiktok-privacy", default="PUBLIC_TO_EVERYONE",
                    choices=["PUBLIC_TO_EVERYONE", "SELF_ONLY",
                             "MUTUAL_FOLLOW_FRIENDS", "FOLLOWER_OF_CREATOR"])
    pb.add_argument("--no-ai-label", action="store_true",
                    help="tiktok: drop the AI-generated content label (default: labeled)")
    pb.add_argument("--scheduled-time", help="ISO 8601, e.g. 2026-06-11T09:00:00Z")
    pb.add_argument("--wait", type=int, nargs="?", const=300, default=0,
                    help="poll until published/failed (seconds, default 300)")

    st = sub.add_parser("status")
    st.add_argument("id")
    st.add_argument("--wait", type=int, nargs="?", const=300, default=0)

    args = ap.parse_args()
    {"accounts": cmd_accounts, "upload": cmd_upload,
     "publish": cmd_publish, "status": cmd_status}[args.cmd](args)


if __name__ == "__main__":
    main()
