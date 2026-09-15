"""Export a section as facsimile+translation page pairs (bilingual EN/ES).

For each source page: page N is the full original scan (source_display.jpg if
present, else source.jpg), page N+1 is the translated title, paragraphs and
figure captions on that page, listed as an EN block then an ES block.

Adapted from D.652-50c's exporter, with two differences this document needs:

* Mixed orientation, decided per page from the scan itself. A section's
  manifest layout field selects the export mode (facsimile then translation);
  it is too coarse to set orientation here, because D.652-41a's scans do not
  divide cleanly by section: G is declared landscape but its first page (the
  plate list and colophon, book page 73) is an ordinary portrait text page,
  while FrontMatter is declared portrait yet book page 1 is a landscape scan.
  Honouring the section would letterbox 29 pages into the wrong box, so each
  facsimile page takes the orientation of its own source image and the page
  size is applied with setPageSize. Translation pages stay A4 portrait
  throughout: they are running text, and portrait is the series standard.
* Null-safe titles. Most D.652-41a pages carry titles of null (the running
  text has no per-page heading); the header falls back to a generic label
  rather than passing None into stringWidth.

Requires validated status for transcription, en-GB and es-ES on every page
unless --allow-draft is passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BOTTOM_MARGIN = 18 * mm
LEFT = 18 * mm
RIGHT = 18 * mm
TOP_OFFSET = 16 * mm
LANG_LABEL = {"en-GB": "EN", "es-ES": "ES"}
LANGUAGES = ["en-GB", "es-ES"]
PORTRAIT = A4
LANDSCAPE = landscape(A4)
UNTITLED = "Original page (no heading)"


class Geometry:
    """Page box for one orientation, so a document can mix both."""

    def __init__(self, pagesize):
        self.pagesize = pagesize
        self.width, self.height = pagesize
        self.top = self.height - TOP_OFFSET
        self.text_width = self.width - LEFT - RIGHT

    def apply(self, pdf):
        pdf.setPageSize(self.pagesize)


def geometry_for_image(image_path):
    """Page geometry matching the orientation of this page's own scan."""
    with PILImage.open(image_path) as image:
        width, height = image.size
    return Geometry(LANDSCAPE if width > height else PORTRAIT)


def source_image_path(page_dir, content):
    source = content["source"]
    return page_dir / source.get("display_image", source["image"])


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


def draw_header(pdf, geom, title, page_number, regular, bold, label, subtitle=None):
    title = title or UNTITLED
    page_label_text = f"{label} {page_number}"
    label_width = pdfmetrics.stringWidth(page_label_text, regular, 9)
    title_size = 13.0
    title_width_limit = geom.width - LEFT - RIGHT - label_width - 6 * mm
    while title_size > 9.5 and pdfmetrics.stringWidth(title, bold, title_size) > title_width_limit:
        title_size -= 0.5
    pdf.setFillColor(HexColor("#102A43"))
    pdf.setFont(bold, title_size)
    pdf.drawString(LEFT, geom.top, title)
    pdf.setFont(regular, 9)
    pdf.setFillColor(HexColor("#52606D"))
    pdf.drawRightString(geom.width - RIGHT, geom.top, page_label_text)

    rule_y = geom.top - 5 * mm
    if subtitle:
        subtitle_size = 10.5
        while subtitle_size > 8 and pdfmetrics.stringWidth(subtitle, regular, subtitle_size) > geom.text_width:
            subtitle_size -= 0.5
        pdf.setFont(regular, subtitle_size)
        pdf.setFillColor(HexColor("#334E68"))
        pdf.drawString(LEFT, geom.top - 6 * mm, subtitle)
        rule_y = geom.top - 10 * mm

    pdf.setStrokeColor(HexColor("#BCCCDC"))
    pdf.setLineWidth(0.5)
    pdf.line(LEFT, rule_y, geom.width - RIGHT, rule_y)
    return rule_y


def render_facsimile_page(pdf, page_dir, content, regular, bold):
    image_path = source_image_path(page_dir, content)
    geom = geometry_for_image(image_path)
    geom.apply(pdf)
    draw_header(pdf, geom, "Original (facsimile)", content["page"], regular, bold, "Page")

    with PILImage.open(image_path) as image:
        image_width, image_height = image.size

    box_top = geom.top - 8 * mm
    box_bottom = BOTTOM_MARGIN
    available_w = geom.text_width
    available_h = box_top - box_bottom
    scale = min(available_w / image_width, available_h / image_height)
    draw_width, draw_height = image_width * scale, image_height * scale
    image_x = (geom.width - draw_width) / 2
    image_y = box_bottom + (available_h - draw_height) / 2
    pdf.drawImage(str(image_path), image_x, image_y, draw_width, draw_height,
                  preserveAspectRatio=True, mask="auto")
    pdf.setStrokeColor(HexColor("#DCE4EC"))
    pdf.setLineWidth(0.5)
    pdf.rect(image_x, image_y, draw_width, draw_height)
    pdf.showPage()


def render_translation_page(pdf, content, regular, bold, italic):
    geom = Geometry(PORTRAIT)
    geom.apply(pdf)
    width = geom.text_width
    es_title = content["titles"].get(LANGUAGES[1])
    rule_y = draw_header(
        pdf, geom, content["titles"].get(LANGUAGES[0]), content["page"], regular, bold,
        "Translation of page", subtitle=es_title,
    )

    y = rule_y - 9 * mm

    def break_page():
        pdf.showPage()
        geom.apply(pdf)
        return geom.top - 10 * mm

    for lang in LANGUAGES:
        for para in content["paragraphs"]:
            text = para["text"][lang]["plain"] if para["text"].get(lang) else ""
            if not text:
                continue
            tagged = f"[{LANG_LABEL[lang]}] {text}"
            lines = wrap_text(tagged, regular, 10.5, width)
            needed = len(lines) * 13 + 6
            if y - needed < BOTTOM_MARGIN:
                y = break_page()
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
            y = break_page()
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
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Export pages even if transcription/en-GB/es-ES are not yet validated.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    section_dir = root / "frontmatter" if args.section == "FrontMatter" else root / "sections" / args.section
    section_manifest = json.loads((section_dir / "manifest.json").read_text(encoding="utf-8"))

    entries = []
    has_draft = False
    for page_number in section_manifest["pages"]:
        page_dir = section_dir / "pages" / f"{page_number:03d}"
        content = json.loads((page_dir / "content.json").read_text(encoding="utf-8"))
        for key in ("transcription", "en-GB", "es-ES"):
            if content["status"][key] != "validated":
                has_draft = True
                if not args.allow_draft:
                    raise SystemExit(f"Page {page_number}: {key} is not validated")
        entries.append((page_dir, content))
    entries.sort(key=lambda e: e[1]["page"])

    regular, bold, italic = register_fonts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(args.output), pagesize=PORTRAIT, pageCompression=1)
    pdf.setTitle(f"D. 652/41a - {args.section} - facsimile + bilingual translation")
    pdf.setAuthor("PanzerLab")
    pdf.setSubject("Facsimile export generated from the canonical JSON decomposition")

    for page_dir, content in entries:
        render_facsimile_page(pdf, page_dir, content, regular, bold)
        render_translation_page(pdf, content, regular, bold, italic)

    pdf.save()
    draft_note = " (contains draft/unvalidated pages)" if has_draft else ""
    print(f"Created {args.output} ({len(entries)} source pages x2){draft_note}.")


if __name__ == "__main__":
    main()
