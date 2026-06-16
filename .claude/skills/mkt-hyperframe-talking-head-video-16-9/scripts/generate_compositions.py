#!/usr/bin/env python3
"""Render compositions/<id>.html × N from scenes.json + Jinja2 templates.

Mapping:
    scene.kind     → composition id            → template
    -------------    -----------------------     -----------------------------
    hook           → fs-lesson-1                composition-tier-row.html.j2
    problem        → fs-lesson-2                composition-chats-stack.html.j2
    solution       → fs-lesson-3                composition-hero-orb.html.j2
    recap          → recap-card                 composition-counter-row.html.j2
    cta            → fs-cta                     composition-terminal-row.html.j2

If `--with-infographics` is set, an `infographic-slot.html.j2` partial is
rendered and substituted into each composition's `infographic_slot` slot.

Usage:
    python3 generate_compositions.py --workspace <folder> [--with-infographics]
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print('[gen] jinja2 missing — pip install jinja2', file=sys.stderr)
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR.parent / 'assets' / 'templates'

KIND_TO = {
    'hook':     {'id': 'fs-lesson-1', 'template': 'composition-tier-row.html.j2'},
    'problem':  {'id': 'fs-lesson-2', 'template': 'composition-chats-stack.html.j2'},
    'solution': {'id': 'fs-lesson-3', 'template': 'composition-hero-orb.html.j2'},
    'recap':    {'id': 'recap-card',  'template': 'composition-counter-row.html.j2'},
    'cta':      {'id': 'fs-cta',      'template': 'composition-terminal-row.html.j2'},
}

# Variant → archetype fallback for legacy scenes.json that use kind="lesson".
VARIANT_TO_KIND = {
    'tier-row':     'hook',
    'post-stack':   'hook',
    'chats-stack':  'problem',
    'ai-window':    'problem',
    'hero-orb':     'solution',
    'app-card':     'solution',
    'counter-row':  'recap',
    'team-grid':    'recap',
    'terminal-row': 'cta',
    'comment-box':  'cta',
}


def resolve_kind(scene: dict) -> str:
    """Resolve scene archetype. Prefer explicit `kind`; fall back to
    `variant`/`mockup_variant` if kind is generic ('lesson'). Final
    fallback is positional from `num`."""
    kind = scene.get('kind', '')
    if kind in KIND_TO:
        return kind
    variant = scene.get('variant') or scene.get('mockup_variant') or ''
    if variant in VARIANT_TO_KIND:
        return VARIANT_TO_KIND[variant]
    # Positional fallback for kind="lesson" (1→hook, 2→problem, 3→solution).
    num = scene.get('num', 0)
    positional = {1: 'hook', 2: 'problem', 3: 'solution', 4: 'recap', 5: 'cta'}
    return positional.get(num, 'hook')

EYEBROW_BY_KIND = {
    'hook':     '#67e8f9',
    'problem':  '#fb923c',
    'solution': '#a78bfa',
    'recap':    '#a3e635',
    'cta':      '#f0abfc',
}

# Brand logo paths (relative to workspace). Each logo expected at this path
# after scaffold_project.py copies them. Compositions will use these as
# fallback if scenes.json doesn't override per-row.
BRAND_LOGO_PATHS = {
    'chatgpt':     'assets/logos/chatgpt.png',
    'gemini':      'assets/logos/gemini.jpg',
    'claude':      'assets/logos/claude.png',
    'claude-code': 'assets/logos/claude-code.png',
}

# Auto-attach logo to fail-row by name match. Lowercase name keyword → logo key.
FAIL_ROW_AUTO_LOGO = {
    'chatgpt': 'chatgpt',
    'gpt':     'chatgpt',
    'gemini':  'gemini',
    'google':  'gemini',
}


def auto_attach_logos_to_fail_rows(rows: list[dict], logos_dir_exists: bool) -> list[dict]:
    """If scenes.json fail_rows entries don't carry `logo`, infer from `name`.
    Skips when logos directory missing — keeps text avatar fallback."""
    if not logos_dir_exists:
        return rows
    out = []
    for r in rows:
        if r.get('logo'):
            out.append(r)
            continue
        name_lc = (r.get('name') or '').lower()
        match = next((logo_key for kw, logo_key in FAIL_ROW_AUTO_LOGO.items() if kw in name_lc), None)
        if match:
            r2 = {**r, 'logo': BRAND_LOGO_PATHS[match]}
            out.append(r2)
        else:
            out.append(r)
    return out


def heading_to_words(heading: str, accent_words: list[str]) -> list[dict]:
    """Tokenize heading into per-word spans. Mark words that appear in
    accent_words as `grad=True` so they render with the gradient class.
    """
    words = re.findall(r'\S+', heading)
    accent_set = set()
    for aw in accent_words:
        for token in re.findall(r'\S+', aw):
            accent_set.add(token.lower().strip(',.;:'))
    out = []
    for w in words:
        clean = w.strip(',.;:').lower()
        out.append({'text': w, 'grad': clean in accent_set})
    return out


def render_scene(env, scene: dict, with_infographic: bool, logos_dir_exists: bool = False, brand_default: str = 'claude'):
    kind = resolve_kind(scene)
    tmap = KIND_TO[kind]
    tpl = env.get_template(tmap['template'])

    common = {
        'id': tmap['id'],
        'kicker': scene.get('kicker', ''),
        'heading_words': heading_to_words(scene.get('heading', ''), scene.get('accent_words', [])),
        'eyebrow_color': EYEBROW_BY_KIND.get(kind, '#67e8f9'),
        'duration': scene['end'] - scene['start'],
    }
    content = scene.get('content', {}) or {}
    brand_logo = BRAND_LOGO_PATHS.get(brand_default) if logos_dir_exists else None

    if kind == 'hook':
        # Auto-add CLAUDE tool-badge to "after" row if logos exist and content
        # doesn't already specify after_tool_badge.
        after_tool_badge = content.get('after_tool_badge')
        if not after_tool_badge and brand_logo:
            after_tool_badge = {'logo': brand_logo, 'name': brand_default.upper()}
        common.update({
            'grad_pair': ['#a3e635', '#67e8f9'],
            'before_letter': content.get('before_letter', '?'),
            'before_label':  content.get('before_label', '⚡ TRƯỚC ĐÂY'),
            'before_items':  content.get('before_items', []),
            'after_letter':  content.get('after_letter', '✓'),
            'after_label':   content.get('after_label', '✓ HÔM NAY'),
            'after_items':   content.get('after_items', []),
            'after_tool_badge': after_tool_badge,
        })
    elif kind == 'problem':
        # Auto-attach logos (chatgpt, gemini) to fail_rows by name match.
        fail_rows = auto_attach_logos_to_fail_rows(
            content.get('fail_rows', []), logos_dir_exists
        )
        common.update({
            'user_text': content.get('user_text', ''),
            'fail_rows': fail_rows,
            'broken_text': content.get('broken_text', 'Đứt mạch'),
        })
    elif kind == 'solution':
        # Auto-add brand logo inside the orb if logos exist.
        orb_logo = content.get('orb_logo')
        if not orb_logo and brand_logo:
            orb_logo = brand_logo
        common.update({
            'orb_label':   content.get('orb_label', ''),
            'task_items':  content.get('task_items', []),
            'ingest_tag':  content.get('ingest_tag', ''),
            'specs':       content.get('specs', []),
            'orb_logo':    orb_logo,
        })
    elif kind == 'recap':
        common.update({
            'big_letter':    content.get('big_letter', ''),
            'counter_label': content.get('counter_label', ''),
            'from_value':    content.get('from_value', ''),
            'to_value':      content.get('to_value', ''),
            'unit':          content.get('unit', ''),
            'clients':       content.get('clients', []),
            'delta_text':    content.get('delta_text', ''),
        })
    elif kind == 'cta':
        common.update({
            'big_letter': content.get('big_letter', 'AI'),
            'keyword':    content.get('keyword', 'AI'),
            'gifts':      content.get('gifts', []),
            'cta_text':   content.get('cta_text', ''),
        })

    if with_infographic:
        slot_tpl = env.get_template('infographic-slot.html.j2')
        common['infographic_slot'] = slot_tpl.render(scene_num=scene['num'])
    else:
        common['infographic_slot'] = ''

    return tmap['id'], tpl.render(**common)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', '-w', default='.', help='Workspace folder')
    ap.add_argument('--with-infographics', action='store_true',
                    help='Inject <img> infographic slots into each composition')
    ap.add_argument('--brand-default', default='claude',
                    choices=['claude', 'chatgpt', 'gemini', 'claude-code'],
                    help='Brand whose logo auto-fills hero-orb + tier-row (default: claude)')
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    scenes_path = workspace / 'scenes.json'
    if not scenes_path.exists():
        print(f'[gen] ERROR: {scenes_path} not found. Run scaffold_project.py first.', file=sys.stderr)
        sys.exit(1)

    data = json.loads(scenes_path.read_text())
    scenes = data['scenes']

    # Detect whether logos directory exists in workspace. If present, auto-fill
    # brand logos in compositions; if absent, fall back to text avatars.
    logos_dir = workspace / 'assets' / 'logos'
    logos_dir_exists = logos_dir.exists() and any(logos_dir.iterdir())

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
        trim_blocks=False,
        lstrip_blocks=False,
    )

    out_dir = workspace / 'compositions'
    out_dir.mkdir(exist_ok=True)

    for scene in scenes:
        comp_id, html = render_scene(env, scene, args.with_infographics,
                                     logos_dir_exists=logos_dir_exists,
                                     brand_default=args.brand_default)
        path = out_dir / f'{comp_id}.html'
        path.write_text(html)
        print(f'[gen] {path}  ({scene["kind"]} → {comp_id})')

    logo_msg = f' · brand logos: {args.brand_default}' if logos_dir_exists else ' · no logos dir (text avatars)'
    print(f'[gen] {len(scenes)} compositions written to {out_dir}{logo_msg}')


if __name__ == '__main__':
    main()
