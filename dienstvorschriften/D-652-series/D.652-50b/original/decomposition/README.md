# D 652/50b — canonical decomposition

This folder contains the format-neutral decomposition of the German source.
The original PDF and its file metadata remain one level above. JSON is the
canonical content source; DOCX, PDF, HTML and Markdown are derived outputs.

## Entry points

- `../D.652-50b_de.pdf`: original German scan (59 photographed spreads).
- `document.json`: document identity, languages and canonical references.
- `manifest.json`: complete physical and logical page inventory. **Pending**:
  the printed-page count and `sections` map are not yet populated — the
  PDF-spread-to-book-page pagination inventory (methodology §5, step 3) still
  needs to be done before page splitting begins.
- `index/contents.json`: trilingual table of contents (empty until sections
  are inventoried).
- `glossary/terminology.json`: controlled German → en-GB → es-ES terminology,
  extending the series-shared glossary.
- `layout.json`: output-independent layout profile.
- `frontmatter/` and `sections/`: page-level JSON and visual resources
  (populated during the page-splitting phase).
- `schema/`: JSON contracts. Page-count bounds are provisional (`maximum: 200`)
  until the pagination inventory fixes the true printed-page count.

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
