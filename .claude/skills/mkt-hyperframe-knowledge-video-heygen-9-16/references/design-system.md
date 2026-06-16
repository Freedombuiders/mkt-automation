# Design System Reference

All compositions share this aesthetic. Authored consistently, it gives
the whole video brand continuity — looks like one cohesive piece rather
than ten unrelated slides.

## Mood

**Dark cinematic keynote.** Inspired by Google I/O 2026 / Antigravity
2.0 / Apple keynote frames. Deep navy → black background with subtle
drifting brand-color particle bokeh. Massive uppercase hero typography
in white cream. Monospace small-caps labels in sky-blue. Glassmorphic
cards with backdrop-blur. Soft radial glow halos behind focal elements.

The aesthetic is **expensive-looking but minimal** — lots of negative
space, restrained color (mostly white + 1 accent per element), no
gradients on text, no stock illustrations. Decorative SVG (icons,
diagrams, charts, metaphor shapes) is welcome — that's where invention
happens. Everything earns its place.

## What's locked vs what's free

**LOCKED** (this is the brand DNA — never deviate):
- Background: dark navy radial per `--bg-radial` token
- Particle bokeh field (5 brand colors drifting)
- Typography: Inter (sans) + JetBrains Mono (mono) only
- Color palette: only the 9 tokens in `tokens.css`
- Meta badge top-left + wordmark top-right on every scene
- Brand stamp (avatar + handle) at concat step bottom-right

**FREE** (sub-agent invents within above):
- Composition, layout, element placement
- Animation choreography (timing, easing, sequence)
- Decorative SVG (icons, diagrams, charts, metaphor shapes)
- Card sizes, shapes, arrangements, counts
- Visual metaphors (timelines, gauges, maps, stacks, splits, etc.)
- Number of elements per scene
- Whether to use cards at all — some scenes don't need cards

## Background

```css
background:
  radial-gradient(ellipse at 30% 20%, rgba(40, 60, 100, 0.35) 0%, transparent 55%),
  radial-gradient(ellipse at 75% 80%, rgba(217, 119, 87, 0.18) 0%, transparent 55%),
  radial-gradient(ellipse at 50% 50%, #0f1626 0%, #050810 70%, #02040a 100%);
```

This stack gives a cool-to-warm pull (cool blue top-left, warm coral
bottom-right) layered over a deep navy radial center. The bokeh particle
field drifts on top.

## Particles

90 dots, 5 brand colors, each ~3-12px with matching `box-shadow` for
glow. Drift over 18s with random offset + opacity sine. Implementation
in `assets/snippets/particle-bokeh.html`. Density rules:

| Density | Particle count | Used for                                 |
|---------|----------------|------------------------------------------|
| Sparse  | 60             | Content-dense (terminal, diff, network)  |
| Normal  | 90             | Default                                  |
| Dense   | 120            | Hero, CTA (visual breathing room)        |

## Typography

**Inter** (sans, 500/700/800/900) — hero text + body. Loaded from
Google Fonts CDN inline.

**JetBrains Mono** (mono, 400/500/600) — eyebrow labels, chips, terminal
content, code lines. Loaded from Google Fonts CDN inline.

| Role           | Font       | Size  | Weight | Tracking | Color           |
|----------------|------------|-------|--------|----------|-----------------|
| Hero           | Inter      | 124px | 900    | -0.035em | cream #faf9f5   |
| Hero accent    | Inter      | 124px | 900    | -0.035em | coral #d97757   |
| Section title  | Inter      | 44px  | 800    | -0.01em  | cream           |
| Body / card    | Inter      | 22px  | 700    | -0.01em  | cream           |
| Caption / desc | Inter      | 14px  | 500    | normal   | cream 70%       |
| Eyebrow label  | JBM        | 22px  | 500    | 0.32em   | sky #7cc4f0     |
| Chip / pill    | JBM        | 11px  | 500/600| 0.18em   | per-accent      |
| Code / terminal| JBM        | 18px  | 500    | normal   | #d8dee9         |
| Code line nums | JBM        | 16px  | 400    | normal   | gutter #555c6b  |

## Color palette

**Foreground**:
- `#faf9f5` cream (Anthropic-style off-white) — primary text
- `#b9c4d4` muted — secondary text
- `#8b95a8` dim — tertiary

**Backgrounds**:
- `#02040a` deep — outermost
- `#050810` navy — body
- `#0f1626` navy-warm — center of radial
- `rgba(20, 28, 46, 0.55)` — card surface (with backdrop-blur)
- `rgba(8, 12, 22, 0.82)` — terminal / code surface (more opaque)

**Brand accents** (rotate across scenes for variety):
- `#4fc3f7` cyan — speed, performance, water
- `#d97757` coral — primary brand accent (Anthropic-style)
- `#ffcb6b` amber — warning, attention, gold
- `#80cbc4` mint — health, success, calm
- `#a78bfa` violet — premium, enterprise
- `#7cc4f0` sky — eyebrow labels (always)
- `#f48fb1` pink — accent variety
- `#66bb6a` green — semantic "fixed" / "OK"
- `#ef5350` red — semantic "broken" / "before"

## Spacing

Everything follows an 8px grid scale: 8, 12, 14, 16, 18, 20, 24, 28, 32,
36, 44, 56, 80, 120. Card padding typically 28-36px. Inter-card gaps
24-36px. Hero margin-bottom 14-24px before underline + 56px before next
element.

## Radii

- `8px` — chips, small buttons, code blocks
- `12px` — terminal windows, small cards
- `18px` — standard cards
- `22px` — large comparison cards
- `999px` — pills

## Effects

**Glassmorphism**: `backdrop-filter: blur(12px)` on cards + low-opacity
fill + soft border.

**Glow halo**: per-card radial in the accent color, 28-40px blur,
30-50% opacity, positioned behind the card via z-index: -1 or ::before
pseudo.

**Text glow** (on stat numbers): `text-shadow: 0 0 40px <accent>` with
a pulse animation that breathes between 40px and 70-100px.

**Cinematic drop-shadow** (on the whole stage): `box-shadow: 0 30px
120px rgba(0,0,0,0.6)` — only on the viewer shell, not inside
compositions (renderer captures composition only).

## Anti-patterns

These ruin the aesthetic — never include:

- Gradient text or rainbow type
- Drop shadows on text (other than glow on stat numbers)
- Decorative emoji
- Stock illustrations or 3D renders
- Gradient backgrounds on cards (use the radial glow + flat surface)
- Multiple typefaces (only Inter + JetBrains Mono)
- Borders thicker than 1px (except hero underline gradient, 4px max)
- Soft pastel everywhere — always have at least one dark navy/black
  region for contrast
