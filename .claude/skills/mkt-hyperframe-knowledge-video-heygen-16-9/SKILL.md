---
name: mkt-hyperframe-knowledge-video-heygen-16-9
description: Tạo video chia sẻ kiến thức / tin tức 16:9 (1920×1080) dạng "podcast keynote" — slide motion-graphic bên trái (1200×1080) + HeyGen avatar lip-synced floating frame bên phải (540×880 claude-orange border) với SPLIT↔PIP zoom mechanic (slide expand 1920 + avatar shrink 320×420 corner) + breathing + scene-start punch-in. Pipeline 3 phase: (1) TTS parallel chunks + alignment — ElevenLabs v3 (mặc định) hoặc MiniMax speech-02 (chọn qua TTS_PROVIDER=minimax hoặc user nói 'dùng minimax'), (2) delegate `heygen-mp3-to-mp4` lip-sync portrait 720×1280, (3) fan out parallel sub-agents author scene HTML 1200×1080 standalone sub-comp (GSAP only, loaded via `data-composition-src`) → master index.html với slide-mount + #avatar-frame + PIP_EVENTS + SFX → `npx hyperframes render`. **Self-contained: copy templates ở `assets/templates/`, KHÔNG cần đọc folder video khác.** **MUST use this skill when** user nói "video keynote 16:9 có avatar", "podcast keynote video", "slide + avatar lip-sync", "knowledge video heygen", "video kiến thức 16:9 có avatar", "video AI có người dẫn", "talking head + slide", "Claude editorial keynote", "hyperframes heygen 16:9", hoặc video knowledge 16:9 cần avatar HeyGen + slide motion graphic.
---

# HyperFrame Knowledge Video + HeyGen Pipeline (16:9 SPLIT/PIP)

Tạo video chia sẻ kiến thức / tin tức 16:9 (1920×1080) dạng "podcast keynote": slide motion-graphic bên trái + HeyGen avatar lip-synced floating frame bên phải, có SPLIT↔PIP zoom mechanic + breathing + scene-start punch-in. Render bằng `npx hyperframes render`.

**AUTOPILOT (override mọi quy tắc "hỏi user / preview-first"):** Chạy 1 mạch tới MP4, KHÔNG dừng hỏi user, KHÔNG mở preview Studio. Thiếu info (topic, ngôn ngữ, avatar, style, số scene, voice) → tự chọn default và chạy tiếp. Chỉ hỏi 1 câu DUY NHẤT khi thiếu input bắt buộc tuyệt đối (không có topic/script nào để bắt đầu). Render `-q standard` (chất lượng vừa phải) xong báo absolute path MP4 cho user.

## Lessons baked in (v1.1) — chạy thẳng, KHÔNG đọc folder video khác

Skill này **self-contained**. Copy template proven ở `assets/templates/` vào project; ĐỪNG đi đọc folder video khác để lấy ví dụ. 15 fix từ run thật (làm đúng các điều này hoặc sẽ dính lại):

