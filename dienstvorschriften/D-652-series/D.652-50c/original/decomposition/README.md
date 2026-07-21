# D 652/50c — canonical decomposition

This folder contains the format-neutral decomposition of the German source.
The original PDF and its file metadata remain one level above. JSON is the
canonical content source; DOCX, PDF, HTML and Markdown are derived outputs.

## Entry points

- `../D.652-50c_de.pdf`: original German scan.
- `document.json`: document identity, languages and canonical references.
- `manifest.json`: complete physical and logical page inventory.
- `index/contents.json`: trilingual table of contents.
- `glossary/terminology.json`: controlled German → en-GB → es-ES terminology.
- `layout.json`: output-independent layout profile.
- `frontmatter/` and `sections/`: page-level JSON and visual resources.
- `schema/`: JSON contracts.

Each numbered page contains:

```text
pages/NNN/
├── manifest.json
├── content.json
├── source.jpg
└── figures/
```

`validated` content may be published. `pending`, `draft` and `candidate_crop`
must be reviewed first. The scripts in `scripts/` provide extraction,
contact-sheet generation and structural validation.
