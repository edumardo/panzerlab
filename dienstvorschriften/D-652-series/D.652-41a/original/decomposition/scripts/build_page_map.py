"""Build the explicit PDF-sheet -> printed-page map for D 652/41a.

D.652-41a is 65 landscape PDF sheets. Sheets 2-37 are book spreads: each
sheet holds two printed pages (left/right) following printed = 2*sheet-4
(left, even) / 2*sheet-3 (right, odd). Sheet 1 is the unnumbered cover.
Sheets 38-65 each carry ONE full plate that crosses the gutter (never
split) -- this is the verified "G. Bilder" mapping from the processing
notes (28 sheets, 31 plates, 3 rotated doubles on sheets 41/46/58).

This script only *writes* the expanded map; nothing downstream should
re-derive it from a formula or from directory listings (see
docs/PDF_TO_CANONICAL_JSON.md Step 3).
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "page_map.json"

# section_id -> (printed_page_start, printed_page_end) for the text spreads
# (sheets 2-37, printed pages 0-71). Derived from D.652-41a_processing-notes_v1.0.md sec.2/3.
TEXT_SECTIONS = [
    ("FrontMatter", 0, 8, "Titelseite, Inhalt, Vorbemerkungen, A. Technische Angaben, B. Beschreibung §1-2"),
    ("S01", 9, 14, "B. Beschreibung §3-4: Panzerwanne, Motor"),
    ("S02", 15, 23, "B. Beschreibung §5-9: Hauptkupplung, Wechselgetriebe, Kegel-/Lenkgetriebe, Stütz-/Lenkbremse, Kraftübertragung"),
    ("S03", 24, 31, "B. Beschreibung §10-17: Seitenvorgelege, Laufwerk, Gestänge, Elektrik, Schalttafel, Werkzeug, Hilfsgerät, Schanzzeug"),
    ("S04", 32, 45, "C. Schmieren §18-19 + D. Aus-/Einbau §20-24 (Anfang)"),
    ("S05", 46, 62, "D. Aus-/Einbau §24 (Forts.)-28"),
    ("S06", 63, 70, "E. Sondervorschriften §29-30 + F. Fahrvorschrift §31-32 (Seite 70 = leere Rückseite)"),
    ("G", 71, 71, "G. Bilder -- Abschnittstrenner"),
]

# Sheet (pdf page) -> list of Bild numbers, from the verified sheet->Bild table
# in the processing notes (sec.3). "rotated" sheets are scanned/kept as-is.
PLATE_SHEETS = [
    (38, [1], False, "Ansicht des Fahrgestells"),
    (39, [2], False, "Antriebsplan"),
    (40, [3], False, "Kühlanlage"),
    (41, [4, 5], True, "Luftfilter / Kraftstofflagerung u. -förderung"),
    (42, [6], False, "Hauptkupplung"),
    (43, [7], False, "Wechselgetriebe"),
    (44, [8], False, "Lenkgetriebe"),
    (45, [9], False, "Schnitt durch Kegeltrieb"),
    (46, [10, 11], True, "Lenkgetriebe Geradeausfahrt / Lenken"),
    (47, [12], False, "Stützbremse"),
    (48, [13], False, "Lenkbremse"),
    (49, [14], False, "Seitenvorgelege"),
    (50, [15], False, "Triebrad"),
    (51, [16], True, "Leitrad mit Kettenspanner"),
    (52, [17], False, "Laufwerk"),
    (53, [18], True, "Laufwerk"),
    (54, [19], True, "Stoßdämpfer"),
    (55, [20], True, "Schaltplan"),
    (56, [21], False, "Schmier- und Pflegeplan"),
    (57, [22], True, "Schmier- und Pflegeanweisung"),
    (58, [23, 24], True, "Einstellbild Stützbremse / Lenkbremse"),
    (59, [25], False, "Gestänge zur Stütz- und Lenkbremse"),
    (60, [26], False, "Lenkgetriebe m. Stützbremse, Ausbau"),
    (61, [27], False, "Lenkgetriebe m. Stützbremse, Einbau"),
    (62, [28], False, "Lenkgetriebe Einbau; Lenkbremse Aus-/Einbau"),
    (63, [29], True, "Seitenvorgelege, Aus- und Einbau"),
    (64, [30], False, "Laufwerk, Ausbau"),
    (65, [31], False, "Laufwerk, Einbau"),
]


def printed_page_location(n: int) -> tuple[int, str]:
    """Inverse of printed = 2*sheet-4 (left, even n) / 2*sheet-3 (right, odd n)."""
    if n % 2 == 0:
        return (n + 4) // 2, "left"
    return (n + 3) // 2, "right"


def section_for_printed_page(n: int) -> tuple[str, str]:
    for section_id, start, end, title in TEXT_SECTIONS:
        if start <= n <= end:
            return section_id, title
    raise ValueError(f"printed page {n} not covered by TEXT_SECTIONS")


def build() -> dict:
    pages = []

    # Sheet 1: unnumbered cover, kept whole.
    pages.append(
        {
            "printed_page": "cover",
            "section": "FrontMatter",
            "pdf_page": 1,
            "side": "whole",
            "kind": "cover",
        }
    )

    # Sheets 2-37: split spreads, printed pages 0-71.
    for n in range(0, 72):
        pdf_page, side = printed_page_location(n)
        section_id, section_title = section_for_printed_page(n)
        pages.append(
            {
                "printed_page": n,
                "section": section_id,
                "pdf_page": pdf_page,
                "side": side,
                "kind": "blank" if n == 70 else ("divider" if n == 71 else "text"),
            }
        )

    # Sheets 38-65: whole-page plates, section "G", one page per sheet
    # (rotated doubles still get ONE page entry with two Bild numbers).
    for sheet, bild_numbers, rotated, title_de in PLATE_SHEETS:
        pages.append(
            {
                "printed_page": None,
                "section": "G",
                "pdf_page": sheet,
                "side": "whole",
                "kind": "plate",
                "bild_numbers": bild_numbers,
                "rotated": rotated,
                "title_de": title_de,
            }
        )

    # Stable, sequential, document-wide "page" id -- distinct from the
    # printed page number (which is null/na for the cover and for plates).
    # This is the id used for folder names, content.json ids, and
    # previous/next navigation (docs/PDF_TO_CANONICAL_JSON.md sec.7).
    for index, entry in enumerate(pages, start=1):
        entry["page"] = index

    sections = {}
    for section_id, start, end, title in TEXT_SECTIONS:
        sections[section_id] = {"printed_pages": [start, end], "title_de": title}
    sections["G"] = {
        "sheets": [PLATE_SHEETS[0][0], PLATE_SHEETS[-1][0]],
        "bild_range": [1, 31],
        "title_de": "G. Bilder",
    }

    return {
        "document_id": "d652-41a",
        "source_pdf_pages": 65,
        "sections": sections,
        "pages": pages,
    }


def main() -> None:
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} with {len(data['pages'])} page entries")


if __name__ == "__main__":
    main()
