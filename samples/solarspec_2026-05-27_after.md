# Patina AI-Farm Audit

> Site: **https://solarspechub.com**
> Date: 2026-05-27
> Pages audited: 5
> Duration: 2.5s

## 🟢 Overall: **96.3/100** — Grade **A** (Human-crafted)

### Per-Dimension Scores

| Dimension | Score | Read |
|---|---|---|
| **emoji_icons** | 🟢 100.0 | Icon system (Unicode emoji = AI tell) |
| **module_density** | 🟢 90.0 | Section count (11+ = programmatic anti-pattern) |
| **boilerplate** | 🟢 100.0 | AI-cliché phrase density |
| **section_rhythm** | 🟢 88.0 | Visual rhythm (bg color variety across sections) |
| **image_density** | 🟢 100.0 | Real images per page (zero = AI farm) |
| **cta_clarity** | 🟢 100.0 | Above-the-fold CTA focus |

---

## 🔧 Remediation Roadmap (worst-first)

### 1. [P2] `section_rhythm` — 88.0/100

**Why it matters:** When >70% of sections share one bg color, the page reads as a wall of cards. Apple/Stripe alternate white / off-white / dark sections to create rhythm — this signals 'a designer touched this'.

**Fix:**

Alternate bg per section using Tailwind tokens:
  - Section 1 (hero): `bg-white py-16`
  - Section 2: `bg-gray-50 py-20`
  - Section 3: `bg-neutral-950 text-white py-24` (dark band)
  - Section 4: `bg-white py-20`
  Larger vertical padding (py-20 / py-24) on contentful sections + tight py-12 on lists.

---

## 📋 Per-Page Detail

### https://solarspechub.com/api/

- HTTP 200 · 27,567 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 100/100 — 5 content modules detected (sections=5, h2s=2)
  - Evidence: `v1 &mdash; Free specs feed` (+1 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 85/100 — 2 section bg classes; 'bg-gray-50' covers 50%
  - Evidence: `('bg-gray-50', 1)` (+1 more)
- **image_density**: 100/100 — 3 real product/scene images (excluding logos/icons/SVG)
  - Evidence: `<img src="https://images.unsplash.com/photo-1605980776566-0486c3ac7617?w=1200&q=80&auto=format" alt=` (+2 more)
- **cta_clarity**: 100/100 — 1 primary CTA(s) — focused

### https://solarspechub.com/authors/jianlin/

- HTTP 200 · 28,529 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 100/100 — 4 content modules detected (sections=4, h2s=1)
  - Evidence: `How I work`
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 85/100 — 2 section bg classes; 'bg-gray-50' covers 50%
  - Evidence: `('bg-gray-50', 1)` (+1 more)
- **image_density**: 100/100 — 3 real product/scene images (excluding logos/icons/SVG)
  - Evidence: `<img src="https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?w=1200&q=80&auto=format" alt=` (+2 more)
- **cta_clarity**: 100/100 — 1 primary CTA(s) — focused

### https://solarspechub.com/

- HTTP 200 · 65,157 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 75/100 — 7 content modules detected (sections=7, h2s=4)
  - Evidence: `Featured &amp; Top Picks` (+3 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 100/100 — 4 section bg classes; 'bg-slate-100' covers 25%
  - Evidence: `('bg-slate-100', 1)` (+3 more)
- **image_density**: 100/100 — 4 real product/scene images (excluding logos/icons/SVG)
  - Evidence: `<img src="https://images.unsplash.com/photo-1509391366360-2e959784a276?w=1200&q=80&auto=format" alt=` (+2 more)
- **cta_clarity**: 100/100 — 2 primary CTA(s) — focused

### https://solarspechub.com/batteries/

- HTTP 200 · 110,030 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 100/100 — 5 content modules detected (sections=5, h2s=4)
  - Evidence: `Top picks at a glance` (+3 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 85/100 — 2 section bg classes; 'bg-slate-100' covers 50%
  - Evidence: `('bg-slate-100', 1)` (+1 more)
- **image_density**: 100/100 — 4 real product/scene images (excluding logos/icons/SVG)
  - Evidence: `<img src="https://images.unsplash.com/photo-1620283085439-39620a1e21c4?w=1200&q=80&auto=format" alt=` (+2 more)
- **cta_clarity**: 100/100 — 1 primary CTA(s) — focused

### https://solarspechub.com/about/

- HTTP 200 · 31,389 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 75/100 — 7 content modules detected (sections=7, h2s=4)
  - Evidence: `Our Mission` (+3 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 85/100 — 3 section bg classes; 'bg-gray-50' covers 33%
  - Evidence: `('bg-gray-50', 1)` (+2 more)
- **image_density**: 100/100 — 3 real product/scene images (excluding logos/icons/SVG)
  - Evidence: `<img src="https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?w=1200&q=80&auto=format" alt=` (+2 more)
- **cta_clarity**: 100/100 — 1 primary CTA(s) — focused

---

## About Patina

Patina audits the **AI-farm feel** of a site — the visual + copy + UX patterns that
signal 'AI made this, a human didn't curate it.' Sister product to **Veris** (data
truthfulness audit).

Six detection dimensions:
1. **emoji_icons** — Unicode emoji used as UI iconography
2. **module_density** — homepage section count
3. **boilerplate_copy** — AI-cliché phrase density
4. **section_rhythm** — bg color variety across sections
5. **image_density** — real product/scene images per content page
6. **cta_clarity** — primary CTA count above the fold

Each scored 0-100 (higher = more human-crafted). Total is the average.

Report generated by Patina v0.1 · 2026-05-27 20:33
