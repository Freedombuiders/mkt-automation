# Slide design tokens — modern AI / Claude editorial signature

All values here are **production-tested** (extracted verbatim from the canonical 16:9 project at `workspace/content/2026-05-08/loi-ich-claude-ai/`). Don't tweak randomly — the look only holds if everything stays consistent.

## Background & ink

| Token | Hex | Used for |
|---|---|---|
| Slide pane bg | `#000` | `.slide-mount` background, `[data-composition-id]` root |
| Avatar frame inner | `#0a0e18` | `#avatar-frame` background (visible briefly during entrance fade) |
| Body bg overall (optional) | `#070912` | If running standalone outside HF root |
| Ink primary | `#f5f7fa` | Title text, primary heading |
| Ink muted | `#8b94a8` | Sub-label, brand-mark, secondary mono caption |
| Ink body | `#b6bdcc` / `#c4cad6` | Body paragraph, item label |
| White ramp | `rgba(255,255,255,0.04 / 0.08 / 0.10 / 0.30)` | Card inset highlight, borders |

## Modern AI accent palette

Six-color set that defines this skill's identity:

| CSS var | Hex | Default scene archetype |
|---|---|---|
| `--violet` | `#a78bfa` | Pivot / mechanism / "Claude theo kiểu khác" |
| `--cyan`   | `#67e8f9` | Knowledge intro / spec / process |
| `--pink`   | `#f0abfc` | CTA / friendly / conversion |
| `--lime`   | `#a3e635` | Result / saving / payoff / success |
| `--orange` | `#fb923c` | Fail / pain point / objection |
| `--rose`   | `#fb7185` | Strong fail / warning / before-state |

Map by scene `kind`:

| Scene kind | Accent (eyebrow + tier-letter) |
|---|---|
| `hook` (before/after) | `rose` (before) + `lime` (after) |
| `problem` / `fail` | `orange` (chat user) + `rose` (broken-chain stamp) |
| `solution` / `mechanism` | `violet` (orb) + `cyan` (spec) + `lime` (highlight) |
| `recap` / `result` | `lime` (counter `to`) + `cyan` (clients) |
| `cta` | `pink` (terminal + tier-letter) + `lime`/`cyan` (gift gradient tag) |

### Editorial cream (for embedded infographics only)

| Token | Hex | Used for |
|---|---|---|
| Cream paper bg | `#F0EEE6` | Infographic image background |
| Slate ink | `#1f2937` (approx) | Infographic text |

This palette is for the `1.png` `2.png` `3.png` cream infographic images — generated separately via `mkt-broll-image` using Claude AI editorial style. Do NOT use cream as a slide pane background.

