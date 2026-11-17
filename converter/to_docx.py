"""HTML -> Word (.docx). Zengin içeriği korur: başlık, liste, tablo, kalın/italik, link."""

from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from docx import Document
from docx.shared import Pt, RGBColor


def _add_inline(paragraph, node, *, bold=False, italic=False, code=False, link=None):
    """Bir HTML düğümünün inline çocuklarını Word run'larına çevirir."""
    for child in node.children:
        if isinstance(child, NavigableString):
            text = str(child)
            if not text:
                continue
            run = paragraph.add_run(text)
            run.bold = bold
            run.italic = italic
            if code:
                run.font.name = "Courier New"
                run.font.size = Pt(10)
            if link:
                run.font.color.rgb = RGBColor(0x05, 0x63, 0xC1)
                run.font.underline = True
            continue

        if not isinstance(child, Tag):
            continue

        name = child.name.lower()
        if name in ("strong", "b"):
            _add_inline(paragraph, child, bold=True, italic=italic, code=code, link=link)
        elif name in ("em", "i"):
            _add_inline(paragraph, child, bold=bold, italic=True, code=code, link=link)
        elif name == "code":
            _add_inline(paragraph, child, bold=bold, italic=italic, code=True, link=link)
        elif name in ("s", "del", "strike"):
            _add_inline(paragraph, child, bold=bold, italic=italic, code=code, link=link)
        elif name == "a":
            _add_inline(
                paragraph, child, bold=bold, italic=italic, code=code,
                link=child.get("href"),
            )
        elif name == "br":
            paragraph.add_run().add_break()
        elif name == "img":
            paragraph.add_run(f"[Görsel: {child.get('alt', 'isimsiz')}]")
        else:
            _add_inline(paragraph, child, bold=bold, italic=italic, code=code, link=link)


def _add_list(tag: Tag, doc: Document, style: str):
    for li in tag.find_all("li", recursive=False):
        paragraph = doc.add_paragraph(style=style)
        for child in li.children:
            if isinstance(child, Tag) and child.name in ("ul", "ol"):
                _add_list(child, doc, "List Bullet" if child.name == "ul" else "List Number")
            else:
                _add_inline(paragraph, child) if isinstance(child, Tag) else paragraph.add_run(str(child))


def _add_table(tag: Tag, doc: Document):
    rows = tag.find_all("tr")
    if not rows:
        return
    col_count = max(len(r.find_all(["th", "td"])) for r in rows)
    table = doc.add_table(rows=len(rows), cols=col_count)
    table.style = "Table Grid"

    for r_i, tr in enumerate(rows):
        cells = tr.find_all(["th", "td"])
        for c_i, cell in enumerate(cells):
            word_cell = table.cell(r_i, c_i)
            word_cell.text = ""
            paragraph = word_cell.paragraphs[0]
            _add_inline(paragraph, cell)
            if cell.name == "th":
                for run in paragraph.runs:
                    run.bold = True


def _walk(container, doc: Document, *, is_first_section: bool = True):
    for node in container.children:
        if not isinstance(node, Tag):
            continue
        name = node.name.lower()

        if name == "section":
            if not is_first_section:
                doc.add_page_break()
            _walk(node, doc, is_first_section=False)
        elif name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = min(int(name[1]), 6)
            doc.add_heading(node.get_text(" ", strip=True), level=level)
        elif name == "p":
            _add_inline(doc.add_paragraph(), node)
        elif name == "ul":
            _add_list(node, doc, "List Bullet")
        elif name == "ol":
            _add_list(node, doc, "List Number")
        elif name == "table":
            _add_table(node, doc)
        elif name in ("pre", "code"):
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(node.get_text())
            run.font.name = "Courier New"
            run.font.size = Pt(10)
        elif name == "blockquote":
            paragraph = doc.add_paragraph(style="Intense Quote")
            _add_inline(paragraph, node)
        elif name == "hr":
            doc.add_paragraph()
        elif name == "img":
            doc.add_paragraph(f"[Görsel: {node.get('alt', 'isimsiz')}]")
        else:
            _walk(node, doc, is_first_section=is_first_section)


def html_to_docx(html: str, output_path: str | Path, title: str | None = None) -> Path:
    soup = BeautifulSoup(html, "html.parser")
    doc = Document()
    if title:
        doc.add_heading(title, level=0)
    _walk(soup.body or soup, doc, is_first_section=True)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    return out
