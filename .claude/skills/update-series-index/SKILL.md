---
name: update-series-index
description: Update a D-series index.md Status column after a document directory is created or gains a new source/translation/language. Use right after decompose-document or translate-section changes what exists on disk for a document — not for editing catalogue content (titles, dates, variants).
---

# Update a series index

Source of truth: AGENTS.md "Series indexes". Each series directory (`dienstvorschriften/<series>/index.md`) holds the catalogue and a **Status** column that must reflect only what is actually present on disk — not what's planned or in progress.

## When to run this

- Right after `decompose-document` creates a new document directory.
- Right after `translate-section` (or any transcription work) adds/promotes a language under a document (`original/`, `en/`, `es/`, `bilingual/`).
- Whenever you notice a catalogue row's Status is stale relative to the actual directory contents.

## Steps

1. **Inspect what actually exists** for the document directory, don't infer from memory or from the last time this index was edited: check for `original/` (source PDF + decomposition present), `en/`, `es/`, `bilingual/` non-empty directories.
2. **Find the row** in `index.md` for that designation (rows are split across subsection tables, e.g. "StuG / StuH", "Panzerkampfwagen III" — search all tables in the file, not just the first).
3. **Set the Status cell**:
   - `—` if the document directory does not exist yet.
   - A link to the document directory listing only what's actually present, in the style already used in this repo: `` [✓ original, ES, EN](D.652-41a/) `` or `` [✓ original](D.652-50c/) ``. Keep the existing ordering convention (`original` first, then target languages) and only list a language once its content is more than an empty stub.
4. **Do not touch other columns** (designation, original title, translation, variant, date) — this skill only maintains Status. If those look wrong or missing, flag it separately rather than silently correcting them.
5. **If a catalogue table has no Status column at all** (some legacy tables in this repo predate the convention), do not silently add one as a side effect of an unrelated update — flag it to the user, since retrofitting a column to an existing table is a bigger edit than a status refresh.
6. Save and, unless asked to commit, leave the change uncommitted like any other edit (AGENTS.md "Git": don't stage/commit/push without being asked).

## Do not

- Do not mark a document `✓` for a language that is only `pending`/`draft`-stage stub content with no real translated pages.
- Do not reorder or renumber catalogue rows while doing a status-only update.
- Do not infer series membership or table placement from designation number alone — some documents are cross-listed by subject (see the "Shared" section for D 652/50a-style manuals covering multiple vehicle types).
