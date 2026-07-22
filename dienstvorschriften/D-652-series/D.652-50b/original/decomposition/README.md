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
  Per-page `source_scan_status`/`transcription_status`/etc. are all
  `pending` — the page-splitting phase (methodology §5, step 4: cropping
  `source.jpg` per page and writing `content.json`) has not started yet.
- `index/contents.json`: trilingual table of contents, one group (`A`,
  "power train repair") with 22 sections (`A01`–`A22`).
- `glossary/terminology.json`: controlled German → en-GB → es-ES terminology,
  extending the series-shared glossary.
- `layout.json`: output-independent layout profile.
- `frontmatter/` (pages 1–4) and `sections/A01`–`A22/` (pages 5–112): each
  has a section-level `manifest.json` (title, page range, export layout).
  Per-page directories (`pages/<NNN>/`) are not yet created.
- `assets/spreads/` and `assets/thumbs/`: the 59 clean base spreads extracted
  from the PDF via `scripts/extract_spreads.py`, plus their extraction
  manifest (`assets/extraction_001_059.json`). Cropping these into individual
  `source.jpg` files per page is the next step.
- `schema/`: JSON contracts, with page-count bounds fixed to 1–112.

Each numbered page will contain:

```text
pages/NNN/
├── manifest.json
├── content.json
├── source.jpg
└── figures/
```

`validated` content may be published. `pending`, `draft` and `candidate_crop`
must be reviewed first. The scripts in `scripts/` provide extraction,
contact-sheet generation and structural validation, adapted from
`D.652-50c/original/decomposition/scripts/`.
