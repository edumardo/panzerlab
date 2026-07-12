# panzerlab

Repo of documents, translations, and processing utilities about German WWII Panzer
documentation. `dienstvorschriften/` (D.V., official service manuals) is the first
document category; other categories (drawings, correspondence, reports...) will live
as sibling folders at repo root, following the same pattern.

## Structure

```
/
└── dienstvorschriften/             # category: service manuals (D.V.)
    └── D-652-series/                # one folder per D.V. series
        ├── index.md                 # series catalogue + consolidated content summary
        └── D.652-41a/                # one folder per individual document
            ├── metadata.md           # metadata + provenance, in English
            ├── original/
            │   ├── D.652-41a_de.pdf
            │   └── D.652-41a_processing-notes_v1.0.md  # optional, processing notes
            ├── es/
            │   └── D.652-41a_es_v1.0.docx
            └── en/
                └── D.652-41a_en_v1.0.docx
```

## Conventions

- **Series folder**: `D-<number>-series` (e.g. `D-652-series`).
- **Document folder**: official designation with `/` replaced by `-`, e.g.
  `D 652/41a` → `D.652-41a`.
- **Language folders inside a document**: `original/` is always the German source;
  each translation gets its own language-code folder (`es/`, `en/`, ...). Original and
  translations sit side by side — no separate `originals/` vs `translations/` trees.
- **File names**:
  - Original (no version, it's the source scan as received):
    `<document-designation>_<language>.<ext>`, e.g. `D.652-41a_de.pdf`.
  - Translations and processing notes (versioned, since they get revised):
    `<document-designation>_<language-or-description>_v<version>.<ext>`, e.g.
    `D.652-41a_es_v1.0.docx`, `D.652-41a_en_v1.0.docx`,
    `D.652-41a_processing-notes_v1.0.md`. Bump the version on meaningful revisions.
- **`metadata.md`** per document, always in English, Markdown only (no YAML): title
  (DE/EN/ES, and any other language the document gets translated into), variant,
  date, and provenance of the original (original file name as received, source/URL).
  No separate status section — status/links live in the series `index.md` instead.
- **Processing notes** (e.g. OCR/scan processing) live inside `original/`, named
  `<document-designation>_processing-notes_v<version>.md`.
- **`index.md`** per series: catalogue table of every document (title, date, status,
  link) plus a consolidated content summary for the series. Every catalogue table
  needs a **Status** column: `—` while a document has no folder yet, or a link to it
  once it does, e.g. `[✓ original, ES, EN](D.652-41a/)` listing what's actually
  present (original / which translations). Update it whenever a document's folder is
  created or gains content.
- No shared `tools/` folder for now. A document only gets its own `scripts/` folder
  if it needs something one-off and non-reusable.

## Git

- **Never add Claude/AI authorship or co-authorship to commits.** No
  `Co-Authored-By: Claude ...` trailer, ever — commits must show only the user as
  author.
