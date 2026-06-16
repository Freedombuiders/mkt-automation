# Troubleshooting

Pitfalls orchestrator-level. Editor pitfalls (composition HTML, GSAP, lint config) đã document trong [`mkt-hyperframe-talking-head-video-16-9/SKILL.md`](../../mkt-hyperframe-talking-head-video-16-9/SKILL.md) "Common pitfalls" section (L272-292) — không lặp lại ở đây.

## Orchestrator-specific

### Sub-skill path resolution

Orchestrator gọi script ở 2 path khác nhau giữa repo:

| Repo | Skill install path |
|---|---|
| `claudeclaw-os` | `.claude/skills/<skill-name>/scripts/...` |
| `hoang-ai-marketing` | `.claude/skills/<skill-name>/scripts/...` (project-local) hoặc `~/.claude/skills/<skill-name>/scripts/...` (user global) |

**Resolution order trong orchestrator commands:**
1. Project-local: `.claude/skills/<skill-name>/scripts/...` (relative tới CWD = workspace folder OR git root)
2. User global: `~/.claude/skills/<skill-name>/scripts/...`

Nếu cả 2 fail → báo user `<skill-name> not installed` và stop.

### Script > 5000 chars

Stop ở Step 0 với message rõ: "Script <N> chars, vượt limit 5000. Tách semantic thành 2 video hoặc rút gọn → rerun."

KHÔNG auto-truncate (sẽ mất ý đoạn cuối).

### MP3 > 300s

Phase 2 `heygen-mp3-to-mp4` sẽ fail-fast (skill có guard). Orchestrator chỉ cần báo lỗi đó cho user, KHÔNG cần check duration trước.

### Phase 2 + Phase 3a CPU contention (M-series Mac)

Whisper `medium` model + ffmpeg upload đồng thời có thể spike CPU > 100% và làm cả 2 chậm hơn sequential.

**Symptom:** wall time của parallel block = sequential time × ~1.0 (no speedup).

**Mitigation:**
1. Test trên 1 video 60-90s thật, đo `time` cho cả parallel và sequential mode.
2. Nếu net-zero hoặc chậm hơn → fallback sequential. Edit orchestrator command để chạy `transcribe_audio.py` sau khi `heygen-mp3-to-mp4` poll done.
3. Whisper `small` thay vì `medium` giảm CPU 40% nhưng accuracy thấp hơn — chỉ fallback nếu user OK chất lượng caption thấp.

### 2 checkpoint cùng fire cho scenes outline

`mkt-hyperframe-talking-head-video-16-9/scripts/detect_scenes.py` có checkpoint riêng (L155 trong skill SKILL.md). Khi orchestrator đã chạy `mkt-plan-short-video-edit-16-9` và có `visual-plan.json`, gọi `detect_scenes.py` MUST pass `--auto` để skip checkpoint nội bộ — không thì user sẽ thấy 2 prompt liên tiếp về cùng outline.

```bash
python3 .claude/skills/mkt-hyperframe-talking-head-video-16-9/scripts/detect_scenes.py \
  --workspace . --auto    # khi visual-plan.json đã exist
```

### Infographic gen sai thứ tự

Nếu `infographic_mode=now`, image gen phải chạy TRƯỚC `lint_and_preview.py`. Sai thứ tự → preview Studio show broken-image icons (vì `<img onerror>` đã remove element nhưng layout reflow sau khi gen sẽ khác).

**Đúng:** Phase 3b plan → CP2 → apply_plan + scaffold + generate_compositions + generate_root_index → infographic gen → scaffold_infographic_slots (chỉ inject onerror fallback) → lint_and_preview.

### HeyGen render 1280×720 landscape

KHÔNG bao giờ render landscape. Layout 16:9 này ép avatar frame portrait-ish (540×880 SPLIT, 320×420 PIP), cả 2 đều closer to portrait. Render 1280×720 landscape → avatar có 2 dải đen 2 bên ráp vào landscape, hoặc face quá nhỏ trong frame.

→ Phase 2 MCP call PHẢI là `dimension: { width: 720, height: 1280 }`.

### Avatar `object-position` sai

Default `center 25%`. Crop chuẩn 90% HeyGen avatar.

Nếu HeyGen avatar đặc biệt (height khác hoặc face position khác) → tweak `20%`–`30%`. Sửa trong `index.html`:

```css
#v-source { object-fit: cover; object-position: center 25%; }
```

→ Không có lint check. Phải xem preview Studio để verify face không bị crop trán.

## Khi nào escalate sang sibling skills

| Symptom | Skill xử lý |
|---|---|
| Script chưa viết, chỉ có topic | `mkt-create-script-storytelling-video` (chạy trước rồi quay lại skill này) |
| Đã có MP3 sẵn, không cần Phase 1 | `heygen-mp3-to-mp4` rồi `mkt-hyperframe-talking-head-video-16-9` standalone |
| Cần TikTok/Reels vertical 9:16 | `mkt-full-video-with-11-hyperframe-heygen` (sibling) |
| Cần video montage / music video không talking-head | KHÔNG dùng skill này — talking-head spine là core assumption |
