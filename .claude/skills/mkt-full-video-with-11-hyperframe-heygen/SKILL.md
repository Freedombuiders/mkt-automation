---
name: mkt-full-video-with-11-hyperframe-heygen
description: End-to-end short-video pipeline — từ kịch bản (Việt/Anh) ra MP4 TikTok/Reels 9:16 hoàn chỉnh. Orchestrator 3 phase ghép 3 skill có sẵn — (1) `mkt-elevenlabs-tts-to-mp3` đọc script bằng voice của Hoàng, (2) `heygen-mp3-to-mp4` lip-sync avatar HeyGen, (3) delegate Phase 3 packaging cho sub-agent `mkt-full-video-phase3-packager` (transcribe + scene outline + fan-out N scene writers parallel + scaffold + render MP4). Chạy autopilot end-to-end: KHÔNG checkpoint, KHÔNG preview, tự chọn default khi thiếu info, render xong báo absolute path MP4. USE WHEN user nói "tạo full video từ script", "script to tiktok video", "pipeline full video heygen + hyperframe", "tạo video từ kịch bản đến mp4", "elevenlabs heygen hyperframe full pipeline", "kịch bản ra video tiktok", hoặc có sẵn 1 script + (optional) ảnh b-roll và muốn ra MP4 9:16 đóng gói có captions, SFX, b-roll.
---

# mkt-full-video-with-11-hyperframe-heygen

End-to-end orchestrator: **script → final TikTok/Reels MP4 9:16**.

**AUTOPILOT (override):** Theo mục AUTOPILOT trong `agents/videoeditor/CLAUDE.md`. Chạy 1 mạch script → MP4, KHÔNG dừng ở checkpoint nào, KHÔNG mở preview. Hai checkpoint dưới đây (MP3, scenes-outline) đều **bỏ qua** — không hỏi user, tự duyệt và chạy tiếp. Phase 3 luôn gọi với `auto_scenes=true`. Thiếu info thì tự chọn default. Render xong báo absolute path MP4 cho user.

## Khi nào dùng

- User có script Việt/Anh ≤ 5000 ký tự muốn ra video TikTok hoàn chỉnh
- Có sẵn (optional) ảnh hoặc video b-roll kèm mục đích sử dụng
- Muốn đi 1 mạch từ kịch bản đến MP4 cuối (autopilot, báo path khi xong)

Không dùng skill này nếu:
- User đã có MP3 sẵn → dùng thẳng `heygen-mp3-to-mp4`
- User đã có MP4 talking-head sẵn → dùng thẳng `mkt-hyperframe-talking-head-video`
- User cần HeyGen tự đọc text (không qua ElevenLabs) → dùng `heygen-script-to-mp4`
- Script > 5000 ký tự → split semantic rồi gọi pipeline cho từng segment

## Pipeline overview

```
Script (text + optional b-roll)
    │
    ▼
Phase 1 ── mkt-elevenlabs-tts-to-mp3 ───► voiceover.mp3
    │                                         │
    │                                         ▼
    │                              (autopilot — KHÔNG dừng duyệt MP3)
    │                                         │
    │                                         ▼
Phase 2 ── heygen-mp3-to-mp4 ──────────► source.mp4 (9:16 lip-sync)
    │
    ▼
Phase 3 ── spawn agent mkt-full-video-phase3-packager (isolated context)
            │
            ├─ transcribe + clean + group captions
            ├─ detect scene boundaries + classify mockup_variant
            ├─ (autopilot — KHÔNG dừng duyệt scenes outline)
            ├─ FAN-OUT N general-purpose sub-agents (1 per scene) parallel
            │   → mỗi sub-agent build content JSON theo variant schema
            ├─ merge → scenes.json
            ├─ parallel: scaffold sub-comps + copy SFX + inject captions
            ├─ generate root index.html
            └─ lint + render -q standard → <slug>.mp4
    │
    ▼
Báo absolute path MP4 cho user
```

**Checkpoint rule (AUTOPILOT):** KHÔNG checkpoint nào dừng. MP3 tự duyệt, scenes outline tự duyệt (`auto_scenes=true`), render thẳng (KHÔNG Studio gate).

## Inputs

