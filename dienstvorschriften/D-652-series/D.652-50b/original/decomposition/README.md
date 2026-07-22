# D 652/50b — canonical decomposition

This folder contains the format-neutral decomposition of the German source.
The original PDF and its file metadata remain one level above. JSON is the
canonical content source; DOCX, PDF, HTML and Markdown are derived outputs.

## Entry points

- `../D.652-50b_de.pdf`: original German scan (59 photographed spreads).
- `document.json`: document identity, languages and canonical references.
- `manifest.json`: complete physical and logical page inventory. The book has
  112 numbered printed pages (plus unnumbered covers/flyleaves); the
  PDF-spread-to-book-page map and `sections` ranges are recorded here.
  `source_scan_status` is `extracted_clean` for all 112 pages (physical
  splitting is done); `transcription_status`/`translation_en_status`/
  `translation_es_status` are all `pending` — transcription and translation
  (methodology §5, steps 6–7) have not started yet.
- `index/contents.json`: trilingual table of contents, one group (`A`,
  "power train repair") with 22 sections (`A01`–`A22`).
- `glossary/terminology.json`: controlled German → en-GB → es-ES terminology,
  extending the series-shared glossary.
- `layout.json`: output-independent layout profile.
- `frontmatter/` (pages 1–4) and `sections/A01`–`A22/` (pages 5–112): each
  has a section-level `manifest.json` (title, page range, export layout) and
  a `pages/<NNN>/` directory per page with `manifest.json`, `content.json`
  and `source.jpg`. Paragraph text, figures and translations are still empty
  (`content.json` stubs, `type` classified visually as `text`/`figures`/
  `index`/`blank` but not yet transcribed).
- `assets/spreads/` and `assets/thumbs/`: the 59 clean base spreads extracted
  from the PDF via `scripts/extract_spreads.py`, plus their extraction
  manifest (`assets/extraction_001_059.json`).
- `schema/`: JSON contracts, with page-count bounds fixed to 1–112.

Each numbered page contains:

```text
pages/NNN/
├── manifest.json
├── content.json
├── source.jpg
└── figures/
```

Per-page `source.jpg` files were cropped from their spread with a single
fixed crop box (`scripts/split_book_pages.py`), calibrated by visual
inspection since the camera rig was fixed for the whole shoot; one spread
(page 1's, spread 002) was captured at ~4.17x higher resolution and the box
is scaled accordingly. Minor background slivers/skew may remain — refine
later with `generate_display_crops.py` (produces `source_display.jpg`,
never touches `source.jpg`).

`validated` content may be published. `pending`, `draft` and `candidate_crop`
must be reviewed first. The scripts in `scripts/` provide extraction, page
splitting, contact-sheet generation and structural validation, adapted from
`D.652-50c/original/decomposition/scripts/`.
