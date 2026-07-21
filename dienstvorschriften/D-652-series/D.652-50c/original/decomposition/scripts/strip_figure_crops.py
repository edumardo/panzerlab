"""One-off maintenance: remove all figure crop images and their metadata.

D.652-50c now exports exclusively via the facsimile-then-translation layout
(see export_facsimile_pdf.py), which never reads a figure crop file. Per-figure
crop images (validated or candidate_crop) are therefore pure dead weight: this
script deletes every sections/*/pages/*/figures/ directory and strips the
corresponding path/image/status fields from manifest.json and content.json,
keeping only `number` (page manifest) and `id`/`number`/`captions`/`label_keys`
(content.json) since captions remain real canonical content consumed by the
translation page. Also resyncs the global manifest.json to match.

Destructive and NOT idempotent in the sense of being re-runnable to reproduce
deleted files (there is no source to regenerate a crop from once deleted) —
but re-running after a first successful pass is a safe no-op.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def strip_page(page_dir: Path) -> dict:
    manifest_path = page_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["figures"] = [
        {"number": f["number"]} for f in manifest.get("figures", []) if f.get("number") is not None
    ]
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    content_path = page_dir / "content.json"
    content = json.loads(content_path.read_text(encoding="utf-8"))
    stripped_figures = []
    for figure in content.get("figures", []):
        stripped = {k: v for k, v in figure.items() if k in ("id", "number", "captions", "label_keys")}
        stripped_figures.append(stripped)
    content["figures"] = stripped_figures
    content_path.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    figures_dir = page_dir / "figures"
    if figures_dir.is_dir():
        shutil.rmtree(figures_dir)

    return manifest


def main():
    global_manifest_path = ROOT / "manifest.json"
    global_manifest = json.loads(global_manifest_path.read_text(encoding="utf-8"))

    updated_by_page = {}
    for entry in global_manifest["pages"]:
        page_number = entry["page"]
        section = entry["section"]
        base = ROOT / ("frontmatter" if section == "FrontMatter" else f"sections/{section}") / "pages" / f"{page_number:03d}"
        updated_by_page[page_number] = strip_page(base)
        print(f"page {page_number:03d} ({section}): figures -> {[f['number'] for f in updated_by_page[page_number]['figures']]}")

    for entry in global_manifest["pages"]:
        page_number = entry["page"]
        entry.clear()
        entry.update(updated_by_page[page_number])
    global_manifest_path.write_text(
        json.dumps(global_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
