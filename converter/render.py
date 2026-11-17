"""Markdown -> HTML dönüşümü ve bölüm sarma (docx/pdf/xlsx ortak kullanır)."""

from html import escape

from markdown_it import MarkdownIt

_md = MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")


def markdown_to_html(text: str) -> str:
    return _md.render(text)


def wrap_sections(merged, render_fn=markdown_to_html) -> str:
    """Her dosyayı ayrı <section> içine alır; yazıcılar arasında sayfa sonu ekler."""
    parts = []
    for sec in merged.sections:
        safe_name = escape(sec.name, quote=True)
        parts.append(
            f'<section data-source="{safe_name}">{render_fn(sec.text)}</section>'
        )
    return "\n".join(parts)
