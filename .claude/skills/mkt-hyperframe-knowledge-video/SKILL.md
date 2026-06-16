---
name: mkt-hyperframe-knowledge-video
description: Tạo video chia sẻ kiến thức / tin tức 16:9 (1920×1080) bằng HyperFrames runtime + ElevenLabs v3 TTS — pipeline design.md → script → TTS parallel chunks → forced alignment → fan out parallel sub-agents author từng scene HTML dạng `<template>` sub-comp (GSAP only, seeded PRNG) → master `index.html` với scene transitions + brand stamp + SFX → `npx hyperframes render` ra MP4. Style dark cinematic navy + particle bokeh + hero Inter 900 + glassmorphic cards. Output `workspace/content/<date>/<slug>/<slug>.mp4`. **MUST use this skill when** user nói "tạo video chia sẻ kiến thức", "tạo video tin tức", "knowledge sharing video", "news video AI/tech", "hyperframe video", "video motion graphic 16:9", "video về github repo hot", "video review tool", "video release notes", "video keynote", "video kiểu Google I/O", "video kiểu Apple keynote", "explainer video AI", "video về repo X kèm screenshots", hoặc tạo video knowledge/news cần motion graphic + voiceover ElevenLabs + render bằng HyperFrames.
---

# HyperFrame Knowledge Video Pipeline

Tạo video chia sẻ kiến thức / tin tức 16:9 bằng HyperFrames runtime (`npx hyperframes render` trên `index.html`). Style cinematic dark navy + particle bokeh + hero uppercase + glassmorphic cards.

**AUTOPILOT (override mọi quy tắc "hỏi user / preview-first"):** Chạy 1 mạch tới MP4, KHÔNG dừng hỏi user, KHÔNG mở preview Studio. Thiếu info (topic, ngôn ngữ, slug, style, số scene, voice) → tự chọn default và chạy tiếp. Chỉ hỏi 1 câu DUY NHẤT khi thiếu input bắt buộc tuyệt đối (không có topic/script nào để bắt đầu). Render `-q standard` (chất lượng vừa phải) xong báo absolute path MP4 cho user.

## Khi nào dùng skill này

User muốn 1 video knowledge-sharing / news có:
- Không cần talking head, voice-over ElevenLabs
- Motion graphic chuyên nghiệp (typography, stat counters, diagrams)
- Footer brand `@tranvanhoang.com` + avatar Hoàng cố định
- Output 1 file MP4 16:9 (1920×1080)

KHÔNG dùng skill này khi:
- User có footage talking-head → `mkt-hyperframe-talking-head-video-16-9`
- Carousel ảnh tĩnh → skill khác
- Landing page HTML → skill khác

## Đầu vào

| Input | Bắt buộc | Format |
|---|---|---|
| Topic / script gốc | Có | Text — chủ đề ngắn HOẶC kịch bản đầy đủ |
| Input images (ảnh demo) | Không | Danh sách file paths — screenshots, demos, GitHub headers |
| Slug | Không | Suy ra từ topic |
| Ngôn ngữ | Không | Mặc định English; "tiếng Việt" thì dùng VN |
| ElevenLabs voice ID | Không | Mặc định voice Hoàng |
| Tổng thời lượng | Không | 60-90s; long form 5-9 phút OK |

## Output

```
workspace/content/<YYYY-MM-DD>/<slug>/
├── design.md                palette + typography source of truth
├── script.md                kịch bản + beat segmentation
├── inputs/                  ảnh user cung cấp
├── images-manifest.json     caption + assignment ảnh vào beat
├── audio/{full.mp3, alignment.json}
├── beats.json               beat → pattern → time range → image
├── assets/{brand/, sfx/}    brand stamp + SFX audio files
├── scenes/scene-NN-*.html   sub-compositions HyperFrames
├── index.html               MASTER composition
└── <slug>.mp4               FILE CUỐI
```

## HARD RULES (NON-NEGOTIABLE)

1. **Fan out parallel LLM sub-agents** — Step 8 spawn 1 sub-agent / scene. Tuyệt đối không dùng Python template generator. ([[feedback_compositions_via_llm_subagents]])
2. **Scene HTML = `<template>` sub-composition** — NO `<html>`, `<head>`, `<body>`, `.stage` wrapper.
3. **GSAP only** — no anime.js. No CSS `animation: ... infinite`. All repeats finite, computed từ DURATION.
4. **Seeded PRNG (mulberry32)** — no `Math.random()`. Mỗi scene 1 seed unique.
5. **Register `window.__timelines["scene-NN-..."] = gsap.timeline({ paused: true })`** — runtime drives playhead.
6. **`gsap.fromTo()` cho entrances** (NOT `gsap.from()` — sub-comps load async).
7. **No exit anims trong scene** (except final scene). Transitions live in MASTER index.html timeline.
8. **Render bằng `npx hyperframes render`**, KHÔNG dùng Playwright per-scene + ffmpeg concat.

