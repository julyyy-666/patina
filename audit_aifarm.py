#!/usr/bin/env python3
"""
Patina — AI-Farm Audit for Programmatic SEO Sites

MVP v0.1 (2026-05-25)

Sister product to Veris (which audits data truthfulness). Patina audits
the **AI-farm feel** of a site — visual + copy + UX patterns that signal
"AI generated this, a human didn't curate it" — and outputs concrete
remediation suggestions.

Usage:
    python3 audit_aifarm.py <url> [--pages N] [--out report.md]

Example:
    python3 audit_aifarm.py https://solarspechub.com --pages 5 --out solar_patina.md

Six detection dimensions (each 0-100, higher = more human-crafted):
    1. emoji_icons       — Unicode emoji used as UI iconography
    2. module_density    — homepage section/h2 count
    3. boilerplate_copy  — AI-cliché phrase density
    4. section_rhythm    — bg color alternation across sections
    5. image_density     — real product/scene images per content page
    6. cta_clarity       — primary CTA count above the fold

Output: markdown report with per-dimension score + total grade + concrete
"do these N things to fix it" remediation list.
"""

import argparse
import urllib.request
import urllib.error
import concurrent.futures
import re
import json
import time
from collections import Counter, defaultdict
from datetime import datetime

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# ============================================================
# Detection patterns
# ============================================================

# Dimension 1: Emoji icons used as UI elements
# HTML entity emoji (e.g. &#36; &#9889; &#128267;) — common AI shortcut
RE_HTML_ENTITY_EMOJI = re.compile(r'&#(?:\d{4,6}|x[0-9a-fA-F]{4,6});')
# Direct Unicode emoji in UI-ish contexts (inside small div/span)
RE_UNICODE_EMOJI = re.compile(
    r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001F600-\U0001F64F]'
)
# Specific lazy patterns: emoji wrapped in small text class
RE_EMOJI_AS_ICON = re.compile(
    r'<(?:div|span|i)[^>]*class="[^"]*(?:text-[234]xl|text-lg|text-xl)[^"]*"[^>]*>\s*'
    r'(?:&#\d+;|[\U0001F300-\U0001F9FF\U00002600-\U000027BF])\s*</'
)

# Dimension 2: Section/h2 density on homepage
RE_SECTION_TAG = re.compile(r'<section\b', re.IGNORECASE)
RE_H2_TAG = re.compile(r'<h2[^>]*>([^<]{3,80})</h2>', re.IGNORECASE)

# Dimension 3: AI-cliché boilerplate phrases
AI_CLICHES = [
    # Marketing speak that AI loves
    r"discover the best",
    r"empower your",
    r"unlock the (?:power|secret|potential)",
    r"in today'?s fast[- ]paced",
    r"revolutioniz(?:e|ing)",
    r"game[- ]chang(?:er|ing)",
    r"comprehensive guide",
    r"cutting[- ]edge",
    r"seamlessly",
    r"elevate your",
    r"take your \w+ to the next level",
    r"unleash the (?:power|potential)",
    r"transform your",
    r"world[- ]class",
    r"state[- ]of[- ]the[- ]art",
    r"one[- ]stop (?:shop|solution|resource)",
    r"deep dive into",
    r"navigate the (?:complex|world)",
    r"harness the power",
    r"at your fingertips",
    # Programmatic SEO listicle clichés
    r"top \d+ (?:best )?\w+ (?:for|in) 20\d{2}",
    r"ultimate guide",
    r"everything you need to know",
    r"the ultimate",
]
RE_CLICHES = re.compile(r'\b(?:' + '|'.join(AI_CLICHES) + r')\b', re.IGNORECASE)

# Dimension 4: Section bg color variety (tailwind / inline style)
RE_SECTION_BG = re.compile(
    r'<section[^>]*class="[^"]*\b(bg-(?:white|gray-\d+|neutral-\d+|primary|accent|black|slate-\d+|zinc-\d+|stone-\d+)(?:/\d+)?)\b',
    re.IGNORECASE
)

