---
name: mkt-hyperframe-knowledge-video-heygen-9-16
description: Tạo video chia sẻ kiến thức / tin tức 9:16 DỌC (1080×1920) cho TikTok/Reels/Shorts — HeyGen avatar lip-synced FULL-SCREEN khi nói trực tiếp, co xuống BOTTOM HALF (1080×960) khi slide motion-graphic hiện ở TOP HALF, với FULL↔SPLIT breath mechanic (avatar expand full cho punchline cuối mỗi beat) + breathing + scene-start punch-in + captions word-level track 60. Pipeline 3 phase như sibling 16:9: (1) TTS — ElevenLabs v3 (mặc định) hoặc MiniMax speech-02 (chọn qua TTS_PROVIDER=minimax hoặc user nói 'dùng minimax'), (2) heygen-mp3-to-mp4 lip-sync portrait 720×1280 + re-encode keyframe dày, (3) fan out parallel sub-agents author scene HTML 1080×960 standalone sub-comp (GSAP only, data-composition-src) → master index.html với #avatar-stage FULL↔SPLIT + SFX + captions → npx hyperframes render. Self-contained: templates ở assets/templates/. USE WHEN user nói 'video kiến thức 9:16 có avatar', 'knowledge video dọc heygen', 'tiktok keynote avatar', 'video dọc slide + avatar', 'avatar full screen và nửa màn hình', 'heygen full + split 9:16', 'video kiến thức tiktok có người dẫn', 'hyperframes heygen 9:16', 'slide trên avatar dưới', hoặc video knowledge 9:16 cần avatar HeyGen + slide motion graphic. KHÁC sibling 16-9 (avatar floating frame phải + SPLIT↔PIP) và KHÁC mkt-hyperframe-talking-head-video (dùng footage quay sẵn, infographic generator Python).
---

# HyperFrame Knowledge Video + HeyGen Pipeline (9:16 FULL↔SPLIT)

Tạo video chia sẻ kiến thức 9:16 dọc (1080×1920) cho TikTok/Reels: HeyGen avatar lip-synced **full-screen** khi nói trực tiếp, **co xuống bottom half** khi slide motion-graphic chiếm top half, expand lại full cho punchline ("breath"). Captions word-level luôn hiển thị. Render bằng `npx hyperframes render`.

**AUTOPILOT (override mọi quy tắc "hỏi user / preview-first"):** Chạy 1 mạch tới MP4, KHÔNG dừng hỏi, KHÔNG mở preview Studio. Thiếu info → tự chọn default. Render `-q standard` xong báo absolute path MP4 cho user.

## Khi nào dùng skill này

- Video knowledge/news **9:16 dọc** có AI avatar (HeyGen lip-sync từ MP3)
- Phối hợp avatar **full-screen** (nói trực tiếp) và avatar **1/2 dưới** + slide 1/2 trên
- Cần captions (TikTok xem không bật tiếng)

KHÔNG dùng khi:
- 16:9 ngang → sibling `mkt-hyperframe-knowledge-video-heygen-16-9`
- Footage talking-head quay sẵn + infographic template Python → `mkt-hyperframe-talking-head-video`
- Không cần avatar → `mkt-hyperframe-knowledge-video`

## Khác biệt với sibling 16:9

| Aspect | 16:9 sibling | Skill này (9:16) |
|---|---|---|
| Canvas | 1920×1080 | **1080×1920** |
| Avatar | Floating frame 540×880 bên phải, viền orange | **Full-screen**, không frame |
| Zoom mechanic | SPLIT↔PIP (avatar thu về corner) | **FULL↔SPLIT** (avatar co xuống bottom half) |
| Scene canvas | 1200×1080 (pane trái) | **1080×960 (top half)** |
| Scene mount window | start → end | **start → brollEnd** (mount hết = avatar expand) |
| Captions | KHÔNG (avatar voice là spine) | **CÓ** — word-level, track 60, bottom anim 160↔920 |
| Hero font | 80-110px | **64-84px** (pane ngắn 960px) |

## HARD RULES (NON-NEGOTIABLE)

