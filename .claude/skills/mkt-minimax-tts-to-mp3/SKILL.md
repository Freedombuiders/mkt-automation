---
name: mkt-minimax-tts-to-mp3
description: "Convert Vietnamese/English script text to MP3 voiceover using MiniMax T2A v2 API (speech-02). Drop-in alternative to mkt-elevenlabs-tts-to-mp3 — same input (script text) and output (MP3 file) contract, so downstream skills (heygen-mp3-to-mp4, mkt-full-video-with-11-hyperframe-heygen*) work unchanged. Reads MINIMAX_API_KEY, MINIMAX_GROUP_ID, MINIMAX_VOICE_ID from .env. USE WHEN user says 'tạo mp3 minimax', 'minimax tts', 'tạo voiceover minimax', 'text to speech minimax', 'đọc text bằng minimax', 'giọng minimax', 'hailuo voice', 'minimax script to mp3', or wants a voiceover MP3 and MiniMax is the chosen TTS provider."
---

# MiniMax TTS → MP3

Chuyển script text thành file MP3 voiceover bằng MiniMax T2A v2 (`speech-02-hd` /
`speech-02-turbo`). Output là MP3 chuẩn, dùng tiếp được cho `heygen-mp3-to-mp4`
và các pipeline `mkt-full-video-with-11-hyperframe-heygen*` (thay thế Phase 1
ElevenLabs).

## Env vars (đọc từ `.env` ở project root)

```bash
MINIMAX_API_KEY=        # bắt buộc — https://platform.minimax.io
MINIMAX_GROUP_ID=       # bắt buộc — GroupId của account
MINIMAX_VOICE_ID=       # bắt buộc — system voice hoặc cloned voice id
MINIMAX_MODEL=          # optional — mặc định speech-02-hd (chậm, chất lượng cao);
                        # dùng speech-02-turbo nếu cần nhanh/rẻ
MINIMAX_API_BASE=       # optional — mặc định https://api.minimax.io
                        # (account China dùng https://api.minimaxi.com)
```

## Workflow

1. **Lấy script**: user đưa text trực tiếp hoặc đường dẫn file. Nếu script dài
   hơn ~10.000 ký tự, chia nhỏ theo đoạn và gọi nhiều lần, sau đó nối bằng
   ffmpeg (`concat` demuxer).

2. **Chạy helper script** (nằm trong `scripts/` của skill này):

   ```bash
   python3 <skill_dir>/scripts/minimax_tts.py \
     --text-file /path/to/script.txt \
     --out /path/to/voiceover.mp3
   ```

   Tham số optional: `--voice-id <id>` (override env), `--model speech-02-turbo`,
   `--speed 1.1` (0.5–2.0).

   Script tự load `.env` từ thư mục hiện hành, gọi `POST /v1/t2a_v2?GroupId=...`,
   decode hex audio trong JSON response và ghi MP3. Stdout là JSON một dòng:
   `{out, bytes, duration_ms, usage_characters, voice_id, model}`.

3. **Validate output**: kiểm tra file tồn tại và `duration_ms` hợp lý so với độ
   dài script (~150 từ/phút tiếng Việt). Nghe thử nếu user yêu cầu — gửi file
   cho user duyệt trước khi đưa vào bước HeyGen.

4. **Báo kết quả**: đường dẫn MP3 + duration + số ký tự đã dùng (tính phí theo
   ký tự).

## Lỗi thường gặp

| Lỗi | Nguyên nhân / xử lý |
|-----|---------------------|
| `status_code 1004` | API key sai hoặc hết hạn — kiểm tra `MINIMAX_API_KEY` |
| `status_code 2013` | Voice id không tồn tại với account này — kiểm tra `MINIMAX_VOICE_ID` |
| `invalid GroupId` | `MINIMAX_GROUP_ID` sai — lấy lại từ platform.minimax.io account settings |
| Response không có `data.audio` | In nguyên payload ra để debug; thường do text rỗng hoặc model name sai |
| Tiếng Việt đọc sai | Thử `speech-02-hd` thay vì turbo; viết số/từ viết tắt thành chữ đầy đủ trong script |

## Ghi chú

- MiniMax trả audio dạng **hex string trong JSON** (non-streaming) — không phải
  bytes trực tiếp như ElevenLabs. Helper script đã xử lý, đừng tự curl rồi ghi
  thẳng response ra file.
- Voice cloning: tạo cloned voice trên platform.minimax.io rồi dùng voice id đó
  trong `MINIMAX_VOICE_ID` — giống pattern brand voice của ElevenLabs.
- Contract giống `mkt-elevenlabs-tts-to-mp3`: text in → MP3 out. Khi pipeline
  cha (`mkt-full-video-with-11-hyperframe-heygen*`) gọi Phase 1, có thể dùng
  skill này thay thế mà không đổi gì ở Phase 2/3.
