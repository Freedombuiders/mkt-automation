# Infographic prompt template — cream-paper editorial for 16:9 video

Adapted from `mkt-landing-presentation-style/references/infographic-prompt-template.md` for **video context** — same Claude AI editorial signature style, but tuned to 7 short-video beat archetypes.

The infographic image (`1.png` `2.png` `3.png` …) is embedded inside a slide composition via `<img>` slot (see `composition-patterns.md` § image-slot). When the file exists in the workspace folder, it renders. When missing, a dashed placeholder shows.

## Why this style for video

Three visual languages coexist in one frame:
1. **Slide pane** — dark `#000` modern AI futurist (cyan/violet/lime/pink glass cards).
2. **Avatar** — HeyGen face (warm skin, neutral background).
3. **Cream infographic** — `#F0EEE6` warm cream paper, hand-drawn editorial (Claude AI marketing aesthetic).

The cream paper inside the dark slide reads as an "embedded artifact" — like a page torn from a notebook held up against a futuristic tech backdrop. This contrast is the signature visual hook.

## Hard rules (always apply)

| Rule | Spec |
|---|---|
| Background | warm cream `#F0EEE6` — modern matte cream, **NOT** parchment, **NOT** vintage, **NOT** aged texture |
| Illustration | hand-drawn editorial line art with subtle warm color fills — confident strokes, modern, polished, like New Yorker spot illustration |
| Visual thinking | every image must have a clear visual metaphor (see archetypes below) |
| Text language | ALL text in image is Vietnamese with full diacritics — only brand names + tech terms + currency/math symbols stay English |
| Exception language | brand names (CLAUDE, ANTHROPIC, OPENAI, MIT, GPT…), tech (TERMINAL, API, CLI, SDK…), inline code (`$ claude`), math/currency ($, %, ×, ₫, →) |
| Aspect | **16:9 default** (AI33 / Nano Banana Pro do not support 16:10) |
| Typography | bold modern serif-sans hybrid for title (Tiempos Headline / Inter Display feel), neat sans-serif for annotations, monospace for tech labels |
| Palette | cream bg + dark slate text + brand color + accent (green `#3FCF8E` saving / amber `#F4B860` highlight) |
| File name | `1.png`, `2.png`, `3.png` (sequence order in video, not by content) |
| Resolution | 2K minimum (~2048×1152) so it stays sharp at 1920×1080 video render |

## Skeleton prompt (fork & fill)

```
Editorial infographic in Claude AI signature style, 16:9 aspect ratio. Warm cream background (#F0EEE6) with very subtle paper grain — modern matte cream like Claude AI's marketing pages, NOT parchment, NOT vintage, NOT aged texture. Hand-drawn but clean and confident line illustrations with subtle warm color fills, like a thoughtful New Yorker spot illustration. Generous whitespace, considered composition, friendly intelligent feel.

ALL on-image text in VIETNAMESE WITH FULL DIACRITICS — only brand names ({{BRAND_LIST}}) and {{TECH_OR_SYMBOLS}} stay in English.

TYPOGRAPHY:
• Title in bold modern serif-sans hybrid (Tiempos Headline / Inter Display feel), dark slate text: "{{TITLE_VI}}".
• Subtitle below in lighter weight grey: "{{SUBTITLE_VI}}".
• Annotation labels in neat sans-serif, dark slate ink with handwritten warmth.

{{LAYOUT_DESCRIPTION — describe layout block by block, color accents per block, visual metaphor used, exact Vietnamese text in each label}}

{{DECORATIVE_ELEMENTS — small floating annotation tags with curved hand-drawn connector lines, optional doodle icons (gear, lightning bolt, dollar with strikethrough)}}

Visual style: hand-drawn editorial line illustration in Claude AI marketing aesthetic — confident strokes on warm cream paper, modern minimal feel, NOT parchment, NOT vintage, NOT photorealistic. Palette: cream background (#F0EEE6), dark slate text, {{BRAND_1_NAME}} {{BRAND_1_HEX}}, {{BRAND_2_NAME}} {{BRAND_2_HEX}}, accent {{ACCENT_USE_CASE}} {{ACCENT_HEX}}. Warm, intelligent, considered.
```

## 7 video beat archetypes — ready-to-use prompts

Each archetype maps a common short-video moment to a metaphor and includes a fully-written prompt example. Copy, replace topic-specific details, paste into `mkt-broll-image`.

### Archetype 1 — BEFORE / AFTER (Hook payoff)

