# D 652/50a — canonical decomposition

This folder contains the format-neutral decomposition of the German source.
The original PDF and its file metadata remain one level above. JSON is the
canonical content source; DOCX, PDF, HTML and Markdown are derived outputs.

## Status: Phase 4 (transcription) done in German; translation pending

Per `docs/PDF_TO_CANONICAL_JSON.md` §13:

- [x] Phase 1 — Inventory: source `metadata.json` and `document.json`
      created; original PDF preserved with checksum.
- [x] Phase 2 — Visual resources: base spread images extracted and visually
      reviewed (clean, no watermark compositing).
- [x] Phase 3 — Content model: `manifest.json` (explicit PDF-to-page map,
      §5 Step 3), `index/contents.json` (German chapter titles, all 33
      confirmed — see below), per-section `manifest.json` files (facsimile
      layout), and all 101 pages split from their spreads into individual
      `source.jpg` files.
- [~] Phase 4 — Linguistic content: all 101 pages have a `content.json` with
      a direct-from-image German transcription (paragraphs, titles, figure
      captions), `status.transcription: "draft"` — visually spot-checked
      against the source scans but not yet human-reviewed page by page, so
      not promoted to `"validated"`. EN/ES translation has not started
      (`status.en-GB`/`status.es-ES: "pending"`, `titles.en-GB`/`es-ES` and
      all paragraph/caption `en-GB`/`es-ES` fields are `null`).
- [ ] Phase 5 — Consumers: web viewer, DOCX/PDF exporters, search index.

### Known editorial inconsistency to resolve before validating

Different transcription passes split figure captions vs. body paragraphs
slightly differently: some pages (e.g. `sections/A03/pages/010`,
`sections/A06/pages/019`) put the full descriptive sentence into the
figure's `captions` field, while others (e.g. `sections/A13/pages/046`-`048`)
leave captions as a bare "Bild NN" and move all descriptive text into
`paragraphs`. Both are valid against `schema/content.schema.json`, but this
should be normalized to one convention during human review, before any page
is promoted from `"draft"` to `"validated"`.

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
"Arbeitszeiten" §33 repair-time table). Chapters §19 ("Anbau der
Stützrolle") and §27 ("Einbau der Scherscheibe an dem Kettenspanner älterer
Ausführung") were not on any spread's top-of-page masthead because both
start mid-page, sharing an archive page with the previous chapter (57 and
72 respectively) — found during page-by-page transcription and confirmed
against the source scan; no separate A19/A27 section directories exist.

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

- `layout.json`: a document-level (not per-section) output-independent
  layout profile, if one is needed beyond each section's own
  `manifest.json.layout`.
- EN/ES translation of every `titles`/paragraph/caption field.
- Human review promoting `status.transcription` from `"draft"` to
  `"validated"` page by page (after resolving the caption/paragraph
  convention noted above).
