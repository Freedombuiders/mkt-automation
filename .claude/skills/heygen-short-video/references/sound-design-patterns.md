# Sound Design Patterns

Editorial patterns for syncing sound effects with video moments. All achievable using the existing `soundEffects` array in props.

## Recommended SFX by Moment

### Video Start (0.0s)
- Camera flash: `camera flash.mp3` — immediate attention grab
- Suspense: `SUDDEN SUSPENSE.mp3` — dramatic opener

### Hook → Pain Transition
- Bruh: `Bruh - Sound Effect (HD).mp3` — comedic disappointment
- Buzzer: `Wrong Buzzer.mp3` — wrong answer feel

### Pain → Solution Transition
- Tada: `tada.mp3` — reveal moment
- Ting: `ting.mp3` — light bulb moment
- Snap: `búng tay.mp3` — snap to attention

### Key Facts / Numbers
- Cha-ching: `Cash Register.mp3` — money-related stats
- Pop: `Pop up - Sound Effect.mp3` — when overlay/text appears

### Scene Transitions
- Whoosh: `Whoosh sound effect (1).mp3` — between clips
- Riser: Place 0.5s before clip transition for J-cut feel
- Laser: `Laser.mp3` — tech/futuristic transitions

### CTA (End)
- Notification: `Discord Notification - Sound Effect.mp3` — subscribe/follow prompt
- Tada tada: `tada tada.mp3` — celebratory ending

## Pacing Rules

1. **Max 3-5 SFX per video** — more becomes noisy
2. **Front-load effects** — 60% of SFX in first 10 seconds
3. **Match energy** — loud SFX for hook, subtle for transitions
4. **Volume levels**: hook SFX 0.25-0.35, transition SFX 0.15-0.2, CTA SFX 0.25. SFX phải nhẹ nhàng, KHÔNG được lấn át giọng nói.
5. **Never overlap** — space SFX at least 1.5s apart

## J-cut Audio Pattern

To simulate J-cuts (audio leads video):
1. Set `crossFadeFrames: 15-20` (overlaps clip audio)
2. Add whoosh/riser SFX 0.5s before each clip boundary
3. This creates smooth audio flow without actual audio pre-roll

Sound files at: `workspace/assets/reels/MEME SOUND/`
Full catalog: [meme-sounds.md](meme-sounds.md)
