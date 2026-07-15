#!/usr/bin/env python3
"""Validate dossier data, source annotations, links, and generated pages."""

from __future__ import annotations

import html
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
SOURCE_ROOT = ROOT / ".sources" / "system_prompts_leaks"
BAD_SOURCE_TOKENS = ("todo", "待核对", "unknown", "unverified", "confirm exact", "pin upstream")
REQUIRED_PAGE_FIELDS = (
    "slug",
    "source_page",
    "dist_page",
    "title",
    "model",
    "model_name",
    "data_path",
    "face",
    "hero_title_html",
    "persona_tag",
    "subtitle_html",
    "content_html",
)
REQUIRED_SOURCE_FIELDS = ("source_repo", "source_path", "source_commit", "license")


sys.path.insert(0, str(SCRIPTS_DIR))
import build_pages  # noqa: E402


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.links.append((key, html.unescape(value)))


class QuoteCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.quotes: list[tuple[int, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "div":
            return
        attr_map = {key: value for key, value in attrs}
        classes = set((attr_map.get("class") or "").split())
        if "quote" in classes:
            self.quotes.append((self.getpos()[0], attr_map.get("data-source-label")))


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        return None


def is_bad_source_value(value: object) -> bool:
    text = str(value or "").strip()
    return not text or any(token in text.lower() for token in BAD_SOURCE_TOKENS)


def validate_data_file(path: Path, errors: list[str]) -> None:
    data = load_json(path, errors)
    if data is None:
        return
    if not isinstance(data, list):
        errors.append(f"{path.relative_to(ROOT)}: expected top-level array")
        return

    for index, item in enumerate(data):
        label = f"{path.relative_to(ROOT)}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: expected object")
            continue

        prompt = item.get("prompt")
        if not isinstance(prompt, str) or not prompt:
            errors.append(f"{label}: prompt is empty or missing")
            continue

        actual_words = len(prompt.split())
        actual_lines = len(prompt.splitlines())
        if item.get("words") != actual_words:
            errors.append(f"{label}: words={item.get('words')} but actual={actual_words}")
        if item.get("lines") != actual_lines:
            errors.append(f"{label}: lines={item.get('lines')} but actual={actual_lines}")

        source = item.get("source")
        if not isinstance(source, dict):
            errors.append(f"{label}: source is missing")
            continue

        for field in REQUIRED_SOURCE_FIELDS:
            if is_bad_source_value(source.get(field)):
                errors.append(f"{label}: source.{field} is empty or unresolved")

        source_path = source.get("source_path")
        if isinstance(source_path, str) and SOURCE_ROOT.exists():
            if not (SOURCE_ROOT / source_path).is_file():
                errors.append(f"{label}: source_path does not exist in .sources ({source_path})")

        quoted_lines = source.get("quoted_lines")
        if not isinstance(quoted_lines, list) or not quoted_lines:
            errors.append(f"{label}: source.quoted_lines is empty or missing")
            continue

        for q_index, quote in enumerate(quoted_lines):
            q_label = f"{label}.source.quoted_lines[{q_index}]"
            if not isinstance(quote, dict):
                errors.append(f"{q_label}: expected object")
                continue
            if not str(quote.get("label", "")).strip():
                errors.append(f"{q_label}: label is empty")
            start = quote.get("start")
            end = quote.get("end")
            if not isinstance(start, int) or not isinstance(end, int):
                errors.append(f"{q_label}: start/end must be integers")
                continue
            if start < 1 or end < start or end > actual_lines:
                errors.append(f"{q_label}: line range {start}-{end} is outside 1-{actual_lines}")


def validate_pages(errors: list[str]) -> list[dict[str, str]]:
    data = load_json(ROOT / "data" / "pages.json", errors)
    if data is None:
        return []
    pages = data.get("pages") if isinstance(data, dict) else None
    if not isinstance(pages, list) or not pages:
        errors.append("data/pages.json: pages must be a non-empty array")
        return []

    seen_slugs: set[str] = set()
    valid_pages: list[dict[str, str]] = []
    for index, page in enumerate(pages):
        label = f"data/pages.json.pages[{index}]"
        if not isinstance(page, dict):
            errors.append(f"{label}: expected object")
            continue
        for field in REQUIRED_PAGE_FIELDS:
            if not str(page.get(field, "")).strip():
                errors.append(f"{label}: {field} is empty or missing")
        slug = str(page.get("slug", ""))
        if slug in seen_slugs:
            errors.append(f"{label}: duplicate slug {slug}")
        seen_slugs.add(slug)

        data_path = ROOT / str(page.get("data_path", ""))
        if not data_path.is_file():
            errors.append(f"{label}: data_path does not exist ({page.get('data_path')})")
        valid_pages.append(page)  # type: ignore[arg-type]
    return valid_pages


def should_skip_link(value: str) -> bool:
    value = value.strip()
    if not value or value.startswith("#") or value.startswith("{{"):
        return True
    parsed = urlsplit(value)
    return parsed.scheme in {"http", "https", "mailto", "tel", "data", "javascript", "about"} or bool(parsed.netloc)


def validate_links(path: Path, errors: list[str]) -> None:
    parser = LinkCollector()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path.relative_to(ROOT)}: unable to parse HTML links ({exc})")
        return

    for attr, raw_value in parser.links:
        if should_skip_link(raw_value):
            continue
        parsed = urlsplit(raw_value)
        target_value = unquote(parsed.path)
        if not target_value:
            continue
        target = (path.parent / target_value).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: {attr} points outside repo ({raw_value})")
            continue
        if not target.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing local {attr} target ({raw_value})")


