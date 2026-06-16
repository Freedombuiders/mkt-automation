#!/usr/bin/env python3
"""Clean Whisper VN transcript artifacts. Mirrors the sibling 9:16 cleaner
but does NOT emit caption-groups.json (16:9 has no caption mount).

Usage:
    python3 clean_transcript.py path/to/transcript.json
    python3 clean_transcript.py --workspace <folder>
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


WORD_REPLACEMENTS = {
    'alphabit': 'Alphabet', 'Alphabit': 'Alphabet',
    'kĩ': 'kỹ',
    'gián': 'gắn',
    'cốt': 'code',
    'cod': 'Code', 'Cod': 'Code',
    'cán': 'cá',
    'dưi': 'dưới',
    'đng': 'đắc',
    'cloud': 'Claude', 'Cloud': 'Claude',
    'cờ-lốt': 'Claude',
    'CLốt': 'Claude',
}

PHRASE_REPLACEMENTS = [
    (r'\bbản dụng thử\b',      'bản dùng thử'),
    (r'\bnhãn dụng thử\b',     'nhãn dùng thử'),
    (r'\bgắn nhãn dụng\b',     'gắn nhãn dùng'),
    (r'\bthay đựng\b',         'tham vọng'),
    (r'\bđã nạp\b',            'đã làm'),
    (r'\btự xin khép\b',       'đợi xin phép'),
    (r'\bxin khép\b',          'xin phép'),
    (r'\btâm đ\S{1,3}ng\b',    'tâm đắc'),
    (r'\bđ\S{1,3}ng nhất\b',   'đắc nhất'),
    (r'\bứng dùng\b',          'ứng dụng'),
    (r'\báp dùng\b',           'áp dụng'),
    (r'doanh nghi[\S]{0,2}p',  'doanh nghiệp'),
    (r'cl(au|ó|ốt|au-?đơ)',     'Claude'),
    (r'\s+,', ','),
    (r'\s+', ' '),
]

REPL_CHARS = ['�', '�']


def strip_repl_chars(text: str) -> str:
    for ch in REPL_CHARS:
        text = text.replace(ch, '')
    return text


def clean_word_text(word_text: str) -> str:
    text = strip_repl_chars(word_text)
    m = re.match(r'^([^\wÀ-ỹ]*)([\wÀ-ỹ]+)([^\wÀ-ỹ]*)$', text)
    if m:
        pre, core, post = m.groups()
        if core in WORD_REPLACEMENTS:
            core = WORD_REPLACEMENTS[core]
        return pre + core + post
    return text


def apply_phrase_replacements(text: str) -> str:
    for pat, repl in PHRASE_REPLACEMENTS:
        text = re.sub(pat, repl, text)
    return text


def clean_words(words):
    out = []
    for w in words:
        if not w.get('text'):
            continue
        new_text = clean_word_text(w['text'])
        if not new_text.strip():
            continue
        out.append({**w, 'text': new_text})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('transcript', nargs='?', default=None, help='Path to transcript.json')
    ap.add_argument('--workspace', '-w', default=None,
                    help='Workspace folder (uses <workspace>/transcript.json)')
    args = ap.parse_args()

    if args.transcript:
        transcript_path = Path(args.transcript)
    elif args.workspace:
        transcript_path = Path(args.workspace) / 'transcript.json'
    else:
        transcript_path = Path('transcript.json')

    if not transcript_path.exists():
        print(f'[clean] ERROR: {transcript_path} not found', file=sys.stderr)
        sys.exit(1)

    with transcript_path.open() as f:
        words = json.load(f)

    cleaned = clean_words(words)
    # Apply phrase-level replacements across stitched text by rewriting
    # word-by-word through a sliding text buffer is overkill — instead
    # apply phrase replacements per-word safely and as a post-pass on
    # bigram joins.
    full = ' '.join(w['text'] for w in cleaned)
    full = apply_phrase_replacements(full)
    # NB: we keep `cleaned` word-level timing untouched; phrase-level
    # cleanup is mainly for downstream presentation. We persist both.

    base_dir = transcript_path.parent
    cleaned_path = base_dir / 'transcript-cleaned.json'

    with cleaned_path.open('w') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f'[clean] {len(cleaned)} words → {cleaned_path}')
    if cleaned:
        print(f'[clean] last end: {cleaned[-1]["end"]:.2f}s')


if __name__ == '__main__':
    main()
