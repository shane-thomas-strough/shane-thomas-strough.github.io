"""Render the Strix field study into the site's existing article layout."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]
SOURCE = SITE / "_build/strix-workflow-report.md"
TEMPLATE = SITE / "stale-state.html"
OUTPUT = SITE / "the-finding-is-not-the-report.html"
SLUG = OUTPUT.name
TITLE = "The Finding Is Not the Report"
SUBTITLE = "What twenty-four local Strix attempts taught me about security-agent reliability"
DESCRIPTION = (
    "A controlled field study of four locally served security agents: why finding a flaw, "
    "proving it, and delivering a usable report are different outcomes."
)


def inline(value: str) -> str:
    value = html.escape(value, quote=False)
    code: list[str] = []

    def hold(match: re.Match[str]) -> str:
        code.append(f"<code>{match.group(1)}</code>")
        return f"\x00{len(code) - 1}\x00"

    value = re.sub(r"`([^`]+)`", hold, value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*(.+?)\*", r"<em>\1</em>", value)
    for index, element in enumerate(code):
        value = value.replace(f"\x00{index}\x00", element)
    return value


EVIDENCE_CHAIN = """<figure class="study-figure chain-figure" aria-labelledby="chain-caption">
  <div class="chain-grid" role="list">
    <div role="listitem"><span>01</span><strong>Locate</strong><small>The right route and mechanism</small></div>
    <div role="listitem"><span>02</span><strong>Prove</strong><small>A discriminating, harmless result</small></div>
    <div role="listitem"><span>03</span><strong>Control</strong><small>Reject nearby safe routes</small></div>
    <div role="listitem"><span>04</span><strong>File</strong><small>A structured artifact exists</small></div>
    <div role="listitem"><span>05</span><strong>Bound</strong><small>Scope and impact match evidence</small></div>
  </div>
  <figcaption id="chain-caption">The evaluation chain. A result must survive each handoff; an earlier success cannot fill in a missing later artifact.</figcaption>
</figure>"""

REPORT_FIGURE = """<figure class="study-figure delivery-figure" aria-labelledby="delivery-caption">
  <div class="figure-heading"><span>FIGURE 1 / STRUCTURED REPORT DELIVERY</span><strong>Filed is an artifact state, not a quality score</strong></div>
  <div class="bar-row"><span>Hinted target</span><div class="bar-track"><div class="bar-fill" style="width:83.333%"></div></div><strong>10 / 12</strong></div>
  <div class="bar-row"><span>Four-flaw target</span><div class="bar-track"><div class="bar-fill warm-fill" style="width:33.333%"></div></div><strong>4 / 12</strong></div>
  <figcaption id="delivery-caption">Ten of twelve hinted-target attempts produced a findings file; four of twelve four-flaw attempts did. The targets differ in difficulty and instruction, so this is a description of these runs, not a measured difficulty effect. The bars count file presence, not valid findings.</figcaption>
