---
name: mkt-blotato-publish-social
description: >-
  Đăng content (MP4 video, ảnh, text) lên nhiều nền tảng social cùng lúc qua
  Blotato API — Facebook Page (feed/reel/story), TikTok, Instagram, YouTube,
  Threads, X/Twitter, LinkedIn. Upload media local lên Blotato (presigned),
  publish per-platform, poll tới khi có public URL. USE WHEN user nói "đăng
  video lên fanpage", "post lên tiktok", "đăng đa nền tảng", "publish lên
  facebook và tiktok", "blotato", "đăng reel", "phân phối video lên social",
  "đăng mp4 vừa render lên fb", "share video lên các kênh", hoặc sau khi một
  video skill render xong MP4 và user muốn đăng nó lên mạng xã hội.
---

# Blotato Multi-Platform Publisher

Đăng 1 content lên nhiều nền tảng qua [Blotato](https://blotato.com) bằng helper
script `scripts/blotato_publish.py` (python3 stdlib, không cần pip).

## Prerequisites

- `BLOTATO_API_KEY` trong `.env` ở project root (script tự walk-up tìm). Đã set sẵn.
- Tài khoản social phải được kết nối trước trong Blotato dashboard
  (https://my.blotato.com → Accounts). API **không** kết nối account mới được.

## ⚠️ RÀNG BUỘC: CHỈ ĐĂNG LÊN "Tony Hoàng Learn AI Automation"

CHỈ được publish lên đúng 1 đích:

| Platform | accountId | pageId | Tên |
|---|---|---|---|
| facebook (Hoang Tran) | `30606` | `704841222706761` | **Tony Hoàng Learn AI Automation** ← ĐÍCH DUY NHẤT |

- KHÔNG đăng lên bất kỳ page/account nào khác (Prediction 3D, BIM Speed, Feroz Ahmed,
  Instagram tradewizeadmin, TikTok, v.v.) trừ khi user yêu cầu rõ ràng và đổi ý.
- Mọi lệnh `publish` mặc định `--account-id 30606 --page-id 704841222706761`.
- Account khác có thể xuất hiện khi chạy `accounts` — bỏ qua, đừng đăng lên chúng.

```bash
SKILL_DIR="$(pwd)/.claude/skills/mkt-blotato-publish-social"
python3 "$SKILL_DIR/scripts/blotato_publish.py" accounts
```

## Workflow

### Bước 0 — Có MP4 chưa?
Nếu user muốn "tạo video rồi đăng": chạy video skill phù hợp trước
(`mkt-hyperframe-*`, `mkt-full-video-*`) ra MP4, rồi quay lại đây.

### Bước 1 — Viết caption per-platform (đừng dùng 1 caption cho mọi nền tảng)
- **Facebook**: caption dài hơn, hook dòng đầu, 3-5 hashtag cuối, tiếng Việt tự nhiên.
- **TikTok**: `--text` ngắn + hashtags; `--title` ≤ 90 ký tự (hook chính).
- Tự viết từ nội dung video nếu user không đưa caption. Không hỏi lại.

### Bước 2 — Publish (script tự upload media local qua presigned flow)

Facebook Reel lên fanpage mặc định:
```bash
python3 "$SKILL_DIR/scripts/blotato_publish.py" publish \
  --platform facebook --account-id 30606 --page-id 704841222706761 \
  --fb-media-type reel \
  --media /absolute/path/video.mp4 \
  --text "Caption tiếng Việt ở đây..." \
  --wait 300
```
- Bỏ `--fb-media-type` → post feed thường. `story` cũng hợp lệ.

TikTok (sau khi đã kết nối, lấy accountId từ `accounts`):
```bash
python3 "$SKILL_DIR/scripts/blotato_publish.py" publish \
  --platform tiktok --account-id <TIKTOK_ACCOUNT_ID> \
  --media /absolute/path/video.mp4 \
  --text "Caption + #hashtags" --title "Hook ngắn ≤90 ký tự" \
  --wait 300
```
- Video HeyGen/AI mặc định được gắn nhãn AI (`isAiGenerated: true`). Chỉ thêm
  `--no-ai-label` khi video là footage quay thật.
- Privacy mặc định `PUBLIC_TO_EVERYONE`; test thì dùng `--tiktok-privacy SELF_ONLY`.

Đăng cùng 1 video lên nhiều nền tảng: **upload 1 lần, tái dùng URL** —
```bash
BLOTATO_URL=$(python3 "$SKILL_DIR/scripts/blotato_publish.py" upload /absolute/path/video.mp4)
# rồi publish nhiều lần với --media "$BLOTATO_URL" (script nhận diện URL blotato, không upload lại)
```

Lên lịch thay vì đăng ngay: thêm `--scheduled-time 2026-06-11T09:00:00Z` (UTC; giờ VN = UTC+7).

### Bước 3 — Verify + báo cáo
- `--wait` đã poll sẵn: exit 0 + JSON có `publicUrl` = published; exit 2 = failed
  (đọc `errorMessage`, fix rồi thử lại — lỗi thường gặp: video quá dài/quá nặng
  cho platform, thiếu quyền page).
- Check lại sau: `python3 .../blotato_publish.py status <postSubmissionId>`
- Báo cáo cho user: mỗi platform 1 dòng — tên page/kênh + public URL (hoặc lý do fail).
- Log hive mind (action `published_social`) theo quy tắc agent.

## Gotchas

- `mediaUrls` phải là URL thuộc domain blotato — script tự lo việc này, đừng đưa
  thẳng URL ngoài vào content khi tự gọi API tay.
- Rate limit: 30 posts/phút, 120 presigned uploads/phút.
- TikTok bắt buộc đủ bộ flags (privacy/duet/stitch/AI) — script đã set default đúng.
- `presignedUrl` hết hạn nhanh — script PUT ngay sau khi tạo, đừng tách 2 bước thủ công.
- Nền tảng chưa kết nối → API trả lỗi account không tồn tại: nhắc user vào
  my.blotato.com kết nối, KHÔNG tự retry vô ích.
- MP4 > giới hạn plan của Blotato → upload fail; báo size + path cho user.
