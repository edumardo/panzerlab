"""Build the global manifest, section manifests, page manifests and
content.json stubs for D.652-41a from page_map.json.

Idempotent: safe to re-run. It will NOT downgrade a page manifest's
workflow-state fields if they have already been advanced past "pending" by
later transcription/translation work -- it only fills in provenance fields
(page/section/pdf_page/side/figures) and creates missing files. Delete a
specific page's manifest.json/content.json first if you want this script to
fully regenerate it.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS_DIR = ROOT / "sections"
FRONTMATTER_DIR = ROOT / "frontmatter"


def section_base_dir(section_id: str) -> Path:
    return FRONTMATTER_DIR if section_id == "FrontMatter" else SECTIONS_DIR / section_id

DOCUMENT_ID = "d652-41a"
DOCUMENT_ID_COMPACT = DOCUMENT_ID.replace("-", "")

# Section id -> (titles, layout). Landscape plates keep their own layout
# value since -- unlike D.652-50c's portrait pages -- a plate here is a
# whole landscape sheet that crosses the gutter and must never be split.
SECTION_META = {
    "FrontMatter": {
        "titles": {
            "de": "Titelseite, Inhalt, Vorbemerkungen, A. Technische Angaben, B. Beschreibung §1-2",
            "en-GB": None,
            "es-ES": None,
        },
        "layout": "A4_portrait_facsimile_then_translation",
    },
    "S01": {
        "titles": {
            "de": "B. Beschreibung §3-4: Panzerwanne, Motor",
            "en-GB": None,
            "es-ES": None,
        },
        "layout": "A4_portrait_facsimile_then_translation",
    },
    "S02": {
        "titles": {
            "de": "B. Beschreibung §5-9: Hauptkupplung, Wechselgetriebe, Kegel-/Lenkgetriebe, Stütz-/Lenkbremse, Kraftübertragung",
            "en-GB": None,
            "es-ES": None,
        },
        "layout": "A4_portrait_facsimile_then_translation",
    },
    "S03": {
        "titles": {
            "de": "B. Beschreibung §10-17: Seitenvorgelege, Laufwerk, Gestänge, Elektrik, Schalttafel, Werkzeug, Hilfsgerät, Schanzzeug",
            "en-GB": None,
            "es-ES": None,
        },
        "layout": "A4_portrait_facsimile_then_translation",
    },
    "S04": {
        "titles": {
            "de": "C. Schmieren §18-19 + D. Aus-/Einbau §20-24 (Anfang)",
            "en-GB": None,
            "es-ES": None,
        },
        "layout": "A4_portrait_facsimile_then_translation",
    },
    "S05": {
        "titles": {
            "de": "D. Aus-/Einbau §24 (Forts.)-28",
            "en-GB": None,
            "es-ES": None,
        },
        "layout": "A4_portrait_facsimile_then_translation",
    },
    "S06": {
        "titles": {
            "de": "E. Sondervorschriften §29-30 + F. Fahrvorschrift §31-32",
            "en-GB": None,
            "es-ES": None,
        },
        "layout": "A4_portrait_facsimile_then_translation",
    },
    "G": {
        "titles": {
            "de": "G. Bilder",
            "en-GB": "G. Plates",
            "es-ES": "G. Láminas",
        },
        "layout": "A4_landscape_facsimile_then_translation",
    },
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def page_type(entry: dict) -> str:
    if entry["kind"] == "cover":
        return "text"
    if entry["kind"] == "blank":
        return "blank"
    if entry["kind"] == "divider":
        return "index"
    if entry["kind"] == "plate":
        return "figures"
    return "text"


def build_page_manifest(entry: dict, existing: dict | None) -> dict:
    manifest = existing.copy() if existing else {}
    manifest["page"] = entry["page"]
    manifest["section"] = entry["section"]
    manifest["pdf_page"] = entry["pdf_page"]
    manifest["side"] = entry["side"]
    manifest["source_scan"] = "source.jpg"
    manifest["content"] = "content.json"
    manifest.setdefault("source_scan_status", "extracted_clean")
    manifest.setdefault("transcription_status", "pending")
    manifest.setdefault("translation_en_status", "pending")
    manifest.setdefault("translation_es_status", "pending")
    if entry["kind"] == "plate":
        manifest["figures"] = [
            existing_fig if existing_fig else {"number": n, "status": "pending"}
            for n, existing_fig in zip(
                entry["bild_numbers"],
                (manifest.get("figures") or [None] * len(entry["bild_numbers"])),
            )
        ]
    else:
        manifest.setdefault("figures", [])
    return manifest


def build_content_stub(entry: dict, document_id: str, existing: dict | None) -> dict:
    content = existing.copy() if existing else {}
    compact_id = document_id.replace("-", "")
    page_id = f"{compact_id}-page-{entry['page']:03d}"
    content["schema_version"] = 1
    content["id"] = page_id
    content["document_id"] = document_id
    content["page"] = entry["page"]
    content["section"] = entry["section"]
    content.setdefault("type", page_type(entry))
    content.setdefault("titles", {"de": entry.get("title_de"), "en-GB": None, "es-ES": None})
    content["source"] = {
        "image": "source.jpg",
        "pdf_page": entry["pdf_page"],
        "side": entry["side"],
        "status": content.get("source", {}).get("status", "extracted_clean"),
    }
    content.setdefault("paragraphs", [])
    if entry["kind"] == "plate" and not content.get("figures"):
        content["figures"] = [
            {
                "id": f"{compact_id}-bild{n:03d}",
                "number": n,
                "captions": {"de": None, "en-GB": None, "es-ES": None},
                "label_keys": {"de": None, "en-GB": None, "es-ES": None},
            }
            for n in entry["bild_numbers"]
        ]
    else:
        content.setdefault("figures", [])
    content.setdefault(
        "status",
        {
            "transcription": "pending",
            "en-GB": "pending",
            "es-ES": "pending",
            "figures": "not_applicable" if entry["kind"] != "plate" else "pending",
        },
    )
    return content


def main() -> None:
    page_map = json.loads((ROOT / "page_map.json").read_text(encoding="utf-8"))
    pages = page_map["pages"]

    # Section manifests
    section_pages: dict[str, list[int]] = {}
    for entry in pages:
        section_pages.setdefault(entry["section"], []).append(entry["page"])

    for section_id, page_numbers in section_pages.items():
        meta = SECTION_META[section_id]
        manifest_path = section_base_dir(section_id) / "manifest.json"
        write_json(
            manifest_path,
            {
                "id": section_id,
                "pages": page_numbers,
                "titles": meta["titles"],
                "output": {"cover": False, "header": False, "footer": False},
                "layout": meta["layout"],
            },
        )

    # Page manifests + content.json, with previous/next navigation in
    # document-wide page order.
    for index, entry in enumerate(pages):
        page_dir = section_base_dir(entry["section"]) / "pages" / f"{entry['page']:03d}"
        page_manifest_path = page_dir / "manifest.json"
        content_path = page_dir / "content.json"

        page_manifest = build_page_manifest(entry, load_json(page_manifest_path))
        write_json(page_manifest_path, page_manifest)

        content = build_content_stub(entry, DOCUMENT_ID, load_json(content_path))
        previous_entry = pages[index - 1] if index > 0 else None
        next_entry = pages[index + 1] if index < len(pages) - 1 else None
        content["navigation"] = {
            "previous": f"{DOCUMENT_ID_COMPACT}-page-{previous_entry['page']:03d}" if previous_entry else None,
            "next": f"{DOCUMENT_ID_COMPACT}-page-{next_entry['page']:03d}" if next_entry else None,
        }
        write_json(content_path, content)

    # Global manifest
    write_json(
        ROOT / "manifest.json",
        {
            "document_id": DOCUMENT_ID,
            "source_pdf_pages": page_map["source_pdf_pages"],
            "book_pages": [1, len(pages)],
            "sections": {
                section_id: [min(nums), max(nums)] for section_id, nums in section_pages.items()
            },
            "pages": [
                {
                    "page": entry["page"],
                    "section": entry["section"],
                    "pdf_page": entry["pdf_page"],
                    "side": entry["side"],
                    "content": "content.json",
                }
                for entry in pages
            ],
        },
    )

    print(f"Wrote global manifest, {len(section_pages)} section manifests, {len(pages)} page manifests/content stubs")


if __name__ == "__main__":
    main()
