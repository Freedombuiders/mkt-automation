#!/usr/bin/env python3
"""Render root index.html (1920×1080) from scenes.json + index.html.j2.

Wires up:
- video + audio source.mp4 (lip-synced TTS) at track 0/1
- 6 SFX (camera-flash hook, whoosh L1, snap L2, laser L3, ting recap, discord CTA)
- brand mark
- N slide-mount clips referencing compositions/<id>.html
- GSAP timeline with SPLIT↔PIP transitions
- "Hybrid Hook" zoom strategy on .avatar-breathing layer:
    HOOK ramp (1.0→1.10) → reset → BODY beats (1.06 punches) → CTA gentle (1.04)
- Cream-paper b-roll image PIP-swap layer (per-scene <img> fades during PIP windows)
- Optional yt-lower-third subscribe banner at last 3s

Usage:
    python3 generate_root_index.py --workspace <folder> \
        [--title "..." --brand-handle "tranvanhoang.com" --brand-label "Claude AI workflow"] \
        [--no-yt-lower-third]  # disable subscribe banner
        [--yt-lower-third-duration 4.5]  # custom duration
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print('[root] jinja2 missing — pip install jinja2', file=sys.stderr)
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR.parent / 'assets' / 'templates'

# SFX wiring schema. Each entry maps to a scene boundary or an absolute
# offset; if the scene index doesn't exist (shorter than 5 scenes) the
# entry is skipped.
# SFX semantic mapping. Hook fires at video start (camera-flash). One SFX
# per scene transition INTO scenes 2..5 (whoosh / snap / laser / ting /
# discord). If a scene N is missing in scenes.json the entry is skipped.
SFX_PLAN = [
    {'id': 'sfx-hook',  'offset_kind': 'absolute', 'time': 0.0,   'src': 'sfx/camera-flash.mp3',                       'duration': 0.6, 'volume': 0.32, 'track_index': 20},
    {'id': 'sfx-l1',    'offset_kind': 'scene',    'scene': 2,    'src': 'sfx/Whoosh sound effect (1).mp3',            'duration': 0.5, 'volume': 0.18, 'track_index': 21, 'lead': 0.0},
    {'id': 'sfx-l2',    'offset_kind': 'scene',    'scene': 3,    'src': 'sfx/búng tay.mp3',                           'duration': 0.5, 'volume': 0.18, 'track_index': 22, 'lead': 0.0},
    {'id': 'sfx-l3',    'offset_kind': 'scene',    'scene': 4,    'src': 'sfx/Laser.mp3',                              'duration': 0.5, 'volume': 0.18, 'track_index': 23, 'lead': 0.0},
    {'id': 'sfx-recap', 'offset_kind': 'scene',    'scene': 4,    'src': 'sfx/ting.mp3',                               'duration': 0.5, 'volume': 0.20, 'track_index': 24, 'lead': 0.0},
    {'id': 'sfx-cta',   'offset_kind': 'scene',    'scene': 5,    'src': 'sfx/Discord Notification - Sound Effect.mp3','duration': 0.6, 'volume': 0.28, 'track_index': 25, 'lead': 0.0},
]


def build_sfx(scenes: list[dict]) -> list[dict]:
    """Resolve SFX_PLAN against actual scene boundaries; skip entries
    whose scene index doesn't exist."""
    by_num = {s['num']: s for s in scenes}
    out = []
    for plan in SFX_PLAN:
        if plan['offset_kind'] == 'absolute':
            t = plan['time']
        else:
            scene = by_num.get(plan['scene'])
            if scene is None:
                continue
            t = max(0.0, scene['start'] - plan.get('lead', 0.0))
        out.append({
            'id': plan['id'],
            'src': plan['src'],
            'start': t,
            'duration': plan['duration'],
            'volume': plan['volume'],
            'track_index': plan['track_index'],
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', '-w', default='.', help='Workspace folder')
    ap.add_argument('--title', default=None, help='Document title (default: workspace name)')
    ap.add_argument('--brand-handle', default='tranvanhoang.com')
    ap.add_argument('--brand-label', default='Claude AI workflow')
    ap.add_argument('--yt-lower-third', dest='yt_lower_third', action='store_true', default=True,
                    help='Mount yt-lower-third subscribe banner at last 3s if composition exists (default: on)')
    ap.add_argument('--no-yt-lower-third', dest='yt_lower_third', action='store_false')
    ap.add_argument('--yt-lower-third-duration', type=float, default=3.0,
                    help='Duration of YT lower-third at video end (default: 3.0s)')
    ap.add_argument('--captions', dest='captions', action='store_true', default=True,
                    help='Mount captions overlay if compositions/captions.html exists (default: on). '
                         'Generate captions.html via generate_captions.py before running this script.')
    ap.add_argument('--no-captions', dest='captions', action='store_false')
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    scenes_path = workspace / 'scenes.json'
    if not scenes_path.exists():
        print(f'[root] ERROR: {scenes_path} not found. Run scaffold_project.py first.', file=sys.stderr)
        sys.exit(1)

    data = json.loads(scenes_path.read_text())
    total_duration = float(data.get('total_duration', 60.0))
    scenes = data['scenes']

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)
    tpl = env.get_template('index.html.j2')

    # Composition mount: ALWAYS scene-{num}.html — matches LLM sub-agent output
    # filenames from Phase 3d fanout. No kind→fs-lesson-1/recap-card mapping
    # because that collides on listicles (multiple tip-N scenes mapping to the
    # same archetype file). 1 file per scene, regardless of N.
    #
    # `kind` is still resolved (for body-punch routing + scene-range tagging),
    # but it does NOT determine the composition filename.
    KIND_ALIASES = {
        'tier-row': 'hook', 'post-stack': 'hook',
        'chats-stack': 'problem', 'ai-window': 'problem',
        'hero-orb': 'solution', 'app-card': 'solution',
        'counter-row': 'recap', 'team-grid': 'recap',
        'terminal-row': 'cta', 'comment-box': 'cta',
    }

    def resolve_kind(s: dict) -> str:
        """Best-effort archetype tag for routing (body-punch, hybrid-hook
        zoom). Listicle kinds like 'tip-1'..'tip-N' resolve to 'tip' so
        body-punch fires at their PIP events."""
        k = s.get('kind', '')
        if k in ('hook', 'problem', 'solution', 'recap', 'cta'):
            return k
        if k.startswith('tip'):
            return 'tip'
        v = s.get('variant') or s.get('mockup_variant') or ''
        return KIND_ALIASES.get(v, 'tip')

    mounts = []
    for i, s in enumerate(scenes):
        # Always scene-{num} — unique per scene, matches LLM fanout output.
        comp_id = f"scene-{s['num']}"
        mounts.append({
            'id': comp_id,
            'src': f'compositions/{comp_id}.html',
            'start': s['start'],
            'duration': max(0.05, s['end'] - s['start']),
            'track_index': 40 + i,
        })

    # PIP events aggregated from per-scene pip_events list.
    pip_events = []
    for s in scenes:
        for ev in s.get('pip_events', []) or []:
            pip_events.append(ev)

    # Scene starts for punch-in.
    scene_starts = [round(max(0.05, s['start']), 2) for s in scenes]
    # Always punch-in at very start of video too.
    if scene_starts and scene_starts[0] > 0.2:
        scene_starts.insert(0, 0.07)

    sfx = build_sfx(scenes)

    # Scene ranges (for body-punch routing in Hybrid Hook zoom + b-roll routing)
    scene_ranges = [
        {
            'num': s.get('num', i + 1),
            'start': round(float(s['start']), 2),
            'end': round(float(s['end']), 2),
            'kind': resolve_kind(s),
        }
        for i, s in enumerate(scenes)
    ]

    # Cream-paper b-roll <img> mounts (PIP-swap layer). One <img> per scene, named
    # N.png by convention (matches planner's placeholder_filename).
    # When N.png doesn't exist on disk, browser shows broken image at opacity 0
    # (no flicker — inert until it fades in during PIP).
    broll_images = [
        {
            'num': r['num'],
            'start': r['start'],
            'end': r['end'],
            'file': f"{r['num']}.png",
        }
        for r in scene_ranges
    ]

    # YT subscribe lower-third at last N seconds.
    yt_lt_path = workspace / 'compositions' / 'yt-lower-third.html'
    yt_lower_third = None
    if args.yt_lower_third and yt_lt_path.exists():
        dur = max(1.0, min(args.yt_lower_third_duration, total_duration))
        yt_lower_third = {
            'enable': True,
            'start': round(max(0.0, total_duration - dur), 2),
            'duration': round(dur, 2),
        }

    # Captions overlay (full-duration phrase-by-phrase) — auto-mount when
    # generate_captions.py has produced compositions/captions.html.
    captions_path = workspace / 'compositions' / 'captions.html'
    captions = {'enable': True} if (args.captions and captions_path.exists()) else None

    title = args.title or workspace.name.replace('-', ' ').title()

    html = tpl.render(
        title=title,
        brand_handle=args.brand_handle,
        brand_label=args.brand_label,
        total_duration=round(total_duration, 2),
        sfx=sfx,
        scenes=mounts,
        pip_events=pip_events,
        scene_starts=scene_starts,
        scene_ranges=scene_ranges,
        broll_images=broll_images,
        yt_lower_third=yt_lower_third,
        captions=captions,
    )

    out_path = workspace / 'index.html'
    out_path.write_text(html)
    print(f'[root] wrote {out_path}')
    yt_msg = f", yt-lower-third {yt_lower_third['start']:.2f}s+{yt_lower_third['duration']:.1f}s" if yt_lower_third else ''
    cap_msg = ', captions on' if captions else ''
    print(f'[root] {len(mounts)} scene mounts, {len(pip_events)} PIP events, {len(sfx)} SFX, '
          f'{len(broll_images)} broll-image mounts, total {total_duration:.2f}s{yt_msg}{cap_msg}')


if __name__ == '__main__':
    main()
