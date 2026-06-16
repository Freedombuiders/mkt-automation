# Composition patterns — landscape 1200×1080

8 reusable section archetypes. Every snippet here is **production-shipped** in `workspace/content/2026-05-08/loi-ich-claude-ai/compositions/` — copy, paste, edit text + accent colors only.

Each pattern:
- HTML markup
- Scoped CSS
- GSAP timeline
- Recommended accent
- Recommended voiceover beat

## Table of contents

1. [tier-row before-after (Hook)](#1-tier-row-before-after-hook)
2. [chats-stack with broken-chain stamp (Problem)](#2-chats-stack-problem)
3. [hero-orb + spec-trio (Solution)](#3-hero-orb--spec-trio-solution)
4. [counter-row (Recap)](#4-counter-row-recap)
5. [comment-terminal (CTA)](#5-comment-terminal-cta)
6. [stats 3-card landing-style](#6-stats-3-card)
7. [comparison 2-column](#7-comparison-2-col)
8. [embedded infographic image-slot](#8-image-slot)

All patterns share the same **scaffolded skeleton** (eyebrow + title + content + GSAP tl). Only the content section + accent change.

---

## 1. tier-row before-after (Hook)

**When:** Hook scene with before/after contrast (8h → 0h, $62 → $0.02, 100 trang → 1 lần).

**Accent:** `rose` (before) + `lime` (after). Or `orange`/`cyan`. Always negative-positive pair.

**Voiceover beat:** "Trước đây mình ___ . Giờ mình ___ ."

```html
<template id="fs-hook-template">
  <div data-composition-id="fs-hook" data-start="0" data-width="1200" data-height="1080">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />

    <style>
      [data-composition-id="fs-hook"] { width: 100%; height: 100%; background: #000; color: #f5f7fa; position: relative; overflow: hidden; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }
      [data-composition-id="fs-hook"] .bg-glow { position: absolute; inset: 0; z-index: 0;
        background: radial-gradient(ellipse 600px 400px at 30% 35%, rgba(251,113,133,0.10), transparent 60%),
                    radial-gradient(ellipse 600px 400px at 70% 75%, rgba(163,230,53,0.10), transparent 60%); }
      [data-composition-id="fs-hook"] .stage { position: relative; z-index: 5; width: 100%; height: 100%; padding: 130px 70px 80px; box-sizing: border-box; display: flex; flex-direction: column; gap: 32px; }
      [data-composition-id="fs-hook"] .eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: #67e8f9; display: inline-flex; align-items: center; gap: 12px; align-self: flex-start; }
      [data-composition-id="fs-hook"] .eyebrow .live { width: 8px; height: 8px; border-radius: 50%; background: #67e8f9; box-shadow: 0 0 12px #67e8f9; }
      [data-composition-id="fs-hook"] .title { font-weight: 800; font-size: 84px; line-height: 0.96; letter-spacing: -0.035em; margin: 0; }
      [data-composition-id="fs-hook"] .title .word { display: inline-block; margin-right: 0.18em; }
      [data-composition-id="fs-hook"] .title .grad-l { background: linear-gradient(135deg, #a3e635, #67e8f9); -webkit-background-clip: text; background-clip: text; color: transparent; }

      [data-composition-id="fs-hook"] .rows { display: flex; flex-direction: column; gap: 18px; margin-top: 12px; }
      [data-composition-id="fs-hook"] .tier-row { display: grid; grid-template-columns: 140px 1fr; gap: 20px; background: rgba(15,20,30,0.55); border: 1.5px solid rgba(103,232,249,0.30); border-radius: 20px; padding: 20px 24px; backdrop-filter: blur(14px); box-shadow: 0 0 32px rgba(103,232,249,0.10), inset 0 1px 0 rgba(255,255,255,0.04); align-items: center; }
      [data-composition-id="fs-hook"] .tier-letter { font-weight: 900; font-size: 88px; letter-spacing: -0.04em; line-height: 1; text-align: center; font-variant-numeric: tabular-nums; }
      [data-composition-id="fs-hook"] .tier-row.before .tier-letter { color: #fb7185; text-shadow: 0 0 28px rgba(251,113,133,0.85), 0 0 12px rgba(251,113,133,0.6); }
      [data-composition-id="fs-hook"] .tier-row.after .tier-letter { color: #a3e635; text-shadow: 0 0 28px rgba(163,230,53,0.85), 0 0 12px rgba(163,230,53,0.6); }
      [data-composition-id="fs-hook"] .tier-row.after { border-color: rgba(163,230,53,0.40); box-shadow: 0 0 32px rgba(163,230,53,0.16), inset 0 1px 0 rgba(255,255,255,0.04); }
      [data-composition-id="fs-hook"] .tier-content { display: flex; flex-direction: column; gap: 8px; }
      [data-composition-id="fs-hook"] .tier-label { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #8b94a8; }
      [data-composition-id="fs-hook"] .tier-row.before .tier-label { color: #fb7185; }
      [data-composition-id="fs-hook"] .tier-row.after  .tier-label { color: #a3e635; }
      [data-composition-id="fs-hook"] .items { display: flex; gap: 14px; flex-wrap: wrap; }
      [data-composition-id="fs-hook"] .item { display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 90px; }
      [data-composition-id="fs-hook"] .item .ic { width: 60px; height: 60px; display: inline-flex; align-items: center; justify-content: center; font-size: 32px; background: rgba(255,255,255,0.04); border-radius: 14px; border: 1px solid rgba(255,255,255,0.10); filter: drop-shadow(0 0 8px rgba(255,255,255,0.15)); }
      [data-composition-id="fs-hook"] .item .lb { font-size: 13px; color: #c4cad6; font-weight: 500; text-align: center; }
      [data-composition-id="fs-hook"] .tier-row.after .item .ic { background: rgba(163,230,53,0.08); border-color: rgba(163,230,53,0.30); filter: drop-shadow(0 0 10px rgba(163,230,53,0.35)); }
    </style>

    <div class="bg-glow"></div>
    <div class="stage">
      <span class="eyebrow"><span class="live"></span>BEFORE / AFTER · {{CONTEXT_VI}}</span>

      <h1 class="title">
        <span class="word">{{BEFORE_NUMBER}}</span> <span class="word">{{BEFORE_UNIT}}</span>
        <span class="word">→</span>
        <span class="word grad-l">{{AFTER_NUMBER}}</span> <span class="word grad-l">{{AFTER_UNIT}}</span>
      </h1>

      <div class="rows">
        <div class="tier-row before">
          <div class="tier-letter">{{BEFORE_TIER}}</div>
          <div class="tier-content">
            <span class="tier-label">⚡ TRƯỚC ĐÂY · {{BEFORE_PERIOD}}</span>
            <div class="items">
              <div class="item"><div class="ic">{{EMOJI_1}}</div><div class="lb">{{LABEL_1}}</div></div>
              <div class="item"><div class="ic">{{EMOJI_2}}</div><div class="lb">{{LABEL_2}}</div></div>
              <div class="item"><div class="ic">{{EMOJI_3}}</div><div class="lb">{{LABEL_3}}</div></div>
              <div class="item"><div class="ic">{{EMOJI_4}}</div><div class="lb">{{LABEL_4}}</div></div>
            </div>
          </div>
        </div>
        <div class="tier-row after">
          <div class="tier-letter">{{AFTER_TIER}}</div>
          <div class="tier-content">
            <span class="tier-label">✓ HÔM NAY · {{AFTER_PERIOD}}</span>
            <div class="items">
              <div class="item"><div class="ic">📝</div><div class="lb">Bản nháp</div></div>
              <div class="item"><div class="ic">📊</div><div class="lb">Báo cáo</div></div>
              <div class="item"><div class="ic">📧</div><div class="lb">Email</div></div>
              <div class="item"><div class="ic">✓</div><div class="lb">Sẵn sàng</div></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      const R = '[data-composition-id="fs-hook"]';

      tl.from(R + ' .eyebrow', { y: -20, opacity: 0, duration: 0.5, ease: 'power3.out' }, 0.1);
      tl.from(R + ' .title .word', { y: 50, opacity: 0, scale: 0.85, duration: 0.55, ease: 'back.out(1.6)', stagger: 0.07 }, 0.4);

      tl.from(R + ' .tier-row.before', { x: -60, opacity: 0, duration: 0.55, ease: 'power3.out' }, 1.5);
      tl.from(R + ' .tier-row.before .tier-letter', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 1.8);
      tl.from(R + ' .tier-row.before .item', { y: 20, opacity: 0, duration: 0.4, stagger: 0.12 }, 2.2);

      tl.from(R + ' .tier-row.after', { x: -60, opacity: 0, duration: 0.55, ease: 'power3.out' }, 5.5);
      tl.from(R + ' .tier-row.after .tier-letter', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 5.9);
      tl.from(R + ' .tier-row.after .item', { y: 20, opacity: 0, duration: 0.4, stagger: 0.12 }, 6.4);

      tl.to(R + ' .tier-row.after', { boxShadow: '0 0 60px rgba(163,230,53,0.35), inset 0 1px 0 rgba(255,255,255,0.04)', duration: 1.2, ease: 'sine.inOut', yoyo: true, repeat: 4 }, 8.0);

      window.__timelines["fs-hook"] = tl;
    </script>
  </div>
</template>
```

**PIP trigger recommendation:** at `5.9s` when `.tier-row.after .tier-letter` scales in (the payoff "0h" reveal). Hold ~3.3s.

---

## 2. chats-stack (Problem)

**When:** Problem scene showing multiple AI tools failing with chat-message visual + broken-chain stamp.

**Accent:** `orange` (user message) + `rose` (broken-chain).

**Voiceover beat:** "Mình thử ChatGPT, Gemini... đều đứt mạch."

```html
<style>
[data-composition-id="fs-prob"] .chats { display: flex; flex-direction: column; gap: 14px; margin-top: 8px; }
[data-composition-id="fs-prob"] .chat-row { display: grid; grid-template-columns: 90px 1fr; gap: 18px; align-items: center; background: rgba(15,20,30,0.55); border: 1.5px solid rgba(103,232,249,0.30); border-radius: 18px; padding: 16px 22px; backdrop-filter: blur(14px); box-shadow: 0 0 28px rgba(103,232,249,0.08), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-prob"] .chat-row.user { border-color: rgba(251,146,60,0.40); box-shadow: 0 0 28px rgba(251,146,60,0.12), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-prob"] .chat-row.fail { border-color: rgba(251,113,133,0.40); box-shadow: 0 0 28px rgba(251,113,133,0.10), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-prob"] .av { width: 70px; height: 70px; border-radius: 18px; display: inline-flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 800; justify-self: center; }
[data-composition-id="fs-prob"] .av.you { background: #fb923c; color: #0b0f1a; box-shadow: 0 0 22px rgba(251,146,60,0.5); }
[data-composition-id="fs-prob"] .av.gpt { background: #10a37f; color: #fff; box-shadow: 0 0 18px rgba(16,163,127,0.4); }
[data-composition-id="fs-prob"] .av.gem { background: linear-gradient(135deg, #4285f4, #a855f7); color: #fff; box-shadow: 0 0 18px rgba(168,85,247,0.45); }
[data-composition-id="fs-prob"] .body { display: flex; flex-direction: column; gap: 4px; }
[data-composition-id="fs-prob"] .name { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #8b94a8; }
[data-composition-id="fs-prob"] .chat-row.user .name { color: #fb923c; }
[data-composition-id="fs-prob"] .chat-row.fail .name { color: #fb7185; }
[data-composition-id="fs-prob"] .text { font-size: 22px; font-weight: 500; color: #e7ecf3; line-height: 1.4; }
[data-composition-id="fs-prob"] .text b { color: #fff; font-weight: 700; }
[data-composition-id="fs-prob"] .chat-row.fail .text { color: #b6bdcc; font-style: italic; }

[data-composition-id="fs-prob"] .broken { display: flex; align-items: center; justify-content: center; gap: 16px; padding: 16px 24px; border: 2px dashed #fb7185; border-radius: 16px; background: rgba(251,113,133,0.08); font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700; letter-spacing: 0.10em; text-transform: uppercase; color: #fb7185; backdrop-filter: blur(12px); box-shadow: 0 0 30px rgba(251,113,133,0.18); }
[data-composition-id="fs-prob"] .broken .ico { font-size: 30px; }
</style>

<div class="chats">
  <div class="chat-row user">
    <div class="av you">B</div>
    <div class="body">
      <span class="name">BẠN</span>
      <span class="text">Tổng hợp toàn bộ <b>tài liệu dự án</b> này cho mình</span>
    </div>
  </div>
  <div class="chat-row fail" id="ch-gpt">
    <div class="av gpt">G</div>
    <div class="body">
      <span class="name">CHATGPT</span>
      <span class="text">"Xin lỗi, tôi không nhớ tin nhắn trước. Bạn vui lòng nhắc lại từ đầu…"</span>
    </div>
  </div>
  <div class="chat-row fail" id="ch-gem">
    <div class="av gem">✦</div>
    <div class="body">
      <span class="name">GEMINI</span>
      <span class="text">"Tôi cần thêm context. Bạn dán lại nội dung gốc giúp tôi nhé…"</span>
    </div>
  </div>
  <div class="broken">
    <span class="ico">⛓️‍💥</span>
    <span>Đứt mạch · phải nhắc lại · mệt cái đầu</span>
  </div>
</div>
```

GSAP:
```js
tl.from(R + ' .chat-row.user', { x: -60, opacity: 0, duration: 0.5, ease: 'power3.out' }, 1.5);
tl.from(R + ' #ch-gpt',         { x: -60, opacity: 0, duration: 0.5, ease: 'power3.out' }, 3.5);
tl.from(R + ' #ch-gem',         { x: -60, opacity: 0, duration: 0.5, ease: 'power3.out' }, 5.5);
tl.from(R + ' .broken', { scale: 0.6, opacity: 0, duration: 0.5, ease: 'back.out(2)' }, 8.0);
tl.to(R   + ' .broken', { x: -8, duration: 0.08, yoyo: true, repeat: 5, ease: 'sine.inOut' }, 8.5);
```

**PIP trigger recommendation:** none (chat content is dense — keep SPLIT so avatar reactions read).

---

## 3. hero-orb + spec-trio (Solution)

**When:** Solution scene introducing the new tool/method, with iridescent orb visual + 3 spec rows below.

**Accent:** `violet` (orb + spec1) + `cyan` (spec2) + `lime` (spec3).

**Voiceover beat:** "Cho đến lúc mình thử Claude theo kiểu khác... nó nhớ được, nó đọc được, nó tự bấm máy."

```html
<style>
[data-composition-id="fs-sol"] .hero-row { display: grid; grid-template-columns: 180px 1fr; gap: 24px; align-items: center; background: rgba(15,20,30,0.55); border: 1.5px solid rgba(167,139,250,0.40); border-radius: 20px; padding: 18px 22px; backdrop-filter: blur(14px); box-shadow: 0 0 32px rgba(167,139,250,0.15), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-sol"] .orb-cell { display: flex; align-items: center; justify-content: center; position: relative; }
[data-composition-id="fs-sol"] .orb { width: 130px; height: 130px; border-radius: 50%; background: radial-gradient(circle at 32% 30%, #fff, #a78bfa 28%, #67e8f9 64%, #f0abfc 100%); box-shadow: 0 0 50px rgba(167,139,250,0.65), inset -16px -16px 32px rgba(0,0,0,0.30); position: relative; }
[data-composition-id="fs-sol"] .orb::after { content: ""; position: absolute; top: 16%; left: 22%; width: 32%; height: 22%; border-radius: 50%; background: rgba(255,255,255,0.6); filter: blur(8px); }
[data-composition-id="fs-sol"] .hero-content { display: flex; flex-direction: column; gap: 10px; }
[data-composition-id="fs-sol"] .hero-label { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #a78bfa; }
[data-composition-id="fs-sol"] .task-items { display: flex; gap: 14px; }
[data-composition-id="fs-sol"] .task-items .item { display: flex; flex-direction: column; align-items: center; gap: 4px; }
[data-composition-id="fs-sol"] .task-items .ic { width: 56px; height: 56px; display: inline-flex; align-items: center; justify-content: center; font-size: 26px; background: rgba(167,139,250,0.10); border: 1px solid rgba(167,139,250,0.30); border-radius: 13px; filter: drop-shadow(0 0 8px rgba(167,139,250,0.35)); }
[data-composition-id="fs-sol"] .ingest-tag { display: inline-flex; align-items: center; gap: 8px; font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; color: #a78bfa; padding: 5px 12px; border: 1px solid rgba(167,139,250,0.40); background: rgba(167,139,250,0.08); border-radius: 8px; letter-spacing: 0.06em; align-self: flex-start; }

[data-composition-id="fs-sol"] .specs { display: flex; flex-direction: column; gap: 12px; }
[data-composition-id="fs-sol"] .tier-row { display: grid; grid-template-columns: 130px 1fr 90px; gap: 18px; align-items: center; background: rgba(15,20,30,0.55); border: 1.5px solid rgba(103,232,249,0.30); border-radius: 18px; padding: 14px 22px; backdrop-filter: blur(14px); box-shadow: 0 0 28px rgba(103,232,249,0.08), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-sol"] .tier-letter { font-weight: 900; font-size: 56px; letter-spacing: -0.04em; line-height: 1; text-align: center; }
[data-composition-id="fs-sol"] .tier-row.s1 { border-color: rgba(167,139,250,0.40); box-shadow: 0 0 28px rgba(167,139,250,0.12), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-sol"] .tier-row.s1 .tier-letter { color: #a78bfa; text-shadow: 0 0 24px rgba(167,139,250,0.85), 0 0 10px rgba(167,139,250,0.6); }
[data-composition-id="fs-sol"] .tier-row.s2 { border-color: rgba(103,232,249,0.40); }
[data-composition-id="fs-sol"] .tier-row.s2 .tier-letter { color: #67e8f9; font-size: 38px; text-shadow: 0 0 24px rgba(103,232,249,0.85), 0 0 10px rgba(103,232,249,0.6); }
[data-composition-id="fs-sol"] .tier-row.s3 { border-color: rgba(163,230,53,0.40); box-shadow: 0 0 28px rgba(163,230,53,0.18), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-sol"] .tier-row.s3 .tier-letter { color: #a3e635; text-shadow: 0 0 24px rgba(163,230,53,0.85), 0 0 10px rgba(163,230,53,0.6); }
[data-composition-id="fs-sol"] .tier-content { display: flex; flex-direction: column; gap: 2px; }
[data-composition-id="fs-sol"] .ttl { font-size: 22px; font-weight: 700; color: #f5f7fa; }
[data-composition-id="fs-sol"] .sub { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #8b94a8; letter-spacing: 0.05em; }
[data-composition-id="fs-sol"] .icon-cell { font-size: 36px; text-align: center; opacity: 0.85; filter: drop-shadow(0 0 10px currentColor); }
[data-composition-id="fs-sol"] .tier-row.s1 .icon-cell { color: #a78bfa; }
[data-composition-id="fs-sol"] .tier-row.s2 .icon-cell { color: #67e8f9; }
[data-composition-id="fs-sol"] .tier-row.s3 .icon-cell { color: #a3e635; }
</style>

<div class="hero-row">
  <div class="orb-cell"><div class="orb"></div></div>
  <div class="hero-content">
    <span class="hero-label">{{TOOL_NAME}} · {{TAGLINE_VI}}</span>
    <div class="task-items">
      <div class="item"><div class="ic">📝</div><div class="lb">{{TASK_1}}</div></div>
      <div class="item"><div class="ic">📊</div><div class="lb">{{TASK_2}}</div></div>
      <div class="item"><div class="ic">📧</div><div class="lb">{{TASK_3}}</div></div>
      <div class="item"><div class="ic">📦</div><div class="lb">{{TASK_4}}</div></div>
    </div>
    <div class="ingest-tag">📦 {{INGEST_NOTE}}</div>
  </div>
</div>

<div class="specs">
  <div class="tier-row s1">
    <div class="tier-letter">∞</div>
    <div class="tier-content"><span class="ttl">{{SPEC_1_TITLE}}</span><span class="sub">{{SPEC_1_SUB}}</span></div>
    <div class="icon-cell">🧠</div>
  </div>
  <div class="tier-row s2">
    <div class="tier-letter">100tr</div>
    <div class="tier-content"><span class="ttl">{{SPEC_2_TITLE}}</span><span class="sub">{{SPEC_2_SUB}}</span></div>
    <div class="icon-cell">📄</div>
  </div>
  <div class="tier-row s3">
    <div class="tier-letter">8h</div>
    <div class="tier-content"><span class="ttl">{{SPEC_3_TITLE}}</span><span class="sub">{{SPEC_3_SUB}}</span></div>
    <div class="icon-cell">🌙</div>
  </div>
</div>
```

GSAP:
```js
tl.from(R + ' .hero-row', { y: 30, opacity: 0, duration: 0.6, ease: 'power3.out' }, 1.5);
tl.from(R + ' .orb', { scale: 0, duration: 0.7, ease: 'back.out(1.4)' }, 1.7);
tl.to(R   + ' .orb', { scale: 1.04, duration: 1.6, ease: 'sine.inOut', yoyo: true, repeat: 8, transformOrigin: 'center' }, 2.5);
tl.from(R + ' .task-items .item', { y: 20, opacity: 0, duration: 0.4, stagger: 0.12 }, 2.4);
tl.from(R + ' .ingest-tag', { y: 10, opacity: 0, duration: 0.4 }, 3.4);

tl.from(R + ' .tier-row.s1', { x: 60, opacity: 0, duration: 0.55, ease: 'power3.out' }, 8.0);
tl.from(R + ' .tier-row.s1 .tier-letter', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 8.3);
tl.from(R + ' .tier-row.s2', { x: 60, opacity: 0, duration: 0.55, ease: 'power3.out' }, 11.0);
tl.from(R + ' .tier-row.s2 .tier-letter', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 11.3);
tl.from(R + ' .tier-row.s3', { x: 60, opacity: 0, duration: 0.6, ease: 'back.out(1.4)' }, 14.0);
tl.from(R + ' .tier-row.s3 .tier-letter', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 14.4);
tl.to(R   + ' .tier-row.s3', { boxShadow: '0 0 50px rgba(163,230,53,0.4), inset 0 1px 0 rgba(255,255,255,0.04)', duration: 1.0, ease: 'sine.inOut', yoyo: true, repeat: 4 }, 14.8);
```

**PIP trigger recommendation:** 2 PIP windows — at orb reveal (1.7s relative → ~28.8s absolute) for ~4.7s, and at spec trio (8.0–14.4s relative → ~35.2s absolute) for ~9.3s.

---

## 4. counter-row (Recap)

**When:** Result/recap scene with one big number + arrow transition + supporting clients/badges.

**Accent:** `lime` (number `to`) + `cyan` (clients).

**Voiceover beat:** "Tuần đầu mình tiết kiệm 15 tiếng. Tháng sau nhận thêm 2 khách."

```html
<style>
[data-composition-id="fs-recap"] .counter-row { display: grid; grid-template-columns: 130px 1fr; gap: 24px; align-items: center; background: rgba(15,20,30,0.55); border: 1.5px solid rgba(163,230,53,0.40); border-radius: 22px; padding: 22px 28px; backdrop-filter: blur(14px); box-shadow: 0 0 36px rgba(163,230,53,0.16), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-recap"] .tier-letter { font-weight: 900; font-size: 64px; letter-spacing: -0.04em; line-height: 1; text-align: center; color: #a3e635; text-shadow: 0 0 28px rgba(163,230,53,0.85), 0 0 12px rgba(163,230,53,0.6); }
[data-composition-id="fs-recap"] .counter-content { display: flex; flex-direction: column; gap: 6px; }
[data-composition-id="fs-recap"] .counter-label { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; letter-spacing: 0.20em; text-transform: uppercase; color: #a3e635; }
[data-composition-id="fs-recap"] .counter { display: flex; align-items: baseline; gap: 18px; }
[data-composition-id="fs-recap"] .counter .from { position: relative; font-size: 56px; font-weight: 900; color: #8b94a8; letter-spacing: -0.04em; line-height: 1; }
[data-composition-id="fs-recap"] .counter .from::after { content: ""; position: absolute; left: -8%; right: -8%; top: 56%; height: 4px; background: #fb7185; border-radius: 3px; transform: scaleX(0); transform-origin: left center; }
[data-composition-id="fs-recap"] .counter .arr { font-size: 36px; color: #a3e635; font-weight: 600; }
[data-composition-id="fs-recap"] .counter .to { font-size: 96px; font-weight: 900; letter-spacing: -0.05em; line-height: 1; background: linear-gradient(135deg, #a3e635, #67e8f9); -webkit-background-clip: text; background-clip: text; color: transparent; }
[data-composition-id="fs-recap"] .counter .u { font-family: 'JetBrains Mono', monospace; font-size: 16px; color: #8b94a8; text-transform: uppercase; letter-spacing: 0.18em; align-self: flex-end; margin-bottom: 8px; }

[data-composition-id="fs-recap"] .clients { display: flex; gap: 14px; }
[data-composition-id="fs-recap"] .client { flex: 1; display: grid; grid-template-columns: 70px 1fr; gap: 14px; align-items: center; padding: 14px 20px; background: rgba(15,20,30,0.55); border: 1.5px solid rgba(103,232,249,0.40); border-radius: 18px; backdrop-filter: blur(14px); box-shadow: 0 0 28px rgba(103,232,249,0.10), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-recap"] .client .av { width: 50px; height: 50px; border-radius: 14px; background: linear-gradient(135deg, #a78bfa, #67e8f9); display: inline-flex; align-items: center; justify-content: center; color: #0b0f1a; font-weight: 800; font-size: 22px; box-shadow: 0 0 18px rgba(103,232,249,0.4); justify-self: center; }
[data-composition-id="fs-recap"] .client .ttl { font-size: 20px; font-weight: 700; color: #f5f7fa; }
[data-composition-id="fs-recap"] .client .sb { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #a3e635; letter-spacing: 0.12em; font-weight: 700; }

[data-composition-id="fs-recap"] .delta { font-family: 'JetBrains Mono', monospace; font-size: 22px; color: #a3e635; background: rgba(163,230,53,0.10); border: 1.5px solid rgba(163,230,53,0.45); border-radius: 14px; padding: 14px 24px; letter-spacing: 0.10em; backdrop-filter: blur(12px); align-self: flex-start; box-shadow: 0 0 28px rgba(163,230,53,0.18); }
</style>

<div class="counter-row">
  <div class="tier-letter">{{DELTA_LETTER}}</div>
  <div class="counter-content">
    <span class="counter-label">{{COUNTER_UNIT_VI}}</span>
    <div class="counter">
      <span class="from">{{FROM}}</span>
      <span class="arr">→</span>
      <span class="to">{{TO}}</span>
      <span class="u">{{UNIT_VI}}</span>
    </div>
  </div>
</div>

<div class="clients">
  <div class="client" id="cl1">
    <div class="av">N</div>
    <div class="col"><span class="ttl">{{CLIENT_1_TTL}}</span><span class="sb">{{CLIENT_1_SUB}}</span></div>
  </div>
  <div class="client" id="cl2">
    <div class="av">T</div>
    <div class="col"><span class="ttl">{{CLIENT_2_TTL}}</span><span class="sb">{{CLIENT_2_SUB}}</span></div>
  </div>
</div>

<div class="delta">{{DELTA_TAGLINE_VI}}</div>
```

GSAP:
```js
tl.from(R + ' .counter-row', { y: 30, opacity: 0, duration: 0.5, ease: 'power3.out' }, 0.9);
tl.from(R + ' .tier-letter', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 1.1);
tl.from(R + ' .counter .from', { x: -20, opacity: 0, duration: 0.4 }, 1.3);
tl.fromTo(R + ' .counter .from::after', { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: 'power2.out' }, 1.6);
tl.from(R + ' .counter .arr', { scale: 0, opacity: 0, duration: 0.3, ease: 'back.out(2)' }, 1.8);
tl.from(R + ' .counter .to', { scale: 0.5, opacity: 0, duration: 0.6, ease: 'back.out(1.8)' }, 2.0);
tl.from(R + ' #cl1', { y: 30, opacity: 0, duration: 0.45, ease: 'power3.out' }, 2.5);
tl.from(R + ' #cl2', { y: 30, opacity: 0, duration: 0.45, ease: 'power3.out' }, 2.7);
tl.from(R + ' .delta', { y: 20, opacity: 0, duration: 0.45, ease: 'back.out(1.6)' }, 3.0);
tl.to(R + ' .delta', { boxShadow: '0 0 40px rgba(163,230,53,0.5)', duration: 0.8, ease: 'sine.inOut', yoyo: true, repeat: 3 }, 3.3);
```

**PIP trigger recommendation:** at counter `.to` scale-in (2.0s relative). Hold ~4.5s.

---

## 5. comment-terminal (CTA)

**When:** CTA scene asking viewer to comment a magic word + 2 free gifts.

**Accent:** `pink` (terminal + tier-letter) + `lime`/`cyan` gradient (gift tag).

**Voiceover beat:** "Comment AI mình gửi bạn cách dùng."

```html
<style>
[data-composition-id="fs-cta"] .comment-row { display: grid; grid-template-columns: 130px 1fr; gap: 24px; align-items: center; background: rgba(15,20,30,0.55); border: 1.5px solid rgba(240,171,252,0.40); border-radius: 22px; padding: 22px 28px; backdrop-filter: blur(14px); box-shadow: 0 0 36px rgba(240,171,252,0.18), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-cta"] .tier-letter { font-weight: 900; font-size: 76px; letter-spacing: -0.04em; line-height: 1; text-align: center; color: #f0abfc; text-shadow: 0 0 30px rgba(240,171,252,0.85), 0 0 14px rgba(240,171,252,0.6); }
[data-composition-id="fs-cta"] .terminal { background: rgba(0,0,0,0.55); border: 1px solid rgba(255,255,255,0.10); border-radius: 14px; padding: 12px 16px; font-family: 'JetBrains Mono', monospace; }
[data-composition-id="fs-cta"] .terminal .head { display: flex; align-items: center; gap: 8px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.10); margin-bottom: 10px; }
[data-composition-id="fs-cta"] .terminal .dot { width: 10px; height: 10px; border-radius: 50%; }
[data-composition-id="fs-cta"] .terminal .dot.r { background: #ff5f56; }
[data-composition-id="fs-cta"] .terminal .dot.y { background: #ffbd2e; }
[data-composition-id="fs-cta"] .terminal .dot.g { background: #27c93f; }
[data-composition-id="fs-cta"] .terminal .lb { margin-left: auto; font-size: 11px; color: #8b94a8; letter-spacing: 0.10em; text-transform: uppercase; font-weight: 600; }
[data-composition-id="fs-cta"] .terminal .row { display: flex; align-items: center; gap: 10px; font-size: 22px; color: #f5f7fa; }
[data-composition-id="fs-cta"] .terminal .prompt { color: #a78bfa; font-weight: 700; }
[data-composition-id="fs-cta"] .terminal .input { color: #f0abfc; font-weight: 700; }
[data-composition-id="fs-cta"] .terminal .cursor { display: inline-block; width: 12px; height: 22px; background: #f0abfc; margin-left: 2px; }
[data-composition-id="fs-cta"] .terminal .out { margin-top: 10px; font-size: 14px; color: #b6bdcc; line-height: 1.6; }

[data-composition-id="fs-cta"] .gifts { display: flex; gap: 14px; }
[data-composition-id="fs-cta"] .gift { flex: 1; display: grid; grid-template-columns: 70px 1fr 80px; gap: 14px; align-items: center; padding: 14px 18px; background: rgba(15,20,30,0.55); border: 1.5px solid rgba(103,232,249,0.30); border-radius: 18px; backdrop-filter: blur(14px); box-shadow: 0 0 24px rgba(103,232,249,0.10), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-cta"] .gift .ic { width: 50px; height: 50px; display: inline-flex; align-items: center; justify-content: center; font-size: 26px; background: rgba(103,232,249,0.10); border: 1px solid rgba(103,232,249,0.30); border-radius: 13px; filter: drop-shadow(0 0 10px rgba(103,232,249,0.35)); justify-self: center; }
[data-composition-id="fs-cta"] .gift .ttl { font-size: 18px; font-weight: 700; color: #f5f7fa; line-height: 1.3; }
[data-composition-id="fs-cta"] .gift .tag { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 800; background: linear-gradient(135deg, #a3e635, #67e8f9); color: #0b0f1a; padding: 6px 12px; border-radius: 7px; letter-spacing: 0.12em; text-align: center; }

[data-composition-id="fs-cta"] .cta-line { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 700; color: #f0abfc; letter-spacing: 0.10em; align-self: center; }
</style>

<div class="comment-row">
  <div class="tier-letter">{{KEYWORD}}</div>
  <div class="terminal">
    <div class="head"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="lb">comment.input</span></div>
    <div class="row"><span class="prompt">→</span><span class="input" id="ti">{{KEYWORD}}</span><span class="cursor" id="cur"></span></div>
    <div class="out">→ Đang gửi cho bạn:<br/><b>· {{GIFT_PEEK_1}}</b> · <b>{{GIFT_PEEK_2}}</b></div>
  </div>
</div>

<div class="gifts">
  <div class="gift" id="g1"><div class="ic">🤖</div><div class="ttl">{{GIFT_1_TTL}}</div><div class="tag">FREE</div></div>
  <div class="gift" id="g2"><div class="ic">⚡</div><div class="ttl">{{GIFT_2_TTL}}</div><div class="tag">FREE</div></div>
</div>

<div class="cta-line">{{CTA_LINE_VI}}</div>
```

GSAP — type-in animation (note: requires GSAP TextPlugin):
```js
tl.from(R + ' .comment-row', { y: 30, opacity: 0, duration: 0.5, ease: 'back.out(1.5)' }, 0.9);
tl.from(R + ' .tier-letter', { scale: 0, opacity: 0, duration: 0.5, ease: 'back.out(1.8)' }, 1.1);
tl.set(R + ' #ti', { text: '' }, 1.4);
tl.to(R   + ' #ti', { text: 'A',  duration: 0.18, ease: 'none' }, 1.5);
tl.to(R   + ' #ti', { text: 'AI', duration: 0.18, ease: 'none' }, 1.75);
tl.to(R   + ' #cur', { opacity: 0, duration: 0.5, ease: 'steps(1)', yoyo: true, repeat: 5 }, 1.5);
tl.from(R + ' .terminal .out', { opacity: 0, y: 8, duration: 0.4 }, 2.2);
tl.from(R + ' #g1', { y: 30, scale: 0.9, opacity: 0, duration: 0.5, ease: 'back.out(1.6)' }, 2.6);
tl.from(R + ' #g2', { y: 30, scale: 0.9, opacity: 0, duration: 0.5, ease: 'back.out(1.6)' }, 2.8);
tl.to(R   + ' .gift .tag', { scale: 1.08, duration: 0.6, ease: 'sine.inOut', yoyo: true, repeat: 3, stagger: 0.1, transformOrigin: 'center' }, 3.2);
tl.from(R + ' .cta-line', { y: 20, opacity: 0, duration: 0.4 }, 3.3);
tl.to(R   + ' .cta-line', { y: -8, duration: 0.6, ease: 'sine.inOut', yoyo: true, repeat: 4 }, 3.7);
```

Add TextPlugin:
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/TextPlugin.min.js"></script>
<script>gsap.registerPlugin(TextPlugin);</script>
```

**PIP trigger recommendation:** at type-in completion (~1.95s relative → ~54.4s absolute). Hold to scene end.

---

## 6. stats 3-card (landing-style)

**When:** Knowledge intro scene introducing 3 numeric facts about a tool/topic. Adapted from landing skill section #2.

**Accent:** `cyan` + `lime` + `orange` (one per card).

```html
<style>
[data-composition-id="fs-stats"] .stats-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 18px; }
[data-composition-id="fs-stats"] .stat-card { background: rgba(15,20,30,0.55); border: 1.5px solid rgba(255,255,255,0.10); border-radius: 20px; padding: 24px 22px; backdrop-filter: blur(14px); box-shadow: inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-stats"] .stat-card .lbl { font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 0.18em; margin-bottom: 16px; }
[data-composition-id="fs-stats"] .stat-card .num { font-weight: 900; font-size: 76px; line-height: 1; letter-spacing: -0.04em; }
[data-composition-id="fs-stats"] .stat-card .ttl { font-size: 18px; font-weight: 700; color: #f5f7fa; margin-top: 12px; }
[data-composition-id="fs-stats"] .stat-card .sub { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #8b94a8; margin-top: 4px; }

[data-composition-id="fs-stats"] .c1 { border-color: rgba(103,232,249,0.30); box-shadow: 0 0 28px rgba(103,232,249,0.10), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-stats"] .c1 .lbl { color: #67e8f9; }
[data-composition-id="fs-stats"] .c1 .num { background: linear-gradient(135deg, #67e8f9, #a3e635); -webkit-background-clip: text; background-clip: text; color: transparent; }

[data-composition-id="fs-stats"] .c2 { border-color: rgba(163,230,53,0.30); box-shadow: 0 0 28px rgba(163,230,53,0.10), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-stats"] .c2 .lbl { color: #a3e635; }
[data-composition-id="fs-stats"] .c2 .num { color: #a3e635; }

[data-composition-id="fs-stats"] .c3 { border-color: rgba(251,146,60,0.30); box-shadow: 0 0 28px rgba(251,146,60,0.10), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-stats"] .c3 .lbl { color: #fb923c; }
[data-composition-id="fs-stats"] .c3 .num { color: #fb923c; }
</style>

<div class="stats-grid">
  <div class="stat-card c1"><div class="lbl">// {{LBL_1}}</div><div class="num">{{NUM_1}}</div><div class="ttl">{{TTL_1}}</div><div class="sub">{{SUB_1}}</div></div>
  <div class="stat-card c2"><div class="lbl">// {{LBL_2}}</div><div class="num">{{NUM_2}}</div><div class="ttl">{{TTL_2}}</div><div class="sub">{{SUB_2}}</div></div>
  <div class="stat-card c3"><div class="lbl">// {{LBL_3}}</div><div class="num">{{NUM_3}}</div><div class="ttl">{{TTL_3}}</div><div class="sub">{{SUB_3}}</div></div>
</div>
```

GSAP:
```js
tl.from(R + ' .stat-card', { y: 40, opacity: 0, duration: 0.5, ease: 'power3.out', stagger: 0.18 }, 1.2);
tl.from(R + ' .stat-card .num', { scale: 0.6, opacity: 0, duration: 0.5, ease: 'back.out(1.6)', stagger: 0.18 }, 1.5);
```

---

## 7. comparison 2-col

**When:** Decision frame "When to use X vs Y" — both are valid, no winner.

**Accent:** `cyan` (col A) + `pink` (col B).

```html
<style>
[data-composition-id="fs-cmp"] .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
[data-composition-id="fs-cmp"] .col { background: rgba(15,20,30,0.55); border: 1.5px solid rgba(255,255,255,0.10); border-radius: 20px; padding: 24px; backdrop-filter: blur(14px); }
[data-composition-id="fs-cmp"] .col.a { border-color: rgba(103,232,249,0.40); box-shadow: 0 0 28px rgba(103,232,249,0.12), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-cmp"] .col.b { border-color: rgba(240,171,252,0.40); box-shadow: 0 0 28px rgba(240,171,252,0.12), inset 0 1px 0 rgba(255,255,255,0.04); }
[data-composition-id="fs-cmp"] .col-head { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
[data-composition-id="fs-cmp"] .col-head .ic { width: 44px; height: 44px; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; font-size: 22px; }
[data-composition-id="fs-cmp"] .col.a .col-head .ic { background: rgba(103,232,249,0.15); border: 1px solid rgba(103,232,249,0.40); color: #67e8f9; }
[data-composition-id="fs-cmp"] .col.b .col-head .ic { background: rgba(240,171,252,0.15); border: 1px solid rgba(240,171,252,0.40); color: #f0abfc; }
[data-composition-id="fs-cmp"] .col-head .lbl { font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 0.18em; }
[data-composition-id="fs-cmp"] .col.a .col-head .lbl { color: #67e8f9; }
[data-composition-id="fs-cmp"] .col.b .col-head .lbl { color: #f0abfc; }
[data-composition-id="fs-cmp"] .col-head .ttl { font-size: 22px; font-weight: 700; color: #f5f7fa; }
[data-composition-id="fs-cmp"] .col ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
[data-composition-id="fs-cmp"] .col li { display: grid; grid-template-columns: 36px 1fr; gap: 10px; align-items: start; font-size: 16px; color: #b6bdcc; line-height: 1.5; }
[data-composition-id="fs-cmp"] .col li .yes { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 800; padding: 3px 6px; border-radius: 6px; background: rgba(163,230,53,0.15); color: #a3e635; border: 1px solid rgba(163,230,53,0.30); height: fit-content; text-align: center; }
[data-composition-id="fs-cmp"] .col li b { color: #f5f7fa; font-weight: 700; }
</style>

<div class="grid2">
  <div class="col a">
    <div class="col-head"><span class="ic">⚡</span><div><div class="lbl">// {{COL_A_LBL}}</div><div class="ttl">{{COL_A_TTL}}</div></div></div>
    <ul>
      <li><span class="yes">YES</span><span><b>{{ITEM_A1_T}}</b> — {{ITEM_A1_D}}</span></li>
      <li><span class="yes">YES</span><span><b>{{ITEM_A2_T}}</b> — {{ITEM_A2_D}}</span></li>
      <li><span class="yes">YES</span><span><b>{{ITEM_A3_T}}</b> — {{ITEM_A3_D}}</span></li>
    </ul>
  </div>
  <div class="col b">
    <div class="col-head"><span class="ic">✨</span><div><div class="lbl">// {{COL_B_LBL}}</div><div class="ttl">{{COL_B_TTL}}</div></div></div>
    <ul>
      <li><span class="yes">YES</span><span><b>{{ITEM_B1_T}}</b> — {{ITEM_B1_D}}</span></li>
      <li><span class="yes">YES</span><span><b>{{ITEM_B2_T}}</b> — {{ITEM_B2_D}}</span></li>
      <li><span class="yes">YES</span><span><b>{{ITEM_B3_T}}</b> — {{ITEM_B3_D}}</span></li>
    </ul>
  </div>
</div>
```

GSAP:
```js
tl.from(R + ' .col.a', { x: -40, opacity: 0, duration: 0.5, ease: 'power3.out' }, 1.2);
tl.from(R + ' .col.b', { x:  40, opacity: 0, duration: 0.5, ease: 'power3.out' }, 1.4);
tl.from(R + ' .col li', { y: 14, opacity: 0, duration: 0.35, stagger: 0.10 }, 1.8);
```

---

## 8. image-slot (cream infographic embed)

**When:** Want to show a hand-drawn editorial cream-paper metaphor inside the slide. Sits below the title or between rows.

**Aspect:** 16:9 default. Optional 4:3 if image is square-ish.

```html
<style>
[data-composition-id="<scene>"] .image-slot { position: relative; width: 100%; aspect-ratio: 16/9; border-radius: 20px; overflow: hidden; border: 1.5px dashed rgba(255,255,255,0.18); background: rgba(255,255,255,0.02); display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px); }
[data-composition-id="<scene>"] .image-slot.img-loaded { border-style: solid; border-color: rgba(255,255,255,0.10); background: transparent; }
[data-composition-id="<scene>"] .image-slot img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
[data-composition-id="<scene>"] .image-slot.img-loaded .ph-fallback { display: none; }
[data-composition-id="<scene>"] .ph-fallback { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 24px; }
[data-composition-id="<scene>"] .ph-tag { font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase; color: #8b94a8; }
[data-composition-id="<scene>"] .ph-hint { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: rgba(255,255,255,0.4); }
</style>

<div class="image-slot">
  <img src="{{N}}.png" alt="{{ALT_VI}}"
       onload="this.parentElement.classList.add('img-loaded')"
       onerror="this.remove()" />
  <div class="ph-fallback">
    <span class="ph-tag">▮ IMAGE PLACEHOLDER #{{N}} — {{N}}.png</span>
    <span class="ph-hint">Xem prompt #{{N}} trong prompts.md</span>
  </div>
</div>
```

GSAP (entrance):
```js
tl.from(R + ' .image-slot', { y: 30, opacity: 0, duration: 0.55, ease: 'power3.out' }, t);
```

**Note:** sub-skill `mkt-broll-image` uses AI33 / Nano Banana Pro at 16:9 (NO 16:10 support). Aspect locked.

---

## Pattern selection cheat sheet

| Voiceover beat archetype | Pattern |
|---|---|
| "Trước đây / Giờ" | tier-row before-after |
| "Mình thử X, Y... đều ___" | chats-stack |
| "Khác ở chỗ ___ / Cách dùng" | hero-orb + spec-trio |
| "Kết quả: ___ tăng / giảm" | counter-row |
| "Comment X / Lưu video / Subscribe" | comment-terminal |
| "X có 3 tính năng" | stats 3-card |
| "X dùng cho A, Y dùng cho B" | comparison 2-col |
| "Hình dung như ___" / metaphor moment | image-slot |
