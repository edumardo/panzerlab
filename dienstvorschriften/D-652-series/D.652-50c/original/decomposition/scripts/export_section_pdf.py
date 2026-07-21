"""Export one validated canonical section to an A4 translated PDF."""

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


LANGUAGE_NAMES = {"en-GB": "British English", "es-ES": "Spanish (Spain)"}


def register_fonts() -> tuple[str, str, str]:
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


def wrap_text(text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
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


def draw_wrapped(
    pdf: canvas.Canvas, text: str, x: float, y: float, width: float,
    font: str, size: float, leading: float, colour=HexColor("#262626"),
) -> float:
    pdf.setFillColor(colour)
    pdf.setFont(font, size)
    for line in wrap_text(text, font, size, width):
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_figure(
    pdf: canvas.Canvas, page_dir: Path, figure: dict, language: str,
    box_bottom: float, box_top: float, regular: str, bold: str, italic: str,
) -> None:
    left = 18 * mm
    width = A4[0] - 36 * mm
    caption = figure["captions"][language]["plain"]
    key = figure.get("label_keys", {}).get(language)
    key_text = key["plain"] if key else None
    label = f"Fig. {figure['number']} (Bild {figure['number']})"
    caption_lines = wrap_text(caption, regular, 8.4, width)
    key_lines = wrap_text(key_text, italic, 7.8, width) if key_text else []
    text_height = (12 + len(caption_lines) * 10 + len(key_lines) * 9) * 1.0
    available_image_height = box_top - box_bottom - text_height - 8 * mm
    if available_image_height < 35 * mm:
        raise ValueError(
            f"Fig. {figure['number']}: caption leaves insufficient image space"
        )

    image_path = page_dir / figure["image"]
    with PILImage.open(image_path) as image:
        image_width, image_height = image.size
    preferred_image_width = 132 * mm
    scale = min(
        preferred_image_width / image_width,
        width / image_width,
        available_image_height / image_height,
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
    pdf.drawString(left, text_y, label)
    text_y -= 4.5 * mm
    text_y = draw_wrapped(pdf, caption, left, text_y, width, regular, 8.4, 10)
    if key_text:
        text_y -= 1.5 * mm
        draw_wrapped(pdf, key_text, left, text_y, width, italic, 7.8, 9, HexColor("#52606D"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--section", required=True)
    parser.add_argument("--language", choices=sorted(LANGUAGE_NAMES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    section_dir = root / "sections" / args.section
    section_manifest = json.loads((section_dir / "manifest.json").read_text(encoding="utf-8"))
    page_numbers = section_manifest["pages"]
    pages: list[tuple[Path, dict]] = []
    for page_number in page_numbers:
        page_dir = section_dir / "pages" / f"{page_number:03d}"
        content = json.loads((page_dir / "content.json").read_text(encoding="utf-8"))
        if content["status"][args.language] != "validated":
            raise SystemExit(f"Page {page_number}: {args.language} is not validated")
        if content["status"]["figures"] != "validated" or len(content["figures"]) != 2:
            raise SystemExit(f"Page {page_number}: exactly two validated figures are required")
        pages.append((page_dir, content))

    regular, bold, italic = register_fonts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(args.output), pagesize=A4, pageCompression=1)
    pdf.setTitle(f"D. 652/50c — {args.section} — {LANGUAGE_NAMES[args.language]}")
    pdf.setAuthor("PanzerLab")
    pdf.setSubject("Translated section generated from the canonical JSON decomposition")
    for page_dir, content in pages:
        title = content["titles"][args.language]
        page_label = "Original page" if args.language == "en-GB" else "Página original"
        page_label_text = f"{page_label} {content['page']}"
        label_width = pdfmetrics.stringWidth(page_label_text, regular, 9)
        title_size = 14.0
        title_width_limit = A4[0] - 36 * mm - label_width - 6 * mm
        while title_size > 10.5 and pdfmetrics.stringWidth(title, bold, title_size) > title_width_limit:
            title_size -= 0.5
        pdf.setFillColor(HexColor("#102A43"))
        pdf.setFont(bold, title_size)
        pdf.drawString(18 * mm, 281 * mm, title)
        pdf.setFont(regular, 9)
        pdf.setFillColor(HexColor("#52606D"))
        pdf.drawRightString(A4[0] - 18 * mm, 281 * mm, page_label_text)
        pdf.setStrokeColor(HexColor("#BCCCDC"))
        pdf.setLineWidth(0.5)
        pdf.line(18 * mm, 276 * mm, A4[0] - 18 * mm, 276 * mm)
        draw_figure(pdf, page_dir, content["figures"][0], args.language,
                    149 * mm, 270 * mm, regular, bold, italic)
        draw_figure(pdf, page_dir, content["figures"][1], args.language,
                    18 * mm, 141 * mm, regular, bold, italic)
        pdf.showPage()
    pdf.save()
    print(f"Created {args.output} ({len(pages)} A4 pages, two figures per page).")


if __name__ == "__main__":
    main()