| Input | Required | Format / ví dụ |
|---|---|---|
| Script text | Yes | File path (`.txt`/`.md`) hoặc inline string. ≤ 5000 ký tự. |
| Slug project | No | Auto-derive từ 5 từ đầu của script. Lowercase, ASCII, dash. |
| B-roll list | No | Array `[{path: "...", purpose: "Bài học 1 — minh họa X"}, ...]`. |
| Voice settings override | No | `{stability, similarity_boost, style}` cho ElevenLabs. |
| Avatar look | No | 1 ID lấy từ `HEYGEN_AVATAR_LOOKS` env (.env, comma-separated). Random nếu không chọn. |
| `auto_scenes` | No | **AUTOPILOT: luôn `true`** — skip scenes-outline checkpoint trong Phase 3. |

## Workspace layout

```
workspace/content/YYYY-MM-DD/<slug>/
├── script.txt              # Phase 0
├── voiceover.mp3           # Phase 1
├── source.mp4              # Phase 2
├── broll/                  # User-provided b-roll (copy)
├── transcript.json         # Phase 3
├── caption-groups.json     # Phase 3
├── scenes-outline.json     # Phase 3 — pre-checkpoint outline
├── scenes/                 # Phase 3 — fan-out per-scene content writes here
│   ├── scene-1.json
│   └── ...
├── scenes.json             # Phase 3 — merged final
├── compositions/           # Phase 3 — HF sub-comps
├── sfx/                    # Phase 3 — 6 SFX
└── index.html              # Phase 3 — root composition
```

`YYYY-MM-DD` = ngày hôm nay (UTC+7).

## Workflow

### Step 0 — Setup

1. Validate `len(script_text) <= 5000`. Vượt → stop, yêu cầu user split semantic.
2. Derive slug nếu thiếu: 5 từ đầu → lowercase → bỏ dấu → space→dash.
3. Tạo `workspace/content/YYYY-MM-DD/<slug>/`. Save `script.txt`.
4. Nếu user có b-roll: tạo `<folder>/broll/`, copy file giữ tên gốc.
5. Báo user: "Workspace tạo tại `<folder>`. Bắt đầu Phase 1 — ElevenLabs TTS."

### Step 1 — Phase 1: Script → MP3 (ElevenLabs)

```bash
uv run .claude/skills/mkt-elevenlabs-tts-to-mp3/scripts/text_to_mp3.py \
  --file workspace/content/YYYY-MM-DD/<slug>/script.txt \
  -o workspace/content/YYYY-MM-DD/<slug>/voiceover.mp3
```

Voice settings overrides → thêm `--stability` / `--similarity_boost` / `--style`.

Sau khi xong, check duration:

```bash
uv run .claude/skills/heygen-mp3-to-mp4/scripts/check_duration.py \
  workspace/content/YYYY-MM-DD/<slug>/voiceover.mp3
```

`TOO_LONG` → stop, báo user MP3 > 5 phút HeyGen, yêu cầu rút script.

### Step 2 — MP3 (AUTOPILOT, KHÔNG dừng duyệt)

KHÔNG dừng hỏi user. Verify MP3 tồn tại + duration ≤ 300s rồi auto-flow sang Phase 2. In 1 dòng:

```
Phase 1 done — voiceover.mp3 (<X.X>s, <Y.Y>MB). Sang Phase 2 (HeyGen)…
```

Nếu MP3 fail/empty → rerun `text_to_mp3.py` 1 lần; vẫn fail thì báo lỗi cho user.

### Step 3 — Phase 2: MP3 → HeyGen MP4 (auto)

Theo sub-skill `heygen-mp3-to-mp4`:

1. **Pick avatar ID** — read `HEYGEN_AVATAR_LOOKS` từ `.env` (comma-separated), random pick nếu user không chỉ định:
   ```bash
   HEYGEN_AVATAR_LOOKS=$(grep '^HEYGEN_AVATAR_LOOKS=' .env | cut -d'=' -f2- | tr -d '"' | tr -d "'")
   echo "$HEYGEN_AVATAR_LOOKS" | tr ',' '\n' | awk 'BEGIN{srand()} {a[NR]=$0} END{print a[int(rand()*NR)+1]}'
   ```
   Nếu env var thiếu/empty → stop và báo user thêm `HEYGEN_AVATAR_LOOKS=<id1>,<id2>` vào `.env`. Báo user pick nào trước khi gọi MCP.

