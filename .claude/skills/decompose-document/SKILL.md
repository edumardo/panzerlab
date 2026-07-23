---
name: decompose-document
description: Scaffold a new document's canonical JSON decomposition (metadata, manifests, sections, pages) from a source PDF, following docs/PDF_TO_CANONICAL_JSON.md and AGENTS.md. Use when starting a new D-series document or adding a new document to an existing series.
---

# Decompose a document into canonical JSON

Governing docs — read both before starting, do not infer conventions from a single existing example:

- `AGENTS.md` (repository-wide structure, naming, canonical content rules)
- `docs/PDF_TO_CANONICAL_JSON.md` (full end-to-end methodology)

## Steps

1. **Locate or create the series.** `dienstvorschriften/<series>/`, e.g. `D-652-series`. If new, create `index.md` and `glossary/terminology.json` (scope: series, see AGENTS.md "Series-shared glossary").
2. **Create the document directory** using the naming convention in AGENTS.md (`D 652/50c` → `D.652-50c`). Keep `original/` top-level small: the PDF, `metadata.json`, and `decomposition/`.
3. **Write `metadata.md`** (English, no YAML frontmatter): designation, series, German title + translated titles, vehicle/equipment variants, original date, original filename/current filename/provenance/source URL. No status section — that belongs in the series `index.md`.
4. **Write `original/metadata.json`**: filename, media type, byte size, sha256 checksum, page count, language, provenance, path to decomposition. Compute the checksum before any processing (§3.1).
5. **Inventory the PDF** (§5 Step 1): `pdfinfo`, `pdffonts`, `pdfimages -list`; note embedded-text availability, spreads vs. single pages, scan resolution, PDF-page-to-printed-page relationship.
6. **Build the explicit PDF-to-book page map** (§5 Step 3) — never infer order from a formula alone; store the expanded result, since covers/blanks/fold-outs/duplicates break formulas.
7. **Extract and split pages** (§5 Step 2 & 4): prefer embedded base images over re-rendering; save each printed page at `sections/<ID>/pages/<NNN>/source.jpg`; record normalised crop rectangle, rotation, checksum.
8. **Create `document.json` and the global `manifest.json`** (§3.2–3.3): explicit `pages` array with `page`, `section`, `pdf_page`, `side`, `content` — page order is data, never inferred from the filesystem.
9. **Create each section's `manifest.json`** (§3.4): pick `layout` deliberately —
   - `A4_portrait_source_left_translation_right_or_two_figures` (per-figure-crop, the older default), or
   - `A4_portrait_facsimile_then_translation` (full-page facsimile + bilingual translation page — see the `translate-section` skill and `project-d652-facsimile-translation-approach` memory for when this is preferable).
10. **Create per-page `manifest.json` + `content.json`** (§3.5–3.6): workflow-state fields start at `pending`/`draft`, never `validated`, until actually reviewed. A page's own `titles`/`paragraphs` must be filled even if a structured `index/contents.json` covers the same ground.
11. **Candidate figure crops** (§5 Step 5) only apply to the per-figure-crop layout; do not treat crops as validated until visually checked for completeness, correct numbering, orientation, and legible callouts — cross-check the printed "Bild N." against the manifest, don't trust an automated `number` at face value (see `project-d652-decomposition-lessons` memory: a prior pipeline had a self-cancelling +2 numbering drift).
12. **Stop after one section.** Test the complete cycle (extract → manifest → content.json → validate) on a single small section before processing the whole document (§13 Phase plan).

## Do not

- Do not mark any workflow-state field `validated` during scaffolding — that's a separate review step.
- Do not invent IDs from translated titles; use the stable-ID scheme in §7.
- Do not duplicate series-shared glossary terms into the document glossary — check the series glossary first.
- Do not commit/push unless explicitly asked (AGENTS.md "Git").

After scaffolding, hand off transcription/translation to the `translate-section` skill and run the `validate-decomposition` skill before calling the work done.
