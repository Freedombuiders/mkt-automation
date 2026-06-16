#!/usr/bin/env python3
"""Scaffold optional cream-paper editorial infographic <img> slots into
each composition + write infographics/prompts.md the user (or `mkt-broll-image`)
can run later.

Behavior:
- For each scene in scenes.json, derive a metaphor prompt from heading+kicker
- Write `infographics/prompts.md` (cream-paper editorial style)
- Inject `<img>` slot near the bottom of each composition with onerror fallback

Usage:
    python3 scaffold_infographic_slots.py --workspace <folder>
    python3 scaffold_infographic_slots.py --workspace <folder> --inject-only
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print('[infographics] jinja2 missing — pip install jinja2', file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR.parent / 'assets' / 'templates'

ACCENT_BY_KIND = {
    'hook':     'cyan',
    'problem':  'orange',
    'solution': 'violet',
    'recap':    'lime',
    'cta':      'pink',
}

METAPHOR_BY_KIND = {
    'hook':     'A small notebook with a clock face split in half — "8h" on the left page, "0h" on the right; arrow flowing from work-pile to a finished stack.',
    'problem':  'Three speech bubbles disconnected by a broken chain link in the middle; lines fade out, indicating lost context.',
    'solution': 'A glowing orb at the center with three orbits of small icons (document, mail, report) spinning around — labeled like a workflow diagram.',
    'recap':    'A simple bar chart annotated by hand — left bar tall (40), right bar shorter (25), with a curved arrow + delta label.',
    'cta':      'A speech bubble drawn over a phone outline with a single hand-lettered word inside; "AI" written in chunky brush stroke.',
}


def derive_prompts(scenes: list[dict]) -> list[dict]:
    out = []
    for s in scenes:
        kind = s['kind']
        out.append({
            'num': s['num'],
            'kind': kind,
            'variant': s.get('mockup_variant') or s.get('variant'),
            'heading': s.get('heading', ''),
            'kicker':  s.get('kicker', ''),
            'metaphor_prompt': METAPHOR_BY_KIND.get(kind, 'Hand-drawn editorial illustration that represents the heading.'),
            'accent_color': ACCENT_BY_KIND.get(kind, 'cyan'),
        })
    return out


def write_prompts_md(env: Environment, workspace: Path, scenes: list[dict]):
    info_dir = workspace / 'infographics'
    info_dir.mkdir(exist_ok=True)
    tpl = env.get_template('prompts.md.j2')
    enriched = derive_prompts(scenes)
    md = tpl.render(slug=workspace.name, scenes=enriched)
    (info_dir / 'prompts.md').write_text(md)
    print(f'[infographics] wrote {info_dir / "prompts.md"} ({len(enriched)} prompts)')


SLOT_RE = re.compile(r'<img class="infographic-slot"[^>]*?>\s*', re.DOTALL)


def inject_into_composition(comp_path: Path, scene_num: int, env: Environment):
    if not comp_path.exists():
        print(f'[infographics] WARN: {comp_path} missing — skip', file=sys.stderr)
        return
    html = comp_path.read_text()
    # Avoid double-injection.
    html = SLOT_RE.sub('', html)

    slot_tpl = env.get_template('infographic-slot.html.j2')
    slot_html = slot_tpl.render(scene_num=scene_num).rstrip() + '\n'

    # Insert the slot just before the closing </template> tag (or </div>
    # if missing).
    if '</template>' in html:
        html = html.replace('</template>', slot_html + '  </template>', 1)
    elif '</div>' in html.rsplit('</div>', 2)[0]:
        # Insert before the last </div>
        i = html.rfind('</div>')
        html = html[:i] + slot_html + html[i:]
    else:
        html += '\n' + slot_html

    comp_path.write_text(html)
    print(f'[infographics] injected slot into {comp_path}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', '-w', default='.', help='Workspace folder')
    ap.add_argument('--inject-only', action='store_true', help='Skip writing prompts.md, only inject slots')
    ap.add_argument('--prompts-only', action='store_true', help='Only write prompts.md, skip injection')
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    scenes_path = workspace / 'scenes.json'
    if not scenes_path.exists():
        print(f'[infographics] ERROR: {scenes_path} not found', file=sys.stderr)
        sys.exit(1)

    data = json.loads(scenes_path.read_text())
    scenes = data['scenes']

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)

    if not args.inject_only:
        write_prompts_md(env, workspace, scenes)

    if not args.prompts_only:
        KIND_ID = {
            'hook': 'fs-lesson-1', 'problem': 'fs-lesson-2', 'solution': 'fs-lesson-3',
            'recap': 'recap-card', 'cta': 'fs-cta',
        }
        for s in scenes:
            comp_id = KIND_ID.get(s['kind'], f"scene-{s['num']}")
            inject_into_composition(workspace / 'compositions' / f'{comp_id}.html', s['num'], env)


if __name__ == '__main__':
    main()
