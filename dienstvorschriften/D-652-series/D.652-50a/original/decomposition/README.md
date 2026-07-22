# D 652/50a — canonical decomposition

This folder contains the format-neutral decomposition of the German source.
The original PDF and its file metadata remain one level above. JSON is the
canonical content source; DOCX, PDF, HTML and Markdown are derived outputs.

## Status: Phase 2 (visual resources) in progress

Per `docs/PDF_TO_CANONICAL_JSON.md` §13:

- [x] Phase 1 — Inventory: source `metadata.json` and `document.json`
      created; original PDF preserved with checksum.
- [~] Phase 2 — Visual resources: base spread images extracted and visually
      reviewed (clean, no watermark compositing). Splitting spreads into
      individual printed book pages and building the explicit PDF-to-page
      map (§5 Step 3) is still pending.
- [ ] Phase 3 — Content model: `manifest.json`, `index/contents.json`,
      per-page `content.json` files.
- [ ] Phase 4 — Linguistic content: transcription and translation.
- [ ] Phase 5 — Consumers: web viewer, DOCX/PDF exporters, search index.

`manifest.json`, `layout.json`, and `index/contents.json` are not yet created
— they require the page-by-page inspection done in Phase 2/3 and must not be
fabricated ahead of that review (see AGENTS.md "Validation").

## Source inventory

- 52 PDF pages, photographed spreads, page size 2762.88 x 2037.12 pt
  (landscape double-page spreads). Unlike D.652-50c, there is no separate
  watermark image object on most pages; a few pages carry a small unrelated
  strip image (e.g. a scanner timestamp) that `extract_spreads.py` correctly
  ignores by selecting the largest-area raster per page.
- `../D.652-50a_de.pdf`: original German scan (Bushmakow restoration
  archive copy).
- `document.json`: document identity, languages and canonical references.
- `glossary/terminology.json`: document-local terminology, extending the
  series-shared glossary at `../../../glossary/terminology.json`.
- `extraction_log.json`: per-page record of the image object selected by
  `scripts/extract_spreads.py` (dimensions, candidate objects considered).

## Observed structure (visual pass over `assets/thumbnails/`, pending exact page-number mapping)

| PDF pages | Content |
|---|---|
| 1 | Front cover, scanned flat (single page) |
| 2 | Spread: blank inside-front-cover (left) + front cover repeated (right) |
| 3 | Spread: Sachverzeichnis (subject index) (left) + first numbered section (right) |
| 3–48 | Technical content spreads: numbered repair-procedure sections ("Ausbau …", "Einbau …") with figures (`Bild NN`); the last few spreads (~44–48) switch to line-drawing spare-parts diagrams/tables |
| 49–51 | Back matter: mostly blank leaves, with page 50 carrying a printed numbered table of contents (Inhaltsverzeichnis) |
| 52 | Back cover, scanned flat, carries a unit ownership stamp ("Pz.-Verf. u. Ers. Abt. 300" or similar — needs closer transcription) |

This table is a navigational aid only, not the canonical page map. Building
`manifest.json` requires reading the printed page number on every spread
(visible in-image, e.g. "— 50 —") to build the explicit map required by §5
Step 3 — do not infer it from a formula.

## Entry points (once populated)

- `manifest.json`: complete physical and logical page inventory.
- `index/contents.json`: trilingual table of contents.
- `layout.json`: output-independent layout profile.
- `frontmatter/` and `sections/`: page-level JSON and visual resources.
- `schema/`: JSON contracts.
