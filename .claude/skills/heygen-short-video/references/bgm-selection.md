# Background Music Selection

Library: `workspace/assets/reels/background music/`

## Available Tracks

| File | Mood | Best for |
|------|------|----------|
| `Aluminum - Roie Shpigler.mp3` | Reflective, ambient | Thoughtful content, AI insights, calm explanation |
| `Ascension - Creative Cut - Orchestra Song.mp3` | Orchestral, uplifting | Success stories, achievement reveals, climactic moments |
| `Chase Velocity - FableForte - Cinematic.mp3` | Fast-paced, intense | Urgency, competition, "you're falling behind" sections |
| `Epic Emotional Music - Lux-Inspira - Liberation.mp3` | Epic, emotional | Transformation stories, before/after, breakthroughs |
| `Fortitude (Shorter Version).mp3` | Short, determined | Quick hooks, punchy intros (short track ~20s) |
| `Miracle - Roman P - Cinematic.mp3` | Cinematic, wonder | Demos, "magic moment" reveals, wow factor |
| `Rising Star - Song by TURPAK.mp3` | Rising energy, motivational | Build-up sections, growing momentum, CTA buildup |
| `The Last Hero - Veaceslav Draganov.mp3` | Heroic, cinematic | Bold statements, overcoming obstacles, empowerment |

## Volume Settings

- **Default volume**: `0.12` (subtle, won't compete with avatar speech)
- **Max volume**: `0.15` (hard cap in code — values above 0.15 are clamped)
- **Fade**: Default `fadeInSec: 1`, `fadeOutSec: 2` — increase fadeOut to 3-4s for smoother endings
- **Multiple tracks**: Switch tracks to match mood shifts (e.g., calm intro → intense middle → uplifting CTA)

## Music Matching by Video Section

| Section | Recommended Track | Volume |
|---------|------------------|--------|
| Hook (0-3s) | `Fortitude` or `Chase Velocity` | 0.15 |
| Pain point | `Chase Velocity` or `Epic Emotional` | 0.12 |
| Solution/Demo | `Miracle` or `Aluminum` | 0.10 |
| Climax/Result | `Ascension` or `The Last Hero` | 0.15 |
| CTA | `Rising Star` | 0.15 |
