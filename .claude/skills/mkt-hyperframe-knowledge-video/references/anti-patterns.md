# Anti-Patterns — Lỗi Thường Gặp

Tổng hợp 24 lỗi đã gặp + cách tránh. SKILL.md tóm tắt HARD RULES; file này chi tiết WHY + cách fix.

## Scene HTML structure

1. **`<html>/<head>/<body>` wrapper trong scene HTML** — sub-comp loaded via `data-composition-src` phải là `<template>` only. Standalone HTML = broken in runtime.
2. **anime.js** — hyperframes runtime expect GSAP. Bỏ hoàn toàn anime.js.
3. **CSS `animation: ... infinite`** — banned. Convert sang finite GSAP repeat với yoyo, compute từ DURATION.
4. **`Math.random()`** — banned (non-deterministic). Use seeded mulberry32. Mỗi scene 1 seed unique (vd `0x5cNN`).
5. **`gsap.from()` trong sub-comp** — unreliable vì sub-comps load async. Use `gsap.fromTo()` luôn.
6. **Exit animations trong scene** — banned trừ final scene. Master timeline handles transitions.
7. **`<script src=...gsap...>` trong scene HTML** — master index.html load GSAP. Đừng add lại.
8. **Avatar/footer trong scene HTML** — brand stamp chỉ ở master index.html.

## Asset paths

9. **Path `../../../assets/...`** — không work với hyperframes runtime. Copy asset vào `<project>/assets/`.

## Script writing

10. **Em dash trong VO script** — ElevenLabs đọc em dash sai. Dùng comma / period.

## Pattern selection

11. **Forced fit beat content vào pattern không phù hợp** — invent (Approach C) thay vì ép.
12. **Quá 50% scenes có ảnh** — video trông như slideshow. Mix 60/40 motion graphic vs ảnh.

## Design tokens

13. **Không tạo design.md trước** — sub-agents không có source of truth → palette / typography drift.

## Timing

14. **Hardcoded scene durations** — luôn lấy từ `beats.json` (sau alignment).
15. **Không extend scene-mount duration cho crossfade** — scenes back-to-back = jump cut. Extend mỗi scene duration +0.4s để overlap với scene kế tiếp, sau đó tween opacity ở master timeline.

## Rendering

16. **Render qua Playwright per-scene + ffmpeg concat** — KHÔNG. Đó là approach v1 cũ đã bỏ. HyperFrames render trên `index.html` xử lý đầy đủ.

## SFX

17. **Quá nhiều SFX** — cap 1 SFX / 30s. Background music không thuộc skill này.
18. **SFX volume = 1.0** — sẽ át voiceover. Stick 0.4-0.5.

## Title card

19. **Title-card slider có wipe bars / flash** — slider 0-5s đã nhỏ, thêm wipe/flash sẽ che ảnh. Chỉ crossfade sạch + ken-burns scale 1.0→1.05. Đặt wipe/flash CHO SCENE BOUNDARIES không phải slider.

## Brand stamp

20. **Brand stamp avatar 56px** — quá nhỏ, viewer không nhìn ra. Default 112px, handle text 30px mono.

## Transitions

21. **Mọi scene boundary đều flash** — flash là cho "loud" moments (premise hit, big stat, finale). Mặc định 5-6/15 boundaries.
22. **Wipe color không xoay vòng** — 15 wipes cùng coral = monotone. Rotate coral/cyan/cream, alternate LTR/RTL.
23. **`gsap.fromTo()` với scene-mount mà không có `overwrite: 'auto'`** — sẽ conflict với scene's own internal animations. Master timeline tween luôn dùng `overwrite: 'auto'`.

## Layout validation

24. **Slider/showcase không có `data-layout-ignore`** — inspect sẽ flag `clipped_text` vì sum của 4 slide labels > showcase width. Mark showcase + slides với `data-layout-ignore` + `data-layout-allow-overflow`.
