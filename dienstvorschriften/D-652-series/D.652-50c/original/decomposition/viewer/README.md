# Decomposition viewer (draft)

A single-file static viewer for validating the canonical decomposition, matching
the `A4_portrait_facsimile_then_translation` layout: it shows the full-page
facsimile scan next to a translation panel (title, paragraphs, and figure
captions) with DE/EN/ES stacked together (DE hideable via a checkbox), and
page navigation. This is a throwaway validation tool, not a production reader.

## Usage

Browsers block `fetch()` against local JSON over `file://`, so serve the
`decomposition` folder over HTTP:

```sh
cd dienstvorschriften/D-652-series/D.652-50c/original/decomposition
python -m http.server 8000
```

Then open `http://localhost:8000/viewer/`.
