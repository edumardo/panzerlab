"""Map each docx_reference_<lang>.json table tagged "Original page N" (or
"Original page Titelblatt / cover") onto this archive's printed_page / page
numbers (via page_map.json), producing translation_reference.json:
  { "<page>": {"printed_page": ..., "en": "<table text>", "es": "<table text>"} }

Scratch/reference data only -- an aid for filling in content.json paragraph
translations from the existing v1.0 docx deliverables; not itself canonical.
Tables that are plate label-key fragments (no "Original page" prefix) are
NOT included here; those are handled by direct visual transcription of the
plate images (see README.md "Current state").
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LABEL_PREFIXES = {"en": "Original page", "es": "Página original"}
LABEL_RE_TEMPLATE = r"^{prefix} (Titelblatt / (?:cover|portada)|\d+)"


def load_by_printed_page(lang: str) -> dict[str, str]:
    tables = json.loads((ROOT / f"docx_reference_{lang}.json").read_text(encoding="utf-8"))
    label_re = re.compile(LABEL_RE_TEMPLATE.format(prefix=re.escape(LABEL_PREFIXES[lang])))
    result = {}
    for table in tables:
        match = label_re.match(table["text"])
        if not match:
            continue
        key = "cover" if match.group(1).startswith("Titelblatt") else str(int(match.group(1)))
        result[key] = table["text"]
    return result


def main() -> None:
    page_map = json.loads((ROOT / "page_map.json").read_text(encoding="utf-8"))
    en = load_by_printed_page("en")
    es = load_by_printed_page("es")

    reference = {}
    for entry in page_map["pages"]:
        if entry["kind"] == "plate":
            continue
        printed = entry["printed_page"]
        printed_key = str(printed) if isinstance(printed, int) else printed
        reference[str(entry["page"])] = {
            "printed_page": printed,
            "section": entry["section"],
            "en": en.get(printed_key),
            "es": es.get(printed_key),
        }

    missing = [k for k, v in reference.items() if v["en"] is None or v["es"] is None]
    out = ROOT / "translation_reference.json"
    out.write_text(json.dumps(reference, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out} ({len(reference)} entries, {len(missing)} missing en/es: {missing})")


if __name__ == "__main__":
    main()
