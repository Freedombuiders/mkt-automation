# Scene Patterns — Reference Library, Not Required Menu

11 canonical patterns covering the most common narrative beats in knowledge / news videos. **Use them when the beat genuinely fits — never force a beat into the wrong pattern.**

When a beat doesn't fit, **invent**. Hard constraints: `design.md` (colors, fonts) + particle bokeh + brand stamp ở master. Layout, animation, decorative elements, visual metaphor là creative territory của sub-agent.

**Rule of thumb**: nếu phải twist beat content để fit template → invent. Nếu beat lays out tự nhiên → reuse. Templates save time khi fit honest, không constrain creativity.

## How to use this library

1. **Đọc scene-01 reference** (pre-authored bởi orchestrator) end-to-end để absorb design DNA: `<template>` structure, scoped CSS, mulberry32 PRNG, particle field, focal glow, animation easings.
2. **Đọc `design.md`** cho palette + typography.
3. Decide approach: **reuse / adapt / invent** (xem SKILL.md Step 3).
4. Author scene HTML respect `design.md` tokens; layout freely within that.

## Pattern selection

```
Narrative beat                          → Pattern
──────────────────────────────────────────────────────────
"Big number opener / stats announce"    → hero
"Before vs after / patch fixes"         → diff-window
"6 things to know / headlines"          → card-grid-3x2
"4 categories / 2×2 features"           → card-grid-2x2
"4 items horizontal row"                → card-row-4
"CLI demo / typewriter commands"        → terminal-typewriter
"UI behavior demo (scroll, dialog…)"    → mock-app
"Architecture / data flow"              → network-graph
"A vs B side-by-side"                   → comparison-2card
"Real screenshot / demo image reveal"   → image-feature
"Closing CTA + command"                 → cta-outro
```

If a beat doesn't fit cleanly, prefer `card-grid-2x2` or `card-row-4` as generic fallbacks (they read well for almost any list of features).

## Inventing new compositions (Approach C)

When the beat content doesn't fit any canonical pattern, invent. Here
are concrete beat → invention examples to seed your imagination — these
are NOT templates, they're just demos of what "invention" looks like.

| Beat content | Invented composition idea |
|---|---|
| "In 2023, GPT-4 launched. By 2024, Claude 3.5 was out. In 2025, agents went mainstream." | **Horizontal timeline** — 3 dated nodes connected by a glowing line that draws left-to-right. Year label above each node (JBM large), event label below (Inter 700). Nodes fade in sequentially as the line reaches them. Final node pulses. |
| "100 million users. 40% in Europe, 35% in US, 25% rest of world." | **Radial split** — one massive number center (count-up to 100M), three arc segments around it filling sequentially (40/35/25). Each arc colored per token palette. Tiny region label at end of each arc. |
| "The agent took 47 minutes. The human took 4 hours. Same task." | **Side-by-side bars** — two horizontal progress bars stacking vertically. Top: agent (47m, fills fast in coral). Bottom: human (4h, fills slow in muted). Numbers tick up while bars fill. Final state has clear length disparity. |
| "Every notification you've ignored this week." | **Notification stack cascade** — 6-8 mock notification cards drop in from top in rapid succession, slight rotation per card, settling into a stack at center. Total stack fills ~60% of screen by the end. |
| Long quote with attribution | **Editorial quote layout** — quote text Inter 700 italic at 56px center-aligned (not hero-sized), oversized opening curly quote " in coral at top-left of quote, attribution below in mono small-caps. Subtle vertical line draws left of quote during entrance. |
| "Active in 42 countries." | **World map with pulsing pins** — SVG world map (light stroke), 42 small dots pulse in over 2-3 seconds in different colors from the palette. Count-up label "42" in corner. |
| "Speed jumped from 12 tokens/sec to 89 tokens/sec." | **Speedometer / gauge** — circular arc gauge sweeping from 12 → 89 over 1.5s. Needle animates, value at center counts up. Two zone bands (slow grey, fast coral). |
| "Imagine 10 agents working in parallel." | **Multi-cursor mock IDE** — single code window with 10 colored cursors blinking at different lines, each editing simultaneously. No single dominant cursor — chaotic but coordinated. |
| "Three pillars hold this up: speed, safety, scale." | **Greek temple / 3-column architecture** — abstract column SVG (just 3 vertical bars), label on each, with a roof line drawing across top connecting them. Pillars rise from bottom in sequence. |

