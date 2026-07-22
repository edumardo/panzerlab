# Decomposition viewer (draft)

A single-file static viewer for validating any canonical decomposition built
per [`docs/PDF_TO_CANONICAL_JSON.md`](../docs/PDF_TO_CANONICAL_JSON.md),
matching the `A4_portrait_facsimile_then_translation` layout: it shows the
full-page facsimile scan next to a translation panel (title, paragraphs, and
figure captions) with the source language and every target language stacked
together (source hideable via a checkbox), and page navigation. This is a
throwaway validation tool, not a production reader.

It is not tied to one document: `documents.json` lists every decomposition to
offer, and a dropdown in the sidebar switches between them. Source/target
languages, section grouping and page order are all read from each document's
own `document.json` and manifests — nothing about a specific document is
hardcoded in `index.html`.

## Adding a document

Add an entry to `documents.json` pointing at the document's
`decomposition/` folder (relative to this `viewer/` directory):

```json
{ "id": "d652-41a", "decomposition": "../dienstvorschriften/D-652-series/D.652-41a/original/decomposition" }
```

The viewer fetches that folder's `document.json` for the title and language
list, so no other change is needed.

## Usage

Browsers block `fetch()` against local JSON over `file://`, so serve the
repository root over HTTP:

```sh
python -m http.server 8000
```

Then open `http://localhost:8000/viewer/`.