1. **Fan out parallel LLM sub-agents** — 1 sub-agent / scene. KHÔNG dùng Python template generator. ([[feedback_compositions_via_llm_subagents]])
2. **Scene HTML = standalone full HTML doc 1080×960**, load qua `data-composition-src`. Root `<div data-composition-id="scene-NN-slug" data-width="1080" data-height="960">`, CSS scoped.
3. **GSAP only**, no anime.js, no infinite CSS animations, scene KHÔNG load gsap riêng.
4. **Seeded mulberry32 PRNG** (seed 0x5cNN unique/scene). No `Math.random()`.
5. **`window.__timelines["scene-NN-slug"] = gsap.timeline({ paused: true })`**, entrances bằng `gsap.fromTo()`, no exit anims.
6. **Scene mount `data-duration = brollEnd - start`** — mount kết thúc tại brollEnd để avatar expand full (breath). Scene DURATION nội bộ cũng = mount window đó.
7. **3 giây đầu LUÔN full face** — không mount scene đè mặt lúc mở video.
8. **HeyGen render 720×1280 portrait** (aspectRatio="9:16"), re-encode keyframe dày bằng `scripts/prep_source_video.sh reencode` TRƯỚC khi render. TOTAL + mọi data-duration = ffprobe của file ĐÃ re-encode.
9. **`<video #v-source muted>`**, audio chỉ qua `<audio #a-source>`.
10. **Root `#root` PHẢI có `data-duration`** + mọi ambient loop tính repeat từ TOTAL — loop dư kéo dài MP4 (bug đã gặp: repeat:60 → video 60s render thành 88s).
11. **Captions mount CUỐI, track 60, `style="z-index:100"`**; `.caption-stage` dùng `left:0;right:0;bottom:<px>;text-align:center` — KHÔNG transform centering. Timing từ word-level transcript, KHÔNG hand-edit.
12. **Scene canvas ngắn (960px)**: hero 64-84px, KHÔNG element dưới y≈900px. Meta-badge top:92px left:48px. Content flex-centered.
13. **Sub-agents KHÔNG chạy `npx hyperframes`** — orchestrator validate tập trung (lint + inspect + draft render + frame QA).
14. **Master select bằng `#root`**; `.avatar-breathing/.avatar-punch` có `data-layout-allow-overflow`; `tl.set(opacity:0)` hard-kill sau mỗi wipe/flash/divider fade.
15. **Whisper LUÔN `--language vi`** cho audio Việt, không bao giờ model `.en`.

Chi tiết anti-patterns chung: `references/anti-patterns.md`. Layout chi tiết: `references/full-split-layout.md`.

## Pipeline overview

```
Phase 1 ── TTS (ElevenLabs scripts/tts.py | MiniMax scripts/tts_minimax.py) ──► audio/full.mp3 + alignment.json
Phase 2 ── heygen-mp3-to-mp4 (sub-agent, background) ─────────► source_heygen_raw.mp4
              └─ prep_source_video.sh reencode ───────────────► source.mp4 (dense keyframes)
Phase 3 ── design.md + beats.json + master scaffold (song song Phase 2)
       ── transcribe + clean + captions (cần source.mp4)
       ── fan out N sub-agents ──────────────────────────────► scenes/scene-N.html (1080×960)
       ── wire master: mounts (start→brollEnd) + SCENES[] + SFX + captions
       ── lint + inspect + draft render + frame QA
       ── npx hyperframes render -q standard ────────────────► <slug>.mp4
```

**Resume mode:** nếu `audio/full.mp3` + `source.mp4` (hoặc từ project khác) đã tồn tại → skip Phase 1+2, re-encode nếu chưa, vào thẳng Phase 3.

## Step 0 — Scaffold project

```bash
PROJECT_ROOT=$(pwd)
OUT=$PROJECT_ROOT/workspace/content/$(date +%Y-%m-%d)/<slug>
SKILL=<abs path to this skill dir>
mkdir -p $OUT/audio $OUT/scenes $OUT/assets/sfx $OUT/compositions
cp $SKILL/assets/templates/hyperframes.json $OUT/
cp $SKILL/assets/templates/package.json $OUT/          # sửa "name" → slug
cp $SKILL/assets/templates/master-index.reference.html $OUT/index.html   # replace markers [1]..[8]
cp $SKILL/assets/templates/captions.html.template $OUT/compositions/captions.html
# SFX: copy từ mkt-hyperframe-talking-head-video/assets/sfx/ (6 file chuẩn)
```

## Step 1-4 — Script, beats, TTS (giống sibling 16:9)

