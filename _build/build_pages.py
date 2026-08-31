"""Build the-comprehension-horizon.html + stale-state.html in the site's chrome.

Outputs per page: a repo-ready file (relative image paths) and a preview file
(downscaled data-URI images) for review before anything goes live.
"""
import base64
import io
import re

import markdown
from PIL import Image

SP = "/tmp/claude-1000/-home-s-projects-root-elevare-edge-official/4c35fc3e-4710-4ff5-9c8d-7e2d4700f1e6/scratchpad"
SITE = "/home/s/projects_root/shanestrough-com"
DL = "/home/s/Downloads"
TEMPLATE = open(f"{SITE}/field-notes-blue-origin.html").read()

# ---- carve the chrome out of the template --------------------------------
chrome_top = TEMPLATE.split('<header class="page-header reveal">')[0]
footer = "<!-- FOOTER -->" + TEMPLATE.split("<!-- FOOTER -->")[1]

# the template's font links + full style block live inside its <head> — keep them
template_head = chrome_top.split("</head>")[0]
font_links = "\n".join(re.findall(r'<link[^>]*(?:fonts|preconnect)[^>]*>', template_head))
style_m = re.search(r"<style>.*</style>", template_head, re.S)
site_style = style_m.group(0) if style_m else ""
print(f"carried over: {len(font_links.splitlines())} font links, {len(site_style)//1024}KB site CSS")

EXTRA_CSS = """
  <style>
    .article-content table { width:100%; border-collapse:collapse; margin:2rem 0; font-family:'DM Mono',monospace; font-size:0.85rem; }
    .article-content th { color:var(--warm,#C8A96E); text-align:left; padding:0.6rem 0.8rem; border-bottom:1px solid var(--border,#1E2D3D); font-weight:500; letter-spacing:0.04em; }
    .article-content td { padding:0.55rem 0.8rem; border-bottom:1px solid rgba(30,45,61,0.55); color:var(--white,#F0F4F8); }
    .article-content tr:hover td { background:rgba(0,229,255,0.03); }
    .article-content .tbl-wrap { overflow-x:auto; }
    .article-content code { font-family:'DM Mono',monospace; font-size:0.9em; color:var(--electric,#00E5FF); }
    .article-content .eq { font-family:'DM Mono',monospace; color:var(--electric,#00E5FF); background:rgba(0,229,255,0.05); border-left:2px solid var(--electric,#00E5FF); padding:0.9rem 1.2rem; margin:1.6rem 0; font-size:0.95rem; overflow-x:auto; }
    .article-content h3 { color:var(--warm,#C8A96E); font-size:1.05rem; letter-spacing:0.02em; margin:2.2rem 0 0.8rem; }
    .article-content .fig-note { color:var(--muted,#6B8099); font-size:0.8rem; }
    figure.article-photo { margin: 2.4rem 0; }
    .article-photo img { display: block; }
    .article-photo-caption { line-height: 1.55; padding: 0.7rem 0.2rem 0; letter-spacing: 0.05em; }
    .article-content ul, .article-content ol { margin: 1.2rem 0 1.6rem 1.4rem; }
    .article-content li { margin: 0.55rem 0; line-height: 1.65; }
    .article-content .pull-quote { margin: 2rem 0; }
    .article-content hr { border: 0; border-top: 1px solid var(--border,#1E2D3D); margin: 2.6rem 0; }
    .article-content h2.section-header { margin-top: 3rem; }
    .article-content table td, .article-content table th { font-variant-numeric: tabular-nums; }
    .useful-block { margin: 3rem 0 1rem; padding: 1rem 1.3rem; border: 1px solid var(--border,#1E2D3D); border-radius: 4px; font-family: 'DM Mono', monospace; font-size: 0.85rem; color: var(--muted,#6B8099); }
    .useful-block a { color: var(--electric,#00E5FF); margin-left: 0.6rem; }
    .article-content a { color: var(--electric,#00E5FF); text-decoration: underline; text-underline-offset: 3px; text-decoration-color: rgba(0,229,255,0.35); }
    .article-content a:hover { text-decoration-color: var(--electric,#00E5FF); }
  </style>
"""

def head_block(title, desc, slug, keywords, headline, alt_headline):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="https://shanestrough.com/{slug}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://shanestrough.com/images/comprehension-horizon-envelope.jpg" />
  <meta property="og:url" content="https://shanestrough.com/{slug}" />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://shanestrough.com/images/comprehension-horizon-envelope.jpg" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{headline}",
    "alternativeHeadline": "{alt_headline}",
    "description": "{desc}",
    "author": {{
      "@type": "Person",
      "name": "Shane Thomas Strough",
      "url": "https://shanestrough.com",
      "sameAs": [
        "https://www.linkedin.com/in/shane-thomas-strough/",
        "https://github.com/shane-thomas-strough",
        "https://medium.com/@shane-thomas-strough"
      ]
    }},
    "url": "https://shanestrough.com/{slug}",
    "datePublished": "2026-08-31",
    "publisher": {{ "@type": "Person", "name": "Shane Thomas Strough" }}
  }}
  </script>
