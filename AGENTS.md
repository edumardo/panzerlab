# panzerlab repository instructions

This is the single canonical instruction file for contributors and AI assistants
working in this repository. Do not add tool-specific duplicates such as
`CLAUDE.md`, `COPILOT.md`, or equivalent files. Tools that do not discover
`AGENTS.md` automatically must be directed to read it before making changes.

## Repository purpose and language

`panzerlab` stores German WWII Panzer documentation, source decompositions,
translations, and document-processing utilities.

- Repository documentation, metadata, filenames, code comments, and commit
  messages must be in English.
- Original German text and target-language translations remain in their proper
  language fields.
- `dienstvorschriften/` contains official service manuals. Other categories,
  such as drawings, correspondence, and reports, may be added as sibling
  directories and must follow the same general pattern.

## Structure

```text
/
├── AGENTS.md
├── docs/
│   └── PDF_TO_CANONICAL_JSON.md
├── viewer/
│   ├── index.html
│   └── documents.json
└── dienstvorschriften/
    └── D-652-series/
        ├── index.md
        ├── glossary/
        │   └── terminology.json
        └── D.652-50c/
            ├── metadata.md
            ├── original/
            │   ├── D.652-50c_de.pdf
            │   ├── metadata.json
            │   └── decomposition/
            │       ├── document.json
            │       ├── manifest.json
            │       ├── layout.json
            │       ├── assets/
            │       ├── frontmatter/
            │       ├── glossary/
            │       ├── index/
            │       ├── schema/
            │       ├── sections/
            │       └── scripts/
            ├── en/
            ├── es/
            └── bilingual/
```

`viewer/` is a generic, document-agnostic static viewer for validating any
decomposition built per `docs/PDF_TO_CANONICAL_JSON.md`; `viewer/documents.json`
lists which decompositions it offers. It is a draft validation tool, not a
production reader — see `viewer/README.md`.

## Naming conventions

- **Series directory**: `D-<number>-series`, for example `D-652-series`.
- **Document directory**: replace `/` in the official designation with `-` and
  use a dot after `D`, for example `D 652/50c` becomes `D.652-50c`.
- **Original source**: `<document-designation>_<language>.<ext>`, without a
  version suffix, for example `D.652-50c_de.pdf`.
- **Translations and processing notes**: use a version suffix such as
  `_v1.0`. Increase it on meaningful revisions.
- **Language directories**: use language codes such as `en/`, `es/`, or `fr/`.
  The German source remains under `original/`.
- **Bilingual exports**: a `bilingual/` directory holds exports that show more
  than one target language side by side on the same page (for example a
  facsimile-then-translation export listing EN and ES together), so they are
  not misfiled under a single-language directory. Name files
  `<document-designation>_bilingual_<section>_v<version>.pdf`.

## Document metadata

Every document directory must contain `metadata.md` in English, without YAML
front matter. It must include:

- designation and series;
- German title and available translated titles;
- vehicle or equipment variants;
- original date;
- original filename, current filename, provenance, and source URL when known.

Do not add a separate status section to `metadata.md`. Availability and links
belong in the series `index.md`.

The `original/metadata.json` file describes the source file itself: filename,
media type, byte size, checksum, page count, language, provenance, and the path
to its decomposition.

## Original source and canonical decomposition

Keep the top level of `original/` intentionally small:

```text
original/
├── <document>_de.pdf
├── metadata.json
└── decomposition/
```

All extracted spreads, pages, figures, canonical JSON, schemas, processing
notes, and document-specific scripts belong under `original/decomposition/`.

JSON is the canonical source for reconstructed content. DOCX, PDF, HTML,
Markdown, databases, and search indexes are derived outputs. Corrections must be
made in canonical JSON and then regenerated; never leave the only corrected
version in a derived document.

Follow [`docs/PDF_TO_CANONICAL_JSON.md`](docs/PDF_TO_CANONICAL_JSON.md) when
creating or changing a decomposition.

## Canonical content rules

- Use stable IDs for documents, sections, pages, paragraphs, and figures.
- Use explicit BCP 47 language tags in JSON, such as `de-DE`, `en-GB`, and
  `es-ES`.
- Align translations within the same paragraph or figure object.
- Keep plain searchable text and structured formatting runs.
- Store figure captions and label keys separately.
- Preserve page order in manifests; do not infer it from directory listings.
- Use relative paths inside the archive.
- Maintain explicit workflow states: `pending`, `draft`, `reviewed`,
  `validated`, `candidate_crop`, and `not_applicable`.
