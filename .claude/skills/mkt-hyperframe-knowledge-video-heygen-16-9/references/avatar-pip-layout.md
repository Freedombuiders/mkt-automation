# Avatar Frame + SPLIT ↔ PIP Layout

HeyGen avatar floating right pane + breathing + scene-start punch-in + SPLIT↔PIP zoom mechanic. Tham khảo verbatim từ reference project `mkt-full-video-with-11-hyperframe-heygen-16-9`.

## DOM tree (master `index.html` root composition)

```
[data-composition-id="root"]  (1920×1080)
├── #slide-bg        (full canvas, #000, z-index 5)
├── #heygen-bg       (right pane warm side-light, z-index 9)
├── slide-mount × N  (compositions/scene-N.html, width 1200 SPLIT / 1920 PIP, z-index 20)
├── #avatar-frame    (SPLIT 540×880 @ 1290,100 — animatable, z-index 30)
│   └── .avatar-breathing  [data-layout-allow-overflow]
│       └── .avatar-punch  [data-layout-allow-overflow]
│           └── <video #v-source src="source.mp4" muted>
├── <audio #a-source src="source.mp4" volume=1>  (track-index 1)
├── #brand-mark      (top-left, z-index 45)
└── SFX <audio> × N  (track-index 70+)
```

**HeyGen MP4 source split**:
- `<video #v-source muted>` — visual track, NO audio (avoid double-audio)
- `<audio #a-source>` — audio track, drives timing
- Same src URL → HF auto-sync, no drift

## Geometry constants

| State | top | left | width | height | border-radius |
|---|---|---|---|---|---|
| SPLIT (default) | 100 | 1290 | 540 | 880 | 32 |
| PIP | 600 | 1540 | 320 | 420 | 20 |

- **Slide-mount width**: 1200px (SPLIT) / 1920px (PIP)
- **Why 540×880**: aspect ≈ 1:1.63, gần portrait. HeyGen source 720×1280 crop sạch (no face squish)
- **Why bottom-right PIP**: least-occupied khi slide expand. 3:4 ratio crop tốt hơn 1:1 thumbnail
- **`object-position: center 25%`**: face centered + hair-room ở trên (tweak 20-30% per avatar)

## CSS verbatim

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
  --claude-orange: #d97757;
}
[data-composition-id="root"] {
  position: relative; width: 1920px; height: 1080px;
  overflow: hidden; background: #000;
}

#slide-bg {
  position: absolute; top: 0; left: 0;
  width: 1920px; height: 1080px;
  background: #000; z-index: 5;
}

#heygen-bg {
  position: absolute;
  top: 0; left: 1200px;
  width: 720px; height: 1080px;
  background:
    radial-gradient(ellipse 400px 600px at 0% 50%, rgba(217,119,87,0.12), transparent 60%),
    #000;
  z-index: 9;
}

#avatar-frame {
  position: absolute;
  top: 100px; left: 1290px;
  width: 540px; height: 880px;
  border-radius: 32px;
  overflow: hidden;
  background: #0a0e18;
  border: 3px solid var(--claude-orange);
  box-shadow:
    0 0 0 6px rgba(217,119,87,0.18),
    0 0 80px rgba(217,119,87,0.35),
    0 30px 80px -20px rgba(0,0,0,0.8);
  z-index: 30;
  will-change: top, left, width, height, border-radius, box-shadow, border-color;
}
.avatar-breathing { position: absolute; inset: 0; will-change: transform; }
.avatar-punch     { position: absolute; inset: 0; will-change: transform; }
#v-source {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  object-position: center 25%;
}

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
```

**KHÔNG add `!important` lên `.slide-mount { width }`** — GSAP cần animate width đó cho PIP transition.

## Audio + media wiring

```html
<video id="v-source" data-start="0" data-duration="<total>"
       data-track-index="0" src="source.mp4" muted playsinline></video>

<audio id="a-source" data-start="0" data-duration="<total>"
       data-track-index="1" data-volume="1" src="source.mp4"></audio>