</figure>"""


def render_markdown(source: str) -> str:
    lines = source.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    index = 0

    def flush() -> None:
        if paragraph:
            output.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    while index < len(lines):
        line = lines[index].strip()
        if not line:
            flush()
            index += 1
            continue
        if line.startswith("# "):
            flush()
            index += 1
            continue
        if line == "[EVIDENCE CHAIN]":
            flush()
            output.append(EVIDENCE_CHAIN)
            index += 1
            continue
        if line == "[REPORT DELIVERY FIGURE]":
            flush()
            output.append(REPORT_FIGURE)
            index += 1
            continue
        if line.startswith("## "):
            flush()
            output.append(f'<h2 class="section-header">{inline(line[3:])}</h2>')
            index += 1
            continue
        if line.startswith("| "):
            flush()
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    rows.append(cells)
                index += 1
            header, *body = rows
            parts = ['<div class="tbl-wrap"><table><thead><tr>']
            parts.extend(f"<th>{inline(cell)}</th>" for cell in header)
            parts.append("</tr></thead><tbody>")
            for row in body:
                parts.append("<tr>")
                parts.extend(f"<td>{inline(cell)}</td>" for cell in row)
                parts.append("</tr>")
            parts.append("</tbody></table></div>")
            output.append("".join(parts))
            continue
        paragraph.append(line)
        index += 1
    flush()
    return "\n".join(output)


def build() -> None:
    template = TEMPLATE.read_text()
    style = "\n".join(re.findall(r"<style>.*?</style>", template, re.S))
    footer = template.split("<!-- FOOTER -->", 1)[1]
    source = SOURCE.read_text()
    body = render_markdown(source)
    report_css = """<style>
      .study-label { margin: 0 0 1rem; color: var(--warm); font-size: .65rem; letter-spacing: .21em; text-transform: uppercase; }
      .nav-hamburger { border: 0; background: transparent; padding: .5rem; }
      .article-content { max-width: 850px; }
      .article-content p { line-height: 1.86; }
      .article-content h2 { scroll-margin-top: 7rem; }
      .study-figure { margin: 2.7rem 0; padding: 1.4rem; border: 1px solid var(--border); background: linear-gradient(140deg, rgba(0,229,255,.045), rgba(200,169,110,.025)); }
      .study-figure figcaption { color: #A8B8C8; font-size: .78rem; line-height: 1.65; margin-top: 1.3rem; }
      .chain-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: .5rem; }
      .chain-grid > div { padding: .9rem .7rem; border-top: 2px solid var(--electric); background: rgba(8,10,12,.45); min-width: 0; }
      .chain-grid span { display: block; color: var(--electric); font-size: .62rem; letter-spacing: .15em; margin-bottom: .5rem; }
      .chain-grid strong { display: block; font-family: 'Bebas Neue', sans-serif; font-size: 1.45rem; font-weight: 400; letter-spacing: .05em; }
      .chain-grid small { display: block; color: #A8B8C8; font-size: .7rem; line-height: 1.5; margin-top: .45rem; }
      .figure-heading span { display: block; color: var(--electric); font-size: .64rem; letter-spacing: .15em; margin-bottom: .45rem; }
      .figure-heading strong { display: block; font-family: 'Fraunces', serif; font-size: 1.14rem; font-weight: 400; margin-bottom: 1.4rem; }
      .bar-row { display: grid; grid-template-columns: 9.2rem 1fr 4.4rem; align-items: center; gap: .75rem; margin: .9rem 0; font-size: .78rem; }
      .bar-row > span { color: var(--white); }
      .bar-row > strong { text-align: right; font-weight: 500; font-variant-numeric: tabular-nums; }
      .bar-track { height: 1.1rem; background: rgba(107,128,153,.17); }
      .bar-fill { height: 100%; background: var(--electric); }
      .bar-fill.warm-fill { background: var(--warm); }
      .downloads { margin: 3rem 0; padding: 1.4rem; border: 1px solid var(--border); background: var(--panel); }
      .downloads h2 { margin: 0 0 .7rem !important; font-size: 1.4rem; }
      .downloads p { margin: .6rem 0; }
      .downloads-links { display: flex; flex-wrap: wrap; gap: .65rem; margin-top: 1rem; }
      .downloads-links a { border: 1px solid var(--electric); padding: .55rem .8rem; font-size: .72rem; letter-spacing: .04em; text-decoration: none; }
      .downloads-links a:hover { background: var(--dim-teal); }
      @media (max-width: 700px) { .chain-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .bar-row { grid-template-columns: 1fr 3.4rem; } .bar-row > span { grid-column: 1 / -1; } }
      @media (max-width: 420px) { .study-figure { padding: .9rem; } .chain-grid { grid-template-columns: 1fr; } }
    </style>"""
    description = html.escape(DESCRIPTION, quote=True)
    schema = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": TITLE,
        "alternativeHeadline": SUBTITLE,
        "description": DESCRIPTION,
        "author": {"@type": "Person", "name": "Shane Thomas Strough", "url": "https://shanestrough.com"},
        "publisher": {"@type": "Person", "name": "Shane Thomas Strough"},
        "dateCreated": "2026-10-09",
        "url": f"https://shanestrough.com/{SLUG}",
        "image": "https://shanestrough.com/images/strix-workflow-report.png",
    }
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{TITLE} | Shane Thomas Strough</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="https://shanestrough.com/{SLUG}" />
  <meta property="og:title" content="{TITLE}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="https://shanestrough.com/images/strix-workflow-report.png" />
  <meta property="og:url" content="https://shanestrough.com/{SLUG}" />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&family=Fraunces:ital,wght@0,300;0,400;0,600;1,300&display=swap" rel="stylesheet" />
  <script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script>
{style}
{report_css}
</head>
<body>
  <nav aria-label="Primary navigation">
    <a class="nav-logo" href="index.html">STS</a>
    <ul class="nav-links" id="nav-links">
      <li><a href="about.html">About</a></li>
      <li><a href="insights.html" class="active">Field Notes</a></li>
      <li><a href="Poetry/poetry.html">Poetry</a></li>
      <li><a href="podcast-stop-the-chaos.html">Podcast</a></li>
      <li><a href="index.html#contact">Contact</a></li>
    </ul>
    <button class="nav-hamburger" id="hamburger" aria-label="Toggle menu" aria-controls="nav-links" aria-expanded="false" onclick="toggleMenu()"><span></span><span></span><span></span></button>
  </nav>
  <div class="page-header-grid" aria-hidden="true"></div>
  <header class="page-header reveal">
    <div class="breadcrumb"><a href="index.html">shanestrough.com</a> / <a href="insights.html">Field Notes</a> / The Finding Is Not the Report</div>
    <p class="study-label">Research / AI assurance</p>
    <h1 class="page-title">The Finding Is <span>Not the Report</span></h1>
    <p class="page-subtitle">{SUBTITLE}</p>
    <p class="page-byline">Shane Thomas Strough &middot; An Elevare field study &middot; October 2026</p>
  </header>
  <main class="article-content" id="article">
"""
    # The title, subtitle, and byline live in the page header, not the prose body.
    for _ in range(2):
        body = re.sub(r"^<p><em>.*?</em></p>\n", "", body, count=1)
    downloads = """<aside class="downloads" aria-labelledby="downloads-title">
      <h2 id="downloads-title">Inspect the evidence</h2>
      <p>The public packet includes the exact invented targets, separate instructions, answer key, sanitized run ledger, hashes, and a script that recomputes the counts. Raw agent transcripts remain private.</p>
      <div class="downloads-links">
        <a href="research/strix-workflow-2026/index.html">Companion materials</a>
        <a href="research/strix-workflow-2026/run-ledger.json" download>Run ledger JSON</a>
        <a href="research/strix-workflow-2026.zip" download>Download packet ZIP</a>
      </div>
    </aside>"""
    footer = footer.replace("function toggleMenu() {\n      document.getElementById('nav-links').classList.toggle('open');\n    }", "function toggleMenu() {\n      const menu = document.getElementById('nav-links');\n      const button = document.getElementById('hamburger');\n      const open = menu.classList.toggle('open');\n      button.setAttribute('aria-expanded', String(open));\n    }")
    page = head + body + "\n" + downloads + "\n</main>\n<!-- FOOTER -->" + footer
    OUTPUT.write_text(page)
    print(f"Wrote {OUTPUT} ({len(page):,} characters)")


if __name__ == "__main__":
    build()
