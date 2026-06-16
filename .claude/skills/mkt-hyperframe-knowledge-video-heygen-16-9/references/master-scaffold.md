# Master `index.html` Scaffold (HeyGen + SPLIT/PIP variant)

Master `index.html` orchestrate root composition 1920×1080 với slide pane bên trái (1200×1080) + HeyGen avatar floating frame bên phải. Scenes là `<template>` sub-comp **1200×1080** loaded vào slide-mount.

## Layer stack (z-index + track-index)

| Element | track-index | z-index | Purpose |
|---|---|---|---|
| `<video id="v-source" muted>` HeyGen MP4 | 0 | — | Avatar visual, NO audio |
| `<audio id="a-source">` HeyGen MP4 audio | 1 | — | Voiceover, volume 1.0 |
| `#brand-mark` top-left text | 2 | 45 | `@tranvanhoang.com` JBM mono |
| `#slide-bg` black canvas | — | 5 | Full 1920×1080 black bg |
| `#heygen-bg` right pane | — | 9 | Warm side-light backdrop |
| Scene mounts `.slide-mount × N` | 40..40+N | 20 | data-composition-src → scene-N.html, animatable width |
| Scene wipe overlay | 55 | 50 | Color bar sweep (chỉ trong slide pane) |
| Scene flash overlay | 56 | 51 | Brightness flash (chỉ slide pane) |
| `#avatar-frame` HeyGen avatar | — | 30 | SPLIT 540×880 / PIP 320×420, animatable |
| SFX layer | 70..70+M | — | Sound effects |

## Geometry constants

- **Root canvas**: 1920×1080
- **Slide pane** (default SPLIT): 1200×1080 left
- **Right pane**: 720×1080 right (cho avatar + warm backdrop)
- **Avatar SPLIT**: 540×880 at (1290, 100), border-radius 32, claude-orange border
- **Avatar PIP**: 320×420 at (1540, 600), border-radius 20, violet border
- **Slide-mount expand (PIP)**: 1920×1080 (full canvas)

Chi tiết CSS + GSAP timeline: `avatar-pip-layout.md`.

## Brand mark replacement

**KHÔNG dùng brand stamp avatar 112px bottom-right** (knowledge-video skill gốc) — vì avatar HeyGen đã chiếm chỗ đó.

Thay vào text-only brand mark top-left:

```html
<div id="brand-mark" class="clip brand-mark"
     data-start="0" data-duration="<total>" data-track-index="2">
  <span class="dot"></span>
  <span><span class="at">@</span>tranvanhoang.com</span>
  <span class="sep">·</span>
  <span>Knowledge AI</span>
</div>
```

CSS đầy đủ: `avatar-pip-layout.md`.

## Asset copies (parallel bootstrap)

1 `cp -r` block ở Step 0.5 — không serial vài lần:

```bash
mkdir -p $OUT/assets/sfx
cp workspace/assets/reels/sfx/*.mp3 $OUT/assets/sfx/
```

HeyGen MP4 `source.mp4` được Phase 2 download trực tiếp vào `$OUT/`, KHÔNG copy. KHÔNG cần avatar PNG nữa (avatar source là HeyGen MP4).

## Scene-mount declarations

```html
<div class="clip slide-mount" data-composition-src="scenes/scene-1-hero.html"
     data-start="0" data-duration="13.66"
     data-composition-id="scene-1-hero" data-track-index="40"></div>

<div class="clip slide-mount" data-composition-src="scenes/scene-2-premise.html"
     data-start="13.66" data-duration="9.7"
     data-composition-id="scene-2-premise" data-track-index="41"></div>
```

- Each `.slide-mount` shares same `data-composition-id` với inner sub-comp
- Track index 40+ — separates from audio (0/1), brand (2), wipe/flash (55/56), SFX (70+)
- `data-start` of next scene = `data-start + data-duration` of previous

## Scene overlap KHÔNG dùng (khác với base skill)

Trong base `mkt-hyperframe-knowledge-video`, scene-mount overlap 0.4s cho crossfade. Ở skill này KHÔNG cần — vì:
- Slide-mount tween width 1200↔1920 cho PIP. Overlap sẽ gây 2 mount chồng chéo + flicker.
- Transitions giữa scene vẫn dùng wipe/flash overlay (cùng slide pane), không tween scene opacity.

`data-start` scene N+1 = `data-start + data-duration` scene N. Không gap, không overlap.

## Audio + media wiring

```html
<video id="v-source" data-start="0" data-duration="<total>"
       data-track-index="0" src="source.mp4" muted playsinline></video>

<audio id="a-source" data-start="0" data-duration="<total>"
       data-track-index="1" data-volume="1" src="source.mp4"></audio>
```

`<total>` = ffprobe duration của `source.mp4` (NOT alignment.json — HeyGen có thể truncate / pad).

## Initial scaffold trước Phase 2

Có thể tạo skeleton master `index.html` SONG SONG khi HeyGen render (Phase 2 background mode). Skeleton có sẵn:
- `<head>`, full CSS (`avatar-pip-layout.md`)
- `#slide-bg`, `#heygen-bg`, `#brand-mark`
- `#avatar-frame` div empty (sẽ wire `<video>` sau)

Chỉ thiếu (fill khi Phase 2 + Step 8 xong):
- `data-duration` của video/audio/brand (probe ffprobe `source.mp4`)
- `<video src="source.mp4">` + `<audio src="source.mp4">`
- Scene mounts (sau Step 8 fanout)
- PIP_EVENTS array (sau Step 7.3 pip-schedule)
- SCENE_STARTS array (từ beats.json)
