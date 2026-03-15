# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML/CSS/JavaScript personal portfolio and consulting website for Shane Thomas Strough. No build system, package manager, or framework—edit files directly and view in browser.

## Development

**No build commands required.** Open `index.html` or `insights.html` directly in a browser.

To test locally with a development server (optional):
```bash
npx serve .
# or
python -m http.server 8000
```

## Architecture

### File Structure
- `index.html` - Main portfolio/marketing page with all sections (hero, expertise grid, timeline, services, contact)
- `insights.html` - Technical library/field notes page with article filtering
- `images/` - Image assets

### Design System (CSS Custom Properties)

Colors:
- Primary accent: `--cyan` (#00E5FF)
- Warm accent: `--gold` (#C8A96E)
- Backgrounds: Various deep blacks and grays

Typography:
- Headings: Bebas Neue
- Serif accents: Fraunces
- Body/monospace: DM Mono

### CSS/JavaScript Patterns

**All CSS is embedded** in `<style>` tags within each HTML file. No external stylesheets.

**Responsive breakpoints:** 900px, 768px, 600px, 480px

**Animations:** CSS keyframes (`fadeInUp`, `gridPulse`, `glowFloat`) triggered by Intersection Observer on scroll.

**JavaScript features:**
- Sticky nav behavior with scroll-triggered padding changes
- Mobile hamburger menu toggle
- Article filtering (insights page)
- Staggered animation delays for card grids

### SEO/Structured Data

Both pages include JSON-LD schema markup (Person, CollectionPage) for search engine optimization.

### Image Handling

Images use native lazy loading (`loading="lazy"` attribute). No build-time image optimization.

### Contact/Email

Email addresses are protected via Cloudflare email obfuscation.