"""

# splice our head onto the template chrome (styles + nav come from template)
chrome_after_head = chrome_top.split("</head>")[1]

FIGS = {
    "envelope": dict(src=f"/tmp/claude-1000/-home-s-projects-root-elevare-edge-official/4c35fc3e-4710-4ff5-9c8d-7e2d4700f1e6/scratchpad/envelope-rotated.jpg", site="images/comprehension-horizon-envelope.jpg",
        alt="Original blue-ballpoint sketch on a torn envelope: a long flat line climbing into a near-vertical stroke, with halving interval marks beneath it",
        cap="Figure 1 — The original envelope. Blue ballpoint, torn edge and all: the flat centuries, the climb, and the stroke that leaves the page. Drawn at a kitchen table, August 2026."),
    "model": dict(src=f"{DL}/napkin-lol.png", site="images/comprehension-horizon-model.png",
        alt="Chart comparing the halving-interval series curve C(t)=1/(1-t/400) against a pure exponential, with the finite-time singularity marked at t=400 and a table mapping shrinking intervals to human timescales",
        cap="Figure 2 — The sketch, formalized: the halving series produces a hyperbola with a finite-time blow-up at 400 years — a wall the exponential never has. Right panel: what each shrinking interval means at human scale."),
    "clock": dict(src=f"{DL}/napkin2-lol.png", site="images/comprehension-horizon-clock.png",
        alt="The halving series pinned to history starting 1660, with real events plotted — Principia, steam, telegraph, electric light, transistor, ARPANET, AlexNet, Transformer, ChatGPT — and the model horizon marked at 2060, with NOW August 2026 indicated",
        cap="Figure 3 — The clock pinned to 1660: predicted windows against what actually clustered in them. August 2026 sits 91.7% of the way to the model's horizon. Treat the calendar as illustration — the argument doesn't need it."),
    "ensemble": dict(src=f"{DL}/denominator-ensemble.png", site="images/stale-state-ensemble.png",
        alt="Bar chart of generation exposure G for FDA reviews and grid interconnection queues in selected years, computed on three different frontier-clock definitions, with the G=1 line marked — queue bars far above 1, FDA bars far below",
        cap="Figure 4 — The denominator ensemble: the same two institutional loops scored on three materially different definitions of a frontier generation. The queue stays multi-generational, the FDA review sub-generational, on every clock."),
    "plane": dict(src=f"{DL}/v3.1-generation-exposure.png", site="images/stale-state-plane.png",
        alt="Two-panel figure: generation exposure per loop over time, and the R versus average-shear state plane with FDA plotted in the buffer-shrinking quadrant and the interconnection queue in the divergent-shear quadrant",
        cap="Generation exposure and the R × σ̄ state plane: one instrument panel, two very different machines — FDA losing margin inside the safe half-plane, the queue compounding mismatch in the unsafe one."),
    "shear": dict(src=f"{DL}/temporal-sheer-2.png", site="images/stale-state-shear.png",
        alt="Chart of institutional loop durations against shrinking frontier generation lengths over 2015-2025, illustrating positive temporal shear on both measured systems",
        cap="Aligned-window shear, 2015–2025: the queue lengthens while the frontier accelerates — mismatch compounding from both ends. The FDA loop holds its speed against the same accelerating clock."),
}

def figure_html(key, preview):
    f = FIGS[key]
    if preview:
        img = Image.open(f["src"])
        w = min(img.width, 1400)
        img = img.convert("RGB") if f["src"].endswith(".jpg") else img
        r = w / img.width
        img = img.resize((w, int(img.height * r)), Image.LANCZOS)
        buf = io.BytesIO()
        if f["src"].endswith(".jpg"):
            img.save(buf, "JPEG", quality=78)
            src = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        else:
            img.save(buf, "PNG", optimize=True)
            src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    else:
        src = f["site"]
    return (f'<figure class="article-photo"><img src="{src}" alt="{f["alt"]}" loading="lazy" '
            f'style="width:100%;height:auto;border:1px solid var(--border,#1E2D3D);border-radius:4px;" />'
            f'<figcaption class="article-photo-caption">{f["cap"]}</figcaption></figure>')

def md_to_body(md_text):
    body = markdown.markdown(md_text, extensions=["tables"])
    body = body.replace("<blockquote>", '<div class="pull-quote">').replace("</blockquote>", "</div>")
    body = re.sub(r"<h2>(.*?)</h2>", r'<h2 class="section-header">\1</h2>', body)
    body = re.sub(r"<table>", '<div class="tbl-wrap"><table>', body)
    body = re.sub(r"</table>", "</table></div>", body)
    return body

def build(md_path, page_header, head, figs_by_token, figs_by_anchor, out_slug):
    md = open(md_path).read()
    md = re.sub(r"^# .*\n", "", md)                      # h1 -> page-title
    md = re.sub(r"^\*An engineering theory.*\n", "", md, flags=re.M)
    md = re.sub(r"^\*The measurement program behind.*\n", "", md, flags=re.M)
    md = md.replace("./Stale-State.md", "stale-state.html").replace("./The-Comprehension-Horizon.md", "the-comprehension-horizon.html")
    for token in figs_by_token:
        md = re.sub(r"\[FIGURE " + token + r"[^\]]*\]", f"@@FIG:{figs_by_token[token]}@@", md)
    body = md_to_body(md)
    for anchor, key in figs_by_anchor:
        idx = body.find(anchor)
        if idx == -1:
            print(f"ANCHOR MISS ({out_slug}): {anchor[:50]}")
            continue
        end = body.find("</p>", idx)
        end = body.find(">", end) + 1
        body = body[:end] + f"@@FIG:{key}@@" + body[end:]
    for preview, suffix in ((True, "-preview"), (False, "")):
        b = re.sub(r"@@FIG:(\w+)@@", lambda m: figure_html(m.group(1), preview), body)
        page = (head + font_links + "\n" + site_style + EXTRA_CSS + chrome_after_head
                + '<header class="page-header reveal">' + page_header + "</header>\n"
                + '<main class="article-content">\n' + b + "\n</main>\n\n" + footer)
        out = f"{SP}/{out_slug}{suffix}.html"
        open(out, "w").write(page)
        print(f"built {out} ({len(page)//1024}KB)")

# ---------------- Essay ----------------
build(
    f"{SP}/horizon-final.md",
    page_header="""
    <div class="breadcrumb"><a href="index.html">shanestrough.com</a> / <a href="insights.html">Field Notes</a> / The Comprehension Horizon</div>
    <h1 class="page-title">The Comprehension<br><span>Horizon</span></h1>
    <p class="page-subtitle">An Engineering Theory of Technological Time-Compression</p>
    <p class="page-byline">Shane Thomas Strough &middot; Field Note &middot; August 2026 &middot; companion report: <a href="stale-state.html">Stale State</a></p>
    """,
    head=head_block(
        "The Comprehension Horizon — Shane Thomas Strough",
        "The time between major technological shifts keeps halving — and the mechanisms society uses to understand technology can't keep pace. An engineering theory of time compression, from a sketch on a torn envelope to a measured claim.",
        "the-comprehension-horizon.html",
        "Shane Thomas Strough, Comprehension Horizon, technological singularity, time compression, AI acceleration, architecture half-life, consensus lag, finite-time singularity, sovereign AI, technology strategy",
        "The Comprehension Horizon",
        "An Engineering Theory of Technological Time-Compression"),
    figs_by_token={"1": "envelope", "2": "model", "3": "clock", "4": "ensemble"},
    figs_by_anchor=[],
    out_slug="the-comprehension-horizon",
)

# ---------------- Stale State ----------------
build(
    f"{SP}/stale-state-final.md",
    page_header="""
    <div class="breadcrumb"><a href="index.html">shanestrough.com</a> / <a href="insights.html">Field Notes</a> / Stale State</div>
    <h1 class="page-title">Stale <span>State</span></h1>
    <p class="page-subtitle">A Commissioning Test Report for Institutional Clock-Speed</p>
    <p class="page-byline">Shane Thomas Strough &middot; Measurement Program v4 &middot; August 2026 &middot; the essay: <a href="the-comprehension-horizon.html">The Comprehension Horizon</a></p>
    """,
    head=head_block(
        "Stale State — the measurement program behind The Comprehension Horizon",
        "Two institutional loops, three frontier clocks, numbers you can rerun: generation exposure, temporal shear, and the state plane — a commissioning test report measuring whether institutions keep pace with AI's cadence.",
        "stale-state.html",
        "Shane Thomas Strough, Stale State, generation exposure, temporal shear, FDA 510k AI, interconnection queue, LBNL Queued Up, Epoch AI compute trend, institutional lag, measurement",
        "Stale State: Measuring Institutional Clock-Speed Against Frontier AI Cadence",
        "Two loops, three clocks, numbers you can rerun"),
    figs_by_token={},
    figs_by_anchor=[
        ("mismatch compounds on both ends", "shear"),
        ("One instrument panel, two very different machines", "plane"),
        ("The systems are not perched on G = 1", "ensemble"),
    ],
    out_slug="stale-state",
)
print("done")
