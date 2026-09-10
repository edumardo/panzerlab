"""Export the entire D.652-50a document as a single bilingual PDF.

Renders, into one PDF in this order: the compiled-edition title page,
FrontMatter (facsimile+translation, skipping the blank scan's translation
page), then every section A01-B31 in manifest order (facsimile+translation
per page). This replaces generating a separate PDF per section and merging
them: the document's only canonical bilingual output is
bilingual/D.652-50a_bilingual_full_v1.0.pdf -- no per-section PDFs are kept.

Requires validated status for transcription, en-GB and es-ES on every page,
unless --allow-draft is passed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as canvas_module

from export_facsimile_pdf import (
    PAGE_H,
    PAGE_W,
    register_fonts,
    render_facsimile_page,
    render_translation_page,
)
from title_page_spec import TITLE_PAGE_SPEC

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
from title_page import render_title_page  # noqa: E402


def _load_entries(section_dir, page_numbers, allow_draft):
    entries = []
    has_draft = False
    for page_number in page_numbers:
        page_dir = section_dir / "pages" / f"{page_number:03d}"
        content = json.loads((page_dir / "content.json").read_text(encoding="utf-8"))
        for key in ("transcription", "en-GB", "es-ES"):
            # "not_applicable" is a legitimate final state for a blank page
            # (nothing to transcribe/translate), not an unreviewed draft.
            if content["status"][key] not in ("validated", "not_applicable"):
                has_draft = True
                if not allow_draft:
                    raise SystemExit(f"Page {page_number}: {key} is not validated")
        entries.append((page_dir, content))
    entries.sort(key=lambda e: e[1]["page"])
    return entries, has_draft


def _render_entries(pdf, entries, regular, bold, italic, skip_blank_translation=False):
    translation_pages = 0
    for page_dir, content in entries:
        render_facsimile_page(pdf, page_dir, content, regular, bold)
        is_blank = (
            skip_blank_translation
            and content.get("type") == "blank"
            and not content["titles"].get("en-GB")
            and not content["paragraphs"]
            and not content["figures"]
        )
        if not is_blank:
            render_translation_page(pdf, content, regular, bold, italic)
            translation_pages += 1
    return translation_pages


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
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))

    regular, bold, italic = register_fonts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas_module.Canvas(str(args.output), pagesize=A4, pageCompression=1)
    pdf.setTitle("D. 652/50a - complete bilingual facsimile + translation")
    pdf.setAuthor("PanzerLab")
    pdf.setSubject("Facsimile export generated from the canonical JSON decomposition")

    render_title_page(pdf, TITLE_PAGE_SPEC, regular, bold, italic, PAGE_W, PAGE_H)

    has_draft = False
    total_pages = 0
    total_translations = 0

    frontmatter_dir = root / "frontmatter"
    frontmatter_pages = json.loads((frontmatter_dir / "manifest.json").read_text(encoding="utf-8"))["pages"]
    entries, draft = _load_entries(frontmatter_dir, frontmatter_pages, args.allow_draft)
    has_draft = has_draft or draft
    total_translations += _render_entries(pdf, entries, regular, bold, italic, skip_blank_translation=True)
    total_pages += len(entries)

    for section_id, page_numbers in manifest["sections"].items():
        if section_id == "FrontMatter":
            continue
        section_dir = root / "sections" / section_id
        page_range = list(range(page_numbers[0], page_numbers[1] + 1))
        entries, draft = _load_entries(section_dir, page_range, args.allow_draft)
        has_draft = has_draft or draft
        total_translations += _render_entries(pdf, entries, regular, bold, italic)
        total_pages += len(entries)

    pdf.save()
    draft_note = " (contains draft/unvalidated pages)" if has_draft else ""
    print(
        f"Created {args.output} (1 title page + {total_pages} source pages + "
        f"{total_translations} translation pages){draft_note}."
    )


if __name__ == "__main__":
    main()
