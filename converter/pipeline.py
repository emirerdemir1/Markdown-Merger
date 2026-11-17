"""Tüm adımları birleştiren ana dönüştürme fonksiyonu."""

from pathlib import Path

from .merge import merge_files
from .render import wrap_sections
from .to_docx import html_to_docx
from .to_pdf import html_to_pdf
from .to_xlsx import html_to_xlsx

FORMATLAR = {"docx": "Word", "pdf": "PDF", "xlsx": "Excel"}


def convert_files(
    files: list[str | Path],
    fmt: str,
    output_path: str | Path,
    *,
    title: str | None = None,
) -> Path:
    """Markdown dosyalarını birleştirir ve istediğin formatta kaydeder.

    fmt: 'docx' (Word), 'pdf' veya 'xlsx' (Excel)
    """
    fmt = fmt.lower().lstrip(".")
    if fmt not in FORMATLAR:
        raise ValueError(f"Bilinmeyen format: {fmt}. Geçerli: {', '.join(FORMATLAR)}")

    merged = merge_files(files)
    html = wrap_sections(merged)

    if fmt == "docx":
        return html_to_docx(html, output_path, title=title)
    if fmt == "pdf":
        return html_to_pdf(html, output_path)
    return html_to_xlsx(html, output_path)
