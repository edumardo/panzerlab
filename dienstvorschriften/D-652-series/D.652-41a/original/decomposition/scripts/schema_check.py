"""One-off JSON Schema conformance check for every page manifest.json and
content.json against schema/page.schema.json and schema/content.schema.json.
Not part of the regular pipeline (validate_original_archive.py does the
structural checks); this is a stricter, supplementary pass.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]

page_schema = json.loads((ROOT / "schema" / "page.schema.json").read_text(encoding="utf-8"))
content_schema = json.loads((ROOT / "schema" / "content.schema.json").read_text(encoding="utf-8"))

errors = []
for manifest_path in list((ROOT / "frontmatter" / "pages").glob("*/manifest.json")) + list(
    (ROOT / "sections").glob("*/pages/*/manifest.json")
):
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(data, page_schema)
    except jsonschema.ValidationError as exc:
        errors.append(f"{manifest_path}: {exc.message}")

for content_path in list((ROOT / "frontmatter" / "pages").glob("*/content.json")) + list(
    (ROOT / "sections").glob("*/pages/*/content.json")
):
    data = json.loads(content_path.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(data, content_schema)
    except jsonschema.ValidationError as exc:
        errors.append(f"{content_path}: {exc.message}")

if errors:
    print(f"{len(errors)} schema violations:")
    for e in errors:
        print(" -", e)
else:
    print("Schema check: PASS (all manifest.json + content.json conform)")