- Script: hook mạnh → 3-7 beats → CTA. Câu ngắn, KHÔNG em dash. ~60-120s.
- `beats.json`: mỗi beat `{id, slug, start, end, brollEnd, hasBreath, summary}`.
  `brollEnd = end - 1.5` mặc định. **Beat hook PHẢI có scene visual** (user feedback
  10/06/2026: "trong 3-5s đầu phải chuyển sang cảnh visual hyperframe rồi") —
  mount scene-00-hook từ giây ~4.0 (0-3s full face), brollEnd = beat2.start - 1.5.
  Nội dung scene hook: brand title slam + stat lock mạnh nhất của video.
- TTS — chọn provider trước khi chạy (xem "TTS provider" bên dưới):
  - **ElevenLabs (mặc định)**: `python $SKILL/scripts/tts.py --script script.md
    --out-audio audio/full.mp3 --out-alignment audio/alignment.json`
    (cần `ELEVENLABS_API_KEY`).
  - **MiniMax**: `python $SKILL/scripts/tts_minimax.py --script script.md
    --out-audio audio/full.mp3 --out-alignment audio/alignment.json --lang vi`
    (cần `MINIMAX_API_KEY` + `MINIMAX_GROUP_ID` + `MINIMAX_VOICE_ID`).
  Map beats: `scripts/map_beats.py` — chạy giống nhau cho cả 2 provider.

### TTS provider (ElevenLabs | MiniMax)

Quy tắc chọn:
1. User nói rõ ("dùng minimax", "giọng minimax", "dùng elevenlabs") → theo user.
2. Không nói → đọc `TTS_PROVIDER` từ `.env` project root (`elevenlabs` | `minimax`).
3. Không có biến → mặc định **elevenlabs**.

Khác biệt cần biết khi dùng MiniMax:
- MiniMax KHÔNG trả word timestamps — `tts_minimax.py` tự transcribe lại MP3 bằng
  Whisper local (`--language vi`, cần `pip install -U openai-whisper`) để dựng
  `alignment.json` cùng format. Words là kết quả Whisper nghe lại, có thể lệch nhẹ
  so với script → **anchor trong beats-spec.json phải là từ thường** (không số,
  không viết tắt, không tên riêng khó). Nếu `map_beats.py` báo anchor not found →
  đổi anchor sang cụm từ khác trong cùng câu, đừng sửa alignment.json bằng tay.
- Env: `MINIMAX_MODEL` (default `speech-02-hd`), `MINIMAX_API_BASE`
  (default `https://api.minimax.io`; account China: `https://api.minimaxi.com`).
- Output contract giống hệt tts.py (`full.mp3` + `alignment.json`) — Phase 2/3
  không đổi gì.

## Step 5 — Phase 2: HeyGen (background) + re-encode

Delegate skill `heygen-mp3-to-mp4` qua sub-agent `run_in_background: true` (portrait 720×1280). Poll `mcp__heygen__get_video` TRỰC TIẾP (render thật mất 10-15 phút, KHÔNG stuck nếu failure_code=null). Download xong:

```bash
bash $SKILL/scripts/prep_source_video.sh reencode $OUT/source_heygen_raw.mp4 $OUT/source.mp4
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $OUT/source.mp4  # → TOTAL
```

Trong lúc chờ: `prep_source_video.sh placeholder $OUT` để validate sớm.

## Step 6 — Captions

```bash
cd $OUT && npx hyperframes transcribe source.mp4 --model medium --language vi
python3 $SKILL/scripts/clean_transcript.py transcript.json          # → caption-groups.json
python3 $SKILL/scripts/fix_caption_typos.py caption-groups.json script.txt
# soi suspicious tokens → sửa text-only (KHÔNG sửa timing)
python3 $SKILL/scripts/inject_captions.py compositions/captions.html caption-groups.json
```

## Step 7 — Master wiring

Từ template `master-index.reference.html`, replace markers [1]..[8]:
- [2]+[8]: TOTAL = ffprobe source.mp4 đã re-encode
- [4]: mounts `data-start = beat.start`, `data-duration = brollEnd - start`, track 40+
- [6]: `SCENES = [{start, brollEnd, hasBreath}]`
- [7]: `SCENE_STARTS` (punch-in)
- [3]/[5]: SFX + transitions (xem `references/sfx-layer.md`)

Geometry + editorial rules FULL vs SPLIT: `references/full-split-layout.md`.

