# Decomposing a PDF into a reusable canonical JSON archive

## 1. Purpose

This guide describes how to transform a scanned PDF into a neutral, versionable
document source that can later feed a web viewer, DOCX exporter, PDF exporter,
search index, or another publishing system.

The archive must make it possible to:

- preserve the received source and its provenance;
- navigate by document, section, printed page, paragraph, and figure;
- display the source scan beside the original transcription or a translation;
- add languages without changing visual assets;
- generate individual sections or a complete publication;
- distinguish automatic, reviewed, and publishable content;
- regenerate every derived format from the same data.

The governing rule is:

> **JSON is canonical. DOCX, PDF, HTML, Markdown, databases, and search indexes
> are derived outputs.**

---

## 2. Repository placement

The archive belongs inside the directory of the document to which it applies.
It is independent of a particular D-series number or document category.

```text
<category>/
└── <series>/
    ├── glossary/
    │   └── terminology.json
    └── <document-id>/
        ├── metadata.md
        ├── original/
        │   ├── <document-id>_de.pdf
        │   ├── metadata.json
        │   └── decomposition/
        │       ├── document.json
        │       ├── manifest.json
        │       ├── layout.json
        │       ├── README.md
        │       ├── assets/
        │       │   ├── spreads/
        │       │   └── thumbnails/
        │       ├── frontmatter/
        │       ├── index/
        │       │   └── contents.json
        │       ├── glossary/
        │       │   └── terminology.json
        │       ├── sections/
        │       │   ├── A01/
        │       │   │   ├── manifest.json
        │       │   │   └── pages/
        │       │   │       └── 005/
        │       │   │           ├── manifest.json
        │       │   │           ├── content.json
        │       │   │           ├── source.jpg
        │       │   │           └── figures/
        │       │   └── B02/
        │       ├── schema/
        │       │   ├── page.schema.json
        │       │   └── content.schema.json
        │       └── scripts/
        ├── en/
        └── es/
```

The top level of `original/` stays deliberately small. Everything created while
decomposing the source lives under `original/decomposition/`.

---

## 3. Canonical entry points

### 3.1 Source `metadata.json`

This file describes the received source, not its reconstructed content.

```json
{
  "schema_version": 1,
  "document_id": "manual-001",
  "designation": "ABC 123",
  "file": "ABC.123_de.pdf",
  "original_file_name": "scan-as-received.pdf",
  "language": "de-DE",
  "media_type": "application/pdf",
  "size_bytes": 64310217,
  "sha256": "...",
  "pdf_pages": 75,
  "page_layout": "photographed spreads",
  "decomposition": "decomposition/document.json",
  "source": {
    "description": "Archive or collection description",
    "url": "https://example.org/source"
  }
}
```

Record the checksum before processing. It establishes which exact source file
was decomposed.

### 3.2 `document.json`

This is the entry point for all consumers of the decomposition.

```json
{
  "schema_version": 1,
  "id": "manual-001",
  "code": "ABC 123",
  "titles": {
    "de": "Originaltitel",
    "en-GB": "English title",
    "es-ES": "Título en español"
  },
  "original_date": "1943-11-03",
  "source_language": "de-DE",
  "target_languages": ["en-GB", "es-ES"],
  "source_pdf": "../ABC.123_de.pdf",
  "manifest": "manifest.json",
  "index": "index/contents.json",
  "glossary": "glossary/terminology.json",
  "layout": "layout.json"
}
```

Use explicit BCP 47 language tags. Prefer `en-GB` to `en` and `es-ES` to `es`.

### 3.3 Global `manifest.json`

The global manifest declares physical and logical order.

```json
{
  "document_id": "manual-001",
  "source_pdf_pages": 75,
  "book_pages": [1, 143],
  "sections": {
    "A01": [5, 7],
    "A02": [8, 12]
  },
  "pages": [
    {
      "page": 5,
      "section": "A01",
      "pdf_page": 4,
      "side": "right",
      "content": "content.json"
    }
  ]
}
```

Never infer order from filesystem enumeration. Store it explicitly.

### 3.4 Section manifest

```json
{
  "id": "A01",
  "pages": [5, 6, 7],
  "titles": {
    "de": "Titel des Abschnitts",
    "en-GB": "Section title",
    "es-ES": "Título de la sección"
  },
  "output": {
    "cover": false,
    "header": false,
    "footer": false
  },
  "layout": "A4_portrait_source_left_translation_right_or_two_figures"
}
```

`layout` selects the section's export mode. Two values are in use:

