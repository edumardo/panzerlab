"""Render a compiled-edition title page in the D-652 series' standard style.

Confirmed as the series-wide format (2026-09-08) after reviewing D.652-50c's
title page: A4 portrait, dark-olive-green title, bold black model lines, an
EN-then-ES-then-DE subtitle block, an EN-then-ES edition line, then a grey
org/date line, a credit block, and a version line. Colours and sizes were
extracted from D.652-41a's compiled docx (D-652-series/D.652-41a/en/
D.652-41a_en_v1.0.docx) via python-docx introspection of its actual runs and
paragraph spacing, not eyeballed from the rendered PDF.

A document's own export script imports render_title_page from here and
supplies its own spec dict (see any D.652-*/original/decomposition/scripts/
title_page_spec.py for the field shapes: designation, model_lines,
subtitle_en/es/de, edition_line/edition_line_es, org_line, credit_line,
source_line, version_line). Keep the credit_line text identical across the
series; source_line should cite that document's own metadata.md/metadata.json
source URL.
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
        y = _draw_centered(pdf, line, bold, 16, MODEL_LINE_COLOR, page_w, y, max_width)
        y -= 6 * mm if i < len(spec["model_lines"]) - 1 else 10 * mm

    y = _draw_centered(pdf, spec["subtitle_en"], italic, 13, SUBTITLE_EN_COLOR, page_w, y, max_width)
    y -= 6 * mm
    y = _draw_centered(pdf, spec["subtitle_es"], italic, 13, SUBTITLE_EN_COLOR, page_w, y, max_width)
    y -= 6 * mm
    _draw_centered(pdf, spec["subtitle_de"], regular, 11, SUBTITLE_DE_COLOR, page_w, y, max_width)
    y -= 16 * mm

    y = _draw_centered(pdf, spec["edition_line"], regular, 11, EDITION_COLOR, page_w, y, max_width)
    y -= 6 * mm
    y = _draw_centered(pdf, spec["edition_line_es"], regular, 11, EDITION_COLOR, page_w, y, max_width)
    y -= 6 * mm
    _draw_centered(pdf, spec["org_line"], regular, 10, ORG_COLOR, page_w, y, max_width)
    y -= 26 * mm

    y = _draw_centered(pdf, spec["credit_line"], italic, 9, CREDIT_COLOR, page_w, y, max_width)
    y -= 5 * mm
    y = _draw_centered(pdf, spec["source_line"], italic, 9, CREDIT_COLOR, page_w, y, max_width)
    y -= 8 * mm
    _draw_centered(pdf, spec["version_line"], bold, 9, VERSION_COLOR, page_w, y, max_width)

    pdf.showPage()