**Metaphor:** Đồng hồ cát đầy ↔ vơi (fullness drains away — time savings).

**When:** Hook scene's "trước đây ___ / giờ ___" moment.

**Example prompt (Image #1 — Lessons "8h → 0h"):**

```
Editorial infographic in Claude AI signature style, 16:9 aspect ratio. Warm cream background (#F0EEE6) with very subtle paper grain — modern matte cream like Claude AI marketing pages, NOT parchment, NOT vintage. Hand-drawn editorial line art with subtle warm fills.

ALL on-image text in VIETNAMESE WITH FULL DIACRITICS — only "AI" stays English.

TYPOGRAPHY:
• Title (top-left): "TRƯỚC ĐÂY · 8 TIẾNG / NGÀY" in bold modern serif-sans, dark slate ink.
• Title (right): "BÂY GIỜ · NGỦ DẬY LÀ XONG" in same style, with the word "XONG" in green #3FCF8E.

LEFT BLOCK (red-rose accent #FB7185, "trước đây" — exhausted past):
• Hand-drawn hourglass FULL of sand at top — exaggerated proportions, warm red-rose fill on the sand, dark slate outline. Visual metaphor: time piling up endlessly.
• Below, 4 small icon doodles in a horizontal row: pen scribbling on paper ("viết content"), envelope ("soạn email"), open book ("đọc tài liệu"), bar chart ("tổng hợp BC"). Each labeled in Vietnamese underneath in sans-serif.
• A small floating annotation tag with curved connector line: "8 tiếng — hết ngày."

CENTER:
• Big bold dark slate arrow curving from left to right with the label "AI" in a green pill #3FCF8E above.

RIGHT BLOCK (lime-green accent #A3E635, "bây giờ" — restful payoff):
• Hand-drawn hourglass NEARLY EMPTY — sand at the bottom, top mostly clear. Light green fill on remaining sand. Above the hourglass, a small crescent moon and "06:30" timestamp in monospace.
• 3 task cards stacked: "Bản nháp ✓", "Báo cáo ✓", "Email ✓" — each with green checkmark.
• Annotation tag: "Sáng dậy — sẵn sàng duyệt."

Decorative: tiny dotted connector lines between blocks, small "Z Z Z" doodle near the moon, friendly arrow curling around the green pill.

Visual style: hand-drawn editorial line illustration in Claude AI marketing aesthetic — confident strokes on warm cream paper, NOT parchment, NOT vintage. Palette: cream #F0EEE6, dark slate text, rose #FB7185, lime green #A3E635 + accent #3FCF8E. Warm, intelligent, considered.
```

---

### Archetype 2 — FAIL (Problem scene metaphor)

**Metaphor:** ⛓️‍💥 broken chain / cốc đầy tràn / dây diều bị đứt — interrupted flow.

**When:** Problem scene where "tools fail mid-task".

**Example prompt:**

```
Editorial infographic in Claude AI signature style, 16:9 aspect ratio. Warm cream background (#F0EEE6), modern matte cream, NOT parchment.

ALL text in Vietnamese with full diacritics — brand names (CHATGPT, GEMINI) stay English.

TYPOGRAPHY:
• Title: "GIAO VIỆC — RỒI ĐỨT MẠCH" in bold modern serif-sans, dark slate.
• Subtitle: "Hỏi đáp ổn — giao việc dài thì quên giữa chừng" in lighter grey.

CENTER LAYOUT:
• A long hand-drawn chain stretching horizontally across the canvas, dark slate strokes with subtle metallic grey fill.
• At the center of the chain, ONE link is visibly broken — exaggerated split, small motion lines around the break, a tiny "💥" doodle.
• Above the broken link, a Vietnamese annotation in handwritten warmth: "Đứt mạch — phải nhắc lại từ đầu."

LEFT END (orange #FB923C — user side):
• A small character figure (simple line silhouette) holding the chain end, with a speech bubble: "Tổng hợp tài liệu này cho mình…"

RIGHT END (rose #FB7185 — AI side):
• A small AI box icon (rectangle with antenna), holding the broken end of the chain, with a speech bubble: "Xin lỗi… tôi không nhớ tin nhắn trước."

Below the chain, two small chat-bubble icons labeled "CHATGPT" and "GEMINI" with an X mark next to each.

Bottom annotation tag: "Không nhớ context — phải dán lại — mệt cái đầu."

Decorative: small dotted lines tracing where the chain "should have been continuous", tiny doodle question marks floating around the break.

Visual style: hand-drawn editorial line illustration, warm cream paper. Palette: cream #F0EEE6, dark slate, orange #FB923C, rose #FB7185, accent grey #8B94A8. NOT parchment, NOT vintage.
```

---

### Archetype 3 — PIVOT (Solution intro / "Cho đến lúc mình thử ___")

**Metaphor:** Ngã ba đường / cánh cửa mở / chìa khoá mới — discovery moment.

**Example prompt:**

```
Editorial infographic in Claude AI signature style, 16:9 aspect ratio. Warm cream background (#F0EEE6).

ALL Vietnamese with diacritics — brand "CLAUDE" stays English.

TYPOGRAPHY:
• Title: "CHO ĐẾN LÚC MÌNH THỬ CLAUDE" in bold serif-sans, dark slate, with "CLAUDE" in Claude orange #DA7756.
• Subtitle: "Không phải hỏi đáp — mà giao việc."

CENTER LAYOUT:
• A hand-drawn fork-in-the-road scene from a top-down friendly perspective.
• LEFT path (faded grey, "đã đi rồi"): a winding road with worn arrow signs labeled "CHATGPT", "GEMINI", "HỎI ĐÁP". The road curves back on itself, ending in a frowning face emoji-style scribble.
• RIGHT path (bright Claude orange #DA7756, "đường mới"): a clean straight road forward with a glowing arrow. At the start, a small open door icon with warm light spilling out. Labeled "GIAO VIỆC TỰ CHẠY".
• At the fork center, a small character silhouette pausing, looking right.

Annotation tags:
• Left path: "Nhắc lại từng câu" + small ⛓️‍💥 doodle.
• Right path: "Giao một lần — tự xong" + small ✓ doodle.
• Right of fork: "Cùng một việc — cách dùng khác hẳn."

Decorative: tiny dotted lines fading from left path, brighter solid lines on right path. Small gear-and-pipe doodle near the open door.

Visual style: hand-drawn editorial, warm cream paper. Palette: cream #F0EEE6, dark slate, Claude orange #DA7756, faded grey #B6BDCC. NOT parchment.
```

---

### Archetype 4 — DIFF / MECHANISM (How it works)

**Metaphor:** Diagram flow Claude orb → outputs (input → core → multi-output).

**Example prompt:**

```
Editorial infographic in Claude AI signature style, 16:9 aspect ratio. Warm cream #F0EEE6.

ALL Vietnamese — brand "CLAUDE" stays English.

TYPOGRAPHY:
• Title: "CLAUDE — GIAO VIỆC, NÓ TỰ CHẠY" in bold serif-sans, dark slate, "CLAUDE" highlighted with subtle orange #DA7756 underline doodle.
• Subtitle: "Một lần ingest — nhiều lần output."

CENTER LAYOUT (left-to-right flow):
• LEFT INPUT BLOCK: A hand-drawn stack of papers labeled "100 TRANG TÀI LIỆU", with small arrow pointing right. Above it, a small label "Đầu vào".
• CENTER NODE: A large iridescent orb (Claude orb metaphor) — circular gradient from white center to soft orange #DA7756 edge, with a subtle glow halo. Labeled "CLAUDE" in monospace below the orb. Small "ingest 1 lần" annotation tag with curved connector to the input stack.
• RIGHT OUTPUT FAN: 4 small artifacts radiating outward like a hand of cards: "BẢN NHÁP" (pen icon), "BÁO CÁO" (chart icon), "EMAIL" (envelope icon), "TÓM TẮT" (list icon). Each connected to the orb with soft hand-drawn line.
• Below the output fan: small annotation "Mỗi output — chỉ tốn 1 prompt."

3 spec callouts at the bottom (3-column row, each a tiny card):
• "∞ Nhớ cuộc trò chuyện dài"
• "100tr Đọc tài liệu một lần"
• "🌙 Tự bấm máy thay mình"

Decorative: tiny radiating dots around the orb, subtle gear icon in the corner.

Visual style: hand-drawn editorial, warm cream paper. Palette: cream #F0EEE6, dark slate, Claude orange #DA7756, accent green #3FCF8E for output checks. NOT parchment.
```

---

### Archetype 5 — RESULT / NUMBER PROOF (Recap scene)

**Metaphor:** Heo đất vỡ vs két sắt nhỏ / cân nghiêng / bậc thang lên — concrete change.

**Example prompt:**

```
Editorial infographic in Claude AI signature style, 16:9 aspect ratio. Warm cream #F0EEE6.

ALL Vietnamese — currency symbols ($, ₫) stay English.

TYPOGRAPHY:
• Title: "TUẦN ĐẦU · TIẾT KIỆM 15 TIẾNG" in bold serif-sans, dark slate, "15 TIẾNG" in lime green #A3E635.
• Subtitle: "Tháng sau — thêm 2 khách hàng mới."

LEFT BLOCK (rose #FB7185 — "before, exhausted"):
• Hand-drawn cracked piggy bank, pinkish-rose fill, small cracks, a single coin still falling out. Label below: "40 TIẾNG / TUẦN" with a strike-through line in rose color.
• Small annotation: "Đầu tuần đã mệt."

CENTER:
• Big bold dark slate arrow curving from left to right.
• Above the arrow: a small "−15h" pill in lime green #A3E635.

RIGHT BLOCK (lime #A3E635 — "after, restful"):
• Small intact safe / treasure chest with a gold coin on top, lime green accent on the lid. Label: "25 TIẾNG / TUẦN" in dark slate with a green checkmark.
• Beside the safe, two tiny figure silhouettes labeled "Khách mới #1", "Khách mới #2" each with a "SIGNED" green badge.
• Small annotation: "Cuối tuần vẫn khoẻ."

Bottom: a wide green pill with "−15h/tuần · +2 khách · 0 hire thêm" in monospace.

Decorative: tiny doodle hour symbols floating, faded "₫₫₫" coins near the piggy bank.

Visual style: hand-drawn editorial, warm cream paper. Palette: cream #F0EEE6, dark slate, rose #FB7185, lime #A3E635, accent gold for coins. NOT parchment.
```

---

### Archetype 6 — CTA / GIFT (Closing scene)

**Metaphor:** Mũi tên ↓ + thư mời / quà — directing action.

**Example prompt:**

```
Editorial infographic in Claude AI signature style, 16:9 aspect ratio. Warm cream #F0EEE6.

ALL Vietnamese — "AI" stays English.

TYPOGRAPHY:
• Title: "COMMENT 'AI' — MÌNH GỬI" in bold serif-sans, dark slate, "'AI'" in pink #F0ABFC.
• Subtitle: "Cách giao việc cho Claude — prompt thật, workflow thật."

CENTER LAYOUT:
• A large open envelope facing the viewer (3/4 perspective), warm peach interior, dark slate outline. Inside, two small folded letters peeking out:
  • Letter 1 (cyan #67E8F9 fold): "Cách dùng Claude — làm việc thay mình"
  • Letter 2 (lime #A3E635 fold): "Prompt + quy trình giao việc cụ thể"
• Above the envelope, a hand-drawn ribbon banner with "FREE" in monospace bold.

LEFT (the comment action):
• A speech bubble labeled "AI" with a typing cursor "|" inside. Below: "👇 Chỉ 2 ký tự."

RIGHT (the delivery promise):
• A small downward arrow pointing into the viewer's lap, with an annotation tag: "Mình gửi thẳng — không spam."

Bottom CTA strip: monospace text "👇 LƯU VIDEO · COMMENT AI 👇" in pink #F0ABFC on a subtle pink-tinted band.

Decorative: tiny floating heart and sparkle doodles around the envelope. Curved connector line from the speech bubble to the envelope.

Visual style: hand-drawn editorial, warm cream paper. Palette: cream #F0EEE6, dark slate, pink #F0ABFC, accent cyan #67E8F9, lime #A3E635. NOT parchment, NOT vintage.
```

---

### Archetype 7 — COMPARISON (When to use which)

**Metaphor:** 2 cột song song với cân nghiêng / 2 cánh cửa.

**Example prompt:**

```
Editorial infographic in Claude AI signature style, 16:9 aspect ratio. Warm cream #F0EEE6.

ALL Vietnamese — brand names stay English.

TYPOGRAPHY:
• Title: "DÙNG CÁI NÀO — KHI NÀO?" in bold serif-sans, dark slate.
• Subtitle: "Cả hai đều đúng — chỉ là tuỳ việc."

CENTER LAYOUT (2-column split with subtle vertical divider):

LEFT COL (cyan #67E8F9 accent — "{{TOOL_A}}"):
• Small icon at top: zap / lightning bolt, cyan filled.
• Below: "{{TOOL_A}}" in bold dark slate.
• 3 hand-drawn bullet items, each with a green ✓:
  • "{{USE_CASE_A1}}"
  • "{{USE_CASE_A2}}"
  • "{{USE_CASE_A3}}"

VERTICAL DIVIDER:
• A thin dashed line down the middle. At the center, a small "VS" pill in dark slate.

RIGHT COL (pink #F0ABFC accent — "{{TOOL_B}}"):
• Small icon at top: sparkle, pink filled.
• "{{TOOL_B}}" in bold dark slate.
• 3 bullet items with green ✓:
  • "{{USE_CASE_B1}}"
  • "{{USE_CASE_B2}}"
  • "{{USE_CASE_B3}}"

BOTTOM COMBO BANNER:
• A wide pill spanning both columns, dark slate text on a soft amber #F4B860 band: "Combo tốt nhất — dùng A để hỏi nhanh, B để giao việc dài."

Decorative: small handshake doodle in the bottom margin tying the two columns.

Visual style: hand-drawn editorial, warm cream. Palette: cream #F0EEE6, dark slate, cyan #67E8F9, pink #F0ABFC, accent amber #F4B860. NOT parchment.
```

---

## Mapping cheat sheet — script beat → archetype → file

When outlining `scenes-outline.json`, decide for each scene whether an infographic helps. Default: not every scene needs one. Sweet spot is 1–3 infographics per video.

| Scene `kind` | Archetype | Filename slot |
|---|---|---|
| `hook` (before/after) | Archetype 1 (đồng hồ cát) | `1.png` |
| `problem` (fail) | Archetype 2 (broken chain) | `2.png` (or skip — chats-stack alone is dense) |
| `solution` (mechanism) | Archetype 3 (fork) or Archetype 4 (orb flow) | `2.png` or `3.png` |
| `recap` (result) | Archetype 5 (heo đất / két sắt) | `3.png` |
| `cta` | Archetype 6 (envelope + ribbon) | usually skip — terminal pattern is enough |
| `comparison` | Archetype 7 (2 col + cân) | next available number |

## Workflow

1. Read scene context from `scenes-outline.json`.
2. Pick archetype from cheat sheet above.
3. Pick metaphor — verify it's everyday-recognizable in Vietnamese culture.
4. Plan layout block-by-block (don't let the AI improvise).
5. Write all Vietnamese labels with diacritics — every label, every annotation.
6. Specify exact hex colors for each block.
7. Save full prompt to `prompts.md` (file under workspace folder).
8. Optionally generate via `mkt-broll-image`:

```bash
python3 .claude/skills/mkt-broll-image/scripts/generate.py \
  '<PROMPT_<2K_CHARS>' \
  -o workspace/content/YYYY-MM-DD/<slug>/N.png \
  -ar 16:9 -p ai33 --size 2K -v
```

⚠️ **Prompt length cap**: AI33 returns `temporary_model_error` if prompt > ~2000 chars. For auto-gen, trim to ~1500–2000 chars: keep layout description + visual metaphor + brand colors, drop redundant style adjectives.

⚠️ **Aspect**: 16:9 only on AI33. Output ~1344×768 (2K). HTML slot uses `aspect-ratio: 16/9`.

## prompts.md output format

```markdown
# Image prompts — {{VIDEO_TITLE}}

Tổng cộng N ảnh. Đặt tên `1.png`, `2.png`, ..., `N.png` cùng folder. HTML tự load qua `<img onerror="this.remove()">`.

## 1.png — {{SHORT_TITLE_VI}}

[Aspect: 16:9 · Provider: AI33 / Nano Banana Pro · Resolution: 2K · Used in: scene-1 fs-hook]

{{FULL_PROMPT_TEXT}}

---

## 2.png — {{SHORT_TITLE_VI}}

[Aspect: 16:9 · Provider: AI33 / Nano Banana Pro · Resolution: 2K · Used in: scene-3 fs-solution]

{{FULL_PROMPT_TEXT}}

---
```

## Anti-patterns (avoid)

- Vintage parchment, aged paper, Da Vinci style — user has rejected this consistently.
- Photorealistic 3D render — breaks the editorial feel.
- Generic "infographic of X vs Y" prompts — AI will improvise unpredictably.
- English-only on-image text — must be Vietnamese with diacritics.
- Brand colors written as "blue and orange" — must be hex.
- Skipping the visual metaphor — image will come back abstract.
- Aspect 16:10 — AI33 doesn't support; use 16:9.
- Filename based on content (`piggy-bank.png`) — must be `N.png` ordinal.