- `A4_portrait_source_left_translation_right_or_two_figures`: the original
  per-figure-crop export (source text/paragraphs alongside up to two figure
  crops per page).
- `A4_portrait_facsimile_then_translation`: each source page is exported as a
  full facsimile page followed by a translation page listing that page's
  title and figure captions (see §9 and
  `original/decomposition/scripts/export_facsimile_pdf.py`). Adopt this value
  when a section drops per-figure crops in favour of full-page facsimiles.
- `A4_landscape_facsimile_then_translation`: the same facsimile-then-
  translation export, but for a source page that is itself a landscape sheet
  crossing the gutter (a wide plate/drawing spanning two book pages) and must
  therefore never be split into left/right halves. Introduced for D.652-41a's
  plate section (`G`), where one sheet can carry one or two `Bild` numbers;
  the translation page lists captions and label keys for every `Bild` on
  that sheet.

### 3.5 Page manifest

The page manifest stores provenance and workflow state. Linguistic content
belongs in `content.json`.

```json
{
  "page": 5,
  "section": "A01",
  "pdf_page": 4,
  "side": "right",
  "source_scan": "source.jpg",
  "content": "content.json",
  "source_scan_status": "extracted_clean",
  "transcription_status": "validated",
  "translation_en_status": "validated",
  "translation_es_status": "draft",
  "figures": [
    {
      "number": 1,
      "path": "figures/fig001.jpg",
      "status": "validated"
    }
  ],
  "display_scan": "source_display.jpg",
  "display_scan_crop_box_px": [120, 84, 1348, 2015]
}
```

`display_scan` and `display_scan_crop_box_px` are optional — present only when
Step 4b generated a trimmed display copy of `source.jpg`.

### 3.6 Page `content.json`

This is the main unit consumed by web, DOCX, and PDF exporters.

```json
{
  "schema_version": 1,
  "id": "manual001-page-005",
  "document_id": "manual-001",
  "page": 5,
  "section": "A01",
  "type": "text",
  "titles": {
    "de": "1. Originaltitel",
    "en-GB": "Section A.1 - English title",
    "es-ES": "Sección A.1 - Título español"
  },
  "source": {
    "image": "source.jpg",
    "pdf_page": 4,
    "side": "right",
    "status": "extracted_clean",
    "display_image": "source_display.jpg"
  },
  "navigation": {
    "previous": "manual001-page-004",
    "next": "manual001-page-006"
  },
  "paragraphs": [
    {
      "id": "manual001-p005-para01",
      "text": {
        "de": {
          "plain": "Original text.",
          "runs": [{"text": "Original text.", "bold": false}]
        },
        "en-GB": {
          "plain": "Translated text, Fig. 1.",
          "runs": [
            {"text": "Translated text, ", "bold": false},
            {"text": "Fig. 1", "bold": true},
            {"text": ".", "bold": false}
          ]
        },
        "es-ES": null
      }
    }
  ],
  "figures": [],
  "status": {
    "transcription": "validated",
    "en-GB": "validated",
    "es-ES": "pending",
    "figures": "not_applicable"
  }
}
```

Keep all language versions of a paragraph in the same object. Parallel arrays
drift easily and make side-by-side display unreliable.

A page whose `type` is `"index"` (a printed table of contents, list of
figures, etc.) still needs real `titles` and `paragraphs` transcribing what is
printed on that page, the same as a `"text"` page — even when a separate
structured file (such as `index/contents.json`) also holds the same
information for navigation. The structured file and the page's own
transcription serve different purposes (machine-readable navigation vs. an
accurate record of the printed page) and neither substitutes for the other. Do
not mark `status.transcription`/`status.en-GB`/`status.es-ES` as `validated`
while `titles` is null and `paragraphs` is empty — that combination means the
page was never actually transcribed, regardless of what the status fields say.

### 3.7 Figure objects

```json
{
  "id": "manual001-bild-001",
  "number": 1,
  "image": "figures/fig001.jpg",
  "status": "validated",
  "captions": {
    "de": {"plain": "Original caption.", "runs": []},
    "en-GB": {"plain": "Translated caption.", "runs": []},
    "es-ES": {"plain": "Pie traducido.", "runs": []}
  },
  "label_keys": {
    "de": null,
    "en-GB": {"plain": "1 = master switch", "runs": []},
    "es-ES": {"plain": "1 = interruptor principal", "runs": []}
  }
}
```

Store label keys separately from captions. A web viewer can then show, hide, or
turn them into interactive annotations.

### 3.8 Terminology glossary

