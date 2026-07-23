---
name: validate-decomposition
description: Run the acceptance checklist from docs/PDF_TO_CANONICAL_JSON.md and AGENTS.md against a document's canonical JSON decomposition before considering it complete or before export. Use after scaffolding/transcribing/translating a document, or before generating DOCX/PDF output.
---

# Validate a canonical JSON decomposition

Source of truth: `docs/PDF_TO_CANONICAL_JSON.md` §8 and §14 (Acceptance checklist), and AGENTS.md "Validation". Re-read both if this document's schema has changed since last use — do not rely on memory of a prior document's shape.

## Step 0: run the automated validator

Run `python scripts/validate_archive.py <document-dir>` (or point it at an `original/decomposition/` path directly) first. It mechanically covers items 1–6 and 9 below (JSON validity, referential integrity/absolute paths, page order, unique page/figure IDs, figure-number duplicates and gaps, workflow-state vocabulary, validated-but-empty pages, glossary `extends` resolution and id-prefix collisions) and exits non-zero on any error. Warnings it prints (numbering gaps, missing paragraph-language keys) are not automatically wrong — confirm each one is legitimate (e.g. a documented gap, a blank page) rather than dismissing it.

Fix anything it flags in canonical JSON before moving on to the checks below, which it cannot automate.

## Checklist to run, in order

1. **JSON validity & schema conformance** — every `.json` file under `original/decomposition/` parses (script); conforms to `schema/*.schema.json` where one exists (not checked by the script — no `jsonschema` dependency is assumed; verify by hand or extend the script if this becomes a recurring gap).
2. **Referential integrity** — every path referenced (`content`, `source.image`, `source.display_image`, figure `image`/`path`, glossary `extends`) actually exists on disk. No absolute local paths. (script)
3. **Page order** — `manifest.json`'s `pages` array is consecutive or gaps are documented; never re-derive order from directory listing. `previous`/`next` navigation in each `content.json` is coherent with it. (script checks ascending order and figure-number gaps; `previous`/`next` coherence is not yet automated)
4. **Unique IDs** — document, section, page, paragraph, and figure IDs collide with nothing else in the archive (including the series glossary's `series-term-NNN` range vs. the document glossary's `term-NNN` range). (script checks page/figure/glossary-term ids; paragraph ids are not yet checked)
5. **Figure numbering** — no unexplained gaps or duplicates. Cross-check the manifest's figure `number` against the actual printed "Bild N." in the source scan for any page not already `validated` — do not assume a numbering pipeline was reliable (see `project-d652-decomposition-lessons` memory for a documented drift bug in this repo's history). The script flags duplicates as errors and gaps as warnings; the printed-page cross-check itself still requires visual review.
6. **Workflow states** — only the closed vocabulary appears (`pending`, `draft`, `reviewed`, `validated`, `candidate_crop`, `not_applicable`); no stray values like `candidate`. (script)
7. **Validated ⇒ actually populated** — no page/figure/paragraph is marked `validated` while its `titles`/`paragraphs`/`captions` are null or empty, including `"index"`-type pages (a structured `index/contents.json` does not substitute for a page's own transcription). The script checks this for pages (exempting `type: "blank"`); figure/paragraph-level emptiness is not yet automated.
8. **Translation alignment** — translations live inside the same paragraph/figure object per language, not in parallel arrays; each language's validation status is tracked independently. The script warns when a paragraph's `text` is missing a language key entirely (a null value is fine; an absent key is not).
9. **Glossary** — valid JSON; if `extends` is set, the target series glossary file exists and no term id range overlaps. (script)
10. **No pending content in production export** — if this validation run precedes an export, confirm the exporter path fails closed on anything not `validated`. (not automated by the script — a property of the exporter, not the archive)
11. **Visual review** — pages and figures (or the full facsimile + translation page pair, for `A4_portrait_facsimile_then_translation` sections) pass visual inspection; DOCX/PDF outputs specifically require render-to-image review before delivery (AGENTS.md "Validation"). Never automatable — always do this by hand.

## Reporting

Report findings as a checklist against the 11 items above — pass/fail per item, with specific file paths and line/field references for any failure, not just "some issues found." Do not silently fix content while validating; flag issues first, then fix in canonical JSON (never in a derived DOCX/PDF/HTML) once confirmed.
