"""Export a section as facsimile+translation page pairs (bilingual EN/ES).

For each source page: page N is the full original scan (source_display.jpg if
present, else source.jpg), page N+1 is the translated title and every figure
caption on that page, shown side by side in English and Spanish. This replaces
the per-figure crop export for sections that adopt the
"A4_portrait_facsimile_then_translation" section layout: the reader always sees
the untouched original page, so individual figure crops are no longer required.

Requires validated status for transcription, en-GB and es-ES on every page.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

TOP_MARGIN = 281 * mm
BOTTOM_MARGIN = 18 * mm
LEFT = 18 * mm
RIGHT = 18 * mm
PAGE_W, PAGE_H = A4
LANG_LABEL = {"en-GB": "EN", "es-ES": "ES"}
LANGUAGES = ["en-GB", "es-ES"]


def register_fonts():
    font_dir = Path("C:/Windows/Fonts")
    candidates = {
        "regular": font_dir / "arial.ttf",
        "bold": font_dir / "arialbd.ttf",
        "italic": font_dir / "ariali.ttf",
    }
    if all(path.is_file() for path in candidates.values()):
        pdfmetrics.registerFont(TTFont("FacsimileSans", str(candidates["regular"])))
        pdfmetrics.registerFont(TTFont("FacsimileSans-Bold", str(candidates["bold"])))
        pdfmetrics.registerFont(TTFont("FacsimileSans-Italic", str(candidates["italic"])))
        return "FacsimileSans", "FacsimileSans-Bold", "FacsimileSans-Italic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


def wrap_text(text, font, size, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if not current or pdfmetrics.stringWidth(candidate, font, size) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(pdf, text, x, y, width, font, size, leading, colour=HexColor("#262626")):
    pdf.setFillColor(colour)
    pdf.setFont(font, size)
    for line in wrap_text(text, font, size, width):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_header(pdf, title, page_number, regular, bold, label):
    page_label_text = f"{label} {page_number}"
    label_width = pdfmetrics.stringWidth(page_label_text, regular, 9)
    title_size = 13.0
    title_width_limit = PAGE_W - LEFT - RIGHT - label_width - 6 * mm
    while title_size > 9.5 and pdfmetrics.stringWidth(title, bold, title_size) > title_width_limit:
        title_size -= 0.5
    pdf.setFillColor(HexColor("#102A43"))
    pdf.setFont(bold, title_size)
    pdf.drawString(LEFT, TOP_MARGIN, title)
    pdf.setFont(regular, 9)
    pdf.setFillColor(HexColor("#52606D"))
    pdf.drawRightString(PAGE_W - RIGHT, TOP_MARGIN, page_label_text)
    pdf.setStrokeColor(HexColor("#BCCCDC"))
    pdf.setLineWidth(0.5)
    pdf.line(LEFT, TOP_MARGIN - 5 * mm, PAGE_W - RIGHT, TOP_MARGIN - 5 * mm)


def render_facsimile_page(pdf, page_dir, content, regular, bold):
    draw_header(pdf, "Original (facsimile)", content["page"], regular, bold, "Page")

    source = content["source"]
    image_name = source.get("display_image", source["image"])
    image_path = page_dir / image_name
    with PILImage.open(image_path) as image:
        image_width, image_height = image.size

    box_top = TOP_MARGIN - 8 * mm
    box_bottom = BOTTOM_MARGIN
    available_w = PAGE_W - LEFT - RIGHT
    available_h = box_top - box_bottom
    scale = min(available_w / image_width, available_h / image_height)
    draw_width, draw_height = image_width * scale, image_height * scale
    image_x = (PAGE_W - draw_width) / 2
    image_y = box_bottom + (available_h - draw_height) / 2
    pdf.drawImage(str(image_path), image_x, image_y, draw_width, draw_height,
                  preserveAspectRatio=True, mask="auto")
    pdf.setStrokeColor(HexColor("#DCE4EC"))
    pdf.setLineWidth(0.5)
    pdf.rect(image_x, image_y, draw_width, draw_height)
    pdf.showPage()


def render_translation_page(pdf, content, regular, bold, italic):
    width = PAGE_W - LEFT - RIGHT
    draw_header(pdf, content["titles"][LANGUAGES[0]], content["page"], regular, bold, "Translation of page")

    y = TOP_MARGIN - 14 * mm

    for lang in LANGUAGES:
        for para in content["paragraphs"]:
            text = para["text"][lang]["plain"] if para["text"].get(lang) else ""
            if not text:
                continue
            tagged = f"[{LANG_LABEL[lang]}] {text}"
            lines = wrap_text(tagged, regular, 10.5, width)
            needed = len(lines) * 13 + 6
            if y - needed < BOTTOM_MARGIN:
                pdf.showPage()
                y = TOP_MARGIN - 10 * mm
            y = draw_wrapped(pdf, tagged, LEFT, y, width, regular, 10.5, 13)
            y -= 6

    for figure in content["figures"]:
        label = f"Fig. {figure['number']}"
        per_lang_lines = {}
        block_lines = 1
        for lang in LANGUAGES:
            caption = figure["captions"][lang]["plain"] if figure["captions"].get(lang) else ""
            lines = wrap_text(f"[{LANG_LABEL[lang]}] {caption}", regular, 9.5, width) if caption else []
            per_lang_lines[lang] = lines
            block_lines += len(lines)
        needed = block_lines * 12 + 8
        if y - needed < BOTTOM_MARGIN:
            pdf.showPage()
            y = TOP_MARGIN - 10 * mm
        pdf.setFillColor(HexColor("#102A43"))
        pdf.setFont(bold, 10.5)
        pdf.drawString(LEFT, y, label)
        y -= 13
        for lang in LANGUAGES:
            for line in per_lang_lines[lang]:
                pdf.setFillColor(HexColor("#262626"))
                pdf.setFont(regular, 9.5)
                pdf.drawString(LEFT, y, line)
                y -= 12
            y -= 3
        y -= 6

    pdf.showPage()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--section", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-validated", action="store_true", default=True)
    args = parser.parse_args()

    root = args.root.resolve()
    section_dir = root / "sections" / args.section
    section_manifest = json.loads((section_dir / "manifest.json").read_text(encoding="utf-8"))

    entries = []
    for page_number in section_manifest["pages"]:
        page_dir = section_dir / "pages" / f"{page_number:03d}"
        content = json.loads((page_dir / "content.json").read_text(encoding="utf-8"))
        if args.require_validated:
            for key in ("transcription", "en-GB", "es-ES"):
                if content["status"][key] != "validated":
                    raise SystemExit(f"Page {page_number}: {key} is not validated")
        entries.append((page_dir, content))
    entries.sort(key=lambda e: e[1]["page"])

    regular, bold, italic = register_fonts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(args.output), pagesize=A4, pageCompression=1)
    pdf.setTitle(f"D. 652/50c - {args.section} - facsimile + bilingual translation")
    pdf.setAuthor("PanzerLab")
    pdf.setSubject("Facsimile export generated from the canonical JSON decomposition")

    for page_dir, content in entries:
        render_facsimile_page(pdf, page_dir, content, regular, bold)
        render_translation_page(pdf, content, regular, bold, italic)

    pdf.save()
    print(f"Created {args.output} ({len(entries)} source pages x2).")


if __name__ == "__main__":
    main()