A document's own glossary holds only terms specific to its subject matter:

```json
{
  "schema_version": 1,
  "document_id": "manual-001",
  "source_language": "de-DE",
  "target_languages": ["en-GB", "es-ES"],
  "extends": "../../../../glossary/terminology.json",
  "terms": [
    {
      "id": "term-001",
      "de": "Kühler",
      "en-GB": "radiator",
      "es-ES": "radiador",
      "status": "validated"
    }
  ]
}
```

`extends` is optional and points at the series-shared glossary (§2), if the
series has one. Prefer adding a new term there over the document glossary when
it is generic vehicle/tool/component vocabulary rather than specific to this
document's subject.

The series-shared glossary uses the same term shape, with no `document_id`,
an id prefix of `series-term-NNN` to avoid colliding with document-local
`term-NNN` ids, and a scope marker:

```json
{
  "schema_version": 1,
  "scope": "series",
  "series_id": "D-652",
  "source_language": "de-DE",
  "target_languages": ["en-GB", "es-ES"],
  "terms": [
    {
      "id": "series-term-001",
      "de": "Heckpanzerung",
      "en-GB": "rear armour plate",
      "es-ES": "blindaje trasero",
      "status": "validated"
    }
  ]
}
```

A consumer (exporter, web viewer, translator reference) that needs the full
glossary for a document reads the document's own `terms` plus, when `extends`
is present, the series glossary's `terms` — the two lists never share an id
range, so they can simply be concatenated.

---

## 4. Workflow states

Use a closed vocabulary:

- `pending`: not started;
- `draft`: automatically generated or transcribed but not reviewed;
- `reviewed`: checked once but not approved for publication;
- `validated`: approved for publication;
- `candidate_crop`: automatic image crop awaiting visual review;
- `not_applicable`: the field does not apply to this page.

Production exporters must fail when required content is `pending`, `draft`, or
`candidate_crop`.

---

## 5. End-to-end workflow

### Step 1. Inventory the PDF

Record before extraction:

- PDF page count;
- page dimensions and orientation;
- embedded text availability;
- single pages versus photographed spreads;
- approximate scan resolution;
- forms, layers, transparency, and watermarks;
- relationship between PDF pages and printed page numbers.

Useful commands:

```bash
pdfinfo original/<document>_de.pdf
pdffonts original/<document>_de.pdf
pdfimages -list original/<document>_de.pdf
```

Use `pypdf` or `pdfplumber` for structural inspection, but never as a substitute
for visual review.

### Step 2. Extract the cleanest available image

There are two main cases.

#### Embedded base images

If the PDF stores each scan as a separate image object, extract that object with
`pdfimages` or `pypdf`. This avoids recompositing watermarks, text overlays, or
other PDF furniture.

#### Composited PDF pages

If no usable base image exists, render the page with Poppler:

```bash
pdftoppm -jpeg -r 300 original/<document>_de.pdf tmp/page
```

Do not assume that the largest image object is always correct. Review samples
from the beginning, middle, and end of the document.

### Step 3. Build an explicit page map

Represent the PDF-to-book relationship as data:

```json
{
  "pdf_page": 4,
  "left_book_page": 4,
  "right_book_page": 5,
  "rotation": 0
}
```

A formula may help generate the map, but store the expanded result. Covers,
blank pages, fold-outs, duplicates, and missing pages often break formulas.

### Step 4. Split printed pages

Save each printed page in its final location:

```text
sections/A01/pages/005/source.jpg
```

Express crop boxes as normalised fractions of width and height, not only as
pixels. Normalised boxes survive changes in scan resolution.

Record:

- source PDF page or spread;
- left/right side;
- normalised crop rectangle;
- applied rotation;
- final dimensions;
- optional SHA-256 checksum.

### Step 4b. Generate a display crop (optional)

Raw scans can include stray scan-bed background (marble, cloth, sticky tabs)
bleeding in around the printed page. When this happens, generate a derived
`source_display.jpg` next to `source.jpg` that trims this background for
display, without ever overwriting or replacing `source.jpg` itself:

```text
sections/A03/pages/008/source.jpg           # untouched archival scan
sections/A03/pages/008/source_display.jpg   # derived, regenerable crop
```

Record `display_scan` (page manifest) and `source.display_image`
(`content.json`) pointing at the derived file, plus the pixel crop box used, so
the crop is reproducible if the crop heuristic or the scan is redone. A script
that performs this step must be idempotent and must state that it only ever
writes the derived file and its own metadata fields, never `source.jpg`. See
`original/decomposition/scripts/generate_display_crops.py` for the reference
implementation (a warm-paper vs. cool-background heuristic scanning inward
from each edge).