### Invention guardrails

These guardrails keep invented scenes brand-coherent:

- **Pick a dominant element** — there's always one focal element
  (a big number, a chart, a diagram, an image, a code block). Don't
  spread visual weight evenly across 5 things.
- **Limit accent colors to 2-3 per scene** — pick from the palette,
  don't introduce new ones.
- **Particle field stays** — even on busy scenes, the background bokeh
  is non-negotiable.
- **Meta badge + wordmark stay** — top-left + top-right.
- **Animation must arrive in waves, not all at once** — entrance
  choreography is what makes scenes feel alive. Stagger by 100-250ms.
- **Don't invent typography** — Inter + JetBrains Mono only. Sizing
  can vary but stay in the token scale.

### When in doubt — pick a metaphor first

Before laying out anything, ask: "What's the physical metaphor for
this idea?" A timeline is a road. A growth stat is a rising line. A
choice is a fork. A network is a constellation. A breakdown is a pie.
A comparison is a versus screen.

Start from the metaphor, then choose the visual primitive (line, arc,
grid, stack, tree, map, gauge…). Then choose the animation
(draw-on, scale-in, count-up, cascade, sweep…). That's a strong scene.

## Sub-agent prompt template

SKILL.md Step 8 đã chứa prompt template chuẩn cho sub-agent (đầy đủ Hard Rules + Process steps). File này KHÔNG duplicate template đó — chỉ liệt kê **pattern-specific extras** mà orchestrator nên inject vào "Content brief" section của prompt.

## Animation rhythm guidelines

Cho beat duration `D` ms, structure timeline:

| Time (ms) | What happens |
|---|---|
| 0 | Particles + BG fade in |
| 400 | Meta badge + wordmark fade in (parallel) |
| 800 | Eyebrow char-typewriter starts |
| 2000 | Hero words stagger reveal |
| 2800-3500 | Main content entrance (cards / window / diagram) |
| `D - 1500` | Subtitle / closing element fades in |
| Throughout | Particles drift, focal-element glow pulse loop |

Hold final composition visible ít nhất 500ms trước khi scene kế tiếp takeover để viewer's eye register.

## Color-accent rotation

Khi scene có multiple cards/items, rotate accents để visual continuity:

`cyan → coral → amber → mint → violet → sky → pink → green`

Tránh 2 scenes liền dùng cùng dominant accent.

## Pattern details

### 1. hero

**Use for**: Opening scene, big stats announcement.
**Anatomy**: eyebrow (small-caps mono) → hero text (massive uppercase, accent word in coral) → underline gradient draw → 3 stat cards (count-up numbers) → subtitle. Particles dense (90-120).
**Typical duration**: 6-9s.
**Sub-agent extras**: 3 stat values (number + label + chip) and accent colors (cyan / coral / amber default).

### 2. diff-window

**Use for**: Before/after, patch notes, fix list.
**Anatomy**: eyebrow + hero on top → mock IDE diff window dominating center → 4 red `-` lines (animated strike-through) → 4 green `+` lines (animated reveal with green glow flash) → "all patched" subtitle.
**Typical duration**: 9-12s.
**Sub-agent extras**: 4 diff pairs (broken behavior → fixed behavior).

### 3. card-grid-3x2

**Use for**: 6 parallel items (headlines, features, top-X).
**Anatomy**: eyebrow + hero on top → 6 cards in 3×2 grid → each card has inline SVG icon (60px, stroke only, per-card accent), title (Inter 700), mono small-caps sub. Stagger scale-in 150-180ms apart.
**Typical duration**: 10-13s.
**Sub-agent extras**: 6 items (icon hint + title + sub + accent color from cyan/coral/amber/mint/violet/pink rotation).

