# Remotion Composition Reference

Component: `src/templates/HeyGenShort.tsx` (imports from `src/templates/heygen-short/`)

## Props Structure (`props/heygen-short.json`)

```json
{
  "clips": [
    { "videoPath": "media/heygen/chunk_000.mp4", "durationSeconds": 3.5 },
    { "videoPath": "media/grok/1.mp4", "durationSeconds": 5.5 },
    { "videoPath": "media/heygen/chunk_001.mp4", "durationSeconds": 15.0 }
  ],
  "captions": [
    {
      "text": "Opening hook text here",
      "startSec": 0.0, "endSec": 3.44,
      "style": "hook",
      "highlights": ["key phrase"],
      "emoji": "mind-blown",
      "textEffect": "word-by-word",
      "captionPosition": 55,
      "words": [
        {"word": "Một", "start": 0.0, "end": 0.2},
        {"word": "mình", "start": 0.2, "end": 0.45}
      ]
    }
  ],
  "soundEffects": [
    { "audioPath": "media/sfx/SUDDEN SUSPENSE.mp3", "startSec": 0.0, "volume": 0.3 }
  ],
  "zoomPulses": [
    { "timeSec": 0.0, "scale": 1.15, "type": "hold", "durationFrames": 10, "holdSec": 2.5 }
  ],
  "bRollOverlays": [
    { "mediaPath": "media/broll/money-rain.gif", "startSec": 5.0, "endSec": 8.0, "position": "bottom", "borderRadius": 20 }
  ],
  "backgroundMusic": [
    { "audioPath": "media/bgm/Aluminum - Roie Shpigler.mp3", "startSec": 0, "volume": 0.12, "fadeInSec": 1, "fadeOutSec": 2 },
    { "audioPath": "media/bgm/Rising Star - Song by TURPAK.mp3", "startSec": 30, "volume": 0.15, "fadeInSec": 1, "fadeOutSec": 3 }
  ],
  "durationSeconds": 39.11,
  "crossFadeFrames": 0,
  "showProgressBar": true,
  "hookBoostSec": 10,
  "defaultCaptionPosition": 55
}
```

## Assembling Clips

The `clips` array contains BOTH avatar clips (HeyGen) and visual clips (Grok) in timeline order. Interleave avatar and Grok clips in the order they appear in the script timeline.

### CRITICAL: Always set `crossFadeFrames: 0`

**NEVER use `crossFadeFrames > 0` when `audioPath` is set.** Each non-zero crossFadeFrames subtracts overlap per clip transition. With N clips, the accumulated shift = `(N-1) × crossFadeFrames / FPS` seconds, causing visual clips to progressively desync from the audio voiceover. For example, 8 clips with `crossFadeFrames: 10` at 30fps = 2.33s drift by the last clip — avatar lip-sync and Grok visuals no longer match the spoken words.

## Built-in Visual Effects

1. **Zoom in/out per clip** — scale 1.0→1.05 entry, 1.05→1.0 exit
2. **Hook boost** — extra 1.08x zoom in first N seconds (`hookBoostSec`)
3. **Flash transition** — white flash between avatar clips
4. **Vignette overlay** — radial gradient darkening edges
5. **Spring-animated captions** — slide up with spring physics
6. **Text effects** — word-by-word fade, deep-glow pulse, flicker on highlights
7. **Keyword highlights** — accent-colored bold text within captions
8. **Visual overlays** — animated emoji or b-roll GIF at bottom position with spring bounce/fade
9. **Caption position** — configurable top% (default 55, near neck area)
10. **Progress bar** — gradient bar at top
11. **CTA arrow** — animated pointing finger for call-to-action
12. **Sound effects** — meme sounds at specific timestamps
13. **Style-based caption boxes** — different bg/border/glow per style type
14. **Background music** — multi-track with per-track volume, fade in/out, loop

## Setup & Render

1. Copy clips and assets to Remotion public folder:
```bash
mkdir -p workspace/video-projects/remotion-studio/public/media/{heygen,grok,sfx,broll,bgm,logos}
cp <working_dir>/heygen_clips/*.mp4 workspace/video-projects/remotion-studio/public/media/heygen/
cp workspace/assets/reels/grok_visuals/*.mp4 workspace/video-projects/remotion-studio/public/media/grok/
cp "workspace/assets/reels/MEME SOUND/<chosen_sound>.mp3" workspace/video-projects/remotion-studio/public/media/sfx/
cp "workspace/assets/reels/background music/<chosen_track>.mp3" workspace/video-projects/remotion-studio/public/media/bgm/
cp "workspace/assets/reels/broll_gifs/<category>/<chosen_gif>.gif" workspace/video-projects/remotion-studio/public/media/broll/
```

2. Create props JSON at `workspace/video-projects/remotion-studio/props/heygen-short.json`

3. Render:
```bash
cd workspace/video-projects/remotion-studio
npx remotion render src/index.ts HeyGenShort out/heygen-short.mp4 --props=props/heygen-short.json
```

## Audio Architecture

**CRITICAL: HeyGen avatar clips already contain lip-synced audio. NEVER overlay `audioPath` on them.**

- **HeyGen avatar clips**: Play their own built-in lip-synced audio natively. Do NOT mute or override.
- **Grok visual clips**: Have no useful audio — need voiceover from original MP3 segments.
- **`audioPath`** (top-level prop): ONLY use when there are Grok/visual-only segments. When set, it mutes ALL clips including HeyGen avatars — so NEVER use it for all-avatar videos.
- **All-avatar videos (no Grok)**: Do NOT set `audioPath`. Each HeyGen clip plays its own audio.
- **Mixed avatar + Grok videos**: Do NOT use `audioPath`. Let HeyGen clips play their own audio. For Grok segments, split the original MP3 into segment chunks and attach as per-clip audio or compose audio tracks per segment in Remotion.

## Grok Visual Video Handling

- Grok generates 6s videos. Trim with `ffmpeg -t <needed_duration>` if segment is shorter
- Place trimmed Grok videos in `public/media/grok/1.mp4`, `2.mp4`...
- Grok clips appear as full-screen video in the clips timeline (same as avatar clips)
- **IMPORTANT**: Grok video audio is always muted — the original MP3 voiceover plays instead
- Captions still overlay on top of Grok visual clips — this creates a "voiceover + visual" effect
- Use fewer emoji/GIF overlays on Grok visual segments since the visual is already rich

## Caption Style Types

| Style | When to use | Visual |
|-------|-------------|--------|
| `hook` | Opening 1-2 sentences | Red bg, 44px bold, gold accent |
| `pain` | Pain points, problems | Black bg + red border/glow |
| `solution` | Benefits, solutions | Dark green bg + green glow |
| `cta` | Call-to-action (last) | Purple gradient + bouncing arrow |
| `normal` | Everything else | Black semi-transparent bg |