### Step 5. Detect and crop figures (per-section, see 3.4 `layout`)

Sections whose manifest `layout` is
`A4_portrait_source_left_translation_right_or_two_figures` still need
individual figure crops:

Create automatic crops as candidates first. Do not validate them until checking:

- the entire figure is present;
- headers and printed captions are excluded when appropriate;
- original figure numbering is correct;
- orientation is correct;
- callouts and labels remain legible.

For plates and tables, preserve a complete page image even when smaller details
are also cropped.

Sections whose manifest `layout` is `A4_portrait_facsimile_then_translation`
skip this step: the exported facsimile page already shows the complete
original page, so per-figure crop files are optional archival extras rather
than a rendering requirement. Figure objects still carry their `number` and
translated `captions`/`label_keys` — those remain canonical content consumed
by the translation page — but `figures[].image`/`figures[].path` may be
omitted.

### Step 6. Transcribe the source language

OCR is a draft, never a validation. Visual transcription must preserve:

- original spelling and punctuation;
- umlauts, accents, and special characters;
- numbers, measurements, and figure references;
- real paragraph boundaries;
- headings and continuation headings;
- captions, labels, and table contents.

Remove hyphens caused only by line wrapping unless they are part of the original
word.

### Step 7. Translate

- Translate directly from the source language.
- Declare the exact language variant.
- Reuse the controlled glossary.
- Align translations at paragraph or block level.
- Preserve the original technical term in parentheses when useful.
- Validate each language independently.

### Step 8. Validate the archive

At minimum, check:

- valid JSON;
- schema conformance;
- all referenced paths exist;
- pages are consecutive or documented;
- IDs are unique;
- previous/next navigation is coherent;
- figure numbering has no unexplained gaps or duplicates;
- every validated object contains the declared languages;
- no pending content is included in a production export;
- pages and figures pass visual contact-sheet review.

### Step 9. Generate derived outputs

Exporters must read only:

1. `document.json`;
2. global, section, and page manifests;
3. page `content.json` files;
4. referenced images;
5. the glossary and layout profile.

They must not reopen the PDF or parse Markdown during publication.

---

## 6. Image formats

### JPEG

Use JPEG for photographs and historical scans. If the PDF already contains a
JPEG, preserve the original encoded stream when possible.

### PNG

Use PNG for:

- digitally generated diagrams with flat colours;
- screenshots;
- sharp line art;
- transparency;
- digitally generated tables.

Converting an existing JPEG photograph to PNG does not restore detail and often
increases its size by four to eight times.

### WebP and AVIF

Treat WebP and AVIF as publication derivatives rather than canonical originals:

```text
source.jpg
generated/800.webp
generated/1600.webp
```

The canonical JSON may reference `source.jpg`; the frontend can select a derived
resource with `srcset` or an image service.

---

## 7. Stable IDs and web routes

IDs must not depend on translated titles:

```text
document:  manual-001
section:   manual-001-A01
page:      manual001-page-005
figure:    manual001-bild-001
paragraph: manual001-p005-para01
```

This supports stable routes:

```text
/documents/manual-001/A01/005
/documents/manual-001/figures/001
```

Titles may change without breaking links.

---

## 8. Web viewer architecture

A static viewer can load `document.json` and follow its references:

```text
document.json
├── index/contents.json
├── manifest.json
├── glossary/terminology.json
└── section → page → content.json
```

Natural features include:

- language selector;
- source and translation side by side;
- previous/next page navigation;
- section tree and thumbnails;
- scan and figure zoom;
- search over `plain` fields;
- caption and label-key display;
- validation-state filters;
- permanent links to pages, paragraphs, and figures.

For a small collection, serve JSON as static assets. For a large collection, a
build step may aggregate it into SQLite, PostgreSQL, or a search index without
changing the canonical source.

---

## 9. DOCX and PDF export

An exporter receives:

```text
document_id + section/range + language + layout profile
```

Conceptual commands:

```bash
export-docx manual-001 --section A01 --language es-ES
export-pdf manual-001 --from A01 --to B31 --language en-GB
```

The exporter must:

1. validate workflow states;
2. order pages from the manifest;
3. select the requested language;
4. convert formatting runs into target-format runs;
5. insert scans, figures, captions, and label keys;
6. apply `layout.json`;
7. render the result;
8. visually inspect every rendered page.

