# D 652/41a — canonical decomposition

This folder contains the format-neutral decomposition of the German source.
The original PDF and its file metadata remain one level above. JSON is the
canonical content source; DOCX, PDF, HTML and Markdown are derived outputs.

The source PDF is 65 landscape sheets. Sheet 1 is the unnumbered cover;
sheets 2-37 are book spreads (two printed pages per sheet, split left/right);
sheets 38-65 each carry one whole plate (`Bild 1`-`31`, three sheets rotated
with two plates each) that crosses the gutter and is kept whole. See
`scripts/build_page_map.py` for the exact, explicit page map (never re-derive
it from the split formula or from directory listings).

## Entry points

- `../D.652-41a_de.pdf`: original German scan.
- `document.json`: document identity, languages and canonical references.
- `manifest.json`: complete physical and logical page inventory (101 pages).
- `page_map.json`: the expanded PDF-sheet -> printed-page map (source of
  truth for `build_manifests.py`/`build_index.py`/`split_pages.py`).
- `index/contents.json`: table of contents (text-section blocks + the full
  Bild 1-31 plate list).
- `glossary/terminology.json`: document-specific terms; extends the
  series-shared glossary at `../../../../glossary/terminology.json`.
- `layout.json`: output-independent layout profiles (portrait text pages,
  landscape plates).
- `frontmatter/` and `sections/`: page-level JSON and visual resources.
  Front matter lives at the top-level `frontmatter/`, not
  `sections/FrontMatter/`.
- `schema/`: JSON contracts.

Each numbered page contains:

```text
pages/NNN/
├── manifest.json
├── content.json
└── source.jpg
```

`validated` content may be published. `pending`, `draft` and `candidate_crop`
must be reviewed first.

## Current state

All 101 pages are split, imaged, transcribed, translated into en-GB and
es-ES, and marked `validated`, as are the document's 169 glossary terms and
its 31 figures (numbered 1-31, no gaps). The canonical compiled output is
`../../bilingual/D.652-41a_bilingual_full_v1.0.pdf`. The earlier `en/` and
`es/` deliverables described in `../D.652-41a_processing-notes_v1.0.md` came
from a separate build pipeline and were removed when this document moved to a
bilingual-only export; they remain in git history.

### Known defects accepted at validation

The source scans lose a few millimetres at the outer edge on some pages, so a
small amount of ink is cut in the original images themselves, not in the
export. It is most visible on the fold-out plates: on book page 74 (Bild 1)
the labels "Bild 1" and "Leitrad" are clipped at the right, and page 75
(Bild 2) loses part of "Seitenwelle", "Vorgelege" and "Kegeltrieb" at the
left. Pages 54, 56, 70, 92 and 93 show ink reaching the right edge too. The
affected words are all recoverable from the transcription, which is complete,
so the pages were validated as they stand. Re-extracting them from a wider
scan would be the fix if a better source ever turns up; do not crop or
in-paint the existing archival images.

## Regenerating

Idempotent; re-running only touches the files each script states it owns.

```bash
# run from original/decomposition/
python3 scripts/build_page_map.py                          # -> page_map.json (the explicit map)
python3 scripts/extract_spreads.py ../D.652-41a_de.pdf assets   # -> assets/spreads, assets/thumbs
python3 scripts/split_pages.py                              # -> frontmatter|sections/*/pages/NNN/source.jpg
python3 scripts/build_manifests.py                          # -> manifest.json + section/page manifests + content.json stubs
python3 scripts/build_index.py                              # -> index/contents.json
python3 scripts/validate_original_archive.py
```

Compiled bilingual output (needs `reportlab` and `pillow`):

```bash
# run from original/decomposition/scripts/
python3 export_full_document.py --output ../../../bilingual/D.652-41a_bilingual_full_v1.0.pdf
```

It refuses to run unless every page is `validated`; `--allow-draft` overrides
that for previews only and must not produce a committed export.