2. **Upload MP3** lên HeyGen qua MCP (`upload_asset`, asset type `audio`). **KHÔNG** curl `https://upload.heygen.com/...`.

3. **Tạo avatar video** qua MCP (`generate_avatar_video`):
   ```yaml
   character: { type: avatar, avatar_id: <picked>, scale: 1.0 }
   voice:     { type: audio, audio_asset_id: <from upload> }
   dimension: { width: 720, height: 1280 }   # 9:16
   title:     "<slug>-<timestamp>"
   ```

4. **Poll status** mỗi ~10s → `completed` (cap 10 min). `failed` → stop, show error.

5. **Download MP4** → `workspace/content/YYYY-MM-DD/<slug>/source.mp4` (filename inviolable):
   ```bash
   uv run .claude/skills/heygen-mp3-to-mp4/scripts/download_video.py \
     "<video_url>" "workspace/content/YYYY-MM-DD/<slug>/source.mp4"
   ```

6. Báo user 1 dòng: "Phase 2 done — `<path>` (avatar `<id>`, <duration>s, <size>MB). Spawning Phase 3 packager…"

**Không stop ở đây.** Auto-flow sang Phase 3.

### Step 4 — Phase 3: Spawn packager sub-agent

Use the Task tool with `subagent_type: "mkt-full-video-phase3-packager"`. Pass a self-contained prompt with the inputs the agent needs. Example:

```
Workspace: workspace/content/2026-05-03/hom-nay-minh-chia-se/
Slug: hom-nay-minh-chia-se
Script: <full script text>
B-roll: [
  {"path": "workspace/content/2026-05-03/hom-nay-minh-chia-se/broll/alphabet.png", "purpose": "Bài học 1"},
  ...
]
auto_scenes: true
header_label: "3 BÀI HỌC AI"
footer_handle: "@tranvanhoang.com"

Run the full Phase 3 packaging pipeline per your agent definition. AUTOPILOT: skip scenes-outline checkpoint, no preview — render -q standard to <slug>.mp4 and return the absolute MP4 path.
```

The sub-agent (AUTOPILOT — luôn `auto_scenes: true`):
- Transcribes `source.mp4`, builds scene outline (tự duyệt, KHÔNG hỏi)
- Fans out N scene-content writers in parallel
- Merges + scaffolds + lints + renders MP4 (KHÔNG preview)
- Returns absolute MP4 path

Orchestrator KHÔNG dừng relay checkpoint nào — Phase 3 chạy thẳng tới MP4.

### Step 5 — Hand off (render xong → báo path)

When the sub-agent returns the MP4 path, format the final report với absolute path:

```markdown
## Full video pipeline DONE ✅

**File:** `workspace/content/YYYY-MM-DD/<slug>/<slug>.mp4` (1080×1920 30fps, ~<D>s)

**Phase 1 (ElevenLabs):** voiceover.mp3 — <D1>s, <S1>MB
**Phase 2 (HeyGen):** source.mp4 — avatar `<avatar_id>`, <D2>s, <S2>MB
**Phase 3 (HyperFrames):** <N> scenes (<list variants>), <K> caption groups, 6 SFX

**Absolute path:** `/absolute/path/workspace/content/YYYY-MM-DD/<slug>/<slug>.mp4`
```

## Critical orchestration rules

1. **AUTOPILOT — 0 checkpoint** — KHÔNG dừng ở MP3, KHÔNG dừng ở scenes-outline (`auto_scenes=true`), KHÔNG render gate. Chạy thẳng tới MP4 rồi báo path.

2. **Path conventions inviolable** — voiceover phải là `voiceover.mp3`, talking-head phải là `source.mp4`. HF sub-skill expect tên `source.mp4`.

3. **HeyGen MCP only** — không bao giờ curl `https://api.heygen.com/...`. Hard constraint của `heygen-mp3-to-mp4`.