Chi tiết anti-patterns: `references/anti-patterns.md`.

## Pipeline overview

```
1.  Lấy topic / script                           (Claude — tự suy, KHÔNG hỏi)
1.5 Phân tích input images (PARALLEL)            (1 Read call / ảnh trong 1 message)
2.  Viết script nếu cần                          (Claude — copywriting principles)
3.  Chia beats + chọn approach                   (1 beat = 1 scene)
3.5 Gán ảnh vào beat                             (match ảnh với context beat)
4.  TTS + alignment (PARALLEL chunks)            (scripts/tts.py)
5.  Map beats → time ranges                      (Claude — dùng alignment.json)
6.  Tạo design.md                                (palette + typography)
7.  Tạo master index.html scaffold               (references/master-scaffold.md)
8.  Fan out N parallel LLM sub-agents            (1 sub-agent / scene, Agent tool)
8.5 Layer SFX vào master                         (references/sfx-layer.md)
9.  Validate (PARALLEL)                          (lint + inspect + validate cùng 1 message)
10. `npx hyperframes render -q standard`
11. Report MP4 path
```

**Bootstrap optimization**: Step 4 (TTS) là network-bound 30-120s. Kick TTS qua `run_in_background: true`, song song viết design.md (Step 6) + master scaffold skeleton (Step 7 phần asset copy + brand stamp). TTS xong mới Step 5 + Step 8.

## Step 1 — Lấy intent (AUTOPILOT, KHÔNG dừng hỏi)

Tự suy ra từ input, KHÔNG hỏi user:
- **Topic**: lấy từ message của user. Nếu user đã có script → skip Step 2.
- **Ngôn ngữ**: mặc định English (match reference aesthetic tốt hơn). VN thì hero text + section labels vẫn có thể English cho đẹp, chỉ VO + captions VN. Chỉ dùng VN khi user nói rõ "tiếng Việt".

Chỉ hỏi 1 câu DUY NHẤT khi không có topic/script nào để bắt đầu.

## Step 1.5 — Phân tích input images (PARALLEL)

Nếu user attach ảnh:

1. Copy vào `workspace/content/<date>/<slug>/inputs/`, kebab-case (`01-repo-homepage.png`)
2. **Parallel Read** — 1 message với N Read calls (Claude native vision đọc ảnh):
   - Sinh caption 1-2 câu
   - Note key visual elements
   - Suy luận placement (beat nào dùng)
3. Lưu `images-manifest.json`:

```json
[{
  "filename": "01-repo-homepage.png",
  "abs_path": "/abs/path/to/inputs/01-repo-homepage.png",
  "caption": "GitHub homepage <repo-name>, 12.4k stars",
  "key_elements": ["star count: 12.4k", "repo name", "tagline"],
  "best_used_when": "Beat introducing the repo"
}]
```

Nếu KHÔNG có ảnh → skip Step 1.5 + 3.5.

## Step 2 — Viết script

Format knowledge-sharing motion-graphic VO:
- Mở đầu: hook stat-driven hoặc statement mạnh
- Thân bài: 3-7 narrative beats, mỗi beat 1 ý chính
- Kết: CTA hoặc takeaway + thương hiệu

Quy tắc:
- Câu ngắn (12-15 từ / câu)
- KHÔNG em dash. Dùng comma / period / "and" (ElevenLabs đọc em dash sai)
- Tránh "I" / "we" trừ closing CTA — narrator khách quan
- Mỗi beat ~6-12s khi đọc (50-100 words)
- Tổng video 60-120s (short) hoặc 5-9 phút (long form)

## Step 3 — Chia beats + chọn approach

Chia script thành N beats (3-16). Mỗi beat: **reuse / adapt / invent**.

Patterns + invention guardrails: `references/scene-patterns.md`.

beats.json schema:

```json
[{
  "index": 1,
  "approach": "reuse|adapt|invent",
  "pattern": "hero",
  "adapt_notes": null,
  "design_brief": null,
  "start_ms": 0,
  "end_ms": 12362,
  "duration_ms": 12362,
  "text": "...",
  "image": null
}]
```

## Step 3.5 — Gán ảnh vào beats (nếu có images)

Đọc `images-manifest.json`. Với mỗi beat:
- Beat cần ảnh không? (stat opener, CTA thường không cần)
- Ảnh nào hợp? (match `best_used_when` với context beat)
- 2 cách dùng ảnh:
  - **A. Image as hero** → pattern `image-feature`, ảnh chiếm canvas
  - **B. Image as thumbnail proof** → ảnh framed nhỏ overlay vào layout motion-graphic. Chi tiết: `references/image-thumbnail-overlay.md`

