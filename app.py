"""Masaüstü uygulama giriş noktası (pywebview)."""

from __future__ import annotations

import sys
from pathlib import Path

import webview

from converter import convert_files, merge_files, wrap_sections

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
UI_FILE = BASE_DIR / "ui" / "index.html"

window = None

OPEN_DIALOG = getattr(webview, "FileDialog", None)
OPEN = OPEN_DIALOG.OPEN if OPEN_DIALOG else webview.OPEN_DIALOG
SAVE = OPEN_DIALOG.SAVE if OPEN_DIALOG else webview.SAVE_DIALOG


class Api:
    """JavaScript'ten çağrılan fonksiyonlar."""

    def pick_files(self):
        try:
            result = window.create_file_dialog(
                OPEN,
                allow_multiple=True,
                file_types=(
                    "Markdown dosyaları (*.md;*.markdown;*.txt)",
                    "Tüm dosyalar (*.*)",
                ),
            )
            return list(result or [])
        except Exception as exc:  # kullanıcı iptal ederse boş döner
            return []

    def preview(self, files):
        try:
            merged = merge_files(files)
            return {"ok": True, "html": wrap_sections(merged)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def convert(self, files, fmt, title):
        ext = {"docx": "docx", "pdf": "pdf", "xlsx": "xlsx"}.get(fmt, fmt)
        default_name = f"birlesik-rapor.{ext}"
        try:
            result = window.create_file_dialog(
                SAVE,
                save_filename=default_name,
                file_types=(
                    f"{fmt.upper()} dosyası (*.{ext})",
                    "Tüm dosyalar (*.*)",
                ),
            )
            if not result:
                return {"ok": False, "msg": "Kaydetme iptal edildi."}
            output = result if isinstance(result, str) else result[0]
            convert_files(files, fmt, output, title=(title or "").strip() or None)
            return {"ok": True, "msg": f"Kaydedildi: {output}"}
        except Exception as exc:
            return {"ok": False, "msg": str(exc)}


def main():
    global window
    window = webview.create_window(
        "Markdown Dönüştürücü",
        str(UI_FILE),
        js_api=Api(),
        width=980,
        height=720,
        min_size=(760, 560),
        background_color="#0f1420",
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
