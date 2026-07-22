# D 652/50a — canonical decomposition

This folder contains the format-neutral decomposition of the German source.
The original PDF and its file metadata remain one level above. JSON is the
canonical content source; DOCX, PDF, HTML and Markdown are derived outputs.

## Status: Phase 3 (content model) started

Per `docs/PDF_TO_CANONICAL_JSON.md` §13:

- [x] Phase 1 — Inventory: source `metadata.json` and `document.json`
      created; original PDF preserved with checksum.
- [x] Phase 2 — Visual resources: base spread images extracted and visually
      reviewed (clean, no watermark compositing).
- [~] Phase 3 — Content model: `manifest.json` (explicit PDF-to-page map,
      §5 Step 3) and `index/contents.json` (German chapter titles) are
      populated from direct visual reading of every spread's printed folio
      number and chapter heading. Splitting spreads into individual page
      image files and writing per-page `content.json` (paragraph-level
      transcription) is still pending.
- [ ] Phase 4 — Linguistic content: transcription and translation.
- [ ] Phase 5 — Consumers: web viewer, DOCX/PDF exporters, search index.

## PDF-to-book-page map (§5 Step 3)

`pdf_page` 1 (the front cover, scanned flat) is not part of the paginated
manifest — its content duplicates the right-hand side of `pdf_page` 2's
spread and is kept only as an asset for provenance, following the same
convention D.652-50c uses for its own redundant opening scan.

For every other `pdf_page`, both spread halves were read directly (not
inferred from a formula) to confirm the printed folio number in each
page's masthead:

- `pdf_page` 2 → archive pages 1–2 (blank inside-cover + duplicated cover/title, unnumbered)
- `pdf_page` 3 → archive pages 3–4 (printed "4" Vorbemerkungen, printed "5" start of chapter 1)
- `pdf_page` N for N = 3..51 → archive pages (2N-3) left, (2N-2) right, which equals printed folio (archive_page + 1)
- `pdf_page` 52 (back cover, scanned flat, unit stamp) → archive page 101

This was spot-verified across the full range (pages 3, 4, 5, 6, 7, 8, 9, 10,
11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
49, 50, 51 — i.e. every content spread) with 100% consistency; see
`manifest.json` for the expanded per-page result.

## Chapters (33 numbered repair procedures + front/back matter)

`index/contents.json` lists all 33 numbered chapters ("Ausbau"/"Einbau" —
removal/installation — pairs for each running-gear component, then
"Sonderwerkzeuge" §32 with its `Zeichnung` spare-parts drawings, then an
"Arbeitszeiten" §33 repair-time table). Two chapter headings (§19 and §27)
were not located in the top-of-page region read for every spread — they
likely start mid-page on an already-identified archive page and need a
direct look at the full page (not just its masthead) during the page-split
step; they are marked `"status": "pending"` in `index/contents.json` rather
than guessed.

## Source inventory

- 52 PDF pages, photographed spreads, page size 2762.88 x 2037.12 pt
  (landscape double-page spreads). Unlike D.652-50c, there is no separate
  watermark image object on most pages; a few pages carry a small unrelated
  strip image (e.g. a scanner timestamp) that `extract_spreads.py` correctly
  ignores by selecting the largest-area raster per page.
- `../D.652-50a_de.pdf`: original German scan (Bushmakow restoration
  archive copy).
- `document.json`: document identity, languages and canonical references.
- `manifest.json`: complete physical and logical page inventory (see above).
- `index/contents.json`: German chapter titles (EN/ES translation pending).
- `glossary/terminology.json`: document-local terminology, extending the
  series-shared glossary at `../../../glossary/terminology.json`.
- `extraction_log.json`: per-page record of the image object selected by
  `scripts/extract_spreads.py` (dimensions, candidate objects considered).

Back matter (archive pages 96–99) is an "Arbeitszeiten" (repair-time) table
listing each job with its duration in minutes — not a table of contents;
archive pages 100–101 are blank trailing leaves before the back cover.

## Entry points (still pending)

- `layout.json`: output-independent layout profile.
- Per-page split images (`sections/<id>/pages/<NNN>/source.jpg`) and
  per-page `content.json` (paragraph-level transcription) — currently only
  the shared full-spread images in `assets/spreads/` exist.
- `schema/`: JSON contracts (page and content schemas added this pass;
  page-level `content.json` files that conform to them are not yet
  written).
