# Architecture — root composition + slide-mount + avatar-frame mechanics

Code-level deep dive for the 16:9 root composition. Every snippet here is **verbatim from the production project** at `workspace/content/2026-05-08/loi-ich-claude-ai/index.html` — copy and adapt, don't reinvent.

## Root canvas

- `[data-composition-id="root"]` width 1920, height 1080.
- Background `#000` (pure black).
- Inner `<body>` font Inter.

```html
<div data-composition-id="root" data-start="0" data-width="1920" data-height="1080">
  <!-- content -->
</div>
```

## DOM tree

```
[data-composition-id="root"]  (1920×1080)
├── #slide-bg        (full canvas, #000, z-index 5)
├── #heygen-bg       (right pane backdrop with warm side-light, z-index 9)
├── #avatar-frame    (SPLIT default 540×880 @ 1290,100 — animatable, z-index 30)
│   └── .avatar-breathing
│       └── .avatar-punch
│           └── <video #v-source src="source.mp4" muted>  (object-fit: cover, position center 25%)
├── <audio #a-source src="source.mp4" volume=1>  (track-index 1)
├── <audio #sfx-hook>   ... 6 SFX  (track-index 20–25)
├── #brand-mark      (top-left clip, z-index 45)
├── <script gsap>    (root timeline)
└── slide-mount × N  (compositions/<scene>.html, z-index 20, animatable width)
```

## CSS — full root style block

Copy verbatim, swap colors per brand:

```css
:root {
  --bg: #000000;
  --ink: #f5f7fa;
  --ink-mute: #8b94a8;
  --line: rgba(255,255,255,0.10);
  --cyan: #67e8f9;
  --violet: #a78bfa;
  --pink: #f0abfc;
  --lime: #a3e635;
  --orange: #fb923c;
  --rose: #fb7185;
}
html, body {
  margin: 0; padding: 0;
  background: var(--bg);
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
}
[data-composition-id="root"] {
  position: relative; width: 1920px; height: 1080px;
  overflow: hidden; background: #000;
}

/* Right pane backdrop — pure black with very subtle warm side-light */
#heygen-bg {
  position: absolute;
  top: 0; left: 1200px;
  width: 720px; height: 1080px;
  background:
    radial-gradient(ellipse 400px 600px at 0% 50%, rgba(251,146,60,0.10), transparent 60%),
    #000;
  z-index: 9;
}

/* Slide pane bg — pure black */
#slide-bg {
  position: absolute;
  top: 0; left: 0;
  width: 1920px; height: 1080px;
  background: #000;
  z-index: 5;
}

/* Avatar wrapper — animatable position+size for SPLIT ↔ PIP */
#avatar-frame {
  position: absolute;
  top: 100px; left: 1290px;
  width: 540px; height: 880px;
  border-radius: 32px;
  overflow: hidden;
  background: #0a0e18;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow:
    0 30px 80px -20px rgba(0,0,0,0.8),
    0 0 0 1px rgba(103,232,249,0.10),
    0 0 60px rgba(103,232,249,0.08);
  z-index: 30;
  will-change: top, left, width, height, border-radius, box-shadow;
}
.avatar-breathing { position: absolute; inset: 0; will-change: transform; }
.avatar-punch     { position: absolute; inset: 0; will-change: transform; }
#v-source {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  object-position: center 25%;  /* face centered, hair-room above */
}

/* SCENE SLIDE MOUNT — animatable width for SPLIT (1200) ↔ PIP (1920) */
.slide-mount {
  position: absolute;
  top: 0; left: 0;
  width: 1200px; height: 1080px;
  overflow: hidden;
  background: transparent;
  z-index: 20;
  will-change: width;
}
.slide-mount > [data-composition-id] {
  width: 100% !important; height: 100% !important;
  position: absolute !important;
  top: 0; left: 0;
}

/* Brand mark — minimal, top-left */
.brand-mark {
  position: absolute;
  top: 40px; left: 60px;
  z-index: 45;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600; font-size: 14px;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--ink-mute);
  display: inline-flex; align-items: center; gap: 10px;
}
.brand-mark .dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--lime);
  box-shadow: 0 0 10px var(--lime);
}
.brand-mark .at  { color: var(--pink); }
.brand-mark .sep { opacity: 0.4; }
```