- Production exporters must reject required content that is not validated.
- Translations must be made from the original language, not through another
  translation.
- A section's `manifest.json` `layout` field selects its export mode.
  `A4_portrait_facsimile_then_translation` shows the full original page
  (`source_display.jpg` when present, else `source.jpg`) followed by a
  translation page listing the section's titles and figure captions; per-figure
  crop images are then optional archival data, not a rendering requirement.
  Other sections keep the per-figure-crop layout until they adopt the
  facsimile approach.
- `A4_landscape_facsimile_then_translation` is the same facsimile-then-
  translation export mode, for sections whose printed page is itself a
  landscape sheet that crosses the gutter and must never be split into
  left/right halves (a plate spanning two book pages, for example). Used by
  D.652-41a's `G` (plates) section: each source page carries one or two
  `Bild` numbers, and the following translation page lists captions and
  label keys for all of them.
- `source_display.jpg` (when present next to a page's `source.jpg`) is a
  derived, regenerable crop that trims scan background/edges for display. It
  never replaces `source.jpg`, which stays as the untouched archival scan.

## Series-shared glossary

A series may hold a shared terminology file at `<series>/glossary/terminology.json`,
using the same term shape as a document glossary but no `document_id`, an id
prefix of `series-term-NNN` (to stay unambiguous next to any document-local
`term-NNN` ids), and a `scope: "series"` / `series_id` pair identifying it.

Vehicle/tool/component vocabulary that is not specific to one document's
subject (chassis part names, spanner types, fastener types, and similar) belongs
in the series glossary so every document in the series translates it the same
way. A document's own `glossary/terminology.json` then adds only terms specific
to that document's subject matter, and points at the shared file with an
`"extends"` field, for example:

```json
{
  "schema_version": 1,
  "document_id": "d652-50c",
  "source_language": "de-DE",
  "target_languages": ["en-GB", "es-ES"],
  "extends": "../../../../glossary/terminology.json",
  "terms": []
}
```

Before adding a new document-level term, check whether the series glossary
already has it. When a term used only in one document turns out to be needed by
a second document in the series, move it to the series glossary rather than
duplicating it.

## Series indexes

Each series directory has an `index.md` containing its catalogue and consolidated
summary. Every catalogue table must include a **Status** column:

- use `—` when a document directory does not exist;
- link to the document when content exists;
- list only what is actually present, for example
  `[✓ original, ES, EN](D.652-41a/)`.

Update the series index whenever a document directory is created or gains a new
source or translation.

## Scripts and generated files

- Document-specific processing scripts belong in
  `original/decomposition/scripts/`.
- Add shared tooling only when it is genuinely reusable across several
  documents and its interface is stable.
- `scripts/validate_archive.py` (repository root) is such shared tooling: it
  runs the acceptance checklist in
  [`docs/PDF_TO_CANONICAL_JSON.md`](docs/PDF_TO_CANONICAL_JSON.md) (JSON
  validity, referential integrity, page order, unique IDs, figure numbering,
  workflow-state vocabulary, glossary `extends` resolution) against any
  document directory or `original/decomposition/` path. It does not replace
  the visual-review steps in that checklist.
- Scripts must state what they overwrite and should be idempotent where
  practical.
- Never overwrite validated transcription, translation, or figure data with OCR
  or automatic crops.
- Temporary renders, contact sheets, caches, and exported output must not be
  treated as canonical data.

## Validation

Before considering a decomposition complete, verify:

- all JSON parses and conforms to the repository schemas;
- every referenced file exists;
- page order and previous/next navigation are coherent;
- IDs are unique;
- figure numbering is complete or documented;
- source checksums match;
- validated languages contain no pending required fields;
- a page marked validated is not missing its own titles/paragraphs just
  because a separate structured file (index, glossary) covers the same
  ground;
- extracted pages and figures pass visual inspection.

DOCX and PDF outputs require render-to-image visual review before delivery.

## Git

- Preserve unrelated working-tree changes.
- Do not stage, commit, or push unless the user explicitly asks.
- Do not enable repository-wide Git LFS rules without an explicit decision about
  storage and bandwidth. Prefer document-scoped rules if LFS is adopted.
- Never add AI authorship or co-authorship to commits. Do not add
  `Co-Authored-By` trailers for any AI tool; commits must show only the human
  author.

