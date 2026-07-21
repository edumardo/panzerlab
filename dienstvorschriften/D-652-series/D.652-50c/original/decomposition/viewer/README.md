# Decomposition viewer (draft)

A single-file static viewer for validating the canonical decomposition: it
shows translated paragraph text next to the corresponding figures for each
page, with a language switch (DE / EN / ES) and page navigation. This is a
throwaway validation tool, not a production reader.

## Usage

Browsers block `fetch()` against local JSON over `file://`, so serve the
`decomposition` folder over HTTP:

```sh
cd dienstvorschriften/D-652-series/D.652-50c/original/decomposition
python -m http.server 8000
```

Then open `http://localhost:8000/viewer/`.
