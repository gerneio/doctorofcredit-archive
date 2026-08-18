#!/usr/bin/env python3
"""Fetch Doctor of Credit pages and save selected HTML."""

from pathlib import Path
from urllib.request import Request, urlopen

from lxml import html

BASE_URL = "https://www.doctorofcredit.com"
ARCHIVE_DIR = Path(__file__).resolve().parent.parent / "archive"
USER_AGENT = "doctorofcredit-archive/0.1 (+https://github.com/)"
TIMEOUT_SEC = 60

# page path -> CSS/tag selector (XPath: //{selector})
PAGES = {
    "/high-interest-savings-to-get/": "main",
}


def path_parts(page_path: str) -> list[str]:
    parts = [p for p in page_path.split("/") if p]
    if not parts:
        raise ValueError(f"cannot compute path from {page_path!r}")
    return parts


def page_url(page_path: str) -> str:
    return f"{BASE_URL.rstrip('/')}/{'/'.join(path_parts(page_path))}/"


def archive_path(page_path: str) -> Path:
    # /high-interest-savings-to-get/ -> archive/high-interest-savings-to-get.html
    # /path/content/                 -> archive/path/content.html
    parts = path_parts(page_path)
    return ARCHIVE_DIR.joinpath(*parts[:-1], f"{parts[-1]}.html")


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
    with urlopen(req, timeout=TIMEOUT_SEC) as resp:
        return resp.read()


def extract(page_bytes: bytes, selector: str, url: str) -> str:
    doc = html.fromstring(page_bytes)
    # XPath avoids the optional cssselect dependency
    matches = doc.xpath(f"//{selector}")
    if not matches:
        raise RuntimeError(f"selector {selector!r} matched nothing on {url}")

    root = matches[0]
    comments_nodes = root.xpath('.//*[@class="meta-item comments"]')
    if comments_nodes:
        comments_nodes[0].clear()

    return html.tostring(root, encoding="unicode", pretty_print=True)


def archive_page(page_path: str, selector: str) -> None:
    url = page_url(page_path)
    out = archive_path(page_path)
    snippet = extract(fetch(url), selector, url)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(snippet, encoding="utf-8", newline="\n")
    print(f"wrote {out} ({len(snippet)} chars)")


def main() -> None:
    for page_path, selector in PAGES.items():
        archive_page(page_path, selector)


if __name__ == "__main__":
    main()
