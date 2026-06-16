# Text Effects Reference

Caption text effects controlled via `textEffect` field on each `CaptionSegment`.

## Available Effects

### `word-by-word`
Each word fades up with staggered timing (~3 frames/word). Creates a teleprompter feel.
- Best for: `hook` and `cta` captions — draws attention to each word
- Uses Remotion `spring()` with `{ damping: 14, mass: 0.4 }` per word
- Each word slides up 12px and fades from 0→1 opacity

### `deep-glow`
Highlighted keywords pulse with multi-layer text-shadow (10px, 20px, 40px, 60px layers).
- Best for: `solution` captions with impressive numbers/results
- Glow intensity pulses via `sin(frame * 0.15)` between 60-100%
- Only affects highlighted words — non-highlighted text renders normally

### `flicker`
Highlighted keywords oscillate opacity between 30-100% at different frequencies.
- Best for: `pain` captions — creates unease/urgency on negative keywords
- Each word gets unique frequency (0.3-0.6) and phase (deterministic by word index)
- Non-highlighted text stays at full opacity

### `typewriter`
Words appear one-by-one with sharp cut (no fade), like typing on screen. Blinking cursor `|` follows the last revealed word.
- Best for: `hook` on tech/AI topics — feels like a prompt being typed
- Stagger: 4 frames/word (~133ms), hard cut visibility
- Cursor blinks at ~2Hz until all words revealed
- Pair with: keyboard click or digital beep SFX

### `slam`
Words drop in from above with scale bounce — starts at 1.8x scale and slams down to normal.
- Best for: `hook` and `pain` — dramatic, impactful entrance
- Spring config: `{ damping: 8, mass: 0.6, stiffness: 200 }` — bouncy overshoot
- Each word drops from -40px with scale 1.8x → 1.0x
- Pair with: SUDDEN SUSPENSE, boom, or bass drop SFX

### `wave`
Words ripple in with continuous sine-wave vertical motion after entry.
- Best for: `hook` on lifestyle/casual topics — playful, energetic
- Entry uses spring fade, then continuous `6px * sin(frame * 0.12 + i * 0.8)` wave
- Creates a "living text" feel — words keep subtly moving
- Pair with: whoosh, snap, or rising tone SFX

### `none` (default)
Standard highlight rendering — **bold white text** + subtle text-shadow. KHÔNG đổi màu chữ highlight — chỉ dùng **font-weight: bold** để làm nổi bật.

## When to Use

| Caption Style | Recommended Effect | Why |
|---------------|-------------------|-----|
| `hook` | `typewriter` / `slam` / `wave` | **Rotate across videos** for variety |
| `pain` | `flicker` or `slam` | Creates visual unease or dramatic impact |
| `solution` | `deep-glow` or `word-by-word` | Makes positive results feel impressive |
| `cta` | `word-by-word` or `typewriter` | Ensures CTA text is fully read |
| `normal` | `none` | Keeps information-dense sections clean |

## Hook Style Recipes (rotate across videos)

| Recipe | textEffect | Paired SFX | Best for |
|--------|-----------|-----------|----------|
| **Tech/AI** | `typewriter` | keyboard click, digital beep | Demo, tutorial, prompt-focused hooks |
| **Bold/Shock** | `slam` | SUDDEN SUSPENSE, boom, bass drop | Data hooks, bold claims, myth busting |
| **Fun/Energy** | `wave` | whoosh, snap, rising tone | Lifestyle, casual, storytelling hooks |

**Rule**: Don't use the same hook recipe for 2 consecutive videos. Alternate to keep content feeling fresh.

## Caption Position

`captionPosition` controls vertical placement (top % of frame). Defaults:
- Default: `55` (near neck area of HeyGen avatar — optimal for talking head)
- Range: `40`-`70` depending on avatar framing
- Override per-segment or globally via `defaultCaptionPosition`

## Pacing Tips (J-cuts & Hook Optimization)

### Hook Optimization (first 10s)
- Set `hookBoostSec: 10` to auto-boost zoom by 1.08x with quadratic falloff
- Combine with aggressive `zoomPulses` (type: "hold" or "punch") in first 10s
- Use `textEffect: "word-by-word"` on hook caption
- Add camera-flash sound effect at 0.0s
- Use fast crossFadeFrames (8-10) for snappy transitions

### J-cuts (editorial technique)
Overlap audio from next scene before visual cut. In HeyGen avatar videos, achieve this by:
- Increasing `crossFadeFrames` to 15-20 (audio bleeds across flash transition)
- Adding a riser/whoosh sound effect 0.5s before each clip transition
- These create the perception of seamless flow without actual audio pre-roll
