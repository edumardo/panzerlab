"""Export the FrontMatter pages as facsimile+translation page pairs (bilingual EN/ES).

FrontMatter pages use the same content.json schema as section pages (titles,
paragraphs, figures, status), so this reuses the facsimile+translation
rendering from export_facsimile_pdf.py. A blank source page (type == "blank",
no title/paragraphs/figures) has nothing to translate, so only its facsimile
page is emitted.

Requires validated status for transcription, en-GB and es-ES on every page.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as canvas_module

from export_facsimile_pdf import (
    register_fonts,
    render_facsimile_page,
    render_translation_page,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Export pages even if transcription/en-GB/es-ES are not yet validated.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    frontmatter_dir = root / "frontmatter"
    manifest = json.loads((frontmatter_dir / "manifest.json").read_text(encoding="utf-8"))

    entries = []
    has_draft = False
    for page_number in manifest["pages"]:
        page_dir = frontmatter_dir / "pages" / f"{page_number:03d}"
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
    pdf = canvas_module.Canvas(str(args.output), pagesize=A4, pageCompression=1)
    pdf.setTitle("D. 652/50c - FrontMatter - facsimile + bilingual translation")
    pdf.setAuthor("PanzerLab")
    pdf.setSubject("Facsimile export generated from the canonical JSON decomposition")

    translation_pages = 0
    for page_dir, content in entries:
        render_facsimile_page(pdf, page_dir, content, regular, bold)
        is_blank = content.get("type") == "blank" and not content["titles"].get("en-GB") and not content["paragraphs"] and not content["figures"]
        if not is_blank:
            render_translation_page(pdf, content, regular, bold, italic)
            translation_pages += 1

    pdf.save()
    draft_note = " (contains draft/unvalidated pages)" if has_draft else ""
    print(f"Created {args.output} ({len(entries)} source pages, {translation_pages} translation pages){draft_note}.")


if __name__ == "__main__":
    main()
