# HeyGen Integration — Phase 2 (MP3 → lip-sync MP4)

Sau khi ElevenLabs TTS xong (`audio/full.mp3` + `audio/alignment.json`), Phase 2 push MP3 lên HeyGen → nhận MP4 portrait 720×1280 với avatar lip-synced. MP4 đó nguồn cho `<video #v-source>` + `<audio #a-source>` ở master `index.html`.

## Delegation strategy — KHÔNG re-implement

Skill `heygen-mp3-to-mp4` đã handle toàn bộ:
- Upload MP3 lên HeyGen Assets (REST helper script, vì post-2026 MCP bỏ upload tool)
- Create video từ avatar look + uploaded audio (HeyGen MCP `create_video_from_avatar`)
- Poll status (HeyGen MCP `get_video`)
- Download final MP4

Orchestrator skill này **delegate qua sub-agent** với prompt scoped chỉ để chạy Phase 2 — không spawn tool calls inline.

## Env requirements

```bash
HEYGEN_API_KEY=...                   # bắt buộc cho REST upload
HEYGEN_AVATAR_LOOKS=look_id_1,look_id_2,...   # comma-separated, pick random
```

Real values ở `~/Documents/GitHub/hoang-ai-marketing/.env`. `.env.local` của project ship với stub.

## Output format

| File | Spec |
|---|---|
| `source.mp4` | 720×1280 portrait, H.264, lip-synced |
| Duration | Khớp `full.mp3` ±50ms |

**Critical: render HeyGen ở 720×1280 portrait, KHÔNG 1280×720 landscape.** Avatar frame layout (540×880 SPLIT / 320×420 PIP) cả 2 đều closer to portrait. Portrait source có headroom đủ để `object-fit: cover; object-position: center 25%` crop sạch. Landscape source → 2 dải đen hoặc face quá nhỏ.

## Re-encode keyframe dày (REQUIRED — v1.1)

HeyGen MP4 download về là **25fps, keyframe cách ~8s**. HyperFrames renderer seek per-frame → warn `"Video has sparse keyframes (max interval: 8.33s). This causes seek failures and frame freezing"` và avatar bị đơ frame. **LUÔN re-encode** trước khi wire vào master:

```bash
bash $SKILL/scripts/prep_source_video.sh reencode $OUT/source_heygen_raw.mp4 $OUT/source.mp4
# = ffmpeg -i raw.mp4 -c:v libx264 -r 30 -g 30 -keyint_min 30 -pix_fmt yuv420p -movflags +faststart -c:a aac source.mp4
```

Set master TOTAL + mọi `data-duration` = ffprobe của `source.mp4` ĐÃ re-encode.

## Polling (orchestrator — đừng tin sub-agent)

Render 110s/720p mất **~10-15 phút** (KHÔNG phải 60-180s). HeyGen **KHÔNG stuck nếu `failure_code` = null** — chỉ đang queue. Orchestrator poll TRỰC TIẾP:

```
mcp__heygen__get_video(videoId) → status: processing | completed | failed
```

Khi `completed` → lấy `video_url`, `curl -fsSL "$URL" -o source_heygen_raw.mp4`, rồi re-encode. **Đừng tin sub-agent báo "stuck N phút"** — chúng bịa elapsed time (run thật: sub-agent báo "stuck 85 phút" trong khi render xong sau ~13 phút).

## Validate composition trong lúc chờ (placeholder)

```bash
bash $SKILL/scripts/prep_source_video.sh placeholder $OUT   # dark 720×1280 + audio thật
```

→ lint + inspect + draft render full composition ngay, swap avatar thật (re-encode) khi HeyGen xong rồi render final. Tiết kiệm wall-clock + de-risk layout/PIP trước render thật.

## Delegation prompt template

