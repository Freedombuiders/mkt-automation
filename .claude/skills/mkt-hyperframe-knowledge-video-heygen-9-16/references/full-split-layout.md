# FULL↔SPLIT Layout — 9:16 (1080×1920)

## Purpose
Geometry, DOM, GSAP timeline và scheduling rules cho cơ chế FULL↔SPLIT: HeyGen avatar full-screen khi nói trực tiếp, co xuống BOTTOM HALF khi slide scene hiện ở TOP HALF.

## When to Load
Khi wire master index.html (Step 7-8.5) hoặc khi debug layout/transition.

---

## Geometry

| Element | FULL mode | SPLIT mode |
|---|---|---|
| `#avatar-stage` | top:0, height:1920 (cả canvas) | top:960, height:960 (bottom half) |
| `#v-source` object-position | `center 25%` (mặt ở 1/3 trên) | `center 58%` (mặt nâng lên trong khung ngang) |
| `.slide-mount` | (mount đã hết clip, ẩn) | top:0, 1080×960 (top half) |
| `#split-divider` | opacity 0 | opacity 1 (line cam tại y=956) |
| captions `.caption-stage` | bottom: 160 | bottom: 920 (ngay dưới divider, trên mặt avatar) |

KHÔNG có PIP, KHÔNG width tween — chỉ height/top của `#avatar-stage`.

## DOM tree (master)

```
#root (1080×1920)
├── #slide-bg                      z5   (đen, lót sau slide pane)
├── <audio #a-source>              track 1 (voiceover từ source.mp4)
├── SFX <audio> clips              track 70+
├── #avatar-stage                  z10  ← tween height/top
│   └── .avatar-breathing [data-layout-allow-overflow]
│       └── .avatar-punch [data-layout-allow-overflow]
│           └── <video #v-source>  track 0 (muted)
├── .slide-mount #m1..#mN          z20, track 40+ ← data-duration KẾT THÚC tại brollEnd
├── #split-divider                 z30
├── #scene-wipe / #scene-flash     z50/51, track 55/56 (top pane only, height 960)
├── #brand-mark                    z45, track 2
└── captions-mount                 z100, track 60 — LUÔN mount CUỐI
```

## Mount window = beat.start → beat.brollEnd (QUAN TRỌNG NHẤT)

Scene mount `data-duration = brollEnd - start`, KHÔNG phải end - start. Khi clip hết
tại brollEnd, framework tự ẩn mount → avatar expand full không bị scene che. Đây là cách
"breath" hoạt động mà không cần exit animation trong scene.

```
beat:    |—— start ——————— brollEnd ——— end ——|
mount:   |■■■■■■■■■■■■■■■■■■■■■■■■|             (clip window)
avatar:  SPLIT (bottom half)        FULL (breath punchline)
```

`brollEnd` mặc định = `end - 1.5` (1.5s breath). Beat cuối (CTA) có thể breath dài hơn
(2-3s) cho lời kêu gọi trực tiếp.

## Editorial cheat sheet (khi nào FULL vs SPLIT)

| Moment | Layout |
|---|---|
| Hook mở đầu 0 → beat 2 start | **FULL face** (3s đầu BẮT BUỘC full — không che mặt) |
| Thân mỗi beat (data/mockup heavy) | **SPLIT** (scene top, avatar bottom) |
| Cuối mỗi beat (punchline ~1.5s) | **FULL face breath** |
| CTA ask trực tiếp | **FULL face**, hoặc SPLIT 2-3s đầu (pricing card) rồi FULL |

Beat đầu tiên (hook) thường KHÔNG có scene mount — avatar full nói thẳng. Nếu hook cần
visual (stat lock), mount scene hook từ giây ~4-5 trở đi, giữ 0-4s full face.

## Master GSAP timeline (verbatim — copy từ template)

