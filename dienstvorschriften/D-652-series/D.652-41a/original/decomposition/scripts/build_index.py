"""Build index/contents.json from page_map.json.

Two groups: the running-text sections (block granularity, matching what the
processing notes document) and the plates (one entry per printed Bild
number, including the two entries sharing a rotated-double sheet).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEXT_TITLES = {
    "FrontMatter": "Titelseite, Inhalt, Vorbemerkungen, A. Technische Angaben, B. Beschreibung §1-2",
    "S01": "B. Beschreibung §3-4: Panzerwanne, Motor",
    "S02": "B. Beschreibung §5-9: Hauptkupplung, Wechselgetriebe, Kegel-/Lenkgetriebe, Stütz-/Lenkbremse, Kraftübertragung",
    "S03": "B. Beschreibung §10-17: Seitenvorgelege, Laufwerk, Gestänge, Elektrik, Schalttafel, Werkzeug, Hilfsgerät, Schanzzeug",
    "S04": "C. Schmieren §18-19 + D. Aus-/Einbau §20-24 (Anfang)",
    "S05": "D. Aus-/Einbau §24 (Forts.)-28",
    "S06": "E. Sondervorschriften §29-30 + F. Fahrvorschrift §31-32",
}


def main() -> None:
    page_map = json.loads((ROOT / "page_map.json").read_text(encoding="utf-8"))
    pages = page_map["pages"]

    first_page_of_section: dict[str, int] = {}
    for entry in pages:
        first_page_of_section.setdefault(entry["section"], entry["page"])

    text_sections = []
    for section_id, title_de in TEXT_TITLES.items():
        manifest_ref = (
            "../frontmatter/manifest.json"
            if section_id == "FrontMatter"
            else f"../sections/{section_id}/manifest.json"
        )
        text_sections.append(
            {
                "id": section_id,
                "page": first_page_of_section[section_id],
                "titles": {"de": title_de, "en-GB": None, "es-ES": None},
                "manifest": manifest_ref,
            }
        )

    plates = []
    for entry in pages:
        if entry["kind"] != "plate":
            continue
        for bild_number in entry["bild_numbers"]:
            plates.append(
                {
                    "bild": bild_number,
                    "page": entry["page"],
                    "titles": {"de": f"Bild {bild_number}  {entry['title_de']}", "en-GB": None, "es-ES": None},
                    "rotated": entry["rotated"],
                    "manifest": f"../sections/G/pages/{entry['page']:03d}/manifest.json",
                }
            )
    plates.sort(key=lambda p: p["bild"])

    contents = {
        "schema_version": 1,
        "groups": [
            {
                "id": "TEXT",
                "titles": {"de": "Text (Titelseite bis Fahrvorschrift)", "en-GB": None, "es-ES": None},
                "sections": text_sections,
            },
            {
                "id": "G",
                "titles": {"de": "G. Bilder", "en-GB": "G. Plates", "es-ES": "G. Láminas"},
                "plates": plates,
            },
        ],
    }

    out = ROOT / "index" / "contents.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(contents, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
