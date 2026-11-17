"""HTML -> PDF (Playwright / Chromium). Metin seçilebilir, baskıya hazır çıktı."""

from pathlib import Path

from playwright.sync_api import sync_playwright

DEFAULT_CSS = """
@page { size: A4; margin: 18mm; }
* { box-sizing: border-box; }
body {
  font-family: "Helvetica Neue", Arial, "Segoe UI", sans-serif;
  font-size: 11pt;
  line-height: 1.55;
  color: #1a1a1a;
}
h1, h2, h3, h4, h5, h6 { color: #1f3864; margin: 1.1em 0 0.5em; line-height: 1.25; }
h1 { font-size: 20pt; border-bottom: 2px solid #1f3864; padding-bottom: 6px; }
h2 { font-size: 16pt; }
h3 { font-size: 13pt; }
p { margin: 0 0 0.7em; }
ul, ol { margin: 0 0 0.8em; padding-left: 1.6em; }
li { margin-bottom: 0.25em; }
a { color: #0563c1; }
code {
  font-family: "Courier New", monospace;
  background: #f2f2f2;
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 0.9em;
}
pre {
  background: #f6f6f6;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px 12px;
  overflow-x: auto;
  white-space: pre-wrap;
}
pre code { background: none; padding: 0; }
blockquote {
  border-left: 4px solid #1f3864;
  margin: 0.8em 0;
  padding: 0.2em 0 0.2em 12px;
  color: #444;
  background: #f7f9fc;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.8em 0 1.1em;
  font-size: 10pt;
}
th, td {
  border: 1px solid #b8c4d6;
  padding: 6px 9px;
  text-align: left;
  vertical-align: top;
}
th { background: #1f3864; color: #fff; font-weight: 600; }
tr:nth-child(even) td { background: #f4f6fa; }
hr { border: 0; border-top: 1px solid #ccc; margin: 1.2em 0; }
section:not(:last-child) { page-break-after: always; break-after: page; }
"""


def html_to_pdf(html: str, output_path: str | Path, css: str = DEFAULT_CSS) -> Path:
    """Chromium'un yazdırma motoruyla PDF üretir."""
    full_doc = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<style>{css}</style></head><body>{html}</body></html>"
    )
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # Önce Playwright'ın kendi Chromium'unu dener; yoksa Windows'ta hazır
        # gelen Edge'i kullanır (paketlemede tarayıcı indirmeyi önler).
        browser = None
        last_error = None
        # Arka plan ağ trafiğini tamamen kapat: hiçbir veri dışarı çıkmaz.
        offline_args = [
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-sync",
            "--no-first-run",
        ]
        for options in (
            {"args": offline_args},
            {"channel": "msedge", "args": offline_args},
        ):
            try:
                browser = p.chromium.launch(**options)
                break
            except Exception as exc:  # noqa: BLE001 - fallback zinciri
                last_error = exc
        if browser is None:
            raise RuntimeError(
                "PDF için tarayıcı bulunamadı. `playwright install chromium` "
                "komutunu çalıştırın veya Microsoft Edge kurulu olduğundan emin olun."
            ) from last_error
        page = browser.new_page()
        page.set_content(full_doc, wait_until="load")
        page.pdf(
            path=str(out),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        browser.close()
    return out
