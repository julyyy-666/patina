# Patina — AI-Farm Audit for Websites

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: v0.1 MVP](https://img.shields.io/badge/status-v0.1%20MVP-orange.svg)]()

> Patina audits the **AI-farm feel** of a website — the visual + copy + UX patterns
> that signal *"AI generated this, a human didn't curate it"* — and outputs concrete
> remediation suggestions.

**Why "Patina"?** Real-world objects develop patina — surface marks from genuine use.
Curated websites have a similar quality: small inconsistencies, varied rhythm, human
attention. AI-generated sites are uniformly clean in the wrong way. Patina detects that.

---

## Why Patina (vs Lighthouse / PageSpeed / Ahrefs)

| Tool | What it measures | Detects AI-farm patterns? |
|---|---|---|
| **Google Lighthouse / PageSpeed** | Performance + accessibility + SEO best practices | ❌ No |
| **Ahrefs / Semrush** | Backlinks, keyword rankings, SERP visibility | ❌ No |
| **Originality.ai / GPTZero** | Whether a single block of **text** is AI-written | ⚠️ Text only, not site-level |
| **Sistrix Visibility Index** | SERP movement (indirect proxy for Google AI-farm penalties) | ⚠️ Lagging indicator |
| **Patina** | Visual + copy + UX patterns of the entire site | ✅ Direct, immediate |

If you run a programmatic-SEO site and worry that Google's algorithm flags it as
low-quality AI content, **Patina gives you a concrete score + fix list** before
Google's next core update demolishes your rankings.

---

## Quick start

```bash
git clone https://github.com/julyyy-666/patina.git
cd patina
python3 audit_aifarm.py https://your-site.com --pages 5 --out report.md
```

Requirements: **Python 3.8+ stdlib + `curl` on PATH**. No external dependencies.

---

## Six detection dimensions

Each scored 0-100 (higher = more human-crafted). Total is the average.

| # | Dimension | What it catches | Why it matters |
|---|---|---|---|
| 1 | `emoji_icons` | Unicode emoji or HTML entity emoji (`💡` `⚡`) used as UI iconography | Real designers use SVG/icon-font; emoji as icons = AI shortcut |
| 2 | `module_density` | Homepage section/h2 count — 11+ is anti-pattern | Programmatic-SEO sites stack identical sections; humans stop at 5-8 |
| 3 | `boilerplate_copy` | AI-cliché phrases ("Discover the best", "Unlock the power of") | Detectable LLM tells in copy |
| 4 | `section_rhythm` | Background color variety across sections | Monotone bg = no designer touched it |
| 5 | `image_density` | Real product/scene images per page (excluding logos/icons/SVG) | Zero images = pure text desert, classic AI farm |
| 6 | `cta_clarity` | Primary CTA count above the fold | 7+ scattered CTAs = Hick's Law violation |

---

## Grading

| Score | Grade | Label |
|---|---|---|
| 90-100 | A | Human-crafted |
| 80-89 | B | Mostly human |
| 70-79 | C | Some AI traces |
| 60-69 | D | Noticeably AI-farm |
| 40-59 | F | Clearly AI-generated |
| <40 | F | Severe AI farm |

---

## Example output

```
🔍 Patina AI-farm audit: https://solarspechub.com
   Pages to audit: 5

   1/3 Fetching sitemap...
   ✓ Found 5720 URLs
   2/3 Selecting representative pages...
   ✓ Auditing: /, /about/, /api/, /authors/jianlin/, /batteries/
   3/3 Running 6-dimension scoring (concurrency=5)...

✅ Report → report.md

📊 Grade: A (96.3/100) — Human-crafted
```

The generated `report.md` includes:
- Per-dimension scores
- Per-page detail (which sections triggered which signals)
- **Prioritized remediation roadmap** with concrete fix recipes:
  - Tailwind tokens for `section_rhythm`
  - Icon library suggestions for `emoji_icons`
  - Unsplash + manufacturer hero shots for `image_density`
  - Specific cliché phrases to rewrite for `boilerplate_copy`

📄 **Sample report**: see [`samples/solarspec_2026-05-25.md`](samples/solarspec_2026-05-25.md)
(real audit from a 5720-page programmatic-SEO site over 4 weeks of iterative fixes:
D 60 → A 96.3 with this tool guiding each iteration).

---

## CLI options

```bash
python3 audit_aifarm.py <URL> [options]

Options:
  --pages N         Pages to audit (default: 5, max: 50)
  --out FILE        Output markdown report file (default: stdout)
  --concurrency N   Parallel HTTP fetches (default: 5)
  --timeout SEC     Per-page fetch timeout (default: 10)
```

---

## Roadmap

- **v0.1** (2026-05-25): CLI MVP, 6 dimensions, markdown output ← **you are here**
- **v0.2** (planned): Section-type awareness — brand-listing pages shouldn't be
  penalized for "32 CTAs" when those are brand links, not hero buttons
- **v0.3** (planned): LLM-assisted boilerplate detection (Claude API for nuanced
  cliché spotting beyond regex)
- **v1.0** (planned): Web UI + Stripe paid tier ($9 single audit / $29/mo unlimited)

---

## Who is Patina for?

- **Programmatic-SEO site operators** worried about Google AI-content penalties
- **Affiliate-site builders** validating that their template + AI content doesn't
  trigger algorithmic downranking
- **SEO agencies** running pre-launch audits for clients
- **Content engineers** doing PR reviews on AI-assisted site updates

---

## Sister project: Veris

[Veris](https://github.com/julyyy-666/veris) (coming soon) audits the **data
truthfulness** of a programmatic-SEO site — broken links, render anomalies, source
citation density, trust signals.

**Patina + Veris together** form a complete trust-audit suite for AI-built sites.

---

## Contributing

This is an early MVP. Contributions welcome:

1. Open an issue describing the false-positive / false-negative case you hit
2. Include the URL + the dimension that misfired
3. PRs that add new heuristics get merged fast if they preserve the
   "no external dependencies" rule (Python stdlib + curl only)

---

## License

[MIT](LICENSE) — use freely for commercial and non-commercial projects.

---

*Built by [Jianlin](https://solarspechub.com/authors/jianlin/) — first dogfooded on
[SolarSpec Hub](https://solarspechub.com/) (5720-page programmatic-SEO site).*
