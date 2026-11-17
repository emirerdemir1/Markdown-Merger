"""HTML -> Excel (.xlsx). Her markdown tablosu ayrı sayfaya, metin de 'Metin' sayfasına."""

from pathlib import Path

from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


def _autosize(ws):
    for column_cells in ws.columns:
        length = max((len(str(c.value or "")) for c in column_cells), default=0)
        ws.column_dimensions[get_column_letter(column_cells[0].column)].width = min(
            max(length + 2, 10), 60
        )


def html_to_xlsx(html: str, output_path: str | Path, include_text: bool = True) -> Path:
    soup = BeautifulSoup(html, "html.parser")
    wb = Workbook()
    wb.remove(wb.active)

    tables = soup.find_all("table")
    for index, table in enumerate(tables, start=1):
        ws = wb.create_sheet(f"Tablo {index}")
        caption = table.find("caption")
        if caption and caption.get_text(strip=True):
            ws.cell(row=1, column=1, value=caption.get_text(" ", strip=True)).font = Font(
                bold=True, size=12
            )
            start_row = 3
        else:
            start_row = 1

        for r_i, tr in enumerate(table.find_all("tr"), start=start_row):
            for c_i, cell in enumerate(tr.find_all(["th", "td"]), start=1):
                value = cell.get_text(" ", strip=True)
                target = ws.cell(row=r_i, column=c_i, value=value)
                target.alignment = Alignment(vertical="top", wrap_text=True)
                if cell.name == "th":
                    target.font = Font(bold=True, color="FFFFFF")
                    target.fill = PatternFill("solid", fgColor="1F3864")
        _autosize(ws)
        ws.freeze_panes = ws.cell(row=start_row + 1, column=1)

    if include_text:
        ws = wb.create_sheet("Metin")
        lines = soup.get_text("\n", strip=True).split("\n")
        for r_i, line in enumerate((l for l in lines if l), start=1):
            ws.cell(row=r_i, column=1, value=line)
        _autosize(ws)

    if not wb.sheetnames:
        wb.create_sheet("Sayfa1")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out