**Rule of thumb**: max 50% scenes có ảnh — quá nhiều = slideshow. Mix 60/40 motion graphic vs ảnh.

Update `beats.json` thêm field `image`:

```json
{
  "index": 2,
  "pattern": "image-feature",
  "image": {
    "abs_path": "/abs/path/to/inputs/01-repo-homepage.png",
    "caption": "GitHub homepage...",
    "annotations": [{"label": "12.4k stars", "anchor": "top-right"}]
  }
}
```

## Step 4 — TTS + alignment (PARALLEL chunks)

```bash
SLUG=<slug>; DATE=$(date +%Y-%m-%d)
OUT=workspace/content/$DATE/$SLUG
mkdir -p $OUT/audio
python "$(skill_dir)/scripts/tts.py" \
  --script $OUT/script.md \
  --out-audio $OUT/audio/full.mp3 \
  --out-alignment $OUT/audio/alignment.json
```

Env: `ELEVENLABS_API_KEY`. Optional: `ELEVENLABS_VOICE_ID` (default: voice Hoàng).

`tts.py` tự fan out HTTP calls qua `ThreadPoolExecutor(max_workers=4)` — script dài 5-9 phút (5-10 chunks) wall-clock ~30s thay vì ~120s. Order preserved bởi index.

**Background mode**: kick `Bash` với `run_in_background: true` rồi parallel làm Step 6 (design.md) + Step 7 partial (asset copies + scaffold skeleton).

## Step 5 — Map beats → time ranges

Đọc `alignment.json`, match beat với khoảng word → `(start_ms, end_ms, duration_ms)`. Lưu vào `beats.json`.

## Step 6 — Tạo design.md

Source of truth cho palette + typography mà mọi scene phải tôn trọng. Template tối thiểu:

```markdown
# Design — <project>

## Palette
- Background: #050810 (root), #0f1626 (warm center)
- Accents: cyan #4fc3f7, coral #d97757, amber #ffcb6b, sky #7cc4f0
- Lines: rgba(255,255,255,0.07/0.12/0.18)

## Typography
- Sans: Inter 400-900
- Mono: JetBrains Mono 400-700
- Hero: 124px 900 -0.035em uppercase
- Stat: 88px 900 tabular-nums
- Eyebrow/label: 22px 500 mono +0.32em tracking

## Avoidance rules
- No anime.js, no Math.random(), no infinite CSS animations
- No exit fades (except final scene)
- No avatar/footer inside scene HTML — brand stamp ở master index.html
```

Sub-agents BẮT BUỘC đọc file này trước khi viết HTML.

## Step 7 — Master `index.html` scaffold

Chi tiết layer stack + brand stamp + asset copies: `references/master-scaffold.md`.

**Title card 0-5.8s**: nếu có input images, dùng image slider thay vì text centered. Chi tiết: `references/title-card-slider.md`.

**Scene transitions**: master timeline có 3 styles (wipe / push-left / push-up-blur) xoay vòng. Chi tiết: `references/scene-transitions.md`.

## Step 8 — Fan out parallel LLM sub-agents (STEP QUAN TRỌNG)

Spawn N sub-agents trong **1 message** (1 sub-agent / beat) dùng `Agent` tool. Best `subagent_type`: `fullstack-developer`.

### Pre-author scene-01 reference

Trước khi spawn, orchestrator tự viết scene-01 với full structure: template wrapping, scoped CSS, mulberry32 PRNG, particle bokeh, focal glow, meta badge, wordmark, stat cards, count-up, `window.__timelines` registration. Sub-agents copy primitives từ đó.

### Prompt template (mỗi sub-agent)

