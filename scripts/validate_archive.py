#!/usr/bin/env python3
"""Generic structural validator for a document's canonical JSON decomposition.

Implements the checklist from docs/PDF_TO_CANONICAL_JSON.md (sections 8 and
14) and AGENTS.md ("Validation"), against any document under
dienstvorschriften/<series>/<document>/original/decomposition/ -- not just
one hardcoded document. It does not replace the visual-review steps in that
checklist (source/figure crop inspection, rendered DOCX/PDF review); those
still require a human or a separate contact-sheet tool.

Usage:
    python scripts/validate_archive.py dienstvorschriften/D-652-series/D.652-50c
    python scripts/validate_archive.py path/to/original/decomposition

Exit code is non-zero if any error-level issue is found. Warnings are
informational (e.g. numbering gaps that may be legitimately documented
elsewhere) and do not fail the run.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WORKFLOW_STATES = {"pending", "draft", "reviewed", "validated", "candidate_crop", "not_applicable"}
WINDOWS_ABS_PATH = re.compile(r"^[A-Za-z]:[\\/]")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def resolve_decomposition_dir(arg: str) -> Path:
    path = Path(arg).resolve()
    if path.name == "decomposition" and (path / "manifest.json").is_file():
        return path
    candidate = path / "original" / "decomposition"
    if (candidate / "manifest.json").is_file():
        return candidate
    if (path / "manifest.json").is_file():
        return path
    raise SystemExit(f"Could not find a decomposition directory (with manifest.json) under {path}")


def load_json(path: Path, report: Report):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(f"Missing file: {path}")
    except json.JSONDecodeError as exc:
        report.error(f"Invalid JSON in {path}: {exc}")
    return None


def check_json_validity_and_absolute_paths(root: Path, report: Report) -> None:
    for json_path in root.rglob("*.json"):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(f"Invalid JSON in {json_path.relative_to(root)}: {exc}")
            continue
        stack = [("$", data)]
        while stack:
            pointer, value = stack.pop()
            if isinstance(value, dict):
                stack.extend((f"{pointer}.{key}", child) for key, child in value.items())
            elif isinstance(value, list):
                stack.extend((f"{pointer}[{index}]", child) for index, child in enumerate(value))
            elif isinstance(value, str) and (WINDOWS_ABS_PATH.match(value) or value.startswith("\\\\")):
                report.error(f"Absolute local path in {json_path.relative_to(root)} at {pointer}: {value}")


def page_base_dir(root: Path, section: str, page: int) -> Path:
    folder = root / "frontmatter" if section == "FrontMatter" else root / "sections" / section
    return folder / "pages" / f"{page:03d}"


def lang_status_key(lang_tag: str) -> str:
    # "en-GB" -> "translation_en_status", matching this repo's page-manifest convention.
    return f"translation_{lang_tag.split('-')[0].lower()}_status"


def check_status_value(value, location: str, report: Report) -> None:
    if value is not None and value not in WORKFLOW_STATES:
        report.error(f"Non-standard workflow state '{value}' at {location}")


def validate_pages(root: Path, manifest: dict, document: dict, report: Report):
    target_languages = document.get("target_languages", []) if document else []
    seen_content_ids: dict[str, str] = {}
    seen_figure_ids: dict[str, str] = {}
    all_figure_numbers: list[int] = []
    page_numbers: list[int] = []

    for entry in manifest.get("pages", []):
        page = entry.get("page")
        section = entry.get("section")
        if page is None or section is None:
            report.error(f"Manifest page entry missing page/section: {entry}")
            continue
        page_numbers.append(page)
        base = page_base_dir(root, section, page)

        required = [base / "manifest.json", base / "content.json"]
        source_ref = entry.get("source_scan", "source.jpg")
        required.append(base / source_ref)
        missing = [str(p) for p in required if not p.is_file() or p.stat().st_size == 0]
        for m in missing:
            report.error(f"Missing or empty required file: {m}")
        if missing:
            continue

        local_manifest = load_json(base / "manifest.json", report)
        if local_manifest is not None and local_manifest != entry:
            report.error(f"Global/local page manifest mismatch on page {page} ({section})")

        content = load_json(base / "content.json", report)
        if content is None:
            continue

        content_id = content.get("id")
        if content_id:
            if content_id in seen_content_ids:
                report.error(f"Duplicate page id '{content_id}': {seen_content_ids[content_id]} and page {page}")
            else:
                seen_content_ids[content_id] = f"page {page} ({section})"

        # Workflow states: transcription + per-language translation + figures marker.
        check_status_value(entry.get("transcription_status"), f"page {page} manifest.transcription_status", report)
        for lang in target_languages:
            key = lang_status_key(lang)
            check_status_value(entry.get(key), f"page {page} manifest.{key}", report)

        status = content.get("status", {}) or {}
        for key, value in status.items():
            check_status_value(value, f"page {page} content.status.{key}", report)

        # Validated-but-empty: a page can't be validated with no titles and no paragraphs.
        titles = content.get("titles") or {}
        has_any_title = any(v for v in titles.values())
        has_paragraphs = bool(content.get("paragraphs"))
        transcription_validated = status.get("transcription") == "validated" or entry.get("transcription_status") == "validated"
        if transcription_validated and not has_any_title and not has_paragraphs and content.get("type") != "blank":
            report.error(f"Page {page} ({section}) marked validated but has no titles and no paragraphs")

        # Paragraph translation alignment: every paragraph's text dict should carry
        # a key for the source language and each target language (value may be null).
        for paragraph in content.get("paragraphs", []):
            text = paragraph.get("text", {})
            missing_keys = [lang for lang in target_languages if lang not in text]
            if missing_keys:
                report.warn(
                    f"Paragraph {paragraph.get('id', '?')} on page {page} missing language key(s) {missing_keys} "
                    "(present but null is fine; absent key is not)"
                )

        # Figures: ids, numbers, referenced crop files.
        for figure in content.get("figures", []):
            figure_id = figure.get("id")
            if figure_id:
                if figure_id in seen_figure_ids:
                    report.error(f"Duplicate figure id '{figure_id}': {seen_figure_ids[figure_id]} and page {page}")
                else:
                    seen_figure_ids[figure_id] = f"page {page} ({section})"
            if figure.get("number") is not None:
                all_figure_numbers.append(figure["number"])
            check_status_value(figure.get("status"), f"page {page} figure {figure_id or figure.get('number')}.status", report)
            for image_field in ("image", "path"):
                if image_field in figure:
                    target = base / figure[image_field]
                    if not target.is_file() or target.stat().st_size == 0:
                        report.error(f"Missing figure file on page {page}: {figure[image_field]}")

    if page_numbers != sorted(page_numbers):
        report.error("Manifest pages array is not in ascending page order")
    gaps = [b - a for a, b in zip(page_numbers, page_numbers[1:]) if b - a != 1]
    if gaps:
        report.warn(f"Page sequence has {len(gaps)} gap(s) larger than 1 -- confirm these are documented, not accidental")

    duplicate_figure_numbers = {n for n in all_figure_numbers if all_figure_numbers.count(n) > 1}
    if duplicate_figure_numbers:
        report.error(f"Duplicate figure numbers: {sorted(duplicate_figure_numbers)}")
    if all_figure_numbers:
        expected = set(range(min(all_figure_numbers), max(all_figure_numbers) + 1))
        missing_numbers = expected - set(all_figure_numbers)
        if missing_numbers:
            report.warn(f"Figure numbering has gaps (confirm documented): {sorted(missing_numbers)}")


def validate_glossary(root: Path, glossary_path: Path, report: Report, id_prefix: str, forbidden_prefix: str | None):
    glossary = load_json(glossary_path, report)
    if glossary is None:
        return None
    extends = glossary.get("extends")
    if extends:
        target = (glossary_path.parent / extends).resolve()
        if not target.is_file():
            report.error(f"Glossary 'extends' target does not exist: {glossary_path} -> {extends}")
    ids = [term.get("id") for term in glossary.get("terms", [])]
    for term_id in ids:
        if term_id and forbidden_prefix and term_id.startswith(forbidden_prefix):
            report.error(f"Glossary term id '{term_id}' in {glossary_path} uses the other glossary's id prefix")
        if term_id and id_prefix and not term_id.startswith(id_prefix):
            report.warn(f"Glossary term id '{term_id}' in {glossary_path} does not follow the '{id_prefix}' convention")
        status = None
        for term in glossary.get("terms", []):
            if term.get("id") == term_id:
                status = term.get("status")
                break
        check_status_value(status, f"{glossary_path} term {term_id}.status", report)
    return glossary


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <document-dir-or-decomposition-dir>")

    root = resolve_decomposition_dir(sys.argv[1])
    report = Report()

    manifest = load_json(root / "manifest.json", report)
    document = load_json(root / "document.json", report)

    for required in (root / "document.json", root / "index" / "contents.json", root / "glossary" / "terminology.json", root / "layout.json"):
        if not required.is_file() or required.stat().st_size == 0:
            report.error(f"Missing canonical file: {required}")

    check_json_validity_and_absolute_paths(root, report)

    if manifest is not None:
        validate_pages(root, manifest, document, report)
        for section_id in manifest.get("sections", {}):
            folder = root / "frontmatter" if section_id == "FrontMatter" else root / "sections" / section_id
            if not (folder / "manifest.json").is_file():
                report.error(f"Missing section manifest for {section_id}")

    doc_glossary_path = root / "glossary" / "terminology.json"
    if doc_glossary_path.is_file():
        validate_glossary(root, doc_glossary_path, report, id_prefix="term-", forbidden_prefix="series-term-")

    series_glossary_path = root.parents[2] / "glossary" / "terminology.json"
    if series_glossary_path.is_file():
        validate_glossary(root, series_glossary_path, report, id_prefix="series-term-", forbidden_prefix=None)

    if report.warnings:
        print(f"Warnings ({len(report.warnings)}):", file=sys.stderr)
        for warning in report.warnings:
            print(f"  - {warning}", file=sys.stderr)

    if report.errors:
        print(f"Archive validation: FAIL ({len(report.errors)} error(s))", file=sys.stderr)
        for error in report.errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)

    print("Archive validation: PASS")
    if manifest is not None:
        print(f"Pages: {len(manifest.get('pages', []))}")


if __name__ == "__main__":
    main()
