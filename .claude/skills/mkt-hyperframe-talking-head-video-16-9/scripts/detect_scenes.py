#!/usr/bin/env python3
"""Detect 5-scene knowledge-video skeleton from a Vietnamese transcript +
script.txt. Output is `scenes-outline.json` ready for user CHECKPOINT.

Standard archetype skeleton:
    1. hook      — first paragraph of script
    2. problem   — paragraph mentioning "khó", "đứt mạch", "ChatGPT/Gemini",
                   "vấn đề", "không nhớ", etc.
    3. solution  — paragraph introducing tool/method ("Claude theo kiểu khác",
                   "thử X", "khác biệt ở chỗ", etc.)
    4. recap     — paragraph with numerical result ("X tiếng/tuần",
                   "+N khách hàng", "tiết kiệm Y")
    5. cta       — last paragraph with comment/lưu/follow trigger

If the script doesn't have all 5, the script falls back gracefully (min 3
scenes). Variant mapping is fixed per archetype.

Usage:
    python3 detect_scenes.py --workspace <folder>
    python3 detect_scenes.py --workspace . --auto      # skip checkpoint print
"""
import argparse
import json
import re
import sys
from pathlib import Path


VARIANT_BY_KIND = {
    'hook':     'tier-row',
    'problem':  'chats-stack',
    'solution': 'hero-orb',
    'recap':    'counter-row',
    'cta':      'terminal-row',
}

PROBLEM_HINTS = [
    r'chatgpt', r'gemini', r'đứt mạch', r'không nhớ', r'nhắc lại từ đầu',
    r'mệt đầu', r'mệt tay', r'khó', r'đủ kiểu ai', r'phải canh', r'không xong',
    r'vẫn ngồi canh', r'đỡ mệt được tay',
]
SOLUTION_HINTS = [
    r'cho đến lúc', r'thử claude', r'theo kiểu khác', r'mà giao việc',
    r'cái khác biệt', r'khác biệt ở chỗ', r'không phải hỏi đáp',
    r'tự bấm máy', r'tự chạy', r'tự làm',
]
RECAP_HINTS = [
    r'\d+\s*tiếng', r'tiết kiệm', r'tháng sau', r'\d+ khách hàng',
    r'tổng kết', r'kết quả', r'không thuê',
]
CTA_HINTS = [
    r'\bcomment\b', r'\blưu\b', r'\btheo dõi\b', r'\bfollow\b',
    r'\bđăng ký\b', r'\blike\b', r'\bgửi bạn\b', r'mình gửi',
    r'thử để\b', r'lưu lại video',
]


def script_paragraphs(script_path: Path):
    """Split script.txt into clean paragraphs."""
    raw = script_path.read_text(encoding='utf-8')
    paras = [p.strip() for p in re.split(r'\n\s*\n', raw) if p.strip()]
    return paras


def find_paragraph_index(paras, hints):
    """Return index of first paragraph matching any hint, or None."""
    for i, p in enumerate(paras):
        low = p.lower()
        for h in hints:
            if re.search(h, low):
                return i
    return None


def find_word_time(words, needle):
    """Find the absolute start time of the first word matching `needle`
    (substring, lowercased). Used to anchor scene boundaries to the
    voiceover."""
    n = needle.lower()
    for w in words:
        if n in w.get('text', '').lower():
            return float(w['start'])
    return None


def first_word_of_paragraph(words, paragraph: str):
    """Locate paragraph anchor in word stream by finding the first
    distinctive 2-3 word phrase from paragraph in `words`. Returns absolute
    start time, or None.
    """
    tokens = re.findall(r'[\wÀ-ỹ]+', paragraph.lower())
    if not tokens:
        return None
    # Try the first 4-grams, then 3, then 2.
    for size in (4, 3, 2):
        if len(tokens) < size:
            continue
        target = ' '.join(tokens[:size])
        text_buf = []
        for i, w in enumerate(words):
            text_buf.append(w.get('text', '').lower())
            if len(text_buf) > size:
                text_buf.pop(0)
            if len(text_buf) == size and ' '.join(text_buf).find(target) != -1:
                return float(words[i - size + 1]['start'])
    return None


def derive_kicker(paragraph: str) -> str:
    """Pull a short kicker (4-6 words) from the paragraph head."""
    s = paragraph.strip()
    s = re.sub(r'^[^\wÀ-ỹ]+', '', s)
    words = re.findall(r"[\wÀ-ỹ%]+|[—–]", s)
    out = ' '.join(words[:5])
    return out[:42]


def derive_heading(paragraph: str) -> str:
    """Extract a punchy heading line from the paragraph."""
    s = paragraph.strip().split('\n', 1)[0]
    if len(s) > 70:
        # Try first sentence.
        m = re.split(r'(?<=[.!?])\s+', s, maxsplit=1)
        s = m[0]
    return s.strip().rstrip('.').strip()[:80]


