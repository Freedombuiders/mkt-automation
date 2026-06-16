# Anti-Patterns — Lỗi Thường Gặp

Tổng hợp 24 lỗi đã gặp + cách tránh. SKILL.md tóm tắt HARD RULES; file này chi tiết WHY + cách fix.

## Scene HTML structure

1. **(CORRECTED v1.1)** Scene file load qua `data-composition-src` **ĐƯỢC PHÉP full standalone HTML doc** (`<!doctype html>…<html><head><body>`). Runtime extract element `[data-composition-id]` + scoped style/script — proven render clean. (Inline `<template>` chỉ cần khi embed trực tiếp trong index.html; pipeline này KHÔNG dùng.) Quan trọng: root `<div data-composition-id="scene-N" data-width="1200" data-height="1080">`, CSS scoped, KHÔNG gsap riêng.
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

14. **Hardcoded scene durations** — luôn lấy từ `beats.json` (qua `map_beats.py`). Set TOTAL + data-duration = ffprobe source.mp4 ĐÃ re-encode (không phải alignment.json).
15. **(N/A cho skill này)** Overlap +0.4s crossfade = base-skill only. Skill HeyGen: NO overlap, mount back-to-back, `fromTo opacity 0→1` ở start, scene sau (DOM sau) che scene trước. Overlap + slide-mount width tween = flicker.

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

## HeyGen + master (v1.1 — từ run thật)

25. **Không re-encode HeyGen MP4** — HeyGen = 25fps, keyframe ~8s → renderer warn "sparse keyframes → seek failures / frame freezing", avatar đơ frame. Fix: `prep_source_video.sh reencode raw.mp4 source.mp4` (libx264 -r 30 -g 30 -keyint_min 30). LUÔN làm.
26. **Tin sub-agent báo HeyGen "stuck N phút"** — nó bịa elapsed time. HeyGen KHÔNG stuck nếu `failure_code`=null; render 110s/720p ~10-15 phút. Poll `mcp__heygen__get_video` trực tiếp từ orchestrator.
27. **Block chờ HeyGen** — tạo placeholder (`prep_source_video.sh placeholder`) để lint/inspect/draft-render full composition song song, swap avatar thật sau.
28. **Scene meta-badge đè master brand-mark** — cả 2 ở top-left. Scene meta-badge xuống top:92px left:56px; KHÔNG wordmark top-right (avatar ngồi đó).
29. **Lo lắng PIP stretch** — KHÔNG stretch nếu scene content flex-center intrinsic-width: khi slide-mount tween 1200→1920 content chỉ re-center. Đừng dùng block width:100% bên trong scene.
30. **`#avatar-frame > .avatar-breathing/.avatar-punch` thiếu `data-layout-allow-overflow`** — breathing scale 1.025 vượt clip → inspect flag `container_overflow` (vô hại nhưng noise). Thêm attr.
31. **Master select root bằng `[data-composition-id="main"]`** → lint `composition_self_attribute_selector`. Dùng `#root`.
32. **Wipe/flash thiếu hard-kill** → lint `gsap_exit_missing_hard_kill`. Thêm `tl.set('#scene-flash'/'#scene-wipe',{opacity:0}, t)` sau fade.
33. **Mong `npx hyperframes lint` validate scene** — lint CHỈ check index.html, KHÔNG recurse scene mounted, KHÔNG nhận file path ("Not a directory"). Validate scene qua `inspect` + draft-render frame check.
34. **Sub-agent chạy `npx hyperframes`** — concurrent + asset chưa có = false error. Sub-agent author + self-review only; orchestrator validate tập trung.