```js
const TRANS = 0.45;
const PRE_SHRINK = 0.30;
function goSplit(t) {
  tl.to('#avatar-stage', { height: 960, top: 960, duration: TRANS, ease: 'power2.inOut', overwrite: 'auto' }, t);
  tl.to('#v-source', { objectPosition: 'center 58%', duration: TRANS, ease: 'power2.inOut', overwrite: 'auto' }, t);
  tl.to('#split-divider', { opacity: 1, duration: 0.35, overwrite: 'auto' }, t + 0.1);
  tl.to('[data-composition-id="captions"] .caption-stage', { bottom: 920, duration: TRANS, ease: 'power2.inOut', overwrite: 'auto' }, t);
}
function goFull(t) {
  tl.to('#avatar-stage', { height: 1920, top: 0, duration: TRANS, ease: 'power2.inOut', overwrite: 'auto' }, t);
  tl.to('#v-source', { objectPosition: 'center 25%', duration: TRANS, ease: 'power2.inOut', overwrite: 'auto' }, t);
  tl.to('#split-divider', { opacity: 0, duration: 0.3, overwrite: 'auto' }, t);
  tl.set('#split-divider', { opacity: 0 }, t + 0.32);
  tl.to('[data-composition-id="captions"] .caption-stage', { bottom: 160, duration: TRANS, ease: 'power2.inOut', overwrite: 'auto' }, t);
}
SCENES.forEach((sc) => { goSplit(sc.start - PRE_SHRINK); if (sc.hasBreath) goFull(sc.brollEnd); });
```

Breathing + punch-in: giống bản 16:9 — `.avatar-breathing` scale 1.025 yoyo
(`repeat: Math.ceil(TOTAL/9)-1`), `.avatar-punch` scale 1.06→1.0 tại mỗi SCENE_START.

## Zoom package (BẮT BUỘC — user feedback 10/06/2026 "cần thêm hiệu ứng zoom cho thu hút")

4 lớp zoom, đều đã bake trong master template:

| Lớp | Element | Tween | Khi nào |
|---|---|---|---|
| Hook punch-zoom | `.avatar-punch` | 1.16→1.0, 0.85s power3.out | t=0.05, sync camera-flash SFX |
| Ken-burns push-in | `#v-source` | 1.0→1.06-1.07, 1.4-3.6s sine | Mọi đoạn full-face (open + sau mỗi goFull) |
| Breath overshoot | `.avatar-punch` | 1.10→1.0, 0.7s power3.out | Trong goFull(t), tại t+0.1 |
| Scene punch-zoom xen kẽ | `.slide-mount` (mount div) | scene lẻ 1.06→1.0, chẵn 0.95→1.0, 0.65s | Tại mỗi mount start |

Quy tắc: `goSplit` PHẢI reset `#v-source` scale về 1.0 (kèm objectPosition tween) — nếu
không ken-burns scale dồn tích qua các lần split. Tween scale trên mount div (clip) OK —
lint chỉ cấm visibility/display, transform + opacity hợp lệ.

## Captions wiring

1. Transcribe: `npx hyperframes transcribe source.mp4 --model medium --language vi`
   (LUÔN `--language vi`, KHÔNG dùng model `.en`).
2. `python3 scripts/clean_transcript.py transcript.json` → caption-groups.json
   (3-5 từ/group, timing giữ nguyên từ word-level).
3. `python3 scripts/fix_caption_typos.py caption-groups.json script.txt` rồi soi
   suspicious tokens, sửa text-only.
4. `cp assets/templates/captions.html.template compositions/captions.html` rồi
   `python3 scripts/inject_captions.py compositions/captions.html caption-groups.json`.
5. Mount CUỐI CÙNG: track 60 + `style="z-index: 100;"` — nếu không captions bị scene che.
6. `.caption-stage` phải positioned bằng `left:0; right:0; bottom:<px>; text-align:center`
   — KHÔNG transform centering (GSAP `y` xung đột translate(-50%,...)).

## Pitfalls riêng của 9:16

- **3 giây đầu luôn FULL face** — không mount scene đè mặt lúc mở.
- **Scene canvas NGẮN (960px)**: hero 64-84px, không element dưới y≈900 (đụng divider).
- **Timeline length = TOTAL**: root div PHẢI có `data-duration` + mọi ambient loop
  trong master/scene tính repeat từ TOTAL/DURATION — loop dư kéo dài MP4 render
  (bug đã gặp: divider pulse repeat:60 → video 60s thành 88s).
- **HeyGen portrait 720×1280** scale lên 1080×1920 hơi soft — chấp nhận được ở
  standard; muốn nét hơn render HeyGen 1080p.
- **objectPosition tween** trên #v-source là string — GSAP interpolate được nhưng
  KHÔNG đổi đơn vị giữa 2 state (giữ `center N%`).