```
Author HyperFrames sub-composition for scene-NN.

# Files
- OUTPUT (write): <abs path to scenes/scene-NN-slug.html>
- REFERENCE (READ FIRST): <abs path to scenes/scene-01-*.html>
- DESIGN: <abs path to design.md>

# Context
- Composition id: scene-NN-slug
- Duration: <N.NNN> seconds
- Visual continuity with prior scenes — keep the look.

# Hard rules (NON-NEGOTIABLE)
1. Single <template id="scene-NN-slug-template"> containing
   <div data-composition-id="scene-NN-slug" data-width="1920" data-height="1080">.
   NO <html>/<head>/<body>. NO .stage wrapper.
2. <style> and <script> INSIDE the composition div. CSS scoped via
   [data-composition-id="scene-NN-slug"] .your-class.
3. GSAP only. No anime.js. Don't add a <script src=...gsap...> tag —
   master index.html loads GSAP.
4. Seeded mulberry32 PRNG, unique seed (e.g. 0x5cNN). No Math.random().
5. No infinite CSS keyframes — finite GSAP repeats with yoyo, computed
   from DURATION via Math.max(0, Math.ceil(DURATION / cycle) - 1).
6. Use gsap.fromTo() for entrances (NOT gsap.from()).
7. No exit animations. Final state at DURATION must be fully visible.
8. window.__timelines["scene-NN-slug"] = gsap.timeline({ paused: true });
9. All animation completes before DURATION - 0.3s.
10. Particle bokeh field 80-120 dots, seeded positions, finite drift.
11. Meta badge top-left + wordmark top-right (text different per scene).
12. Brand stamp avatar/footer — NEVER inside scene HTML. Master adds it.

# Content brief
<scene-specific content from beat — narrative phasing, key elements,
 visual metaphor, palette accents from design.md>

# Image-feature beats
Nếu beat có image: set <img src="<image.abs_path>"> absolute path,
include caption, add annotation pins nếu có.

# Process
1. Read REFERENCE scene-01 end-to-end.
2. Read design.md for palette + typography.
3. Write the output file.
4. Verify: cd <project> && npx hyperframes lint 2>&1 | tail -10
5. Verify: cd <project> && npx hyperframes inspect --at <t1>,<t2>,<t3> --samples 3 2>&1 | tail -25
   Fix any text_box_overflow on YOUR scene's selectors.
6. Report under 200 words ending with:
   **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
   **Summary:** [1 sentence]
   **Concerns/Blockers:** [if applicable]
```

## Step 8.5 — Layer SFX vào master timeline

SFX library + placement rules + wiring pattern + common mistakes: `references/sfx-layer.md`.

Target density: ~1 SFX / 30-40s. Max 15 hits cho video 8-9 phút.

## Step 9 — Validate (PARALLEL)

Chạy 3 lệnh **trong 1 message** (parallel — đều read-only):

```bash
cd $OUT && npx hyperframes lint
cd $OUT && npx hyperframes inspect --samples 24
cd $OUT && npx hyperframes validate --no-contrast
```

Mọi `text_box_overflow` → giảm `font-size` / thêm `max-width` / `data-layout-allow-overflow` (nếu intentional decorative element animating off-canvas).

Console errors → check asset paths.

## Step 10 — Render

```bash
cd $OUT && npx hyperframes render -q standard -o <slug>.mp4
```

Quality: `draft` (fast), `standard` (default), `high` (slow). Mặc định `standard`.

Render tự compile composition + inline fonts + process audio + capture frames (headless Chromium) + encode H.264 + AAC. Time: ~0.5-2 min per minute of output.

## Step 11 — Report (AUTOPILOT)

KHÔNG mở preview, KHÔNG dừng hỏi — render xong báo cáo và in absolute path MP4 cho user:

```
Render xong: <slug>.mp4 (1920×1080, ~<duration>s)
báo absolute path của file MP4 cho user: /absolute/path/<OUT>/<slug>.mp4
```

Lấy duration bằng `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <slug>.mp4`.
Thiếu info đầu vào (slug, style, số scene) → tự chọn default, không hỏi.

## Pattern decision flow

```
Beat content
   │
   ▼
Beat fit canonical pattern tự nhiên?
   │
   ├── CÓ      → Approach A (reuse). Chọn pattern.
   ├── GẦN ĐÚNG → Approach B (adapt). Ghi twist vào adapt_notes.
   └── KHÔNG   → Approach C (invent). Viết design_brief gồm:
                 - visual element chủ đạo
                 - metaphor (timeline / gauge / map / stack)
                 - entrance choreography
                 - 1-2 accent color từ palette
```

## References

- `references/scene-patterns.md` — 11 canonical patterns + invention guardrails + sub-agent prompt details
- `references/master-scaffold.md` — master index.html layer stack + brand stamp
- `references/title-card-slider.md` — title card image slider (5-6s opener)
- `references/scene-transitions.md` — wipe / push-left / push-up-blur transition library
- `references/sfx-layer.md` — SFX library + placement rules + wiring pattern
- `references/image-thumbnail-overlay.md` — in-scene thumbnail proof pattern (image as thumbnail, not hero)
- `references/anti-patterns.md` — 24 lỗi thường gặp + cách tránh
- `references/elevenlabs-v3.md` — API spec, voice IDs, alignment format
- `scripts/tts.py` — ElevenLabs TTS + alignment (parallel chunks)
- `scripts/prep_avatar.py` — JPG portrait → circular PNG (chạy 1 lần, output dùng chung)

**Reference live project:** `workspace/content/2026-05-28/remotion-vs-hyperframes/` — 16 scenes, 511s, full hyperframes runtime, design.md + scene-01 canonical, title-card image slider, 3-style scene transition library, 15 SFX hits, brand stamp avatar 112px.

---

**Spec version 2.2** — split SKILL.md (867→320 LOC) into references, parallelized TTS chunks, removed dead Playwright+ffmpeg pipeline. Brand stamp avatar 112px. HyperFrames runtime thật + `npx hyperframes render`.
