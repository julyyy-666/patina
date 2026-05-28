# Patina AI-Farm Audit

> Site: **https://solarspechub.com**
> Date: 2026-05-25
> Pages audited: 5
> Duration: 3.6s

## 🟠 Overall: **60.0/100** — Grade **D** (Noticeably AI-farm)

### Per-Dimension Scores

| Dimension | Score | Read |
|---|---|---|
| **emoji_icons** | 🟢 100.0 | Icon system (Unicode emoji = AI tell) |
| **module_density** | 🟡 63.0 | Section count (11+ = programmatic anti-pattern) |
| **boilerplate** | 🟢 100.0 | AI-cliché phrase density |
| **section_rhythm** | 🟠 57.0 | Visual rhythm (bg color variety across sections) |
| **image_density** | 🔴 10.0 | Real images per page (zero = AI farm) |
| **cta_clarity** | 🔴 30.0 | Above-the-fold CTA focus |

---

## 🔧 Remediation Roadmap (worst-first)

### 1. [P0] `image_density` — 10.0/100

**Why it matters:** Zero real images = AI agriculture's most famous tell. Stock photos are still better than nothing — and product/spec sites need actual product photography to break the text wall.

**Fix:**

Add 1-3 real images per content page:
  - Product pages: Pull manufacturer hero shot from the same datasheet URL you cite
  - Guides: Add 1 schematic + 1 contextual photo (rooftop install / panel close-up)
  - State pages: Add 1 location-relevant image (state map or local install)
  - For purely tabular pages: at minimum add brand logo SVGs at the top of brand sections
  Source: Unsplash (free), Pexels (free), or scraped manufacturer assets per their press kit.

---

### 2. [P0] `cta_clarity` — 30.0/100

**Why it matters:** 7+ primary CTAs above the fold = decision paralysis. Hick's Law: choice time grows logarithmically with options. AI scaffolds always overload because they don't trust any single CTA.

**Fix:**

Restructure hero to:
  - **One** primary CTA (strong color, large) — your single most-wanted action
  - **One** secondary link/ghost button (smaller, lower contrast)
  - Demote category navigation to the header nav, not the hero body
  Pattern: `<button class="bg-accent text-white px-8 py-4 rounded-xl text-lg font-bold">Primary</button><a class="text-gray-600 underline text-sm ml-4">or learn more</a>`

---

### 3. [P1] `section_rhythm` — 57.0/100

**Why it matters:** When >70% of sections share one bg color, the page reads as a wall of cards. Apple/Stripe alternate white / off-white / dark sections to create rhythm — this signals 'a designer touched this'.

**Fix:**

Alternate bg per section using Tailwind tokens:
  - Section 1 (hero): `bg-white py-16`
  - Section 2: `bg-gray-50 py-20`
  - Section 3: `bg-neutral-950 text-white py-24` (dark band)
  - Section 4: `bg-white py-20`
  Larger vertical padding (py-20 / py-24) on contentful sections + tight py-12 on lists.

---

### 4. [P1] `module_density` — 63.0/100

**Why it matters:** 10+ stacked sections is a programmatic-SEO anti-pattern. Yes EnergySage etc. do it, but the AI tell is when each section is generic ('Popular X', 'Top Y', 'Best Z') with no internal hierarchy.

**Fix:**

Either:
  - **Collapse** to 5-6 high-signal sections (Hero, primary entries, social proof, CTA, FAQ, About)
  - Or **add internal hierarchy**: turn 'Popular Comparisons' into `<details>` accordions, group with `<h3>` instead of `<h2>`, demote secondary sections

---

## 📋 Per-Page Detail

### https://solarspechub.com/

- HTTP 200 · 45,425 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 30/100 — 12 content modules detected (sections=12, h2s=10)
  - Evidence: `Popular Products` (+9 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 85/100 — 2 section bg classes; 'bg-primary' covers 50%
  - Evidence: `('bg-primary', 1)` (+1 more)
- **image_density**: 10/100 — 0 real product/scene images (excluding logos/icons/SVG)
- **cta_clarity**: 50/100 — 6 CTAs — too many competing entries

### https://solarspechub.com/about/

- HTTP 200 · 12,517 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 75/100 — 8 content modules detected (sections=8, h2s=7)
  - Evidence: `Our Mission` (+6 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 50/100 — No section bg classes detected (inconclusive)
- **image_density**: 10/100 — 0 real product/scene images (excluding logos/icons/SVG)
- **cta_clarity**: 30/100 — 0 primary CTAs above the fold (no clear action)

### https://solarspechub.com/batteries/

- HTTP 200 · 84,793 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 10/100 — 27 content modules detected (sections=3, h2s=27)
  - Evidence: `Editor's Picks: Top Solar Batteries for 2026` (+11 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 50/100 — No section bg classes detected (inconclusive)
- **image_density**: 10/100 — 0 real product/scene images (excluding logos/icons/SVG)
- **cta_clarity**: 30/100 — 0 primary CTAs above the fold (no clear action)

### https://solarspechub.com/brands/

- HTTP 200 · 25,645 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 100/100 — 5 content modules detected (sections=5, h2s=5)
  - Evidence: `Solar Panel Manufacturers (32)` (+4 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 50/100 — No section bg classes detected (inconclusive)
- **image_density**: 10/100 — 0 real product/scene images (excluding logos/icons/SVG)
- **cta_clarity**: 20/100 — 32 CTAs scattered above the fold — analysis paralysis

### https://solarspechub.com/best/

- HTTP 200 · 26,132 bytes
- **emoji_icons**: 100/100 — No emoji used as UI icons
- **module_density**: 100/100 — 4 content modules detected (sections=4, h2s=4)
  - Evidence: `Best Solar Panels` (+3 more)
- **boilerplate**: 100/100 — Zero AI-cliché phrases detected
- **section_rhythm**: 50/100 — No section bg classes detected (inconclusive)
- **image_density**: 10/100 — 0 real product/scene images (excluding logos/icons/SVG)
- **cta_clarity**: 20/100 — 18 CTAs scattered above the fold — analysis paralysis

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

Report generated by Patina v0.1 · 2026-05-25 22:03
