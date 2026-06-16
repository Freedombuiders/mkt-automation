# Scene-to-Scene Transitions

Mặc định scene boundaries KHÔNG phải jump cut. Master timeline có **3 transition styles** xoay vòng theo content nhịp.

## Style A — Color wipe (cho boundaries quan trọng)

Bar màu sweep ngang qua canvas, optional brightness flash ở giữa.

### Master HTML

```html
<div id="scene-wipe" class="clip scene-wipe coral"
     data-start="0" data-duration="<total>" data-track-index="55"
     data-layout-ignore data-layout-allow-overflow></div>

<div id="scene-flash" class="clip scene-flash"
     data-start="0" data-duration="<total>" data-track-index="56"
     data-layout-ignore></div>
```

### CSS

```css
#root .scene-wipe {
  position: absolute; top: 0; bottom: 0; left: -200px;
  width: 140px; z-index: 50;
  opacity: 0; pointer-events: none;
}
#root .scene-wipe.coral { background: linear-gradient(90deg, transparent, #d97757 50%, transparent); box-shadow: 0 0 140px 30px rgba(217,119,87,0.55); }
#root .scene-wipe.cyan  { background: linear-gradient(90deg, transparent, #4fc3f7 50%, transparent); box-shadow: 0 0 140px 30px rgba(79,195,247,0.55); }
#root .scene-wipe.cream { background: linear-gradient(90deg, transparent, #faf9f5 50%, transparent); box-shadow: 0 0 140px 30px rgba(255,255,255,0.45); }

#root .scene-flash {
  position: absolute; inset: 0; background: #faf9f5;
  z-index: 51; opacity: 0; pointer-events: none;
  mix-blend-mode: screen;
}
```

Variations: `wipe-coral-ltr`, `wipe-coral-rtl`, `wipe-cyan-ltr`, `wipe-cyan-rtl`, `wipe-cream-ltr`, `wipe-cream-rtl`. Sweep duration 0.55s `power2.inOut`.

## Style B — Push left

Scene cũ trượt sang trái + scale 0.97, scene mới fly in từ phải.

```js
tl.to(id, { x: -120, scale: 0.97, duration: 0.5, ease: 'expo.in', overwrite: 'auto' }, end - 0.05);
tl.fromTo(next, { x: 100, scale: 1.02 }, { x: 0, scale: 1, duration: 0.55, ease: 'expo.out', overwrite: 'auto' }, end);
```

## Style C — Push up + blur

Scene cũ trượt lên + blur, scene mới fly in từ dưới.

```js
tl.to(id, { y: -80, scale: 0.97, filter: 'blur(4px)', duration: 0.5, ease: 'expo.in', overwrite: 'auto' }, end - 0.05);
tl.fromTo(next, { y: 60, scale: 1.02 }, { y: 0, scale: 1, duration: 0.55, ease: 'expo.out', overwrite: 'auto' }, end);
```

## Boundary routing strategy

KHÔNG phải mọi boundary đều cần flash. **Flash chỉ dùng ở "loud" moments**: premise hit, technical reveal, big stat payoff, final CTA. Mặc định 5-6 flash hits trong 15 boundaries.

Color rotation: dùng accent palette từ design.md. Coral cho moments "hyperframes-favored", cyan cho "remotion-favored", cream cho neutral. Đổi direction LTR↔RTL xen kẽ để không monotone.

## Wiring đầy đủ

```js
const transitions = [
  { id: '#m1',  next: '#m2',  end: 17.805,  style: 'wipe-coral-ltr',  flash: true  },
  { id: '#m2',  next: '#m3',  end: 25.527,  style: 'wipe-cyan-rtl',   flash: true  },
  { id: '#m3',  next: '#m4',  end: 61.623,  style: 'push-left',       flash: false },
  { id: '#m4',  next: '#m5',  end: 112.722, style: 'wipe-cream-ltr',  flash: false },
  { id: '#m5',  next: '#m6',  end: 154.238, style: 'push-up',         flash: false },
  // ... rotate the 3 styles + 3 colors + 2 directions
];

transitions.forEach(({ id, next, end, style, flash }) => {
  const t0 = end - 0.18;

  tl.fromTo(id, { opacity: 1 }, { opacity: 0, duration: 0.45, ease: 'power2.inOut', overwrite: 'auto' }, end - 0.05);

  if (style === 'push-left') {
    tl.to(id, { x: -120, scale: 0.97, duration: 0.5, ease: 'expo.in', overwrite: 'auto' }, end - 0.05);
    tl.fromTo(next, { x: 100, scale: 1.02 }, { x: 0, scale: 1, duration: 0.55, ease: 'expo.out', overwrite: 'auto' }, end);
  } else if (style === 'push-up') {
    tl.to(id, { y: -80, scale: 0.97, filter: 'blur(4px)', duration: 0.5, ease: 'expo.in', overwrite: 'auto' }, end - 0.05);
    tl.fromTo(next, { y: 60, scale: 1.02 }, { y: 0, scale: 1, duration: 0.55, ease: 'expo.out', overwrite: 'auto' }, end);
  } else if (style.startsWith('wipe-')) {
    const [, color, dir] = style.split('-');
    tl.set('#scene-wipe', { className: 'clip scene-wipe ' + color }, t0);
    if (dir === 'ltr') {
      tl.fromTo('#scene-wipe', { x: -200, opacity: 0 }, { x: 2120, opacity: 1, duration: 0.55, ease: 'power2.inOut' }, t0);
    } else {
      tl.fromTo('#scene-wipe', { x: 2120, opacity: 0 }, { x: -200, opacity: 1, duration: 0.55, ease: 'power2.inOut' }, t0);
    }
    tl.to('#scene-wipe', { opacity: 0, duration: 0.15, ease: 'power2.out' }, t0 + 0.45);
    tl.fromTo(next, { scale: 1.04 }, { scale: 1, duration: 0.7, ease: 'expo.out', overwrite: 'auto' }, end);
  }

  if (flash) {
    tl.fromTo('#scene-flash', { opacity: 0 }, { opacity: 0.45, duration: 0.08, ease: 'power2.out' }, t0 + 0.18);
    tl.to('#scene-flash', { opacity: 0, duration: 0.22, ease: 'power2.in' }, t0 + 0.26);
  }
});
```

**SFX sync**: nếu dùng `Whoosh`, đặt `data-start` = boundary - 0.1s để Whoosh khớp với wipe sweep peak.

## Common mistakes

- **Mọi boundary đều flash** — flash là cho "loud" moments. Mặc định 5-6/15.
- **Wipe color không xoay vòng** — 15 wipes cùng coral = monotone. Rotate coral/cyan/cream.
- **`gsap.fromTo()` scene-mount thiếu `overwrite: 'auto'`** — conflict với scene's own internal animations.
