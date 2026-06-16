# Image as In-Scene Thumbnail Proof

Pattern B (xem SKILL.md Step 3.5). Khi scene đã có layout motion-graphic (stats, code block, side-by-side compare), ảnh là 1 framed thumbnail thêm vào để reinforce content. Dùng khi beat cần motion-graphic + bằng chứng visual cùng lúc.

Phân biệt với Pattern A (Image as hero, `image-feature` pattern): pattern A ảnh chiếm phần lớn canvas, là main visual.

## Markup

```html
<div class="proof-thumb" data-layout-allow-overflow>
  <div class="thumb-img-wrap" data-layout-allow-overflow>
    <img src="inputs/03-repo-github.png" alt="" />
  </div>
  <div class="proof-caption">github.com/owner/repo</div>
</div>
```

## CSS

```css
.proof-thumb {
  position: absolute;
  width: 360px; height: 225px;
  border-radius: 14px; overflow: hidden;
  background: rgba(8,12,22,0.6);
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 30px 80px rgba(0,0,0,0.7),
              0 0 0 1px rgba(79,195,247,0.25),
              0 0 36px rgba(79,195,247,0.18);
  transform: rotate(-2deg);
  opacity: 0;
}
.proof-thumb img { width: 100%; height: 100%; object-fit: cover; will-change: transform; }
.proof-caption {
  position: absolute; bottom: -22px; left: 0; right: 0;
  text-align: center;
  font: 500 10px/1 var(--font-mono);
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--accent-cyan);
}
```

## Timeline (entrance + ken-burns drift)

```js
tl.fromTo('.proof-thumb', { opacity: 0, scale: 0.9, y: 20 }, {
  opacity: 1, scale: 1, y: 0,
  duration: 0.8, ease: 'expo.out',
}, ENTRY_TIME);
tl.fromTo('.proof-thumb img', { scale: 1.0 }, {
  scale: 1.06,
  duration: DURATION - ENTRY_TIME - 0.5,
  ease: 'sine.inOut',
}, ENTRY_TIME);
tl.fromTo('.proof-caption', { opacity: 0 }, { opacity: 1, duration: 0.5 }, ENTRY_TIME + 0.3);
```

## SFX sync

`Discord Notification` ở ENTRY_TIME (pop-in moment).

## Layout-allow-overflow quan trọng

KHÔNG quên `data-layout-allow-overflow` trên:
- `.proof-thumb` (vì caption sit OUTSIDE thumb với `bottom: -22px`)
- `.thumb-img-wrap` (vì ken-burns scale làm img bulge ra)