# Dimension 5: Real images (not icons / logos / sprites / 1px tracking)
RE_IMG = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', re.IGNORECASE)
RE_IMG_PRODUCT_LIKE = re.compile(
    r'\.(?:jpe?g|png|webp|avif)(?:\?|"|$)', re.IGNORECASE
)
# Filter out: tiny icons by alt/class, logos, sprites
def looks_like_real_image(img_tag):
    if 'icon' in img_tag.lower(): return False
    if 'logo' in img_tag.lower(): return False
    if 'sprite' in img_tag.lower(): return False
    if 'avatar' in img_tag.lower(): return False
    if 'badge' in img_tag.lower(): return False
    if '.svg' in img_tag.lower(): return False  # SVG usually decorative
    # Skip tracking pixels (width=1 or height=1)
    if re.search(r'\b(?:width|height)="1"', img_tag): return False
    return True

# Dimension 6: CTA count above the fold
# Heuristic: count <a> with button-like classes inside first <section>
RE_FIRST_SECTION = re.compile(
    r'<section\b[^>]*>(.*?)</section>',
    re.IGNORECASE | re.DOTALL
)
RE_BUTTON_LINK = re.compile(
    r'<(?:a|button)\b[^>]*class="[^"]*\b(?:bg-\w+|border-\d+|rounded-(?:lg|xl|full)|btn|button)\b',
    re.IGNORECASE
)


# ============================================================
# Core fetcher (mirrors Veris)
# ============================================================

