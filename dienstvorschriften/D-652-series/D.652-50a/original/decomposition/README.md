# D 652/50a — canonical decomposition

This folder contains the format-neutral decomposition of the German source.
The original PDF and its file metadata remain one level above. JSON is the
canonical content source; DOCX, PDF, HTML and Markdown are derived outputs.

## Status: Phase 1 (inventory) complete, Phase 2+ pending

Per `docs/PDF_TO_CANONICAL_JSON.md` §13:

- [x] Phase 1 — Inventory: source `metadata.json` and `document.json`
      created; original PDF preserved with checksum.
- [ ] Phase 2 — Visual resources: extract base images, split printed pages,
      generate thumbnails and figure crop candidates.
- [ ] Phase 3 — Content model: `manifest.json`, `index/contents.json`,
      per-page `content.json` files.
- [ ] Phase 4 — Linguistic content: transcription and translation.
- [ ] Phase 5 — Consumers: web viewer, DOCX/PDF exporters, search index.

`manifest.json`, `layout.json`, and `index/contents.json` are not yet created
— they require the page-by-page inspection done in Phase 2/3 and must not be
fabricated ahead of that review (see AGENTS.md "Validation").

## Source inventory

- 52 PDF pages, photographed spreads, page size 2762.88 x 2037.12 pt
  (landscape double-page spreads).
- `../D.652-50a_de.pdf`: original German scan (Bushmakow restoration
  archive copy).
- `document.json`: document identity, languages and canonical references.
- `glossary/terminology.json`: document-local terminology, extending the
  series-shared glossary at `../../../glossary/terminology.json`.

## Entry points (once populated)

- `manifest.json`: complete physical and logical page inventory.
- `index/contents.json`: trilingual table of contents.
- `layout.json`: output-independent layout profile.
- `frontmatter/` and `sections/`: page-level JSON and visual resources.
- `schema/`: JSON contracts.