### Why these values

| Decision | Reason |
|---|---|
| Slide-mount default width 1200px | Leaves 720px right pane; avatar frame `1290 left` sits 90px inset from right pane edge → not touching slide edge → "floating" feel. |
| Avatar frame 540×880 | Aspect ≈ 1:1.63 (closer to portrait than 1:1). HeyGen 720×1280 portrait source crops cleanly here without face squish. |
| `object-position: center 25%` | HeyGen avatar usually frames face roughly center-top of portrait. 25% from top keeps face centered with hair-room above. Tweak 20%–30% per avatar. |
| Border-radius 32 | Modern editorial / glassmorphism feel. PIP state drops to 20 (smaller frame, smaller radius). |
| `box-shadow` triple-layer | First shadow = drop (depth). Second = subtle cyan border halo (continuity with eyebrow chip color). Third = ambient cyan glow (matches design accent). |
| `slide-mount > [data-composition-id] { width: 100% !important }` | Inner sub-composition fills the mount regardless of its own `data-width`. **DO NOT add `!important` to `.slide-mount` itself** — GSAP needs to animate that width during PIP. |
| `will-change: top, left, width, height, border-radius, box-shadow` | Hint the compositor to layer-promote ahead of GSAP tweens — keeps PIP transitions smooth. |
| `#brand-mark` z-index 45 (above PIP avatar @30) | Brand stays visible even when avatar shrinks to bottom-right and slide expands. |

## Audio + media wiring

```html
<video id="v-source" data-start="0" data-duration="60.72"
       data-track-index="0" src="source.mp4" muted playsinline></video>

<audio id="a-source" data-start="0" data-duration="60.72"
       data-track-index="1" data-volume="1" src="source.mp4"></audio>

<!-- 6 SFX, track-index 20–25, low volume 0.18–0.32 -->
<audio id="sfx-hook"  data-start="0"     data-duration="0.6" data-track-index="20" data-volume="0.32" src="sfx/camera-flash.mp3"></audio>
<audio id="sfx-l1"    data-start="13.73" data-duration="0.5" data-track-index="21" data-volume="0.18" src="sfx/Whoosh sound effect (1).mp3"></audio>
<audio id="sfx-l2"    data-start="27.37" data-duration="0.5" data-track-index="22" data-volume="0.18" src="sfx/búng tay.mp3"></audio>
<audio id="sfx-l3"    data-start="47.75" data-duration="0.5" data-track-index="23" data-volume="0.18" src="sfx/Laser.mp3"></audio>
<audio id="sfx-recap" data-start="47.75" data-duration="0.5" data-track-index="24" data-volume="0.20" src="sfx/ting.mp3"></audio>
<audio id="sfx-cta"   data-start="53.80" data-duration="0.6" data-track-index="25" data-volume="0.28" src="sfx/Discord Notification - Sound Effect.mp3"></audio>
```

Lý do split `<video muted>` + `<audio>` cùng src:
- HeyGen MP4 có cả video + audio
- HF render compositor cần video silent (avoid double-audio) trong khi audio track dẫn timing
- Dùng cùng src giúp HF auto-sync, KHÔNG drift

## Brand mark

```html
<div id="brand-mark" class="clip brand-mark"
     data-start="0" data-duration="60.72" data-track-index="2">
  <span class="dot"></span>
  <span><span class="at">@</span>tranvanhoang.com</span>
  <span class="sep">·</span>
  <span>Claude AI workflow</span>
</div>
```

`data-duration` = full video. `data-track-index="2"` to keep it above audio tracks but below SFX.

## Slide-mount declarations