## Step 8 — Fan out sub-agents (scene HTML 1080×960)

Spawn N sub-agents trong **1 message**. Prompt template (per scene):

```
Author HyperFrames sub-composition for scene-NN (TOP pane 1080×960).
# Files
- OUTPUT: <abs>/scenes/scene-NN-slug.html
- REFERENCE (READ FIRST): $SKILL/assets/templates/scene-reference.html
- DESIGN: <abs>/design.md
# Context
- Composition id: scene-NN-slug · Duration: <brollEnd - start> s
- Canvas 1080×960 — TOP HALF; HeyGen avatar chiếm bottom half (master lo split).
# Hard rules: (copy 15 rules từ SKILL.md, đổi kích thước: hero 64-84px,
  meta-badge top:92 left:48, no element below y≈900, seed 0x5cNN,
  bokeh 50-70 dots, content flex-centered)
# Content brief: <beat summary + voiceover đoạn đó + accent colors>
# Process: Read reference → design.md → write → self-review → KHÔNG chạy npx hyperframes
  → report <150 words, Status: DONE/DONE_WITH_CONCERNS/BLOCKED
```

## Step 9 — Validate (orchestrator, central)

```bash
cd $OUT && npx hyperframes lint                  # 0 errors yêu cầu; google_fonts warning OK
cd $OUT && npx hyperframes inspect --samples 14  # bắt overflow mọi scene
npx hyperframes render -q draft -o _draft.mp4
for t in <sample times>; do ffmpeg -y -ss $t -i _draft.mp4 -frames:v 1 qa_$t.png; done
# Read các frame: soi FULL↔SPLIT đúng moment, captions vị trí đúng cả 2 mode,
# 3s đầu full face, scene không tràn xuống divider
```

Fix thường gặp: như sibling 16:9 (`gsap_exit_missing_hard_kill` → thêm `tl.set`,
`container_overflow .avatar-breathing` → `data-layout-allow-overflow`,
overflow text → giảm font, sparse keyframes → re-encode).

## Step 10-11 — Render (AUTOPILOT)

```bash
cd $OUT && rm -f _draft.mp4 qa_*.png && npx hyperframes render -q standard -o <slug>.mp4
ffprobe ... # verify duration == TOTAL ±0.1s và 1080×1920 — nếu dài hơn: tìm GSAP loop dư
```

```
Render xong: <slug>.mp4 (1080×1920, ~<duration>s)
```

Báo absolute path của file MP4 cho user + size. Log hive_mind sau khi xong.

## Quality Criteria

- 3s đầu full face, không scene đè mặt
- FULL↔SPLIT transition mượt (0.45s power2.inOut), divider chỉ hiện khi SPLIT
- Mỗi beat có breath (avatar full ~1.5s punchline) trước beat kế
- Captions sync word-level, đổi vị trí đúng theo mode, không bị scene che
- Render duration == TOTAL (không đuôi thừa do loop dư)
- Scene hero ≤84px, không element dưới y≈900

## References & Scripts

- `references/full-split-layout.md` — geometry + master JS + editorial rules (ĐỌC khi wire master)
- `references/scene-patterns.md`, `references/sfx-layer.md`, `references/anti-patterns.md`, `references/design-system.md`, `references/heygen-integration.md`, `references/elevenlabs-v3.md`, `references/image-thumbnail-overlay.md` — kế thừa từ sibling 16:9 (aspect-agnostic)
- `scripts/tts.py`, `scripts/map_beats.py`, `scripts/prep_source_video.sh`, `scripts/prep_avatar.py` — như sibling
- `scripts/clean_transcript.py`, `scripts/fix_caption_typos.py`, `scripts/inject_captions.py` — captions pipeline (từ talking-head skill)
- `assets/templates/master-index.reference.html` — master 9:16 FULL↔SPLIT (markers [1]..[8])
- `assets/templates/scene-reference.html` — DNA scene 1080×960
- `assets/templates/captions.html.template` — captions sub-comp proven

---

**Spec version 1.0** — fork từ `mkt-hyperframe-knowledge-video-heygen-16-9` v1.1, đổi SPLIT↔PIP → FULL↔SPLIT cho 9:16, scene canvas 1080×960, thêm captions layer, mount window start→brollEnd, bake lesson "root data-duration + finite loops" (bug video 60s render 88s).