def fetch(url, timeout=15, max_bytes=None):
    """Fetch URL via curl subprocess. curl handles gzip/br/HTTP-2/Cloudflare
    automatically; avoids urllib's brittleness against modern CDN responses.

    Returns (status_code_int_or_string, html_text).
    """
    import subprocess
    try:
        # --compressed handles gzip/br/deflate
        # -s silent, -L follow redirects, --max-time enforces total timeout
        # -w writes status code to stderr-like channel via %{http_code}
        # We split with a sentinel: body...\n<<<PATINA_STATUS:200>>>
        cmd = [
            'curl', '-sL', '--compressed',
            '--max-time', str(timeout),
            '-A', UA,
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            '-H', 'Accept-Language: en-US,en;q=0.9',
            '-w', '\n<<<PATINA_STATUS:%{http_code}>>>',
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
        out = result.stdout.decode('utf-8', errors='ignore')
        m = re.search(r'<<<PATINA_STATUS:(\d+)>>>$', out)
        if m:
            status = int(m.group(1))
            html = out[:m.start()].rstrip()
        else:
            status = 'ERR:no_status'
            html = out
        if max_bytes:
            html = html[:max_bytes]
        return (status, html)
    except subprocess.TimeoutExpired:
        return ('ERR:Timeout', '')
    except Exception as e:
        return (f'ERR:{type(e).__name__}', '')


def fetch_sitemap(site_url):
    candidates = [
        f'{site_url}/sitemap-0.xml',
        f'{site_url}/sitemap.xml',
        f'{site_url}/sitemap-index.xml',
    ]
    for sm_url in candidates:
        status, xml = fetch(sm_url, timeout=10)
        if status == 200 and xml:
            urls = re.findall(r'<loc>([^<]+)</loc>', xml)
            if urls:
                if '<sitemap>' in xml and '<urlset>' not in xml:
                    all_urls = []
                    for sub_sm in urls[:5]:
                        s2, x2 = fetch(sub_sm, timeout=10)
                        if s2 == 200:
                            all_urls.extend(re.findall(r'<loc>([^<]+)</loc>', x2))
                    return all_urls
                return urls
    return []


# ============================================================
# Per-dimension scorers (each returns 0-100, higher = more human)
# ============================================================

def score_emoji_icons(html):
    """100 = no UI emoji, 0 = heavy emoji UI."""
    matches = RE_EMOJI_AS_ICON.findall(html)
    entity_count = len(RE_HTML_ENTITY_EMOJI.findall(html))
    if not matches and entity_count == 0:
        return 100, "No emoji used as UI icons", []
    # Penalize emoji-as-icon heavily; entity emoji also bad
    penalty = min(60, len(matches) * 15) + min(30, entity_count * 5)
    score = max(0, 100 - penalty)
    evidence = []
    for m in matches[:5]:
        evidence.append(m[:120])
    if entity_count > 0:
        evidence.append(f"{entity_count} HTML entity emoji refs (e.g. &#36; &#9889;) — typical AI shortcut")
    return score, f"{len(matches)} emoji-as-icon + {entity_count} HTML-entity emoji found", evidence


def score_module_density(html):
    """100 = 4-6 sections, 0 = 11+ sections piled up."""
    sections = len(RE_SECTION_TAG.findall(html))
    h2s = RE_H2_TAG.findall(html)
    h2_count = len(h2s)
    # Use max of sections/h2 as effective module count
    n = max(sections, h2_count)
    if n <= 6:
        score = 100
    elif n <= 8:
        score = 75
    elif n <= 10:
        score = 50
    elif n <= 12:
        score = 30
    else:
        score = 10
    return score, f"{n} content modules detected (sections={sections}, h2s={h2_count})", h2s[:12]


def score_boilerplate(html):
    """100 = no AI clichés, 0 = drowning in marketing speak."""
    # Strip tags for cleaner text analysis
    text = re.sub(r'<[^>]+>', ' ', html)
    matches = RE_CLICHES.findall(text)
    if not matches:
        return 100, "Zero AI-cliché phrases detected", []
    penalty = min(80, len(matches) * 10)
    score = max(0, 100 - penalty)
    sample = list(dict.fromkeys(matches))[:8]  # unique, keep order
    return score, f"{len(matches)} AI-cliché phrase occurrences ({len(set(matches))} unique)", sample


def score_section_rhythm(html):
    """100 = alternating bg (rhythm), 0 = all same bg (monotone)."""
    bgs = RE_SECTION_BG.findall(html)
    if not bgs:
        return 50, "No section bg classes detected (inconclusive)", []
    counter = Counter(bgs)
    most_common, most_count = counter.most_common(1)[0]
    monotone_ratio = most_count / len(bgs) if bgs else 0
    if monotone_ratio > 0.85:
        score = 20
    elif monotone_ratio > 0.7:
        score = 40
    elif monotone_ratio > 0.5:
        score = 60
    elif monotone_ratio > 0.3:
        score = 85
    else:
        score = 100
    return score, f"{len(bgs)} section bg classes; '{most_common}' covers {int(monotone_ratio*100)}%", list(counter.items())[:5]


def score_image_density(html):
    """100 = ≥3 real images per content page, 0 = pure text desert."""
    all_imgs = RE_IMG.findall(html)
    # Re-grab full <img ...> tag string for filter
    full_tags = re.findall(r'<img\b[^>]*>', html, re.IGNORECASE)
    real_imgs = [t for t in full_tags if looks_like_real_image(t)]
    n = len(real_imgs)
    if n >= 3:
        score = 100
    elif n == 2:
        score = 70
    elif n == 1:
        score = 40
    else:
        score = 10
    return score, f"{n} real product/scene images (excluding logos/icons/SVG)", [t[:100] for t in real_imgs[:3]]


def score_cta_clarity(html):
    """100 = 1 clear CTA + secondary, 0 = 7+ scattered CTAs."""
    # Look at first <section> only (above the fold proxy)
    first_section = RE_FIRST_SECTION.search(html)
    target = first_section.group(1) if first_section else html[:5000]
    ctas = RE_BUTTON_LINK.findall(target)
    n = len(ctas)
    if n == 0:
        score = 30  # no CTA at all is also bad
        msg = "0 primary CTAs above the fold (no clear action)"
    elif n <= 2:
        score = 100
        msg = f"{n} primary CTA(s) — focused"
    elif n <= 4:
        score = 75
        msg = f"{n} CTAs above the fold — slightly busy"
    elif n <= 6:
        score = 50
        msg = f"{n} CTAs — too many competing entries"
    else:
        score = 20
        msg = f"{n} CTAs scattered above the fold — analysis paralysis"
    return score, msg, []


# ============================================================
# Per-page audit
# ============================================================

def audit_page(url):
    status, html = fetch(url)
    findings = {
        'url': url,
        'status': status,
        'html_size': len(html) if html else 0,
        'dimensions': {},
    }
    if status != 200 or not html:
        return findings
    scorers = [
        ('emoji_icons',    score_emoji_icons),
        ('module_density', score_module_density),
        ('boilerplate',    score_boilerplate),
        ('section_rhythm', score_section_rhythm),
        ('image_density',  score_image_density),
        ('cta_clarity',    score_cta_clarity),
    ]
    for name, fn in scorers:
        score, summary, evidence = fn(html)
        findings['dimensions'][name] = {
            'score': score,
            'summary': summary,
            'evidence': evidence,
        }
    return findings


# ============================================================
# Aggregate + grade
# ============================================================

def aggregate(per_page_findings):
    """Average each dimension across pages, then overall."""
    dim_scores = defaultdict(list)
    for f in per_page_findings:
        if not f.get('dimensions'):
            continue
        for dim, info in f['dimensions'].items():
            dim_scores[dim].append(info['score'])
    avg_dims = {dim: round(sum(s) / len(s), 1) if s else 0 for dim, s in dim_scores.items()}
    total = round(sum(avg_dims.values()) / len(avg_dims), 1) if avg_dims else 0
    if total >= 90: grade, label = 'A', 'Human-crafted'
    elif total >= 80: grade, label = 'B', 'Mostly human'
    elif total >= 70: grade, label = 'C', 'Some AI traces'
    elif total >= 60: grade, label = 'D', 'Noticeably AI-farm'
    elif total >= 40: grade, label = 'F', 'Clearly AI-generated'
    else: grade, label = 'F', 'Severe AI farm'
    return {
        'avg_dimensions': avg_dims,
        'total_score': total,
        'grade': grade,
        'label': label,
    }


# ============================================================
# Remediation suggestions (the money output)
# ============================================================

REMEDIATIONS = {
    'emoji_icons': {
        'why': "Unicode emoji `$ ⛨ 🔋 ⏱ ⚡` used as UI icons is the #1 AI-farm tell — Google AdSense reviewers, designers, and users all read it as 'low-effort template'.",
        'fix': """Replace each emoji with an inline SVG from a real icon system:
  - **Lucide** (lucide.dev) — free, MIT, 1000+ icons matching modern web aesthetic
  - **Phosphor** (phosphoricons.com) — multi-weight, free
  - **Heroicons** (heroicons.com) — Tailwind-native
Pattern: wrap SVG in `<div class="w-11 h-11 flex items-center justify-center bg-accent/10 rounded-lg text-accent">` for branded icon containers.""",
    },
    'module_density': {
        'why': "10+ stacked sections is a programmatic-SEO anti-pattern. Yes EnergySage etc. do it, but the AI tell is when each section is generic ('Popular X', 'Top Y', 'Best Z') with no internal hierarchy.",
        'fix': """Either:
  - **Collapse** to 5-6 high-signal sections (Hero, primary entries, social proof, CTA, FAQ, About)
  - Or **add internal hierarchy**: turn 'Popular Comparisons' into `<details>` accordions, group with `<h3>` instead of `<h2>`, demote secondary sections""",
    },
    'boilerplate': {
        'why': "Phrases like 'Discover the best', 'Unlock the power of', 'Comprehensive guide' are AI's default vocabulary. A real expert writes specific numbers and specific scenarios, not abstract verbs.",
        'fix': """Find/replace pass:
  - 'Discover the best X' → 'Compare specs for X (n=N verified, updated MMM YYYY)'
  - 'Empower your home with solar' → 'Sized for a 1800 sqft home pulling 9.5 MWh/yr'
  - 'Comprehensive guide' → 'X SKUs across Y brands' or specific scope
  - 'Cutting-edge' → name the specific tech (TOPCon / HJT / heterojunction)""",
    },
    'section_rhythm': {
        'why': "When >70% of sections share one bg color, the page reads as a wall of cards. Apple/Stripe alternate white / off-white / dark sections to create rhythm — this signals 'a designer touched this'.",
        'fix': """Alternate bg per section using Tailwind tokens:
  - Section 1 (hero): `bg-white py-16`
  - Section 2: `bg-gray-50 py-20`
  - Section 3: `bg-neutral-950 text-white py-24` (dark band)
  - Section 4: `bg-white py-20`
  Larger vertical padding (py-20 / py-24) on contentful sections + tight py-12 on lists.""",
    },
    'image_density': {
        'why': "Zero real images = AI agriculture's most famous tell. Stock photos are still better than nothing — and product/spec sites need actual product photography to break the text wall.",
        'fix': """Add 1-3 real images per content page:
  - Product pages: Pull manufacturer hero shot from the same datasheet URL you cite
  - Guides: Add 1 schematic + 1 contextual photo (rooftop install / panel close-up)
  - State pages: Add 1 location-relevant image (state map or local install)
  - For purely tabular pages: at minimum add brand logo SVGs at the top of brand sections
  Source: Unsplash (free), Pexels (free), or scraped manufacturer assets per their press kit.""",
    },
    'cta_clarity': {
        'why': "7+ primary CTAs above the fold = decision paralysis. Hick's Law: choice time grows logarithmically with options. AI scaffolds always overload because they don't trust any single CTA.",
        'fix': """Restructure hero to:
  - **One** primary CTA (strong color, large) — your single most-wanted action
  - **One** secondary link/ghost button (smaller, lower contrast)
  - Demote category navigation to the header nav, not the hero body
  Pattern: `<button class="bg-accent text-white px-8 py-4 rounded-xl text-lg font-bold">Primary</button><a class="text-gray-600 underline text-sm ml-4">or learn more</a>`""",
    },
}


def build_remediations(agg):
    """Return ordered list of fixes, worst dimension first."""
    fixes = []
    for dim, score in sorted(agg['avg_dimensions'].items(), key=lambda x: x[1]):
        if score >= 90:
            continue  # skip dimensions that are already good
        priority = 'P0' if score < 40 else ('P1' if score < 70 else 'P2')
        r = REMEDIATIONS.get(dim, {})
        fixes.append({
            'dimension': dim,
            'score': score,
            'priority': priority,
            'why': r.get('why', ''),
            'fix': r.get('fix', ''),
        })
    return fixes


# ============================================================
# Report renderer
# ============================================================

def render_report(site_url, audited_urls, per_page, agg, fixes, elapsed):
    grade_emoji = {'A': '🟢', 'B': '🟢', 'C': '🟡', 'D': '🟠', 'F': '🔴'}.get(agg['grade'], '⚪')
    md = f"""# Patina AI-Farm Audit

> Site: **{site_url}**
> Date: {datetime.now().strftime('%Y-%m-%d')}
> Pages audited: {len(audited_urls)}
> Duration: {elapsed:.1f}s

## {grade_emoji} Overall: **{agg['total_score']}/100** — Grade **{agg['grade']}** ({agg['label']})

### Per-Dimension Scores

| Dimension | Score | Read |
|---|---|---|
"""
    READS = {
        'emoji_icons':    'Icon system (Unicode emoji = AI tell)',
        'module_density': 'Section count (11+ = programmatic anti-pattern)',
        'boilerplate':    'AI-cliché phrase density',
        'section_rhythm': 'Visual rhythm (bg color variety across sections)',
        'image_density':  'Real images per page (zero = AI farm)',
        'cta_clarity':    'Above-the-fold CTA focus',
    }
    for dim, score in agg['avg_dimensions'].items():
        emoji = '🟢' if score >= 80 else ('🟡' if score >= 60 else ('🟠' if score >= 40 else '🔴'))
        md += f"| **{dim}** | {emoji} {score} | {READS.get(dim, '')} |\n"

    md += "\n---\n\n## 🔧 Remediation Roadmap (worst-first)\n\n"
    if not fixes:
        md += "✨ All dimensions ≥90. No critical AI-farm signals detected.\n"
    for i, f in enumerate(fixes, 1):
        md += f"### {i}. [{f['priority']}] `{f['dimension']}` — {f['score']}/100\n\n"
        md += f"**Why it matters:** {f['why']}\n\n"
        md += f"**Fix:**\n\n{f['fix']}\n\n---\n\n"

    md += "## 📋 Per-Page Detail\n\n"
    for p in per_page:
        md += f"### {p['url']}\n\n"
        if p.get('status') != 200:
            md += f"- ❌ Status: {p['status']}\n\n"
            continue
        md += f"- HTTP {p['status']} · {p['html_size']:,} bytes\n"
        for dim, info in p.get('dimensions', {}).items():
            md += f"- **{dim}**: {info['score']}/100 — {info['summary']}\n"
            if info.get('evidence'):
                ev = info['evidence']
                if isinstance(ev, list) and ev:
                    md += f"  - Evidence: `{ev[0]}`{f' (+{len(ev)-1} more)' if len(ev) > 1 else ''}\n"
        md += "\n"

    md += f"""---

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

Report generated by Patina v0.1 · {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    return md


# ============================================================
# Orchestrator
# ============================================================

def pick_pages_to_audit(all_urls, n):
    """Patina audits a small sample of distinct pages (homepage + key
    section landings + a handful of product pages). Not stratified
    sampling like Veris — we want representative diversity."""
    if not all_urls:
        return []
    chosen = []
    # Always include root
    roots = [u for u in all_urls if u.rstrip('/').count('/') <= 2]
    if roots:
        chosen.append(roots[0])
    # Pick distinct section landings (one per top-level path)
    seen_sections = set()
    for u in all_urls:
        parts = u.rstrip('/').split('/')
        if len(parts) >= 4:
            section = parts[3]
            if section not in seen_sections:
                seen_sections.add(section)
                chosen.append(u)
        if len(chosen) >= n:
            break
    return chosen[:n]


def run(site_url, pages=5, concurrency=5):
    site_url = site_url.rstrip('/')
    print(f'\n🔍 Patina AI-farm audit: {site_url}')
    print(f'   Pages to audit: {pages}\n')
    started = time.time()

    print('   1/3 Fetching sitemap...')
    all_urls = fetch_sitemap(site_url)
    if not all_urls:
        # Fallback: just audit homepage
        all_urls = [site_url]
    print(f'   ✓ Found {len(all_urls)} URLs')

    print(f'   2/3 Selecting representative pages...')
    selected = pick_pages_to_audit(all_urls, pages)
    if site_url not in selected and len([u for u in selected if u.rstrip('/') == site_url]) == 0:
        selected.insert(0, site_url)
    selected = selected[:pages]
    print(f'   ✓ Auditing: {", ".join(u.replace(site_url, "/") or "/" for u in selected)}')

    print(f'   3/3 Running 6-dimension scoring (concurrency={concurrency})...')
    per_page = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {ex.submit(audit_page, u): u for u in selected}
        for f in concurrent.futures.as_completed(futures):
            per_page.append(f.result())

    elapsed = time.time() - started
    agg = aggregate(per_page)
    fixes = build_remediations(agg)
    report = render_report(site_url, selected, per_page, agg, fixes, elapsed)
    return report, agg, per_page


def main():
    ap = argparse.ArgumentParser(description='Patina — AI-farm audit')
    ap.add_argument('url', help='Site URL (e.g. https://solarspechub.com)')
    ap.add_argument('--pages', type=int, default=5, help='Number of pages to audit (default 5)')
    ap.add_argument('--out', default=None, help='Output markdown file (default: stdout)')
    ap.add_argument('--json', default=None, help='Also dump raw JSON to this file')
    ap.add_argument('--concurrency', type=int, default=5)
    args = ap.parse_args()

    report, agg, per_page = run(args.url, pages=args.pages, concurrency=args.concurrency)

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f'\n✅ Report → {args.out}')
    else:
        print('\n' + report)

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump({'agg': agg, 'per_page': per_page}, f, indent=2, default=str)
        print(f'✅ JSON   → {args.json}')

    print(f'\n📊 Grade: {agg["grade"]} ({agg["total_score"]}/100) — {agg["label"]}')


if __name__ == '__main__':
    main()
