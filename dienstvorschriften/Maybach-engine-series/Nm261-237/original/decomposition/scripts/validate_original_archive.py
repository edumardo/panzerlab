"""Validate the Nm 261/237 decomposition archive: schema conformance, referenced
files exist, page navigation and IDs are coherent. Read-only, no output files.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors = []

    content_schema = load(ROOT / "schema" / "content.schema.json")
    page_schema = load(ROOT / "schema" / "page.schema.json")

    global_manifest = load(ROOT / "manifest.json")
    seen_ids = set()
    pages_by_number = {}

    for entry in global_manifest["pages"]:
        page_number = entry["page"]
        try:
            jsonschema.validate(entry, page_schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"page {page_number} manifest: {exc.message}")

        section = entry["section"]
        section_dir = ROOT / ("frontmatter" if section == "FrontMatter" else f"sections/{section}")
        page_dir = section_dir / "pages" / f"{page_number:03d}"

        for fname in ("source.jpg", "manifest.json", "content.json"):
            if not (page_dir / fname).exists():
                errors.append(f"page {page_number}: missing {fname}")

        content = load(page_dir / "content.json")
        try:
            jsonschema.validate(content, content_schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"page {page_number} content: {exc.message}")

        if content["id"] in seen_ids:
            errors.append(f"duplicate id {content['id']}")
        seen_ids.add(content["id"])
        pages_by_number[page_number] = content

    for page_number, content in pages_by_number.items():
        nav = content["navigation"]
        if page_number > 1 and nav["previous"] != f"nm261237-page-{page_number - 1:03d}":
            errors.append(f"page {page_number}: bad previous link {nav['previous']}")
        if page_number < max(pages_by_number) and nav["next"] != f"nm261237-page-{page_number + 1:03d}":
            errors.append(f"page {page_number}: bad next link {nav['next']}")

    # document.json / index / glossary exist and parse
    for relpath in ("document.json", "layout.json", "index/contents.json", "glossary/terminology.json"):
        p = ROOT / relpath
        if not p.exists():
            errors.append(f"missing {relpath}")
        else:
            load(p)

    if errors:
        print(f"{len(errors)} problem(s):")
        for e in errors:
            print(" -", e)
        return 1

    print(f"OK: {len(pages_by_number)} pages validated, 0 problems.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
