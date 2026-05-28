# Sample Patina Reports

These are real audit reports from [SolarSpec Hub](https://solarspechub.com/) — a
5720-page programmatic-SEO site — used as Patina's primary dogfood case.

## Before → After (4 weeks of iterative fixes guided by Patina)

| File | Date | Grade | Score | What was happening |
|---|---|---|---|---|
| [`solarspec_2026-05-25.md`](solarspec_2026-05-25.md) | 2026-05-25 | 🟠 **D** | **60.0** | Initial audit. AdSense placeholder, OG image 0 bytes, ITC tax credit text contradicted itself across pages, sections used identical bg colors |
| [`solarspec_2026-05-27_after.md`](solarspec_2026-05-27_after.md) | 2026-05-27 | 🟢 **A** | **96.3** | After 4 weeks of iterative fixes: added section bg rhythm, Unsplash + manufacturer hero shots, deduped CTAs, removed emoji icons, fixed module density |

## What changed between the two audits

The 5 worst dimensions in the D 60 report (`image_density 10`, `cta_clarity 30`,
`section_rhythm 57`, `module_density 63`, `boilerplate 100`) drove the iteration
plan. Each Patina report includes a **prioritized remediation roadmap** with specific
Tailwind class snippets and copy fix recipes.

For the SolarSpec case:
- `image_density 10 → 100`: Added 3+ Unsplash images per content page + manufacturer hero shots on product pages
- `cta_clarity 30 → 100`: Removed scattered secondary CTAs above the fold, kept one primary CTA per page
- `section_rhythm 57 → 88-100`: Alternated `bg-white` / `bg-gray-50` / `bg-slate-100` / `bg-stone-100` across sections
- `module_density 63 → 90`: Collapsed nested `<section>` blocks, demoted excess `<h2>` to `<h3>`
- All while keeping `boilerplate` and `emoji_icons` already-perfect 100 scores

This is the test case Patina was built for.
