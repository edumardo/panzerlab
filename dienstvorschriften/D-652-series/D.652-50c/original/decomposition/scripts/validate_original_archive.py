"""Structural validation for the format-neutral original/ archive."""

from __future__ import annotations

import json
import re
from pathlib import Path


ORIGINAL = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []
    manifest = json.loads((ORIGINAL / "manifest.json").read_text(encoding="utf-8"))
    pages = manifest["pages"]
    if [entry["page"] for entry in pages] != list(range(1, 144)):
        errors.append("Global page sequence is not exactly 1-143")
    if len(list((ORIGINAL / "assets" / "spreads").glob("spread_*.jpg"))) != 75:
        errors.append("Clean spread count is not 75")

    windows_absolute = re.compile(r"^[A-Za-z]:[\\/]")
    for json_path in ORIGINAL.rglob("*.json"):
        data = json.loads(json_path.read_text(encoding="utf-8"))
        pending = [("$", data)]
        while pending:
            pointer, value = pending.pop()
            if isinstance(value, dict):
                pending.extend((f"{pointer}.{key}", child) for key, child in value.items())
            elif isinstance(value, list):
                pending.extend((f"{pointer}[{index}]", child) for index, child in enumerate(value))
            elif isinstance(value, str) and (windows_absolute.match(value) or value.startswith("\\\\")):
                errors.append(f"Absolute local path in {json_path.relative_to(ORIGINAL)} at {pointer}: {value}")

    extraction_manifest = ORIGINAL / "assets" / "extraction_001_075.json"
    extraction_records = json.loads(extraction_manifest.read_text(encoding="utf-8"))
    for record in extraction_records:
        for field in ("spread", "thumbnail"):
            reference = Path(record[field])
            if reference.is_absolute() or not (extraction_manifest.parent / reference).is_file():
                errors.append(f"Invalid extraction reference on PDF page {record['pdf_page']}: {field}={record[field]}")

    figure_numbers: list[int] = []
    status_counts: dict[str, int] = {}
    for entry in pages:
        page = entry["page"]
        section = entry["section"]
        base = ORIGINAL / ("frontmatter" if section == "FrontMatter" else f"sections/{section}") / "pages" / f"{page:03d}"
        for required in (base / "source.jpg", base / "content.json", base / "manifest.json"):
            if not required.is_file() or required.stat().st_size == 0:
                errors.append(f"Missing or empty: {required}")
        local = json.loads((base / "manifest.json").read_text(encoding="utf-8"))
        if local != entry:
            errors.append(f"Global/local manifest mismatch on page {page}")
        content = json.loads((base / "content.json").read_text(encoding="utf-8"))
        if content["id"] != f"d65250c-page-{page:03d}" or content["page"] != page:
            errors.append(f"Invalid canonical content identity on page {page}")
        if content["source"]["image"] != "source.jpg":
            errors.append(f"Invalid source image reference on page {page}")
        status = entry["transcription_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        for figure in entry["figures"]:
            target = base / figure["path"]
            if not target.is_file() or target.stat().st_size == 0:
                errors.append(f"Missing figure on page {page}: {figure['path']}")
            if figure.get("number") is not None:
                figure_numbers.append(figure["number"])

    if sorted(figure_numbers) != list(range(1, 257)):
        errors.append("Figure sequence is not exactly Bild 1-256")
    for section in manifest["sections"]:
        base = ORIGINAL / ("frontmatter" if section == "FrontMatter" else f"sections/{section}")
        if not (base / "manifest.json").is_file():
            errors.append(f"Missing section files: {section}")

    for required in (ORIGINAL / "document.json", ORIGINAL / "index" / "contents.json", ORIGINAL / "glossary" / "terminology.json", ORIGINAL / "layout.json"):
        if not required.is_file() or required.stat().st_size == 0:
            errors.append(f"Missing canonical file: {required}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("Archive validation: PASS")
    print(f"Pages: {len(pages)}")
    print(f"Figures: {len(figure_numbers)} (Bild 1-256)")
    print(f"Transcription states: {status_counts}")


if __name__ == "__main__":
    main()