```html
<div class="clip slide-mount" data-composition-src="compositions/fs-lesson-1.html"
     data-start="0.07"  data-duration="13.66" data-composition-id="fs-lesson-1" data-track-index="40"></div>
<div class="clip slide-mount" data-composition-src="compositions/fs-lesson-2.html"
     data-start="13.73" data-duration="13.64" data-composition-id="fs-lesson-2" data-track-index="41"></div>
<div class="clip slide-mount" data-composition-src="compositions/fs-lesson-3.html"
     data-start="27.37" data-duration="20.38" data-composition-id="fs-lesson-3" data-track-index="42"></div>
<div class="clip slide-mount" data-composition-src="compositions/recap-card.html"
     data-start="47.75" data-duration="6.05"  data-composition-id="recap-card"  data-track-index="43"></div>
<div class="clip slide-mount" data-composition-src="compositions/fs-cta.html"
     data-start="53.80" data-duration="6.92"  data-composition-id="fs-cta"      data-track-index="44"></div>
```

Track index 40+ for slides — separates from audio (1, 2, 20–25) and avatar (0).

`data-start` of next scene = `data-start + data-duration` of previous (inclusive transition handled by HF). Allow ~0.06s gap if you want hard cut padding.

## GSAP timeline — full root JS

```js
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });

// ---- Initial entrance ----
tl.from("#avatar-frame", {
  scale: 0.95, opacity: 0, duration: 0.7, ease: 'power3.out',
  transformOrigin: 'center'
}, 0);
tl.from("#brand-mark", {
  x: -20, opacity: 0, duration: 0.5, ease: 'power3.out'
}, 0.3);

// ---- SPLIT ↔ PIP transitions ----
const SPLIT = { top: 100, left: 1290, width: 540, height: 880, borderRadius: 32 };
const PIP   = { top: 600, left: 1540, width: 320, height: 420, borderRadius: 20 };
const TRANS = 0.55;

function goPIP(t) {
  tl.to('#avatar-frame', {
    ...PIP,
    boxShadow: '0 0 40px rgba(103,232,249,0.45), 0 16px 48px rgba(0,0,0,0.7)',
    duration: TRANS, ease: 'power2.inOut',
    overwrite: 'auto',
  }, t);
  tl.to('.slide-mount', {
    width: 1920,
    duration: TRANS, ease: 'power2.inOut',
    overwrite: 'auto',
  }, t);
}
function goSplit(t) {
  tl.to('#avatar-frame', {
    ...SPLIT,
    boxShadow: '0 30px 80px -20px rgba(0,0,0,0.8), 0 0 60px rgba(103,232,249,0.08)',
    duration: TRANS, ease: 'power2.inOut',
    overwrite: 'auto',
  }, t);
  tl.to('.slide-mount', {
    width: 1200,
    duration: TRANS, ease: 'power2.inOut',
    overwrite: 'auto',
  }, t);
}

// ---- PIP emphasis moments (option B: tier-letter glow reveals) ----
const PIP_EVENTS = [
  // Scene 1 — "0h" AFTER payoff
  { in: 5.80,  out: 9.20  },
  // Scene 3 — orb reveal
  { in: 28.80, out: 33.50 },
  // Scene 3 — spec trio (∞ / 100tr / 8h)
  { in: 35.20, out: 44.50 },
  // Scene 4 — RESULT 15h counter
  { in: 48.50, out: 53.20 },
  // Scene 5 — CTA "AI" terminal
  { in: 54.40, out: 60.50 },
];
PIP_EVENTS.forEach(e => { goPIP(e.in); goSplit(e.out); });

// ---- Avatar BREATHING zoom (subtle, continuous) ----
tl.to('.avatar-breathing', {
  scale: 1.025, duration: 4.5, ease: 'sine.inOut',
  yoyo: true, repeat: 14, transformOrigin: 'center center',
}, 1);

// ---- Avatar PUNCH-IN at each scene start (beat-driven) ----
const SCENE_STARTS = [0.07, 13.73, 27.37, 47.75, 53.80];
SCENE_STARTS.forEach(t => {
  tl.to('.avatar-punch', {
    scale: 1.06, duration: 0.35, ease: 'power2.out',
    transformOrigin: 'center center', overwrite: 'auto',
  }, t);
  tl.to('.avatar-punch', {
    scale: 1.0, duration: 0.7, ease: 'power3.out', overwrite: 'auto',
  }, t + 0.45);
});

window.__timelines["root"] = tl;
```

