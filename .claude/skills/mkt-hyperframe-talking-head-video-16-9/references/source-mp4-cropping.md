# Source MP4 cropping for the landscape avatar frame

## The problem

HeyGen renders avatar lip-sync videos at **9:16 portrait** by default (1080×1920). The 16:9 landscape composition needs a portrait-ish avatar in a 540×880 (SPLIT) or 320×420 (PIP) frame. So we have a portrait MP4 sourced into a portrait frame — the math actually works without distortion, but framing requires care.

## CSS-only fallback (default)

```css
#v-source {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  object-position: center 25%;
}
```

`object-fit: cover` ensures the video fills the frame without letterboxing. `object-position: center 25%` shifts the visible region UP — keeps the avatar's face roughly center-of-frame instead of letting their chest / desk dominate.

Tweak `object-position`:
- `center 15%` — face high in frame (good if HeyGen rendered with lots of headroom)
- `center 25%` — neutral default
- `center 35%` — face lower (good if avatar's hands gesture a lot at the bottom)

## When CSS isn't enough

If the avatar's face still looks awkwardly cropped, the cleanest fix is to regenerate HeyGen with a tighter portrait crop or a pre-cropped landscape source. Two options:

### Option A — Re-render at portrait-but-tight

In HeyGen, choose a "close-up" or "head-and-shoulders" framing preset. The output is still 9:16 but the face occupies 70-80% of the frame instead of 50-60%. This makes the SPLIT avatar look full and natural. PIP corner thumb still works because the face is dominant.

### Option B — Pre-crop to 540×880 with ffmpeg

If you have a wider HeyGen MP4 (1920×1080 landscape avatar with empty space), you can crop to portrait before mounting:

```bash
ffmpeg -i source-raw.mp4 \
  -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=540:880" \
  -c:a copy source.mp4
```

This produces a 540×880 source.mp4 ready to drop in. Avoid this approach if HeyGen is already 9:16 — re-cropping adds compression artifacts.

### Option C — Two source MP4s for SPLIT vs PIP

Advanced: render one MP4 framed for SPLIT (full upper body) and a tighter one for PIP corner (face only). Switch via `<video>` element swap during PIP transitions. Adds complexity; only worth it for hero videos with very tight quality bar.

## Audio handling

`source.mp4` from HeyGen contains the lip-synced TTS audio. Mount this audio at track 1:

```html
<audio id="a-source" data-start="0" data-duration="60.72" data-track-index="1" data-volume="1" src="source.mp4"></audio>
```

DO NOT also mount `voiceover.mp3` separately — that's the same audio twice and will sound like robotic doubling. `voiceover.mp3` is kept in the workspace folder for record-keeping (TTS source of truth) but is not used in the final composition.

## When PIP framing breaks

In PIP corner (320×420), the avatar can look awkward if:
- Face is too small (object-position: center 25% pushes face out of crop) → try `center 35%`
- Avatar gestures with hands cut off at the bottom → accept it; PIP is a small thumbnail and viewers don't expect full body
- Gradient/halo from `box-shadow: 0 0 40px rgba(103,232,249,0.45)` clashes with avatar's own color → adjust `boxShadow` in the `goPIP()` block to a neutral color