1. **Scene = full standalone HTML doc, load qua `data-composition-src`.** Runtime tự extract element `[data-composition-id]` + scoped `<style>/<script>`. (`<template>` inline là alternative nhưng pipeline này dùng external file — chính là `assets/templates/scene-reference.html`.)
2. **Re-encode HeyGen MP4 keyframe dày TRƯỚC khi render.** HeyGen xuất 25fps, keyframe cách ~8s → renderer warn "sparse keyframes → seek failures / frame freezing". Fix: `scripts/prep_source_video.sh reencode raw.mp4 source.mp4` (libx264 `-r 30 -g 30 -keyint_min 30`). BẮT BUỘC.
3. **HeyGen KHÔNG stuck nếu `failure_code` = null.** Render 110s/720p mất ~10-15 phút. Poll `mcp__heygen__get_video` TRỰC TIẾP; đừng tin sub-agent báo "stuck N phút" — nó bịa elapsed time.
4. **Dùng placeholder source.mp4 để validate trong lúc HeyGen render.** `scripts/prep_source_video.sh placeholder <out>` tạo clip 720×1280 tối + audio thật. Chạy lint + inspect + DRAFT render trên placeholder, extract frame, soi từng scene + PIP. Swap avatar thật rồi render final.
5. **Master brand-mark ở top-left, nên scene meta-badge xuống DƯỚI nó** (top:92px left:56px) và scene KHÔNG có wordmark top-right (chỗ đó avatar ngồi).
6. **PIP re-center, KHÔNG stretch** — vì scene dùng content flex-center intrinsic-width. Khi slide-mount tween về 1920, content chỉ re-center trong pane rộng hơn. Giữ scene content flex-centered; đừng dùng block `width:100%` bên trong.
7. **`#avatar-frame > .avatar-breathing/.avatar-punch` cần `data-layout-allow-overflow`** (breathing scale 1.025 vượt clip; vô hại vì `overflow:hidden` cắt, nhưng inspect flag nếu thiếu attr).
8. **Master CSS select root bằng `#root`, KHÔNG `[data-composition-id="main"]`** (lint: composition_self_attribute_selector).
9. **Thêm `tl.set('#scene-flash'/'#scene-wipe', {opacity:0}, ...)` sau mỗi fade** (lint: gsap_exit_missing_hard_kill — cần cho frame-accurate seeking).
10. **`npx hyperframes lint` CHỈ check index.html, KHÔNG check scene đã mount, và KHÔNG nhận file path đơn** (báo "Not a directory"). Validate scene qua `inspect` (nó render mọi scene mounted) + draft-render frame check.
11. **Sub-agents TUYỆT ĐỐI KHÔNG chạy `npx hyperframes`** — chạy song song + asset chưa có = false error. Chúng chỉ author + self-review; orchestrator validate tập trung.
12. **Warning `google_fonts_import` chấp nhận được** — render env có mạng, fonts load OK (proven). Đừng block vì nó.
13. **Scene-mount KHÔNG overlap/crossfade.** Mount back-to-back; mỗi cái fade-in ở start (DOM sau = nằm trên, che cái trước). (anti-pattern #15 chỉ áp dụng base skill, KHÔNG áp dụng ở đây.)
14. **Set master TOTAL + mọi data-duration = ffprobe duration của source.mp4 ĐÃ re-encode**, không phải alignment.json.
15. **Env cần:** `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `HEYGEN_API_KEY`, `HEYGEN_AVATAR_LOOKS`. (KHÔNG dùng `HEYGEN_VOICE_ID` — ta lip-sync MP3.) System `python3` đã có `requests`; không cần venv.

## Khi nào dùng skill này

User muốn 1 video knowledge / news 16:9 có:
- AI avatar (HeyGen lip-sync từ MP3) thay vì không có người
- Slide motion-graphic bên trái + avatar bên phải (podcast keynote layout)
- Voice ElevenLabs → HeyGen lip-sync
- SPLIT↔PIP zoom moments khi slide cần emphasis full-screen
- Brand mark + SFX layer

KHÔNG dùng skill này khi:
- KHÔNG muốn avatar → `mkt-hyperframe-knowledge-video` (base skill, không HeyGen)
- Footage talking-head thật → `mkt-hyperframe-talking-head-video-16-9`
- 9:16 portrait → `mkt-full-video-with-11-hyperframe-heygen` (sibling)

## Khác biệt với base `mkt-hyperframe-knowledge-video`

| Aspect | Base (no HeyGen) | This skill (HeyGen 16:9) |
|---|---|---|
| Avatar | Static PNG 112px bottom-right (brand stamp) | HeyGen lip-synced MP4, floating frame 540×880 right |
| Scene canvas | 1920×1080 full | **1200×1080 slide pane** (expand 1920 khi PIP) |
| Audio source | `audio/full.mp3` (ElevenLabs only) | `source.mp4` (HeyGen MP4 lip-sync, có cả video+audio) |
| Brand mark | Avatar PNG + handle bottom-right | Text-only `@tranvanhoang.com` top-left |
| Pipeline phases | 1 phase (TTS → scenes → render) | **3 phase**: TTS → HeyGen lip-sync → scenes |
| Zoom mechanic | Crossfade scene transitions | **SPLIT↔PIP zoom** + breathing + punch-in |
| Scene overlap | 0.4s overlap cho crossfade | KHÔNG overlap — slide-mount width tween cho PIP |

## Đầu vào

| Input | Bắt buộc | Format |
|---|---|---|
| Topic / script gốc | Có | Text |
| Input images | Không | Screenshots / demos |
| Slug | Không | Suy ra từ topic |
| Ngôn ngữ | Không | EN default; "tiếng Việt" → VN |
| ElevenLabs voice ID | Không | Default voice Hoàng |
| HeyGen avatar look ID | Không | Random từ `HEYGEN_AVATAR_LOOKS` env |
| Brand accent (claude/chatgpt/gemini) | Không | Default `claude` (orange #d97757) |

## Output

```
workspace/content/<YYYY-MM-DD>/<slug>/
├── design.md                palette + typography source of truth
├── script.md                kịch bản + beat segmentation
├── inputs/                  ảnh user cung cấp
├── images-manifest.json     caption + assignment ảnh vào beat
├── audio/{full.mp3, alignment.json}    TTS Phase 1 (ElevenLabs | MiniMax)
├── source.mp4               HeyGen lip-sync 720×1280 portrait (Phase 2)
├── beats.json               beat → pattern → time range → image
├── pip-schedule.json        PIP_EVENTS (emphasis beats)
├── assets/sfx/              SFX audio files
├── scenes/scene-N-*.html    sub-compositions 1200×1080
├── index.html               MASTER root composition 1920×1080
└── <slug>.mp4               FILE CUỐI
```

## HARD RULES (NON-NEGOTIABLE)

1. **Fan out parallel LLM sub-agents** — Step 8 spawn 1 sub-agent / scene. KHÔNG dùng Python template generator. ([[feedback_compositions_via_llm_subagents]])
2. **Scene HTML = standalone full HTML doc 1200×1080**, load qua `data-composition-src`. Root `<div data-composition-id="scene-N-..." data-width="1200" data-height="1080">`, CSS scoped under `[data-composition-id=...]`. Runtime tự extract element + scoped `<style>/<script>`. (KHÔNG cần `<template>` wrapper — proven full-doc works.)
3. **GSAP only** — no anime.js. No CSS `animation: ... infinite`. All repeats finite. Scene KHÔNG load gsap riêng (dùng global của master).
4. **Seeded PRNG (mulberry32)** — no `Math.random()`. Mỗi scene 1 seed unique.
5. **Register `window.__timelines["scene-N-..."] = gsap.timeline({ paused: true })`**.
6. **`gsap.fromTo()` cho entrances** (NOT `gsap.from()` — sub-comps load async).
7. **No exit anims trong scene** (except final scene). Slide transitions live in MASTER timeline.
8. **HeyGen render 720×1280 portrait** (aspectRatio="9:16" resolution="720p"). KHÔNG landscape 1280×720.
9. **`<video #v-source muted>`** — avoid double-audio. Audio chỉ qua `<audio #a-source>`.
10. **`.slide-mount { width }` KHÔNG `!important`** — GSAP cần animate cho SPLIT↔PIP. Chỉ `!important` ở `> [data-composition-id]`.
11. **Brand mark text-only top-left**, KHÔNG avatar PNG bottom-right (chỗ đó avatar HeyGen ngồi).
12. **Render bằng `npx hyperframes render`**, KHÔNG Playwright + ffmpeg concat.
13. **Re-encode HeyGen MP4 keyframe dày** (`scripts/prep_source_video.sh reencode raw.mp4 source.mp4`) TRƯỚC render — fix sparse-keyframe freeze. Set TOTAL + mọi data-duration = ffprobe của file ĐÃ re-encode.
14. **Scene meta-badge ở top:92px left:56px** (dưới master brand-mark), KHÔNG wordmark top-right (avatar territory). KHÔNG element > x≈1100px.
15. **Sub-agents KHÔNG chạy `npx hyperframes` command** — orchestrator validate tập trung (lint + inspect + draft render).
16. **Master root select bằng `#root`** (không `[data-composition-id="main"]`); `.avatar-breathing/.avatar-punch` có `data-layout-allow-overflow`; thêm `tl.set(opacity:0)` hard-kill sau mỗi wipe/flash fade.

Chi tiết anti-patterns: `references/anti-patterns.md`.

## Pipeline overview

```
Phase 1 ── TTS PARALLEL chunks (ElevenLabs tts.py | MiniMax tts_minimax.py) ──► audio/full.mp3 + alignment.json
Phase 2 ── heygen-mp3-to-mp4 (sub-agent) ─────► source.mp4 (720×1280 portrait)
              │  (background mode — 60-180s)
              │
Phase 3 ── (parallel với Phase 2 background) ─► design.md + master scaffold skeleton + scene-01 reference
       ── (after Phase 2 done) ───────────────► wire <video #v-source> + probe duration
       ── fan out N sub-agents ───────────────► scenes/scene-N.html (1200×1080 sub-comp)
       ── compose pip-schedule ───────────────► pip-schedule.json (emphasis beats)
       ── wire SFX layer + PIP_EVENTS + SCENE_STARTS
       ── lint + inspect + validate (PARALLEL)
       ── npx hyperframes render
```

## Step 0 — Probe project root

```bash
PROJECT_ROOT=$(pwd)
DATE=$(date +%Y-%m-%d)
SLUG=<from topic>
OUT=$PROJECT_ROOT/workspace/content/$DATE/$SLUG
SKILL=<abs path to this skill dir>
mkdir -p $OUT/audio $OUT/inputs $OUT/scenes $OUT/assets/sfx
cp $PROJECT_ROOT/workspace/assets/reels/sfx/*.mp3 $OUT/assets/sfx/ 2>/dev/null || true
# Self-contained scaffolding — copy proven templates (KHÔNG đọc folder video khác)
cp $SKILL/assets/templates/hyperframes.json     $OUT/hyperframes.json
cp $SKILL/assets/templates/package.json         $OUT/package.json   # sửa "name" → slug
cp $SKILL/assets/templates/master-index.reference.html $OUT/index.html   # rồi replace [1]..[8] markers
cp $SKILL/assets/templates/scene-reference.html $OUT/scenes/scene-01-<slug>.html   # adapt content cho beat 1
```

`master-index.reference.html` là master proven (rendered clean). `scene-reference.html` là DNA scene 1200×1080 mọi sub-agent phải mirror. Đây là "code mẫu" duy nhất cần — nằm ngay trong skill.

## Step 1 — Lấy intent (AUTOPILOT, KHÔNG dừng hỏi)

Tự suy ra từ input, KHÔNG hỏi user:
- **Topic**: lấy từ message của user. Nếu user đưa script đầy đủ → skip Step 2.
- **Ngôn ngữ**: default English vì aesthetic match (VN thì hero text vẫn có thể EN cho đẹp). Chỉ dùng VN khi user nói rõ "tiếng Việt".

Chỉ hỏi 1 câu DUY NHẤT khi không có topic/script nào để bắt đầu.

## Step 1.5 — Phân tích input images (PARALLEL)

Nếu user attach ảnh: 1 message với N Read calls (Claude native vision). Sinh caption + key_elements + best_used_when. Lưu `images-manifest.json` (xem base skill format).

Skip nếu không có ảnh.

## Step 2 — Viết script

Format keynote VO:
- Mở: hook stat-driven hoặc statement mạnh
- Thân: 3-7 beats, mỗi beat 1 ý chính
- Kết: CTA / takeaway

Quy tắc:
- Câu ngắn 12-15 từ
- KHÔNG em dash (ElevenLabs đọc sai). Dùng comma / period.
- Mỗi beat ~6-12s khi đọc
- Tổng 60-120s (short) hoặc 5-9 phút (long)

## Step 3 — Chia beats + chọn approach

N beats (3-16). Reuse / adapt / invent. Patterns + invention guardrails: `references/scene-patterns.md`.

beats.json schema giống base skill — thêm field `pip` (boolean / nullable): có là PIP emphasis beat không.

## Step 3.5 — Gán ảnh vào beats (nếu có images)

Logic giống base skill. Pattern A (image-feature) hoặc Pattern B (thumbnail proof — `references/image-thumbnail-overlay.md`). Max 50% scenes có ảnh.

## Step 4 — Phase 1: TTS + alignment (PARALLEL chunks)

Chọn provider trước: (1) user nói rõ ("dùng minimax" / "dùng elevenlabs") → theo user;
(2) không nói → đọc `TTS_PROVIDER` từ `.env` project root (`elevenlabs` | `minimax`);
(3) không có biến → mặc định **elevenlabs**.

**ElevenLabs (mặc định):**

```bash
python "$(skill_dir)/scripts/tts.py" \
  --script $OUT/script.md \
  --out-audio $OUT/audio/full.mp3 \
  --out-alignment $OUT/audio/alignment.json
```

Env: `ELEVENLABS_API_KEY`. `tts.py` tự fan out chunks qua `ThreadPoolExecutor(max_workers=4)` — video 5-9 phút ~30s thay vì ~120s.

**MiniMax:**

```bash
python "$(skill_dir)/scripts/tts_minimax.py" \
  --script $OUT/script.md \
  --out-audio $OUT/audio/full.mp3 \
  --out-alignment $OUT/audio/alignment.json \
  --lang vi
```

Env: `MINIMAX_API_KEY` + `MINIMAX_GROUP_ID` + `MINIMAX_VOICE_ID` (optional:
`MINIMAX_MODEL` default `speech-02-hd`, `MINIMAX_API_BASE` default
`https://api.minimax.io`; account China dùng `https://api.minimaxi.com`).
MiniMax KHÔNG trả word timestamps — script tự transcribe lại MP3 bằng Whisper
local (`pip install -U openai-whisper`) để dựng `alignment.json` cùng format.
Words là Whisper nghe lại nên có thể lệch nhẹ so với script → **anchor trong
beats-spec.json phải là từ thường** (không số, không viết tắt); nếu
`map_beats.py` báo anchor not found → đổi anchor sang cụm khác trong cùng câu.
Output contract giống hệt tts.py — Step 5 trở đi không đổi gì.

## Step 5 — Phase 2: HeyGen lip-sync (BACKGROUND)

**Critical**: kick HeyGen qua sub-agent với `run_in_background: true`, song song chạy Step 6-7 (design.md + scaffold skeleton + scene-01 reference). HeyGen render 60-180s — đừng block.

```
Agent({
  description: "HeyGen lip-sync MP3 → MP4",
  prompt: "Phase 2 — convert <abs path>/audio/full.mp3 to <abs path>/source.mp4
           via heygen-mp3-to-mp4 skill. Output portrait 720×1280, duration must
           match MP3 ±50ms. Report path + duration + avatar_look_id.",
  run_in_background: true,
})
```

Chi tiết MCP OAuth + delegation prompt + resume mode: `references/heygen-integration.md`.

**Reality check (từ run thật):**
- Render 110s/720p mất **~10-15 phút**, KHÔNG phải 60-180s. **KHÔNG block** — chạy Phase 3 setup song song.
- **HeyGen KHÔNG stuck nếu `failure_code` = null.** Poll `mcp__heygen__get_video` TRỰC TIẾP từ orchestrator (đừng tin sub-agent báo "stuck N phút" — nó bịa). Khi `status=completed` → lấy `video_url`, `curl` về `source_heygen_raw.mp4`.
- **Re-encode keyframe dày** ngay sau download (HeyGen = 25fps, keyframe ~8s → freeze):
  ```bash
  bash $SKILL/scripts/prep_source_video.sh reencode $OUT/source_heygen_raw.mp4 $OUT/source.mp4
  ```
- **Trong lúc chờ HeyGen**, tạo placeholder để validate full composition (lint + inspect + draft render):
  ```bash
  bash $SKILL/scripts/prep_source_video.sh placeholder $OUT
  ```
  Swap bằng avatar thật (re-encode) rồi render final.

## Step 5.5 — Map beats → time ranges (deterministic)

Viết `beats-spec.json` (array `{id,slug,pattern,anchor:[words],pip?}`; `anchor` = vài từ đầu mỗi beat, lowercase giữ dấu) rồi:

```bash
python "$SKILL/scripts/map_beats.py" --project $OUT
```

→ ghi `beats.json` (start_ms/end_ms/duration mỗi beat, first beat luôn start=0). In ra context mỗi anchor để verify khớp.

## Step 6 — Tạo design.md (PARALLEL với Phase 2)

Source of truth cho palette + typography. Template:

```markdown
# Design — <project>

## Palette (Modern AI / Claude editorial)
- BG: #000 slide pane, #0a0e18 avatar frame inner
- Modern accents: cyan #67e8f9, violet #a78bfa, pink #f0abfc, lime #a3e635, orange #fb923c, rose #fb7185
- Brand (avatar frame border SPLIT): claude-orange #d97757
- PIP border: violet #a78bfa
- Lines: rgba(255,255,255,0.07/0.12/0.18)

## Typography
- Sans: Inter 400-900
- Mono: JetBrains Mono 400-700
- Hero (slide pane): 80-110px 800 -0.035em (nhỏ hơn base skill 124px vì pane chỉ 1200 wide)
- Stat: 88px 900 tabular-nums
- Eyebrow: JBM 16px 700 +0.22em UPPERCASE

## Avoidance rules
- No anime.js, no Math.random(), no infinite CSS animations
- No exit fades (except final scene)
- Scene canvas 1200×1080 (NOT 1920×1080) — slide pane only
- No brand stamp avatar trong scene HTML — text brand-mark ở master
- KHÔNG embed avatar HeyGen trong scene HTML — root layer only
```

Sub-agents BẮT BUỘC đọc trước khi viết HTML.

## Step 7 — Master scaffold skeleton (PARALLEL với Phase 2)

Skeleton trước (chưa wire `<video>`):
- `<head>` + full CSS từ `references/avatar-pip-layout.md`
- `#slide-bg` + `#heygen-bg`
- `#brand-mark` top-left text
- `#avatar-frame` div empty (sẽ wire `<video>` khi Phase 2 xong)

Chi tiết layer stack + geometry: `references/master-scaffold.md`.

### Step 7.1 — Title card (nếu có input images)

Title card 0-5.8s với image slider — geometry adjust: showcase frame ở SLIDE PANE 1200×1080 (NOT 1920×1080). Slider 800×450 center pane. Chi tiết: `references/title-card-slider.md`.

### Step 7.2 — Scene wipe / flash overlay (chỉ trong slide pane)

Wipe + flash overlay layer ở slide pane (left 1200), KHÔNG full canvas. Khi PIP active, wipe co theo slide-mount width. Chi tiết: `references/scene-transitions.md`.

### Step 7.3 — Compose pip-schedule.json

Sau khi Phase 2 xong + beats.json có time ranges, chọn PIP emphasis events:

```json
{
  "pip_events": [
    {"in": 5.80, "out": 9.20, "beat_index": 1, "reason": "hero stat lock"},
    {"in": 28.80, "out": 33.50, "beat_index": 3, "reason": "premise reveal"}
  ]
}
```

Rules + per-pattern PIP timing: `references/avatar-pip-layout.md` § PIP scheduling.

## Step 8 — Fan out parallel sub-agents (scene HTML 1200×1080)

Spawn N sub-agents trong **1 message** (1 sub-agent / beat). Best `subagent_type`: `fullstack-developer`.

### Pre-author scene-01 reference (orchestrator tự viết)

Scene-01 template wrapping + scoped CSS + mulberry32 PRNG + particle bokeh (NHỚ — chỉ 1200×1080 canvas) + meta badge + window.__timelines registration.

### Prompt template (mỗi sub-agent)

```
Author HyperFrames sub-composition for scene-NN (slide pane 1200×1080).

# Files
- OUTPUT (write): <abs path to scenes/scene-NN-slug.html>
- REFERENCE (READ FIRST): <abs path to scenes/scene-01-*.html>
- DESIGN: <abs path to design.md>

# Context
- Composition id: scene-NN-slug
- Duration: <N.NNN> seconds
- Canvas: 1200×1080 (slide pane, NOT 1920×1080). Will expand to 1920 during PIP via master tween.

# Hard rules (NON-NEGOTIABLE)
1. Full standalone HTML doc (<!doctype html>…) EXACTLY like the REFERENCE.
   Root: <div data-composition-id="scene-NN-slug" data-width="1200" data-height="1080">.
   (Loaded via data-composition-src — full doc is proven; NOT inline <template>.)
2. ALL CSS scoped via [data-composition-id="scene-NN-slug"] .your-class. Inline <style> in <head>.
3. GSAP only. No anime.js. Don't add <script src=...gsap...> (rely on master's global gsap).
4. Seeded mulberry32 PRNG, unique seed (e.g. 0x5cNN). No Math.random().
5. No infinite CSS keyframes — finite GSAP repeats from DURATION.
6. gsap.fromTo() for entrances (NOT gsap.from()).
7. No exit animations. Final state at DURATION fully visible.
8. window.__timelines["scene-NN-slug"] = gsap.timeline({ paused: true });
9. All animation completes before DURATION - 0.3s.
10. Particle bokeh field 60-90 dots (LESS than base skill 80-120 vì canvas hẹp hơn).
11. Hero text 80-110px (NOT 124px — pane 1200 wide).
12. Meta badge top-left at top:92px left:56px (BELOW master brand-mark). NO top-right wordmark (avatar territory).
13. NO brand stamp / avatar / footer trong scene HTML. Master adds at root.
14. KHÔNG layout element ở right edge (>1100px) — sẽ overlap avatar frame khi tween về SPLIT 1200 width. Content flex-CENTERED (để PIP expand re-center sạch, không stretch).

# Content brief
<scene-specific content from beat — narrative, key elements, visual metaphor,
 palette accents from design.md>

# Image-feature beats
Nếu beat có image: set <img src="<image.abs_path>"> absolute path,
include caption, add annotation pins. Image frame max 1080px wide.

# Process
1. Read REFERENCE scene-01 end-to-end.
2. Read design.md for palette + typography.
3. Write the output file.
4. Self-review against the Hard rules. Do NOT run any `npx hyperframes` command
   (concurrent runs + not-yet-present assets cause false errors; orchestrator
   validates centrally via inspect + draft render).
5. Report under 150 words ending with:
   **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
   **Summary:** [1 sentence]
   **Concerns/Blockers:** [if applicable]
```

## Step 8.5 — Wire master timeline + SFX

Sau khi Phase 2 + Step 8 xong, fill master:

1. Wire `<video #v-source>` + `<audio #a-source>` (probe `source.mp4` duration)
2. Wire scene-mount declarations (track-index 40+, data-composition-src, NO overlap)
3. Wire PIP_EVENTS array từ `pip-schedule.json`
4. Wire SCENE_STARTS array từ `beats.json` (cho avatar punch-in)
5. Wire breathing repeat = `Math.ceil(TOTAL / 9) - 1`
6. Wire SFX layer (track 70+) — chi tiết: `references/sfx-layer.md`

GSAP timeline đầy đủ: `references/avatar-pip-layout.md` § GSAP timeline.

## Step 9 — Validate (orchestrator, central)

```bash
cd $OUT && npx --yes hyperframes@0.6.52 lint              # CHỈ check index.html, KHÔNG check scene mounted
cd $OUT && npx --yes hyperframes@0.6.52 inspect --samples 14   # render frame mọi scene → bắt text_box_overflow / container_overflow
```

`lint` KHÔNG nhận file path đơn (báo "Not a directory") và KHÔNG recurse vào scene → muốn validate scene phải dùng `inspect` (nó mount + render thật).

**Bắt buộc: draft render + frame check** (placeholder hoặc avatar thật):
```bash
cd $OUT && npx --yes hyperframes@0.6.52 render -q draft -o _draft.mp4
for t in 6 17 26 40 47 64 82 94 105; do ffmpeg -y -ss $t -i _draft.mp4 -frames:v 1 qa_$t.png; done
```
Read các frame → soi từng scene + PIP. Draft 110s ~75s.

Fix thường gặp:
- `audio_src_not_found: source.mp4` → chưa có source (tạo placeholder hoặc đợi HeyGen).
- `text_box_overflow` → giảm font / max-width / `data-layout-allow-overflow`.
- `container_overflow div.avatar-breathing` → thêm `data-layout-allow-overflow` vào `.avatar-breathing` + `.avatar-punch` (vô hại, breathing scale).
- `composition_self_attribute_selector` → master dùng `#root` thay `[data-composition-id="main"]`.
- `gsap_exit_missing_hard_kill` → thêm `tl.set('#scene-flash'/'#scene-wipe', {opacity:0}, t)` sau fade.
- `google_fonts_import` → warning chấp nhận được (render env có mạng).
- Video warn "sparse keyframes" → re-encode source.mp4 (`prep_source_video.sh reencode`).

## Step 10 — Render

```bash
cd $OUT && npx hyperframes render -q standard -o <slug>.mp4
```

Quality: `draft` / `standard` (default) / `high`.

## Step 11 — Report (AUTOPILOT)

KHÔNG mở preview, KHÔNG dừng hỏi — render xong báo cáo và in absolute path MP4 cho user:

```
Render xong: <slug>.mp4 (1920×1080, ~<duration>s)
Absolute path: /absolute/path/<OUT>/<slug>.mp4
```

Lấy duration bằng `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <slug>.mp4`.
Thiếu info đầu vào (avatar, style, số scene, voice) → tự chọn default, không hỏi.

## References

- `references/avatar-pip-layout.md` — DOM tree, geometry, CSS verbatim, GSAP timeline, PIP scheduling, breathing/punch-in
- `references/heygen-integration.md` — Phase 2 workflow, MCP OAuth, delegation prompt, resume mode
- `references/master-scaffold.md` — layer stack + track-index allocation + scene-mount declarations
- `references/scene-patterns.md` — 11 patterns + invention guardrails (canvas 1200×1080)
- `references/title-card-slider.md` — title card image slider (800×450 showcase trong pane)
- `references/scene-transitions.md` — wipe / push transition library (slide pane only)
- `references/sfx-layer.md` — SFX library + placement rules + wiring
- `references/image-thumbnail-overlay.md` — in-scene thumbnail proof pattern
- `references/anti-patterns.md` — 24 lỗi base + thêm pitfalls của layout SPLIT/PIP
- `references/elevenlabs-v3.md` — Phase 1 API spec
- `scripts/tts.py` — ElevenLabs TTS + alignment (parallel chunks)
- `scripts/tts_minimax.py` — MiniMax speech-02 TTS + Whisper alignment (cùng output contract với tts.py)
- `scripts/map_beats.py` — deterministic beat → time-range (anchor matching) → beats.json
- `scripts/prep_source_video.sh` — placeholder source.mp4 + HeyGen MP4 dense-keyframe re-encode
- `scripts/prep_avatar.py` — JPG portrait → circular PNG (chạy 1 lần)

## Embedded templates (code mẫu duy nhất — KHÔNG đọc folder video khác)

- `assets/templates/master-index.reference.html` — master proven (rendered clean). Copy → `index.html`, replace markers [1]..[8].
- `assets/templates/scene-reference.html` — DNA scene 1200×1080 (hero). Mọi sub-agent mirror cái này.
- `assets/templates/hyperframes.json`, `assets/templates/package.json` — project config.

---

**Spec version 1.1** — fork từ `mkt-hyperframe-knowledge-video` v2.2 + Phase 2 HeyGen + SPLIT↔PIP + scene canvas 1200×1080 + breathing/punch-in.
v1.1 (run thật YC AI Agency Model): self-contained templates in `assets/templates/` (bỏ dependency folder video khác), full-doc scene via data-composition-src, HeyGen re-encode keyframe, placeholder+draft QA workflow, HeyGen polling reality (~10-15min, không stuck nếu failure_code null), meta-badge top:92 / no top-right wordmark, PIP re-center (không stretch), #root selector + hard-kill + data-layout-allow-overflow, lint chỉ check index.html. Xem "Lessons baked in".
