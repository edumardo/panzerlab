"""Render a compiled-edition title page, matching the style already established
for D.652-41a (dienstvorschriften/D-652-series/D.652-41a/en/D.652-41a_en_v1.0.docx).

This is a series-wide visual template, not specific to one document: a future
document's export should import render_title_page and pass its own spec dict
(see TITLE_PAGE_SPEC below for the field shapes) rather than re-deriving the
style. Once the format is confirmed, consider promoting this file to a
series-level scripts/ location so every D-652 document imports the same copy
instead of each carrying its own.

Colours and sizes were extracted from the 41a docx's actual runs and
paragraph spacing (python-docx introspection), not eyeballed from the PDF.
"""

from __future__ import annotations

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics

TITLE_COLOR = HexColor("#2E3A22")
MODEL_LINE_COLOR = HexColor("#000000")
SUBTITLE_EN_COLOR = HexColor("#444444")
SUBTITLE_DE_COLOR = HexColor("#777777")
EDITION_COLOR = HexColor("#2E3A22")
ORG_COLOR = HexColor("#777777")
CREDIT_COLOR = HexColor("#999999")
VERSION_COLOR = HexColor("#777777")
RUNNING_TEXT_COLOR = HexColor("#888888")

# Example spec for D.652-50c. A future document builds its own dict with the
# same keys and passes it to render_title_page -- nothing here is read
# implicitly, so copying this file to another document's scripts/ needs no
# further edits beyond swapping this constant (or passing a fresh dict).
TITLE_PAGE_SPEC = {
    "designation": "D 652/50c",
    "model_lines": [
        "Panzerkampfwagen III · Panzerbefehlswagen (Ausf. E–L)",
        "Gepanzerte Selbstfahrlafette / StuG (Ausf. A–G)",
    ],
    "subtitle_en": "Preliminary repair instructions for the engine",
    "subtitle_de": "Vorläufige Instandsetzungsanleitung für den Motor",
    "edition_line": (
        "Complete bilingual edition — full facsimile of the original German "
        "with English and Spanish translation"
    ),
    "org_line": "Heereswaffenamt · Berlin, 3 November 1943",
    "credit_line": (
        "Compiled by Eduardo Delgado Díaz (edelgadodiaz@gmail.com, "
        "https://github.com/edumardo/panzerlab) · Asociación de Amigos del "
        "Museo Histórico Militar de Cartagena (AAMMILCAR, aammilcar@gmail.com)"
    ),
    "source_line": "Original file: https://bushmakow.com/library/",
    "version_line": "Version 1.0",
}


def _wrap(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if not current or pdfmetrics.stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_centered(pdf, text, font, size, color, page_w, y, max_width=None, leading=None):
    pdf.setFont(font, size)
    pdf.setFillColor(color)
    if max_width and pdfmetrics.stringWidth(text, font, size) > max_width:
        lines = _wrap(text, font, size, max_width)
        leading = leading or size * 1.3
        for line in lines:
            pdf.drawCentredString(page_w / 2, y, line)
            y -= leading
        return y + leading
    pdf.drawCentredString(page_w / 2, y, text)
    return y


def render_title_page(pdf, spec, regular, bold, italic, page_w, page_h):
    margin = 20 * mm
    max_width = page_w - 2 * margin
    y = page_h - 65 * mm

    _draw_centered(pdf, spec["designation"], bold, 32, TITLE_COLOR, page_w, y)
    y -= 10 * mm

    for i, line in enumerate(spec["model_lines"]):
        _draw_centered(pdf, line, bold, 16, MODEL_LINE_COLOR, page_w, y, max_width)
        y -= 6 * mm if i < len(spec["model_lines"]) - 1 else 10 * mm

    _draw_centered(pdf, spec["subtitle_en"], italic, 13, SUBTITLE_EN_COLOR, page_w, y, max_width)
    y -= 6 * mm
    _draw_centered(pdf, spec["subtitle_de"], regular, 11, SUBTITLE_DE_COLOR, page_w, y, max_width)
    y -= 16 * mm

    y = _draw_centered(pdf, spec["edition_line"], regular, 11, EDITION_COLOR, page_w, y, max_width)
    y -= 6 * mm
    _draw_centered(pdf, spec["org_line"], regular, 10, ORG_COLOR, page_w, y, max_width)
    y -= 26 * mm

    y = _draw_centered(pdf, spec["credit_line"], italic, 9, CREDIT_COLOR, page_w, y, max_width)
    y -= 5 * mm
    y = _draw_centered(pdf, spec["source_line"], italic, 9, CREDIT_COLOR, page_w, y, max_width)
    y -= 8 * mm
    _draw_centered(pdf, spec["version_line"], bold, 9, VERSION_COLOR, page_w, y, max_width)

    pdf.showPage()
