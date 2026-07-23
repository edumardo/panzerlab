---
name: validate-decomposition
description: Run the acceptance checklist from docs/PDF_TO_CANONICAL_JSON.md and AGENTS.md against a document's canonical JSON decomposition before considering it complete or before export. Use after scaffolding/transcribing/translating a document, or before generating DOCX/PDF output.
---

# Validate a canonical JSON decomposition

Source of truth: `docs/PDF_TO_CANONICAL_JSON.md` §8 and §14 (Acceptance checklist), and AGENTS.md "Validation". Re-read both if this document's schema has changed since last use — do not rely on memory of a prior document's shape.

## Checklist to run, in order

1. **JSON validity & schema conformance** — every `.json` file under `original/decomposition/` parses; conforms to `schema/*.schema.json` where one exists.
2. **Referential integrity** — every path referenced (`content`, `source.image`, `source.display_image`, figure `image`/`path`, glossary `extends`) actually exists on disk. No absolute local paths.
3. **Page order** — `manifest.json`'s `pages` array is consecutive or gaps are documented; never re-derive order from directory listing. `previous`/`next` navigation in each `content.json` is coherent with it.
4. **Unique IDs** — document, section, page, paragraph, and figure IDs collide with nothing else in the archive (including the series glossary's `series-term-NNN` range vs. the document glossary's `term-NNN` range).
5. **Figure numbering** — no unexplained gaps or duplicates. Cross-check the manifest's figure `number` against the actual printed "Bild N." in the source scan for any page not already `validated` — do not assume a numbering pipeline was reliable (see `project-d652-decomposition-lessons` memory for a documented drift bug in this repo's history).
6. **Workflow states** — only the closed vocabulary appears (`pending`, `draft`, `reviewed`, `validated`, `candidate_crop`, `not_applicable`); no stray values like `candidate`.
7. **Validated ⇒ actually populated** — no page/figure/paragraph is marked `validated` while its `titles`/`paragraphs`/`captions` are null or empty, including `"index"`-type pages (a structured `index/contents.json` does not substitute for a page's own transcription).
8. **Translation alignment** — translations live inside the same paragraph/figure object per language, not in parallel arrays; each language's validation status is tracked independently.
9. **Glossary** — valid JSON; if `extends` is set, the target series glossary file exists and no term id range overlaps.
10. **No pending content in production export** — if this validation run precedes an export, confirm the exporter path fails closed on anything not `validated`.
11. **Visual review** — pages and figures (or the full facsimile + translation page pair, for `A4_portrait_facsimile_then_translation` sections) pass visual inspection; DOCX/PDF outputs specifically require render-to-image review before delivery (AGENTS.md "Validation").

## Reporting

Report findings as a checklist against the 11 items above — pass/fail per item, with specific file paths and line/field references for any failure, not just "some issues found." Do not silently fix content while validating; flag issues first, then fix in canonical JSON (never in a derived DOCX/PDF/HTML) once confirmed.
