#!/usr/bin/env python3
"""Build source and standalone dossier pages from shared metadata."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE_PATH = ROOT / "src" / "styles.css"
READER_PATH = ROOT / "src" / "reader.js"
PAGES_PATH = ROOT / "data" / "pages.json"
TEMPLATE_PATH = ROOT / "templates" / "model.html"
SOURCE_DOC_PATH = ROOT / "docs" / "source-annotations.md"
SOURCES_OUTPUT_PATH = ROOT / "sources.html"
DIST_DIR = ROOT / "dist"


STYLE_LINK = '<link rel="stylesheet" href="src/styles.css">'
READER_SCRIPT = '<script src="src/reader.js" defer></script>'
EMPTY_DATA_TAG = ""


SOURCES_NAV = """  <nav class="global-nav" aria-label="页面导航">
    <a class="nav-link" href="index.html">INDEX</a>
    <a class="nav-link" href="methodology.html">方法论</a>
    <div class="nav-group">
      <button class="nav-trigger" type="button" aria-haspopup="true">模型档案</button>
      <div class="nav-menu" role="menu">
        <div class="nav-menu-section"><p>通用助手</p><a role="menuitem" href="claude-sample.html">Claude</a><a role="menuitem" href="gpt.html">GPT</a><a role="menuitem" href="gemini.html">Gemini</a></div>
        <div class="nav-menu-section"><p>开发 Agent</p><a role="menuitem" href="cursor.html">Cursor</a><a role="menuitem" href="devin.html">Devin</a><a role="menuitem" href="copilot.html">Copilot</a></div>
        <div class="nav-menu-section"><p>实时 / 平台</p><a role="menuitem" href="grok.html">Grok</a></div>
      </div>
    </div>
    <div class="nav-group">
      <button class="nav-trigger" type="button" aria-haspopup="true">人格对比</button>
      <div class="nav-menu nav-menu-compact" role="menu">
        <div class="nav-menu-section"><p>两种讲法</p><a role="menuitem" href="persona-student.html">大学生 · 科普版</a><a role="menuitem" href="persona-ka.html">KA 高层 · 授课版</a></div>
      </div>
    </div>
    <a class="nav-link" href="sources.html">来源规范</a>
  </nav>"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def script_json(data: object) -> str:
    """Return JSON that is safe to embed inside a script tag."""
    text = json.dumps(data, ensure_ascii=False, indent=2)
    return text.replace("</", "<\\/")


def inline_markdown(text: str) -> str:
    html = escape(text)
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    html = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", html)
    return html


def render_table(lines: list[str]) -> str:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(set(cell) <= {"-"} for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    head = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in rows[0])
    body = []
    for row in rows[1:]:
        body.append("<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>")
    return "<table><thead><tr>" + head + "</tr></thead><tbody>" + "".join(body) + "</tbody></table>"


def markdown_to_html(markdown: str) -> str:
    html: list[str] = []
    lines = markdown.splitlines()
    i = 0
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            html.append("</ul>")
            in_list = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                html.append(
                    '<pre><code class="language-'
                    + escape(code_lang)
                    + '">'
                    + escape("\n".join(code_lines))
                    + "</code></pre>"
                )
                in_code = False
                code_lines = []
                code_lang = ""
            else:
                close_list()
                in_code = True
                code_lang = stripped[3:].strip()
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            close_list()
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            close_list()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            html.append(render_table(table_lines))
            continue

        if stripped.startswith("## "):
            close_list()
            html.append("<h2>" + inline_markdown(stripped[3:]) + "</h2>")
            i += 1
            continue

        if stripped.startswith("# "):
            close_list()
            html.append("<h1>" + inline_markdown(stripped[2:]) + "</h1>")
            i += 1
            continue

        if stripped.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append("<li>" + inline_markdown(stripped[2:]) + "</li>")
            i += 1
            continue

        close_list()
        html.append("<p>" + inline_markdown(stripped) + "</p>")
        i += 1

    close_list()
    if in_code:
        html.append("<pre><code>" + escape("\n".join(code_lines)) + "</code></pre>")
    return "\n".join(html)


def render_sources_page(css_link: str = STYLE_LINK) -> str:
    doc_html = markdown_to_html(read_text(SOURCE_DOC_PATH))
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>来源标注规范</title>
{css_link}
</head>
<body>
<div class="deck source-page">
{SOURCES_NAV}
  <div class="hero">
    <div class="avatar"><span class="face">SRC</span><span class="logo">DOSSIER</span></div>
    <div class="htext">
      <h1><span class="en">Sources</span> 标注规范</h1>
      <span class="persona-tag">可追溯 · 可复现 · 可审计</span>
    </div>
    <div class="arrows">&raquo;&raquo;&raquo;</div>
  </div>
  <p class="subtitle">站内版来源规范，内容由 <code>docs/source-annotations.md</code> 生成。模型档案页的摘录、来源字段、行号和版本 diff 都按这套规则校验。</p>
  <article class="source-doc">
{doc_html}
  </article>
</div>
</body>
</html>
"""


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


def build_sources_page() -> None:
    SOURCES_OUTPUT_PATH.write_text(render_sources_page(), encoding="utf-8")
    print(f"Built {SOURCES_OUTPUT_PATH.relative_to(ROOT)}")


def build() -> None:
    css = read_text(STYLE_PATH).rstrip()
    reader_js = standalone_reader(read_text(READER_PATH).rstrip())
    build_sources_page()
    for page in page_meta():
        build_source_page(page)
        build_dist_page(page, css, reader_js)


if __name__ == "__main__":
    build()
