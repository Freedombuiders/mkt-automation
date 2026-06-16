# Visual Overlays Reference

Visual overlays add motion/emphasis to **avatar segments only**. Segments using Grok visual video must NOT have overlays.

Max 6-7 overlays per video total. Each segment gets at most ONE overlay type (emoji OR b-roll GIF OR tech logo).

## Animated Emoji

Use `@remotion/animated-emoji`. Set `emoji` field in caption. See [animated-emoji-map.md](animated-emoji-map.md) for full list.

| Context | Emoji Name |
|---------|-----------|
| Shock | `mind-blown`, `screaming` |
| Sleep/bored | `sleep`, `yawn` |
| Pain | `weary`, `distraught`, `cross-mark` |
| Idea | `light-bulb`, `thinking-face` |
| Success | `check-mark`, `sparkles`, `fire`, `muscle` |
| CTA | `bell`, `wave`, `index-finger` |

## B-roll GIF

Read `workspace/assets/reels/broll_gifs/_catalog.json` to find by mood/tags/emotion. Set as `bRollOverlays` entry.

| Segment topic | Catalog category | Example tags |
|---------------|-----------------|--------------|
| Money/revenue | `01_tien_bac` | money, revenue, profit |
| Growth/success | `02_tang_truong` | growth, chart, rocket |
| AI/tech | `04_AI_cong_nghe` | AI, robot, automation |
| Work/productivity | `05_lam_viec` | typing, laptop, team |
| Time/speed | `08_toc_do` | fast, clock, running |

### GIF Selection from Catalog

1. Match segment **mood/emotion** → category `emotion` field
2. Match segment **topic keywords** → file `tags` field
3. Match segment **intent** → file `best_for` field
4. Use `position: "bottom"` to place GIF at same position as emoji
5. Time `startSec`/`endSec` to match the caption's timing

## Tech Logo

When mentioning a specific tool/platform → set as `bRollOverlays` entry with `position: "bottom"`. Read `workspace/assets/reels/logos/_catalog.json`.

| Caption mentions | Logo file | Label |
|-----------------|-----------|-------|
| claude, anthropic | `claude.webp` | Claude |
| claude code | `claude code.jpeg` | Claude Code |
| chatgpt, gpt, openai | `chatgpt.png` | ChatGPT |
| gemini, google ai | `gemini.svg` | Gemini |
| excel, spreadsheet | `excel.jpg` | Excel |
| nano banana, nano | `nano banana.jpg` | Nano Banana |

To add more logos: place image files in `workspace/assets/reels/logos/` and update `_catalog.json`.
