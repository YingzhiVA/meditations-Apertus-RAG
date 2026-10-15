"""Render technical_report.md to the submission PDF (A4, diagram embedded).

    pip install markdown playwright pypdf   # dev only, not in the image
    python docs/render_report.py . YingzhiVA_Report.pdf

Chromium prints the PDF; set CHROMIUM to its path if Playwright has none.
"""
import os
import sys
from pathlib import Path
import markdown
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

root = Path(sys.argv[1]).resolve(); out = root / sys.argv[2]
body = markdown.markdown((root / "technical_report.md").read_text(encoding="utf-8"),
                         extensions=["tables", "sane_lists"])
css = """
@page { size: A4; margin: 16mm 15mm 16mm 15mm; }
body { font-family: 'DejaVu Sans', Helvetica, Arial, sans-serif; font-size: 9.4pt;
       line-height: 1.42; color: #111; }
h1 { font-size: 17pt; margin: 0 0 4pt; }
h2 { font-size: 12.5pt; margin: 12pt 0 4pt; border-bottom: 1px solid #bbb; padding-bottom: 2pt; }
h3 { font-size: 10.5pt; margin: 9pt 0 3pt; }
p, li { margin: 0 0 5pt; }
ul, ol { margin: 0 0 5pt; padding-left: 16pt; }
table { border-collapse: collapse; margin: 4pt 0 8pt; font-size: 8.4pt; width: 100%; }
th, td { border: 1px solid #ccc; padding: 2.5pt 4pt; text-align: left; vertical-align: top; }
th { background: #f1f1f1; }
code { font-size: 8.4pt; background: #f4f4f4; padding: 0 2px; }
img { width: 100%; margin: 4pt 0 6pt; }
a { color: #1a4f8a; text-decoration: none; }
h2, h3 { break-after: avoid; } table, img { break-inside: avoid; }
"""
html = f"<!doctype html><html><head><meta charset='utf-8'><base href='{root.as_uri()}/'>" \
       f"<style>{css}</style></head><body>{body}</body></html>"
tmp = root / ".report.html"; tmp.write_text(html, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
    pg = b.new_page(); pg.goto(tmp.as_uri()); pg.wait_for_timeout(500)
    pg.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True)
    b.close()
tmp.unlink()
r = PdfReader(str(out))
pages = [p.extract_text() for p in r.pages]
ref_page = next((i + 1 for i, t in enumerate(pages) if "References" in t and "1. M. Aurelius" in t.replace("\n", " ")), None)
print(f"{out.name}: {len(pages)} pages; References start on page {ref_page}")
