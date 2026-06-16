# Pattern selection — which composition for which scene archetype

## Default mapping (5-scene knowledge skeleton)

| Scene archetype | Variant | Composition id | Use when |
|---|---|---|---|
| Hook (`kind: hook`) | `tier-row` | `fs-lesson-1` | Script opens with a "trước đây vs giờ" / "before vs after" contrast. 2 tier rows show the gap. |
| Problem (`kind: problem`) | `chats-stack` | `fs-lesson-2` | Script lists how multiple alternatives fail. User row + 2-3 AI fail rows + broken-tag. |
| Solution (`kind: solution`) | `hero-orb` | `fs-lesson-3` | Script introduces ONE tool with 3 distinguishing specs. Glowing orb + task tiles + 3 spec tier rows. |
| Recap (`kind: recap`) | `counter-row` | `recap-card` | Script reveals a numerical result. Big counter (FROM → TO) + clients + delta. |
| CTA (`kind: cta`) | `terminal-row` | `fs-cta` | Script asks user to comment X. Tier-letter "X" + terminal mockup + 2 gift cards. |

## Decision tree (when default doesn't fit)

### Hook is NOT before/after

If the hook is a single bold question or claim (no contrast):
- Switch variant to `hero-orb` with a single hero metaphor (orb + tiles).
- Or use `tier-row` but make `before_items` empty and put everything in `after_items`.

### Problem is NOT multi-AI

If the problem section is a single point of pain (not "AI X fails, AI Y fails too"):
- Switch to `tier-row` with `before` = problem state and `after` = "still no answer".
- Keep `chats-stack` for genuine "I tried X, I tried Y" content.

### Solution has more than 3 specs

`hero-orb` template renders up to 3 spec rows (s1/s2/s3 styling). For 4+:
- Either consolidate (merge similar specs)
- Or extend the template to add `s4` (matching `s2` cyan styling)

### Recap is NOT counter-style

If the recap is a list of results (not a single number transformation):
- Switch to `tier-row` with both rows as positive (after-style) results
- Keep `counter-row` for FROM → TO numerical recaps

### CTA is NOT a comment keyword

If the CTA is "follow", "save this", or "DM me":
- Replace `keyword` with the actual CTA word
- Or switch to `tier-row` with a clear "DO THIS" tier-letter

## Variant rotation across scene order

The default 5-scene skeleton (hook→problem→solution→recap→cta) gives a built-in visual rotation:
- Cyan (hook) → Orange (problem) → Violet (solution) → Lime (recap) → Pink (CTA)

Each variant has a distinct accent color. DO NOT assign the same eyebrow color to two adjacent scenes — it breaks visual rhythm and viewers can't feel the section transitions.

## Custom variants

Adding a 6th composition? Create `composition-<name>.html.j2` in `assets/templates/` mirroring one of the existing templates' structure, then add a row to the `KIND_TO` dict in `generate_compositions.py`. Keep the template self-contained (CSS scoped to `[data-composition-id="..."]`, GSAP block at end, internal timeline relative to 0).
