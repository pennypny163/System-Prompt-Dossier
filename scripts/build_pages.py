#!/usr/bin/env python3
"""Build source and standalone dossier pages from shared metadata."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE_PATH = ROOT / "src" / "styles.css"
READER_PATH = ROOT / "src" / "reader.js"
PAGES_PATH = ROOT / "data" / "pages.json"
TEMPLATE_PATH = ROOT / "templates" / "model.html"
DIST_DIR = ROOT / "dist"


STYLE_LINK = '<link rel="stylesheet" href="src/styles.css">'
READER_SCRIPT = '<script src="src/reader.js" defer></script>'
EMPTY_DATA_TAG = ""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def script_json(data: object) -> str:
    """Return JSON that is safe to embed inside a script tag."""
    text = json.dumps(data, ensure_ascii=False, indent=2)
    return text.replace("</", "<\\/")


def page_meta() -> list[dict[str, str]]:
    pages = json.loads(read_text(PAGES_PATH)).get("pages", [])
    if not pages:
        raise RuntimeError("No pages found in data/pages.json")
    return pages


def standalone_reader(reader_js: str) -> str:
    fetch_loader = """  function loadVersions(){
    return fetch(dataPath).then(function(response){
      if(!response.ok){ throw new Error('Unable to load ' + modelName + ' data: ' + response.status); }
      return response.json();
    });
  }"""
    embedded_loader = """  function loadVersions(){
    var data = document.getElementById('vdata');
    if(!data){ return Promise.reject(new Error('Missing embedded ' + modelName + ' data')); }
    return Promise.resolve(JSON.parse(data.textContent));
  }"""

    if fetch_loader not in reader_js:
        raise RuntimeError("Unable to find the fetch-based loadVersions() block")

    return reader_js.replace(fetch_loader, embedded_loader)


def render_page(page: dict[str, str], style_tag: str, data_tag: str, reader_tag: str) -> str:
    values = {
        "nav_prefix": "",
        **page,
        "style_tag": style_tag,
        "data_tag": data_tag,
        "reader_tag": reader_tag,
    }
    html = read_text(TEMPLATE_PATH)
    for key, value in values.items():
        html = html.replace("{{" + key + "}}", str(value))
    missing = [key for key in values if "{{" + key + "}}" in html]
    if missing:
        raise RuntimeError(f"Unresolved template placeholders: {', '.join(missing)}")
    return html


def build_source_page(page: dict[str, str]) -> None:
    output_path = ROOT / page["source_page"]
    html = render_page(page, STYLE_LINK, EMPTY_DATA_TAG, READER_SCRIPT)
    output_path.write_text(html, encoding="utf-8")
    print(f"Built {output_path.relative_to(ROOT)}")


def build_dist_page(page: dict[str, str], css: str, reader_js: str) -> None:
    data_path = ROOT / page["data_path"]
    data = json.loads(read_text(data_path))

    page_for_dist = {**page, "nav_prefix": "../"}
    html = render_page(
        page_for_dist,
        f"<style>\n{css}\n</style>",
        '<script id="vdata" type="application/json">\n'
        f"{script_json(data)}\n"
        "</script>",
        "<script>\n"
        f"{reader_js}\n"
        "</script>",
    )

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DIST_DIR / page["dist_page"]
    output_path.write_text(html, encoding="utf-8")
    print(f"Built {output_path.relative_to(ROOT)} ({len(data)} versions)")


def build() -> None:
    css = read_text(STYLE_PATH).rstrip()
    reader_js = standalone_reader(read_text(READER_PATH).rstrip())
    for page in page_meta():
        build_source_page(page)
        build_dist_page(page, css, reader_js)


if __name__ == "__main__":
    build()
