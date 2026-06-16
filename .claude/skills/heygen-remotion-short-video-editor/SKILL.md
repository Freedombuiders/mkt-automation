---
name: heygen-remotion-short-video-editor
description: "Compose final short video from production plan + HeyGen avatar clips + Grok/custom visuals using Remotion. Builds props JSON and renders the final MP4 autopilot (no Studio preview, no approval gate), and reports the output path. Handles interleaving avatar/visual clips, captions with effects, BGM, sound effects, and progress bar. USE WHEN user says 'ghép video remotion', 'compose video', 'editor video ngắn', 'remotion compose', 'ghép clip heygen', 'tạo video cuối cùng', 'render video remotion'."
---

# HeyGen Remotion Short Video Editor

Compose final short video from all production assets using Remotion. Preview first, render on approval.

```
production-plan.json + HeyGen clips + Grok/custom videos + MP3
  → Build Remotion props → Render MP4 (autopilot, no preview) → báo absolute path cho user
```

**AUTOPILOT:** Theo mục AUTOPILOT trong `agents/videoeditor/CLAUDE.md`. KHÔNG mở Studio, KHÔNG đợi approval. Render thẳng rồi báo absolute path của file MP4 cho user. Thiếu info thì tự chọn default.

## Input

1. **production-plan.json path** (required) — from `plan-short-video-edit` skill
2. **HeyGen clips directory** (required) — from `heygen-short-video` skill, contains `heygen_manifest.json`
3. **Grok/custom video directory** (optional) — visual segment videos
4. **MP3 voiceover path** (required) — for visual segment audio
5. **SRT path** (required) — for caption timing

## Step 1: Gather & Verify Assets

1. Read `production-plan.json` for segment list, effects, BGM
2. Read `heygen_manifest.json` for avatar clip mapping
3. **Verify Grok visuals exist (do NOT generate here)**: If plan has `grok` segments, check that the referenced `grok_visuals/*.mp4` files exist. Grok generation is handled upstream by `video-ai-editor` Phase 1b — this skill only verifies. If Grok videos are missing, STOP and report the error.
4. Verify all referenced files exist:
   - HeyGen clips: `heygen_clips/chunk_XXX.mp4`
   - Grok videos: `grok_visuals/1.mp4`, `2.mp4`...
   - Custom b-roll: from manifest paths
5. Trim Grok/custom videos to segment duration if needed:
   ```bash
   ffmpeg -i "<video>" -t <segment_duration> -c copy "<output>"
   ```

## Step 2: Stage Assets in Remotion

Place all clips in `workspace/assets/reels/` subfolders (symlinked as Remotion `public/media/`):

```bash
# HeyGen clips
cp heygen_clips/*.mp4 workspace/assets/reels/heygen/

# Grok visuals (strip audio first)
for f in grok_visuals/*.mp4; do
  ffmpeg -i "$f" -an -c:v copy "workspace/assets/reels/grok/$(basename $f)"
done

# Custom b-roll
cp custom_media/* workspace/assets/reels/custom/

# Visual segment audio (split from MP3 for non-avatar segments)
cp visual_audio/*.mp3 workspace/assets/reels/visual_audio/
```

## Step 3: Build Remotion Props JSON

Build `props/heygen-short.json` following the structure in `heygen-short-video/references/remotion-composition.md`.

Key rules:
- **Avatar clips**: use their built-in audio, set `volume: 1`. NEVER add `audioPath` to avatar clips.
- **Visual/Grok clips**: mute video (`volume: 0`), attach per-clip audio from split MP3 segments via sound effects or audio tracks.
- **NEVER set top-level `audioPath`** when mixing avatar + visual clips (it mutes everything).
- **All-avatar videos**: no `audioPath` at all — each clip plays its own lip-synced audio.
- Interleave clips in segment order from production-plan.json
- Include captions with `words` arrays, `textEffect`, `highlights`, `style` from plan
- Include `soundEffects`, `bgmTracks`, `zoomPulses` from plan
- Set `hookBoostSec: 10` if plan specifies it

Save to: `workspace/video-projects/remotion-studio/props/heygen-short.json`

## Step 4: Render MP4 (AUTOPILOT — KHÔNG mở Studio preview)

KHÔNG mở Remotion Studio, KHÔNG đợi user. Render thẳng:

```bash
cd workspace/video-projects/remotion-studio
npx remotion render src/index.ts HeyGenShort out/heygen-short.mp4 --props=props/heygen-short.json
```

Nếu render fail (props lỗi, asset thiếu) → fix rồi render lại. Chỉ báo lỗi khi đã thử fix mà vẫn fail.

## Step 5: Save Final Output

Copy rendered video to content directory:

```
workspace/content/{YYYY-MM-DD}/video-short/{slug}/
├── final.mp4              # Rendered video
├── plan/                  # From plan-short-video-edit
├── heygen_clips/          # From heygen-short-video
├── grok_visuals/          # User-provided Grok videos
└── props/                 # Remotion props used
    └── heygen-short.json
```

Báo absolute path của file MP4 cho user:

```
Render xong: final.mp4 (~<duration>s)
Output: /absolute/path/workspace/content/{date}/video-short/{slug}/final.mp4
```

Nếu render fail → báo lỗi cho user.
