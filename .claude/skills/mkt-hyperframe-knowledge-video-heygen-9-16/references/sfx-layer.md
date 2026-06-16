# SFX Layer (Sound Effects)

SFX là layer **trên top voiceover** để nhấn mạnh peak moments — KHÔNG phải background music. Quy tắc vàng: **fewer well-placed hits beat constant noise.**

**Target density**: ~1 SFX / 30-40s video. Video 8-9 phút → max 15 hits.

## SFX library mặc định

Đặt tại `workspace/assets/reels/sfx/`:

| File | Duration | Best use |
|---|---|---|
| `boom.mp3` | 1.30s | Premise hit, finale punch, "0 packages" / "free" big claims |
| `búng tay.mp3` | 0.29s | Finger snap — slide change, micro tick, count step |
| `camera-flash.mp3` | 4.50s | Title slideshow kickoff, screenshot reveals |
| `Discord Notification - Sound Effect.mp3` | 0.86s | Thumbnail pop-in, callout reveal, notification moment |
| `lung linh.mp3` | 1.70s | Magical reveal — seal, certification, award, prize |
| `SUDDEN SUSPENSE.mp3` | 1.30s | Problem setup, "but here's the issue" tension |
| `ting.mp3` | 0.95s | Stat tick, count-up start, checkmark, +1 reveal |
| `Whoosh sound effect (1).mp3` | 1.02s | Scene wipe, element fly-in, transition |
| `Wow.mp3` | 2.35s | Big number reveal, impressive stat payoff |

## Placement decision rules

1. **Title card / showcase opener**: `camera-flash` ở t=0 nếu có slideshow ảnh
2. **Title slide transitions**: `búng tay` mỗi slide tick (max 4 ticks)
3. **Title → scene-01 wipe**: `Whoosh` (chỉ 1 lần ở major intro transition)
4. **Stat reveal beat (hero scene)**: `ting` ở moment count-up start
5. **Premise hit / "X vs Y" reveal**: `boom`
6. **Problem setup beat ("here's the wall")**: `SUDDEN SUSPENSE`
7. **Payoff line / final reveal in a long beat**: `Wow`
8. **Screenshot / thumbnail pop-in**: `Discord Notification`
9. **Magical seal moment (license, award, badge)**: `lung linh`
10. **Final CTA outro entrance**: `boom`

## Track index allocation

- Voiceover (`#vo`): track-0 (volume 1.0, NEVER touch)
- Scene mounts: tracks 10–25 (one per scene)
- Brand stamp: track-60
- **SFX**: tracks 70+ (1 SFX per track-index)
- Total tracks <100

## Volume rule

SFX volume luôn `data-volume="0.4"` đến `"0.5"`. Voiceover ở volume 1.0 và phải dominate; SFX punctuate, không compete.

## Wiring pattern

Trong `index.html`, INSIDE `<div id="root">`, AFTER `<audio id="vo">`, BEFORE title-card div:

```html
<!-- ── SFX layer (track 70+) ── -->
<audio id="sfx-title-flash"
       data-start="0"
       data-duration="2.0"
       data-track-index="70"
       data-volume="0.45"
       src="assets/sfx/camera-flash.mp3"></audio>

<audio id="sfx-snap-1"
       data-start="1.7"
       data-duration="0.3"
       data-track-index="71"
       data-volume="0.45"
       src="assets/sfx/búng tay.mp3"></audio>

<audio id="sfx-whoosh-intro"
       data-start="5.443"
       data-duration="1.0"
       data-track-index="72"
       data-volume="0.5"
       src="assets/sfx/Whoosh sound effect (1).mp3"></audio>

<audio id="sfx-premise-boom"
       data-start="17.805"
       data-duration="1.3"
       data-track-index="73"
       data-volume="0.5"
       src="assets/sfx/boom.mp3"></audio>
```

## Process

1. Copy SFX vào project: `mkdir -p $OUT/assets/sfx && cp workspace/assets/reels/sfx/*.mp3 $OUT/assets/sfx/`
2. Đọc `beats.json` để biết start_ms / end_ms mỗi beat
3. Liệt kê 10-15 SFX hits dựa trên decision rules. Không quá 15 cho video 8-9 phút. Ít hơn là OK.
4. Trong mỗi beat, xác định ms tương đối của moment nhấn (peak word, reveal element). Tính ABSOLUTE time = `beat.start_ms / 1000 + relative_s`.
5. Wire vào index.html theo pattern trên. Mỗi audio có unique `id` + unique `data-track-index` (70, 71, 72, ...).
6. Validate: `npx hyperframes lint` (0 errors), `npx hyperframes validate --no-contrast` (no console errors). Nếu báo 404 → check path.

## Common mistakes

1. **Quá nhiều SFX** — video 5 phút có 30+ SFX = noise. Cap 1 SFX / 30s.
2. **SFX overlap với voiceover peak word** — fade hoặc shift 0.2-0.5s để SFX kết thúc trước/sau peak word.
3. **Volume quá to** — SFX ≥ 0.6 sẽ át voice. Stick 0.4-0.5.
4. **SFX dài hơn moment** — `camera-flash` 4.5s cho moment 1s = ghê. Set `data-duration` ngắn lại (HyperFrames clip audio).
5. **Mỗi scene transition đều có Whoosh** — overkill. Chỉ Whoosh ở 1-2 major intro transition.
6. **Quên track-index 70+** — nếu trùng với scene track-index sẽ conflict.
7. **Quên copy file vào project** — runtime serve từ project root, path tuyệt đối ngoài project sẽ 404.