def build_outline(paras, words, total_duration):
    """Map paragraphs → 5 scene archetypes; anchor times in words."""
    # Decide which paragraph maps to which archetype.
    n = len(paras)
    if n == 0:
        return []

    # Greedy: hook is paragraph 0; cta is last paragraph; problem/solution/
    # recap are picked by hint matching, falling back to evenly spaced.
    used = {0}
    plan = [{'kind': 'hook', 'para_idx': 0}]

    cta_idx = n - 1
    used.add(cta_idx)

    problem_idx = find_paragraph_index(paras, PROBLEM_HINTS)
    if problem_idx is None or problem_idx in used:
        problem_idx = 1 if n >= 3 else None
    if problem_idx is not None and problem_idx not in used:
        plan.append({'kind': 'problem', 'para_idx': problem_idx})
        used.add(problem_idx)

    solution_idx = find_paragraph_index(paras, SOLUTION_HINTS)
    if solution_idx is None or solution_idx in used:
        # fallback: middle-ish paragraph
        for i in range(2, n - 1):
            if i not in used:
                solution_idx = i
                break
    if solution_idx is not None and solution_idx not in used:
        plan.append({'kind': 'solution', 'para_idx': solution_idx})
        used.add(solution_idx)

    recap_idx = find_paragraph_index(paras, RECAP_HINTS)
    if recap_idx is None or recap_idx in used:
        for i in range(n - 2, 1, -1):
            if i not in used:
                recap_idx = i
                break
    if recap_idx is not None and recap_idx not in used:
        plan.append({'kind': 'recap', 'para_idx': recap_idx})
        used.add(recap_idx)

    # CTA last
    plan.append({'kind': 'cta', 'para_idx': cta_idx})

    # Sort by paragraph index → ensures temporal order.
    plan.sort(key=lambda x: x['para_idx'])

    # Anchor each plan entry to a word-time. If anchor missing, distribute
    # evenly across total_duration.
    anchored = []
    for entry in plan:
        para = paras[entry['para_idx']]
        t = first_word_of_paragraph(words, para)
        anchored.append((entry, t))

    # Fill missing anchors with evenly spaced fallbacks.
    k = len(anchored)
    for i, (entry, t) in enumerate(list(anchored)):
        if t is None:
            t = round(total_duration * (i / k), 2)
            anchored[i] = (entry, t)

    # Build scenes with start/end pairs.
    scenes = []
    for i, (entry, t) in enumerate(anchored):
        start = round(max(0.0, t), 2)
        if i + 1 < len(anchored):
            end = round(anchored[i + 1][1], 2)
        else:
            end = round(total_duration, 2)
        para = paras[entry['para_idx']]
        scenes.append({
            'num': i + 1,
            'kind': entry['kind'],
            'start': start,
            'end': end,
            'kicker': derive_kicker(para),
            'heading': derive_heading(para),
            'variant': VARIANT_BY_KIND.get(entry['kind'], 'tier-row'),
        })
    return scenes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', '-w', default='.', help='Workspace folder')
    ap.add_argument('--transcript', default=None, help='Override transcript path')
    ap.add_argument('--script', default=None, help='Override script.txt path')
    ap.add_argument('--auto', action='store_true', help='Skip checkpoint print')
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    transcript_path = Path(args.transcript) if args.transcript else \
        (workspace / 'transcript-cleaned.json' if (workspace / 'transcript-cleaned.json').exists()
         else workspace / 'transcript.json')
    script_path = Path(args.script) if args.script else workspace / 'script.txt'

    if not transcript_path.exists():
        print(f'[scenes] ERROR: {transcript_path} not found', file=sys.stderr)
        sys.exit(1)
    if not script_path.exists():
        print(f'[scenes] ERROR: {script_path} not found', file=sys.stderr)
        sys.exit(1)

    with transcript_path.open() as f:
        words = json.load(f)
    paras = script_paragraphs(script_path)
    total_duration = float(words[-1]['end']) if words else 60.0

    scenes = build_outline(paras, words, total_duration)
    out = workspace / 'scenes-outline.json'
    with out.open('w') as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)

    print(f'[scenes] wrote {out} ({len(scenes)} scenes, total {total_duration:.2f}s)')
    if not args.auto:
        for s in scenes:
            print(f'  #{s["num"]} {s["kind"]:8s} {s["start"]:6.2f}-{s["end"]:6.2f}s · {s["kicker"]} · {s["variant"]}')
        print('\n[CHECKPOINT] Review/edit scenes-outline.json above, then run scaffold_project.py')


if __name__ == '__main__':
    main()