### PIP scheduling rules

1. **Trigger only at emphasis beats** — typically when a tier-letter scales in inside the slide. PIP every scene start = too busy.
2. **Min hold 2.5s, max 5s** — under 2.5s feels jittery, over 5s makes user forget there's an avatar.
3. **`out` event ≥ 0.5s before next `in`** — gives the slide-mount tween time to fully snap to 1200 before next expand.
4. **Pair `goPIP(t)` and `goSplit(t)` always** — never leave PIP state hanging at end of timeline.
5. **`overwrite: 'auto'`** on every avatar-frame tween — without this, a half-finished PIP→SPLIT transition glow can clash with the next breathing scale tween, causing visible jitter.

### Breathing yoyo math

- `scale: 1.0 → 1.025` over 4.5s, yoyo back, repeat 14 times = 4.5 × 2 × 14 = 126s of coverage.
- For longer videos, bump `repeat` accordingly: `Math.ceil(totalDuration / 9) - 1`.
- Magnitude 1.025 is intentionally subtle — anything above 1.04 looks like the avatar is "pulsing" rather than "breathing".

### Punch-in math

- `1.0 → 1.06` (0.35s back.out) → `1.0` (0.7s power3.out) at each `SCENE_STARTS[i]`.
- Total punch envelope = 1.05s. Keeps below ~15% of typical scene length.
- Combines with breathing (multiplicative scale on different layers — `.avatar-punch` and `.avatar-breathing` are separate divs intentionally).

## Why bottom-right corner for PIP

User reference (the production project this skill canonicalizes) chose `(1540, 600)` because:
- Bottom-right = least-occupied screen real estate when slide expands to 1920.
- 320×420 PIP frame is closer to 3:4 — better face crop from 720×1280 source than 1:1 thumbnail would be.
- Cyan-glow border (continuity with eyebrow chip cyan in scenes) ties PIP visually into the slide.
- Top-right would conflict with brand-mark; top-left would steal eye-flow at scene start; center would dominate.

## Extending — adding a 6th scene

1. Add entry to `scenes-outline.json` with new `start`/`end`.
2. Bump `data-duration` of `<video #v-source>` and `<audio #a-source>` to new total.
3. Add new `<div class="clip slide-mount">` declaration, increment `data-track-index`.
4. Update `SCENE_STARTS` array.
5. Re-evaluate `PIP_EVENTS` — if new scene has emphasis beat, add pair.
6. Bump breathing `repeat` count.
7. Re-add SFX trigger at new scene start (track-index 26).

## Extending — changing PIP corner

Edit `PIP` constant:
- Bottom-left: `{ top: 600, left: 60, ... }`
- Top-right: `{ top: 60, left: 1540, ... }` (will overlap brand-mark — move brand-mark first)
- Top-left: `{ top: 60, left: 60, ... }` (same brand collision)

If face crop looks wrong in new corner, also adjust `object-position` per state by adding to `goPIP`:
```js
tl.to('#v-source', { objectPosition: 'center 30%', duration: TRANS }, t);
```

## Extending — swap breathing magnitude

| Magnitude | Feel |
|---|---|
| 1.015 | Almost imperceptible — meditative |
| 1.025 (default) | Natural breathing — used in production |
| 1.04 | Noticeable — energetic / podcast |
| 1.06 | Distracting — avoid except for high-energy scripts |

## Lint gotchas

| Lint warning | Fix |
|---|---|
| `data-duration missing on <video>` | Add `data-duration="<total>"` |
| `slide-mount has !important on width` | Remove `!important` from `.slide-mount { width }` (NOT from inner `[data-composition-id]`) |
| `track-index conflict` | Audio 1, brand 2, SFX 20–25, slides 40+ — keep separated |
| `composition-id duplicate` | Each `<div class="clip slide-mount">` and the inner sub-comp must share the SAME `data-composition-id` |
