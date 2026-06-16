# mkt-hyperframe-knowledge-video-heygen-16-9

Skill tạo video chia sẻ kiến thức / tin tức 16:9 (1920×1080) dạng **"podcast keynote"** — slide motion-graphic bên trái (1200×1080) + HeyGen avatar lip-synced floating frame bên phải (540×880, claude-orange border) + SPLIT↔PIP zoom mechanic + breathing yoyo + scene-start punch-in. Output `workspace/content/<YYYY-MM-DD>/<slug>/<slug>.mp4`.

Style modern AI / Claude editorial: BG pure black + cyan/violet/pink/lime/orange accents + glassmorphic cards + hero Inter 800.

## Khác biệt với base skill

| Aspect | Base (no HeyGen) | This skill |
|---|---|---|
| Avatar | Static PNG bottom-right | HeyGen lip-synced MP4 floating right |
| Scene canvas | 1920×1080 full | 1200×1080 slide pane (expand 1920 khi PIP) |
| Audio | ElevenLabs MP3 | HeyGen MP4 (video+audio cùng src) |
| Brand mark | Avatar PNG + handle bottom-right | Text-only top-left |
| Pipeline | 1 phase | 3 phase (TTS → HeyGen → scenes) |
| Zoom mechanic | Crossfade transitions | SPLIT↔PIP + breathing + punch-in |

Dùng base `mkt-hyperframe-knowledge-video` nếu KHÔNG cần avatar.

## Quickstart

```
tạo video keynote 16:9 có avatar về <topic>
```

Skill sẽ tự động:
1. Viết script (hoặc nhận user đưa) + chia beats
2. **Phase 1**: TTS (parallel chunks) + alignment — ElevenLabs v3 mặc định, hoặc MiniMax speech-02 (`TTS_PROVIDER=minimax`)
3. **Phase 2**: delegate `heygen-mp3-to-mp4` để lip-sync portrait 720×1280 (background mode, 60-180s)
4. Parallel với Phase 2: tạo `design.md` + master scaffold skeleton + scene-01 reference
5. **Phase 3**: fan out parallel sub-agents — 1 sub-agent / scene (1200×1080 `<template>` sub-comp)
6. Compose `pip-schedule.json` (emphasis beats)
7. Wire master timeline (slide-mount + #avatar-frame + PIP_EVENTS + breathing + punch-in + SFX)
8. `npx hyperframes lint / inspect / validate` (parallel)
9. `npx hyperframes render` ra MP4 cuối

## One-time setup

### Environment

```bash
TTS_PROVIDER=elevenlabs                         # elevenlabs (default) | minimax
ELEVENLABS_API_KEY=sk_xxx                       # bắt buộc Phase 1 nếu provider=elevenlabs
ELEVENLABS_VOICE_ID=K7ewtjKRNtwwt3lKQ6M0        # voice Hoàng
ELEVENLABS_MODEL_ID=eleven_v3
MINIMAX_API_KEY=...                             # bắt buộc Phase 1 nếu provider=minimax
MINIMAX_GROUP_ID=...
MINIMAX_VOICE_ID=...                            # system voice hoặc cloned voice
MINIMAX_MODEL=speech-02-hd                      # optional
MINIMAX_API_BASE=https://api.minimax.io         # optional (China: api.minimaxi.com)
HEYGEN_API_KEY=...                              # bắt buộc Phase 2
HEYGEN_AVATAR_LOOKS=look_id_1,look_id_2         # comma-separated pool
```

Provider MiniMax cần thêm Whisper local cho alignment: `pip install -U openai-whisper`.

Real HeyGen values ở `~/Documents/GitHub/hoang-ai-marketing/.env`.

### Deps

```bash
pip install requests Pillow
npm install -g hyperframes
brew install ffmpeg
```

### HeyGen MCP OAuth (lần đầu mỗi session)

Nếu MCP báo "tool not found" cho `create_video_from_avatar`:
1. Run `mcp__heygen__authenticate` → paste authorize URL cho user
2. User authorize browser → callback → paste lại
3. `mcp__heygen__complete_authentication`
4. Video tools mới load

## Skill structure

```
mkt-hyperframe-knowledge-video-heygen-16-9/
├── SKILL.md                       entry point cho LLM
├── README.md                      file này
├── references/
│   ├── avatar-pip-layout.md       DOM tree, CSS, GSAP timeline, PIP scheduling, breathing/punch-in
│   ├── heygen-integration.md      Phase 2 workflow, MCP, delegation, resume mode
│   ├── master-scaffold.md         layer stack + track-index + scene-mount declarations
│   ├── scene-patterns.md          11 canonical patterns (canvas 1200×1080)
│   ├── title-card-slider.md       title card image slider
│   ├── scene-transitions.md       wipe / push transition library
│   ├── sfx-layer.md               SFX library + placement + wiring
│   ├── image-thumbnail-overlay.md in-scene thumbnail proof pattern
│   ├── anti-patterns.md           lỗi thường gặp
│   ├── elevenlabs-v3.md           Phase 1 API spec
│   └── design-system.md           palette + typography tokens
└── scripts/
    ├── tts.py                     ElevenLabs TTS + alignment (parallel chunks)
    └── prep_avatar.py             JPG portrait → circular PNG (1 lần, output dùng chung)
```

## Khi nào skill này TỰ kích hoạt

Khi user nói (VN hoặc EN):
- "video keynote 16:9 có avatar"
- "podcast keynote video"
- "slide + avatar lip-sync"
- "knowledge video heygen"
- "video kiến thức 16:9 có avatar"
- "video AI có người dẫn"
- "talking head + slide"
- "Claude editorial keynote"
- "hyperframes heygen 16:9"

Không tự kích hoạt khi:
- User KHÔNG muốn avatar → base `mkt-hyperframe-knowledge-video`
- Footage talking-head thật → `mkt-hyperframe-talking-head-video-16-9`
- 9:16 portrait → `mkt-full-video-with-11-hyperframe-heygen` (sibling)

## Giới hạn hiện tại

- Chỉ 16:9 (1920×1080). 9:16 → sibling skill.
- HeyGen render time 60-180s (parallel hóa với scaffold giảm tác động).
- HyperFrames render ~0.5-2 phút per minute of output.
- ElevenLabs ~$0.05 cho 90s, HeyGen ~$0.10-0.30 cho 60s avatar.
- Background music KHÔNG support — chỉ voiceover + SFX.

## Spec version

**1.0** — fork từ `mkt-hyperframe-knowledge-video` v2.2 + Phase 2 HeyGen + SPLIT↔PIP zoom + scene canvas 1200×1080 + breathing/punch-in. Pattern avatar position + claude-orange border tham khảo `mkt-full-video-with-11-hyperframe-heygen-16-9`.