def source_labels_for_page(page: dict[str, str], errors: list[str]) -> set[str]:
    data = load_json(ROOT / page["data_path"], errors)
    if not isinstance(data, list):
        return set()
    labels: set[str] = set()
    for item in data:
        if not isinstance(item, dict):
            continue
        source = item.get("source")
        if not isinstance(source, dict):
            continue
        quoted_lines = source.get("quoted_lines")
        if not isinstance(quoted_lines, list):
            continue
        for quote in quoted_lines:
            if isinstance(quote, dict) and quote.get("label"):
                labels.add(str(quote["label"]))
    return labels


def validate_quote_bindings(path: Path, page: dict[str, str], errors: list[str]) -> None:
    parser = QuoteCollector()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path.relative_to(ROOT)}: unable to parse quote bindings ({exc})")
        return

    if not parser.quotes:
        errors.append(f"{path.relative_to(ROOT)}: no .quote blocks found")
        return

    labels = source_labels_for_page(page, errors)
    for line, label in parser.quotes:
        location = f"{path.relative_to(ROOT)}:{line}"
        if not label or not label.strip():
            errors.append(f"{location}: .quote is missing data-source-label")
            continue
        if label not in labels:
            errors.append(f"{location}: data-source-label '{label}' is not present in {page['data_path']} quoted_lines")


def validate_generated_pages(pages: list[dict[str, str]], errors: list[str]) -> None:
    css = build_pages.read_text(build_pages.STYLE_PATH).rstrip()
    reader_js = build_pages.standalone_reader(build_pages.read_text(build_pages.READER_PATH).rstrip())

    for page in pages:
        source_path = ROOT / page["source_page"]
        expected_source = build_pages.render_page(
            page,
            build_pages.STYLE_LINK,
            build_pages.EMPTY_DATA_TAG,
            build_pages.READER_SCRIPT,
        )
        if not source_path.is_file():
            errors.append(f"{page['source_page']}: generated source page is missing")
        elif source_path.read_text(encoding="utf-8") != expected_source:
            errors.append(f"{page['source_page']}: generated source page is stale; run python3 scripts/build.py")

        data = load_json(ROOT / page["data_path"], errors)
        if data is None:
            continue
        dist_page = {**page, "nav_prefix": "../"}
        expected_dist = build_pages.render_page(
            dist_page,
            f"<style>\n{css}\n</style>",
            '<script id="vdata" type="application/json">\n'
            f"{build_pages.script_json(data)}\n"
            "</script>",
            "<script>\n"
            f"{reader_js}\n"
            "</script>",
        )
        dist_path = ROOT / "dist" / page["dist_page"]
        if not dist_path.is_file():
            errors.append(f"dist/{page['dist_page']}: generated dist page is missing")
        elif dist_path.read_text(encoding="utf-8") != expected_dist:
            errors.append(f"dist/{page['dist_page']}: generated dist page is stale; run python3 scripts/build.py")

    sources_path = ROOT / "sources.html"
    expected_sources = build_pages.render_sources_page()
    if not sources_path.is_file():
        errors.append("sources.html: generated sources page is missing")
    elif sources_path.read_text(encoding="utf-8") != expected_sources:
        errors.append("sources.html: generated sources page is stale; run python3 scripts/build.py")


def main() -> int:
    errors: list[str] = []
    pages = validate_pages(errors)

    for data_path in sorted((ROOT / "data").glob("*.json")):
        if data_path.name != "pages.json":
            validate_data_file(data_path, errors)

    html_paths = [ROOT / "index.html", ROOT / "methodology.html", ROOT / "sources.html"]
    html_paths.extend(ROOT / page["source_page"] for page in pages)
    html_paths.extend(ROOT / "dist" / page["dist_page"] for page in pages)
    for html_path in html_paths:
        if html_path.is_file():
            validate_links(html_path, errors)
        else:
            errors.append(f"{html_path.relative_to(ROOT)}: HTML file is missing")

    for page in pages:
        source_path = ROOT / page["source_page"]
        dist_path = ROOT / "dist" / page["dist_page"]
        if source_path.is_file():
            validate_quote_bindings(source_path, page, errors)
        if dist_path.is_file():
            validate_quote_bindings(dist_path, page, errors)

    validate_generated_pages(pages, errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
