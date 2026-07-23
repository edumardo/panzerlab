---
name: translate-section
description: Translate a section's transcribed content into target languages (en-GB, es-ES, etc.) following this repo's glossary-driven, section-by-section workflow. Use when adding or updating translations in a document's canonical JSON, not for one-off ad hoc translation.
---

# Translate a section

Source of truth: `docs/PDF_TO_CANONICAL_JSON.md` §3.7–3.8 (figures, glossary) and §7 (translate), AGENTS.md "Series-shared glossary" and "Canonical content rules". This encodes the workflow validated on D.652-50c (see `project-d652-decomposition-lessons` memory) — translate section-by-section in transcription order, not the whole document in one pass, and grow the glossary incrementally rather than doing a separate consistency pass afterward.

## Before starting

1. Confirm the section's German transcription (`content.json` `paragraphs[].text.de`, figure `captions.de`, `label_keys.de`) is at least `draft`/`reviewed` — never translate from OCR-only text.
2. Read the **series-shared glossary** (`<series>/glossary/terminology.json`) first, then the document's own `glossary/terminology.json` (which `extends` it). Check both before inventing a new term.

## While translating

3. Translate **directly from German** — never through an intermediate language.
4. Work **section by section, in the same order sections were transcribed** — do not jump ahead or batch the whole document, so terminology decisions made early are still fresh when later sections reuse the same terms.
5. For each paragraph/caption/label_key, fill the target-language object **in the same object as the source text** (`text.en-GB`, `text.es-ES`), not a separate parallel structure.
6. Preserve the original German technical term in parentheses when it aids traceability, e.g. "front superstructure armour (Bugpanzerung)" — see `project-d652-bugpanzer-terminology` memory for an approved example pair (EN/ES).
7. When a new technical term appears:
   - If it's generic vehicle/tool/component vocabulary (chassis parts, spanner types, fasteners, etc.), add it to the **series** glossary with a `series-term-NNN` id.
   - If it's specific to this document's subject, add it to the **document** glossary with a `term-NNN` id.
   - If a document-local term turns out to be needed by a second document in the series, move it to the series glossary rather than duplicating it.
8. Declare explicit BCP 47 variants (`en-GB`, `es-ES`), not bare `en`/`es`.
9. Set each language's status independently (`draft` → `reviewed` → `validated`); do not validate a language you have not actually reviewed.

## After translating a section

10. Re-read the section once translated for consistency against the glossary (not the whole document — the incremental-glossary approach is what keeps a separate full consistency pass unnecessary).
11. Hand off to the `validate-decomposition` skill before considering the section done, and update the series `index.md` status column if this changes what's available for the document (AGENTS.md "Series indexes").
