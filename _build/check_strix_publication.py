"""Static acceptance checks for the staged Strix article and companion packet."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

sys.dont_write_bytecode = True
from pack_strix_packet import PUBLIC_FILES


SITE = Path(__file__).resolve().parents[1]
ARTICLE = SITE / "the-finding-is-not-the-report.html"
PACKET = SITE / "research/strix-workflow-2026"
ZIP = SITE / "research/strix-workflow-2026.zip"


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.headings: list[str] = []
        self.images: list[str] = []
        self._h1 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "img" and values.get("src"):
            self.images.append(values["src"] or "")
        if tag == "h1":
            self._h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self._h1 = False

    def handle_data(self, data: str) -> None:
        if self._h1:
            self.headings.append(data)


def check_links(path: Path) -> None:
    parser = Links()
    parser.feed(path.read_text())
    for link in parser.links + parser.images:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc or link.startswith("#") or link.startswith("mailto:"):
            continue
        relative = unquote(parsed.path)
        target = SITE / relative.lstrip("/") if relative.startswith("/") else path.parent / relative
        assert target.exists(), f"Broken link in {path.name}: {link}"
    assert parser.headings, f"No h1 in {path}"
    print(f"Checked {path.relative_to(SITE)}: {len(parser.links)} links, {len(parser.images)} images")


def main() -> None:
    check_links(ARTICLE)
    check_links(PACKET / "index.html")
    assert 'href="the-finding-is-not-the-report.html"' in (SITE / "insights.html").read_text()
    ET.parse(SITE / "sitemap.xml")
    for stem in ("README", "CLAIM-MAP", "TRACE-EXCERPT"):
        assert (PACKET / f"{stem}.md").read_bytes() == (PACKET / f"{stem}.txt").read_bytes(), f"Plain-text mirror stale: {stem}"
    assert (SITE / "images/strix-workflow-report.png").exists()
    assert ZIP.exists()
    with ZipFile(ZIP) as archive:
        names = set(archive.namelist())
        expected = set(PUBLIC_FILES)
        assert names == expected, f"ZIP contents differ: {names ^ expected}"
        for name in names:
            assert archive.read(name) == (PACKET / name).read_bytes(), f"ZIP stale: {name}"
    page = ARTICLE.read_text()
    assert page.count("<h1") == 1
    assert "<figcaption" in page and "10 / 12" in page and "4 / 12" in page
    assert "datePublished" not in page, "Do not claim a publication date before deployment"
    assert not re.search(r"/home/|\.secrets|\.ssh", page)
    ledger = json.loads((PACKET / "run-ledger.json").read_text())
    assert len(ledger["runs"]) == 25
    print("Sitemap, page structure, ZIP bytes, and publication boundary: verified")


if __name__ == "__main__":
    main()