```
Phase 2 — Convert ElevenLabs MP3 to HeyGen lip-sync MP4.

# Files
- INPUT: <abs path>/workspace/content/<date>/<slug>/audio/full.mp3
- OUTPUT: <abs path>/workspace/content/<date>/<slug>/source.mp4

# Constraints
- HeyGen avatar look: pick random from HEYGEN_AVATAR_LOOKS env
- Render aspectRatio="9:16", resolution="720p" (= 720×1280 portrait)
- Duration must match input MP3 ±50ms
- Use the `heygen-mp3-to-mp4` skill — its SKILL.md has the full workflow.

# Process
1. Invoke `heygen-mp3-to-mp4` skill.
2. Pass --input <mp3 path> --output <mp4 path>.
3. Wait for completion (HeyGen render 60-180s).
4. Verify: ffprobe shows 720×1280, duration matches MP3.
5. Report: file path + duration_seconds + avatar_look_id.

# Status reporting
End with:
**Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
**Summary:** [1 sentence]
**Concerns/Blockers:** [if applicable]
```

## OAuth check (first call mỗi session)

HeyGen MCP chỉ expose `mcp__heygen__authenticate` + `complete_authentication` cho đến khi auth complete. Nếu các tool video (`create_video_from_avatar`, `get_video`) chưa load trong deferred-tool list:

1. Gọi `mcp__heygen__authenticate` → paste authorize URL cho user
2. User authorize ở browser → callback URL → user paste lại
3. `mcp__heygen__complete_authentication`
4. Video tools mới load — retry Phase 2

## Concurrent với Phase 3 setup (TỐI ƯU)

Phase 2 HeyGen render typically 60-180s. **KHÔNG đợi blocking** — kick HeyGen qua background mode, song song chuẩn bị:
- Step 6: viết `design.md`
- Step 7.1: master scaffold skeleton (CSS layout, brand-mark, slide-bg, heygen-bg — chưa có scene mounts)
- Step 3.5: gán ảnh vào beats
- Step 8 scene-01 reference pre-author

Khi HeyGen xong → wire `<video #v-source src="source.mp4">` + `<audio #a-source>` + run Step 8 fanout sub-agents (scenes không phụ thuộc HeyGen).

## Duration probe

Sau khi HeyGen xong, lấy duration để build SCENE_STARTS array + PIP_EVENTS + brand-mark `data-duration`:

```bash
TOTAL=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 source.mp4)
echo "Total: ${TOTAL}s"
```

Cross-check với `alignment.json.duration_ms / 1000`. Lệch >200ms → HeyGen có thể bị truncate / cộng silence padding. Adjust `data-duration` theo `ffprobe`, vì runtime đọc source.mp4 thật.

## Resume mode (skip Phase 2)

Nếu `source.mp4` đã tồn tại trong project dir + duration match `full.mp3` → skip Phase 2, vào thẳng scaffold + fanout. User hỏi "tạo lại scenes" hoặc "redo phase 3" thường ở case này.

```bash
if [ -f "$OUT/source.mp4" ] && [ -f "$OUT/audio/full.mp3" ]; then
  MP3_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT/audio/full.mp3")
  MP4_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT/source.mp4")
  echo "MP3=$MP3_DUR  MP4=$MP4_DUR — skip Phase 2 nếu match"
fi
```

## Common pitfalls

| Pitfall | Fix |
|---|---|
| HeyGen render 1280×720 landscape | Set aspectRatio="9:16" resolution="720p". Avatar frame portrait crops từ portrait source. |
| MCP báo "tool not found" cho `upload_asset` | Old MCP name. Dùng REST helper script (`heygen-mp3-to-mp4/scripts/upload_asset.py`). |
| MCP chỉ expose `authenticate` / `complete_authentication` | Chưa OAuth — run auth flow trước. |
| Avatar look ID stub placeholder | `.env.local` ship `avatar_look_id_1` stub. Real values ở marketing repo `~/Documents/GitHub/hoang-ai-marketing/.env`. |
| Avatar face crop trán | `object-position: center 25%` ở avatar frame CSS (xem `avatar-pip-layout.md`). Tweak 20-30% per avatar. |
| HeyGen duration ≠ MP3 duration | Trust ffprobe `source.mp4`, set `data-duration` theo MP4. |
| Block waiting cho HeyGen 60-180s | Kick background, parallel scaffold + scene-01 + design.md. Wire `source.mp4` khi xong. |
