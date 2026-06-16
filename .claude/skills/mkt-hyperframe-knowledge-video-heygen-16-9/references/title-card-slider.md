# Title Card — Image Slider Pattern

Dùng cho **5-6s đầu** khi user đưa input images (Step 1.5 trong SKILL.md). Hook attention bằng visual proof ngay đầu video, thay vì chỉ text centered.

## Layout

- **Title text** pinned top (Inter 900 ~84px), sub mono nhỏ — không dominate canvas
- **Showcase frame** 1280×720px center (`left:320 top:240`), glass border + soft brand-color glow
- **4 slides** = 4 input images fullscreen trong showcase, crossfade
- **Label pill** bottom-left mỗi slide (mono small caps: `REMOTION · GITHUB · 45K STARS`)
- **Progress dots** 4 thin bars under showcase, active dot coral

## Timing (5.4s total, 4 slides)

| t (s) | Event |
|---|---|
| 0.4 | showcase + slide-1 + dots entrance |
| 1.7 | crossfade slide-1 → slide-2 |
| 3.0 | crossfade slide-2 → slide-3 |
| 4.3 | crossfade slide-3 → slide-4 |
| 5.443 | title-card fade-out (master crossfade vào scene-01) |

Mỗi slide entrance: opacity 0→1 trong 0.35s `power2.out`. Ken-burns: image scale 1.0→1.05 trong 1.5s `sine.inOut`.

**KHÔNG dùng wipe bars / flash giữa slides** — chỉ crossfade sạch. Ảnh nhỏ mà thêm hiệu ứng phức tạp sẽ che ảnh.

**SFX sync** (xem `sfx-layer.md`): `camera-flash` ở t=0, `búng tay` ở t=1.7/3.0/4.3.

## Markup

```html
<div class="showcase" data-layout-allow-overflow data-layout-ignore>
  <div class="slide s1" data-layout-allow-overflow data-layout-ignore>
    <img src="inputs/01-image.png" alt="" />
    <div class="label">CATEGORY · DESCRIPTION</div>
  </div>
  <!-- s2, s3, s4 -->
</div>
<div class="dots">
  <div class="dot d1"></div>
  <div class="dot d2"></div>
  <div class="dot d3"></div>
  <div class="dot d4"></div>
</div>
```

## Timeline JS

```js
const slides = [
  { sel: '#title-card .slide.s1', dot: '#title-card .dots .d1', start: 0.4 },
  { sel: '#title-card .slide.s2', dot: '#title-card .dots .d2', start: 1.7 },
  { sel: '#title-card .slide.s3', dot: '#title-card .dots .d3', start: 3.0 },
  { sel: '#title-card .slide.s4', dot: '#title-card .dots .d4', start: 4.3 },
];
slides.forEach((s, i) => {
  tl.fromTo(s.sel, { opacity: 0 }, { opacity: 1, duration: 0.35, ease: 'power2.out' }, s.start);
  tl.fromTo(s.sel + ' img', { scale: 1.0 }, { scale: 1.05, duration: 1.5, ease: 'sine.inOut', overwrite: 'auto' }, s.start);
  if (i < slides.length - 1) {
    tl.to(s.sel, { opacity: 0, duration: 0.35, ease: 'power2.in' }, slides[i + 1].start - 0.05);
  }
  tl.fromTo(s.dot, { backgroundColor: 'rgba(255,255,255,0.18)' }, { backgroundColor: '#d97757', duration: 0.1 }, s.start);
  if (i < slides.length - 1) {
    tl.to(s.dot, { backgroundColor: 'rgba(255,255,255,0.18)', duration: 0.1 }, slides[i + 1].start);
  }
});
```

## Fallback

Nếu KHÔNG có input images → title card chỉ text centered. Đơn giản hơn, vẫn OK.

## Layout-ignore quan trọng

Showcase + slides phải có `data-layout-ignore` + `data-layout-allow-overflow`. Inspect sẽ flag `clipped_text` vì sum của 4 slide labels > showcase width — flag sai.
