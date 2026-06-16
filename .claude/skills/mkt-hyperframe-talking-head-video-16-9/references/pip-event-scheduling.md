# PIP event scheduling — when and why to fire `goPIP(t)` / `goSplit(t)`

## Concept

In SPLIT mode (default), the avatar lives in a 540×880 frame on the right and the slide pane is 1200×1080 on the left. In PIP mode, the slide pane expands to fill 1920×1080 (full canvas) and the avatar shrinks to a 320×420 corner thumbnail at `top:600, left:1540`.

Each `goPIP(t)` schedules the transition INTO PIP at absolute timeline time `t`. Each `goSplit(t)` schedules the transition BACK to SPLIT.

## Default scheduling rule

Per scene, fire **one** PIP window aligned with the scene's first emphasis beat — typically the first tier-letter glow scale-in (~scene_start + 1.0–1.5s in the composition's local timeline). Hold for 2.5–4.0 seconds, then `goSplit`.

For long scenes (≥ 12s — solution scenes are the typical case) fire **two** PIP windows, separated by ~2 seconds in SPLIT mode so the avatar regains visual weight between data points.

## Computing absolute times

`scenes.json` per scene has:

```json
{
  "num": 3,
  "start": 27.37,    // absolute video time
  "end":   47.75,
  "pip_events": [
    { "in": 28.77, "out": 32.77 },   // ≈ start + 1.4 → start + 5.4
    { "in": 34.37, "out": 38.87 }
  ]
}
```

`scaffold_project.py` derives this automatically. Override per-scene if a specific moment in the spoken voiceover should drive the cut (e.g., right when avatar says "100 trang", schedule the PIP to land on the `100tr` tier-letter glow in fs-lesson-3 — usually around `start + 11.0s`).

## Anti-rules

- **Never overlap two PIP windows.** `goSplit(out_1) < goPIP(in_2)` strictly.
- **Don't `goPIP` in the last 1.5s of a scene** — there's no time to enjoy the slide before the next scene mounts.
- **Don't `goPIP` before scene_start + 0.5s** — punch-in animation on avatar is still active; both at once = jittery.
- **Don't fire PIP during the entrance beat (0–0.7s of video)** — `tl.from('#avatar-frame', { scale:0.95, opacity:0 })` is doing its work; PIP would interfere.

## Hook scene exception

The hook scene typically does NOT trigger PIP — first 13s should establish the SPLIT layout in viewer's mind. PIP starts being useful from scene 2 onwards.

If you want a PIP in the hook (e.g., to show the BEFORE/AFTER tier rows full-screen), schedule it after both tier rows have animated in (~start + 7s) and exit before `next_scene_start - 0.6s`.

## Recap and CTA scenes

- Recap: PIP for the counter reveal moment (`start + 1.5s`), exit 3-4s later. Avatar full-frame again for the rally line at end.
- CTA: PIP from `start + 0.6s` to `start + 4.0s` while the typing animation runs and gifts appear; SPLIT for final 2.5s direct-ask.

## How to verify

After running `generate_root_index.py`, scrub the Studio timeline with mouse. At each PIP window, the slide pane should expand smoothly over 0.55s and avatar should shrink to corner with cyan glow box-shadow. At `goSplit`, both reverse smoothly. Visual hitch = animation collision (probably overlapping windows or a missing `overwrite: 'auto'` on a tween).
