# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

Static HTML/CSS/JavaScript personal portfolio and consulting website for Shane Thomas Strough. No build system, package manager, or framework—edit files directly and view in browser. Hosted on GitHub Pages, deployed from `main` branch.

## Development

**No build commands required.** Open any `.html` file directly in a browser.

To test locally with a development server (optional):
```bash
npx serve .
# or
python -m http.server 8000
```

## Deployment

- **Hosting:** GitHub Pages from the `main` branch
- **Repo:** `shane-thomas-strough/shane-thomas-strough.github.io`
- **Domain:** `shanestrough.com` (configured via CNAME)
- **Local branch:** `master` — push to `main` with `git push origin master:main`

## Architecture

### File Structure
- `index.html` — Main portfolio/marketing page (hero, expertise grid, timeline, services, contact)
- `insights.html` — Technical library/field notes page with article filtering
- `poetry.html` — Poetry page ("The Accent of the Soul" + backstory). Uses warm gold accents (`--warm`) instead of cyan for key elements
- `Poetry/` — Source markdown for poems (not served directly; content is rendered into `poetry.html`)
- `images/` — Image assets
- `sitemap.xml` — Sitemap submitted to Google Search Console
- `.github/workflows/index-search-engines.yml` — Automated search engine indexing

### Design System (CSS Custom Properties)

Colors:
- Primary accent: `--electric` (#00E5FF)
- Warm accent: `--warm` (#C8A96E)
- Backgrounds: Various deep blacks and grays (`--black`, `--deep`, `--panel`)
- Border: `--border` (#1E2D3D)
- Text: `--white` (#F0F4F8), `--muted` (#6B8099)

Typography:
- Headings: Bebas Neue
- Serif accents / poetry: Fraunces
- Body/monospace: DM Mono

### CSS/JavaScript Patterns

**All CSS is embedded** in `<style>` tags within each HTML file. No external stylesheets.

**Responsive breakpoints:** 900px, 768px, 600px, 480px

**Animations:** CSS keyframes (`fadeInUp`, `gridPulse`, `glowFloat`) triggered by Intersection Observer on scroll. Poetry page uses `reveal-slow` class for slower, contemplative animations.

**JavaScript features:**
- Sticky nav behavior with scroll-triggered padding changes
- Mobile hamburger menu toggle
- Article filtering (insights page)
- Staggered animation delays for card grids

### SEO/Structured Data

All pages include JSON-LD schema markup:
- `index.html` — Person schema
- `insights.html` — CollectionPage schema
- `poetry.html` — CreativeWork schema

### Automated Search Engine Indexing

A GitHub Actions workflow (`.github/workflows/index-search-engines.yml`) runs on every push to `main` that changes `.html` files:

1. **IndexNow** (Bing, Yandex, Seznam, Naver) — batch submission, no auth required. Key file: `5891ff7061e0f42802e84221382b9ca9.txt`
2. **Google Indexing API** — OAuth2 via service account. Credentials stored as GitHub secret `GOOGLE_INDEXING_KEY`

**No manual indexing steps are needed.** Changed pages are automatically submitted to all search engines on deploy.

Google Cloud project: `shanestrough-indexing`
Service account: `indexing-bot@shanestrough-indexing.iam.gserviceaccount.com` (Owner in Search Console)

### Image Handling

Images use native lazy loading (`loading="lazy"` attribute). No build-time image optimization.

### Contact/Email

Email addresses are protected via Cloudflare email obfuscation.

## Navigation

All pages share a consistent nav. When adding new pages, update the nav in all three HTML files and add the page to `sitemap.xml`.
