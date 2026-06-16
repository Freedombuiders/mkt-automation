# mkt-hyperframe-knowledge-video

Skill tạo video chia sẻ kiến thức / tin tức 16:9 (1920×1080) hoàn toàn bằng HyperFrames runtime + ElevenLabs v3 TTS. Output 1 file MP4 ở `workspace/content/<YYYY-MM-DD>/<slug>/<slug>.mp4`.

Style: dark cinematic navy + brand-color particle bokeh + hero uppercase + glassmorphic cards. Lấy cảm hứng từ keynote Google I/O / Apple keynote / Antigravity.

## Quickstart

Trong Claude Code chỉ cần nói:

```
tạo video chia sẻ kiến thức về <topic>
```

hoặc đưa script đầy đủ:

```
tạo video hyperframe từ script này: <script>
```

Skill sẽ tự động:
1. Viết script (hoặc nhận script user đưa) + chia beats
2. ElevenLabs v3 TTS với forced alignment (parallel chunks)
3. Tạo `design.md` + master `index.html` scaffold
4. Fan out parallel LLM sub-agents — mỗi sub-agent author 1 scene HTML dạng `<template>` sub-composition (GSAP only, seeded PRNG)
5. Layer SFX vào master timeline
6. `npx hyperframes lint / inspect / validate` (parallel)
7. `npx hyperframes render` ra MP4 cuối

## One-time setup

### Environment

Thêm vào `.env` của project root:

```bash
ELEVENLABS_API_KEY=sk_xxx                       # bắt buộc
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB        # tùy chọn (mặc định Adam)
ELEVENLABS_MODEL_ID=eleven_v3                   # tùy chọn (mặc định v3)
```

### Deps

```bash
pip install requests Pillow            # Python
npm install -g hyperframes              # CLI
brew install ffmpeg                     # ffprobe cho duration check
```

### Prep brand avatar (chạy 1 lần)

```bash
python agents/videoeditor/.claude/skills/mkt-hyperframe-knowledge-video/scripts/prep_avatar.py \
  --input  workspace/assets/brand/tony-avatar.jpg \
  --output workspace/assets/brand/tony-avatar-circle.png \
  --size 240 --ring 2 --shadow
```

File PNG circular dùng làm brand stamp ở bottom-right mọi video. Tái sử dụng cho mọi video sau.

## Skill structure

```
mkt-hyperframe-knowledge-video/
├── SKILL.md                       entry point cho LLM
├── README.md                      file này
├── references/
│   ├── scene-patterns.md          11 canonical patterns + sub-agent extras
│   ├── master-scaffold.md         master index.html layer stack + brand stamp
│   ├── title-card-slider.md       title card image slider (5-6s opener)
│   ├── scene-transitions.md       wipe / push-left / push-up-blur library
│   ├── sfx-layer.md               SFX library + placement rules + wiring
│   ├── image-thumbnail-overlay.md in-scene thumbnail proof pattern
│   ├── anti-patterns.md           24 lỗi thường gặp + cách tránh
│   └── elevenlabs-v3.md           API spec, voice IDs, alignment format
└── scripts/
    ├── tts.py                     ElevenLabs TTS + alignment (parallel chunks)
    └── prep_avatar.py             JPG portrait → circular PNG
```

## Khi nào skill này TỰ kích hoạt

Khi user nói (VN hoặc EN):
- "tạo video chia sẻ kiến thức về X"
- "tạo video tin tức"
- "knowledge sharing video"
- "news video AI/tech"
- "hyperframe video"
- "video motion graphic 16:9"
- "video về github repo hot"
- "video review tool có ảnh demo"
- "video release notes"
- "video keynote Apple / Google I/O"
- "explainer video AI"

Không tự kích hoạt khi:
- User có footage talking-head → `mkt-hyperframe-talking-head-video-16-9` (16:9) / `mkt-hyperframe-talking-head-video` (9:16)
- Landing page HTML → skill khác
- Carousel ảnh → skill khác

## Giới hạn hiện tại

- Chỉ support 16:9 (1920×1080), chưa làm 9:16
- HyperFrames render time ~0.5-2 phút per minute of output
- ElevenLabs v3 cost ~$0.05 cho 90s script
- Captions tiếng Việt có dấu OK nhưng font hệ thống phải có Inter
- Chưa có background music — chỉ voiceover + SFX

## Spec version

**2.2** — split SKILL.md (867→320 LOC) vào references, parallelized TTS chunks (`ThreadPoolExecutor`), removed dead Playwright + ffmpeg pipeline. Brand stamp avatar 112px. HyperFrames runtime thật + `npx hyperframes render`.