4. **Voice ID lock** — ElevenLabs default `K7ewtjKRNtwwt3lKQ6M0` (Hoàng's brand voice). Override qua `--voice_id` nhưng pipeline báo rõ pick nào.

5. **Script length hard cap 5000 ký tự** — fail fast ở Step 0.1.

6. **MP3 duration ≤ 300s** — HeyGen single-video cap. Check ngay sau Phase 1.

7. **AUTOPILOT render** — Phase 3 render thẳng MP4 (KHÔNG preview, KHÔNG gate). Render xong báo path.

8. **Phase 3 isolation** — Phase 3 chạy trong sub-agent context riêng. HF skill body + 4 reference docs (~40KB) load vào sub-agent thay vì main orchestrator.

## Failure modes & fallback

| Symptom | Hành động |
|---|---|
| Script > 5000 ký tự | Stop, yêu cầu user split semantic |
| ElevenLabs API fail | Báo error, suggest check `ELEVENLABS_API_KEY` trong `.env` |
| MP3 > 300s sau Phase 1 | Stop pipeline, suggest `heygen-short-video` (chunking) |
| HeyGen MCP not connected | Stop, báo `claude mcp list` để verify |
| HeyGen render failed | Show error, gợi ý check credits qua `mcp__heygen__get_current_user` |
| Phase 3 sub-agent fail | Đọc error trace, gợi ý user re-run Phase 3 standalone bằng `mkt-hyperframe-talking-head-video` skill |
| Scene writer returns malformed JSON | Sub-agent tự re-spawn cho scene đó (không phải orchestrator's concern) |
| User reject MP3 voice | Quay lại Phase 1 với voice settings tweak |

## Example end-to-end

User:
> Có script đây, chạy full pipeline ra video TikTok. Kèm 2 ảnh b-roll cho lesson 1 và lesson 2.
> Script: "Hôm nay mình chia sẻ 3 bài học từ Anthropic. Bài học đầu tiên là Alphabet ship beta. Bài học thứ 2 là 24h…"
> B-roll: alphabet.png (lesson 1), clock.png (lesson 2)

Pipeline:
1. **Step 0** — slug `hom-nay-minh-chia-se`. Folder `workspace/content/2026-05-03/hom-nay-minh-chia-se/`. Save `script.txt`, copy b-roll.
2. **Step 1** — `text_to_mp3.py` → `voiceover.mp3` (45s, 0.7MB).
3. **Step 2 (AUTOPILOT)** — verify MP3 path + duration, in 1 dòng, KHÔNG dừng đợi reply.
5. **Step 3** — Pick avatar (random từ `HEYGEN_AVATAR_LOOKS`, ví dụ `66e75e22…`). Upload MP3 → asset_id. Generate video → poll → download `source.mp4` (45s, 7.5MB).
6. **Step 4** — Spawn `mkt-full-video-phase3-packager` sub-agent.
7. Sub-agent transcribes (35s), builds outline (3 lessons + recap + cta) — tự duyệt, KHÔNG dừng.
8. Sub-agent fan-out 5 scene writers parallel (~8s wall-clock vs ~40s serial).
9. Sub-agent merges → scenes.json → scaffold + SFX + captions parallel → root → lint → render -q standard.
10. Sub-agent returns absolute MP4 path.
11. **Step 5** — Orchestrator báo format chốt + in absolute path của MP4 cho user.

Total wall-clock: ~4–6 phút (vs 5–8 phút ở pipeline serial cũ).

## What this skill does NOT do

- KHÔNG viết script (dùng `mkt-create-script-short-video` hoặc `mkt-create-script-storytelling-video` trước).
- KHÔNG handle script > 5000 ký tự (fail fast — user split semantic).
- KHÔNG chunk MP3 (single-clip pipeline; > 300s dùng `heygen-short-video`).
- (Autopilot: CÓ auto-render MP4 cuối + báo path, KHÔNG preview gate.)
- KHÔNG handle Phase 3 internals — delegate cho sub-agent `mkt-full-video-phase3-packager`.
- KHÔNG override hard constraint của sub-skill (avatar allowlist, MCP-only, font Be Vietnam Pro, etc.).

## References

- **Sub-skill `mkt-elevenlabs-tts-to-mp3`** — `.claude/skills/mkt-elevenlabs-tts-to-mp3/SKILL.md`
- **Sub-skill `heygen-mp3-to-mp4`** — `.claude/skills/heygen-mp3-to-mp4/SKILL.md`
- **Sub-skill `mkt-hyperframe-talking-head-video`** — `.claude/skills/mkt-hyperframe-talking-head-video/SKILL.md` (loaded by Phase 3 sub-agent)
- **Sub-agent `mkt-full-video-phase3-packager`** — `.claude/agents/mkt-full-video-phase3-packager.md`
- **Reference HyperFrames project** — `workspace/video-projects/3-bai-hoc/`
