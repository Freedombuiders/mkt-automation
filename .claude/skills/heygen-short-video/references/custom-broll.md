# Custom B-roll Media

Users often have specific images or videos they want shown at certain moments — screenshots of articles, GitHub repos, app UIs, product demos, etc. These replace Grok visual segments with user-provided media, giving more authentic and contextual visuals.

## When to ask

After Step 1 (transcription) and before Step 2 (segment planning), ask:

> Bạn có ảnh hoặc video nào muốn dùng làm cảnh trám không?
> (Ví dụ: screenshot bài báo, giao diện GitHub, demo app...)
> Nếu có, tạo 1 file text mô tả theo format sau rồi đưa path cho mình:
>
> ```
> /path/to/screenshot.png | Bài báo TechCrunch về Claude AI ra mắt tính năng mới
> /path/to/github-repo.png | Thư viện GitHub anthropic-sdk với 50k stars
> /path/to/demo.mp4 | Video demo chạy Claude Code trên terminal
> ```
>
> Mỗi dòng: `đường dẫn file | mô tả nội dung`. Mình sẽ tự động ghép vào đúng chỗ phù hợp trong video.

If user says no or skips, proceed normally with Grok-only visuals.

## Manifest format

One line per media item: `file_path | description`

- **file_path**: absolute or relative path to image (.png, .jpg, .jpeg, .webp) or video (.mp4, .mov)
- **description**: brief Vietnamese/English description of what the media shows and when it should appear

## How to match custom media to segments

After reading the SRT transcript in Step 2:

1. **Parse the manifest** — read each line, split by `|`, validate file exists
2. **Semantic matching** — compare each media description against SRT text to find the best-fit segment. Look for keyword overlap, topic alignment, and contextual relevance. For example:
   - Media: "Thư viện GitHub claude-code" → matches segment discussing "claude-code trên GitHub"
   - Media: "Bài báo về AI Agent" → matches segment mentioning "tin tức mới về AI Agent"
3. **Mark matched segments as `custom`** type (not `visual`/`grok`) in the plan table
4. **Remaining visual segments** (unmatched by custom media) become Grok prompts as usual
5. If the user provides more custom media than visual segments, add extra visual segments where contextually appropriate (split longer avatar segments)

## Handling in production

- **Images**: Convert to a clip with static display. In Remotion props, use `imagePath` instead of `videoPath`:
  ```json
  { "imagePath": "media/custom/screenshot-1.png", "durationSeconds": 5.5 }
  ```
  Remotion displays the image full-screen (object-fit: cover) for the segment duration with the same zoom/effects as video clips.

- **Videos**: Trim to segment duration with ffmpeg, same as Grok videos:
  ```bash
  ffmpeg -i "<custom_video>" -t <segment_duration> -c copy "<output_path>"
  ```

- **Audio**: Same rule as Grok segments — custom media clips have no useful audio. Split the original MP3 for voiceover on these segments.

- **Copy to Remotion**: Place in `media/custom/` (inside the reels assets folder, which is symlinked as Remotion's `public/media/`):
  ```bash
  mkdir -p workspace/assets/reels/custom
  cp <custom_files> workspace/assets/reels/custom/
  ```