For A4 figure pages containing two vertically arranged figures, the exporter
must preserve each source image's aspect ratio and embedded raster pixels. Aim
for a rendered width of 120-135 mm (132 mm by default), which is close to the
printed size in the source manual. Use the full space available in each
half-page cell and reduce a figure only when its caption or label key would
otherwise leave the cell, overlap adjacent content, or cross the page margins.
Long captions take priority over the preferred image width. Do not impose one
small fixed height on every figure, and never stretch an image independently in
one dimension.

Generate the final PDF from canonical content or from an already validated DOCX,
not from a separate reconstruction.

### 9.1 Facsimile-then-translation export mode

For sections with `layout: "A4_portrait_facsimile_then_translation"`, the
exporter instead:

1. renders the full page image (`source.display_image` when present, else
   `source.image`), scaled to fill the page while preserving aspect ratio, with
   no per-figure splitting;
2. follows it with a translation page listing that page's title and every
   figure's caption, one language block per target language (bilingual — all
   requested languages together, not one exported file per language).

Because this mode shows the untouched original page directly, per-figure crop
files are not required to produce it (see §5 Step 5). Bilingual output does not
belong under a single-language `en/` or `es/` directory; save it under
`bilingual/` (see AGENTS.md naming conventions). Reference implementation:
`original/decomposition/scripts/export_facsimile_pdf.py`.

---

## 10. Version control and large files

PDFs and scans may require Git LFS:

```gitattributes
*.pdf filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
```

Decide on LFS deliberately. It affects storage, bandwidth, and contributor
setup. Document-scoped rules may be preferable to repository-wide rules.

Do not commit regenerable files:

```gitignore
tmp/
output/
**/validation/
**/generated/
```

For very large collections, store source images in object storage and version
their checksums and URLs instead.

---

## 11. Recommended scripts

Keep responsibilities separate:

```text
scripts/
├── inspect_pdf.py
├── extract_base_images.py
├── split_book_pages.py
├── crop_figure_candidates.py
├── build_manifests.py
├── import_ocr_drafts.py
├── validate_archive.py
├── export_docx.js
├── export_pdf.py
└── build_web.ts
```

Scripts should be idempotent where practical and must state what they
overwrite. Never overwrite validated content with automated output.

---

## 12. Common mistakes

- Using filenames as the only IDs.
- Embedding HTML or Word styling in canonical content.
- Storing translations in independent, unaligned arrays.
- Treating OCR as validated transcription.
- Overwriting reviewed content during regeneration.
- Using absolute local image paths.
- Publishing candidate crops.
- Converting every scan to PNG.
- Inferring order from the filesystem.
- Maintaining separate data models for web, DOCX, and PDF.
- Correcting only the final DOCX or PDF.

Every correction must return to canonical JSON.

---

## 13. Phased adoption

### Phase 1. Inventory

- Create source `metadata.json` and `document.json`.
- Preserve or reference the original PDF.
- Build the PDF-to-printed-page map.

### Phase 2. Visual resources

- Extract clean base images.
- Split printed pages.
- Generate thumbnails and candidate figure crops.

### Phase 3. Content model

- Create manifests.
- Create one `content.json` per page.
- Add index and glossary data.

### Phase 4. Linguistic content

- Transcribe.
- Translate.
- Review and validate.

### Phase 5. Consumers

- Web viewer.
- DOCX exporter.
- PDF exporter.
- Search index.

Test the complete cycle with one small section before processing the entire
document.

---

## 14. Acceptance checklist

- [ ] The document has a permanent ID.
- [ ] The source PDF is preserved or referenced with a checksum.
- [ ] The PDF-to-printed-page map is explicit.
- [ ] Every page has a manifest, `content.json`, and source image.
- [ ] Every figure has an ID, number, path, and state.
- [ ] Original and translated paragraphs are aligned.
- [ ] No page is marked validated with null titles and empty paragraphs
      (including `"index"`-type pages — see §3.6).
- [ ] `status` fields use the closed workflow-state enum, not a stray value
      (e.g. `candidate` instead of `candidate_crop`).
- [ ] The glossary is JSON.
- [ ] If the document glossary has an `extends` field, the target file exists
      and no term id is reused between the document and series glossaries.
- [ ] Workflow states use a closed vocabulary.
- [ ] JSON schemas are versioned.
- [ ] Validation detects broken paths and pending content.
- [ ] Web, DOCX, and PDF consume the same JSON.
- [ ] Derived outputs are not treated as source.
- [ ] Every correction returns to canonical JSON.
