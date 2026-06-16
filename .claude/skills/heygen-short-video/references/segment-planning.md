# Segment Planning & Duration Constraints

## Segment Types

| Type | When to use | Source |
|------|-------------|--------|
| `avatar` | Direct speaking, opinions, CTA, hooks, explanations | HeyGen avatar clip (lip-sync) |
| `visual` | Concepts, demos, scenarios, metaphors, processes | Grok AI-generated video (6s) |
| `custom` | User-provided b-roll matching this segment's content | User image/video from manifest |
| `prompt-typing` | Speaker reads/shows a prompt, command, text input | Remotion PromptTyping composition |

## Duration Constraints

### Rule 1: HeyGen ≤ 50% total duration
Total avatar segment time must NOT exceed 50% of the video's total duration. If initial planning exceeds 50%, convert avatar segments to visual segments (more Grok scenes) until the ratio is met.

### Rule 2: Short video limits (≤ 40s total)
When total video duration ≤ 40s:
- **≤ 30s**: Max 2 HeyGen avatar segments (≤ 15s total avatar time). Fill remaining with Grok visual scenes.
- **31-40s**: Max 3 HeyGen avatar segments (≤ 20s total avatar time). Fill remaining with Grok visual scenes.

When converting avatar → visual to meet these limits, prioritize keeping avatar for: **hook** (first segment) and **CTA** (last segment). Convert middle segments to visual first.

### Rule 3: Audio source
- **HeyGen avatar clips**: Already contain lip-synced audio. NEVER overlay `audioPath` on avatar clips — their built-in audio IS the voiceover.
- **Grok visual clips**: Have NO useful audio (mute them). For Grok segments, split the original MP3 into segment chunks and set each chunk as the audio source for that segment only.
- **`audioPath`** (top-level prop): ONLY set this when there are Grok/visual segments that need voiceover audio. When set, it mutes ALL clips including HeyGen avatars — so NEVER use it when video is all-avatar.
- **Mixed avatar + Grok videos**: Do NOT use `audioPath`. Instead, let HeyGen clips play their own audio, and attach MP3 segment chunks to Grok-only clips via per-clip `audioPath` or compose audio tracks per segment in Remotion.
- **All-avatar videos (no Grok)**: Do NOT set `audioPath` at all. Each HeyGen clip plays its own lip-synced audio natively.

## Planning Rules

1. Read full SRT to understand story flow
2. Calculate total video duration from SRT
3. **Apply duration constraints** above:
   - Calculate max allowed avatar time (50% of total, or stricter if ≤ 40s)
   - Plan avatar segments within this budget
   - If budget is tight, keep avatar for hook + CTA only, convert all middle segments to visual
4. Identify where **visual illustration** > talking head ("imagine...", "while you sleep...", "the AI automatically...")
5. Keep `avatar` for: personal statements, hooks, CTAs, transitions (within budget)
6. Use `prompt-typing` when: speaker reads a prompt verbatim or shows a command
7. Aim for 3-6+ visual/prompt-typing segments — more visual scenes for shorter videos
8. Each visual segment: 4-8 seconds of audio
9. Visual segments can span multiple SRT entries — group by semantic meaning
10. **Show duration budget** in plan: `Avatar: X.Xs / Y.Ys budget (Z%)`

## Output Format

```
| # | Time | Type | SRT text (summary) | Grok prompt / Avatar note |
|---|------|------|--------------------|---------------------------|
| 1 | 0.0-3.5s | avatar | Hook: "Bạn có biết..." | Avatar front view, energetic |
| 2 | 3.5-9.0s | visual | "...AI tự động chạy..." | [Grok prompt here] |
```
