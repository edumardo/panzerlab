# Processing notes — Nm 261/237 (Maybach HL 120 TRM Ersatzteil-Liste)

## Source

15-page PDF, each page a photographed spread of two facing printed pages (no
embedded OCR text, no separate watermark layer — one raster image per PDF
page). Spread widths vary because the cover board, the blank endpapers and the
text-block leaves are not the same physical width; a blind 50/50 split clips
the wider leaves, so each spread's crop fractions were calibrated by visual
inspection rather than assumed uniform (see `scripts/split_spreads.py` for the
explicit per-spread crop map).

## Page map

Printed page numbers are stamped in the corners starting at page 4 (Tafel 1);
pages 1–3 (title, engine photos, table of contents) are unnumbered on paper but
numbered 1–3 here for a contiguous sequence. Body pages 4–21 cover Tafel
(plate) 1–9, each plate spanning one diagram page + one parts-list page.
Trailing blank endpapers and the pencil collector's-inventory annotation are
archived as unnumbered frontmatter assets, not as numbered pages.

| Section | Pages | Tafel | Content |
|---|---|---|---|
| FrontMatter | 1–3 | — | Title, engine photos (Ausf. A/B), Inhaltsverzeichnis |
| A01 | 4–5 | 1 | Brennstoffpumpe, Druckölfilter, Elektrische Apparate |
| A02 | 6–7 | 2 | Kurbelgehäuse |
| A03 | 8–9 | 3 | Kurbelgehäuse (Fortsetzung), Motorlagerung |
| A04 | 10–11 | 4 | Ölbehälter/Ölkühler/Ölpumpen — Ausführung A |
| A05 | 12–13 | 5 | Ölbehälter/Ölkühler/Ölpumpen — Ausführung B |
| A06 | 14–15 | 6 | Saug- und Auspuffrohr mit Vergaser |
| A07 | 16–17 | 7 | Schwingungsdämpfer, Schwungkraft-Anlasser, Triebwerk |
| A08 | 18–19 | 8 | Wasserpumpe mit Antrieb, Zylinderkopf |
| A09 | 20–21 | 9 | Zylinderkopf (Fortsetzung), Zubehörteile und Werkzeuge |

## Status

- FrontMatter (pages 1–3) and A01–A02 (pages 4–7): transcribed and translated
  (en-GB, es-ES), status `validated`. Verified against the source images
  row-by-row (part name, quantity, Maybach part number).
- A03–A09 (pages 8–21): skeleton only. Titles are confirmed from the source
  (diagram-page headings), but `paragraphs`/`figures` are empty and
  `transcription`/translation status is `pending`. The parts-list rows for
  these plates still need transcription in a follow-up pass, following the
  same per-row shape used in A01/A02 (`{id, number, de, en-GB, es-ES,
  quantity, maybach_part_no}`).

## Scripts (run in this order for a from-scratch rebuild)

1. `extract_spreads.py` — pulls the embedded raster image per PDF page into
   `assets/spreads/` + `assets/thumbs/` (never touches the PDF).
2. `split_spreads.py` — crops each spread into the individual printed-page
   `source.jpg` files per the explicit fraction map (recalibrate the map if
   the source PDF is ever re-scanned).
3. `build_skeleton.py` — (re)generates all `manifest.json`/`content.json`
   files from the data tables in the script. Re-run after editing the
   transcription/translation tables for A03–A09.
4. `generate_display_crops.py` — trims scan background into
   `source_display.jpg` for the facsimile export; safe to re-run any time.
5. `validate_original_archive.py` — schema + referential-integrity check.

## Open items

- Full transcription/translation of A03–A09 (roughly 260 more part rows).
- `en/`, `es/`, `bilingual/` exports (DOCX/PDF) once all sections are
  validated — not yet generated.