```

Track index allocation:
- Avatar video: 0 (muted)
- Avatar audio: 1
- Brand mark: 2
- Scene mounts: 40+
- Scene wipe / flash overlays: 55-56
- SFX: 70+

## GSAP timeline — root JS

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
    borderColor: '#a78bfa',
    boxShadow: '0 0 0 6px rgba(167,139,250,0.20), 0 0 60px rgba(167,139,250,0.40), 0 16px 48px rgba(0,0,0,0.7)',
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
    borderColor: '#d97757',
    boxShadow: '0 0 0 6px rgba(217,119,87,0.18), 0 0 80px rgba(217,119,87,0.35), 0 30px 80px -20px rgba(0,0,0,0.8)',
    duration: TRANS, ease: 'power2.inOut',
    overwrite: 'auto',
  }, t);
  tl.to('.slide-mount', {
    width: 1200,
    duration: TRANS, ease: 'power2.inOut',
    overwrite: 'auto',
  }, t);
}

// ---- PIP events from pip-schedule.json ----
const PIP_EVENTS = /* loaded from pip-schedule.json */ [
  { in: 5.80,  out: 9.20  },
  { in: 28.80, out: 33.50 },
];
PIP_EVENTS.forEach(e => { goPIP(e.in); goSplit(e.out); });

// ---- Breathing (subtle yoyo) ----
const TOTAL = /* total duration */ 60.72;
tl.to('.avatar-breathing', {
  scale: 1.025, duration: 4.5, ease: 'sine.inOut',
  yoyo: true, repeat: Math.max(1, Math.ceil(TOTAL / 9) - 1),
  transformOrigin: 'center center',
}, 1);

// ---- Punch-in at each scene start ----
const SCENE_STARTS = /* from beats.json — array of beat.start_ms / 1000 */ [];
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

## PIP scheduling rules

1. **Trigger only at emphasis beats** — typically khi 1 element major reveal trong slide (hero number lock, count-up xong, big stat scale-in). PIP mọi scene start = too busy.
2. **Min hold 2.5s, max 5s** — under 2.5s feels jittery, over 5s user forget có avatar.
3. **`out` event ≥ 0.5s trước next `in`** — slide-mount tween cần thời gian snap về 1200.
4. **Pair `goPIP(t)` và `goSplit(t)` luôn** — never leave PIP state hanging cuối timeline.
5. **`overwrite: 'auto'`** trên mọi avatar-frame tween — without this, half-finished transition glow conflict với breathing scale.
6. **Density**: 1-2 PIP / scene là sweet spot. 7 scenes × 1.5 = ~10 PIP events là max trước khi feel busy.

## Breathing magnitude scale

| Magnitude | Feel |
|---|---|
| 1.015 | Almost imperceptible — meditative |
| **1.025** (default) | Natural breathing — production setting |
| 1.04 | Noticeable — energetic / podcast |
| 1.06 | Distracting — avoid |

## pip-schedule.json format

Sinh ở Step 7.3 (sau khi beats.json có time ranges):

```json
{
  "pip_events": [
    {
      "in": 5.80,
      "out": 9.20,
      "beat_index": 1,
      "reason": "hero stat count-up lock"
    },
    {
      "in": 28.80,
      "out": 33.50,
      "beat_index": 3,
      "reason": "premise reveal — orb pattern"
    }
  ]
}
```

Claude orchestrator chọn PIP events dựa trên scene `pattern`:

| Scene pattern | PIP timing |
|---|---|
| `hero` | Khi count-up final value locks |
| `card-grid-3x2` / `card-grid-2x2` | KHÔNG PIP (cards parallel reveal — không có single emphasis) |
| `terminal-typewriter` | Khi last command completes + checkmark |
| `comparison-2card` | Khi cả 2 cards fully revealed |
| `image-feature` | Khi annotation pins all settled (image is the focus) |
| `cta-outro` | Toàn bộ outro scene |
| `pipeline` / `network-graph` | Khi diagram complete |
| `diff-window` | Khi "all patched" subtitle xuất hiện |

## Brand mark replacement

**Pattern này KHÔNG dùng "brand stamp avatar 112px bottom-right"** từ skill knowledge-video gốc. Vì avatar HeyGen đã chiếm chỗ đó.

Thay vào: minimal text-only brand mark top-left:

```html
<div id="brand-mark" class="clip brand-mark"
     data-start="0" data-duration="<total>" data-track-index="2">
  <span class="dot"></span>
  <span><span class="at">@</span>tranvanhoang.com</span>
  <span class="sep">·</span>
  <span>Knowledge AI</span>
</div>
```

```css
.brand-mark {
  position: absolute; top: 40px; left: 60px; z-index: 45;
  font: 600 14px/1 'JetBrains Mono', monospace;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--ink-mute);
  display: inline-flex; align-items: center; gap: 10px;
}
.brand-mark .dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--claude-orange);
  box-shadow: 0 0 10px var(--claude-orange);
}
.brand-mark .at  { color: var(--pink); }
.brand-mark .sep { opacity: 0.4; }
```

z-index 45 = above PIP avatar (30) để brand luôn visible khi avatar shrink xuống corner.

## Common pitfalls

| Pitfall | Fix |
|---|---|
| White avatar frame border | Default phải là claude-orange `#d97757` (3px solid + 6px halo + 80px outer glow) |
| `!important` trên `.slide-mount { width }` | Xoá. GSAP cần animate width. Chỉ giữ `!important` ở inner `> [data-composition-id]`. |
| HeyGen render 1280×720 landscape | Vẫn render 720×1280 portrait — landscape avatar frame crop từ portrait source. |
| Avatar face crop trán | `object-position: center 25%` (default), tweak 20-30% per avatar |
| PIP cyan/violet glow conflict với split-mode glow | Add `overwrite: 'auto'` vào mọi tween chỉnh `boxShadow` của `#avatar-frame` |
| PIP_EVENTS overlap | Tách ≥ 0.3s giữa `out` và next `in` |
| Track-index conflict | Avatar 0/1, brand 2, scenes 40+, wipe 55-56, SFX 70+ |
| Double audio (video không muted) | `<video #v-source muted>` luôn. Audio chỉ từ `<audio #a-source>` |
| Scene canvas 1920×1080 | KHÔNG. Scenes là 1200×1080 (slide pane), expand thành 1920 khi PIP (slide-mount tween width) |
| `container_overflow div.avatar-breathing` (inspect) | Thêm `data-layout-allow-overflow` vào `.avatar-breathing` + `.avatar-punch` (breathing scale 1.025 vượt clip; vô hại, `overflow:hidden` cắt) |
| `composition_self_attribute_selector` (lint) | Master select root bằng `#root` (id), KHÔNG `[data-composition-id="main"/"root"]` |
| PIP "feels stretched" | Scene content phải flex-CENTER intrinsic-width → khi slide-mount tween 1200→1920 content RE-CENTER (không stretch). Đừng dùng block `width:100%` bên trong scene |
| Wipe/flash `gsap_exit_missing_hard_kill` (lint) | Thêm `tl.set('#scene-flash'/'#scene-wipe',{opacity:0}, t)` sau mỗi fade |