## Typography

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
```

| Stack | Font | Used for |
|---|---|---|
| Sans | **Inter** (400, 500, 600, 700, 800, 900) | Body, title, item label |
| Mono | **JetBrains Mono** (400, 500, 700) | Eyebrow chip, code, tier-label, terminal |
| Decorative | **Instrument Serif** italic (load only if needed) | Step numbers, image alt-caption inside slide |

### Title spec (per composition)

```css
.title {
  font-weight: 800;
  font-size: 68px / 72px / 80px / 84px;   /* tune per scene density */
  line-height: 0.96;
  letter-spacing: -0.035em;
  margin: 0;
}
.title .word { display: inline-block; margin-right: 0.18em; will-change: transform, opacity; }
.title .grad-l {
  background: linear-gradient(135deg, #a3e635, #67e8f9);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
```

Title sizes by scene type (tested):

| Scene | Size |
|---|---|
| Hook (short punch) | 84px |
| Problem (chat-stack) | 72px |
| Solution (orb + spec) | 68px (denser content) |
| Recap (counter) | 80px |
| CTA (comment-terminal) | 80px |

Wrap each word in `<span class="word">` so GSAP can stagger-animate. Wrap the keyword/highlight in `<span class="word grad-X">` for gradient text.

### Eyebrow chip spec

The signature element of every scene. Always at the top, above the title:

```css
.eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px; font-weight: 600;
  letter-spacing: 0.22em; text-transform: uppercase;
  color: <accent>;
  display: inline-flex; align-items: center; gap: 12px;
  align-self: flex-start;
}
.eyebrow .live {
  width: 8px; height: 8px; border-radius: 50%;
  background: <accent>;
  box-shadow: 0 0 12px <accent>;
}
```

```html
<span class="eyebrow"><span class="live"></span>BEFORE / AFTER · 1 năm freelance</span>
```

Text rules:
- Always English label first (BEFORE/AFTER, FAIL, PIVOT, RESULT, CTA)
- `·` separator (middle dot)
- Vietnamese context after, lowercase

## Glass card spec

The base building block of every content row:

```css
.row {
  background: rgba(15, 20, 30, 0.55);
  border: 1.5px solid rgba(<accent-rgb>, 0.30);
  border-radius: 18-22px;
  padding: 14-22px 22-28px;
  backdrop-filter: blur(14-20px);
  box-shadow:
    0 0 28-36px rgba(<accent-rgb>, 0.10),
    inset 0 1px 0 rgba(255,255,255,0.04);
  will-change: transform, opacity;
}
```

Border-radius by row size:
- 18px — chat-row, gift-row, client-row (height ~80–120px)
- 20px — tier-row, hero-row (height ~140–180px)
- 22px — counter-row, comment-row (hero of scene, height ~180–220px)

Border-color opacity by row state:
- `0.30` — neutral / default
- `0.40` — emphasized / brand-color row
- `0.45` — hot row (delta tag, broken-chain stamp)

## Tier-letter spec

The neon-glowing big number/letter on the left of every tier-row:

```css
.tier-letter {
  font-weight: 900;
  font-size: 56-88px;
  letter-spacing: -0.04em;
  line-height: 1;
  text-align: center;
  font-variant-numeric: tabular-nums;
  color: <accent>;
  text-shadow:
    0 0 28px rgba(<accent-rgb>, 0.85),
    0 0 12px rgba(<accent-rgb>, 0.6);
}
```

Sizes by content:
- 56px — short labels in dense spec rows (e.g. `∞`)
- 64px — medium standalone (counter row `15h`)
- 76–88px — hero tier-letter (hook before/after `8h` `0h`, CTA `AI`)

For 4-character labels (`100tr`, `15tr`):
- Drop font-size to 38–42px so it fits the 130–140px column width.
- Add `font-family: 'Inter', sans-serif;` (default is already Inter, but make sure `font-variant-numeric: tabular-nums` is set for digit alignment).

## Background glow

Each composition root has a `.bg-glow` div absolutely positioned:

```css
.bg-glow {
  position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse 600px 400px at 30% 35%, rgba(<accent1-rgb>, 0.10), transparent 60%),
    radial-gradient(ellipse 600px 400px at 70% 75%, rgba(<accent2-rgb>, 0.10), transparent 60%);
}
```

Two ellipses placed diagonally, accent colors matching the scene's primary + secondary. Opacity `0.08–0.14` — any higher and it fights the slide content.

## Stage container

```css
.stage {
  position: relative; z-index: 5;
  width: 100%; height: 100%;
  padding: 130px 70px 80px;
  box-sizing: border-box;
  display: flex; flex-direction: column;
  gap: 22-32px;
}
```

- Top padding 130px = leaves room for brand-mark at the root (40 + ~60 height + buffer).
- Bottom padding 80px = avoids cutoff if slide is rendered standalone.
- Side padding 70px = comfortable breathing room at 1200px width.
- Internal gap 22–32px depending on content density.

## Spacing rhythm

| Element gap | Value |
|---|---|
| Eyebrow → title | 32px (default `gap: 32px` on `.stage`) |
| Title → first content row | 12px (margin-top on `.rows`) |
| Row → row | 12–18px (gap on `.rows` flex container) |
| Tier-letter → content (grid column gap) | 18–24px |
| Item icon → label (within `.item`) | 4px |
| Multi-item row gap | 14px |

## Decoration patterns

### Strike-line (used on counter "from" value)

```css
.counter .from { position: relative; }
.counter .from::after {
  content: ""; position: absolute;
  left: -8%; right: -8%; top: 56%;
  height: 4px; background: #fb7185; border-radius: 3px;
  transform: scaleX(0); transform-origin: left center;
  will-change: transform;
}
```

GSAP animation:
```js
tl.fromTo(R + ' .counter .from::after', { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: 'power2.out' }, 1.6);
```

### Broken-chain stamp (used on problem scene)

```css
.broken {
  display: flex; align-items: center; justify-content: center;
  gap: 16px;
  padding: 16px 24px;
  border: 2px dashed #fb7185;
  border-radius: 16px;
  background: rgba(251,113,133,0.08);
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px; font-weight: 700;
  letter-spacing: 0.10em; text-transform: uppercase;
  color: #fb7185;
  backdrop-filter: blur(12px);
  box-shadow: 0 0 30px rgba(251,113,133,0.18);
}
```

Shake animation:
```js
tl.to(R + ' .broken', { x: -8, duration: 0.08, yoyo: true, repeat: 5, ease: 'sine.inOut' }, t);
```

### Iridescent orb (used in solution scene)

```css
.orb {
  width: 130px; height: 130px; border-radius: 50%;
  background: radial-gradient(circle at 32% 30%, #ffffff, #a78bfa 28%, #67e8f9 64%, #f0abfc 100%);
  box-shadow:
    0 0 50px rgba(167,139,250,0.65),
    inset -16px -16px 32px rgba(0,0,0,0.30);
  position: relative;
}
.orb::after {
  content: ""; position: absolute;
  top: 16%; left: 22%; width: 32%; height: 22%;
  border-radius: 50%;
  background: rgba(255,255,255,0.6);
  filter: blur(8px);
}
```

Breathing:
```js
tl.to(R + ' .orb', { scale: 1.04, duration: 1.6, ease: 'sine.inOut', yoyo: true, repeat: 8, transformOrigin: 'center' }, t);
```

### macOS terminal mock (used in CTA scene)

Traffic-light dots `r/y/g`, mono header label, prompt + input + cursor, output block. See `composition-patterns.md` § comment-terminal for full snippet.

### Gift tag (gradient pill)

```css
.gift .tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px; font-weight: 800;
  background: linear-gradient(135deg, #a3e635, #67e8f9);
  color: #0b0f1a;
  padding: 6px 12px; border-radius: 7px;
  letter-spacing: 0.12em;
  text-align: center;
}
```

Used for `FREE`, `NEW`, `2K` style tags. Always lime→cyan or violet→pink gradient.

## Icon strategy

Unlike landing skill (which mandates Lucide SVG), **video compositions use emoji** for icons inside tier-row items:

```html
<div class="item"><div class="ic">✍️</div><div class="lb">Viết content</div></div>
<div class="item"><div class="ic">📧</div><div class="lb">Soạn email</div></div>
```

Reasons:
- Renders pixel-identical in Chromium (HF render engine)
- Zero dependency
- Faster scaffold
- Visually warmer / less corporate at video scale

But emoji wrapped in glass `.ic` container:
```css
.ic {
  width: 60px; height: 60px;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 32px;
  background: rgba(255,255,255,0.04);
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.10);
  filter: drop-shadow(0 0 8px rgba(255,255,255,0.15));
}
```

The container makes them look intentional rather than chat-tier emoji.

## Responsive (none — fixed canvas)

Compositions are **fixed 1200×1080** native (slides) and **1920×1080** root. NO responsive logic. NO media queries. NO viewport units. Everything pixel-anchored.

## Accessibility (production)

- Skip caption mount by default (slide carries the message visually + voiceover audio).
- If user explicitly asks for captions, mount them on top of the slide-mount area (left pane, bottom 200px), NOT over the avatar — uses `mkt-hyperframe-talking-head-video` style word-by-word.
- `prefers-reduced-motion` respect: optionally wrap all GSAP `tl.to` motion in a check. Default skill ignores this — videos are inherently motion content.

## File structure for a composition

Every composition file follows this exact skeleton:

```html
<template id="<scene-id>-template">
  <div data-composition-id="<scene-id>" data-start="0" data-width="1200" data-height="1080">
    <link rel="preconnect" ... />
    <link href="https://fonts.googleapis.com/css2?family=Inter..." rel="stylesheet" />

    <style>
      [data-composition-id="<scene-id>"] { ... }
      [data-composition-id="<scene-id>"] .bg-glow { ... }
      [data-composition-id="<scene-id>"] .stage { ... }
      [data-composition-id="<scene-id>"] .eyebrow { ... }
      [data-composition-id="<scene-id>"] .title { ... }
      [data-composition-id="<scene-id>"] .<row-class> { ... }
    </style>

    <div class="bg-glow"></div>
    <div class="stage">
      <span class="eyebrow"><span class="live"></span><eyebrow-text></span>
      <h1 class="title">
        <span class="word">...</span>
        <span class="word grad-X">...</span>
      </h1>
      <div class="<row-container>">
        <!-- rows -->
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      const R = '[data-composition-id="<scene-id>"]';
      // tl.from(R + ' ...', ...);
      window.__timelines["<scene-id>"] = tl;
    </script>
  </div>
</template>
```

ALL CSS scoped via `[data-composition-id="..."]` prefix — prevents bleed when multiple sub-compositions load in the same DOM.
