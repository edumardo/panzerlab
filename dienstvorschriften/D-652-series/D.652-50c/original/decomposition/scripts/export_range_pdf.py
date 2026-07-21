"""Export a validated page range (mixing text and figure pages) to an A4 PDF."""

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

LANGUAGE_NAMES = {"en-GB": "British English", "es-ES": "Spanish (Spain)", "de-DE": "German (original)"}
TOP_MARGIN = 281 * mm
BOTTOM_MARGIN = 18 * mm
LEFT = 18 * mm
RIGHT = 18 * mm

def register_fonts():
    font_dir = Path("C:/Windows/Fonts")
    candidates = {
        "regular": font_dir / "arial.ttf",
        "bold": font_dir / "arialbd.ttf",
        "italic": font_dir / "ariali.ttf",
    }
    if all(path.is_file() for path in candidates.values()):
        pdfmetrics.registerFont(TTFont("ArchiveSans", str(candidates["regular"])))
        pdfmetrics.registerFont(TTFont("ArchiveSans-Bold", str(candidates["bold"])))
        pdfmetrics.registerFont(TTFont("ArchiveSans-Italic", str(candidates["italic"])))
        return "ArchiveSans", "ArchiveSans-Bold", "ArchiveSans-Italic"
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

def draw_header(pdf, title, page_number, regular, bold, lang_key):
    page_label = {"en-GB": "Original page", "es-ES": "Página original", "de-DE": "Originalseite"}[lang_key]
    page_label_text = f"{page_label} {page_number}"
    label_width = pdfmetrics.stringWidth(page_label_text, regular, 9)
    title_size = 14.0
    title_width_limit = A4[0] - LEFT - RIGHT - label_width - 6 * mm
    while title_size > 10.5 and pdfmetrics.stringWidth(title, bold, title_size) > title_width_limit:
        title_size -= 0.5
    pdf.setFillColor(HexColor("#102A43"))
    pdf.setFont(bold, title_size)
    pdf.drawString(LEFT, TOP_MARGIN, title)
    pdf.setFont(regular, 9)
    pdf.setFillColor(HexColor("#52606D"))
    pdf.drawRightString(A4[0] - RIGHT, TOP_MARGIN, page_label_text)
    pdf.setStrokeColor(HexColor("#BCCCDC"))
    pdf.setLineWidth(0.5)
    pdf.line(LEFT, TOP_MARGIN - 5 * mm, A4[0] - RIGHT, TOP_MARGIN - 5 * mm)

def draw_figure(pdf, page_dir, figure, language, box_bottom, box_top, regular, bold, italic):
    width = A4[0] - LEFT - RIGHT
    caption = figure["captions"][language]["plain"] if figure["captions"].get(language) else ""
    key = figure.get("label_keys", {}).get(language)
    key_text = key["plain"] if key else None
    label = f"Fig. {figure['number']} (Bild {figure['number']})"
    caption_lines = wrap_text(caption, regular, 8.4, width) if caption else []
    key_lines = wrap_text(key_text, italic, 7.8, width) if key_text else []
    text_height = (12 + len(caption_lines) * 10 + len(key_lines) * 9) * 1.0
    available_image_height = box_top - box_bottom - text_height - 8 * mm

    image_path = page_dir / figure["image"]
    with PILImage.open(image_path) as image:
        image_width, image_height = image.size
    preferred_image_width = 132 * mm
    scale = min(
        preferred_image_width / image_width,
        width / image_width,
        max(available_image_height, 20 * mm) / image_height,
    )
    draw_width = image_width * scale
    draw_height = image_height * scale
    image_x = (A4[0] - draw_width) / 2
    image_y = box_top - draw_height
    pdf.drawImage(str(image_path), image_x, image_y, draw_width, draw_height,
                  preserveAspectRatio=True, mask="auto")

    text_y = image_y - 4 * mm
    pdf.setFillColor(HexColor("#102A43"))
    pdf.setFont(bold, 9.2)
    pdf.drawString(LEFT, text_y, label)
    text_y -= 4.5 * mm
    if caption:
        text_y = draw_wrapped(pdf, caption, LEFT, text_y, width, regular, 8.4, 10)
    if key_text:
        text_y -= 1.5 * mm
        draw_wrapped(pdf, key_text, LEFT, text_y, width, italic, 7.8, 9, HexColor("#52606D"))

def render_figures_page(pdf, page_dir, content, language, regular, bold, italic):
    draw_header(pdf, content["titles"][language], content["page"], regular, bold, language)
    figs = content["figures"]
    if len(figs) == 2:
        draw_figure(pdf, page_dir, figs[0], language, 149 * mm, 270 * mm, regular, bold, italic)
        draw_figure(pdf, page_dir, figs[1], language, 18 * mm, 141 * mm, regular, bold, italic)
    elif len(figs) == 1:
        draw_figure(pdf, page_dir, figs[0], language, 18 * mm, 270 * mm, regular, bold, italic)
    pdf.showPage()


def render_text_page(pdf, content, language, regular, bold):
    width = A4[0] - LEFT - RIGHT
    draw_header(pdf, content["titles"][language], content["page"], regular, bold, language)
    y = TOP_MARGIN - 14 * mm
    for para in content["paragraphs"]:
        text = para["text"][language]["plain"] if para["text"].get(language) else ""
        if not text:
            continue
        lines = wrap_text(text, regular, 10.5, width)
        needed = len(lines) * 13 + 6
        if y - needed < BOTTOM_MARGIN:
            pdf.showPage()
            y = TOP_MARGIN - 10 * mm
        pdf.setFillColor(HexColor("#262626"))
        pdf.setFont(regular, 10.5)
        for line in lines:
            pdf.drawString(LEFT, y, line)
            y -= 13
        y -= 6
    pdf.showPage()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--sections", required=True, help="comma-separated section ids, e.g. A01,A02,A03")
    parser.add_argument("--language", choices=sorted(LANGUAGE_NAMES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-validated", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    lang = args.language
    trans_key = "transcription" if lang == "de-DE" else lang

    entries = []
    for section in args.sections.split(","):
        section_dir = root / "sections" / section
        section_manifest = json.loads((section_dir / "manifest.json").read_text(encoding="utf-8"))
        for page_number in section_manifest["pages"]:
            page_dir = section_dir / "pages" / f"{page_number:03d}"
            content = json.loads((page_dir / "content.json").read_text(encoding="utf-8"))
            if args.require_validated and content["status"][trans_key] != "validated":
                raise SystemExit(f"Page {page_number}: {trans_key} is not validated")
            entries.append((page_dir, content))

    entries.sort(key=lambda e: e[1]["page"])

    regular, bold, italic = register_fonts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(args.output), pagesize=A4, pageCompression=1)
    pdf.setTitle(f"D. 652/50c - {args.sections} - {LANGUAGE_NAMES[lang]}")
    pdf.setAuthor("PanzerLab")
    pdf.setSubject("Export generated from the canonical JSON decomposition")

    for page_dir, content in entries:
        if content["type"] == "text":
            render_text_page(pdf, content, lang, regular, bold)
        else:
            render_figures_page(pdf, page_dir, content, lang, regular, bold, italic)

    pdf.save()
    print(f"Created {args.output} ({len(entries)} source pages).")


if __name__ == "__main__":
    main()
