"""Dump every table's full text from the existing en/es v1.0 docx deliverables
into a reference JSON, keyed by table index, for use while aligning German
transcription + translation into the canonical decomposition.

This is a READ-ONLY reference extraction: it does not touch en/ or es/, and
its output (docx_reference_<lang>.json) is scratch data for the transcription
pass, not part of the canonical archive itself.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import docx

ROOT = Path(__file__).resolve().parents[1]
DOC_ROOT = ROOT.parents[1]  # D.652-41a/


def dump(lang: str, path: Path) -> None:
    document = docx.Document(path)
    tables = []
    for index, table in enumerate(document.tables):
        cell_text = table.rows[0].cells[-1].text
        tables.append({"index": index, "text": cell_text})
    out = ROOT / f"docx_reference_{lang}.json"
    out.write_text(json.dumps(tables, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out} ({len(tables)} tables)")


def main() -> None:
    dump("en", DOC_ROOT / "en" / "D.652-41a_en_v1.0.docx")
    dump("es", DOC_ROOT / "es" / "D.652-41a_es_v1.0.docx")


if __name__ == "__main__":
    main()
