#!/usr/bin/env python3
"""Enrich scenes-outline.json → scenes.json with full per-scene metadata
(content, badges, pip_events, brollEnd, hasBreath) and copy/symlink SFX.

Usage:
    python3 scaffold_project.py --workspace <folder>
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path


# Try to find a bundled SFX folder; fall back to none if missing.
# Priority: skill-bundled assets (self-contained), then legacy workspace paths.
_SKILL_DIR = Path(__file__).resolve().parent.parent
SFX_CANDIDATE_DIRS = [
    _SKILL_DIR / 'assets' / 'sfx',
    Path.home() / 'Documents' / 'GitHub' / 'claudeclaw-os' / 'workspace' / 'assets' / 'reels' / 'sfx',
    Path.home() / 'Documents' / 'GitHub' / 'hoang-ai-marketing' / 'workspace' / 'assets' / 'reels' / 'sfx',
]

SFX_FILES = [
    'camera-flash.mp3',
    'Whoosh sound effect (1).mp3',
    'búng tay.mp3',
    'Laser.mp3',
    'ting.mp3',
    'Discord Notification - Sound Effect.mp3',
]

# Brand logos + avatar candidate locations. Logos enable per-row brand
# attribution in compositions (chats-stack fail rows, hero-orb, tier-row tool-badge).
# Avatar.jpg is used by yt-lower-third subscribe banner.
LOGO_CANDIDATE_DIRS = [
    _SKILL_DIR / 'assets' / 'logos',
    Path.home() / 'Documents' / 'GitHub' / 'claudeclaw-os' / 'workspace' / 'assets' / 'logos',
    Path.home() / 'Documents' / 'GitHub' / 'hoang-ai-marketing' / 'workspace' / 'assets' / 'logos',
]
LOGO_FILE_MAP = {
    # source-name (with spaces accepted) → workspace target name (no spaces)
    'chatgpt logo.png': 'chatgpt.png',
    'chatgpt.png':       'chatgpt.png',
    'gemini logo.jpg':  'gemini.jpg',
    'gemini.jpg':        'gemini.jpg',
    'claude logo.png':  'claude.png',
    'claude.png':        'claude.png',
    'claude code logo big.png': 'claude-code.png',
    'claude-code.png':           'claude-code.png',
}

AVATAR_CANDIDATE_PATHS = [
    # Prefer skill-bundled (self-contained, real Hoang avatar 1280×1280).
    _SKILL_DIR / 'assets' / 'avatar.jpg',
    # Then look in workspace/assets/brand/ which is where the canonical
    # Hoang avatar lives in the claudeclaw-os repo.
    Path.home() / 'Documents' / 'GitHub' / 'claudeclaw-os' / 'workspace' / 'assets' / 'brand' / 'tony-avatar.jpg',
    Path.home() / 'Documents' / 'GitHub' / 'claudeclaw-os' / 'workspace' / 'assets' / 'brand' / 'Hoang profile.jpg',
    Path.home() / 'Documents' / 'GitHub' / 'hoang-ai-marketing' / 'workspace' / 'assets' / 'brand' / 'tony-avatar.jpg',
    # Last resort: small placeholder.
    Path.home() / 'Documents' / 'GitHub' / 'claudeclaw-os' / 'assets' / 'avatar.jpg',
]


def find_sfx_source() -> Path | None:
    for c in SFX_CANDIDATE_DIRS:
        if c.exists() and (c / 'camera-flash.mp3').exists():
            return c
    return None


def copy_sfx(workspace: Path):
    src = find_sfx_source()
    dst = workspace / 'sfx'
    dst.mkdir(exist_ok=True)
    if src is None:
        print(f'[scaffold] WARN: SFX source not found; skipping copy. Place files manually in {dst}', file=sys.stderr)
        return
    for fn in SFX_FILES:
        s = src / fn
        d = dst / fn
        if not d.exists() and s.exists():
            shutil.copy2(s, d)
    print(f'[scaffold] sfx ← {src}')


def find_logos_source() -> Path | None:
    """First candidate dir that contains at least one recognized logo file."""
    for c in LOGO_CANDIDATE_DIRS:
        if not c.exists():
            continue
        for src_name in LOGO_FILE_MAP:
            if (c / src_name).exists():
                return c
    return None


def copy_logos(workspace: Path):
    """Copy brand logos into workspace/assets/logos/. Renames source files
    that contain spaces to clean kebab-case (chatgpt.png, gemini.jpg, …).
    Skip silently if no source dir has any logo (compositions fall back to
    text avatars in that case)."""
    src = find_logos_source()
    dst = workspace / 'assets' / 'logos'
    if src is None:
        return  # No logos available — compositions will use text-avatar fallback.
    dst.mkdir(parents=True, exist_ok=True)
    copied = 0
    for src_name, target_name in LOGO_FILE_MAP.items():
        s = src / src_name
        d = dst / target_name
        if s.exists() and not d.exists():
            shutil.copy2(s, d)
            copied += 1
    if copied:
        print(f'[scaffold] logos ← {src} ({copied} copied)')


def copy_avatar(workspace: Path):
    """Copy avatar.jpg (used by yt-lower-third subscribe banner) into
    workspace/assets/avatar.jpg if a source is available."""
    dst = workspace / 'assets' / 'avatar.jpg'
    if dst.exists():
        return
    for src in AVATAR_CANDIDATE_PATHS:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f'[scaffold] avatar.jpg ← {src}')
            return


def copy_yt_lower_third(workspace: Path):
    """Copy yt-lower-third.html composition into workspace/compositions/.
    The root index.html.j2 will mount it at last 3s if present."""
    dst = workspace / 'compositions' / 'yt-lower-third.html'
    if dst.exists():
        return
    candidates = [
        _SKILL_DIR / 'assets' / 'compositions' / 'yt-lower-third.html',
        Path.home() / 'Documents' / 'GitHub' / 'claudeclaw-os' / 'compositions' / 'yt-lower-third.html',
    ]
    for src in candidates:
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f'[scaffold] yt-lower-third.html ← {src}')
            return


def derive_accent_words(heading: str, k: int = 3) -> list[str]:
    """Extract the most distinctive 2-3 phrases from heading.
    Heuristic: prefer numbers + uppercase words + final clause.
    """
    h = heading.strip()
    out = []
    nums = re.findall(r'\d+\s*[a-zA-ZÀ-ỹ%]*', h)
    out.extend(nums[:2])
    # Last clause after "—" or "→" if present
    for sep in ['—', '→', '·']:
        if sep in h:
            tail = h.split(sep)[-1].strip()
            if tail and tail not in out:
                out.append(tail.split()[0:3] and ' '.join(tail.split()[:3]))
                break
    # Fall back: last word if still empty
    if not out:
        words = h.split()
        out = [' '.join(words[-2:])] if words else ['—']
    return [w for w in out if w][:k]


def default_content_for_kind(kind: str, kicker: str, heading: str) -> dict:
    """Pattern-default content payload. Templates apply sensible defaults
    for any missing keys; this is a starting point user can edit."""
    if kind == 'hook':
        return {
            'before_letter': '?',
            'before_label': '⚡ TRƯỚC ĐÂY',
            'before_items': [
                {'icon': '✍️', 'label': 'Việc cũ 1'},
                {'icon': '📧', 'label': 'Việc cũ 2'},
                {'icon': '📚', 'label': 'Việc cũ 3'},
            ],
            'after_letter': '✓',
            'after_label': '✓ HÔM NAY',
            'after_items': [
                {'icon': '📝', 'label': 'Output 1'},
                {'icon': '📊', 'label': 'Output 2'},
                {'icon': '✓', 'label': 'Sẵn sàng'},
            ],
        }
    if kind == 'problem':
        return {
            'eyebrow_color': 'orange',
            'user_text': 'Câu hỏi/yêu cầu khó',
            'fail_rows': [
                {'name': 'CHATGPT', 'av': 'gpt', 'av_letter': 'G', 'text': 'Phản hồi không đạt — đứt mạch'},
                {'name': 'GEMINI',  'av': 'gem', 'av_letter': '✦', 'text': 'Cần thêm context — phải nhắc lại'},
            ],
            'broken_text': 'Đứt mạch · phải nhắc lại · mệt cái đầu',
        }
    if kind == 'solution':
        return {
            'eyebrow_color': 'violet',
            'orb_label': 'CLAUDE AI · giao việc → tự chạy',
            'task_items': [
                {'icon': '📝', 'label': 'Bản nháp'},
                {'icon': '📊', 'label': 'Báo cáo'},
                {'icon': '📧', 'label': 'Email'},
                {'icon': '📦', 'label': '100 trang'},
            ],
            'ingest_tag': '📦 Tài liệu dài → 🤖 ingest 1 lần',
            'specs': [
                {'letter': '∞',     'title': 'Nhớ cuộc trò chuyện dài', 'sub': 'không cần nhắc lại',  'icon': '🧠'},
                {'letter': '100tr', 'title': 'Đọc tài liệu một lần',     'sub': 'không cần chia nhỏ',  'icon': '📄'},
                {'letter': '8h',    'title': 'Tự bấm máy thay mình',     'sub': 'mình ngủ · sáng có output', 'icon': '🌙'},
            ],
        }
    if kind == 'recap':
        return {
            'eyebrow_color': 'lime',
            'big_letter': '15h',
            'counter_label': 'Giờ làm / tuần',
            'from_value': '40',
            'to_value': '25',
            'unit': 'tiếng',
            'clients': [
                {'av': 'N', 'title': 'Khách mới #1', 'sub': 'SIGNED · tháng sau'},
                {'av': 'T', 'title': 'Khách mới #2', 'sub': 'SIGNED · 0 hire thêm'},
            ],
            'delta_text': '−15h/tuần · +2 client · 0 hire',
        }
    if kind == 'cta':
        keyword = 'AI'
        return {
            'eyebrow_color': 'pink',
            'big_letter': keyword,
            'keyword': keyword,
            'avatar_letter': 'B',
            'gifts': [
                {'icon': '🤖', 'title': 'Cách dùng tool<br/>làm việc thay mình', 'tag': 'FREE'},
                {'icon': '⚡', 'title': 'Prompt + quy trình<br/>giao việc cụ thể', 'tag': 'FREE'},
            ],
            'cta_text': '👇 LƯU VIDEO · COMMENT ' + keyword + ' 👇',
        }
    return {}


def default_badges(kind: str) -> list[dict]:
    """1-2 floating-badge defaults per archetype."""
    if kind == 'hook':
        return [
            {'pos': 'tr', 'color': 'orange', 'icon': '⏰', 'num': '8h', 'label': 'Trước đây'},
            {'pos': 'bl', 'color': 'green',  'icon': '✅', 'num': '0h', 'label': 'Giờ cần làm'},
        ]
    if kind == 'problem':
        return [
            {'pos': 'tr', 'color': 'purple', 'icon': '🔄', 'num': '3x', 'label': 'Nhắc lại'},
            {'pos': 'bl', 'color': 'orange', 'icon': '😩', 'num': '+',  'label': 'Mệt đầu'},
        ]
    if kind == 'solution':
        return [
            {'pos': 'tr', 'color': 'cyan',   'icon': '📄', 'num': '100', 'label': 'Trang/lần'},
            {'pos': 'br', 'color': 'orange', 'icon': '✅', 'num': '3',   'label': 'Output loại'},
        ]
    if kind == 'recap':
        return [
            {'pos': 'tr', 'color': 'green',  'icon': '⏱️', 'num': '15h', 'label': 'Tiết kiệm/tuần'},
            {'pos': 'bl', 'color': 'orange', 'icon': '👥', 'num': '+2',  'label': 'Khách hàng mới'},
        ]
    if kind == 'cta':
        return [
            {'pos': 'tr', 'color': 'orange', 'icon': '💬', 'num': 'AI', 'label': 'Comment ngay'},
        ]
    return []


def derive_pip_events(scene: dict) -> list[dict]:
    """Default: 1 PIP window per scene around 1.5-4.5s after scene start
    (the tier-letter glow window). For long solution scenes, schedule 2.
    """
    start = scene['start']
    end = scene['end']
    duration = max(0.0, end - start)
    if duration < 3.0:
        return []
    # Single PIP for short scenes.
    if duration < 12.0:
        return [{'in': round(start + 1.4, 2), 'out': round(min(end - 0.3, start + 1.4 + min(3.5, duration - 1.5)), 2)}]
    # Two PIPs for longer (solution-style) scenes.
    return [
        {'in': round(start + 1.4, 2), 'out': round(start + 5.4, 2)},
        {'in': round(start + 7.0, 2), 'out': round(min(end - 0.3, start + 11.5), 2)},
    ]


def maybe_apply_visual_plan(workspace: Path) -> bool:
    """If visual-plan.json exists, delegate scenes.json generation to the
    planner skill's apply_plan_to_scenes.py (or an inline fallback).
    Returns True if the plan was applied (caller should skip default scaffold)."""
    plan_path = workspace / 'visual-plan.json'
    if not plan_path.exists():
        return False

    candidates = [
        Path.home() / 'Documents' / 'GitHub' / 'claudeclaw-os' / '.claude' / 'skills'
            / 'mkt-plan-short-video-edit-16-9' / 'scripts' / 'apply_plan_to_scenes.py',
        Path.home() / 'Documents' / 'GitHub' / 'hoang-ai-marketing' / '.claude' / 'skills'
            / 'mkt-plan-short-video-edit-16-9' / 'scripts' / 'apply_plan_to_scenes.py',
        Path.home() / '.claude' / 'skills' / 'mkt-plan-short-video-edit-16-9'
            / 'scripts' / 'apply_plan_to_scenes.py',
    ]
    apply_script = next((c for c in candidates if c.exists()), None)
    if apply_script is None:
        print('[scaffold] WARN: visual-plan.json present but planner apply_plan_to_scenes.py not found. '
              'Falling back to manual scaffold.', file=sys.stderr)
        return False

    import subprocess
    print(f'[scaffold] visual-plan.json detected — delegating to {apply_script.name}')
    subprocess.run(['python3', str(apply_script), '--workspace', str(workspace)], check=True)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', '-w', default='.', help='Workspace folder')
    ap.add_argument('--no-sfx', action='store_true', help='Skip SFX copy')
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()

    # If a visual-plan.json from mkt-plan-short-video-edit-16-9 exists,
    # use it instead of the manual outline → content fill flow.
    if maybe_apply_visual_plan(workspace):
        if not args.no_sfx:
            copy_sfx(workspace)
        copy_logos(workspace)
        copy_avatar(workspace)
        copy_yt_lower_third(workspace)
        return

    outline_path = workspace / 'scenes-outline.json'
    transcript_path = workspace / 'transcript-cleaned.json'
    if not transcript_path.exists():
        transcript_path = workspace / 'transcript.json'

    if not outline_path.exists():
        print(f'[scaffold] ERROR: {outline_path} not found. Run detect_scenes.py first.', file=sys.stderr)
        sys.exit(1)
    if not transcript_path.exists():
        print(f'[scaffold] ERROR: {transcript_path} not found.', file=sys.stderr)
        sys.exit(1)

    outline = json.loads(outline_path.read_text())
    words = json.loads(transcript_path.read_text())
    total_duration = float(words[-1]['end']) if words else outline[-1]['end']

    scenes = []
    for s in outline:
        kind = s['kind']
        enriched = {
            **s,
            'accent_words': derive_accent_words(s.get('heading', '')),
            'mockup_variant': s.get('variant', 'tier-row'),
            'brollEnd': round(s['end'] - 2.6, 2),
            'hasBreath': True,
            'content': default_content_for_kind(kind, s.get('kicker', ''), s.get('heading', '')),
            'badges': default_badges(kind),
            'pip_events': derive_pip_events(s),
        }
        scenes.append(enriched)

    out = {
        'total_duration': round(total_duration, 2),
        'scenes': scenes,
    }
    (workspace / 'scenes.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f'[scaffold] scenes.json — {len(scenes)} scenes, total {total_duration:.2f}s')

    if not args.no_sfx:
        copy_sfx(workspace)
    copy_logos(workspace)
    copy_avatar(workspace)
    copy_yt_lower_third(workspace)


if __name__ == '__main__':
    main()
