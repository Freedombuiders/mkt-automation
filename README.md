# HeyGen + HyperFrames Skills Pack

18 Claude Code skills cho pipeline video ngắn: HeyGen avatar lip-sync + HyperFrames compositing.

## Cài đặt

1. Copy thư mục `.claude/` vào project root của bạn (giữ nguyên cấu trúc `.claude/skills/...`).
2. Copy file `.env` vào project root và điền API keys (xem chú thích trong file).
3. Mở Claude Code tại project đó — skills tự động được load.

## Skills bao gồm

**HeyGen**
- `heygen-mp3-to-mp4` — MP3 voiceover → HeyGen avatar lip-sync MP4
- `heygen-script-to-mp4` — script text → HeyGen MP4 (HeyGen TTS)
- `heygen-short-video` — pipeline video ngắn HeyGen
- `heygen-remotion-short-video-editor` — editor Remotion cho clip HeyGen

**HyperFrames core**
- `hyperframes` — authoring composition HTML, captions, transitions, audio-reactive
- `hyperframes-cli` — init / lint / preview / render
- `hyperframes-media` — tts, transcribe, remove-background
- `hyperframes-registry` — registry components

**Pipelines end-to-end**
- `mkt-full-video-with-11-hyperframe-heygen` — script → MP4 9:16 (TikTok/Reels)
- `mkt-full-video-with-11-hyperframe-heygen-16-9` — script → MP4 16:9 (podcast keynote)
- `mkt-hyperframe-knowledge-video` / `-heygen-16-9` / `-heygen-9-16` — knowledge video
- `mkt-hyperframe-talking-head-video` / `-16-9` — đóng gói footage talking-head

**TTS**
- `mkt-minimax-tts-to-mp3` — script text → MP3 bằng MiniMax T2A v2 (thay thế ElevenLabs)
- 2 skill `mkt-hyperframe-knowledge-video-heygen-9-16` / `-16-9` chọn được provider qua
  `TTS_PROVIDER=elevenlabs|minimax` trong `.env` (đường MiniMax cần `pip install -U openai-whisper`
  để dựng alignment word-level)

**Converters**
- `remotion-to-hyperframes`, `website-to-hyperframes`

## Yêu cầu

- Node 20+, Claude Code CLI
- HeyGen API key (Pro plan cho API)
- ElevenLabs API key (voiceover)
- OpenAI API key (Whisper transcribe)