### 4. card-grid-2x2

**Use for**: 4 parallel items, more breathing room than 6.
**Anatomy**: eyebrow + hero → 4 cards in 2×2 grid → each card has icon column on left, title + desc + chip on right. Stagger 200ms.
**Typical duration**: 7-9s.
**Sub-agent extras**: 4 items (icon hint + title + 1-line desc + chip label + accent color).

### 5. card-row-4

**Use for**: 4 items horizontal (when 2×2 feels too "boxed").
**Anatomy**: eyebrow + hero → 4 cards in 1 row → each card has top-left icon, top-right status chip, title, desc, bottom code-style label. Stagger left-to-right.
**Typical duration**: 7-9s.
**Sub-agent extras**: 4 items (icon, chip text, title, desc, mono code label, accent color).

### 6. terminal-typewriter

**Use for**: Demo CLI commands, code examples, "before pipeline / after pipeline".
**Anatomy**: eyebrow + hero up top → mock terminal window (mac chrome, dark surface) → 3-5 commands type out one after another, each followed by green check or "OK". Optional pill callout below for secondary detail.
**Typical duration**: 9-12s. Allow tail past beat duration if commands need time to type.
**Sub-agent extras**: 3-5 command lines, terminal title (e.g. `~/projects/repo · zsh`).

### 7. mock-app

**Use for**: Showing UI behavior (terminal scroll, dialog, URL click).
**Anatomy**: eyebrow + hero → 1 or 2 mock app windows side-by-side showing behavior with animated overlays (arrows, chips, strikethroughs morphing into fixes).
**Typical duration**: 7-9s.
**Sub-agent extras**: Which app to mock (iTerm2, Ghostty, VS Code, browser…), behavior to show, visual overlay morphs from broken → fixed.

### 8. network-graph

**Use for**: Architecture, system connections, data flow with proxy / hub / spoke nodes.
**Anatomy**: eyebrow + hero → central node + 3-4 satellite nodes connected by SVG lines with dash-flow animation → 4 callouts floating around diagram, each tied to one fix.
**Typical duration**: 8-10s.
**Sub-agent extras**: Central node label + satellite labels + 4 callout labels.

### 9. comparison-2card

**Use for**: A vs B (e.g. Vertex AI vs Bedrock, Pro vs Flash).
**Anatomy**: eyebrow + hero → 2 large cards side-by-side → each card has top pill badge, large SVG icon with radial glow halo, title, 2-line feature list, "AVAILABLE NOW" chip at bottom.
**Typical duration**: 6-8s.
**Sub-agent extras**: 2 card titles + 2 pill badges + icon hints + 2 features each + accent colors per card.

### 10. cta-outro

**Use for**: Closing scene — big command + social CTAs.
**Anatomy**: eyebrow → massive command typewriter (`$ <something>`, with verb in coral) → 3 CTA pills (like / comment / subscribe with SVG icons) → big tagline → closing line.
**Typical duration**: 6-8s. The typewriter sets minimum duration.
**Sub-agent extras**: The command to type, 3 CTA labels, the tagline.

### 11. image-feature

**Use for**: Beats referencing a specific real image — screenshot, demo UI, GitHub homepage, chart, photo. The image is focal element.
**Anatomy**: eyebrow + smaller title (Inter 800 56px, not hero 124px — image is star) → large image frame ~80% canvas width, 16:9.5 aspect with soft glow halo, rounded 16px → optional pin annotations anchored to specific points → caption below image (Inter 500, accent-highlighted keywords).
**Typical duration**: 8-11s. Allow extra time for viewer to read / absorb image.
**Sub-agent extras**:
- `image_abs_path` — absolute path to image (set as `<img src>`)
- `image_caption` — 1-2 sentences with strong + accent highlights
- `annotations` (optional) — list of `{label, anchor}` to pin parts of image
- `object-fit`: `cover` for screenshots, `contain` for portraits / full-context shots
